#!/usr/bin/env bash
# Preflight for the wholesale-realestate skill. The only copy of the rulebook
# is SKILL.md at the repo root; this script loads it and prints its version.
# Run BEFORE any sourcing, comping, repair or underwriting work.
# Exit 0 = the skill is intact and current. Exit 1 = STOP and report what is missing.
set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILL_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
SKILL_MD="$SKILL_ROOT/SKILL.md"

PASS=0
FAIL=0
WARN=0
pass() { echo "  [PASS] $1"; PASS=$((PASS + 1)); }
fail() { echo "  [FAIL] $1"; FAIL=$((FAIL + 1)); }

echo "REAL ESTATE DEAL SOURCING — preflight"
echo "skill root: $SKILL_ROOT"

if [ ! -f "$SKILL_MD" ]; then
  fail "SKILL.md missing at $SKILL_MD"
  echo "STOP. Do not source from memory or from generic browsing."
  exit 1
fi
pass "SKILL.md present"

name="$(awk 'NR==1 && $0!="---"{exit} NR>1 && $0=="---"{exit} NR>1{print}' "$SKILL_MD" \
        | awk -F': *' '/^name:/{print $2}')"
if [ "$name" = "wholesale-realestate" ]; then
  pass "frontmatter name = $name"
else
  fail "frontmatter name is '$name', expected wholesale-realestate"
fi

refs="market-research on-market off-market comps condition repairs underwriting qualification data-integrity data-access negotiation hood-verification"
missing=0
for r in $refs; do
  if [ -r "$SKILL_ROOT/references/$r.md" ]; then
    :
  else
    echo "  [MISSING] references/$r.md"
    missing=$((missing + 1))
  fi
done
if [ "$missing" -eq 0 ]; then
  pass "all 11 references present and readable"
else
  fail "$missing reference file(s) missing — README says which steps you cannot run"
fi

# The defect log is institutional memory: every mistake the system has made, and what
# prevents it recurring. It must exist and must not be empty, or a new agent has no way
# to learn from a previous session's errors.
if [ -r "$SKILL_ROOT/DEFECT_LOG.md" ]; then
  defects=$(grep -c '^## D-' "$SKILL_ROOT/DEFECT_LOG.md" 2>/dev/null || true)
  empty=$(grep -c '^## D-' "$SKILL_ROOT/DEFECT_LOG.md" 2>/dev/null | head -1)
  if [ "$defects" -ge 10 ] 2>/dev/null; then
    pass "defect log present ($defects logged defects)"
  else
    fail "DEFECT_LOG.md has only $defects entries — it is append-only, never trimmed"
  fi
else
  fail "DEFECT_LOG.md missing — institutional memory is gone"
fi

scripts="underwrite.py zip_ledger.py gate.py comps.py rank_listing.py comp.py anchor.py negotiate.py"
missing=0
for s in $scripts; do
  if [ -r "$SKILL_ROOT/scripts/$s" ]; then :; else
    echo "  [MISSING] scripts/$s"; missing=$((missing + 1)); fi
done
if [ "$missing" -eq 0 ]; then
  pass "all 8 scripts present"
else
  fail "$missing script(s) missing — arithmetic and ledger checks unavailable"
fi

if [ -r "$SKILL_ROOT/state/property_ledger.csv" ]; then
  n=$(( $(wc -l < "$SKILL_ROOT/state/property_ledger.csv") - 1 ))
  pass "property ledger present ($n properties - duplicate guard has history)"
else
  fail "state/property_ledger.csv missing - duplicate guard has no history, stop and restore it"
fi
# Offline guard for the ledger <-> sheet drift that D-7 recorded. state/sheet_export.csv is
# refreshed by hand from get_values; every address it lists must exist in the ledger.
if [ -r "$SKILL_ROOT/state/sheet_export.csv" ] && [ -r "$SKILL_ROOT/state/property_ledger.csv" ] && command -v python3 >/dev/null 2>&1; then
  drift="$(python3 - "$SKILL_ROOT" <<'PYX'
