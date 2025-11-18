#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
IFNS - Update Index & Troubleshooting for Phase 4 (Tables & Telemetry).

- Adds rows to docs/IFNS_Notion_Page_Index.md for:
  - Tables & Telemetry (DB Hub)
  - Each child page under that hub

- Appends a Phase 4 entry to docs/IFNS_Troubleshooting_Log.md (idempotent).
"""

import os
import sys
from pathlib import Path
from typing import List, Tuple, Optional, Dict
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


def load_existing_index_ids() -> Tuple[int, set]:
    max_idx = 0
    ids = set()
    if not INDEX_PATH.exists():
        return 0, set()
    text = INDEX_PATH.read_text(encoding="utf-8")
    for line in text.splitlines():
        if not line.startswith("|"):
            continue
        parts = [p.strip() for p in line.split("|")[1:-1]]
        if not parts:
            continue
        # parts[0] = serial, parts[2] = page_id by our convention
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


def append_index_rows(hub_id: str, hub_children: List[Tuple[str, str]]) -> None:
    max_idx, existing_ids = load_existing_index_ids()
    print(f"Current max index row: {max_idx}")
    print(f"Existing page IDs in index: {len(existing_ids)}")

    new_lines: List[str] = []
    next_idx = max_idx + 1

    # Hub row
    if hub_id not in existing_ids:
        hub_line = (
            f"| {next_idx} | {TABLES_HUB_TITLE} | {hub_id} | IFNS  UI Master |  | "
            f"Hub for CSV-backed databases and telemetry specs (Phase 4). | "
            f"Child pages synced from `docs/ifns/tables` via `ifns_sync_tables_phase4.py`. |"
        )
        new_lines.append(hub_line)
        existing_ids.add(hub_id)
        next_idx += 1

    # Child pages
    for pid, title in hub_children:
        if pid in existing_ids:
            continue
        line = (
            f"| {next_idx} | {title} | {pid} | {TABLES_HUB_TITLE} |  | "
            f"Phase 4 spec page under Tables & Telemetry (DB Hub). | Auto-synced from matching file in `docs/ifns/tables`. |"
        )
        new_lines.append(line)
        existing_ids.add(pid)
        next_idx += 1

    if not new_lines:
        print("No new index rows to append.")
        return

    with INDEX_PATH.open("a", encoding="utf-8") as f:
        f.write("\n" + "\n".join(new_lines) + "\n")
    print(f"Appended {len(new_lines)} row(s) to {INDEX_PATH}")


def append_troubleshooting_entry() -> None:
    heading = "## 2025-11-18  Phase 4  Tables & Telemetry (DB Hub) initial sync"
    if LOG_PATH.exists():
        text = LOG_PATH.read_text(encoding="utf-8")
        if heading in text:
            print("Troubleshooting entry for Phase 4 already exists, skipping.")
            return

    entry = f"""
{heading}

| Field    | Details |
|---------|---------|
| **Area** | Phase 4 Tables & Telemetry specs (docs/ifns/tables -> Notion pages) |
| **Symptom** | Initial runs showed `WARNING: No .md files found under docs\\\\ifns\\\\tables`. After updating the sync script to consider all files in that folder, the `Tables & Telemetry (DB Hub)` page gained one child page per spec file, with content replaced from the Git-backed files. |
| **Context** | Markdown/text specs for Phase 4 live under `docs/ifns/tables`. Script is run from repo root with Notion env loaded via `.\local_env\\notion_env.ps1`. Pages are created as children of `Tables & Telemetry (DB Hub)` and their content fully replaced each sync. |
| **Root cause** | The first version of the Phase 4 sync script filtered on `*.md` only, while the specs were not being picked up as expected. The updated script now lists all files in `docs/ifns/tables`, logs them, and syncs each one. |
| **Fix** | Overwrote `scripts/ifns_sync_tables_phase4.py` to enumerate all files under `docs/ifns/tables`, then re-ran the sync so each Phase 4 spec file became a Notion child page. |
| **Prevent / lessons** | 1) Prefer robust file discovery and logging when folder contents may change. 2) Keep Phase 4 specs isolated in `docs/ifns/tables` so the script can reliably discover them. 3) After each sync, update `IFNS_Notion_Page_Index.md` and this log via scripted operations. |
| **Commands** | `.\local_env\\notion_env.ps1` then `python .\\scripts\\ifns_sync_tables_phase4.py` and `python .\\scripts\\ifns_update_index_and_log_phase4.py`. |
"""
    with LOG_PATH.open("a", encoding="utf-8") as f:
        f.write("\n" + entry.strip() + "\n")
    print(f"Appended Phase 4 troubleshooting entry to {LOG_PATH}")


def main() -> None:
    print("IFNS - Update Index & Troubleshooting for Phase 4")
    print(f"Root page id: {NOTION_ROOT_PAGE_ID}")
    print(f"Looking for '{IFNS_MASTER_TITLE}' under root...")

    master_id = find_child_page_recursive(NOTION_ROOT_PAGE_ID, IFNS_MASTER_TITLE, max_depth=4)
    if not master_id:
        print(f"ERROR: Could not find '{IFNS_MASTER_TITLE}' under root {NOTION_ROOT_PAGE_ID}", file=sys.stderr)
        sys.exit(1)
    print(f"Found IFNS  UI Master page id: {master_id}")

    hub_id = find_child_page_recursive(master_id, TABLES_HUB_TITLE, max_depth=2)
    if not hub_id:
        print(f"ERROR: Could not find hub '{TABLES_HUB_TITLE}' under IFNS  UI Master.", file=sys.stderr)
        sys.exit(1)
    print(f"Found Tables & Telemetry hub id: {hub_id}")

    children = list_child_pages(hub_id)
    print(f"Found {len(children)} child page(s) under hub.")
    append_index_rows(hub_id, children)
    append_troubleshooting_entry()
    print("Done.")


if __name__ == "__main__":
    main()
