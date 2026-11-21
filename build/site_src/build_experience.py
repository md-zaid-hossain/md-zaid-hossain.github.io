#!/usr/bin/env python3
"""Experience page (all themes + phone). The page content comes from build_exp_page_prop.py + exp_data.py
(approved by Zaid on 2026-11-20); this file puts it into the page shell."""
import build_exp_page_prop as XP
P = XP.P


def body():
    return f"""
  <main class="wrap" style="position:relative;z-index:1">
    <div class="epg">{XP.page_body()}</div>
  </main>
"""


def experience_page(theme, title):
    b = body()
    html = P.H.page(theme, title)
    import build_exp_role_prop as RP
    html = html.replace("<style>", "<style>" + P.EG.CSS + P.CSS + XP.CSS + RP.CSS + XP.S.CSS + "\n.zrlD.zrl1{max-width:none;margin-top:16px}"
                        + "\n.edw.xqw{timeline-scope:--w1,--w2,--w3,--w4,--x11,--x12,--x21,--x22,--x31,--x41}", 1)
    a = html.index("  <!-- Hero: static page backdrop")
    e = html.index("  </main>") + len("  </main>")
    html = html[:a] + b + html[e:]
    i = html.rindex("</body>")
    html = html[:i] + '<div class="ssv">' + "".join(XP.VIEW) + "</div>" + html[i:]
    return html.replace('<a href="#">Experience</a>', '<a href="#" class="on" aria-current="page">Experience</a>', 1)


if __name__ == "__main__":
    import type_scale as TS
    out = __import__("os").environ.get("PORTFOLIO_OUT", "/home/claude/zaid/project")
    for key, name in [("dark", "Experience"), ("dark_blue", "ExperienceBlue"), ("dark_green", "ExperienceGreen"),
                      ("light", "ExperienceLight"), ("light_blue", "ExperienceLightBlue"), ("light_green", "ExperienceLightGreen"),
                      ("dark", "ExperienceMobile")]:
        open(f"{out}/{name}.dc.html", "w").write(TS.apply(experience_page(key, f"Experience · {name}")))
    print("experience written")
