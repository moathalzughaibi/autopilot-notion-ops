#!/usr/bin/env python3
import os, argparse
from notion_client import Client

def find_page(notion, title):
    r=notion.search(query=title, filter={"value":"page","property":"object"})
    for o in r.get("results",[]):
        if o.get("object")=="page" and o["properties"]["title"]["title"]:
            if o["properties"]["title"]["title"][0]["plain_text"]==title:
                return o["id"]

def find_db(notion, title):
    r=notion.search(query=title, filter={"value":"database","property":"object"})
    for o in r.get("results",[]):
        if o.get("object")=="database": return o["id"]

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--home_title", default="Operator Home")
    ap.add_argument("--playbook_title", default="Saved Views Playbook")
    ap.add_argument("--admin_db_title", default="Admin Config Index")
    a=ap.parse_args()

    token=os.environ.get("NOTION_TOKEN")
    if not token: raise SystemExit("NOTION_TOKEN missing")
    notion=Client(auth=token)

    home = find_page(notion, a.home_title)
    pb = find_page(notion, a.playbook_title)
    adm = find_db(notion, a.admin_db_title)
    blocks=[]
    if pb:
        blocks.append({"object":"block","type":"callout","callout":{"icon":{"type":"emoji","emoji":""},"rich_text":[{"type":"text","text":{"content":"Open Saved Views Playbook"}}]}})
        blocks.append({"object":"block","type":"link_to_page","link_to_page":{"type":"page_id","page_id":pb}})
    if adm:
        blocks.append({"object":"block","type":"callout","callout":{"icon":{"type":"emoji","emoji":""},"rich_text":[{"type":"text","text":{"content":"Admin Config Index"}}]}})
        blocks.append({"object":"block","type":"link_to_page","link_to_page":{"type":"database_id","database_id":adm}})
    if home and blocks:
        notion.blocks.children.append(block_id=home, children=blocks)
        print("Operator Home: quick links added.")
    else:
        print("Nothing to add (home/playbook/admin not found).")

if __name__=="__main__": main()
