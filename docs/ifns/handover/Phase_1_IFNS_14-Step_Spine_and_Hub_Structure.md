# Phase 1 – IFNS 14-Step Master Spine & Hub/Child Structure

This handover file turns the **14-step IFNS – UI Master** into a clear spine with a consistent hub/child pattern,
so that future agents can reorganize Notion without deleting any content.

## 1. Canonical 14-step spine

The table below treats the 14 steps as the conceptual spine of IFNS. Each row maps the step to its Notion hub page and
to the Core ML build stages it primarily relates to.

| Step | Section Key | Canonical Title | Step Hub URL | Narrative & Intent lines (approx.) | Core ML Stage Link |
|-----:|-------------|-----------------|-------------|-------------------------------------|--------------------|
| 1 | Preface | Preface Integration | https://www.notion.so/2adb22c770d98068a351dc6f69822f3b | ~37 lines | Cross-cutting (all stages) |
| 2 | Preface | Executive Summary | https://www.notion.so/2adb22c770d98037a4a0c184f917d64d | ~47 lines | Cross-cutting (all stages) |
| 3 | 0.0 | Visionary–Technical Overview | https://www.notion.so/2adb22c770d98074b9e8f2083a4788f4 | ~86 lines | Core ML lifecycle overview |
| 4 | 0.1 | Preface Timeline – Evolutionary Arc | https://www.notion.so/2adb22c770d980118757c73286ae8eee | ~128 lines | Phased evolution of capabilities |
| 5 | 1.0 | Introduction — Operational Genesis Framework | https://www.notion.so/2adb22c770d9801480f0f8e8b8fdfbc1 | ~64 lines | Stage 1 – Foundations & Architecture |
| 6 | 2.0 | System Architecture | https://www.notion.so/2adb22c770d9804c8bf0c3eea37bd508 | ~126 lines | Stages 1–7 – Structural view |
| 7 | 3.0 | Data Intelligence Layer (DIL) | https://www.notion.so/2adb22c770d980d9bf13e90e8ec2a3f2 | ~153 lines | Stage 2 – Data & Feature pipeline |
| 8 | 4.0 | Modeling Intelligence (MI) | https://www.notion.so/2adb22c770d98023af38f62fc8fb2f1c | ~163 lines | Stage 3 – Modeling & Training |
| 9 | 5.0 | Execution Intelligence (EI) | https://www.notion.so/2adb22c770d980b09792ec621d9ad5a3 | ~144 lines | Stages 4–7 – Backtests, Risk, Execution |
| 10 | 6.0 | Market Structural Awareness (MSA) | https://www.notion.so/2adb22c770d980dba9b7eb32efd12839 | ~134 lines | Stages 2–4 – Regimes & structure |
| 11 | 7.0 | Model & Signal Integration (MSI) | https://www.notion.so/2adb22c770d980bd9079f1ccfba0ffac | ~166 lines | Stages 3–5 – Integration & risk link |
| 12 | 8.0 | Decision & Risk Architecture (DRA) | https://www.notion.so/2adb22c770d9802e83cfec4d22442a27 | ~168 lines | Stages 4–7 – Risk & governance |
| 13 | 9.0 | Self-Evaluation & Learning (SEL) | https://www.notion.so/2adb22c770d980b99d76dadeee0f46f8 | ~170 lines | Stages 3–7 – Learning & evolution |
| 14 | 10.0 | Advanced Awareness & Quantum Cognition | https://www.notion.so/2afb22c770d9814992a7dfd8195ebbc4 | ~152 lines | Stages 3–7 – Scenarios & meta-reasoning |

## 2. Standard hub/child model for all steps

Each step already has three child pages linked from its hub:

- `01 – Narrative & Intent`
- `02 – Implementation Reference`
- `03 – Notes & Decisions`

To make the 14-step master easier to read and extend, keep this structure as the **baseline** and apply the following roles:

1. **Step Hub (this page)** – Index/landing page for the step. Keep only:

   - A short 3–5 line summary of what this step does.

   - A structured list of child pages (the three standard ones plus any future children).

2. **01 – Narrative & Intent** – Long-form explanation of *why* this step exists and how it fits into the overall IFNS story.

3. **02 – Implementation Reference** – Technical and operational detail: data flows, components, configs, and references into V2 / runtime.

