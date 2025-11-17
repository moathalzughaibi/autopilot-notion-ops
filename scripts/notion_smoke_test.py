#!/usr/bin/env python3
"""
Notion smoke test for Autopilot / IFNS

What it does:
- Reads NOTION_TOKEN from environment.
- Optionally reads NOTION_ROOT_PAGE_ID or ROOT_PAGE_ID.
- Calls Notion API to:
  1) List users (to verify the token works).
  2) If a root page ID is present, fetch that page and print its URL.

This script NEVER prints the token itself.
"""

import os
import sys
import requests

NOTION_TOKEN = os.environ.get("NOTION_TOKEN")
if not NOTION_TOKEN:
    print("ERROR: NOTION_TOKEN is not set in this shell.", file=sys.stderr)
    sys.exit(1)

root_page_id = (
    os.environ.get("NOTION_ROOT_PAGE_ID")
    or os.environ.get("ROOT_PAGE_ID")
)

HEADERS = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Notion-Version": "2022-06-28",
}

def test_users():
    url = "https://api.notion.com/v1/users"
    resp = requests.get(url, headers=HEADERS)
    if resp.status_code != 200:
        print(f"[FAIL] /v1/users -> {resp.status_code}")
        print(resp.text)
        return False

    data = resp.json()
    count = len(data.get("results", []))
    print(f"[OK] Notion token works. /v1/users returned {count} users.")
    return True

def test_root_page(page_id):
    if not page_id:
        print("[INFO] No NOTION_ROOT_PAGE_ID/ROOT_PAGE_ID set; skipping root page test.")
        return

    url = f"https://api.notion.com/v1/pages/{page_id}"
    resp = requests.get(url, headers=HEADERS)
    if resp.status_code != 200:
        print(f"[WARN] Could not fetch root page {page_id} -> {resp.status_code}")
        print(resp.text)
        return

    data = resp.json()
    url_field = data.get("url", "(no url field)")
    print(f"[OK] Root page reachable. id={page_id}")
    print(f"      Notion URL: {url_field}")

def main():
    print("=== Notion smoke test (Autopilot / IFNS) ===")
    test_users()
    test_root_page(root_page_id)
    print("=== Done ===")

if __name__ == "__main__":
    main()
