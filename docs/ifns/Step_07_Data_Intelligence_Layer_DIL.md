# Step 07 – Section 3.0: Data Intelligence Layer (DIL)

## 01 – Narrative & Intent

This step defines the **Data Intelligence Layer (DIL)** — the sensory cortex of IFNS.

DIL is responsible for transforming messy, heterogeneous market inputs into **clean, aligned, and information-rich representations** that the Core ML engine can actually use. It is where prices, volumes, events, and contextual signals are:

- Ingested from providers,
- Normalized and aligned in time,
- Checked for quality and coverage,
- Enriched into features,
- Paired with labels,
- Assembled into training and evaluation datasets.

The intent of this step is to:

1. Clearly define what “data done right” means for IFNS.
2. Specify the **data model, feature frameworks, and labeling policies** that form the basis of modeling and backtesting.
3. Ensure that DIL is treated as a **first-class intelligence layer**, not just a background ETL job.

By the end of this step, there should be no ambiguity about how data enters the system, how it is transformed, and how it is presented to the Core ML engine and SxE surfaces.

### 1. Role of DIL in the IFNS Stack

DIL sits directly beneath Modeling Intelligence (MI) and above raw providers:

- Upstream, it receives:
  - Trade and quote data (prices, volumes, spreads),
  - Reference and corporate action data (splits, dividends),
  - Optional contextual data (indices, volatility measures, calendars, sector/industry tags).

- Downstream, it delivers:
  - Canonical **price/volume tables**,
  - Multi-timeframe **feature tables**,
  - **Labels** representing future outcomes over defined horizons,
  - **Training and evaluation datasets** ready for ML pipelines,
  - Data quality and coverage metrics for SxE.

DIL is responsible not only for correctness but also for **expressivity**: the features and labels it produces define the vocabulary through which MI can “understand” the market.

### 2. Data Domains and Sources

DIL organizes input data into several domains, each with its own schema and contracts:

1. **Core Price & Volume**
   - OHLCV bars at one or more base timeframes (e.g., 1m, 5m, 15m, 1h, daily).
   - Bid/ask quotes where available, including spread and depth snapshots.

2. **Corporate Actions & Reference**
   - Splits, dividends, symbol changes, delistings.
   - Reference mappings for instruments (ISIN, exchange, sector, currency).

3. **Market Context**
   - Index levels, volatility indices, benchmark yields.
   - Calendar effects (sessions, holidays, market open/close times).

4. **Optional Alternative Signals**
   - News sentiment, order book imbalance, flow metrics (if/when available).
   - These are treated as **feature extensions**, not core dependencies.

Each domain must be:

- Explicitly modeled in schemas,
- Versioned when fields change,
- Linked to instruments and timestamps in a consistent way.

### 3. Canonical Price & Bar Model

DIL defines a **canonical bar schema** that all downstream processes rely on. At minimum, this includes:

- `ts` – timestamp (with explicit timezone and session handling),
- `symbol` – instrument identifier (with mapping to a reference table),
- `open`, `high`, `low`, `close`,
- `volume`,
- Optional:
  - `vwap`,
  - `bid`, `ask`, `bid_size`, `ask_size`,
  - `turnover`, `num_trades`,
  - `session_id`, `market_state` (pre/open/close/auction).

Responsibilities:

- Normalize bars across providers so that downstream features do not depend on provider quirks.
- Encode **session boundaries** (e.g., gaps, opens, closes) explicitly, not implicitly.
- Preserve raw provider identifiers and timestamps as needed for auditability.

The canonical bar model is the anchor for all feature frameworks and labels.

### 4. Feature Frameworks

DIL implements and maintains a set of **feature frameworks** — structured families of features that capture different aspects of market behavior. Key examples include:

1. **TREND_MTF (Multi-Timeframe Trend)**
   - Moving averages, slopes, and momentum signals across multiple horizons.
   - Local and global trend indicators (e.g., MA crossovers, regression slopes).

2. **CANDLE_SHAPE**
   - Candle body and wick proportions.
   - Patterns (e.g., engulfing, pin bars, inside bars) encoded as features rather than boolean flags.
   - Contextual statistics (e.g., candle range vs. recent ATR).

3. **STRUCTURE_MTF (Market Structural Awareness)**
   - Higher highs / higher lows, lower highs / lower lows.
   - Swing points (major, primary, minor) and structural regimes.
   - Multi-timeframe structural tags that later feed MSA and MI.

4. **VOL_LIQ (Volatility & Liquidity)**
   - ATR, realized volatility, intraday range measures.
   - Volume spikes, relative volume, spread-based liquidity metrics.

5. **MICROSTRUCTURE**
   - If available: order book imbalance, short-term reversal pressure, microprice deviations.

6. **REGIME_TAGS**
   - Coarse-grained regime labels (e.g., trending, mean-reverting, volatile, calm).
   - Derived from combinations of trend, volatility, and structure features.

Each framework has:

- A **definition table** (feature names, descriptions, data types, ranges).
- A **generation pipeline** (how features are computed, on which inputs, under which parameters).
- A **version tag** so models can be trained against specific feature versions and later audits know exactly what was used.

### 5. Labeling Policies

DIL also defines **labeling policies** that convert future outcomes into targets suitable for ML:

Examples:

- **Directional labels**
  - `y_direction = sign(Price_{t+H} - Price_t)` over one or more horizons `H`.
- **Return bins**
  - Discrete buckets of future returns (e.g., large up / small up / flat / small down / large down).
- **Event-based labels**
  - “Did price hit +X% before -Y% within H bars?” (path-dependent labels).
- **Risk-adjusted labels**
  - Returns normalized by volatility, liquidity, or structural context.

