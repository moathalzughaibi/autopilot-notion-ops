#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
IFNS - Sync Phase 2 master pages (GitHub -> Notion)

Auto-discovers the three Markdown files anywhere under ./docs
and syncs them into child pages under "IFNS  UI Master":

- "UI Master Summary"
- "Steps Index"
- "Drafts & Working Notes"

Requires:
- NOTION_TOKEN
- NOTION_ROOT_PAGE_ID (Autopilot Hub root)
"""

import os
import sys
from pathlib import Path
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

# Use Unicode escape for the en-dash so source stays ASCII-safe.
IFNS_MASTER_TITLE = "IFNS \u2013 UI Master"

# Mapping: child page title -> filename stem we look for
PAGE_FILE_STEMS: Dict[str, str] = {
    "UI Master Summary": "IFNS_UI_Master_Summary",
    "Steps Index": "IFNS_UI_Steps_Index",
    "Drafts & Working Notes": "IFNS_UI_Drafts_and_Working_Notes",
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
            "title": {"title": [{"text": {"content": title}}]}
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


def clear_page_content(page_id: str) -> None:
    """Archive all existing blocks inside the child page."""
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
                    "rich_text": [
                        {
                            "type": "text",
                            "text": {"content": ch},
                        }
                    ]
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


def locate_markdown_file(stem: str) -> Optional[Path]:
    """
    Search under ./docs for a .md file whose name contains the given stem.
    Prefer:
      1) Files inside a folder named 'ifns'
      2) Exact stem match (ignoring case)
      3) Shorter paths
    """
    search_root = Path("docs")
    if not search_root.exists():
        print("ERROR: docs/ folder not found at project root.", file=sys.stderr)
        return None

    candidates: List[Path] = []
    for p in search_root.rglob("*.md"):
        if stem.lower() in p.name.lower():
            candidates.append(p)

    if not candidates:
        print(f"!! No file found for stem '{stem}' under docs/", file=sys.stderr)
        return None

    def score(p: Path) -> Tuple[int, int, int]:
        parts_lower = [part.lower() for part in p.parts]
        in_ifns = 0 if "ifns" in parts_lower else 1
        exact_stem = 0 if p.stem.lower() == stem.lower() else 1
        length = len(str(p))
        return (in_ifns, exact_stem, length)

    candidates.sort(key=score)
    chosen = candidates[0]
    print(f"  -> Using file '{chosen}' for stem '{stem}'")
    return chosen


def main() -> None:
    print("IFNS - Sync Phase 2 master pages (GitHub -> Notion)")
    print(f"Root page id: {NOTION_ROOT_PAGE_ID}")
    print(f"Looking for '{IFNS_MASTER_TITLE}' under root...")

    master_id = find_child_page_recursive(NOTION_ROOT_PAGE_ID, IFNS_MASTER_TITLE, max_depth=4)
    if not master_id:
        print(f"ERROR: Could not find '{IFNS_MASTER_TITLE}' under root {NOTION_ROOT_PAGE_ID}", file=sys.stderr)
        sys.exit(1)
    print(f"Found IFNS  UI Master page id: {master_id}")

    for title, stem in PAGE_FILE_STEMS.items():
        print(f"\n=== Syncing '{title}' (stem '{stem}') ===")
        md_path = locate_markdown_file(stem)
        if md_path is None:
            print(f"!! Skipping {title}: no matching file found under docs/", file=sys.stderr)
            continue

        page_id = ensure_child_page(master_id, title)
        if not page_id:
            continue
        clear_page_content(page_id)
        md_text = md_path.read_text(encoding="utf-8")
        write_page_markdown(page_id, md_text)

    print("\nDone.")


if __name__ == "__main__":
    main()
