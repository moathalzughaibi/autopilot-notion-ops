# Step 13 – Section 9.0: Self‑Evaluation & Learning (SEL)

## 01 – Narrative & Intent

This step defines **Self‑Evaluation & Learning (SEL)** — the meta‑layer of IFNS that continuously evaluates how the system is performing and uses that evidence to **improve models, policies, and configurations over time**.

Where:

- DIL, MI, MSA, MSI, EI, and DRA describe how IFNS *acts right now*,
- **SEL** describes how IFNS **learns from its past actions and observations** to shape its future behavior.

SEL answers questions such as:

- *Are our models, integration logic, and risk policies actually working in the real world?*
- *Where are we over‑confident, under‑confident, or structurally wrong?*
- *What should we retrain, re‑evaluate, promote, roll back, or retire — and why?*

The intent of this step is to:

1. Define SEL as a **continuous learning loop** that spans offline, paper, and live environments.
2. Specify the **evidence, metrics, and workflows** that drive retraining, promotion, and policy updates.
3. Ensure that learning is **structured, explainable, and auditable**, not ad‑hoc tuning.

By the end of this step, IFNS is not just a static engine; it is a system with a clear, governed path for getting smarter over time.

---

### 1. Role of SEL in the IFNS Stack

SEL sits above all other layers as the **meta‑observer and planner**:

- **Inputs**
  - Backtest metrics and diagnostics (from Stage 4).
  - Paper‑run and live‑run KPIs and telemetry (from Stages 6 and 7).
  - Execution metrics (slippage, TE, fill quality).
  - Risk metrics (envelope usage, breaches, kill switch and cooldown events).
  - Incident logs, reasoning reports, and operator feedback.

- **Outputs**
  - **Learning decisions and recommendations**, such as:
    - Retrain or refresh specific models or families.
    - Change MSI weighting or conflict rules.
    - Adjust risk envelopes or gate thresholds.
    - Refine DIL feature frameworks or labeling policies.
  - **Promotion and rollback proposals** for models and strategies.
  - **Roadmaps and review schedules** (e.g., quarterly re‑evaluations of specific components).

SEL does not directly execute trades or change policies; instead, it **produces structured recommendations and tasks** that flow into DRA and Admin workflows for approval and implementation.

---

### 2. The Continuous Learning Loop

SEL operates as a continuous loop from data to decision to outcome to learning:

1. **Plan**
   - Define what we expect from models, strategies, and policies:
     - Target KPIs (e.g., Sharpe, hit rate, TE, slippage bands).
     - Risk and envelope expectations.
     - Operational constraints (incident rates, execution failure tolerances).

2. **Observe**
   - Collect evidence from:
     - Backtests,
     - Paper sessions,
     - Live sessions,
     - Incidents and runbook executions.
   - Consolidate this evidence into **performance dashboards and datasets**.

3. **Diagnose**
   - Identify:
     - Under‑performing models, strategies, or integration rules.
     - Regimes where performance is systematically weaker or stronger.
     - Sources of incidents and operational friction.
   - Use both quantitative analysis and narrative reasoning.

4. **Decide**
   - Formulate **recommendations**:
     - Retraining specific models with updated data ranges or features.
     - Changing MSI policies (weights, eligibility, conflict thresholds).
     - Adjusting DRA envelopes or promotion/rollback criteria.
     - Refining feature frameworks or labeling policies in DIL.

5. **Act**
   - Convert recommendations into:
     - Approved changes in Admin (model promotions/retirements, policy updates).
     - Scheduled retraining jobs and experiments.
     - Updates to documentation and SxE surfaces.

6. **Review**
   - Evaluate the impact of changes:
     - Did performance improve?
     - Did risk behavior improve or degrade?
     - Are incidents less frequent or better handled?

This loop ensures IFNS evolves **deliberately and evidence‑first**, not haphazardly.

---

### 3. Evidence, Metrics, and Learning Artifacts

SEL relies on a well‑defined set of **learning artifacts** and metrics, built from telemetry and registries:

- **Performance Evidence**
  - Backtest metrics by strategy, regime, and period.
  - Paper‑run and live‑run KPIs (Sharpe, TE, drawdowns, hit rates, slippage, etc.).
  - Per‑model and per‑MSI‑policy performance breakdowns.

- **Risk & Incident Evidence**
  - Envelope usage and breach statistics.
  - Kill switch and cooldown activations and their causes.
  - Incident frequency, types, and resolution quality.

- **Execution Evidence**
  - Slippage and TE distributions vs. targets.
  - Rejection rates and reasons.
  - Execution anomalies correlated with structure, regime, or policy changes.

- **Learning Datasets**
  - Aggregations of telemetry into **learning tables**, for example:
    - `Model_Performance_By_Regime`,
    - `Strategy_Performance_By_Structure`,
    - `Execution_Quality_By_Route`,
    - `Risk_Breaches_By_Envelope_And_Condition`.

These artifacts are stored in structured tables/JSON and are accessible to both automated analysis and human reviewers.

---

### 4. Retraining, Refresh, and Experiment Cycles

SEL orchestrates **retraining and refresh cycles** for models and policies.

Key elements:

- **Retraining Schedules**
  - Baseline schedules (e.g., monthly, quarterly) for model retraining.
  - Event‑driven retraining (e.g., after a regime shift or significant performance change).

- **Retraining Specs**
  - Which datasets to use (time ranges, markets, regimes).
  - What label and feature versions to apply.
  - Whether to:
    - Maintain architecture,
    - Tune hyperparameters,
    - Experiment with new architectures.

