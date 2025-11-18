# Stage 02 – Data & Feature Pipeline (DIL Implementation)

## 01 – Narrative & Intent

This document defines **Stage 02 – Data & Feature Pipeline** for the Intelligent Financial Neural System (IFNS).

Conceptually, this stage **implements** the Data Intelligence Layer (DIL) described in:

- Step 07 – Data Intelligence Layer (DIL)
- Step 10 – Market Structural Awareness (MSA) (for structure/regime features)
- Other Steps where features, labels, and datasets are referenced

Stage 02 answers:

- What **raw data** do we ingest and in what format?
- How do we transform raw data into **canonical tables**?
- How do we build **feature frameworks** (TREND_MTF, STRUCTURE_MTF, VOL_LIQ, etc.)?
- How do we define **labels** and **datasets** for training, backtesting, and evaluation?
- How are these artifacts **versioned, registered, and surfaced** to other stages and SxE?

The outcome of Stage 02 is a **governed, reproducible data and feature layer** that downstream stages (03–07) can rely on without reinventing basic data logic.

---

## 02 – Scope & Responsibilities

Stage 02 covers:

1. **Data Sources & Ingestion**
   - Market data (prices, volumes, corporate actions).
   - Supplemental data where relevant (e.g., sector, fundamentals, news tags if used later).
   - Ingestion and normalization rules.

2. **Canonical Data Tables**
   - Bar-level price/volume data across multiple timeframes.
   - Reference data (instrument metadata, calendars, mappings).

3. **Feature Frameworks**
   - Multi-timeframe trend features (TREND_MTF).
   - Structure and regime features (STRUCTURE_MTF, REGIME_TAGS).
   - Volatility and liquidity features (VOL_LIQ).
   - Any additional feature families required by Step 07.

4. **Labeling Policies**
   - Directional labels (up/down/flat).
   - Return buckets or continuous labels.
   - Event-based labels (e.g., breakouts, structural events) if needed.

5. **Datasets & Splits**
   - Training/validation/test splits.
   - Backtest vs. live-like evaluation windows.
   - Dataset registries.

6. **Governance & Versioning**
   - Versioned feature and label definitions.
   - Dataset IDs and registries.
   - Data quality and coverage indicators.

Stage 02 does **not** define models or backtests — those are Stage 03 and Stage 04.  
It defines the **data contracts** those later stages must depend on.

---

## 03 – Data Sources & Ingestion

### 3.1 Raw Data Sources

Stage 02 assumes a set of **logical data sources**, such as:

- `market_prices` – OHLCV and related fields from exchanges or data vendors.
- `corporate_actions` – splits, dividends, symbol changes.
- `instrument_reference` – static metadata (ticker, ISIN, sector, currency, etc.).
- Optional: `news_events`, `macro_events`, or other future extensions.

These sources may come from different vendors and storage backends, but Stage 02 specifies:

- **Logical schemas** (columns, data types).
- **Time handling** (timezones, session boundaries).
- **Instrument keys** (primary identifiers, mapping from vendor symbols).

### 3.2 Ingestion Pipelines

In the repo, ingestion lives under:

```text
pipelines/ingest/
```

Outputs are stored in:

```text
data/raw/
```

Key principles:

- **Idempotence** – rerunning ingestion for the same date range should produce the same result (or identify differences explicitly).
- **Auditability** – ingestion logs should capture:
  - Source files/feeds,
  - Time of ingestion,
  - Row counts,
  - Basic quality checks (e.g., missing values, extreme outliers).

Stage 02 does not mandate vendor-specific details; it defines the **target canonical view** that all data must fit into.

---

## 04 – Canonical Data Tables

After ingestion, data is normalized into **canonical tables** under:

```text
data/canonical/
```

### 4.1 Price/Volume Tables

Example: `prices_1m.parquet`, `prices_5m.parquet`, `prices_1d.parquet` (formats are illustrative).

Core fields:

- `ts` – timestamp (aligned to timeframe, e.g., bar close).
- `symbol` – instrument identifier (canonical).
- `open`, `high`, `low`, `close`, `volume`.
- Optional:
  - `vwap`, `turnover`, `bid`, `ask`, etc.

