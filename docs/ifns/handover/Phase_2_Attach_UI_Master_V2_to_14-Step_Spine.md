# Phase 2 – Attach IFNS – UI Master (V2) to the 14-Step Spine

This handover binds the **IFNS – UI Master (V2)** surfaces to the 14-step master spine defined in Phase 1.
It does **not** delete or overwrite any pages. Instead, it tells a Notion/Git agent how to:

- Position each V2 asset under one or more of the 14 step hubs, and

- Rename or relabel pages where useful so their role is obvious.

## 1. V2 asset inventory (from export)

The table below lists every page under `IFNS – UI Master (V2)` and the 14-step(s) it most naturally attaches to.

| # | V2 Asset Title | Export Path | Related Step(s) |
|---|----------------|-------------|-----------------|
| 1 | IFNS – UI Master (V2) | Private & Shared/Autopilot Hub/IFNS – UI Master (V2) 2afb22c770d981b79316e9105265a4b3.md | 01, 02, 03, 04, 05, 06, 07, 08, 09, 10, 11, 12, 13, 14 |
| 2 | Indicator System (Phases 1–7) | Private & Shared/Autopilot Hub/IFNS – UI Master (V2)/Indicator System (Phases 1–7) 2afb22c770d981a5822ce9c4154a5c62.md | 07, 08, 10 |
| 3 | Core ML Build (Stages 0–7) | Private & Shared/Autopilot Hub/IFNS – UI Master (V2)/Core ML Build (Stages 0–7) 2afb22c770d98164b89ae51a55e2727e.md | 03, 06, 08 |
| 4 | Manifests & Policy | Private & Shared/Autopilot Hub/IFNS – UI Master (V2)/Manifests & Policy 2afb22c770d981b5ae1accb55e565eda.md | 05, 07, 08, 10, 12 |
| 5 | Telemetry & QC | Private & Shared/Autopilot Hub/IFNS – UI Master (V2)/Telemetry & QC 2afb22c770d9818882dcc1548e951932.md | 05, 07, 08, 09, 12, 13 |
| 6 | Runtime Templates & Calendars | Private & Shared/Autopilot Hub/IFNS – UI Master (V2)/Runtime Templates & Calendars 2afb22c770d9811b973ec99095e81a7e.md | 04, 09, 12 |
| 7 | Change Log (V1 → V2 deltas) | Private & Shared/Autopilot Hub/IFNS – UI Master (V2)/Change Log (V1 → V2 deltas) 2afb22c770d98107b83cd53601a66115.md |  |
| 8 | Attachments | Private & Shared/Autopilot Hub/IFNS – UI Master (V2)/Attachments 2afb22c770d9817aa715e4c43c250e07.md |  |
| 9 | Indicator Feature Schema v1 (with family) | Private & Shared/Autopilot Hub/IFNS – UI Master (V2)/Manifests & Policy/Indicator Feature Schema v1 (with family) 2afb22c770d981a5b1c4d980b454ef59.md | 07, 08, 10 |
| 10 | Indicator Feature Schema H1 v1 (with family) | Private & Shared/Autopilot Hub/IFNS – UI Master (V2)/Manifests & Policy/Indicator Feature Schema H1 v1 (with family) 2afb22c770d9815ca196d53551ce87a8.md | 07, 08, 10 |
| 11 | Feature Policy Matrix | Private & Shared/Autopilot Hub/IFNS – UI Master (V2)/Manifests & Policy/Feature Policy Matrix 2afb22c770d981debfc7c75e43c15859.md | 05, 07, 08, 10, 12 |
| 12 | Feature Family Map | Private & Shared/Autopilot Hub/IFNS – UI Master (V2)/Manifests & Policy/Feature Family Map 2afb22c770d9810fa271fa0f937a9327.md | 07, 08, 10 |
| 13 | Indicators – Universe Catalog (Phase 2 Draft) | Private & Shared/Autopilot Hub/IFNS – UI Master (V2)/Manifests & Policy/Indicators – Universe Catalog (Phase 2 Draft) 2afb22c770d981f9879ee41191de19b1.md | 07, 08, 10 |
| 14 | Indicators – L1 Catalog (Phase 3) | Private & Shared/Autopilot Hub/IFNS – UI Master (V2)/Manifests & Policy/Indicators – L1 Catalog (Phase 3) 2afb22c770d9816b992aced0b0811516.md | 07, 08, 10 |
| 15 | Indicators – L2 L3 Framework Catalog (Phase 4) | Private & Shared/Autopilot Hub/IFNS – UI Master (V2)/Manifests & Policy/Indicators – L2 L3 Framework Catalog (Phase 4) 2afb22c770d98140b1d3dc822fe19525.md | 07, 08, 10 |
| 16 | QC Weekly Schema v1 | Private & Shared/Autopilot Hub/IFNS – UI Master (V2)/Telemetry & QC/QC Weekly Schema v1 2afb22c770d981c79fb7e76a3ae1511e.md | 07, 08, 09, 10, 12, 13 |
| 17 | QC Weekly Example v1 | Private & Shared/Autopilot Hub/IFNS – UI Master (V2)/Telemetry & QC/QC Weekly Example v1 2afb22c770d9818c99dbc237eb46fdc0.md | 07, 08, 09, 10, 12, 13 |
| 18 | QC Weekly Telemetry V1 (Doc) | Private & Shared/Autopilot Hub/IFNS – UI Master (V2)/Telemetry & QC/QC Weekly Telemetry V1 (Doc) 2afb22c770d981d7b5e2e07d40a63326.md | 07, 08, 09, 10, 12, 13 |
| 19 | QC Weekly ETL Skeleton | Private & Shared/Autopilot Hub/IFNS – UI Master (V2)/Telemetry & QC/QC Weekly ETL Skeleton 2afb22c770d98194bcc0e5b10a6288d4.md | 07, 08, 09, 10, 12, 13 |
| 20 | QC Weekly ETL Clip Integration | Private & Shared/Autopilot Hub/IFNS – UI Master (V2)/Telemetry & QC/QC Weekly ETL Clip Integration 2afb22c770d98123954dc16073a49902.md | 07, 08, 09, 10, 12, 13 |
| 21 | QC Weekly ETL Script | Private & Shared/Autopilot Hub/IFNS – UI Master (V2)/Telemetry & QC/QC Weekly ETL Script 2afb22c770d9815ca652e513fa0b348a.md | 07, 08, 09, 10, 12, 13 |
| 22 | IO Utils (Telemetry Manifest I O helpers) | Private & Shared/Autopilot Hub/IFNS – UI Master (V2)/Telemetry & QC/IO Utils (Telemetry Manifest I O helpers) 2afb22c770d98191b530dc3c70c67420.md | 05, 07, 08, 09, 10, 12, 13 |
| 23 | Manifest Diff Tool | Private & Shared/Autopilot Hub/IFNS – UI Master (V2)/Telemetry & QC/Manifest Diff Tool 2afb22c770d98182a3cfc3ac35dd9d10.md | 07, 08, 09, 10, 12, 13 |
| 24 | CI IFNS Guard Workflow | Private & Shared/Autopilot Hub/IFNS – UI Master (V2)/Telemetry & QC/CI IFNS Guard Workflow 2afb22c770d98109ba8bfbf5fbede124.md | 05, 07, 08, 09, 10, 12, 13 |
| 25 | CI Manifest Guard (Python) | Private & Shared/Autopilot Hub/IFNS – UI Master (V2)/Telemetry & QC/CI Manifest Guard (Python) 2afb22c770d9812496aafd166f4e6ced.md | 05, 07, 08, 10, 12 |
| 26 | Runtime – Calendar Gaps 2025 | Private & Shared/Autopilot Hub/IFNS – UI Master (V2)/Runtime Templates & Calendars/Runtime – Calendar Gaps 2025 2afb22c770d981bc8461e491fd37d89a.md | 04, 07, 08, 09, 10, 12 |
| 27 | Runtime Templates (YAML) | Private & Shared/Autopilot Hub/IFNS – UI Master (V2)/Runtime Templates & Calendars/Runtime Templates (YAML) 2afb22c770d98194bf46d590918f802f.md | 04, 07, 08, 09, 10, 12 |

