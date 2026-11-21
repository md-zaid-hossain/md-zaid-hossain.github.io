#!/usr/bin/env python3
"""More auto-running figures for the proposal board, plus the footer factory scene
and the hero figure rotation (FIG. A -> B -> C). Pure SVG + CSS/SMIL, no JavaScript."""
import math
from or_figs import iso, poly, box, factory_svg

GREEN_D, GREEN_L = "#4FC08A", "#1E7F55"   # trees stay green in every theme


# ---------------- G3: 3D printer (FDM) ----------------
PR_T = 12.0          # one print cycle in seconds
PR_N = 12            # layers


def _pct(t):
    return f"{t / PR_T * 100:.2f}%"


def printer_css():
    css = []
    t_print = 9.6
    for i in range(PR_N):
        on = (i + 1) * t_print / PR_N
        css.append(f"@keyframes prL{i}{{0%,{_pct(on-0.01)}{{opacity:0}}{_pct(on)},95%{{opacity:1}}100%{{opacity:0}}}}"
                   f".prl{i}{{animation:prL{i} {PR_T}s linear infinite}}")
    # gantry steps up one layer at a time
    steps = []
    for i in range(PR_N):
        t0 = i * t_print / PR_N
        steps.append(f"{_pct(t0)}{{transform:translateY({-i*0.3*30:.1f}px)}}")
        steps.append(f"{_pct(t0 + t_print / PR_N - 0.01)}{{transform:translateY({-i*0.3*30:.1f}px)}}")
    steps.append(f"{_pct(t_print)},96%{{transform:translateY({-PR_N*0.3*30:.1f}px)}}100%{{transform:translateY(0)}}")
    css.append("@keyframes prZ{" + "".join(steps) + "}.prz{animation:prZ " + f"{PR_T:g}" + "s linear infinite}")
    css.append("@keyframes prBar{0%{transform:scaleX(0)}80%,95%{transform:scaleX(1)}100%{transform:scaleX(0)}}"
               ".orf .prog{height:7px;border-radius:999px;background:var(--line);overflow:hidden}"
               ".orf .prog i{display:block;height:100%;background:var(--acc);transform-origin:left;animation:prBar " + f"{PR_T:g}" + "s linear infinite}")
    css.append("@media (prefers-reduced-motion:reduce){" + ",".join(f".prl{i}" for i in range(PR_N)) + "{opacity:1}}")
    return "\n".join(css)


def printer_svg(compact=False):
    s, ox, oy = 30, 300, 300
    P = lambda x, y, z: iso(x, y, z, s, ox, oy)
    o = [f'<svg class="prsvg" viewBox="0 0 600 560" role="img" aria-label="3D printer printing a part layer by layer">']
    o.append(poly([P(-1.5, -1.5, 0), P(9.5, -1.5, 0), P(9.5, 9.5, 0), P(-1.5, 9.5, 0)], "floor"))
    o.append(box(0, 8, 0, 8, 0, 0.8, P))                       # base
    o.append(box(1, 7, 1, 7, 0.8, 1.0, P))                     # bed
    o.append(box(0.2, 0.8, 3.7, 4.3, 0.8, 8.2, P))             # left upright
    o.append(box(0.2, 7.8, 3.7, 4.3, 8.2, 8.6, P))             # top bar
    for i in range(PR_N):                                      # printed part
        z0 = 1.0 + i * 0.3
        a, b = (2.4, 5.6) if i < 8 else (3.0, 5.0)
        o.append(f'<g class="prl{i}">{box(a, b, a, b, z0, z0 + 0.3, P, "at", "al", "ar")}</g>')
    # gantry: X bar + moving head, lifted one layer at a time
    zb = 1.9
    head = box(-0.45, 0.45, -0.45, 0.45, 0.35, 1.2, lambda x, y, z: iso(x, y, z, s, 0, 0))
    nozzle = [iso(-0.12, 0, 0.35, s, 0, 0), iso(0.12, 0, 0.35, s, 0, 0), iso(0, 0, 0, s, 0, 0)]
    a, b = P(2.6, 4.0, zb - 0.6), P(5.4, 4.0, zb - 0.6)
    o.append(f'<g class="prz">{box(0.5, 7.5, 3.85, 4.15, zb, zb + 0.3, P)}'
             f'<g>{head}{poly(nozzle, "at")}<animateMotion dur="0.8s" repeatCount="indefinite" '
             f'keyTimes="0;0.5;1" keyPoints="0;1;0" calcMode="linear" path="M{a[0]:.1f},{a[1]:.1f} L{b[0]:.1f},{b[1]:.1f}"/></g></g>')
    o.append(box(7.2, 7.8, 3.7, 4.3, 0.8, 8.2, P))             # right upright (front)
    if not compact:
        tx, ty = P(8, 0, 0.8)
        o.append(f'<text x="{tx+10:.1f}" y="{ty:.1f}">ENDER-3 V2 NEO</text>')
    o.append("</svg>")
    return "".join(o)


