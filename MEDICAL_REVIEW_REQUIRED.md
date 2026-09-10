# Medical Review Required

This file intentionally flags medically sensitive wording for physician review. Engineering should not silently rewrite these claims. URLs below use the public extensionless convention.

| URL | Exact wording / source wording | Context | Reason for review |
|---|---|---|---|
| `/` | “Early diagnosis and regular follow-up with a dermatologist in Amman significantly improves treatment outcomes.” | Vitiligo card | Strong outcome claim; requires physician review and evidence-appropriate wording. |
| `/` | “Modern treatments effectively control psoriasis and reduce flares.” | Psoriasis card | General efficacy claim; confirm wording and scope. |
| `/` | “Acne scars and post-inflammatory hyperpigmentation are treatable with the right medical approach.” | Acne-scar card | Treatment-effect claim; confirm that wording is appropriately qualified. |
| `/` | “with effective treatments including specialized Botox injections” and “proven protocols.” | Hyperhidrosis card | Efficacy/proven wording requires review. |
| `/` | “Regular mole checks with a dermatologist are essential, especially for numerous or large nevi.” | Mole card | Screening recommendation/interval implication requires review. |
| `/` | “Botox injections are a safe, non-surgical cosmetic procedure…” and “natural, safe results.” | Cosmetic Botox card | Safety/outcome wording requires physician review. |
| `/` | “uses premium certified fillers to deliver natural, balanced results.” / “يستخدم أفضل أنواع الفيلر المعتمدة” | Dermal fillers card | “Best/premium/certified” and outcome wording should be substantiated and physician-reviewed. |
| `/` | “Botox for hyperhidrosis is a safe and effective treatment… with results lasting 6-12 months.” | Hyperhidrosis Botox card | Safety, efficacy and exact duration claims require review. |
| `/` | “Laser hair removal is the optimal solution for permanent and effective removal of unwanted hair compared to traditional methods.” | Laser hair-removal card | Superiority and permanence claims require review. |
| `/` | “نقوم بوضع بروتوكول علاجي مخصص ومتابعة مستمرة ودقيقة لضمان أفضل النتائج والشفاء التام.” | Personalized-care section | “Guarantee,” “best results,” and “complete healing” language is inappropriate without explicit medical/legal review. |
| `/` | “Surgery is the only effective treatment with excellent outcomes.” / “الجراحة هي العلاج الوحيد الفعّال ونتائجها ممتازة.” | Cataract card | “Only effective treatment” and outcome wording require ophthalmologist review and evidence-appropriate qualification. |
| `/` | “Every diabetic patient is advised to have regular retinal screenings.” | Diabetic-retinopathy card | Screening recommendation should be checked against the intended patient population and current clinical guidance. |
| `/` | “Early diagnosis, especially in children, is essential to prevent permanent vision impairment.” | Strabismus card | Strong prevention/outcome wording requires ophthalmologist review. |
| `/` | “Early pediatric eye exams detect vision problems, strabismus, and amblyopia at a treatable stage.” | Pediatric-eye-care card | Screening/treatability wording requires ophthalmologist review. |
| `/` | “Accurate refraction testing and proper glasses or contact lens prescription significantly improves quality of life.” | Refractive-errors card | Strong outcome wording requires review. |
| `/botox-hyperhidrosis` | “نتائج تدوم حتى 12 شهراً.” | Meta description | Exact duration claim; patient response varies and requires physician-reviewed wording. |
| `/botox-hyperhidrosis` | “حل آمن وفعّال… بنسب نجاح عالية ونتائج تدوم حتى عام كامل” / “A safe and effective medical solution… with results lasting up to 12 months.” | Hero | Safety, efficacy, success-rate and exact-duration wording require review. |
| `/botox-hyperhidrosis` | “Dr. Osama Alwreikat… provides FDA-approved Botox injections to safely block sweat signals.” | Introductory explanation | Regulatory and safety claim; confirm product/indication-specific accuracy. |
| `/botox-hyperhidrosis` | “Reduces sweating by 85% to 95%…” / “تقليل إفراز العرق… بنسبة تتراوح بين 85% إلى 95%.” | Mechanism/results section | Exact efficacy percentage requires sourcing and physician review. |
| `/botox-hyperhidrosis` | “Results begin showing within 3–7 days, reaching full efficacy in 2 weeks.” | Expected results | Exact onset/time-to-maximum-effect claim requires review. |
| `/botox-hyperhidrosis` | “Results last 6 to 12 months and can be safely repeated annually.” | Expected results | Exact duration and repeat-safety wording require review. |
| `/botox-hyperhidrosis` | “Yes, it is FDA-approved and performed under strict medical safety standards using certified authentic products…” | FAQ | Regulatory/safety/product-authenticity claim requires verification. |
| `/botox-hyperhidrosis` | “compensatory sweating is extremely rare with Botox injections compared to surgical options…” | FAQ | Comparative adverse-event frequency claim requires evidence-appropriate wording. |
| `/vitiligo-jordan` | “Modern dermatology focuses on halting disease progression and restoring natural skin pigment with high success rates, especially when initiated early.” | FAQ answer | “High success rates” and timing/outcome relationship require review. |
| `/vitiligo-jordan` | “Early clinical diagnosis and structured medical follow-ups with a dermatologist significantly improve re-pigmentation outcomes.” | Introductory explanation | Strong outcome claim requires review. |
| `/mole-removal` | “Comprehensive guide on dermoscopic mole screening and scar-free laser or surgical removal.” | JSON-LD description | “Scar-free” is an outcome guarantee and should not remain without explicit physician approval. |
| `/mole-removal` | Any wording that implies laser removal is appropriate for all moles or that removal is scar-free, safest, permanent, or guaranteed | Main guide | Modality selection and outcome guarantees require physician review. |
| `/school-health` | Any exact screening interval, guaranteed/rapid cure wording, “safe/painless” procedure wording, or claims of complete healing | Main guide | Pediatric screening intervals, safety and efficacy claims require physician review. |

