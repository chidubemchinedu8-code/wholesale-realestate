#!/usr/bin/env python3
"""
gate.py - the 15-point qualification gate, executable. Standard library only.

Feeds each check an explicit PASS/FAIL/UNKNOWN plus its evidence, then decides the
verdict mechanically so a deal cannot be talked into "strong" by prose.

Usage:
    python3 scripts/gate.py --selftest
    python3 scripts/gate.py --from-json deal.json      # see assets/deal_template.json
    python3 scripts/gate.py --checks G05=pass,G06=pass,G12=unknown --missing 2
"""

from __future__ import annotations

import argparse
import json
import sys

# code -> (check text, is it a hard blocker for STRONG?)
GATES = [
    ("G01", "Within an intended market and property type", False),
    ("G02", "Listing or ownership information credible", False),
    ("G03", "Asking price potentially negotiable", False),
    ("G04", "Evidence of an actual discount opportunity", False),
    ("G05", "Five credible sold comps", True),
    ("G06", "ARV supported by those comps", True),
    ("G07", "Repair estimate defensible", True),
    ("G08", "Buyer-side arithmetic works", True),
    ("G09", "Seller MAO leaves room for the assignment fee", False),
    ("G10", "Asking at or below MAO, or a credible negotiation path", False),
    ("G11", "Buyer spread sufficient after other costs", False),
    ("G12", "Condition verifiable adequately", False),
    ("G13", "Current photos or a walkthrough obtainable", False),
    ("G14", "Transaction timeline realistic (21-30 day close)", False),
    ("G15", "No title/occupancy/access/legal due-diligence red flag", False),
]
HARD_BLOCKERS = {c for c, _t, hard in GATES if hard}
VERDICTS = ("STRONG OPPORTUNITY", "POTENTIAL OPPORTUNITY", "REJECT")


MIN_PASSES_TO_BE_POTENTIAL = 8


def verdict(checks: dict[str, str]) -> tuple[str, list[str]]:
    """checks: {'G01': 'pass'|'fail'|'unknown', ...}. Missing == unknown.

    REJECT when the deal cannot be underwritten at all, when a hard blocker fails,
    or when there is no evidence of any discount to chase. POTENTIAL when the deal
    is real but something important is unverified. STRONG only when all fifteen pass.
    """
    passed, failed, unknown = [], [], []
    for code, _text, _hard in GATES:
        state = str(checks.get(code, "unknown")).lower()
        if state == "pass":
            passed.append(code)
        elif state == "fail":
            failed.append(code)
        else:
            unknown.append(code)

    open_and_failed = sorted(set(failed) | set(unknown))

    # 1. A failed hard blocker is a rejection on its face: no comps, no supported
    #    ARV, indefensible repairs, or buyer maths that does not work.
    hard_failed = [c for c in failed if c in HARD_BLOCKERS]
    if hard_failed:
        return "REJECT", hard_failed

    # 2. Three or more outright failures is a rejected deal, not a gap to close.
    if len(failed) >= 3:
        return "REJECT", failed

    # 3. Market identity failing is a rejection: wrong product, wrong place, or a
    #    listing whose own facts do not hold up.
    identity_failed = [c for c in failed if c in ("G01", "G02")]
    if identity_failed:
        return "REJECT", identity_failed

    # 4. No evidence of any discount anywhere is a rejection, not a research task.
    #    Turnkey retail at market price sits here: there is nothing to chase.
    could_be_negotiable = str(checks.get("G03", "unknown")).lower() == "pass"
    discount_evidence = str(checks.get("G04", "unknown")).lower() == "pass"
    if not (could_be_negotiable or discount_evidence):
        return "REJECT", open_and_failed

    # 5. Too little established to underwrite responsibly.
    if len(passed) < MIN_PASSES_TO_BE_POTENTIAL:
        return "REJECT", open_and_failed

    if failed or unknown:
        return "POTENTIAL OPPORTUNITY", open_and_failed
    return "STRONG OPPORTUNITY", []


def reasons_for(codes: list[str], checks: dict[str, str]) -> list[str]:
    out = []
    for c in codes:
        text = next(t for code, t, _h in GATES if code == c)
        state = str(checks.get(c, "unknown")).lower()
        out.append(f"{c} {text} [{state}]")
    return out


