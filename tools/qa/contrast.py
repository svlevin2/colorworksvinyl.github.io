#!/usr/bin/env python3
"""WCAG contrast for every text/background token pair used in styles.css. Exit 1 if any text pair < 4.5 (or < 3 for large/UI)."""
import sys
def lum(h):
    h=h.lstrip('#'); c=[int(h[i:i+2],16)/255 for i in (0,2,4)]
    c=[x/12.92 if x<=0.04045 else ((x+0.055)/1.055)**2.4 for x in c]
    return 0.2126*c[0]+0.7152*c[1]+0.0722*c[2]
def ratio(a,b):
    la,lb=sorted([lum(a),lum(b)],reverse=True); return (la+0.05)/(lb+0.05)
PAIRS=[('body navy on white','#00204A','#FFFFFF',4.5),('body navy on cream','#00204A','#F8F4EF',4.5),
 ('muted on white','#3E4C63','#FFFFFF',4.5),('muted on cream','#3E4C63','#F8F4EF',4.5),
 ('white on navy (buttons, dark sections)','#FFFFFF','#00204A',4.5),('on-dark muted on navy','#C9D2DF','#00204A',4.5),
 ('navy on white button (dark section)','#00204A','#FFFFFF',4.5),('focus ring navy on white (UI)','#00204A','#FFFFFF',3.0),('focus ring navy on cream (UI)','#00204A','#F8F4EF',3.0),
 ('focus ring white on navy (UI)','#FFFFFF','#00204A',3.0),('navy icon on cream badge (UI)','#00204A','#F8F4EF',3.0)]
bad=0
for n,f,b,need in PAIRS:
    r=ratio(f,b); ok=r>=need; bad+=not ok
    print(f"{'PASS' if ok else 'FAIL'} {r:5.2f}:1 (need {need}) {n} {f} on {b}")
print(f'SUMMARY contrast pairs={len(PAIRS)} fails={bad} min={min(ratio(f,b) for _,f,b,_ in PAIRS):.2f}')
sys.exit(1 if bad else 0)
