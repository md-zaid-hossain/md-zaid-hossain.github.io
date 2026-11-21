#!/usr/bin/env python3
"""Parts approved on the proposal board (Zaid, 2026-11-17) and now used on the real pages:
hero facts table with the turning-gear indicator, rotating hero figure (A landscape -> B gear -> C QC),
part-sheet project cards, footer with revision table + green factory, printer figure for the Projects header."""
import math
import or_figs as OR
import or_figs2 as OR2
import or_figs3 as OR3
import or_figs4 as OR4

SOFTWARE = {"SOLIDWORKS", "KeyShot", "Creality", "Creality Slicer", "Bambu Studio", "Fusion 360", "3DEXPERIENCE", "AutoCAD"}
PARTNO = {k: i + 1 for i, k in enumerate(["foil-plant", "distillation", "ev-station", "headstock", "gear-holder", "pin-locator",
                                           "vice", "haas-vf2", "rotor", "differential", "quadcopter", "servo", "payloader", "bicycle"])}


def gear_icon(size=14):
    pts = []
    for i in range(16):
        a0 = i * math.pi / 8
        r = 7 if i % 2 == 0 else 5.2
        for da in (-0.17, 0.17):
            pts.append((8 + r * math.cos(a0 + da), 8 + r * math.sin(a0 + da)))
    d = "M" + " L".join(f"{x:.2f} {y:.2f}" for x, y in pts) + " Z M10.2 8 A2.2 2.2 0 1 0 5.8 8 A2.2 2.2 0 1 0 10.2 8 Z"
    return (f'<span class="ind ind-gear" aria-hidden="true"><svg width="{size}" height="{size}" viewBox="0 0 16 16">'
            f'<path fill-rule="evenodd" d="{d}"/></svg></span>')


def hero_facts():
    """CURRENTLY + degrees in one balanced table; M.Sc. first (Zaid)."""
    return (f'<div class="deg deg3">'
            f'<span class="k">{gear_icon()}CURRENTLY</span><span>Fab Lab Program Engineer · <em>IAT, BUET</em></span>'
            f'<span class="k">M.SC. ENG.</span><span>IEM · KUET · <em>ongoing</em></span>'
            f'<span class="k">B.SC. ENG.</span><span>IPE · KUET · <em>2025</em></span></div>')


def hero_figure(gear_html):
    style, html = OR3.hero_cycle2(gear_html, compact=True)
    return style + html


# project detail pages that exist (real site paths)
PAGES = {"ev-station": "/projects/ev-charging-station/", "foil-plant": "/projects/aluminium-foil-plant/", "rotor": "/projects/dc-motor-rotor/", "differential": "/projects/car-differential/",
         "quadcopter": "/projects/quadcopter-drone/", "servo": "/projects/servo-motor/", "bicycle": "/projects/bicycle/", "payloader": "/projects/payloader/", "gear-holder": "/projects/gear-pinion-phone-holder/", "headstock": "/projects/lathe-headstock-gearbox/",
         "pin-locator": "/projects/3-2-1-pin-locator/", "vice": "/projects/bench-vice/",
         "distillation": "/projects/distillation-plant/", "haas-vf2": "/projects/haas-vf2-cnc-milling/"}


def part_card(key, cat, title, tags, img_html):
    """Project card: same frame + hover as before; part number and spec rows instead of description and tags."""
    soft = [t for t in tags if t in SOFTWARE]
    work = [t for t in tags if t not in SOFTWARE]
    n = PARTNO.get(key, 99)
    short = cat.split(" · ")[0].replace("MANUFACTURING", "MFG")
    rows = f'<span class="k">SOFTWARE</span><span>{" · ".join(soft) if soft else "SOLIDWORKS"}</span>'
    rows += f'<span class="k">OUTPUT</span><span>{" · ".join(work) if work else "3D model · render"}</span>'
    return f'''
        <a class="card pc pcx" href="{PAGES.get(key, "#")}">
          {img_html}
          <div class="ph2"><span>PART NO. <b>MZH-P-{n:03d}</b></span><span class="cat" title="{cat}">{short}</span></div>
          <h3>{title}</h3>
          <div class="spec">{rows}</div>
        </a>'''


