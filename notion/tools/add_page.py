import os, json, sys, time
from notion_client import Client

token = os.environ.get("NOTION_TOKEN","")
root  = os.environ.get("ROOT_PAGE_ID","")
title = os.environ.get("DB_TITLE","").strip()
props_json = os.environ.get("PROPS_JSON","{}")

if not token or not root or not title:
    print("[quick-add] Missing env (NOTION_TOKEN/ROOT_PAGE_ID/DB_TITLE)"); sys.exit(1)

try:
    user_props = json.loads(props_json)
except Exception as e:
    print(f"[quick-add] Bad JSON: {e}"); sys.exit(1)

notion = Client(auth=token)

def pt(text): return [{"type":"text","text":{"content":str(text)}}]

def norm_props(db, user_props):
    """حوّل dict بسيط إلى خصائص Notion الصحيحة بحسب أنواع الحقول.
       العنوان نبحث عنه تلقائيًا (أول حقل type=title). بقية الحقول تُعبّأ كـ rich_text افتراضيًا."""
    props = {}
    db_props = db.get("properties",{})
    title_prop_name = None
    for k,v in db_props.items():
        if v.get("type")=="title":
            title_prop_name = k; break
    if not title_prop_name:
        # fallback اسم شائع
        title_prop_name = "Name"

    # عين العنوان
    title_val = user_props.get("Name") or user_props.get("Title") or user_props.get(title_prop_name) or "New Page"
    props[title_prop_name] = {"title": pt(title_val)}

    # بقية الحقول
    for k,v in user_props.items():
        if k == title_prop_name: 
            continue
        meta = db_props.get(k, {"type":"rich_text"})
        t = meta.get("type","rich_text")
        if t == "select":
            props[k] = {"select": {"name": str(v)}}
        elif t == "multi_select":
            if isinstance(v, (list, tuple)):
                props[k] = {"multi_select": [{"name": str(x)} for x in v]}
            else:
                props[k] = {"multi_select": [{"name": str(v)}]}
        elif t == "status":
            props[k] = {"status": {"name": str(v)}}
        elif t == "people":
            # بدون lookups لناس محددين: فقط نتجاهله افتراضيًا
            continue
        else:
            props[k] = {"rich_text": pt(v)}
    return props

def find_db_by_title(t):
    resp = notion.search(query=t, filter={"value":"database","property":"object"})
    for obj in resp.get("results", []):
        if obj.get("object")=="database":
            # طابق العنوان
            title_arr = obj.get("title",[])
            plain = title_arr[0]["plain_text"] if title_arr and "plain_text" in title_arr[0] else ""
            # ضمن الجذر؟
            parent = obj.get("parent",{})
            under_root = parent.get("type")=="page_id" and parent.get("page_id")==root
            if plain==t and under_root:
                return obj
    return None

def main():
    db = find_db_by_title(title)
    if not db:
        print(f"[quick-add] DB not found under ROOT: {title}"); sys.exit(1)
    props = norm_props(db, user_props)
    notion.pages.create(parent={"database_id": db["id"]}, properties=props)
    print("[quick-add] Added ✔")

if __name__ == "__main__":
    main()
