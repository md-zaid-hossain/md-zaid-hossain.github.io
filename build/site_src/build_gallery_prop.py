#!/usr/bin/env python3
"""Proposal: Gallery page. Same frame as Education, Research, Experience and Awards (stats strip, sticky index).
Four chapters (MAKING, COMPETITIONS, CAMPUS, PROFESSIONAL); each album is a short story:
a title block (album code, title, place, date), two or three lines of story, then the photos as numbered frames
with a one-line caption. Click a frame to enlarge it with its caption (CSS checkbox lightbox, no JS).
Rows are always full: the grid columns follow the photo count, and on phone an odd count lets the first photo span the row.
Writes GalleryProp* boards. Class prefix: zg."""
import build_edu_detail_prop as P
import gallery_data as G
import slideshow as S

CSS = """
/* ===== gallery page (prefix zg) ===== */
.zga{border:1px solid var(--line2);border-radius:12px;background:var(--surface);padding:18px 20px 20px;margin-top:16px;transition:border-color .35s ease,box-shadow .35s ease}
.zga:hover{border-color:var(--muted);box-shadow:0 14px 30px rgba(0,0,0,.14)}
.zgh{display:grid;grid-template-columns:auto minmax(0,1fr) auto;align-items:stretch;border:1px solid var(--line2);border-radius:8px;overflow:hidden;background:var(--surface2)}
.zgh>*{padding:9px 14px;min-width:0}
.zgc{display:flex;align-items:center;gap:8px;border-right:1px solid var(--line2);font:600 11px 'IBM Plex Mono',monospace;letter-spacing:.1em;color:var(--acc-t);white-space:nowrap}
.zgc svg{width:15px;height:15px;flex:none;animation:zgspin 30s linear infinite}
.zga:hover .zgc svg{animation-duration:9s}
@keyframes zgspin{to{transform:rotate(360deg)}}
.zgh h3{margin:0;font:600 17px/1.3 'Space Grotesk',sans-serif;color:var(--strong)}
.zgh .zgp{margin-top:1px;font-size:13px;color:var(--muted)}
.zgd{display:flex;flex-direction:column;justify-content:center;align-items:flex-end;border-left:1px solid var(--line2);font:600 11px 'IBM Plex Mono',monospace;letter-spacing:.08em;color:var(--body);white-space:nowrap}
.zgd small{font-size:9.5px;letter-spacing:.12em;color:var(--muted);margin-top:2px}
.zgl{color:var(--strong);border-bottom:1px dotted var(--line2);white-space:nowrap;transition:color .25s ease}.zgl:hover{color:var(--acc-t)}
.zgrl{margin-top:18px;font:600 10px 'IBM Plex Mono',monospace;letter-spacing:.12em;color:var(--muted)}
.zgq{gap:10px 10px}.zgq .zgf span{font-size:0}.zgq .zgf span b{font-size:9.5px;margin:0}
.zgcr{margin-top:6px;font:600 10px 'IBM Plex Mono',monospace;letter-spacing:.1em;color:var(--muted)}
.zgs{margin:14px 0 0;font-size:15px;line-height:1.6;color:var(--body);max-width:900px}
.zgg.zgn1{max-width:560px}
.zgg{display:grid;grid-template-columns:repeat(var(--zgc),minmax(0,1fr));gap:16px 12px;margin-top:16px}
.zgn14{--zgc:7}.zgn1{--zgc:1}.zgn2{--zgc:2}.zgn20{--zgc:5}.zgn15{--zgc:5}.zgn3{--zgc:3}.zgn4{--zgc:4}.zgn5{--zgc:5}.zgn8{--zgc:4}.zgn10{--zgc:5}.zgn12{--zgc:4}
.zgf{display:flex;flex-direction:column;gap:7px;min-width:0;cursor:zoom-in}
.zgf i{position:relative;display:block;border-radius:6px;overflow:hidden;border:1px solid var(--line)}
.zgf img{display:block;width:100%;aspect-ratio:4/3;object-fit:cover;filter:saturate(.92);transition:transform .5s ease,filter .5s ease}
.zgf:hover img{transform:scale(1.035);filter:none}
.zgf span{font-size:13px;line-height:1.4;color:var(--muted)}
.zgf span b{display:block;font:600 9.5px 'IBM Plex Mono',monospace;letter-spacing:.12em;color:var(--body);margin-bottom:1px;transition:color .25s ease}
.zgf:hover span b{color:var(--acc-t)}
.zgx{display:flex;align-items:center;justify-content:space-between;gap:12px;margin-top:16px;padding:12px 16px;border:1px dashed var(--line2);border-radius:10px;font-size:14px;color:var(--body)}
.zgx a{font:600 11px 'IBM Plex Mono',monospace;letter-spacing:.08em;color:var(--muted);border-bottom:1px dotted var(--line2);white-space:nowrap}
.zgx a:hover{color:var(--acc-t)}
@media (prefers-reduced-motion:reduce){.zgc svg{animation:none}.zgf img{transition:none}.zgf:hover img{transform:none}}
@media (max-width:1300px){.zgn12{--zgc:3}.zgn14{--zgc:7}.zgn20{--zgc:4}.zgn15{--zgc:3}.zgn4{--zgc:2}.zgn5{--zgc:3}.zgn5 .zgf:first-child{grid-column:span 2}}
@media (max-width:760px){
  .zga{padding:14px 12px 16px}
  .zgh{grid-template-columns:minmax(0,1fr) auto}
  .zgc{grid-column:1/-1;border-right:0;border-bottom:1px solid var(--line2);padding:7px 12px}
  .zgh>div{padding:8px 12px}
  .zgh h3{font-size:15.5px}
  .zgs{font-size:14px}
  .zgg{--zgc:2!important;gap:12px 8px}
  .zgg.zgn1{--zgc:1!important}
  .zgn3 .zgf:first-child,.zgn5 .zgf:first-child,.zgn15 .zgf:first-child{grid-column:1/-1}
  .zgf span{font-size:12px}
  .zgx{flex-direction:column;align-items:flex-start}
}
"""

