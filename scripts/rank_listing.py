#!/usr/bin/env python3
"""
rank_listing.py - on-market screening. Standard library only.

Implements the priorities and default rejections in references/on-market.md so a
listing cannot be waved through by prose.

    python3 scripts/rank_listing.py --dom 3 --redemptions 0 --ask 195000 \
        --zip-ppsf 128 --sqft 1600 --condition turnkey
    python3 scripts/rank_listing.py --selftest
"""

from __future__ import annotations

import argparse
import sys

# Weights from references/on-market.md. Research ordering only, not a valuation.
WEIGHTS = {
    "dom_60_plus": 20,
    "dom_30_59": 12,
    "reductions": 15,
    "back_on_market": 10,
    "as_is": 10,
    "dated_photos": 10,
    "deferred_maintenance": 10,
    "estate": 8,
    "below_zip_ppsf": 15,
    "absentee": 5,
}
MAX_SCORE = sum(WEIGHTS.values())  # 115

REJECT_CONDITIONS = {"turnkey", "fully_renovated", "retail_ready", "reo"}


def score(dom: int, reductions: int, back_on_market: False = False,
          as_is: False = False, dated: False = False,
          deferred: False = False, estate: False = False,
          absentee: False = False, ask: float | None = None,
          sqft: float | None = None,
          zip_ppsf_renovated: float | None = None) -> dict:
    s, reasons = 0, []

    if dom >= 60:
        s += WEIGHTS["dom_60_plus"]; reasons.append(f"+{WEIGHTS['dom_60_plus']} DOM {dom} (60+)")
    elif dom >= 30:
        s += WEIGHTS["dom_30_59"]; reasons.append(f"+{WEIGHTS['dom_30_59']} DOM {dom} (30-59)")

    if reductions:
        s += WEIGHTS["reductions"]
        reasons.append(f"+{WEIGHTS['reductions']} {reductions} price reduction(s)")

    flags = [
        (back_on_market, "back_on_market", "back on market"),
        (as_is, "as_is", "as-is"),
        (dated, "dated_photos", "dated interiors"),
        (deferred, "deferred_maintenance", "deferred maintenance"),
        (estate, "estate", "estate/inherited"),
        (absentee, "absentee", "absentee owner"),
    ]
    for present, key, label in flags:
        if present:
            s += WEIGHTS[key]
            reasons.append(f"+{WEIGHTS[key]} {label}")

    implied_ppsf = None
    discount = None
    if ask and sqft:
        implied_ppsf = ask / sqft
        if zip_ppsf_renovated:
            discount = (zip_ppsf_renovated - implied_ppsf) / zip_ppsf_renovated
            if implied_ppsf < zip_ppsf_renovated * 0.90:
                s += WEIGHTS["below_zip_ppsf"]
                reasons.append(f"+{WEIGHTS['below_zip_ppsf']} asking ${implied_ppsf:.0f}/sf "
                               f"vs ZIP renovated ${zip_ppsf_renovated:.0f}/sf "
                               f"({discount*100:.0f}% below)")

    return {"score": s, "max": MAX_SCORE, "reasons": reasons,
            "implied_ppsf": round(implied_ppsf, 2) if implied_ppsf else None,
            "discount_vs_zip": round(discount, 4) if discount is not None else None}


def screen(dom: int, condition: str = "", ask: float | None = None,
           sqft: float | None = None, zip_ppsf: float | None = None,
           reductions: int = 0, **flags) -> dict:
    """Full screen: rejections first, then score. Returns verdict + reason."""
    cond = (condition or "").strip().lower()
    result = {"dom": dom, "condition": cond or "unknown"}

    if cond in REJECT_CONDITIONS:
        return {**result, "verdict": "REJECT", "code": "turnkey_or_retail",
                "reason": f"condition '{cond}' - there is no wholesale spread in "
                          f"retail pricing"}

    # under 14 days: rejected unless documented mispricing
    documented_misprice = False
    if ask and sqft and zip_ppsf:
        implied = ask / sqft
        if implied < zip_ppsf * 0.65:
            documented_misprice = True
    if dom < 14 and not documented_misprice:
        return {**result, "verdict": "REJECT", "code": "under_14_days",
                "reason": f"{dom} days on market - new listings are rejected by "
                          f"default; no documented mispricing "
                          f"(needs asking < 65% of the ZIP's renovated $/sqft)"}

    scored = score(dom=dom, reductions=reductions, ask=ask, sqft=sqft,
                   zip_ppsf_renovated=zip_ppsf, **flags)
    if dom < 14 and documented_misprice:
        return {**result, **scored, "verdict": "PURSUE", "code": "under_14_days_exception",
                "reason": "under 14 days BUT documented mispricing "
                          "(asking < 65% of ZIP renovated $/sqft)"}

    if scored["score"] < 20:
        return {**result, **scored, "verdict": "DEPRIORITISE",
                "code": "weak_signal",
                "reason": f"score {scored['score']}/{MAX_SCORE} - no meaningful "
                          f"motivation signal"}

    return {**result, **scored, "verdict": "PURSUE", "code": "ok",
            "reason": f"score {scored['score']}/{MAX_SCORE}"}


