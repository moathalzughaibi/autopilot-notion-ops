import os, json, argparse, requests
from datetime import datetime, timedelta
API = "https://api.notion.com/v1"
def hdrs(token): return {"Authorization": f"Bearer {token}","Notion-Version":"2022-06-28","Content-Type":"application/json"}
def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--config", required=True); args = ap.parse_args()
    with open(args.config,"r",encoding="utf-8") as f: cfg = json.load(f)
    token = os.getenv("NOTION_TOKEN"); archive = os.getenv("ARCHIVE_PAGE_ID")
    if not token or not archive: raise SystemExit("Missing NOTION_TOKEN/ARCHIVE_PAGE_ID")
    stale = cfg.get("policy",{}).get("stale_days",60)
    cutoff = datetime.utcnow() - timedelta(days=stale)
    r = requests.post(f"{API}/search", headers=hdrs(token), json={"query":"IFNS","filter":{"value":"page","property":"object"}}, timeout=60); r.raise_for_status()
    for pg in r.json().get("results",[]):
        last = pg.get("last_edited_time","")
        try: dt = datetime.fromisoformat(last.replace("Z","+00:00"))
        except: dt = datetime.utcnow()
        if dt.replace(tzinfo=None) < cutoff:
            pid = pg["id"]
            payload = {"parent":{"type":"page_id","page_id": archive}}
            rr = requests.patch(f"{API}/pages/{pid}", headers=hdrs(token), json=payload, timeout=60); rr.raise_for_status()
            print(f"[ARCHIVED] {pid}")
    print("Archive policy applied.")
if __name__ == "__main__": main()
