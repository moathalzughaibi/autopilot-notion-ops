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
