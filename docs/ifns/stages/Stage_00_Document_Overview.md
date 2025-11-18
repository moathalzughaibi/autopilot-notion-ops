# Stage 00 – Core ML Build Document Overview

## 01 – Narrative & Intent

This document defines **Stage 00 – Core ML Build Document Overview** for the Intelligent Financial Neural System (IFNS).

The goal of Stage 00 is **not** to introduce new logic or components. Instead, it:

- Explains **how the Core ML Build specification is structured** (Stages 01–07).
- Shows how these stages **connect to the 14 IFNS Integrated Steps** and to the SxE (System-to-Experience) philosophy.
- Defines the **artifact types, naming conventions, and locations** that the rest of the spec will use (Markdown, tables, JSON/NDJSON, registries, telemetry).
- Acts as the **entry point** for anyone reading or implementing the IFNS Core ML Build.

You can think of Stage 00 as the **table of contents plus contract for the spec itself**.  
All subsequent Stage documents (01–07) will follow the patterns laid out here.

---

## 02 – Structure of the Core ML Build

The Core ML Build spec is organized into **eight stages** (00–07).  
Stage 00 is this overview; Stages 01–07 describe the actual build phases.

### 2.1 Stage List

- **Stage 00 – Document Overview**  
  Explains what the Core ML Build spec is, how it is organized, and how it relates to the 14 IFNS Steps and SxE.

- **Stage 01 – Foundations & Architecture**  
  Defines repository layout, configuration schemas, core services/components, environment separation (`offline`, `paper`, `live`), and key JSON/NDJSON contracts.

- **Stage 02 – Data & Feature Pipeline**  
  Specifies Data Intelligence Layer (DIL) schemas, ingestion pipelines, feature frameworks, labeling policies, and dataset definitions.

- **Stage 03 – Modeling & Training**  
  Defines model families, Model Registry, training/experiment process, metrics, and artifacts.

- **Stage 04 – Backtesting & Evaluation**  
  Describes the Harness, Signal API usage, backtest scenarios, evaluation metrics, and Backtests Index.

- **Stage 05 – Risk, Execution & SxE Link**  
  Encodes Decision & Risk Architecture (DRA), execution policies, MSI contracts, and the binding to SxE (Mirror/Admin + telemetry).

- **Stage 06 – Paper Trading**  
  Specifies Paper Trading environment, Paper Broker behavior, session registries, and paper-run telemetry.

- **Stage 07 – Live Trading & Operations**  
  Defines Live Trading environment, live broker adapters, operational runbooks, incident handling, and operational telemetry.

Each Stage document answers three questions:

1. **Narrative & Intent** – What is this stage for?  
2. **Contracts & Artifacts** – Which tables, JSON/NDJSON files, and UI bindings does it define?  
3. **Notes & Decisions** – Key design decisions, trade-offs, and implementation hints.

---

### 2.2 Relationship to the 14 IFNS Integrated Steps

The **14 IFNS Steps** are the **conceptual and architectural blueprint**.  
The **Core ML Build Stages** are the **implementation-oriented build plan**.

A simplified mapping:

- **Steps 01–04** (Preface & Overview)  
  → Provide framing and narrative context for all Stages 00–07.

- **Step 05 – Operational Genesis Framework**  
  → Directly informs **Stage 01** (Foundations & Architecture) and this overview.

- **Step 06 – System Architecture**  
  → Cross-cuts **Stages 01–07**, describing how all components fit together.

- **Step 07 – DIL**  
  → Primary reference for **Stage 02**.

- **Step 08 – MI**  
  → Primary reference for **Stage 03**.

- **Step 09 – EI**  
  → Shared reference for **Stages 04, 05, 06, 07**.

- **Step 10 – MSA**  
  → Shared reference for **Stages 02–04**.

- **Step 11 – MSI**  
  → Shared reference for **Stages 03–05**.

- **Step 12 – DRA**  
  → Primary reference for **Stage 05**, with implications in **Stages 04, 06, 07**.

- **Step 13 – SEL**  
  → Cross-cuts **Stages 03–07** (learning loops, evidence, promotion/rollback).

- **Step 14 – Advanced Awareness & Quantum Cognition**  
  → Builds on **Stages 03–07** using scenario engines, meta-metrics, and narrative intelligence.

**Rule of thumb:**

- If you want to understand **what** a layer is and why it exists → read the relevant **Step**.  
- If you want to know **how to build and wire it** → read the corresponding **Stage**.

---

## 03 – Artifact Types & Naming Conventions

To keep the specification and implementation aligned, Stage 00 defines a set of **standard artifact types** and **naming conventions**.

