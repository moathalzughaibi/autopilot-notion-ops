# Phase 4 – Catalog & Feature Universe Surfaces

This handover file focuses on the **CatalogL1 / CatalogL2L3** assets and their related feature-schema spec cards 
under `Manifests & Policy` in IFNS – UI Master (V2). It defines how to turn them into coherent Notion databases, 
and how to attach them to the 14-step IFNS spine without deleting or overwriting any existing content.

## 1. Asset inventory from the export

### 1.1 CatalogL1 assets

- **Table exports (CSV):**

  - `Private & Shared/Autopilot Hub/CatalogL1 066b5cc56f8f4f1baa1059a351e608fa.csv`
  - `Private & Shared/Autopilot Hub/CatalogL1 066b5cc56f8f4f1baa1059a351e608fa_all.csv`
- **Row pages (Notion cards):**

  - `Private & Shared/Autopilot Hub/CatalogL1/Untitled 2afb22c770d98101a7f1d60cf3a06824.md`
  - `Private & Shared/Autopilot Hub/CatalogL1/Untitled 2afb22c770d9810ab07ace6b235c91d1.md`
  - `Private & Shared/Autopilot Hub/CatalogL1/Untitled 2afb22c770d9811789a9d908777b4b29.md`
  - `Private & Shared/Autopilot Hub/CatalogL1/Untitled 2afb22c770d98119b8fcea6d1f1819e3.md`
  - `Private & Shared/Autopilot Hub/CatalogL1/Untitled 2afb22c770d9811dbcfcc70c4a152ae9.md`
  - `…` (plus additional `Untitled …` rows not listed here for brevity)

**CatalogL1 CSV – key columns (truncated):**

```
Name
default_params
default_timeframes
digitization_level
family_role_primary
family_role_secondary
feature_outputs_default
formula_pseudocode
indicator_id
inputs
ml_role_primary
ml_role_secondary
name
notes_phase3
output_type_primary
required_fields
universe_tier
…
```

Example CatalogL1 row (truncated to main conceptual fields):

```
Name: nan
default_params: {"window": 20, "price_field": "close"}
default_timeframes: ["1h","1d"]
digitization_level: formula
family_role_primary: Trend & Price Location
family_role_secondary: nan
feature_outputs_default: {"value": true, "state": false, "events": false}
formula_pseudocode: sma_20_t = mean(close_{t-19}...close_t)
indicator_id: sma_20
inputs: price
ml_role_primary: feature
ml_role_secondary: context
name: Simple Moving Average (20)
notes_phase3: Baseline MA for short/medium trend context.
output_type_primary: scalar
required_fields: close
universe_tier: 0
…
```

### 1.2 CatalogL2L3 assets

- **Table exports (CSV):**

  - `Private & Shared/Autopilot Hub/CatalogL2L3 ef3175fe046d47b88944607d5bcf5d21.csv`
  - `Private & Shared/Autopilot Hub/CatalogL2L3 ef3175fe046d47b88944607d5bcf5d21_all.csv`
- **Row pages (Notion cards):**

  - `Private & Shared/Autopilot Hub/CatalogL2L3/Untitled 2afb22c770d98109b7c1c48ab4664905.md`
  - `Private & Shared/Autopilot Hub/CatalogL2L3/Untitled 2afb22c770d98114862ff215ae0f7572.md`
  - `Private & Shared/Autopilot Hub/CatalogL2L3/Untitled 2afb22c770d981198cb9d4fd70a06273.md`
  - `Private & Shared/Autopilot Hub/CatalogL2L3/Untitled 2afb22c770d9811ea9acc4cddf8619f1.md`
  - `Private & Shared/Autopilot Hub/CatalogL2L3/Untitled 2afb22c770d98130a307c5bae437eefa.md`
  - `…` (plus additional `Untitled …` rows not listed here for brevity)

**CatalogL2L3 CSV – key columns (truncated):**

```
Name
backtest_hooks
construction_type
default_timeframes
dependencies_L1
dependencies_external
digitization_level
family_role_primary
family_role_secondary
feature_outputs_default
indicator_id
inputs
level
ml_role_primary
ml_role_secondary
name
notes_phase4
output_components
output_type_primary
pattern_window
state_space_def
universe_tier
…
```

