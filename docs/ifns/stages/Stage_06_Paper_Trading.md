# Stage 06 – Paper Trading

## 01 – Narrative & Intent

This document defines **Stage 06 – Paper Trading** for the Intelligent Financial Neural System (IFNS).

Conceptually, this stage implements the **real-time but capital-safe rehearsal environment** described across:

- Step 09 – Execution Intelligence (EI),
- Step 11 – Model & Signal Integration (MSI),
- Step 12 – Decision & Risk Architecture (DRA),
- Step 13 – Self-Evaluation & Learning (SEL),

using the contracts and policies defined in:

- Stage 01 – Foundations & Architecture,
- Stage 02 – Data & Feature Pipeline,
- Stage 03 – Modeling & Training,
- Stage 04 – Backtesting & Evaluation,
- Stage 05 – Risk, Execution & SxE Link.

Stage 06 answers:

- How do we run IFNS **in real time** with:
  - Live data,
  - Real MSI/DRA decisions,
  - Real EI execution flows,
  - But **simulated capital and fills**?
- How do we define and manage **paper sessions and lanes** (e.g., `paper_research`, `paper_gatecheck`)?
- What telemetry and registries does paper trading produce, and how are they exposed in SxE?
- How does paper trading act as the **bridge** between backtests (Stage 04) and live (Stage 07)?

The outcome of Stage 06 is a **controlled rehearsal environment** where:

- Strategies run as if live,
- Risk and execution logic are exercised under real-time conditions,
- SEL and operators can study behavior **without risking capital**.

---

## 02 – Scope & Responsibilities

Stage 06 covers:

1. **Paper Environment & Lanes**
   - Definition of `paper` environment and standard lanes.
   - Relationship to risk envelopes and MSI/DRA policies.

2. **Paper Broker & Execution Flow**
   - How orders are routed to a Paper Broker.
   - How fills, slippage, and failures are simulated in real time.

3. **Paper Sessions & Registry**
   - How paper runs are defined, started, and tracked.
   - Session metadata and lifecycle states.

4. **Telemetry & Metrics**
   - Events produced by paper runs (orders, fills, risk events, DRA/MSI decisions).
   - Metrics used to compare paper vs. backtest vs. live.

5. **SxE Representation**
   - Mirror dashboards for paper runs and lanes.
   - Admin controls for starting/stopping, gating, and promoting.

Stage 06 does **not** change core MSI/DRA/EI logic; it reuses Stage 05 logic in a **paper environment**.

---

## 03 – Paper Environment & Lanes

### 3.1 Environment Definition

In the environment model (Stage 01), `paper` is a top-level environment:

- Uses **live or near-live data feeds** (same canonical format as Stage 02).
- Uses **current MSI/DRA policies and risk envelopes**, possibly with:
  - More permissive limits,
  - Additional experimentation-enabled toggles.

The goal is to mimic `live` logic as closely as possible, but with:

- No connection to real brokers or capital,
- Explicit labeling as **paper** in all telemetry and registries.

### 3.2 Paper Lanes

Paper lanes are logical sub-environments under `paper`, for example:

- `paper_research`
  - Used for early-stage strategies and models.
  - More experimental settings allowed (e.g., higher candidate turnover).

- `paper_gatecheck`
  - Used for strategies/models considered for promotion.
  - Configuration as close as possible to intended live settings.

Each lane has:

- Its own risk envelopes and capital budgets (simulated),
- Its own promotion rules (e.g., required performance over N days),
- Its own telemetry tags (`env = "paper"`, `lane = "paper_gatecheck"`).

---

## 04 – Paper Broker & Execution Flow

### 4.1 Paper Broker Role

The **Paper Broker** is an execution adapter that:

- Receives orders from EI (using the same order contracts as live),
- Simulates fills according to configurable rules,
- Emits order and fill events to telemetry and registries as if talking to a real broker.

The Paper Broker is configured under:

