import { chromium } from 'playwright';
import fs from 'fs';
const base='https://deploy-preview-2--gregarious-malabi-0dc7e1.netlify.app';
const browser=await chromium.launch({headless:true});
const paths=['/','/dermatology','/psoriasis-treatment','/acne-scar-treatment','/vitiligo-jordan'];
const mobile=[]; const errors=[];
for(const p of paths){
  const ctx=await browser.newContext({viewport:{width:390,height:844},deviceScaleFactor:1});
  const page=await ctx.newPage(); const errs=[];
  page.on('pageerror',e=>errs.push('pageerror: '+String(e)));
  page.on('console',m=>{if(m.type()==='error') errs.push('console: '+m.text())});
  const resp=await page.goto(base+p,{waitUntil:'networkidle',timeout:45000});
  const m=await page.evaluate(()=>({scrollWidth:document.documentElement.scrollWidth,bodyScrollWidth:document.body.scrollWidth,h1:document.querySelectorAll('h1').length,broken:[...document.images].filter(i=>i.complete&&i.naturalWidth===0).map(i=>i.src),canonical:document.querySelector('link[rel="canonical"]')?.href||null}));
  mobile.push({path:p,status:resp?.status(),...m,consoleErrors:errs});
  if(resp?.status()!==200||m.scrollWidth>390||m.bodyScrollWidth>390||m.h1!==1||m.broken.length||errs.length) errors.push('mobile '+p);
  await ctx.close();
}
const ctx=await browser.newContext({viewport:{width:1280,height:900}}); const page=await ctx.newPage();
await page.addInitScript(()=>document.addEventListener('click',e=>{if(e.target.closest?.('a[href]')) e.preventDefault()},true));
async function cta(path,selector,event){
  await page.goto(base+path,{waitUntil:'networkidle',timeout:45000});
  await page.evaluate(()=>{window.gtag=undefined;window.dataLayer=[]});
  const r=await page.evaluate(({selector,event})=>{const a=document.querySelector(selector);if(!a)return {found:false};a.click();const dl=window.dataLayer||[];return {found:true,count:dl.filter(x=>x?.event===event).length,payloads:dl.filter(x=>x?.event===event),forbidden:[...new Set(dl.flatMap(x=>Object.keys(x||{})).filter(k=>/patient|diagnosis|symptom|message|text/i.test(k)))]}}, {selector,event});
  if(!r.found||r.count!==1||r.forbidden.length) errors.push('CTA '+event);
  return {event,...r};
}
const ctas=[];
ctas.push(await cta('/psoriasis-treatment','a.book-appointment','appointment_click'));
ctas.push(await cta('/acne-scar-treatment','a[href^="tel:"]','phone_click'));
ctas.push(await cta('/dermatology','a[href*="google.com/maps"]','directions_click'));
ctas.push(await cta('/','a[href*="wa.me/"]:not([data-appointment]):not(.book-appointment)','whatsapp_click'));
const report={mobile,ctas,errors}; fs.writeFileSync('browser-report.json',JSON.stringify(report,null,2)); console.log(JSON.stringify(report,null,2));
await browser.close(); if(errors.length) process.exit(1);
