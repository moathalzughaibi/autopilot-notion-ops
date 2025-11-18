# IFNS / Autopilot – Troubleshooting Log

> Purpose  
> Track issues, root causes, and fixes so we don’t repeat the same mistakes –
> whether its Moath, this agent, or any future agent working on IFNS / Core ML / Notion.

---

## How to use this log

- Each issue is a separate section: `## YYYY-MM-DD  Short issue title`.
- Under each issue, fill this table:

| Field    | Details |
|---------|---------|
| Area    | Where in the system this happened (Notion sync, Core ML UI, GA4, etc.) |
| Symptom | What you saw (error messages, behavior). Copy exact messages when possible. |
| Context | What you were doing (commands, files, environment). |
| Root cause | The underlying mistake / mismatch / misunderstanding. |
| Fix     | What you changed to solve it. |
| Prevent / lessons | Rules or habits to avoid this in future. |
| Commands | Key commands or API calls used to debug/fix it. |

When this file becomes long, new agents can scan it to understand **what we already tried** and which traps to avoid.

---

## 2025-11-18  Notion sync script cant find IFNS  UI Master

| Field    | Details |
|---------|---------|
| **Area** | IFNS  Notion sync (`scripts/ifns_sync_all_steps.py`) |
| **Symptom** | Running `python .\scripts\ifns_sync_all_steps.py` printed:<br>`ERROR: Could not find page titled 'IFNS  UI Master' under root 29ab22c770d980918736f0dcad3bac83` |
| **Context** | We had: `NOTION_ROOT_PAGE_ID = 29ab22c770d980918736f0dcad3bac83` (Autopilot Hub). The script tried to find the IFNS  UI Master page under that root before syncing all 14 steps. |
| **Root cause** | Title mismatch between the script and the real Notion page: the constant `IFNS_MASTER_TITLE` in the script was set to `IFNS  UI Master` (two spaces, no dash). The actual Notion page is named `IFNS  UI Master` (with an en-dash and single spaces). |
| **Fix** | Overwrote `scripts/ifns_sync_all_steps.py` and changed the constant to:<br>`IFNS_MASTER_TITLE = "IFNS  UI Master"` (copy-pasted exactly from Notion). Then re-ran the script after loading the env (`.\local_env\notion_env.ps1`). |
| **Prevent / lessons** | 1) When scripting against Notion, always **copy-paste page titles** directly from Notion instead of retyping them. 2) Prefer using **page IDs** as primary identifiers; titles are for humans. 3) When a script says Could not find page titled , first check spelling, spaces, and special characters like dashes. |
| **Commands** | - Load env: `.\local_env\notion_env.ps1`<br>- Run sync: `python .\scripts\ifns_sync_all_steps.py` |

---

## Template for new issues (copy-paste this section)

## YYYY-MM-DD  <Short issue title>

| Field    | Details |
|---------|---------|
| **Area** | <Which part of the system?> |
| **Symptom** | <Exact error message or behavior> |
| **Context** | <What you were doing, which repo/branch, which Notion page, etc.> |
| **Root cause** | <What we learned was actually wrong> |
| **Fix** | <What we changed to solve it> |
| **Prevent / lessons** | <Rules to avoid repeating it> |
| **Commands** | <Key terminal/API commands used to debug/fix it> |
## 2025-11-18 – Second IFNS UI Master lookup failed (title mismatch still in script)

| Field    | Details |
|---------|---------|
| **Area** | IFNS – Notion sync (`scripts/ifns_sync_all_steps.py`) |
| **Symptom** | Running `python .\scripts\ifns_sync_all_steps.py` printed:<br>`ERROR: Could not find page titled 'IFNS  UI Master' under root 29ab22c770d980918736f0dcad3bac83`. |
| **Context** | After wiring all 14 `Step_XX_*.md` files into `docs/ifns`, attempted a full-phase sync to IFNS – UI Master. The script was still using the old title string `IFNS  UI Master` (two spaces, no dash) in `IFNS_MASTER_TITLE` and log messages. |
| **Root cause** | The newer version of the sync script (with the correct `IFNS – UI Master` title) had not been applied; the file still contained the old literal string `IFNS  UI Master`. |
| **Fix** | Used a PowerShell in-place replace to update the script:<br>`(Get-Content .\scripts\ifns_sync_all_steps.py) -replace 'IFNS  UI Master','IFNS – UI Master' -replace 'IFNS  Sync all 14 Steps','IFNS – Sync all 14 Steps' \| Set-Content .\scripts\ifns_sync_all_steps.py`<br>Then re-ran `.\local_env\notion_env.ps1` and `python .\scripts\ifns_sync_all_steps.py`. |
| **Prevent / lessons** | After changing a script via a big `Set-Content` block, always double-check the file content with `Select-String` or opening it in VS Code before assuming the change took effect. When matching Notion page titles, copy-paste the title from Notion instead of retyping. |
| **Commands** | `Select-String -Path .\scripts\ifns_sync_all_steps.py -Pattern 'IFNS'` to verify strings; then `python .\scripts\ifns_sync_all_steps.py`. |
## 2025-11-18 – Logs redirection failed (missing logs folder)

