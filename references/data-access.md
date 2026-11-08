# Data access — legitimate routes, and which one to use

Read this before buying any data subscription, and before claiming the skill
"has MLS access" (it does not). It changes **how listings and sales are
obtained**, not any sourcing, comping or underwriting rule.

## Source hierarchy (decided 2026-11-08)

| Rank | Source | Role |
|---|---|---|
| 1 | **Zillow** | Primary **manual discovery** reference. Human-read property pages: price history, Zestimate, MLS #, lot/features. Never automated, never a filter URL. |
| 2 | **Redfin** | Secondary **cross-check**. Confirms or contradicts Zillow; supplies DOM and sold records on the secondary pass. |
| 3 | MLS / RESO (licensed) | **Only** authoritative source for sold prices, DOM, and status — once licensed. Required before any figure is called `VERIFIED`. |
| 4 | County records / GIS | Hard facts: owner, deed, sqft, year built, tax delinquency, sheriff sales. Public data, usable for outreach. |
| 5 | Investor data (ATTOM, PropStream, BatchData) | Enrichment: equity, absentee, pre-foreclosure, permits. **Not** listing status, DOM, or comps. |

Two directories exist by accident of history, not by merit. Discovery is manual
on Zillow first because its property pages are the richest and its filters are
unreliable — a filter failure is not a reason to abandon the page.

## The constraint that decides everything

**MLS-licensed data may not be used to generate seller outreach.**

From NAR model MLS rules, Section 4.4.1 (*Use of MLS Data by MLS Participant*):

> MLS participants, subscribers, and affiliated licensees are strictly
> prohibited from transferring, distributing, or incorporating any MLS data, or
> information derived from such data, into any external database or system, for
> use of business solicitation.

Local rules restate it. REcolorado: *"Trolling/prospecting Expired and/or
Withdrawn listings is not an acceptable use of MLS content… prohibited from
taking MLS information in mass for purposes of lead generation. A subscriber may
solicit on a listing by listing basis, but not in mass."* MLSListings: MLS
information may be used only *"to market property to bona fide prospective
purchasers or to support market evaluations or appraisals."* IDX rules add
Section 16.2.2: IDX listings may not be used for any purpose other than display.

**Consequence: no MLS license — at any price — can be your deal-sourcing
engine.** It can only price deals you already found.

But the same policy explicitly protects the valuation side (NAR Policy 7.90):

> Any MLS content in data feeds available to participants for real estate
> brokerage purposes must also be available to participants for valuation
> purposes, including automated valuations.

So the ARV engine is squarely permitted. Sourcing from MLS is not. That is why
the workflow is split into two data planes.

## The two-plane architecture

| | Plane A — price it | Plane B — find it |
|---|---|---|
| Question | What is it worth, what will a buyer pay | Whose property might sell below value |
| Authorised source | MLS via RESO Web API | County records, investor data, public sites |
| Buys you | Sold prices, DOM, status history, photos, ZIP search | Owner, equity, tax delinquency, absentee, pre-foreclosure |
| Cannot buy | Seller names, motivation | Verified sold prices, true DOM |
| Rule | Found elsewhere, priced here | Found here, priced by Plane A |

A property may **never** move from Plane B to a shortlist without Plane A
comps. A property found in Plane A may not be contacted based on what Plane A
told you.

## The licensed options, honestly compared

### 1. RESO Web API — the standard, not a vendor

JSON/OData over REST, standard field names (`ListPrice`, `StandardStatus`,
`BedroomsTotal`, `DaysOnMarket`, `ListingKey`, `ModificationTimestamp`).
~90% of US MLSs are RESO Web API certified; RESO tracks ~489 MLS systems.
Certification is plumbing only — **the licence comes from the MLS.** RESO itself
sells no data and issues no credentials.

### 2. Gateways (one integration, still one licence per MLS)