4. **03 – Notes & Decisions** – Decision log, trade-offs, and historical notes; nothing should be deleted, only appended or clarified.


For long steps (most Narrative & Intent pages are 120–170 non-empty lines), future agents may additionally:

- Insert level-2 headings (`##`) inside `Narrative & Intent` to create **logical sections** (Context, Actors, Flows, Scenarios, Edge Cases).

- Or, when a section becomes independently important, split it into a **new child page**, linked from the hub under a fourth slot, e.g.:

  - `04 – UX & SxE Mirrors`
  - `04 – Telemetry & QC Anchors`
  - `04 – Runtime & Calendars`

The golden rule is: **never delete text**; instead, move or duplicate it into clearer child pages.

## 3. Per-step hub/child plan

For each step, this section describes how the existing pages should be treated and where future splits should happen.

### Step 01 – Preface Integration

- **Section key:** `Preface`
- **Step hub page:** `Private & Shared/Autopilot Hub/IFNS – UI Master/Step 01 – Preface Integration 2adb22c770d98068a351dc6f69822f3b.md`
- **Hub URL:** https://www.notion.so/2adb22c770d98068a351dc6f69822f3b
- **`01  Narrative & Intent` size:** ≈ 37 non-empty lines
- **Existing children (keep all):**
  - `01 – Narrative & Intent`
  - `02 – Implementation Reference`
  - `03 – Notes & Decisions`

**Recommended structure:**

1. Treat the current step page as a **pure hub** (no long body text; only summary + links).

2. Keep `Narrative & Intent` as the primary long-form document, but:

   - Introduce clear `##` sections: Context, Actors, Flows, Scenarios, Edge Cases.

   - When sections become very long, split them into new child pages (04/05…) and link them from the hub.

3. Keep `Implementation Reference` focused on structures that will later bind into V2 (indicators, telemetry, runtimes, catalogs).

4. Use `Notes & Decisions` strictly as a log (date-stamped bullets) so nothing is lost during future refactors.


**Step-specific notes:**
- Acts as the conceptual entry point for the entire IFNS; keep references broad and cross-cutting rather than technical.


### Step 02 – Executive Summary

- **Section key:** `Preface`
- **Step hub page:** `Private & Shared/Autopilot Hub/IFNS – UI Master/Step 02 – Executive Summary 2adb22c770d98037a4a0c184f917d64d.md`
- **Hub URL:** https://www.notion.so/2adb22c770d98037a4a0c184f917d64d
- **`01  Narrative & Intent` size:** ≈ 47 non-empty lines
- **Existing children (keep all):**
  - `01 – Narrative & Intent`
  - `02 – Implementation Reference`
  - `03 – Notes & Decisions`

**Recommended structure:**

1. Treat the current step page as a **pure hub** (no long body text; only summary + links).

2. Keep `Narrative & Intent` as the primary long-form document, but:

   - Introduce clear `##` sections: Context, Actors, Flows, Scenarios, Edge Cases.

   - When sections become very long, split them into new child pages (04/05…) and link them from the hub.

3. Keep `Implementation Reference` focused on structures that will later bind into V2 (indicators, telemetry, runtimes, catalogs).

4. Use `Notes & Decisions` strictly as a log (date-stamped bullets) so nothing is lost during future refactors.


**Step-specific notes:**
- Designed for executive readers; ensure `Narrative & Intent` is readable as a standalone story with minimal technical detail.


### Step 03 – Visionary–Technical Overview

- **Section key:** `0.0`
- **Step hub page:** `Private & Shared/Autopilot Hub/IFNS – UI Master/Step 03 – Visionary–Technical Overview 2adb22c770d98074b9e8f2083a4788f4.md`
- **Hub URL:** https://www.notion.so/2adb22c770d98074b9e8f2083a4788f4
- **`01 – Narrative & Intent` size:** ≈ 86 non-empty lines
- **Existing children (keep all):**
  - `01 – Narrative & Intent`
  - `02 – Implementation Reference`
  - `03 – Notes & Decisions`

**Recommended structure:**

1. Treat the current step page as a **pure hub** (no long body text; only summary + links).

2. Keep `Narrative & Intent` as the primary long-form document, but:

   - Introduce clear `##` sections: Context, Actors, Flows, Scenarios, Edge Cases.

   - When sections become very long, split them into new child pages (04/05…) and link them from the hub.

