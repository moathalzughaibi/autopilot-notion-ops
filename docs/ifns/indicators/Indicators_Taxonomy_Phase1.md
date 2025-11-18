# Stock Indicator System — Phase 1 Taxonomy & Governance
Version: v0.1 (Draft)

## 1. Purpose and Scope

This document defines the **indicator taxonomy and governance rules** for the Stock Indicator System under the Intelligent Financial Neural System (IFNS). It is the root specification for how indicators are named, grouped, and classified before we move to detailed catalogs (L1/L2/L3) and feature engineering.

This taxonomy is designed to integrate cleanly with the existing IFNS governance for the **Feature Recipes → Feature Views → Models** pipeline, where code‑free operators manage features and models through Admin pages, while engineers and data scientists implement the underlying logic. It provides a common language so that:

- Every indicator belongs to well‑defined **families** (what it tells us about the market).
- Every indicator has a **construction level** (L1/L2/L3) aligned with the IFNS three‑level indicator system.
- Every indicator has a clear **output type** and **digitization level**, so we know exactly how it will appear in data tables and ML features.
- Governance, status, and ownership of indicators can be tied into IFNS Admin & UI matrices.

Subsequent phases will build on this taxonomy:

- **Phase 2** — Universe Draft: list all candidate indicators and frameworks in this structure.
- **Phase 3** — L1 Catalog: define the atomic, formula‑based indicators.
- **Phase 4** — L2/L3 Framework Catalog: define composite indicators, schools, and pattern frameworks.
- **Phase 5** — Digitization & Feature Schema: map indicators into concrete feature columns.
- **Phase 6** — Implementation Playbook: pseudo‑code and patterns for engineering.
- **Phase 7** — Final Handover: checklists and guidance for new agents/teams.


---

## 2. Axes of Classification

Each indicator is classified along **three main axes**:

1. **Axis A — Role / Family:** What aspect of the market it describes.
2. **Axis B — Construction Level:** How it is constructed (L1/L2/L3).
3. **Axis C — Output Type:** How its output looks in data form.

Together, these axes define the “coordinate” of any indicator in the system.


### 2.1 Axis A — Role / Family

Axis A describes the **semantic role** of an indicator: what part of market behavior it aims to capture. An indicator may belong to more than one family, but it must have a **primary family_role**.

#### A1. Trend & Price Location

- **Intent:** Describe the direction and “position” of price over time.
- **Examples:**
  - Moving Averages: SMA/EMA/WMA.
  - MACD and signal line.
  - ADX (trend strength).
  - Donchian channels or price channels.
  - Price distance to key levels (high/low of range, last swing, major high/low).
- **Typical questions answered:**
  - Is the market trending up, down, or sideways?
  - Where is current price inside its recent range (bottom, middle, top)?
- **Typical ML roles:**
  - Context features for slicing backtests.
  - Regime labels or trend states.
  - Filters for which strategies should be active.

#### A2. Momentum & Strength

- **Intent:** Measure the **speed and strength** of recent price moves.
- **Examples:**
  - RSI, Stochastics, ROC, CCI, Williams %R, momentum.
  - Normalized change indicators (percent change, z‑scores).
- **Typical questions answered:**
  - Is the move accelerating or losing steam?
  - Is price overextended relative to recent history?
- **Typical ML roles:**
  - Short‑term entry/exit features.
  - Filters to avoid entering into exhausted moves.


#### A3. Volatility & Range

- **Intent:** Quantify the **width and variability** of price movement.
- **Examples:**
  - ATR, standard deviation of returns, Bollinger Bands.
  - Realized volatility, range expansion/contraction metrics.
- **Typical questions answered:**
  - How wide is the market’s “breathing” right now?
  - Is volatility rising, falling, or stable?
- **Typical ML roles:**
  - Position sizing logic (risk per trade).
  - Regime classification (calm vs volatile).
  - Normalization factors for other indicators.


#### A4. Volume / Flow / Liquidity

- **Intent:** Capture **participation, imbalance, and liquidity conditions**.
- **Examples:**
  - Volume, volume moving averages.
  - OBV (On‑Balance Volume).
  - Order flow imbalance (OFI), depth imbalance.
  - VWAP and deviations from VWAP.
  - Spread z‑scores and liquidity stress markers.
