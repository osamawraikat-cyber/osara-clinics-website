import { chromium } from 'playwright';
import fs from 'fs';
const BASE='https://deploy-preview-4--gregarious-malabi-0dc7e1.netlify.app';
const PAGES=['/','/vitiligo-jordan','/mole-removal','/dermatology','/ophthalmology','/doctors/dr-osama-alwreikat','/doctors/dr-sara-abu-touq','/psoriasis-treatment','/acne-scar-treatment'];
const MOBILE=['/','/vitiligo-jordan','/mole-removal','/dermatology','/ophthalmology','/doctors/dr-osama-alwreikat','/doctors/dr-sara-abu-touq','/psoriasis-treatment','/acne-scar-treatment'];
const browser=await chromium.launch({headless:true});
const errors=[]; const report={pages:[],events:[],errors};
fs.mkdirSync('pr4-screenshots',{recursive:true});
function slug(p){return p==='/'?'homepage':p.replace(/^\//,'').replaceAll('/','--')}
for(const path of MOBILE){
  const ctx=await browser.newContext({viewport:{width:390,height:844},deviceScaleFactor:1});
  const page=await ctx.newPage(); const consoleErrors=[];
  page.on('pageerror',e=>consoleErrors.push('pageerror: '+String(e)));
  page.on('console',m=>{if(m.type()==='error')consoleErrors.push('console: '+m.text())});
  const resp=await page.goto(BASE+path,{waitUntil:'networkidle',timeout:60000}); await page.waitForTimeout(800);
  const metrics=await page.evaluate(()=>{
    const imgs=[...document.images].filter(i=>i.complete&&i.naturalWidth===0).map(i=>i.src);
    const buttons=[...document.querySelectorAll('a.cta,a.book-appointment,.whatsapp-float')].map(a=>{const r=a.getBoundingClientRect();return {text:(a.textContent||'').trim(),w:r.width,h:r.height}});
    const cs=getComputedStyle(document.body);
    return {scrollWidth:document.documentElement.scrollWidth,bodyScrollWidth:document.body.scrollWidth,brokenImages:imgs,h1:document.querySelectorAll('h1').length,bodyFont:cs.fontFamily,bodyBg:cs.backgroundColor,buttons,header:!!document.querySelector('header'),footer:!!document.querySelector('footer')};
  });
  if(resp?.status()!==200)errors.push(`${path} status ${resp?.status()}`);
  if(metrics.scrollWidth>390||metrics.bodyScrollWidth>390)errors.push(`${path} horizontal overflow ${metrics.scrollWidth}/${metrics.bodyScrollWidth}`);
  if(metrics.brokenImages.length)errors.push(`${path} broken images`);
  if(metrics.h1!==1)errors.push(`${path} H1 ${metrics.h1}`);
  if(consoleErrors.length)errors.push(`${path} console ${consoleErrors.join(' | ')}`);
  for(const b of metrics.buttons){if(b.w<44||b.h<44)errors.push(`${path} small CTA ${b.text} ${b.w}x${b.h}`)}
  await page.screenshot({path:`pr4-screenshots/mobile-${slug(path)}.png`,fullPage:true});
  report.pages.push({path,status:resp?.status(),...metrics,consoleErrors}); await ctx.close();
}
// Desktop comparison screenshots for requested reference + repaired set.
for(const path of PAGES){const ctx=await browser.newContext({viewport:{width:1440,height:1000}});const page=await ctx.newPage();await page.goto(BASE+path,{waitUntil:'networkidle',timeout:60000});await page.screenshot({path:`pr4-screenshots/desktop-${slug(path)}.png`,fullPage:true});await ctx.close();}

const tests=[
 {path:'/psoriasis-treatment',selector:'a.book-appointment',event:'appointment_click'},
 {path:'/acne-scar-treatment',selector:'a[href^="tel:"]',event:'phone_click'},
 {path:'/dermatology',selector:'a[href*="google.com/maps"]',event:'directions_click'},
 {path:'/psoriasis-treatment',selector:'a.whatsapp-float',event:'whatsapp_click'}
];
for(const t of tests){
 const ctx=await browser.newContext({viewport:{width:1280,height:900}});const page=await ctx.newPage();
 await page.addInitScript(()=>document.addEventListener('click',e=>{if(e.target.closest?.('a[href]'))e.preventDefault()},true));
 const consoleErrors=[];page.on('pageerror',e=>consoleErrors.push(String(e)));page.on('console',m=>{if(m.type()==='error')consoleErrors.push(m.text())});
 await page.goto(BASE+t.path,{waitUntil:'networkidle',timeout:60000});
 const result=await page.evaluate(({selector,event})=>{const a=document.querySelector(selector);if(!a)return {found:false};a.click();const commands=(window.dataLayer||[]).map(x=>Array.from(x||[])).filter(x=>Array.isArray(x)&&x.length);const matches=commands.filter(x=>x[0]==='event'&&x[1]===event);return {found:true,count:matches.length,payloads:matches.map(x=>x[2]||{})}},t);
 const payload=result.payloads?.[0]||{};const allowed=['source_page','specialty','service','campaign'];const bad=Object.keys(payload).filter(k=>!allowed.includes(k)||/patient|name|phone|email|symptom|diagnos|message|text|note|query|url/i.test(k));
 if(!result.found)errors.push(`${t.event} selector missing`);if(result.count!==1)errors.push(`${t.event} count ${result.count}`);if(bad.length)errors.push(`${t.event} payload keys ${bad}`);if(consoleErrors.length)errors.push(`${t.event} console errors`);
 report.events.push({...t,result,payload,bad,consoleErrors});await ctx.close();
}
report.errors=errors;fs.writeFileSync('pr4-browser.json',JSON.stringify(report,null,2));console.log(JSON.stringify(report,null,2));await browser.close();if(errors.length)process.exit(1);