3. Keep `Implementation Reference` focused on structures that will later bind into V2 (indicators, telemetry, runtimes, catalogs).

4. Use `Notes & Decisions` strictly as a log (date-stamped bullets) so nothing is lost during future refactors.


**Step-specific notes:**
- Should tie the narrative to the Core ML lifecycle; `Implementation Reference` can host the high-level lifecycle diagrams.


### Step 04 – Preface Timeline – Evolutionary Arc

- **Section key:** `0.1`
- **Step hub page:** `Private & Shared/Autopilot Hub/IFNS – UI Master/Step 04 – Preface Timeline 2adb22c770d980118757c73286ae8eee.md`
- **Hub URL:** https://www.notion.so/2adb22c770d980118757c73286ae8eee
- **`01 – Narrative & Intent` size:** ≈ 128 non-empty lines
- **Existing children (keep all):**
  - `01 – Narrative & Intent`
  - `02 – Implementation Reference`
  - `03 – Notes & Decisions`

**Recommended structure:**

1. Treat the current step page as a **pure hub** (no long body text; only summary + links).

2. Keep `Narrative & Intent` as the primary long-form document, but:

   - Introduce clear `##` sections: Context, Actors, Flows, Scenarios, Edge Cases.

   - When sections become very long, split them into new child pages (04/05…) and link them from the hub.

3. Keep `Implementation Reference` focused on structures that will later bind into V2 (indicators, telemetry, runtimes, catalogs).

4. Use `Notes & Decisions` strictly as a log (date-stamped bullets) so nothing is lost during future refactors.


**Step-specific notes:**
- Timeline/roadmap of IFNS evolution; good candidate for Gantt-style or milestone tables later in Notion.


### Step 05 – Introduction — Operational Genesis Framework

- **Section key:** `1.0`
- **Step hub page:** `Private & Shared/Autopilot Hub/IFNS – UI Master/Step 05 – Section 1 0 – Introduction 2adb22c770d9801480f0f8e8b8fdfbc1.md`
- **Hub URL:** https://www.notion.so/2adb22c770d9801480f0f8e8b8fdfbc1
- **`01 – Narrative & Intent` size:** ≈ 64 non-empty lines
- **Existing children (keep all):**
  - `01 – Narrative & Intent`
  - `02 – Implementation Reference`
  - `03 – Notes & Decisions`

**Recommended structure:**

1. Treat the current step page as a **pure hub** (no long body text; only summary + links).

2. Keep `Narrative & Intent` as the primary long-form document, but:

   - Introduce clear `##` sections: Context, Actors, Flows, Scenarios, Edge Cases.

   - When sections become very long, split them into new child pages (04/05…) and link them from the hub.

3. Keep `Implementation Reference` focused on structures that will later bind into V2 (indicators, telemetry, runtimes, catalogs).

4. Use `Notes & Decisions` strictly as a log (date-stamped bullets) so nothing is lost during future refactors.


**Step-specific notes:**
- This is where the **Operational Genesis Framework** is defined; make sure the language is stable before binding V2 artifacts here.


### Step 06 – System Architecture

- **Section key:** `2.0`
- **Step hub page:** `Private & Shared/Autopilot Hub/IFNS – UI Master/Step 06 – Section 2 0 – System Architecture 2adb22c770d9804c8bf0c3eea37bd508.md`
- **Hub URL:** https://www.notion.so/2adb22c770d9804c8bf0c3eea37bd508
- **`01 – Narrative & Intent` size:** ≈ 126 non-empty lines
- **Existing children (keep all):**
  - `01 – Narrative & Intent`
  - `02 – Implementation Reference`
  - `03 – Notes & Decisions`

**Recommended structure:**

1. Treat the current step page as a **pure hub** (no long body text; only summary + links).

2. Keep `Narrative & Intent` as the primary long-form document, but:

   - Introduce clear `##` sections: Context, Actors, Flows, Scenarios, Edge Cases.

   - When sections become very long, split them into new child pages (04/05…) and link them from the hub.

3. Keep `Implementation Reference` focused on structures that will later bind into V2 (indicators, telemetry, runtimes, catalogs).

4. Use `Notes & Decisions` strictly as a log (date-stamped bullets) so nothing is lost during future refactors.


**Step-specific notes:**
- Primary home for system diagrams and component lists; future SXE bridge work will attach strongly to this step.