def footer(clock_now, dark=True):
    # profile links with a small dot between each, so the six words read as separate items
    prof = [("https://github.com/md-zaid-hossain", "GITHUB"), ("https://www.linkedin.com/in/md-zaid-hossain", "LINKEDIN"),
            ("https://www.researchgate.net/profile/Md-Zaid-Hossain", "RESEARCHGATE"), ("https://scholar.google.com/citations?user=Fu6JmxIAAAAJ", "SCHOLAR"),
            ("https://orcid.org/0009-0003-3301-3609", "ORCID"), ("https://grabcad.com/md.zaid.hossain-1", "GRABCAD")]
    links = '<i class="efd" aria-hidden="true"></i>'.join(f'<a href="{u}">{t}</a>' for u, t in prof)
    revs = """<div class="revs"><div><table><thead><tr><th>REV</th><th>DATE</th><th>WHAT CHANGED<span class="lg"> ON THIS SITE</span></th></tr></thead><tbody>
          <tr><td class="r">A</td><td class="d">2026-11</td><td>First release</td></tr>
        </tbody></table><a class="all" href="#">ALL REVISIONS →</a></div></div>"""
    return f'''
  <footer class="ftr ftrx">
    <div class="wrap">
      {revs}
      <div class="fsc">{OR4.footer3_scene(dark)}</div>
      <div class="efr"><div class="cp"><b>© 2026 Md. Zaid Hossain</b> · Dhaka, Bangladesh · <span class="tm">{clock_now} GMT+6</span></div>
      <nav aria-label="Profiles">{links}</nav></div>
    </div>
  </footer>'''


def printer_figure():
    return (f'<div class="prfr"><div class="hcl">FIG. A · FDM 3D PRINTING · ENDER-3 V2 NEO</div>{OR4.printer3_svg()}'
            f'<div class="prcap"><span>3-2-1 FIXTURE · PLA · {OR4.PR3_N} LAYERS</span><div class="prog2 prog3"><i></i></div></div></div>')


