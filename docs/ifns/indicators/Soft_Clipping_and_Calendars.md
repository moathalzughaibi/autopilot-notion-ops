# v0.10 — Soft Clipping Policies + Exchange-Holiday Calendars (Stamped)
Date: 2025-11-18

## Manifests
- Added explicit **clip_policy** per numeric feature (`method: cap_and_log`, soft_clip thresholds by slice).
- Kept coverage/NA/drift/value expectations and raw-value exceptions.
- Files:
  - `sync/ifns/training_manifest_D1_v1_1.json`
  - `sync/ifns/training_manifest_H1_v1_0.json`

## YAMLs with calendars (2025 baseline)
- Stamped holiday & early-close overrides into all H1/D1 runtime templates so QA expects intentional gaps.
- Files (examples):
  - `runtime_templates/RUN_IFNS_FEATUREVIEW_H1_XNAS_MSFT_V1_1.yaml`
  - `runtime_templates/RUN_IFNS_FEATUREVIEW_H1_ARCX_SPY_V1_1.yaml`
  - `runtime_templates/RUN_IFNS_FEATUREVIEW_H1_XNAS_AAPL_V1_1.yaml`
  - `runtime_templates/RUN_IFNS_FEATUREVIEW_H1_ARCX_IWM_V1_1.yaml`
  - `runtime_templates/RUN_IFNS_FEATUREVIEW_D1_XNYS_AAPL_V1_1.yaml`
  - `runtime_templates/RUN_IFNS_FEATUREVIEW_D1_ARCX_SPY_V1_1.yaml`
  - `runtime_templates/RUN_IFNS_FEATUREVIEW_D1_XNAS_MSFT_V1_1.yaml`
  - `runtime_templates/RUN_IFNS_FEATUREVIEW_D1_ARCX_IWM_V1_1.yaml`

**Note:** The calendar block is a **baseline** for 2025. In production, swap in the authoritative exchange calendar (ICS or service) at job init; this block ensures QA signals are deterministic meanwhile.
