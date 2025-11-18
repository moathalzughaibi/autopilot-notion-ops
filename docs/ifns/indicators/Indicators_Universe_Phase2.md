# Stock Indicator System — Phase 2 Universe Draft
Version: v0.1 (Draft)

## 1. Purpose

This Phase 2 document defines the **Indicator Universe Draft** for the Stock Indicator System under IFNS.
It takes the Phase 1 taxonomy (families, levels, output types, digitization levels) and applies it to a
concrete but extensible list of indicators and frameworks that we may use.

The goal is **coverage and clarity**, not final detail:

- Define the *universe tiers* (what is essential vs optional vs experimental).
- List a first-pass roster of indicators and frameworks across all 9 families.
- Assign each candidate a consistent identity and basic metadata so it can be promoted into the
  formal catalogs (L1, L2/L3) in later phases.

This universe is intentionally broader than what will be used in production; later phases and backtesting
will prune and refine it.

---

## 2. Universe Tiers

To reflect real-world practice at top-tier firms, the indicator universe is organized into **tiers**.
Not all indicators are equal in importance or maturity, and the system should be explicit about that.

### 2.1 Tier Definitions

- **Tier 0 — Mandatory Core**
  - Ubiquitous, extremely well-understood indicators that almost any serious system will support.
  - They are simple, stable, easily digitized (`digitization_level = formula`).
  - They form the baseline “language” of the system.

- **Tier 1 — Strong Candidates**
  - Indicators and frameworks with strong theoretical or empirical support.
  - They are highly likely to be used in production, but the exact parametrization and role may still evolve.
  - Often include L2 transforms of Tier 0 indicators and basic L3 frameworks.

- **Tier 2 — Exploratory / Advanced**
  - Advanced, niche, or experimental indicators.
  - May require ML-based pattern detection, complex structure engines, or less-mature research.
  - Included so that the system has a “parking lot” for future expansion without polluting the core.

Each indicator in the universe is tagged with `universe_tier ∈ {0,1,2}` to signal priority and maturity.

---

## 3. Indicator Universe Overview by Family

This section lists the **main indicator groups** per family (Axis A), with examples and typical levels.
Detailed definitions and formulas will be moved to Phase 3 (L1) and Phase 4 (L2/L3).

### 3.1 Trend & Price Location (A1)

**Core idea:** Direction and position of price over time.

**Tier 0 (Mandatory Core):**

- `sma_n` — Simple Moving Average (various windows, e.g. 10, 20, 50, 100, 200).
  - Level: L1, digitization: formula, output: scalar.
- `ema_n` — Exponential Moving Average (e.g. 12, 26, 50).
  - L1, formula, scalar.
- `wma_n` — Weighted Moving Average (optional in Tier 0 but common).
- `macd_12_26_9` — MACD line, signal, histogram.
  - L1 (basic formula) with L2 variants for normalization.
- `price_location_range_n` — Price location vs N-bar high/low (0–1 normalized).
  - L1, formula, oscillator.

**Tier 1 (Strong Candidates):**

- `slope_ma_n` — Slope of MA (e.g. EMA(50) slope over window k).
- `adx_14` — Average Directional Index.
- `donchian_n` — Donchian channel high/low and mid.
- `trend_regression_n` — Linear regression slope over N bars.
- `trend_mtf_v1` — Multi-timeframe trend framework (L3).

**Tier 2 (Exploratory):**

- `hurst_exponent_n` — Hurst exponent over window N.
- `trend_persistence_score_v1` — ML-computed trend persistence score.

### 3.2 Momentum & Strength (A2)

**Core idea:** Speed and strength of recent price moves.

**Tier 0:**

- `rsi_14` — Relative Strength Index (14-period).
- `roc_n` — Rate of Change (N-period).
- `%k_stoch_14_3` / `%d_stoch_14_3_3` — Stochastics.
- `mom_n` — Simple momentum (close_t - close_{t-n}).

**Tier 1:**

- `cci_20` — Commodity Channel Index.
- `williams_r_14` — Williams %R.
- `rsi_slow_14_v1` — Smoothed/denoised RSI.
- `momentum_zscore_n` — Z-scored momentum.

