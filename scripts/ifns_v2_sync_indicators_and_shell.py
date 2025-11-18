#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
IFNS – V2: Seed IFNS – UI Master (V2) + Indicator System (Phases 1–7) + Quickstart/Rollout.

- Creates/ensures:
    IFNS  UI Master (V2)
      - Indicator System (Phases 1–7)
      - Core ML Build (Stages 0–7)
      - Manifests & Policy
      - Telemetry & QC
      - Runtime Templates & Calendars
      - Change Log (V1 → V2 deltas)
      - Attachments

- Under Indicator System (Phases 1–7):
    - Indicators_Master_Index_Phases_1_to_7
    - Phase 17 spec pages (content from docs/ifns/indicators/*.md)

- Under Attachments:
    - IFNS_Indicators_Quickstart_v0_18
    - IFNS_V2_Rollout_Checklist
    - IFNS_V2_Meta_Index (stub listing meta_index/*)
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

V2_MASTER_TITLE = "IFNS \u2013 UI Master (V2)"
SECTION_TITLES = [
    "Indicator System (Phases 1\u20137)",
    "Core ML Build (Stages 0\u20137)",
    "Manifests & Policy",
    "Telemetry & QC",
    "Runtime Templates & Calendars",
    "Change Log (V1 \u2192 V2 deltas)",
    "Attachments",
]

INDICATORS_DIR = Path("docs/ifns/indicators")
META_DIR = Path("meta_index")
QS_PATH = Path("IFNS_Indicators_Quickstart_v0_18.md")
ROLLOUT_PATH = Path("IFNS_V2_Rollout_Checklist.md")


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
    for cid, t in list_child_pages(parent_id):
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


def append_banner(page_id: str, text: str) -> None:
    # Just append a paragraph banner, do not clear existing content.
    url = f"https://api.notion.com/v1/blocks/{page_id}/children"
    payload = {
        "children": [
            {
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [{"type": "text", "text": {"content": text}}],
                },
            }
        ]
    }
    resp = requests.patch(url, headers=HEADERS, json=payload)
    try:
        resp.raise_for_status()
    except Exception as e:
        print(f"[WARN] append_banner({page_id}) -> {e}", file=sys.stderr)
        print(resp.text, file=sys.stderr)


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


def write_page_markdown(page_id: str, md_text: str, file_source: Optional[str] = None) -> None:
    chunks = []
    if file_source:
        chunks.append(f"[File Source] {file_source}\n\n")
    chunks.extend(chunk_text(md_text, max_len=1500))

    blocks = []
    for ch in chunks:
        blocks.append(
            {
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [{"type": "text", "text": {"content": ch}}],
                },
            }
        )
    url = f"https://api.notion.com/v1/blocks/{page_id}/children"
    payload = {"children": blocks}
    resp = requests.patch(url, headers=HEADERS, json=payload)
    try:
        resp.raise_for_status()
    except Exception as e:
        print(f"[ERROR] write_page_markdown({page_id}) -> {e}", file=sys.stderr)
        print(resp.text, file=sys.stderr)
        return
    total_chars = sum(len(b["paragraph"]["rich_text"][0]["text"]["content"]) for b in blocks)
    print(f"    -> Content updated ({total_chars} chars, {len(blocks)} block(s))")


def find_file_by_token(base_dir: Path, token: str) -> Optional[Path]:
    token_lower = token.lower()
    if not base_dir.exists():
        return None
    for p in base_dir.glob("*.*"):
        if token_lower in p.name.lower():
            return p
    return None


def ensure_v2_root() -> str:
    v2_id = find_child_page_recursive(NOTION_ROOT_PAGE_ID, V2_MASTER_TITLE, max_depth=3)
    if v2_id:
        print(f"Found existing V2 master page id: {v2_id}")
    else:
        print("V2 master not found, creating IFNS  UI Master (V2)")
        v2_id = ensure_child_page(NOTION_ROOT_PAGE_ID, V2_MASTER_TITLE)
        append_banner(
            v2_id,
            "Source of truth = repo files (packs v0.10v0.18). "
            "Do NOT edit specs directly here; overwrite from Git."
        )
    return v2_id


def ensure_sections(v2_id: str) -> Dict[str, str]:
    ids: Dict[str, str] = {}
    for title in SECTION_TITLES:
        sid = ensure_child_page(v2_id, title)
        ids[title] = sid
    return ids


def sync_indicator_system(indicator_section_id: str) -> None:
    if not INDICATORS_DIR.exists():
        print(f"Indicators dir not found at {INDICATORS_DIR}, skipping.", file=sys.stderr)
        return

    # Master index page
    master_file = find_file_by_token(INDICATORS_DIR, "Master_Index")
    master_title = "Indicators_Master_Index_Phases_1_to_7"
    master_page_id = ensure_child_page(indicator_section_id, master_title)

    if master_file is not None:
        print(f"\n=== Syncing Indicators master index from '{master_file.name}' ===")
        clear_page_content(master_page_id)
        md = master_file.read_text(encoding="utf-8")
        write_page_markdown(
            master_page_id,
            md,
            file_source=str(master_file.relative_to(Path(".")))
        )
    else:
        print("!! No master index file found (token 'Master_Index').", file=sys.stderr)

    # Phases 17
    phase_configs = [
        ("Phase 1  Indicator Taxonomy & Governance", "Taxonomy"),
        ("Phase 2  Indicator Universe Draft", "Universe"),
        ("Phase 3  L1 Indicator Catalog", "L1_Catalog"),
        ("Phase 4  L2/L3 Framework Catalog", "L2L3"),
        ("Phase 5  Feature Output & Digitization Schema", "Feature_Schema"),
        ("Phase 6  Implementation & Runtime Templates", "Implementation_Templates"),
        ("Phase 7  ML Integration & Operationalization", "ML_Integration"),
    ]

    for title, token in phase_configs:
        print(f"\n=== Syncing {title} (token '{token}') ===")
        f = find_file_by_token(INDICATORS_DIR, token)
        if f is None:
            print(f"  !! No file matching '{token}' in {INDICATORS_DIR}, skipping.", file=sys.stderr)
            continue
        print(f"  -> Using file '{f.name}'")
        page_id = ensure_child_page(master_page_id, title)
        clear_page_content(page_id)
        md = f.read_text(encoding="utf-8")
        write_page_markdown(
            page_id,
            md,
            file_source=str(f.relative_to(Path(".")))
        )


def sync_attachments(attachments_id: str) -> None:
    # Quickstart
    if QS_PATH.exists():
        print(f"\n=== Syncing Quickstart from '{QS_PATH.name}' ===")
        page_id = ensure_child_page(attachments_id, "IFNS_Indicators_Quickstart_v0_18")
        clear_page_content(page_id)
        md = QS_PATH.read_text(encoding="utf-8")
        write_page_markdown(page_id, md, file_source=str(QS_PATH.relative_to(Path("."))))
    else:
        print(f"Quickstart file '{QS_PATH}' not found, skipping.", file=sys.stderr)

    # Rollout Checklist
    if ROLLOUT_PATH.exists():
        print(f"\n=== Syncing Rollout Checklist from '{ROLLOUT_PATH.name}' ===")
        page_id = ensure_child_page(attachments_id, "IFNS_V2_Rollout_Checklist")
        clear_page_content(page_id)
        md = ROLLOUT_PATH.read_text(encoding="utf-8")
        write_page_markdown(page_id, md, file_source=str(ROLLOUT_PATH.relative_to(Path("."))))
    else:
        print(f"Rollout file '{ROLLOUT_PATH}' not found, skipping.", file=sys.stderr)

    # Meta Index stub
    title = "IFNS_V2_Meta_Index"
    page_id = ensure_child_page(attachments_id, title)
    clear_page_content(page_id)

    if META_DIR.exists():
        entries = []
        for p in sorted(META_DIR.glob("*")):
            if p.is_file():
                entries.append(f"- `{p.relative_to(Path('.'))}`")
        manifest = "\n".join(entries)
    else:
        manifest = "_meta_index directory not present in repo._"

    stub = f"""# IFNS V2 Meta Index

This page summarizes the contents of the `meta_index/` directory from the consolidated bundle
`IFNS_Indicators_All_v0_10_to_v0_18.zip`.

Files:

{manifest}

> Reminder: checksums and merge-order information here are authoritative for verifying that Notion V2
> was seeded from the correct bundle. Do not edit data here; update the underlying files instead.
"""
    write_page_markdown(page_id, stub, file_source=str(META_DIR.relative_to(Path("."))) if META_DIR.exists() else None)


def main() -> None:
    print("IFNS  V2: Seed IFNS  UI Master (V2) basic structure + indicators + attachments")
    print(f"Root page id: {NOTION_ROOT_PAGE_ID}")

    v2_id = ensure_v2_root()
    sections = ensure_sections(v2_id)

    indicator_section_id = sections["Indicator System (Phases 17)"]
    attachments_id = sections["Attachments"]

    sync_indicator_system(indicator_section_id)
    sync_attachments(attachments_id)

    print("\nDone: V2 base + Indicator System + Attachments seeded.")


if __name__ == "__main__":
    main()
