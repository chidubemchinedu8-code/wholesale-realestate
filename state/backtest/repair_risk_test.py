"""The decision test above assumed repairs cancel out.  They don't.

profit = ARV_true - 0.70*ARV_est  ONLY IF the repairs we budgeted equal the
repairs actually needed.  Repair scope error is asymmetric: you cannot spend
less than zero, but a 1905 house with window units can eat $30k nobody saw.
"""
import statistics as st

# the same 39 deals, from decision_test
import subprocess, json
PY_DEALS=None

# recompute inline (kept independent so this file stands alone)
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
import datetime as dt
D=lambda m: dt.datetime.utcfromtimestamp(m/1000).date()
sales=sorted([{"sf":s,"p":p,"date":D(m),"ppsf":p/s} for s,p,m in RAW],key=lambda r:r["date"])
use=[r for r in sales if r["ppsf"]<=250]

# moderate tier on the subject's own scale: $35/sf
REPAIR_RATE=35
deals=[]
for t in use:
    pool=[c["ppsf"] for c in use
          if c["date"]<t["date"] and (t["date"]-c["date"]).days<=365
          and abs(c["sf"]-t["sf"])/t["sf"]<=.30]
    if len(pool)<3: continue
    est=t["sf"]*st.median(pool)
    rep=t["sf"]*REPAIR_RATE
    deals.append({"sf":t["sf"],"est":est,"true":t["p"],"rep":rep})

print("="*76)
print("ADDING REPAIR-SCOPE RISK (the assumption I got wrong)")
print("="*76)
print(f"  repairs budgeted at ${REPAIR_RATE}/sf of living area (moderate tier)\n")
print(f"  {'repair overrun':>16} {'profitable':>12} {'median return':>15}")
for over in [0.0,0.15,0.25,0.50,1.00]:
    rets=[]
    for d in deals:
        p=0.70*d["est"]-d["rep"]-10000          # what we'd pay
        spend=d["rep"]*(1+over)                 # what we'd actually spend
        profit=d["true"]-p-spend-10000
        rets.append(profit/d["true"])
    win=sum(1 for r in rets if r>0)/len(rets)
    print(f"  {over:>15.0%} {win:>11.0%} {st.median(rets):>+14.1%}")

print("\n"+"="*76)
print("WHY THIS IS THE REAL RISK, NOT THE ARV ERROR")
print("="*76)
print("""  ARV error is symmetric: the backtest's median bias was -1.1%.
  Repair error is a one-way ratchet. You cannot 'come in under' a gutted
  1905 kitchen by 30% - the floor is zero and the ceiling is open.

  At $35/sf on a 1,440 sf subject the budget is $50,400.
  A 50% overrun is $25,200 of pure loss, on a deal whose entire MAO is $9,530.""")
