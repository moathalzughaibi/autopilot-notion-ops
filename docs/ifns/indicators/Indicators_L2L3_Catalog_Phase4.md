# Stock Indicator System — Phase 4 L2/L3 Framework Catalog
Version: v0.1 (Draft)

## 1. Purpose

This Phase 4 document defines the **L2/L3 Framework Catalog** for the Stock Indicator System under IFNS.
It builds directly on:

- Phase 1 — Taxonomy & Governance (families, levels, output types, digitization levels).
- Phase 2 — Indicator Universe Draft (concept list across all families).
- Phase 3 — L1 Indicator Catalog (atomic, formula-based indicators).

In Phase 4 we formalize **composite indicators and frameworks** (L2/L3) that:

- Combine one or more L1 indicators.
- Implement **rules**, **state machines**, or **ML-based pattern detectors**.
- Produce **context states**, **events**, **episodes**, or **high-level scores** that the rest of the IFNS
  uses for regime awareness, structure, execution, and risk control.

This catalog is represented as:

- A human-readable Markdown spec (this file).
- A machine-usable CSV: `sync/ifns/indicators_catalog_L2L3.csv` (Phase 4 artifact).


---

## 2. Scope and Design Principles

### 2.1 In-Scope for Phase 4

- All **L2** and **L3** indicators from the Phase 2 universe that are considered **v1 frameworks**, including:
  - Multi-timeframe trend and structure engines.
  - Volatility and liquidity regimes.
  - Candle pattern detectors and grammar frameworks.
  - Event/regime state machines.
  - Fundamental and macro regime composites.
  - Risk and stress state frameworks.

The goal is not to list every possible future framework, but to define a **clean v1 core set** that is:

- Sufficient for a serious first-generation trading system.
- Modular and easily extendable.
- Explicit about dependencies on L1 indicators and external data.

### 2.2 Out-of-Scope

- Detailed feature column schemas for each output (Phase 5).
- Full ML training recipes and experiment designs (will reference IFNS modeling and telemetry specs).
- Implementation code in any specific language (Phase 6 will cover templates and patterns).


---

## 3. Catalog Schema (L2/L3)

The L2/L3 catalog is stored as a CSV table with the following columns:

| Column name               | Type   | Description |
|---------------------------|--------|-------------|
| `indicator_id`            | string | Stable ID (e.g., `trend_mtf_v1`, `candle_grammar_v1`). |
| `name`                    | string | Human-readable name. |
| `family_role_primary`     | string | Primary family (Trend, Market Structure, etc.). |
| `family_role_secondary`   | string | Optional secondary family. |
| `level`                   | enum   | `L2` or `L3`. |
| `universe_tier`           | int    | Tier from Phase 2 (0 core, 1 strong candidate, 2 exploratory). |
| `digitization_level`      | enum   | `formula`, `rule`, or `ml_pattern`. |
| `construction_type`       | enum   | `aggregation`, `state_machine`, `pattern_engine`, `composite_score`. |
| `dependencies_L1`         | string | Comma-separated list of `indicator_id`s for L1 dependencies. |
| `dependencies_external`   | string | Extra data or labels needed (e.g., microstructure, macro, labels). |
| `inputs`                  | string | High-level domains required (price, volume, events, fundamental, portfolio, macro). |
| `output_type_primary`     | enum   | scalar, oscillator, category, flag, vector, episode. |
| `output_components`       | string | JSON-style description of sub-outputs (states, scores, episode fields). |
| `default_timeframes`      | string | JSON-style list of timeframes. |
| `pattern_window`          | string | JSON-style description of lookback/forward windows (where relevant). |
| `state_space_def`         | string | JSON-style description of possible states (for categorical outputs). |
| `ml_role_primary`         | enum   | feature, context, risk, filter, label. |
| `ml_role_secondary`       | string | Additional roles, if any. |
| `backtest_hooks`          | string | JSON-style description of backtest metrics/uses. |
| `feature_outputs_default` | string | JSON-style description of default feature outputs (value/state/events). |
| `notes_phase4`            | string | Implementation and governance notes. |

