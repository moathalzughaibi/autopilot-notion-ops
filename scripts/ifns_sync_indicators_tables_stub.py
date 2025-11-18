#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
IFNS - Sync Indicator CSV anchors into Tables & Telemetry (DB Hub).

Notion structure:

IFNS – UI Master
  -> Tables & Telemetry (DB Hub)
       -> Indicators  Universe Catalog (Phase 2 Draft)
       -> Indicators  L1 Catalog (Phase 3)
       -> Indicators  L2/L3 Framework Catalog (Phase 4)
       -> Indicator Feature Schema v1 (Phase 5)

Each page contains a stub pointing to the CSV under sync/ifns.
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
SYNC_DIR = Path("sync/ifns")


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
    for line in text.splitlines(True):
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


def find_csv(token: str) -> Optional[Path]:
    token_lower = token.lower()
    for p in SYNC_DIR.glob("*.csv"):
        if token_lower in p.name.lower():
            return p
    return None


def build_stub(title: str, path: Path, purpose: str) -> str:
    return f"""# {title}

This page represents an indicator table used in the IFNS pipeline.

- **File name:** `{path.name}`
- **Path in repo:** `sync/ifns/{path.name}`

**Purpose**

{purpose}

**Notes for next agent**

- Treat this CSV as the source-of-truth for this indicator layer.
- When building Notion databases, use this file as the backing dataset.
- Map each column in the CSV to a Notion property (type, description, constraints).
"""


def main() -> None:
    print("IFNS - Sync Indicator CSV anchors into Tables & Telemetry (DB Hub)")
    print(f"Root page id: {NOTION_ROOT_PAGE_ID}")

    if not SYNC_DIR.exists():
        print(f"ERROR: sync dir not found at {SYNC_DIR}", file=sys.stderr)
        sys.exit(1)

    master_id = find_child_page_recursive(NOTION_ROOT_PAGE_ID, IFNS_MASTER_TITLE, max_depth=4)
    if not master_id:
        print(f"ERROR: Could not find '{IFNS_MASTER_TITLE}' under root {NOTION_ROOT_PAGE_ID}", file=sys.stderr)
        sys.exit(1)
    print(f"Found IFNS  UI Master page id: {master_id}")

    hub_id = find_child_page_recursive(master_id, TABLES_HUB_TITLE, max_depth=3)
    if not hub_id:
        print(f"ERROR: Could not find hub '{TABLES_HUB_TITLE}' under IFNS  UI Master.", file=sys.stderr)
        sys.exit(1)
    print(f"Found Tables & Telemetry hub id: {hub_id}")

    configs = [
        (
            "Indicators  Universe Catalog (Phase 2 Draft)",
            "universe_cata",
            "Phase 2 universe draft: all candidate indicators before pruning and promotion into L1."
        ),
        (
            "Indicators  L1 Catalog (Phase 3)",
            "catalog_l1",
            "Phase 3 L1 atomic indicator catalog: cleaned, deduped, and named metrics used directly by models."
        ),
        (
            "Indicators  L2/L3 Framework Catalog (Phase 4)",
            "catalog_l2l3",
            "Phase 4 L2/L3 catalog: higher-level frameworks/regimes composed from L1 indicators."
        ),
        (
            "Indicator Feature Schema v1 (Phase 5)",
            "feature_schema",
            "Phase 5 feature schema: final columns/features that the ML model sees (bins, scaling, types)."
        ),
    ]

    for title, token, purpose in configs:
        print(f"\n=== Syncing '{title}' (token '{token}') ===")
        csv_path = find_csv(token)
        if csv_path is None:
            print(f"  !! No CSV found in {SYNC_DIR} matching token '{token}', skipping.", file=sys.stderr)
            continue
        print(f"  -> Using CSV '{csv_path.name}'")
        page_id = ensure_child_page(hub_id, title)
        if not page_id:
            continue
        clear_page_content(page_id)
        stub = build_stub(title, csv_path, purpose)
        write_page_markdown(page_id, stub)

    print("\nDone.")


if __name__ == "__main__":
    main()
