#!/usr/bin/env python3
"""
underwrite.py - the buyer/seller arithmetic. Standard library only.

Two numbers, never merged:
    buyer max contract = (ARV x 0.70) - repairs - buyer costs
    seller-facing MAO  = buyer max - assignment fee - wholesaler costs

Default is Mode A: repairs inside the 70% cap, buyer's own profit/closing/holding
assumed to live inside the remaining 30%. --mode-b deducts repairs AND buyer costs,
which is more conservative; the report must say which mode it used.

Usage:
    python3 scripts/underwrite.py --arv 200000 --repairs 25000 --fee 10000
    python3 scripts/underwrite.py --arv 125000 --repairs 65000 --fee 10000 --ask 95000
    python3 scripts/underwrite.py --selftest
"""

from __future__ import annotations

import argparse
import sys

BUYER_PCT = 0.70
WHOLE_FEE_DEFAULT = 10_000


def underwrite(arv: float, repairs: float = 0.0, fee: float = WHOLE_FEE_DEFAULT,
               buyer_costs: float = 0.0, wholesaler_costs: float = 0.0,
               ask: float | None = None, mode: str = "A",
               open_pct_of_mao: float | None = None) -> dict:
    if arv <= 0:
        raise ValueError("ARV must be positive")

    screening = int(round(BUYER_PCT * arv))
    buyer_max = int(round(screening - repairs - (buyer_costs if mode == "B" else 0)))
    seller_mao = int(round(buyer_max - fee - wholesaler_costs))
    gross_spread = int(round(arv - seller_mao - repairs))

    out = {
        "MODE": "A (repairs inside the 70% cap)" if mode == "A"
                else "B (repairs AND buyer costs deducted)",
        "ARV": int(round(arv)),
        "SCREENING CEILING (0.70 x ARV)": screening,
        "REPAIRS": int(round(repairs)),
        "BUYER COSTS": int(round(buyer_costs if mode == "B" else 0)),
        "BUYER MAX CONTRACT": buyer_max,
        "ASSIGNMENT FEE": int(round(fee)),
        "WHOLESALER COSTS": int(round(wholesaler_costs)),
        "SELLER-FACING MAO": seller_mao,
        "BUYER GROSS SPREAD (gross, not profit)": gross_spread,
    }
    if ask is not None:
        pct = (seller_mao / ask * 100) if ask else 0.0
        out["ASKING"] = int(round(ask))
        out["MAO AS % OF ASKING"] = round(pct, 1)
        out["GAP (asking - MAO)"] = int(round(ask - seller_mao))
        if seller_mao >= ask:
            out["ATTAINABLE?"] = "YES - MAO clears asking"
        elif pct >= 80:
            out["ATTAINABLE?"] = f"MAYBE - MAO is {pct:.1f}% of asking, needs a real cut"
        else:
            out["ATTAINABLE?"] = f"NO - MAO is {pct:.1f}% of asking, not a negotiation"
    if open_pct_of_mao is not None:
        out["OPENING OFFER"] = int(round(buyer_max * open_pct_of_mao
                                        - fee - wholesaler_costs))
    return out


# --- the worked check from the standard ------------------------------------
CHECKS = [
    # arv, repairs, fee, buyer_costs, wholesaler, mode, expected buyer_max, mao, spread
    (200_000, 25_000, 10_000, 0, 0, "A", 115_000, 105_000, 70_000),
    (200_000, 25_000, 10_000, 5_000, 0, "B", 110_000, 100_000, 75_000),
    (125_000, 0, 10_000, 0, 0, "A", 87_500, 77_500, 47_500),
]


def selftest() -> int:
    failures = 0
    print("UNDERWRITING SELFTEST - the mandatory arithmetic check\n")
    for arv, rep, fee, bc, wc, mode, bmax, mao, spread in CHECKS:
        r = underwrite(arv, rep, fee, bc, wc, mode=mode)
        got = (r["BUYER MAX CONTRACT"], r["SELLER-FACING MAO"],
               r["BUYER GROSS SPREAD (gross, not profit)"])
        want = (bmax, mao, spread)
        ok = got == want
        print(f"  {'PASS' if ok else 'FAIL'}  ARV ${arv:,} repairs ${rep:,} "
              f"fee ${fee:,} costs ${bc:,} mode {mode}")
        print(f"        buyer max ${got[0]:,}  MAO ${got[1]:,}  gross spread ${got[2]:,}")
        if not ok:
            print(f"        EXPECTED {want}")
            failures += 1

    print("\n  The $200K / $25K / $10K case must reproduce exactly:")
    print("    buyer max $115,000  ->  MAO $105,000  ->  gross spread $70,000")
    print("  $70,000 is a GROSS SPREAD, not net profit.\n")

    # mutation: a model that merges buyer max into the offer must be caught
    bad = underwrite(200_000, 25_000, 10_000, mode="A")
    merged = bad["BUYER MAX CONTRACT"] == bad["SELLER-FACING MAO"]
    print(f"  {'CAUGHT' if not merged else 'MISSED'}  buyer max and seller MAO "
          f"are distinct numbers")
    if merged:
        failures += 1

    print("\n" + ("PASS  arithmetic reproduces" if failures == 0
                  else "FAIL  the model is broken - do not quote a number"))
    return 0 if failures == 0 else 1


def main(argv=None) -> int:
    p = argparse.ArgumentParser(description="Buyer max / seller MAO underwriting")
    p.add_argument("--arv", type=float)
    p.add_argument("--repairs", type=float, default=0.0)
    p.add_argument("--fee", type=float, default=WHOLE_FEE_DEFAULT)
    p.add_argument("--buyer-costs", type=float, default=0.0)
    p.add_argument("--wholesaler-costs", type=float, default=0.0)
    p.add_argument("--ask", type=float)
    p.add_argument("--mode", choices=["A", "B"], default="A")
    p.add_argument("--open-pct", type=float,
                   help="opening offer as a fraction of buyer max (e.g. 0.85)")
    p.add_argument("--selftest", action="store_true")
    a = p.parse_args(argv)

    if a.selftest:
        return selftest()
    if a.arv is None:
        p.print_help()
        return 0

    r = underwrite(a.arv, a.repairs, a.fee, a.buyer_costs, a.wholesaler_costs,
                   a.ask, a.mode, a.open_pct)
    for k, v in r.items():
        if isinstance(v, int) and not isinstance(v, bool):
            print(f"  {k:44}{f'${v:,}':>14}")
        elif isinstance(v, float):
            print(f"  {k:44}{v:>13}%")
        else:
            print(f"  {k:44}{v:>14}")
    print("\n  Buyer max is the cap. Your offer is below your MAO.")
    print("  Gross spread is NOT net profit. ESTIMATE - not an offer.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
