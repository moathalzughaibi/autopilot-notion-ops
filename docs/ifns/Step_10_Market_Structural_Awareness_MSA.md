# Step 10 – Section 6.0: Market Structural Awareness (MSA)

## 01 – Narrative & Intent

This step defines **Market Structural Awareness (MSA)** — the layer of IFNS that understands the *shape* and *context* of the market, not just its immediate price moves.

Where DIL transforms raw data into features and MI converts those features into predictions, MSA is concerned with **how prices are organized over time**:

- Are we in an uptrend, downtrend, or range?
- Where are the major and minor swing highs and lows?
- Are we in a regime of high volatility, low liquidity, or structural instability?
- Is the current signal aligned with, or fighting against, the prevailing structure?

The intent of this step is to:

1. Define a **structural ontology** for IFNS (how we name and classify structure).
2. Describe the **STRUCTURE_MTF** and related frameworks that DIL produces for MSA.
3. Clarify how MSA influences MI, MSI, DRA, and execution policies (EI).
4. Ensure that structural context is **explicit, visible, and governable**, not implicit or ad-hoc.

By the end of this step, “market structure” becomes a first-class concept with clear data, models, and SxE representations.

---

### 1. Role of MSA in the IFNS Stack

MSA bridges the gap between **raw price action** and **strategic decision-making**:

- It consumes:
  - Canonical bars and derived structure features (from DIL’s STRUCTURE_MTF, TREND_MTF, VOL_LIQ frameworks).
  - Historical context for swing points, regimes, and volatility states.

- It produces:
  - **Structural tags** at each point in time (e.g., “HHHL uptrend”, “range-bound”, “breakdown from range”).
  - **Regime labels** (e.g., trending vs. mean-reverting, high-vol vs. low-vol, stable vs. structurally stressed).
  - Optional **structure-aware signals** (e.g., “pullback within uptrend”, “failed breakout”).

MSA’s outputs influence:

- How MI models are trained and interpreted (e.g., regime-conditioned models).
- How MSI integrates multiple models and signals (e.g., preferring certain models in certain regimes).
- How DRA and EI behave (e.g., tightening risk or execution constraints in structurally stressed conditions).

MSA ensures that IFNS does not treat all time periods as interchangeable — the system is aware of *where* in the structural map it is operating.

---

### 2. Structural Ontology: Swings, Trends, and Regimes

MSA uses a clear structural ontology so that all components talk about structure in the same language.

Key elements:

1. **Swing Points**
   - **Major swing highs/lows** – large, structurally significant turning points.
   - **Primary swing highs/lows** – intermediate-level swings within major trends.
   - **Minor swing highs/lows** – local fluctuations within primary swings.

2. **Trend States**
   - Higher highs / higher lows (**HHHL**) – canonical uptrend.
   - Lower highs / lower lows (**LHLL**) – canonical downtrend.
   - Higher highs / lower lows or similar mixed patterns – **transition or range** states.

3. **Regime Labels**
   - **Trend vs. Range**:
     - Trending (strong directional bias).
     - Range-bound (oscillating within a defined band).
   - **Volatility**:
     - High-vol regime.
     - Low-vol regime.
   - **Liquidity**:
     - Deep/liquid vs. thin/fragile.
   - **Structural stress**:
     - Breakout/breakdown zones, structural gaps, halted or fragmented trading.

4. **Multi-Timeframe Context**
   - Each instrument can have separate but related structure labels at:
     - Short-term (e.g., intraday),
     - Medium-term (e.g., swing),
     - Long-term (e.g., positional).

The ontology is encoded in **STRUCTURE_MTF** and **REGIME_TAGS** feature frameworks, allowing models and policies to reason over structure in a consistent way.

---

### 3. STRUCTURE_MTF and Derived Feature Frameworks

MSA is built on DIL’s **STRUCTURE_MTF** and related frameworks, which translate raw prices into structured features and labels.

Key components:

- **STRUCTURE_MTF**
  - Identifies swing highs/lows at multiple timeframes.
  - Computes trend state tags (HHHL, LHLL, range, transition).
  - Tracks distance to key structural levels (previous major high/low, breakout levels).

- **REGIME_TAGS**
  - Combines STRUCTURE_MTF, TREND_MTF, and VOL_LIQ to classify regimes (e.g., “high-vol uptrend”, “low-vol range”).

- **STRUCTURE_EVENTS**
  - Optional event stream describing:
    - Breakouts above previous highs,
    - Breakdowns below previous lows,
    - Tests and failures of significant levels.

These frameworks are used by:

- MI (structure-aware models),
- MSI (structure-informed integration and gating),
- DRA (structure-aware risk and allocation),
- SxE (visualizations of structural state for operators).

---

### 4. Structure-Aware Modeling and MSI

MSA has two modes of interaction with MI and MSI:

1. **Conditioning**
   - Models are trained and evaluated **conditional on structure**:
     - Separate models per regime (e.g., trending vs. range).
     - Models that learn regime-specific behaviors (e.g., signals only active in pullbacks within trends).
   - Model performance is tracked by regime in backtests and live telemetry.

