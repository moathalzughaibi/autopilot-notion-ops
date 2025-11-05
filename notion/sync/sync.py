# notion/sync/sync.py
import os, csv, glob, time
from typing import Optional, Dict, Any, List
from notion_client import Client
from notion_client.helpers import iterate_paginated_api

NOTION_TOKEN = os.environ.get("NOTION_TOKEN", "")
ROOT_PAGE_ID = os.environ.get("ROOT_PAGE_ID", "")
CONTENT_DIR  = os.environ.get("CONTENT_DIR", "content/databases")

if not NOTION_TOKEN:
    raise SystemExit("Missing NOTION_TOKEN")
if not ROOT_PAGE_ID:
    raise SystemExit("Missing ROOT_PAGE_ID")

notion = Client(auth=NOTION_TOKEN)

def log(msg: str) -> None:
    print(f"[sync] {time.strftime('%H:%M:%S')} {msg}", flush=True)

def _db_title(db: Dict[str, Any]) -> str:
    t = db.get("title", [])
    if isinstance(t, list) and t and t[0].get("plain_text"):
        return t[0]["plain_text"]
    return ""

def _retrieve_db(db_id: str) -> Dict[str, Any]:
    try:
        return notion.databases.retrieve(db_id)
    except Exception as e:
        log(f"Failed retrieve for {db_id}: {e}")
        return {"id": db_id, "properties": {}}

def find_database_by_title(title: str) -> Optional[Dict[str, Any]]:
    # 1) ابحث ضمن Children لصفحة الجذر
    cursor = None
    while True:
        resp = notion.blocks.children.list(block_id=ROOT_PAGE_ID, start_cursor=cursor, page_size=100)
        for child in resp.get("results", []):
            if child.get("type") == "child_database":
                ch = child["child_database"]
                if ch.get("title") == title:
                    return _retrieve_db(child["id"])
        if not resp.get("has_more"): break
        cursor = resp.get("next_cursor")

    # 2) احتياط: بحث عام
    for obj in iterate_paginated_api(
        notion.search,
        filter={"value": "database", "property": "object"},
        sort={"direction": "ascending", "timestamp": "last_edited_time"},
        query=title,
    ):
        if obj.get("object") == "database" and _db_title(obj) == title:
            return _retrieve_db(obj["id"])
    return None

def ensure_schema(db_id: str, csv_headers: List[str]) -> str:
    """
    يتأكد من وجود عمود عنوان + أي أعمدة مطلوبة من CSV.
    يرجّع اسم عمود العنوان للاستخدام عند إنشاء الصفحات.
    """
    db = _retrieve_db(db_id)
    props = db.get("properties") or {}
    # ابحث عن عمود العنوان
    title_prop = next((k for k, v in props.items() if v.get("type") == "title"), None)

    update_props: Dict[str, Any] = {}

    if not title_prop:
        # أنشئ عمود عنوان افتراضي
        update_props["Name"] = {"title": {}}
        title_prop = "Name"

    # أضف أي أعمدة من CSV غير موجودة
    for h in csv_headers:
        if h == title_prop:              # موجود مسبقًا
            continue
        if h in props:                   # العمود موجود
            continue
        # أنشئه كنص افتراضي
        update_props[h] = {"rich_text": {}}

    if update_props:
        log(f"Updating DB schema with: {list(update_props.keys())}")
        notion.databases.update(db_id=db_id, properties=update_props)
        # استرجع بعد التحديث
        db = _retrieve_db(db_id)
        props = db.get("properties") or {}

    return title_prop

def ensure_property_types(db: Dict[str, Any]) -> Dict[str, str]:
    props = db.get("properties", {}) or {}
    return {name: meta.get("type", "rich_text") for name, meta in props.items()}

def upsert_page(db_id: str, title_prop: str, row: Dict[str, str], prop_types: Dict[str, str]) -> None:
    # قيّم العنوان من عدة مفاتيح محتملة
    name_val = (
        row.get(title_prop) or
        row.get("Name") or row.get("Title") or
        row.get("name") or row.get("title") or ""
    )
    if not name_val:
        return

    props: Dict[str, Any] = {
        title_prop: {"title": [{"type": "text", "text": {"content": str(name_val)}}]}
    }

    for k, v in row.items():
        if k == title_prop:
            continue
        v = "" if v is None else str(v)
        ptype = prop_types.get(k, "rich_text")
        if ptype == "number":
            try: num = float(v) if v else None
            except ValueError: num = None
            props[k] = {"number": num}
        elif ptype == "checkbox":
            props[k] = {"checkbox": v.lower() in ("1", "true", "yes")}
        elif ptype == "url":
            props[k] = {"url": v or None}
        elif ptype == "email":
            props[k] = {"email": v or None}
        elif ptype == "phone_number":
            props[k] = {"phone_number": v or None}
        else:
            props[k] = {"rich_text": [{"type": "text", "text": {"content": v}}]}

    notion.pages.create(parent={"database_id": db_id}, properties=props)

def infer_db_title_from_filename(csv_path: str) -> str:
    return os.path.splitext(os.path.basename(csv_path))[0]

def sync_csv_to_db(db_title: str, csv_path: str) -> None:
    log(f"Syncing CSV → DB | {os.path.basename(csv_path)} -> {db_title}")
    db = find_database_by_title(db_title)
    if not db:
        raise SystemExit(f"Database not found in Notion: {db_title}")

    # اقرأ الرؤوس أولاً لتجهيز المخطط
    with open(csv_path, encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        headers = reader.fieldnames or []
    if not headers:
        log(f"Empty/invalid CSV headers in: {csv_path}")
        return

    title_prop = ensure_schema(db["id"], headers)
    # بعد التحديث خذ الأنواع
    db = _retrieve_db(db["id"])
    prop_types = ensure_property_types(db)

    # أدرج الصفوف
    with open(csv_path, encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            upsert_page(db["id"], title_prop, row, prop_types)

    log(f"Done: {db_title}")

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
