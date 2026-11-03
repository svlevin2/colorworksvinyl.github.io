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
PAIRS+=[('cyan-ink text on white', '#0A6A90', '#FFFFFF', 4.5), ('cyan-ink text on cream', '#0A6A90', '#F8F4EF', 4.5), ('cyan-ink text/icon on cyan tint', '#0A6A90', '#E3F4FA', 4.5), ('navy on cyan tint', '#00204A', '#E3F4FA', 4.5), ('muted on cyan tint', '#3E4C63', '#E3F4FA', 4.5), ('magenta-ink text on white', '#A3216A', '#FFFFFF', 4.5), ('magenta-ink text on cream', '#A3216A', '#F8F4EF', 4.5), ('magenta-ink text/icon on magenta tint', '#A3216A', '#FBE7F2', 4.5), ('navy on magenta tint', '#00204A', '#FBE7F2', 4.5), ('muted on magenta tint', '#3E4C63', '#FBE7F2', 4.5), ('purple-ink text on white', '#7234A8', '#FFFFFF', 4.5), ('purple-ink text on cream', '#7234A8', '#F8F4EF', 4.5), ('purple-ink text/icon on purple tint', '#7234A8', '#F2EAFA', 4.5), ('navy on purple tint', '#00204A', '#F2EAFA', 4.5), ('muted on purple tint', '#3E4C63', '#F2EAFA', 4.5), ('orange-ink text on white', '#A04600', '#FFFFFF', 4.5), ('orange-ink text on cream', '#A04600', '#F8F4EF', 4.5), ('orange-ink text/icon on orange tint', '#A04600', '#FFEEE0', 4.5), ('navy on orange tint', '#00204A', '#FFEEE0', 4.5), ('muted on orange tint', '#3E4C63', '#FFEEE0', 4.5), ('white on band gradient stop', '#FFFFFF', '#0A6A90', 4.5), ('white on band gradient stop', '#FFFFFF', '#7234A8', 4.5), ('white on band gradient stop', '#FFFFFF', '#A3216A', 4.5)]
bad=0
for n,f,b,need in PAIRS:
    r=ratio(f,b); ok=r>=need; bad+=not ok
    print(f"{'PASS' if ok else 'FAIL'} {r:5.2f}:1 (need {need}) {n} {f} on {b}")
print(f'SUMMARY contrast pairs={len(PAIRS)} fails={bad} min={min(ratio(f,b) for _,f,b,_ in PAIRS):.2f}')
sys.exit(1 if bad else 0)
