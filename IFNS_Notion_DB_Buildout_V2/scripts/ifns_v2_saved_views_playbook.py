#!/usr/bin/env python3
import os, json, argparse, pathlib
from notion_client import Client

ENC="utf-8-sig"
PLAYBOOK_TITLE="Saved Views Playbook"

VIEW_TIPS = {
  "FeatureSchemaV1": [
    "Group by **family**; sort by **feature_name** (AZ).",
    "Filter: **status != deprecated**.",
    "Add columns: **dtype**, **bins**, **range_hint**."
  ],
  "FeatureSchemaH1": [
    "Same as V1; add filter **tf = H1** if present.",
    "Group by **family**, then **usage**."
  ],
  "FamilyMap": [
    "Sort by **family** then **feature_name**.",
    "Use quick-find for a family to scan its members."
  ],
  "PolicyMatrix": [
    "Group by **risk_bucket**; then by **usage**.",
    "Filter: **enforced = true** to see active constraints."
  ],
  "UniverseP2": [
    "Group by **market**; filter **active = true**.",
    "Add a view for Top symbols if rank/weight exists."
  ],
  "CatalogL1": [
    "Group by **family**; filter **adoption_status != deprecated**.",
    "Sort by **indicator_id**; show **inputs**, **window**, **params**."
  ],
  "CatalogL2L3": [
    "Group by **layer** (L2 vs L3), then **family**.",
    "Filter **enabled = true**; show **composite_id**, **components**."
  ],
  "QCWeekly": [
    "Group by **severity**; sort by **ts** desc.",
    "Filter **is_breach = true**."
  ],
  "CalendarGaps2025": [
    "Sort by **date** asc.",
    "Group by **market**; filter **reason contains Holiday**."
  ]
}

def load_cfg(p): return json.load(open(p,"r",encoding=ENC))

def find_root(notion, title):
    r=notion.search(query=title, filter={"value":"page","property":"object"})
    for o in r.get("results",[]):
        if o.get("object")=="page" and o["properties"]["title"]["title"]:
            if o["properties"]["title"]["title"][0]["plain_text"]==title:
                return o["id"]

def find_or_create_page(notion, parent_id, title):
    r=notion.search(query=title, filter={"value":"page","property":"object"})
    for o in r.get("results",[]):
        if o.get("object")=="page" and o["properties"]["title"]["title"]:
            if o["properties"]["title"]["title"][0]["plain_text"]==title:
                return o["id"]
    p=notion.pages.create(parent={"type":"page_id","page_id":parent_id},
                          properties={"title":{"title":[{"type":"text","text":{"content":title}}]}})
    return p["id"]

def clear_children(notion, page_id):
    cur=None
    while True:
        resp = notion.blocks.children.list(block_id=page_id, start_cursor=cur) if cur \
               else notion.blocks.children.list(block_id=page_id)
        for b in resp.get("results",[]): notion.blocks.delete(block_id=b["id"])
        cur = resp.get("next_cursor")
        if not resp.get("has_more"): break

def to_paragraph(text):
    return {"object":"block","type":"paragraph","paragraph":{"rich_text":[{"type":"text","text":{"content":text}}]}}

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--config", default="IFNS_Notion_DB_Buildout_V2/config/ifns_v2_db_map.json")
    ap.add_argument("--root_title", default="IFNS  UI Master (V2)")
    args=ap.parse_args()

    token=os.environ.get("NOTION_TOKEN"); root=os.environ.get("NOTION_ROOT_PAGE_ID")
    if not token: raise SystemExit("NOTION_TOKEN not set")
    notion=Client(auth=token)

    if not root:
        root=find_root(notion, args.root_title)
        if not root: raise SystemExit("V2 root not found")

    # write .md copies (file-first tips)
    outdir=pathlib.Path("docs/ifns/saved_views"); outdir.mkdir(parents=True, exist_ok=True)
    for key, tips in VIEW_TIPS.items():
        (outdir / f"{key}_views.md").write_text("# "+key+"  Saved Views\n\n"+"\n".join(f"- {t}" for t in tips)+"\n", encoding="utf-8")

    # Notion playbook page (plain paragraphs, no emojis)
    playbook_page = find_or_create_page(notion, root, PLAYBOOK_TITLE)
    clear_children(notion, playbook_page)
    notion.blocks.children.append(block_id=playbook_page,
        children=[to_paragraph("Saved Views you can add in seconds. Data stays synced from Git; views are operator-defined.")])

    for key, tips in VIEW_TIPS.items():
        child = notion.pages.create(parent={"type":"page_id","page_id":playbook_page},
                                    properties={"title":{"title":[{"type":"text","text":{"content":f"{key} Views"}}]}})
        blocks=[to_paragraph(f"- {t}") for t in tips]
        notion.blocks.children.append(block_id=child["id"], children=blocks)

    print("Saved Views Playbook updated (files + Notion).")

if __name__=="__main__": main()