Rules:

- Price series are **forward-adjusted** or **split-adjusted** according to a documented policy.
- Missing bars (e.g., holidays) are represented consistently (e.g., absent, not as zero).
- Any corporate actions impacting price/volume are encoded and applied consistently.

### 4.2 Reference Tables

Under `data/canonical/reference/`, for example:

- `instruments.parquet` – static instrument metadata.
- `trading_calendar.parquet` – per-venue session times and holidays.
- `sector_mapping.parquet` – sector/industry classification.

These tables are used by later stages for:

- Universe selection,
- Risk aggregation by sector/country,
- Execution and session logic.

---

## 05 – Feature Frameworks

Feature engineering lives under:

```text
pipelines/feature_engineering/
data/features/
```

Stage 02 defines **named feature frameworks**, each versioned, e.g.:

- `Feature_TREND_MTF_V1`
- `Feature_STRUCTURE_MTF_V1`
- `Feature_REGIME_TAGS_V1`
- `Feature_VOL_LIQ_V1`

Each framework:

- Has a **formal definition** (what features exist, how they’re computed).
- Produces tables keyed by (`ts`, `symbol`) plus feature columns.
- Is versioned, so later improvements can be added as V2, V3, etc.

### 5.1 TREND_MTF

**Purpose:** capture trend direction and strength across multiple timeframes.

Examples of features:

- Returns over different lookback windows (e.g., 1d, 5d, 20d, 60d).
- Normalized or volatility-adjusted returns.
- Moving averages and crossovers (short vs. long MA).
- Trend strength indicators (e.g., ADX-like measures, directional persistence scores).

Each feature:

- Is documented with:
  - Name (e.g., `ret_20d_vol_norm`),
  - Description,
  - Formula,
  - Input data required.

### 5.2 STRUCTURE_MTF

**Purpose:** support Market Structural Awareness (MSA).

Features include:

- Swing highs/lows at multiple timeframes.
- Distance to recent major/primary/minor highs and lows.
- Encoded pattern / state tags (HHHL, LHLL, range, transition).

Implementation is typically a multi-pass algorithm over canonical prices, producing features like:

- `struct_state_short`, `struct_state_medium`, `struct_state_long`.
- `dist_to_major_high`, `dist_to_major_low`.

### 5.3 REGIME_TAGS

**Purpose:** classify combined trend/volatility/liquidity regimes.

Features/tags:

- `regime_trend` – trending vs. range.
- `regime_vol` – high-vol vs. low-vol (based on VOL_LIQ features).
- `regime_liquidity` – deep vs. thin.
- `regime_tag` – combined tag (e.g., `trend_highvol`, `range_lowvol`).

These tags are crucial for structure-aware modeling (Stage 03) and risk policies (Stage 05).

### 5.4 VOL_LIQ

**Purpose:** volatility and liquidity characterization.

Features include:

- Realized volatility over multiple horizons.
- Volume and turnover metrics.
- Spread or depth proxies (if available).
- Liquidity stress indicators.

---

## 06 – Labeling Policies

Label computation lives under:

```text
pipelines/labeling/
data/labels/
```

Stage 02 defines **label families**, such as:

- `Label_Direction_Horizon_X`
- `Label_ReturnBucket_Horizon_X`
- `Label_Event_Breakout` (if used)

### 6.1 Directional Labels

For example, `Label_Direction_Horizon_20d_V1`:

- Inputs:
  - `close` prices from canonical tables.
- Logic:
  - Compute forward 20-day return.
  - Apply thresholds to define:
    - `up`, `down`, `flat` (or `1`, `-1`, `0`).
- Parameters:
  - Return horizon (e.g., 20 bars).
  - Flat band threshold (e.g., ±0.5% or volatility-adjusted).

These parameters are **externalized** into config/registry so they can evolve under governance.

### 6.2 Return Buckets / Continuous Labels

- `Label_ReturnBucket_Horizon_X` – discretized returns into bins (e.g., quintiles).
- `Label_ReturnContinuous_Horizon_X` – raw or volatility-normalized returns.

