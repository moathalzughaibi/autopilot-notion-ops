# notion/sync/sync.py
import os, csv, glob, time
from typing import Optional, Dict, Any, List
from notion_client import Client
from notion_client.helpers import iterate_paginated_api

# ====== env ======
NOTION_TOKEN = os.environ.get("NOTION_TOKEN", "")
ROOT_PAGE_ID = os.environ.get("ROOT_PAGE_ID", "")
CONTENT_DIR  = os.environ.get("CONTENT_DIR", "content/databases")

if not NOTION_TOKEN:
    raise SystemExit("Missing NOTION_TOKEN")
if not ROOT_PAGE_ID:
    raise SystemExit("Missing ROOT_PAGE_ID")

# ====== client ======
notion = Client(auth=NOTION_TOKEN)

# ====== utils ======
def log(msg: str) -> None:
    print(f"[sync] {time.strftime('%H:%M:%S')} {msg}", flush=True)

def db_plain_title(db: Dict[str, Any]) -> str:
    """
    يدعم إرجاع العنوان سواء كان كائن Database كامل
    أو كائن child_database block (قبل الاسترجاع الكامل).
    """
    # Database object
    if db.get("object") == "database":
        title = db.get("title", [])
        if title and isinstance(title, list) and title[0].get("plain_text"):
            return title[0]["plain_text"]
        return ""
    # child_database block
    if db.get("type") == "child_database":
        return db.get("child_database", {}).get("title", "") or ""
    return ""

def list_child_databases_under_root(root_page_id: str) -> List[Dict[str, Any]]:
    """
    نجلب كل child_database تحت صفحة الجذر، ثم نقوم بـ retrieve
    للحصول على الـ schema (الخصائص).
    """
    items: List[Dict[str, Any]] = []
    # قائمة البلوكات تحت الجذر (قد تتعدّد الصفحات؛ استخدم paginate)
    for blk in iterate_paginated_api(
        notion.blocks.children.list,
        block_id=root_page_id,
        page_size=100,
    ):
        if blk.get("type") == "child_database":
            db_id = blk.get("id")
            try:
                full_db = notion.databases.retrieve(database_id=db_id)
                items.append(full_db)
            except Exception as e:
                # في حال فشل الاسترجاع لأي سبب، نضيف البلوك كما هو (بدون خصائص)
                log(f"warn: failed to retrieve DB meta for {db_id}: {e}")
                items.append(blk)
    return items

def normalize_titles(cand: str) -> List[str]:
    """
    يساعد في التطابق بين أسماء ملفات CSV وأسماء قواعد Notion
    (يدعم استبدال _ بـ space والعكس).
    """
    alts = {cand, cand.replace("_", " "), cand.replace(" ", "_")}
    return list(alts)

def find_database_by_title(title: str) -> Optional[Dict[str, Any]]:
    """
    البحث عن قاعدة بيانات بعنوان مطابق من تحت ROOT_PAGE_ID فقط
    (بدون استخدام /v1/search لتفادي قيود الفلتر الجديدة).
    """
    wanted = set(normalize_titles(title))
    for db in list_child_databases_under_root(ROOT_PAGE_ID):
        t = db_plain_title(db)
        if t in wanted:
            # إن كان block child_database قمنا بالفعل بـ retrieve أعلاه،
            # وإلا فهو كائن database مكتمل.
            if db.get("object") == "database":
                return db
            try:
                return notion.databases.retrieve(database_id=db["id"])
            except Exception:
                return None
    return None

def ensure_property_types(db: Dict[str, Any]) -> Dict[str, str]:
    props = db.get("properties", {})
    return {name: meta.get("type", "rich_text") for name, meta in props.items()}

