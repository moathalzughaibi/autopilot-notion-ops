# Stage 07 – Live Trading & Operations

## 01 – Narrative & Intent

This document defines **Stage 07 – Live Trading & Operations** for the Intelligent Financial Neural System (IFNS).

Conceptually, this stage brings together and operationalizes:

- The **data and feature contracts** (Stage 02),
- The **models and Model Registry** (Stage 03),
- The **backtest evidence engine** (Stage 04),
- The **risk, MSI, and execution policies** (Stage 05),
- The **paper rehearsal environment** (Stage 06),

into a **production live environment** where:

- Real capital is deployed,
- Real venues and brokers are used,
- Operational excellence, observability, and safety are first-class concerns.

Stage 07 answers:

- How do we run IFNS in **live capital environments** with:
  - Clear lanes and capital allocations,
  - Strong risk and incident controls,
  - Continuous monitoring and telemetry?
- How are **live sessions, incidents, and operational states** represented in registries and SxE?
- How do we ensure that live behavior is:
  - Aligned with specs and policies,
  - Auditable and explainable,
  - Continuously improvable via SEL?

The outcome of Stage 07 is a **governed live trading layer** that turns IFNS from a research system into a running, observable financial organism.

---

## 02 – Scope & Responsibilities

Stage 07 covers:

1. **Live Environment & Lanes**
   - Definition of `live` environment.
   - Standard live lanes (e.g., `live_canary`, `live_promoted`).

2. **Live Broker Adapters & Routing**
   - Integration with real brokers and venues.
   - Mapping of logical routes to broker-specific behavior.

3. **Live Sessions, Capital & Registry**
   - How live sessions and capital allocations are defined and tracked.
   - Lifecycle states for live strategies and portfolios.

4. **Operations, Incidents & Runbooks**
   - Operational concepts (health, incidents, maintenance windows).
   - How incidents are logged and resolved.

5. **Telemetry & Observability**
   - Live telemetry requirements and key dashboards.
   - Error budgets, SLIs/SLOs where appropriate.

6. **SxE Representation**
   - Mirror views for live posture and health.
   - Admin controls for capital, gates, and incident response.

Stage 07 does **not** redefine MSI/DRA/EI logic; it **deploys** them into a live production setting.

---

## 03 – Live Environment & Lanes

### 3.1 Environment Definition

In the environment model (Stage 01), `live` is the **production** environment:

- Connected to real brokers/venues.
- Subject to regulatory and operational constraints.
- Protected by:
  - Risk envelopes,
  - Kill switches,
  - Incident management processes.

All live behavior must be explicitly tagged with `env = "live"` in telemetry and registries.

### 3.2 Live Lanes

Live lanes separate **stages of trust and capital**. At minimum:

- `live_canary`
  - Small capital allocation.
  - Used for newly promoted strategies/models.
  - Stricter risk limits and more conservative execution.

- `live_promoted`
  - Main production lane.
  - Higher capital allocation.
  - Policies tuned based on sustained evidence.

Optional additional lanes:

- `live_experimental` (if allowed under strict constraints).
- `live_reduced` (e.g., used after downgrades or partial rollbacks).

Each lane has:

- A defined **capital budget**,
- Separate **risk envelopes** (Stage 05),
- Promotion and demotion rules (tightly coupled with SEL).

---

## 04 – Live Broker Adapters & Routing

### 4.1 Live Broker Adapters

Live Broker adapters implement the contract defined in Stage 05/06, but for real venues.

They are responsible for:

- Managing connectivity to broker APIs and/or FIX sessions.
- Translating logical orders into broker-specific messages.
- Handling acknowledgements, partial fills, rejects, and cancels.
- Implementing any venue-specific constraints.

Configuration lives under:

```text
config/environments/live.yaml
config/brokers/
  <broker_name>.yaml
```

Adapters must:

- Respect the `route_id` and execution policies.
- Produce telemetry events:
  - `order_submitted`,
  - `order_acknowledged`,
  - `order_filled`,
  - `order_rejected`,
  - `order_cancelled`.

### 4.2 Route Mapping

The same logical `route_id` set defined in Stage 05 (e.g., `vwap_default`, `smart_limit`, `urgent_mkt`) is mapped in live to:

