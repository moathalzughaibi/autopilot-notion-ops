# Stock Indicator System — Phase 5 Feature Output & Digitization Schema
Version: v0.1 (Draft)

## 1. Purpose

Phase 5 defines **how indicators turn into concrete features** that can be stored, queried, and consumed by
models and strategies in IFNS. It connects:

- Phase 1: Taxonomy (families, levels, output types, digitization levels).
- Phase 2: Indicator Universe Draft.
- Phase 3: L1 Indicator Catalog.
- Phase 4: L2/L3 Framework Catalog.

to the **Feature Recipes → Feature Views → Models** pipeline by specifying:

- Exact **feature columns** for each indicator (value, state, events, episodes, vectors).
- **Naming conventions** and **data types**.
- **Default aggregations** and **missing-data policies**.
- Which features are **enabled by default** vs optional.

This document is paired with a machine-usable CSV:

- `sync/ifns/indicator_feature_schema_v1.csv` (Phase 5 artifact).


---

## 2. Feature Channels and Naming

We standardize indicator outputs into **channels**. Each indicator may populate multiple channels.

### 2.1 Core Channels

1. **Value channel (`value`)**
   - Continuous numeric values directly emitted by the indicator.
   - Examples:
     - `rsi_14_value`
     - `atr_14_value`
     - `fund_quality_score_value`

2. **State channel (`state`)**
   - Categorical or discretized regimes derived from values or frameworks.
   - Examples:
     - `rsi_14_state` ∈ {`oversold`, `neutral`, `overbought`}
     - `vol_regime_state` ∈ {`calm`, `normal`, `stressed`}
     - `trend_state_mtf` ∈ {`strong_up`, `up`, `sideways`, `down`, `strong_down`}

3. **Event channel (`event`)**
   - Binary flags indicating discrete events or triggers.
   - Examples:
     - `breakout_up_event`
     - `earnings_window_event`
     - `candle_engulfing_bull_event`

4. **Episode channel (`episode`)**
   - Start/end spans or zones, usually represented as:
     - Episode tables (e.g., zones, swings) **and/or**
     - Derived features such as distance-to-episode, in/out-of-episode flags.
   - Examples:
     - `sr_zone_id`, `sr_zone_type`, `sr_zone_strength`, `distance_to_nearest_sr_zone`

5. **Vector channel (`vector`)**
   - Fixed-length numeric vectors, typically from ML embeddings.
   - Examples:
     - `candle_embedding_16d`

   - Often complemented by a **cluster/state** channel (e.g., `candle_cluster_id`).


### 2.2 Column Naming Convention

For tabular features (value/state/event), we use:

```text
<indicator_id>_<channel_suffix>
```

- `rsi_14_value`
- `rsi_14_state`
- `rsi_14_oversold_event`
- `trend_state_mtf` (already categorical; no suffix needed)
- `breakout_flag_up_event`

Where needed, we may define **sub-features**:

```text
<indicator_id>_<component>_<channel_suffix>
```

- `macd_12_26_9_line_value`
- `macd_12_26_9_signal_value`
- `macd_12_26_9_hist_value`

Episode outputs often live in separate tables keyed by symbol/timeframe, with a clear ID scheme
(e.g., `sr_zone_v1_zone_id`), but for the main time-series we expose:

- Distance or relationship features:
  - `sr_zone_v1_distance_to_nearest_support`
  - `sr_zone_v1_distance_to_nearest_resistance`
  - `sr_zone_v1_in_strong_zone_state`


---

## 3. Feature Schema Table

The feature schema CSV (`indicator_feature_schema_v1.csv`) uses the following columns:

| Column name           | Type   | Description |
|-----------------------|--------|-------------|
| `indicator_id`        | string | ID from Phase 3/4 catalogs. |
| `feature_id`          | string | Stable ID for the feature column. |
| `feature_name`        | string | Human-readable name. |
| `feature_channel`     | enum   | `value`, `state`, `event`, `episode`, `vector`. |
| `feature_dtype`       | enum   | `float32`, `int8`, `bool`, `string`, `json`. |
| `source_output`       | string | Which logical output it comes from (e.g., `rsi`, `trend_state_mtf`). |
| `state_space`         | string | JSON-style description of allowed categories or value range (for state/event). |
| `default_timeframe`   | string | Default bar timeframe for this feature (e.g., `1h`, `1d`). |
| `default_agg`         | string | Aggregation when rolling up (e.g., `last`, `mean`, `max`, `any`). |
| `missing_policy`      | string | How to handle missing values (e.g., `ffill`, `zero`, `drop`, `sentinel`). |
| `enabled_default`     | bool   | Whether this feature is enabled in the v1 default pack. |
| `notes_phase5`        | string | Usage or implementation notes. |

