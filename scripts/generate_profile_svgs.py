#!/usr/bin/env python3
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; ASSETS=ROOT/'assets'
p=ASSETS/'contributions.json'
if not p.exists(): raise SystemExit('contributions.json not found')
data=json.loads(p.read_text()); days=[d for w in data.get('weeks',[]) for d in w.get('contributionDays',[])][-364:]
maximum=max([d['contributionCount'] for d in days] or [1]); total=sum(d['contributionCount'] for d in days)
rects=[]
for i,d in enumerate(days):
    x=45+(i//7)*18; y=65+(i%7)*24; ratio=d['contributionCount']/maximum; op=.10+.85*ratio
    rects.append(f'<rect x="{x}" y="{y}" width="12" height="12" rx="3" fill="#58a6ff" fill-opacity="{op:.3f}"><animate attributeName="fill-opacity" values="{op:.3f};{min(1,op+.12):.3f};{op:.3f}" dur="3s" repeatCount="indefinite"/></rect>')
svg=f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 370"><rect width="100%" height="100%" rx="20" fill="#0d1117" stroke="#21262d"/><text x="42" y="36" fill="#8b949e" font-family="monospace" font-size="13">CONTRIBUTION SIGNAL // {total} CONTRIBUTIONS</text><g>{''.join(rects)}</g><text x="42" y="350" fill="#8b949e" font-family="monospace" font-size="11">LOW</text><text x="1110" y="350" fill="#8b949e" font-family="monospace" font-size="11">HIGH</text></svg>'''
(ASSETS/'contribution-neural.svg').write_text(svg,encoding='utf-8')
