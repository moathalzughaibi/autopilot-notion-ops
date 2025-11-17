# Step 03 – Visionary–Technical Overview: From System to Experience

## 01 – Narrative & Intent

This step explains how IFNS is designed to be experienced, not just operated. It connects the conceptual architecture of an “intelligent financial nerve system” to the actual surfaces where humans will see, steer, and govern it. In other words, it describes the bridge **from system to experience (SxE)** and defines the roles of the main experience layers: Mirror, Admin, and the underlying telemetry and registry fabric.

At the highest level, IFNS is not a collection of disconnected tools. It is a **single, coherent organism** whose internal activity is exposed through a small number of carefully designed experiences:

- **Mirror** – the awareness surface: how the system “looks at itself” and how operators see health, context, risk, and performance at a glance.
- **Admin** – the control and governance surface: how policies, models, risk envelopes, and operational toggles are configured, approved, and audited.
- **Harness & Telemetry** – the measurement and narrative surface: how simulations, paper runs, live sessions, and incidents are captured as a continuous event stream and turned into structured evidence.

This step clarifies the intent and responsibilities of each surface and defines how they work together so that the entire system feels like a **single integrated experience**, even though it rests on many technical components.

### 1. System-to-Experience (SxE) as a First-Class Layer

IFNS introduces SxE as an explicit architectural layer, not an afterthought. SxE is the contract between:

- The **Core ML engine** (data, features, models, backtests, risk logic, execution), and  
- The **operator experiences** (Mirror, Admin, consoles, reports).

The purpose of SxE is to ensure that every important internal object—datasets, models, backtests, KPIs, risk envelopes, sessions, incidents—has:

1. A **clear data contract** (what fields exist, how they are named, how they are versioned).
2. A **UX representation** (how it is visualized, summarized, and interacted with).
3. A **governance path** (who can change it, under what conditions, with what audit trail).

In practical terms, SxE is realized via:

- A set of **registry and telemetry JSON files** (and equivalent tables in Excel/CSV) that encode the state of important objects.
- A **Mirror UI** that reads from those registries and telemetry streams and presents them as dashboards, status cards, and drill-down views.
- An **Admin UI** that uses the same contracts to expose safe, controlled configuration and governance workflows.

This step sets the expectation that any new capability in IFNS must define both its **internal behavior** and its **SxE representation** as part of its design.

### 2. Mirror – Awareness as a Primary Product

Mirror is the main execution-facing and risk-facing surface for IFNS. Its purpose is to turn the system’s internal complexity into **clear, actionable awareness**.

Key principles:

- Mirror is not a collection of raw charts; it is a **story of the system’s state**, broken into cards and views that answer specific questions:
  - What is IFNS doing right now?
  - Is it safe?
  - Where is performance coming from?
  - What has changed since yesterday?
- Mirror consumes **KPIs and status flags** derived from:
  - Backtest metrics and live performance,
  - MSI context states and DRA outcomes,
  - Risk envelope state, kill switch status, cooldowns,
  - Paper and live session telemetry,
  - Incident logs and reasoning reports.

Concrete roles of Mirror:

- Present a **“Current Posture”** view (risk, capital usage, key models’ states, MSI context).
- Present **“Performance & Learning”** views (backtest summaries, paper/live session KPIs, promotion/rollback events).
- Present **“Safety & Incidents”** views (risk limits, breaches, kill switch activations, ongoing investigations).

This step’s intent is not to design pixel-perfect layouts, but to fix the concept that **Mirror is the awareness mirror** of IFNS: it must always reflect the true state of the system in a way that supports timely human judgment.

### 3. Admin – Control, Policy, and Governance

Admin is the second major experience surface. While Mirror is optimized for awareness and monitoring, Admin is optimized for **configuration, governance, and controlled change**.

Admin’s responsibilities include:

- Exposing **read/write views** over key registries and policy tables, such as:
  - Model Registry and model statuses (draft, baseline, canary, promoted, deprecated).
  - Risk Envelope definitions and overrides.
  - Promotion and rollback rules.
  - MSI context state definitions and DRA decision tables.
  - Capital allocation plans and environment/lanes configuration.
- Providing **safe workflows** for changes:
  - Who can propose a change to a risk limit, promotion rule, or capital slice?
  - Who must approve it?
  - What evidence (backtests, paper runs, incidents) must be attached?
- Maintaining a **Change Log**:
  - Every impactful change (models, policies, envelopes, routing) is recorded with timestamps, authors, approvers, and scope.

Admin is also where IFNS’s “no-code” control vision is realized: non-coding operators should be able to **adjust policies and thresholds** within well-defined bounds, while the system guarantees consistency with the underlying JSON/Excel contracts.

