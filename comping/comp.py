#!/usr/bin/env python3
"""
comp.py - the comping + ARV engine. One rule, executable, standard library only.

The rule (see COMPING.md, section 2):

    ARV = subject_sqft x p75($/sqft of >=3 arm's-length closed sales, same
          neighbourhood, within 1.5 mi, inside the window, within +-30% sqft)
          x 0.88

    under 3 comps at 1.50 mi -> NO ARV. Do not widen, do not average.

Modes:
    python3 comping/comp.py --selftest
        offline: run the six checks on a synthetic fixture, then inject six
        targeted defects and require the targeted check to flip to FAIL.

    python3 comping/comp.py --comps comping/fixtures/akron_44302.csv \
        --subject '{"sqft": 1642, "hood": "44302", "lat": 41.0790, "lon": -81.5360, "style": "COLONIAL"}'
        price a subject off a comp CSV.

    python3 comping/comp.py --offer 350000 --repairs 34933
        the graded version of the economics model.

    python3 comping/comp.py --exclusions
        the exclusion rules, as a checklist.

Every number this prints is an ESTIMATE. It is not an appraisal and not an offer.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import sys
from dataclasses import dataclass, field
from datetime import date, timedelta

# ---------------------------------------------------------------------------
# Constants - from superpowers/leadgen/pull_leads.py. Do not tune per deal.
# ---------------------------------------------------------------------------

RADIUS_LADDER = (0.25, 0.50, 0.75, 1.00, 1.25, 1.50)
RADIUS_CAP = 1.50
MIN_COMPS = 3
HIGH_CONFIDENCE_COMPS = 6
SQFT_BAND = 0.30
HAIRCUT = 0.88
MIN_COMP_SQFT = 400
MIN_COMP_PRICE = 20_000
PPSF_MIN, PPSF_MAX = 20.0, 300.0

BUYER_PCT = 0.70
OFFER_LOW_PCT = 0.55
OFFER_HIGH_PCT = 0.60
WHOLE_FEE = 10_000
JV_SPLIT = 0.50

# Not comps. See COMPING.md section 3.
EXCLUSION_REASONS = {
    "deed_restricted": "Sale restricted (AMI / income-limited) - a FLOOR, not market value",
    "new_build": "Newer build - different product from the subject",
    "non_arms_length": "Non-arm's-length transfer (quitclaim / family / $1 deed)",
    "condo": "Condo - different product unless the subject is a condo",
    "not_sold": "Not a closed sale (active / pending / withdrawn)",
}

STATUS_PRICED = "PRELIMINARY - not an offer"
STATUS_NONE = "NO COMPS"


# ---------------------------------------------------------------------------
# Small maths helpers
# ---------------------------------------------------------------------------

def miles(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Equirectangular - accurate at neighbourhood scale, no library needed."""
    dlat = (lat2 - lat1) * 69.0
    dlon = (lon2 - lon1) * 69.0 * math.cos(math.radians((lat1 + lat2) / 2.0))
    return math.hypot(dlat, dlon)


def percentile(values: list[float], q: float) -> float:
    """Linear interpolation. q is 0..1."""
    v = sorted(values)
    if not v:
        raise ValueError("percentile of empty list")
    if len(v) == 1:
        return float(v[0])
    pos = (len(v) - 1) * q
    lo = int(pos)
    hi = min(lo + 1, len(v) - 1)
    return v[lo] + (v[hi] - v[lo]) * (pos - lo)


# ---------------------------------------------------------------------------
# Economics - one model, two percentages, fee deducted exactly once
# ---------------------------------------------------------------------------