## 2. Global attachment rules

Use these rules as the **default policy** when wiring V2 pages into the 14-step structure in Notion:

1. **Never delete** any V2 page. Instead:

   - Relocate it under the most appropriate **Step hub**, and

   - If necessary, add a short note at the top: `Status: attached to Step XX – …`.

2. For assets that span multiple steps (e.g. Telemetry & QC, Runtime Templates & Calendars):

   - Keep the **V2 page in its current folder** as a canonical spec,

   - Then add inbound links from each relevant Step hub under a section like `V2 surfaces linked to this step`.

3. For CSV/DB-backed assets (Feature Schema, Policy Matrix, Family Map, Catalog drafts):

   - Treat the V2 page as the **DB spec card**,

   - Attach it primarily to the **Data Intelligence (Step 07)** and **Modeling (Step 08)** hubs,

   - Optionally cross-link from **Risk (Step 12)** when policy/guardrails are involved.

## 3. Per-asset placement & naming suggestions

This section gives **concrete instructions** for the Notion agent: where to attach each V2 asset and how to label it from the perspective of the 14-step spine.

### IFNS – UI Master (V2)

- **V2 page:** `Private & Shared/Autopilot Hub/IFNS – UI Master (V2) 2afb22c770d981b79316e9105265a4b3.md`
- **URL:** https://www.notion.so/2afb22c770d981b79316e9105265a4b3
- **Primary step attachment:** Step 01 – Preface Integration
- **Secondary cross-links:** Step 02 – Executive Summary, Step 03 – Visionary–Technical Overview, Step 04 – Preface Timeline, Step 05 – Section 1.0 – Introduction, Step 06 – Section 2.0 – System Architecture, Step 07 – Section 3.0 – Data Intelligence Layer (DIL), Step 08 – Section 4.0 – Modeling Intelligence (MI), Step 09 – Section 5.0 – Execution Intelligence (EI), Step 10 – Section 6.0 – Market Structural Awareness (MSA), Step 11 – Section 7.0 – Model & Signal Integration (MSI), Step 12 – Section 8.0 – Decision & Risk Architecture (DRA), Step 13 – Section 9.0 – Self-Evaluation & Learning (SEL), Step 14 – Sections 11.0–14.0 – Advanced Awareness

