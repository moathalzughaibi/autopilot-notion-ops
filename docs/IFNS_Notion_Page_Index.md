# IFNS – Notion Page Index

> Purpose  
> Single place to see all key Notion pages (titles, IDs, parents, URLs, and roles),
> so scripts can use the correct IDs and new team members understand the structure.

| Serial | Page Title                                          | Page ID                                | Parent          | URL | Scope / What this page is                                      | Notes |
|--------|-----------------------------------------------------|----------------------------------------|-----------------|-----|----------------------------------------------------------------|-------|
| 1      | Autopilot Hub (root)                                | 29ab22c770d980918736f0dcad3bac83       | Workspace root  |     | Main workspace root for Autopilot & IFNS projects.             | Used as `NOTION_ROOT_PAGE_ID` in env. |
| 2      | IFNS  UI Master                                    | 2adb22c7-70d9-807f-96ee-c817ecb37402   | Autopilot Hub   |     | Master UI / UX spec container for all IFNS steps.              | Script `ifns_sync_all_steps.py` looks under this page. |
| 3      | Step 01  Preface Integration                       | (fill from Notion)                     | IFNS  UI Master |    | High-level positioning of IFNS and integration story.          | Has children: 01/02/03 subpages. |
| 4      | Step 02  Executive Summary                         | (fill from Notion)                     | IFNS  UI Master |    | Executive-level view of IFNS goals and outcomes.               | Has children: 01/02/03 subpages. |
| 5      | Step 03  VisionaryTechnical Overview              | (fill from Notion)                     | IFNS  UI Master |    | SxE bridge: how cores and awareness layers show up as UX.      | Children created by sync: 01/02/03. |
| 6      | Step 04  Preface Timeline                          | (fill from Notion)                     | IFNS  UI Master |    | Timeline-style narrative of IFNS evolution and milestones.     | Children created by sync: 01/02/03. |
| 7      | Step 05  Section 1.0  Introduction                | (fill from Notion)                     | IFNS – UI Master |    | First detailed introduction section to the IFNS system.        | Children created by sync: 01/02/03. |
| 8      | Step 06  Section 2.0  System Architecture         | (fill from Notion)                     | IFNS  UI Master |    | Overall architecture: cores, layers, flows, and contracts.     | Children created by sync: 01/02/03. |
| 9      | Step 07  Section 3.0  Data Intelligence Layer     | (fill from Notion)                     | IFNS  UI Master |    | DIL: data ingestion, quality, features, and pipelines.         | Children created by sync: 01/02/03. |
| 10     | Step 08  Section 4.0  Modeling Intelligence       | (fill from Notion)                     | IFNS  UI Master |    | MI: modeling stack, training, evaluation, and catalog.         | Children created by sync: 01/02/03. |
| 11     | Step 09  Section 5.0  Execution Intelligence      | (fill from Notion)                     | IFNS  UI Master |    | EI: routing, execution, slippage, and trading behavior.        | Children created by sync: 01/02/03. |
| 12     | Step 10  Section 6.0  Market Structural Awareness | (fill from Notion)                     | IFNS  UI Master |    | MSA: regime, volatility, structure, and context awareness.     | Children created by sync: 01/02/03. |
| 13     | Step 11  Section 7.0  Model & Signal Integration  | (fill from Notion)                     | IFNS  UI Master |    | MSI: how models and signals are routed, combined, and gated.   | Children created by sync: 01/02/03. |
| 14     | Step 12  Section 8.0  Decision & Risk Architecture| (fill from Notion)                    | IFNS  UI Master |    | DRA: governance, limits, overrides, and risk decisions.        | Children created by sync: 01/02/03. |
| 15     | Step 13  Section 9.0  Self-Evaluation & Learning  | (fill from Notion)                     | IFNS  UI Master |    | SEL: post-trade reviews, self-scoring, and feedback loops.     | Children created by sync: 01/02/03. |
| 16     | Step 14  (to be created in Notion)                 | (TBD)                                  | IFNS  UI Master |    | Advanced Awareness layer (TAC / MCEE / GMCL / QDA concepts).   | Create page in Notion, then rerun sync. |

