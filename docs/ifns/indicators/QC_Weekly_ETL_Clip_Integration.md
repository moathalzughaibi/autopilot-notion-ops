# v0.17 — Clip-Event Integration in QC Weekly ETL
Date: 2025-11-18

## New
- `--clip_glob` flag reads **feat_softclip** logs (CSV or NDJSON) matching `clip_events_schema_v1.json`.
- Computes:
  - `clip_events_pct` = sum(clips) / sum(non-NA feature values)
  - `clip_budget_violations` = count of (feature, day) where clip rate > budget
    - Budget sourced from `manifest.policy_defaults.clip_policy.max_clipped_pct_per_day` (default 0.005),
      overridden by `per_feature_qc[feature_id].clip_policy.max_clipped_pct_per_day` when present.
  - Per-family `clip_events_pct` in `family_breakdown[]`.

## Example run
```
python etl/qc_weekly_etl.py   --manifest sync/ifns/training_manifest_H1_v1_0.json   --calendar sync/ifns/calendar_gaps_2025.json   --input_glob data/h1/xnas_msft/*.parquet   --clip_glob sync/ifns/examples/clip_events_sample.ndjson   --week_end 2025-11-28   --out sync/ifns/qc_weekly_2025-11-28.ndjson
```
