import os, sys, json, glob, re, time, csv
from typing import Any, Dict, List, Optional
from notion_client import Client
from notion_client.helpers import iterate_paginated_api

try:
    import yaml  # type: ignore
except Exception:
    yaml = None

NOTION_TOKEN = os.environ.get("NOTION_TOKEN", "")
ROOT_PAGE_ID = os.environ.get("ROOT_PAGE_ID", "")
if not NOTION_TOKEN:
    raise SystemExit("Missing NOTION_TOKEN")

client = Client(auth=NOTION_TOKEN)

def log(msg: str) -> None:
    print(f"[ops] {time.strftime('%H:%M:%S')} {msg}", flush=True)

# ---------- Helpers ----------
def find_db_by_title(title: str) -> Optional[Dict[str, Any]]:
    # search without filter, then pick databases
    for obj in iterate_paginated_api(client.search, query=title):
        if obj.get("object") == "database":
            # extract title
            db_title = ""
            t = obj.get("title", [])
            if t and isinstance(t, list) and t[0].get("plain_text"):
                db_title = t[0]["plain_text"]
            if db_title == title:
                return obj
    return None

def get_title_prop(db: Dict[str, Any]) -> Optional[str]:
    for name, meta in db.get("properties", {}).items():
        if meta.get("type") == "title":
            return name
    return None

def ensure_props(db_id: str, props_needed: List[str], extra_types: Dict[str, str] = None) -> None:
    """Ensure properties exist on database; default rich_text; title remains untouched."""
    db = client.databases.retrieve(database_id=db_id)
    existing = set(db.get("properties", {}).keys())
    to_add = [p for p in props_needed if p not in existing]
    if not to_add:
        return
    log(f"Adding missing properties: {to_add}")
    update_props: Dict[str, Any] = {}
    extra_types = extra_types or {}
    for p in to_add:
        ptype = extra_types.get(p, "rich_text")
        if ptype == "select":
            update_props[p] = {"select": {}}
        elif ptype == "multi_select":
            update_props[p] = {"multi_select": {}}
        elif ptype == "number":
            update_props[p] = {"number": {"format": "number"}}
        elif ptype == "date":
            update_props[p] = {"date": {}}
        elif ptype == "relation":
            # requires relation database id in extra_types, e.g., "relation:<db_id>"
            # example: extra_types["Project"] = "relation:<db_id>"
            target = extra_types.get(f"{p}__target_id", "")
            if not target:
                raise SystemExit(f"Missing relation target id for property {p}")
            update_props[p] = {"relation": {"database_id": target, "type":"single_property"}}
        else:
            update_props[p] = {"rich_text": {}}
    client.databases.update(database_id=db_id, properties=update_props)

def page_props_from_dict(title_prop: str, row: Dict[str, Any]) -> Dict[str, Any]:
    props: Dict[str, Any] = {}
    # Title
    title_val = (
        row.get("Name")
        or row.get("Title")
        or row.get("title")
        or row.get(title_prop)
        or ""
    )
    if not title_val:
        raise SystemExit("Missing title value for page creation")
    props[title_prop] = {"title": [{"type": "text", "text": {"content": str(title_val)}}]}
    # Others
    for k, v in row.items():
        if k == title_prop or k in ("Name", "Title", "title"):
            continue
        if v is None:
            v = ""
        props[k] = {"rich_text": [{"type": "text", "text": {"content": str(v)}}]}
    return props

def find_page_by(db_id: str, title_prop: str, row: Dict[str, Any]) -> Optional[str]:
    """Find by prioritized keys: id, Key, Title/Name, else None."""
    # 1) explicit id
    explicit = row.get("id") or row.get("ID") or row.get("Id")
    if explicit:
        return explicit

    # 2) Key
    key = row.get("Key") or row.get("key")
    if key:
        q = {
            "filter": {
                "property": "Key",
                "rich_text": {"equals": str(key)}
            },
            "page_size": 1
        }
        res = client.databases.query(database_id=db_id, **q)
        for r in res.get("results", []):
            return r["id"]

    # 3) by title
    ttl = row.get("Title") or row.get("Name") or row.get("title")
    if ttl:
        res = client.databases.query(
            database_id=db_id,
            filter={
                "property": title_prop,
                "title": {"equals": str(ttl)}
            },
            page_size=1
        )
        for r in res.get("results", []):
            return r["id"]

    return None

# ---------- Actions ----------
def action_add_page(cmd: Dict[str, Any]) -> None:
    db_title = cmd["db"]
    row = cmd["properties"]
    db = find_db_by_title(db_title)
    if not db:
        raise SystemExit(f"Database not found: {db_title}")
    title_prop = get_title_prop(db)
    if not title_prop:
        raise SystemExit(f"No title property in DB: {db_title}")
    # ensure non-title props exist
    others = [k for k in row.keys() if k not in (title_prop, "Name", "Title", "title")]
    ensure_props(db["id"], others)
    props = page_props_from_dict(title_prop, row)
    client.pages.create(parent={"database_id": db["id"]}, properties=props)
    log(f"ADDED page to {db_title}")

def action_update_page(cmd: Dict[str, Any]) -> None:
    db_title = cmd["db"]
    row = cmd["properties"]
    db = find_db_by_title(db_title)
    if not db:
        raise SystemExit(f"Database not found: {db_title}")
    title_prop = get_title_prop(db)
    page_id = find_page_by(db["id"], title_prop or "Name", row)
    if not page_id:
        raise SystemExit("Page to update not found")
    # ensure props
    others = [k for k in row.keys() if k not in (title_prop, "Name", "Title", "title")]
    ensure_props(db["id"], others)
    props = page_props_from_dict(title_prop or "Name", row)
    client.pages.update(page_id=page_id, properties=props)
    log(f"UPDATED page in {db_title}")

def action_delete_page(cmd: Dict[str, Any]) -> None:
    db_title = cmd["db"]
    row = cmd.get("where", {})
    db = find_db_by_title(db_title)
    if not db:
        raise SystemExit(f"Database not found: {db_title}")
    title_prop = get_title_prop(db)
    page_id = find_page_by(db["id"], title_prop or "Name", row)
    if not page_id:
        raise SystemExit("Page to delete not found")
    client.pages.update(page_id=page_id, archived=True)
    log(f"ARCHIVED page in {db_title}")

def dispatch(cmd: Dict[str, Any]) -> None:
    action = cmd.get("action")
    if action == "add_page":
        action_add_page(cmd)
    elif action == "update_page":
        action_update_page(cmd)
    elif action == "delete_page":
        action_delete_page(cmd)
    else:
        raise SystemExit(f"Unknown action: {action}")

# ---------- Entry ----------
def load_file(path: str) -> List[Dict[str, Any]]:
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()
    if path.endswith(".json"):
        data = json.loads(text)
    else:
        if yaml is None:
            raise SystemExit("PyYAML not installed")
        data = yaml.safe_load(text)
    # allow single object or list
    if isinstance(data, dict):
        return [data]
    elif isinstance(data, list):
        return data
    else:
        raise SystemExit("Command file must be an object or a list of objects")

def main():
    changed = sys.stdin.read().strip().splitlines()
    files = [p for p in changed if p.strip()]
    if not files:
        log("No command files to run.")
        return
    log(f"Running commands for: {files}")
    for path in files:
        cmds = load_file(path)
        for cmd in cmds:
            dispatch(cmd)

if __name__ == "__main__":
    main()
