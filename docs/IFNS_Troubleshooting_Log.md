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
