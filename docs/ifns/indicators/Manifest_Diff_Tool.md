# Manifest Diff Tool
Date: 2025-11-18

Usage:
```
python tools/manifest_diff.py --a sync/ifns/training_manifest_D1_v1_1.json --b sync/ifns/training_manifest_H1_v1_0.json --out sync/ifns/manifest_diff_report.json
```
The report includes:
- added/removed features,
- order changes,
- per_feature_qc differences (thresholds, dtype, family, clip_policy),
- meta changes (view/horizon/frequency/alignment).