import csv, sys
root = sys.argv[1]
led = {r["address"].strip().lower() for r in csv.DictReader(open(root + "/state/property_ledger.csv"))}
sheet = [r["address"].strip() for r in csv.DictReader(open(root + "/state/sheet_export.csv"))]
missing = [a for a in sheet if a.lower() not in led]
print("|".join(missing))
PYX
)"
  if [ -z "$drift" ]; then
    pass "ledger matches the last sheet export (no drift)"
  else
    fail "sheet rows absent from the property ledger: $drift"
  fi
fi
if [ -r "$SKILL_ROOT/state/zip_ledger.csv" ]; then
  n=$(( $(wc -l < "$SKILL_ROOT/state/zip_ledger.csv") - 1 ))
  pass "zip ledger present ($n scanned ZIPs)"
else
  fail "state/zip_ledger.csv missing - scan history lost"
fi
if [ -r "$SKILL_ROOT/assets/zip_universe.csv" ]; then
  n=$(( $(wc -l < "$SKILL_ROOT/assets/zip_universe.csv") - 1 ))
  pass "zip universe seeded ($n ZIPs)"
else
  fail "assets/zip_universe.csv missing — no ranked ZIP list, do not scan blind"
fi

# The arithmetic must reproduce before any number is quoted.
if command -v python3 >/dev/null 2>&1; then
  if out="$(python3 "$SKILL_ROOT/scripts/underwrite.py" --selftest 2>&1)"; then
    pass "underwriting arithmetic reproduces (\$200K/\$25K/\$10K -> 115K/105K/70K)"
  else
    fail "underwriting selftest FAILED — do not quote any number"
    printf '%s\n' "$out" | tail -5
  fi
  if python3 "$SKILL_ROOT/scripts/gate.py" --selftest >/dev/null 2>&1; then
    pass "qualification gate behaves"
  else
    fail "gate selftest FAILED"
  fi
  if python3 "$SKILL_ROOT/scripts/zip_ledger.py" --selftest >/dev/null 2>&1; then
    pass "ledger and duplicate guard behave"
  else
    fail "ledger selftest FAILED"
  fi
  if python3 "$SKILL_ROOT/scripts/comps.py" --selftest >/dev/null 2>&1; then
    pass "five-comp rule enforced"
  else
    fail "five-comp selftest FAILED"
  fi
  if python3 "$SKILL_ROOT/scripts/rank_listing.py" --selftest >/dev/null 2>&1; then
    pass "on-market listing screen behaves"
  else
    fail "listing screen selftest FAILED"
  fi
  if python3 "$SKILL_ROOT/scripts/comp.py" --selftest >/dev/null 2>&1; then
    pass "ARV engine: 9 checks, 9/9 mutations caught"
  else
    fail "ARV engine selftest FAILED - do not quote an ARV"
  fi
  if python3 "$SKILL_ROOT/scripts/anchor.py" --selftest >/dev/null 2>&1; then
    pass "median anchor + bimodal detection behave"
  else
    fail "anchor selftest FAILED"
  fi
  if python3 "$SKILL_ROOT/scripts/negotiate.py" --selftest >/dev/null 2>&1; then
    pass "pre-call negotiation gate refuses a talk track without a BATNA"
  else
    fail "negotiation gate selftest FAILED - do not open a seller conversation"
  fi
else
  fail "python3 not available — arithmetic cannot be verified, do not quote numbers"
fi

# --- data freshness --------------------------------------------------------
# A comp is only good for its window. Yesterday's sold data is today's stale ARV,
# so the preflight reports ledger age rather than letting a silent drift through.
if [ -r "$SKILL_ROOT/state/zip_ledger.csv" ] && command -v python3 >/dev/null 2>&1; then
  newest="$(python3 - "$SKILL_ROOT/state/zip_ledger.csv" <<'PYEOF'
import csv, sys
from datetime import date
try:
    rows = [r for r in csv.DictReader(open(sys.argv[1], encoding="utf-8"))
            if r.get("last_scan_date")]
    print(max(r["last_scan_date"] for r in rows) if rows else "none")
except Exception:
    print("none")
