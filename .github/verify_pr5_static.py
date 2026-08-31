import json,re,requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin,urlparse
PRE='https://deploy-preview-5--gregarious-malabi-0dc7e1.netlify.app'
PROD='https://osaraclinics.com'
MAP='https://maps.app.goo.gl/FMrYnf8xmhJJETsG9?g_st=ac'
ROUTES=['/','/dermatology','/ophthalmology','/doctors/dr-osama-alwreikat','/doctors/dr-sara-abu-touq','/psoriasis-treatment','/acne-scar-treatment','/vitiligo-jordan','/mole-removal','/school-health','/botox-hyperhidrosis']
S=requests.Session(); S.headers['User-Agent']='OSara-PR5-validation/1.0'
errors=[]; rep={'routes':{},'directions':{},'schema_geo':{},'variants':{},'broken_links':[],'broken_images':[]}
all_internal=set()
for r in ROUTES:
    resp=S.get(PRE+r,timeout=20); soup=BeautifulSoup(resp.text,'html.parser')
    can=soup.find('link',rel='canonical'); meta=soup.find('meta',attrs={'name':'description'}); title=soup.title.string.strip() if soup.title and soup.title.string else None
    if resp.status_code!=200: errors.append(f'{r} status {resp.status_code}')
    expected=PROD+('/' if r=='/' else r)
    if not can or can.get('href')!=expected: errors.append(f'{r} canonical')
    if not title or not meta or not meta.get('content'): errors.append(f'{r} title/meta missing')
    # JSON-LD parses; capture geo without altering/verifying it.
    for sc in soup.find_all('script',type='application/ld+json'):
        try:
            data=json.loads(sc.string or sc.get_text())
        except Exception as e:
            errors.append(f'{r} JSON-LD parse {e}'); continue
        stack=[data]
        while stack:
            x=stack.pop()
            if isinstance(x,dict):
                if x.get('@type')=='GeoCoordinates': rep['schema_geo'][r]={'latitude':x.get('latitude'),'longitude':x.get('longitude')}
                stack.extend(x.values())
            elif isinstance(x,list): stack.extend(x)
    dirs=[]
    for a in soup.find_all('a',href=True):
        href=a['href']
        text=' '.join(a.stripped_strings)
        if 'الاتجاهات' in text or 'Directions' in text or 'maps.app.goo.gl' in href or 'google.com/maps' in href or 'maps.google.com' in href:
            dirs.append(href)
        if href.startswith('/'):
            all_internal.add(href.split('#')[0])
    rep['directions'][r]=dirs
    for href in dirs:
        if href!=MAP: errors.append(f'{r} non-authoritative directions {href}')
    # old bad coordinate may remain only inside schema, never a patient href/embed.
    for a in soup.find_all('a',href=True):
        if '32.062463' in a['href'] or '35.864789' in a['href']: errors.append(f'{r} old coordinate href')
    for iframe in soup.find_all('iframe',src=True):
        if 'maps' in iframe['src'] or '32.062463' in iframe['src'] or '35.864789' in iframe['src']: errors.append(f'{r} interactive/old map iframe remains')
    for img in soup.find_all('img',src=True):
        u=urljoin(PRE+r,img['src']); ir=S.get(u,timeout=15)
        if ir.status_code>=400: rep['broken_images'].append((r,u,ir.status_code)); errors.append(f'broken image {u}')
    rep['routes'][r]={'status':resp.status_code,'canonical':can.get('href') if can else None,'title':title,'description':meta.get('content') if meta else None}
# internal links
for href in sorted(all_internal):
    if href.startswith('//'): continue
    rr=S.get(PRE+href,allow_redirects=True,timeout=20)
    if rr.status_code>=400:
        rep['broken_links'].append((href,rr.status_code)); errors.append(f'broken internal {href}')
# sitemap/robots
sm=S.get(PRE+'/sitemap.xml',timeout=20); urls=re.findall(r'<loc>(.*?)</loc>',sm.text)
expected=[PROD+('/' if r=='/' else r) for r in ROUTES]
rep['sitemap_count']=len(urls); rep['sitemap_urls']=urls
if urls!=expected: errors.append('sitemap not exact 11 canonical URLs')
rob=S.get(PRE+'/robots.txt',timeout=20).text
prodrob=S.get(PROD+'/robots.txt',timeout=20).text
rep['robots']=rob
if rob!=prodrob: errors.append('robots changed')
# .html/trailing behavior vs production on representative and all routes
for r in ROUTES[1:]:
    for suffix in ['.html','/']:
        pth=r+suffix
        a=S.get(PRE+pth,allow_redirects=False,timeout=20); b=S.get(PROD+pth,allow_redirects=False,timeout=20)
        rep['variants'][pth]={'preview':[a.status_code,a.headers.get('location')],'production':[b.status_code,b.headers.get('location')]}
        if (a.status_code,a.headers.get('location'))!=(b.status_code,b.headers.get('location')): errors.append(f'variant changed {pth}')
# www -> non-www current behavior check
w=S.get('https://www.osaraclinics.com/',allow_redirects=False,timeout=20); rep['www']=[w.status_code,w.headers.get('location')]
if w.status_code not in (301,302,307,308) or not (w.headers.get('location') or '').startswith('https://osaraclinics.com'): errors.append('www redirect')
rep['errors']=errors
open('pr5-static.json','w',encoding='utf-8').write(json.dumps(rep,ensure_ascii=False,indent=2))
print(json.dumps(rep,ensure_ascii=False,indent=2))
raise SystemExit(1 if errors else 0)
