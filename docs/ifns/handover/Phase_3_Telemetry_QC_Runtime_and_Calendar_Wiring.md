# Phase 3 – Telemetry, QC, Runtime & Calendar Wiring

This handover file turns the existing **Telemetry & QC**, **QCWeekly**, **CalendarGaps2025**, and **Runtime Templates** assets 
into a coherent Notion-first structure that is clearly attached to the 14-step IFNS spine and UI Master V2 surfaces. 
It assumes Phase 1 (14-step hubs) and Phase 2 (V2 attachments) are conceptually in place, but it can be applied independently.

## 1. Asset inventory from the export

### 1.1 Top-level V2 telemetry/runtime pages

| Page | Export Path | URL |
|------|-------------|-----|
| Telemetry & QC | Private & Shared/Autopilot Hub/IFNS – UI Master (V2)/Telemetry & QC 2afb22c770d9818882dcc1548e951932.md | https://www.notion.so/2afb22c770d9818882dcc1548e951932 |
| Runtime Templates & Calendars | Private & Shared/Autopilot Hub/IFNS – UI Master (V2)/Runtime Templates & Calendars 2afb22c770d9811b973ec99095e81a7e.md | https://www.notion.so/2afb22c770d9811b973ec99095e81a7e |

### 1.2 Telemetry & QC child spec cards

| # | Title | Export Path |
|---|-------|-------------|
| 1 | CI IFNS Guard Workflow | Private & Shared/Autopilot Hub/IFNS – UI Master (V2)/Telemetry & QC/CI IFNS Guard Workflow 2afb22c770d98109ba8bfbf5fbede124.md |
| 2 | CI Manifest Guard (Python) | Private & Shared/Autopilot Hub/IFNS – UI Master (V2)/Telemetry & QC/CI Manifest Guard (Python) 2afb22c770d9812496aafd166f4e6ced.md |
| 3 | IO Utils (Telemetry Manifest I O helpers) | Private & Shared/Autopilot Hub/IFNS – UI Master (V2)/Telemetry & QC/IO Utils (Telemetry Manifest I O helpers) 2afb22c770d98191b530dc3c70c67420.md |
| 4 | Manifest Diff Tool | Private & Shared/Autopilot Hub/IFNS – UI Master (V2)/Telemetry & QC/Manifest Diff Tool 2afb22c770d98182a3cfc3ac35dd9d10.md |
| 5 | QC Weekly ETL Clip Integration | Private & Shared/Autopilot Hub/IFNS – UI Master (V2)/Telemetry & QC/QC Weekly ETL Clip Integration 2afb22c770d98123954dc16073a49902.md |
| 6 | QC Weekly ETL Script | Private & Shared/Autopilot Hub/IFNS – UI Master (V2)/Telemetry & QC/QC Weekly ETL Script 2afb22c770d9815ca652e513fa0b348a.md |
| 7 | QC Weekly ETL Skeleton | Private & Shared/Autopilot Hub/IFNS – UI Master (V2)/Telemetry & QC/QC Weekly ETL Skeleton 2afb22c770d98194bcc0e5b10a6288d4.md |
| 8 | QC Weekly Example v1 | Private & Shared/Autopilot Hub/IFNS – UI Master (V2)/Telemetry & QC/QC Weekly Example v1 2afb22c770d9818c99dbc237eb46fdc0.md |
| 9 | QC Weekly Schema v1 | Private & Shared/Autopilot Hub/IFNS – UI Master (V2)/Telemetry & QC/QC Weekly Schema v1 2afb22c770d981c79fb7e76a3ae1511e.md |
| 10 | QC Weekly Telemetry V1 (Doc) | Private & Shared/Autopilot Hub/IFNS – UI Master (V2)/Telemetry & QC/QC Weekly Telemetry V1 (Doc) 2afb22c770d981d7b5e2e07d40a63326.md |

### 1.3 Runtime child spec cards

| # | Title | Export Path |
|---|-------|-------------|
| 1 | Runtime Templates (YAML) | Private & Shared/Autopilot Hub/IFNS – UI Master (V2)/Runtime Templates & Calendars/Runtime Templates (YAML) 2afb22c770d98194bf46d590918f802f.md |
| 2 | Runtime – Calendar Gaps 2025 | Private & Shared/Autopilot Hub/IFNS – UI Master (V2)/Runtime Templates & Calendars/Runtime – Calendar Gaps 2025 2afb22c770d981bc8461e491fd37d89a.md |

