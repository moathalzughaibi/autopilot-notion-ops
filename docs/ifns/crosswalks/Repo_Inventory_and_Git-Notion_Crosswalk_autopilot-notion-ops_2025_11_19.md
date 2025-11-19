# Repo Inventory & Git–Notion Crosswalk (autopilot-notion-ops_2025_11_19)

This handover file documents the **Git-side assets** from the `autopilot-notion-ops` repo and maps them to the 
Notion-first Source-of-Truth (SoT) plan defined in Phases 0–5.

## 1. Repo overview

Top-level folders in the archive:

- `.git/`
- `.github/`
- `.venv/`
- `.vscode/`
- `IFNS_Notion_DB_Buildout_V2/`
- `config/`
- `content/`
- `data/`
- `docs/`
- `etl/`
- `local_env/`
- `logs/`
- `meta_index/`
- `notion/`
- `runtime_templates/`
- `schemas/`
- `scripts/`
- `sync/`
- `tests/`
- `tools/`
- `‎.github/`

Focus for IFNS + Notion SoT is on:

- `content/databases/` – generic Autopilot-level CSV databases.

- `sync/ifns/` – IFNS-specific CSV/JSON mirrors for Notion DBs.

- `IFNS_Notion_DB_Buildout_V2/` – scripts + config for auto-creating V2 DBs in Notion.

- `runtime_templates/` – YAML run templates for feature views.

- `schemas/` – shared DB schema definitions (e.g. `databases.yml`).


## 2. IFNS_Notion_DB_Buildout_V2 – DB map

The file `IFNS_Notion_DB_Buildout_V2/config/ifns_v2_db_map.json` defines how Git CSV/JSON files map to Notion DBs.

Key entries (summarized):

| Key | Path | Primary key | Notion DB UUID | Notion DB logical role | Phase |

|-----|------|-------------|----------------|------------------------|-------|
| `FeatureSchemaV1` | `sync/ifns/indicator_feature_schema_v1_with_family.csv` | `feature_name` | `6484618c-ca0b-4a31-9544-4ecf11d0df87` | Indicator Feature Schema (base, all families) | Phase 4 – Feature Catalog / schemas |
| `FeatureSchemaH1` | `sync/ifns/indicator_feature_schema_h1_v1_with_family.csv` | `feature_name` | `dfe40c25-9e24-4928-8fa1-4bed6114ce9f` | Indicator Feature Schema for H1 view | Phase 4 – H1 Feature Schema |
| `PolicyMatrix` | `sync/ifns/feature_policy_matrix.csv` | `` | `9e48b82d-4d6a-4d2b-aa17-a88080bc35ac` | Feature Policy Matrix (risk/usage constraints) | Phase 4 – Feature Policy Matrix |
| `FamilyMap` | `sync/ifns/feature_family_map.csv` | `feature_name` | `e4562cd0-3d8a-4986-b72f-a9cf94b68e7e` | Feature Family Map (families & roles) | Phase 4 – Feature Family Map |
| `UniverseP2` | `sync/ifns/indicators_universe_catalog_phase2.csv` | `symbol` | `de828cc4-0b81-49fa-aa69-d328d6930779` | Universe Catalog (Phase 2 universe) | Phase 4 – Universe catalog |
| `CatalogL1` | `sync/ifns/indicators_catalog_L1_phase3.csv` | `indicator_id` | `066b5cc5-6f8f-4f1b-aa10-59a351e608fa` | Indicators – L1 Catalog (Phase 3) | Phase 4 – L1 Catalog |
| `CatalogL2L3` | `sync/ifns/indicators_catalog_L2L3_phase4.csv` | `composite_id` | `ef3175fe-046d-47b8-8944-607d5bcf5d21` | Indicators – L2/L3 Framework Catalog (Phase 4) | Phase 4 – L2/L3 Catalog |
| `QCWeekly` | `sync/ifns/qc_weekly_schema_v1.json` | `entry_id` | `cee29b9e-4071-45a5-bb9d-9a4f7b543ceb` | QCWeekly schema / DB id (telemetry) | Phase 3 – QCWeekly DB (telemetry) |
| `CalendarGaps2025` | `sync/ifns/calendar_gaps_2025.json` | `event_id` | `2afb22c7-70d9-8100-ae4a-d9f64b6b6441` | Calendar gaps 2025 schema / DB id | Phase 3 – Calendar gaps DB |

## 3. `sync/ifns/` CSVs – Git mirrors of core IFNS DBs

