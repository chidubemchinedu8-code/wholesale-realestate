#!/usr/bin/env python3
"""
zip_ledger.py - ZIP scan ledger + property ledger. Standard library only.

Keeps the scan honest across sessions: what was scanned, when, what it produced,
and which properties have already been seen (so nothing is reported as new twice).

Ledgers live in state/ (gitignored). Commit assets/zip_universe.csv instead.

Usage:
    python3 scripts/zip_ledger.py --log --city Akron --zip 44302 --score 78 \
        --category A --qualifying 3 --potential 5 --rejected 41 \
        --best "156 Colony Cres POTENTIAL"
    python3 scripts/zip_ledger.py --list
    python3 scripts/zip_ledger.py --due
    python3 scripts/zip_ledger.py --check "141 Grand Ave" --city Akron --zip 44302
    python3 scripts/zip_ledger.py --selftest
"""

from __future__ import annotations

import argparse
import csv
import re
import os
import sys
from datetime import date, datetime, timedelta

HERE = os.path.dirname(os.path.abspath(__file__))
SKILL_ROOT = os.path.dirname(HERE)
STATE = os.path.join(SKILL_ROOT, "state")
ZIP_LEDGER = os.path.join(STATE, "zip_ledger.csv")
PROP_LEDGER = os.path.join(STATE, "property_ledger.csv")

ZIP_FIELDS = ["city", "zip", "priority_score", "priority_category", "evidence",
              "scanned", "last_scan_date", "qualifying_count", "potential_count",
              "rejected_count", "rejection_reasons", "best_opportunity", "revisit",
              "notes"]
PROP_FIELDS = ["address", "city", "zip", "first_seen", "last_seen", "channel",
               "status", "last_verdict", "last_price", "last_scan_date", "notes"]

CADENCE_DAYS = {"A": 7, "B": 14, "C": 30}


def _ensure(path: str, fields: list[str]) -> None:
    os.makedirs(STATE, exist_ok=True)
    if not os.path.exists(path):
        with open(path, "w", newline="", encoding="utf-8") as fh:
            csv.DictWriter(fh, fieldnames=fields).writeheader()


def _read(path: str, fields: list[str]) -> list[dict]:
    _ensure(path, fields)
    with open(path, newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def _write(path: str, fields: list[str], rows: list[dict]) -> None:
    os.makedirs(STATE, exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=fields)
        w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k, "") for k in fields})


def category_for(score: int) -> str:
    if score >= 75:
        return "A"
    if score >= 60:
        return "B"
    return "C"


def log_zip(city, zip5, score, category, qualifying, potential, rejected,
            best="", reasons="", evidence="", notes="", today=None) -> dict:
    today = today or date.today()
    rows = _read(ZIP_LEDGER, ZIP_FIELDS)
    row = next((r for r in rows if r["zip"] == str(zip5)), None)
    if row is None:
        row = {k: "" for k in ZIP_FIELDS}
        row["zip"] = str(zip5)
        row["first_seen"] = str(today)
        rows.append(row)
    row.update({
        "city": city or row.get("city", ""),
        "priority_score": str(score),
        "priority_category": category or category_for(score),
        "evidence": evidence or row.get("evidence", ""),
        "scanned": "yes",
        "last_scan_date": str(today),
        "qualifying_count": str(qualifying),
        "potential_count": str(potential),
        "rejected_count": str(rejected),
        "rejection_reasons": reasons,
        "best_opportunity": best or "none",
        "revisit": "no",
        "notes": notes,
    })
    _write(ZIP_LEDGER, ZIP_FIELDS, rows)
    return row


