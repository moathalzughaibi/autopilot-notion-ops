#!/usr/bin/env python3
import os, sys, json, argparse, csv
from notion_client import Client

def load_cfg(p): return json.load(open(p,"r",encoding="utf-8-sig"))
def tstr(s): return [{"type":"text","text":{"content":str(s)[:2000]}}] if s not in (None,"") else []
def as_val(t, v):
    if t=="title":    return {"title": tstr(v)}
    if t=="rich_text":return {"rich_text": tstr(v)}
    if t=="number":
        try: return {"number": float(v)}
        except: return {"number": None}
    if t=="checkbox": return {"checkbox": str(v).lower()=="true"}
    if t=="url":      return {"url": str(v) if v else None}
    if t=="date":     return {"date": {"start": str(v)}} if v else {"date": None}
    if t=="multi_select":
        items=[x.strip() for x in str(v).replace(";",",").split(",") if x.strip()]
        return {"multi_select":[{"name":i} for i in items]}
    return {"rich_text": tstr(v)}

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--config", default="config/ifns_v2_db_map.json")
    ap.add_argument("--key", required=True)
    a=ap.parse_args()

    token=os.environ.get("NOTION_TOKEN")
    if not token: print("ERROR: NOTION_TOKEN not set"); sys.exit(1)
    notion=Client(auth=token)

    cfg=load_cfg(a.config); db_cfg=cfg["databases"][a.key]
    db_id=db_cfg["database_id"]; path=db_cfg["path"]; pk=db_cfg.get("primary_key") or ""

    db=notion.databases.retrieve(database_id=db_id); ptypes={n:spec.get("type") for n,spec in db.get("properties",{}).items()}

    created=updated=0
    with open(path, newline="", encoding="utf-8-sig") as f:
      for row in csv.DictReader(f):
        props={c:as_val(ptypes.get(c,"rich_text"), v) for c,v in row.items()}
        page_id=None
        if pk and row.get(pk):
          try:
            filt_type=ptypes.get(pk,"rich_text")
            res=notion.databases.query(database_id=db_id, filter={"property":pk, filt_type:{"equals": row[pk]}}, page_size=1)
            if res.get("results"): page_id=res["results"][0]["id"]
          except Exception as e:
            print("WARN: query fail, creating:", e)
        try:
          if page_id: notion.pages.update(page_id=page_id, properties=props); updated+=1
          else:       notion.pages.create(parent={"database_id":db_id}, properties=props); created+=1
        except Exception as e:
          print("ERROR row:", row, "err:", e)
    print(f"Sync {a.key}: created={created}, updated={updated}")

if __name__=="__main__": main()