def printer_fig():
    return f'''<div class="orf">
      <div class="stage">{printer_svg()}<div class="tagl">AUTO-RUNS · ONE LAYER AT A TIME, THEN STARTS A NEW PART</div></div>
      <div class="dash">
        <div class="ft">FIG. C · OPTION 3</div>
        <h3>FDM 3D printing</h3>
        <div class="kp">
          <div><span class="k">LAYERS</span><b>{PR_N}</b></div>
          <div><span class="k">LAYER HEIGHT</span><b>0.2 mm</b></div>
          <div><span class="k">MATERIAL</span><b>PLA</b></div>
          <div><span class="k">INFILL</span><b>20%</b></div>
        </div>
        <div class="live">PRINT PROGRESS</div><div class="prog"><i></i></div>
        <div class="nt">The FabLab side of the work: a part grows layer by layer on the printer bed. Demo values.</div>
      </div>
    </div>'''


# ---------------- G4: supply-chain network ----------------
def network_svg():
    s, ox, oy = 25, 400, 40
    P = lambda x, y, z: iso(x, y, z, s, ox, oy)
    nodes = {"PLANT A": (1.5, 2.0, "plant"), "PLANT B": (2.0, 12.5, "plant"), "DC": (9.0, 7.5, "dc"),
             "C1": (16.5, 1.5, "cust"), "C2": (17.5, 6.5, "cust"), "C3": (16.0, 12.0, "cust"), "C4": (11.0, 15.5, "cust")}
    routes = [("PLANT A", "DC"), ("PLANT B", "DC"), ("DC", "C1"), ("DC", "C2"), ("DC", "C3"), ("DC", "C4")]
    o = ['<svg viewBox="0 0 860 470" role="img" aria-label="Supply chain network with trucks moving between plants, a distribution centre and customers">']
    o.append(poly([P(-1, -1, 0), P(20, -1, 0), P(20, 18, 0), P(-1, 18, 0)], "floor"))
    for a, b in routes:
        (x1, y1, _), (x2, y2, _) = nodes[a], nodes[b]
        p, q = P(x1, y1, 0), P(x2, y2, 0)
        o.append(f'<line class="route" x1="{p[0]:.1f}" y1="{p[1]:.1f}" x2="{q[0]:.1f}" y2="{q[1]:.1f}"/>')
    order = sorted(nodes.items(), key=lambda kv: kv[1][0] + kv[1][1])
    for name, (x, y, kind) in order:
        if kind == "plant":
            o.append(box(x - 1.2, x + 1.2, y - 1.0, y + 1.0, 0, 1.6, P))
            o.append(box(x + 0.4, x + 0.9, y - 0.6, y - 0.1, 1.6, 2.8, P))
        elif kind == "dc":
            o.append(box(x - 1.8, x + 1.8, y - 1.4, y + 1.4, 0, 1.3, P, "at", "al", "ar"))
        else:
            o.append(box(x - 0.6, x + 0.6, y - 0.6, y + 0.6, 0, 0.9, P))
        tx, ty = P(x, y, 3.0 if kind == "plant" else 2.6 if kind == "dc" else 2.0)
        o.append(f'<text class="{"h" if kind == "dc" else "s" if kind == "plant" else ""}" x="{tx-20:.1f}" y="{ty:.1f}">{name}{" · DISTRIBUTION CENTRE" if kind == "dc" else ""}</text>')
    truck = box(-0.45, 0.45, -0.3, 0.3, 0, 0.55, lambda x, y, z: iso(x, y, z, s, 0, 0), "at", "al", "ar")
    for k, (a, b) in enumerate(routes):
        (x1, y1, _), (x2, y2, _) = nodes[a], nodes[b]
        p, q = P(x1, y1, 0), P(x2, y2, 0)
        dur = 5 + (k % 3)
        o.append(f'<g>{truck}<animateMotion dur="{dur}s" begin="-{k*1.3:.1f}s" repeatCount="indefinite" '
                 f'keyTimes="0;0.45;0.5;0.95;1" keyPoints="0;1;1;0;0" calcMode="linear" '
                 f'path="M{p[0]:.1f},{p[1]:.1f} L{q[0]:.1f},{q[1]:.1f}"/></g>')
    o.append("</svg>")
    return "".join(o)