### 1.4 QCWeekly & CalendarGaps2025 databases

**QCWeekly (table export)**

- CSV: `Private & Shared/Autopilot Hub/QCWeekly cee29b9e407145a5bb9d9a4f7b543ceb.csv`
- Columns: `Name, clip_budget_violations, clip_events_pct, coverage_pct_mean, drift_alerts_count, entry_id, family_breakdown, frequency, horizon, integrity_pct, manifest_sha256, max_na_pct_any_feature, notes, row_count, ts_week_end, view`
- Example row (first row):
  ```
  Name: nan
  clip_budget_violations: 0
  clip_events_pct: 0.003
  coverage_pct_mean: 0.977
  drift_alerts_count: 3
  entry_id: d954f565c56e46acb4084ce40951f0a156730114
  family_breakdown: {'family': 'CONTEXT' 'feature_count': 4 'coverage_pct_mean': 0.955 'max_na_pct': 0.045 'dr, {'family': 'MOMENTUM' 'feature_count': 8 'coverage_pct_mean': 0.981 'max_na_pct': 0.018 'd, {'family': 'TREND' 'feature_count': 6 'coverage_pct_mean': 0.979 'max_na_pct': 0.019 'drif, {'family': 'VOLATILITY' 'feature_count': 2 'coverage_pct_mean': 0.975 'max_na_pct': 0.022 
  frequency: 1h
  horizon: H1
  integrity_pct: 0.982
  manifest_sha256: MANIFEST_SHA_H1_PLACEHOLDER
  max_na_pct_any_feature: 0.021
  notes: Thanksgiving week; early close Friday handled.
  row_count: 98000
  ts_week_end: 2025-11-28
  view: H1_v1_0
  ```

**QCWeekly row pages** (Notion card-level pages)

- `Private & Shared/Autopilot Hub/QCWeekly cee29b9e/Untitled 2afb22c770d98149895df391e88160e5.md`
  ```
  # Untitled

  clip_budget_violations: 0
  clip_events_pct: 0.001
  coverage_pct_mean: 0.988
  drift_alerts_count: 0
  entry_id: 4c6bac10f6d5940b4d19c488b86e4de2564c65d4
  family_breakdown: {'family': 'CONTEXT' 'feature_count': 4 'coverage_pct_mean': 0.97 'max_na_pct': 0.03 'drif, {'family': 'MOMENTUM' 'feature_count': 7 'coverage_pct_mean': 0.99 'max_na_pct': 0.009 'dr, {'family': 'TREND' 'feature_count': 6 'coverage_pct_mean': 0.989 'max_na_pct': 0.01 'drift, {'family': 'VOLATILITY' 'feature_count': 2 'coverage_pct_mean': 0.987 'max_na_pct': 0.012 
  frequency: 1d
  horizon: D1
  ```
- `Private & Shared/Autopilot Hub/QCWeekly cee29b9e/Untitled 2afb22c770d981daa60ae97e856bf5b4.md`
  ```
  # Untitled

  clip_budget_violations: 0
  clip_events_pct: 0.003
  coverage_pct_mean: 0.977
  drift_alerts_count: 3
  entry_id: d954f565c56e46acb4084ce40951f0a156730114
  family_breakdown: {'family': 'CONTEXT' 'feature_count': 4 'coverage_pct_mean': 0.955 'max_na_pct': 0.045 'dr, {'family': 'MOMENTUM' 'feature_count': 8 'coverage_pct_mean': 0.981 'max_na_pct': 0.018 'd, {'family': 'TREND' 'feature_count': 6 'coverage_pct_mean': 0.979 'max_na_pct': 0.019 'drif, {'family': 'VOLATILITY' 'feature_count': 2 'coverage_pct_mean': 0.975 'max_na_pct': 0.022 
  frequency: 1h
  horizon: H1
  ```

**CalendarGaps2025 (table export)**

- CSV: `Private & Shared/Autopilot Hub/CalendarGaps2025 2afb22c770d98100ae4ad9f64b6b6441.csv`
- Columns: `event_id, date, market, notes, reason`
- Example rows:
  ```
  event_id=gap-2025-01-01, date=2025-01-01, market=US, notes=No trading, reason=Holiday • New Year
  event_id=gap-2025-01-20, date=2025-01-20, market=US, notes=No trading, reason=Holiday  MLK Day
  ```

**CalendarGaps2025 row pages**

