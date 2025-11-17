# Step 08 – Section 4.0: Modeling Intelligence (MI)

## 01 – Narrative & Intent

This step defines **Modeling Intelligence (MI)** — the cognitive heart of IFNS.

MI is responsible for turning the rich representations produced by the Data Intelligence Layer (DIL) into **predictions, scores, and structured views of opportunity and risk**. It does this through a governed ecosystem of model families, training pipelines, evaluation metrics, and promotion rules, all anchored in explicit contracts.

The intent of this step is to:

1. Define how models are organized, versioned, and governed within IFNS.
2. Specify the **Model Registry**, model families, and training/evaluation workflows.
3. Clarify how MI interacts with DIL (inputs), Execution Intelligence (EI) (consumers), and SxE (visibility and control).

By the end of this step, there should be a clear understanding of **what it means to be a model in IFNS**, how models are created and compared, and how they move from research to production roles.

### 1. Role of MI in the IFNS Stack

MI sits between DIL and EI:

- **Upstream / Inputs**
  - Feature frameworks and labels from DIL (e.g., TREND_MTF, CANDLE_SHAPE, STRUCTURE_MTF, VOL_LIQ).
  - Training and evaluation datasets defined in DIL’s dataset schemas.
  - Regime and structural tags (from MSA) that can be used as model inputs or segmentation keys.

- **Downstream / Outputs**
  - Predictions and scores (e.g., directional probabilities, expected returns, risk-adjusted scores).
  - Uncertainty estimates or confidence scores.
  - Regime or structure-aware signals (e.g., strategy recommendations conditioned on MSA context).
  - Artifacts and metrics that feed Backtesting & Evaluation (Stage 4) and SEL.

MI’s primary responsibilities:

- Define **model families** and their roles.
- Provide **reproducible training pipelines**.
- Maintain a **Model Registry** with robust metadata and statuses.
- Enforce **evaluation and calibration standards** before models can influence execution.

### 2. Model Families and Roles

IFNS organizes models into **families** based on their purpose and behavior. Examples include:

1. **Alpha / Directional Models**
   - Predict direction or return over a horizon (e.g., probability of upward move in the next H bars).
   - Drive primary trade entry and position sizing decisions.

2. **Structure & Regime Models**
   - Infer market regimes (trending vs. mean-reverting, high vs. low volatility).
   - Interpret STRUCTURE_MTF features to classify structural states (e.g., breakout, consolidation, topping).

3. **Risk & Volatility Models**
   - Forecast volatility, drawdown risk, or tail risk.
   - Feed into risk envelopes and position limits.

4. **Execution Cost / Slippage Models**
   - Estimate expected slippage, market impact, and execution quality.
   - Influence routing decisions and time-slicing strategies.

5. **Auxiliary / Diagnostic Models**
   - Detect anomalies in data, model behavior, or environment conditions.
   - Support SEL and incident detection.

Each model family is defined by:

- **Input feature sets** (which feature frameworks and versions).
- **Label definitions** (what future outcome is predicted).
- **Intended role** (alpha, risk, structure, etc.).
- **Acceptable algorithms** (e.g., tree-based, linear, neural, hybrid).
- **Evaluation metrics** that matter for that role (e.g., directional accuracy, calibration error, drawdown profile).

Model families provide **templates** that individual models (with specific hyperparameters, training periods, and feature subsets) can instantiate.

### 3. Model Registry

The **Model Registry** is the authoritative catalog of all models in IFNS. It is a structured registry rather than a folder of arbitrary files.

Each model entry includes at least:

- **Model ID and name**
- **Family and role** (e.g., Alpha_MTF_V1, Volatility_Forecast_V2)
- **Version** (semantic versioning where applicable)
- **Input dataset(s)** (dataset IDs from DIL)
- **Feature frameworks and versions**
- **Label definition(s)**
- **Training period(s) and universe**
- **Training configuration**
  - Algorithm type,
  - Hyperparameters,
  - Regularization/constraints.
- **Evaluation metrics**
  - On training, validation, and test sets.
- **Calibration metrics**
  - For probabilistic models (e.g., Brier score, calibration curves).
- **Status**
  - `draft`, `candidate`, `baseline`, `canary`, `promoted`, `deprecated`.
- **Operational deployment info**
  - Where and how it is used (offline, paper, live),
  - Associated gates and risk envelopes.

The Model Registry is the **single source of truth** for “what models exist, what they do, and whether they are allowed to influence decisions”.

### 4. Training & Evaluation Pipelines

MI defines **standardized training pipelines** that take DIL datasets and produce models plus metrics.

Key properties:

- **Reproducible**
  - Training jobs are fully specified (config, code version, data snapshot).
  - Jobs can be re-run to confirm results.

- **Config-driven**
  - Training specifications live in structured configs (e.g., `Model_Training_Spec` tables).
  - Hyperparameter ranges, seeds, and stopping criteria are defined explicitly.

- **Metrics-rich**
  - Metrics include:
    - Predictive performance (e.g., AUC, accuracy, log loss),
    - Risk-related measures (e.g., drawdown of strategy prototypes),
    - Stability metrics (e.g., performance consistency across folds),
    - Calibration quality (for probabilistic outputs).

- **Evaluation-first**
  - Models are not merely “trained”; they are evaluated via:
    - Cross-validation or rolling windows,
    - Out-of-sample segments,
    - Scenario-based stress testing.

Results of each training run are:

- Logged to an **Experiments or Training Runs table**,
- Linked back to the Model Registry entry,
- Used as evidence for promotion decisions in SEL.

### 5. Calibration, Constraints, and Robustness