**Instructions for Notion agent:**
1. Keep this as the **root index** for all V2 surfaces (Indicators, Core ML, Manifests, Telemetry, Runtime).
2. Under **Step 03 – Visionary–Technical Overview** and **Step 06 – System Architecture**, link this page as `UI Master V2 – Surfaces Index`.
3. Do not move this page under a single step; it should remain visible from the Autopilot Hub root as the technical surfaces entry point.

### Indicator System (Phases 1–7)

- **V2 page:** `Private & Shared/Autopilot Hub/IFNS – UI Master (V2)/Indicator System (Phases 1–7) 2afb22c770d981a5822ce9c4154a5c62.md`
- **URL:** https://www.notion.so/2afb22c770d981a5822ce9c4154a5c62
- **Primary step attachment:** Step 07 – Section 3.0 – Data Intelligence Layer (DIL)
- **Secondary cross-links:** Step 08 – Section 4.0 – Modeling Intelligence (MI), Step 10 – Section 6.0 – Market Structural Awareness (MSA)

**Instructions for Notion agent:**
1. Under the **Step 07 – Data Intelligence Layer (DIL)** hub, add a section `V2 surfaces → Indicator System` and link this page.
2. Under **Step 08 – Modeling Intelligence (MI)** and **Step 10 – Market Structural Awareness (MSA)** hubs, add cross-links in a `Indicators & Regimes` subsection.
3. Do **not** duplicate the indicator definitions here; instead, this page remains the spec index for indicator bundles and phases.

### Core ML Build (Stages 0–7)

- **V2 page:** `Private & Shared/Autopilot Hub/IFNS – UI Master (V2)/Core ML Build (Stages 0–7) 2afb22c770d98164b89ae51a55e2727e.md`
- **URL:** https://www.notion.so/2afb22c770d98164b89ae51a55e2727e
- **Primary step attachment:** Step 03 – Visionary–Technical Overview
- **Secondary cross-links:** Step 06 – Section 2.0 – System Architecture, Step 08 – Section 4.0 – Modeling Intelligence (MI)

**Instructions for Notion agent:**
1. Under the **Step 03 – Visionary–Technical Overview** hub, add this page as the canonical `Core ML lifecycle spec` link.
2. Under **Step 06 – System Architecture** hub, place a link in the `Lifecycle diagrams & flows` section.
3. Under **Step 08 – Modeling Intelligence (MI)**, add a `Model training lifecycle` link back to this page.

### Manifests & Policy

- **V2 page:** `Private & Shared/Autopilot Hub/IFNS – UI Master (V2)/Manifests & Policy 2afb22c770d981b5ae1accb55e565eda.md`
- **URL:** https://www.notion.so/2afb22c770d981b5ae1accb55e565eda
- **Primary step attachment:** Step 05 – Section 1.0 – Introduction
- **Secondary cross-links:** Step 07 – Section 3.0 – Data Intelligence Layer (DIL), Step 08 – Section 4.0 – Modeling Intelligence (MI), Step 10 – Section 6.0 – Market Structural Awareness (MSA), Step 12 – Section 8.0 – Decision & Risk Architecture (DRA)

**Instructions for Notion agent:**
1. Under **Step 05 – Operational Genesis Framework**, link this page under a `Manifests & Policy surfaces` section.
2. Under **Step 07 – DIL**, **Step 08 – MI**, and **Step 12 – Decision & Risk Architecture (DRA)**, add cross-links for policy-bound features and risk constraints.
3. Make this page the **entry point** for Feature Schema, Policy Matrix, Family Map, and Catalog spec cards (see below).

### Telemetry & QC

- **V2 page:** `Private & Shared/Autopilot Hub/IFNS – UI Master (V2)/Telemetry & QC 2afb22c770d9818882dcc1548e951932.md`
- **URL:** https://www.notion.so/2afb22c770d9818882dcc1548e951932
- **Primary step attachment:** Step 05 – Section 1.0 – Introduction
- **Secondary cross-links:** Step 07 – Section 3.0 – Data Intelligence Layer (DIL), Step 08 – Section 4.0 – Modeling Intelligence (MI), Step 09 – Section 5.0 – Execution Intelligence (EI), Step 12 – Section 8.0 – Decision & Risk Architecture (DRA), Step 13 – Section 9.0 – Self-Evaluation & Learning (SEL)

