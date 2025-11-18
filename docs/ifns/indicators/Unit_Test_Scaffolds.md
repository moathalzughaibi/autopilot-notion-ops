# Unit Test Scaffolds — How to Use
Date: 2025-11-18

## Files
- **Fixtures (CSV):** `tests/fixtures/*.csv`
- **Assertions:** `sync/ifns/test_assertions_manifest.json`
- **Calendar:** `sync/ifns/calendar_gaps_2025.json`

## Suggested Checks
1. **Scaling & Bounds**
   - RSI14 (D1): raw in [0,100] → minmax → [0,1]; assert no clipping.
   - BOLL_Z20x2 (D1): z-soft-clip at ±6; assert values beyond are capped and event logged.
   - ATR14_PCT (D1): raw non-negative; assert min ≥ 0.

2. **Calendar Gaps**
   - RET_1H (H1): assert no bars after 13:00 on `2025-11-28` and no bars on `2025-11-27`.

3. **Categoricals**
   - PRICE_LOCATION_BIN (H1): cardinality ≥ 3; max_single_class_pct ≤ 0.9.

Wire these into your existing CI to read the fixtures, compute features with your pipeline, then compare to the **assertions**.