COG = ('<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="none" stroke="currentColor" stroke-width="1.6" '
       'd="M12 8.5a3.5 3.5 0 1 0 0 7 3.5 3.5 0 0 0 0-7zM10.6 2.5h2.8l.5 2.4 1.9.8 2-1.4 2 2-1.4 2 .8 1.9 2.3.4v2.8l-2.3.5-.8 1.9 1.4 2-2 2-2-1.4-1.9.8-.5 2.4h-2.8l-.4-2.4-1.9-.8-2 1.4-2-2 1.4-2-.8-1.9-2.4-.5v-2.8l2.4-.4.8-1.9-1.4-2 2-2 2 1.4 1.9-.8z"/></svg>')

LB = []

SHORT = {"a1": "Printer revival", "a2": "CAD to print", "a3": "Certificate day", "a4": "Lab set-up", "a5": "CNC on the VF-2",
         "b1": "Technomize 1.0", "b2": "CAD Rush 1.0", "b3": "MECHCELLENCE 1.0", "b4": "IGNITION 2023", "b5": "KitCAD 2024",
         "b6": "MindSparks 24", "c1": "DSW award", "c2": "Farewell 2K19", "c3": "Term project", "c4": "Thesis defence day",
         "d1": "CAD and CAM seminar", "d2": "BRACU FabLab session"}


def img(stem):
    if stem.startswith(("/_blob/", "/media/")):
        return stem
    if __import__("os").environ.get("GAL_LOCAL"):
        return f"file:///home/claude/zaid/source/photos/gallery/{stem}.webp"
    return G.GAL_IMG.get(stem, f"photos/gallery/{stem}.webp")


def album(a):
    n = len(a["photos"])
    feat = a.get("featured", 0)
    rest_cap = a.get("rest_caption", "")
    items = [(img(s), c or rest_cap) for s, c, _ in a["photos"]]
    rid, viewer = S.group(a["key"], items, a["code"])
    LB.append(viewer)
    ratio = a.get("ratio", "4/3")

    def frame(i, s, c, pos, cap=True):
        alt = c or rest_cap
        txt = f"<span><b>{i+1:02d}</b>{c}</span>" if cap else f"<span><b>{i+1:02d}</b></span>"
        return (f'<label class="zgf" for="{rid(i)}" title="Click to open the slideshow"><i><img src="{img(s)}" alt="{alt}" '
                f'style="object-position:{pos};aspect-ratio:{ratio}"></i>{txt}</label>')
    ph = a["photos"]
    if feat:
        top = "".join(frame(i, *ph[i]) for i in range(feat))
        rest = "".join(frame(i, *ph[i], cap=False) for i in range(feat, n))
        grids = (f'<div class="zgg zgn{feat}">{top}</div>'
                 f'<div class="zgrl">{a.get("rest_label", "MORE")} · {n - feat}</div><div class="zgg zgn{n - feat} zgq">{rest}</div>')
    else:
        grids = f'<div class="zgg zgn{n}">' + "".join(frame(i, *ph[i]) for i in range(n)) + "</div>"
    credit = f'<div class="zgcr">{a["credit"]}</div>' if a.get("credit") else ""
    return (f'<article class="zga zgn{n}"><div class="zgh"><span class="zgc">{COG}{a["code"]}</span>'
            f'<div><h3>{a["title"]}</h3><div class="zgp">{a["place"]}</div></div>'
            f'<div class="zgd">{a["date"]}<small>{n} PHOTO{"S" if n > 1 else ""}</small></div></div>'
            f'<p class="zgs">{a["story"]}</p>{credit}{grids}</article>')


