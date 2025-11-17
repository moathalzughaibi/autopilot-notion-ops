# Step 06 – Section 2.0: System Architecture

## 01 – Narrative & Intent

This step defines the **System Architecture** of IFNS: the concrete way the intelligence layers, environments, data flows, and SxE surfaces are wired together into a single operational system.

Where Step 05 (Operational Genesis Framework) described *what* IFNS is and *which roles* it plays, this step describes **how those roles are realized in structure**:

- Which components exist and what responsibilities they carry.
- How data and decisions flow between them.
- How environments (`offline`, `paper`, `live`) are separated and connected.
- How SxE (Mirror and Admin) plug into the architecture without breaking safety or integrity.

The intent is to provide a **clear, implementation-oriented mental model** that can be translated into repositories, services, configurations, and deployment topologies.

### 1. High-Level Architectural View

At the highest level, IFNS is structured as a **layered nervous system**:

1. **Data & Features (DIL)** – ingest, cleanse, align, and encode data into machine-ready features.
2. **Core ML Engine (MI + MSA)** – train and run models, including structure-aware models, to produce predictions and structural interpretations.
3. **Execution & Risk (EI + MSI + DRA)** – transform signals into orders and positions under explicit risk and decision policies.
4. **Operations & Environments (Paper & Live)** – run the system in `offline`, `paper`, and `live` modes, with clear boundaries and deployment lanes.
5. **System-to-Experience (SxE)** – expose the system’s state and controls through Mirror, Admin, and telemetry/registry contracts.

These layers are connected through **well-defined contracts**:

- Data schemas (tables, Parquet, CSV).
- Model interfaces and Signal APIs.
- Backtest and session artifacts.
- Policy and registry JSON files.
- Telemetry event schemas.

The architecture is deliberately designed so that each layer can evolve **independently but coherently**, as long as it respects the contracts it shares with neighboring layers.

### 2. Core Components and Their Responsibilities

The System Architecture defines a small set of named components. Each has a clear job and a constrained interface:

1. **Ingestion & DIL Pipelines**
   - Pull raw data (prices, volumes, corporate actions, news-derived features, etc.) from providers.
   - Normalize timestamps, symbols, and calendars.
   - Write canonical price and feature tables that conform to the DIL schemas.

2. **Core ML Engine**
   - Owns the **feature frameworks**, **labeling policies**, and **training pipelines**.
   - Maintains the **Model Registry** and model artifacts (weights, configs, metrics).
   - Exposes a **Signal API** used by backtests, the Harness, paper, and live execution.

3. **Harness (Backtesting & Simulation)**
   - Consumes the Signal API and historical data to simulate strategy behavior.
   - Produces backtest P&L, risk metrics, and gate-level summaries.
   - Writes results into the **Backtests Index** and related artifacts.

4. **Execution Engine & Brokers**
   - In **paper mode**, connects to a **Paper Broker** that simulates orders against live or historical prices.
   - In **live mode**, connects to one or more **Live Brokers** via well-defined adapters.
   - Applies MSI and DRA policies (context, risk, promotion state) to decide whether/how to execute each action.

5. **Telemetry Adapter & Event Store**
   - Receives events from the Core ML engine, Harness, and execution components.
   - Normalizes them to the **IFNS telemetry schema**.
   - Writes them to NDJSON or similar event streams for Mirror, Admin, and analytics.

6. **SxE Surfaces: Mirror & Admin**
   - **Mirror** reads KPIs, registries, and telemetry to present awareness (health, posture, performance, incidents).
   - **Admin** reads and writes policy and registry JSONs within controlled workflows (approvals, change logs).

7. **Governance & Runbooks**
   - Encodes incident types, operational runbooks, and change procedures.
   - Ensures that critical actions (promotions, rollbacks, risk limit changes) are logged and recoverable.

Each of these components maps directly to directories, services, or configuration groups in the Core ML build.

### 3. Environments and Deployment Lanes

The architecture is **environment-aware**. Every component operates in one of three environments:

- **Offline**
  - Used for research, historical backtesting, and experimentation.
  - No live or paper brokers are involved.
  - Telemetry is written to offline logs for later analysis.

- **Paper**
  - Used for real-time behavior in a **capital-free** setting.
  - Paper Broker accepts orders and generates simulated fills against streaming prices.
  - Telemetry and KPIs mirror what would happen in live trading, but with no financial exposure.

- **Live**
  - Used for real capital in production.
  - Live Broker adapters route orders to real venues.
  - Incident handling, risk envelopes, and capital allocation plans are fully enforced.

**Deployment lanes** define allowed transitions between environments, for example:

- `offline → paper_canary → paper_promoted`
- `paper_promoted → live_canary → live_promoted`

The System Architecture ensures that:

- Configuration, telemetry, and policies are **environment-scoped** (e.g., different risk limits in paper vs. live).
- SxE clearly shows which environment the system is in and what lane transitions are possible or pending.
- All environment transitions are logged in the **Change Log**.

### 4. Data and Decision Flow

From a flow perspective, the architecture can be viewed as a pipeline of **data → features → models → decisions → actions → telemetry**:

1. **Data Flow**
   - Provider → Ingestion → Canonical price/feature tables (DIL).
   - Outputs are versioned and annotated with quality/coverage metadata.

2. **Model Flow**
   - Features + labels → Training pipelines → Model artifacts + metrics.
   - Models registered in the Model Registry with status (`draft`, `baseline`, `canary`, `promoted`).

