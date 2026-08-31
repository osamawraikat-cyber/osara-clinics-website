import { chromium } from 'playwright';
import fs from 'fs';
const base='https://osaraclinics.com';
const browser=await chromium.launch({headless:true});
const errors=[]; const mobile=[];
const mobilePaths=['/','/dermatology','/ophthalmology','/doctors/dr-osama-alwreikat','/doctors/dr-sara-abu-touq','/vitiligo-jordan'];
for(const p of mobilePaths){
 const ctx=await browser.newContext({viewport:{width:390,height:844}}); const page=await ctx.newPage(); const ce=[];
 page.on('pageerror',e=>ce.push('pageerror: '+e)); page.on('console',m=>{if(m.type()==='error')ce.push('console: '+m.text())});
 const resp=await page.goto(base+p,{waitUntil:'networkidle',timeout:45000});
 const m=await page.evaluate(()=>({sw:document.documentElement.scrollWidth,bsw:document.body.scrollWidth,iw:innerWidth,broken:[...document.images].filter(i=>i.complete&&i.naturalWidth===0).map(i=>i.src),h1:document.querySelectorAll('h1').length}));
 mobile.push({path:p,status:resp?.status(),url:page.url(),...m,consoleErrors:ce});
 if(resp?.status()!==200||m.sw>390||m.bsw>390||m.broken.length||ce.length)errors.push('mobile '+p);
 await ctx.close();
}
const ctx=await browser.newContext({viewport:{width:1280,height:900}}); const page=await ctx.newPage(); const consoleErrors=[];
page.on('pageerror',e=>consoleErrors.push('pageerror: '+e)); page.on('console',m=>{if(m.type()==='error')consoleErrors.push('console: '+m.text())});
await page.addInitScript(()=>document.addEventListener('click',e=>{if(e.target.closest?.('a[href]'))e.preventDefault()},true));
await page.goto(base+'/',{waitUntil:'networkidle',timeout:45000});
const rendered=await page.evaluate(()=>{
 const body=document.body.innerText; let clinic=null;
 for(const s of document.querySelectorAll('script[type="application/ld+json"]')){try{const x=JSON.parse(s.textContent);if(x?.['@type']==='MedicalClinic'&&x?.['@id']==='https://osaraclinics.com/#clinic')clinic=x}catch{}}
 return {hours:clinic?.openingHoursSpecification||null,hoursText:document.querySelector('.hours-container')?.innerText||'',urgentAr:body.includes('تواصل للحالات العاجلة خارج ساعات العمل'),urgentEn:body.includes('For urgent dermatological or ophthalmological concerns outside regular clinic hours'),has24:/24\s*\/\s*7|24\s*hours/i.test(body)};
});
const expected=[{'@type':'OpeningHoursSpecification',dayOfWeek:['Saturday','Sunday'],opens:'16:30',closes:'20:30'},{'@type':'OpeningHoursSpecification',dayOfWeek:['Monday','Tuesday','Wednesday','Thursday'],opens:'08:00',closes:'13:30'},{'@type':'OpeningHoursSpecification',dayOfWeek:['Monday','Tuesday','Wednesday','Thursday'],opens:'16:30',closes:'20:30'}];
if(JSON.stringify(rendered.hours)!==JSON.stringify(expected))errors.push('rendered hours');
for(const x of ['Saturday - Sunday','Monday - Thursday','Friday','Closed','8:00 AM - 1:30 PM','4:30 PM - 8:30 PM'])if(!rendered.hoursText.includes(x))errors.push('visible hours '+x);
if(!rendered.urgentAr||!rendered.urgentEn||rendered.has24)errors.push('urgent wording');
async function testCTA(path,selector,name){await page.goto(base+path,{waitUntil:'networkidle',timeout:45000});await page.evaluate(()=>{window.gtag=undefined;window.dataLayer=[]});return await page.evaluate(({selector,name})=>{const a=document.querySelector(selector);if(!a)return {found:false,name};a.click();const dl=window.dataLayer||[];return {found:true,name,count:dl.filter(x=>x?.event===name).length,dataLayer:dl}}, {selector,name});}
const ctas=[];
ctas.push(await testCTA('/','a[href*="wa.me/"]:not([data-appointment]):not(.book-appointment)','whatsapp_click'));
ctas.push(await testCTA('/','a[href^="tel:"]','phone_click'));
ctas.push(await testCTA('/dermatology','a[href*="google.com/maps"]','directions_click'));
ctas.push(await testCTA('/','a[data-appointment],a.book-appointment','appointment_click'));
for(const c of ctas)if(!c.found||c.count!==1)errors.push('cta '+c.name);
if(consoleErrors.length)errors.push('desktop console');
const physician=[];
for(const p of ['/doctors/dr-osama-alwreikat','/doctors/dr-sara-abu-touq']){await page.goto(base+p,{waitUntil:'networkidle',timeout:45000});const x=await page.evaluate(()=>({imgs:[...document.images].map(i=>i.src),og:document.querySelector('meta[property="og:image"]')?.content||null,schema:[...document.querySelectorAll('script[type="application/ld+json"]')].some(s=>s.textContent.includes('"image"'))}));physician.push({path:p,...x});if(x.imgs.length||x.og||x.schema)errors.push('physician '+p)}
const report={mobile,rendered,ctas,physician,consoleErrors,errors};fs.writeFileSync('production-browser-report.json',JSON.stringify(report,null,2));console.log(JSON.stringify(report,null,2));await browser.close();if(errors.length)process.exit(1);