BASE_CSS = """
/* ===== approved parts (site_parts.py) ===== */
.deg{display:grid;grid-template-columns:120px 1fr;width:100%;max-width:440px;border-top:1px solid var(--line2)}
.deg>span{padding:8px 0;border-bottom:1px solid var(--line);font-size:15px;color:var(--strong)}
.deg>span.k{font:600 12.5px 'IBM Plex Mono',monospace;letter-spacing:.1em;color:var(--muted);padding-top:10px}
.deg em{font-style:normal;color:var(--muted)}
.deg3{grid-template-columns:150px 1fr;max-width:520px}
.deg3 .k{display:flex;align-items:center;gap:8px}
.ind{flex:none;display:inline-flex;align-items:center;justify-content:center}
.ind-gear svg{display:block;animation:indSpin 6s linear infinite}
.ind-gear path{fill:var(--acc)}
@keyframes indSpin{to{transform:rotate(360deg)}}
@media (prefers-reduced-motion:reduce){.ind-gear svg{animation:none}}
/* hero figure slot */
.hcy.solo{display:block}
.hcy.solo .stg{position:relative;height:470px;overflow:hidden}
.hcy .pgs.mini{display:grid;grid-template-columns:repeat(3,1fr) auto;gap:10px;margin-top:8px;padding:0 14px}
.hcy .pgs.mini .pg{gap:5px}
.hcy .pgs.mini span{font:600 11.5px 'IBM Plex Mono',monospace;letter-spacing:.1em;color:var(--muted)}
/* part-sheet project cards */
.spec{display:grid;grid-template-columns:96px 1fr;border-top:1px solid var(--line2)}
.spec>span{padding:7px 0;border-bottom:1px solid var(--line);font-size:14px;color:var(--text)}
.spec>span.k{font:600 12px 'IBM Plex Mono',monospace;letter-spacing:.1em;color:var(--muted);padding-top:9px}
.pcx .ph2{display:flex;justify-content:space-between;gap:12px;padding:12px 20px;border-bottom:1px solid var(--line);font:600 12.5px 'IBM Plex Mono',monospace;letter-spacing:.08em;color:var(--muted)}
.pcx .ph2 b{color:var(--acc-t);font-weight:600}
.pcx .ph2 span{white-space:nowrap}
.pcx .ph2 .cat{overflow:hidden;text-overflow:ellipsis;min-width:0}
.pcx h3{margin:0;padding:14px 20px 4px;font:600 19px/1.25 'Space Grotesk',sans-serif;color:var(--strong)}
.pcx .spec{margin:8px 20px 18px}
.pcx:hover .ph2{border-bottom-color:var(--line2)}
/* footer: revision table + factory beside it */
.ftr.ftrx .wrap{grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:22px 32px;padding-top:26px;align-items:end}
.ftr.ftrx nav{justify-self:end}
/* footer profile links: dot separators between words */
.ftr nav{align-items:center;column-gap:13px!important}
.ftr nav .efd{display:block;flex:none;width:4px;height:4px;border-radius:50%;background:var(--muted);opacity:.55}
/* copyright line and profile links never break onto a second line */
.ftr .cp,.ftr .cp b{white-space:nowrap}
.ftr nav{flex-wrap:nowrap!important}.ftr nav a{white-space:nowrap}
/* copyright left, links right on one row; links move under it only when both cannot fit side by side */
.ftr.ftrx .efr{grid-column:1/-1;display:flex;flex-wrap:wrap;justify-content:space-between;align-items:center;column-gap:28px;row-gap:14px;min-width:0}
.ftr nav{column-gap:clamp(9px,1vw,13px)!important}
/* between phone and desktop: shrink the two lines a little so they still share one row */
@media (min-width:761px) and (max-width:1100px){.zh .ftr .cp{font-size:clamp(10.5px,1.4vw,15px)!important}.zh .ftr .cp .tm{font-size:.88em!important}.zh .ftr nav a{font-size:clamp(9px,1.2vw,13px)!important;letter-spacing:.03em!important}.zh .ftr nav{column-gap:clamp(7px,.95vw,13px)!important}.zh .ftr.ftrx .efr{column-gap:clamp(14px,2.4vw,28px)}}
.ftr.ftrx .cp{grid-column:1}
.ftrx .fsc{align-self:end;min-width:0}
.ftrx .revs{align-self:end;border:1px solid var(--line2);border-radius:8px;overflow:hidden;background:var(--surface)}
.ftrx .revs table{width:100%;border-collapse:collapse;font-size:13.5px}
.ftrx .revs th{font:600 12px 'IBM Plex Mono',monospace;letter-spacing:.12em;color:var(--muted);text-align:left;padding:8px 14px;border-bottom:1px solid var(--line2)}
.ftrx .revs td{padding:8px 14px;border-top:1px solid var(--line);color:var(--text)}
.ftrx .revs td.r{font:700 13px 'IBM Plex Mono',monospace;color:var(--acc-t);width:56px}
.ftrx .revs td.d{font:500 12.5px 'IBM Plex Mono',monospace;color:var(--body);white-space:nowrap;width:96px}
.ftrx .revs .all{display:block;padding:8px 14px;border-top:1px solid var(--line);font:600 12px 'IBM Plex Mono',monospace;letter-spacing:.08em;color:var(--acc-t)}
/* projects header with the printer */
.phg{display:grid;grid-template-columns:minmax(0,1fr) 440px;gap:32px;align-items:center}
.phf{overflow:hidden}
.prfr{position:relative;padding:14px 10px 10px}
.prfr .hcl{font:600 12px 'IBM Plex Mono',monospace;letter-spacing:.1em;color:var(--acc-t)}
.prfr .pr3{max-width:400px;margin:0 auto}
.prcap{margin-top:14px;display:flex;align-items:center;gap:12px;font:600 12px 'IBM Plex Mono',monospace;letter-spacing:.08em;color:var(--muted)}
.prog2{flex:1;height:5px;border-radius:999px;background:var(--line);overflow:hidden}
.prog2 i{display:block;height:100%;background:var(--acc);transform-origin:left}
/* shared keyframes used by the figures */
@keyframes beltMove2{to{stroke-dashoffset:-21}}
@keyframes bladeSpin{to{transform:rotate(360deg)}}
@keyframes spoolTurn{to{stroke-dashoffset:-240}}
@keyframes winFlick{0%,60%,100%{fill-opacity:.55}70%{fill-opacity:.2}}
@media (max-width:960px){.phg{grid-template-columns:1fr}.phf{max-width:440px}}
/* phone type scale v2 (2026-11-18, Zaid: overall text still too large on the phone).
   One scale for every page; !important because page CSS uses many two-class rules. */
@media (max-width:760px){
  .zh .h1{font-size:34px!important}
  .zh .ph .h1,.zh .phx .ph .h1{font-size:28px!important}
  .zh .h2,.zh .ctx .h2,.zh .cta .h2{font-size:22px!important}
  .zh .fb2 h2{font-size:21px!important}
  .zh main h3,.zh .card h3,.zh .dash h3{font-size:16px!important}
  .zh .lead,.zh .ph .lead{font-size:15px!important}
  .zh main p,.zh main li,.zh .org,.zh .vn,.zh .st .s,.zh .tbn,.zh .pubfoot,.zh .pub .yr,
  .zh .note2,.zh .brief p,.zh .card span.t,.zh .more-card span{font-size:14px!important}
  /* phone: copyright, city and clock always on one line */
  .zh .ftr .cp,.zh .ftr .cp b{font-size:clamp(10px,3.05vw,13px)!important;white-space:nowrap}
  .zh .ftr .cp .tm{font-size:.92em!important}
  /* phone: all six profile links on one line, spread edge to edge */
  .zh .ftr nav{flex-wrap:nowrap!important;justify-content:space-between;gap:0!important;column-gap:0!important;width:100%;justify-self:stretch!important}
  .zh .ftr nav .efd{width:3px;height:3px}
  .zh .ftr nav a{font-size:clamp(9px,2.6vw,11.5px)!important;letter-spacing:.02em!important;white-space:nowrap}
  .zh .btn{font-size:14px!important;height:44px}
  .zh .bkb{font-size:12px!important;height:38px;padding:0 14px;gap:8px}
  .zh .ebt,.zh .ebn{font-size:12.5px!important}
  .zh .st .n{font-size:24px!important}
  .zh .res b{font-size:24px!important}
  .zh .more-card b{font-size:30px!important}
  .zh .tmtx .dig b{font-size:26px!important}
  .zh .orf .kp b{font-size:16px!important}
  .zh .num b,.zh .rnum b{font-size:15px!important}
  .zh .brand b{font-size:15px!important}
  .zh .csheet .em{font-size:14px!important}
  .zh .focus li{font-size:14px!important}
  .zh .deg>span,.zh .csheet>span{font-size:13.5px}
  /* phone type scale v3 + spacing (2026-11-18, Zaid: finer scaling, less empty space) */
  .zh .h1{font-size:32px!important}
  .zh .ph .h1,.zh .phx .ph .h1,.zh .eph h1{font-size:28.6px!important}   /* every page title 30 px on the phone; Home and 404 heroes keep their own */
  .zh .h2,.zh .ctx .h2,.zh .cta .h2{font-size:21px!important}
  .zh .fb2 h2{font-size:20px!important}
  .zh main h3,.zh .card h3,.zh .dash h3{font-size:15.5px!important}
  .zh .chip,.zh .fc,.zh .doc,.zh .fb{font-size:13px!important}
  .zh .tag,.zh .bd,.zh .lk a,.zh .crumb{font-size:11.5px!important}
  .zh .pll{font-size:10.5px!important}
  /* spacing */
  .zh .sec{padding-top:52px!important}
  .zh .sh{margin-bottom:16px!important}
  .zh .hin{padding:28px 0 20px!important;gap:18px!important}
  .zh .hc{gap:16px!important}
  .zh .hcy.solo .stg{height:340px!important}
  .zh .hcy .sl2 .hsv{padding:0 4px}
  .zh .hcy .pgs.mini{margin-top:4px}
  .zh .pl{margin-top:16px!important}
  .zh .stats{margin-top:14px}
  .zh .st{padding:16px 18px!important}
  .zh .ph{padding-top:28px!important}
  .zh .phg{gap:12px!important}
  .zh .prfr .pr3{max-width:280px}
  .zh .prfr{padding:6px 10px 4px}
  .zh .tool{margin-top:20px!important}
  .zh .th{height:160px!important}
  .zh .more-card{min-height:0!important;padding:28px 20px!important}
  .zh .feat .fi{min-height:190px!important}
  .zh .ftr{margin-top:48px!important}
  .zh .ctx{padding:22px 18px!important;gap:22px!important}
  .zh .cact{margin-top:18px!important}
  .zh .pub{padding:16px 18px!important}
  .zh .card.sk,.zh .sk{padding:18px!important}
  .zh .area{padding:18px!important}
  .zh .figband{margin-top:24px!important}
  .zh .deg>span.k,.zh .csheet>span.k{font-size:11px!important;letter-spacing:.08em}
  .zh .deg3{grid-template-columns:112px 1fr}
  /* hero gear pair: smaller on phones so the big gear is not cut at the left edge */
  .zh .hcy .g3d{height:250px}
  .zh .hcy .g3d .pl3{transform:translateX(28px) scale(.74) rotateX(57deg) rotateZ(-24deg)}
}
@media (max-width:760px){
  .ftr.ftrx .wrap{grid-template-columns:1fr}.ftr.ftrx nav{justify-self:start}
  .ftrx .revs td.d{width:auto}
  .hcy.solo .stg{height:380px}
  .hcy.solo .sl{display:flex;flex-direction:column;justify-content:center}
  .hcy .hcl{position:relative;z-index:3;padding-bottom:6px}
  .hcy .hsv .lsv text{font-size:34px!important}
  .hcy .hsv .qcs text{font-size:30px}
  .hcy .hsv .qcc text{font-size:30px}
  .ftrx .revs .lg{display:none}
  .deg3{grid-template-columns:118px 1fr}
  .pcx .ph2{flex-direction:column;gap:4px}
}
"""


