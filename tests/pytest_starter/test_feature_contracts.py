# tests/pytest_starter/test_feature_contracts.py
# Minimal, tool-agnostic pytest scaffolds that check fixtures & assertions.
# Usage:
#   pip install pytest pandas python-dateutil
#   pytest -q tests/pytest_starter

import json, os, pandas as pd
from datetime import datetime
from dateutil import parser as dtparser

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
SYNC = os.path.join(ROOT, "sync", "ifns")
FIX = os.path.join(ROOT, "tests", "fixtures")

def load_assertions():
    with open(os.path.join(SYNC, "test_assertions_manifest.json"), "r", encoding="utf-8") as f:
        return json.load(f)

def load_calendar():
    with open(os.path.join(SYNC, "calendar_gaps_2025.json"), "r", encoding="utf-8") as f:
        return json.load(f)

def in_range(x, lo, hi, tol=0.0):
    return (x >= lo - tol) & (x <= hi + tol)

def test_fixtures_exist():
    asrt = load_assertions()
    for fname in asrt["fixtures"].keys():
        path = os.path.join(FIX, fname)
        assert os.path.exists(path), f"Missing fixture: {path}"

def test_RSI14_D1_minmax_and_bounds():
    asrt = load_assertions()
    cfg = asrt["fixtures"]["test_RSI14_D1_fixture.csv"]["expect"]
    df = pd.read_csv(os.path.join(FIX, "test_RSI14_D1_fixture.csv"))
    lo, hi = cfg["post_scale_range"]
    assert (df["rsi14_minmax"].between(lo, hi)).all(), "RSI14 post-scale out of [0,1]"
    # No clipping expected
    assert cfg.get("no_clip", False), "no_clip flag should be True in assertions"

def test_BOLL_Z20x2_D1_softclip():
    asrt = load_assertions()
    cfg = asrt["fixtures"]["test_BOLL_Z20x2_D1_fixture.csv"]["expect"]
    df = pd.read_csv(os.path.join(FIX, "test_BOLL_Z20x2_D1_fixture.csv"))
    lo, hi = cfg["z_soft_clip"]
    # Emulate soft-clip
    clipped = df["boll_z20x2"].clip(lower=lo, upper=hi)
    # Ensure at least one clipping occurred if expected
    if cfg.get("clip_events_expected", False):
        assert (clipped.ne(df["boll_z20x2"])).any(), "Expected some values to be soft-clipped"

def test_ATR14_PCT_non_negative():
    df = pd.read_csv(os.path.join(FIX, "test_ATR14_PCT_D1_fixture.csv"))
    assert (df["atr14_pct"] >= 0).all(), "ATR % should be non-negative"

def test_RET_1H_calendar_gaps():
    asrt = load_assertions()
    cal = load_calendar()
    closed_days = set(cal["closed"])
    early_close_day = asrt["fixtures"]["test_RET_1H_H1_fixture.csv"]["expect"]["calendar_respects_early_close"]
    df = pd.read_csv(os.path.join(FIX, "test_RET_1H_H1_fixture.csv"))
    # No bars on closed days
    dates = set([d.split(" ")[0] for d in df["timestamp"].astype(str).tolist()])
    assert closed_days.isdisjoint(dates), "Found bars on closed days"
    # Ensure all timestamps on early-close day are before 13:00 local
    early = [t for t in df["timestamp"].astype(str).tolist() if t.startswith(early_close_day)]
    if early:
        hhmm = [dtparser.parse(t).time().strftime("%H:%M") for t in early]
        assert all(h < "13:00" for h in hhmm), "Found bar at/after early close"

def test_CTX_cardinality():
    asrt = load_assertions()
    cfg = asrt["fixtures"]["test_CTX_PRICE_LOCATION_BIN_H1_fixture.csv"]["expect"]
    df = pd.read_csv(os.path.join(FIX, "test_CTX_PRICE_LOCATION_BIN_H1_fixture.csv"))
    # Cardinality check
    card = df["price_location_bin"].nunique()
    assert card >= cfg["min_cardinality_ge"], f"CTX cardinality {card} < {cfg['min_cardinality_ge']}"
    # Dominance check
    max_pct = df["price_location_bin"].value_counts(normalize=True).max()
    assert max_pct <= cfg["max_single_class_pct_le"], f"CTX dominance {max_pct:.2f} > {cfg['max_single_class_pct_le']:.2f}"