Labeling policy definitions include:

- Exact formulas and horizons,
- Required input fields,
- Handling of gaps, missing data, and corporate actions,
- Conditions under which labels are **invalid** (and should be dropped).

The goal is for labels to be **unambiguous and reproducible**: anyone with the DIL schemas and raw data should be able to recompute them and get the same results.

### 6. Training & Evaluation Dataset Assembly

DIL is responsible for assembling **training and evaluation datasets** that feed the Core ML engine. This includes:

- Joining features and labels on `(symbol, ts)` keys.
- Applying filters:
  - Data quality filters (e.g., minimum coverage, liquidity thresholds).
  - Scenario filters (e.g., market hours only, particular regimes).
- Splitting data into:
  - Training, validation, and test sets,
  - Time-based folds for cross-validation,
  - Optional out-of-sample periods reserved for backtests.

Datasets are described in a **Training Dataset Schema**, which includes:

- Feature lists and versions,
- Label definitions and horizons,
- Time coverage,
- Instrument universe,
- Filters and exclusions,
- Dataset IDs used to link models, backtests, and experiments.

This schema is the contract that ensures models and backtests know exactly **what they were trained and tested on**.

### 7. Data Quality, Coverage, and Health

DIL must continuously track and expose:

- **Coverage metrics**
  - Percentage of bars with complete features and labels.
  - Gaps by symbol, timeframe, and date.
- **Quality metrics**
  - Outlier detection (price jumps, volume spikes) and remediation actions.
  - Provider discrepancies (e.g., price mismatches vs. secondary sources).
- **Latency/staleness metrics** (for near-real-time data, where applicable)
  - Time between provider event and system ingestion.

These metrics are surfaced to SxE:

- Mirror shows high-level **data health views** (coverage charts, alerts).
- Admin exposes **data quality dashboards** and configurations (e.g., thresholds for discarding or flagging data).

### 8. SxE Representation of DIL

From a system-to-experience perspective, DIL has its own presence in Mirror and Admin:

- **Mirror (read-only awareness)**
  - Data health overview (coverage per symbol/universe).
  - Feature readiness status (e.g., “TREND_MTF v1 ready for universe X from date Y”).
  - Label availability and horizon coverage.

- **Admin (control and governance)**
  - Configuration of:
    - Provider connections and priority order,
    - Feature framework versions,
    - Labeling policies and horizons,
    - Dataset definitions and filters.
  - Audit logs for:
    - Changes to schemas,
    - Changes to filtering rules,
    - Rebuilds of major datasets.

DIL is thus **visible and governable**, not a black box. Operators know when data is trustworthy enough to train, backtest, or run live.

---

## 02 – Implementation Reference

The Data Intelligence Layer described in this step is concretely implemented in the **IFNS – Core ML Build Specification** as follows:

- **Stage 2 – Data & Feature Pipeline**
  - Defines the canonical schemas for:
    - Core price and volume tables (`Data_Model_Prices`),
    - Feature definitions (e.g., `Feature_Definitions`, `Feature_TREND_MTF_V1`, `Feature_CANDLE_SHAPE_V1`, `Feature_STRUCTURE_MTF_V1`),
    - Labeling policies (`Labeling_Policy`),
    - Training and evaluation datasets (`Training_Dataset_Schema`).
  - Specifies the pipelines and contracts for:
    - Ingesting raw data and producing canonical tables,
    - Generating features from frameworks,
    - Computing labels over defined horizons,
    - Assembling ML-ready datasets.

- **Stage 1 – Foundations & Architecture**
  - Declares where DIL artifacts live in the repository structure (e.g., `data/`, `features/`, `schemas/`, `pipelines/`).
  - Incorporates DIL schemas and dataset references into `core_ml_config`, so that all downstream components know which datasets and feature versions to use.

- **Stage 3 – Modeling & Training**
  - Consumes DIL’s datasets and references them in:
    - Model family definitions,
    - Training job specifications,
    - Model Registry entries.

- **Stage 4 – Backtesting & Evaluation**
  - Uses the same DIL datasets and labeling policies to:
    - Define backtest universes and sample periods,
    - Align backtest metrics with the labels and features used during training.

In practice, any change to DIL — new feature frameworks, updated labeling policies, new dataset definitions — must follow this path:

1. Update the relevant schemas and definitions in Stage 2 tables and contracts.
2. Update `core_ml_config` and any dataset references in Stages 3 and 4.
3. Ensure Mirror and Admin surfaces for DIL (data health, feature readiness, dataset catalogs) are consistent with the new definitions.

This guarantees that the Data Intelligence Layer remains **coherent, reproducible, and visible** across the entire IFNS stack.

---

## 03 – Notes & Decisions

- DIL is the **single source of truth** for data schemas, features, labels, and ML-ready datasets. Other layers must not introduce alternative or ad-hoc versions of these concepts.
- Feature frameworks (TREND_MTF, CANDLE_SHAPE, STRUCTURE_MTF, VOL_LIQ, etc.) should be versioned and documented in dedicated tables so that:
  - Models and backtests can reference them unambiguously,
  - Changes do not silently alter historical results.
- Labeling policies must be treated as part of the **core modeling contract**: when labels change, associated models and backtests may need to be revisited.
- Data quality and coverage metrics should be monitored continuously, and significant issues should raise incidents that appear in Mirror and Admin, just like model or execution incidents.
- As IFNS expands into new asset classes or markets, this step should be revisited to:
  - Add new domains and schemas,
  - Extend feature frameworks where necessary,
  - Confirm that environment-specific nuances (e.g., different sessions or trading calendars) are correctly encoded.