def economics(arv: float, repairs: float = 0.0) -> dict:
    """70% is a CAP. 55-60% is a TARGET under the cap. The gap is the pay stack."""
    ceiling = int(round(BUYER_PCT * arv - repairs))
    offer_low = int(round(OFFER_LOW_PCT * arv - repairs))
    offer_high = int(round(OFFER_HIGH_PCT * arv - repairs))
    return {
        "ARV": int(round(arv)),
        "REPAIRS": int(round(repairs)),
        "CEILING (0.70 x ARV - repairs)": ceiling,
        "OFFER LOW (0.55)": offer_low,
        "OFFER HIGH (0.60)": offer_high,
        "FRICTION (ceiling - offer high)": ceiling - offer_high,
        "FRICTION % OF ARV": round((ceiling - offer_high) / arv * 100, 1) if arv else 0.0,
        "CONTRACT FOR $10K FEE": ceiling - WHOLE_FEE,
        "WHOLE FEE": WHOLE_FEE,
        "MY SIDE @50/50": int(WHOLE_FEE * JV_SPLIT),
    }


# ---------------------------------------------------------------------------
# The comp ladder
# ---------------------------------------------------------------------------

@dataclass
class Comp:
    address: str
    sold: date
    price: float
    sqft: float
    hood: str
    lat: float
    lon: float
    style: str = ""
    beds: str = ""
    exclusion: str = ""          # key from EXCLUSION_REASONS, or ""

    @property
    def ppsf(self) -> float:
        return self.price / self.sqft


@dataclass
class CompResult:
    status: str                                  # STATUS_PRICED | STATUS_NONE
    arv: int | None = None
    as_is: int | None = None
    basis: str = ""
    n: int = 0
    radius: float | None = None
    hood: str = ""
    confidence: str = STATUS_NONE
    chosen: list[Comp] = field(default_factory=list)
    excluded_in_radius: list[Comp] = field(default_factory=list)
    rejected: dict = field(default_factory=dict)  # universe screen drop counts
    note: str = ""


def screen_universe(comps: list[Comp], as_of: date, window_days: int) -> tuple[list[Comp], dict]:
    """Drop sales that are not usable comps at all, before any ladder runs."""
    cutoff = as_of - timedelta(days=window_days)
    kept, dropped = [], {"geometry": 0, "sqft_or_price": 0, "price_floor": 0,
                         "ppsf": 0, "window": 0, "not_sold": 0, "non_arms_length": 0}
    for c in comps:
        if c.exclusion in ("non_arms_length", "not_sold"):
            dropped[c.exclusion] += 1
            continue
        if c.lat is None or c.lon is None or c.lat == 0 or c.lon == 0:
            dropped["geometry"] += 1
            continue
        if not c.sqft or c.sqft < MIN_COMP_SQFT or not c.price:
            dropped["sqft_or_price"] += 1
            continue
        if c.price < MIN_COMP_PRICE:
            dropped["price_floor"] += 1
            continue
        if not (PPSF_MIN <= c.ppsf <= PPSF_MAX):
            dropped["ppsf"] += 1
            continue
        if c.sold < cutoff:
            dropped["window"] += 1
            continue
        kept.append(c)
    return kept, dropped


