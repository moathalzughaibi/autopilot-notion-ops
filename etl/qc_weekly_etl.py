#!/usr/bin/env python3
"""
QC Weekly ETL (with clip-event support)

Adds:
- --clip_glob: path pattern to clip-event logs (NDJSON or CSV)
- Computes overall clip_events_pct and per-family clip_events_pct
- Computes clip_budget_violations using per-feature daily rates vs manifest's clip_policy.max_clipped_pct_per_day
"""

import os, sys, json, glob, argparse, pandas as pd
from datetime import datetime, timedelta
from collections import defaultdict

def load_manifest(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def load_calendar(path):
    if not path or not os.path.exists(path):
        return {"closed": [], "early_close": {}}
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days) + 1):
        yield start_date + timedelta(n)

def expected_rows_for_week(start, end, frequency, calendar):
    closed = set(calendar.get("closed", []))
    early = calendar.get("early_close", {})
    exp = 0
    for d in daterange(start, end):
        ds = d.strftime("%Y-%m-%d")
        if ds in closed: 
            continue
        if frequency == "1d":
            exp += 1
        elif frequency == "1h":
            exp += 3 if ds in early else 7
    return exp

def load_feature_view_rows(input_glob, columns):
    files = sorted(glob.glob(input_glob))
    if not files:
        return pd.DataFrame(columns=columns + ["timestamp"])
    dfs = []
    for fp in files:
        if fp.lower().endswith(".csv"):
            df = pd.read_csv(fp)
        elif fp.lower().endswith(".parquet"):
            df = pd.read_parquet(fp)
        else:
            continue
        keep = [c for c in columns if c in df.columns]
        if "timestamp" in df.columns:
            keep = ["timestamp"] + keep
        df = df[keep]
        dfs.append(df)
    if not dfs:
        return pd.DataFrame(columns=columns + ["timestamp"])
    out = pd.concat(dfs, ignore_index=True)
    if "timestamp" in out.columns:
        out["timestamp"] = pd.to_datetime(out["timestamp"])
        out["date"] = out["timestamp"].dt.date.astype(str)
    return out

def load_clip_events(clip_glob):
    if not clip_glob:
        return pd.DataFrame(columns=["timestamp","date","feature_id"])
    files = sorted(glob.glob(clip_glob))
    if not files:
        return pd.DataFrame(columns=["timestamp","date","feature_id"])
    rows = []
    for fp in files:
        if fp.lower().endswith(".ndjson") or fp.lower().endswith(".jsonl"):
            with open(fp, "r", encoding="utf-8") as f:
                for line in f:
                    line=line.strip()
                    if not line: continue
                    try:
                        obj = json.loads(line)
                        rows.append(obj)
                    except:
                        continue
        elif fp.lower().endswith(".csv"):
            df = pd.read_csv(fp)
            rows.extend(df.to_dict(orient="records"))
    if not rows:
        return pd.DataFrame(columns=["timestamp","date","feature_id"])
    df = pd.DataFrame(rows)
    if "timestamp" in df.columns:
        df["timestamp"] = pd.to_datetime(df["timestamp"])
        df["date"] = df["timestamp"].dt.date.astype(str)
    if "feature_id" not in df.columns:
        df["feature_id"] = ""
    return df[["timestamp","date","feature_id"]]