def network_fig():
    return f'''<div class="orf">
      <div class="stage">{network_svg()}<div class="tagl">AUTO-RUNS · ON THE REAL SITE, CLICK A ROUTE TO CLOSE IT AND SEE THE COST CHANGE</div></div>
      <div class="dash">
        <div class="ft">FIG. C · OPTION 4</div>
        <h3>Supply chain network</h3>
        <div class="kp">
          <div><span class="k">PLANTS</span><b>2</b></div>
          <div><span class="k">DC</span><b>1</b></div>
          <div><span class="k">CUSTOMERS</span><b>4</b></div>
          <div><span class="k">FILL RATE</span><b class="a">96%</b></div>
        </div>
        <div class="nt">Trucks run plant → distribution centre → customers. Network design and route optimization, the CSCA and Log-hub side of the work. Demo data.</div>
      </div>
    </div>'''


# ---------------- G5: ergonomics posture ----------------
def ergo_svg():
    hx, hy = 330, 300                   # hip (pivot)
    o = ['<svg viewBox="0 0 860 470" role="img" aria-label="Sewing operator bending forward; posture risk changes from low to high">']
    o.append('<line class="gl2" x1="60" y1="400" x2="800" y2="400"/>')
    # table + sewing machine
    o.append('<rect class="eq" x="430" y="270" width="300" height="14"/><rect class="eq" x="450" y="284" width="10" height="116"/>'
             '<rect class="eq" x="700" y="284" width="10" height="116"/>'
             '<path class="eq" d="M520 270 V220 H660 V250 H630 V270"/><rect class="eqa" x="600" y="250" width="10" height="20"/>')
    # chair
    o.append(f'<rect class="eq" x="{hx-70}" y="{hy+8}" width="100" height="10"/><rect class="eq" x="{hx-25}" y="{hy+18}" width="8" height="82"/>'
             f'<rect class="eq" x="{hx-75}" y="{hy-90}" width="8" height="108"/>')
    # legs (fixed)
    o.append(f'<path class="body" d="M{hx} {hy} L{hx+95} {hy+4} L{hx+100} 400"/>')
    # upper body rotates about the hip
    o.append(f'<g class="trunk" style="transform-origin:{hx}px {hy}px">'
             f'<path class="body" d="M{hx} {hy} L{hx} {hy-120}"/>'
             f'<g class="neck" style="transform-origin:{hx}px {hy-120}px"><path class="body" d="M{hx} {hy-120} L{hx} {hy-145}"/>'
             f'<circle class="head" cx="{hx}" cy="{hy-170}" r="24"/></g>'
             f'<path class="body" d="M{hx} {hy-110} L{hx+70} {hy-60} L{hx+150} {hy-40}"/>'
             f'<circle class="jt" cx="{hx}" cy="{hy-120}" r="5"/></g>')
    o.append(f'<circle class="jt" cx="{hx}" cy="{hy}" r="6"/>')
    # reference line + angle label
    o.append(f'<line class="ref" x1="{hx}" y1="{hy}" x2="{hx}" y2="{hy-200}"/>'
             f'<text x="{hx-120}" y="{hy-205}">VERTICAL REF.</text>')
    o.append("</svg>")
    return "".join(o)