def compute_arv(subject_sqft: float, subject_hood: str, lat: float, lon: float,
                style: str, comps: list[Comp], as_of: date,
                window_days: int = 180) -> CompResult:
    """The ladder, in order. Returns STATUS_NONE rather than inventing a number."""
    universe, dropped = screen_universe(comps, as_of, window_days)
    result = CompResult(status=STATUS_NONE, hood=subject_hood, rejected=dropped)

    if not subject_sqft or subject_sqft <= 0:
        result.note = "subject has no living area - cannot be comped"
        return result

    # 1. same neighbourhood code, identical
    pool = [c for c in universe if c.hood.strip().upper() == subject_hood.strip().upper()]
    if not pool:
        result.note = f"no usable sale in neighbourhood {subject_hood} inside the window"
        return result

    # Hard exclusions stay in the pool for REPORTING only, never in the maths.
    usable = []
    for c in pool:
        if c.exclusion in EXCLUSION_REASONS:
            result.excluded_in_radius.append(c)
        else:
            usable.append(c)
    if not usable:
        result.note = "every same-neighbourhood sale was excluded (see excluded list)"
        return result

    # 2. +-30% sqft band
    band = [c for c in usable
            if abs(c.sqft - subject_sqft) / subject_sqft <= SQFT_BAND]
    if not band:
        result.note = f"no same-neighbourhood sale within +-{int(SQFT_BAND*100)}% sqft"
        return result

    # 3 + 4. smallest radius with >=3, style preference inside it
    for radius in RADIUS_LADDER:
        hits = [c for c in band if miles(lat, lon, c.lat, c.lon) <= radius]
        if len(hits) < MIN_COMPS:
            continue
        styled = [c for c in hits if c.style and c.style == style]
        chosen = styled if len(styled) >= MIN_COMPS else hits
        ppsf = [c.ppsf for c in chosen]
        p75 = percentile(ppsf, 0.75)
        p25 = percentile(ppsf, 0.25)
        result.status = STATUS_PRICED
        result.arv = int(round(subject_sqft * p75 * HAIRCUT))
        result.as_is = int(round(subject_sqft * p25 * HAIRCUT))
        result.n = len(chosen)
        result.radius = radius
        result.chosen = chosen
        result.confidence = "HIGH" if len(chosen) >= HIGH_CONFIDENCE_COMPS else "LOW"
        result.basis = (f"{int(subject_sqft)}sqft x ${p75:,.0f}/sqft p75 x {HAIRCUT}"
                        f" (n={len(chosen)}, {radius} mi, {subject_hood})")
        result.note = "p25 kept separately as the as-is value - never shown as ARV"
        return result

    result.note = (f"fewer than {MIN_COMPS} comps at every radius up to {RADIUS_CAP} mi "
                   f"- UNPRICED. Do not widen, do not average.")
    return result


# ---------------------------------------------------------------------------
# The six checks. Each compares two independent things, and each can FAIL.
# ---------------------------------------------------------------------------

@dataclass
class Priced:
    """A row as it would be reported, so checks can run over real output."""
    subject: dict
    result: CompResult
    repairs: float | None = None        # None == UNGRADED
    ceiling: int | None = None
    repairs_status: str = "UNGRADED"


def check_1_same_neighbourhood(row: Priced) -> tuple[bool, str]:
    if row.result.status != STATUS_PRICED:
        return True, "unpriced - check does not apply"
    bad = [c.address for c in row.result.chosen
           if c.hood.strip().upper() != row.result.hood.strip().upper()]
    return (not bad), (f"{len(bad)} comps outside subject neighbourhood "
                       f"{row.result.hood}" if bad else
                       f"all {len(row.result.chosen)} comps in {row.result.hood}")


def check_2_min_comps(row: Priced) -> tuple[bool, str]:
    if row.result.status != STATUS_PRICED:
        return True, "unpriced - check does not apply"
    return (row.result.n >= MIN_COMPS), f"n={row.result.n} (min {MIN_COMPS})"


def check_3_radius_cap(row: Priced) -> tuple[bool, str]:
    if row.result.radius is None:
        return True, "no radius recorded"
    over = [c.address for c in row.result.chosen
            if miles(row.subject["lat"], row.subject["lon"], c.lat, c.lon) > RADIUS_CAP + 1e-9]
    return (row.result.radius <= RADIUS_CAP + 1e-9 and not over,
            f"radius {row.result.radius} mi (cap {RADIUS_CAP}), {len(over)} comps beyond cap")


def check_4_window(row: Priced) -> tuple[bool, str]:
    if row.result.status != STATUS_PRICED:
        return True, "unpriced - check does not apply"
    as_of = row.subject["as_of"]
    window = row.subject.get("window_days", 180)
    cutoff = as_of - timedelta(days=window)
    old = [c.address for c in row.result.chosen if c.sold < cutoff]
    return (not old), (f"{len(old)} comps older than {cutoff.isoformat()}" if old
                       else f"every comp sold on/after {cutoff.isoformat()}")


def check_5_no_invented_arv(row: Priced) -> tuple[bool, str]:
    r = row.result
    if r.status == STATUS_PRICED:
        return True, "priced from comps"
    invented = (r.arv is not None) or bool(r.basis) or r.confidence != STATUS_NONE
    return (not invented), ("unpriced row carries an ARV/basis/confidence"
                            if invented else "unpriced row is clean: no ARV, no basis")