### Step 07 – Data Intelligence Layer (DIL)

- **Section key:** `3.0`
- **Step hub page:** `Private & Shared/Autopilot Hub/IFNS – UI Master/Step 07 – Section 3 0 – Data Intelligence Layer (D 2adb22c770d980d9bf13e90e8ec2a3f2.md`
- **Hub URL:** https://www.notion.so/2adb22c770d980d9bf13e90e8ec2a3f2
- **`01 – Narrative & Intent` size:** ≈ 153 non-empty lines
- **Existing children (keep all):**
  - `01 – Narrative & Intent`
  - `02 – Implementation Reference`
  - `03 – Notes & Decisions`

**Recommended structure:**

1. Treat the current step page as a **pure hub** (no long body text; only summary + links).

2. Keep `Narrative & Intent` as the primary long-form document, but:

   - Introduce clear `##` sections: Context, Actors, Flows, Scenarios, Edge Cases.

   - When sections become very long, split them into new child pages (04/05…) and link them from the hub.

3. Keep `Implementation Reference` focused on structures that will later bind into V2 (indicators, telemetry, runtimes, catalogs).

4. Use `Notes & Decisions` strictly as a log (date-stamped bullets) so nothing is lost during future refactors.


**Step-specific notes:**
- Main anchor for **Data Intelligence Layer (DIL)**; this is where CatalogL1/L2L3 and feature schemas will attach in later phases.


### Step 08 – Modeling Intelligence (MI)

- **Section key:** `4.0`
- **Step hub page:** `Private & Shared/Autopilot Hub/IFNS – UI Master/Step 08 – Section 4 0 – Modeling Intelligence (MI) 2adb22c770d98023af38f62fc8fb2f1c.md`
- **Hub URL:** https://www.notion.so/2adb22c770d98023af38f62fc8fb2f1c
- **`01 – Narrative & Intent` size:** ≈ 163 non-empty lines
- **Existing children (keep all):**
  - `01 – Narrative & Intent`
  - `02 – Implementation Reference`
  - `03 – Notes & Decisions`

**Recommended structure:**

1. Treat the current step page as a **pure hub** (no long body text; only summary + links).

2. Keep `Narrative & Intent` as the primary long-form document, but:

   - Introduce clear `##` sections: Context, Actors, Flows, Scenarios, Edge Cases.

   - When sections become very long, split them into new child pages (04/05…) and link them from the hub.

3. Keep `Implementation Reference` focused on structures that will later bind into V2 (indicators, telemetry, runtimes, catalogs).

4. Use `Notes & Decisions` strictly as a log (date-stamped bullets) so nothing is lost during future refactors.


**Step-specific notes:**
- Main anchor for **Modeling Intelligence (MI)**; training flows, CV regimes, and model selection live here conceptually.


### Step 09 – Execution Intelligence (EI)

- **Section key:** `5.0`
- **Step hub page:** `Private & Shared/Autopilot Hub/IFNS – UI Master/Step 09 – Section 5 0 – Execution Intelligence (EI 2adb22c770d980b09792ec621d9ad5a3.md`
- **Hub URL:** https://www.notion.so/2adb22c770d980b09792ec621d9ad5a3
- **`01 – Narrative & Intent` size:** ≈ 144 non-empty lines
- **Existing children (keep all):**
  - `01 – Narrative & Intent`
  - `02 – Implementation Reference`
  - `03 – Notes & Decisions`

**Recommended structure:**

1. Treat the current step page as a **pure hub** (no long body text; only summary + links).

2. Keep `Narrative & Intent` as the primary long-form document, but:

   - Introduce clear `##` sections: Context, Actors, Flows, Scenarios, Edge Cases.

   - When sections become very long, split them into new child pages (04/05…) and link them from the hub.

3. Keep `Implementation Reference` focused on structures that will later bind into V2 (indicators, telemetry, runtimes, catalogs).

4. Use `Notes & Decisions` strictly as a log (date-stamped bullets) so nothing is lost during future refactors.


**Step-specific notes:**
- Main anchor for **Execution Intelligence (EI)**; will later host autopilot harness behavior and gate definitions conceptually.


### Step 10 – Market Structural Awareness (MSA)