> How to fill IDs and URLs  
> - Open the page in Notion, copy the URL, and (optionally) extract the page ID from it.  
> - Paste the ID into the **Page ID** column and the URL into **URL**.  
> - Keep this file updated when new pages (e.g., Core ML root, Admin Console, Awareness Mirror) are added.
| 17 | UI Master Summary      | 2afb22c7-70d9-8118-a932-f5372d894674 | IFNS – UI Master |  | High-level summary of IFNS – UI Master coverage, Core ML linkage, and roadmap. | Synced from `docs/ifns/IFNS_UI_Master_Summary_v2.md` via `ifns_sync_master_phase2.py`. |
| 18 | Steps Index            | 2afb22c7-70d9-8157-89be-d5b9598a9604 | IFNS  UI Master |  | Index of all 14 IFNS UI Steps with spec file mapping and Core ML stage links. | Synced from `docs/ifns/IFNS_UI_Steps_Index_v2.md`. |
| 19 | Drafts & Working Notes | 2afb22c7-70d9-81e5-805f-e96d174eebe6 | IFNS  UI Master |  | Log of drafts, phases, and working notes for IFNS UI work. | Synced from `docs/ifns/IFNS_UI_Drafts_and_Working_Notes_v2.md`. |
| 20 | Core ML Build Stages                     | TBD_COREML_HUB_ID  | IFNS  UI Master |  | Hub for Stage 0007 Core ML build specs (pipeline from document overview to live trading). | Child pages synced from `docs/ifns/stages/Stage_*.md` via `ifns_sync_coreml_stages.py`. |
| 21 | Stage 00  Document Overview             | TBD_STAGE_00_ID    | Core ML Build Stages |  | Overall document overview and framing for the Core ML pipeline. | Sections 01/02/03 from `Stage_00_Document_Overview.md`. |
| 22 | Stage 01  Foundations & Architecture    | TBD_STAGE_01_ID    | Core ML Build Stages |  | Environment, infra, and architecture foundations for IFNS ML. | Sections 01/02/03 from `Stage_01_Foundations_and_Architecture.md`. |
| 23 | Stage 02  Data & Feature Pipeline       | TBD_STAGE_02_ID    | Core ML Build Stages |  | Data sourcing, feature pipeline, and transformations. | Sections 01/02/03 from `Stage_02_Data_and_Feature_Pipeline.md`. |
| 24 | Stage 03 – Modeling & Training           | TBD_STAGE_03_ID    | Core ML Build Stages |  | Modeling stack, training flows, and experiment structure. | Sections 01/02/03 from `Stage_03_Modeling_and_Training.md`. |
| 25 | Stage 04  Backtesting & Evaluation      | TBD_STAGE_04_ID    | Core ML Build Stages |  | Backtesting, evaluation, and performance measurement layer. | Sections 01/02/03 from `Stage_04_Backtesting_and_Evaluation.md`. |
| 26 | Stage 05  Risk, Execution & SxE Link    | TBD_STAGE_05_ID    | Core ML Build Stages |  | Risk controls, execution linkage, and System-to-Experience bridge. | Sections 01/02/03 from `Stage_05_Risk_Execution_and_SxE_Link.md`. |
| 27 | Stage 06  Paper Trading                 | TBD_STAGE_06_ID    | Core ML Build Stages |  | Paper-trading harness and dry-run operations. | Sections 01/02/03 from `Stage_06_Paper_Trading.md`. |
| 28 | Stage 07  Live Trading & Operations     | TBD_STAGE_07_ID    | Core ML Build Stages |  | Live trading rollout, monitoring, and operational procedures. | Sections 01/02/03 from `Stage_07_Live_Trading_and_Operations.md`. |
| 29 | Tables & Telemetry (DB Hub) | TBD_TABLES_HUB_ID | IFNS – UI Master |  | Hub for all CSV-backed databases and telemetry specs (Phase 4). | Child pages synced from `docs/ifns/tables/*.md` via `ifns_sync_tables_phase4.py`. |
| 30 | <Phase 4 Page 1 Title>      | TBD_P4_PAGE1_ID   | Tables & Telemetry (DB Hub) |  | Phase 4 spec page (see matching .md in `docs/ifns/tables`). | Auto-synced. |
| 31 | <Phase 4 Page 2 Title>      | TBD_P4_PAGE2_ID   | Tables & Telemetry (DB Hub) |  | Phase 4 spec page (see matching .md in `docs/ifns/tables`). | Auto-synced. |
| 32 | <Phase 4 Page 3 Title>      | TBD_P4_PAGE3_ID   | Tables & Telemetry (DB Hub) |  | Phase 4 spec page (see matching .md in `docs/ifns/tables`). | Auto-synced. |

| 33 | Tables & Telemetry (DB Hub) | 2afb22c7-70d9-81bf-84ee-d2edab2733e6 | IFNS  UI Master |  | Hub for CSV-backed databases and telemetry specs (Phase 4). | Child pages synced from `docs/ifns/tables` via `ifns_sync_tables_phase4.py`. |
| 34 | IFNS Core Registry v1 Seeds | 2afb22c7-70d9-8185-a13c-d470249a1aa1 | Tables & Telemetry (DB Hub) |  | Phase 4 spec page under Tables & Telemetry (DB Hub). | Auto-synced from matching file in `docs/ifns/tables`. |

