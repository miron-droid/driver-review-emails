"""Собирает письма всех компаний из _base/template.html и companies.json.

  python3 build.py

Для каждой компании пишет <id>/template.html (вставлять в портал) и
<id>/preview.html (выдуманные данные, звёзды ведут на общую страницу).
Компании с custom_template (TLS) не трогает: их шаблон сделан руками.
"""

import html
import json
import os

BASE = "https://miron-droid.github.io/driver-review-emails"
STAR = (
    '<td width="20%" align="center" style="padding:4px;">'
    '<a href="{{link}}?r={n}" style="display:block;text-decoration:none;'
    "font-family:Arial,Helvetica,sans-serif;font-size:38px;line-height:44px;"
    'color:#f2b01e;" aria-label="{n} star{s}">&#9733;</a></td>'
)
HERO_ALT = "Illustration: a delivery vehicle on the road"

companies = json.load(open("companies.json"))
base = open("_base/template.html").read()
stars = "".join(STAR.format(n=n, s="s" if n > 1 else "") for n in range(1, 6))

for c in companies:
    os.makedirs(c["id"], exist_ok=True)
    if not c.get("custom_template"):
        out = base
        for key, value in {
            "[[BASE]]": BASE,
            "[[HERO]]": c["hero"],
            "[[HERO_ALT]]": HERO_ALT,
            "[[LOGO]]": c["logo_mail"],
            "[[LOGO_W]]": str(c["logo_mail_w"]),
            "[[LOGO_H]]": str(c["logo_mail_h"]),
            "[[NAME]]": html.escape(c["name"]),
            "[[SHORT]]": html.escape(c["short"]),
            "[[ACCENT]]": c["accent"],
            "[[STARS]]": stars,
        }.items():
            out = out.replace(key, value)
        open(f"{c['id']}/template.html", "w").write(out)

    template = open(f"{c['id']}/template.html").read()
    preview = (
        template.replace("{first_name}", c["sample"]["driver"])
        .replace("{link}?r=", f"../page/index.html?c={c['id']}&r=")
        .replace("{link}", f"../page/index.html?c={c['id']}")
        .replace("<head>", '<head>\n<base target="_blank">', 1)
    )
    open(f"{c['id']}/preview.html", "w").write(preview)

print(f"{len(companies)} companies built")
