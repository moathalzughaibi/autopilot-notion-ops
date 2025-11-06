import os, json, argparse, requests, time, pandas as pd
API = "https://api.notion.com/v1"
def hdrs(token): return {"Authorization": f"Bearer {token}","Notion-Version":"2022-06-28","Content-Type":"application/json"}

def create_page(token, parent_id, title):
    data = {"parent":{"type":"page_id","page_id": parent_id},"properties":{"title":{"title":[{"text":{"content": title}}]}}}
    r = requests.post(f"{API}/pages", headers=hdrs(token), json=data, timeout=60); r.raise_for_status(); return r.json()["id"]

def create_db_from_csv(token, parent_id, title, path):
    df = pd.read_csv(path)
    props = {}
    for c in df.columns:
        t = "rich_text"
        cl = c.lower()
        if "date" in cl: t="date"
        elif any(k in cl for k in ["status","phase","priority"]): t="select"
        elif any(k in cl for k in ["sharpe","drawdown","slippage","return","cagr","%","bps"]): t="number"
        props[c] = {t:{}}
    data = {"parent":{"type":"page_id","page_id": parent_id},"title":[{"type":"text","text":{"content": title}}],"properties":props}
    r = requests.post(f"{API}/databases", headers=hdrs(token), json=data, timeout=60); r.raise_for_status(); db = r.json()
    for _, row in df.iterrows():
        pr = {}
        for c in df.columns:
            v = row[c]
            if pd.isna(v): continue
            if isinstance(v,(int,float)): pr[c]={"number": float(v)}
            else: pr[c]={"rich_text":[{"text":{"content": str(v)}}]}
        rr = requests.post(f"{API}/pages", headers=hdrs(token), json={"parent":{"database_id": db["id"]},"properties": pr}, timeout=60); rr.raise_for_status(); time.sleep(0.1)
    return db["id"]

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--config", required=True); args = ap.parse_args()
    with open(args.config,"r",encoding="utf-8") as f: cfg = json.load(f)
    token = os.getenv("NOTION_TOKEN"); root = os.getenv("ROOT_PAGE_ID")
    if not token or not root: raise SystemExit("Missing NOTION_TOKEN/ROOT_PAGE_ID")
    # create IFNS root
    data = {"parent":{"type":"page_id","page_id": root},"properties":{"title":{"title":[{"text":{"content": cfg['ifns']['root_title']}}]}}}
    r = requests.post(f"{API}/pages", headers=hdrs(token), json=data, timeout=60); r.raise_for_status(); ifns_root = r.json()["id"]
    # pages (titles only; content can be added later via block append if needed)
    for p in cfg["ifns"]["pages"]:
        create_page(token, ifns_root, p["title"])
    # databases
    for d in cfg["ifns"]["databases"]:
        create_db_from_csv(token, ifns_root, d["title"], d["source"])
    print("IFNS sync done.")
if __name__ == "__main__": main()
