# create_test_incident.py
import os
import sys
import argparse
import requests

API = "https://api.notion.com/v1"
NOTION_VERSION = "2022-06-28"
TIMEOUT = 60

def headers(token: str) -> dict:
    return {
        "Authorization": f"Bearer {token}",
        "Notion-Version": NOTION_VERSION,
        "Content-Type": "application/json"
    }

def get_env_incident_db_id() -> str | None:
    """
    Prefer NOTION_INCIDENT_LOG_DB_ID; fallback to legacy INCIDENT_LOG_DB_ID.
    """
    return os.environ.get("NOTION_INCIDENT_LOG_DB_ID") or os.environ.get("INCIDENT_LOG_DB_ID")

def verify_db_access(token: str, db_id: str) -> bool:
    """
    Verify that a database id exists and is accessible.
    """
    try:
        r = requests.get(f"{API}/databases/{db_id}", headers=headers(token), timeout=TIMEOUT)
        if r.ok:
            return True
        # Some Notion API clients return 404 when id format has dashes stripped incorrectly.
        # Accept both dashed and non-dashed forms by trying to add dashes if missing.
        return False
    except requests.RequestException:
        return False

def search_incident_db(token: str, query: str = "Incident Log") -> str | None:
    """
    Fallback: search for a database whose title contains 'Incident Log'.
    """
    try:
        r = requests.post(
            f"{API}/search",
            headers=headers(token),
            json={"query": query, "page_size": 100},
            timeout=TIMEOUT,
        )
        r.raise_for_status()
        for res in r.json().get("results", []):
            if res.get("object") == "database":
                title = "".join([t.get("plain_text", "") for t in res.get("title", [])])
                if query.lower() in (title or "").lower():
                    return res["id"]
        return None
    except requests.RequestException as e:
        print(f"Search failed: {e}", file=sys.stderr)
        return None

def create_incident(token: str, db_id: str, title: str, severity: str, incident_type: str, summary: str):
    """
    Create a page in the Incident database with the provided properties.
    """
    props = {
        # Notion expects a 'title' property (the name of the title prop can vary).
        # Using 'title' key maps to the database's title property automatically.
        "title": {"title": [{"text": {"content": title}}]},
        # The following property names must exist in your DB schema:
        #   - 'Incident Type' (select)
        #   - 'Severity' (select)
        #   - 'Status' (status)
        #   - 'Summary' (rich_text)
        "Incident Type": {"select": {"name": incident_type}},
        "Severity": {"select": {"name": severity}},
        "Status": {"status": {"name": "Open"}},
        "Summary": {"rich_text": [{"text": {"content": summary}}]},
    }
    r = requests.post(
        f"{API}/pages",
        headers=headers(token),
        json={"parent": {"database_id": db_id}, "properties": props},
        timeout=TIMEOUT,
    )
    r.raise_for_status()
    created_id = r.json().get("id")
    print(f"[+] Incident Created in Notion: {title} ({created_id})")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--title", required=True)
    ap.add_argument("--severity", required=True)
    ap.add_argument("--type", required=True, dest="incident_type")
    ap.add_argument("--summary", required=True)
    args = ap.parse_args()

    token = os.getenv("NOTION_TOKEN")
    if not token:
        print("Missing NOTION_TOKEN", file=sys.stderr)
        sys.exit(1)

    # 1) Try environment ID first (recommended + fastest)
    db_id = get_env_incident_db_id()
    if db_id:
        if not verify_db_access(token, db_id):
            print("Provided NOTION_INCIDENT_LOG_DB_ID is not accessible; falling back to search…", file=sys.stderr)
            db_id = None

    # 2) Fallback: search by title
    if not db_id:
        db_id = search_incident_db(token, "Incident Log")

    if not db_id:
        print("Incident Log DB not found", file=sys.stderr)
        sys.exit(2)

    # 3) Create incident
    try:
        create_incident(
            token=token,
            db_id=db_id,
            title=args.title,
            severity=args.severity,
            incident_type=args.incident_type,
            summary=args.summary,
        )
    except requests.HTTPError as e:
        # Surface useful context if the schema doesn't match
        print(f"HTTP error while creating incident: {e.response.status_code} -> {e.response.text}", file=sys.stderr)
        sys.exit(3)
    except requests.RequestException as e:
        print(f"Network error while creating incident: {e}", file=sys.stderr)
        sys.exit(4)

if __name__ == "__main__":
    main()
# --- add near the other imports ---
import re
# -----------------------------------

def normalize_db_id(dbid: str) -> str:
    """
    Normalize a 32-hex Notion DB ID into dashed form required by Notion API.
    Example:
      2a5b22c770d981d9a084e824ab1a84d0
      -> 2a5b22c7-70d9-81d9-a084-e824ab1a84d0
    If the input already contains dashes or isn't 32 hex chars, it's returned as-is.
    """
    if not dbid:
        return dbid
    clean = re.sub(r"[^0-9a-fA-F]", "", dbid)
    if len(clean) == 32:
        return f"{clean[0:8]}-{clean[8:12]}-{clean[12:16]}-{clean[16:20]}-{clean[20:]}"
    return dbid  # already dashed or unexpected length

def get_env_incident_db_id() -> str | None:
    """
    Prefer NOTION_INCIDENT_LOG_DB_ID; fallback to legacy INCIDENT_LOG_DB_ID.
    Always return the dashed/normalized form compatible with Notion API.
    """
    raw = os.environ.get("NOTION_INCIDENT_LOG_DB_ID") or os.environ.get("INCIDENT_LOG_DB_ID")
    return normalize_db_id(raw) if raw else None
