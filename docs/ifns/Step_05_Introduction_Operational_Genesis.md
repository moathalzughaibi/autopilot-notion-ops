# Step 05 – Section 1.0: Introduction — Operational Genesis Framework

## 01 – Narrative & Intent

This step introduces the **Operational Genesis Framework**: the way IFNS is defined, scoped, and structured as a living system, not just a set of tools or isolated models. It explains *what* IFNS is trying to be in practice, *which layers* of intelligence and control it is composed of, and *how* those layers will be described throughout the rest of the specification.

The intent is to give every reader — architect, engineer, quant, operator, or risk owner — a common mental model so that later sections feel like **different views of the same organism**, not separate projects.

### 1. IFNS as an Operational System, Not a Toolkit

IFNS is framed as an **Intelligent Financial Neural System**. In operational terms, this means:

- It is always in one of a small set of **environments** (offline, paper, live).
- It receives **sensory input** in the form of market data and contextual information.
- It processes this input through a series of **intelligence layers** (data, modeling, execution, risk, self-evaluation).
- It exposes its internal state and decisions through **System-to-Experience (SxE)** surfaces (Mirror and Admin).
- It operates under explicit **policies and risk envelopes** that can be inspected and governed.

The goal of the Operational Genesis Framework is to describe IFNS in a way that supports **real-world operations**: day-by-day running, monitoring, adjusting, and evolving the system in a controlled manner.

### 2. Core Intelligence Layers

IFNS is described using a set of core intelligence layers, each responsible for a specific class of decisions:

- **DIL – Data Intelligence Layer**  
  The sensory cortex: ingesting, cleansing, aligning, and encoding data (prices, volumes, context) into consistent, ML-ready representations.

- **MI – Modeling Intelligence**  
  The cognitive heart: a set of model families and ensembles that transform encoded data into predictions, scores, and directional views.

- **EI – Execution Intelligence**  
  The motor system: converting signals from MI (and higher layers) into orders, routes, and timing decisions, subject to constraints and costs.

- **MSA – Market Structural Awareness**  
  The structural sense: understanding higher highs/lows, regimes, volatility clusters, and structural features that shape how signals should be interpreted.

- **MSI – Model & Signal Integration**  
  The integration fabric: combining multiple models, contexts, and structural views into coherent, conflict-resolved decision proposals.

- **DRA – Decision & Risk Architecture**  
  The control grid: applying risk envelopes, capital constraints, kill-switch logic, and cooldown rules to decide whether and how to execute actions.

- **SEL – Self-Evaluation & Learning**  
  The meta-layer: observing performance, incidents, and context over time and deciding when to retrain, promote, demote, or retire models and policies.

These layers are not separate systems; they are **roles** that the specification uses to organize behavior, metrics, and responsibilities. Later sections assign concrete tables, JSON contracts, and SxE views to each layer.

### 3. SxE: From System to Experience

The Operational Genesis Framework is explicitly **SxE-aware**: every internal object that matters operationally must be visible and governable from the outside.

This step therefore establishes three primary experience surfaces:

- **Mirror** – the awareness surface: how IFNS “looks at itself” and how operators see posture, performance, risk, context, and incidents.
- **Admin** – the control and governance surface: where policies, thresholds, registries, capital allocations, and environment transitions are configured and approved.
- **Telemetry & Registries** – the connective tissue: where structured events, metrics, and indices are recorded so that Mirror and Admin can reflect the true state of the system.

From this point forward, any new capability introduced in the specification is expected to answer two questions:

1. *What does this capability do internally?* (data, models, rules, computations)
2. *How is this capability exposed and controlled externally?* (Mirror views, Admin panels, registries, telemetry events)

### 4. Operating Principles

This step also codifies the operating principles that guide how IFNS should behave and evolve:

1. **Safety first, always**  
   Risk envelopes, kill switches, and cooldowns are not optional extras; they are core parts of the architecture and must be defined before live capital is exposed.

