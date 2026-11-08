#!/usr/bin/env bash
# Preflight for the real-estate-deal-sourcing skill.
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

refs="market-research on-market off-market comps condition repairs underwriting qualification data-integrity"
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
  pass "all 9 references present and readable"
else
  fail "$missing reference file(s) missing — README says which steps you cannot run"
fi

scripts="underwrite.py zip_ledger.py gate.py comps.py rank_listing.py comp.py anchor.py"
missing=0
for s in $scripts; do
  if [ -r "$SKILL_ROOT/scripts/$s" ]; then :; else
    echo "  [MISSING] scripts/$s"; missing=$((missing + 1)); fi
done
if [ "$missing" -eq 0 ]; then
  pass "all 7 scripts present"
else
  fail "$missing script(s) missing — arithmetic and ledger checks unavailable"
fi

if [ -r "$SKILL_ROOT/state/property_ledger.csv" ]; then
  n=$(( $(wc -l < "$SKILL_ROOT/state/property_ledger.csv") - 1 ))
  pass "property ledger present ($n properties - duplicate guard has history)"
else
  fail "state/property_ledger.csv missing - duplicate guard has no history, stop and restore it"
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

echo
if [ "$FAIL" -gt 0 ]; then
  echo "PREFLIGHT FAILED ($FAIL failure(s), $PASS pass(es))."
  echo "STOP. Report exactly this to the operator. Do not fall back to generic sourcing."
  exit 1
fi

echo "PREFLIGHT PASSED ($PASS checks${WARN:+, $WARN warning(s)})."
echo "Loaded: SKILL.md v$(awk -F': *' '/^version:/{print $2}' "$SKILL_MD" 2>/dev/null || echo 1.0.0)"
echo "Next: read references/market-research.md, then scan ranked ZIPs by priority."
