#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
IFNS - Sync Phase 4 Tables & Telemetry specs (GitHub -> Notion).

Structure in Notion:

IFNS – UI Master
  -> Tables & Telemetry (DB Hub)
       -> <one child page per .md file in docs/ifns/tables>

Each child page receives the full markdown content of its file.
"""

import os
import sys
from pathlib import Path
from typing import Optional, List, Tuple
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

IFNS_MASTER_TITLE = "IFNS \u2013 UI Master"
TABLES_HUB_TITLE = "Tables & Telemetry (DB Hub)"
TABLES_DIR = Path("docs/ifns/tables")


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
        "properties": {"title": {"title": [{"text": {"content": title}}]}},
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


def clear_page_content(page_id: str) -> None:
    blocks = get_children_blocks(page_id)
    if not blocks:
        return
    for block in blocks:
        bid = block.get("id")
        if not bid:
            continue
        url = f"https://api.notion.com/v1/blocks/{bid}"
        payload = {"archived": True}
        print(f"    - Archiving block {bid}")
        resp = requests.patch(url, headers=HEADERS, json=payload)
        try:
            resp.raise_for_status()
        except Exception as e:
            print(f"[WARN] archiving {bid} -> {e}", file=sys.stderr)
            print(resp.text, file=sys.stderr)


def chunk_text(text: str, max_len: int = 1500):
    chunks = []
    current = []
    current_len = 0
    for line in text.splitlines(True):  # keep line breaks
        if current_len + len(line) > max_len and current:
            chunks.append("".join(current))
            current = [line]
            current_len = len(line)
        else:
            current.append(line)
            current_len += len(line)
    if current:
        chunks.append("".join(current))
    return chunks


def write_page_markdown(page_id: str, md_text: str) -> None:
    chunks = chunk_text(md_text, max_len=1500)
    children_blocks = []
    for ch in chunks:
        children_blocks.append(
            {
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [{"type": "text", "text": {"content": ch}}],
                },
            }
        )
    url = f"https://api.notion.com/v1/blocks/{page_id}/children"
    payload = {"children": children_blocks}
    resp = requests.patch(url, headers=HEADERS, json=payload)
    try:
        resp.raise_for_status()
    except Exception as e:
        print(f"[ERROR] write_page_markdown({page_id}) -> {e}", file=sys.stderr)
        print(resp.text, file=sys.stderr)
        return
    total_chars = sum(len(b["paragraph"]["rich_text"][0]["text"]["content"]) for b in children_blocks)
    print(f"    -> Content updated ({total_chars} chars in {len(chunks)} block(s))")


def pretty_title_from_stem(stem: str) -> str:
    # Simple: turn underscores into spaces and strip.
    return stem.replace("_", " ").strip()


def main() -> None:
    print("IFNS - Sync Phase 4 Tables & Telemetry (GitHub -> Notion)")
    print(f"Root page id: {NOTION_ROOT_PAGE_ID}")
    print(f"Looking for '{IFNS_MASTER_TITLE}' under root...")

    master_id = find_child_page_recursive(NOTION_ROOT_PAGE_ID, IFNS_MASTER_TITLE, max_depth=4)
    if not master_id:
        print(f"ERROR: Could not find '{IFNS_MASTER_TITLE}' under root {NOTION_ROOT_PAGE_ID}", file=sys.stderr)
        sys.exit(1)
    print(f"Found IFNS  UI Master page id: {master_id}")

    if not TABLES_DIR.exists():
        print(f"ERROR: Tables dir not found at {TABLES_DIR}", file=sys.stderr)
        sys.exit(1)

    # Ensure hub
    hub_id = ensure_child_page(master_id, TABLES_HUB_TITLE)

    # Sync each .md file as a child under the hub
    md_files = sorted(TABLES_DIR.glob("*.md"))
    if not md_files:
        print(f"WARNING: No .md files found under {TABLES_DIR}")
    for path in md_files:
        stem = path.stem
        title = pretty_title_from_stem(stem)
        print(f"\n=== Syncing file '{path}' -> page '{title}' ===")
        page_id = ensure_child_page(hub_id, title)
        if not page_id:
            continue
        clear_page_content(page_id)
        md_text = path.read_text(encoding="utf-8")
        write_page_markdown(page_id, md_text)

    print("\nDone.")
    

if __name__ == "__main__":
    main()
