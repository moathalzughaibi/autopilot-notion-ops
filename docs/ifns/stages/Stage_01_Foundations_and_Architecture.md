# Stage 01 – Foundations & Architecture

## 01 – Narrative & Intent

This document defines **Stage 01 – Foundations & Architecture** for the Intelligent Financial Neural System (IFNS).

Stage 01 is about putting a **solid, opinionated skeleton** under the rest of the build:

- Repository layout and naming.
- Environment model (`offline`, `paper`, `live`) and lanes.
- Core configuration contracts and parameter registries.
- Core services and adapters (data, models, brokers, telemetry).
- High-level SxE bindings (what Mirror/Admin “see” from the foundation).

It does **not** go deep into data schemas (Stage 02), modeling (Stage 03), backtesting (Stage 04), or risk/execution (Stage 05).  
Instead, Stage 01 acts as the **ground floor** that all those stages stand on.

If Stage 05–07 are the “nervous system” and “organs”, Stage 01 is the **skeleton and wiring closet**.

---

## 02 – Core Concepts & Scope

Stage 01 covers the following concepts:

1. **Environment Model**
   - Three primary environments:
     - `offline` – historical data and backtests, no real-time.
     - `paper` – real-time but simulated capital and fills.
     - `live` – real-time with real capital and venues.
   - Within `paper` and `live`, multiple **lanes**:
     - Example: `paper_research`, `paper_gatecheck`, `live_canary`, `live_promoted`.

2. **Core Services & Adapters**
   - Data access layer (reading canonical datasets and views).
   - Model execution layer (running MI models consistently across environments).
   - Execution adapters:
     - Paper Broker adapter,
     - Live Broker adapters.
   - Telemetry adapter:
     - Emitting NDJSON events into telemetry streams.

3. **Configuration System**
   - Hierarchical configuration (global → stage-level → strategy-level).
   - Environment-aware overrides (e.g., stricter limits in live).
   - Integration with the **Default Parameters Registry** (admin-editable parameters).

4. **Repository Layout**
   - Standardized folder and file naming for:
     - Specs (docs),
     - Pipelines (data, models, backtests),
     - Config (YAML/JSON),
     - Telemetry schemas.

5. **SxE Foundation**
   - Common registry and telemetry structures that Mirror/Admin will build on:
     - Sessions (backtest, paper, live),
     - Runs and jobs,
     - Change Log entries.

Stage 01 answers: **“Where does everything live, and how do we wire it cleanly so later stages don’t turn into spaghetti?”**

---

## 03 – Repository Layout & Naming

Stage 01 defines a **canonical repo layout** for the Core ML Build. A typical structure:

```text
repo_root/
  docs/
    ifns/
      Step_01_…md … Step_14_…md
      Stage_00_Document_Overview.md
      Stage_01_Foundations_and_Architecture.md
      Stage_02_Data_and_Feature_Pipeline.md
      …
      Stage_07_Live_Trading_and_Operations.md
      IFNS_UI_Steps_Index.md
      IFNS_UI_Master_Summary.md
      IFNS_UI_Drafts_and_Working_Notes.md

  config/
    core_ml_config.yaml
    environments/
      offline.yaml
      paper.yaml
      live.yaml
    policies/
      risk_envelope.json
      execution_policies.json
      msi_policies.json
      promotion_rules.json

  data/
    raw/
    canonical/
    features/
    labels/
    datasets/
    registry/
      model_registry.json
      backtests_index.json
      paper_sessions.json
      live_sessions.json

  pipelines/
    ingest/
    feature_engineering/
    labeling/
    training/
    backtesting/
    execution_sim/
    paper_trading/
    live_trading/

  telemetry/
    schemas/
      telemetry_schema.json
      events_backtest.schema.json
      events_execution.schema.json
      events_risk.schema.json
      events_sel.schema.json
    sinks/
      (configs for where events are written)

  tools/
    harness/
    admin_utils/
    maintenance/
```

**Naming principles:**

- Use **lower_snake_case** for folders and files, except for Markdown spec titles.
- Keep environment-specific configs under `config/environments/`.
- Keep policy and envelope configs under `config/policies/`.
- Keep runtime registries under `data/registry/`.
- Keep telemetry **schemas** under `telemetry/schemas/`; actual logs live wherever the runtime stores them.

Stage 02–07 documents will reference this layout when they describe where artifacts live.

---

## 04 – Configuration & Default Parameters

Stage 01 standardizes the **configuration system** and tight integration with the **Default Parameters Registry**.

### 4.1 core_ml_config

`core_ml_config.yaml` (or equivalent) is the top-level configuration that:

- Declares:
  - Available environments (`offline`, `paper`, `live`).
  - Available lanes in each environment.
  - Where to find:
    - Data sources (datasets, features, labels),
    - Model registry and artifacts,
    - Backtest harness settings,
    - Risk and execution policies,
    - Telemetry sinks.

- Provides **logical names** for:
  - Strategy bundles,
  - Model families,
  - SxE consoles and dashboards.

Other configs (e.g., `offline.yaml`, `paper.yaml`, `live.yaml`) **inherit from or extend** `core_ml_config` with environment-specific overrides.

### 4.2 Default Parameters Registry

Stage 01 assumes a **central Default Parameters Registry**, maintained outside of code (for example, in a Notion page or a config DB) and mirrored in configuration files for runtime.

Examples (non-exhaustive):