Example CatalogL2L3 row (truncated to main conceptual fields):

```
Name: nan
backtest_hooks: {"slice_metrics": ["PnL_by_trend_state","hit_rate_by_trend_state"], "gate_usage": ["strategy_activation_by_trend_state"]}
construction_type: state_machine
default_timeframes: ["15m","1h","1d"]
dependencies_L1: ema_12,ema_26,ema_50,sma_20,sma_50,price_location_20,atr_14
dependencies_external: nan
digitization_level: rule
family_role_primary: Trend & Price Location
family_role_secondary: Market Structure & Geometry
feature_outputs_default: {"value": true, "state": true, "events": false}
indicator_id: trend_mtf_v1
inputs: price
level: L3
ml_role_primary: context
ml_role_secondary: feature,filter
name: Multi-Timeframe Trend Framework v1
notes_phase4: Aggregates MA slopes and price location across timeframes into discrete trend states and a score; hysteresis is used to avoid state churning.
output_components: {"trend_state_mtf": "category", "trend_score_mtf": "scalar", "trend_state_short": "category", "trend_state_medium": "category", "trend_state_long": "category"}
…
```

### 1.3 Related V2 spec cards (feature schema & universe)

- **Indicator Feature Schema v1 (with family)**
  - Export path: `Private & Shared/Autopilot Hub/IFNS – UI Master (V2)/Manifests & Policy/Indicator Feature Schema v1 (with family) 2afb22c770d981a5b1c4d980b454ef59.md`
  - URL: https://www.notion.so/2afb22c770d981a5b1c4d980b454ef59
  - Snippet:
    ```
    # Indicator Feature Schema v1 (with family)

    # Indicator Feature Schema v1 (with family)

    This page documents a V2 asset from the consolidated indicators bundle.

    - **File name:** `indicator_feature_schema_v1_with_family.csv`
    - **Repo path:** `sync/ifns/indicator_feature_schema_v1_with_family.csv`
    ```
- **Indicator Feature Schema H1 v1 (with family)**
  - Export path: `Private & Shared/Autopilot Hub/IFNS – UI Master (V2)/Manifests & Policy/Indicator Feature Schema H1 v1 (with family) 2afb22c770d9815ca196d53551ce87a8.md`
  - URL: https://www.notion.so/2afb22c770d9815ca196d53551ce87a8
  - Snippet:
    ```
    # Indicator Feature Schema H1 v1 (with family)

    # Indicator Feature Schema H1 v1 (with family)

    This page documents a V2 asset from the consolidated indicators bundle.

    - **File name:** `indicator_feature_schema_h1_v1_with_family.csv`
    - **Repo path:** `sync/ifns/indicator_feature_schema_h1_v1_with_family.csv`
    ```
- **Feature Policy Matrix**
  - Export path: `Private & Shared/Autopilot Hub/IFNS – UI Master (V2)/Manifests & Policy/Feature Policy Matrix 2afb22c770d981debfc7c75e43c15859.md`
  - URL: https://www.notion.so/2afb22c770d981debfc7c75e43c15859
  - Snippet:
    ```
    # Feature Policy Matrix

    # Feature Policy Matrix

    This page documents a V2 asset from the consolidated indicators bundle.

    - **File name:** `feature_policy_matrix.csv`
    - **Repo path:** `sync/ifns/feature_policy_matrix.csv`
    ```
- **Feature Family Map**
  - Export path: `Private & Shared/Autopilot Hub/IFNS – UI Master (V2)/Manifests & Policy/Feature Family Map 2afb22c770d9810fa271fa0f937a9327.md`
  - URL: https://www.notion.so/2afb22c770d9810fa271fa0f937a9327
  - Snippet:
    ```
    # Feature Family Map

    # Feature Family Map

    This page documents a V2 asset from the consolidated indicators bundle.

    - **File name:** `feature_family_map.csv`
    - **Repo path:** `sync/ifns/feature_family_map.csv`
    ```
