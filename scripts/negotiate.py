#!/usr/bin/env python3
"""
negotiate.py - the pre-call gate. Standard library only.

The research says the strongest determinant of a negotiated outcome is your
BATNA and your written reservation, not your technique. So the machine refuses
to print a talk track until they exist.

Nothing here invents a number. If you have no ARV from comp.py, there is no
number, and the gate says so.

Usage:
    python3 scripts/negotiate.py --check --target 62000 --reservation 69239 \
        --batna "two 43204 leads at gate stage" --their-batna "retail listing net ~71K" \
        --deadline "taxes due Nov 30" --trades "closing 12 days; cash as-is; your timeline"

    python3 scripts/negotiate.py --selftest
"""

from __future__ import annotations

import argparse
import sys

MIN_BATNA_WORDS = 3
PLACEHOLDERS = {"unknown", "n/a", "na", "none", "tbd", "?", "-", "x"}
# A BATNA that just restates the deal is not an alternative.
NON_ALTERNATIVES = ("this deal", "this house", "this property", "nothing", "wait")


def _bad(text: str) -> bool:
    t = (text or "").strip().lower()
    if len(t.split()) < MIN_BATNA_WORDS:
        return True
    if t in PLACEHOLDERS:
        return True
    return any(t.startswith(p) for p in NON_ALTERNATIVES)


def check(target, reservation, batna, their_batna, deadline, trades) -> dict:
    problems = []

    # --- the arithmetic order: target is what you want, reservation is the wall.
    if target is None or reservation is None:
        problems.append("target and reservation are both required")
    elif target > reservation:
        problems.append(
            f"target ${target:,} is above reservation ${reservation:,} - "
            "you would be negotiating past your own walk-away")
    elif target == reservation:
        problems.append("target equals reservation - no room to concede, nothing to trade")

    # --- no BATNA, no conversation
    if _bad(batna):
        problems.append(
            "BATNA missing or a restatement of this deal. Name a real alternative "
            "property or course of action, or you are not ready to talk.")
    if _bad(their_batna):
        problems.append(
            "their BATNA is missing. Anchoring research: focusing on THEIR "
            "alternatives is one of the three focuses that removes the first-offer "
            "advantage aimed at you. You cannot skip it.")

    if not (deadline or "").strip():
        problems.append("their deadline unknown - ask 'when do you need to be out?'")

    trade_list = [t.strip() for t in (trades or "").split(";") if t.strip()]
    if len(trade_list) < 3:
        problems.append(
            f"only {len(trade_list)} trade variable(s). Name at least 3 non-price "
            "variables (closing date, earnest money, repairs, possession, financing).")

    return {"ok": not problems, "problems": problems,
            "trades": trade_list,
            "room": (reservation - target) if (target and reservation) else None}


def talk_track(target: int, reservation: int, trades: list) -> list:
    """The opening lines. Printed only after the gate passes."""
    return [
        "1. EVIDENCE FIRST  - 'Here are the five closed sales and the repair range. "
        "That's what the house is worth after work.'",
        "2. INTEREST        - 'Where are you going next? / When do you need to be out?'",
        f"3. ANCHOR          - one precise number at ${target:,}, one sentence of why, "
        "then silence. Do not speak into the gap.",
        "4. ANCHOR DEFENCE  - if they open high, do not counter immediately. Focus on "
        "their alternatives, their walk-away, and your written target.",
        "5. TRADE           - every counter gets a question, then a trade from: "
        + "; ".join(trades),
        f"6. THE WALL        - beyond ${reservation:,} say so plainly and leave the "
        "relationship open. A clean no is worth more than a thin yes.",
        "7. SAME DAY        - write the summary first. The drafter frames the ambiguity.",
    ]


def render(res: dict, target, reservation) -> str:
    out = []
    if not res["ok"]:
        out.append("NO TALK TRACK - the gate failed:")
        for p in res["problems"]:
            out.append(f"  [BLOCKED] {p}")
        out.append("")
        out.append("This is not a formatting problem. Starting a seller call without a "
                   "written BATNA is the single most expensive thing you can do.")
        return "\n".join(out)
    out.append(f"GATE PASSED. Room to trade: ${res['room']:,} "
               f"(${target:,} -> ${reservation:,}).")
    out.append("PRELIMINARY - not an offer. Everything said on the call is subject to "
               "the comps and the contract.")
    out.append("")
    out.extend(talk_track(target, reservation, res["trades"]))
    return "\n".join(out)


CHECKS = [
    # (target, reservation, batna, their_batna, deadline, trades, expect_ok, why)
    (62000, 69239, "two 43204 leads at gate stage", "retail listing net ~71K",
     "taxes due Nov 30", "closing 12 days; cash as-is; your timeline", True, "complete"),
    (62000, 69239, "unknown", "retail listing net ~71K",
     "taxes due Nov 30", "closing 12 days; cash as-is; your timeline", False, "no BATNA"),
    (62000, 69239, "nothing", "retail listing net ~71K",
     "taxes due Nov 30", "closing 12 days; cash as-is; your timeline", False, "fake BATNA"),
    (72000, 69239, "two 43204 leads at gate stage", "retail listing net ~71K",
     "taxes due Nov 30", "closing 12 days; cash as-is; your timeline", False,
     "target above reservation"),
    (62000, 69239, "two 43204 leads at gate stage", "retail listing net ~71K",
     "taxes due Nov 30", "closing 12 days", False, "fewer than 3 trades"),
    (62000, 69239, "two 43204 leads at gate stage", "retail listing net ~71K",
     "", "closing 12 days; cash as-is; your timeline", False, "no deadline"),
]


def selftest() -> int:
    bad = 0
    for t, r, b, tb, d, tr, want, why in CHECKS:
        got = check(t, r, b, tb, d, tr)["ok"]
        if got != want:
            print(f"  [FAIL] {why}: expected ok={want}, got {got}")
            bad += 1
        else:
            print(f"  [ok]   {why}")
    print("SELFTEST PASSED" if not bad else f"SELFTEST FAILED ({bad})")
    return 1 if bad else 0


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="pre-call negotiation gate")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--target", type=int)
    ap.add_argument("--reservation", type=int)
    ap.add_argument("--batna")
    ap.add_argument("--their-batna")
    ap.add_argument("--deadline")
    ap.add_argument("--trades")
    a = ap.parse_args(argv)

    if a.selftest:
        return selftest()
    if not a.check:
        ap.error("use --check (with the six fields) or --selftest")

    res = check(a.target, a.reservation, a.batna, a.their_batna, a.deadline, a.trades)
    print(render(res, a.target, a.reservation))
    return 0 if res["ok"] else 2


if __name__ == "__main__":
    sys.exit(main())
