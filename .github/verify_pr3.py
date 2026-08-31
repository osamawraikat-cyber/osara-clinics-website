import json, re, sys
from urllib.parse import urljoin, urlparse
import requests
from bs4 import BeautifulSoup

PREVIEW='https://deploy-preview-3--gregarious-malabi-0dc7e1.netlify.app'
PROD='https://osaraclinics.com'
MID='G-72BY7LC2V2'
ROUTES=['/','/dermatology','/ophthalmology','/doctors/dr-osama-alwreikat','/doctors/dr-sara-abu-touq','/psoriasis-treatment','/acne-scar-treatment','/vitiligo-jordan','/botox-hyperhidrosis','/mole-removal','/school-health']
EXPECTED={r:PROD+r for r in ROUTES}; EXPECTED['/']=PROD+'/'
s=requests.Session(); s.headers['User-Agent']='OSara-PR3-validator/1.0'
errors=[]; report={'routes':{},'broken_links':[],'broken_images':[]}

def meta(soup,name=None,prop=None):
    el=soup.find('meta',attrs={'name':name}) if name else soup.find('meta',attrs={'property':prop})
    return el.get('content') if el else None

for r in ROUTES:
    pr=s.get(PREVIEW+r,allow_redirects=False,timeout=30)
    po=s.get(PROD+r,allow_redirects=False,timeout=30)
    if pr.status_code!=200: errors.append(f'{r} preview status {pr.status_code}')
    if po.status_code!=200: errors.append(f'{r} production baseline status {po.status_code}')
    ps=BeautifulSoup(pr.text,'html.parser'); bs=BeautifulSoup(po.text,'html.parser')
    canonical=(ps.find('link',rel='canonical') or {}).get('href') if ps.find('link',rel='canonical') else None
    og=meta(ps,prop='og:url')
    if canonical!=EXPECTED[r]: errors.append(f'{r} canonical {canonical}')
    if og!=EXPECTED[r]: errors.append(f'{r} og {og}')
    # SEO/content fields must match production baseline exactly.
    ptitle=ps.title.get_text(strip=True) if ps.title else None
    btitle=bs.title.get_text(strip=True) if bs.title else None
    if ptitle!=btitle: errors.append(f'{r} title changed')
    if meta(ps,name='description')!=meta(bs,name='description'): errors.append(f'{r} meta description changed')
    if canonical != ((bs.find('link',rel='canonical') or {}).get('href') if bs.find('link',rel='canonical') else None): errors.append(f'{r} canonical changed vs production')
    if og != meta(bs,prop='og:url'): errors.append(f'{r} og changed vs production')
    pld=[(x.string or x.get_text()).strip() for x in ps.find_all('script',type='application/ld+json')]
    bld=[(x.string or x.get_text()).strip() for x in bs.find_all('script',type='application/ld+json')]
    if pld!=bld: errors.append(f'{r} JSON-LD changed')
    for raw in pld:
        try: json.loads(raw)
        except Exception as e: errors.append(f'{r} invalid JSON-LD {e}')
    # Exactly one official loader and one config call.
    loaders=[x.get('src','') for x in ps.find_all('script',src=True) if 'googletagmanager.com/gtag/js' in x.get('src','')]
    if loaders!=[f'https://www.googletagmanager.com/gtag/js?id={MID}']:
        errors.append(f'{r} GA loader count/value {loaders}')
    inline='\n'.join((x.string or x.get_text()) for x in ps.find_all('script') if not x.get('src'))
    cfg_count=len(re.findall(r"gtag\(\s*['\"]config['\"]\s*,\s*['\"]G-72BY7LC2V2['\"]\s*\)",inline))
    if cfg_count!=1: errors.append(f'{r} GA config count {cfg_count}')
    if pr.text.count(MID)!=2: errors.append(f'{r} measurement ID occurrence count {pr.text.count(MID)}')
    # No GTM container was introduced.
    if re.search(r'GTM-[A-Z0-9]+',pr.text): errors.append(f'{r} GTM container found')
    # Existing Meta Pixel source occurrences must remain identical to production.
    pfb=pr.text.count('connect.facebook.net') + pr.text.count('fbq(')
    bfb=po.text.count('connect.facebook.net') + po.text.count('fbq(')
    if pfb!=bfb: errors.append(f'{r} Meta Pixel changed {bfb}->{pfb}')
    report['routes'][r]={'status':pr.status_code,'canonical':canonical,'ga_loader_count':len(loaders),'ga_config_count':cfg_count,'meta_pixel_markers':pfb}

