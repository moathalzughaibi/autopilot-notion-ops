# Stock Indicator System — Phase 7 ML Integration & Operationalization
Version: v0.1 (Draft)

## 1. Purpose

Phase 7 describes **how the indicator and feature platform plugs into ML and live trading**. It assumes
Phases 1–6 are available and focuses on:

- How features flow into **training**, **backtesting**, and **live inference**.
- How models are **versioned, evaluated, and promoted**.
- How indicator/feature changes are coordinated with **model lifecycle and governance**.
- How to keep the system **observable and safe** in production.

This document is a **conceptual and architectural spec** for the “last mile” between the Indicators
System and the trading/autopilot stack.


---

## 2. Reference Artifacts from Earlier Phases

Phase 7 treats the following as **inputs**:

- Phase 3 — `indicators_catalog_L1.csv`
- Phase 4 — `indicators_catalog_L2L3.csv`
- Phase 5 — `indicator_feature_schema_v1.csv`
- Phase 6 — Implementation Templates (Indicator Engine + Feature Service)

From the ML perspective, these artifacts define:

- **What can be computed** (indicators & frameworks).
- **What can be exposed as features** (feature schema & packs).
- **How** they are computed and served (Phase 6 runtime).


---

## 3. ML Data Flow Overview

At a high level, the ML data flow is:

1. **Raw Data → Indicator Engine**
   - Bars, fundamentals, events, portfolio data.
   - L1/L2/L3 indicators computed per symbol/timeframe.

2. **Indicator Engine → Feature Service**
   - Indicator outputs transformed into feature columns using `indicator_feature_schema_v1.csv`.
   - Features materialized into **Feature Views** (e.g., `core_pack_1h`, `core_pack_1d`).

3. **Feature Views → ML Pipelines**
   - Training datasets for models.
   - Feature sets for backtesting engines.
   - Live feature snapshots for inference.

4. **Models → Strategies / Autopilot**
   - Model scores feed strategy logic (entry/exit, sizing, risk adjustments).
   - Strategies are monitored, with performance fed back into the ML loop.

The **Indicator System** is therefore the **canonical feature factory** for IFNS.


---

## 4. Feature Packs and Model Recipes

### 4.1 Feature Packs

Phase 5 defines **feature packs** as configurations (subsets of rows in `indicator_feature_schema_v1.csv`):

- `core_value_v1`
- `core_state_v1`
- `core_event_v1`
- `core_episode_v1`
- `core_vector_v1` (optional/advanced)

In Phase 7, packs are:

- The **contract** between the Feature Service and ML pipelines.
- Versioned entities (e.g., `core_value_v1`, `core_value_v2`) independent of individual indicators.


### 4.2 Model Recipes

Each model defines a **recipe** specifying:

- `feature_pack_ids` — which packs to include (e.g., `["core_value_v1","core_state_v1"]`).
- Optional additional feature overrides:
  - Include/exclude particular features.
  - Transformations (e.g., lags, moving averages on features).
- Label definition:
  - Target horizon (e.g., 1-day return, 20-bar forward Sharpe).
  - Label construction rules.
- Universe constraints:
  - Which symbols, markets, regimes, or strategies it serves.

Conceptually:

```text
ModelRecipe:
    id: "equity_intraday_momentum_v1"
    feature_packs: ["core_value_v1","core_state_v1","core_event_v1"]
    extra_features: ["sr_zone_v1_distance_to_nearest_support_value"]
    label_spec: { horizon_bars: 20, target: "forward_return", transform: "sign" }
    universe_spec: { asset_class: "equity", min_volume: X, regions: ["US"] }
```

These recipes are stored in a **Model Registry** (see Section 6).


---

## 5. Training & Backtesting Pipelines

### 5.1 Training Data Construction

For a given model recipe:

1. **Request Features**
   - Use Feature Service to pull feature views according to `feature_packs` and `default_timeframe`.
   - Restrict to training period and universe.

2. **Generate Labels**
   - Use price series to compute forward returns / classification targets as per `label_spec`.

3. **Align & Clean**
   - Align features and labels by timestamp/symbol.
   - Apply missing policies at feature level (already defined in Phase 5).
   - Drop or mask rows failing quality checks.

4. **Train/Test Split & Cross-Validation**
   - Use time-based splits (e.g., rolling windows) to avoid look-ahead bias.
   - Configure cross-validation in the ML pipeline (outside the indicator system).


### 5.2 Backtesting with Indicator-Based Features

Backtesting engines consume the **same feature outputs** as models, but may use different windows or
aggregation strategies.

Workflow:

1. **Choose strategy** (e.g., “RSI-based intraday mean reversion”).  
2. **Specify feature usage** (e.g., `rsi_14_value`, `trend_state_mtf`, `vol_regime_state`).
3. **Use Feature Service** to retrieve feature time-series aligned with backtest data.
4. **Run strategy logic** using those features.
5. **Log performance metrics** and regime-sliced views (by trend, vol, event state).

Because indicators and features are **centralized and versioned**, backtests become **reproducible**:

- Change an indicator or feature schema → version bump.
- Old experiments stay pinned to old versions.


---

## 6. Model Registry & Versioning

The **Model Registry** tracks:

