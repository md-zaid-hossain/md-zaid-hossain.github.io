#!/usr/bin/env python3
"""Projects page mockup (dark / light / mobile). Calm pass approved by Zaid on 2026-11-20. Reuses the homepage header, footer, theme and
backdrop from build_home.py and swaps the page body."""
import re
import build_home as H

PIMG = H.PIMG

# (key, category label, filter group, title, one-line description, tools)
PROJECTS = [
    ("foil-plant", "CLIENT · 2026", "client", "Aluminium Foil Plant (50 TPD)",
     "Full 3D site layout of a 50-tonne-per-day foil plant: 12-step process line from melting to dispatch, utilities and material flow.", ["SOLIDWORKS", "Plant layout", "Walk-through video"]),
    ("distillation", "CLIENT · SOAP PROCESS PLANT", "client", "Distillation Plant",
     "Distillation section of a soap manufacturing plant, laid out to the client's process requirements.", ["SOLIDWORKS", "Plant layout"]),
    ("headstock", "ACADEMIC LAB · IPE 4126", "academic", "Lathe Head-stock Gearbox",
     "Speed gearbox modelled from the lab lathe: gear train, shafts and housing.", ["SOLIDWORKS", "Gear design"]),
    ("gear-holder", "3D PRINTING", "additive", "Gear-Pinion Phone Holder",
     "Designed for printing, sliced in Creality and printed on an Ender-3 V2 Neo.", ["SOLIDWORKS", "Creality", "FDM"]),
    ("pin-locator", "ACADEMIC LAB · IPE 4226", "academic", "3-2-1 Pin Locator",
     "Fixture for exact workpiece location, modelled, drawn and 3D printed in the Tool Engineering lab.", ["SOLIDWORKS", "Drawing", "3D print"]),
    ("vice", "3D PRINTING", "additive", "3D-Printed Bench Vice",
     "Working vice with a printed lead screw and sliding jaw. Sliced in Creality Slicer and printed on a Creality CR-10 Smart.", ["SOLIDWORKS", "Creality Slicer", "FDM"]),
    ("haas-vf2", "TRAINING · KUET", "training", "HAAS VF-2 CNC Milling",
     "Machine model, toolpaths and NC program for a milling job, simulated before cutting.", ["Fusion 360", "CAM", "NC code"]),
    ("rotor", "PERSONAL", "self", "Rotor of a DC Motor",
     "Armature, commutator and windings modelled in detail and rendered.", ["SOLIDWORKS", "KeyShot"]),
    ("differential", "PERSONAL", "self", "Car Differential Gearbox",
     "Bevel-gear differential with a motion study of the gear train.", ["SOLIDWORKS", "KeyShot", "Motion study"]),
    ("quadcopter", "PERSONAL", "self", "Quadcopter Drone",
     "Frame, arms, motors and propellers assembled and rendered.", ["SOLIDWORKS", "KeyShot"]),
    ("servo", "PERSONAL", "self", "Servo Motor",
     "Micro-servo with its internal gear train shown through a clear housing.", ["SOLIDWORKS"]),
    ("payloader", "PERSONAL", "self", "Payloader",
     "Wheel loader assembly: chassis, cab, lift arms and bucket.", ["SOLIDWORKS"]),
    ("bicycle", "PERSONAL", "self", "Bicycle",
     "BMX-style bicycle assembly: frame, wheels, drive train and controls.", ["SOLIDWORKS"]),
]

FILTERS = [("all", "All", "30+"), ("client", "Client", None), ("competition", "Competition", None),
           ("academic", "Academic lab", None), ("training", "Training", None), ("additive", "3D printing", None),
           ("self", "Personal", None)]

STATS = [("30+", "projects"), ("477", "parts"), ("109", "assemblies"), ("34", "STEP models"), ("23", "STL files")]