**Tier 2:**

- `momentum_consensus_v1` — Composite momentum score using multiple L1 indicators and ML weighting.
- `trend_follow_thrust_v1` — Pattern-based thrust strength indicator (rule/ML hybrid).

### 3.3 Volatility & Range (A3)

**Core idea:** Magnitude and variability of price movement.

**Tier 0:**

- `atr_14` — Average True Range.
- `true_range` — 1-bar true range.
- `realized_vol_n` — Realized volatility over window N (e.g. stdev of log returns).

**Tier 1:**

- `bollinger_band_n_k` — Bollinger upper, middle, lower bands.
- `%b_bollinger_n_k` — Bollinger %B oscillator.
- `range_expansion_ratio_n` — Current range / rolling average range.

**Tier 2:**

- `vol_regime_state_v1` — Discrete volatility regimes (e.g. calm/normal/stressed).
- `vol_of_vol_n` — Volatility of volatility.

### 3.4 Volume / Flow / Liquidity (A4)

**Core idea:** Participation, imbalance, and liquidity.

**Tier 0:**

- `volume` — Raw volume.
- `vol_sma_n` — Volume moving averages.
- `obv` — On-Balance Volume.
- `vwap_intraday` — Volume-Weighted Average Price (intraday).

**Tier 1:**

- `vwap_dev` — Price deviation from VWAP (absolute and normalized).
- `ofi_n` — Order Flow Imbalance over window N (if order book data available).
- `depth_imbalance_n` — Bid/ask depth imbalance.
- `spread_bp` — Bid-ask spread in basis points.

**Tier 2:**

- `liq_stress_v1` — Composite liquidity stress indicator (spread, depth, volume, impact).
- `vpin_v1` — Volume-synchronized probability of informed trading (advanced).

### 3.5 Market Structure & Geometry (A5)

**Core idea:** Swings, levels, formations of price.

**Tier 0:**

- `swing_high_n` / `swing_low_n` — Local swing points based on window N.
- `hh_hl_state_v1` — HH/HL vs LH/LL state (basic version).
- `range_high_low_n` — Rolling range boundaries.

**Tier 1:**

- `structure_mtf_v1` — Multi-timeframe structure state machine with swing tiers.
- `sr_zone_v1` — Support/resistance zones with strength scores.
- `breakout_flag_v1` — Rule-based breakout/breakdown flags.

**Tier 2:**

- `wyckoff_phase_v1` — Approximate Wyckoff accumulation/distribution phase labels.
- `market_profile_nodes_v1` — High-volume nodes and value areas (where data is available).

### 3.6 Candle Grammar & Micro-Patterns (A6)

**Core idea:** Bar-by-bar micro-signals.

**Tier 0:**

- `candle_body_pct` — Body size as % of full range.
- `upper_wick_pct` / `lower_wick_pct` — Wick sizes as % of full range.
- `close_position_pct` — Close position in the candle’s range [0, 1].

**Tier 1:**

- `candle_pattern_basic_v1` — Flags for simple patterns: engulfing, pin bar, doji, hammer, shooting star.
- `gap_flag_v1` — Gap up/down detection.
- `multi_candle_pattern_v1` — Simple two- or three-candle combinations.

**Tier 2:**

- `candle_embedding_v1` — Learned embedding vector of last N candles.
- `candle_cluster_id_v1` — Discrete cluster ID from embedding clustering.
- `micro_flow_pattern_v1` — ML-based local pattern classification.

### 3.7 Valuation & Fundamentals (A7)

**Core idea:** Business value and financial strength.

**Tier 0:**

- `pe_ttm` — Price/Earnings (trailing 12 months).
- `pb` — Price/Book.
- `dividend_yield` — Dividend yield.

**Tier 1:**

- `ev_ebitda` — Enterprise Value/EBITDA.
- `eps_growth_yoy` — EPS growth year-over-year.
- `revenue_growth_yoy` — Revenue growth year-over-year.
- `debt_to_equity` — Leverage measure.

**Tier 2:**

- `fundamental_quality_score_v1` — Composite quality factor.
- `valuation_percentile_v1` — Percentile vs peers/universe for valuation metrics.

