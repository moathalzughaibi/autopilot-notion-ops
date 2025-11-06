# autopilot-notion-ops

> Unified Notion ⇄ GitHub integration for **Autopilot Hub** + **IFNS (The Intelligent Financial Neural System)**

_Last updated: 2025-11-06 · Status: Stable · Policy: **Archive-Safe** (no destructive deletes)_

---

## 🚀 Overview
This repository hosts the **Autopilot Notion Integration Layer** and the **IFNS** module. It enables bidirectional sync between GitHub (Markdown/CSV) and Notion (Pages/Databases), plus health monitoring and automations (KPIs, incidents, and actions).

### Key capabilities
- **Seed & Sync** Notion pages/databases from GitHub.
- **Two-way ops**: run typed commands via Actions to list schemas or push updates.
- **IFNS module**: opinionated framework for a financial neural system (Conceptual, Operational, Dashboard, Analytics).
- **Unified KPIs + Neural Health Indicator** surfaced in Notion.
- **Archive-Safe** governance: stale pages are **archived**, not deleted.

---

## 🗂️ Repository layout
```
/docs/ifns/                  # Markdown pages for IFNS (Conceptual / Operational / Wireframe / Analytics / Reference)
/sync/ifns/                  # CSV seeds for Notion databases (Layers, Backtests, Experiments, Registry, Portfolios, Execution, Risk Alerts)
/scripts/                    # Sync & audit utilities (see below)
/config/                     # Integration mappings (e.g., ifns-mappings.json)
.github/workflows/           # Actions (seed/sync/ops/ifns-sync/audit)
Integration Setup.json       # (optional) Notion credentials if not using GitHub secrets
```

---

## 🔐 Integration setup
Use **GitHub Secrets** (recommended):
- `NOTION_TOKEN` – Notion internal integration token
- `ROOT_PAGE_ID` – Notion root page to host Autopilot/IFNS
- `ARCHIVE_PAGE_ID` – Notion Archive page for safe archiving

_or_ provide `Integration Setup.json` with:
```json
{ "notion_token": "...", "root_page_id": "...", "archive_page_id": "..." }
```

---

## ⚙️ GitHub Actions
| Workflow | Purpose | Triggers |
|---|---|---|
| `notion-seed.yml` | Create initial pages/DBs (Autopilot) | Manual |
| `notion-sync.yml` | Sync CSV → Notion DBs | Push to `sync/**` |
| `ops-command-runner.yml` | Run typed Notion ops (list/show/apply) | Manual |
| `notion-integration-layer.yml` | Bi-directional integration helpers | Scheduled/Manual |
| **`ifns-sync.yml`** | **Sync IFNS pages/DBs; optional archive policy** | Push to `docs/ifns/**` or `sync/ifns/**`, Manual with input |
| `notion_audit.yml` | Weekly audit & duplicate detection; emits plan/report | Weekly/Manual |

### IFNS Sync (important)
- Creates an **IFNS root** page under `ROOT_PAGE_ID`.
- Pushes pages from `/docs/ifns/*.md`.
- Creates databases from `/sync/ifns/*.csv`.
- Optional input `apply_archive=true` moves stale IFNS pages (≥ 60d) to Archive.

---

## 🧠 IFNS module (Financial Neural System)
### Pages (Markdown → Notion)
- **Conceptual Framework** – seven layers (Data → Feature → Model → Signal → Risk → Execution → Feedback).
- **ML Operational Framework** – APIs, System Layers Tracker, Model Registry, Portfolio Matrix.
- **IFNS Main Dashboard – Wireframe** – layout, neural pathway (Mermaid), navigation.
- **Dashboard Analytics (Backtesting & Live Intelligence)** – KPIs, backtests, paper trading, attribution.
- **Reference Library** – source docs & artifacts.

### Databases (CSV → Notion)
- `System Layers Tracker` · `Backtest Results Table` · `Experiment Logs` · `Model Registry` · `Portfolio Matrix` · `Execution API Log` · `RiskAPI Alerts`

### Unified KPI Layer + Neural Health Indicator
- KPIs: **Active Models, Sharpe, MaxDD, Slippage, Risk Alerts, Retrained Models (7d), Phase Completion**.
- Health formula → one color: 🟢 Stable · 🟡 Attention · 🟠 Warning · 🔴 Critical · ⚫ Offline.

### Incident → Action Items Auto-Generator
- Incident types: **Model / Risk / Execution / Data / Integration**.
- Generates follow-up tasks in **Phase Tasks** with **SLA**, **Priority**, and **DoD** criteria.

---

## 🧯 Archive-Safe policy
- Stale pages (no edits in ≥ **60 days**) are moved under `ARCHIVE_PAGE_ID` instead of deleting.
- Duplicate titles (≥ **84%** similarity) are suggested for merge/rename via weekly audit report.

---

## ▶️ Quickstart
1. Set secrets (`NOTION_TOKEN`, `ROOT_PAGE_ID`, `ARCHIVE_PAGE_ID`) or provide `Integration Setup.json`.
2. Commit IFNS content under `/docs/ifns` and `/sync/ifns`.
3. Push to main → **ifns-sync** runs and provisions Notion.
4. (Optional) Run **Notion Audit** workflow weekly to keep your space clean.

---

## 🧪 Local utilities
```bash
pip install requests python-dateutil PyYAML rapidfuzz pandas markdownify python-frontmatter
python scripts/ifns_sync.py --config config/ifns-mappings.json
# audit plan/report
python scripts/audit_notion.py --project "ML" --filters examples/filters.example.yaml
python scripts/apply_changes.py --plan plans/decision_plan.yaml --safe
```

---

## 🧭 Governance & Safety
- All destructive ops are **disabled by default**. Use archive instead of delete.
- Workflows are **idempotent**: re-runs won’t duplicate content.
- Clear ownership via Incident → Phase Tasks → Gate Tracker.

---

## 🤝 Contributing
1) Open a PR with changes to `/docs/ifns` or `/sync/ifns`.  
2) CI will preview the plan and the audit report.  
3) Merge → Notion updates automatically.

---

© 2025 Autopilot / IFNS