| Gateway | Model | Note |
|---|---|---|
| **Bridge Interactive** (Zillow Group) | No gateway service fee; the MLS charges its own | FMLS, Stellar, MIAMI, REcolorado. Partner-gated, MLS affiliation usually required |
| **Trestle** (Cotality/CoreLogic) | ~$85/mo per MLS connection, **plus** whatever the MLS charges | ~100–105 MLS orgs; biggest territory; MLS sets and collects the licensing fee |
| **MLS Grid** | One standard licence across participating MLSs | Vendor ~$250/mo feed + $20/mo per licence; broker must ratify each |
| **Spark API** | MLS-member-gated | Members only |

None of these remove the requirement that *you* hold a licence with *each* MLS.
A gateway is a pipe; the right to the water is per-board.

### 3. IDX vs VOW vs BBO vs vendor feed

| Feed | Contains | Who may hold it |
|---|---|---|
| IDX | Active + (optionally) sold. **No** expired/withdrawn (prohibited) | MLS participants, for public display |
| IDX Plus | Adds recent sold | Same |
| VOW | All statuses, up to 7 years off-market, incl. expired/withdrawn | Participants and their AVPs, for registered clients only |
| BBO (Broker Back Office) | All listings, all participants — for CRM/back-office use | Participants; may not be opted out |
| Vendor / tech-provider feed | Whatever the MLS configures | Approved third-party vendors |

For comps you need **IDX Plus or VOW**. Basic IDX alone has no sold data, which
makes it useless for ARV.

### 4. Who may apply — the eligibility wall

NAR policy: a Participant is a REALTOR® acting as principal, partner, corporate
officer or branch office manager, holding a current, valid **broker's** licence.
An unlicensed investor cannot hold an MLS seat. Practical routes:

- **A. Qualify as a broker.** Licence + MLS membership in each market. Cheapest
  per market, slowest, and you carry the compliance obligations.
- **B. Vendor under a sponsoring broker.** Apply as a technology provider; a
  participating broker authorises the feed (three-way agreement). Typical for
  software products.
- **C. Partner with a licensed brokerage.** They hold the seat, you build the
  tool. Fastest to real data; the licence stays theirs and so do the limits.
- **D. Skip MLS entirely.** County records + investor data + manual discovery.
  Zero licence, no true DOM, no authoritative sold prices.

## Coverage: six markets, six boards

| Market | MLS | Board | Notes |
|---|---|---|---|
| **Cleveland** | Yes MLS (ex-MLS Now / NEOHREX, merged with CRIS) | Yes MLS | Largest Ohio MLS, ~12,500 members, 2m+ listings to 1991, 32 counties |
| **Akron** | **Yes MLS — same board as Cleveland** | Yes MLS | **One licence covers both** |
| **Columbus** | Columbus REALTORS® (CBOR) | Columbus REALTORS | Separate licence |
| **Dayton** | Dayton Area Board of REALTORS® (DABR) | DABR | Separate licence |
| **Birmingham** | Greater Alabama MLS (GALMLS) | Birmingham AOR | Separate licence. RETS→WebAPI migration; some vendor listings still show RETS |
| **Atlanta** | FMLS **and** GAMLS | FMLS (Bridge) / GAMLS | Two competing boards over one metro. FMLS = $250 application fee (waived for member brokerages) + per-subscriber monthly tiers; GAMLS = statewide 159 counties |

**Six markets = five or six licences, not one.** Cleveland and Akron share a
board, which is the only favourable accident here.

### Published / reported cost signals

| Item | Reported figure | Confidence |
|---|---|---|
| Trestle connection fee | ~$85/mo per MLS | Vendor-stated (2021), widely repeated |
| MLS-side licence fee | $0–$200/mo typical; higher for vendor/public-display use | Varies by board, not published |
| Setup fee | $50–$250/feed; GNMLS cites $500 setup + $200/mo + $10,000 liquidated damages for vendor display | Board-specific |
| FMLS | $250 application fee; monthly fee per subscribed member, tiered | Board-published |
| MLS Grid vendor | $250/mo feed + $20/mo per licence | Board-published |
| ATTOM Basic Property API | From ~$95–$500/mo depending on endpoint | Reseller-reported; confirm in writing |
| PropStream | $99/mo Essentials | Published |
| BatchData | ~$1,000/mo for 100k records tier | Published tier |