The following CSVs in `sync/ifns/` should be treated as **Git mirrors** of Notion databases or specs. 
The SoT is Notion; these CSVs are export/import artifacts.

| File | Purpose (short) | Phase |

|------|------------------|-------|
| `sync/ifns/Backtest_Results_Table.csv` | Backtest results table (per-run / per-strategy). | Later – Backtesting DB (future phase) |
| `sync/ifns/Execution_API_Log.csv` | Execution API log (orders/fills/events). | Later – Ops / Execution / Risk DBs |
| `sync/ifns/Experiment_Logs.csv` | Experiment log table for ML runs. | Later – Experiments / Model registry |
| `sync/ifns/Model_Registry.csv` | Model registry table. | Later – Experiments / Model registry |
| `sync/ifns/Portfolio_Matrix.csv` | Portfolio matrix (allocations / configurations). | Later – Ops / Execution / Risk DBs |
| `sync/ifns/RiskAPI_Alerts.csv` | Risk API alerts table. | Later – Ops / Execution / Risk DBs |
| `sync/ifns/System_Layers_Tracker.csv` | System layers tracker (status by layer). | Later – Ops / Execution / Risk DBs |
| `sync/ifns/examples/feature_view_D1_demo.csv` | Example feature view outputs (demo D1/H1). |  |
| `sync/ifns/examples/feature_view_H1_demo.csv` | Example feature view outputs (demo D1/H1). |  |
| `sync/ifns/examples/indicator_feature_schema_d1_demo.csv` | Feature schema (base or H1) with family annotations. | Phase 4 – Feature schemas |
| `sync/ifns/examples/indicator_feature_schema_h1_demo.csv` | Feature schema (base or H1) with family annotations. | Phase 4 – Feature schemas |
| `sync/ifns/feature_family_map.csv` | CSV mirror of Feature Family Map (families & roles). | Phase 4 – Family Map |
| `sync/ifns/feature_policy_matrix.csv` | CSV mirror of Feature Policy Matrix. | Phase 4 – Policy Matrix |
| `sync/ifns/indicator_feature_schema_h1_v1_with_family.csv` | Feature schema (base or H1) with family annotations. | Phase 4 – Feature schemas |
| `sync/ifns/indicator_feature_schema_v1.csv` | Feature schema (base or H1) with family annotations. | Phase 4 – Feature schemas |
| `sync/ifns/indicator_feature_schema_v1_with_family.csv` | Feature schema (base or H1) with family annotations. | Phase 4 – Feature schemas |
| `sync/ifns/indicators_catalog_L1_phase3.csv` | L1 indicator catalog (Phase 3). | Phase 4 – Catalog / Universe |
| `sync/ifns/indicators_catalog_L2L3_phase4.csv` | L2/L3 framework catalog (Phase 4). | Phase 4 – Catalog / Universe |
| `sync/ifns/indicators_universe_catalog_phase2.csv` | Indicator universe catalog for Phase 2. | Phase 4 – Catalog / Universe |
| `sync/ifns/lint_report.csv` |  |  |

## 4. `content/databases/` – generic Autopilot databases

These CSVs represent general Autopilot project DBs. They are **not IFNS-specific**, but the same SoT principle applies: 
Notion DB → CSV mirror in Git.

| File | Purpose |

|------|---------|

| `content/databases/Autopilot_Architecture_Notes.csv` | Architecture notes log (design-level). |
| `content/databases/Autopilot_Decisions_Log.csv` | Decision log across the Autopilot project. |
| `content/databases/Autopilot_Experiments_Log.csv` | Experiments log (not IFNS-specific). |
| `content/databases/Autopilot_Glossary.csv` | Glossary of terms. |
| `content/databases/Autopilot_Tasks_Backlog.csv` | Backlog of tasks / tickets. |
| `content/databases/Autopilot_Variables_Config.csv` | Central variables/config registry. |

## 5. Telemetry & runtime JSON/YAML artifacts

These files support telemetry schemas, manifests, and runtime templates. They belong primarily to **Phase 3** 
and to the runtime/scheduling parts of **Phase 5 SoT rules**.

### 5.1 JSON files under `sync/ifns/`

| File | Purpose (short) | Phase |

|------|------------------|-------|