- **Indicators – Universe Catalog (Phase 2 Draft)**
  - Export path: `Private & Shared/Autopilot Hub/IFNS – UI Master (V2)/Manifests & Policy/Indicators – Universe Catalog (Phase 2 Draft) 2afb22c770d981f9879ee41191de19b1.md`
  - URL: https://www.notion.so/2afb22c770d981f9879ee41191de19b1
  - Snippet:
    ```
    # Indicators – Universe Catalog (Phase 2 Draft)

    # Indicators – Universe Catalog (Phase 2 Draft)

    This page documents a V2 asset from the consolidated indicators bundle.

    - **File name:** `indicators_universe_catalog_phase2.csv`
    - **Repo path:** `sync/ifns/indicators_universe_catalog_phase2.csv`
    ```
- **Indicators – L1 Catalog (Phase 3)**
  - Export path: `Private & Shared/Autopilot Hub/IFNS – UI Master (V2)/Manifests & Policy/Indicators – L1 Catalog (Phase 3) 2afb22c770d9816b992aced0b0811516.md`
  - URL: https://www.notion.so/2afb22c770d9816b992aced0b0811516
  - Snippet:
    ```
    # Indicators – L1 Catalog (Phase 3)

    # Indicators – L1 Catalog (Phase 3)

    This page documents a V2 asset from the consolidated indicators bundle.

    - **File name:** `indicators_catalog_L1_phase3.csv`
    - **Repo path:** `sync/ifns/indicators_catalog_L1_phase3.csv`
    ```
- **Indicators – L2 L3 Framework Catalog (Phase 4)**
  - Export path: `Private & Shared/Autopilot Hub/IFNS – UI Master (V2)/Manifests & Policy/Indicators – L2 L3 Framework Catalog (Phase 4) 2afb22c770d98140b1d3dc822fe19525.md`
  - URL: https://www.notion.so/2afb22c770d98140b1d3dc822fe19525
  - Snippet:
    ```
    # Indicators – L2/L3 Framework Catalog (Phase 4)

    # Indicators – L2/L3 Framework Catalog (Phase 4)

    This page documents a V2 asset from the consolidated indicators bundle.

    - **File name:** `indicators_catalog_L2L3_phase4.csv`
    - **Repo path:** `sync/ifns/indicators_catalog_L2L3_phase4.csv`
    ```

## 2. Target Notion database design – Feature Catalog

Instead of treating `CatalogL1` and `CatalogL2L3` as separate, opaque tables, we define a unified **Feature Catalog** 
Notion database that can still preserve the notion of levels (L1 vs L2/L3) but feels like a single universe.

### 2.1 Unified Feature Catalog DB

Create a Notion database called `Feature Catalog` with the following properties (mapped from the CSV columns):

| Property | Type | Source | Description |
|----------|------|--------|-------------|
| `Name` | Title | `name` / `Name` | Human-readable indicator / framework name. |
| `indicator_id` | Text | `indicator_id` | Stable machine identifier (used in code & manifests). |
| `level` | Select | `level` or inferred | Indicator level (`L1`, `L2`, `L3`). For CatalogL1 rows, set `L1`; for CatalogL2L3 rows, use `level` column. |
| `digitization_level` | Select | `digitization_level` | How formalized the spec is (formula/rule/state_machine/ML, etc.). |
| `family_role_primary` | Select | `family_role_primary` | Primary family role (e.g. `Trend & Price Location`). |
| `family_role_secondary` | Multi-select | `family_role_secondary` | Secondary roles (e.g. `Market Structure & Geometry`). |
| `ml_role_primary` | Select | `ml_role_primary` | Primary ML role (`feature`, `context`, `target`, `filter`, etc.). |
| `ml_role_secondary` | Multi-select | `ml_role_secondary` | Secondary ML roles (comma-split when imported). |
| `output_type_primary` | Select | `output_type_primary` | Main output type (`scalar`, `vector`, `state`, `event`, etc.). |
| `feature_outputs_default` | Text / JSON | `feature_outputs_default` | Default feature outputs (value/state/events flags). |
| `inputs` | Text | `inputs` | Required input domains (e.g. `price`, `volume`, `hlc3`). |
| `required_fields` | Text | `required_fields` | Specific fields required from the feed (e.g. `close`, `high`, `low`). |
| `default_timeframes` | Text | `default_timeframes` | JSON-like list of default timeframes (e.g. `["1h","1d"]`). |
| `default_params` | Text | `default_params` | JSON-like object of parameters (e.g. `{ "window": 20 }`). |
| `dependencies_L1` | Text | `dependencies_L1` (L2/L3 only) | Upstream L1 indicators used by this L2/L3 framework. |
| `dependencies_external` | Text | `dependencies_external` | External dependencies if any. |
| `construction_type` | Select | `construction_type` (L2/L3) | Construction style (`state_machine`, `composite`, etc.). |
| `output_components` | Text / JSON | `output_components` (L2/L3) | Named outputs for multi-component frameworks. |
| `pattern_window` | Text | `pattern_window` | Window/lag structure if applicable. |
| `state_space_def` | Text | `state_space_def` | State definitions for stateful indicators. |
| `universe_tier` | Select | `universe_tier` (L2/L3) | Tiering for inclusion in default universes. |
| `notes_phase3` / `notes_phase4` | Rich Text | `notes_phase3` / `notes_phase4` | Notes by phase; can be merged into a single rich-text property. |
| `Step link` | Relation | manual | Relation to the relevant Step hubs (07, 08, 10, 12). |
| `Spec cards` | Relation | manual | Relation to V2 spec pages (Feature Schema, Family Map, Policy Matrix, etc.). |

