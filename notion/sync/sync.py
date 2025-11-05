# notion/sync/sync.py
import os, csv, glob, time
from typing import Optional, Dict, Any, List
from notion_client import Client
from notion_client.helpers import iterate_paginated_api

NOTION_TOKEN   = os.environ.get("NOTION_TOKEN", "")
ROOT_PAGE_ID   = os.environ.get("ROOT_PAGE_ID", "")
CONTENT_DIR    = os.environ.get("CONTENT_DIR", "content/databases")

if not NOTION_TOKEN:
    raise SystemExit("Missing NOTION_TOKEN")

notion = Client(auth=NOTION_TOKEN)

def log(msg: str) -> None:
    print(f"[sync] {time.strftime('%H:%M:%S')} {msg}", flush=True)

def _db_title(db: Dict[str, Any]) -> str:
    title = db.get("title", [])
    if title and isinstance(title, list) and title[0].get("plain_text"):
        return title[0]["plain_text"]
    return ""

def find_database_by_title(title: str) -> Optional[Dict[str, Any]]:
    """
    Search for a Notion database by title.
    ملاحظة: واجهة /v1/search أصبحت تتطلب filter.value = "page" أو "data_source".
    ما زالت النتائج تُرجِع object == "database" لقواعد البيانات.
    """
    # نجمع كل النتائج عبر التصفح المتعدد
    all_results: List[Dict[str, Any]] = list(
        iterate_paginated_api(
            notion.search,
            query=title,
            filter={"value": "data_source", "property": "object"},
            sort={"direction": "ascending", "timestamp": "last_edited_time"},
            page_size=50,
        )
    )
    for db in all_results:
        if db.get("object") == "database" and _db_title(db) == title:
            return db
    return None

def ensure_property_types(db: Dict[str, Any]) -> Dict[str, str]:
    props = db.get("properties", {})
    return {name: meta.get("type", "rich_text") for name, meta in props.items()}

def upsert_page(db_id: str, title_prop: str, row: Dict[str, str], prop_types: Dict[str, str]) -> None:
    # اسم الصفحة (العنوان)
    name_val = row.get("Name") or row.get("Title") or row.get("name") or row.get("title") or ""
    if not name_val:
        return

    props: Dict[str, Any] = {}
    props[title_prop] = {"title": [{"type": "text", "text": {"content": str(name_val)}}]}

    # بقية الخصائص تُحفظ كنص غني افتراضياً
    for k, v in row.items():
        if k in (title_prop, "Name", "Title", "name", "title"):
            continue
        v = "" if v is None else str(v)
        props[k] = {"rich_text": [{"type": "text", "text": {"content": v}}]}

    notion.pages.create(parent={"database_id": db_id}, properties=props)

def sync_csv_to_db(db_title: str, csv_path: str) -> None:
    log(f"Syncing CSV → DB | {os.path.basename(csv_path)} -> {db_title}")

    db = find_database_by_title(db_title)
    if not db:
        raise SystemExit(f"Database not found in Notion: {db_title}")

    # اعثر على اسم خاصية العنوان في القاعدة
    title_prop = None
    for name, meta in db.get("properties", {}).items():
        if meta.get("type") == "title":
            title_prop = name
            break
    if not title_prop:
        raise SystemExit(f"No title property found in DB: {db_title}")

    prop_types = ensure_property_types(db)

    with open(csv_path, encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            upsert_page(db["id"], title_prop, row, prop_types)

    log(f"Done: {db_title}")

def infer_db_title_from_filename(csv_path: str) -> str:
    return os.path.splitext(os.path.basename(csv_path))[0]

def main() -> None:
    csv_paths = sorted(glob.glob(os.path.join(CONTENT_DIR, "*.csv")))
    if not csv_paths:
        log(f"No CSV files under: {CONTENT_DIR}")
        return

    for csv_path in csv_paths:
        db_title = infer_db_title_from_filename(csv_path)
        sync_csv_to_db(db_title, csv_path)

if __name__ == "__main__":
    main()
