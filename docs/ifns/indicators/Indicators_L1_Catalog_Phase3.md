# Stock Indicator System — Phase 3 L1 Indicator Catalog
Version: v0.1 (Draft)

## 1. Purpose

This Phase 3 document defines the **authoritative L1 Indicator Catalog** for the Stock Indicator System
under IFNS. It takes the **universe draft** from Phase 2 and promotes a subset of **Tier 0 (and selected
Tier 1) L1 indicators** into a structured, implementation-ready catalog.

The aims of this phase are:

- To define **precise inputs and outputs** for each L1 indicator.
- To provide **formula-level pseudocode** so engineering teams can implement them consistently across
  languages and platforms.
- To specify **default parameters and timeframes** for each indicator.
- To specify **primary ML roles** (feature, context, risk) for each indicator.
- To prepare a foundation for:
  - Phase 4: composite (L2/L3) frameworks that build on these L1 blocks.
  - Phase 5: feature output schema (actual feature columns).

This catalog is stored as both:

- A human-readable Markdown spec (this file).
- A machine-usable CSV file: `sync/ifns/indicators_catalog_L1.csv` (Phase 3 artifact).


---

## 2. Scope and Selection Policy

### 2.1 In-Scope for Phase 3

This Phase includes **L1 indicators only**, primarily:

- All **Tier 0** L1 indicators from the Phase 2 universe.
- Selected **Tier 1** L1 indicators that are common, simple, and useful across many strategies.

These span all 9 families:

1. Trend & Price Location
2. Momentum & Strength
3. Volatility & Range
4. Volume / Flow / Liquidity
5. Market Structure & Geometry
6. Candle Grammar & Micro-Patterns
7. Valuation & Fundamentals
8. Event & Regime
9. Risk & Exposure

### 2.2 Out-of-Scope (Future Phases)

- All **L2** and **L3** indicators (transforms and frameworks) — handled in **Phase 4**.
- Detailed feature column definitions (value/state/event columns) — handled in **Phase 5**.
- ML-based pattern detectors and embeddings — defined at the indicator level in Phase 4, implemented
  and versioned as models separately.

---

## 3. Catalog Schema (L1)

The L1 catalog is stored as a CSV table with the following columns:

| Column name             | Type   | Description |
|-------------------------|--------|-------------|
| `indicator_id`          | string | Stable ID (e.g., `rsi_14`, `sma_20`). |
| `name`                  | string | Human-readable name. |
| `family_role_primary`   | string | Primary family (Trend & Price Location, Momentum & Strength, etc.). |
| `family_role_secondary` | string | Optional secondary family. |
| `universe_tier`         | int    | Tier from Phase 2 (0 core, 1 strong candidate, 2 exploratory). |
| `digitization_level`    | enum   | For L1 always `formula`. |
| `inputs`                | string | High-level data domains required (e.g., `price`, `volume`, `fundamental`, `events`, `portfolio`). |
| `required_fields`       | string | Concrete fields required (e.g., `close,high,low,volume`). |
| `default_params`        | string | JSON-style parameters (e.g., `{ "window": 14 }`). |
| `default_timeframes`    | string | JSON-style list of timeframes (e.g., `["1h","1d"]`). |
| `output_type_primary`   | enum   | scalar, oscillator, category, flag. |
| `formula_pseudocode`    | string | Short pseudocode describing the formula. |
| `ml_role_primary`       | enum   | feature, context, risk, filter, label. |
| `ml_role_secondary`     | string | Additional roles, if any. |
| `feature_outputs_default` | string | JSON-style description of expected feature outputs (e.g. `{ "value": true, "state": false }`). |
| `notes_phase3`          | string | Implementation or usage notes. |

This schema is intentionally compact but expressive enough to be:

- Directly imported into Notion databases.
- Used by an engineering generator (e.g., templating) to produce code skeletons.
- Referenced by Phase 5 when defining feature output schemas.

---

## 4. L1 Indicator Definitions (High-Level Groups)

