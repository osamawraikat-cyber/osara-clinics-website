import json, re, sys
from urllib.parse import urljoin, urlparse
import requests
from bs4 import BeautifulSoup

PREVIEW='https://osaraclinics.com'
PROD='https://osaraclinics.com'
MID='G-72BY7LC2V2'
ROUTES=['/','/dermatology','/ophthalmology','/doctors/dr-osama-alwreikat','/doctors/dr-sara-abu-touq','/psoriasis-treatment','/acne-scar-treatment','/vitiligo-jordan','/botox-hyperhidrosis','/mole-removal','/school-health']
EXPECTED={r:PROD+r for r in ROUTES}; EXPECTED['/']=PROD+'/'
s=requests.Session(); s.headers['User-Agent']='OSara-PR3-production-validator/1.0'
errors=[]; report={'routes':{},'broken_links':[],'broken_images':[]}

def meta(soup,name=None,prop=None):
    el=soup.find('meta',attrs={'name':name}) if name else soup.find('meta',attrs={'property':prop})
    return el.get('content') if el else None

for r in ROUTES:
    pr=s.get(PREVIEW+r,allow_redirects=False,timeout=30)
    po=s.get(PROD+r,allow_redirects=False,timeout=30)
    if pr.status_code!=200: errors.append(f'{r} production status {pr.status_code}')
    ps=BeautifulSoup(pr.text,'html.parser'); bs=BeautifulSoup(po.text,'html.parser')
    canonical=(ps.find('link',rel='canonical') or {}).get('href') if ps.find('link',rel='canonical') else None
    og=meta(ps,prop='og:url')
    if canonical!=EXPECTED[r]: errors.append(f'{r} canonical {canonical}')
    if og!=EXPECTED[r]: errors.append(f'{r} og {og}')
    for raw in [(x.string or x.get_text()).strip() for x in ps.find_all('script',type='application/ld+json')]:
        try: json.loads(raw)
        except Exception as e: errors.append(f'{r} invalid JSON-LD {e}')
    loaders=[x.get('src','') for x in ps.find_all('script',src=True) if 'googletagmanager.com/gtag/js' in x.get('src','')]
    if loaders!=[f'https://www.googletagmanager.com/gtag/js?id={MID}']:
        errors.append(f'{r} GA loader count/value {loaders}')
    inline='\n'.join((x.string or x.get_text()) for x in ps.find_all('script') if not x.get('src'))
    cfg_count=len(re.findall(r"gtag\(\s*['\"]config['\"]\s*,\s*['\"]G-72BY7LC2V2['\"]\s*\)",inline))
    if cfg_count!=1: errors.append(f'{r} GA config count {cfg_count}')
    if pr.text.count(MID)!=2: errors.append(f'{r} measurement ID occurrence count {pr.text.count(MID)}')
    if re.search(r'GTM-[A-Z0-9]+',pr.text): errors.append(f'{r} GTM container found')
    pfb=pr.text.count('connect.facebook.net') + pr.text.count('fbq(')
    report['routes'][r]={'status':pr.status_code,'canonical':canonical,'ga_loader_count':len(loaders),'ga_config_count':cfg_count,'meta_pixel_markers':pfb}

rob=s.get(PROD+'/robots.txt',timeout=30)
if rob.status_code!=200 or 'Sitemap: https://osaraclinics.com/sitemap.xml' not in rob.text: errors.append('robots regression')
sm=s.get(PROD+'/sitemap.xml',timeout=30)
locs=re.findall(r'<loc>(.*?)</loc>',sm.text)
if sm.status_code!=200 or locs!=[EXPECTED[r] for r in ROUTES]: errors.append(f'sitemap regression/count {len(locs)}')
report['sitemap_count']=len(locs)

seen_links=set(); seen_images=set()
for r in ROUTES:
    soup=BeautifulSoup(s.get(PROD+r,timeout=30).text,'html.parser')
    for a in soup.find_all('a',href=True):
        h=a['href']
        if h.startswith(('#','tel:','mailto:','javascript:','https://wa.me','https://www.google.com','https://maps.app.goo.gl','https://goo.gl/maps')): continue
        u=urljoin(PROD+r,h); pu=urlparse(u)
        if pu.netloc!=urlparse(PROD).netloc: continue
        p=pu.path or '/'
        if p in seen_links: continue
        seen_links.add(p)
        rr=s.get(PROD+p,allow_redirects=True,timeout=30)
        if rr.status_code>=400:
            errors.append(f'broken internal {r}->{p} {rr.status_code}'); report['broken_links'].append([r,p,rr.status_code])
    for im in soup.find_all('img',src=True):
        u=urljoin(PROD+r,im['src']); pu=urlparse(u)
        if pu.netloc!=urlparse(PROD).netloc: continue
        key=pu.path
        if key in seen_images: continue
        seen_images.add(key)
        rr=s.get(u,allow_redirects=True,timeout=30)
        if rr.status_code>=400:
            errors.append(f'broken image {key} {rr.status_code}'); report['broken_images'].append([key,rr.status_code])

for r in ROUTES[1:]:
    clean=s.get(PROD+r,allow_redirects=False,timeout=30)
    slash=s.get(PROD+r+'/',allow_redirects=False,timeout=30)
    html=s.get(PROD+r+'.html',allow_redirects=False,timeout=30)
    if clean.status_code!=200: errors.append(f'{r} clean status {clean.status_code}')
    if slash.status_code not in (301,302,307,308): errors.append(f'{r}/ unexpected status {slash.status_code}')
    if html.status_code!=200: errors.append(f'{r}.html unexpected status {html.status_code}')

# www normalization spot-checks root and representative route.
for r in ['/','/dermatology']:
    rr=s.get('https://www.osaraclinics.com'+r,allow_redirects=True,timeout=30)
    if rr.status_code!=200 or urlparse(rr.url).netloc!='osaraclinics.com': errors.append(f'www normalization failed {r}: {rr.status_code} {rr.url}')

report['errors']=errors
open('pr3-static.json','w').write(json.dumps(report,ensure_ascii=False,indent=2))
print(json.dumps(report,ensure_ascii=False,indent=2))
sys.exit(1 if errors else 0)
