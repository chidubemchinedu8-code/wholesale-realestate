"""Does comp.py's TIGHT/WIDE confidence badge predict accuracy?

comp.py: confidence = TIGHT if (p75-p25)/median <= 25%.
Claim under test: a tight comp set implies a reliable ARV.
"""
import statistics as st, datetime as dt

RAW=[(1512,70000,1736174100000),(1056,60000,1737751740000),(1500,146000,1738341780000),
(1363,83000,1738676460000),(1258,44500,1738939620000),(1612,50000,1741036260000),
(1361,2200000,1741285260000),(1694,50000,1743080160000),(1294,95000,1743187320000),
(1320,295000,1743900120000),(1275,100000,1744054260000),(1628,215000,1745866620000),
(993,70000,1746118080000),(1176,156500,1748532600000),(1208,140000,1749475020000),
(1194,70000,1751000760000),(1311,101000,1752603780000),(2384,262500,1752691560000),
(1247,128750,1753392540000),(1268,151000,1753454220000),(1360,170000,1753469520000),
(1182,165000,1753715160000),(1134,50000,1754670480000),(1411,67000,1754681880000),
(1196,79400,1755694320000),(1521,90000,1755891540000),(1425,70000,1757540220000),
(896,370000,1758199860000),(1081,65000,1758894120000),(1398,65500,1762267140000),
(939,165000,1763043420000),(1052,1221000,1763155080000),(1618,187000,1763393760000),
(1307,157500,1763650140000),(1196,54000,1763997420000),(1161,75500,1764079620000),
(1481,188000,1764706200000),(1020,29500,1765983960000),(1255,83500,1766512620000),
(1554,169000,1767042840000),(1049,95000,1767647100000),(1220,60000,1768503780000),
(1188,82300,1769103900000),(1980,155000,1769195340000),(1408,64000,1770055740000),
(1507,76000,1770820560000)]
D=lambda m: dt.datetime.utcfromtimestamp(m/1000).date()
sales=sorted([{"sf":s,"p":p,"date":D(m),"ppsf":p/s} for s,p,m in RAW],key=lambda r:r["date"])
use=[r for r in sales if r["ppsf"]<=250]

def p25_p75(v):
    v=sorted(v); n=len(v)
    def q(f):
        i=f*(n-1); lo=int(i); hi=min(lo+1,n-1); return v[lo]+(v[hi]-v[lo])*(i-lo)
    return q(.25),q(.75)

rows=[]
for t in use:
    pool=[c["ppsf"] for c in use
          if c["date"]<t["date"] and (t["date"]-c["date"]).days<=365
          and abs(c["sf"]-t["sf"])/t["sf"]<=.30]
    if len(pool)<3: continue
    med=st.median(pool); a,b=p25_p75(pool)
    spread=(b-a)/med*100
    est=t["sf"]*med
    rows.append({"n":len(pool),"spread":spread,"err":(est-t["p"])/t["p"]})

print("="*74)
print("DOES 'TIGHT' PREDICT ACCURACY?")
print("="*74)
tight=[r for r in rows if r["spread"]<=25]
wide=[r for r in rows if r["spread"]>25]
for name,g in [("TIGHT sets (<=25% spread)",tight),("WIDE sets (>25%)",wide)]:
    if not g: print(f"\n{name}: none"); continue
    ae=[abs(r["err"]) for r in g]
    print(f"\n{name}")
    print(f"  n={len(g)}  median abs err {st.median(ae):.1%}  mean {st.mean(ae):.1%}")
    print(f"  within +-20%: {sum(1 for e in ae if e<=.20)/len(ae):.0%}")

print(f"\n  {len(tight)}/{len(rows)} = {len(tight)/len(rows):.0%} of all comp sets "
      f"badged TIGHT.  Worst error among them: {max(abs(r['err']) for r in tight):.0%}")

# how often is a 3-comp set TIGHT, by construction?
three=[r for r in rows if r["n"]==3]
if three:
    print(f"\n  Of {len(three)} sets with exactly 3 comps, "
          f"{sum(1 for r in three if r['spread']<=25)} are TIGHT"
          f" ({sum(1 for r in three if r['spread']<=25)/len(three):.0%}).")
    print(f"  Their median abs error: {st.median([abs(r['err']) for r in three]):.1%}")

# correlation between spread and accuracy
xs=[r["spread"] for r in rows]; ys=[abs(r["err"]) for r in rows]
mx,my=st.mean(xs),st.mean(ys)
cov=sum((x-mx)*(y-my) for x,y in zip(xs,ys))
den=(sum((x-mx)**2 for x in xs)*sum((y-my)**2 for y in ys))**.5
print(f"\n  correlation(spread, |error|) = {cov/den:+.3f}")
print("  -> if ~0 or positive, a tight comp set tells you NOTHING about accuracy.")