| 35 | IFNS Core Tables Phase4 v0 1 | 2afb22c7-70d9-813f-a45b-cba65bbbeb7d | Tables & Telemetry (DB Hub) |  | Phase 4 spec page under Tables & Telemetry (DB Hub). | Auto-synced from matching file in `docs/ifns/tables`. |
| 36 | IFNS Phase4 Mapping v0 1 | 2afb22c7-70d9-817f-979e-efb0ed706318 | Tables & Telemetry (DB Hub) |  | Phase 4 spec page under Tables & Telemetry (DB Hub). | Auto-synced from matching file in `docs/ifns/tables`. |

| 37 | Stock Indicator System – Master Index | 2afb22c7-70d9-8195-b044-db33b7ca5d4a | Core ML Build Stages |  | Master index for the Stock Indicator System (Phases 17) under Core ML Build Stages. | Content synced from `docs/ifns/indicators/Indicators_Master_Index_*.md` via `ifns_sync_indicators_docs.py`. |
| 38 | Phase 1  Indicator Taxonomy & Governance | 2afb22c7-70d9-81e4-9ef3-f9cf13ff7091 | Stock Indicator System – Master Index |  | Indicator phase spec page (see matching .md in `docs/ifns/indicators`). | Auto-synced. |
| 39 | Phase 2  Indicator Universe Draft | 2afb22c7-70d9-81ba-85da-e085cb718f0c | Stock Indicator System – Master Index |  | Indicator phase spec page (see matching .md in `docs/ifns/indicators`). | Auto-synced. |
| 40 | Phase 3  L1 Indicator Catalog | 2afb22c7-70d9-8129-ae6d-df231734a849 | Stock Indicator System – Master Index |  | Indicator phase spec page (see matching .md in `docs/ifns/indicators`). | Auto-synced. |
| 41 | Phase 4  L2/L3 Framework Catalog | 2afb22c7-70d9-8132-a06a-eefd4789433d | Stock Indicator System – Master Index |  | Indicator phase spec page (see matching .md in `docs/ifns/indicators`). | Auto-synced. |
| 42 | Phase 5  Feature Output & Digitization Schema | 2afb22c7-70d9-815e-8c59-ce15a4474094 | Stock Indicator System – Master Index |  | Indicator phase spec page (see matching .md in `docs/ifns/indicators`). | Auto-synced. |
| 43 | Phase 6  Implementation & Runtime Templates | 2afb22c7-70d9-816c-9e3d-e7cad6a308a9 | Stock Indicator System – Master Index |  | Indicator phase spec page (see matching .md in `docs/ifns/indicators`). | Auto-synced. |
| 44 | Phase 7  ML Integration & Operationalization | 2afb22c7-70d9-810f-a328-df8b443e2899 | Stock Indicator System – Master Index |  | Indicator phase spec page (see matching .md in `docs/ifns/indicators`). | Auto-synced. |

## Notion DB build-out snapshot (2025-11-18T13:02:03.307775Z)
- **FeatureSchemaV1**  `sync/ifns/indicator_feature_schema_v1_with_family.csv` (pk: `feature_name`)  DB: `6484618c-ca0b-4a31-9544-4ecf11d0df87`
- **FeatureSchemaH1**  `sync/ifns/indicator_feature_schema_h1_v1_with_family.csv` (pk: `feature_name`)  DB: `dfe40c25-9e24-4928-8fa1-4bed6114ce9f`
- **PolicyMatrix**  `sync/ifns/feature_policy_matrix.csv` (pk: ``)  DB: `9e48b82d-4d6a-4d2b-aa17-a88080bc35ac`
- **FamilyMap**  `sync/ifns/feature_family_map.csv` (pk: `feature_name`)  DB: `e4562cd0-3d8a-4986-b72f-a9cf94b68e7e`
- **UniverseP2**  `sync/ifns/indicators_universe_catalog_phase2.csv` (pk: `symbol`)  DB: `de828cc4-0b81-49fa-aa69-d328d6930779`
- **CatalogL1**  `sync/ifns/indicators_catalog_L1_phase3.csv` (pk: `indicator_id`)  DB: `066b5cc5-6f8f-4f1b-aa10-59a351e608fa`
- **CatalogL2L3**  `sync/ifns/indicators_catalog_L2L3_phase4.csv` (pk: `composite_id`)  DB: `ef3175fe-046d-47b8-8944-607d5bcf5d21`
- **QCWeekly**  `sync/ifns/qc_weekly_schema_v1.json` (pk: `entry_id`)  DB: `cee29b9e-4071-45a5-bb9d-9a4f7b543ceb`
- **CalendarGaps2025**  `sync/ifns/calendar_gaps_2025.json` (pk: `event_id`)  DB: ``

## Notion DB build-out snapshot (2025-11-18T13:05:06.753632Z)

## Notion DB build-out snapshot (2025-11-18T13:09:23.512723Z)

## Notion DB build-out snapshot (2025-11-18T13:17:09.617062Z)

## Notion DB build-out snapshot (2025-11-18T13:41:30.288540Z)
