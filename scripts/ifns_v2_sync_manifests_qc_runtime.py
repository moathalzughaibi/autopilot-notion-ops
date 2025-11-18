#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
IFNS – V2: Wire Manifests & Policy, Telemetry & QC, Runtime assets into IFNS – UI Master (V2).

Creates stub pages under:
  - Manifests & Policy
  - Telemetry & QC
  - Runtime Templates & Calendars

for key CSV/JSON/MD/PY/YAML files from the v0.10–v0.18 bundle.
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
SECTION_MANIFESTS = "Manifests & Policy"
SECTION_TELEMETRY = "Telemetry & QC"
SECTION_RUNTIME = "Runtime Templates & Calendars"

SYNC_IFNS = Path("sync/ifns")
INDICATORS_DIR = Path("docs/ifns/indicators")
ETL_DIR = Path("etl")
TOOLS_DIR = Path("tools")
RUNTIME_DIR = Path("runtime_templates")
GITHUB_WF_DIR = Path(".github/workflows")


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


def write_stub(page_id: str, title: str, path: Path, purpose: str) -> None:
    md = f"""# {title}

This page documents a V2 asset from the consolidated indicators bundle.

- **File name:** `{path.name}`
- **Repo path:** `{path.as_posix()}`
- **Role:** {purpose}

> Source of truth is this file in Git (packs v0.10–v0.18). Do not edit data here;
> update the file and re-sync.
"""
    chunks = chunk_text(md, max_len=1500)
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
        print(f"[ERROR] write_stub({page_id}) -> {e}", file=sys.stderr)
        print(resp.text, file=sys.stderr)
        return
    print(f"    -> Stub written for {path.as_posix()}")


def find_file(base_dir: Path, token: str, patterns: Tuple[str, ...] = ("*",)) -> Optional[Path]:
    if not base_dir.exists():
        return None
    token_lower = token.lower()
    for pat in patterns:
        for p in base_dir.glob(pat):
            if token_lower in p.name.lower():
                return p
    return None