## Wave 1 physician-reviewed pages — APPROVED 2026-09-10

The 15 Wave-1 pages below were reviewed by the physician and are approved **only for the reviewed wording after the corrections documented on 2026-09-10**. This approval does not extend to arbitrary future copy changes. The older unresolved review items above remain pending and are not approved by this section.

| URL | Physician review decision / approved boundary |
|---|---|
| `/vitiligo-surgery-jordan` | **APPROVED — 2026-09-10.** Clinical stability and candidacy remain individualized; NCMT and punch minigrafting remain separate pathways; no fixed success percentage. |
| `/melanocyte-transplantation-vitiligo` | **APPROVED — 2026-09-10.** NCMT terminology, donor/recipient pathway, stability/candidacy, recovery/repigmentation expectations and phototherapy reference reviewed. No cultured melanocyte transplantation claim. |
| `/punch-grafting-vitiligo` | **APPROVED — 2026-09-10.** Punch/mini-punch terminology, candidacy, donor/recipient pathway, limitations including colour/texture/cobblestoning/marks, and comparison with NCMT reviewed. |
| `/acne-treatment` | **APPROVED — 2026-09-10.** Visible clinical content approved; schema wording uses reduction of scarring risk rather than prevention. |
| `/hair-loss-treatment` | **APPROVED — 2026-09-10.** Diagnostic pathway and PRP scope reviewed; FUE/DHI are clearly distinguished from hair-loss services currently offered at OSara. |
| `/wart-removal-cryotherapy` | **APPROVED — 2026-09-10.** Cryotherapy indication, freeze-thaw wording, pigment-change/scar risk, repeat-treatment language and differential-diagnosis cautions reviewed. No single-session clearance guarantee. |
| `/skin-biopsy` | **APPROVED — 2026-09-10.** Biopsy indications, histopathology pathway, possible additional testing, wound care and bleeding/pain/infection/scar risks reviewed. |
| `/melasma-pigmentation-treatment` | **APPROVED — 2026-09-10.** Diagnostic distinctions, light protection, topical/procedural categories, recurrence/maintenance and skin-type suitability reviewed. No permanent-clearance claim. |
| `/cataract-surgery` | **APPROVED — 2026-09-10.** Cataract indications, lens planning, expectations and surgical pathway reviewed. Surgery requiring an operating theatre occurs at an appropriate hospital/facility; no implication it occurs inside OSara and no universal sole/primary-surgeon claim for Dr Sara. |
| `/glaucoma-treatment` | **APPROVED — 2026-09-10.** Diagnostic/treatment categories, goal of slowing/preventing further damage, monitoring and facility pathway reviewed. Laser/surgery is not implied to occur inside OSara when required equipment/facility is unavailable there. |
| `/diabetic-eye-exam-retinopathy` | **APPROVED — 2026-09-10.** Screening/follow-up wording, retinal referral/co-management and prompt-review symptoms reviewed. |
| `/pterygium-treatment-surgery` | **APPROVED — 2026-09-10.** Observation versus surgery, operative pathway, recurrence and expectation wording reviewed; operating-theatre procedures occur at an appropriate hospital/facility. |
| `/pediatric-ophthalmology` | **APPROVED — 2026-09-10.** Age-appropriate routine vision screening, earlier complete examination for symptoms/risk factors, amblyopia terminology and prompt-review symptoms reviewed. |
| `/strabismus-treatment` | **APPROVED — 2026-09-10.** Refraction/amblyopia assessment, individualized treatment and eye-muscle surgical pathway reviewed; surgical team is case-dependent with no universal sole/primary-surgeon claim. |
| `/dry-eye-treatment` | **APPROVED — 2026-09-10.** Dry-eye causes/subtypes, examination, stepped treatment, screen/airflow symptom wording and prompt-review vision wording reviewed. |

