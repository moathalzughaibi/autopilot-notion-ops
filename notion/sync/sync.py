# notion/sync/sync.py
import os, csv, glob, time
from typing import Optional, Dict, Any
from notion_client import Client
from notion_client.helpers import iterate_paginated_api

NOTION_TOKEN   = os.environ.get("NOTION_TOKEN", "")
ROOT_PAGE_ID   = os.environ.get("ROOT_PAGE_ID", "")  # ليس ضرورياً للمزامنة لكن نتركه متاحاً
CONTENT_DIR    = os.environ.get("CONTENT_DIR", "content/databases")

if not NOTION_TOKEN:
    raise SystemExit("Missing NOTION_TOKEN")

notion = Client(auth=NOTION_TOKEN)


# ---------- أدوات مساعدة ----------
def log(msg: str) -> None:
    print(f"[sync] {time.strftime('%H:%M:%S')} {msg}", flush=True)


def _db_title(db: Dict[str, Any]) -> str:
    """استخرج عنوان قاعدة البيانات كما يظهر في Notion."""
    title = db.get("title", [])
    if title and isinstance(title, list) and title[0].get("plain_text"):
        return title[0]["plain_text"]
    return ""


def find_database_by_title(title: str) -> Optional[Dict[str, Any]]:
    """
    ابحث عن قاعدة بيانات بالعنوان باستخدام Notion search.
    مهم: الفلتر الصحيح يجب أن يكون {"value": "database", "property": "object"}
    (وليس "databases")
    """
    # البحث العام
    resp = notion.search(
        query=title,
        filter={"value": "database", "property": "object"},
        sort={"direction": "ascending", "timestamp": "last_edited_time"},
    )
    results = resp.get("results", [])
    for db in results:
        if db.get("object") == "database" and _db_title(db) == title:
            return db

    # في حال كان العنوان دقيقًا لكن لم يرجعه البحث الأول، نجرب بدون query
    for db in iterate_paginated_api(notion.search, filter={"value": "database", "property": "object"}):
        if db.get("object") == "database" and _db_title(db) == title:
            return db

    return None


def ensure_property_types(db: Dict[str, Any]) -> Dict[str, str]:
    """
    رجّع خريطة بأسماء الحقول وأنواعها في قاعدة البيانات.
    (نستخدمها لمعرفة هل الحقل موجود أصلاً أم لا، ولو مفقود سننشئه كنص rich_text.)
    """
    props = db.get("properties", {})
    types = {}
    for name, meta in props.items():
        types[name] = meta.get("type", "rich_text")
    return types


def upsert_page(db_id: str, title_prop: str, row: Dict[str, str], prop_types: Dict[str, str]) -> None:
    """
    أضف صفحة جديدة (صف) بناءً على محتويات CSV.
    - نفترض وجود عمود Name (أو Title) ليكون العنوان.
    - بقية الأعمدة تُحفظ كنصوص rich_text إذا لم نعرف نوعها.
    """
    # حدّد عمود العنوان
    name_val = row.get("Name") or row.get("Title") or row.get("name") or row.get("title") or ""
    if not name_val:
        # إذا ما فيه عنوان نتجاهل السطر
        return

    props: Dict[str, Any] = {}

    # العنوان
    props[title_prop] = {
        "title": [{"type": "text", "text": {"content": str(name_val)}}]
    }

    # بقية الأعمدة
    for k, v in row.items():
        if k in (title_prop, "Name", "Title", "name", "title"):
            continue
        v = "" if v is None else str(v)
        # إذا الحقل موجود في قاعدة البيانات بنوع معيّن، نحاول نرميه نص إن لم نميّز النوع
        # (للتبسيط، دائماً نكتب rich_text هنا)
        props[k] = {"rich_text": [{"type": "text", "text": {"content": v}}]}

    notion.pages.create(parent={"database_id": db_id}, properties=props)


def sync_csv_to_db(db_title: str, csv_path: str) -> None:
    log(f"Syncing CSV → DB | {os.path.basename(csv_path)} -> {db_title}")

    db = find_database_by_title(db_title)
    if not db:
        raise SystemExit(f"Database not found in Notion: {db_title}")

    # حدّد اسم خاصيّة العنوان في هذه القاعدة (غالباً تكون "Name")
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
    """
    اسم القاعدة = اسم الملف بدون الامتداد.
    مثال: Autopilot_Glossary.csv → "Autopilot_Glossary"
    (نستخدم نفس الاسم تماماً كما هو ظاهر في Notion)
    """
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