This schema is designed to be:

- Rich enough to describe complex frameworks.
- Simple enough to serve as a configuration source for engineering and backtesting tools.
- Compatible with Notion and with IFNS Admin/feature governance views.


---

## 4. Key Frameworks by Family

Below we define the **v1 core set** of L2/L3 frameworks. Each one has a corresponding row in
`indicators_catalog_L2L3.csv` with structured metadata.

### 4.1 Trend & Price Location

#### 4.1.1 `trend_mtf_v1` — Multi-Timeframe Trend Framework

**Intent:** Provide a **discrete trend state** across multiple timeframes (e.g., short, medium, long), as well as a
numeric strength score.

- **Level:** L3
- **Digitization:** `rule`
- **Construction type:** `state_machine`
- **Primary family:** Trend & Price Location
- **Secondary family:** Market Structure & Geometry

**Dependencies (L1):**

- `ema_12`, `ema_26`, `ema_50`
- `sma_20`, `sma_50`
- `price_location_20`
- `atr_14` (for noise filtering, optional)

**Outputs:**

- `trend_state_mtf` — categorical, e.g. `{ "strong_up", "up", "sideways", "down", "strong_down" }`.
- `trend_score_mtf` — scalar score in [-1,1] summarizing multi-timeframe alignment.
- Optional per-timeframe states (short/medium/long).

**Logic (high level):**

- For each timeframe (e.g., 15m, 1h, 1d):
  - Evaluate MA slopes (e.g., EMA(12), EMA(26), EMA(50)).
  - Check MA ordering and price vs MAs.
  - Classify local state as up/sideways/down.
- Aggregate across timeframes:
  - Count up/down states, weight by timeframe importance.
  - Map to final `trend_state_mtf` and `trend_score_mtf`.
- Smooth transitions to avoid whipsaw (e.g., require persistence for state changes).

**Roles:**

- `ml_role_primary = context`
- `ml_role_secondary = feature, filter`

**Usage:**

- Slicing backtests by trend regimes.
- Conditioning strategy activation.
- As context features in models (one-hot/embedding of trend state).


---

### 4.2 Market Structure & Geometry

#### 4.2.1 `structure_mtf_v1` — Multi-Timeframe Structure Framework

**Intent:** Provide a **hierarchical structure view** (minor/primary/major swings) and a categorical structure state
(HH/HL vs LH/LL etc.).

- **Level:** L3
- **Digitization:** `rule`
- **Construction type:** `state_machine`
- **Primary family:** Market Structure & Geometry
- **Secondary family:** Trend & Price Location

**Dependencies (L1):**

- `swing_high_5`, `swing_low_5`
- `range_high_20`, `range_low_20`
- Optionally `atr_14` for significance tests.

**Outputs:**

- `structure_state_mtf` — category (e.g. `{ "up_structure", "down_structure", "sideways_structure", "transition" }`).
- `swing_tier_labels` — categorical labels for swings: `{ "minor", "primary", "major" }`.
- Optional per-tier episode info (start/end of major swings).

**Logic (high level):**

- Detect swing highs/lows at multiple scales (e.g., 5-bar, 20-bar, 60-bar windows).
- Tag swings with tiers using volatility and distance thresholds.
- Infer HH/HL vs LH/LL relationships among swings.
- Map structure regime based on recent sequence (e.g., series of HH+HL → up_structure).

**Roles:**

- `ml_role_primary = context`
- `ml_role_secondary = feature`

**Usage:**

- Structural slicing of backtests.
- Stop/target placement logic (stops below swings, targets near structural levels).
- Context features for ML models.


#### 4.2.2 `sr_zone_v1` — Support/Resistance Zones

**Intent:** Detect **price zones** that act as support or resistance, with associated strength scores and episode spans.

- **Level:** L3
- **Digitization:** `rule`
- **Construction type:** `pattern_engine`
- **Primary family:** Market Structure & Geometry

**Dependencies (L1):**

