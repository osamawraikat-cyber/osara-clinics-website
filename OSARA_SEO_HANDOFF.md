# OSARA Clinics SEO & Website Handoff

**Project:** OSara Clinics SEO / local search growth  
**Canonical domain:** https://osaraclinics.com  
**GitHub repository:** `osamawraikat-cyber/osara-clinics-website`  
**Hosting:** Netlify  
**Primary location:** Abu Nusair, Amman, Jordan  
**Core specialties:** Dermatology + Ophthalmology  
**Baseline date:** 2026-08-31

## Purpose
Persistent handoff for future ChatGPT/Codex/engineering sessions. Read before changing the website. First inspect the repository and production site, create a baseline audit, preserve indexed URLs/search equity, and work on a branch/Netlify preview before production.

Core entity model:
- OSara Clinics → Abu Nusair, Amman → Dermatology → Dr. Osama Alwreikat
- OSara Clinics → Abu Nusair, Amman → Ophthalmology → Dr. Sara Abu Touq

## Strategic diagnosis
OSara already has early local-search traction. The homepage contains extensive dermatology, cosmetic dermatology and ophthalmology content, but nearly all search visibility is concentrated on the homepage.

**Primary problem:** OSara has more topical coverage than URL-level authority.

Do not solve this by mass-generating thin AI pages. Build deliberate specialty/service architecture, internal linking, physician trust signals and conversion measurement.

## Google Search Console baseline
Export: last 3 months ending 2026-08-31.

Site totals:
- 54 clicks
- 1,659 impressions
- ~3.25% CTR
- Earlier half: ~23 clicks / 591 impressions / ~3.89% CTR
- Later half: ~31 clicks / 1,068 impressions / ~2.90% CTR
- Last 30 days: ~27 clicks / 944 impressions / ~2.86% CTR

Important: Queries.csv contains only reportable/non-anonymized query rows and does NOT sum to site totals. Use Chart/site totals for overall performance.

Countries:
- Jordan: 49 clicks / 1,421 impressions / 3.45% CTR / pos 6.45
- Saudi: 3 / 24 / 12.5% / 10.08
- Oman: 1 / 21 / 4.76% / 15.71
- Egypt: 1 / 8 / 12.5% / 6

Devices:
- Mobile: 50 clicks / 1,425 impressions / 3.51% CTR / pos 6.1
- Desktop: 4 / 232 / 1.72% / 10.21
- Tablet: negligible

Mobile is the dominant search experience.

## Page-level GSC baseline
- `/` non-www: 46 clicks / 875 impressions / 5.26% CTR / pos 7.21
- historical www homepage: 9 / 910 / 0.99% / 5.57
- `/vitiligo-jordan`: 0 / 32 / pos 7.34
- `/botox-hyperhidrosis`: 0 / 23 / pos 6.65
- `/school-health`: 0 / 4 / pos 9

Canonical host is `https://osaraclinics.com`. Preserve permanent www → non-www consolidation. Verify redirects, canonicals, sitemap and internal links use non-www.

## Important query opportunities
Local dermatology:
- `دكتور جلدية ابو نصير`: 51 impressions / 1 click / pos 7.25
- `دكتور جلدية في ابو نصير`: 35 / 0 / pos 5.14
- `دكتور جلدية في شفا بدران`: 21 / 1 / pos 5.86
- `دكتور جلدية في عين الباشا`: 18 / 0 / pos 7.44
- `دكتور جلدية قريب مني`: 9 impressions / pos 2.67
- `دكتور جلدية عين الباشا`: 6 / pos 7.17
- `دكتور جلدية الجبيهة`: 5 / pos 10.6

Disease/service:
- `psoriasis treatment`: 12 impressions / pos 4.0 — strong dedicated-page opportunity
- acne scar treatment: early pos ~2 signal
- acne scar treatment near me: ~8
- scalp psoriasis treatment: ~7
- vitiligo: ~11
- botox near me: ~4
- scar removal laser: ~5
- chemical peel: ~19
- glycolic peel: ~31

Ophthalmology:
- `طبيب عيون ابو نصير`: early pos ~1
- `دكتور عيون في ابو نصير`: early pos ~1
- `دكتور عيون في شفا بدران`: much weaker (~22)

Small samples are hypotheses, not proof.