CSS = """
/* ===== projects page ===== */
.crumb{font:600 12.5px 'IBM Plex Mono',monospace;letter-spacing:.1em;color:var(--muted)}
.crumb a:hover{color:var(--acc-t)}
.ph{position:relative;padding:64px 0 8px}
.ph .h1{font-size:52px;margin-top:18px}
.ph .lead{margin-top:16px;max-width:720px;font-size:19px}
.nums{display:flex;flex-wrap:wrap;gap:10px;margin-top:22px}
.num{display:flex;align-items:baseline;gap:8px;padding:8px 14px;border:1px solid var(--line);border-radius:8px;background:var(--surface);backdrop-filter:var(--glass)}
.num b{font:600 18px 'IBM Plex Mono',monospace;color:var(--acc-t)}
.num span{font-size:14px;color:var(--body)}
.tool{display:flex;flex-wrap:wrap;align-items:center;justify-content:space-between;gap:14px;margin-top:40px;padding:12px;border:1px solid var(--line);border-radius:12px;background:var(--surface);backdrop-filter:var(--glass);position:relative;z-index:2}
.fl{display:flex;flex-wrap:wrap;gap:6px}
.fb{display:inline-flex;align-items:center;gap:8px;height:36px;padding:0 14px;border-radius:999px;border:1px solid transparent;background:transparent;color:var(--body);font:500 14px 'Inter',system-ui,sans-serif;cursor:pointer;transition:background .2s,color .2s,border-color .2s}
.fb:hover{color:var(--strong);border-color:var(--line2)}
.fb.on{background:var(--acc);color:var(--on-acc)}
.fb em{font:600 12.5px 'IBM Plex Mono',monospace;font-style:normal;opacity:.85}
.tr{display:flex;align-items:center;gap:10px}
.srch{display:flex;align-items:center;gap:8px;height:38px;width:240px;padding:0 12px;border:1px solid var(--line2);border-radius:8px;color:var(--muted);font-size:14px;background:var(--surface2)}
.sort{display:flex;align-items:center;gap:6px;height:38px;padding:0 12px;border:1px solid var(--line2);border-radius:8px;color:var(--body);font-size:14px;font-weight:500;background:var(--surface2)}
.feat{display:grid;grid-template-columns:1.35fr 1fr;margin-top:28px;overflow:hidden}
.feat .fi{position:relative;min-height:380px;background:#1A1D24;overflow:hidden}
.feat .fi img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}
.feat .fi .fx{position:absolute;left:16px;top:16px;font:600 12.5px 'IBM Plex Mono',monospace;letter-spacing:.08em;color:#fff;background:rgba(12,15,20,.72);border:1px solid rgba(255,255,255,.2);padding:6px 10px;border-radius:6px;backdrop-filter:blur(6px)}
.feat .fb2{padding:32px 34px;display:flex;flex-direction:column;gap:12px}
.feat .c{font:600 12.5px 'IBM Plex Mono',monospace;letter-spacing:.1em;color:var(--acc-t)}
.feat h2{margin:0;font:600 30px/1.15 'Space Grotesk',sans-serif;color:var(--strong)}
.feat p{margin:0;font-size:15px;line-height:1.6;color:var(--body)}
.feat ul{margin:4px 0 0;padding:0;list-style:none;display:flex;flex-direction:column;gap:7px}
.feat li{display:flex;gap:10px;font-size:14.5px;color:var(--body)}
.feat li:before{content:"";flex:none;width:7px;height:7px;margin-top:7px;background:var(--acc);transform:rotate(45deg)}
.fg{display:flex;flex-direction:column;gap:10px;margin-top:2px}
.fgh{font:600 12.5px 'IBM Plex Mono',monospace;letter-spacing:.1em;color:var(--muted);margin-bottom:6px}
.brief{padding-top:14px;border-top:1px solid var(--line2)}
.brief .bh{font:600 12.5px 'IBM Plex Mono',monospace;letter-spacing:.1em;color:var(--acc-t);margin-bottom:8px}
.brief p{margin:0 0 12px;font-size:14.5px;line-height:1.6;color:var(--body)}
.brief .spec{grid-template-columns:108px 1fr}
.feat .acts{display:flex;gap:10px;flex-wrap:wrap;margin-top:auto;padding-top:8px}
.pgrid2{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:20px;margin-top:20px}
.pgrid2 .th{height:210px}
.more-card{display:flex;flex-direction:column;align-items:center;justify-content:center;gap:10px;min-height:360px;border:1.5px dashed var(--line2);border-radius:10px;color:var(--body);text-align:center;padding:24px;transition:border-color .2s,color .2s}
.more-card:hover{border-color:var(--acc);color:var(--acc-t)}
.more-card b{font:600 40px/1 'IBM Plex Mono',monospace;color:var(--acc-t)}
.more-card span{font-size:15px}
.more-card em{font-style:normal;font:600 12.5px 'IBM Plex Mono',monospace;letter-spacing:.08em;margin-top:6px}
/* ===== projects list, calm pass, approved 2026-11-20 (prefix pq) ===== */
.pq .ph{padding-top:40px;padding-bottom:0}
.pq .ph .h1{font-size:44px;margin-top:10px}
.pq .ph .lead{margin-top:10px;max-width:720px;font-size:16.5px;line-height:1.6}
.pq .phg{grid-template-columns:minmax(0,1fr) 330px;gap:40px;align-items:end}
.pq .prfr{padding:0}
.pq .prfr .hcl{font-size:11px;letter-spacing:.08em;white-space:nowrap}
.pq .prfr .pr3{max-width:290px}
.pq .prcap{font-size:11px;white-space:nowrap}
.pq .est{grid-template-columns:repeat(5,minmax(0,1fr));margin-top:24px}
.pq .tool{flex-wrap:nowrap;margin-top:32px}
.pq .fl{flex-wrap:nowrap;min-width:0}
.pq .fb{white-space:nowrap}
.pq .srch{width:220px}
.pq .feat .c{white-space:nowrap}
.pq .pgrid2 .more-card{grid-column:span 2;min-height:0;flex-direction:row;gap:22px;text-align:left;padding:28px 36px}
.pq .more-card b{font-size:52px}
.pq .more-card div{display:flex;flex-direction:column;gap:8px;max-width:420px}
.pq .more-card em{margin-top:0}
@media (max-width:1180px){.pq .tool{flex-wrap:wrap}.pq .fl{flex-wrap:wrap}}
@media (max-width:1100px){
  .pq .pgrid2{grid-template-columns:repeat(2,minmax(0,1fr))}
  .pq .pgrid2 .more-card{grid-column:auto;flex-direction:column;text-align:center;padding:24px}
  .pq .more-card div{align-items:center}
}
@media (max-width:960px){.pq .phg{grid-template-columns:1fr;gap:20px}.pq .phf{max-width:360px;width:100%;margin:0 auto}}
@media (max-width:760px){
  .pq .ph{padding-top:28px}
  .pq .feat .c,.pq .prcap,.pq .prfr .hcl{white-space:normal}
  .pq .tool{flex-wrap:nowrap}.pq .fl{flex-wrap:nowrap}
  .pq .est{grid-template-columns:1fr 1fr}
  .pq .est>div{border-left:1px solid var(--line);border-top:0}
  .pq .est>div:nth-child(odd){border-left:0}
  .pq .est>div:nth-child(n+3){border-top:1px solid var(--line)}
  .pq .est>div:last-child{grid-column:span 2}
  .pq .pgrid2{grid-template-columns:1fr}
  .pq .srch{width:auto}
}
@media (max-width:760px){
  .ph{padding-top:40px}
  .ph .h1{font-size:36px}
  .ph .lead{font-size:17px}
  .tool{flex-direction:column;flex-wrap:nowrap;align-items:stretch}
  .fl{flex-wrap:nowrap;overflow-x:auto;padding-bottom:4px;max-width:100%;min-width:0;scrollbar-width:none;-webkit-mask-image:linear-gradient(90deg,#000 82%,transparent);mask-image:linear-gradient(90deg,#000 82%,transparent)}
  .fl::-webkit-scrollbar{display:none}
  .fb{flex:none}
  .tr{width:100%}.srch{flex:1;width:auto}
  .feat{grid-template-columns:1fr}
  .feat .fi{min-height:230px}
  .feat .fb2{padding:22px 20px}
  .feat h2{font-size:24px}
  .pgrid2{grid-template-columns:1fr}
}
"""

