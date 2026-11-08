#!/usr/bin/env bash
# Structural + behavioural tests for the wholesale-realestate skill.
# Covers the eight implementation tests from the build spec, plus the repo
# conventions (frontmatter, size budget, referenced files exist, hook injection).
#
# Run: bash tests/test-real-estate-skill.sh
set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
SKILL_DIR="$REPO_ROOT"
SKILL_MD="$SKILL_DIR/SKILL.md"
HOOK="$REPO_ROOT/hooks/session-start"
UNIVERSE="$SKILL_DIR/assets/zip_universe.csv"

PASS=0
FAIL=0
pass() { echo "  [PASS] $1"; PASS=$((PASS + 1)); }
fail() { echo "  [FAIL] $1"; FAIL=$((FAIL + 1)); }
section() { echo; echo "$1"; }

py() { python3 "$@"; }

# ---------------------------------------------------------------------------
section "1. SKILL DISCOVERY AND FORMAT"
# ---------------------------------------------------------------------------
if [ -f "$SKILL_MD" ]; then pass "SKILL.md exists at repo root"
else fail "SKILL.md missing"; fi

if [ -f "$SKILL_MD" ]; then
  fm="$(awk 'NR==1 && $0!="---"{exit} NR>1 && $0=="---"{exit} NR>1{print}' "$SKILL_MD")"
  printf '%s\n' "$fm" | grep -q '^name: wholesale-realestate$' \
    && pass "frontmatter name is wholesale-realestate" \
    || fail "frontmatter name does not match directory"

  desc="$(printf '%s\n' "$fm" | awk '/^description:/{sub(/^description:[ ]*/,""); print; found=1; next} found && /^[ ]/{print} found && !/^[ ]/{exit}' | tr '\n' ' ')"
  printf '%s' "$desc" | grep -q '^Use when' \
    && pass "description starts with 'Use when'" \
    || fail "description does not start with 'Use when'"
  [ "${#desc}" -le 1024 ] \
    && pass "description under 1024 chars (${#desc})" \
    || fail "description over 1024 chars"

  # repo convention: description names triggers, not the workflow
  case "$desc" in
    *"propwire"*|*"PropWire"*) pass "description names the sourcing tools as triggers" ;;
    *) fail "description does not name PropWire/Zillow/Redfin triggers" ;;
  esac

  size=$(wc -c <"$SKILL_MD" | tr -d ' ')
  (( size < 20000 )) && pass "SKILL.md under the 20000-byte compaction limit ($size)" \
    || fail "SKILL.md is $size bytes (limit 20000)"

  # every reference the skill links to must exist
  missing=0
  for r in $(grep -o 'references/[a-z-]*\.md' "$SKILL_MD" | sort -u); do
    [ -r "$SKILL_DIR/$r" ] || { echo "      missing: $r"; missing=$((missing + 1)); }
  done
  [ "$missing" -eq 0 ] && pass "all references linked from SKILL.md exist" \
    || fail "$missing linked reference(s) missing"
fi

section "2. PREFLIGHT (the mandatory gate)"
if out="$(cd "$SKILL_DIR" && bash scripts/preflight.sh 2>&1)"; then
  pass "preflight passes from the skill directory"
  printf '%s' "$out" | grep -q "PREFLIGHT PASSED" \
    && pass "preflight reports PASSED" || fail "preflight output lacks PASSED"
else
  fail "preflight FAILED"; printf '%s\n' "$out" | tail -6
fi

# preflight must actually fail when a required file is gone
TMP_SKILL="$(mktemp -d)"
cp -R "$SKILL_DIR"/. "$TMP_SKILL"/
rm -f "$TMP_SKILL/references/comps.md"
if (cd "$TMP_SKILL" && bash scripts/preflight.sh >/dev/null 2>&1); then
  fail "preflight passes with references/comps.md deleted (it must fail)"
else
  pass "preflight fails when a reference is missing"
fi
rm -f "$TMP_SKILL/assets/zip_universe.csv"
if (cd "$TMP_SKILL" && bash scripts/preflight.sh >/dev/null 2>&1); then
  fail "preflight passes with no ZIP universe (it must fail)"
else
  pass "preflight fails when the ZIP universe is missing"
fi
rm -rf "$TMP_SKILL"

section "3. TEST 2 - NEWLY LISTED RETAIL TURNKEY IS REJECTED"
# behavioural: the screening script decides, not a grep
out="$(py "$SKILL_DIR/scripts/rank_listing.py" --dom 3 --condition fully_renovated \
        --ask 195000 --sqft 1600 --zip-ppsf 120)"
