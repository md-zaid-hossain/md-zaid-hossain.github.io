"""Site-wide pieces, approved by Zaid on 2026-11-20: phone menu (every page), favicon and share-image tags
(every page head), and the 404 page body. Class prefixes: mn (phone menu), nf (404 page).
Favicon: Zaid's own ZAID favicon since 21 Nov (logo_mark.FAVICON_SVG); before that option A (filled ZH).
404 drawing: B (gear train, middle gear missing) and C (search leaves the feasible region) take turns, 8 s each (Zaid, 21 Nov: was 12 s)."""
import build_home as H
import site_parts as SP

BK = lambda t, a: f'<a class="bkb" href="#"><s></s><s></s><s></s><s></s><span>{t}</span><i>{a}</i></a>'

SHARE = "/_blob/1965184231d6e891b19ccfa9b6d23376"   # photos/share_image.jpg (media_scripts/share_image.py)
NAV = ["Education", "Experience", "Research", "Projects", "Awards", "Gallery", "Contact"]   # Zaid 21 Nov: same order as the Home sections
PROF = [("https://github.com/md-zaid-hossain", "GitHub"), ("https://www.linkedin.com/in/md-zaid-hossain", "LinkedIn"),
        ("https://www.researchgate.net/profile/Md-Zaid-Hossain", "ResearchGate"), ("https://scholar.google.com/citations?user=Fu6JmxIAAAAJ", "Scholar"),
        ("https://orcid.org/0009-0003-3301-3609", "ORCID"), ("https://grabcad.com/md.zaid.hossain-1", "GrabCAD")]
CLOSE = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M6 6l12 12M18 6 6 18" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>'

# ---------------- phone menu (reusable) ----------------
MENU_CSS = """
/* ===== phone menu (prefix mn) ===== */
.mnx{position:fixed;top:0;left:0;width:1px;height:1px;opacity:0;pointer-events:none;margin:0}
.menu .mc{display:none}.menu span{display:flex}
.mnu{display:none;position:absolute;left:0;right:0;top:100%;height:calc(100vh - 64px);overflow:auto;flex-direction:column;gap:22px;
  padding:14px 16px 28px;background:var(--bg);border-top:1px solid var(--line)}
.mnl{display:flex;flex-direction:column}
.mnl a{display:flex;align-items:center;gap:14px;padding:13px 4px 13px 12px;border-bottom:1px solid var(--line);font:500 13.5px/1.1 'Space Grotesk',sans-serif;color:var(--strong);position:relative}
.mnl a i{font:600 11px 'IBM Plex Mono',monospace;font-style:normal;letter-spacing:.08em;color:var(--muted);width:22px}
.mnl a b{margin-left:auto;font:500 14px 'IBM Plex Mono',monospace;color:var(--muted)}
.mnl a.on:before{content:"";position:absolute;left:0;top:12px;bottom:12px;width:3px;border-radius:2px;background:var(--acc)}
.mnl a.on i,.mnl a.on b{color:var(--acc-t)}
.mnr{display:flex;align-items:center;justify-content:space-between;gap:12px;padding:4px 4px 0 12px}
.mnk{font:600 9.5px 'IBM Plex Mono',monospace;letter-spacing:.1em;color:var(--muted)}
.mnu .sw{display:block!important}
.mnu .mncv{width:100%;justify-content:center;height:42px;font-size:11px!important}   /* Zaid 22 Nov: menu text a step below the name */
.mnp{display:flex;flex-wrap:nowrap;align-items:center;justify-content:center;gap:0;padding:0;font-family:'Inter',system-ui,sans-serif;font-weight:600;font-size:clamp(8px,2.45vw,11.5px);letter-spacing:0;white-space:nowrap}
.mnp a{color:var(--body);display:inline-flex;align-items:center}
.mnp a+a:before{content:"";flex:none;width:3px;height:3px;border-radius:50%;background:var(--muted);opacity:.6;margin:0 clamp(3px,.9vw,8px)}   /* Zaid 21 Nov: one line with dots, like the footer */
@media (max-width:359px){.mnp a+a:before{margin:0 2.5px}}   /* Zaid 21 Nov: always one line, centred */
.mnx:checked~.hdr .mnu{display:flex}
.mnx:checked~.hdr .menu .mo{display:none}.mnx:checked~.hdr .menu .mc{display:flex}
@media (min-width:1180px){.hdr>.mnu{display:none!important}}
@media (min-width:761px){.mnu .mnr{display:none}}   /* the header shows the accent buttons from 761 px, so not twice */
@media (max-width:760px){.hdr .tog{zoom:.8}.hdr .menu{width:36px;height:36px}}
"""


