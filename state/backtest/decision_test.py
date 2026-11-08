"""Does the 70% rule survive a 40%-error ARV?  Decision-level backtest.

Underwriting: we offer  P = 0.70*ARV_est - repairs - $10k fee
Realised:     sell at  ARV_true, spend repairs, pay fee
  profit = ARV_true - P - repairs - fee
         = ARV_true - 0.70*ARV_est        <- repairs and fee cancel by design

So the whole strategy reduces to: is the true value at least 70% of our estimate?
Break-even error is +42.9%.  Everything above that loses money, no matter how
well the repairs are scoped.
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

deals=[]
for t in use:
    pool=[c["ppsf"] for c in use
          if c["date"]<t["date"] and (t["date"]-c["date"]).days<=365
          and abs(c["sf"]-t["sf"])/t["sf"]<=.30]
    if len(pool)<3: continue
    est=t["sf"]*st.median(pool)
    profit=t["p"]-0.70*est          # repairs + fee cancel
    deals.append({"sf":t["sf"],"est":est,"true":t["p"],
                  "profit":profit,"ret":profit/t["p"]})

print("="*76)
print("DECISION TEST - the 70% rule against 39 real outcomes")
print("="*76)
wins=[d for d in deals if d["profit"]>0]
losses=[d for d in deals if d["profit"]<=0]
print(f"\n  deals taken                  {len(deals)}")
print(f"  profitable                   {len(wins)}  ({len(wins)/len(deals):.0%})")
print(f"  lost money                   {len(losses)}  ({len(losses)/len(deals):.0%})")
print(f"\n  median return on value       {st.median([d['ret'] for d in deals]):+.1%}")
print(f"  mean   return on value       {st.mean([d['ret'] for d in deals]):+.1%}")
print(f"  best deal                    {max(d['ret'] for d in deals):+.0%}")
print(f"  worst deal                   {min(d['ret'] for d in deals):+.0%}")

print(f"\n  worst loss in dollars (on a typical $80k house):")
worst=min(deals,key=lambda d:d["ret"])
print(f"    est ${worst['est']:,.0f} vs true ${worst['true']:,.0f}"
      f"  ->  ${worst['profit']:,.0f}  ({worst['ret']:+.0%})")

# how much does the loss tail cost?
print(f"\n  If you did all {len(deals)} deals, total P&L: "
      f"${sum(d['profit'] for d in deals):,.0f}")
print(f"  Two worst deals alone: "
      f"${sum(sorted([d['profit'] for d in deals])[:2]):,.0f}")

# sensitivity: what 70%-equivalent is actually safe?
print("\n"+"="*76)
print("SENSITIVITY - what buy ratio would have been safe?")
print("="*76)
for ratio in [0.70,0.65,0.60,0.55,0.50]:
    res=[d["true"]-ratio*d["est"] for d in deals]
    win=sum(1 for r in res if r>0)/len(res)
    print(f"  buy at {ratio:.0%} of ARV:  profitable {win:.0%} of deals"
          f"   median return {st.median([r/d['true'] for r,d in zip(res,deals)]):+.1%}")
