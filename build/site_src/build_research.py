#!/usr/bin/env python3
"""Research page (all themes + phone). Content comes from build_research_prop.py + research_data.py
(approved by Zaid on 2026-11-19); this file puts it into the page shell."""
import build_research_prop as RP
P = RP.P


import slideshow as S

GROUPS = [(f"rs-{k}", "FIGURES", [f"lb-{k}-how", f"lb-{k}-res"]) for k in ("wmsd", "array", "qpain", "sop")]  # HOW and RESULT of each paper


def body():
    return f"""
  <main class="wrap" style="position:relative;z-index:1">
    <div class="epg">{RP.page_body()}</div>
  </main>
"""


def research_page(theme, title):
    html = P.H.page(theme, title)
    html = html.replace("<style>", "<style>" + P.EG.CSS + P.CSS + RP.CSS, 1)
    a = html.index("  <!-- Hero: static page backdrop")
    e = html.index("  </main>") + len("  </main>")
    html = html[:a] + body() + html[e:]
    return html.replace('<a href="#">Research</a>', '<a href="#" class="on" aria-current="page">Research</a>', 1)


if __name__ == "__main__":
    import type_scale as TS
    out = __import__("os").environ.get("PORTFOLIO_OUT", "/home/claude/zaid/project")
    for key, name in [("dark", "Research"), ("dark_blue", "ResearchBlue"), ("dark_green", "ResearchGreen"),
                      ("light", "ResearchLight"), ("light_blue", "ResearchLightBlue"), ("light_green", "ResearchLightGreen"),
                      ("dark", "ResearchMobile")]:
        open(f"{out}/{name}.dc.html", "w").write(TS.apply(S.from_lightboxes(research_page(key, f"Research · {name}"), GROUPS)))
    # FDM PLA study page (approved by Zaid 21 Nov 2026): dark, light and phone, like the project pages
    import research_am as A
    for theme, suf, tt in [("dark", "", "dark"), ("light", "Light", "light"), ("dark", "Mobile", "phone dark")]:
        open(f"{out}/StudyFdm{suf}.dc.html", "w").write(TS.apply(A.page(theme, f"FDM PLA study · {tt}")))
    print("research written")
