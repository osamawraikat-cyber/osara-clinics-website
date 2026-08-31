from pathlib import Path

# Homepage: add one natural service-page link to existing psoriasis and acne-scar cards.
p = Path('index.html')
s = p.read_text()
psoriasis_anchor = '<div class="card-cta-wrapper">\n                        <a href="https://wa.me/962778423361?text=%D9%85%D8%B1%D8%AD%D8%A8%D8%A7%20%D8%B9%D9%8A%D8%A7%D8%AF%D8%A7%D8%AA%20%D8%A3%D9%88%D8%B3%D8%A7%D8%B1%D8%A7%D8%8C%20%D8%A3%D9%88%D8%AF%20%D8%A7%D9%84%D8%A7%D8%B3%D8%AA%D9%81%D8%B3%D8%A7%D8%B1%20%D8%B9%D9%86%20%D8%B9%D9%84%D8%A7%D8%AC%20%D8%A7%D9%84%D8%B5%D8%AF%D9%81%D9%8A%D8%A9%20%7C%20Psoriasis"'
if psoriasis_anchor not in s:
    raise SystemExit('psoriasis homepage anchor not found')
s = s.replace(psoriasis_anchor, '<p style="margin:12px 0 0;"><a href="/psoriasis-treatment">اقرأ دليل علاج الصدفية | Psoriasis treatment guide</a></p>\n                    ' + psoriasis_anchor, 1)
acne_anchor = '<div class="card-cta-wrapper">\n                        <a href="https://wa.me/962778423361?text=%D9%85%D8%B1%D8%AD%D8%A8%D8%A7%20%D8%B9%D9%8A%D8%A7%D8%AF%D8%A7%D8%AA%20%D8%A3%D9%88%D8%B3%D8%A7%D8%B1%D8%A7%D8%8C%20%D8%A3%D9%88%D8%AF%20%D8%A7%D9%84%D8%A7%D8%B3%D8%AA%D9%81%D8%B3%D8%A7%D8%B1%20%D8%B9%D9%86%20%D8%B9%D9%84%D8%A7%D8%AC%20%D9%86%D8%AF%D8%A8%D8%A7%D8%AA%20%D8%AD%D8%A8%20%D8%A7%D9%84%D8%B4%D8%A8%D8%A7%D8%A8%20%7C%20Acne%20Scars"'
if acne_anchor not in s:
    raise SystemExit('acne homepage anchor not found')
s = s.replace(acne_anchor, '<p style="margin:12px 0 0;"><a href="/acne-scar-treatment">اقرأ دليل علاج ندبات حب الشباب | Acne scar treatment guide</a></p>\n                    ' + acne_anchor, 1)
p.write_text(s)

# Existing priority guides: insert a compact, contextual related-reading section before the footer.
related = {
    'vitiligo-jordan.html': '''\n        <div class="card-box">\n            <h2>مواضيع جلدية ذات صلة</h2>\n            <div class="h2-en">Related Dermatology Guides</div>\n            <p>للمزيد، راجع <a href="/dermatology">بوابة الأمراض الجلدية</a>، <a href="/psoriasis-treatment">دليل علاج الصدفية</a> أو <a href="/acne-scar-treatment">دليل علاج ندبات حب الشباب</a>.</p>\n        </div>\n''',
    'botox-hyperhidrosis.html': '''\n        <div class="card-box">\n            <h2>مواضيع جلدية ذات صلة</h2>\n            <div class="h2-en">Related Dermatology Guides</div>\n            <p>ارجع إلى <a href="/dermatology">بوابة الأمراض الجلدية</a>، أو اقرأ عن <a href="/psoriasis-treatment">الصدفية</a> و<a href="/acne-scar-treatment">ندبات حب الشباب</a>.</p>\n        </div>\n''',
    'mole-removal.html': '''\n        <div class="card-box">\n            <h2>مواضيع جلدية ذات صلة</h2>\n            <div class="h2-en">Related Dermatology Guides</div>\n            <p>للمزيد من المعلومات، راجع <a href="/dermatology">بوابة الأمراض الجلدية</a>، <a href="/psoriasis-treatment">دليل الصدفية</a> و<a href="/acne-scar-treatment">دليل ندبات حب الشباب</a>.</p>\n        </div>\n'''
}
for filename, block in related.items():
    p = Path(filename); s = p.read_text()
    marker = '\n    </div>\n\n    <!-- FOOTER'
    if marker not in s:
        marker = '\n    </div>\n\n    <footer'
    if marker not in s:
        raise SystemExit(f'footer marker not found: {filename}')
    s = s.replace(marker, block + marker, 1)
    p.write_text(s)

# Add only the new PR2 statements that merit physician verification.
p = Path('MEDICAL_REVIEW_REQUIRED.md'); s = p.read_text()
rows = '''| `/psoriasis-treatment` | “Some patients may also develop joint symptoms that warrant assessment.” | Psoriasis overview | Association with psoriatic arthritis is appropriate but wording should be physician-reviewed for scope and escalation. |\n| `/psoriasis-treatment` | “Seek urgent medical assessment if psoriasis becomes very widespread, intensely red/painful, or widespread pustules occur with fever or systemic illness.” | Urgent assessment section | Escalation language should be physician-reviewed for severity thresholds and local care pathways. |\n| `/acne-scar-treatment` | “Subcision may be considered for some rolling or tethered depressed scars; TCA CROSS may be discussed for selected deeper narrow scars.” | Treatment-options section | Procedure-to-scar matching is medically specific and should be physician-reviewed; page does not claim these procedures are available at OSara Clinics. |\n| `/acne-scar-treatment` | “Many cases require multiple sessions and may benefit from a staged combination plan.” | Expectations section | General treatment-course statement should be physician-reviewed and kept free of guaranteed outcomes. |\n'''
needle = '\n## Review workflow\n'
if needle not in s: raise SystemExit('medical review insertion point missing')
s = s.replace(needle, '\n' + rows + needle, 1)
s = s.replace('No medically sensitive claims were rewritten as part of SEO PR #1.', 'No medically sensitive claims were rewritten as part of SEO PR #1. PR #2 adds the statements above for physician verification rather than presenting uncertain details as guarantees.')
p.write_text(s)
