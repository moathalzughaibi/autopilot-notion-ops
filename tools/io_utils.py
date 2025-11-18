# tools/io_utils.py
import os, glob, json, hashlib, pandas as pd

def sha256_of_file(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()

def read_table_glob(pattern: str, columns=None, ts_col="timestamp"):
    """Read CSV/Parquet files matching glob pattern into a DataFrame.
    Keeps only requested columns (plus timestamp if present)."""
    files = sorted(glob.glob(pattern))
    if not files:
        return pd.DataFrame(columns=(["timestamp"] if ts_col else []) + (columns or []))
    dfs = []
    for fp in files:
        if fp.lower().endswith(".csv"):
            df = pd.read_csv(fp)
        elif fp.lower().endswith(".parquet"):
            df = pd.read_parquet(fp)
        else:
            continue
        if ts_col and ts_col in df.columns:
            keep = [ts_col] + [c for c in (columns or []) if c in df.columns]
            df = df[keep]
            df[ts_col] = pd.to_datetime(df[ts_col])
        elif columns:
            df = df[[c for c in columns if c in df.columns]]
        dfs.append(df)
    if not dfs:
        return pd.DataFrame(columns=(["timestamp"] if ts_col else []) + (columns or []))
    out = pd.concat(dfs, ignore_index=True)
    return out

def read_ndjson_glob(pattern: str):
    """Read .ndjson/.jsonl lines into a pandas DataFrame."""
    files = sorted(glob.glob(pattern))
    rows = []
    for fp in files:
        if fp.lower().endswith(".ndjson") or fp.lower().endswith(".jsonl"):
            with open(fp, "r", encoding="utf-8") as f:
                for line in f:
                    line=line.strip()
                    if not line: continue
                    rows.append(json.loads(line))
        elif fp.lower().endswith(".json"):
            with open(fp, "r", encoding="utf-8") as f:
                obj = json.load(f)
                if isinstance(obj, list): rows.extend(obj)
                else: rows.append(obj)
    import pandas as pd
    if not rows:
        return pd.DataFrame()
    df = pd.DataFrame(rows)
    if "timestamp" in df.columns:
        df["timestamp"] = pd.to_datetime(df["timestamp"])
    return df

def ensure_columns(df: pd.DataFrame, required: list, ts_col="timestamp"):
    """Add any missing required columns with NaN."""
    import numpy as np
    for c in required:
        if c not in df.columns:
            df[c] = np.nan
    if ts_col and ts_col in df.columns:
        cols = [ts_col] + [c for c in df.columns if c != ts_col]
        df = df[cols]
    return df
