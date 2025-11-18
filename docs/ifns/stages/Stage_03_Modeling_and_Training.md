# Stage 03 – Modeling & Training

## 01 – Narrative & Intent

This document defines **Stage 03 – Modeling & Training** for the Intelligent Financial Neural System (IFNS).

Conceptually, this stage **implements** the Modeling Intelligence (MI) layer described in:

- Step 08 – Modeling Intelligence (MI)
- Step 11 – Model & Signal Integration (MSI) (for roles and signal contracts)
- Step 13 – Self-Evaluation & Learning (SEL) (for evidence and learning loops)

Stage 03 answers:

- What **model families** do we support, and what roles do they play?
- How are models **registered, versioned, and stored**?
- How do we use Stage 02 datasets and labels for **training and evaluation**?
- What are our **metrics, baselines, and promotion criteria** before a model can move towards MSI/DRA?
- How do we keep training runs **reproducible and auditable**?

The outcome of Stage 03 is a **governed modeling layer** that can:

- Train and evaluate models on Stage 02 datasets,
- Publish models into a **Model Registry**,
- Feed **model signals** consistently to MSI and downstream stages.

---

## 02 – Scope & Responsibilities

Stage 03 covers:

1. **Model Families & Roles**
   - Definition of model families (by algorithm, objective, and data usage).
   - Assignment of roles (primary directional, confirmation, risk overlay, structure-aware overlay, etc.).

2. **Model Registry & Artifacts**
   - Logical and physical structure of the Model Registry.
   - Where trained models live on disk or in storage.
   - Metadata and status (candidate, canary, promoted, retired).

3. **Training Data Contracts**
   - Use of Stage 02 Dataset IDs and feature/label versions.
   - Rules for training/validation/test splits and evaluation horizons.

4. **Training & Evaluation Workflow**
   - How experiments are defined.
   - How training jobs are run, logged, and summarized.
   - How evaluation metrics are computed and stored.

5. **Experiment Log & Reproducibility**
   - Experiment identifiers and metadata.
   - Configuration capture (hyperparameters, feature sets, label sets).
   - Links to results and artifacts.

6. **SxE Representation**
   - What Mirror/Admin can see about model families, experiments, and performance.

Stage 03 does **not** define:

- How model signals are combined (MSI – Stage 11 spec, Stage 05 build).
- How decisions are taken (DRA – Stage 05).
- How signals are used in backtests (Stage 04) beyond basic contracts.

Its job is to ensure **models are properly trained, evaluated, and registered**.

---

## 03 – Model Families & Roles

### 3.1 Model Families

A **model family** groups models that share:

- Algorithmic backbone (e.g., tree-based, linear, neural network),
- Objective (e.g., directional classification, return regression, risk estimation),
- Input feature and label families.

Examples:

- `MF_DIR_CORE_V1` – core directional models (classification).
- `MF_RET_CORE_V1` – return regression models.
- `MF_RISK_VOL_V1` – volatility/risk estimators.
- `MF_STRUCT_AWARE_V1` – structure-aware overlays using STRUCTURE_MTF and REGIME_TAGS.
- `MF_EXEC_COST_V1` – transaction cost or slippage models.

Each family is defined in the Model Registry (see Section 04) with:

- `family_id`,
- Description,
- Input data requirements (Dataset/feature/label dependencies),
- Intended role(s),
- Supported environments (e.g., offline/paper/live for inference).

### 3.2 Model Roles

Roles reflect how MSI and DRA will treat models:

- **Primary Directional** – drive trade direction when other conditions are met.
- **Confirmation** – confirm or veto primary signals (e.g., require agreement).
- **Risk Overlay** – estimate volatility, drawdowns, or tail risk for sizing and envelopes.
- **Structure-Aware Overlay** – modulate signals based on structural context (MSA).
- **Execution & Cost** – feed EI with cost and slippage estimates.

Each model entry includes its `role` (or roles), which MSI uses to decide:

- Which models to consult for a given decision,
- How to weight or gate their outputs.

Stage 03 ensures roles are **explicit metadata**, not implicit assumptions.

---

## 04 – Model Registry & Artifacts

### 4.1 Registry Location & Format

The **Model Registry** lives under:

```text
data/registry/model_registry.json
```

(or equivalent structured store), with supporting artifacts under:

```text
models/
  <family_id>/
    <model_id>/
      model.bin (or framework-native artifact)
      config.json
      metrics.json
      …
```

Each **model record** in the registry includes fields such as:

- Identifiers:
  - `model_id`,
  - `model_family`,
  - `model_version`.
- Status & Lifecycle:
  - `status` (e.g., `candidate`, `canary`, `promoted`, `retired`),
  - `created_ts`, `last_updated_ts`,
  - Links to experiments (`experiment_id`).
- Inputs:
  - Required Dataset ID(s),
  - Feature framework versions,
  - Label versions.
- Outputs:
  - Prediction type (classification/regression/probabilities),
  - Supported horizons.
- Performance:
  - Key evaluation metrics (e.g., Sharpe, hit rate, TE, calibration metrics) on standardized validation/test sets.
- Operational:
  - Supported environments for inference (offline/paper/live),
  - Resource requirements (rough sizing).

The registry is the **single source of truth** for which models exist and how they can be used.

### 4.2 Model Artifacts

For each `model_id`, there is a corresponding artifact folder with:

- **Serialized model** (`model.bin`, `model.pth`, etc.).
- **Training config** (`train_config.json`):
  - Hyperparameters,
  - Feature/label set definitions,
  - Dataset ID and ranges.
- **Evaluation results** (`metrics.json`, `curves/`, etc.):
  - Aggregated metrics,
  - Optional per-regime metrics,
  - Calibration and reliability diagrams if applicable.

Stage 03 does not prescribe the ML framework (e.g., scikit-learn, PyTorch); it prescribes the **artifact contract**.

---

## 05 – Training Data & Label Contracts

Stage 03 **must** consume datasets defined in Stage 02.

### 5.1 Dataset References

For each model, we reference:

- `train_dataset_id` – e.g., `DS_TRAIN_CORE_V1`.
- `val_dataset_id` – e.g., `DS_VAL_CORE_V1` or `DS_TRAIN_CORE_V1` with split metadata.
- `test_dataset_id` – e.g., `DS_TEST_CORE_V1` or a specific holdout dataset.

Dataset IDs correspond to entries in:

```text
data/registry/datasets_index.json
```

and Stage 02 tables.

### 5.2 Feature & Label Families

Models must specify which feature and label families they use, e.g.:

- `features_used`:
  - `Feature_TREND_MTF_V1`,
  - `Feature_VOL_LIQ_V1`,
  - Optional `Feature_STRUCTURE_MTF_V1`, etc.

- `labels_used`:
  - `Label_Direction_Horizon_20d_V1`,
  - or `Label_ReturnContinuous_Horizon_20d_V1`.

This ensures:

- Consistent and traceable use of features/labels.
- Easy inspection in Admin for **“which models depend on which data definitions?”**

---

## 06 – Training & Evaluation Workflow

### 6.1 Training Pipelines

Training code lives under:

```text
pipelines/training/
```

Typical pattern:

1. Load experiment configuration (including Dataset IDs, feature/label sets, hyperparameters).
2. Resolve datasets via Stage 02 (using Data & Feature Service).
3. Train model, log intermediate metrics.
4. Evaluate on validation and/or test sets.
5. Write:
   - Trained model artifact,
   - `metrics.json`,
   - Experiment Log entry,
   - Model Registry entry (or update).

### 6.2 Experiment Configuration

Experiments can be defined via configurations under:

```text
config/training/
  exp_<name>.yaml
```

Each experiment config includes:

- `experiment_id` (or generated from name + timestamp).
- Model family and role.
- Dataset IDs and time windows.
- Feature and label sets.
- Hyperparameters and training schedule.
- Evaluation metrics to compute and thresholds for “success”.

### 6.3 Evaluation

Evaluation must be:

- **Consistent across experiments** in the same family.
- **Regime-aware** where appropriate:
  - Metrics broken down by `regime_tag`, structural states, volatility bands.

Outputs are stored in:

- `data/registry/experiments_log.json` (summary),
- `models/<family>/<model_id>/metrics.json` (detailed).

---

## 07 – Metrics & Evaluation Standards

Stage 03 defines **standard metrics** and **minimum expectations** for models.

### 7.1 Core Metrics (Directional / Return Models)