- **Section key:** `6.0`
- **Step hub page:** `Private & Shared/Autopilot Hub/IFNS – UI Master/Step 10 – Section 6 0 – Market Structural Awarenes 2adb22c770d980dba9b7eb32efd12839.md`
- **Hub URL:** https://www.notion.so/2adb22c770d980dba9b7eb32efd12839
- **`01 – Narrative & Intent` size:** ≈ 134 non-empty lines
- **Existing children (keep all):**
  - `01 – Narrative & Intent`
  - `02 – Implementation Reference`
  - `03 – Notes & Decisions`

**Recommended structure:**

1. Treat the current step page as a **pure hub** (no long body text; only summary + links).

2. Keep `Narrative & Intent` as the primary long-form document, but:

   - Introduce clear `##` sections: Context, Actors, Flows, Scenarios, Edge Cases.

   - When sections become very long, split them into new child pages (04/05…) and link them from the hub.

3. Keep `Implementation Reference` focused on structures that will later bind into V2 (indicators, telemetry, runtimes, catalogs).

4. Use `Notes & Decisions` strictly as a log (date-stamped bullets) so nothing is lost during future refactors.


**Step-specific notes:**
- Captures cross-market structure and regime thinking; later linked to market-structure indicators in the Catalog and Telemetry.


### Step 11 – Model & Signal Integration (MSI)

- **Section key:** `7.0`
- **Step hub page:** `Private & Shared/Autopilot Hub/IFNS – UI Master/Step 11 – Section 7 0 – Model & Signal Integration 2adb22c770d980bd9079f1ccfba0ffac.md`
- **Hub URL:** https://www.notion.so/2adb22c770d980bd9079f1ccfba0ffac
- **`01 – Narrative & Intent` size:** ≈ 166 non-empty lines
- **Existing children (keep all):**
  - `01 – Narrative & Intent`
  - `02 – Implementation Reference`
  - `03 – Notes & Decisions`

**Recommended structure:**

1. Treat the current step page as a **pure hub** (no long body text; only summary + links).

2. Keep `Narrative & Intent` as the primary long-form document, but:

   - Introduce clear `##` sections: Context, Actors, Flows, Scenarios, Edge Cases.

   - When sections become very long, split them into new child pages (04/05…) and link them from the hub.

3. Keep `Implementation Reference` focused on structures that will later bind into V2 (indicators, telemetry, runtimes, catalogs).

4. Use `Notes & Decisions` strictly as a log (date-stamped bullets) so nothing is lost during future refactors.


**Step-specific notes:**
- Glue layer for MSxE – how models, signals, and execution interact; a natural home for integration diagrams.


### Step 12 – Decision & Risk Architecture (DRA)

- **Section key:** `8.0`
- **Step hub page:** `Private & Shared/Autopilot Hub/IFNS – UI Master/Step 12 – Section 8 0 – Decision & Risk Architectu 2adb22c770d9802e83cfec4d22442a27.md`
- **Hub URL:** https://www.notion.so/2adb22c770d9802e83cfec4d22442a27
- **`01 – Narrative & Intent` size:** ≈ 168 non-empty lines
- **Existing children (keep all):**
  - `01 – Narrative & Intent`
  - `02 – Implementation Reference`
  - `03 – Notes & Decisions`

**Recommended structure:**

1. Treat the current step page as a **pure hub** (no long body text; only summary + links).

2. Keep `Narrative & Intent` as the primary long-form document, but:

   - Introduce clear `##` sections: Context, Actors, Flows, Scenarios, Edge Cases.

   - When sections become very long, split them into new child pages (04/05…) and link them from the hub.

3. Keep `Implementation Reference` focused on structures that will later bind into V2 (indicators, telemetry, runtimes, catalogs).

4. Use `Notes & Decisions` strictly as a log (date-stamped bullets) so nothing is lost during future refactors.


**Step-specific notes:**
- Central specification for risk, governance, and decision policies; all guardrails and thresholds conceptually roll up here.


### Step 13 – Self-Evaluation & Learning (SEL)

- **Section key:** `9.0`
- **Step hub page:** `Private & Shared/Autopilot Hub/IFNS – UI Master/Step 13 – Section 9 0 – Self-Evaluation & Learning 2adb22c770d980b99d76dadeee0f46f8.md`
- **Hub URL:** https://www.notion.so/2adb22c770d980b99d76dadeee0f46f8
- **`01 – Narrative & Intent` size:** ≈ 170 non-empty lines
- **Existing children (keep all):**
  - `01 – Narrative & Intent`
  - `02 – Implementation Reference`
  - `03 – Notes & Decisions`

