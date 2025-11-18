#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
IFNS - Sync Indicator Docs (Phases 1–7) into Notion.

Notion structure:

IFNS  UI Master
  -> Core ML Build Stages
       -> Stock Indicator System  Master Index
            -> Phase 1  Indicator Taxonomy & Governance
            -> Phase 2  Indicator Universe Draft
            -> Phase 3  L1 Indicator Catalog
            -> Phase 4  L2/L3 Framework Catalog
            -> Phase 5  Feature Output & Digitization Schema
            -> Phase 6  Implementation & Runtime Templates
            -> Phase 7  ML Integration & Operationalization

Sources in Git:

docs/ifns/indicators/*.md
"""

import os
import sys
from pathlib import Path
from typing import Optional, List, Tuple, Dict
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
COREML_HUB_TITLE = "Core ML Build Stages"
INDICATORS_MASTER_TITLE = "Stock Indicator System \u2013 Master Index"
INDICATORS_DIR = Path("docs/ifns/indicators")


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


def chunk_text(text: str, max_len: int = 1500) -> List[str]:
    chunks: List[str] = []
    current: List[str] = []
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


def find_file_by_token(token: str) -> Optional[Path]:
    token_lower = token.lower()
    for p in INDICATORS_DIR.glob("*.*"):
        if token_lower in p.name.lower():
            return p
    return None


def main() -> None:
    print("IFNS - Sync Indicator Docs (Phases 17)")
    print(f"Root page id: {NOTION_ROOT_PAGE_ID}")

    if not INDICATORS_DIR.exists():
        print(f"ERROR: indicators dir not found at {INDICATORS_DIR}", file=sys.stderr)
        sys.exit(1)

    # Find IFNS  UI Master
    master_id = find_child_page_recursive(NOTION_ROOT_PAGE_ID, IFNS_MASTER_TITLE, max_depth=4)
    if not master_id:
        print(f"ERROR: Could not find '{IFNS_MASTER_TITLE}' under root {NOTION_ROOT_PAGE_ID}", file=sys.stderr)
        sys.exit(1)
    print(f"Found IFNS  UI Master page id: {master_id}")

    # Find Core ML hub
    coreml_id = find_child_page_recursive(master_id, COREML_HUB_TITLE, max_depth=3)
    if not coreml_id:
        print(f"ERROR: Could not find '{COREML_HUB_TITLE}' under IFNS  UI Master.", file=sys.stderr)
        sys.exit(1)
    print(f"Found Core ML Build Stages hub id: {coreml_id}")

    # Ensure master indicators page
    indicators_master_id = ensure_child_page(coreml_id, INDICATORS_MASTER_TITLE)

    # Map files
    master_file = find_file_by_token("Master_Index")
    if master_file is None:
        print("!! Could not find Indicators_Master_Index file (token 'Master_Index').", file=sys.stderr)
    else:
        print(f"\n=== Syncing master index from '{master_file}' ===")
        clear_page_content(indicators_master_id)
        md = master_file.read_text(encoding="utf-8")
        write_page_markdown(indicators_master_id, md)

    phase_configs = [
        ("Phase 1  Indicator Taxonomy & Governance", "Taxonomy"),
        ("Phase 2  Indicator Universe Draft", "Universe"),
        ("Phase 3  L1 Indicator Catalog", "L1_Catalog"),
        ("Phase 4  L2/L3 Framework Catalog", "L2L3"),
        ("Phase 5  Feature Output & Digitization Schema", "Feature_Schem"),
        ("Phase 6  Implementation & Runtime Templates", "Implementatio"),
        ("Phase 7  ML Integration & Operationalization", "ML_Integratio"),
    ]

    for title, token in phase_configs:
        print(f"\n=== Syncing {title} (token '{token}') ===")
        f = find_file_by_token(token)
        if f is None:
            print(f"  !! No file found in {INDICATORS_DIR} matching token '{token}', skipping.", file=sys.stderr)
            continue
        print(f"  -> Using file '{f.name}'")
        page_id = ensure_child_page(indicators_master_id, title)
        if not page_id:
            continue
        clear_page_content(page_id)
        md = f.read_text(encoding="utf-8")
        write_page_markdown(page_id, md)

    print("\nDone.")


if __name__ == "__main__":
    main()