case "$out" in
  REJECT*) pass "newly listed fully-renovated retail -> REJECT" ;;
  *) fail "newly listed retail not rejected (got: $out)" ;;
esac
out="$(py "$SKILL_DIR/scripts/rank_listing.py" --dom 5 --condition turnkey)"
case "$out" in
  REJECT*) pass "turnkey -> REJECT" ;;
  *) fail "turnkey not rejected" ;;
esac
out="$(py "$SKILL_DIR/scripts/rank_listing.py" --dom 4 --condition medium \
        --ask 196000 --sqft 1500 --zip-ppsf 128)"
case "$out" in
  REJECT*"under_14_days"*) pass "4-DOM listing at full retail -> REJECT (14-day rule)" ;;
  *) fail "4-DOM listing not rejected by the 14-day rule" ;;
esac
out="$(py "$SKILL_DIR/scripts/rank_listing.py" --dom 6 --condition heavy \
        --ask 75000 --sqft 1500 --zip-ppsf 128)"
case "$out" in
  PURSUE*"exception"*) pass "sub-14-day exception fires only on documented mispricing" ;;
  *) fail "documented-mispricing exception did not fire" ;;
esac
# the gate must also refuse a retail deal
if py "$SKILL_DIR/scripts/gate.py" --checks \
    "G01=pass,G02=pass,G03=fail,G04=fail,G05=pass,G06=pass,G07=pass,G08=pass,G09=fail,G10=fail,G11=fail,G12=pass,G13=pass,G14=pass,G15=pass" \
    | head -1 | grep -q "REJECT"; then
  pass "15-point gate also rejects the retail case"
else
  fail "gate did not reject the retail case"
fi

section "4. TEST 3 - STALE LISTING WITH REDUCTIONS OUTRANKS A FRESH ONE"
if out="$(py "$SKILL_DIR/scripts/rank_listing.py" --selftest)"; then
  pass "ranking selftest passes"
else
  fail "ranking selftest failed"; printf '%s\n' "$out" | tail -5
fi
printf '%s' "$out" | grep -q "stale (88) outranks fresh (15)" \
  && pass "stale listing scores 88 vs 15 for a fresh one on identical price/size" \
  || fail "stale listing did not outrank a fresh one"
printf '%s' "$out" | grep -q "65 DOM (20) outranks 35 DOM (12)" \
  && pass "60+ DOM outranks 30-59 DOM" || fail "DOM buckets not ordered"
# the rule must also be written down, not only coded
grep -q "60+ days on market" "$SKILL_DIR/references/on-market.md" \
  && pass "60+ DOM prioritised in on-market.md" || fail "60+ DOM rule missing"
grep -qi "documented substantial mispricing" "$SKILL_DIR/references/on-market.md" \
  && pass "14-day exception requires documented mispricing" \
  || fail "14-day exception is unbounded"

section "5. TEST 4 - COMP INTEGRITY (no fabricated five comps)"
if py "$SKILL_DIR/scripts/comps.py" --selftest | tail -1 | grep -q "PASS"; then
  pass "comps selftest passes (5 ok / 4 short / active excluded / stale excluded)"
else
  fail "comps selftest failed"
fi
out="$(py "$SKILL_DIR/scripts/comps.py" --selftest)"
printf '%s' "$out" | grep -q "four comps -> ARV INSUFFICIENTLY SUPPORTED" \
  && pass "4 comps produces no ARV" || fail "4 comps produced an ARV"
printf '%s' "$out" | grep -q "active listings never count" \
  && pass "active listings rejected as comps" || fail "active listing counted as a comp"

section "6. TEST 5 - UNDERWRITING ARITHMETIC (\$200K example)"
out="$(py "$SKILL_DIR/scripts/underwrite.py" --arv 200000 --repairs 25000 --fee 10000)"
printf '%s' "$out" | grep -q 'BUYER MAX CONTRACT *\$115,000' \
  && pass "buyer max = \$115,000" || fail "buyer max wrong"
printf '%s' "$out" | grep -q 'SELLER-FACING MAO *\$105,000' \
  && pass "seller MAO = \$105,000" || fail "seller MAO wrong"