PCALM_CSS = """
/* 06 Contact calm tune (approved 2026-11-18) */
.ctx .focus2 .fc{border:1px solid var(--line);border-radius:999px;background:transparent;color:var(--body);font-size:13px;padding:5px 12px}
.ctx .focus2 .fc.open{border:1px dashed var(--line2);color:var(--muted)}
.ctx .focus2 .fc.open:hover{color:var(--acc-t);border-color:var(--acc-t)}
.ctx .dial .work{stroke-width:5;stroke-opacity:.38}
.ctx .dial .hub{fill:var(--strong)}
.ctx .ind-gear path{fill:var(--muted)}

/* project cards: calm pictures + quiet VIEW PROJECT line (approved 2026-11-18) */
.pc{display:flex;flex-direction:column}
.pc .th.has{background:var(--surface2)}
.pc .th.has img{position:absolute;inset:8px;width:calc(100% - 16px)!important;height:calc(100% - 16px)!important;object-fit:cover;border-radius:5px;
  filter:brightness(.9) saturate(.88);transition:filter .4s ease,transform .6s ease}
.pc:hover .th.has img{filter:none;transform:scale(1.03)}
.pc .pvw{display:flex;justify-content:space-between;align-items:center;margin:auto 20px 0;padding:12px 0 16px;border-top:1px solid var(--line);
  font:600 11px 'IBM Plex Mono',monospace;letter-spacing:.12em;color:var(--muted);transition:color .25s ease}
.pc .pvw i{font-style:normal;transition:transform .25s ease}
.pc:hover .pvw{color:var(--acc-t)}
.pc:hover .pvw i{transform:translateX(4px)}
"""