The intent of this step is to ensure that **every technical parameter with real-world consequences has a visible, auditable home** in Admin, and to prevent hidden, code-only behavior from governing the system.

### 4. Telemetry, Registries, and Narrative

The third pillar of SxE is the **telemetry and registry layer**—the connective tissue that feeds Mirror and Admin with trustworthy, structured data.

This layer provides:

- **Registries** – relatively slow-changing objects:
  - `model_registry` (models and their metadata),
  - `backtests_index` (backtest runs and metrics),
  - `paper_sessions` and `live_sessions` (session-level history),
  - `ml_policies` and `risk_envelope` (policy state).
- **Telemetry streams** – high-frequency or event-based data:
  - Orders, fills, P&L updates,
  - MSI context transitions,
  - DRA decisions and gate outcomes,
  - Incidents, kill switch activations, cooldown changes,
  - Reasoning reports and narrative AI summaries.

From a system-to-experience perspective, the intent is:

- Every significant event in IFNS should be **emit-only once**, into the telemetry stream, with a well-defined schema.
- Mirror and Admin should then **consume and aggregate** these events into their views, rather than inventing parallel data models.
- Narrative and explanation (for example, why a model was promoted or why a kill switch fired) should be rooted in these events, so that a human can reconstruct “what happened and why” from the same sources the system uses.

This step anchors the idea that **data contracts and event schemas are part of the UX design**, not just an implementation detail.

### 5. End-to-End Experience Loop

Finally, this step defines SxE as a closed loop:

1. The Core ML engine ingests data, trains models, and produces decisions and performance metrics.
2. Registries and telemetry capture those artifacts and events in structured form.
3. Mirror reads that structure to present awareness; Admin reads it to expose policies and controls.
4. Humans observe, evaluate, and adjust policies, thresholds, or capital allocations through Admin.
5. Those changes are written back into registries and configs, which in turn shape future behavior of the Core ML engine.

The intent is that **no part of IFNS is “off the grid”**: what the system does, what it believes, and what it is allowed to do must all be visible and governable through this loop.

Step 03 therefore acts as the conceptual anchor for everything that follows: every Core ML Stage (data, models, backtests, risk, paper, live) must define **not only its internal mechanics but also its SxE exposure** through Mirror, Admin, and telemetry.

---

## 02 – Implementation Reference

The implementation-level behavior that realizes this Visionary–Technical Overview is defined in the **IFNS – Core ML Build Specification** as follows:

- **Section 0 – Document Overview**  
  Defines the overall purpose, scope, and artifact set of the Core ML build, including how SxE, Admin, Mirror, and telemetry are treated as first-class citizens in the architecture.

- **Stage 1 – Foundations & Architecture**  
  Specifies the directory layout, `core_ml_config` schema, and integration paths for SxE-facing JSON files (such as `model_registry.json`, `backtests_index.json`, `ml_policies.json`, and the main registry consumed by Mirror and Admin).

- **Stage 4 – Backtesting & Evaluation**  
  Defines the Signal API and backtest index that feed performance and evaluation KPIs into Mirror and Admin.

- **Stage 5 – Risk, Execution & SxE Link**  
  Provides the MSI context states, DRA execution decision tables, promotion/rollback rules, risk envelopes, kill switch logic, cooldown rules, and the specific way these are surfaced into Mirror and Admin (including the Event Ledger).

- **Stages 6 & 7 – Paper Trading and Live Trading & Operations**  
  Describe how paper and live sessions are modeled, logged, and exposed in SxE via KPIs, incidents, and governance records (sessions indices, incident types, and the Change Log).

In practice, any new IFNS feature that touches SxE must:

1. Declare its **data contracts and telemetry events** in the schemas and tables defined in the Core ML Build Specification.
2. Declare its **Mirror representation** (which KPIs, cards, or dashboards it affects).
3. Declare its **Admin representation** (which registry entries, policies, or workflows it adds or modifies).

This ensures that the Visionary–Technical “from system to experience” principles in Step 03 are consistently implemented throughout all Core ML stages.

---

## 03 – Notes & Decisions

- Initial version of this step was translated from the original IFNS_Integrated “Step 3 – Visionary–Technical Overview: From System to Experience” into Git-backed Markdown with explicit SxE responsibilities for Mirror, Admin, and telemetry.
- The SxE concepts defined here are **normative**: new capabilities in IFNS should always describe both their internal behavior and their SxE footprint.
- Future refinement: once the SxE wireframes and UI matrices are fully finalized in the Admin & UI Matrix workbook, this step should be updated to reference the exact UI packs and screens (e.g., Mirror awareness packs, Admin policy consoles) by name.
