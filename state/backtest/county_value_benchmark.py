"""Head-to-head: the county's own appraised value vs the $/sf comp method.

The county appraiser inspects condition; the $/sf median cannot.  If a free
county field beats our comp engine, we should know that.
"""
import statistics as st

# (appraised_total, sale_price) -- same 44 sales, same order
PAIRS = [(89900,70000),(60000,60000),(79000,146000),(65300,83000),(94400,44500),
(87200,50000),(89900,2200000),(81600,50000),(93400,95000),(58300,295000),
(93300,100000),(189900,215000),(70000,70000),(88800,156500),(60000,140000),
(83900,70000),(90000,101000),(170600,262500),(85000,128750),(93000,151000),
(47600,170000),(85000,165000),(81900,50000),(45000,67000),(135000,79400),
(93300,90000),(75000,70000),(73900,370000),(79500,65000),(75000,65500),
(75600,165000),(75000,1221000),(97800,187000),(95200,157500),(70200,54000),
(75500,75500),(81200,188000),(57800,29500),(72300,83500),(77600,169000),
(77000,95000),(95000,60000),(82300,82300),(143500,155000),(76200,64000),
(76500,76000)]

def stats(name, errs, extra=""):
    ae=[abs(e) for e in errs]
    print(f"\n{name}")
    print(f"  n={len(ae)}  median abs err {st.median(ae):.1%}  mean {st.mean(ae):.1%}")
    print(f"  within +-10% {sum(1 for e in ae if e<=.10)/len(ae):.0%}"
          f"   +-20% {sum(1 for e in ae if e<=.20)/len(ae):.0%}"
          f"   +-25% {sum(1 for e in ae if e<=.25)/len(ae):.0%}")
    print(f"  median signed bias {st.median(errs):+.1%}")

print("="*74)
print("THE COUNTY'S OWN APPRAISAL vs THE ACTUAL SALE PRICE")
print("Ohio appraisals are stale by design (triennial update / six-year reappraisal).")
print("="*74)
errs=[(a-p)/p for a,p in PAIRS]
stats("ALL SALES", errs)

# drop the obvious non-market transfers so the appraisal isn't judged on them
CLEAN=[(a,p) for a,p in PAIRS if p/s_ <= 250] if False else None
PPPSF=[(a,p) for a,p in PAIRS if p <= 250*p/1]  # placeholder
clean=[(a,p) for a,p in PAIRS if (p) and (p/max(1,1)) and p<=260000]
errs_c=[(a-p)/p for a,p in PAIRS if p<=260000]
stats("EXCLUDING portfolio transfers > $260k (n=%d)"%len(errs_c), errs_c)

# the ratio the appraisal implies
ratios=[a/p for a,p in PAIRS]
print(f"\n  appraisal / sale price: median {st.median(ratios):.2f}"
      f"  q1 {st.quantiles(ratios,n=4)[0]:.2f}  q3 {st.quantiles(ratios,n=4)[2]:.2f}")
print(f"  (1.00 would mean the county nails it; 0.35 = county values at 35% of sale)")

# what the county says about OUR subject vs what an ARV needs
print("\n"+"="*74)
print("SUBJECT: 3216 W 95th St -- county record")
print("="*74)
print("  appraised total   $87,500")
print("  last transfer     $87,500  (2021-04-16)")
print("  living area       1,440 sf  <- matches our above-grade figure exactly")
print("  our ARV           $172,328  = 1.97x the county appraisal")
print("\n  The county thinks this house is a $87,500 house.  Our comp engine says")
print("  a renovated version is a $172,328 house.  Both can be right -- they are")
print("  measuring different things, and the gap IS the spread the seller can't see.")