out2="$(py "$SKILL_DIR/scripts/underwrite.py" --arv 200000 --repairs 25000 --fee 10000 --ask 105000)"
printf '%s' "$out2" | grep -q 'BUYER GROSS SPREAD (gross, not profit) *\$70,000' \
  && pass "gross spread at a \$105,000 contract = \$70,000" || fail "gross spread wrong"
printf '%s' "$out2" | grep -q "GROSS SPREAD" \
  && pass "gross spread is labelled gross, not profit" || fail "spread not labelled gross"

section "7. TEST 6 - REPAIR UNCERTAINTY IS FLAGGED, NOT ASSUMED SOUND"
grep -qi "cannot be confirmed remotely" "$SKILL_DIR/references/condition.md" \
  && pass "condition.md requires an 'cannot confirm remotely' section" \
  || fail "no remote-limits section"
if grep -qi "never write that a photo shows a roof" "$SKILL_DIR/references/condition.md"; then
  pass "explicit prohibition on declaring systems sound from photos"
else
  fail "missing the roof/foundation/electrical prohibition"
fi
grep -qi "UNKNOWN" "$SKILL_DIR/references/repairs.md" \
  && pass "repairs.md carries the unknown-systems allowance" || fail "no unknown allowance"
grep -qi "contingency" "$SKILL_DIR/references/repairs.md" \
  && pass "repairs require a contingency" || fail "no contingency rule"
grep -qi "do not use the contingency to smuggle" "$SKILL_DIR/references/repairs.md" \
  && pass "contingency cannot be used to make a deal pass" || fail "contingency loophole open"

section "8. TEST 7 - DUPLICATE PREVENTION"
if py "$SKILL_DIR/scripts/zip_ledger.py" --selftest | tail -1 | grep -q "PASS"; then
  pass "ledger selftest passes"
else
  fail "ledger selftest failed"
fi
out="$(py "$SKILL_DIR/scripts/zip_ledger.py" --selftest)"
printf '%s' "$out" | grep -q "scanned property is recognised" \
  && pass "a previously scanned property is recognised as SEEN" \
  || fail "duplicate guard does not recognise a seen property"
printf '%s' "$out" | grep -q "re-logging updates in place" \
  && pass "re-logging does not duplicate the ledger row" \
  || fail "re-logging duplicated a row"
if tr '\n' ' ' < "$SKILL_DIR/references/market-research.md" \
     | tr -s ' ' | grep -qi "never as a new opportunity"; then
  pass "the rule is documented, not just coded"
else
  fail "rule not in the reference"
fi

section "9. TEST 8 - SESSION RECOVERY (self-loading routing)"
for f in CLAUDE.md AGENTS.md GEMINI.md .cursorrules .github/copilot-instructions.md; do
  if [ -r "$REPO_ROOT/$f" ] && grep -q "MANDATORY ROUTING" "$REPO_ROOT/$f"; then
    pass "$f tells a new session to load the skill first"
  else
    fail "$f missing the mandatory routing header"
  fi
done
# the routing header must carry the stop rule and the preflight step
hdr="$(sed -n '1,25p' "$REPO_ROOT/CLAUDE.md")"
printf '%s' "$hdr" | grep -q "scripts/preflight.sh" \
  && pass "routing header requires the preflight run" || fail "preflight not required"
printf '%s' "$hdr" | grep -q "STOP" \
  && pass "routing header carries the stop rule" || fail "no stop rule"
printf '%s' "$hdr" | grep -q "conversation" \
  && pass "routing header forbids relying on conversation memory" \
  || fail "memory dependency not forbidden"
# agent-memory pointer must exist in the documented MEMORY.md format
if [ -r "$REPO_ROOT/MEMORY.md" ]; then
  pass "MEMORY.md exists (agent-memory-repo format)"
  grep -q "source of truth" "$REPO_ROOT/MEMORY.md" \
    && pass "MEMORY.md names the repository as source of truth" \
    || fail "MEMORY.md lacks the source-of-truth rule"
  grep -q '^## Index' "$REPO_ROOT/MEMORY.md" \
    && pass "MEMORY.md has the required Index section" || fail "no Index section"
  grep -q '\[added: ' "$REPO_ROOT/MEMORY.md" \
    && pass "MEMORY.md entries carry [added: YYYY-MM-DD] metadata" \
    || fail "entries lack added metadata"
else
  fail "MEMORY.md missing"
fi

section "9b. ARV ENGINE (comping rule, executable)"
if out="$(py "$SKILL_DIR/scripts/comp.py" --selftest)"; then
  pass "ARV engine selftest passes"