- `mirror.auto_refresh.enabled`
- `mirror.auto_refresh.interval_s`
- `harness.route.default`
- `harness.replay.speed`
- `harness.runs.min_minutes`
- `reports.summary.enabled`

Stage 01 defines the rule:

> **Rule:** Any threshold, limit, timing, or toggle that changes over time should be defined as a **parameter** referenced from the Default Parameters Registry, not hardcoded inside code.

This ensures:

- Operators can adjust behavior centrally via Admin.
- Changes can be tracked and audited.
- System behavior is predictable and versioned.

Later Stages (especially 04–07) will reference these parameters by name.

---

## 05 – Environments & Lanes

Stage 01 formalizes the **environment model** and **lanes**:

### 5.1 Environments

- **offline**
  - Backtests,
  - Historical analysis,
  - Scenario / “what-if” runs.
  - No real-time, no brokers.

- **paper**
  - Real-time data and decisions,
  - Orders routed to a **Paper Broker** that simulates fills,
  - No real capital risk, but realistic constraints.

- **live**
  - Real-time data, decisions, and orders,
  - Orders routed to one or more **Live Brokers**,
  - Full capital and operational risk.

### 5.2 Lanes

Within `paper` and `live`, separate **lanes** are defined to manage progression and isolation, for example:

- `paper_research` – fully experimental, relaxed rules.
- `paper_gatecheck` – closer to live behavior, used for promotion validation.
- `live_canary` – small capital, limited exposure for newly promoted strategies/models.
- `live_promoted` – main production lane with full allocation (within risk envelopes).

The mapping between lanes, risk rules, and promotion logic is defined in Stage 05 (DRA), but Stage 01 ensures:

- Lane names are **standardized**.
- Config files and registries use those names consistently.
- Telemetry and SxE surfaces can group metrics and incidents by lane.

---

## 06 – Core Services & Adapters

Stage 01 identifies core services that later Stages will refine but **must not rename conceptually**:

1. **Data Service**
   - Responsible for providing:
     - Canonical price/volume tables,
     - Features and labels,
     - Training and evaluation datasets.
   - Reads from:
     - `data/canonical/`, `data/features/`, `data/labels/`, `data/datasets/`.
   - Contracts defined in detail in Stage 02.

2. **Model Service**
   - Loads models based on the Model Registry (`data/registry/model_registry.json`).
   - Provides prediction APIs to:
     - Backtest Harness (Stage 04),
     - Paper & Live runtime (Stages 06–07),
     - MSI (Stage 11 spec, Stage 05/03 build).
   - Contracts defined in Stage 03.

3. **Execution Service**
   - Talks to:
     - Paper Broker adapter,
     - Live Broker adapters.
   - Applies execution policies and routes orders.
   - Contracts fleshed out in Stages 04, 05, 06, 07.

4. **Telemetry Service**
   - Emits standardized events to telemetry sinks:
     - `events_backtest.ndjson`,
     - `events_execution.ndjson`,
     - `events_risk.ndjson`,
     - `events_sel.ndjson`, etc.
   - Schemas defined in telemetry folder and refined in Stages 04–07.

Stage 01 does not specify implementation language or framework; it specifies **logical services and their responsibilities**.

---

## 07 – SxE Foundation (Mirror & Admin)

Stage 01 also defines the **base SxE artifacts** that future Stages will build on.

### 7.1 Sessions & Runs

Core tables/JSONs:

- `backtests_index.json`
- `paper_sessions.json`
- `live_sessions.json`

Each record includes:

- `session_id` or `run_id`,
- Environment and lane (`offline` / `paper` / `live`, plus lane),
- Start/end timestamps,
- Strategies and models involved,
- Summary KPIs linked to telemetry.

Mirror uses these for:

- Session/run lists and drill-down views.
- High-level KPIs per session.

Admin uses these for:

- Operational oversight,
- Linking sessions to promotions, rollbacks, or incidents.

### 7.2 Change Log

Stage 01 anchors the concept of a **Change Log**:

- Table or JSON (e.g., `change_log.json`) that records:
  - Config changes,
  - Model promotions/retirements,
  - Policy and envelope updates,
  - Code or deployment versions.

Fields typically include:

- `change_id`,
- `timestamp`,
- `actor` (person or automated process),
- `area` (models, risk, execution, data),
- `description`,
- `linked_evidence` (backtests, paper runs, SEL reports).

Later Stages (especially 05 and 13) will reference the Change Log as part of promotion and governance flows.

---

## 08 – Notes & Decisions

- Stage 01 is **foundational**: it sets names and locations rather than detailed behavior.
- All later Stages (02–07) must:
  - Use the environment model (`offline` / `paper` / `live`, plus lanes) defined here.
  - Respect the idea of a **central Default Parameters Registry**.
  - Use the core folder and registry structure unless there is a strong, documented reason not to.

- Any major deviations from:
  - Environment model,
  - Repository layout,
  - Registry file locations,
  - Telemetry naming
  must be treated as a **spec-level change**, reflected in:
  - This Stage 01 document,
  - The Steps Index,
  - The Drafts & Working Notes log.

- Stage 01 is intentionally **technology-agnostic**:
  - It does not mandate a specific broker API, database, or orchestration system.
  - It focuses instead on contracts and logical structure that can survive tooling changes.

As the system matures, Stage 01 can be extended with:

- More detailed examples of configurations (`core_ml_config` snippets),
- Specific guidelines for repo branching/versioning strategy,
- Links to infrastructure-as-code or deployment manifests where appropriate.
