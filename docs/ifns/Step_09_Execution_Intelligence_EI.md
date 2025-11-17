# Step 09 – Section 5.0: Execution Intelligence (EI)

## 01 – Narrative & Intent

This step defines **Execution Intelligence (EI)** — the part of IFNS responsible for turning model outputs and integrated signals into **concrete execution actions**: orders, sizing, routing, and timing decisions, all under explicit risk and policy constraints.

If DIL and MI describe *what we see* and *what we believe*, EI describes **how we act** in the market.

Execution Intelligence answers questions such as:

- *Given this signal and context, should we trade at all?*
- *If yes, how much, through which route, and on what schedule?*
- *How do we balance execution quality, slippage, and market impact against risk envelopes and capital constraints?*

The intent of this step is to:

1. Define the **execution decision chain** from signal to order.
2. Clarify the separation of responsibilities between EI, MSI, and DRA.
3. Specify the key **execution policies, metrics, and telemetry** that make execution behavior visible, tuneable, and governable.

By the end of this step, execution is no longer a black box; it is a structured, policy-driven layer with clear inputs, outputs, and SxE exposure.

---

### 1. Role of EI in the IFNS Stack

Execution Intelligence sits downstream of Modeling Intelligence (MI) and Model & Signal Integration (MSI), and upstream of brokers (paper and live):

- **Inputs**
  - Integrated signals from MSI (e.g., combined directional views, consensus scores, regime-aware adjustments).
  - Context from DIL and MSA (e.g., volatility, liquidity, structure tags).
  - Risk and policy constraints from DRA (e.g., risk envelope, kill switch state, cooldown status, capital allocations).

- **Outputs**
  - Execution decisions (trade vs. no-trade).
  - Orders: side, quantity, price type (market/limit), timing, routing, and any child-order plans.
  - Execution telemetry: fills, slippage, realized TE, and execution exceptions.

EI’s responsibility is to **translate intent into action** while respecting all constraints and providing enough telemetry for post-trade analysis and learning.

---

### 2. Execution Decision Chain

The Execution Intelligence process can be viewed as a decision chain:

1. **Eligibility Check**
   - Verify that:
     - The corresponding model(s) and signals are eligible for execution in the current environment (paper or live).
     - The instrument and venue are currently tradable (session status, halts, circuit breakers).
     - The system is not under a kill switch or relevant cooldown.

2. **Signal-to-Intent Mapping**
   - Convert signals (e.g., probability or expected return) into an **execution intent**:
     - Direction (long/short/flat),
     - Target exposure or position change,
     - Time horizon for the trade.

3. **Sizing & Capital Allocation**
   - Use risk models, volatility estimates, and capital allocation plans to determine:
     - Maximum and target position sizes,
     - Per-order notional caps,
     - Aggregation rules across related symbols/strategies.

4. **Routing & Scheduling**
   - Choose execution style and route:
     - Aggressive vs. passive execution,
     - VWAP/TWAP-style slicing where applicable,
     - Venue or broker preferences.
   - Define order schedules:
     - Immediate-or-cancel vs. time-sliced vs. conditional orders.

5. **Order Emission**
   - Emit orders to the appropriate broker interface:
     - **Paper Broker** in paper environment,
     - **Live Broker(s)** in live environment.
   - Attach identifiers so that fills and events can be traced back to signals and intents.

6. **Feedback & Adjustment**
   - Monitor fills, slippage, and partial executions.
   - Apply adaptive logic within the boundaries defined by DRA and the risk envelope:
     - Adjust price limits or pacing if conditions change.
     - Cancel or reduce orders if risk conditions or signals change materially.

This chain is encoded as a set of **execution policies and algorithms**, rather than ad-hoc logic scattered throughout the system.

---

### 3. Execution Policies and Controls

Execution behavior is governed by a family of **execution policies**. These include:

- **Order Type Policies**
  - Allowed order types by environment, venue, and strategy.
  - Rules for when to use market vs. limit vs. conditional orders.

- **Slippage & Cost Policies**
  - Maximum tolerated slippage (in bps or as TE) for individual orders and aggregated trades.
  - Rules for responding to excessive slippage (e.g., slow down, switch style, halt).

- **Pacing & Participation Policies**
  - Maximum participation rate vs. estimated market volume.
  - Minimum/maximum time windows for execution of large orders.

- **Venue & Route Policies**
  - Preferred venues or brokers for specific instruments or strategies.
  - Fallback routes when preferred venues are unavailable.

- **Environment-Specific Rules**
  - Stricter limits and caps in **paper** vs. **live** may differ (e.g., paper can explore routes but must still respect realistic constraints).
  - Hard caps in live environments tied to the risk envelope and capital allocation plans.

These policies are managed centrally (e.g., in an `execution_policies` table/JSON) and exposed in Admin so operators can understand and adjust them within governance rules.

---

### 4. Execution Metrics and KPIs

To evaluate and tune Execution Intelligence, IFNS tracks a set of **execution metrics** that feed into KPIs in Mirror and Admin.

Key metrics include:

- **Slippage metrics**
  - Per-order and aggregated slippage (bps) vs. arrival mid, decision price, or benchmark.
  - Distribution statistics (p50, p90, p95) by strategy, symbol, venue, and time.