else
  fail "ARV engine selftest failed"
fi
printf '%s' "$out" | grep -q "9/9 checks" \
  && pass "9/9 checks pass on the healthy fixture" || fail "checks did not all pass"
printf '%s' "$out" | grep -q "9/9 checks proven able to fail" \
  && pass "9/9 injected defects are caught (each check can actually fail)" \
  || fail "a check cannot fail - it is a false PASS"
printf '%s' "$out" | grep -q '\$350,000 ARV / \$34,933 repairs -> ceiling \$210,067' \
  && pass "economics regression: \$350K/\$34,933 -> ceiling \$210,067" \
  || fail "economics regression broken"
# the ladder must NOT hand back a number when comps are absent
tmpc="$(mktemp)"
echo "address,sold,price,sqft,hood,lat,lon,style,beds,exclusion" > "$tmpc"
if out2="$(py "$SKILL_DIR/scripts/comp.py" --comps "$tmpc" --as-of 2026-10-31 \
     --subject '{"address":"X","sqft":1642,"hood":"44302","lat":41.079,"lon":-81.536,"style":"COLONIAL"}')"; then
  fail "empty comp file produced a priced ARV"
else
  printf '%s' "$out2" | grep -q "NO COMPS" \
    && pass "empty comp set -> NO COMPS, no ARV" || fail "no COMPS refusal"
fi
rm -f "$tmpc"
# the worked Akron example must reproduce the documented correction
if out3="$(py "$SKILL_DIR/scripts/comp.py" --comps "$SKILL_DIR/fixtures/akron_44302_worked_example.csv" \
     --as-of 2026-10-31 --subject '{"address":"141 Grand Ave","sqft":1642,"hood":"44302","lat":41.0790,"lon":-81.5360,"style":"COLONIAL"}')"; then
  flat3="$(printf '%s' "$out3" | tr -d ' ')"
  printf '%s' "$flat3" | grep -qF 'ARVLOW$114,578' \
    && pass "141 Grand Ave ARV LOW = \$114,578" || fail "ARV LOW wrong"
  printf '%s' "$flat3" | grep -qF 'ARVPOINT$120,571' \
    && pass "141 Grand Ave ARV POINT = \$120,571" || fail "ARV POINT wrong"
  printf '%s' "$flat3" | grep -qF 'ARVHIGH$126,372' \
    && pass "141 Grand Ave ARV HIGH = \$126,372" || fail "ARV HIGH wrong"
  printf '%s' "$flat3" | grep -q 'UNDERWRITELOW' \
    && pass "LOW confidence underwrites to the LOW tier" \
    || fail "lower-confidence row did not underwrite to LOW"
  printf '%s' "$out3" | grep -q "64 Byers Ave" \
    && pass "newer build excluded from the ARV maths but still reported" \
    || fail "newer build not excluded"
fi

section "9c. THE RULES THAT CAME FROM THE ARV-COMPING SPEC"
# bed floor, renovated-only, consistency gate, tiers, anchor
if out="$(py "$SKILL_DIR/scripts/comp.py" --selftest)"; then
  printf '%s' "$out" | grep -q "4-bed subject with only 3-bed comps -> NO COMPS" \
    && pass "bed floor: a lower-bed comp set cannot produce an ARV" \
    || fail "bed floor not enforced"
  printf '%s' "$out" | grep -q "no renovated comps -> NO COMPS" \
    && pass "renovated-only: a dated/distressed pool cannot produce an ARV" \
    || fail "condition gate not enforced"
  printf '%s' "$out" | grep -q "CAUGHT  price_gap" \
    && pass "consistency gate catches a \$40K sale among \$100K comps" \
    || fail "consistency gate does not catch a price gap"
  printf '%s' "$out" | grep -qF "(\$20/sf)" \
    && pass "repair tiers present (light \$20/sf)" || fail "repair tiers missing"
  printf '%s' "$out" | grep -q "MAO by ARV tier" \
    && pass "MAO computed per ARV tier (LOW/POINT/HIGH)" \
    || fail "MAO not computed per ARV tier"
  printf '%s' "$out" | grep -q "ARV LOW" \
    && pass "ARV is reported as a range, not a single point" \
    || fail "ARV is a single number"
else
  fail "comp.py selftest failed"