**Instructions for Notion agent:**
1. Under **Step 07 – DIL**, **Step 08 – MI**, and **Step 09 – EI**, add a `Telemetry & QC surfaces` block linking to this page.
2. Under **Step 12 – DRA** and **Step 13 – SEL**, link this page as the canonical spec for monitoring and learning KPIs.
3. Future: its child pages (QC Weekly Schema, Examples, ETL, CI Guard) will be wired in Phase 3; for now, treat this as their parent index.

### Runtime Templates & Calendars

- **V2 page:** `Private & Shared/Autopilot Hub/IFNS – UI Master (V2)/Runtime Templates & Calendars 2afb22c770d9811b973ec99095e81a7e.md`
- **URL:** https://www.notion.so/2afb22c770d9811b973ec99095e81a7e
- **Primary step attachment:** Step 04 – Preface Timeline
- **Secondary cross-links:** Step 09 – Section 5.0 – Execution Intelligence (EI), Step 12 – Section 8.0 – Decision & Risk Architecture (DRA)

**Instructions for Notion agent:**
1. Under **Step 04 – Preface Timeline / Evolutionary Arc** hub, link this page in a `Runtime activation & calendars` section.
2. Under **Step 09 – Execution Intelligence (EI)** hub, add a `Runtime scheduling & gaps` subsection pointing here.
3. Under **Step 12 – DRA**, cross-link where runtime actions tie to risk or guardrails.

### Change Log (V1 → V2 deltas)

- **V2 page:** `Private & Shared/Autopilot Hub/IFNS – UI Master (V2)/Change Log (V1 → V2 deltas) 2afb22c770d98107b83cd53601a66115.md`
- **URL:** https://www.notion.so/2afb22c770d98107b83cd53601a66115
- **Primary step attachment:** _None detected automatically — keep under V2 root but cross-link manually as needed._

### Attachments

- **V2 page:** `Private & Shared/Autopilot Hub/IFNS – UI Master (V2)/Attachments 2afb22c770d9817aa715e4c43c250e07.md`
- **URL:** https://www.notion.so/2afb22c770d9817aa715e4c43c250e07
- **Primary step attachment:** _None detected automatically — keep under V2 root but cross-link manually as needed._

### Indicator Feature Schema v1 (with family)

- **V2 page:** `Private & Shared/Autopilot Hub/IFNS – UI Master (V2)/Manifests & Policy/Indicator Feature Schema v1 (with family) 2afb22c770d981a5b1c4d980b454ef59.md`
- **URL:** https://www.notion.so/2afb22c770d981a5b1c4d980b454ef59
- **Primary step attachment:** Step 07 – Section 3.0 – Data Intelligence Layer (DIL)
- **Secondary cross-links:** Step 08 – Section 4.0 – Modeling Intelligence (MI), Step 10 – Section 6.0 – Market Structural Awareness (MSA)

**Instructions for Notion agent:**
1. Keep this page under the `Manifests & Policy` folder as a **schema/spec card**.
2. Under **Step 07 – DIL** and **Step 08 – MI** hubs, reference this card from a `Data & Feature Schemas` table.
3. If the asset encodes constraints or policies (e.g. Policy Matrix, Family Map), also link from **Step 12 – DRA** under `Risk & Policy Schemas`.

### Indicator Feature Schema H1 v1 (with family)

- **V2 page:** `Private & Shared/Autopilot Hub/IFNS – UI Master (V2)/Manifests & Policy/Indicator Feature Schema H1 v1 (with family) 2afb22c770d9815ca196d53551ce87a8.md`
- **URL:** https://www.notion.so/2afb22c770d9815ca196d53551ce87a8
- **Primary step attachment:** Step 07 – Section 3.0 – Data Intelligence Layer (DIL)
- **Secondary cross-links:** Step 08 – Section 4.0 – Modeling Intelligence (MI), Step 10 – Section 6.0 – Market Structural Awareness (MSA)

**Instructions for Notion agent:**
1. Attach this page under the **primary step hub** above, in a `V2 surfaces` or `Specs & Schemas` subsection.
2. Add cross-links from the **secondary step hubs** so that readers can discover it from all relevant stages.
3. Do not change the body text; only add a short status line if necessary (e.g., `Attached to Step XX spine on YYYY-MM-DD`).

### Feature Policy Matrix

- **V2 page:** `Private & Shared/Autopilot Hub/IFNS – UI Master (V2)/Manifests & Policy/Feature Policy Matrix 2afb22c770d981debfc7c75e43c15859.md`
- **URL:** https://www.notion.so/2afb22c770d981debfc7c75e43c15859
- **Primary step attachment:** Step 05 – Section 1.0 – Introduction
- **Secondary cross-links:** Step 07 – Section 3.0 – Data Intelligence Layer (DIL), Step 08 – Section 4.0 – Modeling Intelligence (MI), Step 10 – Section 6.0 – Market Structural Awareness (MSA), Step 12 – Section 8.0 – Decision & Risk Architecture (DRA)

