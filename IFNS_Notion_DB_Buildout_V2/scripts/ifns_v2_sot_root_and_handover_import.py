#!/usr/bin/env python3
import os, argparse, pathlib
from notion_client import Client

ENC="utf-8-sig"

def find_page_by_title(notion, title):
    r = notion.search(query=title, filter={"value":"page","property":"object"})
    for o in r.get("results", []):
        if o.get("object")=="page" and o["properties"]["title"]["title"]:
            if o["properties"]["title"]["title"][0]["plain_text"] == title:
                return o["id"]
    return None

def find_or_create_page(notion, parent_id, title):
    pid = find_page_by_title(notion, title)
    if pid: return pid
    p = notion.pages.create(parent={"type":"page_id","page_id":parent_id},
                            properties={"title":{"title":[{"type":"text","text":{"content":title}}]}})
    return p["id"]

def chunk_text(s, maxlen=1800):
    return [s[i:i+maxlen] for i in range(0, len(s), maxlen)]

def code_block(txt, lang="markdown"):
    return {"object":"block","type":"code","code":{"language":lang,"rich_text":[{"type":"text","text":{"content":txt}}]}}

def paragraph(txt):
    return {"object":"block","type":"paragraph","paragraph":{"rich_text":[{"type":"text","text":{"content":txt}}]}}

def link_to_page(notion, title):
    pid = find_page_by_title(notion, title)
    if not pid: return None
    return {"object":"block","type":"link_to_page","link_to_page":{"type":"page_id","page_id":pid}}

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--handover_dir", required=True)
    ap.add_argument("--crosswalk", required=True)
    ap.add_argument("--v1_title", default="IFNS  UI Master")
    ap.add_argument("--v2_title", default="IFNS  UI Master (V2)")
    ap.add_argument("--sot_title", default="IFNS  UI Master (SoT)")
    args = ap.parse_args()

    token = os.environ.get("NOTION_TOKEN")
    root_id = os.environ.get("NOTION_ROOT_PAGE_ID")
    if not token or not root_id:
        raise SystemExit("NOTION_TOKEN / NOTION_ROOT_PAGE_ID missing")
    notion = Client(auth=token)

    # SoT root
    sot = find_or_create_page(notion, root_id, args.sot_title)

    # Intro + links to V1/V2
    links = []
    for t in (args.v2_title, args.v1_title):
        b = link_to_page(notion, t)
        if b: links.append(b)
    intro = [paragraph("Source of Truth working root. Handover phases below; V2 Operational and V1 Historical linked above.")]
    notion.blocks.children.append(block_id=sot, children=intro + links)

    # Handover section
    handover_page = find_or_create_page(notion, sot, "Handover (Phases 05)")

    # Import .md files as code blocks (preserves formatting)
    hd = pathlib.Path(args.handover_dir)
    for md in sorted(hd.glob("*.md")):
        child = notion.pages.create(parent={"type":"page_id","page_id":handover_page},
                                    properties={"title":{"title":[{"type":"text","text":{"content":md.name}}]}})
        text = md.read_text(encoding=ENC, errors="replace")
        blocks = [code_block(t) for t in chunk_text(text)]
        notion.blocks.children.append(block_id=child["id"], children=blocks)

    # Crosswalk page
    cw_parent = find_or_create_page(notion, sot, "Crosswalks")
    cw_child = notion.pages.create(parent={"type":"page_id","page_id":cw_parent},
                                   properties={"title":{"title":[{"type":"text","text":{"content":pathlib.Path(args.crosswalk).name}}]}})
    ctext = pathlib.Path(args.crosswalk).read_text(encoding=ENC, errors="replace")
    blocks = [code_block(t) for t in chunk_text(ctext)]
    notion.blocks.children.append(block_id=cw_child["id"], children=blocks)

    print("SoT root created and handover docs imported.")
if __name__=="__main__": main()
