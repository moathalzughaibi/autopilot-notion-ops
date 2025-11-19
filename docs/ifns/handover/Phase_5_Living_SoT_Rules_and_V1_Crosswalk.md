# Phase 5 – Living Source-of-Truth Rules & V1 Crosswalk

This handover defines how **Notion becomes the living Source of Truth (SoT)** for IFNS, and how the older 
`IFNS – UI Master` (V1) pages should be treated relative to the 14-step spine and the V2/UI surfaces.

It does **not** delete or archive anything automatically; it provides rules, so future agents know exactly 
how to evolve the workspace without breaking the structure you built.

## 1. Source-of-Truth model (Notion ↔ Git ↔ Runtime)

Use this 3-layer SoT model going forward:

1. **Notion = Narrative & Configuration SoT**

   - All **conceptual specs, UX intent, risk policies, and catalog definitions** live here in human-readable form.

   - The 14-step spine + Feature Catalog + QCWeekly + CalendarGaps2025 + V2 spec cards are the anchors.

2. **Git = Implementer-facing mirror**

   - Stores CSV/JSON/YAML **exports** of the Notion databases and spec pages.

   - Any `*.csv`, `*.json`, or `*.yaml` that reflects a Notion DB should be treated as a **generated artifact**, not the primary SoT.

3. **Runtime = Executable state**

   - Uses manifests, templates, and configs that are derived from Notion (directly or via Git).

   - When runtime behavior changes (new indicators, guards, KPIs), the Notion specs **must be updated first**, then propagated.


**Practical rule:** If there is a conflict between Notion and a CSV/JSON/YAML file in Git, **Notion wins**, and Git must be re-synced.

## 2. Page types and how to treat them

Every IFNS page or asset should be classified into one of these types:

1. **Step hubs** (14-step spine) – navigation + high-level framing.

2. **Spec pages / spec cards** – explain *what* a dataset, manifest, indicator family, or runtime template means.

3. **Database row pages** – individual instances (feature rows, QCWeekly snapshots, calendar gaps, etc.).

4. **Historical / drafts** – earlier experiments and working notes.


Rules:

- Hubs should stay **lightweight** (summaries, links, embedded views), not walls of text.

- Spec cards should contain **narrative + field explanations**, *not* full tables copied from CSV.

- Tables live as **Notion databases**, not static markdown lists.

- Drafts are never deleted; at most, they are clearly labeled as historical.

## 3. V1 (`IFNS – UI Master`) crosswalk principles

The `IFNS – UI Master` (V1) tree contains index pages, early summaries, and draft slices. Examples from the export:

- `00 – Index` — `Private & Shared/Autopilot Hub/IFNS – UI Master/00 – Index 2adb22c770d98017a807f70a910c4140.md`
- `01 – Summary` — `Private & Shared/Autopilot Hub/IFNS – UI Master/01 – Summary 2adb22c770d980b59513f1f15f9fbebd.md`
- `02 – Drafts & Working Notes` — `Private & Shared/Autopilot Hub/IFNS – UI Master/02 – Drafts & Working Notes 2adb22c770d98038b869cc5a857acc96.md`
- `Core ML Build Stages` — `Private & Shared/Autopilot Hub/IFNS – UI Master/Core ML Build Stages 2afb22c770d981659934c6f587d8ea9b.md`
- `Drafts & Working Notes` — `Private & Shared/Autopilot Hub/IFNS – UI Master/Drafts & Working Notes 2afb22c770d981e5805fe96d174eebe6.md`
- `IFNS – Notion Page Index` — `Private & Shared/Autopilot Hub/IFNS – UI Master/IFNS – Notion Page Index 2afb22c770d98001a463e236a576a5c3.md`
- `Step 01 – Preface Integration` — `Private & Shared/Autopilot Hub/IFNS – UI Master/Step 01 – Preface Integration 2adb22c770d98068a351dc6f69822f3b.md`
- `Step 02 – Executive Summary` — `Private & Shared/Autopilot Hub/IFNS – UI Master/Step 02 – Executive Summary 2adb22c770d98037a4a0c184f917d64d.md`
- `Step 03 – Visionary–Technical Overview` — `Private & Shared/Autopilot Hub/IFNS – UI Master/Step 03 – Visionary–Technical Overview 2adb22c770d98074b9e8f2083a4788f4.md`
- `Step 04 – Preface Timeline` — `Private & Shared/Autopilot Hub/IFNS – UI Master/Step 04 – Preface Timeline 2adb22c770d980118757c73286ae8eee.md`