Typical metrics for trading-oriented models:

- **Directional models (classification)**
  - Hit rate (`accuracy` on directional label).
  - Precision/recall (for specific label subsets).
  - Calibration metrics (Brier score, reliability curves).
  - TE or realized performance proxies in backtest-style evaluation (if available).

- **Return models (regression)**
  - R² or correlation with future returns.
  - Error metrics (RMSE/MAE).
  - Rank correlation (for ranking-based strategies).

These are always reported at **aggregate level** and, where possible:

- By symbol cluster,
- By regime (`regime_tag`),
- By structural state.

### 7.2 Risk & Stability Metrics

Beyond performance, Stage 03 recommends stability metrics:

- Sensitivity to small changes in training data (e.g., rolling-window evaluations).
- Stability of outputs across regimes and time.
- Model complexity indicators (feature count, parameter count).

These feed into SEL (Stage 13) and DRA (Stage 05) when deciding on promotions or rollbacks.

### 7.3 Promotion Thresholds (Pre-DRA)

Stage 03 may define preliminary **“good enough to consider for promotion”** criteria, such as:

- Minimum improvement vs. baseline (e.g., naive model or simple heuristic).
- Performance robustness across regimes (no catastrophic weakness).
- Calibration quality above defined thresholds.

Final promotion decisions are made through DRA (Stage 05), but Stage 03 sets **technical expectations**.

---

## 08 – Experiment Log & Reproducibility

### 8.1 Experiment Log

The **Experiment Log** lives under:

```text
data/registry/experiments_log.json
```

(or a table/CSV), with entries like:

- `experiment_id`,
- `timestamp`,
- `model_family`,
- `proposed_model_id`,
- Datasets, features, labels used,
- Hyperparameters (or a hash + link to config),
- Key metrics (val/test),
- Status (`completed`, `failed`, `selected`, `discarded`),
- Links to artifacts.

This log is the **primary evidence source** for SEL and DRA.

### 8.2 Reproducibility Rules

Stage 03 sets rules to ensure any trained model can be **reproduced**:

- Every `model_id` must be linked to exactly one `experiment_id`.
- Every `experiment_id` must have:
  - A config file or blob,
  - Dataset IDs and time ranges,
  - Versioned feature/label families.

If any of these pieces are missing, the model is considered **non-compliant** and ineligible for promotion to production use.

---

## 09 – SxE Representation of Stage 03

### 9.1 Mirror (Read-Focused)

Mirror surfaces:

- **Model Family Overview**
  - List of families and roles.
  - Count of models per status (candidate/canary/promoted/retired).
- **Model Performance Panels**
  - Key metrics per model and family.
  - Regime/structure breakdowns (optional in later iterations).
- **Experiment Timeline**
  - Recent experiments, their outcomes, and associated metrics.

### 9.2 Admin (Control-Focused)

Admin provides:

- **Model Registry Console**
  - View models and their statuses.
  - Inspect metadata, datasets, and metrics.
  - Manually flag models for consideration (promotion/rollback proposals to DRA).

- **Experiment Log Console**
  - Search experiments by family, date, status.
  - Drill into configs and detailed metrics.
  - Link experiments to SEL recommendations and DRA decisions.

Stage 03 itself does **not** grant promotion/rollback powers; it provides **visibility and evidence** for those decisions.

---

## 10 – Notes & Decisions

- Stage 03 is the **single source of truth** for model definitions and experimental evidence.
  - MSI, DRA, and SEL must reference models via the Model Registry, **not** ad-hoc identifiers.
- Models must always be tied to Stage 02 datasets and features:
  - No direct usage of raw data inside models without going through canonical tables and feature frameworks.
- Promotion/rollback decisions:
  - Are not taken automatically in Stage 03; they require DRA (Stage 05) and SEL (Stage 13) workflows.
  - However, Stage 03 must record **enough evidence** to support those decisions.
- As IFNS evolves to more asset classes and strategies:
  - New model families can be added as new `model_family` IDs.
  - Stage 03 should be extended with family-specific metrics or evaluation nuances, while preserving the core contracts defined here.

Stage 03 thus turns the conceptual Modeling Intelligence (MI) into a **disciplined modeling factory**, where models are trained, evaluated, and registered in a transparent, reproducible way for the rest of IFNS to consume.
