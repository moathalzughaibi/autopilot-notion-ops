# Stage 04 – Backtesting & Evaluation

## 01 – Narrative & Intent

This document defines **Stage 04 – Backtesting & Evaluation** for the Intelligent Financial Neural System (IFNS).

Conceptually, this stage **implements the evaluation harness** described across:

- Step 08 – Modeling Intelligence (MI) – how models are exercised in historical contexts.
- Step 09 – Execution Intelligence (EI) – simulation of execution and costs.
- Step 11 – Model & Signal Integration (MSI) – integration patterns tested offline.
- Step 12 – Decision & Risk Architecture (DRA) – risk envelopes and gates simulated offline.
- Step 13 – Self-Evaluation & Learning (SEL) – backtest evidence as primary learning input.

Stage 04 answers:

- How do we **exercise models and strategies on historical data** in a realistic way?
- What are the **contracts** between the backtest harness, data (Stage 02), models (Stage 03), MSI, and DRA?
- Which **metrics and outputs** are produced (TE, slippage, drawdowns, incident-like events)?
- How are backtests **indexed, stored, and surfaced** to SxE and SEL?

The outcome of Stage 04 is a **disciplined backtesting environment** that generates trustworthy evidence for:

- Strategy design,
- Model selection and promotion,
- Risk envelope design,
- Execution and cost modeling.

---

## 02 – Scope & Responsibilities

Stage 04 covers:

1. **Backtest Harness Design**
   - Core interfaces and components.
   - Relationship to Signal API, MSI, and DRA.

2. **Scenario & Run Definitions**
   - How we define what a backtest is (universe, period, config).
   - Types of scenarios (baseline, stress, ablation, etc.).

3. **Execution Simulation**
   - Fill and cost models (VWAP, arrival, slippage logic).
   - Route-level simulation where applicable.

4. **Metrics & Outputs**
   - Per-order and per-trade records.
   - Daily/period summary metrics.
   - Strategy- and model-level performance statistics.
   - TE, slippage, drawdowns, risk envelope breaches.

5. **Backtests Index & Artifacts**
   - How runs are registered and stored.
   - Paths and formats of outputs.

6. **SxE Representation**
   - Mirror dashboards for backtests.
   - Admin views for configuration and evidence inspection.

Stage 04 does **not** execute live trades or manage real-time behavior; that’s Stage 06 (paper) and Stage 07 (live).  
It focuses strictly on **historical simulations** and **offline evaluation**.

---

## 03 – Backtest Harness Design

### 3.1 Core Components

The **Backtest Harness** lives under:

```text
pipelines/backtesting/
tools/harness/
```

Key logical components:

- **Data Adapter**
  - Reads historical datasets from Stage 02:
    - Price/volume tables,
    - Feature tables,
    - Label tables,
    - Dataset IDs (e.g., `DS_BACKTEST_CORE_V1`).
  - Provides time-stepped access (bar by bar, or event by event).

- **Signal Adapter**
  - Calls Model Service (Stage 03) and MSI logic (Stage 05 spec) in an **offline mode**:
    - For each time step, obtains model signals or MSI proposals.
  - May apply:
    - Fixed integration policies (mirror of current MSI policies),
    - Experimental policies (for scenario analysis).

- **Decision & Risk Adapter**
  - Optional integration with DRA logic in simulation mode:
    - Applies risk envelopes and gates as if in real time.
    - Produces allow/reduce/deny decisions for proposed trades.

- **Execution Simulator**
  - Receives orders from MSI/DRA decisions.
  - Simulates fills and costs:
    - VWAP, arrival price, slippage in bps,
    - Partial fills and failures depending on liquidity assumptions.

- **Metrics & Telemetry Collector**
  - Aggregates events:
    - Orders, fills, P&L, risk metrics, envelope breaches.
  - Writes outputs to:
    - Per-order CSV/Parquet,
    - Per-run NDJSON,
    - Summary metrics tables.

