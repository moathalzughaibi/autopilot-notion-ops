#!/usr/bin/env python3
"""
IFNS Manifest Diff — compare two training manifests.
Reports: column order changes, added/removed features, per_feature_qc deltas (thresholds, dtype, family, clip_policy).
Usage:
  python tools/manifest_diff.py --a sync/ifns/training_manifest_D1_v1_1.json --b sync/ifns/training_manifest_D1_v1_1.json
"""
import json, argparse, sys

def load(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def list_to_index_map(lst):
    return {k:i for i,k in enumerate(lst)}

def diff_manifests(a, b):
    out = {"summary":{}, "added":[], "removed":[], "reordered":[], "modified":[], "meta_changes":{}}

    # Top-level changes
    for k in ["view","horizon","frequency","alignment"]:
        if a.get(k) != b.get(k):
            out["meta_changes"][k] = {"a": a.get(k), "b": b.get(k)}

    # Columns: added/removed/order
    col_a = a.get("columns", [])
    col_b = b.get("columns", [])
    set_a, set_b = set(col_a), set(col_b)
    out["added"] = sorted(list(set_b - set_a))
    out["removed"] = sorted(list(set_a - set_b))

    idx_a = list_to_index_map(col_a)
    idx_b = list_to_index_map(col_b)
    common = [c for c in col_a if c in set_b]
    for c in common:
        if idx_a[c] != idx_b[c]:
            out["reordered"].append({"feature_id": c, "from": idx_a[c], "to": idx_b[c]})

    # per_feature_qc diffs
    qa, qb = a.get("per_feature_qc", {}), b.get("per_feature_qc", {})
    shared = set(qa.keys()).intersection(qb.keys())
    keys_to_check = ["level","dtype","family","tags","horizon","frequency","thresholds","values","value_exceptions","clip_policy"]
    for fid in sorted(shared):
        da, db = qa[fid], qb[fid]
        changes = {}
        for k in keys_to_check:
            if da.get(k) != db.get(k):
                changes[k] = {"a": da.get(k), "b": db.get(k)}
        if changes:
            out["modified"].append({"feature_id": fid, "changes": changes})

    out["summary"] = {
        "added_count": len(out["added"]),
        "removed_count": len(out["removed"]),
        "reordered_count": len(out["reordered"]),
        "modified_count": len(out["modified"]),
        "meta_changes_count": len(out["meta_changes"])
    }
    return out

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--a", required=True, help="Path to baseline manifest JSON")
    ap.add_argument("--b", required=True, help="Path to candidate manifest JSON")
    ap.add_argument("--out", required=False, help="Optional path to write JSON diff")
    args = ap.parse_args()

    A = load(args.a); B = load(args.b)
    diff = diff_manifests(A, B)
    if args.out:
        with open(args.out, "w", encoding="utf-8") as f:
            json.dump(diff, f, indent=2)
    else:
        print(json.dumps(diff, indent=2))

if __name__ == "__main__":
    main()
