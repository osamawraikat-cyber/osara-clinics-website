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

## Current GBP state and implementation pause

### GBP category state
- Primary category: Dermatologist.
- Secondary categories currently intended: Clinic, Skin Care Clinic, Ophthalmology Clinic.
- Health and Beauty Shop was removed.
- Avoid further category churn while recent Google edits are being reviewed.

### GBP location and service-area decisions
- OSara is a physical clinic.
- Previously configured service areas were removed.
- Do not add neighborhoods as service areas merely for SEO unless the business genuinely becomes a qualifying service-area or hybrid business.
- Keep the physical address accurate.
- A move to an adjacent building is expected. Update address, coordinates and NAP together only when the move actually occurs.

### GBP contact state
- Canonical website URL: `https://osaraclinics.com/`, not `www`.
- Existing contact/WhatsApp information should remain consistent with authoritative clinic information.
- Future dedicated `/services` and `/book` URLs are ideas only, not approved implementation.

### GBP dermatology services
The dermatology service inventory has recently been expanded substantially. Important services include:
- Dermatology Consultation
- Acne Treatment
- Acne Scar Treatment
- Subcision for Acne Scars
- Chemical Peel
- Microneedling / Dermapen
- PRP Skin Treatment
- PRP Hair Loss Treatment
- Hair Loss Treatment
- Skin Boosters
- Hyperhidrosis Treatment
- Botox Injections
- Dermal Fillers
- Vitiligo Treatment
- Psoriasis Treatment
- Eczema Treatment
- Rosacea Treatment
- Mole / skin lesion services
- Wart Removal
- Skin Biopsy
- Cryotherapy
- other genuinely offered dermatology services already present in GBP

Do not create duplicate services merely to use alternate keyword wording.

### GBP ophthalmology services
Ophthalmology services were expanded to provide much broader, truthful service coverage, including relevant combinations of:
- Ophthalmology Consultation
- Comprehensive Eye Examination / Eye Examination
- Vision Testing
- Dry Eye Treatment
- Eye Infection Treatment
- Eye Allergy Treatment
- Red Eye Treatment
- Cataract Treatment
- Cataract Surgery
- Glaucoma Treatment
- Glaucoma Surgery
- Diabetic Eye Examination
- Diabetic Retinopathy Treatment
- Retinal Disease Evaluation/Treatment
- Pediatric Eye Examination
- Strabismus Evaluation/Treatment
- Eyelid Conditions
- Chalazion Treatment/Removal
- Foreign Body Removal
- Pterygium Treatment
- Pterygium Surgery
- Refractive Error Evaluation
- other genuinely offered services already visible in the current GBP

Do not invent a service that is not actually offered.

### Surgical-intent SEO principle
OSara wants to capture high-intent surgical searches when the service is genuinely provided through the clinic/physician.

Do not unnecessarily replace truthful service terms such as Cataract Surgery, Glaucoma Surgery, Pterygium Surgery, or Eyelid Surgery (if genuinely offered) with generic “evaluation” wording merely out of SEO/medical caution.

Truthfulness remains mandatory, but genuine surgical capabilities should be represented clearly because patients commonly search specifically for physicians who perform these procedures.

### GBP service descriptions
Current decision:
- Do NOT rush to populate descriptions for every newly added service.
- Allow recent service/category edits to settle first.
- Later, selectively write useful descriptions for high-value services.
- Descriptions should explain candidacy/service scope naturally.
- Do not keyword-stuff.
- Do not mechanically repeat “Abu Nusair, Amman” in every description.
- Do not make guarantees or unsupported superiority/safety claims.

### AI-search baseline observation
A qualitative AI-assisted local search was able to identify OSara Clinics in Abu Nseir, associate it with Dr. Osama Alwreikat, identify vitiligo treatment, and surface the clinic contact information.

However, when the query became specifically about melanocyte transplantation for vitiligo, the system did not have enough OSara-specific public evidence to confidently verify that procedure at OSara and instead surfaced stronger evidence for another institution.

Interpretation:
- OSara's general local/entity visibility appears to be developing.
- The clinic → doctor → vitiligo relationship is understandable.
- The clinic → doctor → NCMT/melanocyte transplantation relationship is currently weaker.
- Treat this as an evidence/entity gap worth investigating later, not proof of a ranking position or a controlled benchmark.

