#!/usr/bin/env python3
import os, sys, json, argparse, datetime
def append(path, line):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    if os.path.exists(path) and line.strip() in open(path,"r",encoding="utf-8-sig").read(): return
    with open(path,"a",encoding="utf-8-sig") as f: f.write(line)

def main():
    import argparse, json, datetime
    ap=argparse.ArgumentParser()
    ap.add_argument("--config", default="config/ifns_v2_db_map.json")
    a=ap.parse_args()
    cfg=json.load(open(a.config,"r",encoding="utf-8-sig"))
    ts=datetime.datetime.now(datetime.timezone.utc).isoformat()+"Z"
    idx="docs/IFNS_Notion_Page_Index.md"; log="docs/IFNS_Troubleshooting_Log.md"
    append(idx, f"\n## Notion DB build-out snapshot ({ts})\n")
    for k,info in cfg["databases"].items():
        append(idx, f"- **{k}**  `{info.get('path','')}` (pk: `{info.get('primary_key','')}`)  DB: `{info.get('database_id','')}`\n")
    append(log, f"\n### {ts}  DB build-out scripts executed\n- Scripts: create_dbs, sync_generic, sync_qc_weekly, wire_pages\n- Notes: file-first, idempotent upserts by primary key.\n")
    print("Local docs updated.")
if __name__=="__main__": main()


