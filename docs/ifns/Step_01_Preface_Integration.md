# Step 01  Preface Integration

> Purpose of Step 01: give IFNS a single, coherent front door narrative  
> that links the Visionary story, the Operational 14-step master plan,  
> and the future Awareness Mirror / Admin UI.

---

## 01 – Narrative & Intent

### 1.1 What this step does

- Introduces **IFNS (Intelligent Financial Neural System)** as a living system, not just a tool.
- Connects the **Visionary narrative** (why IFNS exists) with the **Operational blueprint** (how it behaves in practice).
- Sets the mental model for all later steps (DIL, MI, EI, MSI, DRA, SEL, Awareness layers).
- Establishes the idea that the interface is a **Mirror of Financial Awareness**, not a traditional dashboard.

### 1.2 Who this step is for

- Executive / strategic readers who want to understand *what IFNS is* in one place.
- Senior engineers and designers who need a shared big-picture before diving into architecture or UI details.
- Future operators who will use the **Admin Console** and **Awareness Mirror** but are not ML or infra experts.

### 1.3 Key messages (must survive in all versions)

- IFNS is designed as a **neural system** with:
  - **Data Intelligence Layer (DIL)**  sensory cortex (what the system sees and trusts).
  - **Modeling Intelligence (MI)**  cognitive heart (how the system thinks and learns).
  - **Execution Intelligence (EI)**  motor system (how the system acts in markets).
  - **Awareness layers (TAC, MCEE, GMCL, QDA, SEL)**  meta-awareness and self-critique.
- The systems interface (UX) is the *visible reflection* of this inner structure:
  - Admin = control center and safety layer.
  - Awareness Mirror = narrative and visualization of system state.
  - Dashboards = curated windows into behaviour, risk, and learning.
- IFNS must be:
  - **Controllable** (operators can switch modes, adjust policies, and stop it safely).
  - **Explainable** (core decisions can be traced to clear signals, models, and constraints).
  - **Upgradeable** (new models, data feeds, and tactics can be added without chaos).

### 1.4 Success criteria for Step 01

This step is done when:

- A non-technical executive can read this step in Notion and say:
  - I understand what IFNS is supposed to be in my organization.
- Designers and engineers can:
  - Reuse this narrative as the **intro section** in slide decks, docs, and onboarding.
  - Trace every later UI/console element back to concepts introduced here.
- The language here does **not** conflict with:
  - The Integrated IFNS Master document.
  - The Admin & UI Matrix.
  - The operational 14-step master plan.

---

## 02  Implementation Reference

> This section tells engineers / designers **how** this preface is wired into  
> GitHub, Notion, and the future Admin / Awareness Mirror surfaces.

### 2.1 Notion mapping

- Notion location:
  - `Autopilot Hub  IFNS  UI Master  Step 01  Preface Integration`
- Internal subpages under this Step:
  - `01  Narrative & Intent`   This Markdowns 01 section should mirror that content.
  - `02  Implementation Reference`  Mirrors this section (links, mappings, assets).
  - `03  Notes & Decisions`   Mirrors the history of decisions for this Step.

Recommended sync behavior:

- `docs/IFNS_UI_Master_Notion_Snapshot.md`  
  - Describes **overall tree** for IFNS  UI Master.
- `docs/ifns/Step_01_Preface_Integration.md`  
  - Mirrors the **Step 01** content and feeds the `01` and `02` subpages in Notion.

### 2.2 GitHub assets for this step

- **Markdown (this file)**  
  - `docs/ifns/Step_01_Preface_Integration.md`  
  - Acts as the *canonical source* for the Step 01 Notion content.
- **Structure snapshot**  
  - `docs/IFNS_UI_Master_Notion_Snapshot.md`  
  - Confirms that Step 01 exists under IFNS  UI Master and has the standard three children.

Future linkage (to be wired later):

- Admin / UI Matrix:
  - Step 01 will reference the top rows/sections that describe:
    - IFNS as a system-of-systems.
    - The main admin consoles and Awareness Mirror entry points.
- Integrated IFNS document:
  - Step 01 should align with the Preface / Overview segments (no contradictions in naming).

### 2.3 UI / UX implications

Even though Step 01 is just narrative, it has **UI consequences**:

- Landing experience:
  - The Awareness Mirror needs a **first-view narrative** that reflects this step:
    - What is IFNS?  
    - What does this mirror show?  
    - What are the main cores and awareness layers?
- Admin Console:
  - Must expose:
    - A **read-only Preface / Overview panel** based on this step.
    - Tooltips / help text in critical controls that reuse terms defined here
      (e.g., DIL, MI, EI, TAC, SEL).
- Documentation links:
  - The UI should have help icons (e.g., ?) that link back to this Step 01 narrative
    in Notion or a rendered help view.

---

## 03  Notes & Decisions

> This section is the logbook for Step 01. It should stay short but precise.

### 3.1 Initial decisions

- **2025-11-17  Baseline created**
  - Established tri-layer structure for all Steps:
    - `01  Narrative & Intent`
    - `02  Implementation Reference`
    - `03  Notes & Decisions`
  - Defined Step 01 as the *front door narrative* for IFNS:
    - Connects Visionary story, 14-step operational master plan, and Awareness Mirror.
  - Decided that:
    - This file (`Step_01_Preface_Integration.md`) is the canonical source
      for Step 01 content synced into Notion.

### 3.2 Open questions / TODOs

- [ ] Confirm final wording of key IFNS definitions against the latest integrated IFNS document.
- [ ] Link Step 01 explicitly to:
      - The exact sections / anchors in the integrated Word doc.
      - The relevant slices of the Admin & UI Matrix.
- [ ] Decide where the Awareness Mirrors first-view text is sourced from:
      - Directly from this Step 01 spec,
      - Or a derived UI copy file under `content/`.

### 3.3 Future evolution notes

- This step should remain **stable but not frozen**:
  - If later steps (e.g., MSI, DRA, SEL) evolve, we may adjust the narrative here
    so the high-level story stays accurate.
- Major narrative changes should:
  - Be reflected in commit messages.
  - Be recorded as bullet decisions in this `03  Notes & Decisions` section.
