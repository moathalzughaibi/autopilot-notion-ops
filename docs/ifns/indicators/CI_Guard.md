# CI Guard — How to use
Date: 2025-11-18

Artifacts:
- `tools/ci_manifest_guard.py` — policy gate over `manifest_diff.py`
- `.github/workflows/ci_ifns_guard.yml` — runs linter, pytest, and the guard

To allow certain changes in a hotfix PR, pass flags in workflow step:
```
python tools/ci_manifest_guard.py ^
  --baseline sync/ifns/training_manifest_D1_v1_1.json ^
  --candidate sync/ifns/training_manifest_D1_v1_1.json ^
  --allow-modified --allow-family-changes --out sync/ifns/manifest_guard_report_D1.json
```