ERGO_CSS = """
.orf .gl2{stroke:var(--line2);stroke-width:1.5}
.orf .eq{fill:var(--strong);fill-opacity:.08;stroke:var(--line2);stroke-width:1.4}
.orf .eqa{fill:var(--acc)}
.orf .body{fill:none;stroke:var(--strong);stroke-width:9;stroke-linecap:round;stroke-linejoin:round}
.orf .head{fill:var(--strong)}
.orf .jt{fill:var(--acc)}
.orf .ref{stroke:var(--acc-t);stroke-width:1.2;stroke-dasharray:6 6}
.orf .trunk{animation:erTrunk 9s ease-in-out infinite}
.orf .neck{animation:erNeck 9s ease-in-out infinite}
@keyframes erTrunk{0%,12%{transform:rotate(8deg)}38%,50%{transform:rotate(24deg)}76%,88%{transform:rotate(42deg)}100%{transform:rotate(8deg)}}
@keyframes erNeck{0%,12%{transform:rotate(5deg)}38%,50%{transform:rotate(15deg)}76%,88%{transform:rotate(28deg)}100%{transform:rotate(5deg)}}
.orf .risk{display:grid;grid-template-columns:repeat(3,1fr);gap:4px}
.orf .risk span{height:8px;border-radius:2px;background:var(--line)}
.orf .risk span:nth-child(1){animation:rk1 9s infinite}.orf .risk span:nth-child(2){animation:rk2 9s infinite}.orf .risk span:nth-child(3){animation:rk3 9s infinite}
@keyframes rk1{0%,100%{background:var(--acc);opacity:.45}}
@keyframes rk2{0%,30%{background:var(--line)}38%,100%{background:var(--acc);opacity:.7}}
@keyframes rk3{0%,66%{background:var(--line)}76%,92%{background:var(--acc);opacity:1}100%{background:var(--line)}}
.orf .rlab{position:relative;height:24px}
.orf .rlab b{position:absolute;left:0;top:0;font:600 20px 'IBM Plex Mono',monospace;opacity:0}
.orf .rlab b:nth-child(1){animation:rl1 9s infinite}.orf .rlab b:nth-child(2){animation:rl2 9s infinite}.orf .rlab b:nth-child(3){animation:rl3 9s infinite;color:var(--acc-t)}
@keyframes rl1{0%,30%{opacity:1}34%,96%{opacity:0}100%{opacity:1}}
@keyframes rl2{0%,30%{opacity:0}34%,62%{opacity:1}66%,100%{opacity:0}}
@keyframes rl3{0%,62%{opacity:0}66%,94%{opacity:1}98%,100%{opacity:0}}
@media (prefers-reduced-motion:reduce){.orf .rlab b:nth-child(1){opacity:1}}
"""


def ergo_fig():
    return f'''<div class="orf">
      <div class="stage">{ergo_svg()}<div class="tagl">AUTO-RUNS · SIDE VIEW · TRUNK AND NECK BEND FURTHER, RISK RISES</div></div>
      <div class="dash">
        <div class="ft">FIG. C · OPTION 5</div>
        <h3>Sewing operator posture</h3>
        <div class="live">POSTURE RISK</div>
        <div class="risk"><span></span><span></span><span></span></div>
        <div class="rlab"><b>LOW</b><b>MEDIUM</b><b>HIGH</b></div>
        <div class="kp">
          <div><span class="k">TRUNK FLEXION</span><b>8° → 42°</b></div>
          <div><span class="k">NECK FLEXION</span><b>5° → 28°</b></div>
        </div>
        <div class="nt">Linked to the WMSD risk paper on garment sewing operators: the more the operator bends, the higher the musculoskeletal risk. Demo values.</div>
      </div>
    </div>'''