SEARCH_ICON = '<svg width="15" height="15" viewBox="0 0 24 24" fill="none" aria-hidden="true"><circle cx="11" cy="11" r="7" stroke="currentColor" stroke-width="2"/><path d="m20 20-3.5-3.5" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>'
CHEV = '<svg width="12" height="12" viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="m6 9 6 6 6-6" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>'
CUBE = '<svg width="15" height="15" viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M12 2 3 7v10l9 5 9-5V7l-9-5Zm0 0v20M3 7l9 5 9-5" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round"/></svg>'


BRIEF = [("FOOTPRINT", "≤ 1 m × 0.8 m"), ("CHARGING", "≥ 2 EVs at once"), ("CABLES", "Concealed or retractable"),
         ("BUILD", "Modular and scalable"), ("ENCLOSURE", "Weatherproof against rain, heat and dust"), ("BONUS", "Renewable or solar energy")]


def fchips(xs):
    return "".join(f'<span class="fc">{x}</span>' for x in xs)


def body():
    import site_parts as SP
    chips = "".join(f'<button type="button" class="fb{" on" if k == "all" else ""}">{lbl}{f"<em>{n}</em>" if n else ""}</button>' for k, lbl, n in FILTERS)
    cards = "".join(H.project(cat, title, desc, tools, key) for key, cat, grp, title, desc, tools in PROJECTS)
    cards += ('<a class="more-card" href="#"><b>+17</b><div><span>more projects: machine tools, fixtures, furniture, '
              'composites and process-plant work</span><em>LOAD MORE ↓</em></div></a>')
    est = "".join(f"<div><b>{n}</b><span>{t}</span></div>" for n, t in STATS)
    return f"""
  <main class="wrap" style="position:relative;z-index:1">
    <div class="pq">
    <section class="ph phg"><div class="phc">
      <div class="crumb"><a href="#">HOME</a> / PROJECTS</div>
      <h1 class="h1">Projects</h1>
      <p class="lead">Client process plants, contest entries, lab assignments and printed parts, modelled in SOLIDWORKS and rendered in KeyShot. Some went on to the 3D printer or the CNC mill.</p>
      <div class="est">{est}</div>
    </div><div class="phf">{SP.printer_figure().replace("FDM 3D PRINTING", "FDM PRINTING")}</div></section>

    <div class="tool" role="toolbar" aria-label="Filter projects">
      <div class="fl">{chips}</div>
      <div class="tr">
        <div class="srch">{SEARCH_ICON}<span>Search projects…</span></div>
      </div>
    </div>

    <article class="card feat">
      <div class="fi"><img src="{PIMG['ev-station']}" alt="EV charging station render"><span class="fx">FEATURED · COMPETITION</span></div>
      <div class="fb2">
        <div class="c">ENERGY FEST 1.0 · ISOMETRIC ILLUMINATORS</div>
        <h2>Multi-purpose EV charging station for urban streets</h2>
        <p>Our answer was a slim kiosk with a solar canopy that adds seating, Wi-Fi, a display and safety systems to the street. We modelled it in SOLIDWORKS and rendered it in KeyShot.</p>
        <div class="brief">
          <div class="bh">THE BRIEF · SELECTION-ROUND QUESTION</div>
          <p>Street-side parking in Dhaka is cramped. A bulky charger blocks pedestrians and adds nothing else to the street. Design a compact, multi-purpose EV charging station that also improves the street.</p>
          <div class="spec">{"".join(f'<span class="k">{k}</span><span>{v}</span>' for k, v in BRIEF)}</div>
        </div>
        <div class="tags"><span class="tag">SOLIDWORKS</span><span class="tag">KeyShot</span><span class="tag">Top 20 finalist</span></div>
        <div class="acts"><a class="bkb" href="/projects/ev-charging-station/"><s></s><s></s><s></s><s></s><span>VIEW PROJECT</span><i>→</i></a><a class="bkb" href="#"><s></s><s></s><s></s><s></s><span>3D MODEL</span><i>→</i></a></div>
      </div>
    </article>

    <div class="pgrid2">{cards}
    </div>
    </div>
  </main>
"""