- Broker-specific algorithms (e.g., broker VWAP algos),
- Specific venues or liquidity pools,
- Fallback behavior if preferred routes fail.

Mappings are defined in artifacts like:

```text
config/policies/execution_routes_live.json
```

This ensures:

- Consistency between backtest, paper, and live,
- Ability to simulate live-like execution in Stage 04 and Stage 06.

---

## 05 – Live Sessions, Capital & Registry

### 5.1 Live Sessions

Live sessions are the **operational runs** of strategies in the live environment.

Each session is defined with:

- `session_id`,
- `env = "live"`, `lane` (`live_canary`, `live_promoted`, etc.),
- Strategy IDs and portfolio definitions,
- Capital allocation details,
- Start and planned review/end dates.

Definitions can live under:

```text
config/live_trading/
  session_<name>.yaml
```

### 5.2 Live Sessions Registry

The **Live Sessions Registry** lives under:

```text
data/registry/live_sessions.json
```

Each entry includes:

- `session_id`,
- Environment/lane,
- Strategy and portfolio IDs,
- Start/end timestamps,
- Current status:
  - `scheduled`, `running`, `suspended`, `completed`, `rolled_back`,
- Capital allocation & utilization,
- Links to:
  - Telemetry streams,
  - P&L and risk summaries,
  - Incidents and SEL evaluations.

This registry is the **authoritative list of live runs**.

### 5.3 Capital & Limits

Capital allocation is controlled via:

- Configuration (capital budgets per lane, per strategy),
- Risk envelopes (Stage 05) that include:
  - Max gross and net exposures,
  - Max leverage,
  - Per-symbol and per-sector caps.

Admin actions that change capital allocations:

- Must be reflected in:
  - Config and/or registry,
  - Change Log entries,
  - Risk envelope updates where needed.

---

## 06 – Operations, Incidents & Runbooks

### 6.1 Operational Concepts

Stage 07 defines key operational states and concepts:

- **Health** – whether data, models, brokers, and decision pipelines are functioning.
- **Degraded Mode** – partial functionality (e.g., some markets disabled).
- **Maintenance Mode** – trades temporarily paused for planned work.
- **Incident** – unexpected deviation from normal behavior requiring explicit handling.

### 6.2 Incident Types

Typical incident categories:

- **Data incidents**
  - Feed gaps or corrupt data.
- **Model incidents**
  - Model outputs behaving erratically, SEL flags, or misalignment vs. expectations.
- **Execution incidents**
  - High rejection rates, extreme slippage, broker errors.
- **Risk incidents**
  - Envelope breaches, unexpected exposures, drawdowns beyond thresholds.
- **Infrastructure incidents**
  - Latency spikes, component crashes, connectivity loss.

Incidents are recorded as structured events in an **Incident Log**, e.g.:

```text
data/registry/incidents_log.json
```

Each incident record includes:

- `incident_id`,
- Timestamps,
- Severity,
- Category,
- Affected env/lane, strategies, portfolios,
- Short description and initial diagnosis,
- Links to telemetry, sessions, and any mitigations.

### 6.3 Runbooks & Response

For each major incident type, Stage 07 expects:

- A **runbook** (operational procedure) stored as documentation (e.g., in `docs/ops/runbooks/` or in Notion).
- SxE integration:
  - Mirror highlights active incidents.
  - Admin provides actions aligned with runbooks:
    - E.g., move lane to cooldown, reduce exposure, force flat, enable kill switch.

SEL uses incident data to:

- Identify root patterns,
- Recommend policy/tuning changes,
- Track incident recurrence after changes.

---

## 07 – Telemetry & Observability

### 7.1 Telemetry Requirements

Live trading must emit:

- The same MSI/DRA/EI events as Stage 05 and Stage 06:
  - `msi_proposal`, `dra_decision`,
  - `order_*` events,
  - `risk_breach`, `kill_switch_change`, `cooldown_state_change`.
- Additional **operational events**, such as:
  - `component_health_change`,
  - `data_feed_status_change`,
  - `broker_connection_status_change`,
  - `incident_created`, `incident_resolved`.

All events must include:

- `env = "live"`,
- `lane`,
- Strategy/portfolio identifiers,
- Timestamps with sufficient precision.