Choice of label depends on model families (Stage 03).  
Stage 02’s job is to define them **once**, consistently.

### 6.3 Event Labels (Optional)

If IFNS uses event-based labels (e.g., breakout events, structural pattern events), Stage 02 defines:

- Event detection logic (often tied to STRUCTURE_MTF and REGIME_TAGS).
- Time window and conditions.
- Label encoding (binary events, categorical event types).

---

## 07 – Datasets & Splits

Dataset definitions live under:

```text
data/datasets/
data/registry/datasets_index.json
```

Stage 02 defines **Dataset IDs** (e.g., `DS_TRAIN_CORE_V1`, `DS_BACKTEST_CORE_V1`) which include:

- Universe definition:
  - Markets, symbols, time range.
- Sampling definition:
  - Timeframes,
  - Bar selection (e.g., daily close),  
  - Any sampling filters (e.g., min volume).
- Feature sets:
  - Which feature frameworks and versions (e.g., TREND_MTF_V1 + VOL_LIQ_V1).
- Label sets:
  - Which label families are included.
- Splits:
  - Train / validation / test ranges and logic,
  - Backtest vs. holdout periods.

These datasets are the **products** consumed by:

- Stage 03 (Modeling & Training),
- Stage 04 (Backtesting & Evaluation).

By standardizing Dataset IDs, Stage 02 ensures that models and backtests are **comparable and reproducible**.

---

## 08 – Governance, Versioning & Data Quality

Stage 02 is also responsible for **governance of data and features**.

### 8.1 Versioning

Each data artifact family is versioned:

- Feature frameworks: `Feature_TREND_MTF_V1`, `Feature_TREND_MTF_V2`, etc.
- Labels: `Label_Direction_Horizon_20d_V1`, etc.
- Datasets: `DS_TRAIN_CORE_V1`, `DS_TRAIN_CORE_V2`.

Versioning rules:

- Major changes (logic changes) → new version.
- Minor changes (bug fixes) → documented and carefully evaluated for backward compatibility.

### 8.2 Data Quality Signals

Data quality checks produce metrics and flags, such as:

- Missing data rates by symbol/date.
- Outlier counts.
- Inconsistent corporate actions.

These can be stored in:

- `data/registry/data_quality.json`
- Quality columns in canonical or feature tables.

SxE can surface:

- Data quality dashboards,
- Warnings for symbols or periods with poor data quality.

---

## 09 – SxE Representation of Stage 02

Stage 02’s artifacts are surfaced in SxE as:

### 9.1 Mirror (Read-Focused)

- Data coverage views:
  - Which markets, symbols, and time ranges are available.
- Feature framework status:
  - Available feature frameworks and their versions.
- Dataset overviews:
  - List of Dataset IDs,
  - Their universes, feature/label sets, and date ranges.

### 9.2 Admin (Control-Focused)

- Dataset Registry console:
  - Create/update dataset definitions (subject to governance).
  - Inspect feature/label composition and splits.
- Feature & Label Registry:
  - View definitions and versions.
  - Attach notes about intended use and limitations.
- Data Quality console:
  - See symbols/periods with quality issues.
  - Flag areas requiring remediation before modeling.

---

## 10 – Notes & Decisions

- Stage 02 is the **authoritative source** for data, features, labels, and datasets:
  - Models (Stage 03) must not invent their own ad-hoc labels or feature definitions.
  - Backtests (Stage 04) must reference Dataset IDs, not custom local slices.

- Any change to feature or label logic must:
  - Be reflected as a new version (or clearly documented minor change),
  - Be visible in the Dataset Registry and SxE consoles.

- Data quality is a **first-class concern**:
  - ML performance cannot be interpreted without understanding data quality.
  - Stage 02 must provide enough signals for SEL (Stage 13) to incorporate data quality into its analyses.

- As IFNS expands to new data sources (fundamentals, options, news, macro), Stage 02 should be extended consistently:
  - New feature frameworks and labels for new data types,
  - Extended Dataset definitions,
  - Clear indication of which models/strategies use which data families.

Stage 02 thus anchors the **Data Intelligence Layer** as a governed, shared foundation for all downstream intelligence and decision-making in IFNS.
