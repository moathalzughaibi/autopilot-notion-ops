#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
IFNS - Ensure Step pages exist under IFNS – UI Master.

- Uses NOTION_TOKEN and NOTION_ROOT_PAGE_ID from the environment.
- Finds the "IFNS  UI Master" page.
- Ensures that Step 01..14 pages exist as child pages.
"""

import os
import sys
from typing import Dict, Optional, List, Tuple
from collections import deque

import requests

NOTION_TOKEN = os.environ.get("NOTION_TOKEN")
NOTION_ROOT_PAGE_ID = os.environ.get("NOTION_ROOT_PAGE_ID")

if not NOTION_TOKEN:
    print("ERROR: NOTION_TOKEN environment variable is not set.", file=sys.stderr)
    sys.exit(1)

if not NOTION_ROOT_PAGE_ID:
    print("ERROR: NOTION_ROOT_PAGE_ID environment variable is not set.", file=sys.stderr)
    sys.exit(1)

HEADERS = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json",
}

# Use Unicode escape for the en-dash so the source stays ASCII-safe.
IFNS_MASTER_TITLE = "IFNS \u2013 UI Master"

# Titles of the Step pages we want under IFNS  UI Master.
STEP_TITLES: Dict[int, str] = {
    1:  "Step 01 \u2013 Preface Integration",
    2:  "Step 02 \u2013 Executive Summary",
    3:  "Step 03 \u2013 Visionary\u2013Technical Overview",
    4:  "Step 04 \u2013 Preface Timeline",
    5:  "Step 05 \u2013 Section 1.0 \u2013 Introduction",
    6:  "Step 06 \u2013 Section 2.0 \u2013 System Architecture",
    7:  "Step 07 \u2013 Section 3.0 \u2013 Data Intelligence Layer",
    8:  "Step 08 \u2013 Section 4.0 \u2013 Modeling Intelligence",
    9:  "Step 09 \u2013 Section 5.0 \u2013 Execution Intelligence",
    10: "Step 10 \u2013 Section 6.0 \u2013 Market Structural Awareness",
    11: "Step 11 \u2013 Section 7.0 \u2013 Model & Signal Integration",
    12: "Step 12 \u2013 Section 8.0 \u2013 Decision & Risk Architecture",
    13: "Step 13 \u2013 Section 9.0 \u2013 Self-Evaluation & Learning",
    14: "Step 14 \u2013 Sections 11.0\u201314.0 \u2013 Advanced Awareness",
}


def get_children_blocks(block_id: str) -> List[dict]:
    url = f"https://api.notion.com/v1/blocks/{block_id}/children"
    results: List[dict] = []
    start_cursor: Optional[str] = None

    while True:
        params = {}
        if start_cursor:
            params["start_cursor"] = start_cursor
        resp = requests.get(url, headers=HEADERS, params=params)
        try:
            resp.raise_for_status()
        except Exception as e:
            print(f"[ERROR] get_children_blocks({block_id}) -> {e}", file=sys.stderr)
            print(resp.text, file=sys.stderr)
            break
        data = resp.json()
        results.extend(data.get("results", []))
        if not data.get("has_more"):
            break
        start_cursor = data.get("next_cursor")
    return results


def list_child_pages(parent_id: str) -> List[Tuple[str, str]]:
    pages: List[Tuple[str, str]] = []
    for block in get_children_blocks(parent_id):
        if block.get("type") == "child_page":
            title = block.get("child_page", {}).get("title", "")
            pages.append((block.get("id"), title))
    return pages


def find_child_page_recursive(root_id: str, target_title: str, max_depth: int = 4) -> Optional[str]:
    queue = deque([(root_id, 0)])
    visited = set()

    while queue:
        current_id, depth = queue.popleft()
        if current_id in visited or depth > max_depth:
            continue
        visited.add(current_id)

        children = get_children_blocks(current_id)
        for block in children:
            if block.get("type") == "child_page":
                title = block.get("child_page", {}).get("title", "")
                if title.strip() == target_title:
                    return block.get("id")
                queue.append((block.get("id"), depth + 1))
    return None


def ensure_child_page(parent_id: str, title: str) -> str:
    existing = list_child_pages(parent_id)
    for cid, t in existing:
        if t.strip() == title.strip():
            print(f"= Exists: {title} ({cid})")
            return cid

    print(f"+ Creating: {title}")
    url = "https://api.notion.com/v1/pages"
    payload = {
        "parent": {"page_id": parent_id},
        "properties": {
            "title": {
                "title": [{"text": {"content": title}}],
            }
        },
    }
    resp = requests.post(url, headers=HEADERS, json=payload)
    try:
        resp.raise_for_status()
    except Exception as e:
        print(f"[ERROR] creating page '{title}' -> {e}", file=sys.stderr)
        print(resp.text, file=sys.stderr)
        return ""
    data = resp.json()
    cid = data.get("id", "")
    print(f"  -> Created page id={cid}")
    return cid


def main() -> None:
    print("IFNS - Ensure Step pages under IFNS  UI Master")
    print(f"Root page id: {NOTION_ROOT_PAGE_ID}")
    print(f"Looking for '{IFNS_MASTER_TITLE}' under root...")

    master_id = find_child_page_recursive(NOTION_ROOT_PAGE_ID, IFNS_MASTER_TITLE, max_depth=4)
    if not master_id:
        print(f"ERROR: Could not find '{IFNS_MASTER_TITLE}' under root {NOTION_ROOT_PAGE_ID}", file=sys.stderr)
        sys.exit(1)
    print(f"Found IFNS  UI Master page id: {master_id}")

    for step_num in sorted(STEP_TITLES.keys()):
        title = STEP_TITLES[step_num]
        ensure_child_page(master_id, title)

    print("\nDone ensuring Step pages.")


if __name__ == "__main__":
    main()
