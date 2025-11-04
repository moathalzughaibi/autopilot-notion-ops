import os, csv, sys, time
from pathlib import Path
from notion_client import Client

NOTION_TOKEN   = os.getenv("NOTION_TOKEN", "")
ROOT_PAGE_ID   = os.getenv("ROOT_PAGE_ID", "")
CONTENT_DIR    = Path("content")
DB_CSV_DIR     = CONTENT_DIR / "databases"

if not NOTION_TOKEN or not ROOT_PAGE_ID:
    print("❌ Missing NOTION_TOKEN or ROOT_PAGE_ID env vars.", file=sys.stderr)
    sys.exit(1)

notion = Client(auth=NOTION_TOKEN)

def _db_title_str(db_obj):
    ttl = db_obj.get("title", [])
    return "".join([t.get("plain_text","") for t in ttl]) if ttl else ""

def find_database_by_title(root_page_id: str, wanted_title: str):
    # Search API + sanity check via list in the root page
    res = notion.search(query=wanted_title, filter={"value":"database","property":"object"})
    for it in res.get("results", []):
        if it.get("object") == "database" and _db_title_str(it) == wanted_title:
            return it
    # fallback: children list (optional)
    return None

def ensure_db_properties(db_id: str, needed: list[str]):
    db = notion.databases.retrieve(db_id=db_id)
    existing = set(db["properties"].keys())
    patch = {}
    for prop in needed:
        if prop == "Name":  # Name is special (title)
            continue
        if prop not in existing:
            patch[prop] = {"rich_text": {}}
    if patch:
        notion.databases.update(db_id=db_id, properties=patch)

def list_existing_pages_by_name(db_id: str) -> dict:
    existing = {}
    cursor = None
    while True:
        resp = notion.databases.query(database_id=db_id, start_cursor=cursor) if cursor else notion.databases.query(database_id=db_id)
        for r in resp.get("results", []):
            name = ""
            title_prop = r["properties"].get("Name", {}).get("title", [])
            if title_prop:
                name = "".join([t.get("plain_text","") for t in title_prop])
            if name:
                existing[name] = r["id"]
        if not resp.get("has_more"):
            break
        cursor = resp.get("next_cursor")
    return existing

def to_rich_text(val: str):
    return [{"type":"text","text":{"content": val or ""}}]

def upsert_row(db_id: str, row: dict, existing_by_name: dict):
    name = (row.get("Name") or "").strip()
    if not name:
        return
    props = {}
    # Title
    props["Name"] = {"title": [{"type":"text","text":{"content": name}}]}
    # The rest as rich_text
    for k, v in row.items():
        if k == "Name":
            continue
        props[k] = {"rich_text": to_rich_text(v)}

    if name in existing_by_name:
        page_id = existing_by_name[name]
        notion.pages.update(page_id=page_id, properties=props)
    else:
        notion.pages.create(parent={"database_id": db_id}, properties=props)

def sync_csv_to_db(db_title: str, csv_path: Path):
    print(f"• Syncing CSV → DB  | {csv_path.name} → {db_title}")
    db = find_database_by_title(ROOT_PAGE_ID, db_title)
    if not db:
        print(f"   ⚠️ Database '{db_title}' not found under ROOT_PAGE_ID. Did you run the seed?", file=sys.stderr)
        return
    db_id = db["id"]

    # Read CSV
    with open(csv_path, encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    # Ensure DB has the CSV columns
    need_cols = list(reader.fieldnames or [])
    ensure_db_properties(db_id, need_cols)

    # Existing pages index
    existing = list_existing_pages_by_name(db_id)

    # Upsert
    for r in rows:
        upsert_row(db_id, r, existing)

def main():
    if not DB_CSV_DIR.exists():
        print("No content/databases directory found. Nothing to sync.")
        return

    # Database names derived from CSV filenames (without extension)
    csvs = sorted(DB_CSV_DIR.glob("*.csv"))
    if not csvs:
        print("No CSV files in content/databases. Nothing to sync.")
        return

    for csv_file in csvs:
        # Keep the exact DB title as the filename stem (already uses Autopilot_XXX)
        db_title = csv_file.stem
        sync_csv_to_db(db_title, csv_file)
        time.sleep(0.2)

if __name__ == "__main__":
    main()