- `Private & Shared/Autopilot Hub/CalendarGaps2025/gap-2025-01-20 2afb22c770d981b29ebccd46b3699f36.md`
  ```
  # gap-2025-01-20

  date: 2025-01-20
  market: US
  notes: No trading
  reason: Holiday  MLK Day
  ```
- `Private & Shared/Autopilot Hub/CalendarGaps2025/gap-2025-01-01 2afb22c770d981ff879aef532b29b05f.md`
  ```
  # gap-2025-01-01

  date: 2025-01-01
  market: US
  notes: No trading
  reason: Holiday • New Year
  ```

## 2. Target Notion database designs

### 2.1 QCWeekly – Telemetry snapshots database

Create a **Notion database** called `QCWeekly` with the following properties:

| Property | Type | Description |
|----------|------|-------------|
| `Name` | Title | Human-readable label for the snapshot (e.g. `QC – XNYS – H1 – Week 2025-11-28`). |
| `ts_week_end` | Date | Week end timestamp (from CSV). |
| `market` | Select / Text | Optional: exchange/venue label (derive from `view` or `notes` if needed). |
| `view` | Select | Logical view identifier (e.g. `H1_v1_0`). |
| `frequency` | Select | Sampling frequency (`1d`, `1h`, etc.). |
| `horizon` | Select | Horizon (`D1`, `H1`, etc.). |
| `row_count` | Number | Number of rows observed in the week. |
| `coverage_pct_mean` | Number (percent) | Mean feature coverage across the week. |
| `integrity_pct` | Number (percent) | Integrity score for the snapshot. |
| `max_na_pct_any_feature` | Number (percent) | Max NA rate across any feature. |
| `clip_budget_violations` | Number | Number of clipping budget breaches. |
| `clip_events_pct` | Number (percent) | Fraction of events affected by clipping. |
| `drift_alerts_count` | Number | Number of drift alerts fired. |
| `manifest_sha256` | Text | Manifest fingerprint used for this snapshot. |
| `family_breakdown` | Rich Text / JSON | Structured breakdown of families (CONTEXT, MICRO, etc.). |
| `notes` | Rich Text | Operator notes (e.g. holiday explanations). |
| `entry_id` | Text | Stable identifier from the telemetry payload. |
| `Step link` | Relation | Relation to the relevant **Step hub(s)** (07, 08, 09, 12, 13). |
| `V2 spec` | Relation | Relation to `Telemetry & QC` V2 spec card. |

**Views to configure in Notion:**

- `By Week`: Group by `ts_week_end`, filter last N weeks.

- `By Horizon`: Group by `horizon` and `view` to compare coverage and integrity across regimes.

- `Watchlist – Drift & Coverage`: Filter where `drift_alerts_count > 0` or `coverage_pct_mean < 0.98` or `clip_budget_violations > 0`.

- `Holiday / Special Weeks`: Filter on `notes` containing `Holiday`, `event`, or being non-empty.


**Row-page layout:**

- At the top of each row page, add a short summary block: `Week end, horizon, integrity, key issues.`

- Below, embed:

  - The raw JSON payload (if practical),

  - Links back to the **manifest** (via `manifest_sha256`) and any **Calendar gaps** for that week.


### 2.2 CalendarGaps2025 – Market schedule exceptions database

Create a **Notion database** called `CalendarGaps2025` with the following properties (mirroring the CSV):

| Property | Type | Description |
|----------|------|-------------|
| `event_id` | Title | Unique identifier (e.g. `gap-2025-01-01`). |
| `date` | Date | Date of the trading gap. |
| `market` | Select | Market/venue (e.g. `US`, `XNAS`, etc.). |
| `reason` | Text | Short reason (e.g. `Holiday • New Year`). |
| `notes` | Rich Text | Additional context (e.g. `No trading`, early close notes). |
| `Step link` | Relation | Relation to Step 04 (timeline), Step 09 (execution), and Step 12 (risk). |
| `Runtime link` | Relation | Relation to `Runtime – Calendar Gaps 2025` V2 spec card. |

**Views to configure in Notion:**

- `By Month`: Calendar view showing gaps by `date`.

- `By Market`: Table grouped by `market`.

- `Risk-Sensitive Gaps`: Filter where `reason` contains key phrases like `Holiday`, `Early close`, or `Unscheduled`.


### 2.3 Linking QCWeekly and CalendarGaps together

Once both DBs exist:

1. Add a relation from **QCWeekly → CalendarGaps2025** using `ts_week_end` and `date` proximity as the linking logic (operator-driven).

