#!/usr/bin/env python3
"""Gallery page (all themes + phone). Content comes from build_gallery_prop.py + gallery_data.py
(approved by Zaid on 2026-11-20); this file puts it into the page shell. Slideshow viewers go before </body>."""
import build_gallery_prop as GP
P = GP.P


def body():
    return f"""
  <main class="wrap" style="position:relative;z-index:1">
    <div class="epg">{GP.page_body()}</div>
  </main>
"""


def gallery_page(theme, title):
    b = body()
    html = P.H.page(theme, title)
    html = html.replace("<style>", "<style>" + P.EG.CSS + P.CSS + GP.CSS + GP.S.CSS + GP.SCOPE, 1)
    a = html.index("  <!-- Hero: static page backdrop")
    e = html.index("  </main>") + len("  </main>")
    html = GP.with_viewers(html[:a] + b + html[e:])
    return html.replace('<a href="#">Gallery</a>', '<a href="#" class="on" aria-current="page">Gallery</a>', 1)


if __name__ == "__main__":
    import os
    import type_scale as TS
    out = os.environ.get("PORTFOLIO_OUT", "/home/claude/zaid/project")
    for key, name in [("dark", "Gallery"), ("dark_blue", "GalleryBlue"), ("dark_green", "GalleryGreen"),
                      ("light", "GalleryLight"), ("light_blue", "GalleryLightBlue"), ("light_green", "GalleryLightGreen"),
                      ("dark", "GalleryMobile")]:
        open(f"{out}/{name}.dc.html", "w").write(TS.apply(gallery_page(key, f"Gallery · {name}")))
    print("gallery written")
