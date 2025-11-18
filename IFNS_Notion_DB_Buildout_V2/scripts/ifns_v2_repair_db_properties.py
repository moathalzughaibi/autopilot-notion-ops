#!/usr/bin/env python3
import os, sys, json, csv, argparse
from notion_client import Client

def load_cfg(p): return json.load(open(p,"r",encoding="utf-8-sig"))
def csv_headers(path):
    with open(path, newline="", encoding="utf-8-sig") as f:
        r=csv.DictReader(f)
        return r.fieldnames or []

def prop_def(name, is_title=False):
    return {name: ({"title":{}} if is_title else {"rich_text":{}})}

def ensure_props(notion, db_id, headers):
    db = notion.databases.retrieve(database_id=db_id)
    existing = set(db.get("properties",{}).keys())
    to_add = [h for h in headers if h not in existing]
    if not to_add: 
        print(f"No missing props for {db_id}"); 
        return
    has_title = any(v.get("type")=="title" for v in db.get("properties",{}).values())
    props={}
    for i,h in enumerate(to_add):
        props.update(prop_def(h, is_title=(not has_title and i==0)))
    notion.databases.update(database_id=db_id, properties=props)
    print(f"Added {len(to_add)} properties  {db_id}")

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--config", required=True)
    ap.add_argument("--keys", nargs="+", required=True)
    a=ap.parse_args()
    token=os.environ.get("NOTION_TOKEN")
    if not token: print("ERROR: NOTION_TOKEN not set"); sys.exit(1)
    notion=Client(auth=token)
    cfg=load_cfg(a.config)
    for k in a.keys:
        db_cfg = cfg["databases"][k]
        path = db_cfg["path"]; db_id = db_cfg["database_id"]
        if not db_id: 
            print(f"Skip {k}: no database_id"); continue
        ensure_props(notion, db_id, csv_headers(path))
if __name__=="__main__": main()
