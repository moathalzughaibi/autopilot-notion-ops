#!/usr/bin/env python3
import os, sys, json, argparse, hashlib
from notion_client import Client

def load_cfg(p): 
    return json.load(open(p, "r", encoding="utf-8-sig"))

def to_list(data):
    if isinstance(data, list): return data
    if isinstance(data, dict) and "events" in data and isinstance(data["events"], list): return data["events"]
    return []

def infer_fields(rows):
    keys = set()
    for r in rows:
        keys.update(r.keys())
    return list(keys)

def notion_type_from_value(v):
    if isinstance(v, bool): return "checkbox"
    if isinstance(v, (int, float)): return "number"
    if isinstance(v, list): return "multi_select"
    if isinstance(v, str) and v.startswith("http"): return "url"
    if isinstance(v, str) and ("T" in v and ":" in v): return "date"  # naive ISO guess
    return "rich_text"

def as_prop(nt, val):
    if nt=="title": return {"title":[{"type":"text","text":{"content":str(val)[:2000]}}]}
    if nt=="number":
        try: return {"number": float(val)}
        except: return {"number": None}
    if nt=="checkbox": return {"checkbox": bool(val)}
    if nt=="date": return {"date":{"start":str(val)}} if val else {"date": None}
    if nt=="multi_select":
        items = val if isinstance(val, list) else []
        return {"multi_select":[{"name":str(x)} for x in items]}
    if nt=="url": return {"url": str(val) if val else None}
    return {"rich_text":[{"type":"text","text":{"content":str(val)[:2000]}}]}

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default="config/ifns_v2_db_map.json")
    a = ap.parse_args()

    token = os.environ.get("NOTION_TOKEN"); root_id = os.environ.get("NOTION_ROOT_PAGE_ID")
    if not token or not root_id:
        print("ERROR: NOTION_TOKEN/NOTION_ROOT_PAGE_ID missing"); sys.exit(1)
    notion = Client(auth=token)

    cfg = load_cfg(a.config)
    db_cfg = cfg["databases"]["CalendarGaps2025"]
    path = db_cfg["path"]

    data = json.load(open(path, "r", encoding="utf-8-sig"))
    rows = to_list(data)
    if not rows:
        print("No events found in", path); sys.exit(0)

    # Choose primary key
    sample = rows[0]
    pk = "event_id" if "event_id" in sample else ("id" if "id" in sample else "event_key")

    # Ensure DB exists
    db_id = db_cfg.get("database_id") or ""
    if not db_id:
        # build props
        fields = infer_fields(rows)
        props = {}
        title_set = False
        for f in fields:
            if not title_set and f in ("event_id","id","title","summary","name"):
                props[f] = {"title":{}}
                title_set = True
            else:
                val = sample.get(f)
                nt = notion_type_from_value(val)
                if nt == "date" and f not in ("start","end","date","start_date","end_date"):
                    nt = "rich_text"
                props[f] = {nt:{}}
        if not title_set:
            props["event_key"] = {"title":{}}
        db = notion.databases.create(parent={"type":"page_id","page_id":root_id},
                                     title=[{"type":"text","text":{"content":"CalendarGaps2025"}}],
                                     properties=props)
        db_id = db["id"]
        cfg["databases"]["CalendarGaps2025"]["database_id"] = db_id
        cfg["databases"]["CalendarGaps2025"]["primary_key"] = pk
        json.dump(cfg, open(a.config,"w",encoding="utf-8"), indent=2)

    # Map property types
    db = notion.databases.retrieve(database_id=db_id)
    ptypes = {name: spec.get("type") for name, spec in db.get("properties",{}).items()}
    if pk not in ptypes and "event_key" in ptypes:
        pk = "event_key"

    def key_for(r):
        if pk in r: return str(r[pk])
        s = json.dumps(r, sort_keys=True)
        return hashlib.sha1(s.encode("utf-8")).hexdigest()

    for r in rows:
        rid = key_for(r)
        props = {}
        # ensure pk exists for title
        r_out = dict(r)
        if pk == "event_key" and "event_key" not in r_out:
            r_out["event_key"] = rid
        for k, v in r_out.items():
            nt = "title" if k == pk and ptypes.get(k) == "title" else ptypes.get(k, "rich_text")
            props[k] = as_prop(nt, v)

        # upsert by pk
        filter_key_type = ptypes.get(pk, "rich_text")
        res = notion.databases.query(database_id=db_id, filter={"property": pk, ( "title" if filter_key_type=="title" else filter_key_type): {"equals": str(rid)}}, page_size=1)
        if res.get("results"):
            notion.pages.update(page_id=res["results"][0]["id"], properties=props)
        else:
            notion.pages.create(parent={"database_id": db_id}, properties=props)

    print("Calendar gaps synced.")
if __name__=="__main__": main()
