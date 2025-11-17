# Autopilot Notion Ops — Local Guide (Moath)

Path on my PC:

- `E:\GitHub\autopilot-notion-ops`

This repository is the **integration layer between GitHub and Notion** for:

- Autopilot Hub
- IFNS (Intelligent Financial Neural System)

It syncs Markdown and CSV files in this repo ⇄ to Notion pages and databases using GitHub Actions and local Python scripts. :contentReference[oaicite:3]{index=3}

---

## 1. Folder layout (how I should think about it)

| Folder / File        | What it is for (in my words) |
|----------------------|------------------------------|
| `.github/workflows`  | GitHub Actions that do the real work: seed Notion, sync IFNS, run audits, etc. |
| `docs/ifns/`         | IFNS pages in Markdown. These become Notion pages (conceptual, operational, dashboards, reference). :contentReference[oaicite:4]{index=4} |
| `sync/ifns/`         | IFNS CSV tables. Each file becomes / updates a Notion database (layers, experiments, backtests, models, portfolios, execution logs, risk alerts). :contentReference[oaicite:5]{index=5} |
| `config/`            | Mapping files that tell the scripts how GitHub files map to Notion (for example `ifns-mappings.json`). |
| `scripts/`           | Python utilities I can run from my PC to sync, audit, or apply planned changes to Notion. :contentReference[oaicite:6]{index=6} |
| `content/`           | Extra content (snippets, templates, notes) that may be pushed to Notion later. |
| `databases/`         | Source CSVs or exports related to Notion databases. |
| `pages/`             | Draft Markdown pages that might be promoted into `docs/ifns` or other areas. |
| `schemas/`           | JSON/YAML schemas that define structure for configs, filters, or payloads. |
| `README.md`          | Main technical README for the project (public, generic description). |
| `README_Moath_Local.md` | This file: my personal notes on how I use the repo from my PC. |

---

## 2. How this repo talks to Notion (high level)

1. **Secrets / credentials** are configured (either via GitHub Secrets or an `Integration Setup.json` file with my Notion token and root page IDs). :contentReference[oaicite:7]{index=7}  
2. I edit content locally in `docs/ifns` and `sync/ifns` and then commit + push to `main`.
3. GitHub Actions detect the changes and:
   - Create / update Notion pages from `docs/ifns/*.md`.
   - Create / update Notion databases from `sync/ifns/*.csv`.
   - Optionally move stale items to an Archive instead of deleting them (archive-safe policy). :contentReference[oaicite:8]{index=8}
4. Optional: audit workflows generate reports and “change plans” which I can review before applying.

---

## 3. Working locally from my PC

### 3.1. Basic Git workflow (mirror style)

From `E:\GitHub\autopilot-notion-ops`:

```powershell
# See what changed
git status

# Stage all changes
git add .

# Commit with a message
git commit -m "Describe the change I made"

# Push to main (GitHub will run the Actions)
git push origin main

# Later, update my local mirror with any new changes
git pull origin main
---

## 5. Code vs Config vs Content (for any agent)

To avoid confusion, treat the repository in three layers:

### 5.1. Code

**What counts as code:**

- `scripts/*.py`
- `.github/workflows/*.yml`
- Anything under `schemas/` that defines strict JSON/YAML schemas.

**Rules for code changes:**

- Do **not** change code casually.
- Any change to Python scripts or workflows must have a clear reason in the commit message.
- Try to keep changes **backwards compatible** with existing content/configs.
- If you change a script’s behavior in a breaking way, note it in the commit message and (ideally) in a `CHANGELOG` later.

### 5.2. Config

**Examples:**

- `config/*.json`
- Any future `*.yaml` files inside `config/`
- Mapping files that connect GitHub files to Notion pages/databases.

**Rules:**

- Config files control **where** things sync and **how** they map.
- Changes here can affect many pages/databases in Notion.
- Before pushing, confirm that mappings (IDs, database names, page slugs) are correct.
- When in doubt, run a dry-run / audit script before a full sync (see section 6).

### 5.3. Content (safe to change frequently)

**Examples:**

- `docs/ifns/*.md` → IFNS pages (narratives, specs, frameworks, etc.)
- `sync/ifns/*.csv` → IFNS tables (layers, experiments, models, backtests, execution, risk alerts, etc.)
- `pages/*.md`, `databases/*.csv` → other pages/tables that may be synced.

**Rules:**

- This is the **main area** for day-to-day editing for specs and data.
- It is safe to edit, refine, and extend as long as:
  - The structure of the CSV/Markdown matches what the mappings expect.
  - You keep consistent IDs / keys if they are used to match rows/items.
---

## 6. Versioning & Git conventions

This repo is used both as:

- A **tooling layer** (code + workflows).
- A **knowledge/spec layer** (IFNS docs + tables).

### 6.1. Branching model

For now, we keep it simple:

- `main` = source of truth.
- Small changes can go directly to `main`.
- For bigger or risky changes (especially in `scripts/` or `config/`), create a temporary feature branch:

```bash
git checkout -b feature/short-name
# edit files
git add .
git commit -m "[feature] Short description"
git push origin feature/short-name
git tag -a v0.6 -m "IFNS v0.6 telemetry integration"
git push origin v0.6
### Notion smoke test (local)

```powershell
$env:NOTION_TOKEN = "..."           # from GitHub secret NOTION_TOKEN
$env:NOTION_ROOT_PAGE_ID = "..."    # from NOTION_ROOT_PAGE_ID
python .\scripts\notion_smoke_test.py
## Local Notion connection (smoke test)

To verify my local dev environment can talk to Notion using the same credentials
as GitHub Actions:

```powershell
# In PowerShell at E:\GitHub\autopilot-notion-ops

# 1) Set the Notion integration token (same value as the GitHub secret NOTION_TOKEN)
$env:NOTION_TOKEN = "ntn_...<redacted>..."

# 2) Set the Autopilot Hub root page id (same as NOTION_ROOT_PAGE_ID)
$env:NOTION_ROOT_PAGE_ID = "29ab22c770d980918736f0dcad3bac83"

# 3) Run the smoke test
python .\scripts\notion_smoke_test.py
## Sync IFNS Steps 01–02 from GitHub → Notion

Pre-requisite (done once): `local_env/notion_env.ps1` holds my Notion token + root page ID
and `local_env/` is ignored in git.

To sync the content of Steps 01 and 02 into Notion:

```powershell
cd E:\GitHub\autopilot-notion-ops

# Load local Notion env (NOTION_TOKEN, NOTION_ROOT_PAGE_ID)
.\local_env\notion_env.ps1

# Run the sync script
python .\scripts\ifns_sync_steps_01_02.py
