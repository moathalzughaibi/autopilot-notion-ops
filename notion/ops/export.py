import os, csv, time
from typing import Any, Dict, List
from notion_client import Client
from notion_client.helpers import iterate_paginated_api

NOTION_TOKEN = os.environ.get("NOTION_TOKEN", "")
if not NOTION_TOKEN:
    raise SystemExit("Missing NOTION_TOKEN")

OUT_DIR = "content/databases/exports"
os.makedirs(OUT_DIR, exist_ok=True)

client = Client(auth=NOTION_TOKEN)

def log(m: str) -> None:
    print(f"[export] {time.strftime('%H:%M:%S')} {m}", flush=True)

def db_title(obj: Dict[str, Any]) -> str:
    t = obj.get("title", [])
    if t and isinstance(t, list) and t[0].get("plain_text"):
        return t[0]["plain_text"]
    return ""

def plain_val(p: Dict[str, Any]) -> str:
    t = p.get("type")
    v = p.get(t)
    if t in ("title", "rich_text"):
        if isinstance(v, list) and v:
            return "".join([x.get("plain_text","") for x in v])
        return ""
    if t == "number":
        return "" if v is None else str(v)
    if t == "select":
        return v.get("name","") if v else ""
    if t == "multi_select":
        return ",".join([x.get("name","") for x in (v or [])])
    if t == "date":
        if not v: return ""
        start = v.get("start","")
        end = v.get("end","")
        return f"{start}..{end}" if end else start
    if t == "people":
        return ",".join([x.get("name","") for x in (v or [])])
    if t == "relation":
        return ",".join([x.get("id","") for x in (v or [])])
    return ""

def export_db(db: Dict[str, Any]) -> None:
    db_id = db["id"]
    title = db_title(db) or db_id[:8]
    rows: List[Dict[str,str]] = []

    props = db.get("properties", {})
    prop_names = list(props.keys())

    for page in iterate_paginated_api(client.databases.query, database_id=db_id, page_size=100):
        row: Dict[str,str] = {}
        for name in prop_names:
            row[name] = plain_val(page["properties"].get(name, {}))
        rows.append(row)

    path = os.path.join(OUT_DIR, f"{title}.csv")
    with open(path, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=prop_names)
        w.writeheader()
        for r in rows:
            w.writerow(r)
    log(f"Exported {title} -> {path} ({len(rows)} rows)")

def main():
    # نصدّر كل قواعد DB تحت وركسبيسك (يمكنك لاحقًا تصفيتها بعنوان محدد)
    for obj in iterate_paginated_api(client.search):
        if obj.get("object") == "database":
            export_db(obj)

if __name__ == "__main__":
    main()
