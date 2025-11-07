import os, json, argparse, requests
from datetime import datetime, timezone
from dateutil.parser import isoparse

API = "https://api.notion.com/v1"
NOTION_VERSION = "2022-06-28"

def headers(token):
    return {
        "Authorization": f"Bearer {token}",
        "Notion-Version": NOTION_VERSION,
        "Content-Type": "application/json"
    }

def search_db_by_title(token, title):
    r = requests.post(f"{API}/search", headers=headers(token), json={"query": title}, timeout=60)
    r.raise_for_status()
    for res in r.json().get("results",[]):
        if res.get("object")=="database":
            t = "".join([x.get("plain_text","") for x in res.get("title",[])])
            if title.lower() in (t or "").lower():
                return res["id"]
    return None

def query_db(token, db_id):
    payload = {"page_size": 25, "sorts":[{"timestamp":"created_time","direction":"descending"}]}
    r = requests.post(f"{API}/databases/{db_id}/query", headers=headers(token), json=payload, timeout=60)
    r.raise_for_status()
    return r.json().get("results", [])

def page_prop(props, name, kind):
    p = props.get(name, {})
    if kind=="title":
        return "".join([x.get("plain_text","") for x in p.get("title",[])])
    if kind=="select":
        return (p.get("select") or {}).get("name")
    if kind=="status":
        return (p.get("status") or {}).get("name")
    if kind=="rich_text":
        return "".join([x.get("plain_text","") for x in p.get("rich_text",[])])
    return None

def notion_page_url(page_id):
    return f"https://www.notion.so/{page_id.replace('-','')}"

def send_slack(webhook_url, payload):
    r = requests.post(webhook_url, json=payload, timeout=30)
    r.raise_for_status()

def send_email(subject, body):
    import smtplib, ssl
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    host = os.getenv("SMTP_HOST"); port = int(os.getenv("SMTP_PORT","587"))
    user = os.getenv("SMTP_USER"); pwd = os.getenv("SMTP_PASS")
    sender = os.getenv("EMAIL_FROM"); to = os.getenv("EMAIL_TO")
    if not (host and user and pwd and sender and to): 
        return
    msg = MIMEMultipart(); msg["From"]=sender; msg["To"]=to; msg["Subject"]=subject
    msg.attach(MIMEText(body, "plain", "utf-8"))
    ctx = ssl.create_default_context()
    with smtplib.SMTP(host, port) as s:
        s.starttls(context=ctx); s.login(user, pwd); s.sendmail(sender, [to], msg.as_string())

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--config", required=True); args = ap.parse_args()
    token = os.getenv("NOTION_TOKEN"); 
    if not token: raise SystemExit("Missing NOTION_TOKEN")
    cfg = json.load(open(args.config,"r",encoding="utf-8"))

    dbid = search_db_by_title(token, cfg["db_names"]["incident_log"])
    if not dbid: raise SystemExit("Incident Log DB not found")

    results = query_db(token, dbid)
    if not results: 
        print("No incidents found"); return

    page = results[0]; pid = page["id"]; props = page["properties"]
    title = page_prop(props, "title", "title") or "Incident"
    itype = page_prop(props, "Incident Type", "select") or "General"
    severity = page_prop(props, "Severity", "select") or "Info"
    created = page.get("created_time")
    created_utc = isoparse(created).strftime("%Y-%m-%d %H:%M UTC")
    url = notion_page_url(pid)

    # Slack payload
    wh = os.getenv("SLACK_WEBHOOK_URL")
    if wh:
        payload = {
          "text": "*IFNS Incident Alert*",
          "blocks": [
            {"type":"section","text":{"type":"mrkdwn","text":f"*{title}* — `{severity}`"}},
            {"type":"context","elements":[{"type":"mrkdwn","text":f"{created_utc} • {itype}" }]},
            {"type":"section","text":{"type":"mrkdwn","text":"Auto alert from IFNS Incident Webhook."}},
            {"type":"section","text":{"type":"mrkdwn","text":f"<{url}|Open Incident> • Reference Library / Weekly Snapshots"}}
          ]
        }
        send_slack(wh, payload)

    subject = f"[IFNS] {title} — {severity} — {created_utc}"
    body = f"IFNS Incident Alert\n\nTitle: {title}\nSeverity: {severity}\nType: {itype}\nDate (UTC): {created_utc}\nLink: {url}\n"
    send_email(subject, body)

    print("Notification sent for:", title)

if __name__ == "__main__":
    main()
