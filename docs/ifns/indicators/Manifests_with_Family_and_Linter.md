# v0.14 — Family in Manifests + CSV Linter
Date: 2025-11-18

## What changed
- **Manifests updated**: each `per_feature_qc` entry now carries `family`, with a `family_breakdown` at top-level.
- **CSV Linter added**: `tools/feature_csv_linter.py` checks tags→family consistency, duplicate IDs, and basic scaling/dtype sanity.
- **Reports**: `sync/ifns/lint_report.csv` and `.json`

## How to run linter locally
```
python tools/feature_csv_linter.py   --d1 sync/ifns/indicator_feature_schema_v1_with_family.csv   --h1 sync/ifns/indicator_feature_schema_h1_v1_with_family.csv   --out sync/ifns/lint_report.csv
```