**Instructions for Notion agent:**
1. Keep this page under the `Manifests & Policy` folder as a **schema/spec card**.
2. Under **Step 07 – DIL** and **Step 08 – MI** hubs, reference this card from a `Data & Feature Schemas` table.
3. If the asset encodes constraints or policies (e.g. Policy Matrix, Family Map), also link from **Step 12 – DRA** under `Risk & Policy Schemas`.

### Feature Family Map

- **V2 page:** `Private & Shared/Autopilot Hub/IFNS – UI Master (V2)/Manifests & Policy/Feature Family Map 2afb22c770d9810fa271fa0f937a9327.md`
- **URL:** https://www.notion.so/2afb22c770d9810fa271fa0f937a9327
- **Primary step attachment:** Step 07 – Section 3.0 – Data Intelligence Layer (DIL)
- **Secondary cross-links:** Step 08 – Section 4.0 – Modeling Intelligence (MI), Step 10 – Section 6.0 – Market Structural Awareness (MSA)

**Instructions for Notion agent:**
1. Keep this page under the `Manifests & Policy` folder as a **schema/spec card**.
2. Under **Step 07 – DIL** and **Step 08 – MI** hubs, reference this card from a `Data & Feature Schemas` table.
3. If the asset encodes constraints or policies (e.g. Policy Matrix, Family Map), also link from **Step 12 – DRA** under `Risk & Policy Schemas`.

### Indicators – Universe Catalog (Phase 2 Draft)

- **V2 page:** `Private & Shared/Autopilot Hub/IFNS – UI Master (V2)/Manifests & Policy/Indicators – Universe Catalog (Phase 2 Draft) 2afb22c770d981f9879ee41191de19b1.md`
- **URL:** https://www.notion.so/2afb22c770d981f9879ee41191de19b1
- **Primary step attachment:** Step 07 – Section 3.0 – Data Intelligence Layer (DIL)
- **Secondary cross-links:** Step 08 – Section 4.0 – Modeling Intelligence (MI), Step 10 – Section 6.0 – Market Structural Awareness (MSA)

**Instructions for Notion agent:**
1. Keep this page under the `Manifests & Policy` folder as a **schema/spec card**.
2. Under **Step 07 – DIL** and **Step 08 – MI** hubs, reference this card from a `Data & Feature Schemas` table.
3. If the asset encodes constraints or policies (e.g. Policy Matrix, Family Map), also link from **Step 12 – DRA** under `Risk & Policy Schemas`.

### Indicators – L1 Catalog (Phase 3)

- **V2 page:** `Private & Shared/Autopilot Hub/IFNS – UI Master (V2)/Manifests & Policy/Indicators – L1 Catalog (Phase 3) 2afb22c770d9816b992aced0b0811516.md`
- **URL:** https://www.notion.so/2afb22c770d9816b992aced0b0811516
- **Primary step attachment:** Step 07 – Section 3.0 – Data Intelligence Layer (DIL)
- **Secondary cross-links:** Step 08 – Section 4.0 – Modeling Intelligence (MI), Step 10 – Section 6.0 – Market Structural Awareness (MSA)

**Instructions for Notion agent:**
1. Keep this page under the `Manifests & Policy` folder as a **schema/spec card**.
2. Under **Step 07 – DIL** and **Step 08 – MI** hubs, reference this card from a `Data & Feature Schemas` table.
3. If the asset encodes constraints or policies (e.g. Policy Matrix, Family Map), also link from **Step 12 – DRA** under `Risk & Policy Schemas`.

### Indicators – L2 L3 Framework Catalog (Phase 4)

- **V2 page:** `Private & Shared/Autopilot Hub/IFNS – UI Master (V2)/Manifests & Policy/Indicators – L2 L3 Framework Catalog (Phase 4) 2afb22c770d98140b1d3dc822fe19525.md`
- **URL:** https://www.notion.so/2afb22c770d98140b1d3dc822fe19525
- **Primary step attachment:** Step 07 – Section 3.0 – Data Intelligence Layer (DIL)
- **Secondary cross-links:** Step 08 – Section 4.0 – Modeling Intelligence (MI), Step 10 – Section 6.0 – Market Structural Awareness (MSA)

**Instructions for Notion agent:**
1. Keep this page under the `Manifests & Policy` folder as a **schema/spec card**.
2. Under **Step 07 – DIL** and **Step 08 – MI** hubs, reference this card from a `Data & Feature Schemas` table.
3. If the asset encodes constraints or policies (e.g. Policy Matrix, Family Map), also link from **Step 12 – DRA** under `Risk & Policy Schemas`.

### QC Weekly Schema v1