# ---------------- footer: green factory scene ----------------
def footer_scene(dark=True):
    leaf = GREEN_D if dark else GREEN_L
    s, ox, oy = 34, 40, 178

    def O(x, y, z):  # oblique projection: x right, z up, y goes back and up
        return (ox + x * s + y * s * 0.55, oy - z * s - y * s * 0.32)

    def ob(x0, x1, y0, y1, z0, z1, top="ft", front="fl", side="fr"):
        f = [O(x0, y0, z0), O(x1, y0, z0), O(x1, y0, z1), O(x0, y0, z1)]
        t = [O(x0, y0, z1), O(x1, y0, z1), O(x1, y1, z1), O(x0, y1, z1)]
        r = [O(x1, y0, z0), O(x1, y1, z0), O(x1, y1, z1), O(x1, y0, z1)]
        return poly(f, front) + poly(r, side) + poly(t, top)

    o = ['<svg class="fscene" viewBox="0 0 1160 200" preserveAspectRatio="xMidYMax meet" role="img" '
         'aria-label="Green factory: solar roof, wind turbines, conveyor and a truck moving">']
    o.append(poly([O(-2, -1.6, 0), O(32, -1.6, 0), O(32, 4, 0), O(-2, 4, 0)], "floor"))

    def tree(x, y, h=1.6, r=0.55):
        bx, by = O(x, y, 0)
        cx, cy = O(x, y, h)
        return (f'<line x1="{bx:.1f}" y1="{by:.1f}" x2="{cx:.1f}" y2="{cy:.1f}" stroke="var(--line2)" stroke-width="2"/>'
                f'<circle cx="{cx:.1f}" cy="{cy-4:.1f}" r="{r*s:.1f}" fill="{leaf}" fill-opacity=".55" stroke="{leaf}" stroke-width="1.2"/>')

    o.append(tree(0, 2.5) + tree(1.0, 1.2, 1.3, 0.45))
    # factory with saw-tooth solar roof
    o.append(ob(2, 9.5, 0, 3, 0, 2.0))
    for k in range(3):
        x0 = 2 + k * 2.5
        a, b, c = O(x0, 0, 2.0), O(x0 + 2.5, 0, 2.0), O(x0 + 2.5, 0, 3.0)
        o.append(poly([a, b, c], "fl"))
        panel = [O(x0, 0, 2.0), O(x0 + 2.5, 0, 3.0), O(x0 + 2.5, 3, 3.0), O(x0, 3, 2.0)]
        o.append(poly(panel, f"sol sol{k}"))
    dx, dy = O(4.0, 0, 0)
    o.append(f'<rect x="{dx:.1f}" y="{dy-1.2*s:.1f}" width="{1.2*s:.1f}" height="{1.2*s:.1f}" class="door"/>')
    # conveyor to the warehouse
    o.append(ob(9.5, 13, 1.0, 1.8, 0.5, 0.75, "belt", "fl", "fr"))
    crate = ob(-0.3, 0.3, 0, 0.6, 0, 0.5, "at", "al", "ar").replace(f"{ox}", f"{ox}")
    pa, pb = O(9.6, 1.1, 0.75), O(12.6, 1.1, 0.75)
    crate0 = []
    for x, y, z in [(-0.3, 0, 0), (0.3, 0, 0), (0.3, 0, 0.5), (-0.3, 0, 0.5)]:
        crate0.append((x * s + y * s * 0.55, -z * s - y * s * 0.32))
    top0 = [(-0.3 * s, -0.5 * s), (0.3 * s, -0.5 * s), (0.3 * s + 0.6 * s * 0.55, -0.5 * s - 0.6 * s * 0.32), (-0.3 * s + 0.6 * s * 0.55, -0.5 * s - 0.6 * s * 0.32)]
    crate_svg = poly(crate0, "al") + poly(top0, "at")
    for k in range(3):
        o.append(f'<g>{crate_svg}<animateMotion dur="4.5s" begin="-{k*1.5}s" repeatCount="indefinite" '
                 f'path="M{pa[0]:.1f},{pa[1]:.1f} L{pb[0]:.1f},{pb[1]:.1f}"/></g>')
    # warehouse / dock
    o.append(ob(13, 17, 0, 3, 0, 1.7))
    wx, wy = O(14.2, 0, 0)
    o.append(f'<rect x="{wx:.1f}" y="{wy-1.1*s:.1f}" width="{1.5*s:.1f}" height="{1.1*s:.1f}" class="door"/>')
    o.append(tree(18.2, 2.2) + tree(19.2, 1.0, 1.3, 0.45))
    # wind turbines
    for k, x in enumerate((22.5, 26.5)):
        bx, by = O(x, 2, 0)
        hx, hy = O(x, 2, 3.6)
        L = 1.35 * s
        blades = "".join(
            f'<path d="M{hx:.1f},{hy:.1f} L{hx + L*math.cos(math.radians(a)):.1f},{hy + L*math.sin(math.radians(a)):.1f}" />'
            for a in (-90, 30, 150))
        o.append(f'<line x1="{bx:.1f}" y1="{by:.1f}" x2="{hx:.1f}" y2="{hy:.1f}" stroke="var(--strong)" stroke-opacity=".45" stroke-width="3"/>'
                 f'<g class="blade b{k}" style="transform-origin:{hx:.1f}px {hy:.1f}px">{blades}</g>'
                 f'<circle cx="{hx:.1f}" cy="{hy:.1f}" r="4" fill="var(--acc)"/>')
    o.append(tree(29.5, 2.4) + tree(30.6, 1.1, 1.3, 0.45))
    # road + truck
    ra, rb = O(-2, -1.0, 0), O(32, -1.0, 0)
    o.append(f'<line class="road" x1="{ra[0]:.1f}" y1="{ra[1]:.1f}" x2="{rb[0]:.1f}" y2="{rb[1]:.1f}"/>')
    tr = (f'<rect x="0" y="-26" width="58" height="26" class="tk"/><rect x="60" y="-18" width="20" height="18" class="tkc"/>'
          f'<circle cx="12" cy="2" r="5" class="wh"/><circle cx="44" cy="2" r="5" class="wh"/><circle cx="70" cy="2" r="5" class="wh"/>')
    o.append(f'<g>{tr}<animateMotion dur="16s" repeatCount="indefinite" path="M{ra[0]-100:.1f},{ra[1]-4:.1f} L{rb[0]+20:.1f},{rb[1]-4:.1f}"/></g>')
    o.append("</svg>")
    return "".join(o)