**Recommended structure:**

1. Treat the current step page as a **pure hub** (no long body text; only summary + links).

2. Keep `Narrative & Intent` as the primary long-form document, but:

   - Introduce clear `##` sections: Context, Actors, Flows, Scenarios, Edge Cases.

   - When sections become very long, split them into new child pages (04/05…) and link them from the hub.

3. Keep `Implementation Reference` focused on structures that will later bind into V2 (indicators, telemetry, runtimes, catalogs).

4. Use `Notes & Decisions` strictly as a log (date-stamped bullets) so nothing is lost during future refactors.


**Step-specific notes:**
- Defines how IFNS learns from itself; log-like content here should be preserved and never overwritten.


### Step 14 – Advanced Awareness & Quantum Cognition

- **Section key:** `10.0`
- **Step hub page:** `Private & Shared/Autopilot Hub/IFNS – UI Master/Step 14 – Sections 11 0–14 0 – Advanced Awareness 2afb22c770d9814992a7dfd8195ebbc4.md`
- **Hub URL:** https://www.notion.so/2afb22c770d9814992a7dfd8195ebbc4
- **`01 – Narrative & Intent` size:** ≈ 152 non-empty lines
- **Existing children (keep all):**
  - `01 – Narrative & Intent`
  - `02 – Implementation Reference`
  - `03 – Notes & Decisions`

**Recommended structure:**

1. Treat the current step page as a **pure hub** (no long body text; only summary + links).

2. Keep `Narrative & Intent` as the primary long-form document, but:

   - Introduce clear `##` sections: Context, Actors, Flows, Scenarios, Edge Cases.

   - When sections become very long, split them into new child pages (04/05…) and link them from the hub.

3. Keep `Implementation Reference` focused on structures that will later bind into V2 (indicators, telemetry, runtimes, catalogs).

4. Use `Notes & Decisions` strictly as a log (date-stamped bullets) so nothing is lost during future refactors.


**Step-specific notes:**
- Speculative/advanced layer; can remain narrative-heavy, but must still link back to concrete telemetry and KPIs where possible.


## 4. Skeleton crosswalk: 14 steps → V2 / runtime surfaces

This table does **not** move any pages yet. It simply states where V2 assets and runtime surfaces are expected to hang off the 14-step spine in later phases.

| Step | Role in lifecycle | Primary V2 / runtime attachments (future) |
|-----:|--------------------|-------------------------------------------|
| 1 | Preface / framing | UI Master V2 Root (high-level links only) |
| 2 | Executive framing | UI Master V2 Root, selected Indicator System overviews |
| 3 | Lifecycle overview | Core ML Build (overview), Indicator System (summary), Runtime & Calendars (high-level) |
| 4 | Evolution roadmap | Core ML Build (phased roadmaps), Runtime & Calendars (phased activations) |
| 5 | Operational genesis | System Architecture, early Manifests & Policy anchors |
| 6 | System structure | Core ML Build, Manifests & Policy, Catalog & Universe (wiring level) |
| 7 | Data intelligence (DIL) | Catalog & Universe, Indicator System (data/feature phases), Telemetry & QC (data health) |
| 8 | Modeling intelligence (MI) | Core ML Build (training stages), Indicator System (model-facing bundles), Telemetry & QC (model health) |
| 9 | Execution intelligence (EI) | Runtime & Calendars, Telemetry & QC (execution metrics), future harness/mirror specs |
| 10 | Market structural awareness (MSA) | Catalog & Universe (market structure), Indicator System (regime features), Telemetry & QC (regime drift) |
| 11 | Model & signal integration (MSI) | Core ML Build, Telemetry & QC (integration checks), Manifests & Policy (signal governance) |
| 12 | Decision & risk architecture (DRA) | Manifests & Policy (constraints), Telemetry & QC (risk KPIs), Runtime & Calendars (risk actions) |
| 13 | Self-evaluation & learning (SEL) | Telemetry & QC (learning KPIs), Catalog & Universe (evolving feature sets) |
| 14 | Advanced awareness & meta-reasoning | Indicator System (advanced features), Telemetry & QC (advanced scenarios), Runtime & Calendars (what-if runs) |