def selftest() -> int:
    fails = 0
    print("GATE SELFTEST\n")

    def case(name, checks, expect):
        nonlocal fails
        v, codes = verdict(checks)
        ok = v == expect
        print(f"  {'PASS' if ok else 'FAIL'}  {name} -> {v}"
              + (f"  open/failed: {','.join(codes)}" if codes else ""))
        if not ok:
            print(f"        EXPECTED {expect}")
            fails += 1

    allpass = {c: "pass" for c, _t, _h in GATES}
    case("all fifteen pass", allpass, "STRONG OPPORTUNITY")

    # Test 4: insufficient comps - must not become strong, must be REJECT
    three_comps = {**allpass, "G05": "fail", "G06": "fail"}
    case("only three comps", three_comps, "REJECT")

    # one hard blocker failing
    case("repairs indefensible", {**allpass, "G07": "fail"}, "REJECT")

    # photos missing is a gap, not a rejection
    case("no interior photos yet", {**allpass, "G12": "unknown", "G13": "unknown"},
         "POTENTIAL OPPORTUNITY")

    # seller MAO does not clear asking but there is a path
    case("MAO below asking, path plausible", {**allpass, "G10": "unknown"},
         "POTENTIAL OPPORTUNITY")

    # Test 2: new listing, retail, turnkey -> multiple failures
    retail = {**allpass, "G03": "fail", "G04": "fail", "G09": "fail", "G10": "fail",
              "G11": "fail"}
    case("newly listed retail turnkey", retail, "REJECT")

    # many soft gaps still is a rejection
    case("six soft failures", {**allpass, "G01": "unknown", "G02": "unknown",
                               "G03": "unknown", "G04": "unknown", "G09": "unknown",
                               "G10": "unknown"}, "REJECT")

    # empty input must never be strong
    case("nothing supplied", {}, "REJECT")

    # negative controls: a gate that rejects everything is as useless as one
    # that accepts everything. A real deal with one soft gap must survive.
    case("clean deal, agent phone not yet called",
         {**allpass, "G14": "unknown"}, "POTENTIAL OPPORTUNITY")
    case("clean deal, title check outstanding",
         {**allpass, "G15": "unknown"}, "POTENTIAL OPPORTUNITY")
    case("clean deal, one soft failure (G11 spread thin)",
         {**allpass, "G11": "fail"}, "POTENTIAL OPPORTUNITY")

    print("\n" + ("PASS  gate behaves" if fails == 0 else "FAIL  gate wrong"))
    return 0 if fails == 0 else 1


def main(argv=None) -> int:
    p = argparse.ArgumentParser(description="15-point qualification gate")
    p.add_argument("--selftest", action="store_true")
    p.add_argument("--from-json", help="JSON with {address, checks:{G01:pass,...}}")
    p.add_argument("--checks", help="comma list: G05=pass,G06=fail")
    p.add_argument("--address", default="")
    a = p.parse_args(argv)

    if a.selftest:
        return selftest()

    checks, address = {}, a.address
    if a.from_json:
        with open(a.from_json, encoding="utf-8") as fh:
            payload = json.load(fh)
        checks = payload.get("checks", {})
        address = payload.get("address", address)
    elif a.checks:
        for pair in a.checks.split(","):
            if "=" not in pair:
                continue
            k, v = pair.split("=", 1)
            checks[k.strip().upper()] = v.strip().lower()
    else:
        p.print_help()
        return 0

    v, codes = verdict(checks)
    print(f"{address or 'property'}: {v}")
    for code, text, hard in GATES:
        state = str(checks.get(code, "unknown")).lower()
        mark = {"pass": "PASS", "fail": "FAIL"}.get(state, "????")
        flag = " (hard)" if hard else ""
        print(f"  {mark}  {code} {text}{flag}")
    if codes:
        print("\nOpen or failed:")
        for line in reasons_for(codes, checks):
            print(f"  - {line}")
        if v == "POTENTIAL OPPORTUNITY":
            print("\nNot submittable. Close the codes above, then re-run.")
        else:
            print("\nRejection reason(s) above. This is a successful outcome.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
