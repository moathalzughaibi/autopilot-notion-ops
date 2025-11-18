# Stock Indicator System — Phase 6 Implementation & Runtime Templates
Version: v0.1 (Draft)

## 1. Purpose

Phase 6 defines **how to actually run** the indicator and feature system described in Phases 1–5.
It does **not** provide concrete code in a specific language, but it specifies:

- The **runtime architecture** (pipelines, services, and stores).
- Standard **implementation templates** for:
  - Indicator computation.
  - Backfilling and recalculation.
  - Feature serving for models and strategies.
  - Monitoring and telemetry of indicators and features.
- How the existing configuration artifacts are used:
  - `indicators_catalog_L1.csv` (Phase 3)
  - `indicators_catalog_L2L3.csv` (Phase 4)
  - `indicator_feature_schema_v1.csv` (Phase 5)

This phase is meant as a **handover-ready guide** for engineers who will implement the system in
a chosen stack (e.g., Python + pandas, Spark, Flink, kdb+, etc.).


---

## 2. High-Level Runtime Architecture

At a high level the system is split into four layers:

1. **Data Ingestion Layer**
   - Brings in raw market data (OHLCV), fundamentals, events, macro data, and portfolio data.
   - Normalizes into **canonical base tables**.

2. **Indicator Engine Layer**
   - Applies L1, L2, and L3 indicators according to the catalogs.
   - Produces **indicator outputs** (values, states, events, episodes, vectors).

3. **Feature Layer**
   - Maps indicator outputs into **feature columns** using `indicator_feature_schema_v1.csv`.
   - Builds **feature views** for specific model recipes and strategy needs.

4. **Serving & Monitoring Layer**
   - Serves features to models/strategies in real-time or batch.
   - Monitors freshness, correctness, and stability of indicators and features.

Each layer is configured (not hard-coded) using the CSV artifacts from Phases 3–5.


---

## 3. Canonical Data Model (Inputs)

### 3.1 Core Base Tables

Minimum recommended input tables (schema is conceptual):

1. **Market Bars Table**
   - `symbol`
   - `timestamp`
   - `open, high, low, close`
   - `volume`
   - `timeframe` (e.g., `1m`, `5m`, `1h`, `1d`)

2. **Fundamentals Table**
   - `symbol`
   - `timestamp` (or reporting date)
   - `eps_ttm`
   - `book_value_per_share`
   - `dividends_per_share_annualized`
   - Other fields required by L1 fundamental indicators.

3. **Events Table**
   - `symbol`
   - `event_type` (earnings, dividend, split, macro_release, etc.)
   - `event_timestamp`
   - Optional metadata (e.g., expected EPS, surprise).

4. **Portfolio & Risk Table**
   - `timestamp`
   - `symbol`
   - `position_notional`
   - `book_id`, `strategy_id`
   - Derived risk fields (optional) for VaR/ES calculations.

5. **Macro Table** (optional but recommended)
   - Macro time series required for macro regimes.

These tables are the **only source of truth** the Indicator Engine consumes directly.


---

## 4. Indicator Engine — Implementation Template

### 4.1 Config-Driven Indicator Runner

The Indicator Engine reads:

- `indicators_catalog_L1.csv`
- `indicators_catalog_L2L3.csv`

and dynamically constructs computation graphs.

**Template responsibilities:**

1. For each `indicator_id`:
   - Identify its **inputs** (`inputs`, `required_fields`).
   - Identify dependencies (`dependencies_L1`, `dependencies_external` for L2/L3).
   - Resolve **timeframes** to be computed.

2. Build a **DAG (Directed Acyclic Graph)** of computations:
   - Nodes = indicator instances (`indicator_id`, `timeframe`).
   - Edges = dependencies between indicators.

3. Execute the DAG:
   - In batch mode for **backfills** (historical data).
   - In streaming/incremental mode for **live updates**.

### 4.2 L1 Indicator Template

Pseudo-interface (language-agnostic):

```text
interface L1Indicator {
    id: string                   # e.g., "rsi_14"
    inputs: InputSpec            # domains/fields from base tables
    params: Dict                 # from default_params (Phase 3), overridable
    compute(batch: DataFrame) -> DataFrame  # returns indicator series
}
```

- The `compute` method takes a time-ordered series (per symbol, timeframe) and returns columns:
  - `timestamp`
  - `symbol`
  - `<indicator_id>_raw` (internal name for value output)

### 4.3 L2/L3 Framework Template

```text
interface FrameworkIndicator {
    id: string                    # e.g., "trend_mtf_v1"
    dependencies: List[string]    # indicator_ids from L1/L2/L3
    inputs: InputSpec             # if additional external inputs needed
    params: Dict                  # thresholds, windows, etc.
    compute(batch: DataFrame, dep_series: Dict[string, DataFrame]) -> DataFrame
}
```

- `dep_series` contains the outputs of lower-level indicators.
- Outputs are logical fields (e.g., `trend_state_mtf`, `vol_regime_state`, `sr_zone_episode`).


### 4.4 Storage of Indicator Outputs

Recommended layout:

