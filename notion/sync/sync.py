# notion/sync/sync.py
import os, csv, glob, time, re
from typing import Optional, Dict, Any, Iterable, List
from notion_client import Client
from notion_client.helpers import iterate_paginated_api

NOTION_TOKEN = os.environ.get("NOTION_TOKEN", "")
ROOT_PAGE_ID = os.environ.get("ROOT_PAGE_ID", "")  # صفحة الجذر التي وضعنا تحتها قواعد البيانات
CONTENT_DIR  = os.environ.get("CONTENT_DIR", "content/databases")

if not NOTION_TOKEN:
    raise SystemExit("Missing NOTION_TOKEN")

notion = Client(auth=NOTION_TOKEN)

def log(msg: str) -> None:
    print(f"[sync] {time.strftime('%H:%M:%S')} {msg}", flush=True)

# ---- أدوات مساعدة على العناوين ----
def normalize_title(s: str) -> str:
    """حوّل أي عنوان لصيغة مقارنة موحّدة (حروف/أرقام فقط مع مسافة واحدة)"""
    s = re.sub(r"[^A-Za-z0-9]+", " ", s or "")
    return " ".join(s.strip().lower().split())

def db_plain_title(db: Dict[str, Any]) -> str:
    """جلب العنوان النصي لقاعدة بيانات أرجعتها Notion (object == database)"""
    title = db.get("title", [])
    if isinstance(title, list) and title:
        t = title[0].get("plain_text") or title[0].get("text", {}).get("content")
        if t:
            return t
    # بعض الاستجابات تحتوي ضمن 'properties' أو child_database لاحقًا
    return ""

def list_child_databases_under_root(root_id: str) -> List[Dict[str, Any]]:
    """يمسح أبناء صفحة الجذر ويعيد child_database كعناصر يمكننا جلبها لاحقًا بـ retrieve"""
    if not root_id:
        return []
    items = []
    try:
        for block in iterate_paginated_api(notion.blocks.children.list, block_id=root_id):
            if block.get("type") == "child_database":
                child = block["child_database"]
                items.append({"object": "database_stub", "id": block["id"], "title_text": child.get("title", "")})
    except Exception as e:
        log(f"warn: could not list children of ROOT_PAGE_ID ({root_id}): {e}")
    # حوّل الــ stub إلى كائنات database بحقيقة عبر retrieve حتى نحصل على بنية موحدة
    results = []
    for it in items:
        try:
            full = notion.databases.retrieve(database_id=it["id"])
            results.append(full)
        except Exception:
            # كاحتياط، أبقِ stub بعنوانه إذا فشل retrieve
            results.append({
                "object": "database",
                "id": it["id"],
                "title": [{"type": "text", "plain_text": it["title_text"], "text": {"content": it["title_text"]}}],
            })
    return results

def search_databases_candidates(queries: Iterable[str]) -> List[Dict[str, Any]]:
    """يستدعي /search بعدة استعلامات ويجمع النتائج التي object=database"""
    seen: set = set()
    out: List[Dict[str, Any]] = []
    for q in queries:
        try:
            resp = notion.search(query=q or None, sort={"direction": "ascending", "timestamp": "last_edited_time"})
            for item in resp.get("results", []):
                if item.get("object") == "database":
                    did = item.get("id")
                    if did and did not in seen:
                        out.append(item); seen.add(did)
        except Exception as e:
            log(f"warn: search('{q}') failed: {e}")
    return out

def find_database_by_title(title: str) -> Optional[Dict[str, Any]]:
    """محاولة قوية للعثور على قاعدة بيانات بالعنوان:
       - جرّب /search بعدة أشكال للاستعلام
       - امسح أبناء ROOT_PAGE_ID من نوع child_database
       - قارن بالعناوين بعد normalize حتى نتجاهل '_' و '-' والفروق البسيطة
    """
    wanted_norm = normalize_title(title)

    queries = [title, title.replace("_", " "), title.replace("_", "-"), title.replace("-", " ")]
    candidates = []
    candidates += search_databases_candidates(queries)
    candidates += list_child_databases_under_root(ROOT_PAGE_ID)

    # إزالة التكرارات بالـ id
    uniq: Dict[str, Dict[str, Any]] = {}
    for db in candidates:
        did = db.get("id")
        if did and did not in uniq:
            uniq[did] = db

    # طابق بالعناوين بعد التطبيع
    for db in uniq.values():
        t = db_plain_title(db)
        if not t:
            continue
        if normalize_title(t) == wanted_norm:
            return db

    # كحل أخير، إذا لم نجد: اطبع ما رصدناه للمساعدة
    if uniq:
        found_titles = ", ".join(sorted({db_plain_title(d) for d in uniq.values() if db_plain_title(d)}))
        log(f"not found; scanned titles: {found_titles}")
    return None

# ---- خصائص & إدخال الصفوف ----
def ensure_property_types(db: Dict[str, Any]) -> Dict[str, str]:
    props = db.get("properties", {})
    return {name: meta.get("type", "rich_text") for name, meta in props.items()}

def upsert_page(db_id: str, title_prop: str, row: Dict[str, str], prop_types: Dict[str, str]) -> None:
    name_val = row.get("Name") or row.get("Title") or row.get("name") or row.get("title") or ""
    if not name_val:
        return
    props: Dict[str, Any] = {}
    props[title_prop] = {"title": [{"type": "text", "text": {"content": str(name_val)}}]}
    for k, v in row.items():
        if k in (title_prop, "Name", "Title", "name", "title"):
            continue
        v = "" if v is None else str(v)
        # استعمال rich_text كافٍ كبداية
        props[k] = {"rich_text": [{"type": "text", "text": {"content": v}}]}
    notion.pages.create(parent={"database_id": db_id}, properties=props)

def sync_csv_to_db(db_title: str, csv_path: str) -> None:
    log(f"Syncing CSV → DB | {os.path.basename(csv_path)} -> {db_title}")
    db = find_database_by_title(db_title)
    if not db:
        raise SystemExit(f"Database not found in Notion: {db_title}")

    # ابحث عن اسم خاصية العنوان في قاعدة البيانات
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
    base = os.path.splitext(os.path.basename(csv_path))[0]
    # نحافظ على الاسم كما هو (بشرطات سفلية)، find_database_by_title يتولّى التطبيع
    return base

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