def compute_weekly_metrics(df_feat, df_clip, manifest):
    cols = manifest["columns"]
    qcm = manifest.get("per_feature_qc", {})
    policy_budget = 0.005  # default 0.5%
    if "policy_defaults" in manifest and "clip_policy" in manifest["policy_defaults"]:
        pb = manifest["policy_defaults"]["clip_policy"].get("max_clipped_pct_per_day", None)
        if isinstance(pb, (int,float)):
            policy_budget = float(pb)

    # Per-feature counts
    per_feat = {}
    # Denominator (per-feature): number of non-NA observations
    for c in cols:
        if c not in df_feat.columns:
            per_feat[c] = {"non_na": 0, "clip_events": 0}
        else:
            non_na = int(df_feat[c].notna().sum())
            per_feat[c] = {"non_na": non_na, "clip_events": 0}

    # Add clip counts (total & per-day for budget checks)
    per_feat_daily = defaultdict(lambda: defaultdict(int))  # feature -> date -> count
    if not df_clip.empty:
        for _, r in df_clip.iterrows():
            fid = r.get("feature_id","")
            if fid in per_feat:
                per_feat[fid]["clip_events"] += 1
                d = r.get("date","")
                if d:
                    per_feat_daily[fid][d] += 1

    # Aggregate: overall clip rate
    total_non_na = sum(v["non_na"] for v in per_feat.values())
    total_clip = sum(v["clip_events"] for v in per_feat.values())
    overall_clip_pct = (total_clip / total_non_na) if total_non_na > 0 else 0.0

    # Family rollups (coverage from df_feat; clip from per_feat)
    fam_roll = {}
    for fid, v in per_feat.items():
        fam = qcm.get(fid, {}).get("family", "OTHER")
        if fam not in fam_roll:
            fam_roll[fam] = {"feature_count": 0, "coverage_acc": 0.0, "na_max": 0.0, "clip_events": 0, "non_na": 0}
        fam_roll[fam]["feature_count"] += 1

        if fid in df_feat.columns and len(df_feat):
            series = df_feat[fid]
            coverage = float(series.notna().mean())
            na_pct = float(series.isna().mean())
        else:
            coverage, na_pct = 0.0, 1.0
        fam_roll[fam]["coverage_acc"] += coverage
        fam_roll[fam]["na_max"] = max(fam_roll[fam]["na_max"], na_pct)
        fam_roll[fam]["clip_events"] += v["clip_events"]
        fam_roll[fam]["non_na"]      += v["non_na"]

    family_breakdown = []
    for fam, agg in fam_roll.items():
        cnt = max(agg["feature_count"], 1)
        fam_clip_pct = (agg["clip_events"] / agg["non_na"]) if agg["non_na"] > 0 else 0.0
        family_breakdown.append({
            "family": fam,
            "feature_count": agg["feature_count"],
            "coverage_pct_mean": agg["coverage_acc"]/cnt,
            "max_na_pct": agg["na_max"],
            "drift_alerts": 0,
            "clip_events_pct": fam_clip_pct
        })

    # Budget violations: per-feature per-day rate vs manifest clip_policy.max_clipped_pct_per_day (if per-feature overrides exist)
    violations = 0
    for fid, day_counts in per_feat_daily.items():
        # per-feature denominator per day ~ number of rows for that day (approx via df_feat date counts)
        if "date" in df_feat.columns:
            df_f = df_feat[["date", fid]].copy() if fid in df_feat.columns else pd.DataFrame(columns=["date", fid])
            denom = df_f.groupby("date")[fid].apply(lambda s: int(s.notna().sum())) if not df_f.empty else pd.Series(dtype=int)
        else:
            denom = pd.Series(dtype=int)
        # budget: per-feature override else policy default
        budget = policy_budget
        pf = qcm.get(fid, {})
        if "clip_policy" in pf and isinstance(pf["clip_policy"], dict):
            b = pf["clip_policy"].get("max_clipped_pct_per_day", None)
            if isinstance(b, (int,float)):
                budget = float(b)

        for d, c in day_counts.items():
            n = int(denom.get(d, 0))
            if n <= 0:
                continue
            rate = c / n
            if rate > budget:
                violations += 1

    return overall_clip_pct, violations, family_breakdown

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--manifest", required=True)
    ap.add_argument("--calendar", required=False, default="")
    ap.add_argument("--input_glob", required=True)
    ap.add_argument("--clip_glob", required=False, default="", help="Path pattern to clip-event logs (NDJSON/CSV)")
    ap.add_argument("--week_end", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    man = load_manifest(args.manifest)
    cal = load_calendar(args.calendar)
    week_end = datetime.fromisoformat(args.week_end).date()
    week_start = week_end - timedelta(days=6)

    df_feat = load_feature_view_rows(args.input_glob, man["columns"])
    # filter to week window if timestamp exists
    if "timestamp" in df_feat.columns:
        df_feat = df_feat[(df_feat["timestamp"].dt.date >= week_start) & (df_feat["timestamp"].dt.date <= week_end)]
    df_clip = load_clip_events(args.clip_glob)
    if not df_clip.empty:
        df_clip = df_clip[(pd.to_datetime(df_clip["timestamp"]).dt.date >= week_start) & (pd.to_datetime(df_clip["timestamp"]).dt.date <= week_end)]

    exp_rows = expected_rows_for_week(week_start, week_end, man["frequency"], cal)
    row_count = len(df_feat)
    integrity = float(row_count) / max(exp_rows, 1)

    # Coverage & NA (mean and max) — as in v0.15
    per_feat_cov = []
    for c in man["columns"]:
        if c in df_feat.columns:
            s = df_feat[c]
            per_feat_cov.append({"coverage": float(s.notna().mean()), "na": float(s.isna().mean())})
        else:
            per_feat_cov.append({"coverage": 0.0, "na": 1.0})
    coverage_pct_mean = sum(p["coverage"] for p in per_feat_cov) / max(len(per_feat_cov), 1)
    max_na_pct_any_feature = max(p["na"] for p in per_feat_cov) if per_feat_cov else 1.0

    # Clip stats
    clip_events_pct, clip_budget_violations, family_breakdown = compute_weekly_metrics(df_feat, df_clip, man)

    record = {
        "ts_week_end": week_end.isoformat(),
        "view": man["view"],
        "horizon": man["horizon"],
        "frequency": man["frequency"],
        "manifest_sha256": man.get("columns_sha256",""),
        "row_count": int(row_count),
        "integrity_pct": round(integrity, 6),
        "coverage_pct_mean": round(coverage_pct_mean, 6),
        "max_na_pct_any_feature": round(max_na_pct_any_feature, 6),
        "drift_alerts_count": 0,
        "clip_events_pct": round(clip_events_pct, 6),
        "clip_budget_violations": int(clip_budget_violations),
        "family_breakdown": family_breakdown,
        "notes": ""
    }
    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    with open(args.out, "a", encoding="utf-8") as f:
        f.write(json.dumps(record) + "\n")
    print(f"Wrote QC weekly line to {args.out}")

if __name__ == "__main__":
    main()