**Views to configure in Notion:**

- `By Level`: Group by `level` so L1 / L2 / L3 frameworks are clearly separated.

- `By Family`: Group by `family_role_primary` (e.g. Trend, Volatility, Market Structure, etc.).

- `By ML Role`: Group by `ml_role_primary` to see which features feed which stages (context vs signal vs control).

- `Universe – Tiered`: Filter by `universe_tier` to show only the default live-ready universe.


**Row-page layout suggestions:**

- Top section: a short prose description (from `notes_phase3/4`).

- Middle section: a table or bullet list of:

  - `indicator_id`, `inputs`, `default_params`, `default_timeframes`.

  - `family_role_primary/secondary`, `ml_role_primary/secondary`.

- Bottom section: links to **Feature Schema**, **Family Map**, **Policy Matrix** rows for this feature (via `Spec cards`).


## 3. Attach Feature Catalog to the 14-step spine

Use the following mapping between the Feature Catalog and the Step hubs (from Phase 1):

| Step | Role | Feature Catalog usage |

|-----:|------|------------------------|

| 07 | Data Intelligence Layer (DIL) | Primary home for Feature Catalog views (by family, by level). |

| 08 | Modeling Intelligence (MI) | Filtered views for `ml_role_primary in {feature, target}` and modeling-relevant tiers. |

| 10 | Market Structural Awareness (MSA) | Views focused on `family_role_primary = Market Structure & Geometry` and related features. |

| 12 | Decision & Risk Architecture (DRA) | Views filtered by features that act as risk controls, guardrails, or governance inputs. |


**Concrete instructions for the Notion agent:**

1. In **Step 07 – DIL hub**, create a `Feature Catalog` section and embed the main `By Level` and `By Family` views.

2. In **Step 08 – MI hub**, embed a `Features for Modeling` view filtered on modeling roles.

3. In **Step 10 – MSA hub**, embed a `Market Structure Features` view filtered on family roles.

4. In **Step 12 – DRA hub**, embed a `Risk & Control Features` view filtered on ML roles and/or tagged via `universe_tier`.


## 4. Link Feature Catalog rows to V2 spec cards

The V2 pages under `Manifests & Policy` act as **spec cards** for the Feature Catalog. The relationships should be:

- `Indicator Feature Schema v1 (with family)` → Column-level schema for features, with family tags.

- `Indicator Feature Schema H1 v1 (with family)` → Time-horizon-specific schema variant.

- `Feature Policy Matrix` → Mapping of features to risk/usage constraints and policy flags.

- `Feature Family Map` → Canonical mapping between indicator families, roles, and higher-level groupings.

- `Universe Catalog (Phase 2 Draft)` → Early draft of the live universe; feeds into `universe_tier`.

- `Indicators – L1 Catalog (Phase 3)` → CSV-backed spec aligned with CatalogL1.