def css():
    import sys, os
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), "lib"))
    import bd_map as BM
    return (BASE_CSS + CONTACT_CSS + BM.MAP_CSS + OR.CSS + OR2.HERO_CSS + OR3.qc_css() + OR4.qc2_css() + OR3.LAND2_CSS + OR3.HERO2_CSS
            + OR4.FOOT3_CSS + OR4.printer3_css() + OR4.SEW3_CSS + OR4.SEW4_CSS + PCALM_CSS)


# ---------------- contact section (approved 2026-11-17: focus boxes + open slot, contact table, 24 h dial, bracket buttons) ----------------
CONTACT_CSS = """
.ctx.ctx{grid-template-columns:minmax(0,1fr) 410px;gap:40px}
.ctx .focus2{flex-wrap:wrap;gap:6px}
.ctx .focus2 .fc{font-size:13.5px;padding:5px 10px;white-space:nowrap}
.ctx .cp2{background:transparent;font-family:'IBM Plex Mono',monospace}
.inst2{align-items:stretch;gap:12px;padding:16px}
.inst2 .ih{gap:10px}
.tmrow{display:grid;grid-template-columns:150px 1fr;gap:16px;align-items:center;padding-top:12px;border-top:1px solid var(--line)}
.tmrow .dial{width:150px;height:150px}
.tmtx{display:flex;flex-direction:column;gap:8px;min-width:0}
.tmtx .ih2{font:600 11.5px 'IBM Plex Mono',monospace;letter-spacing:.1em;color:var(--muted)}
.tmtx .dig b{font:600 34px/1 'IBM Plex Mono',monospace;color:var(--strong)}
.inst2 .tmtx .stt{display:flex;align-items:center;justify-content:flex-start;text-align:left;font-size:13.5px;gap:7px;flex-wrap:nowrap}
.inst2 .tmtx .stt .ind{flex:none}
.inst2 .tmtx .yt{display:flex;flex-wrap:wrap;align-items:baseline;gap:2px 8px;text-align:left;font-size:11.5px;padding-top:8px;border-top:1px dashed var(--line)}
.inst2 .tmtx .yt b{font:600 15px 'IBM Plex Mono',monospace;color:var(--strong)}
.inst2 .tmtx .yt em{flex-basis:100%;font-style:normal;font-family:Inter,sans-serif;font-size:12.5px;color:var(--muted)}
.inst2 .tmtx .stt{align-items:flex-start}
.inst2 .tmtx .stt .ind{margin-top:3px}
.inst2 .tmtx .stt>span{white-space:nowrap}
.inst2 .tmtx .stt{font-size:13px}
.ctx.ctx{align-items:center}
.ctx .cact{margin-top:26px}
.inst2 .ih{font-size:11.5px;white-space:nowrap}
@media (max-width:960px){.ctx.ctx{grid-template-columns:1fr}.inst2{max-width:440px}}
.inst2{transition:border-color .25s,transform .25s,box-shadow .25s}
.inst2:hover{border-color:var(--acc);transform:translateY(-2px);box-shadow:0 10px 26px -18px rgba(0,0,0,.45)}
.inst2 .bdmap .pin .ring{transform-box:fill-box;transform-origin:center;transition:transform .45s cubic-bezier(.3,1.3,.5,1)}
.inst2:hover .bdmap .pin .ring{transform:scale(1.35)}
.inst2:hover .ih span:first-child{color:var(--acc-t)}
.inst2 .ih span{transition:color .25s}
@media (max-width:960px){.ctx.ctx>.inst2{justify-self:center;width:100%;max-width:440px}}
@media (prefers-reduced-motion:reduce){.inst2,.inst2 .bdmap .pin .ring{transition:none}.inst2:hover{transform:none}}
@media (max-width:760px){.inst2 .tmtx .stt>span{white-space:normal}.ctx .focus2 .fc{white-space:normal}.inst2{max-width:100%;min-width:0}.inst2 .ih{white-space:normal;flex-wrap:wrap}.ctx .csheet>span{min-width:0}.ctx .csheet a.plk{margin-right:10px}.tmrow{grid-template-columns:112px 1fr;gap:12px}.tmrow .dial{width:112px;height:112px}.tmtx .dig b{font-size:28px}.inst2 .tmtx .ih2{font-size:10.5px;white-space:nowrap;letter-spacing:.06em}.inst2 .tmtx .stt{font-size:12.5px}}
.focus2{display:flex;flex-wrap:wrap;align-items:center;gap:8px;margin-top:14px}
.focus2 .fk{font:600 12px 'IBM Plex Mono',monospace;letter-spacing:.1em;color:var(--muted);margin-right:4px}
.focus2 .fc{font-size:14px;padding:6px 11px;border:1px solid var(--line2);color:var(--strong);background:var(--surface2)}
.focus2 .fc.open{border-style:dashed;border-color:var(--acc);color:var(--acc-t);background:transparent}
.cact.col{flex-direction:column;align-items:flex-start;gap:14px}
.bkb{position:relative;display:inline-flex;align-items:center;gap:9px;height:40px;padding:0 16px;font:600 12.5px 'IBM Plex Mono',monospace;letter-spacing:.1em;color:var(--strong);background:var(--surface2);transition:background .2s,color .2s}
.bkb s{position:absolute;width:8px;height:8px;border:0 solid var(--line2);transition:all .2s}
.bkb s:nth-child(1){top:0;left:0;border-top-width:2px;border-left-width:2px}
.bkb s:nth-child(2){top:0;right:0;border-top-width:2px;border-right-width:2px}
.bkb s:nth-child(3){bottom:0;left:0;border-bottom-width:2px;border-left-width:2px}
.bkb s:nth-child(4){bottom:0;right:0;border-bottom-width:2px;border-right-width:2px}
.bkb i{font-style:normal;transition:transform .2s}
.bkb span{padding-bottom:2px;background:linear-gradient(var(--acc-t),var(--acc-t)) left bottom/0 2px no-repeat;transition:background-size .3s ease}   /* no line at rest (Zaid, 21 Nov); on hover a theme-colour line draws in from the left */
.bkb:hover span,.bkb:focus-visible span{background-size:100% 2px}
.bkb.p{background:var(--acc);color:var(--on-acc)}
.bkb.p s{border-color:var(--acc-t)}
.bkb:hover s:nth-child(1){top:-5px;left:-5px}.bkb:hover s:nth-child(2){top:-5px;right:-5px}
.bkb:hover s:nth-child(3){bottom:-5px;left:-5px}.bkb:hover s:nth-child(4){bottom:-5px;right:-5px}
.bkb:hover s{border-color:var(--acc)}
.bkb:hover i{transform:translateX(4px)}
.bkb:not(.p):hover{color:var(--acc-t)}
.ctx{position:relative;padding:44px 48px;display:grid;grid-template-columns:minmax(0,1.35fr) 300px;gap:48px;align-items:start}
.ctx .h2{font-size:34px}
.ctx .sub{margin:12px 0 0;font-size:16px;line-height:1.6;color:var(--body)}
.csheet{display:grid;grid-template-columns:120px 1fr;margin-top:22px;border-top:1px solid var(--line2);max-width:620px}
.csheet>span{padding:10px 0;border-bottom:1px solid var(--line);font-size:15px;color:var(--strong);display:flex;align-items:center;gap:10px;flex-wrap:wrap}
.csheet>span.k{font:600 12px 'IBM Plex Mono',monospace;letter-spacing:.1em;color:var(--muted)}
.csheet .em{font:600 15.5px 'IBM Plex Mono',monospace;color:var(--strong)}
.csheet .cp2{font:600 11.5px 'IBM Plex Mono',monospace;letter-spacing:.08em;padding:4px 9px;border:1px solid var(--line2);border-radius:5px;color:var(--body);cursor:pointer}
.csheet .cp2:hover{border-color:var(--acc);color:var(--acc-t)}
.csheet a.plk{font:600 12.5px 'IBM Plex Mono',monospace;letter-spacing:.06em;color:var(--body);white-space:nowrap}
.csheet a.plk:hover{color:var(--acc-t)}
.csheet em{font-style:normal;color:var(--muted)}
.cact{display:flex;gap:12px;flex-wrap:wrap;margin-top:24px}
.inst{border:1px solid var(--line);border-radius:12px;background:var(--surface2);padding:18px 18px 16px;display:flex;flex-direction:column;align-items:center;gap:10px}
.inst .ih{align-self:stretch;display:flex;justify-content:space-between;font:600 12px 'IBM Plex Mono',monospace;letter-spacing:.1em;color:var(--muted)}
.dial{width:210px;height:210px;display:block}
.dial .face{fill:var(--bg);stroke:var(--line2);stroke-width:1.5}
.dial .tk{stroke:var(--muted);stroke-width:1.2}
.dial .tk.b{stroke:var(--strong);stroke-width:2.4}
.dial .num{font:600 13px 'IBM Plex Mono',monospace;fill:var(--body)}
.dial .work{fill:none;stroke:var(--acc);stroke-width:7;stroke-opacity:.55;stroke-linecap:round}
.dial .hh{stroke:var(--strong);stroke-width:5;stroke-linecap:round}
.dial .mh{stroke:var(--strong);stroke-width:3;stroke-linecap:round}
.dial .sh{stroke:var(--acc-t);stroke-width:1.4;stroke-linecap:round}
.dial .hub{fill:var(--acc)}
.dial .lab{font:600 9.5px 'IBM Plex Mono',monospace;letter-spacing:.08em;fill:var(--acc-t)}
.inst .dig{display:flex;align-items:baseline;gap:8px}
.inst .dig b{font:600 30px/1 'IBM Plex Mono',monospace;color:var(--strong)}
.inst .dig span{font:500 13px 'IBM Plex Mono',monospace;color:var(--muted)}
.inst .stt{display:flex;align-items:center;gap:8px;font-size:14px;color:var(--body);text-align:center}
.inst .stt b{color:var(--strong);font-weight:600}
.inst .yt{font:500 12.5px 'IBM Plex Mono',monospace;color:var(--muted);text-align:center}
.ctx{padding:26px 20px;gap:28px}.ctx .h2{font-size:26px}
.csheet{grid-template-columns:96px 1fr}
@media (max-width:960px){.ctx{grid-template-columns:1fr}.inst{max-width:340px}}
@media (max-width:760px){.ctx{padding:26px 20px;gap:28px}.ctx .h2{font-size:26px}.csheet{grid-template-columns:96px 1fr}}
"""

