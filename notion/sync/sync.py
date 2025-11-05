# notion/sync/sync.py
import os, csv, glob, time, re
from typing import Optional, Dict, Any, List, Tuple
from notion_client import Client
from notion_client.helpers import iterate_paginated_api
from notion_client.errors import APIResponseError

NOTION_TOKEN = os.environ.get("NOTION_TOKEN", "")
ROOT_PAGE_ID = os.environ.get("ROOT_PAGE_ID", "")
CONTENT_DIR  = os.environ.get("CONTENT_DIR", "content/databases")
SYNC_DEBUG   = os.environ.get("SYNC_DEBUG", "0") == "1"

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
    return notion.databases.retrieve(database_id=db_id)

def _normalize_name(s: str) -> str:
    # اسم بسيط وآمن للحقول: إزالة الفراغات البادئة/اللاحقة وتوحيد الفراغات الداخلية
    return re.sub(r"\s+", " ", (s or "").strip())

def _unique_ordered(items: List[str]) -> List[str]:
    seen = set()
    out = []
    for x in items:
        if x not in seen:
            seen.add(x)
            out.append(x)
    return out

def _create_db_under_root(title: str, headers: List[str]) -> Dict[str, Any]:
    headers = [_normalize_name(h) for h in (headers or [])]
    headers = _unique_ordered([h for h in headers if h])
    props: Dict[str, Any] = {"Name": {"title": {}}}
    for h in headers:
        if h == "Name":
            continue
        props[h] = {"rich_text": {}}
    log(f"Creating DB '{title}' with props: {list(props.keys())}")
    db = notion.databases.create(
        parent={"type": "page_id", "page_id": ROOT_PAGE_ID},
        title=[{"type": "text", "text": {"content": title}}],
        properties=props,
    )
    return db

def find_database_by_title(title: str) -> Optional[Dict[str, Any]]:
    # 1) child_database تحت جذر المشروع
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
    # 2) بحث عام
    for obj in iterate_paginated_api(
        notion.search,
        filter={"value": "database", "property": "object"},
        sort={"direction": "ascending", "timestamp": "last_edited_time"},
        query=title,
    ):
        if obj.get("object") == "database" and _db_title(obj) == title:
            return _retrieve_db(obj["id"])
    return None

def _wait_props_exist(db_id: str, wanted: List[str], timeout_s: float = 6.0) -> Dict[str, Any]:
    """انتظر حتى تظهر الخصائص المطلوبة فعليًا في المخطط (اتساق Notion)."""
    deadline = time.time() + timeout_s
    wanted = set(_normalize_name(w) for w in wanted)
    while time.time() < deadline:
        db = _retrieve_db(db_id)
        have = set(db.get("properties", {}).keys())
        if wanted.issubset(have):
            return db
        time.sleep(0.5)
    return _retrieve_db(db_id)

def ensure_schema(db_id: str, csv_headers: List[str]) -> Tuple[str, Dict[str, Any]]:
    """يعيد (title_prop, db_after) بعد ضمان المخطط."""
    csv_headers = [_normalize_name(h) for h in (csv_headers or [])]
    csv_headers = _unique_ordered([h for h in csv_headers if h])

    db = _retrieve_db(db_id)
    props = db.get("properties") or {}
    title_prop = next((k for k, v in props.items() if v.get("type") == "title"), None)

    update_props: Dict[str, Any] = {}
    if not title_prop:
        update_props["Name"] = {"title": {}}
        title_prop = "Name"

    for h in csv_headers:
        if h == title_prop: continue
        if h in props:      continue
        update_props[h] = {"rich_text": {}}

    if update_props:
        log(f"Updating DB schema with: {list(update_props.keys())}")
        notion.databases.update(database_id=db_id, properties=update_props)
        db = _wait_props_exist(db_id, list(update_props.keys()))

    return title_prop, db

def ensure_property_types(db: Dict[str, Any]) -> Dict[str, str]:
    props = db.get("properties", {}) or {}
    return {name: meta.get("type", "rich_text") for name, meta in props.items()}

_MISSING_PROP_RE = re.compile(r"([A-Za-z0-9 _\-]+) is not a property that exists")

def _extract_missing_props_from_error(e: APIResponseError) -> List[str]:
    txt = getattr(e, "message", "") or str(e)
    found = _MISSING_PROP_RE.findall(txt)
    # نظّف الأسماء الملتقطة (قد تحتوي فراغًا بادئًا)
    return [_normalize_name(x) for x in found if _normalize_name(x)]

def _add_missing_properties(db_id: str, missing_keys: List[str]) -> Dict[str, Any]:
    missing_keys = _unique_ordered([_normalize_name(k) for k in missing_keys if _normalize_name(k)])
    if not missing_keys:
        return _retrieve_db(db_id)
    update_props = {k: {"rich_text": {}} for k in missing_keys}
    log(f"Adding missing properties on demand: {missing_keys}")
    notion.databases.update(database_id=db_id, properties=update_props)
    return _wait_props_exist(db_id, missing_keys)