- **Typical questions answered:**
  - Is the move supported by strong participation?
  - Is there a liquidity squeeze or imbalance between buyers and sellers?
- **Typical ML roles:**
  - Execution cost models.
  - Filters for avoiding illiquid conditions.
  - Regime‑aware sizing and throttling.


#### A5. Market Structure & Geometry

- **Intent:** Describe the **shape of price swings and levels** over time.
- **Examples:**
  - Swing highs/lows and swing tiers (minor/primary/major).
  - HH/HL vs LH/LL state machines.
  - Support/resistance zones and break/hold flags.
  - Range vs breakout detection.
- **Typical questions answered:**
  - Are we in an up‑structure (HH/HL) or down‑structure (LH/LL)?
  - Which levels are structurally important?
- **Typical ML roles:**
  - Context frameworks (e.g., STRUCTURE_MTF).
  - Feature slices for backtests.
  - Risk anchors for stop‑placement and profit targets.


#### A6. Candle Grammar & Micro‑Patterns

- **Intent:** Capture **bar‑by‑bar micro‑structure** using candle features and patterns.
- **Examples:**
  - Body size and wick ratios.
  - Gap flags, close‑in‑range quantiles.
  - Classic candlestick patterns (engulfing, pin bar, doji, morning star, etc.).
  - Candle embeddings and clusters (e.g., a vector representation of the last N candles).
- **Typical questions answered:**
  - What is the local micro‑tone (rejection, indecision, strong close)?
  - Are we seeing accumulation of certain candle types?
- **Typical ML roles:**
  - Local entry timing.
  - Attention hints for temporal models.
  - Clustering for context slices.


#### A7. Valuation & Fundamentals

- **Intent:** Measure **business value and financial health** apart from short‑term price noise.
- **Examples:**
  - P/E, P/B, EV/EBITDA.
  - Dividend yield, payout ratios.
  - Growth metrics (EPS, revenue, cash flow growth).
  - Balance sheet strength ratios.
- **Typical questions answered:**
  - Is the asset cheap or expensive versus fundamentals?
  - Is the underlying business strengthening or weakening?
- **Typical ML roles:**
  - Slow‑moving structural context (fundamental regimes).
  - Filters for universe selection.
  - Long‑horizon signal components.


#### A8. Event & Regime

- **Intent:** Encode **discrete events and high‑level regimes**.
- **Examples:**
  - Earnings dates, surprises and guidance.
  - Splits, dividends, buybacks.
  - Macro data events and risk‑on/risk‑off states.
  - Volatility regime labels, bull/bear regime labels.
- **Typical questions answered:**
  - Are we in a special regime or around a major event?
  - Should behavior be temporarily modified?
- **Typical ML roles:**
  - Regime labels for slicing backtests and training.
  - Event windows for counterfactual studies.
  - Conditional logic for execution and risk limits.


#### A9. Risk & Exposure

- **Intent:** Describe **risk state and portfolio exposure** directly.
- **Examples:**
  - Drawdown, VaR/ES, realized risk metrics.
  - Beta to a benchmark; factor exposures.
  - Leverage and gross/net exposure.
  - Concentration indices and stress indicators.
- **Typical questions answered:**
  - How much risk is the system currently bearing?
  - Is exposure aligned with policy limits and regimes?
- **Typical ML roles:**
  - Constraints for decision and execution engines.
  - Feedback variables for self‑evaluation and control loops.


### 2.2 Axis B — Construction Level (L1 / L2 / L3)

Axis B aligns directly with the **three‑level indicator system** already adopted in IFNS:

- **L1 — Core / Classic Indicators**
- **L2 — Transformed / Enhanced Indicators**
- **L3 — Composite / Framework Indicators**

#### L1 — Core / Classic Indicators

- **Definition:** Indicators defined by **standard, well‑known formulas** applied directly to market or fundamental data.
- **Examples:**
  - SMA(20), EMA(50), RSI(14), MACD(12,26,9), ATR(14), OBV.
  - Basic valuation ratios, realized volatility, simple z‑scores.
- **Characteristics:**
  - Single formula, minimal dependencies.
  - Typically **digitization_level = formula**.
  - Easy to port across languages and platforms.
- **Typical role in IFNS:**
  - Building blocks for more complex frameworks.
  - Baseline feature set for early model iterations.


