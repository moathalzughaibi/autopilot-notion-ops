import os, argparse, requests, sys

API = "https://api.notion.com/v1"
NOTION_VERSION = "2022-06-28"

def headers(token):
    return {
        "Authorization": f"Bearer {token}",
        "Notion-Version": NOTION_VERSION,
        "Content-Type": "application/json"
    }

def search_incident_db(token):
    r = requests.post(f"{API}/search", headers=headers(token), json={"query":"Incident Log"}, timeout=60)
    r.raise_for_status()
    for res in r.json().get("results",[]):
        if res.get("object")=="database":
            title = "".join([x.get("plain_text","") for x in res.get("title",[])])
            if "Incident Log".lower() in (title or "").lower():
                return res["id"]
    return None

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--title", required=True)
    ap.add_argument("--severity", required=True)
    ap.add_argument("--type", required=True)
    ap.add_argument("--summary", required=True)
    args = ap.parse_args()

    token = os.getenv("NOTION_TOKEN")
    if not token: print("Missing NOTION_TOKEN", file=sys.stderr); sys.exit(1)

    db = search_incident_db(token)
    if not db: print("Incident Log DB not found", file=sys.stderr); sys.exit(2)

    props = {
        "title": {"title":[{"text":{"content": args.title}}]},
        "Incident Type": {"select":{"name": args.type}},
        "Severity": {"select":{"name": args.severity}},
        "Status": {"status":{"name":"Open"}},
        "Summary": {"rich_text":[{"text":{"content": args.summary}}]}
    }
    r = requests.post(f"{API}/pages", headers=headers(token), json={"parent":{"database_id": db}, "properties": props}, timeout=60)
    r.raise_for_status()
    print("Created Incident:", r.json().get("id"))

if __name__ == "__main__":
    main()
