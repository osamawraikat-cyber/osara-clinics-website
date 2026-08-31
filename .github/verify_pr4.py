import json,re,sys,time
from urllib.parse import urljoin,urlparse
import requests
from bs4 import BeautifulSoup

PREVIEW='https://deploy-preview-4--gregarious-malabi-0dc7e1.netlify.app'
PROD='https://osaraclinics.com'
ROUTES=['/','/dermatology','/ophthalmology','/doctors/dr-osama-alwreikat','/doctors/dr-sara-abu-touq','/psoriasis-treatment','/acne-scar-treatment','/vitiligo-jordan','/botox-hyperhidrosis','/mole-removal','/school-health']
AFFECTED=['/dermatology','/ophthalmology','/doctors/dr-osama-alwreikat','/doctors/dr-sara-abu-touq','/psoriasis-treatment','/acne-scar-treatment']
MID='G-72BY7LC2V2'
s=requests.Session(); s.headers['User-Agent']='OSara-PR4-validator/1.0'
errors=[]; report={'routes':{},'broken_links':[],'broken_images':[],'narration_hits':{}}

def meta(soup,name=None,prop=None):
    el=soup.find('meta',attrs={'name':name}) if name else soup.find('meta',attrs={'property':prop})
    return el.get('content') if el else None

def get(url, redirects=False):
    last=None
    for i in range(4):
        try:
            return s.get(url,allow_redirects=redirects,timeout=20)
        except requests.RequestException as e:
            last=e; time.sleep(1.5*(i+1))
    raise last

for r in ROUTES:
    pr=get(PREVIEW+r); po=get(PROD+r)
    if pr.status_code!=200: errors.append(f'{r} preview status {pr.status_code}')
    if po.status_code!=200: errors.append(f'{r} production status {po.status_code}')
    ps=BeautifulSoup(pr.text,'html.parser'); bs=BeautifulSoup(po.text,'html.parser')
    pc=(ps.find('link',rel='canonical') or {}).get('href') if ps.find('link',rel='canonical') else None
    bc=(bs.find('link',rel='canonical') or {}).get('href') if bs.find('link',rel='canonical') else None
    if pc!=bc: errors.append(f'{r} canonical changed {bc}->{pc}')
    if (ps.title.get_text(strip=True) if ps.title else None)!=(bs.title.get_text(strip=True) if bs.title else None): errors.append(f'{r} title changed')
    if meta(ps,name='description')!=meta(bs,name='description'): errors.append(f'{r} description changed')
    if meta(ps,prop='og:url')!=meta(bs,prop='og:url'): errors.append(f'{r} og:url changed')
    pld=[(x.string or x.get_text()).strip() for x in ps.find_all('script',type='application/ld+json')]
    bld=[(x.string or x.get_text()).strip() for x in bs.find_all('script',type='application/ld+json')]
    if pld!=bld: errors.append(f'{r} JSON-LD changed')
    for raw in pld:
        try: json.loads(raw)
        except Exception as e: errors.append(f'{r} JSON-LD invalid {e}')
    h1=len(ps.find_all('h1'))
    if h1!=1: errors.append(f'{r} H1 count {h1}')
    loaders=[x.get('src','') for x in ps.find_all('script',src=True) if 'googletagmanager.com/gtag/js' in x.get('src','')]
    if loaders!=[f'https://www.googletagmanager.com/gtag/js?id={MID}']: errors.append(f'{r} GA loader changed')
    inline='\n'.join((x.string or x.get_text()) for x in ps.find_all('script') if not x.get('src'))
    if len(re.findall(r"gtag\(\s*['\"]config['\"]\s*,\s*['\"]G-72BY7LC2V2['\"]",inline))!=1: errors.append(f'{r} GA config count changed')
    pfb=pr.text.count('connect.facebook.net')+pr.text.count('fbq('); bfb=po.text.count('connect.facebook.net')+po.text.count('fbq(')
    if pfb!=bfb: errors.append(f'{r} Meta Pixel changed {bfb}->{pfb}')
    report['routes'][r]={'status':pr.status_code,'canonical':pc,'h1':h1,'meta_pixel_markers':pfb}

rob=get(PREVIEW+'/robots.txt'); prob=get(PROD+'/robots.txt')
if rob.status_code!=200 or rob.text!=prob.text: errors.append('robots changed')
sm=get(PREVIEW+'/sitemap.xml'); psm=get(PROD+'/sitemap.xml')
locs=re.findall(r'<loc>(.*?)</loc>',sm.text)
if sm.status_code!=200 or sm.text!=psm.text or len(locs)!=11: errors.append(f'sitemap changed/count={len(locs)}')
report['sitemap_count']=len(locs)

seen=set(); imgs=set()
for r in ROUTES:
    soup=BeautifulSoup(get(PREVIEW+r).text,'html.parser')
    for a in soup.find_all('a',href=True):
        h=a['href']
        if h.startswith(('#','tel:','mailto:','javascript:','https://wa.me','https://www.google.com','https://maps.app.goo.gl','https://goo.gl/maps')): continue
        u=urljoin(PREVIEW+r,h); pu=urlparse(u)
        if pu.netloc!=urlparse(PREVIEW).netloc: continue
        path=pu.path or '/'
        if path in seen: continue
        seen.add(path); rr=get(PREVIEW+path,True)
        if rr.status_code>=400: errors.append(f'broken internal {r}->{path} {rr.status_code}'); report['broken_links'].append([r,path,rr.status_code])
    for im in soup.find_all('img',src=True):
        u=urljoin(PREVIEW+r,im['src']); pu=urlparse(u)
        if pu.netloc!=urlparse(PREVIEW).netloc: continue
        if pu.path in imgs: continue
        imgs.add(pu.path); rr=get(u,True)
        if rr.status_code>=400: errors.append(f'broken image {pu.path} {rr.status_code}'); report['broken_images'].append([pu.path,rr.status_code])

for r in ROUTES[1:]:
    for suffix in ['.html','/']:
        a=get(PREVIEW+r+suffix); b=get(PROD+r+suffix)
        if a.status_code!=b.status_code: errors.append(f'{r+suffix} status changed {b.status_code}->{a.status_code}')
        al=a.headers.get('location'); bl=b.headers.get('location')
        if bool(al)!=bool(bl): errors.append(f'{r+suffix} redirect changed')
        if al and bl and urlparse(al).path!=urlparse(bl).path: errors.append(f'{r+suffix} redirect target changed')
www=get('https://www.osaraclinics.com/')
if www.status_code not in (301,302,307,308) or urlparse(www.headers.get('location','')).netloc!='osaraclinics.com': errors.append('www normalization changed')

patterns=[r'تربط هذه الصفحة',r'تعمل صفحة',r'بنية عيادات',r'هذه البوابة لا تكرر',r'الموقع الحالي يذكر',r'this page links',r'this page is part of',r'site structure',r'entity relationship',r'internal link',r'SEO']
for r in AFFECTED:
    text=BeautifulSoup(get(PREVIEW+r).text,'html.parser').get_text(' ',strip=True)
    hits=[pat for pat in patterns if re.search(pat,text,re.I)]
    report['narration_hits'][r]=hits
    if hits: errors.append(f'{r} visible internal narration {hits}')

report['errors']=errors
open('pr4-static.json','w').write(json.dumps(report,ensure_ascii=False,indent=2))
print(json.dumps(report,ensure_ascii=False,indent=2))
sys.exit(1 if errors else 0)