#### L2 — Transformed / Enhanced Indicators

- **Definition:** Indicators built on top of L1, using transforms validated by backtesting or domain evidence.
- **Examples:**
  - Volatility‑normalized MACD.
  - Denoised or smoothed RSI.
  - Fractionally differenced price or features.
  - Signed‑impact OFI and depth‑imbalance metrics.
- **Characteristics:**
  - Combine one or more L1 indicators and/or apply additional filters.
  - Often **digitization_level = formula** or **rule**.
  - Add statistical robustness or make signals more stationary.
- **Typical role in IFNS:**
  - Main workhorses for model features.
  - Controlled expansion of the feature set under policy limits.


#### L3 — Composite / Framework Indicators

- **Definition:** Multi‑component constructs that combine L1/L2 indicators into **structured frameworks** or **patterns**.
- **Examples:**
  - Ichimoku Kinko Hyo (cloud lines, conversion/base lines, lagging span).
  - Multi‑timeframe trend dashboards (e.g., TREND_MTF_V1 combining EMA slopes, ADX, Donchian channels, and price location states).
  - Candle grammar frameworks (CANDLE_GRAMMAR_V1 with embeddings and clusters).
  - Market structure engines (STRUCTURE_MTF_V1 state machines for HH/HL vs LH/LL with swing tiers).
  - Composite risk or momentum scores (e.g., momentum_consensus_v1, liquidity_stress_v1).
- **Characteristics:**
  - Multiple inputs, often multiple outputs.
  - Rich internal structure, sometimes including ML sub‑models.
  - **digitization_level** can be `rule`, `ml_pattern`, or a mixture.
- **Typical role in IFNS:**
  - Context frameworks used for slicing, regimes, and backtesting gates.
  - High‑level signals consumed by integration and decision engines.


### 2.3 Axis C — Output Type

Axis C defines how an indicator’s output appears when stored in data tables and feature views. This is essential for digitization and for mapping to the Feature Recipes → Feature Views → Models pipeline.

The core output types are:

1. **Scalar**
2. **Oscillator**
3. **Category**
4. **Flag**
5. **Vector**
6. **Episode**

#### C1. Scalar

- **Definition:** A continuous numeric value, often unbounded or wide‑ranged.
- **Examples:**
  - ATR value, realized volatility.
  - Moving average value (price level).
  - Raw fundamental ratios (P/E, EV/EBITDA).
- **Usage:**
  - Direct feature columns in ML models.
  - Inputs for further transforms (normalization, binning, etc.).


#### C2. Oscillator

- **Definition:** A scalar confined to a **known bounded range** (e.g., [0, 100] or [-1, 1]).
- **Examples:**
  - RSI in [0, 100].
  - Stochastics, %B (Bollinger %).
- **Usage:**
  - Feature columns directly interpretable by thresholds.
  - Potential binning into states (oversold, neutral, overbought).


#### C3. Category

- **Definition:** A **discrete state** chosen from a finite set of values.
- **Examples:**
  - `TrendState ∈ {Up, Down, Sideways}`.
  - `StructureState ∈ {Up, Down, Transitional}`.
  - `RSI_state ∈ {oversold, neutral, overbought}`.
- **Usage:**
  - Context labels for slicing backtests and evaluation.
  - Conditional logic in policies (e.g., only trade in Up trend).
  - Categorical features after one‑hot or embedding encoding.


#### C4. Flag

- **Definition:** A **binary event** or boolean indicator (true/false) often associated with a particular time point.
- **Examples:**
  - “RSI crossed above 70”.
  - “Price broke the major high”.
  - “Candle formed a bullish engulfing pattern at this bar”.
- **Usage:**
  - Trigger conditions for entries/exits.
  - Markers for event‑based slicing in backtests.
  - Additional columns in feature sets and labels.


#### C5. Vector

- **Definition:** A fixed‑length vector of numeric values.
- **Examples:**
  - Candle embedding vector (e.g., 16D embedding of last N candles).
  - Factor exposure vectors for multi‑factor models.
  - Encoded pattern signatures.
- **Usage:**
  - Direct inputs to advanced models (transformers, GNNs, etc.).
  - Source for downstream dimensionality reduction or clustering.


