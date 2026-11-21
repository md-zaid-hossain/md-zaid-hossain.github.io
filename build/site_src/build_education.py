#!/usr/bin/env python3
"""Education page (all themes + phone). The page content comes from build_edu_detail_prop.py
(approved by Zaid on 2026-11-19); this file puts it into the page shell."""
import build_edu_detail_prop as P


import slideshow as S

GROUPS = [  # every group of certificates or figures opens as a slideshow (Zaid, 21 Nov)
    ("ed-deg", "B.SC. CERTIFICATES", ["lb-prov", "lb-eng", "lb-grade"]),
    ("ed-fig", "THESIS FIGURES", ["lb-fig01", "lb-fig02", "lb-fig06", "lb-fig10"]),
    ("ed-cad", "CAD COMPETITIONS", ["lb-technomize", "lb-cadrush", "lb-mechcellence", "lb-kitcad", "lb-ignition"]),
    ("ed-rec", "RECOGNITION", ["lb-fablabc", "lb-dsw", "lb-hall"]),
    ("ed-sch", "SCHOOL CERTIFICATES", ["lb-hsc", "lb-ssc"]),
]


def body():
    inner = P.page_body()
    return f"""
  <main class="wrap" style="position:relative;z-index:1">
    <div class="epg">{inner}</div>
  </main>
"""


def education_page(theme, title):
    html = P.H.page(theme, title)
    html = html.replace("<style>", "<style>" + P.EG.CSS + P.CSS + P.area_css() + P.R.CSS + P.R.LEG_CSS + P.COLLAPSE_CSS, 1)
    a = html.index("  <!-- Hero: static page backdrop")
    e = html.index("  </main>") + len("  </main>")
    return P.R.inject(html[:a] + body() + html[e:], P.R.viewers())   # routine and teacher panels of the course map


if __name__ == "__main__":
    import type_scale as TS
    out = __import__("os").environ.get("PORTFOLIO_OUT", "/home/claude/zaid/project")
    for key, name in [("dark", "Education"), ("dark_blue", "EducationBlue"), ("dark_green", "EducationGreen"),
                      ("light", "EducationLight"), ("light_blue", "EducationLightBlue"), ("light_green", "EducationLightGreen"),
                      ("dark", "EducationMobile")]:
        open(f"{out}/{name}.dc.html", "w").write(TS.apply(S.from_lightboxes(education_page(key, f"Education · {name}"), GROUPS)))
    print("education written")
