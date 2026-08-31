from pathlib import Path

# Align psoriasis urgent wording to the physician-approved conservative boundary.
p = Path('psoriasis-treatment.html')
s = p.read_text()
old = '<section class="card"><h2>متى قد يكون التقييم عاجلاً؟</h2><p>اطلب تقييماً طبياً عاجلاً إذا أصبحت الصدفية واسعة جداً أو شديدة الاحمرار والألم، ظهرت بثرات منتشرة مع حرارة أو شعور عام بالتعب، حدث تدهور سريع، أو ظهرت أعراض مفصلية شديدة. الحالات الشديدة أو المهددة للحياة تستدعي التوجه إلى قسم الطوارئ المناسب.</p><p class="en">Seek urgent medical assessment for rapid widespread worsening, marked redness or pain, widespread pustules with fever or systemic illness, or severe joint symptoms. Severe or life-threatening illness belongs in the appropriate emergency department.</p></section>'
new = '<section class="card"><h2>متى قد يكون التقييم عاجلاً؟</h2><p>الصدفية اللويحية المستقرة المعتادة لا تُعد بحد ذاتها حالة طارئة. اطلب تقييماً طبياً عاجلاً عند حدوث تدهور سريع وواسع أو شديد، أو ظهور بثرات منتشرة خصوصاً مع حرارة أو شعور عام بالتعب، أو أعراض حادة وشديدة أخرى. الحالات الشديدة أو المهددة للحياة تستدعي التوجه إلى قسم الطوارئ المناسب.</p><p class="en">Ordinary stable plaque psoriasis is not, by itself, a medical emergency. Seek urgent medical assessment for rapid widespread or severe worsening, widespread pustulation particularly with fever or systemic illness, or other severe acute symptoms. Severe or life-threatening illness belongs in the appropriate emergency department.</p></section>'
if old not in s:
    raise SystemExit('psoriasis urgent block not found')
s = s.replace(old, new, 1)
p.write_text(s)

# Align acne-scar wording exactly with physician-approved individualized morphology guidance.
p = Path('acne-scar-treatment.html')
s = p.read_text()
s = s.replace('أفضل خطة لندبات حب الشباب لا تبدأ باسم جهاز أو جلسة؛', 'الخطة المناسبة لندبات حب الشباب لا تبدأ باسم جهاز أو جلسة؛', 1)
old = '<div class="mini"><strong>Subcision | السبسجن</strong><br>تحرير الأشرطة الليفية تحت بعض الندبات المنخفضة، خصوصاً الندبات المتدحرجة أو الملتصقة.</div>'
new = '<div class="mini"><strong>Subcision | السبسجن</strong><br>قد يُناقش لتحرير الأشرطة الليفية في حالات مختارة، خصوصاً بعض الندبات المتدحرجة أو الملتصقة، بحسب الفحص.</div>'
if old not in s:
    raise SystemExit('subcision block not found')
s = s.replace(old, new, 1)
old = '<div class="mini"><strong>TCA CROSS</strong><br>تطبيق موضعي ومحدد لحمض ثلاثي كلورو الأسيتيك داخل بعض الندبات الضامرة، وغالباً يُناقش في الندبات العميقة الضيقة أو بعض أنواع boxcar.</div>'
new = '<div class="mini"><strong>TCA CROSS</strong><br>قد يُناقش كتطبيق موضعي ومحدد لحمض ثلاثي كلورو الأسيتيك في حالات مختارة من الندبات العميقة والضيقة، وخصوصاً بعض ندبات ice-pick، بحسب الفحص.</div>'
if old not in s:
    raise SystemExit('TCA block not found')
s = s.replace(old, new, 1)
p.write_text(s)

# Record PR2 review decisions as completed while keeping all older PR1 flags unresolved.
p = Path('MEDICAL_REVIEW_REQUIRED.md')
s = p.read_text()
start = s.index('\n| `/psoriasis-treatment` |')
end = s.index('\n## Review workflow', start)
approved = '''

## PR #2 physician-reviewed items — APPROVED

The following four PR #2 items were reviewed and approved by the physician on 2026-08-31. They are no longer unresolved review requirements. Older PR #1 flags above remain pending and are not approved by this section.

| URL | Physician review decision | Approved boundary / implementation |
|---|---|---|
| `/psoriasis-treatment` | **APPROVED** — psoriasis joint symptoms | The page may state that joint pain, stiffness or swelling can occur in association with psoriasis and should be discussed with the treating physician/dermatologist. |
| `/psoriasis-treatment` | **APPROVED WITH CONSERVATIVE WORDING** — urgent assessment | Urgent assessment may be advised for rapidly widespread/severe psoriasis, widespread pustulation particularly with systemic illness, or other severe acute symptoms. Ordinary stable plaque psoriasis must not be presented as a medical emergency. |
| `/acne-scar-treatment` | **APPROVED** — morphology and treatment selection | Treatment may be described as morphology-dependent. Subcision may be considered for selected tethered/rolling scars; TCA CROSS may be considered for selected deep/narrow or ice-pick scars. Wording must remain individualized and non-prescriptive. |
| `/acne-scar-treatment` | **APPROVED** — multiple sessions / combination treatment | It is appropriate to state that improvement often requires multiple sessions and that mixed scar morphologies may benefit from staged or combination treatment. Do not promise complete scar removal or a specific percentage of improvement. |
'''
s = s[:start] + approved + s[end:]
s = s.replace('No medically sensitive claims were rewritten as part of SEO PR #1. PR #2 adds the statements above for physician verification rather than presenting uncertain details as guarantees.', 'No medically sensitive claims were rewritten as part of SEO PR #1. The four PR #2 items documented above have completed physician review; all older PR #1 flags remain pending.')
p.write_text(s)
