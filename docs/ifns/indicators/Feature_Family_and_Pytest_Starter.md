# v0.12 — Feature→Family Map + Pytest Starter
Date: 2025-11-18

## Files
- `sync/ifns/feature_family_map.csv` — machine-readable mapping used for dashboards, policy overrides, and reports.
- `tests/pytest_starter/test_feature_contracts.py` — minimal tests for fixtures/assertions made in v0.11.
- `pyproject.toml` — points pytest at the starter folder.

## Notes
- Family inference is by **feature_id pattern** and optional `tags`. You can refine by editing the CSV directly or by adding tags in the schemas.