```text
config/environments/paper.yaml
config/policies/execution_policies.json
config/policies/execution_routes.json
```

It reuses **execution routes** defined in Stage 05 (`route_id`), but maps them to **simulation behaviors** instead of real venues.

### 4.2 Fill & Slippage Models in Paper

Paper fill logic is typically:

- A real-time version of Stage 04 execution simulation, using current live prices and volumes where available.
- Configurable via Default Parameters Registry (e.g., route-specific assumptions).

Key aspects:

- For each incoming order:
  - Determine current `arrival_mid`, `bid`, `ask`, `volume`.
  - Apply route-specific fill rules (VWAP-like, liquidity-aware, etc.).
  - Generate fill events with `fill_price`, `slippage_bps`, `fill_qty`.

- If data is missing or unreliable:
  - Orders may be marked as **simulated failures**,
  - Telemetry should capture these anomalies.

### 4.3 Real-Time Flow

In real time:

1. Data feeds update canonical data and features (Stage 02).
2. MSI (Stage 05) generates decision proposals based on:
   - Current features and regimes,
   - Positions and risk state.
3. DRA (Stage 05) runs gates and determines:
   - ALLOW/REDUCE/DENY,
   - Approved sizes and constraints.
4. EI (Stage 05/09) sends orders to the Paper Broker with:
   - `env = paper`, lane tag, route and policy details.
5. Paper Broker simulates fills and emits events.
6. Positions and exposures in the **paper position registry** are updated.

The same **Signal → MSI → DRA → EI → Broker** chain used in live is exercised, but via Paper Broker.

---

## 05 – Paper Sessions & Registry

### 5.1 Session Definitions

Paper sessions are defined similarly to backtests, but for real time.

A session definition may include:

- `session_id`,
- Environment and lane (`paper_research`, `paper_gatecheck`, etc.),
- Strategy and model configurations (references to Model Registry IDs and MSI/DRA policies),
- Start conditions:
  - Start time,
  - Initialization from a particular portfolio state (e.g., flat, or from backtest end state),
- Target duration or end conditions.

Session definitions can live under:

```text
config/paper_trading/
  session_<name>.yaml
```

### 5.2 Session Registry

The **Paper Sessions Registry** lives under:

```text
data/registry/paper_sessions.json
```

Each entry includes:

- `session_id`,
- `env = "paper"`, `lane`,
- Strategy/portfolio ID(s),
- Start and end timestamps,
- Status (`scheduled`, `running`, `completed`, `aborted`),
- Links to:
  - Telemetry streams,
  - Summary metrics,
  - Incident or anomaly reports,
  - SEL evaluations.

The registry is the **canonical list of paper runs**, used by Mirror/Admin.

### 5.3 Lifecycle & Control

Session lifecycle:

1. **Scheduled** – configuration created and validated.
2. **Running** – MSI/DRA/EI pipeline is active in real time.
3. **Completed** – finished naturally (time or target reached).
4. **Aborted** – stopped manually or by kill switch/cooldown triggers.

Admin consoles can:

- Start/stop sessions (subject to policies),
- Move a session from research lanes to gatecheck lanes (with appropriate checks),
- Tag sessions as promotion evidence or to-be-ignored.

---

## 06 – Telemetry & Metrics

### 6.1 Telemetry Events

Paper runs produce the same **execution and risk telemetry** as in Stage 05, with `env = "paper"` and lane fields.

Common event types:

- `msi_proposal`
- `dra_decision`
- `order_submitted`
- `order_filled`
- `order_rejected`
- `risk_breach`
- `kill_switch_change`
- `cooldown_state_change`
- `paper_session_state_change`

All events are written to telemetry sinks configured for the `paper` environment.

### 6.2 Metrics & Summaries

Paper run summaries are stored similarly to backtests, e.g.:

```text
data/registry/paper_summary.ndjson
```

Metrics per `session_id` include:

- P&L (simulated),
- Slippage distributions (per route, per symbol, per strategy),
- Hit rate and TE vs. benchmarks where applicable,
- Risk envelope usage and breach counts,
- Incident-like events (e.g., extreme simulated slippage, repeated envelope hits).

These metrics are crucial for:

- **Gatecheck decisions** – whether a strategy/model is ready to move closer to live.
- **SEL analyses** – comparing paper vs. backtest behavior.

---

## 07 – Comparison: Backtest vs. Paper vs. Live

Stage 06 explicitly supports **triangulation** between:

- **Backtest** (Stage 04)
  - Fully offline, historical.
  - Controlled data, no real-time constraints.

- **Paper** (Stage 06)
  - Real-time, simulated capital.
  - Same MSI/DRA/EI logic as live (within configuration differences).

- **Live** (Stage 07)
  - Real-time, real capital.
  - Production-grade operating constraints.

Paper occupies the **middle ground**:

- It reveals issues that only show up in real time:
  - Data feed glitches,
  - Latency impacts,
  - Intraday regime shifts.
- It allows tuning of MSI/DRA/EI policies before exposing real capital.

SxE should make these three modes visually and analytically comparable.

---

## 08 – SxE Representation of Stage 06

### 8.1 Mirror – Paper Runs View

Mirror surfaces:

- **Paper Sessions Overview**
  - List of recent and active sessions by lane.
  - Key metrics per session:
    - P&L, slippage, risk usage, TE, major incidents.

- **Session Drill-Down**
  - Time-series charts of P&L and exposures.
  - Event streams (MSI proposals, DRA decisions, orders/fills, risk breaches).
  - Comparison against backtests:
    - How did real-time behavior deviate from historical expectations?

- **Lane Dashboards**
  - Aggregated metrics per lane (`paper_research`, `paper_gatecheck`).
  - Promotion funnel view:
    - How many strategies/models are in each lane?
    - Which ones are approaching promotion criteria?

### 8.2 Admin – Paper Control Panel

Admin surfaces control for:

- **Session Management**
  - Start, pause, resume, stop sessions (under policy).
  - Clone session configs from backtests or other sessions.

- **Lane Policies**
  - Define which strategies/models can run in each lane.
  - Set promotion criteria (e.g., min days, metrics thresholds).

- **Promotion Workflow Hooks**
  - Tag paper sessions as candidates for:
    - MSI model status upgrade,
    - Risk envelope changes,
    - Execution policy adjustments,
    - Progression towards live canary in Stage 07.

Actions in Admin trigger:

- **Change Log entries**,
- Possible **SEL workflows** for recommendation/approval.

---

## 09 – Governance & SEL Integration

Given that paper is a **pre-live safety layer**, governance is important:

- All paper sessions:
  - Must be defined via configuration and registered,
  - Must have clear owners and objectives.

- SEL uses paper data to:
  - Compare real-time vs. historical performance,
  - Evaluate robustness under live-like conditions,
  - Recommend promotions, downgrades, or further experimentation.

- Any transitions:
  - From `paper_research` → `paper_gatecheck`,
  - From `paper_gatecheck` → `live_canary`
  should be:
  - Evidence-driven (backtests + paper results),
  - Logged and reviewable.

Stage 06 is the **primary field laboratory** where ideas make contact with the messy details of real-time behavior.

---

## 10 – Notes & Decisions

- Stage 06 must stay **aligned with Stage 05 contracts**:
  - No special-case execution logic that only exists in paper.
  - Policies and envelopes may be looser, but the structure is the same.

- The Paper Broker is intentionally **not** a toy simulator:
  - It should reuse as much of Stage 04’s execution modeling as possible,
  - It should model realistic limitations so metrics are meaningful.

- SxE views should always make it clear:
  - That results are from the `paper` environment,
  - How they relate to backtests and any live runs.

With Stage 06 in place, IFNS gains a robust **real-time rehearsal stage** that dramatically reduces surprise when moving strategies and models into live capital environments.