def upsert_page(db_id: str, title_prop: str, row: Dict[str, str], prop_types: Dict[str, str]) -> None:
    """
    إدراج صفحة بسيطة (create فقط؛ من دون dedupe/تحديث لمطابقة مفاتيح معيّنة).
    """
    name_val = (
        row.get(title_prop)
        or row.get("Name") or row.get("Title")
        or row.get("name") or row.get("title") or ""
    )
    if not name_val:
        return

    props: Dict[str, Any] = {}

    # خاصية العنوان
    props[title_prop] = {
        "title": [{"type": "text", "text": {"content": str(name_val)}}]
    }

    # باقي الحقول -> rich_text (بسيطة وسهلة)
    for k, v in row.items():
        if k in {title_prop, "Name", "Title", "name", "title"}:
            continue
        v = "" if v is None else str(v)
        # لو الحقل غير موجود في الداتابيس سنتجاهله ببساطة:
        if k not in prop_types:
            continue
        if prop_types.get(k) == "title":
            # احتياط: لا نكتب على العنوان ثانية
            continue
        props[k] = {"rich_text": [{"type": "text", "text": {"content": v}}]}

    notion.pages.create(parent={"database_id": db_id}, properties=props)

# ====== Debug helpers ======
def debug_dump_db_schema(db: dict, label: str):
    props = db.get("properties", {})
    parts = [f"{k}:{v.get('type')}" for k, v in props.items()]
    print(f"[sync] Schema of {label}: {', '.join(parts)}", flush=True)

def debug_list_root_databases():
    print("\n[sync] === ROOT databases (under ROOT_PAGE_ID) ===", flush=True)
    dbs = list_child_databases_under_root(ROOT_PAGE_ID)
    if not dbs:
        print("[sync] (none found - check ROOT_PAGE_ID)")
    for db in dbs:
        # احرص أن يكون لدينا نسخة database كاملة للحصول على الخصائص
        if db.get("object") != "database":
            try:
                db = notion.databases.retrieve(database_id=db.get("id"))
            except Exception:
                pass
        title = db_plain_title(db) or "(no title)"
        did   = db.get("id")
        props = db.get("properties", {}) or {}
        title_keys = [k for k, v in props.items() if v.get("type") == "title"]
        print(
            f"[sync] • {title} | id={did} | title_prop="
            f"{title_keys[0] if title_keys else '—'} | props={list(props.keys())}",
            flush=True
        )
    print("[sync] ==========================================\n", flush=True)

# ====== main sync ======
def infer_db_title_from_filename(csv_path: str) -> str:
    base = os.path.splitext(os.path.basename(csv_path))[0]
    # نعيد الاسم كما هو؛ والمطابق سيأخذ بالاعتبار underscore/space عند المقارنة.
    return base

def sync_csv_to_db(db_title: str, csv_path: str) -> None:
    log(f"Syncing CSV → DB | {os.path.basename(csv_path)} -> {db_title}")
    db = find_database_by_title(db_title)
    if not db:
        raise SystemExit(f"Database not found in Notion: {db_title}")

    # إيجاد اسم خاصية العنوان
    title_prop = None
    for name, meta in db.get("properties", {}).items():
        if meta.get("type") == "title":
            title_prop = name
            break
    if not title_prop:
        # اطبع السكيمة لتشخيص المشكلة
        debug_dump_db_schema(db, db_title)
        raise SystemExit(f"No title property found in DB: {db_title}")

    prop_types = ensure_property_types(db)
    with open(csv_path, encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            upsert_page(db["id"], title_prop, row, prop_types)

    log(f"Done: {db_title}")

def main() -> None:
    # وضع اختبار: اطبع كل قواعد البيانات تحت ROOT_PAGE_ID ثم اخرج
    if os.environ.get("DEBUG_LIST") == "1":
        debug_list_root_databases()
        return

    csv_paths = sorted(glob.glob(os.path.join(CONTENT_DIR, "*.csv")))
    if not csv_paths:
        log(f"No CSV files under: {CONTENT_DIR}")
        return

    for csv_path in csv_paths:
        db_title = infer_db_title_from_filename(csv_path)
        sync_csv_to_db(db_title, csv_path)

if __name__ == "__main__":
    main()
