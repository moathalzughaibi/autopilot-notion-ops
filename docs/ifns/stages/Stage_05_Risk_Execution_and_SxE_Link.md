# Stage 05 – Risk, Execution & SxE Link

## 01 – Narrative & Intent

This document defines **Stage 05 – Risk, Execution & SxE Link** for the Intelligent Financial Neural System (IFNS).

Conceptually, this stage implements and connects:

- **Decision & Risk Architecture (DRA)** – Step 12.
- **Model & Signal Integration (MSI)** – Step 11.
- **Execution Intelligence (EI)** – Step 09.
- The **SxE bridge** to Mirror/Admin – how all of the above become visible and controllable.

Stage 05 answers:

- How do model signals (Stage 03) and structure/feature context (Stage 02/10) become **actual trade decisions**?
- How do we **encode and enforce risk envelopes and gates** in a way that is:
  - Explicit,
  - Auditable,
  - Visible in SxE?
- How do we define **execution policies and routes** that EI will apply in backtests (Stage 04), paper (Stage 06), and live (Stage 07)?
- How do telemetry and registries for risk & execution **tie back** to the IFNS spec and UI?

The outcome of Stage 05 is a **coherent decision & execution control layer** that:

- Orchestrates MSI, DRA, and EI,
- Exposes their state and behavior to Mirror/Admin,
- Keeps all risk-bearing behavior governed and explainable.

---

## 02 – Scope & Responsibilities

Stage 05 covers:

1. **Risk Envelopes & Policies**
   - Definition of envelopes and limits (per-strategy, per-portfolio, per-environment).
   - Representation as structured tables/JSON.

2. **MSI Contracts & Signal Integration**
   - How model outputs are combined into decision proposals.
   - Eligibility, weighting, and conflict-resolution rules.

3. **Execution Policies & Routing**
   - Definition of execution styles (VWAP, POV, limit, market).
   - Route selection logic and associated parameters.

4. **DRA Gates & Decision Tables**
   - Eligibility, risk, capital, and control-state gates.
   - Final decision outputs (allow/reduce/deny, sizing).

5. **Telemetry & Contracts**
   - Events and metrics emitted by MSI, DRA, and EI.
   - How these map to telemetry schemas and SxE dashboards.

6. **SxE Representation**
   - How Mirror shows risk & execution posture.
   - How Admin gives operators control over policies and envelopes.

Stage 05 does **not** define the low-level mechanics of paper/live runtime (Stages 06–07); it defines the **shared logic and contracts** that those stages use.

---

## 03 – Risk Envelopes & Policies

### 3.1 Risk Envelope Structures

Risk envelopes are defined in structured artifacts, for example:

- `config/policies/risk_envelope.json`
- `data/registry/risk_envelope_overrides.json` (optional runtime overrides)

Each envelope entry typically includes:

- Scope:
  - `strategy_id`,
  - Optional `universe_id` or `symbol_group`,
  - Environment/lane (`offline`/`paper`/`live`, `live_canary`, `live_promoted`, etc.).
- Limits:
  - Max position size per instrument (absolute or % of ADV/notional).
  - Max gross and net exposure per strategy and portfolio.
  - Max leverage.
  - Drawdown thresholds (daily/rolling).
  - Volatility- or regime-dependent caps (e.g., multipliers by `regime_tag`).
- Behavior on breach:
  - Scale-down rules,
  - Kill switch escalation rules,
  - Cooldown durations.

These structures are the **inputs** to DRA gates.

### 3.2 Policy Types

Stage 05 also captures other risk-related policies, such as:

- **Stop-out policies** (per-trade or per-position).
- **Position concentration policies** (max weight by sector, country, cluster).
- **Liquidity & participation policies**:
  - Max % of bar volume,
  - Max daily participation per symbol.

Policies are stored under:

```text
config/policies/
  risk_envelope.json
  risk_policies.json
  liquidity_policies.json
```

The precise file breakdown can evolve, but Stage 05 defines that these are **explicit, versioned artifacts**, not hidden in code.

---

## 04 – MSI Contracts & Signal Integration

### 4.1 MSI Inputs & Outputs

MSI consumes:

- Model predictions from Stage 03 via the Model Service:
  - Classification probabilities,
  - Regression outputs,
  - Risk overlays.