2. **Gating & Weighting**
   - MSI uses structural tags as **gating variables**:
     - Certain signals only allowed in specific structural states.
     - Model weights adjusted based on regime (e.g., giving more weight to certain models in high-vol regimes).
   - Structural states can trigger changes in:
     - Position sizing guidelines,
     - Allowed leverage or exposure,
     - Execution style (e.g., more cautious in fragile structures).

MSA thus ensures that the **same signal is not interpreted the same way** in completely different structural contexts.

---

### 5. Structural Constraints for Risk and Execution

Market structure is also a **risk and execution constraint**, not just a modeling input.

Examples of structural constraints:

- **Structural No-Trade Zones**
  - Avoid or reduce activity:
    - Immediately after major breakouts/breakdowns until structure stabilizes.
    - In extremely illiquid or structurally stressed regimes.

- **Position Management Rules**
  - Tighten stops or reduce position sizes when:
    - Volatility spikes above a threshold within a given structure.
    - The market transitions from trend to range or vice versa.

- **Time-of-Structure Constraints**
  - Adjust behavior around key structural events:
    - Pre-/post-earnings or macro events tied to structural resets.
    - Opening and closing auction regimes with structural gaps.

These constraints are encoded in DRA and execution policies, but **MSA provides the structural signals** that drive them.

---

### 6. SxE Representation of MSA

MSA has a strong visual and analytical presence in SxE surfaces:

- **Mirror**
  - Structural overview panels:
    - Current regime and trend state per instrument/universe.
    - Distribution of capital and risk exposure by regime.
  - Structural event timelines:
    - Major breakouts/breakdowns, regime shifts, and their impact on performance.
  - “Structure vs. performance” views:
    - How strategies behave in different regimes.

- **Admin**
  - Structural settings and thresholds:
    - Parameters for swing detection (lookback windows, sensitivity).
    - Regime definition thresholds (trend strength, volatility bands).
  - Structural constraint policies:
    - No-trade zones,
    - Structural risk adjustment rules,
    - Regime-based exposure caps.
  - Audit history for changes to structural definitions or thresholds.

MSA’s SxE representation ensures that operators can **see, adjust, and trust** the way structure is defined and used in IFNS.

---

## 02 – Implementation Reference

Market Structural Awareness is implemented across several parts of the **IFNS – Core ML Build Specification**:

- **Stage 2 – Data & Feature Pipeline** (MSA’s primary data implementation)
  - Defines:
    - `Feature_STRUCTURE_MTF_V1` (and later versions) for swing and trend states.
    - `Feature_REGIME_TAGS_V1` for combined regime labels.
    - Related tables such as `STRUCTURE_Parameters` for swing detection and trend thresholds.
  - Specifies pipelines for:
    - Detecting swing points,
    - Classifying trend states,
    - Generating regime tags at multiple timeframes.

- **Stage 3 – Modeling & Training**
  - Defines **structure-aware model families**:
    - Models that explicitly consume STRUCTURE_MTF and REGIME_TAGS.
    - Models trained per-regime or using regime as an input feature.
  - Extends training and evaluation tables to:
    - Log performance by structural regime,
    - Support regime-conditioned model selection.

- **Stage 4 – Backtesting & Evaluation**
  - Ensures backtest frameworks:
    - Produce metrics broken down by structural regimes,
    - Capture the impact of structure-aware gating and weighting in MSI.

- **Stage 5 – Risk, Execution & SxE Link**
  - Encodes **structural constraints** in DRA decision tables and risk envelopes:
    - No-trade or reduced-trade conditions for stressed regimes.
    - Regime-based exposure caps and stop adjustments.
  - Links structural states into execution policies where appropriate:
    - Different pacing or route preferences in fragile vs. stable structures.

- **Stages 6 & 7 – Paper & Live Operations**
  - Ensure that:
    - Real-time structural state is available to paper and live execution logic.
    - Telemetry includes structural tags so that performance and incidents can be analyzed by regime.

In practice, any change to MSA — such as revised swing detection rules, new regime definitions, or new structure-aware model families — should:

1. Update the **Stage 2** feature and parameter definitions.
2. Propagate to **Stage 3** model definitions and training specs.
3. Ensure **Stage 4–5** metrics, gating rules, and constraints reflect the new structure.
4. Update Mirror and Admin views that depend on structural tags and regimes.

---

## 03 – Notes & Decisions

- MSA is the **authoritative source** for structural and regime definitions; other parts of the system should not invent independent, ungoverned notions of “trend” or “regime.”
- Structural definitions must be:
  - **Stable enough** to support consistent operation,
  - **Versioned and documented** so that historical results can be interpreted correctly.
- When introducing new markets or instruments, MSA should be revisited to:
  - Confirm that swing detection and regime definitions remain appropriate,
  - Add any asset-class-specific structural concepts if required.
- Structural awareness should not be treated as optional: even if early versions of IFNS use simple structures, the architecture should be ready for richer MSA features and models.
