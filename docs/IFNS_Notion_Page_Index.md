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
