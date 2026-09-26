#!/usr/bin/env python3
import json, os, urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; ASSETS=ROOT/'assets'
TOKEN=os.getenv('GITHUB_TOKEN'); USER=os.getenv('GITHUB_USERNAME','Prathmesh-2023')
query='''query($login:String!,$from:DateTime!,$to:DateTime!){user(login:$login){contributionsCollection(from:$from,to:$to){contributionCalendar{totalContributions,weeks{contributionDays{contributionCount,date}}}}}}'''
if not TOKEN: raise SystemExit('GITHUB_TOKEN missing')
today=datetime.now(timezone.utc).date(); start=today-timedelta(days=365)
payload=json.dumps({'query':query,'variables':{'login':USER,'from':f'{start}T00:00:00Z','to':f'{today}T23:59:59Z'}}).encode()
req=urllib.request.Request('https://api.github.com/graphql',data=payload,headers={'Authorization':f'bearer {TOKEN}','Content-Type':'application/json','User-Agent':'profile-generator'})
with urllib.request.urlopen(req,timeout=30) as r: result=json.load(r)
if result.get('errors'): raise SystemExit(result['errors'])
calendar=result['data']['user']['contributionsCollection']['contributionCalendar']
(ASSETS/'contributions.json').write_text(json.dumps(calendar,indent=2),encoding='utf-8')
print('Fetched',calendar['totalContributions'],'contributions')