def page_body():
    LB.clear()
    albums = [a for c in G.CHAPTERS for a in c[3]]
    n_photo = sum(len(a["photos"]) for a in albums)
    nav, secs, scope = [], [], []
    for ci, (hid, eb, h2, items) in enumerate(G.CHAPTERS, 1):
        tl = f"--g{ci}"
        scope.append(tl)
        body = P.head(f"{ci:02d}", eb, h2, f"g-{hid}")
        sb = []
        for ai, a in enumerate(items, 1):
            st = f"--h{ci}{ai}"
            scope.append(st)
            body += P.sub(st, f"{ci}.{ai}", SHORT[a["key"]].upper(), album(a))
            sb.append((st, f"{ci}.{ai}", SHORT[a["key"]]))
        nav.append((tl, f"g-{hid}", f"{ci:02d}", eb, sb))
        secs.append(f'<section class="esc" style="view-timeline-name:{tl}">{P.GO("g-" + hid)}{body}</section>')
    idx = '<nav class="eix" aria-label="On this page"><span class="ixh">ON THIS PAGE</span>'
    for k, (tl, hid, n, lab, sb) in enumerate(nav):
        on = " ion" if k == 0 else ""
        sl = "".join(f'<label for="go-{t[2:]}" style="animation-timeline:{t}" class="ixl{" ion" if (k == 0 and j == 0) else ""}"><b>{sn}</b>{s_}</label>'
                     for j, (t, sn, s_) in enumerate(sb))
        idx += (f'<div class="ixg{on}"><label for="go-{hid}" class="ixl{on}" style="animation-timeline:{tl}"><i>{n}</i>{lab}</label>'
                f'<div class="ixs" style="animation-timeline:{tl}"><div>{sl}</div></div></div>')
    idx += "</nav>"
    global SCOPE
    SCOPE = "\n.edw.zgw{timeline-scope:" + ",".join(scope) + "}"
    return f"""
    <div class="epz">
      <div class="eph"><div class="crumb">HOME / GALLERY</div><h1 class="h1">Gallery</h1>
        <p>Photos from the lab bench, contest days, campus and work, each album with the short story behind it.</p></div>
      <div class="est"><div><b>{len(albums)}</b><span>albums</span></div><div><b>{n_photo}</b><span>photos</span></div>
        <div><b>{len(G.CHAPTERS)}</b><span>chapters</span></div><div><b>2023 to 2026</b><span>years covered</span></div></div>
      <div class="edw zgw">{idx}<div>{"".join(secs)}</div></div>
    </div>"""


SCOPE = ""


def body():
    pb = page_body()
    return f"""
  <main class="wrap" style="position:relative;z-index:1">
    <section class="ph">
      <div class="crumb">PROPOSAL / GALLERY PAGE · FOR REVIEW, NOT APPLIED</div>
      <h1 class="h1">Gallery page · in full</h1>
      <p class="lead">Same frame as Education, Research, Experience and Awards. Everything inside the box is the page itself.</p>
    </section>
    <div class="dnote">
      <div><b>SLIDESHOW IN EVERY ALBUM</b>Click any photo: it opens large with its caption and a 03 / 10 counter. Go through the album with the ← → arrows on screen, the keyboard arrow keys, or by clicking the photo; × or a click outside closes it.</div>
      <div><b>ROWS ALWAYS FULL</b>The grid follows the photo count (3, 4, 5, 8, 10 or 15), so no row has a gap. On phone two per row; with an odd count the first photo spans the row.</div>
      <div><b>EVERY PHOTO EDITED</b>Each photo was corrected on its own: contrast stretched, dark shots and night stages lifted, light clarity and colour, then sharpened. Roll number on the DSW crest glass-blurred.</div>
    </div>
    <div class="dopt">{pb}</div>
  </main>
"""


def with_viewers(html):
    """Slideshow viewers go right before </body>, outside <main>, so they sit above the sticky header."""
    i = html.rindex("</body>")
    return html[:i] + '<div class="ssv">' + "".join(LB) + "</div>" + html[i:]


def page(theme, title):
    b = body()
    html = P.H.page(theme, title)
    html = html.replace("<style>", "<style>" + P.EG.CSS + P.CSS + CSS + S.CSS + SCOPE, 1)
    a = html.index("  <!-- Hero: static page backdrop")
    e = html.index("  </main>") + len("  </main>")
    html = html[:a] + b + html[e:]
    html = with_viewers(html)
    return html.replace('<a href="#">Gallery</a>', '<a href="#" class="on" aria-current="page">Gallery</a>', 1)


if __name__ == "__main__":
    import os
    import type_scale as TS
    out = os.environ.get("PORTFOLIO_OUT", "/home/claude/zaid/project")
    for key, name in [("dark", "GalleryProp"), ("dark_blue", "GalleryPropBlue"), ("dark_green", "GalleryPropGreen"),
                      ("light", "GalleryPropLight"), ("light_blue", "GalleryPropLightBlue"), ("light_green", "GalleryPropLightGreen"),
                      ("dark", "GalleryPropMobile")]:
        open(f"{out}/{name}.dc.html", "w").write(TS.apply(page(key, f"Gallery page proposal · {name}")))
    print("gallery proposal written")
