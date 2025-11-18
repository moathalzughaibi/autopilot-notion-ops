#!/usr/bin/env python3
"""
Create Notion databases for IFNS V2 and register their IDs.
- Infers properties from CSV header or QC JSON schema.
- Stores DB IDs to config/ifns_v2_db_map.json.
"""
import os, sys, json, argparse, csv, re
from typing import Dict, Any, List, Tuple
from notion_client import Client

def guess_type(col: str, sample: str) -> str:
    c = col.lower()
    if c in ("id","key","slug","name","feature_name","indicator_id","composite_id","symbol"): return "title"
    if c.endswith("_date") or c in ("date","ts","timestamp"): return "date"
    if sample and re.fullmatch(r"https?://\S+", str(sample)): return "url"
    if str(sample).lower() in ("true","false"): return "checkbox"
    try: float(sample); return "number"
    except: pass
    if sample and ("," in str(sample) or ";" in str(sample)): return "multi_select"
    return "rich_text"

def pdef(nt: str) -> Dict[str, Any]: return {nt: {}}

def read_csv_head_sample(p: str):
    with open(p, newline="", encoding="utf-8-sig") as f:
        r = csv.DictReader(f); hdr = r.fieldnames or []; s = next(r, {}) or {}
    return hdr, {h: s.get(h, "") for h in hdr}

def build_props(hdr: List[str], samples: Dict[str,str], overrides: Dict[str,str]) -> Dict[str, Any]:
    props = {}; title = False
    for h in hdr:
        nt = overrides.get(h) or guess_type(h, samples.get(h, ""))
        if nt == "title":
            if title: nt = "rich_text"
            else: title = True
        props[h] = pdef(nt)
    if not title and hdr: props[hdr[0]] = pdef("title")
    return props

def ensure_db(notion: Client, parent_id: str, title: str, props: Dict[str, Any]) -> str:
    db = notion.databases.create(parent={"type":"page_id","page_id":parent_id},
                                 title=[{"type":"text","text":{"content":title}}],
                                 properties=props)
    return db["id"]

def find_root_id(notion: Client, env_root: str, title: str) -> str:
    if env_root: return env_root
    r = notion.search(query=title, filter={"value":"page","property":"object"})
    for obj in r.get("results", []):
        if obj.get("object") == "page": return obj["id"]
    return None

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    ap.add_argument("--assets", nargs="+", help="key=path[:primary_key] ...")
    ap.add_argument("--config", default="config/ifns_v2_db_map.json")
    a = ap.parse_args()

    token = os.environ.get("NOTION_TOKEN")
    root_env = os.environ.get("NOTION_ROOT_PAGE_ID")
    if not token:
        print("ERROR: NOTION_TOKEN not set"); sys.exit(1)
    notion = Client(auth=token)

    cfg = json.load(open(a.config, "r", encoding="utf-8-sig"))
    overrides = cfg.get("typing_rules", {})
    parent_id = find_root_id(notion, root_env, a.root)
    if not parent_id:
        print("ERROR: cannot resolve root page"); sys.exit(1)

    for item in a.assets or []:
        key, rest = item.split("=", 1)
        path = rest.split(":")[0]
        pk = rest.split(":")[1] if ":" in rest else ""

        if path.lower().endswith(".csv"):
            hdr, samples = read_csv_head_sample(path)
            props = build_props(hdr, samples, overrides)
        elif path.lower().endswith(".json") and "qc_weekly_schema" in os.path.basename(path).lower():
            schema = json.load(open(path, "r", encoding="utf-8-sig"))
            props = {}; title = False
            for name, spec in (schema.get("properties", {}) or {}).items():
                t = spec.get("type", "string")
                nt = {"string":"rich_text","number":"number","integer":"number","boolean":"checkbox","array":"multi_select"}.get(t, "rich_text")
                if name in ("entry_id","id","key") and not title:
                    nt = "title"; title = True
                props[name] = pdef(nt)
            if not title and props:
                first = list(props.keys())[0]; props[first] = pdef("title")
        else:
            print(f"Skip unsupported: {path}"); continue

        db_id = ensure_db(notion, parent_id, key, props)
        cfg["databases"][key]["database_id"] = db_id
        if pk: cfg["databases"][key]["primary_key"] = pk
        print(f"Created DB {key} -> {db_id}")

    json.dump(cfg, open(a.config, "w", encoding="utf-8-sig"), indent=2)
    print("Saved DB map:", a.config)

if __name__ == "__main__":
    main()


