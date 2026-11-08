#!/usr/bin/env python3
"""
comps.py - the five-comp standard, executable. Standard library only.

Enforces the rule the report is graded on:
    >= 5 credible sold comps, same ZIP first, radius expanded only with a stated
    reason, sold within 6 months, active listings never counted.
    < 5 comps -> ARV INSUFFICIENTLY SUPPORTED. No number is produced.

The ARV arithmetic itself lives in the wholesale-realestate repo (comping/comp.py:
sqft x median $/sqft, neighbourhood gate, radius ladder). This script is the
gate that decides whether that arithmetic is allowed to run at all.

Usage:
    python3 scripts/comps.py --csv comps.csv --as-of 2026-11-08 --zip 44302
    python3 scripts/comps.py --selftest
"""

from __future__ import annotations

import argparse
import csv
import sys
from datetime import date, timedelta

MIN_COMPS = 5
WINDOW_DAYS = 183
HIGH_CONFIDENCE = 6
MAX_BASE_MILES = 1.0
MAX_WIDE_MILES = 2.0

STATUS_OK = "SUPPORTED"
STATUS_SHORT = "ARV INSUFFICIENTLY SUPPORTED"


def load(path: str) -> list[dict]:
    with open(path, newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def evaluate(comps: list[dict], subject_zip: str, as_of: date,
             radius: float | None = None, window_days: int = WINDOW_DAYS) -> dict:
    cutoff = as_of - timedelta(days=window_days)
    drops = {"not_sold": 0, "stale": 0, "no_price_or_sqft": 0, "outside_radius": 0,
             "excluded": 0}
    usable, excluded = [], []

    for c in comps:
        status = (c.get("status") or "sold").strip().lower()
        if status != "sold":
            drops["not_sold"] += 1
            continue
        try:
            sold = date.fromisoformat((c.get("sold") or "").strip())
            price = float(c.get("price") or 0)
            sqft = float(c.get("sqft") or 0)
        except ValueError:
            drops["no_price_or_sqft"] += 1
            continue
        if price <= 0 or sqft <= 0:
            drops["no_price_or_sqft"] += 1
            continue
        if sold < cutoff:
            drops["stale"] += 1
            continue
        if (c.get("exclusion") or "").strip():
            drops["excluded"] += 1
            excluded.append(c)
            continue
        if radius is not None:
            try:
                d = float(c.get("miles") or 0)
            except ValueError:
                d = 0.0
            if d > radius:
                drops["outside_radius"] += 1
                continue
        usable.append({**c, "_sold": sold, "_price": price, "_sqft": sqft})

    same_zip = [c for c in usable
                if (c.get("zip") or "").strip() == str(subject_zip).strip()]
    other_zip = [c for c in usable if c not in same_zip]

    if len(usable) < MIN_COMPS:
        return {
            "status": STATUS_SHORT,
            "n": len(usable),
            "same_zip_n": len(same_zip),
            "drops": drops,
            "excluded": excluded,
            "note": (f"{len(usable)} credible comp(s) inside the window; "
                     f"{MIN_COMPS} required. No ARV. Do not force weak comps and "
                     f"do not borrow another submarket."),
        }

    confidence = "HIGH" if len(usable) >= HIGH_CONFIDENCE and len(same_zip) >= 3 \
                 else "MEDIUM" if len(same_zip) >= 3 else "LOW"
    radius_expanded = len(same_zip) < MIN_COMPS
    return {
        "status": STATUS_OK,
        "n": len(usable),
        "same_zip_n": len(same_zip),
        "other_zip_n": len(other_zip),
        "drops": drops,
        "excluded": excluded,
        "confidence": confidence,
        "radius_expanded": radius_expanded,
        "expansion_note": (
            f"only {len(same_zip)} comp(s) in {subject_zip}; {len(other_zip)} pulled "
            f"from adjacent ZIPs - state this in the report and compare $/sqft"
            if radius_expanded else "no expansion needed"),
        "ppsf_median": round(sorted(c["_price"] / c["_sqft"] for c in usable)[
            len(usable) // 2], 2),
        "comps": usable,
    }


def selftest() -> int:
    """The five-comp rule must reject a 4-comp set and accept a 5-comp set."""
    fails = 0
    print("COMPS SELFTEST - five-comp standard\n")
    as_of = date(2026, 11, 8)

    def mk(n, day_offset=10, zip5="44302", price=100000, sqft=1400, status="sold",
           exclusion="", miles=0.4):
        return [{"address": f"{100+i} Test St",
                 "sold": str(date(2026, 10, 1) - timedelta(days=day_offset + i)),
                 "price": price + i * 1000, "sqft": sqft, "zip": zip5,
                 "miles": miles, "status": status, "exclusion": exclusion}
                for i in range(n)]

    r = evaluate(mk(5), "44302", as_of)
    ok = r["status"] == STATUS_OK and r["n"] == 5
    print(f"  {'PASS' if ok else 'FAIL'}  five clean comps -> {r['status']} (n={r['n']})")
    fails += 0 if ok else 1

    r = evaluate(mk(4), "44302", as_of)
    ok = r["status"] == STATUS_SHORT
    print(f"  {'PASS' if ok else 'FAIL'}  four comps -> {r['status']} (no ARV produced)")
    fails += 0 if ok else 1

    r = evaluate(mk(7, status="active"), "44302", as_of)
    ok = r["status"] == STATUS_SHORT and r["drops"]["not_sold"] == 7
    print(f"  {'PASS' if ok else 'FAIL'}  active listings never count -> {r['status']}")
    fails += 0 if ok else 1

    r = evaluate(mk(6, day_offset=400), "44302", as_of)
    ok = r["status"] == STATUS_SHORT and r["drops"]["stale"] == 6
    print(f"  {'PASS' if ok else 'FAIL'}  stale sales never count -> {r['status']}")
    fails += 0 if ok else 1

    r = evaluate(mk(6, exclusion="deed_restricted"), "44302", as_of)
    ok = r["status"] == STATUS_SHORT
    print(f"  {'PASS' if ok else 'FAIL'}  AMI-restricted sales excluded -> {r['status']}")
    fails += 0 if ok else 1

    r = evaluate([], "44302", as_of)
    ok = r["status"] == STATUS_SHORT
    print(f"  {'PASS' if ok else 'FAIL'}  empty set -> {r['status']}")
    fails += 0 if ok else 1

    # 4 in-ZIP + 1 adjacent = 5 usable: supported, but expansion must be flagged
    r = evaluate(mk(4) + mk(2, zip5="44303"), "44302", as_of)
    ok = r["status"] == STATUS_OK and r["same_zip_n"] == 4 and r["radius_expanded"]
    print(f"  {'PASS' if ok else 'FAIL'}  4 same-ZIP + 2 adjacent -> {r['status']}, "
          f"expansion flagged ({r['same_zip_n']} same-ZIP)")
    fails += 0 if ok else 1

    # 3 in-ZIP + 1 adjacent = 4 usable: still short, expansion must NOT rescue it
    r = evaluate(mk(3) + mk(1, zip5="44303"), "44302", as_of)
    ok = r["status"] == STATUS_SHORT
    print(f"  {'PASS' if ok else 'FAIL'}  3 same-ZIP + 1 adjacent (4 total) -> "
          f"{r['status']} - expansion does not fix a count")
    fails += 0 if ok else 1

    print("\n" + ("PASS  five-comp rule enforced" if fails == 0
                  else "FAIL  comp gate is wrong"))
    return 0 if fails == 0 else 1


def main(argv=None) -> int:
    p = argparse.ArgumentParser(description="five-comp gate")
    p.add_argument("--csv")
    p.add_argument("--zip", dest="zip5", default="")
    p.add_argument("--as-of", default=str(date.today()))
    p.add_argument("--radius", type=float)
    p.add_argument("--selftest", action="store_true")
    a = p.parse_args(argv)
    if a.selftest:
        return selftest()
    if not a.csv:
        p.print_help()
        return 0
    r = evaluate(load(a.csv), a.zip5, date.fromisoformat(a.as_of), a.radius)
    print(f"{r['status']}  n={r['n']}  same-ZIP={r['same_zip_n']}")
    print(f"  drops: {r['drops']}")
    if r.get("note"):
        print(f"  {r['note']}")
    if r["status"] == STATUS_OK:
        print(f"  confidence {r['confidence']}  median ${r['ppsf_median']}/sqft")
        print(f"  {r['expansion_note']}")
    return 0 if r["status"] == STATUS_OK else 3


if __name__ == "__main__":
    sys.exit(main())