NET_CSS = """
.orf .route{stroke:var(--acc-t);stroke-width:1.6;stroke-dasharray:7 6;stroke-opacity:.75;animation:beltMove 1.4s linear infinite}
.orf .stage .prsvg{max-width:520px;margin:0 auto}
.hcy .hsv .prsvg{max-width:380px;margin:0 auto}
"""

SCENE_CSS = """
.fscene{display:block;width:100%;height:auto;margin-bottom:6px}
.fscene polygon.ft{fill:var(--strong);fill-opacity:.12;stroke:var(--line2);stroke-width:1}
.fscene polygon.fl{fill:var(--strong);fill-opacity:.06;stroke:var(--line2);stroke-width:1}
.fscene polygon.fr{fill:var(--strong);fill-opacity:.09;stroke:var(--line2);stroke-width:1}
.fscene polygon.at{fill:var(--acc);fill-opacity:.9}.fscene polygon.al{fill:var(--acc);fill-opacity:.6}
.fscene polygon.belt{fill:var(--strong);fill-opacity:.2;stroke:var(--line2)}
.fscene polygon.floor{fill:none;stroke:none}
.fscene .sol{fill:var(--acc);fill-opacity:.28;stroke:var(--acc);stroke-opacity:.7;stroke-width:1;animation:solGlint 6s ease-in-out infinite}
.fscene .sol1{animation-delay:.6s}.fscene .sol2{animation-delay:1.2s}
@keyframes solGlint{0%,70%,100%{fill-opacity:.28}80%{fill-opacity:.75}}
.fscene .door{fill:var(--strong);fill-opacity:.12;stroke:var(--line2)}
.fscene .blade path{stroke:var(--strong);stroke-width:3.5;stroke-linecap:round;stroke-opacity:.8}
.fscene .blade{animation:bladeSpin 5s linear infinite}.fscene .b1{animation-duration:6.5s}
@keyframes bladeSpin{to{transform:rotate(360deg)}}
.fscene .road{stroke:var(--line2);stroke-width:1.5;stroke-dasharray:14 10;animation:beltMove2 1.2s linear infinite}
@keyframes beltMove2{to{stroke-dashoffset:-24}}
.fscene .tk{fill:var(--acc);fill-opacity:.85}.fscene .tkc{fill:var(--strong);fill-opacity:.55}.fscene .wh{fill:var(--bg);stroke:var(--strong);stroke-width:2}
@media (prefers-reduced-motion:reduce){.fscene *{animation:none!important}}
"""