This table allows:

- A Feature Service to **auto-generate schema**.
- Admin UI to toggle features on/off and adjust policies.
- Models to use **packs** (e.g., “Core Value Pack”, “Core Context Pack”).


---

## 4. Core Feature Packs (v1)

We define v1 **feature packs** to control complexity. Each pack corresponds to a subset of rows in
`indicator_feature_schema_v1.csv`.

### 4.1 Core Value Pack (v1)

Examples (non-exhaustive, but included in the CSV):

- `sma_20_value`, `sma_50_value`
- `ema_12_value`, `ema_26_value`, `ema_50_value`
- `rsi_14_value`
- `roc_10_value`, `mom_10_value`
- `atr_14_value`, `realized_vol_20_value`
- `volume_value`, `vol_sma_20_value`, `obv_value`, `vwap_intraday_value`
- `pe_ttm_value`, `pb_value`, `div_yield_value`
- `fund_quality_score_value` (from L3 when implemented)
- Risk-related scalars: `dd_trailing_20_value`, `beta_market_60_value`, `gross_exposure_value`, `net_exposure_value`

All are numeric (`float32`), typically with:

- `default_agg = "last"`
- `missing_policy = "ffill"` (for continuous time-series)
- Enabled by default in most **model recipes**.


### 4.2 Core State Pack (v1)

Examples:

- `rsi_14_state` ∈ {`oversold`, `neutral`, `overbought`}
- `trend_state_mtf` ∈ {`strong_up`, `up`, `sideways`, `down`, `strong_down`}
- `vol_regime_state` ∈ {`calm`, `normal`, `stressed`}
- `structure_state_mtf` ∈ {`up_structure`, `down_structure`, `sideways_structure`, `transition`}
- `liq_stress_state` ∈ {`normal`, `tight`, `stressed`}
- `event_window_state` ∈ {`none`, `pre_event`, `event_day`, `post_event`}
- `regime_cluster_id` (integer category)
- `macro_regime_state` (macro regimes)
- `stress_state` ∈ {`normal`, `elevated`, `critical`}
- `valuation_percentile_state` (e.g., discretized into quantile buckets)

Defaults:

- `feature_dtype = "string"` or `int8` (if encoded).
- `default_agg = "last"`.
- `missing_policy = "ffill"`.
- Enabled by default for **context-aware** models and backtest slicing.


### 4.3 Core Event Pack (v1)

Examples:

- Candle/event patterns:
  - `candle_pattern_basic_v1_is_doji_event`
  - `candle_pattern_basic_v1_is_pinbar_bull_event`
  - `multi_candle_pattern_v1_is_engulfing_bull_event`
- Structural events:
  - `breakout_flag_up_event`
  - `breakout_flag_down_event`
  - `swing_high_5_event`
  - `swing_low_5_event`
- Corporate/macro event flags:
  - `earnings_flag_event`
  - `dividend_flag_event`
- Risk events:
  - `stress_state_breach_event`
  - `risk_budget_limit_hit_event` (derived from `risk_budget_util_v1`)

Defaults:

- `feature_dtype = "bool"`.
- `default_agg = "any"` (within the aggregation window).
- `missing_policy = "zero"` (no event by default).


### 4.4 Episode & Distance Pack (v1)

From episode-oriented frameworks like `sr_zone_v1` and swing structure:

- `sr_zone_v1_distance_to_nearest_support_value`
- `sr_zone_v1_distance_to_nearest_resistance_value`
- `sr_zone_v1_in_strong_zone_state` (boolean/enum)
- Optional: `structure_mtf_v1_major_swing_id`, `major_swing_age_bars`

Defaults:

- Distance features: `float32`, `default_agg = "last"`, `missing_policy = "ffill"`.
- In/out flags: `bool`, `default_agg = "any"` or `"last"` depending on usage.


### 4.5 Vector & Cluster Pack (v1)

Advanced, optional in v1 but prepared in the schema:

- `candle_embedding_16d` — vector; actual storage may be as JSON or separate embedding store.
- `candle_cluster_id` — discrete state ID (int8).

Defaults:

- `candle_cluster_id` is more broadly usable (context pack).  
- `candle_embedding_16d` may be enabled only for specific ML experiments.


---

## 5. Example Feature Rows (Conceptual)

Below are conceptual examples that reflect what is stored in the CSV.

### 5.1 RSI Feature Set

- `indicator_id = rsi_14`

1. **Value feature**  
   - `feature_id = rsi_14_value`  
   - `feature_channel = value`  
   - `feature_dtype = float32`  
   - `source_output = "rsi"`  
   - `state_space = "[0,100]"`  
   - `default_timeframe = "1h"`  
   - `default_agg = "last"`  
   - `missing_policy = "ffill"`  
   - `enabled_default = true`

2. **State feature**  
   - `feature_id = rsi_14_state`  
   - `feature_channel = state`  
   - `feature_dtype = string`  
   - `state_space = "{oversold,neutral,overbought}"`  
   - `default_timeframe = "1h"`  
   - `default_agg = "last"`  
   - `missing_policy = "ffill"`  
   - `enabled_default = true`

3. **Event features**  
   - `feature_id = rsi_14_cross_oversold_event`  
   - `feature_channel = event`  
   - `feature_dtype = bool`  
   - `state_space = "{0,1}"`  
   - `default_agg = "any"`  
   - `missing_policy = "zero"`  
   - `enabled_default = true`

   - `feature_id = rsi_14_cross_overbought_event`  
   - same structure, for overbought crossing.


### 5.2 Trend Framework Feature Set (`trend_mtf_v1`)

1. **State**  
   - `trend_state_mtf` (string/int8), state space defined in Phase 4.

2. **Score**  
   - `trend_mtf_v1_score_value` (float32, in [-1,1]).

Defaults:

- `default_timeframe = "1h"`/`"1d"` (depending on config).  
- Aggregation = `last`.  
- Missing policy = `ffill`.


### 5.3 SR Zone Distance (`sr_zone_v1`)

1. **Distance to nearest strong support**  
   - `sr_zone_v1_distance_to_nearest_support_value`  
   - `feature_channel = value`  
   - `feature_dtype = float32`  
   - `state_space = ">=0 (price units or %)"`  
   - `default_agg = "last"`  
   - `missing_policy = "sentinel"` (e.g., large value if no zone).

2. **In/near zone state**  
   - `sr_zone_v1_in_strong_zone_state`  
   - `feature_channel = state` or `event` (bool/string).


---

## 6. CSV Artifact: `indicator_feature_schema_v1.csv`

The CSV accompanying this document contains **representative v1 features** across:

- Trend, momentum, volatility, volume, structure, candle grammar.
- Fundamentals, events, regimes, risk.

It is not meant to be “all possible features”, but a **high-quality, top-down v1 pack** that can be
extended later without breaking naming or semantics.

Intended path:

- GitHub: `sync/ifns/indicator_feature_schema_v1.csv`
- Notion: “IFNS – Indicator Feature Schema v1” table (sync target).


---

## 7. Handover Notes for Phase 5

For engineering / next agent:

1. Treat `indicator_feature_schema_v1.csv` as the **single source of truth** for feature column design.
2. When implementing Feature Recipes:
   - Filter by `enabled_default = true` to define the default model input pack.
   - Allow admins to toggle rows on/off for specific recipes.
3. Any new indicator added in future phases must:
   - First appear in the Phase 2 universe.
   - Then be defined in Phase 3/4 catalogs.
   - Finally get one or more rows here in Phase 5 with clear channel, dtype, and policies.
4. Changes to feature semantics should be versioned via `feature_id` (e.g., `rsi_14_value_v2`)
   and logged through IFNS governance mechanisms.

Once Phase 5 is accepted as baseline, Phase 6 can focus on **implementation templates** (code,
storage, and retrieval patterns) using this schema as configuration.