- **V2 page:** `Private & Shared/Autopilot Hub/IFNS – UI Master (V2)/Telemetry & QC/QC Weekly Schema v1 2afb22c770d981c79fb7e76a3ae1511e.md`
- **URL:** https://www.notion.so/2afb22c770d981c79fb7e76a3ae1511e
- **Primary step attachment:** Step 07 – Section 3.0 – Data Intelligence Layer (DIL)
- **Secondary cross-links:** Step 08 – Section 4.0 – Modeling Intelligence (MI), Step 09 – Section 5.0 – Execution Intelligence (EI), Step 10 – Section 6.0 – Market Structural Awareness (MSA), Step 12 – Section 8.0 – Decision & Risk Architecture (DRA), Step 13 – Section 9.0 – Self-Evaluation & Learning (SEL)

**Instructions for Notion agent:**
1. Keep this page under the `Manifests & Policy` folder as a **schema/spec card**.
2. Under **Step 07 – DIL** and **Step 08 – MI** hubs, reference this card from a `Data & Feature Schemas` table.
3. If the asset encodes constraints or policies (e.g. Policy Matrix, Family Map), also link from **Step 12 – DRA** under `Risk & Policy Schemas`.

### QC Weekly Example v1

- **V2 page:** `Private & Shared/Autopilot Hub/IFNS – UI Master (V2)/Telemetry & QC/QC Weekly Example v1 2afb22c770d9818c99dbc237eb46fdc0.md`
- **URL:** https://www.notion.so/2afb22c770d9818c99dbc237eb46fdc0
- **Primary step attachment:** Step 07 – Section 3.0 – Data Intelligence Layer (DIL)
- **Secondary cross-links:** Step 08 – Section 4.0 – Modeling Intelligence (MI), Step 09 – Section 5.0 – Execution Intelligence (EI), Step 10 – Section 6.0 – Market Structural Awareness (MSA), Step 12 – Section 8.0 – Decision & Risk Architecture (DRA), Step 13 – Section 9.0 – Self-Evaluation & Learning (SEL)

**Instructions for Notion agent:**
1. Keep this page under `Telemetry & QC` as a child spec card.
2. Under **Step 07 – DIL** hub, list this page in a `Data health telemetry` table.
3. Under **Step 13 – SEL**, link it in a `Self-evaluation KPIs` subsection.

### QC Weekly Telemetry V1 (Doc)

- **V2 page:** `Private & Shared/Autopilot Hub/IFNS – UI Master (V2)/Telemetry & QC/QC Weekly Telemetry V1 (Doc) 2afb22c770d981d7b5e2e07d40a63326.md`
- **URL:** https://www.notion.so/2afb22c770d981d7b5e2e07d40a63326
- **Primary step attachment:** Step 07 – Section 3.0 – Data Intelligence Layer (DIL)
- **Secondary cross-links:** Step 08 – Section 4.0 – Modeling Intelligence (MI), Step 09 – Section 5.0 – Execution Intelligence (EI), Step 10 – Section 6.0 – Market Structural Awareness (MSA), Step 12 – Section 8.0 – Decision & Risk Architecture (DRA), Step 13 – Section 9.0 – Self-Evaluation & Learning (SEL)

**Instructions for Notion agent:**
1. Keep this page under `Telemetry & QC` as a child spec card.
2. Under **Step 07 – DIL** hub, list this page in a `Data health telemetry` table.
3. Under **Step 13 – SEL**, link it in a `Self-evaluation KPIs` subsection.

### QC Weekly ETL Skeleton

- **V2 page:** `Private & Shared/Autopilot Hub/IFNS – UI Master (V2)/Telemetry & QC/QC Weekly ETL Skeleton 2afb22c770d98194bcc0e5b10a6288d4.md`
- **URL:** https://www.notion.so/2afb22c770d98194bcc0e5b10a6288d4
- **Primary step attachment:** Step 07 – Section 3.0 – Data Intelligence Layer (DIL)
- **Secondary cross-links:** Step 08 – Section 4.0 – Modeling Intelligence (MI), Step 09 – Section 5.0 – Execution Intelligence (EI), Step 10 – Section 6.0 – Market Structural Awareness (MSA), Step 12 – Section 8.0 – Decision & Risk Architecture (DRA), Step 13 – Section 9.0 – Self-Evaluation & Learning (SEL)

**Instructions for Notion agent:**
1. Keep this page under `Telemetry & QC` as a child spec card.
2. Under **Step 07 – DIL** hub, list this page in a `Data health telemetry` table.
3. Under **Step 13 – SEL**, link it in a `Self-evaluation KPIs` subsection.

### QC Weekly ETL Clip Integration