Do **not** treat any of these as a quote. Every MLS must confirm in writing:
scope, statuses included, sold/off-market depth, photo rights, refresh rate,
whether the licence covers an automated valuation product, and whether derived
output may be shown to third parties.

## Photos — what "where licensed" actually means

- MLS media is licensed **for display of that listing**, not as a reusable asset.
  Use in a mailer, ad, or investor deck is not covered.
- Photos may be used for **internal condition analysis** — that is valuation
  support under Policy 7.90 — but do not republish them.
- Some MLSs strip media from statistics feeds (Trestle's Statistics feed has no
  photos) or from expired listings.
- `condition.md` already says photos cannot prove roof, foundation, wiring or
  plumbing. Licensing does not change what a photo can prove.

## What does not exist, so stop looking

| Myth | Reality |
|---|---|
| "Zillow has a public API" | Retired 30 Sep 2021; all ZWSID keys dead. Official route is Bridge, which is MLS-gated |
| "Redfin has an API" | No public API |
| "This $5/1,000-call Zillow API" | Unlicensed scraping resold. Breaches Zillow's ToS; no rights pass to you |
| "RESO can give me credentials" | RESO sells no data; it publishes standards |
| "One licence covers the country" | ~489 MLS systems, each licensing separately |

## The recommendation

### Now — no licence, no spend

Keep exactly what the repo already does, with Zillow as the manual discovery
reference and Redfin as the cross-check. Add county records (Cuyahoga, Summit,
Franklin, Montgomery, Jefferson AL, Fulton GA) as the hard-fact and outreach
plane. Everything stays labelled `REPORTED`, which is honest and sufficient for
screening.

### Next — one licence, one market

Your 18-ZIP universe is entirely Akron. Buy **Yes MLS** (IDX Plus or VOW) and
you cover Akron *and* Cleveland with a single board relationship. That converts
comps from `REPORTED` to `VERIFIED`, supplies real DOM, and gives the ARV engine
authoritative sold prices — the single biggest quality jump available.

Route: **B (vendor under a sponsoring broker)** if you are building tooling;
**A** if you intend to hang your own licence. Confirm in writing that the licence
permits an automated valuation product before paying.

### Later — only when a deal is actually in front of you

Columbus, Dayton, Birmingham, Atlanta are separate boards and separate recurring
fees. Do not buy four licences for markets with no pipeline. The workflow scans
by ZIP; when the universe grows to those metros, licence then.

### Never

- Scraping resellers marketed as "Zillow API".
- Using an MLS/IDX feed to build solicitation lists or to prospect
  expired/withdrawn listings in mass. That forfeits the feed and, under the
  liquidated-damages clauses some boards publish, costs more than the data.
- Calling a data plan "MLS access" when it is a consumer portal being read.

## Adding a source — checklist

1. Which of the seven required capabilities does it actually supply? (active,
   history/reductions, DOM, characteristics, photos, sold comps, ZIP search, export)
2. Is the licence per-market or national, and at what recurring cost?
3. Does the licence permit an **automated valuation product**? Get it in writing.
4. Does it permit **outreach**, or only display/valuation? Most MLS feeds: no.
5. What is the refresh rate, and does the feed drop expired/withdrawn?
6. What happens to derived data at termination? Must you purge it?
7. Record the answer in `state/` with a date. Prices and scopes drift.

## Sources

- NAR Handbook on Multiple Listing Policy — model rules §4.4.1, §13, §16.2.2, §18.3, §19.15; Policy 7.90 (valuation), 8.3 (participant data feed), 8.7 (BBO)
- NAR IDX policy and VOW policy
- FMLS Marketplace Info (fmls.com/marketplace-info) — $250 application fee, Bridge delivery, RESO Platinum
- CoreLogic Trestle documentation for MLS managers and technology providers
- MLS Grid / OneKey MLS data delivery resources — $250/mo + $20/licence
- GNMLS IDX/data feed terms — vendor display $200/mo, $500 setup, $10,000 liquidated damages
- RESO certification and MLS registry (489 MLS systems, ~90% Web API certified)
- RealEstateToolkit / apis.io / MLS Import — Trestle ~$85/mo per MLS, fee variance by board
- PropStream, BatchData, ATTOM published tiers as resale-priced references
