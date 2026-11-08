#!/usr/bin/env python3
"""
comp.py - the comping + ARV engine (v2.1). Standard library only.

The rule (see comping/COMPING.md section 2):

    compset = same neighbourhood -> >= subject beds -> +-30% sqft
              -> smallest radius with >=3 -> RENOVATED condition only
              -> consistency gate (drop illogical price gaps)

    ARV LOW    = subject_sqft x p25 $/sqft x 0.88
    ARV POINT  = subject_sqft x p50 $/sqft x 0.88
    ARV HIGH   = subject_sqft x p75 $/sqft x 0.88

    under 3 comps at 1.50 mi -> NO ARV. Do not widen, do not average.

Modes:
    python3 comp.py --selftest
    python3 comp.py --comps fixtures/akron_44302_worked_example.csv \
        --as-of 2026-10-31 --repairs 65000 \
        --subject '{"address":"141 Grand Ave","beds":"3","sqft":1642,"hood":"44302",
                    "lat":41.079,"lon":-81.536,"style":"COLONIAL"}'
    python3 comp.py --repair-tiers
    python3 comp.py --exclusions
    python3 comp.py --offer 350000 --repairs 34933

Exit codes: 0 priced / 1 a check failed / 3 UNPRICED (no ARV produced).
Every number is an ESTIMATE. Not an appraisal, not an offer.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import re
import sys
from dataclasses import dataclass, field
from datetime import date, timedelta

# ---------------------------------------------------------------------------
# Constants - see comping/COMPING.md. Do not tune per deal.
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

# Consistency gate: a comp further than this from the comp-set median $/sf is
# dropped as an illogical price gap (a $120K sitting next to a $50K).
CONSISTENCY_BAND = 0.45

# Condition tiers. ARV requires the comp pool to already be in the target
# condition, because ARV = value AFTER repair.
CONDITION_ARV = "renovated"
CONDITIONS = ("renovated", "dated", "distressed", "unknown")

BUYER_PCT = 0.70
OFFER_LOW_PCT = 0.55
OFFER_HIGH_PCT = 0.60
WHOLE_FEE = 10_000
JV_SPLIT = 0.50

# Repair tiers, $/sqft of living area. Moderate is the placeholder when
# condition is unconfirmed - see references/repairs.md.
REPAIR_TIERS = {"light": 20, "moderate": 35, "heavy": 50}

EXCLUSION_REASONS = {
    "deed_restricted": "Sale restricted (AMI / income-limited) - a FLOOR, not market value",
    "new_build": "Newer build - different product from the subject",
    "non_arms_length": "Non-arm's-length transfer (quitclaim / family / $1 deed)",
    "condo": "Condo - different product unless the subject is a condo",
    "not_sold": "Not a closed sale (active / pending / withdrawn)",
    "different_tier": "Different market tier (mansion vs distressed rowhouse)",
}

STATUS_PRICED = "PRELIMINARY - not an offer"
STATUS_NONE = "NO COMPS"


# ---------------------------------------------------------------------------
# Small helpers
# ---------------------------------------------------------------------------

def miles(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    dlat = (lat2 - lat1) * 69.0
    dlon = (lon2 - lon1) * 69.0 * math.cos(math.radians((lat1 + lat2) / 2.0))
    return math.hypot(dlat, dlon)


def percentile(values: list[float], q: float) -> float:
    v = sorted(values)
    if not v:
        raise ValueError("percentile of empty list")
    if len(v) == 1:
        return float(v[0])
    pos = (len(v) - 1) * q
    lo = int(pos)
    hi = min(lo + 1, len(v) - 1)
    return v[lo] + (v[hi] - v[lo]) * (pos - lo)


def beds_num(value) -> int | None:
    """'3/2' -> 3. '3 bd' -> 3. '' -> None. Bed count is the floor, baths ignored."""
    if value is None:
        return None
    m = re.match(r"\s*(\d+)", str(value))
    return int(m.group(1)) if m else None


def repair_cost(sqft: float, tier: str) -> int:
    """Tier-based repair estimate. A range comes from the tier boundary, not a guess."""
    t = (tier or "").strip().lower()
    if t not in REPAIR_TIERS:
        raise ValueError(f"tier must be one of {sorted(REPAIR_TIERS)}")
    return int(round(sqft * REPAIR_TIERS[t]))


def repair_range(sqft: float, tier: str) -> tuple[int, int, int]:
    """(low, point, high). Point is the tier rate; the band is +-15% of it."""
    point = repair_cost(sqft, tier)
    return int(round(point * 0.85)), point, int(round(point * 1.15))


# ---------------------------------------------------------------------------
# Economics
# ---------------------------------------------------------------------------

def economics(arv: float, repairs: float = 0.0) -> dict:
    """70% is a CAP. 55-60% is a TARGET under the cap. Fee deducted once, later."""
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


def mao_by_tier(result: "CompResult", repairs: float) -> dict:
    """Step 9: MAO = (ARV x 0.70) - repairs, computed on each ARV tier."""
    out = {}
    for label, key in (("LOW", "arv_low"), ("POINT", "arv_point"), ("HIGH", "arv_high")):
        v = getattr(result, key)
        if v:
            out[label] = economics(v, repairs)["CEILING (0.70 x ARV - repairs)"]
    return out


# ---------------------------------------------------------------------------
# Data model
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
    condition: str = ""            # renovated | dated | distressed | unknown | ""
    exclusion: str = ""

    @property
    def ppsf(self) -> float:
        return self.price / self.sqft

    @property
    def beds_n(self) -> int | None:
        return beds_num(self.beds)


@dataclass
class CompResult:
    status: str
    arv: int | None = None                 # headline = the tier you underwrite to
    arv_low: int | None = None
    arv_point: int | None = None
    arv_high: int | None = None
    as_is: int | None = None
    basis: str = ""
    n: int = 0
    radius: float | None = None
    hood: str = ""
    confidence: str = STATUS_NONE
    chosen: list[Comp] = field(default_factory=list)
    excluded_in_radius: list[Comp] = field(default_factory=list)
    outliers: list[Comp] = field(default_factory=list)
    non_renovated: list[Comp] = field(default_factory=list)
    rejected: dict = field(default_factory=dict)
    note: str = ""
    underwrite_to: str = "POINT"

    def tier(self, label: str) -> int | None:
        return {"LOW": self.arv_low, "POINT": self.arv_point,
                "HIGH": self.arv_high}.get(label)


# ---------------------------------------------------------------------------
# The ladder
# ---------------------------------------------------------------------------

def screen_universe(comps: list[Comp], as_of: date, window_days: int) -> tuple[list[Comp], dict]:
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


def drop_outliers(pool: list[Comp], band: float = CONSISTENCY_BAND) -> tuple[list[Comp], list[Comp]]:
    """Final gate: discard comps causing an illogical price gap around the median.

    Runs once, compares to the median $/sf, and never fires on a set of fewer
    than MIN_COMPS - you cannot call something an outlier without a centre.
    """
    if len(pool) < MIN_COMPS:
        return pool, []
    med = percentile([c.ppsf for c in pool], 0.50)
    lo, hi = med * (1 - band), med * (1 + band)
    keep = [c for c in pool if lo <= c.ppsf <= hi]
    out = [c for c in pool if not (lo <= c.ppsf <= hi)]
    # No rescue. Putting the outlier back to reach a count is the exact failure
    # this system forbids: the caller must accept a smaller set or refuse to price.
    return keep, out


def compute_arv(subject_sqft: float, subject_hood: str, lat: float, lon: float,
                style: str, comps: list[Comp], as_of: date,
                window_days: int = 180, subject_beds: int | None = None,
                consistency_band: float = CONSISTENCY_BAND) -> CompResult:
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

    # hard exclusions: reported, never in the maths
    usable = []
    for c in pool:
        if c.exclusion in EXCLUSION_REASONS:
            result.excluded_in_radius.append(c)
        else:
            usable.append(c)
    if not usable:
        result.note = "every same-neighbourhood sale was excluded (see excluded list)"
        return result

    # 2. BED-COUNT FLOOR - a comp may never have fewer beds than the subject
    if subject_beds:
        kept = [c for c in usable if c.beds_n is None or c.beds_n >= subject_beds]
        dropped_beds = [c for c in usable if c.beds_n is not None and c.beds_n < subject_beds]
        usable = kept
        result.rejected = {**result.rejected, "under_bed_floor": len(dropped_beds)}
        if not usable:
            result.note = (f"every same-neighbourhood sale has fewer than "
                           f"{subject_beds} beds - the bed floor cannot be met, so "
                           f"there is no ARV. Unpriced is the answer.")
            return result

    # 3. +-30% sqft band
    band = [c for c in usable
            if abs(c.sqft - subject_sqft) / subject_sqft <= SQFT_BAND]
    if not band:
        result.note = f"no same-neighbourhood sale within +-{int(SQFT_BAND*100)}% sqft"
        return result

    # A candidate radius must survive every filter below before it is accepted.
    # Widening happens because the closest radius could not produce a CLEAN set,
    # not merely because it was short.
    pool2: list[Comp] = []
    chosen_radius = None
    last_refusal = ""

    for radius in RADIUS_LADDER:
        cand = [c for c in band if miles(lat, lon, c.lat, c.lon) <= radius]
        if len(cand) < MIN_COMPS:
            last_refusal = f"fewer than {MIN_COMPS} sales within {radius} mi"
            continue

        # style preference inside the radius (>=3 sharing it)
        styled = [c for c in cand if c.style and c.style == style]
        cand = styled if len(styled) >= MIN_COMPS else cand

        # CONDITION GATE - ARV is post-repair value, so the pool must already be
        # in the target condition. Unknown counts as not-renovated.
        renovated = [c for c in cand
                     if (c.condition or "").strip().lower() == CONDITION_ARV]
        if len(renovated) < MIN_COMPS:
            last_refusal = (f"only {len(renovated)} renovated comp(s) within {radius} mi "
                            f"(needs {MIN_COMPS})")
            result.non_renovated = [c for c in cand if c not in renovated]
            continue

        # CONSISTENCY GATE - discard illogical price gaps around the median
        clean, outliers = drop_outliers(renovated, consistency_band)
        if len(clean) < MIN_COMPS:
            last_refusal = (f"consistency gate left {len(clean)} comp(s) within "
                            f"{radius} mi (needs {MIN_COMPS})")
            result.outliers = outliers
            result.non_renovated = [c for c in cand if c not in renovated]
            continue

        pool2, chosen_radius = clean, radius
        result.outliers = outliers
        result.non_renovated = [c for c in cand if c not in renovated]
        break

    if chosen_radius is None:
        result.note = (f"no radius up to {RADIUS_CAP} mi produced a clean comp set: "
                       f"{last_refusal}. UNPRICED - do not widen further, do not "
                       f"average across tiers, do not reinstate an outlier to reach a count.")
        return result

    ppsf = [c.ppsf for c in pool2]
    p25, p50, p75 = (percentile(ppsf, q) for q in (0.25, 0.50, 0.75))

    result.status = STATUS_PRICED
    result.arv_low = int(round(subject_sqft * p25 * HAIRCUT))
    result.arv_point = int(round(subject_sqft * p50 * HAIRCUT))
    result.arv_high = int(round(subject_sqft * p75 * HAIRCUT))
    result.as_is = int(round(subject_sqft * p25 * HAIRCUT))
    result.n = len(pool2)
    result.radius = chosen_radius
    result.chosen = pool2
    result.confidence = "HIGH" if len(pool2) >= HIGH_CONFIDENCE_COMPS else "LOW"
    # Underwrite to the POINT when confidence is HIGH, to the LOW when it is not.
    result.underwrite_to = "POINT" if result.confidence == "HIGH" else "LOW"
    result.arv = result.tier(result.underwrite_to)
    result.basis = (f"{int(subject_sqft)}sqft x [${p25:,.0f} / ${p50:,.0f} / ${p75:,.0f}]"
                    f"/sqft p25-p50-p75 x {HAIRCUT}; n={len(pool2)}, {chosen_radius} mi, "
                    f"{subject_hood}; renovate-only; underwriting to "
                    f"{result.underwrite_to}")
    result.note = ("p25 is also the as-is floor - never shown as ARV. "
                   "Underwrite to the LOW when confidence is LOW.")
    return result


# ---------------------------------------------------------------------------
# Checks. Each compares two independent things, and each can FAIL.
# ---------------------------------------------------------------------------

@dataclass
class Priced:
    subject: dict
    result: CompResult
    repairs: float | None = None
    ceiling: int | None = None
    repairs_status: str = "UNGRADED"


def check_1_same_neighbourhood(row: Priced) -> tuple[bool, str]:
    if row.result.status != STATUS_PRICED:
        return True, "unpriced - check does not apply"
    bad = [c.address for c in row.result.chosen
           if c.hood.strip().upper() != row.result.hood.strip().upper()]
    return (not bad), (f"{len(bad)} comps outside subject neighbourhood {row.result.hood}"
                       if bad else f"all {len(row.result.chosen)} comps in {row.result.hood}")


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
    cutoff = as_of - timedelta(days=row.subject.get("window_days", 180))
    old = [c.address for c in row.result.chosen if c.sold < cutoff]
    return (not old), (f"{len(old)} comps older than {cutoff.isoformat()}" if old
                       else f"every comp sold on/after {cutoff.isoformat()}")


def check_5_no_invented_arv(row: Priced) -> tuple[bool, str]:
    r = row.result
    if r.status == STATUS_PRICED:
        return True, "priced from comps"
    invented = (r.arv is not None or r.arv_low is not None or r.arv_point is not None
                or r.arv_high is not None or bool(r.basis) or r.confidence != STATUS_NONE)
    return (not invented), ("unpriced row carries an ARV/basis/confidence"
                            if invented else "unpriced row is clean: no ARV, no basis")


def check_6_repairs_graded(row: Priced) -> tuple[bool, str]:
    if row.repairs is None:
        ok = row.repairs_status == "UNGRADED" and row.ceiling is None
        return ok, "ungraded repairs left blank, no ceiling quoted"
    ok = row.repairs_status != "UNGRADED" and row.ceiling is not None
    return ok, f"repairs ${row.repairs:,.0f} graded, ceiling quoted"


def check_7_bed_floor(row: Priced) -> tuple[bool, str]:
    """No comp may have fewer beds than the subject."""
    if row.result.status != STATUS_PRICED:
        return True, "unpriced - check does not apply"
    sb = row.subject.get("beds_n")
    if not sb:
        return True, "subject bed count not supplied - bed floor not applied"
    bad = [c.address for c in row.result.chosen
           if c.beds_n is not None and c.beds_n < sb]
    return (not bad), (f"{len(bad)} comps below the {sb}-bed floor" if bad
                       else f"every comp has >= {sb} beds")


def check_8_renovated_only(row: Priced) -> tuple[bool, str]:
    """ARV comps must be in the target (renovated) condition."""
    if row.result.status != STATUS_PRICED:
        return True, "unpriced - check does not apply"
    bad = [c.address for c in row.result.chosen
           if (c.condition or "").strip().lower() != CONDITION_ARV]
    return (not bad), (f"{len(bad)} non-renovated comps in the ARV pool" if bad
                       else f"all {len(row.result.chosen)} ARV comps are renovated")


def check_9_no_price_gap(row: Priced) -> tuple[bool, str]:
    """No comp may sit an illogical distance from the comp-set median $/sf."""
    if row.result.status != STATUS_PRICED:
        return True, "unpriced - check does not apply"
    ppsf = [c.ppsf for c in row.result.chosen]
    med = percentile(ppsf, 0.50)
    lo, hi = med * (1 - CONSISTENCY_BAND), med * (1 + CONSISTENCY_BAND)
    bad = [c.address for c in row.result.chosen if not (lo <= c.ppsf <= hi)]
    return (not bad), (f"{len(bad)} comps outside the consistency band around "
                       f"${med:,.0f}/sf" if bad else
                       f"every comp within +-{int(CONSISTENCY_BAND*100)}% of "
                       f"${med:,.0f}/sf")


CHECKS = [
    ("comps sit in the subject's own neighbourhood", check_1_same_neighbourhood),
    ("comp set is at least 3 sales", check_2_min_comps),
    ("no comp beyond the 1.5 mi radius cap", check_3_radius_cap),
    ("every comp sale is inside the window", check_4_window),
    ("an unpriced row carries no invented ARV", check_5_no_invented_arv),
    ("no repair number without a grade", check_6_repairs_graded),
    ("no comp below the subject's bed count", check_7_bed_floor),
    ("ARV pool is renovated-condition only", check_8_renovated_only),
    ("no illogical price gap in the comp set", check_9_no_price_gap),
]


def run_checks(row: Priced) -> list[tuple[str, bool, str]]:
    return [(label, *fn(row)) for label, fn in CHECKS]


# ---------------------------------------------------------------------------
# Loading
# ---------------------------------------------------------------------------

def load_comps(path: str, as_of: date) -> list[Comp]:
    comps = []
    with open(path, newline="", encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            sold = (r.get("sold") or "").strip()
            if not sold:
                continue
            comps.append(Comp(
                address=(r.get("address") or "").strip(),
                sold=date.fromisoformat(sold),
                price=float(r.get("price") or 0),
                sqft=float(r.get("sqft") or 0),
                hood=(r.get("hood") or "").strip(),
                lat=float(r.get("lat") or 0),
                lon=float(r.get("lon") or 0),
                style=(r.get("style") or "").strip().upper(),
                beds=(r.get("beds") or "").strip(),
                condition=(r.get("condition") or "").strip().lower(),
                exclusion=(r.get("exclusion") or "").strip(),
            ))
    return comps


# ---------------------------------------------------------------------------
# Selftest
# ---------------------------------------------------------------------------

def _fixture_subject() -> dict:
    return {"sqft": 1642.0, "hood": "SYNTH-44302", "lat": 41.0790, "lon": -81.5360,
            "style": "COLONIAL", "as_of": date(2026, 10, 31), "window_days": 180,
            "beds_n": 3}


def _fixture_comps(subject: dict) -> list[Comp]:
    """SYNTHETIC. Fabricated to exercise the ladder. Never a lead list."""
    #  (addr, sold, price, sqft, hood, dlat, dlon, style, beds, condition, exclusion)
    base = [
        ("101 Fixture St", date(2026, 8, 14), 100_000, 1_344, "SYNTH-44302", 0.10, 0.00, "COLONIAL", "3", "renovated", ""),
        ("102 Fixture St", date(2026, 7, 2), 112_000, 1_384, "SYNTH-44302", 0.22, 0.10, "COLONIAL", "3", "renovated", ""),
        ("103 Fixture St", date(2026, 6, 20), 120_000, 1_396, "SYNTH-44302", 0.35, -0.12, "COLONIAL", "4", "renovated", ""),
        ("104 Fixture St", date(2026, 9, 8), 94_500, 1_936, "SYNTH-44302", 0.44, 0.28, "COLONIAL", "3", "renovated", ""),
        ("105 Fixture St", date(2026, 5, 11), 187_500, 1_208, "SYNTH-44302", 0.18, -0.30, "COLONIAL", "3", "renovated", "new_build"),
        ("106 Fixture St", date(2026, 4, 3), 74_000, 1_146, "SYNTH-44302", 0.60, 0.60, "COLONIAL", "3", "renovated", "deed_restricted"),
        ("107 Fixture St", date(2026, 8, 1), 96_000, 1_290, "SYNTH-99999", 0.30, 0.30, "COLONIAL", "3", "renovated", ""),
        ("108 Fixture St", date(2024, 8, 1), 99_000, 1_300, "SYNTH-44302", 0.12, 0.12, "COLONIAL", "3", "renovated", ""),
        ("109 Fixture St", date(2026, 9, 1), 325, 1_300, "SYNTH-44302", 0.14, 0.14, "COLONIAL", "3", "renovated", ""),
        # a 2-bed: fails the bed floor for a 3-bed subject
        ("110 Fixture St", date(2026, 7, 15), 150_000, 1_320, "SYNTH-44302", 0.20, 0.05, "COLONIAL", "2", "renovated", ""),
        # distressed: may inform the as-is floor, never the ARV
        ("111 Fixture St", date(2026, 8, 20), 55_000, 1_400, "SYNTH-44302", 0.25, 0.05, "COLONIAL", "3", "distressed", ""),
        # a mansion-tier restoration carrying an absurd $/sf
        ("112 Fixture St", date(2026, 8, 25), 330_000, 1_500, "SYNTH-44302", 0.15, 0.02, "COLONIAL", "5", "renovated", ""),
    ]
    comps = []
    for addr, sold, price, sqft, hood, dlat, dlon, style, beds, cond, excl in base:
        comps.append(Comp(address=addr, sold=sold, price=float(price), sqft=float(sqft),
                          hood=hood, lat=subject["lat"] + dlat / 69.0,
                          lon=subject["lon"] + dlon / (69.0 * math.cos(math.radians(subject["lat"]))),
                          style=style, beds=beds, condition=cond, exclusion=excl))
    return comps


def selftest() -> int:
    print("SELFTEST - SYNTHETIC fixture data. Not a lead list. Not an offer.\n")
    subject = _fixture_subject()
    comps = _fixture_comps(subject)
    result = compute_arv(subject["sqft"], subject["hood"], subject["lat"], subject["lon"],
                         subject["style"], comps, subject["as_of"], subject["window_days"],
                         subject_beds=subject["beds_n"])

    print(f"  universe drops: {result.rejected}")
    print(f"  excluded in radius: {[c.address for c in result.excluded_in_radius]}")
    print(f"  non-renovated dropped: {[c.address for c in result.non_renovated]}")
    print(f"  outliers dropped: {[c.address for c in result.outliers]}")
    print(f"  chosen: {[(c.address, f'${c.ppsf:.0f}/sf', c.beds) for c in result.chosen]}")
    print(f"  ARV ${result.arv_low:,} / ${result.arv_point:,} / ${result.arv_high:,} "
          f"(low/point/high)")
    print(f"  underwriting to {result.underwrite_to} = ${result.arv:,}  n={result.n}  "
          f"radius {result.radius} mi  {result.confidence}\n")

    row = Priced(subject=subject, result=result)
    failures = 0
    for label, ok, detail in run_checks(row):
        print(f"  {'PASS' if ok else 'FAIL'}  {label}  [{detail}]")
        failures += 0 if ok else 1
    print(f"\n  {len(CHECKS) - failures}/{len(CHECKS)} checks PASS on the healthy fixture")

    def mutate(name: str) -> Priced:
        import copy
        local = copy.deepcopy(comps)          # never mutate the shared fixture
        r = compute_arv(subject["sqft"], subject["hood"], subject["lat"], subject["lon"],
                        subject["style"], local, subject["as_of"], subject["window_days"],
                        subject_beds=subject["beds_n"])
        s = dict(subject)
        if name == "cross_neighbourhood":
            r.chosen[0].hood = "SYNTH-99999"
        elif name == "too_few_comps":
            r.chosen = r.chosen[:2]
            r.n = 2
        elif name == "beyond_radius":
            far = Comp("999 Far St", date(2026, 8, 1), 150_000, 1_600, subject["hood"],
                       subject["lat"] + 2.5 / 69.0, subject["lon"], "COLONIAL", "3",
                       "renovated")
            r.chosen = r.chosen + [far]
            r.n = len(r.chosen)
            r.radius = 2.50
        elif name == "stale_comp":
            r.chosen[0].sold = date(2023, 1, 1)
        elif name == "invented_arv":
            blank = CompResult(status=STATUS_NONE, hood=subject["hood"])
            blank.arv = 128_000
            blank.basis = "felt right"
            return Priced(subject=s, result=blank)
        elif name == "ungraded_repairs":
            return Priced(subject=s, result=r, repairs=55_000, ceiling=20_000,
                          repairs_status="UNGRADED")
        elif name == "below_bed_floor":
            r.chosen = list(r.chosen)
            r.chosen[0] = Comp("2bed Comp", date(2026, 8, 1), 100_000, 1_300,
                               subject["hood"], subject["lat"], subject["lon"],
                               "COLONIAL", "2", "renovated")
        elif name == "distressed_in_pool":
            r.chosen = list(r.chosen)
            r.chosen[0] = Comp("Auction Sale", date(2026, 8, 1), 60_000, 1_300,
                               subject["hood"], subject["lat"], subject["lon"],
                               "COLONIAL", "3", "distressed")
        elif name == "price_gap":
            r.chosen = list(r.chosen)
            r.chosen[0] = Comp("Junk Sale", date(2026, 8, 1), 40_000, 1_400,
                               subject["hood"], subject["lat"], subject["lon"],
                               "COLONIAL", "3", "renovated")
        return Priced(subject=s, result=r)

    mutations = [("cross_neighbourhood", 0), ("too_few_comps", 1), ("beyond_radius", 2),
                 ("stale_comp", 3), ("invented_arv", 4), ("ungraded_repairs", 5),
                 ("below_bed_floor", 6), ("distressed_in_pool", 7), ("price_gap", 8)]
    print("\n  Mutation test - one deliberate defect per check:")
    proven = 0
    for name, target in mutations:
        label, ok, detail = run_checks(mutate(name))[target]
        proven += 1 if not ok else 0
        print(f"  {'CAUGHT' if not ok else 'MISSED'}  {name} -> {label}  [{detail}]")
    print(f"\n  {proven}/{len(CHECKS)} checks proven able to fail")

    # -- the ladder's own refusals -----------------------------------------
    print("\n  Refusal tests (the ladder must say no):")
    only_dated = [c for c in comps if c.condition != "renovated"]
    r = compute_arv(subject["sqft"], subject["hood"], subject["lat"], subject["lon"],
                    subject["style"], only_dated, subject["as_of"], subject_beds=3)
    ok = r.status == STATUS_NONE and r.arv is None
    print(f"  {'PASS' if ok else 'FAIL'}  no renovated comps -> {r.status}, no ARV")
    failures += 0 if ok else 1

    five_bed = [c for c in comps if c.beds_n is not None and c.beds_n < 4]
    r = compute_arv(subject["sqft"], subject["hood"], subject["lat"], subject["lon"],
                    subject["style"], five_bed, subject["as_of"], subject_beds=4)
    ok = r.status == STATUS_NONE
    print(f"  {'PASS' if ok else 'FAIL'}  4-bed subject with only 3-bed comps -> "
          f"{r.status} (bed floor cannot be met)")
    failures += 0 if ok else 1

    print("\n  Repair tiers:")
    for t in ("light", "moderate", "heavy"):
        lo, pt, hi = repair_range(1642, t)
        print(f"    {t:9} ${lo:,} / ${pt:,} / ${hi:,}  (${REPAIR_TIERS[t]}/sf)")

    # -- MAO per ARV tier --------------------------------------------------
    print("\n  MAO by ARV tier at $65,000 repairs (Step 9):")
    for label, v in mao_by_tier(result, 65_000).items():
        print(f"    ARV {label:5} ${result.tier(label):>8,}  ->  MAO ${v:>8,}")

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
        bad = {k: (expect[k], got[k]) for k in expect if got[k] != expect[k]}
        line = (f"${arv:,} ARV / ${repairs:,} repairs -> ceiling "
                f"${got['CEILING (0.70 x ARV - repairs)']:,}")
        if bad:
            econ_ok = False
            line += f"   MISMATCH {bad}"
        print(f"  {'PASS' if not bad else 'FAIL'}  {line}")

    ok = (failures == 0) and (proven == len(CHECKS)) and econ_ok
    print("\nPASS  all checks green, all mutations caught, economics reproduce"
          if ok else "\nFAIL  something above is broken - do not quote a number")
    return 0 if ok else 1


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def cmd_arv(args) -> int:
    subject = json.loads(args.subject)
    as_of = date.fromisoformat(args.as_of) if args.as_of else date.today()
    window = args.window
    comps = load_comps(args.comps, as_of)
    beds = beds_num(subject.get("beds"))
    result = compute_arv(subject["sqft"], subject["hood"], subject["lat"], subject["lon"],
                         (subject.get("style") or "").upper(), comps, as_of, window,
                         subject_beds=beds)

    print(f"SUBJECT  {subject.get('address', '(unnamed)')}  "
          f"{subject.get('beds', '?')}  {int(subject['sqft']):,} sf  {subject['hood']}")
    print(f"WINDOW   {window} days to {as_of.isoformat()}\n")

    if result.chosen:
        print(f"{'COMP':22} {'SOLD':11} {'PRICE':>10} {'SQFT':>6} {'$/SF':>6} "
              f"{'BD':>3} {'COND':>10} {'MI':>5}")
        for c in result.chosen:
            d = miles(subject["lat"], subject["lon"], c.lat, c.lon)
            print(f"{c.address[:22]:22} {c.sold.isoformat():11} ${c.price:>9,.0f} "
                  f"{int(c.sqft):>6,} ${c.ppsf:>5.0f} {c.beds:>3} "
                  f"{c.condition or 'unknown':>10} {d:>5.2f}")
    if result.excluded_in_radius:
        print("\nEXCLUDED (in radius, not in the maths):")
        for c in result.excluded_in_radius:
            print(f"  {c.address[:24]:24} ${c.price:>9,.0f}  "
                  f"{EXCLUSION_REASONS.get(c.exclusion, c.exclusion)}")
    if result.non_renovated:
        print("\nDROPPED - not renovated (as-is floor only, never ARV):")
        for c in result.non_renovated:
            print(f"  {c.address[:24]:24} ${c.price:>9,.0f}  "
                  f"{c.condition or 'unknown'}")
    if result.outliers:
        print("\nDROPPED - illogical price gap:")
        for c in result.outliers:
            print(f"  {c.address[:24]:24} ${c.price:>9,.0f}  ${c.ppsf:>5.0f}/sf")
    if result.rejected:
        print(f"\nUNIVERSE / FILTER DROPS  {result.rejected}")

    print()
    if result.status == STATUS_PRICED:
        print(f"ARV LOW    ${result.arv_low:>9,}")
        print(f"ARV POINT  ${result.arv_point:>9,}")
        print(f"ARV HIGH   ${result.arv_high:>9,}")
        print(f"UNDERWRITE {result.underwrite_to} = ${result.arv:,}")
        print(f"AS-IS      ${result.as_is:>9,}   (p25 - never shown as ARV)")
        print(f"CONF       {result.confidence}  n={result.n}  radius {result.radius} mi")
        print(f"BASIS      {result.basis}")
        if args.repairs is not None:
            print("\nMAO BY TIER (Step 9: (ARV x 0.70) - repairs)")
            for label, v in mao_by_tier(result, args.repairs).items():
                mark = "  <- underwrite here" if label == result.underwrite_to else ""
                print(f"  ARV {label:5} ${result.tier(label):>9,}  ->  MAO ${v:>9,}{mark}")
            e = economics(result.arv, args.repairs)
            print(f"\n  CEILING at {result.underwrite_to}  ${e['CEILING (0.70 x ARV - repairs)']:,}")
            print(f"  OFFER LOW (0.55)    ${e['OFFER LOW (0.55)']:,}")
            print(f"  OFFER HIGH (0.60)   ${e['OFFER HIGH (0.60)']:,}")
            print(f"  CONTRACT for fee    ${e['CONTRACT FOR $10K FEE']:,}")
        elif args.tier:
            lo, pt, hi = repair_range(subject["sqft"], args.tier)
            print(f"\nREPAIRS ({args.tier})  ${lo:,} / ${pt:,} / ${hi:,} "
                  f"(${REPAIR_TIERS[args.tier]}/sf)")
            print("  Re-run with --repairs to get MAO per tier.")
        else:
            print("REPAIRS  UNGRADED - no ceiling quoted. Pass --tier or --repairs.")
    else:
        print(f"ARV      {STATUS_NONE} - {result.note}")
        print("         Unpriced is a complete answer. Do not quote a number.")

    row = Priced(subject={**subject, "as_of": as_of, "window_days": window,
                          "beds_n": beds},
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
    if fails:
        return 1
    return 0 if result.status == STATUS_PRICED else 3


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
    print("\n70% is a cap, 55-60% is the target, the gap is the pay stack.")
    print("Fee deducted once, at the contract step. ESTIMATE - not an offer.")
    return 0


def cmd_tiers(_args) -> int:
    print("REPAIR TIERS (references/repairs.md) - $/sqft of living area\n")
    print(f"  {'tier':10}{'$/sf':>6}   {'1,200 sf':>10}{'1,642 sf':>10}{'2,000 sf':>10}")
    for t, rate in REPAIR_TIERS.items():
        row = "".join(f"{repair_cost(s, t):>10,}" for s in (1200, 1642, 2000))
        note = "  <- placeholder when condition is unconfirmed" if t == "moderate" else ""
        print(f"  {t:10}{rate:>6}{row}{note}")
    print("\n  A range is +-15% around the tier. Systems that cannot be verified")
    print("  take a separate allowance (references/repairs.md), not a bigger tier.")
    return 0


def cmd_exclusions(_args) -> int:
    print("EXCLUSIONS - a sale that matches one of these is not an ARV comp:\n")
    for key, why in EXCLUSION_REASONS.items():
        print(f"  {key:16} {why}")
    print("\nAlso excluded, by rule:")
    print("  - a comp with FEWER beds than the subject (no exceptions, no matter the $/sf)")
    print("  - anything not in renovated condition (dated/distressed/unknown)")
    print("  - a comp sitting an illogical distance from the comp-set median $/sf")
    print("  - asking prices (never a comp)")
    print("  - cross-ZIP bracketing when no same-area sale exists")
    print("  - anything that forces widening past 1.5 mi to reach 3 comps")
    print("\nIf <3 comps survive: UNPRICED. That is the answer.")
    return 0


def main(argv=None) -> int:
    p = argparse.ArgumentParser(description="Comping + ARV engine. See comping/COMPING.md")
    p.add_argument("--selftest", action="store_true")
    p.add_argument("--exclusions", action="store_true")
    p.add_argument("--repair-tiers", action="store_true")
    p.add_argument("--offer", type=float, help="ARV, for the economics model")
    p.add_argument("--repairs", type=float, help="graded repairs, in dollars")
    p.add_argument("--tier", choices=list(REPAIR_TIERS),
                   help="repair tier, to size repairs from $/sf")
    p.add_argument("--ask", type=float)
    p.add_argument("--comps")
    p.add_argument("--subject")
    p.add_argument("--as-of")
    p.add_argument("--window", type=int, default=180)
    a = p.parse_args(argv)

    if a.selftest:
        return selftest()
    if a.exclusions:
        return cmd_exclusions(a)
    if a.repair_tiers:
        return cmd_tiers(a)
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