def due_list(today=None) -> list[dict]:
    today = today or date.today()
    out = []
    for r in _read(ZIP_LEDGER, ZIP_FIELDS):
        cat = r.get("priority_category") or "C"
        if cat not in CADENCE_DAYS:
            continue
        last = r.get("last_scan_date") or ""
        try:
            last_d = datetime.strptime(last, "%Y-%m-%d").date()
        except ValueError:
            out.append({**r, "_due_in": "never scanned"})
            continue
        due_on = last_d + timedelta(days=CADENCE_DAYS[cat])
        if today >= due_on:
            out.append({**r, "_due_in": f"due {(today - due_on).days}d ago"})
    out.sort(key=lambda r: (-int(r["priority_score"] or 0)))
    return out


_SUFFIX = {
    "avenue": "ave", "av": "ave", "street": "st", "str": "st", "drive": "dr",
    "road": "rd", "lane": "ln", "court": "ct", "place": "pl", "boulevard": "blvd",
    "terrace": "ter", "trail": "trl", "parkway": "pkwy", "circle": "cir",
    "highway": "hwy", "square": "sq", "north": "n", "south": "s", "east": "e",
    "west": "w", "northeast": "ne", "northwest": "nw", "southeast": "se",
    "southwest": "sw", "mount": "mt", "fort": "ft", "first": "1st", "second": "2nd",
    "third": "3rd",
}
_SUFFIXES = {"ave", "st", "dr", "rd", "ln", "ct", "pl", "blvd", "ter", "trl",
             "pkwy", "cir", "hwy", "sq", "way", "aly", "loop", "path"}
_DIRECTIONALS = {"n", "s", "e", "w", "ne", "nw", "se", "sw"}
# Unit designators are stripped entirely: the ledger keys on the parcel, and
# "Apt 3" must not make the same house look new.
_UNIT = re.compile(r"\b(apt|apartment|unit|ste|suite|bldg|floor|fl|rm|room)\b\.?\s*[a-z0-9-]*")
_STATES = {"oh", "ohio", "al", "alabama", "ga", "georgia", "mi", "michigan",
           "pa", "pennsylvania", "wv", "west", "virginia"}


def normalise_address(address: str, city: str = "") -> str:
    """Canonical key for the duplicate guard.

    Portals disagree on 'Ave'/'Avenue', 'N'/'North', trailing ', Akron OH 44302',
    punctuation and spacing. Two spellings of one parcel must not read as two
    opportunities, so the key is structural: house number + street core.
    Suffixes, directionals, unit designators, city, state and zip are folded
    away because none of them change which parcel it is.
    """
    s = (address or "").lower().replace(".", " ").replace(",", " ")
    s = re.sub(r"#\s*[a-z0-9-]+", " ", s)
    s = _UNIT.sub(" ", s)
    s = re.sub(r"\s+", " ", s).strip()
    city_tokens = set(normalise_plain(city).split()) if city else set()
    tokens = []
    for raw in s.split():
        t = _SUFFIX.get(raw, raw)         # canonicalise FIRST, then test
        if t in _SUFFIXES or t in _DIRECTIONALS:
            continue                      # suffix/direction never identifies a parcel
        if t in _STATES or t in city_tokens:
            continue                      # city/state block adds nothing
        if re.fullmatch(r"\d{5}(-\d{4})?", t):
            continue                      # zip lives in its own column
        tokens.append(t)
    return " ".join(tokens)


def normalise_plain(value: str) -> str:
    s = (value or "").lower().replace(".", " ").replace(",", " ")
    s = re.sub(r"\s+", " ", s).strip()
    return " ".join(_SUFFIX.get(t, t) for t in s.split())


def _same_property(a_key: str, other_address: str, city: str = "") -> bool:
    b_key = normalise_address(other_address, city)
    if not a_key or not b_key:
        return False
    if a_key == b_key:
        return True
    # Real-world typos ('Amelia' vs 'Amelie'): the HOUSE NUMBER must match
    # exactly and the street core must be very close. House numbers are never
    # fuzzy-matched - '1410 Grand' is a different parcel from '141 Grand', and a
    # false SEEN hides a real new lead, which is worse than a duplicate.
    a_t, b_t = a_key.split(), b_key.split()
    if a_t[0] != b_t[0]:
        return False
    from difflib import SequenceMatcher
    return SequenceMatcher(None, " ".join(a_t[1:]),
                           " ".join(b_t[1:])).ratio() >= 0.88