## Current live-site content
Homepage currently presents OSara as Dermatology & Ophthalmology and includes:
- Medical team: Dr. Osama Alwreikat; Dr. Sara Abu Touq
- Dermatology: acne, scars, vitiligo, eczema, psoriasis, melasma, hyperhidrosis, HS, infantile hemangiomas, moles, hair loss, warts/skin tags, allergies, rosacea, birthmarks
- Cosmetic: Botox, fillers, hyperhidrosis Botox, peels, PRP, Dermapen/microneedling, mesotherapy, laser hair removal, anti-aging
- Ophthalmology: eye exam, dry eye, glaucoma, cataract, diabetic retinopathy, conjunctivitis, strabismus, pediatric eye care, refractive errors

Many are homepage sections/anchors rather than dedicated URLs.

## Architecture direction
Do not redesign from scratch. Homepage remains clinic/local/entity hub.

Recommended conceptual hierarchy:
- Homepage
  - Dermatology
    - Psoriasis
    - Acne scars
    - Vitiligo (existing)
    - Hair loss
    - Hyperhidrosis Botox (existing)
  - Cosmetic Dermatology
  - Ophthalmology
    - Eye examination
    - Dry eye
    - Cataract
    - Pediatric eye care
  - Doctors
    - Dr. Osama
    - Dr. Sara
  - Contact/location

Potential hubs after inspecting existing routes:
- `/dermatology`
- `/ophthalmology`
- one of `/cosmetic-dermatology` OR `/aesthetic-dermatology`

Avoid duplicate hubs.

## Priority pages
Highest priority:
1. Dermatology hub
2. Ophthalmology hub
3. Dr. Osama profile
4. Dr. Sara profile
5. Psoriasis
6. Acne-scar treatment

Next:
7. Hair loss
8. Eye examination
9. Dry eye
10. Cataract
11. Pediatric eye care

Improve rather than replace:
- `/vitiligo-jordan`
- `/botox-hyperhidrosis`
- `/school-health`

## Local SEO
Primary entity/location: Abu Nusair, Amman.

Nearby areas with current relevance: Shafa Badran, Jubaiha, Ain Al-Basha. Mention naturally. Do NOT currently create thin location doorway pages for each area. Reassess only when Search Console and genuine user value justify them.

## Internal links
Use crawlable `<a href>` links.

Homepage → Dermatology / Ophthalmology / Cosmetic / Doctors  
Dermatology → Psoriasis / Acne scars / Vitiligo / Hair loss / Hyperhidrosis  
Ophthalmology → Eye exam / Dry eye / Cataract / Pediatric eye care  
Doctors → specialty + relevant services  
Services → physician + parent specialty + related services + booking

Use descriptive natural anchors; do not mechanically exact-match every link.

## Medical/YMYL trust
Medical accuracy outranks aggressive SEO copy. Significant clinical pages should support responsible wording, physician attribution/review, physician profile link, and a genuine last-reviewed date after actual review.

Audit claims involving:
- percentages/success rates
- exact duration/onset
- FDA approval
- permanent/guaranteed/best/safest/complete cure
- recurrence
- superiority
- exact screening intervals
- claims that one treatment is the only effective treatment

Create `MEDICAL_REVIEW_REQUIRED.md` listing URL, exact wording, context and reason for review. Engineering agents should flag medical claims, not independently practice medicine.

Current live copy deserving review includes strong language around permanent laser hair removal, best/premium fillers, result guarantees/strong efficacy wording, hyperhidrosis Botox duration, cataract surgery wording, safety claims, complete healing, and mole-removal modalities.

## Physician entity pages
Dr. Osama: connect clinic → dermatology → appropriate services → booking.
Dr. Sara: connect clinic → ophthalmology → eye services → booking.

Use only verified credentials. Never invent board certification, memberships, affiliations, awards, experience duration or procedure counts.

## Technical SEO audit
Before editing check:
- status codes
- canonical tags
- robots directives and robots.txt
- XML sitemap and membership
- www/non-www
- trailing slashes
- duplicate titles/descriptions/H1
- orphan pages
- broken links / redirect chains
- OG metadata
- alt text
- structured data
- mobile rendering
- JS/indexability

Structured data must represent visible truthful entities. Potentially appropriate: clinic/organization/medical business, physician, service, breadcrumbs, website. Never fabricate ratings, reviews, credentials, services, prices, address details or outcomes.