- **Per symbol/timeframe indicator table** (wide or long):
  - `symbol`, `timestamp`, `timeframe`, plus dynamic columns for indicator outputs.
- OR **one table per family** if scale requires.

Indicator columns should use the **indicator_id** and logical output name from Phases 3–4, e.g.:

- `rsi_14_raw`
- `atr_14_raw`
- `trend_state_mtf`
- `sr_zone_v1_zone_id` (in separate episode store)


---

## 5. Feature Service — Implementation Template

The Feature Service is responsible for turning indicator outputs into **features** according to
`indicator_feature_schema_v1.csv`.

### 5.1 Feature Transformation Steps

For each row in `indicator_feature_schema_v1.csv`:

1. Resolve the **source indicator output** (`source_output`, `indicator_id`).
2. Apply **channel-specific logic**:
   - `value` → direct mapping/normalization.
   - `state` → encode as string or numeric category.
   - `event` → boolean or 0/1 flag; apply windowed aggregations if needed.
   - `episode` → derive distances/in/out flags.
   - `vector` → parse/store as array/embedding.

3. Respect **timeframe**, **agg**, and **missing policy**:
   - Align to `default_timeframe` (or requested timeframe).
   - Apply `default_agg` when aggregating from smaller bars.
   - Apply `missing_policy` (e.g., forward-fill, zero, sentinel).

4. Output final **feature table/view** for a given **feature pack**:
   - Example view: `features_core_pack_1h`.

### 5.2 Feature Service Interface (Conceptual)

```text
interface FeatureService {
    get_features(
        symbols: List[string],
        as_of: Timestamp,
        pack_id: string,           # e.g., "core_v1"
        time_horizon: string       # e.g., "1h", "1d"
    ) -> DataFrame                 # rows: symbol,timestamp + feature columns
}
```

- `pack_id` maps to a subset of rows in `indicator_feature_schema_v1.csv` (Core Value Pack, etc.).
- Used by:
  - Backtest engines (offline).
  - Live model servers (online).


---

## 6. Backfill & Recalculation Templates

### 6.1 Historical Backfill

**Goal:** Compute indicators and features over long historical windows.

Template steps:

1. Select universe, timeframe, and date range.
2. Load base data (bars, fundamentals, events).
3. Run Indicator Engine DAG in batch mode.
4. Store indicator outputs in indicator tables.
5. Run Feature Service transformations to compute feature views.
6. Validate basic invariants (no NaN explosions, reasonable ranges, etc.).

### 6.2 Recalculation / Parameter Changes

When indicator definitions or parameters change:

1. Version the indicator (`rsi_14` → `rsi_14_v2`) if semantics change.
2. Re-run backfill for affected indicators (and dependent frameworks).
3. Rebuild feature views that depend on changed indicators.
4. Keep both versions available if old models depend on v1.

This process should be driven by a simple **CLI or orchestration tool** based on the catalogs and schema.


---

## 7. Monitoring & Telemetry Templates

### 7.1 Indicator Health Metrics

For each indicator and feature:

- **Freshness:** time since last update per symbol.
- **Fill rate:** percentage of non-missing values in last N bars.
- **Range checks:** values within expected ranges (using `state_space` in Phase 5).
- **Drift checks:** distribution shifts vs historical baselines.

These can be implemented as scheduled jobs that:

- Read indicator/feature tables.
- Compute metrics.
- Emit alerts / dashboard entries.


### 7.2 Integration with IFNS Telemetry

Indicator and feature telemetry should be consistent with the broader IFNS telemetry schema, including:

- Event types for:
  - Indicator computation failures.
  - Feature generation failures.
  - Schema mismatches.
- Per-run logs for:
  - Which indicators were computed.
  - Ranges and summary statistics.
  - Warnings on anomalies.

This prepares the ground for later **self-checks** and **auto-disabled** features if they misbehave.


---

## 8. Handover Checklist for Phase 6

For the next engineer / agent implementing this system, the checklist is:

1. **Ingestion:**
   - Implement canonical base tables (bars, fundamentals, events, portfolio, macro).
   - Ensure data quality (no duplicates, correct timezones).

2. **Indicator Engine:**
   - Implement L1 indicators according to `indicators_catalog_L1.csv` (Phase 3).
   - Implement L2/L3 frameworks using `indicators_catalog_L2L3.csv` (Phase 4) and DAG logic.
   - Store outputs in indicator tables with consistent naming.

3. **Feature Service:**
   - Implement transformation from indicator outputs to features using `indicator_feature_schema_v1.csv` (Phase 5).
   - Implement feature packs (Core Value, Core State, etc.).

4. **Backfill & Recalc:**
   - Implement historical backfill pipelines for new universes/timeframes.
   - Implement controlled recalculation when indicator definitions change.

5. **Monitoring:**
   - Implement basic indicator/feature telemetry (freshness, fill-rate, range checks).
   - Wire into IFNS telemetry and dashboards where relevant.

With Phases 1–6 in place, the system is ready for Phase 7, which focuses on **operationalization & ML
integration** (wiring this feature platform into training, evaluation, deployment, and governance cycles).