### 7.2 SLIs, SLOs & Error Budgets (Optional but Recommended)

Where appropriate, Stage 07 can define:

- **Service-Level Indicators (SLIs)**:
  - Data availability (% of expected bars),
  - Decision latency (ms) from data arrival to order submission,
  - Broker uptime (% of time the adapter is connected),
  - Telemetry delivery success.

- **Service-Level Objectives (SLOs)**:
  - Target thresholds for SLIs,
  - Acceptable error rates.

- **Error Budgets**:
  - Allowed deviation from SLOs before triggering escalation.

These can be monitored via SxE dashboards or external observability tools.

---

## 08 – SxE Representation of Stage 07

### 8.1 Mirror – Live Posture & Health

Mirror surfaces high-level live views:

- **Live Capital & Exposure**
  - Capital allocation and utilization by lane and strategy.
  - Current exposures vs. envelopes.

- **Performance & Risk**
  - P&L curves and drawdowns.
  - TE vs. benchmarks where applicable.
  - Envelope usage and risk breaches.

- **Operational Health**
  - Status of data feeds, brokers, MSI/DRA/EI components.
  - Active incidents and their severity.

Mirror must make it easy for a human to answer:

- “What is happening right now?”
- “Is the system healthy?”
- “Where are we close to boundaries?”

### 8.2 Admin – Live Control Plane

Admin provides:

- **Capital & Lane Management**
  - Adjust capital allocations (within policy).
  - Move strategies between lanes (e.g., promote/demote between `live_canary` and `live_promoted`).
  - Apply global or lane-specific trading halts.

- **Risk & Policy Controls**
  - View and adjust (under governance) live risk envelopes.
  - Activate/deactivate kill switches and cooldowns.
  - Apply “safe mode” templates (pre-defined sets of reduced risk settings).

- **Incident Console**
  - View and filter incidents.
  - Acknowledge, annotate, and close incidents.
  - Link incidents to:
    - Change Log entries,
    - SEL analyses,
    - Policy/model changes.

All Admin actions that affect live behavior must:

- Be logged in the Change Log,
- Be visible in audit trails,
- Optionally require multi-step approval for high-risk actions.

---

## 09 – Governance, Compliance & SEL Integration

Stage 07 adds governance layers specific to live capital:

- **Separation of duties**:
  - Those who design models/policies vs. those who approve/operate them in live.
- **Approval workflows**:
  - For promotions from `live_canary` to `live_promoted`,
  - For major envelope or capital changes.

- **Compliance & Audit**:
  - Traceable link from decisions (trades) to:
    - Models and policies,
    - Evidence from backtests and paper runs,
    - Operator actions and overrides.

SEL integration:

- SEL ingests:
  - Live P&L and risk metrics,
  - Incidents and operational anomalies,
  - Policy and model changes from the Change Log.

- SEL then:
  - Produces structured assessments of:
    - Strategy and model robustness in live,
    - Policy effectiveness,
    - Operational reliability.
  - Recommends:
    - Promotions, demotions, or deactivations,
    - Policy tightening or loosening,
    - Technical improvements to data or models.

Stage 07 thus ensures that **learning from live** is formally captured and fed back into the IFNS evolution loop.

---

## 10 – Notes & Decisions

- Stage 07 is where all prior stages become **real**:
  - Any misalignment or ambiguity upstream will show up here as risk or operational pain.
- The live system must always be:
  - Explainable (traceable decisions),
  - Observable (rich telemetry),
  - Governed (policies and approvals).

- SxE is critical:
  - Mirror gives real-time awareness,
  - Admin gives controlled levers,
  - Both tie directly to the artifacts defined in Stages 01–06.

- Any changes introduced in live operations that affect:
  - Risk behavior,
  - Execution routes,
  - MSI policies,
  - Data or models,
  must be:
  - Captured in the Change Log,
  - Supported by evidence (backtests, paper, SEL),
  - Reflected back into the IFNS spec where appropriate.

With Stage 07 in place, IFNS completes its **Core ML Build** cycle: from foundations and data, through models and evaluation, to paper rehearsal and finally governed live operation—always connected back to the specification and SxE mirror that keep the system intelligible and controllable.
