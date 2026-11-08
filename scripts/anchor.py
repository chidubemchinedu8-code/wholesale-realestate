#!/usr/bin/env python3
"""
anchor.py - the ZIP / neighbourhood median anchor (COMPING.md step 4).

A sanity check on the ARV, not a substitute for comps. Pulls the median sale
price and median $/sqft for a ZIP or named neighbourhood over the most recent
~3 months, and detects a bimodal distribution (mansions blended with distress
sales) so you know to drop to a named-neighbourhood median instead.

Input is a CSV of sales you actually pulled - this script does no fetching and
will not invent a median. If the CSV is empty, it says UNKNOWN.

Usage:
    python3 scripts/anchor.py --csv sales_44302.csv --label "44302"
    python3 scripts/anchor.py --selftest
"""

from __future__ import annotations

import argparse
import csv
import sys
from datetime import date, timedelta

BIMODAL_GAP = 0.60          # a >60% gap between the two clusters is bimodal
MIN_SALES = 5
MIN_CLUSTER = 3             # each side of a gap needs this many sales to be a market
MIN_SALES_BIMODAL = 8


def median(v: list[float]) -> float:
    v = sorted(v)
    n = len(v)
    if not n:
        raise ValueError("median of empty list")
    mid = n // 2
    return float(v[mid]) if n % 2 else (v[mid - 1] + v[mid]) / 2.0


def split_clusters(ppsf: list[float]) -> tuple[list[float], list[float]] | None:
    """Find the largest relative gap between consecutive sorted values."""
    v = sorted(ppsf)
    if len(v) < MIN_SALES_BIMODAL:
        return None
    best_i, best_rel = None, 0.0
    for i in range(1, len(v)):
        rel = (v[i] - v[i - 1]) / v[i - 1]
        if rel > best_rel:
            best_i, best_rel = i, rel
    if best_i is None or best_rel < BIMODAL_GAP:
        return None
    # A cluster of one is an OUTLIER, not a market. A single $11/sf junk sale
    # next to a $89/sf field produced the largest relative gap in 45410 and got
    # reported as "bimodal - drop the ZIP median", destroying a usable anchor.
    # Both sides must clear MIN_SALES before we call it two markets.
    if best_i < MIN_CLUSTER or (len(v) - best_i) < MIN_CLUSTER:
        return None
    return v[:best_i], v[best_i:]


def analyse(rows: list[dict], label: str, as_of: date,
            months: int = 3) -> dict:
    cutoff = as_of - timedelta(days=int(months * 30.44))
    used, dropped = [], {"stale": 0, "no_price_or_sqft": 0}
    for r in rows:
        try:
            sold = date.fromisoformat((r.get("sold") or "").strip())
            price = float(r.get("price") or 0)
            sqft = float(r.get("sqft") or 0)
        except ValueError:
            dropped["no_price_or_sqft"] += 1
            continue
        if price <= 0 or sqft <= 0:
            dropped["no_price_or_sqft"] += 1
            continue
        if sold < cutoff:
            dropped["stale"] += 1
            continue
        used.append((price, sqft, price / sqft))

    out = {"label": label, "window_months": months, "n": len(used),
           "dropped": dropped, "status": "OK"}
    if len(used) < MIN_SALES:
        out["status"] = "UNKNOWN"
        out["note"] = (f"only {len(used)} sale(s) in {months} months; a median needs "
                       f"at least {MIN_SALES}. Do not quote an anchor - log it UNKNOWN.")
        return out

    ppsf = [u[2] for u in used]
    out["median_price"] = int(round(median([u[0] for u in used])))
    out["median_ppsf"] = round(median(ppsf), 2)
    out["spread_ppsf"] = (round(min(ppsf), 2), round(max(ppsf), 2))

    clusters = split_clusters(ppsf)
    if clusters:
        lo, hi = clusters
        out["bimodal"] = True
        out["clusters"] = {
            "low": {"n": len(lo), "median_ppsf": round(median(lo), 2)},
            "high": {"n": len(hi), "median_ppsf": round(median(hi), 2)},
        }
        out["advice"] = ("BIMODAL - the ZIP blends two markets. Drop to a named-"
                         "neighbourhood or plat-level median and say why. A single "
                         "ZIP median is not usable here.")
    elif len(used) < MIN_SALES_BIMODAL:
        out["bimodal"] = False
        out["bimodal_tested"] = False
        out["advice"] = (f"NOT TESTED - {len(used)} sale(s) is below the "
                         f"{MIN_SALES_BIMODAL} needed to test for bimodality. The "
                         f"median is arithmetically valid but the shape is unknown, "
                         f"so do not call this a single distribution.")
    else:
        out["bimodal"] = False
        out["bimodal_tested"] = True
        out["advice"] = "single distribution - the ZIP median is a usable sanity check"
    return out


