#!/usr/bin/env python3
"""
IFNS Schema Linter — tags→family consistency, duplicates, basic type/scaling sanity.

Usage:
  python tools/feature_csv_linter.py --d1 sync/ifns/indicator_feature_schema_v1_with_family.csv \
                                     --h1 sync/ifns/indicator_feature_schema_h1_v1_with_family.csv \
                                     --out sync/ifns/lint_report.csv
"""
import argparse, pandas as pd, re, sys, json

TAG_MAP = {
    "momentum":"MOMENTUM",
    "trend":"TREND",
    "volatility":"VOLATILITY",
    "volume":"VOLUME",
    "mean_reversion":"MEAN_REVERSION",
    "mr":"MEAN_REVERSION",
    "breakout":"BREAKOUT",
    "composite":"COMPOSITE",
    "context":"CONTEXT",
}

def family_from_tags(tags: str):
    if not isinstance(tags, str): return ""
    parts = [t.strip().lower() for t in re.split(r"[|, ]+", tags) if t.strip()]
    for k, v in TAG_MAP.items():
        if k in parts: return v
    low = " ".join(parts)
    for k, v in TAG_MAP.items():
        if k in low: return v
    return ""

def infer_family_from_id(fid: str):
    u = fid.upper()
    if u.startswith("FEAT.CTX."): return "CONTEXT"
    if "COMPOSITE" in u or "MR_REGIME_AWARE" in u or "BREAKOUT_CONFIRMATION" in u: return "COMPOSITE"
    if "BREAKOUT" in u or "DONCH" in u: return "BREAKOUT"
    if "RSI" in u or "STOCHK" in u or "CCI" in u: return "MEAN_REVERSION"
    if "ATR" in u or "REALVOL" in u or ("VOL" in u and "VOLUME" not in u): return "VOLATILITY"
    if "VOLUME" in u: return "VOLUME"
    if "BOLL" in u or "PL" in u or "TREND" in u or "STRUCT" in u: return "TREND"
    if "RET_" in u or "MACD" in u or "EMA" in u or "SMA" in u or "MOM" in u: return "MOMENTUM"
    return "OTHER"

def lint(df, name):
    issues = []
    required = ["feature_id","level","dtype","horizon","frequency"]
    for r in required:
        if r not in df.columns:
            issues.append({"severity":"ERROR","file":name,"feature_id":"","code":"MISSING_COL","message":f"Missing column {r}"})
    seen = set()
    for _, row in df.iterrows():
        fid = str(row.get("feature_id","")).strip()
        if not fid:
            issues.append({"severity":"ERROR","file":name,"feature_id":"","code":"EMPTY_ID","message":"Empty feature_id"})
            continue
        if fid in seen:
            issues.append({"severity":"WARN","file":name,"feature_id":fid,"code":"DUPLICATE_ID","message":"Duplicate ID within file"})
        seen.add(fid)
        fam = str(row.get("family","")).strip()
        tags = str(row.get("tags",""))
        tagfam = family_from_tags(tags)
        idfam = infer_family_from_id(fid)
        if fam == "" and tagfam:
            issues.append({"severity":"WARN","file":name,"feature_id":fid,"code":"FAMILY_EMPTY","message":f"family empty, derived from tags -> {tagfam}"})
        if fam and tagfam and fam != tagfam:
            issues.append({"severity":"WARN","file":name,"feature_id":fid,"code":"TAG_FAMILY_CONFLICT","message":f"family={fam}, tags imply {tagfam}"})
        scaling = str(row.get("scaling","")).lower()
        if "RSI" in fid.upper() or "STOCHK" in fid.upper():
            if scaling not in ("minmax",""):
                issues.append({"severity":"WARN","file":name,"feature_id":fid,"code":"SCALING_EXPECT_MINMAX","message":f"{fid} usually minmax-scaled; found {scaling}"})
        ftype = str(row.get("type","")).lower()
        dtype = str(row.get("dtype","")).lower()
        if ftype in ("numeric","") and dtype in ("string","object"):
            issues.append({"severity":"WARN","file":name,"feature_id":fid,"code":"DTYPE_SUSPECT","message":f"numeric feature with dtype {dtype}"})
    return issues

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--d1", required=True)
    ap.add_argument("--h1", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    df_d1 = pd.read_csv(args.d1)
    df_h1 = pd.read_csv(args.h1)

    issues = lint(df_d1, "schema_D1_with_family") + lint(df_h1, "schema_H1_with_family")
    out_df = pd.DataFrame(issues)
    out_df.to_csv(args.out, index=False)
    print(f"Wrote {len(out_df)} lints → {args.out}")

if __name__ == "__main__":
    main()