def _row_props(db_id: str, title_prop: str, row: Dict[str, str], prop_types: Dict[str, str]) -> Dict[str, Any]:
    props: Dict[str, Any] = {title_prop: {"title": []}}
    # عنوان الصف
    name_val = None
    for k in (title_prop, "Name", "Title", "name", "title"):
        if k in row and str(row[k]).strip():
            name_val = str(row[k]).strip()
            break
    if not name_val:
        # لو لم نجد أي عنوان، استخرج أول قيمة غير فارغة لأقرب عمود
        for k, v in row.items():
            if str(v or "").strip():
                name_val = str(v).strip()
                break
    if not name_val:
        name_val = ""  # سيتجاهل الإدراج لاحقًا إذا كان فارغًا
    else:
        props[title_prop] = {"title": [{"type": "text", "text": {"content": name_val}}]}

    # باقي الحقول
    for raw_k, v in row.items():
        k = _normalize_name(raw_k)
        if not k or k == title_prop:
            continue
        # لا تُرسل خصائص غير موجودة في المخطط الحالي
        if k not in prop_types:
            continue
        v = "" if v is None else str(v)
        ptype = prop_types.get(k, "rich_text")
        if ptype == "number":
            try: num = float(v) if v else None
            except ValueError: num = None
            props[k] = {"number": num}
        elif ptype == "checkbox":
            props[k] = {"checkbox": v.strip().lower() in ("1", "true", "yes", "y")}
        elif ptype == "url":
            props[k] = {"url": v or None}
        elif ptype == "email":
            props[k] = {"email": v or None}
        elif ptype == "phone_number":
            props[k] = {"phone_number": v or None}
        else:
            props[k] = {"rich_text": [{"type": "text", "text": {"content": v}}]}
    return props

def upsert_page(db_id: str, title_prop: str, row: Dict[str, str], prop_types: Dict[str, str]) -> None:
    # تجاهل الصفوف التي لن تعطينا عنوانًا
    title_candidate = (
        row.get(title_prop) or row.get("Name") or row.get("Title")
        or row.get("name") or row.get("title") or ""
    )
    if not str(title_candidate).strip():
        # اسمح بإدراج صف بلا عنوان فقط إذا سيُشتق لاحقًا، وإلا تخطَّ
        pass

    props = _row_props(db_id, title_prop, row, prop_types)
    if not props.get(title_prop, {}).get("title"):
        # لا عنوان نهائي = تخطّي الصف بهدوء
        return

    try:
        notion.pages.create(parent={"database_id": db_id}, properties=props)
        return
    except APIResponseError as e:
        missing = _extract_missing_props_from_error(e)
        if missing:
            db = _add_missing_properties(db_id, missing)
            prop_types.update(ensure_property_types(db))
            # أعد بناء الخصائص بعد تحديث الأنواع
            props = _row_props(db_id, title_prop, row, prop_types)
            notion.pages.create(parent={"database_id": db_id}, properties=props)
            return
        raise

def infer_db_title_from_filename(csv_path: str) -> str:
    return os.path.splitext(os.path.basename(csv_path))[0]

def list_root_databases() -> List[Tuple[str, str]]:
    out = []
    cursor = None
    while True:
        resp = notion.blocks.children.list(block_id=ROOT_PAGE_ID, start_cursor=cursor, page_size=100)
        for child in resp.get("results", []):
            if child.get("type") == "child_database":
                dbid = child["id"]
                title = child["child_database"].get("title", "")
                out.append((dbid, title))
        if not resp.get("has_more"): break
        cursor = resp.get("next_cursor")
    return out

def print_root_inventory() -> None:
    rows = list_root_databases()
    log(f"ROOT has {len(rows)} databases:")
    for dbid, title in rows:
        log(f" - {title} ({dbid})")

def sync_csv_to_db(db_title: str, csv_path: str) -> None:
    log(f"Syncing CSV → DB | {os.path.basename(csv_path)} -> {db_title}")

    # حمّل رؤوس CSV ونظّفها
    with open(csv_path, encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        raw_headers = reader.fieldnames or []
    headers = _unique_ordered([_normalize_name(h) for h in raw_headers if _normalize_name(h)])
    if not headers:
        log(f"Empty/invalid CSV headers in: {csv_path}")
        return

    db = find_database_by_title(db_title)
    if not db:
        log(f"DB '{db_title}' not found, creating it under ROOT...")
        db = _create_db_under_root(db_title, headers)

    # ضمن المخطط وارجع اسم عمود العنوان + db المحدّث
    title_prop, db = ensure_schema(db["id"], headers)
    prop_types = ensure_property_types(db)

    if SYNC_DEBUG:
        log(f"Schema of {db_title}: {sorted(list(prop_types.keys()))} | title_prop={title_prop}")

    with open(csv_path, encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            # طبيع أسماء الأعمدة داخل الصف
            row = {_normalize_name(k): v for k, v in row.items()}
            upsert_page(db["id"], title_prop, row, prop_types)

    log(f"Done: {db_title}")

def main() -> None:
    if SYNC_DEBUG:
        print_root_inventory()

    csv_paths = sorted(glob.glob(os.path.join(CONTENT_DIR, "*.csv")))
    if not csv_paths:
        log(f"No CSV files under: {CONTENT_DIR}")
        return

    for csv_path in csv_paths:
        db_title = infer_db_title_from_filename(csv_path)
        sync_csv_to_db(db_title, csv_path)

if __name__ == "__main__":
    main()