### 3.1 Markdown Specs (this repo)

All narrative/system specs live as Markdown under something like:

```text
docs/ifns/
  Step_01_….md … Step_14_….md
  Stage_00_Document_Overview.md
  Stage_01_Foundations_and_Architecture.md
  …
  Stage_07_Live_Trading_and_Operations.md
  IFNS_UI_Steps_Index.md
  IFNS_UI_Master_Summary.md
  IFNS_UI_Drafts_and_Working_Notes.md
```

These files:

- Are the **source of truth** for design and contracts.
- Are synced into Notion as read-only or discussion-friendly copies.
- Use a consistent header format:
  - `# Stage XX – Title`
  - `## 01 – Narrative & Intent`
  - `## 02 – Contracts & Artifacts` (or similar)
  - `## 03 – Notes & Decisions`

### 3.2 Structured Tables (Excel / CSV)

Many implementation details (schemas, matrices, registries) live as **tables**, either in:

- Excel workbooks (for initial design, color-coded views).
- CSV files (for Git + Notion DB synchronization and programmatic use).

Typical table categories:

- **Schemas** – data models (e.g., price/feature/label tables, telemetry schemas).  
- **Registries** – models, backtests, sessions, policies, providers.  
- **Policies & Gates** – risk envelopes, MSI policies, execution policies, promotion rules.  
- **Checklists & Matrices** – provider evaluation, gap matrices, UI/Admin matrices.

Stage docs will refer to tables by **logical names** (e.g., `Risk_Envelopes`, `Model_Registry`, `Feature_TREND_MTF_V1`) and by their physical home (Excel sheet, CSV path, or Notion DB).

### 3.3 JSON / NDJSON Contracts

Runtime components exchange information using **JSON** and **NDJSON** files/streams, for example:

- `model_registry.json`
- `backtests_index.json`
- `paper_sessions.json`, `live_sessions.json`
- `risk_envelope.json`, `kill_switch_spec.json`, `cooldown_spec.json`
- Telemetry streams:
  - `events_backtest.ndjson`
  - `events_execution.ndjson`
  - `events_risk.ndjson`
  - `events_sel.ndjson`

Each Stage doc explicitly lists:

- Which JSON/NDJSON contracts it defines or depends on.
- Which components read/write these artifacts.
- How SxE (Mirror/Admin) binds to them.

### 3.4 SxE Bindings (Mirror & Admin)

Finally, each Stage includes a subsection describing:

- **Mirror views** – KPIs, dashboards, and cards reading from:
  - Registries,
  - Telemetry,
  - Aggregated metrics.

- **Admin views** – consoles and editors that:
  - Inspect and (sometimes) modify registries and policies,
  - Drive promotions, rollbacks, capital changes, and configuration edits.

Stages do **not** define UI layouts pixel-by-pixel. Instead, they define:

- Which backend artifacts exist,
- Which SxE views must exist to surface and control them.

---

## 04 – How to Read and Use the Core ML Build Spec

The intended reading/usage pattern:

1. **Start at Stage 00 (this document)**  
   - Understand the overall structure and purpose of the Stages.

2. **Jump to the Stage relevant to your work**  
   - Data engineer → Stage 02 (DIL)  
   - ML engineer → Stage 03 (Modeling & Training)  
   - Quant/researcher → Stages 02–04  
   - Risk/ops lead → Stages 05–07

3. **Cross-reference the relevant IFNS Step(s)**  
   - For conceptual understanding and terminology alignment.

4. **Follow references into tables and JSON contracts**  
   - Use the names and paths defined in each Stage.

5. **Return to Steps Index & Drafts log**  
   - To see status, open questions, and ongoing refinements.

This loop keeps **conceptual, implementation, and operational views** aligned.

---

## 05 – Notes & Decisions

- Stage 00 is intentionally lightweight on technical detail; its job is to:
  - Fix the **spine of the documentation**,
  - Standardize naming and structure,
  - Make it obvious where any given piece of logic or contract belongs.

- All future changes to documentation structure (e.g., adding a new Stage or major artifact family) should:
  - First be reflected here (Stage 00),
  - Then propagated into the Steps Index, Drafts log, and relevant Stage docs.

- The **14 IFNS Steps** remain the master conceptual framework.  
  The **Core ML Build Stages (00–07)** are the actionable companion: “how to build the system described by those Steps.”

- As the implementation matures, Stage 00 can be extended with:
  - A more detailed diagram of spec dependencies,
  - Pointers to live SxE dashboards and Notion databases,
  - Version history and links to release notes for major spec iterations.
