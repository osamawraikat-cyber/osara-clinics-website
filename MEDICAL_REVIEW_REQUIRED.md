# Medical Review Required

This file intentionally flags medically sensitive wording for physician review. Engineering should not silently rewrite these claims. URLs below use the public extensionless convention.

| URL | Exact wording / source wording | Context | Reason for review |
|---|---|---|---|
| `/` | “Early diagnosis and regular follow-up with a dermatologist in Amman significantly improves treatment outcomes.” | Vitiligo card | Strong outcome claim; requires physician review and evidence-appropriate wording. |
| `/` | “Modern treatments effectively control psoriasis and reduce flares.” | Psoriasis card | General efficacy claim; confirm wording and scope. |
| `/` | “Acne scars and post-inflammatory hyperpigmentation are treatable with the right medical approach.” | Acne-scar card | Treatment-effect claim; confirm that wording is appropriately qualified. |
| `/` | “with effective treatments including specialized Botox injections” and “proven protocols.” | Hyperhidrosis card | Efficacy/proven wording requires review. |
| `/` | “Regular mole checks with a dermatologist are essential, especially for numerous or large nevi.” | Mole card | Screening recommendation/interval implication requires review. |
| `/botox-hyperhidrosis` | “نتائج تدوم حتى 12 شهراً.” | Meta description | Exact duration claim; patient response varies and requires physician-reviewed wording. |
| `/botox-hyperhidrosis` | “Botox for Hyperhidrosis” / any FDA-approval, onset, duration, success-rate or safety wording on the page | Main guide | Regulatory, efficacy, onset/duration and safety claims are explicitly YMYL-sensitive. Review before optimization. |
| `/vitiligo-jordan` | “Modern dermatology focuses on halting disease progression and restoring natural skin pigment with high success rates, especially when initiated early.” | FAQ answer | “High success rates” and timing/outcome relationship require review. |
| `/vitiligo-jordan` | “Early clinical diagnosis and structured medical follow-ups with a dermatologist significantly improve re-pigmentation outcomes.” | Introductory explanation | Strong outcome claim requires review. |
| `/mole-removal` | “Comprehensive guide on dermoscopic mole screening and scar-free laser or surgical removal.” | JSON-LD description | “Scar-free” is an outcome guarantee and should not remain without explicit physician approval. |
| `/mole-removal` | Any wording that implies laser removal is appropriate for all moles or that removal is scar-free, safest, permanent, or guaranteed | Main guide | Modality selection and outcome guarantees require physician review. |
| `/school-health` | Any exact screening interval, guaranteed/rapid cure wording, “safe/painless” procedure wording, or claims of complete healing | Main guide | Pediatric screening intervals, safety and efficacy claims require physician review. |
| `/` | Any “best”, “premium”, “permanent”, “guaranteed”, “safest”, “only effective treatment”, exact duration/onset, recurrence, or superiority wording in cosmetic/ophthalmology sections | Homepage | These categories were identified in the SEO handoff as requiring physician review rather than engineering edits. |

## Review workflow

1. Physician reviews each flagged statement in context.
2. Approved replacement wording is documented explicitly.
3. Only then should the production copy be changed.
4. Add a genuine last-reviewed date to significant medical pages only after actual physician review.

No medical claims were rewritten as part of SEO PR #1.