### 3.2 Signal & Decision Flow

Within each backtest, at each time step:

1. Data Adapter loads current bar/features for the universe.
2. Signal Adapter calls model(s) / MSI to produce **decision proposals**.
3. DRA-sim layer (optional) evaluates proposals under simulated risk envelopes.
4. Execution Simulator applies allowed decisions and generates fills.
5. Metrics Collector updates P&L, TE, slippage, exposures, and risk states.

This reproduces as much of the **live decision chain** as possible, without the operational complexity of Stage 07.

---

## 04 – Scenario & Run Definitions

### 4.1 Scenario Definitions

A **backtest scenario** defines:

- Universe:
  - Symbols, markets, sectors.
- Time period:
  - Start and end timestamps.
- Strategy configuration:
  - Which model families,
  - Which MSI and DRA policies,
  - Which execution styles.
- Data configuration:
  - Dataset ID(s),
  - Feature & label versions.
- Initial capital and constraints:
  - Capital allocation,
  - Leverage rules,
  - Risk envelope presets.

Scenario definitions live under:

```text
config/backtests/
  scenario_<name>.yaml
```

Each scenario gets a **scenario_id**.

### 4.2 Runs

A **backtest run** is a concrete execution of a scenario, possibly with parameter overrides.

Run metadata includes:

- `run_id`,
- `scenario_id`,
- Timestamp,
- Git commit / code version,
- Parameter overrides (if any),
- Notes.

Each run is recorded in the **Backtests Index** (Section 07).

---

## 05 – Execution Simulation

Execution simulation lives under:

```text
pipelines/execution_sim/
```

### 5.1 Fill Models

Stage 04 defines logical fill models, for example:

- **Midpoint model**:
  - Fill at mid-price (`(bid+ask)/2`) with configurable noise/slippage.
- **VWAP model**:
  - Approximate VWAP over the bar or session given known volume.
- **Liquidity-aware model**:
  - Limit fills to a fraction of bar volume,
  - Increase slippage when participation is high.

Which fill model is used is controlled by:

- Backtest scenario config,
- Default Parameters Registry (e.g., `harness.route.default`).

### 5.2 Slippage & Transaction Costs

The simulator computes:

- **Slippage**:
  - `slippage_bps = (fill_price - arrival_mid) / arrival_mid * 10,000` (with sign convention).
- **Transaction costs**:
  - Commissions and fees,
  - Optional taxes or venue-specific costs.

These metrics are:

- Stored per order/trade,
- Aggregated into per-run and per-day summaries.

### 5.3 Failure & Rejection Modeling

Backtests may also model:

- Order rejections (e.g., due to size limits),
- Partial fills,
- Latency impacts (delayed fills).

These elements are optional at first but should be **extensible**.

---

## 06 – Metrics & Outputs

Stage 04 standardizes outputs so that SEL and SxE can rely on them.

### 6.1 Per-Order / Per-Trade Records

Per-order outputs (e.g., CSV/Parquet) include:

- `run_id`, `ts`, `symbol`,
- `order_id`, `side` (buy/sell),
- `quantity`, `notional`,
- `arrival_mid`, `fill_price`,
- `slippage_bps`,
- `route` or execution style,
- Any DRA flags (e.g., reduced size due to risk).

Per-trade or position-level aggregations can be derived or stored separately.

### 6.2 Daily & Run-Level Summaries

Run-level summaries can be stored as NDJSON, e.g.:

```text
data/registry/backtests_summary.ndjson
```

Each record may include:

- `run_id`, `scenario_id`,
- P&L (total, per-day statistics),
- TE (tracking error vs. benchmark),
- Slippage: p50/p95 in bps,
- Hit rate,
- Max drawdown,
- Volatility of returns,
- Breach counts:
  - Risk envelope breaches,
  - Constraint violations.

These summary metrics are:

- Used by SEL for model and strategy evaluation,
- Used by DRA to calibrate envelopes and promotion thresholds.

