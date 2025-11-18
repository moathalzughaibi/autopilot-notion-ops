#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
IFNS - Sync Core ML Build Stages (0-7) into Notion.

Structure in Notion:

IFNS – UI Master
  -> Core ML Build Stages
       -> Stage 00  Document Overview
       -> Stage 01  Foundations & Architecture
       ...
       -> Stage 07  Live Trading & Operations
            -> 01  Narrative & Intent
            -> 02  Contracts / Tables / JSON Artifacts
            -> 03  Notes & Decisions

Sources in Git:

docs/ifns/stages/Stage_00_Document_Overview.md
docs/ifns/stages/Stage_01_Foundations_and_Architecture.md
...
docs/ifns/stages/Stage_07_Live_Trading_and_Operations.md
"""

import os
import sys
import re
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

# Use Unicode escape for the en-dash so the source stays ASCII-safe.
IFNS_MASTER_TITLE = "IFNS \u2013 UI Master"
COREML_HUB_TITLE = "Core ML Build Stages"

STAGE_FILES: Dict[int, str] = {
    0: "docs/ifns/stages/Stage_00_Document_Overview.md",
    1: "docs/ifns/stages/Stage_01_Foundations_and_Architecture.md",
    2: "docs/ifns/stages/Stage_02_Data_and_Feature_Pipeline.md",
    3: "docs/ifns/stages/Stage_03_Modeling_and_Training.md",
    4: "docs/ifns/stages/Stage_04_Backtesting_and_Evaluation.md",
    5: "docs/ifns/stages/Stage_05_Risk_Execution_and_SxE_Link.md",
    6: "docs/ifns/stages/Stage_06_Paper_Trading.md",
    7: "docs/ifns/stages/Stage_07_Live_Trading_and_Operations.md",
}

STAGE_TITLES: Dict[int, str] = {
    0: "Stage 00 \u2013 Document Overview",
    1: "Stage 01 \u2013 Foundations & Architecture",
    2: "Stage 02 \u2013 Data & Feature Pipeline",
    3: "Stage 03 \u2013 Modeling & Training",
    4: "Stage 04 \u2013 Backtesting & Evaluation",
    5: "Stage 05 \u2013 Risk, Execution & SxE Link",
    6: "Stage 06 \u2013 Paper Trading",
    7: "Stage 07 \u2013 Live Trading & Operations",
}

CHILD_TITLES: Dict[str, str] = {
    "01": "01 \u2013 Narrative & Intent",
    "02": "02 \u2013 Contracts / Tables / JSON Artifacts",
    "03": "03 \u2013 Notes & Decisions",
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


def sync_stage(stage_page_id: str, stage_num: int, stage_title: str) -> None:
    md_path = STAGE_FILES.get(stage_num)
    if not md_path:
        print(f"  !! No markdown file configured for stage {stage_num}, skipping.")
        return
    p = Path(md_path)
    if not p.exists():
        print(f"  !! Markdown file not found: {md_path}, skipping stage {stage_num}.", file=sys.stderr)
        return

    print(f"\n=== Stage {stage_num:02d} :: {stage_title} ===")
    md_text = p.read_text(encoding="utf-8")
    sections = split_sections(md_text)
    if not sections:
        print(f"  !! No sections 01/02/03 found in {md_path}, skipping.", file=sys.stderr)
        return

    for code in ["01", "02", "03"]:
        full_title = CHILD_TITLES[code]
        section_text = sections.get(code)
        if not section_text:
            print(f"  ?? No section {code} in markdown for stage {stage_num}, skipping that child.")
            continue
        child_id = ensure_child_page(stage_page_id, full_title)
        if not child_id:
            continue
        print(f"  -> Updating {full_title} ({child_id})")
        clear_page_content(child_id)
        write_page_markdown(child_id, section_text)


def main() -> None:
    print("IFNS - Sync Core ML Build Stages (GitHub -> Notion)")
    print(f"Root page id: {NOTION_ROOT_PAGE_ID}")
    print(f"Looking for '{IFNS_MASTER_TITLE}' under root...")

    master_id = find_child_page_recursive(NOTION_ROOT_PAGE_ID, IFNS_MASTER_TITLE, max_depth=4)
    if not master_id:
        print(f"ERROR: Could not find '{IFNS_MASTER_TITLE}' under root {NOTION_ROOT_PAGE_ID}", file=sys.stderr)
        sys.exit(1)
    print(f"Found IFNS  UI Master page id: {master_id}")

    # Ensure Core ML hub
    coreml_hub_id = ensure_child_page(master_id, COREML_HUB_TITLE)

    for stage_num in sorted(STAGE_TITLES.keys()):
        title = STAGE_TITLES[stage_num]
        stage_page_id = ensure_child_page(coreml_hub_id, title)
        if not stage_page_id:
            continue
        sync_stage(stage_page_id, stage_num, title)

    print("\nDone.")


if __name__ == "__main__":
    main()
