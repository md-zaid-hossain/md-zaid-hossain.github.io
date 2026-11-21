#!/usr/bin/env python3
"""Awards page (all themes + phone). Content comes from build_awards_prop.py + awards_data.py
(approved by Zaid on 2026-11-20); this file puts it into the page shell."""
import build_awards_prop as AP
P = AP.P


import slideshow as S
import awards_data as A

GROUPS = ([("aw-cad", "CAD COMPETITIONS", [f"zlb-{k}" for *_, k in A.COMPETITIONS if k])]
          + [(f"aw-{g[1].replace('.', '-')}", g[3].upper().replace('&AMP;', '&amp;'), [f"zlb-c-{c[0]}" for c in g[5]]) for g in A.GROUPS])  # one slideshow per certificate group


def body():
    return f"""
  <main class="wrap" style="position:relative;z-index:1">
    <div class="epg">{AP.page_body()}</div>
  </main>
"""


def awards_page(theme, title):
    html = P.H.page(theme, title)
    html = html.replace("<style>", "<style>" + P.EG.CSS + P.CSS + AP.CSS + AP.SCOPE, 1)
    a = html.index("  <!-- Hero: static page backdrop")
    e = html.index("  </main>") + len("  </main>")
    html = html[:a] + body() + html[e:]
    return html.replace('<a href="#">Awards</a>', '<a href="#" class="on" aria-current="page">Awards</a>', 1)


if __name__ == "__main__":
    import type_scale as TS
    out = __import__("os").environ.get("PORTFOLIO_OUT", "/home/claude/zaid/project")
    for key, name in [("dark", "Awards"), ("dark_blue", "AwardsBlue"), ("dark_green", "AwardsGreen"),
                      ("light", "AwardsLight"), ("light_blue", "AwardsLightBlue"), ("light_green", "AwardsLightGreen"),
                      ("dark", "AwardsMobile")]:
        open(f"{out}/{name}.dc.html", "w").write(TS.apply(S.from_lightboxes(awards_page(key, f"Awards · {name}"), GROUPS)))
    print("awards written")