| Field    | Details |
|---------|---------|
| **Area** | Local logging for IFNS – Notion sync |
| **Symptom** | PowerShell error when running:<br>`python .\scripts\ifns_sync_all_steps.py *> logs\ifns_sync_phase1_2025-11-18.txt`<br>Message: `Could not find a part of the path 'E:\GitHub\autopilot-notion-ops\logs\ifns_sync_phase1_2025-11-18.txt'`. |
| **Context** | Tried to capture sync output into a log file in `logs\...` before creating the `logs` directory. |
| **Root cause** | The `logs` directory did not exist; `Out-File` (which handles `*>`) cannot create parent directories automatically. |
| **Fix** | Created the folder manually:<br>`New-Item -ItemType Directory -Path "logs" -ErrorAction SilentlyContinue`<br>Then re-ran the sync command with redirection. |
| **Prevent / lessons** | Always ensure the parent folder exists before redirecting output into a nested path. For new log paths, run `New-Item -ItemType Directory -Path '<folder>' -ErrorAction SilentlyContinue` first. |
| **Commands** | `New-Item -ItemType Directory -Path "logs" -ErrorAction SilentlyContinue` |
## 2025-11-18 – Python SyntaxError: Non-UTF-8 code in ifns_sync_all_steps.py

| Field    | Details |
|---------|---------|
| **Area** | IFNS – Notion sync (`scripts/ifns_sync_all_steps.py`) |
| **Symptom** | Running `python .\scripts\ifns_sync_all_steps.py` raised:<br>`SyntaxError: Non-UTF-8 code starting with '\x96' in file ...ifns_sync_all_steps.py on line 3, but no encoding declared`. |
| **Context** | We modified the script on Windows using PowerShell and introduced an en-dash (–) directly in the source without an encoding header. The file ended up saved in a Windows codepage, while Python 3 expected UTF-8 by default. :contentReference[oaicite:1]{index=1} |
| **Root cause** | The script file contained a non-UTF-8 byte (`\x96`, Windows en-dash) with no `# -*- coding: utf-8 -*-` declaration, causing Python’s UTF-8 parser to fail. |
| **Fix** | Replaced the entire script with a new version that: (1) includes `# -*- coding: utf-8 -*-` at the top, (2) keeps the file ASCII-only by using `\u2013` for the “–” character inside strings, and (3) was written via `Set-Content` with `-Encoding UTF8`. |
| **Prevent / lessons** | 1) On Windows, avoid pasting “smart punctuation” (like en-dashes) directly into Python files unless using a proper UTF-8 encoding header and editor. 2) Prefer using Unicode escapes inside literals (e.g., `"IFNS \\u2013 UI Master"`). 3) When you see `Non-UTF-8 code starting with '\x..'`, suspect encoding or pasted special characters. |
| **Commands** | Used a PowerShell heredoc to overwrite the file:<br>`@' ... '@ \| Set-Content -Path "scripts\ifns_sync_all_steps.py" -Encoding UTF8` then reran `.\local_env\notion_env.ps1` and `python .\scripts\ifns_sync_all_steps.py`. |
## IFNS Ops Workflow (Notion + Git)

**Before any structural change or sync:**

1. **Read the Troubleshooting Log**  
   - File: `docs/IFNS_Troubleshooting_Log.md`  
   - Check recent issues related to the area you’re about to touch (Notion sync, IFNS steps, Core ML, etc.).

2. **Consult the Notion Page Index**  
   - File: `docs/IFNS_Notion_Page_Index.md`  
   - Notion page: `IFNS – Notion Page Index`  
   - Confirm page titles, parents, and IDs are correct before using them in scripts.

3. **Choose the action**  
   - Ensure pages exist (structure only).  
   - Sync content from Markdown to Notion.  
   - Add new areas (e.g., Core ML root, Admin Console, Awareness Mirror).

**Typical IFNS steps flow:**

