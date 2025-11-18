# Stock Indicator System — Master Index (Phases 1–7)

Version: v0.1

This file is a **navigation map** for the entire Stock Indicator System within IFNS.  
It shows what each phase does, where its artifacts live, and how a new engineer/agent should read them.

---

## 0. Recommended Reading Order

1. **Phase 1 – Taxonomy & Governance**  
   *What exists and how we classify it.*

2. **Phase 2 – Indicator Universe Draft**  
   *Long list of possible indicators across families.*

3. **Phase 3 – L1 Indicator Catalog**  
   *Atomic, formula-level indicators, implementation-ready.*

4. **Phase 4 – L2/L3 Framework Catalog**  
   *Composite/context frameworks: trend, structure, regimes, risk, etc.*

5. **Phase 5 – Feature Output & Digitization Schema**  
   *Exactly which feature columns we expose and how.*

6. **Phase 6 – Implementation & Runtime Templates**  
   *How to actually run the indicator & feature system (architecture + patterns).*

7. **Phase 7 – ML Integration & Operationalization**  
   *How features flow into ML, backtesting, live trading, and governance.*


---

## 1. File Map (Markdown Specs)

Below are the core **.md specs** for the indicator system.  
Suggested path root: `docs/ifns/`

1. **Phase 1 – Taxonomy & Governance**  
   - `Indicators_Taxonomy_Phase1.md`  
   - Contents: families (Trend, Momentum, Volatility, Volume, Structure, Candle, Fundamentals, Event/Regime, Risk), levels (L1/L2/L3), output types, digitization levels, governance rules.

2. **Phase 2 – Indicator Universe Draft**  
   - `Indicators_Universe_Phase2.md`  
   - Contents: longlist of candidate indicators, tagged by family, tier (0/1/2), digitization potential.

3. **Phase 3 – L1 Indicator Catalog**  
   - `Indicators_L1_Catalog_Phase3.md`  
   - Contents: schema for L1 indicators, detailed rows for core L1 set (RSI, ATR, MAs, volume, candles, fundamentals, basic risk).

4. **Phase 4 – L2/L3 Framework Catalog**  
   - `Indicators_L2L3_Catalog_Phase4.md`  
   - Contents: frameworks like `trend_mtf_v1`, `structure_mtf_v1`, `sr_zone_v1`, `vol_regime_state_v1`, `liq_stress_v1`, `stress_state_v1`, `regime_cluster_id_v1`, etc.

5. **Phase 5 – Feature Output & Digitization Schema**  
   - `Indicators_Feature_Schema_Phase5.md`  
   - Contents: feature channels (`value`, `state`, `event`, `episode`, `vector`), naming rules, and v1 feature packs.

6. **Phase 6 – Implementation & Runtime Templates**  
   - `Indicators_Implementation_Templates_Phase6.md`  
   - Contents: runtime architecture (Ingestion → Indicator Engine → Feature Service → Serving), indicator/feature service templates, backfill & monitoring patterns.

7. **Phase 7 – ML Integration & Operationalization**  
   - `Indicators_ML_Integration_Phase7.md`  
   - Contents: how features connect to ML pipelines, model recipes & feature packs, model registry, live inference, governance, and telemetry.


---

## 2. File Map (CSV / Machine Artifacts)

Suggested root: `sync/ifns/`

1. **L1 Indicator Catalog (Phase 3)**  
   - `indicators_catalog_L1.csv` *or* `indicators_catalog_L1_phase3.csv`  
   - Purpose: single source of truth for atomic indicators (inputs, params, formula pseudocode, default timeframes, ML roles).

2. **L2/L3 Framework Catalog (Phase 4)**  
   - `indicators_catalog_L2L3.csv` *or* `indicators_catalog_L2L3_phase4.csv`  
   - Purpose: describes composite frameworks (dependencies, construction type, state space, backtest hooks, roles).

3. **Feature Schema (Phase 5)**  
   - `indicator_feature_schema_v1.csv`  
   - Purpose: defines **actual feature columns** (feature_id, dtype, channel, default timeframe, aggregation, missing policy, enabled_default).


---

## 3. How a New Engineer / Agent Should Use This Index

### Step 1 — Understand the Design Space
- Read **Phase 1** (taxonomy) and **Phase 2** (universe) to understand the **full menu** of indicators and families.

### Step 2 — Understand What Actually Exists in v1
- Read **Phase 3** and **Phase 4**, and open their CSVs:
  - L1: what atomic signals are defined and how.
  - L2/L3: what frameworks (trend, regime, risk, etc.) exist and their dependencies.

### Step 3 — Understand What Features Models See
- Read **Phase 5** and inspect `indicator_feature_schema_v1.csv`:
  - Which outputs become `value` / `state` / `event` / `vector` features.
  - Which features are **enabled by default** in v1 packs.

### Step 4 — Understand How to Implement & Run
- Read **Phase 6**:
  - How to wire ingestion → Indicator Engine → Feature Service.
  - How to run backfills and recalc when definitions change.
  - How to store and query indicators and features.

### Step 5 — Understand ML & Trading Integration
- Read **Phase 7**:
  - How feature packs feed model recipes and backtests.
  - How models are versioned, deployed, and monitored.
  - How indicators and features are used in risk gates and governance.

After this 5-step path, the engineer/agent should be able to:

- Add new indicators cleanly (Phase 2 → 3 → 5).
- Extend frameworks (Phase 4).
- Add/modify feature columns (Phase 5).
- Implement or adjust the runtime (Phase 6).
- Plug everything into ML / trading safely (Phase 7).


---

## 4. Notion / Documentation Integration

Recommended Notion structure (mirroring this index):

- **Page:** `IFNS – Stock Indicator System`
  - Sub-pages:
    - `Phase 1 – Taxonomy & Governance`
    - `Phase 2 – Indicator Universe`
    - `Phase 3 – L1 Indicator Catalog`
    - `Phase 4 – L2/L3 Framework Catalog`
    - `Phase 5 – Feature Schema`
    - `Phase 6 – Implementation Templates`
    - `Phase 7 – ML Integration`
  - Linked databases:
    - `Indicators – L1 Catalog` (sync from `indicators_catalog_L1*.csv`)
    - `Indicators – L2/L3 Frameworks` (sync from `indicators_catalog_L2L3*.csv`)
    - `Indicator Feature Schema v1` (sync from `indicator_feature_schema_v1.csv`)

This `Master Index` file should sit at the top of the Notion section and in the repo root of the
indicator docs:

- `docs/ifns/Indicators_Master_Index.md`


---

## 5. Maintenance Notes

- When a new phase or major version is created (e.g., `indicator_feature_schema_v2`):
  - Add a new section or line in this index with clear **version tags**.
  - Do **not** delete or overwrite old entries; keep historical versions for reproducibility.

- Any new engineer/agent should always start from this index and confirm:
  - Which phase versions are considered **current baseline**.
  - Which are historical / legacy.

This keeps the Stock Indicator System navigable even as it grows in depth and complexity.