- `range_high_20`, `range_low_20`
- `swing_high_5`, `swing_low_5`
- `volume`, `vol_sma_20` (optional weighting)
- Optionally `atr_14` for zone width scaling.

**Outputs:**

- Episode-style zone records:
  - `zone_id`
  - `zone_type ∈ {support,resistance}`
  - `price_low`, `price_high`
  - `strength_score` (0–1)
  - `first_touch_ts`, `last_touch_ts`
  - `touch_count`

**Logic (high level):**

- Aggregate clusters of swings and highs/lows around similar price regions.
- Define zone width in terms of ATR or percentage bands.
- Track touch events and update `strength_score` based on touches and rejections.
- Emit episodes per zone, eventually turning into features like “distance to nearest strong support”.

**Roles:**

- `ml_role_primary = context`
- `ml_role_secondary = feature, risk`

**Usage:**

- Confluence zones for entries and exits.
- Risk anchoring and sizing (size down near strong resistance, etc.).


#### 4.2.3 `breakout_flag_v1` — Structural Breakout Flags

**Intent:** Emit **event flags** for breakouts/breakdowns relative to significant ranges or SR zones.

- **Level:** L2
- **Digitization:** `rule`
- **Construction type:** `pattern_engine`
- **Primary family:** Market Structure & Geometry
- **Secondary family:** Trend & Price Location

**Dependencies (L1/L3):**

- `range_high_20`, `range_low_20`
- Optionally `sr_zone_v1` zone boundaries.

**Outputs:**

- `breakout_flag_up` (binary).
- `breakout_flag_down` (binary).
- Optional confidence/quality score.

**Logic (high level):**

- Define recent consolidation/range (e.g., 20-bar range with volatility constraints).
- Trigger breakout if close/true_range breaches upper/lower bounds by a threshold (e.g., > x * ATR).
- Optionally require confirmation (e.g., close outside for N bars).

**Roles:**

- `ml_role_primary = filter`
- `ml_role_secondary = context`

**Usage:**

- Entry triggers for breakout strategies.
- Event markers in backtests.


---

### 4.3 Volatility & Range

#### 4.3.1 `vol_regime_state_v1` — Volatility Regime Classifier

**Intent:** Classify volatility into **discrete regimes** for easier policy and model conditioning.

- **Level:** L3
- **Digitization:** `rule`
- **Construction type:** `state_machine`
- **Primary family:** Volatility & Range
- **Secondary family:** Event & Regime

**Dependencies (L1):**

- `atr_14`
- `realized_vol_20`

**Outputs:**

- `vol_regime_state` — category (e.g. `{ "calm", "normal", "stressed" }`).

**Logic (high level):**

- Compute long-run baseline volatility per symbol/timeframe.
- Define thresholds for low/normal/high vol (e.g., quantiles or multiples of baseline).
- Map current ATR/realized_vol values to regimes with hysteresis to avoid chattering.


**Roles:**

- `ml_role_primary = context`
- `ml_role_secondary = filter`

**Usage:**

- Conditioning strategies (e.g., only run some models in calm or normal regimes).
- Slicing performance metrics.


---

### 4.4 Volume / Flow / Liquidity

#### 4.4.1 `liq_stress_v1` — Liquidity Stress Score

**Intent:** Provide a **composite stress score** capturing illiquidity and trading cost risk.

- **Level:** L3
- **Digitization:** `ml_pattern` (though can start with rules)
- **Construction type:** `composite_score`
- **Primary family:** Volume / Flow / Liquidity
- **Secondary family:** Risk & Exposure

**Dependencies (L1/L2):**

- `volume`, `vol_sma_20`
- `spread_bp`
- `ofi_20`
- `depth_imbalance_1` (if order book data available)
- Possibly `true_range`/`atr_14` (for volatility adjustment)

**Outputs:**

- `liq_stress_score` — scalar (e.g. 0–1 or z-score).
- `liq_stress_state` — category `{ "normal", "tight", "stressed" }`.

**Logic (high level):**

- Start with rule-based features: standardized spread, volume deviation, depth imbalance, etc.
- Optionally train an ML model (e.g., gradient boosting) to map features to stress labels derived from
  historical cost slippage outcomes.