# robots and sitemap are untouched and correct.
rob=s.get(PREVIEW+'/robots.txt',timeout=30); prodrob=s.get(PROD+'/robots.txt',timeout=30)
if rob.status_code!=200 or rob.text!=prodrob.text or 'Sitemap: https://osaraclinics.com/sitemap.xml' not in rob.text: errors.append('robots regression')
sm=s.get(PREVIEW+'/sitemap.xml',timeout=30); prodsm=s.get(PROD+'/sitemap.xml',timeout=30)
locs=re.findall(r'<loc>(.*?)</loc>',sm.text)
if sm.status_code!=200 or sm.text!=prodsm.text or locs!=[EXPECTED[r] for r in ROUTES]: errors.append(f'sitemap regression/count {len(locs)}')
report['sitemap_count']=len(locs)

# Internal links/images across canonical pages.
seen_links=set(); seen_images=set()
for r in ROUTES:
    soup=BeautifulSoup(s.get(PREVIEW+r,timeout=30).text,'html.parser')
    for a in soup.find_all('a',href=True):
        h=a['href']
        if h.startswith(('#','tel:','mailto:','javascript:','https://wa.me','https://www.google.com','https://maps.app.goo.gl','https://goo.gl/maps')): continue
        u=urljoin(PREVIEW+r,h); pu=urlparse(u)
        if pu.netloc!=urlparse(PREVIEW).netloc: continue
        p=pu.path or '/'
        if p in seen_links: continue
        seen_links.add(p)
        rr=s.get(PREVIEW+p,allow_redirects=True,timeout=30)
        if rr.status_code>=400:
            errors.append(f'broken internal {r}->{p} {rr.status_code}'); report['broken_links'].append([r,p,rr.status_code])
    for im in soup.find_all('img',src=True):
        u=urljoin(PREVIEW+r,im['src']); pu=urlparse(u)
        if pu.netloc!=urlparse(PREVIEW).netloc: continue
        key=pu.path
        if key in seen_images: continue
        seen_images.add(key)
        rr=s.get(u,allow_redirects=True,timeout=30)
        if rr.status_code>=400:
            errors.append(f'broken image {key} {rr.status_code}'); report['broken_images'].append([key,rr.status_code])

# Existing extension and trailing-slash behavior must match production.
for r in ROUTES[1:]:
    for suffix in ['.html','/']:
        pr=s.get(PREVIEW+r+suffix,allow_redirects=False,timeout=30)
        po=s.get(PROD+r+suffix,allow_redirects=False,timeout=30)
        # new/old routes now all exist in production; compare status and Location semantics.
        if pr.status_code!=po.status_code: errors.append(f'{r+suffix} status changed {po.status_code}->{pr.status_code}')
        pl=pr.headers.get('location'); bl=po.headers.get('location')
        if bool(pl)!=bool(bl): errors.append(f'{r+suffix} redirect presence changed')
        if pl and bl and urlparse(pl).path!=urlparse(bl).path: errors.append(f'{r+suffix} redirect target changed {bl}->{pl}')

report['errors']=errors
open('pr3-static.json','w').write(json.dumps(report,ensure_ascii=False,indent=2))
print(json.dumps(report,ensure_ascii=False,indent=2))
sys.exit(1 if errors else 0)