def check_6_repairs_graded(row: Priced) -> tuple[bool, str]:
    if row.repairs is None:
        ok = row.repairs_status == "UNGRADED" and row.ceiling is None
        return ok, "ungraded repairs left blank, no ceiling quoted"
    ok = row.repairs_status != "UNGRADED" and row.ceiling is not None
    return ok, f"repairs ${row.repairs:,.0f} graded, ceiling quoted"


CHECKS = [
    ("comps sit in the subject's own neighbourhood", check_1_same_neighbourhood),
    ("comp set is at least 3 sales", check_2_min_comps),
    ("no comp beyond the 1.5 mi radius cap", check_3_radius_cap),
    ("every comp sale is inside the window", check_4_window),
    ("an unpriced row carries no invented ARV", check_5_no_invented_arv),
    ("no repair number without a grade", check_6_repairs_graded),
]


def run_checks(row: Priced) -> list[tuple[str, bool, str]]:
    out = []
    for label, fn in CHECKS:
        ok, detail = fn(row)
        out.append((label, ok, detail))
    return out


# ---------------------------------------------------------------------------
# Fixture loading
# ---------------------------------------------------------------------------

def load_comps(path: str, as_of: date) -> list[Comp]:
    comps = []
    with open(path, newline="", encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            sold = r.get("sold", "").strip()
            if not sold:
                continue
            comps.append(Comp(
                address=r.get("address", "").strip(),
                sold=date.fromisoformat(sold),
                price=float(r.get("price") or 0),
                sqft=float(r.get("sqft") or 0),
                hood=r.get("hood", "").strip(),
                lat=float(r.get("lat") or 0),
                lon=float(r.get("lon") or 0),
                style=r.get("style", "").strip().upper(),
                beds=r.get("beds", "").strip(),
                exclusion=r.get("exclusion", "").strip(),
            ))
    return comps


# ---------------------------------------------------------------------------
# Selftest: six checks, then six targeted defects, one per check
# ---------------------------------------------------------------------------

def _fixture_subject() -> dict:
    return {"sqft": 1642.0, "hood": "SYNTH-44302", "lat": 41.0790, "lon": -81.5360,
            "style": "COLONIAL", "as_of": date(2026, 10, 31), "window_days": 180}


def _fixture_comps(subject: dict) -> list[Comp]:
    """SYNTHETIC. Fabricated to exercise the ladder. Never a lead list."""
    base = [
        ("101 Fixture St", date(2026, 8, 14), 100_000, 1_344, "SYNTH-44302", 0.10, 0.00, "COLONIAL", ""),
        ("102 Fixture St", date(2026, 7, 2), 112_000, 1_384, "SYNTH-44302", 0.22, 0.10, "COLONIAL", ""),
        ("103 Fixture St", date(2026, 6, 20), 120_000, 1_396, "SYNTH-44302", 0.35, -0.12, "COLONIAL", ""),
        ("104 Fixture St", date(2026, 9, 8), 94_500, 1_936, "SYNTH-44302", 0.44, 0.28, "COLONIAL", ""),
        ("105 Fixture St", date(2026, 5, 11), 187_500, 1_208, "SYNTH-44302", 0.18, -0.30, "COLONIAL", "new_build"),
        ("106 Fixture St", date(2026, 4, 3), 74_000, 1_146, "SYNTH-44302", 0.60, 0.60, "COLONIAL", "deed_restricted"),
        ("107 Fixture St", date(2026, 8, 1), 96_000, 1_290, "SYNTH-99999", 0.30, 0.30, "COLONIAL", ""),
        ("108 Fixture St", date(2024, 8, 1), 99_000, 1_300, "SYNTH-44302", 0.12, 0.12, "COLONIAL", ""),
        ("109 Fixture St", date(2026, 9, 1), 325, 1_300, "SYNTH-44302", 0.14, 0.14, "COLONIAL", ""),
    ]
    comps = []
    for addr, sold, price, sqft, hood, dlat, dlon, style, excl in base:
        comps.append(Comp(address=addr, sold=sold, price=float(price), sqft=float(sqft),
                          hood=hood, lat=subject["lat"] + dlat / 69.0,
                          lon=subject["lon"] + dlon / (69.0 * math.cos(math.radians(subject["lat"]))),
                          style=style, beds="3", exclusion=excl))
    return comps


def selftest() -> int:
    print("SELFTEST - SYNTHETIC fixture data. Not a lead list. Not an offer.\n")
    subject = _fixture_subject()
    comps = _fixture_comps(subject)
    result = compute_arv(subject["sqft"], subject["hood"], subject["lat"], subject["lon"],
                         subject["style"], comps, subject["as_of"], subject["window_days"])

    print(f"  universe drops: {result.rejected}")
    print(f"  excluded in radius: {[c.address for c in result.excluded_in_radius]}")
    print(f"  chosen: {[(c.address, f'${c.ppsf:.0f}/sf') for c in result.chosen]}")
    print(f"  ARV ${result.arv:,}  as-is ${result.as_is:,}  n={result.n}  "
          f"radius {result.radius} mi  {result.confidence}")
    print(f"  basis: {result.basis}\n")

    row = Priced(subject=subject, result=result)
    failures = 0
    for label, ok, detail in run_checks(row):
        print(f"  {'PASS' if ok else 'FAIL'}  {label}  [{detail}]")
        failures += 0 if ok else 1
    print(f"\n  {len(CHECKS) - failures}/{len(CHECKS)} checks PASS on the healthy fixture")

    # --- the part that matters: prove each check can actually fail ------------
    def mutate(name: str) -> list[Priced]:
        r = compute_arv(subject["sqft"], subject["hood"], subject["lat"],
                        subject["lon"], subject["style"], comps,
                        subject["as_of"], subject["window_days"])
        s = dict(subject)
        if name == "cross_neighbourhood":
            r.chosen[0].hood = "SYNTH-99999"            # comp from a different ZIP
        elif name == "too_few_comps":
            r.chosen = r.chosen[:2]
            r.n = 2
        elif name == "beyond_radius":
            far = Comp("999 Far St", date(2026, 8, 1), 150_000, 1_600, subject["hood"],
                       subject["lat"] + 2.5 / 69.0, subject["lon"], "COLONIAL")
            r.chosen = r.chosen + [far]
            r.n = len(r.chosen)
            r.radius = 2.50
        elif name == "stale_comp":
            r.chosen[0].sold = date(2023, 1, 1)          # older than the window
        elif name == "invented_arv":
            blank = CompResult(status=STATUS_NONE, hood=subject["hood"])
            blank.arv = 128_000                          # the sin
            blank.basis = "felt right"
            return [Priced(subject=s, result=blank)]
        elif name == "ungraded_repairs":
            s["_repairs"] = 55_000
            return [Priced(subject=s, result=r, repairs=55_000,
                           ceiling=20_000, repairs_status="UNGRADED")]
        return [Priced(subject=s, result=r)]

    mutations = [
        ("cross_neighbourhood", 0),
        ("too_few_comps", 1),
        ("beyond_radius", 2),
        ("stale_comp", 3),
        ("invented_arv", 4),
        ("ungraded_repairs", 5),
    ]
    print("\n  Mutation test - one deliberate defect per check:")
    proven = 0
    for name, target in mutations:
        mutated = mutate(name)[0]
        label, ok, detail = run_checks(mutated)[target]
        flipped = not ok
        proven += 1 if flipped else 0
        print(f"  {'CAUGHT' if flipped else 'MISSED'}  {name} -> {label}  [{detail}]")

    print(f"\n  {proven}/{len(CHECKS)} checks proven able to fail")

    # --- economics regressions (the documented worked examples) --------------
    print("\n  Economics regressions:")
    cases = [
        (150_000, 0, {"CEILING (0.70 x ARV - repairs)": 105_000,
                      "OFFER LOW (0.55)": 82_500, "OFFER HIGH (0.60)": 90_000,
                      "FRICTION (ceiling - offer high)": 15_000,
                      "CONTRACT FOR $10K FEE": 95_000}),
        (350_000, 34_933, {"CEILING (0.70 x ARV - repairs)": 210_067,
                           "OFFER LOW (0.55)": 157_567, "OFFER HIGH (0.60)": 175_067,
                           "FRICTION (ceiling - offer high)": 35_000,
                           "CONTRACT FOR $10K FEE": 200_067}),
        (125_000, 0, {"CEILING (0.70 x ARV - repairs)": 87_500,
                      "OFFER LOW (0.55)": 68_750, "OFFER HIGH (0.60)": 75_000,
                      "FRICTION (ceiling - offer high)": 12_500,
                      "CONTRACT FOR $10K FEE": 77_500}),
    ]
    econ_ok = True
    for arv, repairs, expect in cases:
        got = economics(arv, repairs)
        mismatches = {k: (expect[k], got[k]) for k in expect if got[k] != expect[k]}
        line = f"${arv:,} ARV / ${repairs:,} repairs -> ceiling ${got['CEILING (0.70 x ARV - repairs)']:,}"
        if mismatches:
            econ_ok = False
            line += f"   MISMATCH {mismatches}"
        print(f"  {'PASS' if not mismatches else 'FAIL'}  {line}")

    print("\n  Economics must not double-deduct the fee: ceiling already excludes it,")
    print("  contract subtracts it once. 70% cap != offer target.\n")

    ok = (failures == 0) and (proven == len(CHECKS)) and econ_ok
    print("PASS  all checks green, all mutations caught, economics reproduce"
          if ok else "FAIL  something above is broken - do not quote a number")
    return 0 if ok else 1


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def cmd_arv(args) -> int:
    subject = json.loads(args.subject)
    as_of = date.fromisoformat(args.as_of) if args.as_of else date.today()
    window = args.window
    comps = load_comps(args.comps, as_of)
    result = compute_arv(subject["sqft"], subject["hood"], subject["lat"], subject["lon"],
                         (subject.get("style") or "").upper(), comps, as_of, window)

    print(f"SUBJECT  {subject.get('address', '(unnamed)')}  "
          f"{subject.get('beds', '?')}  {int(subject['sqft']):,} sf  {subject['hood']}")
    print(f"WINDOW   {window} days to {as_of.isoformat()}\n")

    if result.chosen:
        print(f"{'COMP':26} {'SOLD':12} {'PRICE':>10} {'SQFT':>6} {'$/SF':>7} {'MI':>5}")
        for c in result.chosen:
            d = miles(subject["lat"], subject["lon"], c.lat, c.lon)
            print(f"{c.address[:26]:26} {c.sold.isoformat():12} "
                  f"${c.price:>9,.0f} {int(c.sqft):>6,} ${c.ppsf:>6.0f} {d:>5.2f}")
    if result.excluded_in_radius:
        print("\nEXCLUDED (in the radius, not in the maths):")
        for c in result.excluded_in_radius:
            print(f"  {c.address[:28]:28} ${c.price:>9,.0f}  "
                  f"{EXCLUSION_REASONS.get(c.exclusion, c.exclusion)}")
    if result.rejected:
        print(f"\nUNIVERSE DROPS  {result.rejected}")

    print()
    if result.status == STATUS_PRICED:
        print(f"ARV      ${result.arv:,}   basis: {result.basis}")
        print(f"AS-IS    ${result.as_is:,}   (p25 - never shown as ARV)")
        print(f"CONF     {result.confidence}  n={result.n}  radius {result.radius} mi")
        print(f"STATUS   {STATUS_PRICED}")
        if args.repairs is not None:
            e = economics(result.arv, args.repairs)
            print("\nECONOMICS (repairs graded)")
            for k, v in e.items():
                print(f"  {k:34} {f'${v:,}' if isinstance(v, int) else v}")
        else:
            print("REPAIRS  UNGRADED - no ceiling quoted. Ceiling cannot be computed.")
    else:
        print(f"ARV      {STATUS_NONE} - {result.note}")
        print("         Unpriced is a complete answer. Do not quote a number.")

    row = Priced(subject={**subject, "as_of": as_of, "window_days": window},
                 result=result,
                 repairs=args.repairs,
                 ceiling=economics(result.arv, args.repairs)["CEILING (0.70 x ARV - repairs)"]
                 if (args.repairs is not None and result.arv) else None,
                 repairs_status="GRADED" if args.repairs is not None else "UNGRADED")
    print("\nCHECKS")
    fails = 0
    for label, ok, detail in run_checks(row):
        print(f"  {'PASS' if ok else 'FAIL'}  {label}  [{detail}]")
        fails += 0 if ok else 1
    print("\nESTIMATE - not an appraisal, not an offer.")
    return 0 if fails == 0 else 1


def cmd_offer(args) -> int:
    e = economics(args.offer, args.repairs or 0)
    print(f"ARV ${args.offer:,.0f}   repairs ${args.repairs or 0:,.0f}")
    print(f"{'':34}{'VALUE':>12}   {'% ARV':>6}")
    for k, v in e.items():
        if "% OF ARV" in k:
            print(f"  {k:32}{v:>11.1f}%   {'':>6}")
            continue
        pct = f"{v / args.offer * 100:>5.1f}%" if args.offer and isinstance(v, int) else ""
        print(f"  {k:32}{f'${v:,}':>12}   {pct:>6}")
    if args.ask is not None:
        need = e["CONTRACT FOR $10K FEE"]
        disc = (need - args.ask) / args.ask * 100
        print(f"\n  asking ${args.ask:,.0f} -> contract needed ${need:,} "
              f"= {disc:+.1f}% vs asking")
        print(f"  {'CLEARS' if need >= args.ask else 'NEEDS A CUT'} at asking price")
    print("\n70% is a cap, 55-60% is the target, the gap is the pay stack.")
    print("Fee deducted once, at the contract step. ESTIMATE - not an offer.")
    return 0


def cmd_exclusions(_args) -> int:
    print("EXCLUSIONS - a sale that matches one of these is not a comp:\n")
    for key, why in EXCLUSION_REASONS.items():
        print(f"  {key:16} {why}")
    print("\nAlso excluded, by judgement:")
    print("  - newer build in an older block (different product)")
    print("  - asking price used as a comp (never)")
    print("  - cross-ZIP / cross-submarket bracketing when no same-area sale exists")
    print("  - anything that forces widening past 1.5 mi to reach 3 comps")
    print("\nIf it survives none of these and there are still <3 comps: UNPRICED.")
    return 0


def main(argv=None) -> int:
    p = argparse.ArgumentParser(description="Comping + ARV engine. See comping/COMPING.md")
    p.add_argument("--selftest", action="store_true",
                   help="offline: 6 checks, 6 mutations, economics regressions")
    p.add_argument("--exclusions", action="store_true", help="print the exclusion rules")
    p.add_argument("--offer", type=float, help="ARV, for the economics model")
    p.add_argument("--repairs", type=float, help="graded repairs")
    p.add_argument("--ask", type=float, help="asking price, to show the discount needed")
    p.add_argument("--comps", help="comp CSV")
    p.add_argument("--subject", help='JSON: {"sqft":..,"hood":..,"lat":..,"lon":..,"style":..}')
    p.add_argument("--as-of", help="YYYY-MM-DD, defaults to today")
    p.add_argument("--window", type=int, default=180, help="comp window in days (max 365)")
    a = p.parse_args(argv)

    if a.selftest:
        return selftest()
    if a.exclusions:
        return cmd_exclusions(a)
    if a.offer is not None:
        return cmd_offer(a)
    if a.comps and a.subject:
        if a.window > 365:
            print("window > 365 days: the rule allows 12 months maximum", file=sys.stderr)
            return 2
        return cmd_arv(a)
    p.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