- **Experiment Coordination**
  - SEL uses the **Experiment Log** and **Model Registry** to:
    - Track which retraining and new model experiments are in flight.
    - Ensure results are compared against baselines and prior versions.
  - Recommendations are made based on:
    - Statistically robust improvements,
    - Operational side‑effects (e.g., more complex models vs. marginal performance gains).

- **Refresh vs. Replace**
  - SEL distinguishes between:
    - Simple **refreshes** (retrain same model family on more recent data),
    - **Replacements** (new architectures, new families),
    - **Retirements** (models that should no longer be used).

SEL ensures that retraining is not an uncontrolled, constant churn; instead, it is a **planned, governed process**.

---

### 5. Learning‑Driven Promotions, Rollbacks, and Policy Updates

SEL feeds **promotion, rollback, and policy update proposals** into DRA and Admin workflows:

- **Promotions**
  - SEL aggregates evidence for candidate models and strategies:
    - Backtests,
    - Paper runs,
    - Live canary performance,
    - Execution and risk behavior.
  - Produces a **Promotion Dossier**:
    - Summary metrics vs. baselines,
    - Regime‑specific strengths and weaknesses,
    - Risk and incident profile.
  - DRA then applies gate logic to decide whether to promote.

- **Rollbacks**
  - SEL monitors ongoing performance:
    - Detects degradation, instability, or structural mismatch.
    - Correlates issues with:
      - Recent changes,
      - Regime shifts,
      - Data quality issues.
  - Issues **Rollback Recommendations** when evidence shows persistent or dangerous under‑performance.

- **Policy Updates**
  - Based on SEL analysis, recommendations may include:
    - Tightening or relaxing risk envelopes.
    - Updating MSI integration policies.
    - Adjusting execution policies (routes, pacing, slippage limits).
  - These proposals are structured and sent to Admin for review and approval.

This keeps change management **anchored in SEL’s evidence**, while ensuring final authority remains with DRA and governed Admin workflows.

---

### 6. SxE Representation of SEL

SEL is surfaced in SxE as both **analytics** and **governance tooling**:

- **Mirror**
  - Learning dashboards:
    - Long‑horizon performance curves for models and strategies.
    - Before‑and‑after comparisons for major changes (e.g., model promotions, policy updates).
  - Health indicators:
    - Areas where IFNS is over/under‑performing expectations.
    - Regimes or structures where reliability is low.

- **Admin**
  - **Learning & Review Console**
    - Scheduled review agendas (e.g., monthly model reviews, quarterly risk reviews).
    - Lists of recommendations from SEL:
      - Pending promotions or rollbacks.
      - Suggested policy adjustments.
  - **Dossiers & Evidence**
    - Access to Promotion Dossiers, Rollback Reports, and Learning Notes.
    - Links to underlying metrics, charts, and telemetry tables.

SEL’s SxE presence ensures that learning is **visible, planned, and traceable**, not buried in code or scattered notebooks.

---

## 02 – Implementation Reference

Self‑Evaluation & Learning is implemented across multiple stages of the **IFNS – Core ML Build Specification**:

- **Stage 3 – Modeling & Training**
  - Provides the **Experiment Log**, training runs, and model metrics that SEL uses to evaluate model quality and retraining needs.

- **Stage 4 – Backtesting & Evaluation**
  - Generates backtest metrics and scenario analyses that feed into SEL’s performance evidence.
  - Supports experiments with alternative configurations to explore sensitivity and robustness.

- **Stage 5 – Risk, Execution & SxE Link**
  - Encodes promotion and rollback rules, risk envelopes, and incident behaviors that SEL analyses and influences.
  - Provides DRA decision outcomes (allow/reduce/deny) and gate activations as part of SEL’s evidence base.

- **Stage 6 – Paper Trading**
  - Produces paper‑run KPIs and telemetry:
    - Session‑level performance,
    - Execution quality,
    - Incidents and near‑misses.
  - SEL uses this evidence:
    - To validate models and policies under real‑time but capital‑free conditions.

- **Stage 7 – Live Trading & Operations**
  - Provides live‑run KPIs, incident logs, and Change Log entries that SEL analyzes for:
    - Long‑term drifts and degradation,
    - Impact of policy changes,
    - Structural regime impacts.

Implementation‑wise, SEL is supported by:

- Tables such as:
  - `SEL_Performance_Summary`,
  - `SEL_Model_Evidence`,
  - `SEL_Strategy_Evidence`,
  - `SEL_Recommendations`,
  - `SEL_Review_Schedule`.
- JSON/NDJSON artifacts for:
  - Learning events,
  - Dossiers and recommendation records.

Any new SEL logic or tools should:

1. Extend these evidence and recommendation structures rather than inventing untracked paths.
2. Ensure that outputs are consumable by Admin and DRA workflows.
3. Maintain traceability from **recommendation → decision → impact**.

---

## 03 – Notes & Decisions

- SEL should **not** directly change live configurations or deploy models; it should propose and justify changes that DRA and Admin workflows approve and enact.
- Learning loops must avoid **overfitting to short‑term noise**:
  - Review horizons and stability criteria should be explicitly defined.
  - Changes should be justified over sufficient time and scenario coverage.
- All significant SEL‑driven recommendations should:
  - Be recorded as structured records (not just free‑form text),
  - Include links to underlying evidence and metrics,
  - Have explicit owners and review dates.
- As IFNS matures, SEL can incorporate more advanced techniques:
  - Meta‑learning over which models and policies perform best under which conditions,
  - Automated proposal generation for configuration sweeps,
  - Simulation of hypothetical changes before deployment.
  - However, these must still be governed through the same **transparent, auditable workflows** described here.