def selftest() -> int:
    fails = 0
    print("ANCHOR SELFTEST\n")
    as_of = date(2026, 11, 8)

    def mk(vals, days=10):
        return [{"sold": str(as_of - timedelta(days=days + i)),
                 "price": str(int(p * s)), "sqft": str(s)}
                for i, (p, s) in enumerate(vals)]

    # A single junk sale must not be called a second market. 45410's $-11.46/sf
    # row (4,798 sf, $55,000) was the largest gap in the file and flipped the
    # whole ZIP to "bimodal", which would have thrown away a usable anchor.
    outlier = mk([(78, 1400), (80, 1450), (82, 1350), (76, 1500), (84, 1420),
                  (79, 1380), (30, 1800)])
    r = analyse(outlier, "45410", as_of)
    ok = r["status"] == "OK" and not r["bimodal"]
    print(f"  {'PASS' if ok else 'FAIL'}  one junk sale -> outlier, NOT bimodal")
    fails += 0 if ok else 1

    # tight distribution
    tight = mk([(78, 1400), (80, 1450), (82, 1350), (76, 1500), (84, 1420), (79, 1380)])
    r = analyse(tight, "44302", as_of)
    ok = r["status"] == "OK" and not r["bimodal"]
    print(f"  {'PASS' if ok else 'FAIL'}  tight market -> not bimodal "
          f"(median ${r.get('median_ppsf')}/sf)")
    fails += 0 if ok else 1

    # bimodal: mansions blended with distress
    bimodal = mk([(180, 1500), (190, 1600), (200, 1550), (210, 1450),
                  (45, 1400), (48, 1500), (50, 1350), (52, 1450)])
    r = analyse(bimodal, "44302", as_of)
    ok = r["status"] == "OK" and r["bimodal"]
    print(f"  {'PASS' if ok else 'FAIL'}  mansion+distress blend -> BIMODAL flagged")
    fails += 0 if ok else 1
    if r.get("bimodal"):
        print(f"        low cluster ${r['clusters']['low']['median_ppsf']}/sf "
              f"(n={r['clusters']['low']['n']}) vs high "
              f"${r['clusters']['high']['median_ppsf']}/sf "
              f"(n={r['clusters']['high']['n']})")

    # too few sales -> UNKNOWN, no median invented
    r = analyse(mk([(80, 1400), (82, 1400)]), "44302", as_of)
    ok = r["status"] == "UNKNOWN" and "median_ppsf" not in r
    print(f"  {'PASS' if ok else 'FAIL'}  2 sales -> UNKNOWN, no median invented")
    fails += 0 if ok else 1

    # stale sales excluded
    old = mk([(80, 1400)] * 6, days=400)
    r = analyse(old, "44302", as_of)
    ok = r["status"] == "UNKNOWN" and r["dropped"]["stale"] == 6
    print(f"  {'PASS' if ok else 'FAIL'}  400-day-old sales excluded -> "
          f"{r['status']}")
    fails += 0 if ok else 1

    print("\n" + ("PASS  anchor behaves" if fails == 0 else "FAIL  anchor wrong"))
    return 0 if fails == 0 else 1


def main(argv=None) -> int:
    p = argparse.ArgumentParser(description="ZIP/neighbourhood median anchor")
    p.add_argument("--csv")
    p.add_argument("--label", default="")
    p.add_argument("--as-of", default=str(date.today()))
    p.add_argument("--months", type=float, default=3)
    p.add_argument("--selftest", action="store_true")
    a = p.parse_args(argv)

    if a.selftest:
        return selftest()
    if not a.csv:
        p.print_help()
        return 0

    with open(a.csv, newline="", encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))
    r = analyse(rows, a.label or a.csv, date.fromisoformat(a.as_of), a.months)
    print(f"ANCHOR {r['label']}  ({r['window_months']} months to {a.as_of})")
    print(f"  sales used {r['n']}   dropped {r['dropped']}")
    print(f"  status {r['status']}")
    if r["status"] != "OK":
        print(f"  {r['note']}")
        return 3
    print(f"  median price ${r['median_price']:,}   median ${r['median_ppsf']}/sf")
    print(f"  spread ${r['spread_ppsf'][0]}/sf - ${r['spread_ppsf'][1]}/sf")
    if r["bimodal"]:
        print(f"  BIMODAL: low cluster ${r['clusters']['low']['median_ppsf']}/sf "
              f"(n={r['clusters']['low']['n']}), high cluster "
              f"${r['clusters']['high']['median_ppsf']}/sf "
              f"(n={r['clusters']['high']['n']})")
    print(f"  {r['advice']}")
    print("\nA sanity check, never a substitute for comps. ESTIMATE.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