- **V2 page:** `Private & Shared/Autopilot Hub/IFNS – UI Master (V2)/Telemetry & QC/QC Weekly ETL Clip Integration 2afb22c770d98123954dc16073a49902.md`
- **URL:** https://www.notion.so/2afb22c770d98123954dc16073a49902
- **Primary step attachment:** Step 07 – Section 3.0 – Data Intelligence Layer (DIL)
- **Secondary cross-links:** Step 08 – Section 4.0 – Modeling Intelligence (MI), Step 09 – Section 5.0 – Execution Intelligence (EI), Step 10 – Section 6.0 – Market Structural Awareness (MSA), Step 12 – Section 8.0 – Decision & Risk Architecture (DRA), Step 13 – Section 9.0 – Self-Evaluation & Learning (SEL)

**Instructions for Notion agent:**
1. Keep this page under `Telemetry & QC` as a child spec card.
2. Under **Step 07 – DIL** hub, list this page in a `Data health telemetry` table.
3. Under **Step 13 – SEL**, link it in a `Self-evaluation KPIs` subsection.

### QC Weekly ETL Script

- **V2 page:** `Private & Shared/Autopilot Hub/IFNS – UI Master (V2)/Telemetry & QC/QC Weekly ETL Script 2afb22c770d9815ca652e513fa0b348a.md`
- **URL:** https://www.notion.so/2afb22c770d9815ca652e513fa0b348a
- **Primary step attachment:** Step 07 – Section 3.0 – Data Intelligence Layer (DIL)
- **Secondary cross-links:** Step 08 – Section 4.0 – Modeling Intelligence (MI), Step 09 – Section 5.0 – Execution Intelligence (EI), Step 10 – Section 6.0 – Market Structural Awareness (MSA), Step 12 – Section 8.0 – Decision & Risk Architecture (DRA), Step 13 – Section 9.0 – Self-Evaluation & Learning (SEL)

**Instructions for Notion agent:**
1. Keep this page under `Telemetry & QC` as a child spec card.
2. Under **Step 07 – DIL** hub, list this page in a `Data health telemetry` table.
3. Under **Step 13 – SEL**, link it in a `Self-evaluation KPIs` subsection.

### IO Utils (Telemetry Manifest I O helpers)

- **V2 page:** `Private & Shared/Autopilot Hub/IFNS – UI Master (V2)/Telemetry & QC/IO Utils (Telemetry Manifest I O helpers) 2afb22c770d98191b530dc3c70c67420.md`
- **URL:** https://www.notion.so/2afb22c770d98191b530dc3c70c67420
- **Primary step attachment:** Step 05 – Section 1.0 – Introduction
- **Secondary cross-links:** Step 07 – Section 3.0 – Data Intelligence Layer (DIL), Step 08 – Section 4.0 – Modeling Intelligence (MI), Step 09 – Section 5.0 – Execution Intelligence (EI), Step 10 – Section 6.0 – Market Structural Awareness (MSA), Step 12 – Section 8.0 – Decision & Risk Architecture (DRA), Step 13 – Section 9.0 – Self-Evaluation & Learning (SEL)

**Instructions for Notion agent:**
1. Attach this page under the **primary step hub** above, in a `V2 surfaces` or `Specs & Schemas` subsection.
2. Add cross-links from the **secondary step hubs** so that readers can discover it from all relevant stages.
3. Do not change the body text; only add a short status line if necessary (e.g., `Attached to Step XX spine on YYYY-MM-DD`).

### Manifest Diff Tool

- **V2 page:** `Private & Shared/Autopilot Hub/IFNS – UI Master (V2)/Telemetry & QC/Manifest Diff Tool 2afb22c770d98182a3cfc3ac35dd9d10.md`
- **URL:** https://www.notion.so/2afb22c770d98182a3cfc3ac35dd9d10
- **Primary step attachment:** Step 07 – Section 3.0 – Data Intelligence Layer (DIL)
- **Secondary cross-links:** Step 08 – Section 4.0 – Modeling Intelligence (MI), Step 09 – Section 5.0 – Execution Intelligence (EI), Step 10 – Section 6.0 – Market Structural Awareness (MSA), Step 12 – Section 8.0 – Decision & Risk Architecture (DRA), Step 13 – Section 9.0 – Self-Evaluation & Learning (SEL)

**Instructions for Notion agent:**
1. Keep this page under the `Manifests & Policy` folder as a **schema/spec card**.
2. Under **Step 07 – DIL** and **Step 08 – MI** hubs, reference this card from a `Data & Feature Schemas` table.
3. If the asset encodes constraints or policies (e.g. Policy Matrix, Family Map), also link from **Step 12 – DRA** under `Risk & Policy Schemas`.

### CI IFNS Guard Workflow

