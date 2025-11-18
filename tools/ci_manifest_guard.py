#!/usr/bin/env python3
"""
CI Guard — enforce manifest change policy.

Policies (default deny):
  - added/removed columns: blocked unless --allow-added/--allow-removed
  - reordered columns: blocked unless --allow-reordered
  - per_feature_qc modifications: blocked unless --allow-modified
  - family changes: blocked unless --allow-family-changes
Exits 0 if allowed; otherwise prints a summary and exits 2.
"""

import argparse, json, sys
from manifest_diff import diff_manifests, load

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--baseline", required=True, help="Known-good manifest (JSON)")
    ap.add_argument("--candidate", required=True, help="Proposed manifest (JSON)")
    ap.add_argument("--allow-added", action="store_true")
    ap.add_argument("--allow-removed", action="store_true")
    ap.add_argument("--allow-reordered", action="store_true")
    ap.add_argument("--allow-modified", action="store_true")
    ap.add_argument("--allow-family-changes", action="store_true")
    ap.add_argument("--out", default="", help="Optional JSON report path")
    args = ap.parse_args()

    A = load(args.baseline); B = load(args.candidate)
    diff = diff_manifests(A, B)

    violations = []
    if diff["added"] and not args.allow_added:
        violations.append(f"Added features not allowed: {len(diff['added'])}")
    if diff["removed"] and not args.allow_removed:
        violations.append(f"Removed features not allowed: {len(diff['removed'])}")
    if diff["reordered"] and not args.allow_reordered:
        violations.append(f"Reordered features not allowed: {len(diff['reordered'])}")

    # per_feature_qc: specifically flag family changes unless allowed
    fam_changes = [m for m in diff["modified"] if "family" in m.get("changes", {})]
    other_mods = [m for m in diff["modified"] if "family" not in m.get("changes", {})]
    if fam_changes and not args.allow_family_changes:
        violations.append(f"Family changes not allowed: {len(fam_changes)}")
    if other_mods and not args.allow_modified:
        violations.append(f"QC modifications not allowed: {len(other_mods)}")

    report = {"diff": diff, "violations": violations}
    if args.out:
        with open(args.out, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2)

    if violations:
        print("CI GUARD — BLOCKED")
        for v in violations: print(" -", v)
        print("(Pass flags to allow specific classes of change)")
        sys.exit(2)
    else:
        print("CI GUARD — OK")
        sys.exit(0)

if __name__ == "__main__":
    main()