- `Indicators – L2/L3 Framework Catalog (Phase 4)` → CSV-backed spec aligned with CatalogL2L3.


**Relations in Notion:**

- Each **Feature Catalog row** should have a `Spec cards` relation to one or more of these V2 pages.

- Conversely, each V2 spec card can have a rollup/list of related Feature Catalog rows.


**Page-level notes for the Notion agent:**

- `Indicator Feature Schema v1 (with family)` — keep this as a **read-only spec card**; do not paste full table data here.
  - Instead, ensure the underlying CSV is mirrored into the `Feature Catalog` DB or a companion DB,
    and let this page serve as the documentation and context for those fields.

- `Indicator Feature Schema H1 v1 (with family)` — keep this as a **read-only spec card**; do not paste full table data here.
  - Instead, ensure the underlying CSV is mirrored into the `Feature Catalog` DB or a companion DB,
    and let this page serve as the documentation and context for those fields.

- `Feature Policy Matrix` — keep this as a **read-only spec card**; do not paste full table data here.
  - Instead, ensure the underlying CSV is mirrored into the `Feature Catalog` DB or a companion DB,
    and let this page serve as the documentation and context for those fields.

- `Feature Family Map` — keep this as a **read-only spec card**; do not paste full table data here.
  - Instead, ensure the underlying CSV is mirrored into the `Feature Catalog` DB or a companion DB,
    and let this page serve as the documentation and context for those fields.

- `Indicators – Universe Catalog (Phase 2 Draft)` — keep this as a **read-only spec card**; do not paste full table data here.
  - Instead, ensure the underlying CSV is mirrored into the `Feature Catalog` DB or a companion DB,
    and let this page serve as the documentation and context for those fields.

- `Indicators – L1 Catalog (Phase 3)` — keep this as a **read-only spec card**; do not paste full table data here.
  - Instead, ensure the underlying CSV is mirrored into the `Feature Catalog` DB or a companion DB,
    and let this page serve as the documentation and context for those fields.

- `Indicators – L2 L3 Framework Catalog (Phase 4)` — keep this as a **read-only spec card**; do not paste full table data here.
  - Instead, ensure the underlying CSV is mirrored into the `Feature Catalog` DB or a companion DB,
    and let this page serve as the documentation and context for those fields.


## 5. Handling existing CatalogL1 / CatalogL2L3 row pages

The export contains many `Untitled …` row pages under `CatalogL1` and `CatalogL2L3`. To avoid losing history:

1. **Do not delete** any of these pages.

2. For each row page:

   - Link it to the corresponding **Feature Catalog row** (using a relation like `Legacy row page`).

   - Optionally, add a short note at the top: `Superseded by Feature Catalog row XYZ but kept for history`. 

3. Over time, new edits should happen on the Feature Catalog row pages, not on the old `Untitled` cards.


## 6. Implementation checklist for the Notion/Git agent

1. **Create the unified `Feature Catalog` DB** with properties listed in §2.1.

2. **Import CSVs:**

   - Import `CatalogL1 … .csv` and `CatalogL2L3 … .csv` into this DB (or into two staging DBs, then merge).

   - Ensure `indicator_id` is preserved exactly; this is the stable key.

   - Derive `level` as `L1` for rows coming from CatalogL1 and use the `level` column for CatalogL2L3.

3. **Normalize select / multi-select fields:**

   - Normalize `family_role_primary`, `family_role_secondary`, `ml_role_primary`, `ml_role_secondary`, `digitization_level` into consistent select options.

4. **Configure views:**

   - Implement the `By Level`, `By Family`, `By ML Role`, and `Universe – Tiered` views.

5. **Attach to Step hubs:**

   - Embed the appropriate views in the Step 07, 08, 10, and 12 hubs as described in §3.

6. **Wire spec cards:**

   - For each of the V2 spec pages in §4, add relations to the Feature Catalog rows and vice versa.

7. **Preserve legacy row pages:**

   - Create a relation from Feature Catalog rows back to the old `CatalogL1` / `CatalogL2L3` cards.

   - Mark those cards explicitly as historical / legacy in their page headers.

8. **No deletions:**

   - At no point should existing content be deleted. The work is purely additive and relational.
