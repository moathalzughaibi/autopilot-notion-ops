# v0.18 — IO Utilities + Synthetic Weekly Inputs (DEMO)
Date: 2025-11-18

## Utilities
- `tools/io_utils.py`
  - `sha256_of_file(path)`
  - `read_table_glob(pattern, columns=None, ts_col="timestamp")` — CSV/Parquet loader
  - `read_ndjson_glob(pattern)` — NDJSON/JSONL reader
  - `ensure_columns(df, required, ts_col="timestamp")` — add missing cols (NaN)

## Demo manifests/schemas/whitelists
- `sync/ifns/examples/indicator_feature_schema_h1_demo.csv`
- `sync/ifns/examples/indicator_feature_schema_d1_demo.csv`
- `sync/ifns/examples/feature_view_H1_demo.csv`
- `sync/ifns/examples/feature_view_D1_demo.csv`
- `sync/ifns/examples/training_manifest_H1_demo.json`
- `sync/ifns/examples/training_manifest_D1_demo.json`

## Synthetic inputs
- H1 week (MSFT): `data/h1_xnas_msft_demo.csv` (Mon/Tue/Wed; Fri early close)
- D1 week (SPY): `data/d1_arcx_spy_demo.csv` (Mon/Tue/Wed/Fri)

### Try the ETL end-to-end (H1 demo)
```
python etl/qc_weekly_etl.py   --manifest sync/ifns/examples/training_manifest_H1_demo.json   --calendar sync/ifns/calendar_gaps_2025.json   --input_glob data/h1_xnas_msft_demo.csv   --clip_glob sync/ifns/examples/clip_events_sample.ndjson   --week_end 2025-11-28   --out sync/ifns/qc_weekly_demo_H1_2025-11-28.ndjson
```

### Try the ETL end-to-end (D1 demo)
```
python etl/qc_weekly_etl.py   --manifest sync/ifns/examples/training_manifest_D1_demo.json   --calendar sync/ifns/calendar_gaps_2025.json   --input_glob data/d1_arcx_spy_demo.csv   --week_end 2025-11-28   --out sync/ifns/qc_weekly_demo_D1_2025-11-28.ndjson
```