CVBTN = SP.BTN_CV.replace('class="bkb"', 'class="bkb mncv"')


def menu_sheet(current=None, theme="dark"):
    links = "".join(f'<a href="#"{" class=on aria-current=page" if n == current else ""}><i>{i:02d}</i>{n}<b>→</b></a>' for i, n in enumerate(NAV, 1))
    prof = "".join(f'<a href="{u}">{t.upper()}</a>' for u, t in PROF)
    return (f'<div class="mnu" id="mnu"><nav class="mnl" aria-label="Main">{links}</nav>'
            f'<div class="mnr"><span class="mnk">ACCENT COLOUR</span>{H.swatches(theme)}</div>'
            f'{CVBTN}<div class="mnp">{prof}</div></div>')


def add_menu(html, current=None, theme="dark"):
    """Turn the header's menu button into a working phone menu (mockup: CSS checkbox; live site: a few lines of JS)."""
    old = f'<button class="menu" aria-label="Open menu" style="color:var(--strong)">{H.MENU}</button>'
    new = f'<label class="menu" for="mnx" aria-label="Open menu" style="color:var(--strong)"><span class="mo">{H.MENU}</span><span class="mc">{CLOSE}</span></label>'
    assert old in html
    html = html.replace(old, new, 1)
    html = html.replace('  <header class="hdr">', '  <input type="checkbox" id="mnx" class="mnx" tabindex="-1" aria-hidden="true">\n  <header class="hdr">', 1)
    a = html.index('  <header class="hdr">')
    b = html.index("  </header>", a)
    return html[:b] + "    " + menu_sheet(current, theme) + "\n" + html[b:]


# ---------------- favicon options ----------------
GEAR = H.PINION_SW.split('d="')[1].split('"')[0]


def fav(kind, size, tab_dark=None):
    if kind == "a":
        body = ('<rect width="64" height="64" rx="12" fill="#C14B3C"/>'
                '<text x="32" y="42.5" text-anchor="middle" font-family="IBM Plex Mono,monospace" font-weight="700" font-size="27" fill="#fff">ZH</text>')
    elif kind == "b":
        c = "var(--strong)" if tab_dark is None else ("#F4F5F7" if tab_dark else "#16233A")
        body = (f'<rect x="3" y="3" width="58" height="58" rx="9" style="fill:none;stroke:{c};stroke-width:4"/>'
                f'<text x="32" y="42.5" text-anchor="middle" font-family="IBM Plex Mono,monospace" font-weight="700" font-size="25" style="fill:{c}">ZH</text>')
    else:
        body = (f'<g transform="scale(2.6667)"><path d="{GEAR}" fill="#C14B3C"/></g><circle cx="32" cy="32" r="15" fill="#fff"/>'
                '<text x="32" y="40" text-anchor="middle" font-family="IBM Plex Mono,monospace" font-weight="700" font-size="22" fill="#C14B3C">Z</text>')
    return f'<svg width="{size}" height="{size}" viewBox="0 0 64 64" aria-hidden="true">{body}</svg>'