| `IFNS_Notion_DB_Buildout_V2/config/ifns_v2_db_map.json` | Authoritative map from CSV/JSON paths → Notion DB IDs. | All phases – DB crosswalk |
| `sync/ifns/calendar_gaps_2025.json` | JSON representation of calendar gaps 2025 (schema mirror). | Phase 3 – CalendarGaps2025 DB |
| `sync/ifns/clip_events_schema_v1.json` | JSON schema for clipping events telemetry. | Phase 3 – Telemetry schema – clipping events |
| `sync/ifns/examples/training_manifest_D1_demo.json` | Training manifest JSON (D1/H1 demo or versioned manifests). | Later – Training manifests (modeling/runtime) |
| `sync/ifns/examples/training_manifest_H1_demo.json` | Training manifest JSON (D1/H1 demo or versioned manifests). | Later – Training manifests (modeling/runtime) |
| `sync/ifns/lint_report.json` | Lint report for IFNS spec and manifests. | Later – Linting & validation |
| `sync/ifns/qc_weekly_schema_v1.json` | JSON schema for QCWeekly telemetry. | Phase 3 – QCWeekly DB |
| `sync/ifns/test_assertions_manifest.json` | Test assertions manifest for CI/guard workflows. | Later – CI / guardrails |
| `sync/ifns/training_manifest_D1_v1_1.json` | Training manifest JSON (D1/H1 demo or versioned manifests). | Later – Training manifests (modeling/runtime) |
| `sync/ifns/training_manifest_H1_v1_0.json` | Training manifest JSON (D1/H1 demo or versioned manifests). | Later – Training manifests (modeling/runtime) |

### 5.2 YAML runtime templates

Under `runtime_templates/`, there are YAML run templates such as:

- `runtime_templates/RUN_IFNS_FEATUREVIEW_D1_ARCX_IWM_V1_1.yaml`
- `runtime_templates/RUN_IFNS_FEATUREVIEW_D1_ARCX_SPY_V1_1.yaml`
- `runtime_templates/RUN_IFNS_FEATUREVIEW_D1_XNAS_MSFT_V1_1.yaml`
- `runtime_templates/RUN_IFNS_FEATUREVIEW_D1_XNYS_AAPL_V1_1.yaml`
- `runtime_templates/RUN_IFNS_FEATUREVIEW_H1_ARCX_IWM_V1_1.yaml`
- `runtime_templates/RUN_IFNS_FEATUREVIEW_H1_ARCX_SPY_V1_1.yaml`
- `runtime_templates/RUN_IFNS_FEATUREVIEW_H1_XNAS_AAPL_V1_1.yaml`
- `runtime_templates/RUN_IFNS_FEATUREVIEW_H1_XNAS_MSFT_V1_1.yaml`
- `schemas/databases.yml`

These correspond to **runtime jobs** for specific feature views (e.g. `D1 XNAS MSFT`). They should be wired to:

- The **Runtime Templates & Calendars** spec in IFNS – UI Master (V2).

- The relevant **Step 09 – Execution Intelligence (EI)** and **Step 12 – DRA** hubs.


## 6. How to use this repo with the Phase 0–5 Notion kit

For the Notion/Git agent, the process should be:

1. **Start from Notion (SoT).**

   - Ensure the DBs described in Phases 3–4 exist (`QCWeekly`, `CalendarGaps2025`, `Feature Catalog`, etc.).

2. **Link DBs to Git paths using this file + `ifns_v2_db_map.json`.**

   - For each DB, confirm its CSV/JSON mirror in `sync/ifns/`.

   - When a DB changes (schema or rows), export a fresh CSV/JSON into the matching path.

3. **Never edit the Git CSV/JSON as primary.**

   - All conceptual changes must happen in Notion first.

   - Git is kept in sync based on explicit exports.

4. **Telemetry & runtime artifacts:**

   - Use `qc_weekly_schema_v1.json`, `calendar_gaps_2025.json`, and `clip_events_schema_v1.json` as schema references for Phase 3 DBs.

   - Use `runtime_templates/*.yaml` as implementation for the runtime templates defined in Step 09 / Step 12 hubs.


## 7. Handover summary for Git-focused agents

If you are responsible primarily for Git and CI/CD:

1. Treat this file as your **index** of IFNS-relevant repo assets.

2. Always cross-check with the Phase 0–5 `.md` files to know:

   - Which Notion DB or spec a given CSV/JSON/YAML mirrors.

   - Which Step hubs and V2 spec cards conceptually own that data.

3. When adding new CSV/JSON/YAML for IFNS:

   - First ensure there is a corresponding Notion DB or spec page.

   - Then add entries to `IFNS_Notion_DB_Buildout_V2/config/ifns_v2_db_map.json` as needed.

4. Use CI (lint, assertions, etc.) to verify consistency between Notion exports and these Git files over time.