- For v1, a linear/rule-based composite score can be used until ML calibration is complete.

**Roles:**

- `ml_role_primary = risk`
- `ml_role_secondary = context, filter`

**Usage:**

- Throttling or blocking trading in stressed conditions.
- Execution algorithm selection.


---

### 4.5 Candle Grammar & Micro-Patterns

#### 4.5.1 `candle_pattern_basic_v1` — Classic Single-Candle Pattern Flags

**Intent:** Flag **classic, interpretable candlestick patterns** based on simple rules.

- **Level:** L2
- **Digitization:** `rule`
- **Construction type:** `pattern_engine`
- **Primary family:** Candle Grammar & Micro-Patterns
- **Secondary family:** Market Structure & Geometry

**Dependencies (L1):**

- `candle_body_pct`
- `upper_wick_pct`
- `lower_wick_pct`
- `close_pos_pct`

**Outputs:**

- Flags like:
  - `is_doji`
  - `is_pinbar_bull`, `is_pinbar_bear`
  - `is_hammer`, `is_shooting_star`
  - `is_strong_bull`, `is_strong_bear`

**Logic (high level):**

- For each pattern, define thresholds on body_pct, wick_pct, and close_pos_pct.
- Emit binary flags when conditions match.
- Optionally track pattern quality based on volatility or structure context.

**Roles:**

- `ml_role_primary = feature`
- `ml_role_secondary = context`

**Usage:**

- Micro-entry hints and pattern-aware strategies.
- As explanatory features in ML models.


#### 4.5.2 `multi_candle_pattern_v1` — Two- and Three-Candle Patterns

**Intent:** Flag **multi-candle patterns** (e.g., engulfing, morning star) based on sequences of L1 candle features.

- **Level:** L2
- **Digitization:** `rule`
- **Construction type:** `pattern_engine`
- **Primary family:** Candle Grammar & Micro-Patterns
- **Secondary family:** Market Structure & Geometry

**Dependencies (L1/L2):**

- Same as `candle_pattern_basic_v1`.
- Previous-candle pattern flags.

**Outputs:**

- Flags like:
  - `is_engulfing_bull`, `is_engulfing_bear`
  - `is_morning_star`, `is_evening_star`

**Logic (high level):**

- Define pattern requirements using prior and current candle attributes (body, wick, close position).
- For example, bullish engulfing requires current body covering prior body with opposite direction, etc.

**Roles:**

- `ml_role_primary = feature`
- `ml_role_secondary = context`


#### 4.5.3 `candle_embedding_v1` — Learned Candle Embedding

**Intent:** Provide a **vector representation** of the last N candles capturing shape and micro-structure in a dense space.

- **Level:** L3
- **Digitization:** `ml_pattern`
- **Construction type:** `pattern_engine`
- **Primary family:** Candle Grammar & Micro-Patterns

**Dependencies (L1):**

- Raw OHLC data and/or L1 candle features (`candle_body_pct`, `upper_wick_pct`, `lower_wick_pct`, `close_pos_pct`).

**Outputs:**

- `candle_embedding` — fixed-length vector (e.g., 16D or 32D).

**Logic (high level):**

- Train a sequence model (CNN/transformer) on raw OHLC or normalized candle features over a window (e.g., last 20 bars).
- Use the last hidden representation as the embedding.

**Roles:**

- `ml_role_primary = feature`
- `ml_role_secondary = context`

**Usage:**

- Input representation for advanced ML models.
- Basis for clustering into discrete micro-pattern states.


#### 4.5.4 `candle_cluster_id_v1` — Candle Cluster ID

**Intent:** Map `candle_embedding_v1` vectors into **discrete micro-pattern states**.

- **Level:** L3
- **Digitization:** `ml_pattern`
- **Construction type:** `pattern_engine`
- **Primary family:** Candle Grammar & Micro-Patterns

**Dependencies (L3):**

- `candle_embedding_v1`

**Outputs:**