BTN_CV = '<a class="bkb" href="#"><s></s><s></s><s></s><s></s><span>DOWNLOAD CV</span><i>↓</i></a>'
BTN_MAIL = '<a class="bkb" href="mailto:mdzaideng@gmail.com"><s></s><s></s><s></s><s></s><span>EMAIL ME</span><i>→</i></a>'


def contact(clock):
    """Home-page contact section. `clock` is build_home.clock_sample()."""
    import build_contact_prop as CP
    import sys, os
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), "lib"))
    import bd_map as BM
    d, kf = CP.dial(clock)
    c = clock
    status = (f'{gear_icon()}<span><b>Working hours</b> · replies today</span>' if c["on"]
              else '<span>○</span><span><b>Off hours</b> · replies after Fajr</span>')
    return "<style>" + kf + "</style>" + f'''
    <section class="sec" aria-labelledby="s-contact">
      <div class="card ctx">
        <div>
          <div class="eb"><span class="ebn">06</span><span class="ebt">CONTACT</span><span class="ebl"></span></div>
          <h2 class="h2" id="s-contact">Open to PhD positions and research collaborations.</h2>
          <div class="focus2"><span class="fc">Operations research</span><span class="fc">Ergonomics &amp; worker safety</span><span class="fc">Additive manufacturing</span><span class="fc open" title="Open to other fields: tell me what you have in mind">+ your field · open to discuss</span></div>
          <div class="csheet">
            <span class="k">EMAIL</span><span><span class="em">mdzaideng@gmail.com</span><button type="button" class="cp2" title="Copy email address">COPY</button></span>
            <span class="k">BASED IN</span><span>Dhaka, Bangladesh <em>· GMT+6</em></span>
            <span class="k">REPLIES</span><span>Fajr to Asr, Dhaka time <em>· today {c["fajr"]} to {c["asr"]}</em></span>
            <span class="k">PROFILES</span><span><a class="plk" href="https://www.linkedin.com/in/md-zaid-hossain">LINKEDIN ↗</a><a class="plk" href="https://orcid.org/0009-0003-3301-3609">ORCID ↗</a><a class="plk" href="https://scholar.google.com/citations?user=Fu6JmxIAAAAJ">SCHOLAR ↗</a></span>
          </div>
          <div class="cact">{BTN_MAIL}{BTN_CV}</div>
        </div>
        <div class="inst inst2">
          <div class="ih"><span>LOCATION · DHAKA</span><span>23.81° N · 90.41° E</span></div>
          {BM.map_svg()}
          <div class="tmrow">
            {d}
            <div class="tmtx">
              <div class="ih2">LOCAL TIME · GMT+6</div>
              <div class="dig"><b>{c["now"]}</b></div>
              <div class="stt">{status}</div>
              <div class="yt"><span>YOUR TIME</span><b>{c["visitor"]}</b><em>{c["diff"]} · from your device</em></div>
            </div>
          </div>
        </div>
      </div>
    </section>'''

# ---- real site: the lists above are replaced by content/*.yml (build/content_io.py) ----
import content_io as _C
PAGES.update({p['key']: f"/projects/{p['slug']}/" for p in _C.load_projects()[0]})
