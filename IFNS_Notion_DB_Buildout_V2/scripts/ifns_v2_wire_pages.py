#!/usr/bin/env python3
import os, sys, json, argparse
from notion_client import Client

SECTIONS = {
  "Manifests & Policy": ["FeatureSchemaV1","FeatureSchemaH1","PolicyMatrix","FamilyMap","UniverseP2","CatalogL1","CatalogL2L3"],
  "Telemetry & QC": ["QCWeekly"],
  "Runtime Templates & Calendars": ["CalendarGaps2025"]
}

def find_page(notion, title):
    r=notion.search(query=title, filter={"value":"page","property":"object"})
    for obj in r.get("results",[]): 
        if obj.get("object")=="page": return obj["id"]
    return None

def append_link(notion, page_id, db_id, caption):
    notion.blocks.children.append(block_id=page_id, children=[
      {"object":"block","type":"paragraph","paragraph":{"rich_text":[{"type":"text","text":{"content":caption}}]}},
      {"object":"block","type":"link_to_page","link_to_page":{"type":"database_id","database_id":db_id}}
    ])

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    ap.add_argument("--config", default="config/ifns_v2_db_map.json")
    a=ap.parse_args()

    token=os.environ.get("NOTION_TOKEN"); root=os.environ.get("NOTION_ROOT_PAGE_ID")
    if not token or not root: print("ERROR: NOTION_TOKEN/NOTION_ROOT_PAGE_ID missing"); sys.exit(1)
    notion=Client(auth=token)

    cfg=json.load(open(a.config,"r",encoding="utf-8-sig"))
    for section, keys in SECTIONS.items():
        sp = find_page(notion, section) or root
        for k in keys:
            db_id = cfg["databases"].get(k,{}).get("database_id")
            if db_id: append_link(notion, sp, db_id, f"{k}  linked database")
    print("Wiring complete.")
if __name__=="__main__": main()