- `candle_cluster_id` — integer category ID.
- Optional cluster-level descriptors (e.g., “strong reversal”, “drift”, etc.).

**Logic (high level):**

- Run unsupervised clustering (e.g., k-means, GMM) on embeddings.
- Assign cluster IDs to each time step.
- Optionally label clusters qualitatively after manual review.

**Roles:**

- `ml_role_primary = context`
- `ml_role_secondary = feature`

**Usage:**

- Discrete context labels for models.
- Slicing backtests by micro-pattern states.


---

### 4.6 Valuation & Fundamentals

#### 4.6.1 `fund_quality_score_v1` — Fundamental Quality Score

**Intent:** Provide a **single composite quality score** from multiple fundamental metrics.

- **Level:** L3
- **Digitization:** `ml_pattern` (eventually; can start as weighted formula)
- **Construction type:** `composite_score`
- **Primary family:** Valuation & Fundamentals
- **Secondary family:** Risk & Exposure

**Dependencies (L1):**

- `pe_ttm`, `pb`, `div_yield`
- `eps_growth_yoy`, `rev_growth_yoy`
- `debt_to_equity` (if/when added as L1)

**Outputs:**

- `fund_quality_score` — scalar (e.g. standardized 0–1 or z-score).

**Logic (high level):**

- Start with normalized metrics (e.g., ranks or z-scores vs universe).
- Combine using weights or ML model to approximate “high-quality” baskets.
- May later be validated by historical performance of quality portfolios.

**Roles:**

- `ml_role_primary = feature`
- `ml_role_secondary = context`


#### 4.6.2 `valuation_percentile_v1` — Relative Valuation Percentile

**Intent:** Provide a **relative valuation measure** versus a peer group/universe.

- **Level:** L2
- **Digitization:** `formula`
- **Construction type:** `aggregation`
- **Primary family:** Valuation & Fundamentals
- **Secondary family:** Event & Regime

**Dependencies (L1):**

- `pe_ttm`, `pb`, and/or other valuation metrics as chosen.

**Outputs:**

- `valuation_percentile` — scalar in [0,1].

**Logic (high level):**

- Within a defined peer group and date, rank assets by chosen valuation metric(s).
- Convert rank to percentile in [0,1].

**Roles:**

- `ml_role_primary = context`
- `ml_role_secondary = feature`


---

### 4.7 Event & Regime

#### 4.7.1 `event_window_state_v1` — Event Window State

**Intent:** Encode a simple **event-relative state** around corporate and macro events.

- **Level:** L2
- **Digitization:** `rule`
- **Construction type:** `state_machine`
- **Primary family:** Event & Regime

**Dependencies (L1):**

- `earnings_flag`, `dividend_flag`, `macro_release_flag_v1` (if implemented as L1)

**Outputs:**

- `event_window_state` — category
  - e.g. `{ "none", "pre_event", "event_day", "post_event" }`.

**Logic (high level):**

- Use event calendars and configured pre/post windows to assign states.
- Resolve conflicts if multiple event types overlap (e.g., priority rules).

**Roles:**

- `ml_role_primary = context`
- `ml_role_secondary = filter`


#### 4.7.2 `regime_cluster_id_v1` — Market Regime Cluster

**Intent:** Provide **unsupervised regime labels** using multiple indicators (trend, volatility, breadth, macro).

- **Level:** L3
- **Digitization:** `ml_pattern`
- **Construction type:** `pattern_engine`
- **Primary family:** Event & Regime
- **Secondary family:** Volatility & Range

**Dependencies (L1/L2/L3):**

- Trend indicators (`trend_mtf_v1` outputs).
- Volatility (`vol_regime_state_v1`, `atr_14`, `realized_vol_20`).
- Breadth or index-level indicators (to be added).
- Macro features (if available).

**Outputs:**

- `regime_cluster_id` — integer category ID.
- Optional meta-labels (e.g., “bull-calm”, “bear-stressed”, etc.).

**Logic (high level):**

- Build feature vectors from selected context indicators.
- Cluster across time using unsupervised methods (e.g., k-means).
- Optionally align clusters with intuitive labels post-hoc.

