from pathlib import Path

files = [
'index.html','dermatology.html','ophthalmology.html','doctors/dr-osama-alwreikat.html','doctors/dr-sara-abu-touq.html','psoriasis-treatment.html','acne-scar-treatment.html','vitiligo-jordan.html','botox-hyperhidrosis.html','mole-removal.html','school-health.html']

snippet = '''  <!-- Google tag (gtag.js) -->\n  <script async src="https://www.googletagmanager.com/gtag/js?id=G-72BY7LC2V2"></script>\n  <script>\n    window.dataLayer = window.dataLayer || [];\n    function gtag(){dataLayer.push(arguments);}\n    gtag('js', new Date());\n    gtag('config', 'G-72BY7LC2V2');\n  </script>\n'''

for name in files:
    p=Path(name)
    text=p.read_text(encoding='utf-8')
    assert 'G-72BY7LC2V2' not in text, name
    assert '</head>' in text, name
    text=text.replace('</head>', snippet + '</head>', 1)
    p.write_text(text, encoding='utf-8')
