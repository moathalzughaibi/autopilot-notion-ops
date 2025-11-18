# Weekly QC Telemetry — Schema (V1) with Family Breakdown
Date: 2025-11-18

Artifacts:
- Schema: `sync/ifns/qc_weekly_schema_v1.json`
- Example: `sync/ifns/qc_weekly_example_v1.ndjson`

**Design goals**
- One event per **view per week**.
- Includes both overall metrics and `family_breakdown[]` for at-a-glance rollups.
- `manifest_sha256` pins the exact feature set used that week.

**Emit guidance**
- Write NDJSON lines to a dated file (e.g., `qc_weekly_2025-11-28.ndjson`).
- Use the per-feature **policy thresholds** from the training manifest to compute coverage/drift/clipping, then aggregate to family-level.
