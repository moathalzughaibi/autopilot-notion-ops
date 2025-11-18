#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
IFNS - Sync all 14 Steps (GitHub -> Notion)

This script:
- Finds the "IFNS – UI Master" page under NOTION_ROOT_PAGE_ID.
- Visits its child pages titled "Step XX  ...".
- For each such page, if we have a markdown mapping for that step number,
  we split the markdown into sections 01/02/03 and sync them into:
    01  Narrative & Intent
    02  Implementation Reference
    03  Notes & Decisions.
"""

import os
import sys
import time
import re
from pathlib import Path
from typing import Dict, Optional, List
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

# Exact Notion page title, but using a Unicode escape so source stays ASCII
IFNS_MASTER_TITLE = "IFNS \u2013 UI Master"

STEP_FILES: Dict[int, str] = {
    1: "docs/ifns/Step_01_Preface_Integration.md",
    2: "docs/ifns/Step_02_Executive_Summary.md",
    3: "docs/ifns/Step_03_Visionary_Technical_Overview.md",
    4: "docs/ifns/Step_04_Preface_Timeline.md",
    5: "docs/ifns/Step_05_Introduction_Operational_Genesis.md",
    6: "docs/ifns/Step_06_System_Architecture.md",
    7: "docs/ifns/Step_07_Data_Intelligence_Layer_DIL.md",
    8: "docs/ifns/Step_08_Modeling_Intelligence_MI.md",
    9: "docs/ifns/Step_09_Execution_Intelligence_EI.md",
    10: "docs/ifns/Step_10_Market_Structural_Awareness_MSA.md",
    11: "docs/ifns/Step_11_Model_and_Signal_Integration_MSI.md",
    12: "docs/ifns/Step_12_Decision_and_Risk_Architecture_DRA.md",
    13: "docs/ifns/Step_13_Self_Evaluation_and_Learning_SEL.md",
    14: "docs/ifns/Step_14_Advanced_Awareness_and_Quantum_Cognition.md",
}

CHILD_TITLES: Dict[str, str] = {
    "01": "01 \u2013 Narrative & Intent",
    "02": "02 \u2013 Implementation Reference",
    "03": "03 \u2013 Notes & Decisions",
}


def split_sections(md_text: str) -> Dict[str, str]:
    """Split markdown into sections keyed by '01', '02', '03' headings."""
    pattern = re.compile(r"^##\s*(0[1-3])\b.*$", re.MULTILINE)
    matches = list(pattern.finditer(md_text))
    sections: Dict[str, str] = {}
    if not matches:
        return sections
    for i, match in enumerate(matches):
        sec = match.group(1)
        start = match.start()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(md_text)
        sections[sec] = md_text[start:end].strip()
    return sections


def get_children_blocks(block_id: str) -> List[dict]:
    """Return all direct child blocks of a page/block, with pagination."""
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


def find_child_page_recursive(root_id: str, target_title: str, max_depth: int = 4) -> Optional[str]:
    """Breadth-first search for a child_page with the given title under root_id."""
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


def list_child_pages(parent_id: str) -> List[tuple]:
    """Return list of (page_id, title) for direct child pages."""
    pages: List[tuple] = []
    for block in get_children_blocks(parent_id):
        if block.get("type") == "child_page":
            title = block.get("child_page", {}).get("title", "")
            pages.append((block.get("id"), title))
    return pages


def ensure_child_page(parent_id: str, code: str, full_title: str) -> Optional[str]:
    """Ensure a child page starting with code (01/02/03) exists; create if not."""
    children = list_child_pages(parent_id)
    for cid, title in children:
        if title.strip().startswith(code):
            print(f"  = Child exists for {code}: {title} ({cid})")
            return cid

    print(f"  + Creating child for {code}: {full_title}")
    url = "https://api.notion.com/v1/pages"
    payload = {
        "parent": {"page_id": parent_id},
        "properties": {
            "title": {"title": [{"text": {"content": full_title}}]}
        },
    }
    resp = requests.post(url, headers=HEADERS, json=payload)
    try:
        resp.raise_for_status()
    except Exception as e:
        print(f"[ERROR] create child {full_title} under {parent_id} -> {e}", file=sys.stderr)
        print(resp.text, file=sys.stderr)
        return None
    data = resp.json()
    cid = data.get("id")
    print(f"    -> Created child page id={cid}")
    return cid


def clear_page_content(page_id: str) -> None:
    """Archive all existing blocks under a child page before re-writing."""
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
        time.sleep(0.2)


def chunk_text(text: str, max_len: int = 1500) -> List[str]:
    """Split text into chunks so each paragraph block stays within limits."""
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
    """Write markdown text into a child page as multiple paragraph blocks."""
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


def sync_step(step_page_id: str, step_number: int, step_title: str) -> None:
    """Sync a single Step page (01..14) from its markdown file into Notion."""
    md_path = STEP_FILES.get(step_number)
    if not md_path:
        print(f"  !! No markdown file configured for step {step_number}, skipping.")
        return
    p = Path(md_path)
    if not p.exists():
        print(f"  !! Markdown file not found: {md_path}, skipping step {step_number}.", file=sys.stderr)
        return

    print(f"\n=== Step {step_number:02d} :: {step_title} ===")
    md_text = p.read_text(encoding="utf-8")
    sections = split_sections(md_text)
    if not sections:
        print(f"  !! No sections 01/02/03 found in {md_path}, skipping.", file=sys.stderr)
        return

    for code in ["01", "02", "03"]:
        full_title = CHILD_TITLES[code]
        section_text = sections.get(code)
        if not section_text:
            print(f"  ?? No section {code} in markdown for step {step_number}, skipping that child.")
            continue
        child_id = ensure_child_page(step_page_id, code, full_title)
        if not child_id:
            continue
        print(f"  -> Updating {full_title} ({child_id})")
        clear_page_content(child_id)
        write_page_markdown(child_id, section_text)
        time.sleep(0.4)


def main() -> None:
    print("IFNS - Sync all 14 Steps (GitHub -> Notion)")
    print(f"Root page id: {NOTION_ROOT_PAGE_ID}")
    print(f"Searching for '{IFNS_MASTER_TITLE}' under root...")

    ifns_master_id = find_child_page_recursive(NOTION_ROOT_PAGE_ID, IFNS_MASTER_TITLE, max_depth=4)
    if not ifns_master_id:
        print(
            f"ERROR: Could not find page titled '{IFNS_MASTER_TITLE}' under root {NOTION_ROOT_PAGE_ID}",
            file=sys.stderr,
        )
        sys.exit(1)
    print(f"Found IFNS UI Master page id: {ifns_master_id}")

    step_pages = list_child_pages(ifns_master_id)
    if not step_pages:
        print("WARNING: No child pages found under IFNS UI Master.")
        return

    for page_id, title in step_pages:
        m = re.match(r"Step\s+(\d+)", title)
        if not m:
            continue
        step_number = int(m.group(1))
        if step_number not in STEP_FILES:
            print(f"Skipping page '{title}' (no markdown mapping for step {step_number}).")
            continue
        sync_step(page_id, step_number, title)

    print("\nDone.")


if __name__ == "__main__":
    main()