### 3.8 Event & Regime (A8)

**Core idea:** Discrete events and high-level regimes.

**Tier 0:**

- `earnings_flag` — Upcoming or recent earnings event.
- `dividend_flag` — Upcoming or recent dividend.
- `split_flag` — Split or reverse split.

**Tier 1:**

- `event_window_state_v1` — “pre-event”, “event-day”, “post-event”.
- `risk_on_off_state_v1` — Simple risk-on/risk-off proxy.
- `macro_release_flag_v1` — Important macro release flag (for index/FX regimes).

**Tier 2:**

- `regime_cluster_id_v1` — ML-based cluster of market regimes using multiple indicators.
- `macro_regime_state_v1` — Discrete macro regimes (e.g. high inflation, low growth, etc.).

### 3.9 Risk & Exposure (A9)

**Core idea:** Direct risk and portfolio exposure metrics.

**Tier 0:**

- `dd_intraday` / `dd_trailing_n` — Drawdown metrics.
- `beta_market_n` — Rolling beta to benchmark.
- `gross_exposure` / `net_exposure` — Portfolio-level exposure.

**Tier 1:**

- `var_n_alpha` — Value-at-Risk estimate.
- `es_n_alpha` — Expected Shortfall.
- `concentration_index_v1` — Concentration of positions.

**Tier 2:**

- `stress_state_v1` — Stress indicator based on correlations, volatility, and drawdowns.
- `risk_budget_utilization_v1` — Utilization of allowed risk budgets.

---

## 4. Universe Draft Table (Concept-Level)

The detailed universe is maintained in a CSV file:

- `sync/ifns/indicators_catalog_draft.csv`

At this Phase 2 stage, we populate **concept-level metadata only**. Later phases will add formulas,
inputs, and feature mappings.

### 4.1 Core Columns (Draft)

For Phase 2, the draft catalog uses the following columns:

- `indicator_id` — Stable ID (e.g., `rsi_14`, `trend_mtf_v1`).
- `name` — Human-readable name.
- `family_role_primary` — Primary family (Trend, Momentum, etc.).
- `family_role_secondary` — Optional secondary family.
- `level` — L1, L2, or L3.
- `output_type_primary` — Scalar, oscillator, category, flag, vector, or episode.
- `digitization_level` — formula, rule, ml_pattern, or manual_only.
- `universe_tier` — 0, 1, or 2.
- `description_short` — One-line summary.
- `notes_phase2` — Optional notes or open questions.

This structure is intentionally lean to keep Phase 2 focused on coverage and classification. Additional
metadata (inputs, parameters, ML roles, governance fields) will be attached in Phase 3 and Phase 4.

---

## 5. Handover Notes for Phase 2

**Intended file locations:**

- Markdown:
  - GitHub: `docs/ifns/Indicators_Universe_Draft.md`
- CSV draft:
  - GitHub: `sync/ifns/indicators_catalog_draft.csv`

**What Phase 2 achieves:**

- Provides a **broad but structured** list of indicators and frameworks across all 9 families.
- Tags each candidate with:
  - Primary family.
  - Level (L1/L2/L3).
  - Output type.
  - Digitization level.
  - Universe tier (priority/maturity).
- Ensures that subsequent phases are not “inventing from scratch” but refining a known universe.

**How the next phases will use this:**

- **Phase 3 (L1 Catalog)** will:
  - Filter `indicators_catalog_draft.csv` where `level = L1`.
  - Add formal definitions (formulas, inputs, parameters) and ML roles.
  - Promote the subset into `indicators_catalog.csv` (authoritative L1 catalog).

- **Phase 4 (L2/L3 Catalog)** will:
  - Focus on rows where `level ∈ {L2, L3}`.
  - Decompose complex frameworks into their components.
  - Specify dependencies on L1 indicators and data sources.

- **Phase 5 (Digitization Schema)** will:
  - Use the `indicator_id`s from this universe as keys to generate feature output schemas.

Going forward, **any new indicator idea** should be added first to the universe draft (this phase), classified
under the Phase 1 taxonomy, and only then promoted to detailed catalogs and implementation.
