#!/usr/bin/env python3
"""
indicative_arv.py - ARV when the strict rule cannot fire (n < 3 in-band).

comp.py REFUSES to price below MIN_COMPS and that refusal is correct: a
two-comp ARV is a guess wearing a number. But "UNPRICED" is not useful when
the user has verified comps and wants a working figure to check.

So this script produces an INDICATIVE ARV under the same method and the same
arithmetic, with the shortfall printed every time:

    ARV        = subject_sqft x MEDIAN $/sqft of renovated, in-band comps
    BUYER MAX  = (ARV x 0.70) - repairs
    SELLER MAO = BUYER MAX - $10,000 fee

It NEVER reports n >= MIN_COMPS as indicative, and it never widens the sqft
band to reach a count. An indicative ARV is labelled INDICATIVE and carries
its own n. Anything built on it must be re-run through comp.py once a third
in-band sale exists.

Usage:
    python3 scripts/indicative_arv.py --comps f.csv \
        --subject '{"address":"...","beds":3,"sqft":1430,"hood":"...","lat":..,"lon":..}' \
        --repairs 67000
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import statistics
import sys
from datetime import date, timedelta

BAND = 0.30
WINDOW_DAYS = 180
MIN_COMPS = 3
BUYER_PCT = 0.70
FEE = 10_000


def miles(la1, lo1, la2, lo2):
    r = 3958.8
    la1, lo1, la2, lo2 = map(math.radians, (la1, lo1, la2, lo2))
    a = math.sin((la2 - la1) / 2) ** 2 + math.cos(la1) * math.cos(la2) * math.sin((lo2 - lo1) / 2) ** 2
    return r * 2 * math.asin(math.sqrt(a))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--comps", required=True)
    ap.add_argument("--subject", required=True)
    ap.add_argument("--repairs", type=int, required=True)
    ap.add_argument("--as-of", default=None)
    ap.add_argument("--window-days", type=int, default=WINDOW_DAYS,
                    help="extend past the 180d rule ONLY to expose a near-miss; "
                         "the shortfall is always printed")
    a = ap.parse_args()

    s = json.loads(a.subject)
    as_of = date.fromisoformat(a.as_of) if a.as_of else date.today()
    cutoff = as_of - timedelta(days=a.window_days)
    sqft = float(s["sqft"])
    lo, hi = sqft * (1 - BAND), sqft * (1 + BAND)

    rows, excluded = [], []
    for r in csv.DictReader(open(a.comps)):
        addr = r["address"]
        try:
            sold = date.fromisoformat(r["sold"].strip())
            price, csq = float(r["price"]), float(r["sqft"])
            lat, lon = float(r["lat"]), float(r["lon"])
            beds = int(float(r["beds"]))
        except (ValueError, KeyError):
            excluded.append((addr, "unparseable row"))
            continue
        cond = (r.get("condition") or "").strip().lower()
        if r.get("exclusion"):
            excluded.append((addr, f"exclusion tag {r['exclusion']}"))
        elif sold < cutoff:
            excluded.append((addr, f"sold {sold} outside {a.window_days}d window"))
        elif cond != "renovated":
            excluded.append((addr, f"condition {cond or 'unknown'}"))
        elif beds < int(s["beds"]):
            excluded.append((addr, f"{beds} beds < subject {s['beds']}"))
        elif not (lo <= csq <= hi):
            excluded.append((addr, f"{csq:.0f} sqft outside {lo:.0f}-{hi:.0f} band"))
        else:
            rows.append((addr, sold, price, csq, price / csq, miles(s["lat"], s["lon"], lat, lon)))

    print(f"SUBJECT  {s['address']}  {s['beds']} bd  {sqft:,.0f} sf  {s['hood']}")
    print(f"BAND     {lo:,.0f}-{hi:,.0f} sqft   WINDOW {cutoff} to {as_of}"
          f"   ({a.window_days}d{'' if a.window_days==WINDOW_DAYS else ' - EXTENDED, NOT THE RULE'})\n")

    if not rows:
        print("INDICATIVE ARV: NONE - no renovated in-band sale at all.")
        for ad, why in excluded:
            print(f"  dropped  {ad:26} {why}")
        return 3

    rows.sort(key=lambda t: t[4])
    ppsf = [r[4] for r in rows]
    med = statistics.median(ppsf)
    arv = round(sqft * med)
    ceiling = arv * BUYER_PCT - a.repairs
    mao = ceiling - FEE
    spread = (max(ppsf) - min(ppsf)) / med * 100

    print(f"{'COMP':28} {'SOLD':11} {'PRICE':>9} {'SQFT':>6} {'$/SF':>8} {'MI':>5}")
    for ad, sold, price, csq, p, mi in rows:
        print(f"{ad:28} {sold} ${price:>8,.0f} {csq:>6,.0f} ${p:>7,.2f} {mi:>5.2f}")

    if excluded:
        print("\nEXCLUDED")
        for ad, why in excluded:
            print(f"  {ad:28} {why}")

    n = len(rows)
    conf = "INDICATIVE - BELOW THE 3-COMP RULE" if n < MIN_COMPS else "meets n>=3, use comp.py"
    print(f"\nMEDIAN   ${med:,.2f}/sf   n={n}   spread {spread:.1f}%")
    print(f"ARV      ${arv:,}   <-- {conf}")
    print(f"BUYER MAX (ARV x 0.70 - repairs ${a.repairs:,})  ${ceiling:,.0f}")
    print(f"SELLER MAO (less ${FEE:,} fee)                ${mao:,.0f}")
    print("\nINDICATIVE - not an appraisal, not an offer. Re-run through comp.py when n>=3.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