## CTR/title strategy
Several page-one local queries have low/zero clicks. Test concise page-specific titles, not keyword lists.

Example style only:
- `دكتور جلدية في أبو نصير، عمّان | عيادات أوسارا`
- `طبيبة عيون في أبو نصير، عمّان | عيادات أوسارا`

Do not stuff every nearby area into titles.

## Conversion measurement
Search Console is not conversion analytics. Track at minimum:
- `whatsapp_click`
- `phone_click`
- `directions_click`
- `appointment_click`

Where possible add non-sensitive source page, specialty, service and campaign context.

Never put patient names, diagnoses, symptoms, consultation messages or treatment details in analytics.

## Mobile UX
Test priority pages on mobile. WhatsApp, call, directions and booking must be easy to reach. Ensure readable text, no overflow, usable navigation, non-obscuring sticky UI, limited layout shift, correct Arabic/English rendering and reasonable performance.

## Bilingual architecture
Do NOT perform a major `/ar/` + `/en/` migration now. Current bilingual URLs have growing history. Reassess separate-language architecture/hreflang later if evidence supports it.

## Workflow
Stack:
- GitHub: `osamawraikat-cyber/osara-clinics-website`
- Netlify
- Production: `https://osaraclinics.com`

Preferred workflow:
GSC/live evidence → inspect repo → baseline audit → SEO branch → implement → diff/PR → Netlify preview → technical/visual verification → physician medical review → approval → merge/deploy → monitor GSC.

Do not push risky structural changes directly to production.

## Baseline report required before editing
Record each indexable URL with:
- status
- title
- meta description
- H1
- canonical
- robots
- schema
- sitemap membership
- inbound/outbound internal links
- approximate content length

Also capture robots.txt, sitemap, redirects, representative desktop/mobile rendering and performance baseline if supported. Repeat after implementation.

## Do NOT
- redesign whole site without cause
- change domain
- reverse non-www canonicalization
- casually delete/rename indexed URLs
- mass-generate AI pages
- create thin nearby-location doorway pages
- keyword-stuff
- fabricate cases/reviews/credentials/statistics/references
- add services not actually provided
- remove/hide ophthalmology because dermatology has more traffic
- rewrite sensitive medical claims without physician review
- deploy structural changes without verification

## Operating timeline
**Now:** focused structural/technical sprint.  
**September:** indexation, technical verification, conversion measurement, GSC monitoring.  
**October:** optimize pages with meaningful impressions, positions ~4–15, weak CTR or strong conversion potential.  
**November:** deepen proven winners with physician-reviewed explanations, genuine FAQs, real imagery/cases where appropriate and consented, stronger links.  
**December:** strengthen ophthalmology entity/service/local signals.  
**2027+:** expand based on GSC + conversion evidence.

Evidence first, pages second.

## Exact instruction for the next coding session
> Access `osamawraikat-cyber/osara-clinics-website`. Do not modify anything yet. Read `OSARA_SEO_HANDOFF.md`, inspect the repository architecture and production site, identify the framework/build system, inspect Netlify configuration, enumerate current routes/pages, and compare the implementation against the handoff. Produce a baseline audit and proposed file-by-file implementation plan. Do not deploy or merge until the audit is reviewed.

The audit should answer:
1. Framework/build system?
2. Current route structure?
3. SEO hard-coded vs generated?
4. Sitemap/robots implementation?
5. Structured data?
6. Analytics?
7. Netlify configuration?
8. Which proposed pages already exist?
9. Duplicate-intent risks?
10. Files requiring modification?
11. New routes/files needed?
12. Medical claims to flag?
13. Changes that could damage current rankings?
14. Recommended first PR?

## Success criteria
- preserve existing search equity
- improve Abu Nusair dermatology visibility/CTR
- establish meaningful ophthalmology visibility
- priority service URLs gain their own impressions/clicks
- gradually reduce homepage dependence
- strengthen physician/specialty entity clarity
- trustworthy physician-reviewed medical content
- frictionless mobile conversion
- measurable WhatsApp/call/directions/appointment actions
- technically clean SEO
- future content driven by Search Console + conversions

The goal is qualified local discovery and patient conversion for a trustworthy dermatology + ophthalmology clinic, not traffic or page count for its own sake.