def selftest() -> int:
    fails = 0
    print("LISTING SCREEN SELFTEST\n")

    def case(name, kw, expect_verdict, expect_code=None):
        nonlocal fails
        r = screen(**kw)
        ok = r["verdict"] == expect_verdict and (
            expect_code is None or r["code"] == expect_code)
        print(f"  {'PASS' if ok else 'FAIL'}  {name}")
        print(f"        -> {r['verdict']} ({r['code']}): {r['reason']}")
        if not ok:
            fails += 1

    # TEST 2: newly listed, fully renovated, retail-ready -> rejected
    case("new listing, fully renovated, retail price",
         dict(dom=3, condition="fully_renovated", ask=195000, sqft=1600,
              zip_ppsf=120), "REJECT", "turnkey_or_retail")

    case("new listing, turnkey",
         dict(dom=5, condition="turnkey", ask=180000, sqft=1500,
              zip_ppsf=120), "REJECT", "turnkey_or_retail")

    case("new listing, dated, but at full retail",
         dict(dom=4, condition="medium", ask=196000, sqft=1500,
              zip_ppsf=128, reductions=0), "REJECT", "under_14_days")

    # the only legitimate sub-14-day exception
    case("sub-14-day BUT 55% below ZIP renovated $/sf",
         dict(dom=6, condition="heavy", ask=75000, sqft=1500, zip_ppsf=128),
         "PURSUE", "under_14_days_exception")

    # TEST 3: stale + reductions + dated condition -> higher priority
    case("stale: 361 DOM, 2 reductions, as-is, dated, deferred, estate",
         dict(dom=361, condition="heavy", ask=95000, sqft=1642, zip_ppsf=78,
              reductions=2, as_is=True, dated=True, deferred=True,
              estate=True), "PURSUE", "ok")

    stale = screen(dom=361, condition="heavy", ask=95000, sqft=1642,
                   zip_ppsf=78, reductions=2, as_is=True, dated=True,
                   deferred=True, estate=True)["score"]
    # 16 days, not 8: sub-14-day listings are rejected before scoring, so the
    # like-for-like comparison has to be a listing that actually reaches scoring
    fresh = screen(dom=16, condition="medium", ask=95000, sqft=1642,
                   zip_ppsf=78)["score"]
    ok = stale > fresh
    print(f"  {'PASS' if ok else 'FAIL'}  stale ({stale}) outranks fresh ({fresh}) "
          f"on identical price/size")
    fails += 0 if ok else 1

    # 60+ DOM must beat 30-59 DOM
    a = score(dom=65, reductions=0)["score"]
    b = score(dom=35, reductions=0)["score"]
    ok = a > b
    print(f"  {'PASS' if ok else 'FAIL'}  65 DOM ({a}) outranks 35 DOM ({b})")
    fails += 0 if ok else 1

    # REO never enters normal results
    case("REO", dict(dom=90, condition="reo"), "REJECT", "turnkey_or_retail")

    print("\n" + ("PASS  listing screen behaves" if fails == 0
                  else "FAIL  listing screen wrong"))
    return 0 if fails == 0 else 1


def main(argv=None) -> int:
    p = argparse.ArgumentParser(description="on-market listing screen")
    p.add_argument("--dom", type=int)
    p.add_argument("--condition", default="")
    p.add_argument("--ask", type=float)
    p.add_argument("--sqft", type=float)
    p.add_argument("--zip-ppsf", type=float,
                   help="ZIP's renovated sold $/sqft")
    p.add_argument("--reductions", type=int, default=0)
    p.add_argument("--as-is", action="store_true")
    p.add_argument("--dated", action="store_true")
    p.add_argument("--deferred", action="store_true")
    p.add_argument("--estate", action="store_true")
    p.add_argument("--back-on-market", action="store_true")
    p.add_argument("--absentee", action="store_true")
    p.add_argument("--selftest", action="store_true")
    a = p.parse_args(argv)

    if a.selftest:
        return selftest()
    if a.dom is None:
        p.print_help()
        return 0
    r = screen(dom=a.dom, condition=a.condition, ask=a.ask, sqft=a.sqft,
               zip_ppsf=a.zip_ppsf, reductions=a.reductions, as_is=a.as_is,
               dated=a.dated, deferred=a.deferred, estate=a.estate,
               back_on_market=a.back_on_market, absentee=a.absentee)
    print(f"{r['verdict']} ({r['code']})  {r['reason']}")
    for line in r.get("reasons", []):
        print(f"  {line}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
