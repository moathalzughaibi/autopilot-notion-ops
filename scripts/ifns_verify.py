import os, argparse, requests, sys
from datetime import datetime

API = "https://api.notion.com/v1"
def hdrs(token): 
    return {"Authorization": f"Bearer {token}","Notion-Version":"2022-06-28","Content-Type":"application/json"}

def search(token, query):
    r = requests.post(f"{API}/search", headers=hdrs(token), json={"query": query}, timeout=60)
    r.raise_for_status()
    return r.json().get("results", [])

def page_title(page):
    props = page.get("properties", {})
    if "title" in props and props["title"]["title"]:
        return "".join([t.get("plain_text","") for t in props["title"]["title"]])
    return "(untitled)"

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root-title", required=True, help='Expected IFNS root page title')
    ap.add_argument("--out", default="reports/ifns_verification_report.md")
    args = ap.parse_args()

    token = os.getenv("NOTION_TOKEN")
    root_id = os.getenv("ROOT_PAGE_ID")
    if not token or not root_id:
        print("Missing NOTION_TOKEN / ROOT_PAGE_ID", file=sys.stderr)
        sys.exit(1)

    # 1) Find IFNS root page by title
    results = search(token, args.root_title)
    ifns_root = None
    for r in results:
        if r.get("object") == "page" and args.root_title.lower() in page_title(r).lower():
            ifns_root = r; break

    lines = []
    lines.append(f"# IFNS Verification Report\n")
    lines.append(f"- Generated: {datetime.utcnow().isoformat()}Z")
    lines.append(f"- Expected root title: **{args.root_title}**\n")

    if not ifns_root:
        lines.append("❌ Could not find IFNS root page by title.")
        open(args.out,"w",encoding="utf-8").write("\n".join(lines))
        print("Report written (root not found).")
        return

    lines.append(f"✅ Found IFNS root page: **{page_title(ifns_root)}** (id: `{ifns_root['id']}`)\n")

    # 2) Search for expected child pages/databases by known titles
    expected_pages = [
        "Conceptual Framework",
        "ML Operational Framework",
        "IFNS Main Dashboard – Wireframe",
        "Dashboard Analytics (Backtesting & Live Intelligence)",
        "Reference Library"
    ]
    expected_dbs = [
        "System Layers Tracker",
        "Backtest Results Table",
        "Experiment Logs",
        "Model Registry",
        "Portfolio Matrix",
        "Execution API Log",
        "RiskAPI Alerts"
    ]

    found_pages = {t: False for t in expected_pages}
    found_dbs = {t: False for t in expected_dbs}

    res_all = search(token, "IFNS")
    for r in res_all:
        if r.get("object") == "page":
            title = page_title(r)
            for t in expected_pages:
                if t.lower() in title.lower():
                    found_pages[t] = True
        elif r.get("object") == "database":
            # best-effort: Notion search includes DBs too
            title = r.get("title",[{}])[0].get("plain_text","") if r.get("title") else ""
            for t in expected_dbs:
                if t.lower() in title.lower():
                    found_dbs[t] = True

    lines.append("## Pages\n")
    for t, ok in found_pages.items():
        lines.append(f"- {'✅' if ok else '❌'} {t}")
    lines.append("\n## Databases\n")
    for t, ok in found_dbs.items():
        lines.append(f"- {'✅' if ok else '❌'} {t}")

    # 3) KPI/Health minimal presence check (best-effort via search)
    kpi_hits = search(token, "Neural Health Indicator")
    kpi_ok = any(x.get("object")=="page" for x in kpi_hits)
    lines.append("\n## KPI / Health Checks\n")
    lines.append(f"- {'✅' if kpi_ok else '❌'} Neural Health Indicator page/section present (via search)")

    out = args.out
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out,"w",encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"Wrote report to {out}")

if __name__ == "__main__":
    main()
