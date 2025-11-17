# Step 11 – Section 7.0: Model & Signal Integration (MSI)

## 01 – Narrative & Intent

This step defines **Model & Signal Integration (MSI)** — the layer of IFNS that takes multiple model outputs, structural tags, and contextual signals and turns them into **coherent, conflict-resolved decision proposals**.

Where:

- DIL prepares data,
- MI produces model-level predictions,
- MSA provides structural and regime context,

**MSI** is responsible for answering:

- *Given several models and contexts, what is our consolidated view?*
- *Which models should we listen to right now, and with what weight?*
- *How do we handle conflicts, uncertainty, and regime changes?*

The intent of this step is to:

1. Define MSI as the **integration brain** between MI and DRA/EI.
2. Specify the **integration patterns, contracts, and policies** it uses.
3. Ensure that integration behavior is **explicit, transparent, and governable**, not hidden inside individual models.

By the end of this step, the path from “many models” to “one decision proposal” is clear, reproducible, and auditable.

---

### 1. Role of MSI in the IFNS Stack

MSI sits between the **Modeling Intelligence** layer and the **Decision & Risk / Execution** layers:

- **Inputs**
  - Model signals from MI (via the Signal API).
  - Structural and regime tags from MSA (STRUCTURE_MTF, REGIME_TAGS).
  - Contextual data (e.g., volatility and liquidity features from DIL).
  - Model metadata from the Model Registry (roles, families, statuses, strengths and weaknesses).

- **Outputs**
  - Consolidated **decision proposals** per symbol/time:
    - Directional view (e.g., long/short/flat),
    - Strength or conviction score,
    - Time horizon or holding period hints,
    - Any auxiliary information (e.g., preferred execution style hints).
  - Additional **diagnostics**:
    - Which models contributed and how,
    - Where disagreements occurred,
    - Indicators of uncertainty.

MSI does not execute trades or enforce risk limits. Instead, it produces a **structured proposal** that DRA evaluates under risk envelopes and that EI turns into concrete execution actions if allowed.

---

### 2. Integration Patterns

MSI supports several core integration patterns, which can be combined and configured:

1. **Weighted Averaging / Voting**
   - Each model outputs a prediction (e.g., probability, expected return).
   - MSI applies model-specific weights (by family, regime, recency of evidence).
   - Produces a single aggregate score or probability.
   - May use:
     - Simple weighted average,
     - Bayesian-style combinations,
     - Ensemble voting (majority, plurality, or threshold-based).

2. **Role-Based Integration**
   - Models are assigned **roles** (e.g., “primary directional”, “confirmation”, “risk filter”, “structure-aware overlay”).
   - MSI uses role logic, such as:
     - Only act when at least one primary model and one confirmation model agree.
     - Use risk models to modulate sizing, not direction.

3. **Regime-Conditioned Integration**
   - Based on MSA regime tags:
     - Different model subsets are active in different regimes.
     - Weights or voting rules change across regimes.
   - This avoids overusing models that are known to perform poorly in specific structural states.

4. **Conflict Detection & Resolution**
   - MSI defines what constitutes a **conflict** (e.g., models disagree strongly on direction).
   - Possible responses:
     - Stand down (no-trade proposal),
     - Reduce conviction/sizing,
     - Escalate to SEL or mark for investigation.

5. **Confidence & Uncertainty Modeling**
   - MSI aggregates model-level uncertainties into a **composite confidence score**.
   - Low confidence reduces allowed risk or suggests no-trade proposals.

These patterns are encoded as **MSI policies** and can be tuned based on performance and risk appetite.

---

### 3. MSI Contracts: From Signals to Proposals

MSI operates under explicit data contracts.

**Inputs: Model Signal Records**

Each model signal record (from MI) includes at minimum:

- `ts`, `symbol`,
- `model_id`, `model_version`, `model_family`,
- `prediction` (score, probability, expected return),
- `horizon` (time or bars),
- Optional:
  - `confidence` or uncertainty measures,
  - regime or structure hints already encoded by the model.

**Inputs: Context Records**

- Structural tags:
  - `structure_state_short`, `structure_state_medium`, `structure_state_long`,
  - `regime_tag` (e.g., “high-vol-trend”, “low-vol-range”, etc.).
- Context features:
  - Volatility, liquidity summaries,
  - Any relevant DIL features that MSI uses directly.

**Outputs: Decision Proposal Records**

A typical MSI output record contains:

- `ts`, `symbol`,
- `msi_id` or policy version identifier,
- `direction_proposed` (long/short/flat),
- `score` or conviction indicator,
- `effective_horizon`,
- `active_models` (list or summarized representation),
- `disagreement_metric` (how much models differ),
- Optional:
  - `structure_context` (snapshot of relevant structural tags),
  - `policy_flags` (e.g., “reduced_size_due_to_conflict”).

These outputs are the **inputs to DRA**. DRA reads proposals and decides whether they are allowed under current risk envelopes and capital constraints.

---

### 4. Policy-Driven Integration Logic

MSI is governed by **integration policies**, not hardcoded rules.

Examples of policy elements:

- **Model eligibility rules**
  - Only consider models with status `promoted` or `canary` (with additional constraints).
  - Restrict certain models to specific regimes, instruments, or environments.