def check_property(address: str, city: str = "", zip5: str = "") -> dict:
    """Returns {'seen': bool, 'row': dict|None} - the duplicate guard."""
    rows = _read(PROP_LEDGER, PROP_FIELDS)
    a = normalise_address(address, city)
    for r in rows:
        if _same_property(a, r["address"], city):
            if city and r["city"].strip().lower() != city.strip().lower():
                continue
            return {"seen": True, "row": r}
    return {"seen": False, "row": None}


def log_property(address, city, zip5, channel, status, verdict, price="",
                 notes="", today=None) -> dict:
    today = today or date.today()
    rows = _read(PROP_LEDGER, PROP_FIELDS)
    found = check_property(address, city, zip5)
    row = found["row"]
    if row is None:
        row = {k: "" for k in PROP_FIELDS}
        row["address"] = address
        row["first_seen"] = str(today)
        rows.append(row)
    row.update({
        "city": city, "zip": str(zip5), "channel": channel, "status": status,
        "last_verdict": verdict, "last_price": str(price),
        "last_scan_date": str(today), "last_seen": str(today), "notes": notes,
    })
    _write(PROP_LEDGER, PROP_FIELDS, rows)
    return row


def selftest() -> int:
    """Prove the duplicate guard and the cadence both work, in a temp state dir."""
    global STATE, ZIP_LEDGER, PROP_LEDGER
    import tempfile
    tmp = tempfile.mkdtemp(prefix="ledger-selftest-")
    STATE = tmp
    ZIP_LEDGER = os.path.join(tmp, "zip_ledger.csv")
    PROP_LEDGER = os.path.join(tmp, "property_ledger.csv")

    fails = 0
    print("LEDGER SELFTEST\n")

    d0 = date(2026, 11, 1)
    log_zip("Akron", 44302, 78, "A", 3, 5, 41,
            best="156 Colony Cres POTENTIAL", today=d0)
    r = check_property("141 Grand Ave", "Akron", 44302)
    print(f"  {'PASS' if not r['seen'] else 'FAIL'}  unknown property is not 'seen'")
    fails += 0 if not r["seen"] else 1

    log_property("141 Grand Ave", "Akron", 44302, "on-market", "active",
                 "REJECT", 95000, today=d0)
    r = check_property("141 Grand Ave", "Akron", 44302)
    print(f"  {'PASS' if r['seen'] else 'FAIL'}  scanned property is recognised "
          f"(first seen {r['row']['first_seen'] if r['row'] else '-'})")
    fails += 0 if r["seen"] else 1

    # case/space insensitivity
    r2 = check_property("  141 GRAND AVE ", "akron", "44302")
    print(f"  {'PASS' if r2['seen'] else 'FAIL'}  match is case/space insensitive")
    fails += 0 if r2["seen"] else 1

    # logging the same property twice must not duplicate the row
    log_property("141 Grand Ave", "Akron", 44302, "on-market", "pending",
                 "REJECT", 92000, today=date(2026, 11, 5))
    n = len(_read(PROP_LEDGER, PROP_FIELDS))
    print(f"  {'PASS' if n == 1 else 'FAIL'}  re-logging updates in place "
          f"({n} row(s), expected 1)")
    fails += 0 if n == 1 else 1

    # category boundary
    print(f"  {'PASS' if category_for(75)=='A' else 'FAIL'}  75 -> A")
    fails += 0 if category_for(75) == "A" else 1
    print(f"  {'PASS' if category_for(74)=='B' else 'FAIL'}  74 -> B")
    fails += 0 if category_for(74) == "B" else 1
    print(f"  {'PASS' if category_for(59)=='C' else 'FAIL'}  59 -> C")
    fails += 0 if category_for(59) == "C" else 1

    # cadence: A due after 7 days, not before
    due = due_list(today=date(2026, 11, 7))
    not_due = len(due) == 0
    print(f"  {'PASS' if not_due else 'FAIL'}  A ZIP not due at 6 days")
    fails += 0 if not_due else 1
    due = due_list(today=date(2026, 11, 8))
    is_due = len(due) == 1
    print(f"  {'PASS' if is_due else 'FAIL'}  A ZIP due at 7 days")
    fails += 0 if is_due else 1

    import shutil
    shutil.rmtree(tmp, ignore_errors=True)
    print("\n" + ("PASS  ledger behaves" if fails == 0 else "FAIL  ledger broken"))
    return 0 if fails == 0 else 1