```powershell
cd E:\GitHub\autopilot-notion-ops
.\local_env\notion_env.ps1

# 1) Ensure Step pages exist under IFNS – UI Master
python .\scripts\ifns_ensure_step_pages.py

# 2) Push Markdown content (01/02/03 sections) into Steps 01–14
python .\scripts\ifns_sync_all_steps.py

---

From here:

- You can run the new `ifns_ensure_step_pages.py` once to normalize the Step structure (now and any time you add more).  
- You already have the Page Index file and the Troubleshooting Log in place. :contentReference[oaicite:1]{index=1}  

Whenever we hit a new “trap”, I’ll keep giving you a ready **log entry block** so your log and index become more and more powerful over time.
::contentReference[oaicite:2]{index=2}
## 2025-11-18 – Step 14 not synced + confusion about archiving

| Field    | Details |
|---------|---------|
| **Area** | IFNS – Notion sync (`ifns_sync_all_steps.py`) and structure (`ifns_ensure_step_pages.py`) |
| **Symptom** | Running `python .\scripts\ifns_sync_all_steps.py` updated Steps 01–13 (with many “Archiving block …” lines) but **Step 14** in Notion remained unchanged and did not show any `=== Step 14 :: ...` section in the log. |
| **Context** | IFNS – UI Master existed under Autopilot Hub. Step 01–13 pages were children of IFNS – UI Master. A Step 14 page existed in the workspace (with title “Step 14 – Sections 11.0–14.0 – Advanced Awareness”) but was not a direct child of IFNS – UI Master. The sync script loops only over direct child pages of IFNS – UI Master. :contentReference[oaicite:2]{index=2} |
| **Root cause** | 1) Step 14 was **not** a direct child page of IFNS – UI Master, so the sync script never saw it in `list_child_pages(...)` and therefore skipped it. 2) The “Archiving block …” lines were misunderstood: they refer to archiving **paragraph blocks inside the 01/02/03 subpages**, not archiving whole Step pages. |
| **Fix** | Introduced `ifns_ensure_step_pages.py`, which finds IFNS – UI Master and ensures that `Step 01 ... Step 14` pages exist as **direct children** under it. Then rerun `python .\scripts\ifns_sync_all_steps.py` so Step 14 is included and its 01/02/03 subpages are updated from `Step_14_Advanced_Awareness_and_Quantum_Cognition.md`. |
| **Prevent / lessons** | 1) For any group of pages that a sync script should touch, always ensure they are under the expected parent (here: IFNS – UI Master). 2) Use lightweight “ensure pages” scripts to normalize structure instead of creating pages manually. 3) Remember that “Archiving block …” in logs means **clearing old content blocks** inside a page, not deleting the page itself. |
| **Commands** | `python .\scripts\ifns_ensure_step_pages.py` to normalize Step pages, then `python .\scripts\ifns_sync_all_steps.py` to push content. |
## 2025-11-18 – Duplicate Step 07–13 pages created (title mismatch)

| Field    | Details |
|---------|---------|
| **Area** | IFNS – Notion structure (IFNS – UI Master) + sync scripts |
| **Symptom** | After running `ifns_ensure_step_pages.py` and `ifns_sync_all_steps.py`, the sync log showed Steps 07–13 twice: first as `Step 07 – … (DIL)`, `Step 08 – … (MI)` etc., then again as `Step 07 – … Data Intelligence Layer`, `Step 08 – … Modeling Intelligence`, etc. Notion now shows two Step pages (07–13) under IFNS – UI Master. |
| **Context** | Original Step 07–13 pages existed under IFNS – UI Master with titles that include acronyms `(DIL)`, `(MI)`, `(EI)`, `(MSA)`, `(MSI)`, `(DRA)`, `(SEL)`. The new `ifns_ensure_step_pages.py` used titles without the acronyms, so it did not detect the existing pages as matches and created new Step 07–13 pages with slightly different titles. :contentReference[oaicite:3]{index=3} |
| **Root cause** | The ensure script’s `STEP_TITLES` did not exactly match the titles of the existing Step 07–13 pages (difference in the `(DIL)/(MI)/…` suffix), so it created new pages instead of reusing the originals. The sync script then updated both sets because it scans all child pages whose titles start with `Step XX`. |
| **Fix** | Treat the newer Step 07–13 pages (without acronyms) as canonical, and rename/move the older pages (with `(DIL)/(MI)/…`) to an Archive section (e.g., `Archive – Step 07 – … (old)`). Align future structure around the canonical titles used by the ensure script. |
| **Prevent / lessons** | 1) When using an “ensure pages” script, ensure `STEP_TITLES` exactly match the desired titles in Notion to avoid duplicates. 2) If titles change (e.g., adding acronyms), update both the script and, if needed, rename pages in Notion so they stay consistent. 3) Periodically review IFNS – Notion Page Index + Troubleshooting Log before structural changes. |
| **Commands** | `python .\scripts\ifns_ensure_step_pages.py` then `python .\scripts\ifns_sync_all_steps.py`. Manual cleanup in Notion (rename/move old Step 07–13 pages to Archive). |
## 2025-11-18 – Phase 2 sync skipped (Markdown files not found)

| Field    | Details |
|---------|---------|
| **Area** | IFNS – Phase 2 master pages (`ifns_sync_master_phase2.py`) |
| **Symptom** | Running `python .\scripts\ifns_sync_master_phase2.py` printed:<br>`!! Skipping UI Master Summary: file not found at docs/ifns/IFNS_UI_Master_Summary.md`<br>`!! Skipping Steps Index: file not found at docs/ifns/IFNS_UI_Steps_Index.md`<br>`!! Skipping Drafts & Working Notes: file not found at docs/ifns/IFNS_UI_Drafts_and_Working_Notes.md` and finished with no pages updated. |
| **Context** | Phase 2 script was correctly wired to IFNS – UI Master and `NOTION_ROOT_PAGE_ID`, but the three new Markdown spec files were not yet present at the expected paths under `docs/ifns`. :contentReference[oaicite:1]{index=1} |
| **Root cause** | The script’s `PAGE_FILES` mapping pointed to `docs/ifns/IFNS_UI_Master_Summary.md`, `IFNS_UI_Steps_Index.md`, and `IFNS_UI_Drafts_and_Working_Notes.md`, but those files did not exist in that folder (either still in Downloads or named differently). |
| **Fix** | Move/copy the three Phase 2 Markdown files into `docs/ifns` and rename them exactly to the expected filenames, then rerun `python .\scripts\ifns_sync_master_phase2.py`. |
| **Prevent / lessons** | 1) Before running a new sync script, confirm all mapped Markdown files actually exist using `dir` with the expected pattern. 2) Keep filenames in `PAGE_FILES` aligned with the naming convention used in Git and in Notion documentation. |
| **Commands** | `dir .\docs\ifns\IFNS_UI_*.md` to verify files, then `python .\scripts\ifns_sync_master_phase2.py` after placing them. |
## 2025-11-18  Phase 2 master pages synced (auto-discovered Markdown files)

| Field    | Details |
|---------|---------|
| **Area** | IFNS – Phase 2 master pages (`ifns_sync_master_phase2.py`) |
| **Symptom** | Initially, Phase 2 sync reported missing Markdown files for `UI Master Summary`, `Steps Index`, and `Drafts & Working Notes`. After switching to auto-discovery, the script located the `_v2` Markdown files under `docs\ifns` and created the corresponding child pages under IFNS  UI Master. |
| **Context** | Script run from repo root with `.\local_env\notion_env.ps1` loaded. Root page id `29ab22c770d980918736f0dcad3bac83`. The updated script found `IFNS  UI Master` (`2adb22c7-70d9-807f-96ee-c817ecb37402`) and then synced the three Phase 2 pages (`UI Master Summary`, `Steps Index`, `Drafts & Working Notes`). :contentReference[oaicite:3]{index=3} |
| **Root cause** | The first version of the Phase 2 sync script assumed fixed file paths (`docs/ifns/IFNS_UI_*.md`) that did not match the actual filenames (`*_v2.md`). The new version now searches under `docs/` for a `.md` file whose name contains the expected stem (`IFNS_UI_Master_Summary`, etc.), preferring files in `docs\ifns`. |
| **Fix** | Overwrote `scripts/ifns_sync_master_phase2.py` with an auto-discovery implementation and reran `python .\scripts\ifns_sync_master_phase2.py`, which used `IFNS_UI_Master_Summary_v2.md`, `IFNS_UI_Steps_Index_v2.md`, and `IFNS_UI_Drafts_and_Working_Notes_v2.md` to create the three child pages and update their content (4,142 / 3,847 / 2,546 chars respectively). :contentReference[oaicite:4]{index=4} |
| **Prevent / lessons** | 1) Prefer filename-stem matching + auto-discovery over hard-coded full paths when specs may evolve (`v2`, `v3`, etc.). 2) For any new phase, ensure the sync script prints which file it chose so debugging is easy. 3) Keep the rule: after every sync, update both `IFNS_Notion_Page_Index.md` and `IFNS_Troubleshooting_Log.md`. |
| **Commands** | `.\local_env\notion_env.ps1` then `python .\scripts\ifns_sync_master_phase2.py`. |
