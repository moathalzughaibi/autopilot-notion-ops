#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
IFNS - Update Index & Troubleshooting for Indicator System docs (Phases 1–7).

Adds rows to docs/IFNS_Notion_Page_Index.md for:
- Stock Indicator System – Master Index
- All child phase pages under that master

And appends a Troubleshooting entry once.
"""

import os
import sys
from pathlib import Path
from typing import List, Tuple, Optional, Set
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

INDEX_PATH = Path("docs/IFNS_Notion_Page_Index.md")
LOG_PATH = Path("docs/IFNS_Troubleshooting_Log.md")


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


def load_existing_index_ids() -> Tuple[int, Set[str]]:
    max_idx = 0
    ids: Set[str] = set()
    if not INDEX_PATH.exists():
        return 0, ids
    text = INDEX_PATH.read_text(encoding="utf-8")
    for line in text.splitlines():
        if not line.startswith("|"):
            continue
        parts = [p.strip() for p in line.split("|")[1:-1]]
        if not parts:
            continue
        try:
            serial = int(parts[0])
            if serial > max_idx:
                max_idx = serial
        except ValueError:
            pass
        if len(parts) >= 3:
            pid = parts[2]
            if pid:
                ids.add(pid)
    return max_idx, ids


def append_index_rows(coreml_id: str, indicators_master_id: str, phases: List[Tuple[str, str]]) -> None:
    max_idx, existing_ids = load_existing_index_ids()
    next_idx = max_idx + 1
    lines: List[str] = []

    # Master row
    if indicators_master_id not in existing_ids:
        line = (
            f"| {next_idx} | {INDICATORS_MASTER_TITLE} | {indicators_master_id} | {COREML_HUB_TITLE} |  | "
            f"Master index for the Stock Indicator System (Phases 17) under Core ML Build Stages. | "
            f"Content synced from `docs/ifns/indicators/Indicators_Master_Index_*.md` via `ifns_sync_indicators_docs.py`. |"
        )
        lines.append(line)
        existing_ids.add(indicators_master_id)
        next_idx += 1

    # Phase rows
    for pid, title in phases:
        if pid in existing_ids:
            continue
        line = (
            f"| {next_idx} | {title} | {pid} | {INDICATORS_MASTER_TITLE} |  | "
            f"Indicator phase spec page (see matching .md in `docs/ifns/indicators`). | Auto-synced. |"
        )
        lines.append(line)
        existing_ids.add(pid)
        next_idx += 1

    if not lines:
        print("No new index rows to append.")
        return

    with INDEX_PATH.open("a", encoding="utf-8") as f:
        f.write("\n" + "\n".join(lines) + "\n")
    print(f"Appended {len(lines)} row(s) to {INDEX_PATH}")


def append_troubleshooting_entry() -> None:
    heading = "## 2025-11-18  Indicator System (Phases 17) docs sync"
    if LOG_PATH.exists():
        text = LOG_PATH.read_text(encoding="utf-8")
        if heading in text:
            print("Troubleshooting entry for indicators already exists, skipping.")
            return

    entry = f"""
{heading}

| Field    | Details |
|---------|---------|
| **Area** | Indicator System docs (Phases 17) under Core ML Build Stages |
| **Symptom** | N/A (design + initial sync). The indicator docs for Phases 17 and the master index are now synced from Git (`docs/ifns/indicators`) into Notion under `Stock Indicator System  Master Index`. |
| **Context** | Indicator spec files are stored as Markdown under `docs/ifns/indicators`. `ifns_sync_indicators_docs.py` finds IFNS  UI Master, Core ML Build Stages, then ensures `Stock Indicator System  Master Index` and its phase child pages, replacing their content from the Git-backed files. |
| **Root cause** | Need a dedicated, structured home in Notion for all indicator-system documentation that ties directly into the Core ML Build Stages spine. |
| **Fix** | Implemented `scripts/ifns_sync_indicators_docs.py` and `scripts/ifns_update_index_and_log_indicators.py` so indicator docs can be safely round-tripped between Git and Notion with clear indexing and audit trail. |
| **Prevent / lessons** | 1) Keep doc files grouped under `docs/ifns/indicators` with stable naming. 2) Use a single master page (`Stock Indicator System  Master Index`) with phase child pages for navigation. 3) Always run the index/log updater after structural changes so future agents have a reliable map. |
| **Commands** | `.\local_env\\notion_env.ps1` then `python .\\scripts\\ifns_sync_indicators_docs.py` and `python .\\scripts\\ifns_update_index_and_log_indicators.py`. |
"""
    with LOG_PATH.open("a", encoding="utf-8") as f:
        f.write("\n" + entry.strip() + "\n")
    print(f"Appended indicators troubleshooting entry to {LOG_PATH}")


def main() -> None:
    print("IFNS - Update Index & Troubleshooting for Indicator System docs")
    print(f"Root page id: {NOTION_ROOT_PAGE_ID}")

    master_id = find_child_page_recursive(NOTION_ROOT_PAGE_ID, IFNS_MASTER_TITLE, max_depth=4)
    if not master_id:
        print(f"ERROR: Could not find '{IFNS_MASTER_TITLE}' under root {NOTION_ROOT_PAGE_ID}", file=sys.stderr)
        sys.exit(1)
    print(f"Found IFNS  UI Master page id: {master_id}")

    coreml_id = find_child_page_recursive(master_id, COREML_HUB_TITLE, max_depth=3)
    if not coreml_id:
        print(f"ERROR: Could not find '{COREML_HUB_TITLE}' under IFNS  UI Master.", file=sys.stderr)
        sys.exit(1)
    print(f"Found Core ML Build Stages hub id: {coreml_id}")

    indicators_master_id = find_child_page_recursive(coreml_id, INDICATORS_MASTER_TITLE, max_depth=2)
    if not indicators_master_id:
        print(f"ERROR: Could not find '{INDICATORS_MASTER_TITLE}' under Core ML Build Stages.", file=sys.stderr)
        sys.exit(1)
    print(f"Found indicators master page id: {indicators_master_id}")

    phase_pages = list_child_pages(indicators_master_id)
    print(f"Found {len(phase_pages)} child phase page(s) under indicators master.")

    append_index_rows(coreml_id, indicators_master_id, phase_pages)
    append_troubleshooting_entry()
    print("Done.")


if __name__ == "__main__":
    main()