**Roles:**

- `ml_role_primary = context`
- `ml_role_secondary = filter, risk`


#### 4.7.3 `macro_regime_state_v1` — Macro Regime State

**Intent:** Provide **interpretable macro regimes** (e.g., inflation/growth quadrants) based on macro data.

- **Level:** L3
- **Digitization:** `ml_pattern` or `rule` depending on design.
- **Construction type:** `state_machine`
- **Primary family:** Event & Regime
- **Secondary family:** Valuation & Fundamentals

**Dependencies (external):**

- Macro data (inflation, growth, rates, term spreads, etc.).

**Outputs:**

- `macro_regime_state` — category
  - e.g. `{ "hi_infl_hi_growth", "hi_infl_lo_growth", "lo_infl_hi_growth", "lo_infl_lo_growth" }` or similar.

**Roles:**

- `ml_role_primary = context`
- `ml_role_secondary = risk`


---

### 4.8 Risk & Exposure

#### 4.8.1 `stress_state_v1` — Portfolio/System Stress State

**Intent:** Combine multiple risk metrics into a **discrete stress state** for the system.

- **Level:** L3
- **Digitization:** `ml_pattern` (can start rule-based)
- **Construction type:** `composite_score`
- **Primary family:** Risk & Exposure
- **Secondary family:** Event & Regime

**Dependencies (L1/L2):**

- `dd_trailing_20`, `dd_intraday`
- `realized_vol_20`, `vol_regime_state_v1`
- `gross_exposure`, `net_exposure`
- Correlation metrics (to be specified in later phases).

**Outputs:**

- `stress_state` — category, e.g. `{ "normal", "elevated", "critical" }`.
- Optional `stress_score` scalar.

**Roles:**

- `ml_role_primary = risk`
- `ml_role_secondary = context`


#### 4.8.2 `risk_budget_util_v1` — Risk Budget Utilization

**Intent:** Track **how much of allowed risk budgets** are currently used.

- **Level:** L3
- **Digitization:** `rule`
- **Construction type:** `aggregation`
- **Primary family:** Risk & Exposure

**Dependencies (internal):**

- Policy limits (per-asset, per-book, system-level)
- Exposure and risk metrics (e.g., VaR, ES when implemented).

**Outputs:**

- `risk_budget_utilization` — scalar in [0,1] for each relevant budget type.
- Optional flags when exceeding thresholds.

**Roles:**

- `ml_role_primary = risk`
- `ml_role_secondary = filter`

**Usage:**

- Hard/soft risk gates.
- Telemetry for governance and dashboards.


---

## 5. CSV Artifact: `indicators_catalog_L2L3.csv`

The CSV generated for Phase 4 contains one row per L2/L3 framework defined above, following the
schema in Section 3.

- Intended GitHub path: `sync/ifns/indicators_catalog_L2L3.csv`
- Intended Notion representation: “Indicators — L2/L3 Framework Catalog”

This table connects:

- **Indicator taxonomy** from Phase 1.
- **Universe entries** from Phase 2.
- **L1 building blocks** from Phase 3.

with the concrete framework definitions needed for feature engineering, modeling, and control logic.

---

## 6. Handover Notes for Phase 4

For a new engineer or agent:

1. Use this document to understand the **purpose and structure** of each L2/L3 framework.
2. Use `indicators_catalog_L2L3.csv` as the **configuration backbone** for implementation and backtesting.
3. Respect the declared:
   - `digitization_level` (formula/rule/ML).
   - `dependencies_L1` and `dependencies_external`.
   - `state_space_def` and `output_components` when mapping to feature columns (Phase 5).
4. For ML-based frameworks (`ml_pattern`):
   - Treat them as **models** in the IFNS model registry.
   - Ensure proper training data, labeling, validation, and telemetry hooks.

Once this Phase 4 catalog is accepted as baseline, Phase 5 will map each framework’s outputs into
concrete feature columns and data schemas for the Feature Recipes → Feature Views → Models pipeline.