- Structural and regime context from Stage 02/10:
  - `regime_tag`,
  - `struct_state_*`,
  - VOL_LIQ features.
- Current positions and exposures (from runtime position registry).
- Optional operator signals or overrides.

MSI produces **decision proposals**:

- For each symbol (or basket), at a given time:
  - Desired direction/position change,
  - Confidence or conviction score,
  - Time horizon or target holding period,
  - Any supporting metadata (e.g., model contributions, reasons).

These proposals are **not yet trades**; they are inputs to DRA.

### 4.2 Integration Rules

MSI policies are defined in artifacts such as:

```text
config/policies/msi_policies.json
```

Key components:

- **Model selection rules**
  - Which model families are eligible for a given symbol or regime.
- **Weighting rules**
  - How to weight model outputs (fixed weights, regime-aware weights, etc.).
- **Conflict resolution**
  - Rules for when models disagree (e.g., require majority, down-weight outliers).
- **Confidence thresholds**
  - Minimum combined confidence to issue a proposal.
- **Role-based usage**
  - Primary directional vs. confirmation vs. risk overlay.

MSI outputs **include enough metadata** (e.g., per-model contributions) to support:

- DRA decision-making,
- SxE explainability,
- SEL analysis.

---

## 05 – Execution Policies & Routing

Execution logic is driven by **execution policies** and **routes**, shared between:

- Stage 04 (simulated via Execution Simulator),
- Stage 06 (paper broker),
- Stage 07 (live brokers).

### 5.1 Execution Policies

Policies are stored in:

```text
config/policies/execution_policies.json
```

They define, for each strategy/environment:

- Default order types and styles:
  - Market, limit, VWAP, POV, TWAP variants.
- Pacing:
  - Max participation rate (% of volume),
  - Maximum order frequency.
- Slippage targets or budgets:
  - Acceptable slippage bands (bps),
  - Escalation rules if slippage exceeds bands.
- Time-in-force and routing rules:
  - When to cancel or modify orders,
  - Which venues or broker routes to use by default.

### 5.2 Routes & Adapters

Execution routes are identified by logical `route_id` values, such as:

- `vwap_default`,
- `smart_limit`,
- `passive_lo`,
- `urgent_mkt`.

These routes are:

- Mapped to:
  - Simulation behaviors in Stage 04,
  - Paper Broker behaviors in Stage 06,
  - Live Broker adapters and configurations in Stage 07.
- Configured via:
  - `config/policies/execution_routes.json` or similar.

The Default Parameters Registry may include parameters like:

- `harness.route.default = "vwap"`
- Route-specific cooldowns or safety toggles.

---

## 06 – DRA Gates & Decision Tables

Stage 05 implements the **DRA gates** described in Step 12, in concrete form.

### 6.1 Gate Types

DRA uses several conceptual gates, each backed by decision tables:

1. **Eligibility Gate**
   - Is the strategy enabled?
   - Is the environment/lane open?
   - Are required models in allowed statuses (`promoted`, `canary`)?

2. **Risk Envelope Gate**
   - Does the proposed position fit within:
     - Position size limits,
     - Exposure limits,
     - Drawdown or volatility constraints?

3. **Capital Allocation Gate**
   - Does the proposal respect capital allocation plans?
   - Is there remaining budget for this strategy/lane?

4. **Control State Gate**
   - Are any relevant kill switches active?
   - Are we in a cooldown window for this strategy/lane?
   - Are there active incidents blocking action?

5. **Final Decision & Sizing Gate**
   - If allowed, what is the approved size?
   - Should we reduce rather than increase exposure?
   - Should we allow only risk-reducing trades?

### 6.2 Decision Table Representation

Decision tables are defined in artifacts, for example:

```text
config/policies/dra_decision_tables.json
```

Each table:

- Specifies inputs (fields from MSI proposals, envelopes, system state).
- Specifies conditions and outputs:
  - `decision = ALLOW | REDUCE | DENY`,
  - `max_size` or adjustment factors,
  - Any required flags or annotations.

These tables:

- Are **data, not code**.
- Can be visualized and edited in Admin (under governance control).
- Are used consistently in:
  - Stage 04 (simulated DRA),
  - Stage 06 (paper),
  - Stage 07 (live).

---

## 07 – Telemetry & Contracts

