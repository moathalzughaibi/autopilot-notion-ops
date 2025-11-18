# QC Weekly ETL — Skeleton
Date: 2025-11-18

Run (example):
```
python etl/qc_weekly_etl.py --manifest sync/ifns/training_manifest_H1_v1_0.json ^
  --calendar sync/ifns/calendar_gaps_2025.json ^
  --input_glob data/h1/xnas_msft/*.parquet ^
  --week_end 2025-11-28 ^
  --out sync/ifns/qc_weekly_2025-11-28.ndjson
```

What it does (baseline):
- Loads the manifest → uses `columns` as the authoritative feature list, and `family` for rollups.
- Computes simple coverage/NA per feature from files matched by `input_glob`.
- Estimates expected rows using the calendar + frequency (skeleton logic; swap with your exchange calendar API if needed).
- Emits one NDJSON record per run, conforming to `QC_WEEKLY_SUMMARY_V1`.