- **Transaction cost & efficiency metrics**
  - Realized transaction cost (fees, spreads, impact estimates).
  - TE (tracking error) vs. intended execution or benchmark profile.

- **Fill quality metrics**
  - Fill rates and times to fill.
  - Partial vs. complete fill statistics.
  - Frequency and reasons for rejections, cancels, and replaces.

- **Pacing and participation metrics**
  - Participation rate vs. market volume.
  - Schedule adherence metrics (e.g., how close execution was to the planned VWAP/TWAP profile).

These metrics are aggregated into **Execution KPIs**, such as:

- Average and worst-case slippage per strategy.
- Percentage of trades within acceptable slippage bands.
- Execution efficiency scores by route/venue.

They are:

- Logged in the Execution Telemetry stream.
- Summarized in daily, weekly, and campaign-level reports.
- Used by SEL and DRA to refine policies, envelopes, and strategy eligibility.

---

### 5. Environment-Aware Execution Behavior

Execution Intelligence behaves differently in `offline`, `paper`, and `live` environments while preserving a consistent logic structure:

- **Offline**
  - Execution behavior is simulated via the Harness using historical data and cost models.
  - Used primarily for understanding execution impacts during backtesting.

- **Paper**
  - Real-time execution against simulated fills from the Paper Broker.
  - Same decision chain and policies as live, but with:
    - No capital risk,
    - Additional logging and experimentation options (within safe bounds).

- **Live**
  - Execution against real venues via Live Brokers.
  - Strict enforcement of:
    - Risk envelopes,
    - Environment-specific caps,
    - Incident handling policies.

Transitions between environments (e.g., from paper to live) are controlled by Stage 7 deployment lanes and DRA rules and are always logged in the Change Log.

---

### 6. SxE Representation of Execution Intelligence

Execution Intelligence has a strong presence in SxE.

- **Mirror (awareness)**
  - Execution dashboards showing:
    - Recent trades, slippage, and TE metrics.
    - Execution quality by strategy, symbol, route, and venue.
  - Alerts for:
    - Slippage or cost breaches,
    - Unusual rejection rates,
    - Pacing or participation anomalies.

- **Admin (control & governance)**
  - **Execution Policy Console**
    - View and adjust (within bounds) execution policies:
      - Order types, slippage limits, pacing parameters, route preferences.
    - Environment-specific overrides (paper vs. live).
  - **Execution Quality Review**
    - Access to daily/weekly reports and ledger of execution decisions.
    - Tools to approve policy adjustments based on evidence.

Both surfaces rely on the same execution telemetry and policy registries, ensuring there is only **one version of the truth** about how execution behaves and why.

---

## 02 – Implementation Reference

Execution Intelligence is implemented and governed across several stages of the **IFNS – Core ML Build Specification**:

- **Stage 4 – Backtesting & Evaluation**
  - Uses the Harness to simulate execution behavior:
    - Applies simple or advanced execution models in backtests,
    - Produces execution metrics (slippage, TE) used as baseline expectations.

- **Stage 5 – Risk, Execution & SxE Link** (EI’s primary implementation stage)
  - Defines the **Execution Policies**:
    - Order types, venues, pacing, slippage limits, participation caps.
  - Encodes the **Execution Decision Chain**:
    - Eligibility checks, signal-to-intent mapping, sizing, routing, scheduling.
  - Specifies the **execution-related registries and contracts**, such as:
    - `execution_policies.json`,
    - `route_profiles.json`,
    - `execution_metrics_spec.json`.
  - Describes how execution metrics and events are emitted into telemetry streams (`events_execution.ndjson`).

- **Stage 6 – Paper Trading**
  - Implements the **Paper Broker**:
    - Applies execution policies in a simulated environment.
    - Generates realistic fills and execution telemetry.
  - Defines paper-specific behavior and caps for experimentation and validation.

- **Stage 7 – Live Trading & Operations**
  - Implements **Live Broker adapters**:
    - Handles real order routing and venue-specific nuances.
  - Formalizes environment-aware limits:
    - Per-strategy and global execution caps,
    - Incident policies for execution failures or anomalies.
  - Integrates execution telemetry with:
    - Incident taxonomy and runbooks,
    - Change Log entries for execution policy changes.

Engineers and operators implementing or modifying Execution Intelligence should:

1. Treat **Stage 5** as the primary specification of execution logic and policies.
2. Use **Stage 4** to validate and tune execution behavior in backtests.
3. Ensure **Stage 6 & 7** implementations faithfully reflect the same decision chain and policies, adjusted only where required by environment or venue constraints.
4. Keep Mirror and Admin views in sync with the policy and telemetry contracts defined here.

---

## 03 – Notes & Decisions

- EI must **never override DRA**: if DRA determines that an action is not allowed (due to risk, capital, or state), EI must not emit orders.
- Execution policies should be **data-driven**: adjustments to slippage limits, routes, and pacing should be backed by evidence from execution metrics and reports.
- The same logical execution decision chain should exist in offline, paper, and live modes, with differences captured in configuration and environment parameters rather than ad-hoc code.
- As IFNS expands to new asset classes, venues, or execution styles (e.g., derivatives, dark pools, algorithmic execution providers), this step should be extended to:
  - Add new policy dimensions,
  - Define new telemetry events,
  - Document any new SxE views needed to monitor execution quality and risk.
