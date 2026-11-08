"""Does tightening geography fix the error?  Same-street comps are the limit case."""
import statistics as st, datetime as dt

# (street, living_area, sale_price, epoch_ms)
RAW=[("DENISON",1512,70000,1736174100000),("88",1056,60000,1737751740000),
("88",1500,146000,1738341780000),("95",1363,83000,1738676460000),
("84",1258,44500,1738939620000),("92",1612,50000,1741036260000),
("94",1361,2200000,1741285260000),("95",1694,50000,1743080160000),
("84",1294,95000,1743187320000),("92",1320,295000,1743900120000),
("94",1275,100000,1744054260000),("CLARK",1628,215000,1745866620000),
("84",993,70000,1746118080000),("97",1176,156500,1748532600000),
("91",1208,140000,1749475020000),("99",1194,70000,1751000760000),
("94",1311,101000,1752603780000),("97",2384,262500,1752691560000),
("84",1247,128750,1753392540000),("88",1268,151000,1753454220000),
("88",1360,170000,1753469520000),("91",1182,165000,1753715160000),
("90",1134,50000,1754670480000),("94",1411,67000,1754681880000),
("90",1196,79400,1755694320000),("99",1521,90000,1755891540000),
("86",1425,70000,1757540220000),("91",896,370000,1758199860000),
("94",1081,65000,1758894120000),("92",1398,65500,1762267140000),
("ALMIRA",939,165000,1763043420000),("90",1052,1221000,1763155080000),
("DENISON",1618,187000,1763393760000),("86",1307,157500,1763650140000),
("BRINSMADE",1196,54000,1763997420000),("84",1161,75500,1764079620000),
("97",1481,188000,1764706200000),("95",1020,29500,1765983960000),
("86",1255,83500,1766512620000),("84",1554,169000,1767042840000),
("90",1049,95000,1767647100000),("94",1220,60000,1768503780000),
("94",1188,82300,1769103900000),("97",1980,155000,1769195340000),
("86",1408,64000,1770055740000),("90",1507,76000,1770820560000)]
D=lambda m: dt.datetime.utcfromtimestamp(m/1000).date()
sales=sorted([{"st":s,"sf":q,"p":p,"date":D(m),"ppsf":p/q} for s,q,p,m in RAW],
             key=lambda r:r["date"])
use=[r for r in sales if r["ppsf"]<=250]

def run(label, same_street=False, band=.30, minn=3):
    out=[]
    for t in use:
        pool=[c for c in use
              if c["date"]<t["date"] and (t["date"]-c["date"]).days<=365
              and abs(c["sf"]-t["sf"])/t["sf"]<=band
              and (c["st"]==t["st"] if same_street else True)]
        if len(pool)<minn:
            out.append(None); continue
        med_ppsf=st.median([c["ppsf"] for c in pool])
        out.append((med_ppsf*t["sf"],len(pool),t))   # BUG WAS HERE: $/sf never x sf
    priced=[o for o in out if o]
    if not priced:
        print(f"\n{label}\n  NO SALE PRICEABLE ({len(out)} evaluated)"); return
    ae=[abs(e/t["p"]-1) for e,n,t in priced]
    print(f"  [sanity] first estimate ${priced[0][0]:,.0f} vs actual ${priced[0][2]['p']:,.0f}")
    print(f"\n{label}")
    print(f"  priceable {len(priced)}/{len(out)}   median abs err {st.median(ae):.1%}"
          f"   within +-20% {sum(1 for e in ae if e<=.20)/len(ae):.0%}")

print("="*74)
print("DOES TIGHTER GEOGRAPHY HELP?")
print("="*74)
run("Same street only, n>=3 comps", same_street=True)
run("Same street only, n>=2 comps (relaxed)", same_street=True, minn=2)
run("Whole 44102 box, n>=3  (baseline)", )

# what actually differentiates same-street neighbours?
print("\n"+"="*74)
print("WHY SAME-STREET COMPS STILL DISAGREE")
print("="*74)
for st_name in ["94","90","86"]:
    rows=[r for r in use if r["st"]==st_name]
    print(f"\n  W {st_name} St, 2025-2026 sales, all 1-family platted lots in 44102:")
    for r in rows:
        print(f"    {r['date']}  {r['sf']:>5} sf  ${r['p']:>8,}  ${r['ppsf']:>6.0f}/sf")
    if rows:
        pp=[r["ppsf"] for r in rows]
        print(f"    -> ${min(pp):.0f} to ${max(pp):.0f}/sf on ONE street: "
              f"{max(pp)/min(pp):.1f}x range")