Below we summarize key L1 indicators promoted in Phase 3. For each, the detailed row is present in
`indicators_catalog_L1.csv`.

### 4.1 Trend & Price Location

Representative L1 indicators:

- `sma_20`, `sma_50` — Simple Moving Averages over 20 and 50 bars.
- `ema_12`, `ema_26`, `ema_50` — Exponential Moving Averages over 12, 26, 50 bars.
- `macd_12_26_9` — MACD line, signal, and histogram (as an L1 composite with simple formula).
- `price_location_20` — Normalized price position in the last 20-bar high/low range.

All of these:

- Belong primarily to **Trend & Price Location**.
- Take `close` (and sometimes `high, low`) as inputs.
- Produce **scalar** or **oscillator** outputs.
- Are primarily used as **features** and **context** (trend direction, price position).

### 4.2 Momentum & Strength

L1 momentum indicators include:

- `rsi_14` — RSI over 14 bars (oscillator [0,100]).
- `roc_10` — 10-bar Rate of Change.
- `mom_10` — 10-bar raw momentum (`close_t - close_{t-10}`). 
- `stoch_k_14_3`, `stoch_d_14_3_3` — Stochastics %K and %D.

They are:

- Primarily **Momentum & Strength** family.
- Inputs: `high, low, close` as required by formula.
- Outputs: mostly **oscillators**; some unbounded scalars.
- ML roles: **feature** (entry/exit timing) and sometimes **filter**.

### 4.3 Volatility & Range

Core L1 volatility indicators:

- `true_range` — Single-bar True Range.
- `atr_14` — Average True Range over 14 bars.
- `realized_vol_20` — Standard deviation of log returns over 20 bars.

These are:

- **Volatility & Range** family.
- Inputs: `high, low, close, prev_close` (for TR) and series of returns.
- Outputs: **scalar** volatility measures.
- ML roles: **feature**, **context**, and **risk** (position sizing).

### 4.4 Volume / Flow / Liquidity

Core L1 volume indicators:

- `volume` — Raw traded volume.
- `vol_sma_20` — 20-bar volume moving average.
- `obv` — On-Balance Volume.
- `vwap_intraday` — Intraday VWAP.

They are:

- **Volume / Flow / Liquidity** family.
- Inputs: `volume`, `close`, and sometimes intraday trade/quote data for VWAP.
- Outputs: **scalar** values.
- ML roles: **feature** and **context** for participation and flow.

### 4.5 Market Structure & Geometry

Basic structural L1 indicators:

- `swing_high_5` — 5-bar swing high flag.
- `swing_low_5` — 5-bar swing low flag.
- `range_high_20` — 20-bar highest high.
- `range_low_20` — 20-bar lowest low.

These:

- Belong to **Market Structure & Geometry**.
- Inputs: `high, low` (and look-back windows).
- Outputs: mixed **flag** (swing points) and **scalar** (range levels).
- ML roles: **context** and **feature** (levels and pivots).

### 4.6 Candle Grammar & Micro-Patterns

Basic candle-shape features:

- `candle_body_pct` — Candle body size as % of full range.
- `upper_wick_pct` — Upper wick as % of full range.
- `lower_wick_pct` — Lower wick as % of full range.
- `close_pos_pct` — Close position in candle range [0,1].

These:

- Belong to **Candle Grammar & Micro-Patterns**.
- Inputs: `open, high, low, close`.
- Outputs: **scalar** or **oscillator** in [0,1].
- ML roles: **feature** for micro-structure and later as inputs to L2/L3 candle frameworks.

### 4.7 Valuation & Fundamentals

Core fundamental L1 indicators:

- `pe_ttm` — Price/Earnings (trailing 12 months).
- `pb` — Price/Book.
- `div_yield` — Dividend yield.

They are:

- **Valuation & Fundamentals** family.
- Inputs: fundamental fields (earnings, book value, dividends) and price.
- Outputs: **scalar**.
- ML roles: slow-moving **context** and **feature** for universe selection and long-horizon signals.

