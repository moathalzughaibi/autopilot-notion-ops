#!/usr/bin/env python3
import os, json, csv, ndjson, argparse, datetime
from notion_client import Client

ENC="utf-8-sig"
SECTIONS = {
  "Schemas": ["FeatureSchemaV1","FeatureSchemaH1","FamilyMap"],
  "Catalogs": ["UniverseP2","CatalogL1","CatalogL2L3"],
  "Policy Matrix": ["PolicyMatrix"],
  "Telemetry": ["QCWeekly"],
  "Calendars": ["CalendarGaps2025"]
}
EMOJI = {"Schemas":"","Catalogs":"","Policy Matrix":"","Telemetry":"","Calendars":""}

def load_cfg(p): return json.load(open(p,"r",encoding=ENC))

def csv_count(path):
    with open(path, newline="", encoding=ENC) as f:
        r=csv.reader(f); next(r,None); return sum(1 for _ in r)

def ndjson_count(path):
    with open(path, "r", encoding="utf-8") as f:
        return sum(1 for _ in ndjson.reader(f))

def json_events_count(path):
    data=json.load(open(path,"r",encoding=ENC))
    if isinstance(data,list): return len(data)
    for k in ("events","gaps","items","data"):
        v=data.get(k)
        if isinstance(v,list): return len(v)
    return 0

def count_rows(info):
    path=info["path"].replace("\\","/")
    if path.endswith(".csv"): return csv_count(path)
    if path.endswith(".ndjson"): return ndjson_count(path)
    if "calendar_gaps" in path and path.endswith(".json"): return json_events_count(path)
    return None

def find_or_create_page(notion, root_id, title):
    res = notion.search(query=title, filter={"value":"page","property":"object"})
    for obj in res.get("results",[]):
        if obj.get("object")=="page" and obj["properties"]["title"]["title"][0]["plain_text"]==title:
            return obj["id"]
    page = notion.pages.create(parent={"type":"page_id","page_id":root_id},
                               properties={"title":{"title":[{"type":"text","text":{"content":title}}]}})
    return page["id"]

def list_child_blocks(notion, page_id):
    kids=[]; cursor=None
    while True:
        resp = notion.blocks.children.list(block_id=page_id, start_cursor=cursor) if cursor else notion.blocks.children.list(block_id=page_id)
        kids.extend([b["id"] for b in resp.get("results",[])])
        cursor = resp.get("next_cursor")
        if not resp.get("has_more"): break
    return kids

def clear_children(notion, page_id):
    for bid in list_child_blocks(notion, page_id):
        notion.blocks.delete(block_id=bid)

def callout(text, emoji="ℹ"):
    return {"object":"block","type":"callout","callout":{"icon":{"type":"emoji","emoji":emoji},"rich_text":[{"type":"text","text":{"content":text}}]}}

def para(text):
    return {"object":"block","type":"paragraph","paragraph":{"rich_text":[{"type":"text","text":{"content":text}}]}}

def link_db(db_id, caption):
    return {"object":"block","type":"link_to_page","link_to_page":{"type":"database_id","database_id":db_id}}

def heading(text):
    return {"object":"block","type":"heading_2","heading_2":{"rich_text":[{"type":"text","text":{"content":text}}]}}

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--config", default="IFNS_Notion_DB_Buildout_V2/config/ifns_v2_db_map.json")
    ap.add_argument("--root_title", default="IFNS  UI Master (V2)")
    args=ap.parse_args()

    token=os.environ.get("NOTION_TOKEN"); root=os.environ.get("NOTION_ROOT_PAGE_ID")
    if not token: raise SystemExit("NOTION_TOKEN not set")
    notion=Client(auth=token)

    # resolve root if no explicit ID
    if not root:
        res = notion.search(query=args.root_title, filter={"value":"page","property":"object"})
        root = next((o["id"] for o in res.get("results",[]) if o.get("object")=="page"), None)
        if not root: raise SystemExit("Could not locate V2 root page")

    cfg=load_cfg(args.config)
    dbs=cfg["databases"]
    page_id = find_or_create_page(notion, root, "Operator Home")

    # rebuild content
    clear_children(notion, page_id)
    ts=datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

    intro = [
      callout("Welcome. This is your operator entry point. All data below is synced from Git (file-first).", ""),
      para(f"Last refresh: {ts}")
    ]
    notion.blocks.children.append(block_id=page_id, children=intro)

    for section, keys in SECTIONS.items():
        blocks=[heading(f"{EMOJI.get(section,'')} {section}")]
        for k in keys:
            info = dbs.get(k); 
            if not info: continue
            db_id = info.get("database_id")
            src = info.get("path","")
            pk = info.get("primary_key","")
            rows = count_rows(info)
            desc = f"{k}  source: {src}" + (f" | pk: {pk}" if pk else "") + (f" | rows: {rows}" if rows is not None else "")
            blocks.append(callout(desc, ""))
            if db_id: blocks.append(link_db(db_id, k))
        notion.blocks.children.append(block_id=page_id, children=blocks)

    print("Operator Home updated.")
if __name__=="__main__": main()