fi
if out="$(py "$SKILL_DIR/scripts/anchor.py" --selftest)"; then
  printf '%s' "$out" | grep -q "BIMODAL flagged" \
    && pass "anchor flags a bimodal ZIP (mansion + distress)" \
    || fail "bimodal detection missing"
  printf '%s' "$out" | grep -q "no median invented" \
    && pass "anchor refuses to invent a median from too few sales" \
    || fail "anchor invents a median"
else
  fail "anchor selftest failed"
fi

section "9d. THE LEDGERS SURVIVE A FRESH CLONE"
if [ -r "$SKILL_DIR/state/property_ledger.csv" ] && [ -r "$SKILL_DIR/state/zip_ledger.csv" ]; then
  pass "both ledgers are committed (not gitignored)"
else
  fail "a ledger is missing - the duplicate guard resets on every clone"
fi
if grep -qx "state/" "$SKILL_DIR/.gitignore" 2>/dev/null; then
  fail "state/ is gitignored again - history will be lost"
else
  pass "state/ is not gitignored"
fi
# the guard must actually recognise a documented property from a fresh checkout
out="$(py "$SKILL_DIR/scripts/zip_ledger.py" --check "141 Grand Ave" --city Akron --zip 44302)"
case "$out" in
  SEEN*) pass "a documented property is recognised as SEEN in a fresh clone" ;;
  *) fail "fresh clone reports a known property as NEW" ;;
esac
n=$(( $(wc -l < "$SKILL_DIR/state/zip_ledger.csv") - 1 ))
[ "$n" -ge 4 ] && pass "scan history present ($n ZIPs)" || fail "scan history empty"
# append-only must be stated, not just implied
if tr '\n' ' ' < "$SKILL_DIR/SKILL.md" | tr -s ' ' | grep -qi "Never delete a row"; then
  pass "append-only ledger rule is written down"
else
  fail "no append-only rule"
fi

section "9e. SOURCE HIERARCHY AND DATA-LICENSING LIMITS"
# Zillow is primary discovery, Redfin is cross-check. Order matters.
if grep -q "Zillow is the primary manual discovery reference" "$SKILL_DIR/references/on-market.md"; then
  pass "on-market.md states Zillow is the primary discovery reference"
else
  fail "source hierarchy (Zillow primary / Redfin cross-check) is not stated"
fi
if grep -qi "Redfin is a secondary" "$SKILL_DIR/references/on-market.md"; then
  pass "Redfin is explicitly demoted to secondary cross-check"
else
  fail "Redfin not demoted to cross-check"
fi
# the cross-check must not be mistakable for independent verification
if tr '\n' ' ' < "$SKILL_DIR/references/on-market.md" | tr -s ' ' | grep -qi "one portal repeating another portal is not a second source"; then
  pass "a portal echoing a portal is not treated as verification"
else
  fail "no rule against treating Redfin as independent verification"
fi
# the licensing constraint that shapes the whole recommendation must be recorded
if [ -r "$SKILL_DIR/references/data-access.md" ]; then
  pass "data-access reference exists"
else
  fail "references/data-access.md missing"
fi
if tr '\n' ' ' < "$SKILL_DIR/references/data-access.md" | tr -s ' ' | grep -qi "business solicitation"; then
  pass "NAR 4.4.1 solicitation prohibition is recorded"
else
  fail "MLS data may not be used for solicitation - rule missing"
fi
if tr '\n' ' ' < "$SKILL_DIR/references/data-access.md" | tr -s ' ' | grep -qi "automated valuation"; then
  pass "valuation use (Policy 7.90) is recorded as permitted"
else
  fail "no record that valuation use is permitted"
fi
# and it must be reachable from the routing table, not orphaned
if grep -q "references/data-access.md" "$SKILL_DIR/SKILL.md"; then
  pass "data-access is wired into the SKILL.md reference table"
else
  fail "data-access.md is orphaned"
fi
# a new data source cannot be adopted without the capability check
if grep -q "Adding a source" "$SKILL_DIR/references/data-access.md"; then
  pass "new-source checklist present"
else
  fail "no adoption checklist"
fi

section "9f. ONE SOURCE OF TRUTH (no stale copies, no drift)"
# Exactly one SKILL.md may exist in the skill tree. A second copy is a loaded
# instruction set that can contradict this one, which is how a "fixed" rule
# comes back to life months later.
copies="$(find "$SKILL_DIR" -name 'SKILL.md' -not -path '*/node_modules/*' -not -path '*/.git/*' | wc -l)"
if [ "$copies" -eq 1 ]; then
  pass "exactly one SKILL.md in the skill tree"