def projects_page(theme, title):
    html = H.page(theme, title)
    import build_edu_detail_prop as P   # .est stats strip, shared with the other pages
    html = html.replace("<style>", "<style>" + CSS + P.CSS, 1)
    a = html.index("  <!-- Hero: static page backdrop")
    b = html.index("  </main>") + len("  </main>")
    html = html[:a] + body() + html[b:]
    html = html.replace('<a href="#">Projects</a>', '<a href="#" class="on" aria-current="page">Projects</a>', 1)
    return html


if __name__ == "__main__":
    import type_scale as TS
    out = __import__("os").environ.get("PORTFOLIO_OUT", "/home/claude/zaid/project")
    open(f"{out}/Projects.dc.html", "w").write(TS.apply(projects_page("dark", "Projects: Dark")))
    open(f"{out}/ProjectsLight.dc.html", "w").write(TS.apply(projects_page("light", "Projects: Light")))
    open(f"{out}/ProjectsMobile.dc.html", "w").write(TS.apply(projects_page("dark", "Projects: Mobile")))
    open(f"{out}/ProjectsBlue.dc.html", "w").write(TS.apply(projects_page("dark_blue", "Projects: Dark blue")))
    open(f"{out}/ProjectsGreen.dc.html", "w").write(TS.apply(projects_page("dark_green", "Projects: Dark green")))
    open(f"{out}/ProjectsLightBlue.dc.html", "w").write(TS.apply(projects_page("light_blue", "Projects: Light blue")))
    open(f"{out}/ProjectsLightGreen.dc.html", "w").write(TS.apply(projects_page("light_green", "Projects: Light green")))
    print("projects written")

# ---- real site: the lists above are replaced by content/*.yml (build/content_io.py) ----
import content_io as _C
PROJECTS = _C.load_projects()[1]
