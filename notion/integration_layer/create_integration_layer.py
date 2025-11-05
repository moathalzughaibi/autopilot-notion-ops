import os, sys, time
from notion_client import Client

NOTION_TOKEN = os.environ.get("NOTION_TOKEN", "")
ROOT_PAGE_ID = os.environ.get("ROOT_PAGE_ID", "")

if not NOTION_TOKEN:
    print("[integration] Missing NOTION_TOKEN"); sys.exit(1)
if not ROOT_PAGE_ID:
    print("[integration] Missing ROOT_PAGE_ID"); sys.exit(1)

notion = Client(auth=NOTION_TOKEN)

def log(msg: str):
    print(f"[integration] {time.strftime('%H:%M:%S')} {msg}", flush=True)

def find_db_by_title(title: str):
    """ابحث عن قاعدة بيانات بهذا العنوان مباشرة تحت صفحة الجذر."""
    # نستخدم search ثم نتحقق من parent
    resp = notion.search(query=title, filter={"value": "database", "property": "object"})
    for obj in resp.get("results", []):
        if obj.get("object") == "database":
            # تحقق من العنوان
            t = obj.get("title", [])
            plain = t[0]["plain_text"] if t and "plain_text" in t[0] else ""
            # تحقق أن الـ parent هو صفحة الجذر
            parent = obj.get("parent", {})
            is_under_root = parent.get("type") == "page_id" and parent.get("page_id") == ROOT_PAGE_ID
            if plain == title and is_under_root:
                return obj
    return None

def create_db(title: str, properties: dict):
    return notion.databases.create(
        parent={"type": "page_id", "page_id": ROOT_PAGE_ID},
        title=[{"type": "text", "text": {"content": title}}],
        properties=properties,
    )

def ensure_db(title: str, properties: dict):
    db = find_db_by_title(title)
    if db:
        log(f"Found DB: {title}")
        # لو أردت لاحقاً: notion.databases.update(...) لإضافة خصائص جديدة
        return db["id"]
    log(f"Creating DB: {title}")
    created = create_db(title, properties)
    return created["id"]

# === تعريف القواعد الثلاث ===

ARCH_TITLE = "Integration Architecture"
ARCH_PROPS = {
    "Name": {"title": {}},  # اسم المكون
    "Function": {"rich_text": {}},  # الوظيفة
    "Integration Point": {"multi_select": {"options": [
        {"name": "GitHub Actions", "color": "blue"},
        {"name": "Notion API", "color": "green"},
        {"name": "Runpod", "color": "purple"},
    ]}},
    "Status": {"status": {"options": [
        {"name": "Active", "color": "green"},
        {"name": "Planned", "color": "yellow"},
        {"name": "Paused", "color": "red"},
    ]}},
    "Notes": {"rich_text": {}},
}

FLOW_TITLE = "Data Flow"
FLOW_PROPS = {
    "Name": {"title": {}},              # وصف التدفق (مثلاً: CSVs → Notion)
    "Source": {"rich_text": {}},
    "Destination": {"rich_text": {}},
    "Data Type": {"select": {"options": [
        {"name": "Structured", "color": "blue"},
        {"name": "Text", "color": "gray"},
        {"name": "Metrics", "color": "green"},
    ]}},
    "Frequency": {"select": {"options": [
        {"name": "On Push", "color": "blue"},
        {"name": "Hourly", "color": "orange"},
        {"name": "Daily", "color": "green"},
        {"name": "Manual", "color": "gray"},
    ]}},
    "Transport": {"select": {"options": [
        {"name": "GitHub Action", "color": "purple"},
        {"name": "API", "color": "green"},
        {"name": "Webhook", "color": "yellow"},
    ]}},
    "Notes": {"rich_text": {}},
}

FAILOVER_TITLE = "Failover Plan"
FAILOVER_PROPS = {
    "Name": {"title": {}},   # العنصر/المكوّن
    "Failure Type": {"select": {"options": [
        
        {"name": "Auth", "color": "red"},
        {"name": "RateLimit", "color": "yellow"},
        {"name": "Outage", "color": "gray"},
    ]}},
    "Impact": {"select": {"options": [
        {"name": "High", "color": "red"},
        {"name": "Medium", "color": "yellow"},
        {"name": "Low", "color": "green"},
    ]}},
    "Contingency": {"rich_text": {}},
    "Priority": {"select": {"options": [
        {"name": "P1", "color": "red"},
        {"name": "P2", "color": "orange"},
        {"name": "P3", "color": "green"},
    ]}},
    "Owner": {"people": {}},
}

def main():
    arch_id = ensure_db(ARCH_TITLE, ARCH_PROPS)
    flow_id = ensure_db(FLOW_TITLE, FLOW_PROPS)
    fail_id = ensure_db(FAILOVER_TITLE, FAILOVER_PROPS)

    log(f"Ready ✅  Architecture={arch_id} | DataFlow={flow_id} | Failover={fail_id}")
    log("You can start adding rows or letting future automations fill them in.")

if __name__ == "__main__":
    main()
