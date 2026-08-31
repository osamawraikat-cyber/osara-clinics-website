import { chromium } from 'playwright';
import fs from 'fs';

const BASE='https://deploy-preview-3--gregarious-malabi-0dc7e1.netlify.app';
const MID='G-72BY7LC2V2';
const browser=await chromium.launch({headless:true});
const errors=[];
const report={pages:[],events:[],errors};
const mobilePaths=['/','/dermatology','/psoriasis-treatment','/acne-scar-treatment','/vitiligo-jordan'];

function isGoogleAnalytics(url){return url.includes('google-analytics.com/') || url.includes('googletagmanager.com/');}
function eventInRequest(rec,event){
  const hay=(rec.url+'\n'+(rec.postData||''));
  return hay.includes('en='+encodeURIComponent(event)) || hay.includes('en='+event) || hay.includes(event);
}

for(const path of mobilePaths){
  const ctx=await browser.newContext({viewport:{width:390,height:844},deviceScaleFactor:1});
  const page=await ctx.newPage();
  const consoleErrors=[]; const requests=[];
  page.on('pageerror',e=>consoleErrors.push('pageerror: '+String(e)));
  page.on('console',m=>{if(m.type()==='error') consoleErrors.push('console: '+m.text())});
  page.on('request',req=>{if(isGoogleAnalytics(req.url())) requests.push({url:req.url(),method:req.method(),postData:req.postData()})});
  const resp=await page.goto(BASE+path,{waitUntil:'networkidle',timeout:60000});
  await page.waitForTimeout(1500);
  const runtime=await page.evaluate((mid)=>{
    const dl=window.dataLayer||[];
    const commands=dl.map(x=>Array.from(x||[])).filter(x=>Array.isArray(x)&&x.length);
    return {hasGtag:typeof window.gtag==='function',configCount:commands.filter(x=>x[0]==='config'&&x[1]===mid).length,jsCount:commands.filter(x=>x[0]==='js').length,scrollWidth:document.documentElement.scrollWidth,bodyScrollWidth:document.body.scrollWidth,brokenImages:[...document.images].filter(i=>i.complete&&i.naturalWidth===0).map(i=>i.src),canonical:document.querySelector('link[rel="canonical"]')?.href||null,metaPixel:typeof window.fbq==='function'};
  },MID);
  const gtagLoads=requests.filter(r=>r.url.includes('googletagmanager.com/gtag/js?id='+MID)).length;
  const pageViews=requests.filter(r=>eventInRequest(r,'page_view')).length;
  if(resp?.status()!==200) errors.push(`${path} mobile status ${resp?.status()}`);
  if(runtime.scrollWidth>390||runtime.bodyScrollWidth>390) errors.push(`${path} horizontal overflow`);
  if(runtime.brokenImages.length) errors.push(`${path} broken images`);
  if(consoleErrors.length) errors.push(`${path} console errors: ${consoleErrors.join(' | ')}`);
  if(!runtime.hasGtag) errors.push(`${path} gtag missing`);
  if(runtime.configCount!==1) errors.push(`${path} runtime config count ${runtime.configCount}`);
  if(gtagLoads!==1) errors.push(`${path} gtag.js network count ${gtagLoads}`);
  if(pageViews<1) errors.push(`${path} no GA4 page_view request`);
  report.pages.push({path,status:resp?.status(),...runtime,gtagLoads,pageViews,consoleErrors,gaRequests:requests});
  await ctx.close();
}

const tests=[
  {path:'/psoriasis-treatment',selector:'a.book-appointment',event:'appointment_click'},
  {path:'/acne-scar-treatment',selector:'a[href^="tel:"]',event:'phone_click'},
  {path:'/dermatology',selector:'a[href*="google.com/maps"]',event:'directions_click'},
  {path:'/psoriasis-treatment',selector:'a[href*="wa.me/"]:not([data-appointment]):not(.book-appointment)',event:'whatsapp_click'}
];

for(const t of tests){
  const ctx=await browser.newContext({viewport:{width:1280,height:900}});
  const page=await ctx.newPage();
  await page.addInitScript(()=>document.addEventListener('click',e=>{if(e.target.closest?.('a[href]')) e.preventDefault()},true));
  const consoleErrors=[]; const requests=[];
  page.on('pageerror',e=>consoleErrors.push('pageerror: '+String(e)));
  page.on('console',m=>{if(m.type()==='error') consoleErrors.push('console: '+m.text())});
  page.on('request',req=>{if(isGoogleAnalytics(req.url())) requests.push({url:req.url(),method:req.method(),postData:req.postData()})});
  await page.goto(BASE+t.path,{waitUntil:'networkidle',timeout:60000});
  await page.waitForTimeout(1000);
  const result=await page.evaluate(({selector,event})=>{
    const a=document.querySelector(selector); if(!a)return {found:false};
    a.click();
    const commands=(window.dataLayer||[]).map(x=>Array.from(x||[])).filter(x=>Array.isArray(x)&&x.length);
    const matches=commands.filter(x=>x[0]==='event'&&x[1]===event);
    return {found:true,count:matches.length,payloads:matches.map(x=>x[2]||{})};
  },t);
  await page.waitForTimeout(8000);
  const customRequests=requests.filter(r=>eventInRequest(r,t.event));
  const payload=result.payloads?.[0]||{}; const keys=Object.keys(payload);
  const allowed=['source_page','specialty','service','campaign'];
  const forbiddenKeys=keys.filter(k=>!allowed.includes(k));
  const sensitiveKeyHits=keys.filter(k=>/patient|name|phone|email|symptom|diagnos|condition|message|text|note|query|url/i.test(k));
  const sensitiveValueHits=/wa\.me|\?|mailto:|tel:|diagnos|symptom|patient|message/.test(JSON.stringify(payload).toLowerCase());
  if(!result.found) errors.push(`${t.event} selector missing`);
  if(result.count!==1) errors.push(`${t.event} dataLayer/gtag count ${result.count}`);
  if(customRequests.length!==1) errors.push(`${t.event} GA4 transport count ${customRequests.length}`);
  if(forbiddenKeys.length||sensitiveKeyHits.length||sensitiveValueHits) errors.push(`${t.event} privacy payload issue ${JSON.stringify(payload)}`);
  if(!payload.source_page) errors.push(`${t.event} missing source_page`);
  if(consoleErrors.length) errors.push(`${t.event} console errors ${consoleErrors.join(' | ')}`);
  report.events.push({...t,result,customRequestCount:customRequests.length,customRequests,allGoogleRequests:requests,payload,keys,forbiddenKeys,sensitiveKeyHits,sensitiveValueHits,consoleErrors});
  await ctx.close();
}

fs.writeFileSync('pr3-browser.json',JSON.stringify(report,null,2));
console.log(JSON.stringify(report,null,2));
await browser.close();
if(errors.length) process.exit(1);