### 4.8 Event & Regime

Basic event flags:

- `earnings_flag` — Around earnings announcement dates.
- `dividend_flag` — Around dividend events.
- `split_flag` — Around stock split events.

They are:

- **Event & Regime** family.
- Inputs: corporate event calendars.
- Outputs: binary **flag**.
- ML roles: **context**, **filter**, and sometimes used as **label** for event studies.

### 4.9 Risk & Exposure

Core risk-related L1 indicators:

- `dd_intraday` — Intraday drawdown vs intraday peak.
- `dd_trailing_20` — Drawdown vs peak over trailing 20 bars.
- `beta_market_60` — 60-bar rolling beta vs benchmark.
- `gross_exposure` — Sum of absolute portfolio positions.
- `net_exposure` — Net long-minus-short exposure.

These are:

- **Risk & Exposure** family.
- Inputs: price and portfolio holdings; benchmark returns for beta.
- Outputs: **scalar**.
- ML roles: primarily **risk** and **context**, sometimes **feature** for meta-control models.

---

## 5. Example Formula Pseudocode

To illustrate the level of detail in the CSV, here are a few pseudocode examples.

### 5.1 RSI(14) — `rsi_14`

- **Inputs:** `close`
- **Params:** `window = 14`
- **Pseudocode:**

```text
delta_t = close_t - close_{t-1}
gain_t  = max(delta_t, 0)
loss_t  = max(-delta_t, 0)

avg_gain_t = EMA(gain, window)
avg_loss_t = EMA(loss, window)

rs_t  = avg_gain_t / max(avg_loss_t, epsilon)
rsi_t = 100 - 100 / (1 + rs_t)
```

- **Output:** oscillator in [0,100].

### 5.2 ATR(14) — `atr_14`

- **Inputs:** `high, low, close` (and previous `close`).
- **Params:** `window = 14`
- **Pseudocode:**

```text
tr_t = max(
    high_t - low_t,
    abs(high_t - close_{t-1}),
    abs(low_t  - close_{t-1})
)

atr_t = SMA(tr, window)  # or Wilder's smoothing variant
```

- **Output:** scalar volatility measure.

### 5.3 Simple Moving Average (20) — `sma_20`

- **Inputs:** `close`
- **Params:** `window = 20`
- **Pseudocode:**

```text
sma_20_t = mean( close_{t-19} ... close_t )
```

- **Output:** scalar trend/level.

### 5.4 Candle Body % of Range — `candle_body_pct`

- **Inputs:** `open, high, low, close`
- **Pseudocode:**

```text
full_range_t = max(high_t - low_t, epsilon)
body_size_t  = abs(close_t - open_t)
candle_body_pct_t = body_size_t / full_range_t
```

- **Output:** scalar in [0,1].

---

## 6. CSV Artifact: `indicators_catalog_L1.csv`

The CSV file accompanying this document contains one row per L1 indicator with all the columns
defined in Section 3. It is expected to be:

- Stored in GitHub under: `sync/ifns/indicators_catalog_L1.csv`.
- Synced into Notion for Admin / governance views.
- Consumed by Phase 5 when deriving feature output schemas.

**Note:**

- Adding new L1 indicators should always go through this catalog.
- Any change to `indicator_id`, formula semantics, or default parameters must be versioned and
  reviewed (e.g., moving from `rsi_14` to `rsi_14_v2` if semantics change).

---

## 7. Handover Notes for Phase 3

For a new engineer or agent:

1. Use this document to understand the **L1 universe** and the catalog schema.
2. Use `indicators_catalog_L1.csv` as the **single source of truth** for L1 definitions.
3. Implement indicators according to:
   - `inputs`
   - `required_fields`
   - `default_params`
   - `formula_pseudocode`
4. Expose outputs to the feature engineering layer according to:
   - `output_type_primary`
   - `feature_outputs_default`

After Phase 3 is accepted as baseline, Phase 4 will extend this work to L2/L3 frameworks
and pattern systems that depend on these L1 building blocks.