#### C6. Episode

- **Definition:** A structured object describing a **span of time** with a start, an end, and metadata.
- **Examples:**
  - A detected head‑and‑shoulders pattern episode.
  - A distinct volatility regime episode.
  - An accumulation/distribution phase with defined boundaries.
- **Usage:**
  - Episode tables tied to time slices and labels.
  - Derived features like “pattern_present_in_last_N_bars”.
  - Slicing and segmentation for backtests and learning.


---

## 3. Digitization Levels

In addition to Axes A/B/C, each indicator has a **digitization_level**, describing how it will be implemented and maintained:

1. `formula`
2. `rule`
3. `ml_pattern`
4. `manual_only`

These levels are important for planning engineering work, test coverage, and how much human labelling or ML modeling is needed.


### 3.1 formula

- **Definition:** Indicators that can be fully expressed as a **deterministic mathematical formula** applied to known data inputs.
- **Examples:**
  - All basic TA indicators (RSI, MACD, ATR, SMA, EMA, etc.).
  - Simple fundamental ratios.
- **Implications:**
  - Straightforward to implement, test, and port.
  - Clear unit tests and validation against reference implementations.
  - Typically L1 or simple L2.


### 3.2 rule

- **Definition:** Indicators expressed as **logical rules or pattern definitions**, combining multiple conditions.
- **Examples:**
  - Swing high/low detection based on relative highs/lows and ATR thresholds.
  - Simple chart patterns like “price breaks above resistance after N bars of consolidation”.
  - Multi‑timeframe trend state machines defined by crossovers and thresholds.
- **Implications:**
  - Implementation requires careful handling of edge cases and look‑back windows.
  - Still deterministic and testable; no learned parameters.
  - Often L2 or L3 frameworks.


### 3.3 ml_pattern

- **Definition:** Indicators that require **trained ML models** to identify complex patterns or abstractions that are hard to encode as simple rules.
- **Examples:**
  - Candle embeddings and clusters produced by CNNs/transformers.
  - ML‑based chart pattern detectors (head‑and‑shoulders, Wyckoff phases, etc.).
  - Composite ML scores like momentum_consensus_v1 or liquidity stress scores.
- **Implications:**
  - Require training datasets, labels, and model governance.
  - Outputs must be versioned and documented (model ID, training run ID).
  - Fit naturally into the IFNS model registry and telemetry schema.


### 3.4 manual_only

- **Definition:** Concepts that are **not yet consistently digitizable**, and currently depend on human judgment.
- **Examples:**
  - High‑level narrative annotations, e.g., “market feels in distribution” without structural criteria.
  - Ad‑hoc one‑off analyst notes with no stable pattern.
- **Implications:**
  - Stored as annotations or tags, not as systematically computed indicators.
  - May later be used as labels to train `ml_pattern` indicators.
  - Not expected to appear as standard feature columns.


---

## 4. Naming and Identity Conventions

To make indicators stable in code, CSV tables, and Notion databases, each indicator must have a consistent identity and naming scheme.

### 4.1 Indicator IDs

- **Format suggestion:** `family_shortname_level_suffix`
  - Examples:
    - `rsi_14` (L1, Momentum & Strength).
    - `macd_12_26_9` (L1, Trend & Momentum).
    - `trend_mtf_v1` (L3, Trend & Price Location).
    - `structure_mtf_v1` (L3, Market Structure).
    - `candle_grammar_v1` (L3, Candle Grammar).
    - `ichimoku_v1` (L3, Trend & Structure).
- **Rules:**
  - Use lowercase, underscores, and numeric parameters as needed.
  - Suffix with version when semantics change in a breaking way (`_v1`, `_v2`).
  - Keep IDs stable once published to avoid breaking references in data and models.


### 4.2 Feature IDs (Phase 5 Preview)

While detailed feature IDs are a Phase 5 topic, the taxonomy influences how we build them. A typical feature id could be:

- `rsi_14_value_d1` → RSI(14) scalar value on daily timeframe.
- `trend_state_mtf_1h` → categorical trend state at 1‑hour resolution from TREND_MTF_V1.
- `candle_cluster_20_mtf_15m` → candle cluster ID for 20‑bar embedding on 15‑minute timeframe.

These conventions ensure that any feature column can be traced back to:

