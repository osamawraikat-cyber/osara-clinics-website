import json, os, re, sys
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup

BASE = os.environ['PREVIEW_BASE'].rstrip('/')
CANON = 'https://osaraclinics.com'
PATHS = ['/', '/dermatology', '/ophthalmology', '/doctors/dr-osama-alwreikat', '/doctors/dr-sara-abu-touq', '/vitiligo-jordan', '/botox-hyperhidrosis', '/mole-removal', '/school-health']
EXPECTED_HOURS = [
    {'dayOfWeek': ['Saturday','Sunday'], 'opens':'16:30', 'closes':'20:30'},
    {'dayOfWeek': ['Monday','Tuesday','Wednesday','Thursday'], 'opens':'08:00', 'closes':'13:30'},
    {'dayOfWeek': ['Monday','Tuesday','Wednesday','Thursday'], 'opens':'16:30', 'closes':'20:30'},
]
s = requests.Session(); s.headers['User-Agent']='OSara-PR1-final-validator/1.0'
errors=[]; pages=[]; links=set()

def get(path):
    return s.get(BASE + path, allow_redirects=True, timeout=30)

for path in PATHS:
    r=get(path)
    soup=BeautifulSoup(r.text,'html.parser')
    canonical=soup.find('link', rel=lambda x:x and 'canonical' in x)
    h1s=soup.find_all('h1')
    robots=[m.get('content','') for m in soup.find_all('meta', attrs={'name':re.compile('^robots$',re.I)})]
    expected=CANON+'/' if path=='/' else CANON+path
    row={'path':path,'status':r.status_code,'redirects':len(r.history),'canonical':canonical.get('href') if canonical else None,'h1_count':len(h1s),'title':soup.title.get_text(' ',strip=True) if soup.title else None,'noindex':any('noindex' in x.lower() for x in robots)}
    pages.append(row)
    if r.status_code!=200 or len(r.history)!=0: errors.append(f'{path}: expected direct 200')
    if row['canonical']!=expected: errors.append(f'{path}: canonical {row["canonical"]} != {expected}')
    if len(h1s)!=1: errors.append(f'{path}: H1 count {len(h1s)}')
    if not row['title']: errors.append(f'{path}: missing title')
    if row['noindex']: errors.append(f'{path}: accidental noindex')
    for a in soup.find_all('a',href=True):
        href=a['href'].split('#')[0]
        if href.startswith('/') and href:
            links.add(href)

broken=[]
for href in sorted(links):
    r=get(href)
    if r.status_code>=400:
        broken.append({'href':href,'status':r.status_code})
if broken: errors.append('broken internal links: '+json.dumps(broken))

robots=get('/robots.txt'); sitemap=get('/sitemap.xml')
if robots.status_code!=200 or 'Sitemap: https://osaraclinics.com/sitemap.xml' not in robots.text: errors.append('robots invalid')
if sitemap.status_code!=200: errors.append('sitemap not 200')
sitemap_urls=re.findall(r'<loc>(.*?)</loc>',sitemap.text)
expected_urls=[CANON+'/' if p=='/' else CANON+p for p in PATHS]
if sitemap_urls!=expected_urls: errors.append('sitemap URLs mismatch')

home=BeautifulSoup(get('/').text,'html.parser')
clinic=None
for sc in home.find_all('script',attrs={'type':'application/ld+json'}):
    try:
        obj=json.loads(sc.string or sc.get_text())
    except Exception:
        continue
    if isinstance(obj,dict) and obj.get('@type')=='MedicalClinic' and obj.get('@id')==CANON+'/#clinic': clinic=obj
if not clinic: errors.append('MedicalClinic JSON-LD missing')
else:
    actual=[{'dayOfWeek':x.get('dayOfWeek'),'opens':x.get('opens'),'closes':x.get('closes')} for x in clinic.get('openingHoursSpecification',[])]
    if actual!=EXPECTED_HOURS: errors.append('openingHoursSpecification mismatch: '+json.dumps(actual))
    if any('Friday' in (x.get('dayOfWeek') if isinstance(x.get('dayOfWeek'),list) else [x.get('dayOfWeek')]) for x in clinic.get('openingHoursSpecification',[])): errors.append('Friday incorrectly has opening hours')

body=home.get_text(' ',strip=True)
for required in ['Saturday - Sunday','Monday - Thursday','Friday','Closed','Appointments and availability may occasionally vary','For urgent dermatological or ophthalmological concerns outside regular clinic hours','nearest appropriate emergency department']:
    if required not in body: errors.append('visible hours/contact missing: '+required)
if 'Call to enquire' in body or 'Hours vary - Call to confirm' in body: errors.append('old variable-hours wording still visible')
if re.search(r'24\s*/\s*7|24\s*hours', body, re.I): errors.append('24/7 implication found')

for path,bad in [('/doctors/dr-osama-alwreikat','dr_osama.png'),('/doctors/dr-sara-abu-touq','dr_sara.png')]:
    text=get(path).text
    soup=BeautifulSoup(text,'html.parser')
    if bad in text: errors.append(path+': mismatched asset reference remains')
    if soup.find('meta',attrs={'property':'og:image'}): errors.append(path+': OG image remains')
    if soup.find('img'): errors.append(path+': visible image remains')
    for sc in soup.find_all('script',attrs={'type':'application/ld+json'}):
        try: obj=json.loads(sc.string or sc.get_text())
        except Exception: continue
        if '"image"' in json.dumps(obj): errors.append(path+': schema image remains')

report={'pages':pages,'broken_internal_links':broken,'robots_status':robots.status_code,'sitemap_status':sitemap.status_code,'sitemap_urls':sitemap_urls,'hours':clinic.get('openingHoursSpecification',[]) if clinic else None,'errors':errors}
print(json.dumps(report,ensure_ascii=False,indent=2))
sys.exit(1 if errors else 0)
