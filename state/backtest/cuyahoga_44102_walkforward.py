"""Walk-forward backtest of the comp.py ARV method against actual Cuyahoga sales.

Ground truth = the recorded sale price (sales_amount), NOT the county's appraised
value.  Each sale is priced using only sales that CLOSED BEFORE it, within 12
months, +-30% living area, >=3 comps, median $/sf -- i.e. comp.py's rules.
"""
import statistics as st, datetime as dt, json

# (living_area, sale_price, epoch_ms) -- Cuyahoga CAMA, 1-FAMILY PLATTED LOT, 44102
RAW = [
(1512,70000,1736174100000),(1056,60000,1737751740000),(1500,146000,1738341780000),
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
(1507,76000,1770820560000),
]

def d(ms): return dt.datetime.utcfromtimestamp(ms/1000).date()

sales=[{"sf":s,"p":p,"date":d(m),"ppsf":p/s} for s,p,m in RAW]
sales.sort(key=lambda r:r["date"])

# Arms-length screen.  County data carries no transaction-type flag, so portfolio
# / estate / related-party transfers have to be screened on $/sf alone.
def arms_length(r, hi=250.0):
    return r["ppsf"] <= hi

def backtest(screen=True, band=0.30, window=365, minn=3):
    use=[r for r in sales if (arms_length(r) if screen else True)]
    out=[]
    for tgt in use:
        pool=[c for c in use
              if c["date"] < tgt["date"]
              and (tgt["date"]-c["date"]).days <= window
              and abs(c["sf"]-tgt["sf"])/tgt["sf"] <= band]
        if len(pool) < minn:
            out.append({"addr":None,"sf":tgt["sf"],"actual":tgt["p"],"est":None,
                        "n":len(pool),"date":tgt["date"]}); continue
        pp=st.median([c["ppsf"] for c in pool])
        est=tgt["sf"]*pp
        out.append({"sf":tgt["sf"],"actual":tgt["p"],"est":est,"n":len(pool),
                    "date":tgt["date"],"err":(est-tgt["p"])/tgt["p"]})
    return out

def report(name,res):
    priced=[r for r in res if r["est"] is not None]
    errs=[r["err"] for r in priced]
    ae=[abs(e) for e in errs]
    if not ae: print(name,"no results"); return
    within10=sum(1 for e in ae if e<=0.10)/len(ae)
    within15=sum(1 for e in ae if e<=0.15)/len(ae)
    within20=sum(1 for e in ae if e<=0.20)/len(ae)
    print(f"\n{name}")
    print(f"  sales evaluated      {len(res)}")
    print(f"  priced (n>=3 comps)  {len(priced)}  ({len(priced)/len(res):.0%})")
    print(f"  NO CALL              {len(res)-len(priced)}")
    print(f"  median abs error     {st.median(ae):.1%}")
    print(f"  mean abs error       {st.mean(ae):.1%}")
    print(f"  median signed bias   {st.median(errs):+.1%}")
    print(f"  within +-10%         {within10:.0%}")
    print(f"  within +-15%         {within15:.0%}")
    print(f"  within +-20%         {within20:.0%}")
    print(f"  worst miss           {max(ae):.0%}")
    return {"n":len(res),"priced":len(priced),"mape":st.median(ae),
            "bias":st.median(errs),"w10":within10,"w15":within15,"w20":within20}

print("="*72)
print("WALK-FORWARD BACKTEST - Cuyahoga 44102, 1-family platted lots")
print("Each sale priced only from sales closed BEFORE it, <=12mo, +-30% sf, n>=3")
print("="*72)

a=report("A. WITH arms-length screen ($/sf <= $250)", backtest(screen=True))
b=report("B. NO screen (raw county data, incl. portfolio transfers)", backtest(screen=False))
c=report("C. screen + tighter +-20% sf band", backtest(screen=True, band=0.20))
d2=report("D. screen + wider +-40% sf band", backtest(screen=True, band=0.40))

json.dump({"A":a,"B":b,"C":c,"D":d2}, open("state/backtest/walkforward_result.json","w"), indent=2)

print("\n"+"="*72)
print("THE FLIP TEST - what the method would have said")
print("="*72)
for name,pid in [("3235 W 94th (bought $60k 2026-01-14)",(1220,60000,1768503780000))]:
    r=backtest(screen=True)
    for x in r:
        if abs(x["sf"]-pid[0])<1 and abs(x["actual"]-pid[1])<1:
            print(f"  {name}: n={x['n']} comps -> estimate ${x['est']:,.0f} vs actual ${x['actual']:,.0f}")

print("\n"+"="*72)
print("DECOMPOSITION - where does the error come from?")
print("="*72)
res=[r for r in backtest(screen=True) if r["est"]]
import collections
pp=sorted(c["ppsf"] for c in sales if arms_length(c))
med=st.median(pp)
print(f"\n$/sf distribution (n={len(pp)}): min ${pp[0]:.0f}  q1 ${pp[len(pp)//4]:.0f}  "
      f"median ${med:.0f}  q3 ${pp[3*len(pp)//4]:.0f}  max ${pp[-1]:.0f}")
print(f"ratio q3/q1 = {pp[3*len(pp)//4]/pp[len(pp)//4]:.1f}x  <- spread within ONE zip, one property class")

hi=[r for r in res if r["actual"]/r["sf"] >= med]
lo=[r for r in res if r["actual"]/r["sf"] <  med]
for label,grp in [("SUBJECT SOLD ABOVE median $/sf (retail/renovated proxy)",hi),
                  ("SUBJECT SOLD BELOW median $/sf (distressed/dated proxy)",lo)]:
    ae=[abs(r["err"]) for r in grp]
    print(f"\n  {label}")
    print(f"    n={len(grp)}  median abs err {st.median(ae):.1%}  mean {st.mean(ae):.1%}")
    print(f"    within +-20%: {sum(1 for e in ae if e<=.20)/len(ae):.0%}"
          f"   median signed bias {st.median([r['err'] for r in grp]):+.1%}")

print("\n"+"="*72)
print("CONDITION CHANNEL - what a 40% error actually means in dollars")
print("="*72)
print("  1,440 sf subject.  Comp band $90/sf vs $120/sf:")
print(f"    ARV at $90/sf  = ${1440*90:,.0f}")
print(f"    ARV at $120/sf = ${1440*120:,.0f}")
print(f"    difference     = ${1440*30:,.0f}  <- larger than the whole $99,900 asking price")
