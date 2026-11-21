#!/usr/bin/env python3
"""404 page (all themes + phone), approved by Zaid on 2026-11-20. Body from site_extras.nf_body():
"Part not found", the requested address, three bracket buttons, and the drawing where B (gear train,
middle gear missing) and C (search leaves the feasible region) take turns."""
import build_home as H
import site_extras as SX


def notfound_page(theme, title):
    html = H.page(theme, title)
    html = html.replace("<style>", "<style>" + SX.NF_CSS, 1)
    a = html.index("  <!-- Hero: static page backdrop")
    e = html.index("  </main>") + len("  </main>")
    return html[:a] + f'\n  <main class="wrap" style="position:relative;z-index:1">{SX.nf_body()}\n  </main>' + html[e:]


if __name__ == "__main__":
    import os
    import type_scale as TS
    out = os.environ.get("PORTFOLIO_OUT", "/home/claude/zaid/project")
    for key, name in [("dark", "NotFound"), ("dark_blue", "NotFoundBlue"), ("dark_green", "NotFoundGreen"),
                      ("light", "NotFoundLight"), ("light_blue", "NotFoundLightBlue"), ("light_green", "NotFoundLightGreen"),
                      ("dark", "NotFoundMobile")]:
        open(f"{out}/{name}.dc.html", "w").write(TS.apply(notfound_page(key, f"404 · {name}")))
    print("404 written")