MI places strong emphasis on **calibration and robustness**, not just raw predictive strength.

- **Calibration**
  - For probabilistic outputs, predicted probabilities must align with realized frequencies.
  - Calibration plots and metrics are stored and surfaced to SxE.

- **Constraints**
  - Models should adhere to constraints appropriate for their role, such as:
    - Monotonic constraints for certain risk features,
    - Bounds on position recommendations,
    - Limits on sensitivity to specific inputs (where required).

- **Robustness**
  - Models should be stress-tested on:
    - Different regimes (e.g., high vs. low volatility),
    - Crash-like scenarios,
    - Thinner liquidity conditions.
  - Robustness metrics are captured and used in promotion decisions.

Calibration and robustness information must be **inspectable** in Admin and Mirror, so that operators understand not just “how strong” a model is, but **where it might break**.

### 6. SxE Representation of MI

MI is deeply integrated into SxE:

- **Mirror**
  - Provides model-level views:
    - Active and inactive models by family and status,
    - Key performance metrics,
    - Model health and drift indicators.
  - Presents aggregated views:
    - How much of current strategy behavior is driven by each model or family,
    - Which models are under review or in canary mode.

- **Admin**
  - Provides:
    - Read/write access (under governance) to:
      - Model Registry entries (excluding immutable audit fields),
      - Model statuses (promotion/demotion actions via approved workflows).
    - Workflows for:
      - Approving a model to enter canary or promoted status,
      - Deprecating outdated models,
      - Attaching evidence (backtests, paper runs, incidents) to decisions.

- **Telemetry & Registries**
  - Training runs, experiments, and model promotions/rollbacks generate events that are:
    - Stored in telemetry streams,
    - Linked to Model Registry entries,
    - Visible in incident and change logs.

MI is **not invisible**: it has a clear presence in the operator experience, and its lifecycle is part of the governance story.

### 7. Promotion Path and Lifecycle

Models in IFNS follow a **controlled lifecycle**:

1. **Draft**
   - Newly trained models, under research.
   - Not allowed to influence paper or live decisions.

2. **Candidate**
   - Models that meet minimal performance standards in backtests and validation.
   - Eligible for deeper evaluation and scenario testing.

3. **Baseline**
   - Reference models used for comparison.
   - Provide a floor of acceptable performance (e.g., simple benchmarks).

4. **Canary**
   - Models deployed in **paper** or **limited-live** contexts with small capital and strict monitoring.
   - Subject to tight KPIs and fast rollback rules.

5. **Promoted**
   - Models with sufficient evidence across backtests, paper, and live canary phases.
   - Can drive a meaningful portion of production behavior.

6. **Deprecated**
   - Models retired from active use, but preserved for audit and historical analysis.

SEL and DRA use this lifecycle to decide:

- Which models can provide signals to EI and MSI.
- How much weight to give each model.
- When to trigger retraining or demotion.

---

## 02 – Implementation Reference

The Modeling Intelligence layer described in this step is implemented in the **IFNS – Core ML Build Specification** primarily through:

- **Stage 3 – Modeling & Training**
  - Defines:
    - Model families and roles (`Model_Families` table),
    - The Model Registry schema (`Model_Registry`),
    - Training job specifications (`Model_Training_Spec`, `Training_Runs`),
    - Evaluation and calibration metrics (`Model_Metrics_Spec`).
  - Specifies how training pipelines are configured, executed, and logged.
  - Provides contracts for associating each model with:
    - Its input datasets and feature frameworks (from Stage 2),
    - Its evaluation metrics and status.

- **Stage 2 – Data & Feature Pipeline**
  - Supplies the datasets, feature frameworks, and labeling policies that MI consumes.
  - Ensures that each model’s inputs are clearly defined and versioned.

- **Stage 4 – Backtesting & Evaluation**
  - Links model outputs (signals) to backtest configurations and results.
  - Uses model IDs and dataset IDs to ensure backtests are interpretable in terms of specific models and data.

- **Stage 5 – Risk, Execution & SxE Link**
  - Uses MI’s Model Registry and metrics as input to promotion/rollback rules, MSI context states, and DRA decision logic.
  - Ensures that the models allowed to influence execution decisions are always those with clear statuses and evidence.

In practice, any new model or model family must:

1. Be defined in the **Model Families** and **Model Registry** tables (Stage 3).
2. Declare its input datasets and feature frameworks (Stage 2).
3. Produce training and evaluation records that are logged to **Training Runs** and related metrics (Stage 3).
4. Participate in backtests (Stage 4) before it can be considered for canary or promoted roles.
5. Have its status transitions governed by the promotion/rollback policies defined in Stage 5.

This ensures that Modeling Intelligence is **systematic, auditable, and tightly integrated** with the rest of IFNS.

---

## 03 – Notes & Decisions

- MI is the **only authority** for predictive models in IFNS; ad-hoc models outside the Model Registry are not allowed to influence decisions.
- The Model Registry schema should be treated as a core contract: changes to its structure require careful coordination with Stage 3–5 components and SxE surfaces.
- Calibration and robustness metrics are first-class citizens in MI. They must be available in Mirror and Admin so that model decisions can be judged not only by returns but also by reliability and behavior under stress.
- As IFNS expands, new model families should be added by:
  - Extending the Model Families table,
  - Adding new training specs,
  - Ensuring SxE views and promotion policies are updated accordingly.
- SEL logic will build on top of MI’s artifacts and events. This step should be revisited when advanced SEL capabilities (e.g., automated retraining triggers, multi-model arbitration policies) are formally introduced.