# ---------------- 404 page ----------------
NF_CSS = """
/* ===== 404 page (prefix nf) ===== */
.nf{display:grid;grid-template-columns:minmax(0,1fr) 380px;gap:48px;align-items:center;padding:56px 0 40px}
.nf .crumb{color:var(--acc-t)}
.nf h1{margin-top:12px;font-size:56px}
.nf .lead{margin-top:14px;max-width:560px;font-size:18px}
.nf .spec{margin-top:24px;max-width:520px;grid-template-columns:120px 1fr}
.nf .spec code{font:500 13.5px 'IBM Plex Mono',monospace;color:var(--strong)}
.nf .acts{display:flex;flex-wrap:wrap;gap:12px;margin-top:28px}
.nfd{position:relative;aspect-ratio:1;border:1px solid var(--line2);border-radius:12px;background:var(--surface2);
  background-image:linear-gradient(var(--line) 1px,transparent 1px),linear-gradient(90deg,var(--line) 1px,transparent 1px);background-size:26px 26px}
.nfd svg{position:absolute;inset:0;width:100%;height:100%}
.nfd .gg{fill:none;stroke:var(--muted);stroke-width:1.5;stroke-dasharray:6 5;vector-effect:non-scaling-stroke}
.nfd .cl{stroke:var(--muted);stroke-width:1;stroke-dasharray:14 4 2 4;vector-effect:non-scaling-stroke;opacity:.7}
.nfd .bl{fill:var(--bg);stroke:var(--acc);stroke-width:1.6;vector-effect:non-scaling-stroke}
.nfd .ld{stroke:var(--acc);stroke-width:1.4;vector-effect:non-scaling-stroke}
.nfd text{font:600 12px 'IBM Plex Mono',monospace;letter-spacing:.08em;fill:var(--muted)}
.nfd .bt{font:600 15px 'IBM Plex Mono',monospace;fill:var(--acc-t);letter-spacing:0}
.nfd .gs{fill:var(--surface);stroke:var(--strong);stroke-width:1.5;vector-effect:non-scaling-stroke}
.nfd .ct{fill:none;stroke:var(--line2);stroke-width:1;vector-effect:non-scaling-stroke}
.nfd .fz{fill:var(--acc-soft);stroke:var(--acc);stroke-width:1.4;stroke-dasharray:7 5;vector-effect:non-scaling-stroke}
.nfd .sp{fill:none;stroke:var(--strong);stroke-width:2;stroke-dasharray:3 5;stroke-linecap:round}
.nfd .sd{fill:var(--strong)}
.nfd .sx{stroke:var(--acc-t);stroke-width:3;stroke-linecap:round}
.nfd .tb{fill:var(--surface);stroke:var(--line2);stroke-width:1.2}
.nfd .tl{stroke:var(--line2);stroke-width:1}
.nfd .hr{fill:var(--acc-soft)}
.nfd .tv{font:500 12.5px 'IBM Plex Mono',monospace;letter-spacing:0;fill:var(--strong)}
.nfd .hx{font:600 12.5px 'IBM Plex Mono',monospace;letter-spacing:0;fill:var(--acc-t)}
.nfd .sk{stroke:var(--acc-t);stroke-width:1.6}
.nfr svg{opacity:0;animation:nfx 16s linear infinite}.nfr svg+svg{animation-delay:-8s}
@keyframes nfx{0%{opacity:0}3%,47%{opacity:1}50%,100%{opacity:0}}
/* panel: crosshair cursor, accent frame; hover pauses the B and C rotation so the hover state can be seen */
.nfd{transition:border-color .3s ease,box-shadow .3s ease;cursor:crosshair}
.nfd:hover{border-color:var(--acc);box-shadow:0 0 0 4px var(--acc-soft)}
.nfr:hover svg,.nfr:hover svg *{animation-play-state:paused}
.nfd .t1{opacity:0}.nfd .t0,.nfd .t1{transition:opacity .4s ease}
.nfd:hover .t0{opacity:0}.nfd:hover .t1{opacity:1;fill:var(--acc-t)}
.nfd g.blg,.nfd g.sxg,.nfd .gm{transform-box:fill-box;transform-origin:center}
/* C: each run, the search path draws itself, the point travels it, the region flashes as it is crossed,
   then the X and the 404 balloon pop in. Same 16 s clock as the panel (C is on screen 0 to 8 s of its own clock). */
.nfr svg.kc *{animation-delay:-8s}
.nfd .rv{fill:none;stroke:#fff;stroke-width:8;stroke-dasharray:256;stroke-dashoffset:0;animation:nfrv 16s linear infinite}
@keyframes nfrv{0%,6%{stroke-dashoffset:256}32%,100%{stroke-dashoffset:0}}
.nfd .sm{fill:var(--acc);offset-path:path("M110 250 L140 228 L168 214 L205 196 L245 178 L290 150 L328 120");offset-rotate:0deg;offset-distance:100%;opacity:0;animation:nfmv 16s linear infinite}
@keyframes nfmv{0%,6%{offset-distance:0%;opacity:1}32%{offset-distance:100%;opacity:1}36%,100%{offset-distance:100%;opacity:0}}
.nfd .sxg{animation:nfpop 16s linear infinite}
.nfd .kc .blg{animation:nfpop2 16s linear -8s infinite}
@keyframes nfpop{0%,31%{transform:scale(0);opacity:0}34%{transform:scale(1.3);opacity:1}37%,100%{transform:scale(1);opacity:1}}
@keyframes nfpop2{0%,35%{transform:scale(0);opacity:0}38%{transform:scale(1.2);opacity:1}41%,100%{transform:scale(1);opacity:1}}
.nfd .fz{animation:nfmarch 2.4s linear infinite,nfflash 16s linear infinite}
.nfr svg.kc .fz{animation-delay:0s,-8s}
@keyframes nfmarch{to{stroke-dashoffset:-24}}
@keyframes nfflash{0%,25%{stroke-width:1.4px;fill-opacity:1}27.5%{stroke-width:3.5px;fill-opacity:2}31%,100%{stroke-width:1.4px;fill-opacity:1}}
.nfd .ct{animation:nfring 6s ease-in-out infinite}
.nfd .ct:nth-of-type(2){animation-delay:-1s}.nfd .ct:nth-of-type(3){animation-delay:-2s}.nfd .ct:nth-of-type(4){animation-delay:-3s}.nfd .ct:nth-of-type(5){animation-delay:-4s}
@keyframes nfring{0%,100%{opacity:.55}50%{opacity:1}}
/* C on hover: the way back. A solid path curves from the X to the optimum, which pulses and reads HOME */
.nfd .hb{fill:none;stroke:var(--acc);stroke-width:2.2;stroke-linecap:round;stroke-dasharray:260;stroke-dashoffset:260;transition:stroke-dashoffset 1.1s ease}
.nfd .ho{opacity:0;transition:opacity .4s ease .9s}
.nfd .hm{fill:var(--acc)}
.nfd .hp{fill:none;stroke:var(--acc);stroke-width:1.5;transform-box:fill-box;transform-origin:center;animation:nfpulse 1.6s ease-out infinite}
@keyframes nfpulse{from{transform:scale(1);opacity:.9}to{transform:scale(3.2);opacity:0}}
.nfd .hl{fill:var(--acc-t)}
.nfd:hover .hb{stroke-dashoffset:0}.nfd:hover .ho{opacity:1}
/* B on hover: the missing gear drops into place, filled, and the balloon swings */
.nfd .gm .gg{transition:fill .5s ease,stroke .5s ease,stroke-dasharray .5s ease}
.nfd .gm{transition:transform .5s cubic-bezier(.3,1.4,.5,1)}
.nfd:hover .gm{transform:scale(1.04)}
.nfd:hover .gm .gg{fill:var(--acc-soft);stroke:var(--acc);stroke-dasharray:none}
.nfd .kb .blg{transition:transform .5s cubic-bezier(.3,1.4,.5,1)}
.nfd:hover .kb .blg{transform:rotate(-8deg) scale(1.08)}
@media (prefers-reduced-motion:reduce){.nfr svg{animation:none;opacity:1}.nfr svg+svg{display:none}
  .nfd .rv,.nfd .sm,.nfd .sxg,.nfd .blg,.nfd .fz,.nfd .ct,.nfd .hp{animation:none}}
@media (max-width:960px){.nf{grid-template-columns:1fr;gap:28px}.nfd{max-width:360px;width:100%;margin:0 auto}}
@media (max-width:760px){.nf .acts{display:grid;grid-template-columns:1fr 1fr}.nf .acts .bkb{justify-content:center}.nf .acts .bkb:first-child{grid-column:span 2}.nf{padding:32px 0 24px}.nf h1{font-size:34px}.nf .lead{font-size:16px}.nf .spec{grid-template-columns:96px 1fr}}
"""