- **Weighting and aggregation policies**
  - Weight by:
    - Historical performance in similar regimes,
    - Recency of successful evidence,
    - Family role (primary vs. secondary).
  - Cap the influence of any single model to avoid over-concentration.

- **Conflict thresholds**
  - Define thresholds for:
    - Directional disagreement (e.g., probability mass on opposing directions).
    - Confidence mismatch (e.g., high-confidence disagreement vs. low-confidence noise).
  - When exceeded, trigger:
    - No-trade proposals,
    - Reduced-size proposals,
    - Flags to SEL for investigation.

- **Regime transitions**
  - Define how quickly MSI adapts to regime changes:
    - Immediate switch vs. transitional blending.
    - Cooldown periods during structural transitions.

These policies are stored in structured forms (tables/JSON) and surfaced in Admin, so operators can adjust them under governance rules.

---

### 5. Relationship to SEL and DRA

MSI interacts closely with **Self-Evaluation & Learning (SEL)** and **Decision & Risk Architecture (DRA)**:

- MSI is the **front-end** integrator:
  - Produces best-effort decision proposals based on current models and policies.

- DRA is the **risk gate**:
  - Takes MSI proposals and decides:
    - Whether they fit within the risk envelope.
    - How much capital to allocate.
    - Whether environment state (kill switch, cooldown) allows execution.

- SEL is the **evaluation and learning loop**:
  - Observes how MSI’s proposals perform over time.
  - Assesses which integration patterns and policies are most effective.
  - Recommends or triggers updates to MSI policies and model weights.

MSI must therefore:

- Emit telemetry that SEL can analyze (e.g., proposals vs. realized outcomes).
- Keep integration behavior **stable and interpretable** over time so that SEL’s inferences are meaningful.

---

### 6. SxE Representation of MSI

MSI is a key part of the system-to-experience story.

- **Mirror**
  - MSI overview dashboards:
    - Which models are currently active and with what weights.
    - How often MSI is proposing trades vs. standing down.
    - Performance of MSI decisions over time (hit rates, TE, risk-adjusted returns).
  - Conflict and uncertainty indicators:
    - Frequency and impact of conflicts between models.
    - Times when MSI chose no-trade due to conflicts.

- **Admin**
  - **MSI Policy Console**:
    - View and edit (under governance) integration policies:
      - Model eligibility rules,
      - Weighting schemes,
      - Conflict thresholds,
      - Regime transition behaviors.
  - **MSI Diagnostics View**:
    - Inspect specific decisions:
      - Which models contributed,
      - How their outputs were combined,
      - Why a particular direction and size were proposed.

MSI’s SxE presence ensures operators can understand how the “collective mind” of the models behaves and can adjust it with traceable changes.

---

## 02 – Implementation Reference

Model & Signal Integration is implemented across several stages of the **IFNS – Core ML Build Specification**:

- **Stage 3 – Modeling & Training**
  - Provides the **model-level artifacts** and metadata that MSI consumes:
    - Model families, roles, and registry entries.
    - Performance metrics by regime and scenario.

- **Stage 4 – Backtesting & Evaluation**
  - Simulates MSI behavior in offline scenarios:
    - Applies MSI policies to model outputs during backtests.
    - Records performance and conflict statistics for different integration schemes.
  - Uses MSI-aware metrics to evaluate:
    - Overall decision quality,
    - Robustness across regimes,
    - Sensitivity to model changes.

- **Stage 5 – Risk, Execution & SxE Link** (MSI’s primary integration stage)
  - Encodes MSI policies:
    - Eligibility rules, weighting schemes, conflict thresholds.
    - Regime-conditioned integration behaviors.
  - Defines data contracts for **MSI decision proposals**:
    - Tables/JSON such as `msi_policies`, `msi_proposals`, `msi_diagnostics`.
  - Specifies how MSI outputs feed into DRA:
    - Proposal formats, fields, and required metadata.

- **Stages 6 & 7 – Paper & Live Operations**
  - Ensure MSI runs in real time:
    - Consumes live model outputs and context.
    - Produces proposals that DRA evaluates for paper and live trading.
  - Emit MSI telemetry:
    - Proposal streams and outcomes,
    - Conflict events and associated incidents where needed.

In implementation, any change to MSI — new integration pattern, new policy, new model role — should:

1. Be reflected in **Stage 5** policies and contracts.
2. Be tested via **Stage 4** backtests to understand impact.
3. Be visible in SxE via updated Mirror dashboards and Admin policy consoles.
4. Be logged in the Change Log with a clear rationale.

---

## 03 – Notes & Decisions

- MSI is the **only official place** where multiple model outputs are combined into decision proposals; models themselves should not embed ad-hoc ensemble logic that bypasses MSI.
- Integration rules must remain **simple enough to explain**: if an operator cannot understand why MSI produced a decision, integration logic is too complex or under-documented.
- Conflict handling is critical:
  - Standing down (no-trade) is a valid and often desirable outcome when models disagree strongly or when uncertainty is high.
  - MSI should favor not acting over acting on unstable consensus.
- As IFNS evolves, MSI may support more advanced techniques (e.g., online learning of weights, adversarial evaluation of models), but those must:
  - Be captured in policies and contracts,
  - Be explainable via SxE,
  - Be testable through Stage 4 backtests and Stage 6/7 telemetry.