3. **Signal Flow**
   - Online models receive features and context → produce signals via the Signal API.
   - MSI fuses multiple signals and contexts into a consolidated decision proposal.

4. **Risk & Execution Flow**
   - DRA evaluates each proposal against risk envelopes, capital limits, cooldowns, and kill switch state.
   - Approved actions are sent to paper or live brokers; rejected ones are logged with reasons.

5. **Telemetry & SxE Flow**
   - Telemetry Adapter captures events at each stage: training runs, backtests, orders, fills, incidents, promotions, rollbacks.
   - Mirror aggregates events into dashboards and KPIs.
   - Admin exposes controls and histories over the registries and policies that influenced those events.

This flow is intentionally **unidirectional** at the data/event level: events are written once and consumed by multiple surfaces, avoiding divergent views of reality.

### 5. SxE Integration Points

In this architecture, SxE is not bolted on; it is wired in through **specific integration points**:

- **Registries**
  - `model_registry.json` – central list of models, statuses, and metadata.
  - `backtests_index.json` – catalog of backtests, metrics, and gate outcomes.
  - `paper_sessions.json` and `live_sessions.json` – session histories.
  - `ml_policies.json` – promotion, rollback, and SEL-related policies.
  - `risk_envelope.json`, `kill_switch_spec.json`, `cooldown_spec.json` – risk and control definitions.

- **Telemetry Streams**
  - `events_backtest.ndjson` – backtest-level events.
  - `events_execution.ndjson` – orders, fills, and execution anomalies.
  - `events_risk.ndjson` – risk breaches, kill switch activations, cooldown events.
  - `events_sel.ndjson` – promotions, rollbacks, retraining, and learning decisions.

- **UI Bindings**
  - Mirror dashboards and cards are defined to consume specific registries and event streams.
  - Admin panels are defined to edit specific policies and registry fields under governance rules.

The architecture requires that **every SxE view has a known backend contract** (table or JSON), and every contract has at least one SxE consumer. There are no “orphaned” data structures.

### 6. Modularity and Extensibility

The System Architecture is designed to be **modular and extensible**:

- New data sources can be added by:
  - Extending DIL schemas and ingestion pipelines.
  - Registering new feature frameworks.

- New model families can be introduced by:
  - Extending the Model Registry and training pipelines.
  - Updating MSI and DRA to recognize new roles and signals.

- New markets or strategies can be onboarded by:
  - Creating new capital allocation slices and risk envelopes.
  - Adding routing rules and broker adapters where needed.

Crucially, such extensions must:

1. Respect environment separation (offline/paper/live).
2. Adhere to existing registry and telemetry contracts, or explicitly extend them with versioning.
3. Declare their SxE footprint (Mirror and Admin views) from the beginning.

This keeps the system coherent even as it grows in breadth and sophistication.

---

## 02 – Implementation Reference

The System Architecture described in this step is made concrete in the **IFNS – Core ML Build Specification** primarily through:

- **Stage 1 – Foundations & Architecture**
  - Defines the core repository and directory structure for:
    - Data ingestion and DIL pipelines (`data/`, `features/`, `schemas/`),
    - Core ML engine (`core_ml_engine/`),
    - Harness (`harness/`),
    - Telemetry (`telemetry/`),
    - SxE-related registries (`registries/`, `config/`).
  - Specifies the `core_ml_config` schema, including:
    - Environment modes (`offline`, `paper`, `live`),
    - Pointers to data sources, feature sets, and model registries,
    - References to risk envelopes, promotion/rollback policies, and deployment lanes.
  - Establishes the main JSON and NDJSON files used as SxE integration points.

- **Stage 2 – Data & Feature Pipeline**
  - Provides the concrete schemas and pipelines for DIL, aligning with the architecture’s data and feature flow.

- **Stage 3 – Modeling & Training**
  - Implements the Model Registry, training pipelines, and metrics that occupy the Core ML engine portion of the architecture.

- **Stage 4 – Backtesting & Evaluation**
  - Defines the Harness and Signal API contracts, as well as the Backtests Index and KPI mappings.

- **Stage 5 – Risk, Execution & SxE Link**
  - Encodes MSI context states, DRA decision tables, risk envelopes, kill switch and cooldown specs, and their SxE representations.

- **Stages 6 & 7 – Paper and Live Operations**
  - Implement the environment separation and deployment lanes, including:
    - Paper and live brokers,
    - Session registries,
    - Incident taxonomies,
    - Change Log governance.

When implementing or modifying the system, engineers and operators should:

1. Use this System Architecture step as the **conceptual map**.
2. Use Stage 1 as the **structural blueprint** for where things live in the codebase and configuration.
3. Use Stages 2–7 as the **detailed contracts** that fill this architecture with concrete behavior.

---

## 03 – Notes & Decisions

- This step serves as the **bridge** between conceptual layers (DIL, MI, EI, MSA, MSI, DRA, SEL) and the concrete components (Core ML engine, Harness, brokers, telemetry, SxE surfaces).
- The named components (Core ML engine, Harness, Paper Broker, Live Broker, Telemetry Adapter, Mirror, Admin) should be treated as **canonical terminology** in code, documentation, and UI.
- Any new component introduced in the future should:
  - Declare its role within this architecture,
  - Specify its upstream and downstream contracts,
  - Document its SxE integration points.
- As the deployment topology matures (e.g., microservices vs. monolith, cloud vs. on-prem), this step can be extended with diagrams and environment-specific details while preserving the logical architecture described here.