def g(cx, cy, k, cls, rot=""):
    """Pinion outline (24-unit path) centred at cx, cy, scaled by k."""
    spin = f'<animateTransform attributeName="transform" type="rotate" from="0 12 12" to="{rot}" dur="40s" repeatCount="indefinite"/>' if rot else ""
    return (f'<g transform="translate({cx - 12 * k} {cy - 12 * k}) scale({k})"><g><path class="{cls}" d="{GEAR}"/>'
            f'<circle class="{cls}" cx="12" cy="12" r="3.2"/>{spin}</g></g>')


def balloon(x, y, lx, ly):
    return (f'<line class="ld" x1="{lx}" y1="{ly}" x2="{x}" y2="{y}"/><circle class="bl" cx="{x}" cy="{y}" r="20"/>'
            f'<text class="bt" x="{x}" y="{y + 5}" text-anchor="middle">404</text>')


def draw(kind):
    if kind == "a":      # one missing gear
        body = (f'<line class="cl" x1="190" y1="40" x2="190" y2="340"/><line class="cl" x1="40" y1="190" x2="340" y2="190"/>'
                + g(190, 190, 10, "gg") + balloon(320, 60, 262, 118) + '<text x="22" y="358">MZH-P-404 · NOT IN THIS ASSEMBLY</text>')
        lab = "Drawing of a missing gear, marked as part 404"
    elif kind == "b":    # gear train, the middle gear missing
        body = (f'<line class="cl" x1="20" y1="190" x2="360" y2="190"/>'
                + "".join(f'<line class="cl" x1="{x}" y1="110" x2="{x}" y2="270"/>' for x in (80, 190, 300))
                + g(80, 190, 5.2, "gs", "360 12 12") + f'<g class="gm">{g(190, 190, 5.2, "gg")}</g>' + g(300, 190, 5.2, "gs", "-360 12 12")
                + f'<g class="blg">{balloon(268, 82, 214, 140)}</g>'
                + '<text class="t0" x="22" y="358">GEAR TRAIN · MIDDLE GEAR MISSING</text>'
                + '<text class="t1" x="22" y="358">THE GEAR FITS, BUT THE PAGE IS GONE</text>')
        lab = "Gear train with the middle gear missing, marked 404"
    elif kind == "c":    # search leaves the feasible region
        rings = "".join(f'<ellipse class="ct" cx="150" cy="200" rx="{r * 1.35:.0f}" ry="{r}"/>' for r in (24, 48, 72, 96, 120))
        pts = "110,250 140,228 168,214 205,196 245,178 290,150 328,120"
        body = ('<defs><mask id="nfmk" maskUnits="userSpaceOnUse" x="0" y="0" width="380" height="380">'
                f'<polyline class="rv" points="{pts}"/></mask></defs>'
                + rings + '<path class="fz" d="M60 110 L250 80 L300 230 L170 320 L50 260 Z"/>'
                f'<polyline class="sp" points="{pts}" mask="url(#nfmk)"/>'
                '<circle class="sd" cx="110" cy="250" r="5"/><circle class="sm" r="6"/>'
                '<g class="sxg"><path class="sx" d="M321 113l14 14M335 113l-14 14"/></g>'
                + f'<g class="blg">{balloon(330, 58, 328, 104)}</g>'
                '<path class="hb" d="M328 120 C 306 196, 236 236, 152 202"/>'
                '<g class="ho"><circle class="hp" cx="150" cy="200" r="7"/><circle class="hm" cx="150" cy="200" r="5"/>'
                '<text class="hl" x="138" y="184" text-anchor="end">OPTIMUM · HOME</text></g>'
                '<text class="t0" x="22" y="358">SEARCH LEFT THE FEASIBLE REGION</text>'
                '<text class="t1" x="22" y="358">THE WAY BACK: HOME</text>')
        lab = "Contour plot where the search path leaves the feasible region, marked 404"
    else:                # parts list with the row not found
        rows = [("1", "MZH-P-001", "Home page", "1"), ("2", "MZH-P-002", "Projects", "1"), ("3", "MZH-P-404", "Requested page", "0")]
        t = ('<rect class="tb" x="30" y="96" width="320" height="168" rx="6"/><line class="tl" x1="30" y1="134" x2="350" y2="134"/>'
             + "".join(f'<line class="tl" x1="{x}" y1="96" x2="{x}" y2="264"/>' for x in (74, 186, 310))
             + "".join(f'<text x="{x}" y="120">{h}</text>' for x, h in ((40, "ITEM"), (84, "PART NO."), (196, "DESCRIPTION"), (318, "QTY"))))
        for i, (n, pn, d, q) in enumerate(rows):
            y = 134 + i * 43
            hit = n == "3"
            if hit:
                t += f'<rect class="hr" x="31" y="{y + 1}" width="318" height="{263 - y - 1}"/>'
            c = ' class="hx"' if hit else ' class="tv"'
            t += "".join(f'<text{c} x="{x}" y="{y + 27}">{v}</text>' for x, v in ((46, n), (84, pn), (196, d), (322, q)))
            t += f'<line class="tl" x1="30" y1="{y + 43}" x2="350" y2="{y + 43}"/>' if not hit else ""
        body = t + '<line class="sk" x1="190" y1="243" x2="296" y2="243"/>' + balloon(330, 300, 300, 262) + '<text x="22" y="358">PARTS LIST · ITEM 3 NOT FOUND</text>'
        lab = "Parts list where item MZH-P-404 is not found"
    return f'<svg class="k{kind}" viewBox="0 0 380 380" role="img" aria-label="{lab}">{body}</svg>'