def main(argv=None) -> int:
    p = argparse.ArgumentParser(description="ZIP and property ledgers")
    p.add_argument("--log", action="store_true")
    p.add_argument("--list", action="store_true")
    p.add_argument("--due", action="store_true")
    p.add_argument("--check")
    p.add_argument("--city", default="")
    p.add_argument("--zip", dest="zip5", default="")
    p.add_argument("--score", type=int)
    p.add_argument("--category", choices=["A", "B", "C"])
    p.add_argument("--qualifying", type=int, default=0)
    p.add_argument("--potential", type=int, default=0)
    p.add_argument("--rejected", type=int, default=0)
    p.add_argument("--reasons", default="")
    p.add_argument("--best", default="")
    p.add_argument("--evidence", default="")
    p.add_argument("--notes", default="")
    p.add_argument("--selftest", action="store_true")
    a = p.parse_args(argv)

    if a.selftest:
        return selftest()
    if a.log:
        if not a.zip5 or a.score is None:
            print("--log needs --zip and --score", file=sys.stderr)
            return 2
        row = log_zip(a.city, a.zip5, a.score, a.category, a.qualifying,
                      a.potential, a.rejected, a.best, a.reasons, a.evidence,
                      a.notes)
        print(f"logged {row['zip']} ({row['priority_category']}, "
              f"score {row['priority_score']}) scanned {row['last_scan_date']}")
        return 0
    if a.check:
        r = check_property(a.check, a.city, a.zip5)
        if r["seen"]:
            row = r["row"]
            print(f"SEEN - first seen {row['first_seen']}, last "
                  f"{row['last_scan_date']}, verdict {row['last_verdict']}, "
                  f"price {row['last_price']}")
            print("Report as SEEN with the change noted. Not a new opportunity.")
        else:
            print("NEW - not in the property ledger")
        return 0
    if a.due:
        rows = due_list()
        if not rows:
            print("nothing due")
            return 0
        print(f"{'ZIP':8}{'CITY':14}{'CAT':5}{'SCORE':6}{'LAST SCAN':13}STATUS")
        for r in rows:
            print(f"{r['zip']:8}{r['city'][:13]:14}{r['priority_category']:5}"
                  f"{r['priority_score']:6}{r['last_scan_date']:13}{r['_due_in']}")
        return 0
    # --list
    rows = _read(ZIP_LEDGER, ZIP_FIELDS)
    if not rows:
        print("ledger empty - nothing scanned yet")
        return 0
    print(f"{'ZIP':8}{'CITY':14}{'CAT':5}{'SCORE':6}{'QUAL':6}{'POT':5}"
          f"{'REJ':5}{'LAST SCAN':12}BEST")
    for r in rows:
        print(f"{r['zip']:8}{r['city'][:13]:14}{r['priority_category']:5}"
              f"{r['priority_score']:6}{r['qualifying_count']:6}"
              f"{r['potential_count']:5}{r['rejected_count']:5}"
              f"{r['last_scan_date']:12}{r['best_opportunity'][:30]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