def main() -> None:
    print("IFNS – V2: Wiring manifests, policy, telemetry, runtime assets")
    print(f"Root page id: {NOTION_ROOT_PAGE_ID}")

    v2_id = find_child_page_recursive(NOTION_ROOT_PAGE_ID, V2_MASTER_TITLE, max_depth=3)
    if not v2_id:
        print(f"ERROR: Could not find '{V2_MASTER_TITLE}'. Run ifns_v2_sync_indicators_and_shell.py first.", file=sys.stderr)
        sys.exit(1)
    print(f"Found V2 master page id: {v2_id}")

    manifests_id = find_child_page_recursive(v2_id, SECTION_MANIFESTS, max_depth=2)
    telemetry_id = find_child_page_recursive(v2_id, SECTION_TELEMETRY, max_depth=2)
    runtime_id = find_child_page_recursive(v2_id, SECTION_RUNTIME, max_depth=2)

    if not manifests_id or not telemetry_id or not runtime_id:
        print("ERROR: One or more V2 sections missing. Ensure V2 shell is created.", file=sys.stderr)
        sys.exit(1)

    # --- Manifests & Policy (CSV) ---
    manifest_configs = [
        ("Indicator Feature Schema v1 (with family)", "feature_schema_v1_with_family", "Final feature schema with family tags."),
        ("Indicator Feature Schema H1 v1 (with family)", "feature_schema_h1_v1_with_family", "Feature schema for H1 horizon with family tags."),
        ("Feature Policy Matrix", "feature_policy_matrix", "Policy matrix mapping features to risk/usage constraints."),
        ("Feature Family Map", "feature_family_map", "Mapping of indicators/features into semantic families."),
        ("Indicators – Universe Catalog (Phase 2 Draft)", "universe_catalog", "Universe of candidate indicators (Phase 2)."),
        ("Indicators – L1 Catalog (Phase 3)", "catalog_l1", "L1 atomic indicators used downstream."),
        ("Indicators – L2/L3 Framework Catalog (Phase 4)", "catalog_l2l3", "L2/L3 frameworks built from L1 indicators."),
    ]

    for title, token, purpose in manifest_configs:
        print(f"\n=== Manifests & Policy: {title} (token '{token}') ===")
        p = find_file(SYNC_IFNS, token, patterns=("*.csv", "*.ndjson", "*.json"))
        if p is None:
            print(f"  !! No file in sync/ifns matching '{token}', skipping.", file=sys.stderr)
            continue
        page_id = ensure_child_page(manifests_id, title)
        clear_page_content(page_id)
        write_stub(page_id, title, p, purpose)

    # --- Telemetry & QC ---
    telemetry_configs = [
        ("QC Weekly Schema v1", "qc_weekly_schema_v1", "Telemetry schema for weekly QC snapshots."),
        ("QC Weekly Example v1", "qc_weekly_example_v1", "Example NDJSON lines for weekly QC payloads."),
    ]

    for title, token, purpose in telemetry_configs:
        print(f"\n=== Telemetry & QC: {title} (token '{token}') ===")
        p = find_file(SYNC_IFNS, token, patterns=("*.json", "*.ndjson"))
        if p is None:
            print(f"  !! No file in sync/ifns matching '{token}', skipping.", file=sys.stderr)
            continue
        page_id = ensure_child_page(telemetry_id, title)
        clear_page_content(page_id)
        write_stub(page_id, title, p, purpose)

    # Telemetry docs + ETL + tools
    doc_configs = [
        ("QC Weekly Telemetry V1 (Doc)", "QC_Weekly_Telemetry", INDICATORS_DIR, "Narrative spec for weekly QC telemetry."),
        ("QC Weekly ETL Skeleton", "QC_Weekly_ETL_Skeleton", INDICATORS_DIR, "Skeleton design for QC weekly ETL."),
        ("QC Weekly ETL Clip Integration", "QC_Weekly_ETL_Clip_Integration", INDICATORS_DIR, "How QC weekly ETL ties into clip event telemetry."),
        ("QC Weekly ETL Script", "qc_weekly_etl", ETL_DIR, "Python ETL script for generating QC weekly payloads."),
        ("IO Utils (Telemetry/Manifest I/O helpers)", "io_utils", TOOLS_DIR, "Helper functions for reading/writing manifests and telemetry."),
        ("Manifest Diff Tool", "manifest_diff", TOOLS_DIR, "Command-line tool to compare indicator manifests."),
        ("CI IFNS Guard Workflow", "ci_ifns_guard", GITHUB_WF_DIR, "GitHub Actions workflow enforcing manifest/telemetry invariants."),
        ("CI Manifest Guard (Python)", "ci_manifest_guard", TOOLS_DIR, "Python guard enforcing manifest rules in CI."),
    ]

    for title, token, base_dir, purpose in doc_configs:
        print(f"\n=== Telemetry & QC: {title} (token '{token}') ===")
        p = find_file(base_dir, token, patterns=("*.*",))
        if p is None:
            print(f"  !! No file in {base_dir} matching '{token}', skipping.", file=sys.stderr)
            continue
        page_id = ensure_child_page(telemetry_id, title)
        clear_page_content(page_id)
        write_stub(page_id, title, p, purpose)

    # --- Runtime Templates & Calendars ---
    # Calendar gaps JSON
    print("\n=== Runtime: Calendar gaps 2025 ===")
    cal_path = find_file(SYNC_IFNS, "calendar_gaps_2025", patterns=("*.json",))
    if cal_path:
        title = "Runtime – Calendar Gaps 2025"
        page_id = ensure_child_page(runtime_id, title)
        clear_page_content(page_id)
        write_stub(page_id, title, cal_path, "Exchange-holiday overrides and gap calendar for 2025.")
    else:
        print("  !! No calendar_gaps_2025.json in sync/ifns, skipping.", file=sys.stderr)

    # Runtime templates directory
    print("\n=== Runtime: templates directory ===")
    if RUNTIME_DIR.exists():
        title = "Runtime Templates (YAML)"
        page_id = ensure_child_page(runtime_id, title)
        clear_page_content(page_id)
        # Just list files in the stub
        files = []
        for p in sorted(RUNTIME_DIR.rglob("*")):
            if p.is_file():
                files.append(f"- `{p.as_posix()}`")
        md = "# Runtime Templates (YAML)\n\n" \
             "This page documents the YAML runtime templates included in the V2 bundle.\n\n" \
             "Files:\n\n" + "\n".join(files) + "\n\n" \
             "> Use these as the base for runtime configuration per venue/asset/timeframe."
        chunks = chunk_text(md, max_len=1500)
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
            print(f"[ERROR] write runtime templates stub -> {e}", file=sys.stderr)
            print(resp.text, file=sys.stderr)
    else:
        print(f"Runtime templates dir {RUNTIME_DIR} not found, skipping.", file=sys.stderr)

    print("\nDone: Manifests & Policy, Telemetry & QC, Runtime assets wired into V2.")
    

if __name__ == "__main__":
    main()
