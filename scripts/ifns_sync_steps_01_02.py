#!/usr/bin/env python3
"""
IFNS  Sync Steps 01 & 02 (GitHub -> Notion)

- Reads:
    docs/ifns/Step_01_Preface_Integration.md
    docs/ifns/Step_02_Executive_Summary.md

- Splits each file into:
    01 -> Narrative & Intent
    02 -> Implementation Reference
    03 -> Notes & Decisions

- For each Step page in Notion:
    - Finds (or creates) child pages whose titles start with "01", "02", "03".
    - Replaces their content with the corresponding section text.
"""

import os
import sys
import time
import re
import requests
from pathlib import Path

NOTION_TOKEN = os.environ.get("NOTION_TOKEN")
if not NOTION_TOKEN:
    print("ERROR: NOTION_TOKEN environment variable is not set.", file=sys.stderr)
    sys.exit(1)

HEADERS = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json",
}

STEP_CONFIGS = [
    {
        "step": 1,
        "name": "Step 01  Preface Integration",
        "parent_id": "2adb22c770d98068a351dc6f69822f3b",
        "md_path": "docs/ifns/Step_01_Preface_Integration.md",
    },
    {
        "step": 2,
        "name": "Step 02  Executive Summary",
        "parent_id": "2adb22c770d98037a4a0c184f917d64d",
        "md_path": "docs/ifns/Step_02_Executive_Summary.md",
    },
]

CHILD_TITLES = {
    "01": "01  Narrative & Intent",
    "02": "02  Implementation Reference",
    "03": "03  Notes & Decisions",
}


def split_sections(md_text):
    """
    Return dict like {"01": section_text, "02": ..., "03": ...}
    Sections are headed by lines starting with:
        ## 01 ...
        ## 02 ...
        ## 03 ...
    """
    pattern = re.compile(r"^##\s*(0[1-3])\b.*$", re.MULTILINE)
    matches = list(pattern.finditer(md_text))
    sections = {}
    if not matches:
        return sections
    for i, m in enumerate(matches):
        sec = m.group(1)
        start = m.start()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(md_text)
        sections[sec] = md_text[start:end].strip()
    return sections


def list_child_pages(parent_id):
    url = f"https://api.notion.com/v1/blocks/{parent_id}/children"
    results = []
    start_cursor = None
    while True:
        params = {}
        if start_cursor:
            params["start_cursor"] = start_cursor
        resp = requests.get(url, headers=HEADERS, params=params)
        try:
            resp.raise_for_status()
        except Exception as e:
            print(f"[ERROR] list_child_pages({parent_id}) -> {e}", file=sys.stderr)
            print(resp.text, file=sys.stderr)
            return results
        data = resp.json()
        for block in data.get("results", []):
            if block.get("type") == "child_page":
                title = block.get("child_page", {}).get("title", "")
                results.append((block["id"], title))
        if not data.get("has_more"):
            break
        start_cursor = data.get("next_cursor")
    return results


def ensure_child_page(parent_id, code, full_title):
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
            "title": {
                "title": [{"text": {"content": full_title}}],
            }
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


def clear_page_content(page_id):
    url = f"https://api.notion.com/v1/blocks/{page_id}/children"
    resp = requests.get(url, headers=HEADERS)
    try:
        resp.raise_for_status()
    except Exception as e:
        print(f"[ERROR] get children for {page_id} -> {e}", file=sys.stderr)
        print(resp.text, file=sys.stderr)
        return
    data = resp.json()
    blocks = data.get("results", [])
    if not blocks:
        return
    for block in blocks:
        bid = block.get("id")
        if not bid:
            continue
        patch_url = f"https://api.notion.com/v1/blocks/{bid}"
        patch_payload = {"archived": True}
        print(f"    - Archiving block {bid}")
        r2 = requests.patch(patch_url, headers=HEADERS, json=patch_payload)
        try:
            r2.raise_for_status()
        except Exception as e:
            print(f"[WARN] archiving {bid} -> {e}", file=sys.stderr)
            print(r2.text, file=sys.stderr)
        time.sleep(0.2)


def chunk_text(text, max_len=1500):
    """Split long text into smaller chunks so each rich_text is safe."""
    chunks = []
    current = []
    current_len = 0
    lines = text.splitlines(True)  # keep line breaks
    for line in lines:
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


def write_page_markdown(page_id, md_text):
    """
    Write the given markdown text as multiple paragraph blocks on the page.
    """
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
    total_chars = sum(len(c["paragraph"]["rich_text"][0]["text"]["content"]) for c in children_blocks)
    print(f"    -> Content updated ({total_chars} chars in {len(chunks)} block(s))")


def sync_step(step_cfg):
    step = step_cfg["step"]
    name = step_cfg["name"]
    parent_id = step_cfg["parent_id"]
    md_path = Path(step_cfg["md_path"])

    print(f"\n=== Step {step:02} :: {name} ===")
    if not md_path.exists():
        print(f"  !! Markdown file not found: {md_path}", file=sys.stderr)
        return

    md_text = md_path.read_text(encoding="utf-8")
    sections = split_sections(md_text)
    if not sections:
        print(f"  !! No sections 01/02/03 found in {md_path}", file=sys.stderr)
        return

    for code in ["01", "02", "03"]:
        full_title = CHILD_TITLES[code]
        section_text = sections.get(code)
        if not section_text:
            print(f"  ?? No section {code} found in markdown, skipping")
            continue

        child_id = ensure_child_page(parent_id, code, full_title)
        if not child_id:
            continue

        print(f"  -> Updating {full_title} ({child_id})")
        clear_page_content(child_id)
        write_page_markdown(child_id, section_text)
        time.sleep(0.4)


def main():
    print("IFNS  Sync Steps 01 & 02 (GitHub -> Notion)")
    for cfg in STEP_CONFIGS:
        sync_step(cfg)
    print("\nDone.")


if __name__ == "__main__":
    main()
