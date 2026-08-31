from pathlib import Path

p=Path('index.html')
s=p.read_text(encoding='utf-8')
s=s.replace('طبيب جلدية وتجميل | Dermatologist','جلدية وتناسلية وليزر | Dermatologist')
s=s.replace('طبيب متخصص في الأمراض الجلدية والتجميل. يقدم الدكتور أسامة الوريكات في عيادة أوسارا بأبو نصير خدمات تشخيص وعلاج شاملة لأمراض الجلد والشعر والأظافر والتجميل غير الجراحي.','طبيب جلدية وتناسلية وليزر. يقدم الدكتور أسامة الوريكات في عيادة أوسارا بأبو نصير خدمات تشخيص وعلاج شاملة لأمراض الجلد والشعر والأظافر والتجميل غير الجراحي.')
block='''        .map-static-card {\n            display: flex;\n            flex-direction: column;\n            align-items: center;\n            justify-content: center;\n            text-align: center;\n            padding: 36px;\n            background: linear-gradient(145deg, #ffffff 0%, #E6F3F4 100%);\n        }\n\n        .map-static-icon {\n            width: 76px;\n            height: 76px;\n            border-radius: 50%;\n            display: flex;\n            align-items: center;\n            justify-content: center;\n            margin-bottom: 18px;\n            background: var(--primary);\n            color: #fff;\n            font-size: 2rem;\n            box-shadow: var(--shadow-md);\n        }\n\n        .map-static-card h3 { margin-bottom: 8px; font-size: 1.45rem; }\n        .map-static-card > p { margin-bottom: 8px; }\n        .map-actions { margin-top: 22px; width: 100%; max-width: 620px; }\n\n'''
if s.count(block)>1:
    first=s.find(block)
    second=s.find(block, first+len(block))
    s=s[:second]+s[second+len(block):]
p.write_text(s,encoding='utf-8')

p=Path('doctors/dr-osama-alwreikat.html')
s=p.read_text(encoding='utf-8')
s=s.replace('<title>د. أسامة الوريكات — طبيب جلدية | عيادات أوسارا</title>','<title>د. أسامة الوريكات — جلدية وتناسلية وليزر | عيادات أوسارا</title>')
s=s.replace('<meta property="og:title" content="د. أسامة الوريكات — طبيب جلدية | عيادات أوسارا">','<meta property="og:title" content="د. أسامة الوريكات — جلدية وتناسلية وليزر | عيادات أوسارا">')
p.write_text(s,encoding='utf-8')