2. In QCWeekly row pages for special weeks (e.g. Thanksgiving), add links to the relevant `gap` rows from CalendarGaps.

3. In CalendarGaps row pages, embed a filtered view of QCWeekly constrained to the week of that gap.


## 3. Attach telemetry/runtime DBs to the 14-step spine

Use the following attachments between the databases and the Step hubs (as defined in Phase 1):

| Step | Role | Telemetry / Runtime attachments |

|-----:|------|----------------------------------|

| 04 | Preface Timeline / Evolution | Link to `Runtime Templates & Calendars` page + a filtered view of `CalendarGaps2025`. |

| 07 | Data Intelligence Layer (DIL) | Link to `Telemetry & QC` + main `QCWeekly` views (data health). |

| 08 | Modeling Intelligence (MI) | Same `QCWeekly` DB, filtered by modeling horizons; link drift/coverage metrics. |

| 09 | Execution Intelligence (EI) | Runtime surfaces (`Runtime Templates (YAML)`, `Runtime – Calendar Gaps 2025`) and QC snapshots affecting execution. |

| 12 | Decision & Risk Architecture (DRA) | `Watchlist – Drift & Coverage` view + high-risk calendar gaps. |

| 13 | Self-Evaluation & Learning (SEL) | Longitudinal `QCWeekly` trends, e.g. views over many weeks for learning loops. |


**Concrete instructions for the Notion agent:**

1. In each Step hub above, insert a `Telemetry & Runtime` section.

2. Embed the relevant Notion DB **views** there (not just links), so a reader can see live tables from QCWeekly and CalendarGaps2025.

3. Ensure that each QCWeekly and CalendarGaps row has its `Step link` relations set where appropriate (can be done gradually).


## 4. Tying DBs back to V2 spec cards

The V2 pages under `Telemetry & QC` and `Runtime Templates & Calendars` should become **spec cards** for these databases:

- `Telemetry & QC`: parent spec card for `QCWeekly` DB and any future telemetry DBs.

- `QC Weekly Schema v1`: documents the JSON schema; link it from the `QCWeekly` DB description and from the DB itself via a `Spec` relation.

- `QC Weekly Example v1`: example payloads; link similarly as sample data for implementers.

- `QC Weekly Telemetry V1 (Doc)`: narrative doc; embed links to both the DB and the schema.

- `QC Weekly ETL Skeleton / Clip Integration / ETL Script`: implementation notes; link from `Step 07` and `Step 08` hubs under implementation subsections.

- `Manifest I/O helpers`, `Manifest Diff Tool`, `CI IFNS Guard Workflow`, `CI Manifest Guard (Python)`: automation guards; link strongly from `Step 12 – DRA`.

- `Runtime Templates & Calendars`: parent spec card for both `CalendarGaps2025` DB and `Runtime Templates (YAML)` page.

- `Runtime – Calendar Gaps 2025`: narrative/doc spec for how calendar gaps feed runtime behavior; cross-linked from `CalendarGaps2025` DB.

- `Runtime Templates (YAML)`: implementation details for runtime jobs; link from `Step 09` and `Step 12` hubs and from any harness/mirror specs.


## 5. Implementation checklist for the Notion/Git agent

1. **Create/verify Notion DBs:**

   - `QCWeekly` DB with properties listed in §2.1.

   - `CalendarGaps2025` DB with properties listed in §2.2.

2. **Backfill records:**

   - Import the CSV rows into the corresponding DBs.

   - For QCWeekly, ensure the numeric fields (`coverage_pct_mean`, `integrity_pct`, etc.) use proper number/percent types.

3. **Configure core views:**

   - Add the `By Week`, `By Horizon`, `Watchlist – Drift & Coverage`, and `Holiday / Special Weeks` views for QCWeekly.

   - Add `By Month`, `By Market`, and `Risk-Sensitive Gaps` views for CalendarGaps2025.

4. **Wire DBs into Step hubs:**

   - For Steps 04, 07, 08, 09, 12, 13, embed the appropriate DB views under a `Telemetry & Runtime` section.

5. **Link spec cards:**

   - From each DB, add relations to the relevant V2 spec pages listed in §4.

   - From each V2 spec card, add back-links to the DBs (either via relations or inline links).

6. **Gradual enrichment:**

   - Over time, set the `Step link` relations on QCWeekly and CalendarGaps rows to match where they matter most.

   - Do not delete or overwrite any existing Notion pages; only add structure, relations, and views.