else
  fail "$copies SKILL.md copies found - stale instruction sets can be loaded"
fi
# One version number, taken from the rulebook itself.
ver="$(awk -F': *' '/^version:/{print $2; exit}' "$SKILL_MD")"
if [ -n "$ver" ]; then pass "SKILL.md declares version $ver"
else fail "SKILL.md has no version"; fi
# Docs must not pin a version: preflight prints it, prose cannot rot if it is absent.
if grep -rqE 'v[12]\.[01]\.0' --include="*.md" "$SKILL_DIR" 2>/dev/null; then
  fail "a doc pins an old version string - it will drift"
else
  pass "no stale version strings in docs"
fi
# preflight must read the version rather than hard-coding it.
if grep -q 'awk -F.*version' "$SKILL_DIR/scripts/preflight.sh"; then
  pass "preflight reads the version instead of hard-coding it"
else
  fail "preflight hard-codes a version"
fi
# The version must appear in exactly one file - the rulebook.
if [ "$(grep -rl '^version:' --include="*.md" "$SKILL_DIR" 2>/dev/null | wc -l)" -eq 1 ]; then
  pass "version is declared in exactly one file"
else
  fail "more than one file declares a version"
fi
# Docs must not hard-code a check count. Exit codes are the contract; a number
# in prose rots the moment a test is added, and a stale claim is an inaccuracy.
if grep -rqE '[0-9]+ (test )?checks' --include="*.md" "$SKILL_DIR" 2>/dev/null; then
  fail "a doc hard-codes a check count - it rots the moment a test is added"
else
  pass "no doc hard-codes a check count"
fi
# The rulebook is the only place the hard rules live; the notes file indexes them.
if grep -qE '^[0-9]+\. \*\*' "$SKILL_MD"; then
  pass "hard rules live in SKILL.md and are numbered"
else
  fail "SKILL.md has no numbered hard rules"
fi

# ---------------------------------------------------------------------------
section "10. DATA INTEGRITY RULES PRESENT"
for pat in "Invent a property address" "Invent a sold price" \
           "Invent buyer approval" "Claim to have swept a ZIP"; do
  if grep -qi "$pat" "$SKILL_DIR/references/data-integrity.md"; then
    pass "data-integrity: $pat"
  else
    fail "data-integrity rule missing: $pat"
  fi
done
for label in VERIFIED REPORTED ESTIMATED ASSUMED UNKNOWN; do
  grep -q "$label" "$SKILL_DIR/references/data-integrity.md" \
    && pass "label defined: $label" || fail "label missing: $label"
done

section "11. FIVE-COMP AND BUY-BOX RULES STATED"
grep -qi "five" "$SKILL_DIR/references/comps.md" \
  && pass "comps.md states the five-comp standard" || fail "five-comp standard absent"
grep -q "125,000" "$SKILL_DIR/references/underwriting.md" \
  && pass "buy box ARV floor stated" || fail "buy box floor missing"
grep -qi "guideline, not commitment" "$SKILL_DIR/references/underwriting.md" \
  && pass "buy box labelled a guideline, not a commitment" \
  || fail "buy box presented as a commitment"
grep -qi "buyer has approved" "$SKILL_DIR/references/underwriting.md" \
  && pass "buyer approval cannot be claimed" || fail "approval rule missing"

section "12. ZIP UNIVERSE SEED"
if [ -r "$UNIVERSE" ]; then
  pass "assets/zip_universe.csv present"
  for city in Akron Cleveland; do
    grep -q "^$city," "$UNIVERSE" && pass "seed contains $city ZIPs" \
      || fail "seed missing $city"
  done
  # scores must not be invented: every row is UNRANKED with an empty score
  if py - "$UNIVERSE" <<'PY'
import csv, sys
rows = list(csv.DictReader(open(sys.argv[1], encoding="utf-8")))
bad = [r for r in rows if r["priority_score"].strip() and
       not r["evidence"].strip()]
sys.exit(1 if bad else 0)
PY
  then pass "no ZIP carries a score without written evidence"
  else fail "a ZIP has a score but no evidence"; fi
else
  fail "assets/zip_universe.csv missing"
fi

# ---------------------------------------------------------------------------
echo
if [ "$FAIL" -gt 0 ]; then
  echo "STATUS: FAILED ($FAIL failure(s), $PASS pass(es))"
  exit 1
fi
echo "STATUS: PASSED ($PASS checks)"