Stage 05 defines the **risk & execution telemetry contracts** that must be present in the telemetry schema.

### 7.1 Key Event Types

Event streams (likely NDJSON) include, at minimum:

- `event_type = "msi_proposal"`
  - Contains model contributions, aggregated scores, context (regime, structure).
- `event_type = "dra_decision"`
  - Contains decision (allow/reduce/deny), gating reasons, envelope usage.
- `event_type = "order_submitted"`
- `event_type = "order_filled"`
- `event_type = "order_rejected"`
- `event_type = "risk_breach"`
  - Envelope or limit violations.
- `event_type = "kill_switch_change"`
- `event_type = "cooldown_state_change"`

### 7.2 Telemetry Schemas

Schemas are documented under:

```text
telemetry/schemas/
  telemetry_schema.json
  events_execution.schema.json
  events_risk.schema.json
  events_msi.schema.json
```

Each event type has fields for:

- Identifiers:
  - `event_id`,
  - `ts`,
  - `env` & `lane`,
  - `strategy_id`,
  - `symbol` (when applicable).
- Inputs:
  - MSI inputs and scores,
  - Envelope state,
  - Position and capital usage.
- Outputs:
  - DRA decision,
  - Order details,
  - Resulting exposures.

These events are the **raw material** for:

- Mirror dashboards,
- Admin consoles,
- SEL analysis,
- Incident detection and runbooks.

---

## 08 – SxE Representation of Stage 05

### 8.1 Mirror – Risk & Execution Posture

Mirror surfaces high-level views of:

- **Risk Posture**
  - Envelope usage by strategy, symbol group, and lane.
  - Active kill switches and cooldowns.
  - Recent risk breaches and their impact.

- **Execution Quality**
  - Slippage distributions by route and strategy.
  - TE vs. benchmarks where applicable.
  - Fill and rejection rates.

- **Decision Flow**
  - MSI proposals vs. DRA decisions over time (e.g., what was proposed vs. what was allowed).

These views turn invisible internal logic into a **financial awareness mirror**.

### 8.2 Admin – Governance & Control

Admin surfaces control consoles for:

- **Risk Envelope Console**
  - View and edit envelopes and limits (under workflow & approval).
  - Inspect envelope usage and breach history.

- **MSI Policy Console**
  - View model roles and integration rules.
  - Adjust weights, confidence thresholds, and eligibility (via controlled configs).

- **Execution Policy Console**
  - View and adjust execution styles and route mappings.
  - Set global and per-strategy constraints on participation, order types, and venues.

- **DRA Decision Tables Console**
  - Visualize gates and tables.
  - Simulate DRA decisions for specific scenarios (what-if tools).

Changes made via Admin:

- Generate entries in the **Change Log**.
- Can be linked to SEL recommendations and DRA outcomes.

---

## 09 – Governance & Change Management

Given its sensitivity, Stage 05 is heavily governed.

Key rules:

- All risk envelopes, MSI policies, execution policies, and DRA tables:
  - Must be **version-controlled**;
  - Must have clear ownership;
  - Should be linked to evidence (backtests, paper runs, incidents).

- The **Change Log** records:
  - Who changed what policy, when, and why;
  - Links to promotion dossiers or rollback reports;
  - Planned review dates.

- SEL (Stage 13) interacts with Stage 05 by:
  - Proposing changes based on evidence;
  - Providing structured recommendations (not direct edits);
  - Tracking outcomes of policy changes in terms of performance and incidents.

Stage 05 ensures that risk and execution behavior is **governed by policy, not ad-hoc decisions**.

---

## 10 – Notes & Decisions

- Stage 05 is the **bridge** between Core ML (data + models) and operational reality (execution + risk).
- Nothing in MSI, DRA, or EI should be “magic”:
  - All important behavior must be traceable to configurations, envelopes, and decision tables.
- Backtesting (Stage 04), Paper (Stage 06), and Live (Stage 07) **share** these policies:
  - Differences between environments should be deliberate (e.g., stricter in live), not accidental.
- SxE is not just decoration:
  - Mirror/Admin must reflect the true state of risk & execution,
  - Operators must be able to see *why* decisions were made and *where* constraints bind.

With Stage 05 in place, IFNS has a **governed risk & execution core** that binds together MSI, DRA, EI, and the financial-awareness SxE surfaces.