Treat these V1 pages under the following principles:

1. **Do not delete** any V1 pages.

2. Each V1 page should be mapped to:

   - One **Step hub** (primary step), and

   - Zero or more **V2 spec cards** / databases it conceptually belongs to.

3. New work should **not** modify V1 text heavily; instead:

   - If the content is still current, *pull it forward* into the relevant Step hub or spec card.

   - Mark the V1 page header with a short note: `Status: Historical – content reflected in Step 0X / V2`.


### 3.1 Specific V1 pages and suggested roles

- `00 – Index` and `IFNS – Notion Page Index`

  - Keep as **historical index pages**.

  - Add a note pointing to the new Phase 0 inventory and to the 14-step index as the current navigation.

- `01 – Summary`

  - Treat as an **early executive summary**.

  - Copy any still-relevant phrases into `Step 02 – Executive Summary` → `Narrative & Intent`, then mark V1 page as historical.

- `02 – Drafts & Working Notes` and `Drafts & Working Notes`

  - Leave as is; they are pure historical working notes.

  - Link them from a single `Historical drafts` section under `Step 03 – Visionary–Technical Overview` if desired.

- `Core ML Build Stages`

  - Cross-link it with the **Core ML Build** V2 page and the Step 03 hub.

  - Do not override it; instead, treat it as an earlier view on the same lifecycle.


## 4. Rules for creating new content going forward

When you or another agent creates new pages in Notion, use these rules to avoid fragmentation:

1. **Always start from a Step hub or an existing DB.**

   - If content is conceptual and belongs to a given stage → create a child page under that **Step hub**.

   - If content describes rows of data (indicators, telemetry, gaps, runs) → add it as a **row** in the relevant DB.

2. **Name pages with a clear prefix:**

   - `Spec – …` for spec cards.

   - `Runbook – …` for how-to / operational checklists.

   - `Draft – …` for experimental ideas.

3. **Update Notion first, then Git.**

   - When changing a schema, field, or logic, update the Notion spec (and DB property descriptions) first.

   - Only then regenerate/export CSV/JSON/YAML for Git.

4. **Keep “Source of truth” phrases consistent.**

   - Inside spec pages, write: `Source of truth is this Notion page + linked database`.
   - Avoid `Source of truth is this file in Git` going forward.


## 5. SoT checks & QA process

To keep the workspace coherent over time, define a simple QA loop:

1. **Monthly SoT review** (lightweight):

   - Pick 3–5 random features from the **Feature Catalog**.

   - For each feature, check:

     - Does its Notion spec match the CSV / manifest in Git?

     - Is it referenced correctly from the relevant Step hub(s)?

2. **Change log discipline:**

   - Use the existing `Change Log (V1 → V2 deltas)` page under IFNS – UI Master (V2).

   - Add entries whenever a Step hub, core DB schema, or major spec is changed.

3. **Runtime-to-Notion feedback:**

   - When runtime behavior (harness, mirror, execution engine) reveals a necessary change in indicators, telemetry, or risk logic:

     - Add a row to a `Runtime Findings` DB (future), and

     - Update the relevant Notion spec and Step hub to reflect the new understanding.


## 6. Handover summary for the next agent

When a new agent takes over the IFNS Notion workspace, they should:

1. Read the following handover `.md` files in order:

   - `Phase_0_Autopilot_Hub_Inventory.md`

   - `Phase_1_IFNS_14-Step_Spine_and_Hub_Structure.md`

   - `Phase_2_Attach_UI_Master_V2_to_14-Step_Spine.md`

   - `Phase_3_Telemetry_QC_Runtime_and_Calendar_Wiring.md`

   - `Phase_4_Catalog_and_Feature_Universe_Surfaces.md`

   - This file: `Phase_5_Living_SoT_Rules_and_V1_Crosswalk.md`

2. Open Notion and verify that:

   - The 14 Step hubs exist and are wired to the right V2 spec cards.

   - `Feature Catalog`, `QCWeekly`, and `CalendarGaps2025` DBs exist with the described schemas.

   - Telemetry/runtime views are embedded into the appropriate Step hubs.

3. Treat `IFNS – UI Master` (V1) as historical but **extremely valuable context**:

   - Use it to understand the evolution of the system.

   - When in doubt, default to the 14-step spine and the DB-backed views as the current SoT.

4. Remember the core rule:

   - **Notion is the primary SoT; Git mirrors it; runtime reflects it.**
