#!/usr/bin/env python3
import os, json, argparse, subprocess, datetime
from notion_client import Client

ENC="utf-8-sig"
AREAS=[("sync/ifns/","Data (sync/ifns)"),("docs/ifns/","Docs (docs/ifns)"),("IFNS_Notion_DB_Buildout_V2/","Buildout scripts")]

def load_cfg(p): return json.load(open(p,"r",encoding=ENC))

def git_log(since_days=30, max_commits=200):
    fmt="%H|%ad|%s"
    env=os.environ.copy()
    env["TZ"]="UTC"
    cmd=["git","log",f"--since={since_days}.days","--date=iso","--max-count",str(max_commits),"--name-status","--pretty=format:"+fmt]
    out=subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", env=env, check=True).stdout
    items=[]; current=None
    for line in out.splitlines():
        if "|" in line and line.count("|")==2 and len(line.split("|")[0])==40:
            h,dt,msg=line.split("|",2); current={"hash":h,"date":dt,"msg":msg,"files":[]}; items.append(current)
        elif line.strip() and current:
            parts=line.split("\t")
            if len(parts)>=2:
                status, path = parts[0], parts[1]
                current["files"].append((status, path))
    return items

def bucketize(files):
    buckets={label:[] for _,label in AREAS}; buckets["Other"]=[]
    for st,p in files:
        placed=False
        for prefix,label in AREAS:
            if p.startswith(prefix): buckets[label].append((st,p)); placed=True; break
        if not placed: buckets["Other"].append((st,p))
    return {k:v for k,v in buckets.items() if v}

def find_or_create_page(notion, root_id, title):
    res=notion.search(query=title, filter={"value":"page","property":"object"})
    for obj in res.get("results",[]):
        if obj.get("object")=="page": return obj["id"]
    page=notion.pages.create(parent={"type":"page_id","page_id":root_id},
                             properties={"title":{"title":[{"type":"text","text":{"content":title}}]}})
    return page["id"]

def list_child_blocks(notion, page_id):
    kids=[]; cursor=None
    while True:
        resp = notion.blocks.children.list(block_id=page_id, start_cursor=cursor) if cursor else notion.blocks.children.list(block_id=page_id)
        kids.extend([b for b in resp.get("results",[])])
        cursor = resp.get("next_cursor")
        if not resp.get("has_more"): break
    return kids

def append(notion, page_id, blocks):
    notion.blocks.children.append(block_id=page_id, children=blocks)

def block_heading(txt):
    return {"object":"block","type":"heading_2","heading_2":{"rich_text":[{"type":"text","text":{"content":txt}}]}}

def block_bullet(txt):
    return {"object":"block","type":"bulleted_list_item","bulleted_list_item":{"rich_text":[{"type":"text","text":{"content":txt}}]}}

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--config", default="IFNS_Notion_DB_Buildout_V2/config/ifns_v2_db_map.json")
    ap.add_argument("--root_title", default="IFNS  UI Master (V2)")
    ap.add_argument("--since_days", type=int, default=30)
    ap.add_argument("--max_commits", type=int, default=200)
    args=ap.parse_args()

    token=os.environ.get("NOTION_TOKEN"); root=os.environ.get("NOTION_ROOT_PAGE_ID")
    if not token: raise SystemExit("NOTION_TOKEN not set")
    notion=Client(auth=token)

    if not root:
        res=notion.search(query=args.root_title, filter={"value":"page","property":"object"})
        root=next((o["id"] for o in res.get("results",[]) if o.get("object")=="page"), None)
        if not root: raise SystemExit("V2 root not found")

    page_id = find_or_create_page(notion, root, "Change Log (V1  V2 deltas)")

    # Create a new dated section (we append; previous sections remain)
    now=datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
    append(notion, page_id, [block_heading(f"Snapshot @ {now}")])

    for item in git_log(args.since_days, args.max_commits):
        buckets = bucketize(item["files"])
        if not buckets: continue
        # commit header
        append(notion, page_id, [block_bullet(f"{item['date'][:16]}  {item['msg']}")])
        # per-area bullets
        for label, files in buckets.items():
            append(notion, page_id, [block_bullet(f"  {label}:")])
            append(notion, page_id, [block_bullet(f"    " + "; ".join([f"{st} {p}" for st,p in files]) )])

    print("Change Log updated.")
if __name__=="__main__": main()
