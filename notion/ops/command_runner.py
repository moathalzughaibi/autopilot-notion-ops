import os, json, time, sys, subprocess
from notion_client import Client

TOKEN = os.environ.get("NOTION_TOKEN","")
ROOT  = os.environ.get("ROOT_PAGE_ID","")
REPO  = os.environ.get("REPO","")
if not TOKEN or not ROOT: 
    print("[ops] Missing NOTION_TOKEN/ROOT_PAGE_ID"); sys.exit(1)

notion = Client(auth=TOKEN)

def pt(s): return [{"type":"text","text":{"content":str(s)}}]

def find_db_by_title(title: str):
    resp = notion.search(query=title, filter={"value":"database","property":"object"})
    for obj in resp.get("results", []):
        if obj.get("object")=="database":
            tarr = obj.get("title",[])
            plain = tarr[0]["plain_text"] if tarr and "plain_text" in tarr[0] else ""
            parent = obj.get("parent",{})
            if plain == title and parent.get("type")=="page_id" and parent.get("page_id")==ROOT:
                return obj
    return None

def get_queue():
    db = find_db_by_title("Ops_Command_Queue")
    if not db:
        print("[ops] Queue DB not found under ROOT: Ops_Command_Queue"); return []
    # فلترة الصفوف الجديدة
    resp = notion.databases.query(database_id=db["id"], filter={
        "property":"Status","status":{"equals":"New"}
    })
    return db, resp.get("results",[])

def update_status(page_id, status, result=""):
    notion.pages.update(page_id=page_id, properties={
        "Status": {"status":{"name": status}},
        "Result": {"rich_text": pt(result) if result else []}
    })

def run_sync_workflow():
    # مثال: استدعاء وركفلو sync الموجود عندك (بالاسم)
    wf_file = "notion-sync.yml"
    # gh api يحتاج توكن GITHUB_TOKEN المدمج
    cmd = [
        "bash","-lc",
        f'gh api repos/{REPO}/actions/workflows/{wf_file}/dispatches '
        f'-X POST -F ref=main'
    ]
    return subprocess.run(cmd, capture_output=True, text=True)

def add_page(payload: dict):
    """payload: {"db_title":"Autopilot_Architecture_Notes","props":{"Name":"X","Key":"Y"}}"""
    from notion.tools.add_page import norm_props  # أعد استخدام الدالة إن وجدت
    db_title = payload.get("db_title")
    props_in = payload.get("props",{})
    db = find_db_by_title(db_title)
    if not db:
        return False, f"DB not found: {db_title}"
    # تحضير خصائص مرنة (لو ما عندك norm_props انسخ المنطق المكافئ من quick-add)
    db_props = db.get("properties",{})
    title_prop = next((k for k,v in db_props.items() if v.get("type")=="title"), "Name")
    props = {}
    title_val = props_in.get("Name") or props_in.get("Title") or props_in.get(title_prop) or "New Page"
    props[title_prop] = {"title": pt(title_val)}
    for k,v in props_in.items():
        if k == title_prop: continue
        t = db_props.get(k,{}).get("type","rich_text")
        if t == "select": props[k] = {"select":{"name": str(v)}}
        elif t == "multi_select":
            arr = v if isinstance(v,(list,tuple)) else [v]
            props[k] = {"multi_select":[{"name":str(x)} for x in arr]}
        elif t == "status": props[k] = {"status":{"name":str(v)}}
        else: props[k] = {"rich_text": pt(v)}
    notion.pages.create(parent={"database_id": db["id"]}, properties=props)
    return True, "Page added"

def handle(cmd: str, payload_raw: str):
    try:
        payload = json.loads(payload_raw) if payload_raw else {}
    except Exception as e:
        return False, f"Bad payload JSON: {e}"

    if cmd == "sync":
        r = run_sync_workflow()
        ok = (r.returncode == 0)
        return ok, (r.stdout or r.stderr)
    if cmd == "add_page":
        return add_page(payload)
    if cmd == "backup":
        # يمكنك استدعاء backup بنفس أسلوب sync
        return True, "TODO: backup triggered"
    return False, f"Unknown command: {cmd}"

def main():
    q = get_queue()
    if not q: return
    db, rows = q
    for row in rows:
        page_id = row["id"]
        props = row.get("properties",{})
        cmd = props.get("Command",{}).get("select",{}).get("name","")
        payload = "".join([r.get("plain_text","") for r in props.get("Payload",{}).get("rich_text",[])])
        update_status(page_id, "Running")
        ok, res = handle(cmd, payload)
        update_status(page_id, "Done" if ok else "Error", res[:1800])
        time.sleep(1)

if __name__ == "__main__":
    main()