- Model ID (e.g., `equity_intraday_momentum_v1`).
- Version (`v1`, `v2`, etc.).
- Associated feature packs and schemas:
  - `feature_schema_version` (e.g., `indicator_feature_schema_v1`).
  - Indicator catalogs (`L1_v1`, `L2L3_v1`).
- Training metadata:
  - Time period.
  - Universe and filters.
  - Hyperparameters.
  - Performance metrics (train/validation/test).

### 6.1 Indicator & Feature Compatibility

To avoid silent breakage:

- Every model version declares the **expected schema version**.
- If indicators or features change, either:
  - Keep schema backward-compatible (additive changes), or
  - Bump schema version and create a **new model version** pinned to the new schema.

This enforces a **clean boundary** between feature evolution and model reproducibility.


---

## 7. Live Inference & Strategy Integration

### 7.1 Live Feature Serving

At inference time, models request **as-of features** via the Feature Service:

```text
features = FeatureService.get_features(
    symbols = [...],
    as_of   = now,
    pack_id = "core_v1",
    time_horizon = "1h"
)
```

- Features are computed from **current indicator outputs**.
- The same `missing_policy` and aggregation rules from Phase 5 apply.

### 7.2 Model Scoring

For each model:

1. Retrieve the appropriate **feature pack** from Feature Service.
2. Run the model to obtain scores:
   - e.g., expected return, probability of up move, risk adjustment factors.
3. Optionally apply **post-processing**:
   - Score clipping.
   - Neutralization (sector/market-neutral).
   - Blending across models.

### 7.3 Strategy Execution

Strategies use model outputs and raw indicators to:

- Decide **entry/exit** trades.
- Set **position sizes** based on volatility, liquidity, and risk budgets.
- Respect **gates** from risk frameworks:
  - `stress_state_v1`
  - `liq_stress_v1`
  - `risk_budget_util_v1`
  - `vol_regime_state_v1`

The exact strategy logic is outside this document, but **inputs are standardized** via the indicator and
feature system.


---

## 8. Governance, Safety & Change Management

### 8.1 Change Types

There are three main classes of change:

1. **Indicator/Feature Changes**
   - Adding new indicators.
   - Changing formulas or parameters.
   - Changing feature definitions or packs.

2. **Model Changes**
   - New model versions.
   - Hyperparameter updates.
   - Feature set modifications.

3. **Policy/Risk Changes**
   - New gates and thresholds using indicators (e.g., stricter `stress_state` policies).
   - Changes to allowed leverage or exposure.

### 8.2 Governance Rules (Conceptual)

- **Version everything**: indicators, feature schema, feature packs, models.
- **No “in-place” changes** to semantics used by live models without:
  - New version IDs.
  - Validation and approval.
- Changes should be recorded in an **IFNS Decisions Log** with:
  - Before/after specs.
  - Reasoning and expected impact.
  - Backtesting or A/B evidence.

### 8.3 Safe Rollout Procedures

For critical changes:

1. Deploy new models in **paper trading** first (or reduced size).
2. Use the same Feature Service and indicators as live to avoid mismatch.
3. Compare performance and telemetry vs current live models.
4. Promote to live only after acceptable behavior is observed.

Indicator/feature changes may require:

- Backfilling data for new fields.
- Re-training or at least re-evaluating affected models.


---

## 9. Telemetry & Observability for ML

### 9.1 Feature-Level Telemetry

For each feature (Phase 5 row), track:

- **Fill rate** and missing patterns.
- **Distribution summaries** (mean, std, quantiles).
- **Drift metrics** vs historical windows.

If a feature drifts or degrades:

- Tag the event in telemetry.
- Optionally auto-trigger investigations or mark model runs as suspect.


### 9.2 Model-Level Telemetry

Per model and version:

- Input feature quality stats (subset of the above).
- Online performance metrics:
  - Hit rate, PnL contribution, drawdowns.
- Regime-sliced performance:
  - By `trend_state_mtf`, `vol_regime_state`, `regime_cluster_id`, `event_window_state`, etc.

This closes the loop between:

- Indicators/Features → Models → Outcomes → Back to Indicators/Features.


---

## 10. Handover Checklist for Phase 7

For the ML / Autopilot integration team, the checklist is:

1. **Feature Packs & Recipes**
   - Implement pack selection based on `indicator_feature_schema_v1.csv`.
   - Implement model recipes that reference packs and label specs.

2. **Training Pipelines**
   - Build data assembly from Feature Service + label construction.
   - Integrate with existing ML frameworks (e.g., scikit-learn, XGBoost, deep learning).

3. **Backtesting Integration**
   - Make backtest engines consume feature views produced by the Feature Service.
   - Log regime-sliced results based on Phase 4 frameworks.

4. **Model Registry**
   - Implement a registry for model versions, feature schema versions, and training metadata.
   - Enforce compatibility between schema versions and models.

5. **Live Serving**
   - Use Feature Service for real-time feature retrieval.
   - Wire models to strategies and risk gates.

6. **Governance & Monitoring**
   - Implement decision logs for changes in indicators, features, and models.
   - Implement telemetry for data quality, feature drift, and model behavior.

With Phase 7 in place, the Stock Indicator System is **fully integrated** into the ML and trading stack,
with clear boundaries, versioning, and observability from raw data all the way to live decisions.
