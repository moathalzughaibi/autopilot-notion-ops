# IFNS Indicators Quickstart (v0.18)

**Date:** 2025-11-18  
**Scope:** One-page setup to run the indicator/feature pipeline artifacts locally in ~5 minutes, using the v0.10 → v0.18 packs you downloaded from this thread.

---

## 0) Get the packs (v0.10 → v0.18)

Download these archives and unzip into the same project root (they add complementary files; later versions build on earlier ones):

- v0.10 — Soft clipping + stamped exchange-holiday YAMLs → `IFNS_Indicators_Pack_v0_10.zip`
- v0.11 — Policy matrix + unit-test fixtures → `IFNS_Indicators_Pack_v0_11.zip`
- v0.12 — Feature→family map + pytest starter → `IFNS_Indicators_Pack_v0_12.zip`
- v0.13 — Schemas with `family` column + Phase readiness checklists → `IFNS_Indicators_Pack_v0_13.zip`
- v0.14 — Manifests carry `family` + CSV linter + lint reports → `IFNS_Indicators_Pack_v0_14.zip`
- v0.15 — Weekly QC telemetry schema + manifest diff tool → `IFNS_Indicators_Pack_v0_15.zip`
- v0.16 — QC weekly ETL skeleton + CI guard + GH workflow → `IFNS_Indicators_Pack_v0_16.zip`
- v0.17 — ETL reads clip-event logs + computes clip budgets → `IFNS_Indicators_Pack_v0_17.zip`
- v0.18 — IO utilities + synthetic weekly inputs (demo) → `IFNS_Indicators_Pack_v0_18.zip`

> Recommended root on Windows: `E:\GitHub\autopilot-notion-ops`  
> On macOS/Linux: `~/Projects/autopilot-notion-ops`

After unzipping, your tree will include folders like: `docs/`, `sync/ifns/`, `tools/`, `tests/`, `etl/`, `runtime_templates/`, `data/`.

---

## 1) Create a Python env & install deps

**Windows (PowerShell):**
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