- **V2 page:** `Private & Shared/Autopilot Hub/IFNS – UI Master (V2)/Telemetry & QC/CI IFNS Guard Workflow 2afb22c770d98109ba8bfbf5fbede124.md`
- **URL:** https://www.notion.so/2afb22c770d98109ba8bfbf5fbede124
- **Primary step attachment:** Step 05 – Section 1.0 – Introduction
- **Secondary cross-links:** Step 07 – Section 3.0 – Data Intelligence Layer (DIL), Step 08 – Section 4.0 – Modeling Intelligence (MI), Step 09 – Section 5.0 – Execution Intelligence (EI), Step 10 – Section 6.0 – Market Structural Awareness (MSA), Step 12 – Section 8.0 – Decision & Risk Architecture (DRA), Step 13 – Section 9.0 – Self-Evaluation & Learning (SEL)

**Instructions for Notion agent:**
1. Treat this as an **automation/guardrail** implementation detail for manifests and telemetry.
2. Link from **Step 12 – DRA** hub in a `Guards & Automation` subsection.
3. Optionally cross-link from **Step 07 – DIL** and **Step 08 – MI** where manifest changes are most impactful.

### CI Manifest Guard (Python)

- **V2 page:** `Private & Shared/Autopilot Hub/IFNS – UI Master (V2)/Telemetry & QC/CI Manifest Guard (Python) 2afb22c770d9812496aafd166f4e6ced.md`
- **URL:** https://www.notion.so/2afb22c770d9812496aafd166f4e6ced
- **Primary step attachment:** Step 05 – Section 1.0 – Introduction
- **Secondary cross-links:** Step 07 – Section 3.0 – Data Intelligence Layer (DIL), Step 08 – Section 4.0 – Modeling Intelligence (MI), Step 10 – Section 6.0 – Market Structural Awareness (MSA), Step 12 – Section 8.0 – Decision & Risk Architecture (DRA)

**Instructions for Notion agent:**
1. Treat this as an **automation/guardrail** implementation detail for manifests and telemetry.
2. Link from **Step 12 – DRA** hub in a `Guards & Automation` subsection.
3. Optionally cross-link from **Step 07 – DIL** and **Step 08 – MI** where manifest changes are most impactful.

### Runtime – Calendar Gaps 2025

- **V2 page:** `Private & Shared/Autopilot Hub/IFNS – UI Master (V2)/Runtime Templates & Calendars/Runtime – Calendar Gaps 2025 2afb22c770d981bc8461e491fd37d89a.md`
- **URL:** https://www.notion.so/2afb22c770d981bc8461e491fd37d89a
- **Primary step attachment:** Step 04 – Preface Timeline
- **Secondary cross-links:** Step 07 – Section 3.0 – Data Intelligence Layer (DIL), Step 08 – Section 4.0 – Modeling Intelligence (MI), Step 09 – Section 5.0 – Execution Intelligence (EI), Step 10 – Section 6.0 – Market Structural Awareness (MSA), Step 12 – Section 8.0 – Decision & Risk Architecture (DRA)

**Instructions for Notion agent:**
1. Under **Step 04 – Preface Timeline / Evolutionary Arc** hub, link this page in a `Runtime activation & calendars` section.
2. Under **Step 09 – Execution Intelligence (EI)** hub, add a `Runtime scheduling & gaps` subsection pointing here.
3. Under **Step 12 – DRA**, cross-link where runtime actions tie to risk or guardrails.

### Runtime Templates (YAML)

- **V2 page:** `Private & Shared/Autopilot Hub/IFNS – UI Master (V2)/Runtime Templates & Calendars/Runtime Templates (YAML) 2afb22c770d98194bf46d590918f802f.md`
- **URL:** https://www.notion.so/2afb22c770d98194bf46d590918f802f
- **Primary step attachment:** Step 04 – Preface Timeline
- **Secondary cross-links:** Step 07 – Section 3.0 – Data Intelligence Layer (DIL), Step 08 – Section 4.0 – Modeling Intelligence (MI), Step 09 – Section 5.0 – Execution Intelligence (EI), Step 10 – Section 6.0 – Market Structural Awareness (MSA), Step 12 – Section 8.0 – Decision & Risk Architecture (DRA)

**Instructions for Notion agent:**
1. Under **Step 04 – Preface Timeline / Evolutionary Arc** hub, link this page in a `Runtime activation & calendars` section.
2. Under **Step 09 – Execution Intelligence (EI)** hub, add a `Runtime scheduling & gaps` subsection pointing here.
3. Under **Step 12 – DRA**, cross-link where runtime actions tie to risk or guardrails.

## 4. Implementation checklist for the Notion/Git agent

To apply this phase cleanly, the agent should:

1. Open each **Step hub** (from Phase 1) and create a dedicated block titled `V2 surfaces linked to this step`.

2. For each V2 asset in Section 3 above:

   - Add a link from the primary step hub under `V2 surfaces`,

   - Optionally add cross-links from secondary steps where noted.

3. For schema/policy/catalog assets:

   - Ensure they are also represented as **rows in the relevant Notion databases** (to be formalized in later phases),

   - Use the V2 pages as the `Spec card` or `Doc` linked from those rows.

4. Do not remove any existing links; only **add** structure and labels so the relationships become obvious.
