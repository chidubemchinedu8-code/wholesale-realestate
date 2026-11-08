 Wholesale Real Estate — Sourcing & Underwriting System

  >>> START HERE: this repository is the single source of truth for all deal sourcing,
  >>> comping and underwriting. Run `bash scripts/preflight.sh` first. See CLAUDE.md.

  One skill, one procedure, executable rules that fail loudly:
  SKILL.md (entry) + references/ (detail) + scripts/ (enforcement) + fixtures/ (proof).
  Tests: `bash tests/test-real-estate-skill.sh` — 73 checks, all must pass.

What this is

  A fully guided wholesale real estate workflow built as a Claude Code skill. Whether you're a seasoned investor or just
   getting started, this skill walks you through every step of the wholesale process — from finding motivated seller
  leads in any city to closing and collecting your assignment fee.

  ---
  What It Does

  Deal Finder (Search by City/Area)
  Tell the skill what city or area you want to target and it goes to work. It runs parallel web searches across Zillow,
  Redfin, Craigslist, Facebook Marketplace, foreclosure databases, probate records, and tax delinquent lists — pulling
  real, live data on distressed and motivated seller properties. Each lead is automatically scored using a Motivated
  Seller Score (MSS) rubric that weighs signals like days on market, price reductions, as-is status, foreclosure,
  probate, and vacancy. Results are ranked into Hot and Warm leads and presented in a clean table you can act on
  immediately or export to a markdown file.

  Deal Analysis
  Plug in any property's numbers and the skill gives you the ceiling (0.70 × ARV − repairs), the 55–60% offer range
   under it, the friction in between, and the contract price that leaves your $10,000 fee. 70% is a cap, not an offer
   price; the fee is deducted once. It also outputs a Deal Scorecard so you know whether a deal is worth pursuing
   before you ever pick up the phone.

  ARV Estimation (binding standard)
  Comping is rule-based, not vibes-based. ARV = subject sqft × p75 $/sqft of at least 3 arm's-length closed sales in
  the same neighbourhood, within 1.5 mi, inside a 6–12 month window, within ±30% sqft, × 0.88. Under 3 comps the
  answer is UNPRICED — never a widened radius, never an average across tiers. The rulebook is comping/COMPING.md;
  scripts/comp.py runs it, enforces six checks and proves each one can fail.

      python3 scripts/comp.py --selftest      # 6 checks, 6 injected defects, economics regressions
      python3 scripts/comp.py --exclusions    # not comps: AMI-restricted, new builds, quitclaims, asking prices
      python3 scripts/comp.py --comps <csv> --subject '<json>' --as-of YYYY-MM-DD --repairs <graded>

  Offer & Negotiation
  Generates a ready-to-use seller conversation script tailored to your numbers, with negotiation anchors and a Purchase
  and Sale Agreement checklist — including the critical "and/or assigns" clause that makes the contract assignable.

  End Buyer & Assignment
  Suggests where to find cash buyers fast (REIA meetings, Facebook groups, BiggerPockets, co-wholesaling), calculates
  your assignment fee, and provides an assignment agreement checklist to hand off cleanly to your title company.

  Closing Workflow
  Step-by-step closing checklist from title search through disbursement, plus post-close actions to grow your buyers
  list and track your deal history.

  ---
  Who It's For

  - Wholesale real estate investors at any level
  - Beginners who need a structured process to follow
  - Experienced wholesalers who want faster lead research and deal analysis
  - Anyone running a high-volume deal pipeline who wants to move from lead to offer faster

  ---
  How to Use

  Install the skill by placing the SKILL.md file in your .claude/skills/wholesale-realestate/ directory. Then invoke it
  anytime with:

  /wholesale-realestate

  From there you can say things like:

  - "find deals in Memphis, TN" — triggers the Deal Finder
  - "I have a deal at 123 Main St, ARV $180k, repairs $25k" — jumps straight to analysis
  - "help me make an offer" — generates your offer script
  - "export results" — saves your lead table to a markdown file

  The skill is conversational — it asks only for what it needs at each step and flows naturally from one stage to the
  next.