PYEOF
)"
  if [ "$newest" != "none" ]; then
    age=$(( ( $(date -u +%s) - $(date -u -d "$newest" +%s 2>/dev/null || date -u +%s) ) / 86400 ))
    if [ "$age" -gt 30 ]; then
      echo "  [WARN] newest scan is $age days old ($newest). Re-scan before quoting an ARV."
      WARN=$((WARN + 1))
    else
      pass "scan data is fresh (newest $newest, ${age}d old)"
    fi
  fi
fi

# --- the buy box is the repo's, not the agent's -----------------------------
# Failure this catches (2026-11-08): a Dayton sweep was run against a $100,000
# maximum ASKING price and a 3+ bedroom floor. Neither exists in this repo.
# references/underwriting.md constrains the ARV ($125,000-$900,000) and the 70%
# ceiling; references/on-market.md says pull ALL TYPES under the market's price
# band. An invented filter silently deletes real properties and then gets quoted
# as complete coverage. So the buy box must be stated in the repo and the sweep
# must be measured against it, not against a remembered one.
if [ -r "$SKILL_ROOT/state/sweeps/dayton_coverage.csv" ]; then
  if python3 - "$SKILL_ROOT" <<'PYEOF'
import csv, sys, os, re
root = sys.argv[1]
# 1. the buy box must exist in the repo, with an ARV floor and ceiling
u = os.path.join(root, "references", "underwriting.md")
txt = open(u, encoding="utf-8").read() if os.path.exists(u) else ""
has_arv_range = bool(re.search(r"ARV range.*\$\d", txt))
has_ceiling = "70%" in txt
# 2. no sweep file may carry an asking-price cap that the buy box does not state
#    an ARV floor for. A price_cap column is allowed ONLY if labelled as derived.
sweep = os.path.join(root, "state", "sweeps", "dayton_coverage.csv")
rows = list(csv.DictReader(open(sweep, encoding="utf-8")))
bad = []
for r in rows:
    cap = (r.get("price_cap") or "").strip()
    if not cap:
        continue
    note = (r.get("filter_basis") or "").strip().lower()
    if note not in ("repo", "derived", "operator"):
        bad.append(r.get("zip") or "?")
print("OK" if (has_arv_range and has_ceiling and not bad) else
      f"BAD arv_range={has_arv_range} ceiling={has_ceiling} unlabelled_caps={bad}")
PYEOF
  then :; fi
  BBOX="$(python3 - "$SKILL_ROOT" <<'PYEOF'
import csv, sys, os, re
root = sys.argv[1]
u = os.path.join(root, "references", "underwriting.md")
txt = open(u, encoding="utf-8").read() if os.path.exists(u) else ""
has_arv_range = bool(re.search(r"ARV range.*\$\d", txt))
has_ceiling = "70%" in txt
sweep = os.path.join(root, "state", "sweeps", "dayton_coverage.csv")
bad = []
try:
    for r in csv.DictReader(open(sweep, encoding="utf-8")):
        cap = (r.get("price_cap") or "").strip()
        if not cap:
            continue
        basis = (r.get("filter_basis") or "").strip().lower()
        acknowledged = bool((r.get("deviation_note") or "").strip())
        if basis not in ("repo","derived","operator") and not acknowledged:
            bad.append(r.get("zip"))
except Exception as e:
    print("BAD unreadable sweep: %s" % e); raise SystemExit
print("OK" if (has_arv_range and has_ceiling and not bad) else
      "BAD arv_range=%s ceiling=%s unlabelled_caps=%s" % (has_arv_range, has_ceiling, bad))
PYEOF
)"
  case "$BBOX" in
    OK) pass "buy box comes from the repo and every price cap is labelled" ;;
    *)  fail "sourcing filter is not traceable to the repo: ${BBOX#BAD }" ;;
  esac
fi

echo
if [ "$FAIL" -gt 0 ]; then
  echo "PREFLIGHT FAILED ($FAIL failure(s), $PASS pass(es))."
  echo "STOP. Report exactly this to the operator. Do not fall back to generic sourcing."
  exit 1
fi

echo "PREFLIGHT PASSED ($PASS checks${WARN:+, $WARN warning(s)})."
echo "Loaded: SKILL.md v$(awk -F': *' '/^version:/{print $2}' "$SKILL_MD" 2>/dev/null || echo 1.0.0)"
echo "Next: read references/market-research.md, then scan ranked ZIPs by priority."