The approved ophthalmology surgical model across Wave 1 is: consultation/examination and planning through OSara → surgery at an appropriate hospital or surgical facility when an operating facility is required → physician/clinic follow-up. Dr Sara participates in surgical care and follow-up, while her role during an operation and the surgical team depend on the individual case and procedure. This approval must not be expanded into an unsupported claim that she is sole/primary surgeon for every operation.

## PR #2 physician-reviewed items — APPROVED

The following four PR #2 items were reviewed and approved by the physician on 2026-08-31. They are no longer unresolved review requirements. Older PR #1 flags above remain pending and are not approved by this section.

| URL | Physician review decision | Approved boundary / implementation |
|---|---|---|
| `/psoriasis-treatment` | **APPROVED** — psoriasis joint symptoms | The page may state that joint pain, stiffness or swelling can occur in association with psoriasis and should be discussed with the treating physician/dermatologist. |
| `/psoriasis-treatment` | **APPROVED WITH CONSERVATIVE WORDING** — urgent assessment | Urgent assessment may be advised for rapidly widespread/severe psoriasis, widespread pustulation particularly with systemic illness, or other severe acute symptoms. Ordinary stable plaque psoriasis must not be presented as a medical emergency. |
| `/acne-scar-treatment` | **APPROVED** — morphology and treatment selection | Treatment may be described as morphology-dependent. Subcision may be considered for selected tethered/rolling scars; TCA CROSS may be considered for selected deep/narrow or ice-pick scars. Wording must remain individualized and non-prescriptive. |
| `/acne-scar-treatment` | **APPROVED** — multiple sessions / combination treatment | It is appropriate to state that improvement often requires multiple sessions and that mixed scar morphologies may benefit from staged or combination treatment. Do not promise complete scar removal or a specific percentage of improvement. |

## Review workflow

1. Physician reviews each flagged statement in context.
2. Approved replacement wording is documented explicitly.
3. Only then should the production copy be changed.
4. Add a genuine last-reviewed date to significant medical pages only after actual physician review.

No medically sensitive claims were rewritten as part of SEO PR #1. The four PR #2 items documented above have completed physician review; all older PR #1 flags remain pending. The 15 Wave 1 pages listed above were physician-reviewed and approved on 2026-09-10 for the reviewed wording after the specified corrections; future substantive medical copy changes require review.