### 6.3 Incident-Like Events

Simulated incidents may be emitted in telemetry, e.g.:

- Excessive drawdown in a single day,
- Repeated envelope breaches,
- Execution anomalies (e.g., extreme slippage).

These are not real incidents, but **incident-like events** stored for analysis and testing runbooks.

---

## 07 – Backtests Index & Artifacts

The **Backtests Index** lives under:

```text
data/registry/backtests_index.json
```

(or NDJSON/CSV equivalent).

Each entry contains:

- `run_id`,
- `scenario_id`,
- Start/end timestamps,
- Strategies and model families used,
- Code version,
- Pointers to:
  - Per-order file(s),
  - Summary metrics record,
  - Logs and telemetry streams.

The index is:

- The canonical list of all backtests,
- The main entry point for Mirror and Admin to navigate historical runs.

Backtest artifacts live under a structured path, such as:

```text
data/backtests/
  <run_id>/
    orders.parquet
    summary.json
    telemetry_events.ndjson
    config_snapshot.json
```

This keeps each run **self-contained** and easy to archive or reproduce.

---

## 08 – SxE Representation of Stage 04

### 8.1 Mirror (Read-Focused)

Mirror surfaces:

- **Backtests Overview**
  - List of recent runs with key metrics (P&L, TE, slippage, max DD).
  - Filters by scenario, strategy, model family, regime.

- **Run Drill-Down**
  - Time-series charts of equity curves and drawdowns.
  - Slippage distributions.
  - TE vs. benchmark over time.

- **Scenario Comparison**
  - Compare multiple scenarios/runs for:
    - Different models,
    - Different policies,
    - Different execution styles.

These views help quants and stakeholders understand **how strategies behave historically**.

### 8.2 Admin (Control-Focused)

Admin surfaces:

- **Backtest Config Console**
  - View and edit scenario definitions (under governance).
  - Select models, strategies, datasets, and policies for new runs.

- **Run Management Console**
  - Tag runs as:
    - Evidence for promotion,
    - Evidence against a configuration,
    - Obsolete or superseded.
  - Link runs to:
    - Model Registry entries,
    - DRA envelope changes,
    - SEL recommendations.

Stage 04 itself does not decide promotions; it provides the **sandbox and evidence** used by DRA/SEL.

---

## 09 – Governance, Reproducibility & SEL Integration

Stage 04 includes rules to keep backtesting **honest and reproducible**:

- Every `run_id`:
  - Must be linked to a `scenario_id`.
  - Must have a config snapshot (datasets, models, policies).
  - Must record code version (Git commit or equivalent).

- Scenario definitions:
  - Should be version-controlled.
  - Should distinguish between:
    - Baseline runs,
    - Experiments,
    - Sanity checks.

- SEL integration:
  - SEL uses Backtests Index, summaries, and incident-like events:
    - To identify robust configurations,
    - To highlight fragility across regimes,
    - To propose promotions, rollbacks, or policy changes.

Stage 04 is thus the primary **offline evidence engine** for the system.

---

## 10 – Notes & Decisions

- Backtesting must be as close as practical to real-world conditions without being fully live:
  - Same data contracts,
  - Same MSI and DRA logic (where feasible),
  - Realistic execution modeling.

- At the same time, backtesting must be:
  - **Fast enough** for research,
  - **Configurable enough** for scenario analysis.

- Stage 04 does not mandate specific metrics (Sharpe, Sortino, etc.) exhaustively; instead, it defines:
  - A **baseline set** (P&L, drawdown, slippage, TE, hit rate),
  - Hooks for extending metrics per strategy or asset class.

- Any change to the backtest harness that affects decision logic or metrics should:
  - Be versioned and noted in the Backtests Index and Change Log,
  - Be communicated to SEL and DRA stakeholders.

With Stage 04 in place, IFNS has a **coherent historical evaluation engine** that drives model and policy decisions in a transparent, evidential way.