NF_KINDS = [("b", "B · GEAR TRAIN", "Recommended", "Two gears keep turning slowly, the middle one is a dashed outline. Reads as \u201ca piece of the site is missing\u201d at a glance."),
            ("a", "A · ONE GEAR", "", "The first draft: a single dashed gear with a balloon. Clear, but a bit empty."),
            ("c", "C · FEASIBLE REGION", "", "Contour plot from the OR side of the site: the search path leaves the feasible region and stops at an X."),
            ("d", "D · PARTS LIST", "", "A drawing\u2019s parts list where item 3, MZH-P-404, has quantity 0 and is struck out.")]


def nf_body():
    return f"""
    <section class="nf">
      <div>
        <div class="crumb">ERROR 404</div>
        <h1 class="h1">Part not found</h1>
        <p class="lead">This page is not in the assembly. It may have moved when the site was updated, or the link has a typo.</p>
        <div class="spec"><span class="k">REQUESTED</span><span><code>projects/old-page</code></span>
          <span class="k">STATUS</span><span>Not in this assembly</span>
          <span class="k">TRY</span><span>Home, Projects or Contact</span></div>
        <div class="acts"><a class="bkb" href="#"><s></s><s></s><s></s><s></s><span>BACK TO HOME</span><i>→</i></a><a class="bkb" href="#"><s></s><s></s><s></s><s></s><span>SEE PROJECTS</span><i>→</i></a><a class="bkb" href="#"><s></s><s></s><s></s><s></s><span>CONTACT</span><i>→</i></a></div>
      </div>
      <div class="nfd nfr">{draw("b")}{draw("c")}</div>
    </section>"""