### Hair-transplant distinction
Do not treat every missing search result as an SEO failure.

If OSara does not genuinely perform surgical hair transplantation such as FUE/DHI, do not attempt to rank generic hair-loss/PRP services as “hair transplant.” Only target surgical hair-transplant intent if that service becomes genuinely available.

This differs from NCMT if melanocyte transplantation is genuinely provided through OSara.

### Current implementation status
At the time of this documentation update:
- GBP has undergone substantial recent edits.
- Some edits were pending Google review when last checked.
- Website implementation is intentionally paused.
- Netlify credit constraints currently make unnecessary deployments undesirable.
- Allow current SEO architecture and GBP edits time to settle.
- Next major implementation decisions should follow a fresh combined audit rather than automatically continuing page expansion.

## Operating timeline
**Now:** focused structural/technical sprint.  
**September:** indexation, technical verification, conversion measurement, GSC monitoring.  
**October:** optimize pages with meaningful impressions, positions ~4–15, weak CTR or strong conversion potential.  
**November:** deepen proven winners with physician-reviewed explanations, genuine FAQs, real imagery/cases where appropriate and consented, stronger links.  
**December:** strengthen ophthalmology entity/service/local signals.  
**2027+:** expand based on GSC + conversion evidence.

Evidence first, pages second.

## Deferred SEO / AI Visibility Backlog
These are future opportunities only, not approved implementation work.

- AI-search / answer-engine visibility should be audited alongside normal Google SEO.
- Future audits should test whether systems such as Google AI results, ChatGPT-style search, Gemini-style search, and similar answer engines can confidently connect OSara Clinics → Dr. Osama Alwreikat / Dr. Sara Abu Touq → specific services → Abu Nusair/Amman → correct contact/appointment information.
- Optimize underlying factual entity evidence rather than creating “AI SEO” gimmicks or thin pages.
- Strengthen explicit relationships between clinic, doctors, specialties, services, location, and contact details using useful site content, internal linking, structured data where appropriate, GBP consistency, and authoritative public references.
- Identified evidence gap: OSara currently has public visibility for vitiligo treatment, but AI/search systems may not confidently associate OSara specifically with melanocyte transplantation / NCMT.
- Future consideration, only if the service is genuinely offered through OSara:
  - Melanocyte Transplantation for Vitiligo
  - Non-cultured Melanocyte Transplantation (NCMT)
  - Vitiligo Surgery
  - Arabic terminology such as `زراعة الخلايا الصبغية للبهاق` and `جراحة البهاق`
- This NCMT topic may later warrant clearer GBP service representation, stronger vitiligo-page content, doctor-profile association, and possibly a dedicated page if search demand and evidence justify it.
- Ophthalmology future high-intent SEO clusters to evaluate after current data matures:
  - cataract treatment / cataract surgery
  - glaucoma treatment / glaucoma surgery
  - diabetic eye examination / diabetic retinopathy
  - retinal disease
  - dry eye
  - pediatric ophthalmology
  - strabismus
  - eyelid conditions / eyelid surgery
  - pterygium / pterygium surgery
- Do not create one thin page per keyword. Use intent clusters and only create dedicated pages when the service is real and search/business value justifies it.
- Potential future `/services` directory:
  - should cover both Dermatology and Ophthalmology
  - could later be used as the GBP services/menu URL
  - should link into specialty hubs and relevant service pages
- GBP service descriptions may be optimized later, selectively, after the current service/category edits have settled.
- Do not keyword-stuff service descriptions or repeat “Abu Nusair, Amman” mechanically in every service.
- Future audits should combine Google Business Profile, Google Search Console, GA4 conversion events, local rankings, technical SEO, live-site content, and AI/answer-engine visibility.
- Use fresh data before deciding new pages or major structural changes.
- Existing principle remains: broad legitimate query coverage is desired, but relevance and truthfulness outrank keyword volume.
- High-intent surgical services should be represented explicitly when genuinely offered; do not unnecessarily downgrade them to “evaluation only.”
- Do not claim procedures or surgeries that are not genuinely provided through OSara.

**Status: DEFERRED / BACKLOG ONLY.**  
These items are not authorization to modify or deploy the production website.  
No production changes should be made from this section until a future audit is completed and the next PR is explicitly approved.  
Netlify credit constraints are one reason implementation is currently paused.

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
