import { chromium } from 'playwright';
import fs from 'fs';

const base=process.env.PREVIEW_BASE.replace(/\/$/,'');
const browser=await chromium.launch({headless:true});
const mobilePaths=['/','/dermatology','/ophthalmology','/doctors/dr-osama-alwreikat','/doctors/dr-sara-abu-touq','/vitiligo-jordan'];
const mobile=[]; const errors=[];
for (const p of mobilePaths) {
  const ctx=await browser.newContext({viewport:{width:390,height:844},deviceScaleFactor:1});
  const page=await ctx.newPage(); const errs=[];
  page.on('pageerror',e=>errs.push('pageerror: '+String(e)));
  page.on('console',m=>{if(m.type()==='error') errs.push('console: '+m.text())});
  const response=await page.goto(base+p,{waitUntil:'networkidle',timeout:45000});
  const metrics=await page.evaluate(()=>({innerWidth:innerWidth,scrollWidth:document.documentElement.scrollWidth,bodyScrollWidth:document.body.scrollWidth,h1Count:document.querySelectorAll('h1').length,visibleH1:[...document.querySelectorAll('h1')].filter(e=>{const r=e.getBoundingClientRect(),s=getComputedStyle(e);return r.width>0&&r.height>0&&s.display!=='none'&&s.visibility!=='hidden'}).length,brokenImages:[...document.images].filter(i=>i.complete&&i.naturalWidth===0).map(i=>i.src),canonical:document.querySelector('link[rel="canonical"]')?.href||null}));
  const name=p==='/'?'home':p.slice(1).replaceAll('/','_');
  await page.screenshot({path:`mobile-${name}.png`,fullPage:true});
  mobile.push({path:p,status:response?.status(),url:page.url(),...metrics,consoleErrors:errs});
  if(response?.status()!==200||metrics.scrollWidth>390||metrics.bodyScrollWidth>390||metrics.h1Count!==1||metrics.visibleH1!==1||metrics.brokenImages.length||errs.length) errors.push('mobile/render '+p);
  await ctx.close();
}

const ctx=await browser.newContext({viewport:{width:1280,height:900}});
const page=await ctx.newPage(); const consoleErrors=[];
page.on('pageerror',e=>consoleErrors.push('pageerror: '+String(e)));
page.on('console',m=>{if(m.type()==='error') consoleErrors.push('console: '+m.text())});
await page.addInitScript(()=>document.addEventListener('click',e=>{if(e.target.closest?.('a[href]'))e.preventDefault()},true));
await page.goto(base+'/',{waitUntil:'networkidle',timeout:45000});

const rendered=await page.evaluate(()=>{
  const body=document.body.innerText;
  let clinic=null;
  for(const s of document.querySelectorAll('script[type="application/ld+json"]')){try{const x=JSON.parse(s.textContent);if(x?.['@type']==='MedicalClinic'&&x?.['@id']==='https://osaraclinics.com/#clinic')clinic=x}catch{}}
  return {hoursText:document.querySelector('.hours-container')?.innerText||'',hasUrgentArabic:body.includes('تواصل للحالات العاجلة خارج ساعات العمل'),hasUrgentEnglish:body.includes('For urgent dermatological or ophthalmological concerns outside regular clinic hours'),has24:/24\s*\/\s*7|24\s*hours/i.test(body),clinicHours:clinic?.openingHoursSpecification||null};
});
const expectedHours=[
 {'@type':'OpeningHoursSpecification',dayOfWeek:['Saturday','Sunday'],opens:'16:30',closes:'20:30'},
 {'@type':'OpeningHoursSpecification',dayOfWeek:['Monday','Tuesday','Wednesday','Thursday'],opens:'08:00',closes:'13:30'},
 {'@type':'OpeningHoursSpecification',dayOfWeek:['Monday','Tuesday','Wednesday','Thursday'],opens:'16:30',closes:'20:30'}
];
if(JSON.stringify(rendered.clinicHours)!==JSON.stringify(expectedHours)) errors.push('rendered schema hours mismatch');
for(const x of ['Saturday - Sunday','Monday - Thursday','Friday','Closed','8:00 AM - 1:30 PM','4:30 PM - 8:30 PM']) if(!rendered.hoursText.includes(x)) errors.push('rendered visible hours missing '+x);
if(!rendered.hasUrgentArabic||!rendered.hasUrgentEnglish||rendered.has24) errors.push('urgent contact messaging invalid');

async function testCTA(path,selector,eventName){
  await page.goto(base+path,{waitUntil:'networkidle',timeout:45000});
  await page.evaluate(()=>{window.gtag=undefined;window.dataLayer=[]});
  const result=await page.evaluate(({selector,eventName})=>{
    const a=document.querySelector(selector); if(!a)return {found:false,eventName};
    const href=a.getAttribute('href'); a.click(); const dl=window.dataLayer||[];
    return {found:true,href,eventName,eventCount:dl.filter(x=>x?.event===eventName).length,dataLayer:dl,forbiddenKeys:[...new Set(dl.flatMap(x=>Object.keys(x||{})).filter(k=>/patient|diagnosis|symptom|message|text/i.test(k)))]};
  },{selector,eventName});
  if(!result.found||result.eventCount!==1||result.forbiddenKeys.length) errors.push('CTA '+eventName);
  return result;
}
const ctas=[];
ctas.push(await testCTA('/','a[href*="wa.me/"]:not([data-appointment]):not(.book-appointment)','whatsapp_click'));
ctas.push(await testCTA('/','a[href^="tel:"]','phone_click'));
ctas.push(await testCTA('/dermatology','a[href*="google.com/maps"]','directions_click'));
ctas.push(await testCTA('/','a[data-appointment],a.book-appointment','appointment_click'));
if(consoleErrors.length) errors.push('desktop console errors');

const report={mobile,rendered,ctas,consoleErrors,errors};
fs.writeFileSync('browser-report.json',JSON.stringify(report,null,2));
console.log(JSON.stringify(report,null,2));
await browser.close();
if(errors.length) process.exit(1);