- The **indicator_id** (which is governed by this taxonomy).
- The **timeframe** and **role** (raw, state, event, embedding, episode meta, etc.).


---

## 5. Governance Hooks for IFNS

This taxonomy is not just a naming exercise; it must plug into IFNS governance and the existing Admin & UI matrices.

### 5.1 Ownership and Status

Each indicator will carry metadata such as:

- `status`: `planned`, `implemented`, `backtested`, `approved`, `deprecated`.
- `owner_role`: e.g., Data Lead, Modeling Lead.
- `review_cycle`: how often to review its performance and usage.

This aligns with IFNS roles and pipelines, where:

- **Data Lead** curates sources and feature recipes.
- **Modeling Lead** attaches feature views to models and monitors calibration.
- **Program Director / Risk Officer** approve or reject indicators for production use.


### 5.2 Integration with Feature Recipes → Feature Views → Models

In the IFNS pipeline, the flow is:

1. Author Feature Recipes.
2. Publish Feature Views.
3. Attach Views to Models.
4. Gate by calibration and accuracy.
5. Canary test and approval.
6. Monitor and adapt.

Indicators defined in this taxonomy will:

- Appear as **ingredients** in Feature Recipes (via their `indicator_id` and required parameters).
- Be materialized into Feature Views using the output types defined in Axis C.
- Be subject to calibration and backtesting gates as per policy keys (e.g., minimum data integrity, maximum correlation, minimum Sharpe uplift).


### 5.3 Policy‑Relevant Metadata

Certain metadata attributes will be especially important for policy and gating:

- `family_role` (e.g., risk indicators may have stricter controls).
- `digitization_level` (ML‑based indicators may need extra monitoring).
- `complexity_score` (approximate engineering and maintenance complexity).
- `ml_roles_primary` (feature, context, risk, filter, label).

These attributes will be stored in CSV tables in `sync/ifns/` and exposed to Notion databases so that Admin views can filter and manage indicators by these properties.


---

## 6. How This Taxonomy Will Be Used in Later Phases

This Phase 1 document is the **foundation**. Subsequent phases will consume this taxonomy as follows:

- **Phase 2 — Universe Draft**
  - Use Axis A/B/C and digitization levels to draft a complete “universe list” of indicators and frameworks.
  - Every candidate gets a provisional `indicator_id`, `family_role`, `level`, `digitization_level`, and `output_type`.

- **Phase 3 — L1 Catalog**
  - Fill in formal definitions (formula, inputs, parameters) for all L1 indicators.
  - Use taxonomy fields to keep the catalog consistent and searchable.

- **Phase 4 — L2/L3 Catalog**
  - Decompose complex schools (Ichimoku, classical shapes, MTF contexts) into structured, governed indicators.

- **Phase 5 — Digitization & Feature Schema**
  - Build concrete feature tables (`indicator_feature_outputs.csv`) using Axis C definitions, strongly linked to `indicator_id`s defined under this taxonomy.

- **Phase 6 — Implementation Playbook**
  - Use levels and digitization types to provide templates and pseudo‑code for each category (formula, rule, ml_pattern).

- **Phase 7 — Handover & Checklists**
  - Use this taxonomy as the reference for verifying coverage and coherence of the entire system.


---

## 7. Handover Notes for Phase 1

**Intended file location (in the GitHub/Notion ecosystem):**

- GitHub: `docs/ifns/Indicators_Taxonomy.md`
- Synced Notion Page: “Stock Indicator System — Taxonomy & Governance” (under the IFNS documentation tree).

**For the next agent or engineer:**

- Treat this document as the **canonical reference** for:
  - What families exist.
  - What indicator levels mean.
  - How outputs and digitization levels are defined.
- Do **not** introduce new families or levels without updating this document.
- When adding new indicators in Phases 2–4, always ensure they can be mapped back to:
  - One **primary family_role** (Axis A).
  - One **level** (L1/L2/L3).
  - At least one **output_type** (Axis C).
  - One **digitization_level**.

Once Phase 2 (Universe Draft) is completed, this document should remain relatively stable and only change when:

- We add a new family or fundamentally change a definition.
- We introduce new output types or digitization levels.

All such changes should be versioned (e.g., v0.2, v0.3) and referenced in the IFNS change log.
