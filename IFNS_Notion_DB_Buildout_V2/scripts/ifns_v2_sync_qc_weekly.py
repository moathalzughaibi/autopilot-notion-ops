#!/usr/bin/env python3
import os, sys, json, argparse, ndjson, hashlib
from notion_client import Client

ENC = "utf-8-sig"

def load_cfg(p):
    return json.load(open(p, "r", encoding=ENC))

def derive_fields(schema, example_path):
    if isinstance(schema, dict) and "properties" in schema:
        return {k: v.get("type","string") for k,v in schema["properties"].items()}
    if isinstance(schema, dict) and isinstance(schema.get("fields"), list):
        return {f["name"]: f.get("type","string") for f in schema["fields"] if isinstance(f, dict) and "name" in f}
    if isinstance(schema, list):
        return {f["name"]: f.get("type","string") for f in schema if isinstance(f, dict) and "name" in f}
    fields = {}
    with open(example_path, "r", encoding="utf-8") as f:
        for i, rec in enumerate(ndjson.reader(f)):
            for k, v in rec.items():
                if k not in fields:
                    fields[k] = ("number" if isinstance(v,(int,float)) else
                                 "boolean" if isinstance(v,bool) else
                                 "array" if isinstance(v,list) else "string")
            if i >= 50: break
    return fields

def notion_type(t):
    return {"string":"rich_text","number":"number","integer":"number","boolean":"checkbox","array":"multi_select"}.get(t,"rich_text")

def ensure_pk_property(notion, db_id, pk="entry_id"):
    db = notion.databases.retrieve(database_id=db_id)
    if pk in db.get("properties", {}): return
    notion.databases.update(database_id=db_id, properties={pk: {"rich_text": {}}})

def sanitize_option(x: object) -> str:
    s = str(x).strip()
    # Notion forbids commas in multi_select option names
    s = s.replace(",", "")
    # keep options short & readable
    return (s[:90] if len(s) > 90 else s) or ""

def as_prop(ptype, val):
    if ptype=="title":
        return {"title":[{"type":"text","text":{"content":str(val)[:2000]}}]}
    if ptype=="number":
        try: return {"number": float(val)}
        except: return {"number": None}
    if ptype=="checkbox":
        return {"checkbox": bool(val)}
    if ptype=="multi_select":
        items = []
        if isinstance(val, list):
            items = [sanitize_option(v) for v in val if v is not None]
        elif isinstance(val, dict):
            items = [sanitize_option(f"{k}={v}") for k,v in val.items()]
        elif isinstance(val, str):
            # split comma-separated strings into options
            items = [sanitize_option(part) for part in val.split(",") if part.strip()]
        # dedupe while preserving order
        seen=set(); clean=[]
        for it in items:
            if it not in seen:
                seen.add(it); clean.append(it)
        return {"multi_select":[{"name":it} for it in clean]}
    if ptype=="url":
        return {"url": str(val) if val else None}
    if ptype=="date":
        return {"date":{"start":str(val)}} if val else {"date": None}
    return {"rich_text":[{"type":"text","text":{"content":str(val)[:2000]}}]}

def build_equals_filter(prop_name, prop_type, value):
    if prop_type=="number":
        try: v = float(value)
        except: v = None
        return {"property": prop_name, "number": {"equals": v}}
    if prop_type=="checkbox":
        return {"property": prop_name, "checkbox": {"equals": bool(value)}}
    if prop_type=="title":
        return {"property": prop_name, "title": {"equals": str(value)}}
    if prop_type=="rich_text":
        return {"property": prop_name, "rich_text": {"equals": str(value)}}
    if prop_type=="url":
        return {"property": prop_name, "url": {"equals": str(value)}}
    if prop_type=="date":
        return {"property": prop_name, "date": {"equals": str(value)}}
    # multi_select has no equals filter  create-only fallback
    return None

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default="config/ifns_v2_db_map.json")
    a = ap.parse_args()

    token = os.environ.get("NOTION_TOKEN"); root_id = os.environ.get("NOTION_ROOT_PAGE_ID")
    if not token or not root_id:
        print("ERROR: NOTION_TOKEN/NOTION_ROOT_PAGE_ID missing"); sys.exit(1)
    notion = Client(auth=token)

    cfg = load_cfg(a.config)
    db_cfg = cfg["databases"]["QCWeekly"]
    schema_path = db_cfg["path"]
    example_path = "sync/ifns/qc_weekly_example_v1.ndjson"

    schema = json.load(open(schema_path, "r", encoding=ENC))
    fields = derive_fields(schema, example_path)

    # Ensure DB exists (create if needed)
    db_id = db_cfg.get("database_id")
    if not db_id:
        props = {}
        title_present = False
        for name, t in fields.items():
            nt = notion_type(t)
            props[name] = {nt:{}}
            if nt=="title": title_present = True
        if not title_present:
            title_key = "entry_id" if "entry_id" in fields else next(iter(fields.keys()))
            props[title_key] = {"title":{}}
        db = notion.databases.create(parent={"type":"page_id","page_id":root_id},
                                     title=[{"type":"text","text":{"content":"QCWeekly"}}],
                                     properties=props)
        db_id = db["id"]
        cfg["databases"]["QCWeekly"]["database_id"] = db_id
        json.dump(cfg, open(a.config,"w",encoding="utf-8"), indent=2)

    # Textual primary key
    pk = "entry_id"
    ensure_pk_property(notion, db_id, pk=pk)

    # Map property types
    db = notion.databases.retrieve(database_id=db_id)
    ptypes = {name: spec.get("type") for name, spec in db.get("properties",{}).items()}
    pk_type = ptypes.get(pk, "rich_text")

    # Upsert from NDJSON
    with open(example_path,"r",encoding="utf-8") as f:
        for rec in ndjson.reader(f):
            rid = rec.get(pk) or hashlib.sha1(json.dumps(rec, sort_keys=True).encode("utf-8")).hexdigest()
            rec[pk] = rid
            props = {k: as_prop(ptypes.get(k, "rich_text"), v) for k,v in rec.items()}
            flt = build_equals_filter(pk, pk_type, rid)
            page_id = None
            if flt:
                try:
                    res = notion.databases.query(database_id=db_id, filter=flt, page_size=1)
                    if res.get("results"): page_id = res["results"][0]["id"]
                except Exception:
                    pass
            if page_id:
                notion.pages.update(page_id=page_id, properties=props)
            else:
                notion.pages.create(parent={"database_id":db_id}, properties=props)
    print("QC weekly synced.")
if __name__=="__main__": main()