**macOS/Linux (bash):**
```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

> `requirements.txt` ships with v0.16+. If missing, just `pip install pytest pandas python-dateutil pyarrow`.

---

## 2) Sanity checks in 60 seconds

### a) Lint the schemas (tags → family consistency)
```bash
python tools/feature_csv_linter.py   --d1 sync/ifns/indicator_feature_schema_v1_with_family.csv   --h1 sync/ifns/indicator_feature_schema_h1_v1_with_family.csv   --out sync/ifns/lint_report.csv
```
Outputs: `sync/ifns/lint_report.csv` (+ `.json`).

### b) Run the pytest starter on fixtures
```bash
pytest -q tests/pytest_starter
```
Uses fixtures from v0.11 and checks bounds, clipping, calendar gaps, and categorical health.

---

## 3) 5‑minute end‑to‑end demo (H1 and D1)

### Option A — H1 demo (MSFT hourly, synthetic week)
```bash
python etl/qc_weekly_etl.py   --manifest sync/ifns/examples/training_manifest_H1_demo.json   --calendar sync/ifns/calendar_gaps_2025.json   --input_glob data/h1_xnas_msft_demo.csv   --clip_glob sync/ifns/examples/clip_events_sample.ndjson   --week_end 2025-11-28   --out sync/ifns/qc_weekly_demo_H1_2025-11-28.ndjson
```
Result: an NDJSON line at `sync/ifns/qc_weekly_demo_H1_2025-11-28.ndjson` with integrity/coverage/NA and `family_breakdown[]` (includes clip-event rates).

### Option B — D1 demo (SPY daily, synthetic week)
```bash
python etl/qc_weekly_etl.py   --manifest sync/ifns/examples/training_manifest_D1_demo.json   --calendar sync/ifns/calendar_gaps_2025.json   --input_glob data/d1_arcx_spy_demo.csv   --week_end 2025-11-28   --out sync/ifns/qc_weekly_demo_D1_2025-11-28.ndjson
```

---

## 4) Inspect outputs

**Windows (PowerShell):**
```powershell
Get-Content sync/ifns/qc_weekly_demo_H1_2025-11-28.ndjson
```
**macOS/Linux (bash):**
```bash
cat sync/ifns/qc_weekly_demo_H1_2025-11-28.ndjson
```

You should see keys like: `integrity_pct`, `coverage_pct_mean`, `max_na_pct_any_feature`, `clip_events_pct`, and `family_breakdown` entries for MOMENTUM/TREND/VOLATILITY/CONTEXT.

---

## 5) Guardrail tools (optional but recommended)

### a) Manifest diff (what changed between two views?)
```bash
python tools/manifest_diff.py   --a sync/ifns/training_manifest_D1_v1_1.json   --b sync/ifns/training_manifest_H1_v1_0.json   --out sync/ifns/manifest_diff_example.json
```

### b) CI guard (block unauthorized manifest changes)
```bash
python tools/ci_manifest_guard.py   --baseline sync/ifns/training_manifest_D1_v1_1.json   --candidate sync/ifns/training_manifest_D1_v1_1.json   --out sync/ifns/manifest_guard_report_D1.json
```
Relax policy with flags (e.g., `--allow-modified`, `--allow-family-changes`).

---

## 6) Runtime templates & calendars

Runtime YAML templates live in `runtime_templates/` (v0.10). They already include a **2025 baseline US holiday set** under `calendar_overrides:` so QA expects half-days/market closures.

When promoting to production, replace the overrides with an authoritative exchange calendar feed.

---

## 7) Where to look when customizing

- **Per-feature QC + clipping:** `sync/ifns/training_manifest_*.json` (v0.10, v0.14 carry `family` too).
- **Families & policies:** `sync/ifns/feature_policy_matrix.csv` (v0.11) and `sync/ifns/feature_family_map.csv` (v0.12).
- **Schemas with family column:** `sync/ifns/indicator_feature_schema_*_with_family.csv` (v0.13).
- **Weekly telemetry contract:** `sync/ifns/qc_weekly_schema_v1.json` (v0.15).
- **Clip-event logs:** `sync/ifns/clip_events_schema_v1.json` + example NDJSON (v0.17).
- **ETL + IO utilities:** `etl/qc_weekly_etl.py` and `tools/io_utils.py` (v0.15–v0.18).
- **Tests & fixtures:** `tests/pytest_starter/` and `tests/fixtures/` (v0.11–v0.12).

---

## 8) 60‑second checklist before handing to engineering

- [ ] Linter clean: `lint_report.csv` contains only INFO/WARNs you accept.
- [ ] `pytest` passes locally with fixtures.
- [ ] Demo ETL produced NDJSON with sensible coverage/clip rates.
- [ ] Manifest diff/guard configured in your CI to catch unauthorized feature changes.
- [ ] Calendar behavior matches expectations around holidays/early closes.

---

## 9) FAQ

**Q: Do the demos write to my real data lake?**  
A: No. The quickstart uses synthetic CSVs shipped in `data/` and example manifests under `sync/ifns/examples/`.

**Q: Where do I adjust clip budgets?**  
A: Globally: `manifest.policy_defaults.clip_policy.max_clipped_pct_per_day`. Per-feature override in each manifest’s `per_feature_qc[feature_id].clip_policy.max_clipped_pct_per_day`.

**Q: How do I add a new H1 feature?**  
A: Add to the H1 schema CSV + whitelist, update the manifest columns (and `per_feature_qc` entry), then run the linter and CI guard. Use the pytest starter to add a focused fixture if bounds/clipping rules are special.

---

**That’s it — you’re ready to iterate on real data.**  
For next steps, we can issue production-grade exchange calendars, wire the ETL to your storage (S3/ADLS), and expand fixtures to cover your L2/L3 composites.
