import json, re, sys
from urllib.parse import urljoin, urlparse
import requests
from bs4 import BeautifulSoup
BASE='https://deploy-preview-2--gregarious-malabi-0dc7e1.netlify.app'; PROD='https://osaraclinics.com'
ROUTES=['/','/dermatology','/ophthalmology','/doctors/dr-osama-alwreikat','/doctors/dr-sara-abu-touq','/psoriasis-treatment','/acne-scar-treatment','/vitiligo-jordan','/botox-hyperhidrosis','/mole-removal','/school-health']
EXISTING=['/','/dermatology','/ophthalmology','/doctors/dr-osama-alwreikat','/doctors/dr-sara-abu-touq','/vitiligo-jordan','/botox-hyperhidrosis','/mole-removal','/school-health']
EXPECTED={r:PROD+r for r in ROUTES}; EXPECTED['/']=PROD+'/'
s=requests.Session(); s.headers['User-Agent']='OSara-PR2-final-validator/1.0'
errors=[]; pages={}; titles=[]; descs=[]
for r in ROUTES:
 resp=s.get(BASE+r,allow_redirects=False,timeout=20); soup=BeautifulSoup(resp.text,'html.parser'); pages[r]=soup
 if resp.status_code!=200: errors.append(f'{r} clean status {resp.status_code}')
 title=soup.title.get_text(strip=True) if soup.title else ''; md=soup.find('meta',attrs={'name':'description'}); desc=md.get('content','') if md else ''
 c=soup.find('link',rel='canonical'); canonical=c.get('href') if c else None; o=soup.find('meta',attrs={'property':'og:url'}); og=o.get('content') if o else None
 robots=soup.find('meta',attrs={'name':'robots'}); robots=robots.get('content','') if robots else ''
 if not title or not desc: errors.append(f'{r} missing title/description')
 if len(soup.find_all('h1'))!=1: errors.append(f'{r} h1 count {len(soup.find_all("h1"))}')
 if canonical!=EXPECTED[r]: errors.append(f'{r} canonical {canonical}')
 if og!=EXPECTED[r]: errors.append(f'{r} og {og}')
 if 'noindex' in robots.lower(): errors.append(f'{r} noindex')
 for ld in soup.find_all('script',type='application/ld+json'):
  try: json.loads(ld.string or ld.get_text())
  except Exception as e: errors.append(f'{r} invalid JSON-LD {e}')
 titles.append((r,title)); descs.append((r,desc))
 if r!='/' and r not in ['/psoriasis-treatment','/acne-scar-treatment']:
  slash=s.get(BASE+r+'/',allow_redirects=True,timeout=20)
  if slash.status_code!=200 or urlparse(slash.url).path!=r: errors.append(f'{r} slash behavior {slash.status_code} {slash.url}')
 if r!='/' and r in ['/psoriasis-treatment','/acne-scar-treatment','/vitiligo-jordan','/botox-hyperhidrosis','/mole-removal','/school-health']:
  html=s.get(BASE+r+'.html',allow_redirects=False,timeout=20)
  if html.status_code!=200: errors.append(f'{r}.html behavior changed: {html.status_code}')
for field,data in [('title',titles),('description',descs)]:
 vals=[v for _,v in data]
 if len(vals)!=len(set(vals)): errors.append(f'duplicate {field} found')
for r in ['/psoriasis-treatment','/acne-scar-treatment']:
 raw=''.join(x.string or x.get_text() for x in pages[r].find_all('script',type='application/ld+json'))
 for needle in ['https://osaraclinics.com/#clinic','https://osaraclinics.com/doctors/dr-osama-alwreikat#physician','https://osaraclinics.com/dermatology#webpage']:
  if needle not in raw: errors.append(f'{r} missing entity {needle}')
rob=s.get(BASE+'/robots.txt',timeout=20)
if rob.status_code!=200 or 'Sitemap: https://osaraclinics.com/sitemap.xml' not in rob.text: errors.append('robots invalid')
sm=s.get(BASE+'/sitemap.xml',timeout=20); locs=re.findall(r'<loc>(.*?)</loc>',sm.text); expected_locs=[EXPECTED[r] for r in ROUTES]
if sm.status_code!=200 or locs!=expected_locs: errors.append(f'sitemap mismatch: {locs}')
seen=set()
for r,soup in pages.items():
 for a in soup.find_all('a',href=True):
  href=a['href']
  if href.startswith(('#','tel:','mailto:','https://wa.me','https://www.google.com','http://','https://')): continue
  path=urlparse(urljoin(BASE+r,href)).path
  if not path or path in seen: continue
  seen.add(path); rr=s.get(BASE+path,allow_redirects=True,timeout=20)
  if rr.status_code>=400: errors.append(f'broken internal {r}->{path}: {rr.status_code}')
req={'/dermatology':['/psoriasis-treatment','/acne-scar-treatment','/vitiligo-jordan','/botox-hyperhidrosis','/mole-removal'],'/':['/psoriasis-treatment','/acne-scar-treatment'],'/vitiligo-jordan':['/dermatology','/psoriasis-treatment','/acne-scar-treatment'],'/botox-hyperhidrosis':['/dermatology','/psoriasis-treatment','/acne-scar-treatment'],'/mole-removal':['/dermatology','/psoriasis-treatment','/acne-scar-treatment']}
for r,needed in req.items():
 hrefs=[a.get('href') for a in pages[r].find_all('a',href=True)]
 for n in needed:
  if n not in hrefs: errors.append(f'{r} missing link {n}')
for r in EXISTING:
 rr=s.get(PROD+r,allow_redirects=False,timeout=20)
 if rr.status_code!=200: errors.append(f'production regression {r}: {rr.status_code}')
www=s.get('https://www.osaraclinics.com/',allow_redirects=False,timeout=20)
if www.status_code not in (301,302,307,308) or not www.headers.get('location','').startswith(PROD): errors.append(f'www redirect unexpected {www.status_code} {www.headers.get("location")}')
report={'routes':ROUTES,'titles':titles,'sitemap_count':len(locs),'internal_paths_checked':sorted(seen),'errors':errors}
open('http-report.json','w').write(json.dumps(report,ensure_ascii=False,indent=2)); print(json.dumps(report,ensure_ascii=False,indent=2))
if errors: sys.exit(1)