2. **Evidence-based evolution**  
   No change to a live model, policy, or capital allocation should be made without supporting evidence from backtests, paper runs, and/or live performance telemetry.

3. **Explainability and traceability**  
   For any significant decision (execution, promotion, rollback, halt), operators must be able to reconstruct the “why” from registries, telemetry, and reasoning reports.

4. **Environment separation**  
   Offline, paper, and live environments must be clearly separated in configuration, and transitions between them must be governed by explicit lanes and rules.

5. **Single source of truth for contracts**  
   Schemas, registries, metrics, and policies should be defined in one place (tables + JSON contracts) and then reused by all components, including UI and automation.

6. **No hidden behavior**  
   Any behavior that can impact P&L, risk, or capital must be surfaced in Admin and/or Mirror; there should be no “stealth logic” that only exists in code.

These principles form the **baseline expectations** that all subsequent stages of the Core ML build must respect.

### 5. Scope and Boundaries

Finally, this step clarifies what IFNS **does** and **does not** aim to cover:

- IFNS **does** cover:
  - Data ingestion, feature engineering, modeling, backtesting, risk and execution logic, paper and live operations, telemetry, and SxE interfaces.
  - Governance over models, policies, capital, and incident handling.

- IFNS **does not** attempt to:
  - Define broker-specific legal contracts, taxation logic, or end-user account management.
  - Replace existing OMS/EMS platforms; instead, it integrates with them via well-defined interfaces.
  - Guarantee profitability; it guarantees **process, transparency, and control**, not outcomes.

By setting these boundaries early, the Operational Genesis Framework keeps the specification focused and prevents scope creep from weakening the core.

---

## 02 – Implementation Reference

The Operational Genesis Framework described here is implemented and grounded in the **IFNS – Core ML Build Specification** primarily through:

- **Section 0 – Document Overview**  
  - Defines the purpose, scope, audience, and artifact set of the Core ML build, aligned with the intelligence layers and SxE principles introduced in this step.

- **Stage 1 – Foundations & Architecture**  
  - Establishes the directory and repository layout for Core ML, data, and SxE artifacts.  
  - Defines the `core_ml_config` schema, including:
    - Environment modes (`offline`, `paper`, `live`),
    - Pointers to data sources, feature sets, and model registries,
    - References to risk envelopes, promotion/rollback rules, and deployment lanes.
  - Specifies the main JSON/registry files that Mirror and Admin will consume, such as:
    - `model_registry.json`
    - `backtests_index.json`
    - `ml_policies.json`
    - `risk_envelope.json`
    - `deployment_environments.json` and `deployment_lanes.json`

Taken together, Section 0 and Stage 1 provide the **concrete skeleton** of the Operational Genesis Framework: they declare *where* each layer lives in the repository, *how* configuration flows into runtime, and *which files* SxE surfaces must read from.

Any future extension to IFNS that introduces new layers, capabilities, or markets should:

1. Update the Operational Genesis narrative in this step if the conceptual model changes.
2. Extend the Stage 1 configuration schema and registries to add new contracts and references.
3. Ensure that Mirror and Admin visibility for the new capability is defined from the outset.

---

## 03 – Notes & Decisions

- This step is treated as the **conceptual anchor** for the entire specification. Any major structural change to IFNS (new layers, new environments, new SxE surfaces) should be reflected here first.
- The list of intelligence layers (DIL, MI, EI, MSA, MSI, DRA, SEL) is **normative**. New capabilities should be mapped to one or more of these layers rather than inventing ad-hoc categories.
- The operating principles (safety first, evidence-based evolution, explainability, environment separation, single source of truth, no hidden behavior) are intended to guide both design and code review.
- As the Admin and Mirror UI matrices mature, this step may reference specific UI packs or consoles by name (for example, “Risk Envelope Console”, “Model Promotion Ledger”, “Incident Timeline View”) to tighten the link between conceptual roles and concrete screens.