# ---------------- hero figure rotation: A -> B -> C ----------------
def hero_cycle(gear_html):
    fig_b = factory_svg()
    fig_c = printer_svg(compact=True)
    seq = [("A", "SPUR GEAR PAIR", 32.0, gear_html, "2 turns of the pinion"),
           ("B", "SEWING LINE", 2 * 12.4, f'<div class="hcl">FIG. B · SEWING LINE SIMULATION</div><div class="hsv">{fig_b}</div>', "2 full part cycles"),
           ("C", "3D PRINTING", 2 * PR_T, f'<div class="hcl">FIG. C · FDM 3D PRINTING</div><div class="hsv">{fig_c}</div>', "2 full prints")]
    total = sum(x[2] for x in seq)
    fade = 1.2
    css, slides, prog, t = [], [], [], 0.0
    for i, (k, name, d, html, note) in enumerate(seq):
        a = t / total * 100
        b = (t + fade) / total * 100
        c = (t + d) / total * 100
        e = min(100, (t + d + fade) / total * 100)
        if i == 0:
            kf = f"0%{{opacity:1}}{c:.2f}%{{opacity:1}}{e:.2f}%{{opacity:0}}{100-fade/total*100:.2f}%{{opacity:0}}100%{{opacity:1}}"
        else:
            kf = f"0%,{a:.2f}%{{opacity:0}}{b:.2f}%,{c:.2f}%{{opacity:1}}{e:.2f}%,100%{{opacity:0}}"
        css.append(f"@keyframes hcS{i}{{{kf}}}.hcy .sl{i}{{animation:hcS{i} {total:.1f}s linear infinite}}")
        css.append(f"@keyframes hcP{i}{{0%,{a:.2f}%{{transform:scaleX(0)}}{c:.2f}%{{transform:scaleX(1)}}{min(100,c+0.01):.2f}%,100%{{transform:scaleX(0)}}}}"
                   f".hcy .pg{i} i{{animation:hcP{i} {total:.1f}s linear infinite}}")
        slides.append(f'<div class="sl sl{i}">{html}</div>')
        prog.append(f'<div class="pg pg{i}"><span>FIG. {k} · {name}</span><em>{d:.0f} s · {note}</em><b><i></i></b></div>')
        t += d
    style = "<style>" + "".join(css) + "</style>"
    return style, f'''<div class="hcy">
        <div class="stg">{"".join(slides)}</div>
        <div class="pgs">{"".join(prog)}</div>
      </div>'''


HERO_CSS = """
.hcy{display:grid;grid-template-columns:520px 1fr;gap:24px;align-items:center}
.hcy .stg{position:relative;height:430px}
.hcy .sl{position:absolute;inset:0;opacity:0}
.hcy .sl0{opacity:1}
.hcy .hcl{font:600 12px 'IBM Plex Mono',monospace;letter-spacing:.1em;color:var(--acc-t);padding:18px 18px 0}
.hcy .hsv{padding:6px 10px}
.hcy .hsv svg{width:100%;height:auto;display:block;overflow:visible}
.hcy .hsv text{display:none}
.hcy .pgs{display:flex;flex-direction:column;gap:14px}
.hcy .pg{display:grid;grid-template-columns:1fr;gap:6px}
.hcy .pg span{font:600 12.5px 'IBM Plex Mono',monospace;letter-spacing:.1em;color:var(--strong)}
.hcy .pg em{font-style:normal;font-size:13.5px;color:var(--muted)}
.hcy .pg b{display:block;height:4px;border-radius:999px;background:var(--line);overflow:hidden}
.hcy .pg b i{display:block;height:100%;background:var(--acc);transform-origin:left;transform:scaleX(0)}
@media (prefers-reduced-motion:reduce){.hcy .sl{animation:none!important;opacity:0}.hcy .sl0{opacity:1}}
@media (max-width:760px){.hcy{grid-template-columns:1fr}.hcy .stg{height:330px}}
"""