# ---------------- head tags: favicon + share image ----------------
SITE = "https://md-zaid-hossain.github.io"      # GitHub Pages user site (repository md-zaid-hossain.github.io)


def head_tags():
    import urllib.parse
    import logo_mark as LM
    icon = LM.FAVICON_SVG           # Zaid's own favicon (21 Nov); the old option A (filled ZH) is no longer used
    desc = "Industrial engineer: operations research and optimization, CAD and 3D printing, ergonomics. Projects, research, experience and awards."
    return (f'<link rel="icon" type="image/svg+xml" href="data:image/svg+xml,{urllib.parse.quote(icon)}">\n'
            f'<meta name="description" content="{desc}">\n'
            f'<meta property="og:type" content="website">\n<meta property="og:url" content="{SITE}/">\n'
            f'<meta property="og:title" content="Md. Zaid Hossain · Industrial engineer">\n'
            f'<meta property="og:description" content="{desc}">\n'
            f'<meta property="og:image" content="{SITE}/assets/share.jpg">\n<meta property="og:image:width" content="1200">\n'
            f'<meta property="og:image:height" content="630">\n<meta name="twitter:card" content="summary_large_image">\n')


def mark_current(html):
    """Mark the current page in the phone menu, from the desktop nav item the page builder marked."""
    import re
    m = re.search(r'<a href="#" class="on" aria-current="page">(\w+)</a>', html)
    if not m:
        return html
    n = m.group(1)
    return re.sub(rf'<a href="#"><i>(\d\d)</i>{n}<b>', rf'<a href="#" class="on" aria-current="page"><i>\1</i>{n}<b>', html, count=1)
