#!/usr/bin/env python3
"""Round 3 figures (Zaid 2026-11-17):
- QC inspection line + live I-chart  (hero FIG. C)
- optimization landscape v2, filled surface (hero FIG. A)
- sewing line v2, realistic stations (placement open)
- FDM printer v2, Ender-3 style, prints a spur gear (Projects page header)
- footer factory v2, sits beside the revision table
- hero rotation v2: landscape -> gear -> QC
All pure SVG + CSS/SMIL so they run on the canvas without JavaScript."""
import math
import statistics as st
from or_figs import iso, poly, box, f as land_f, descent, C30, S30

PASS, FAIL = "#3FB47A", "#E0524A"          # semantic colours, same in every theme


def pct(t, T):
    return f"{max(0.0, min(100.0, t / T * 100)):.3f}%"


def defs_metal(uid):
    return (f'<defs><linearGradient id="mt{uid}" x1="0" x2="1">'
            f'<stop offset="0" stop-color="#6F7682"/><stop offset=".35" stop-color="#D9DEE5"/>'
            f'<stop offset=".6" stop-color="#9AA2AE"/><stop offset="1" stop-color="#5B626D"/></linearGradient>'
            f'<radialGradient id="mtop{uid}"><stop offset="0" stop-color="#EEF1F5"/><stop offset="1" stop-color="#9AA2AE"/></radialGradient></defs>')


def cylinder(r, h, s, uid, extra=""):
    rx, ry, H = 1.2247 * r * s, 0.7071 * r * s, h * s
    body = (f'<path fill="url(#mt{uid})" stroke="rgba(0,0,0,.35)" stroke-width=".6" '
            f'd="M{-rx:.1f},0 A{rx:.1f},{ry:.1f} 0 0 0 {rx:.1f},0 L{rx:.1f},{-H:.1f} A{rx:.1f},{ry:.1f} 0 0 0 {-rx:.1f},{-H:.1f} Z"/>')
    top = f'<ellipse cx="0" cy="{-H:.1f}" rx="{rx:.1f}" ry="{ry:.1f}" fill="url(#mtop{uid})" stroke="rgba(0,0,0,.3)" stroke-width=".6"/>'
    return body + top + extra


# =====================================================================
# QC: inspection line with laser gauge, reject pusher and a live I-chart
# =====================================================================
QC_T = 12.0                 # one full cycle (6 parts); 2 cycles = 24 s hero slot
QC_N = 6
QC_GAP = QC_T / QC_N        # a new part every 2 s
QC_TRAVEL = 10.0            # seconds from infeed to outfeed
QC_X0, QC_X1 = -0.6, 19.4   # belt run (units)
QC_GAUGE, QC_PUSH = 7.0, 11.0
GOOD = [25.008, 24.988, 25.014, 24.993, 25.004]    # in-control diameters, in inspection order
BAD_VALUE = 25.062                                    # chipped tool -> oversize
BAD_SLOT = 3                                          # 4th point on the chart


def _local(x):              # local time when a part reaches belt position x
    return (x - QC_X0) / (QC_X1 - QC_X0) * QC_TRAVEL


def _doc(local, k):         # document time when part k is at that local time
    return (local - QC_GAP * k) % QC_T


def qc_timeline():
    t_insp = {k: _doc(_local(QC_GAUGE), k) for k in range(QC_N)}
    order = sorted(range(QC_N), key=lambda k: t_insp[k])
    return t_insp, order


QC_BAD = qc_timeline()[1][BAD_SLOT]       # the part that reaches the gauge 4th


def qc_stats():
    t_insp, order = qc_timeline()
    j_bad = BAD_SLOT
    vals = GOOD[:j_bad] + [BAD_VALUE] + GOOD[j_bad:]
    good = list(GOOD)
    mu, sd = st.mean(good), st.stdev(good)
    ucl, lcl = mu + 3 * sd, mu - 3 * sd
    usl, lsl = 25.05, 24.95
    cpk = min(usl - mu, mu - lsl) / (3 * sd)
    return dict(vals=vals, j_bad=j_bad, mu=mu, sd=sd, ucl=ucl, lcl=lcl, usl=usl, lsl=lsl, cpk=cpk,
                t_insp=t_insp, order=order)


def qc_scene(uid="q", hero=False):
    s, ox, oy = 26, 250, 120
    P = lambda x, y, z: iso(x, y, z, s, ox, oy)
    o = [f'<svg class="qcs" viewBox="0 0 820 400" role="img" aria-label="Inspection line: a laser gauge measures every shaft and a pusher rejects the oversize one">',
         defs_metal(uid)]
    o.append(poly([P(-2, -4, 0), P(21.5, -4, 0), P(21.5, 4.5, 0), P(-2, 4.5, 0)], "floor"))
    # pusher cylinder behind the belt
    o.append(box(10.5, 11.5, -3.2, -1.0, 0.7, 1.5, P))
    o.append(box(10.75, 11.25, -1.0, -0.8, 0.9, 1.3, P))
    # gauge gantry: back post
    o.append(box(6.8, 7.2, -1.6, -1.2, 0, 3.6, P))
    # belt
    o.append(box(QC_X0 - 0.6, QC_X1 + 0.4, -0.7, 0.7, 0, 0.7, P, "belt", "fl", "fr"))
    a, b = P(QC_X0 - 0.6, 0, 0.7), P(QC_X1 + 0.4, 0, 0.7)
    o.append(f'<line class="beltln" x1="{a[0]:.1f}" y1="{a[1]:.1f}" x2="{b[0]:.1f}" y2="{b[1]:.1f}"/>')
    # reject chute + bin in front of the belt
    o.append(poly([P(10.4, 0.7, 0.65), P(11.6, 0.7, 0.65), P(11.6, 1.8, 0.2), P(10.4, 1.8, 0.2)], "chute"))
    o.append(box(9.9, 12.1, 1.8, 3.6, 0, 1.0, P, "bin", "binl", "binr"))
    rx_, ry_ = P(11.0, 3.6, 0)
    o.append(f'<text x="{rx_-34:.1f}" y="{ry_+20:.1f}" class="fail">REJECT</text>')
    # accepted tote at the end
    o.append(box(QC_X1 + 0.5, QC_X1 + 2.3, -1.0, 1.0, 0, 0.9, P, "bin", "binl", "binr"))
    ax_, ay_ = P(QC_X1 + 1.4, 1.0, 0)
    o.append(f'<text x="{ax_-30:.1f}" y="{ay_+20:.1f}" class="pass">ACCEPTED</text>')
    # parts (machined shafts)
    t_insp, order = qc_timeline()
    pa, pb = P(QC_X0, 0, 0.7), P(QC_X1, 0, 0.7)
    l_push = _local(QC_PUSH) / QC_T
    l_end = QC_TRAVEL / QC_T
    pp = P(QC_PUSH, 0, 0.7)
    pchute = P(QC_PUSH, 1.9, 0.25)
    pbin = P(QC_PUSH, 2.7, 0.2)
    for k in range(QC_N):
        bad = k == QC_BAD
        mark = ""
        if bad:
            ti = _local(QC_GAUGE) / QC_T
            mark = (f'<ellipse cx="0" cy="{-0.95*s:.1f}" rx="{0.62*s:.1f}" ry="{0.36*s:.1f}" fill="none" stroke="{FAIL}" stroke-width="2.4" opacity="0">'
                    f'<animate attributeName="opacity" dur="{QC_T}s" begin="-{QC_GAP*k:.2f}s" repeatCount="indefinite" '
                    f'keyTimes="0;{ti:.4f};{ti+0.005:.4f};1" values="0;0;1;1"/></ellipse>')
        part = cylinder(0.32, 0.9, s, uid, mark)
        if not bad:
            mot = (f'<animateMotion dur="{QC_T}s" begin="-{QC_GAP*k:.2f}s" repeatCount="indefinite" calcMode="linear" '
                   f'keyTimes="0;{l_end:.4f};1" keyPoints="0;1;1" path="M{pa[0]:.1f},{pa[1]:.1f} L{pb[0]:.1f},{pb[1]:.1f}"/>')
            vis = (f'<animate attributeName="opacity" dur="{QC_T}s" begin="-{QC_GAP*k:.2f}s" repeatCount="indefinite" '
                   f'keyTimes="0;0.02;{l_end:.4f};{l_end+0.02:.4f};1" values="0;1;1;0;0"/>')
        else:
            t1, t2, t3 = l_push, l_push + 0.6 / QC_T, l_push + 1.1 / QC_T
            path = (f"M{pa[0]:.1f},{pa[1]:.1f} L{pp[0]:.1f},{pp[1]:.1f} L{pchute[0]:.1f},{pchute[1]:.1f} L{pbin[0]:.1f},{pbin[1]:.1f}")
            L1 = math.dist(pa, pp); L2 = math.dist(pp, pchute); L3 = math.dist(pchute, pbin); Lt = L1 + L2 + L3
            mot = (f'<animateMotion dur="{QC_T}s" begin="-{QC_GAP*k:.2f}s" repeatCount="indefinite" calcMode="linear" '
                   f'keyTimes="0;{t1:.4f};{t2:.4f};{t3:.4f};1" keyPoints="0;{L1/Lt:.4f};{(L1+L2)/Lt:.4f};1;1" path="{path}"/>')
            vis = (f'<animate attributeName="opacity" dur="{QC_T}s" begin="-{QC_GAP*k:.2f}s" repeatCount="indefinite" '
                   f'keyTimes="0;0.02;{t3:.4f};{t3+0.03:.4f};1" values="0;1;1;0;0"/>')
        o.append(f'<g opacity="0">{part}{mot}{vis}</g>')
    # pusher rod (fires when the bad part arrives)
    t_fire = _doc(_local(QC_PUSH), QC_BAD)
    dx, dy = -C30 * s * 1.4, S30 * s * 1.4      # +y direction on screen, 1.4 units
    o.append(f'<g class="rod" style="--dx:{dx:.1f}px;--dy:{dy:.1f}px">{box(10.8, 11.2, -0.85, -0.55, 0.95, 1.25, P, "at", "al", "ar")}</g>')
    # gauge gantry: front post, beam, sensor head, laser sheet
    o.append(box(6.8, 7.2, 1.2, 1.6, 0, 3.6, P))
    o.append(box(6.7, 7.3, -1.6, 1.6, 3.6, 4.0, P))
    o.append(box(6.75, 7.25, -0.4, 0.4, 3.0, 3.6, P, "at", "al", "ar"))
    beam = [P(7.0, -0.35, 3.0), P(7.0, 0.35, 3.0), P(7.0, 0.45, 0.7), P(7.0, -0.45, 0.7)]
    o.append(poly(beam, "laser"))
    lx, ly = P(7.0, -1.4, 4.4)
    o.append(f'<circle class="lampok" cx="{lx:.1f}" cy="{ly:.1f}" r="6"/><circle class="lampbad" cx="{lx:.1f}" cy="{ly:.1f}" r="6"/>')
    if not hero:
        gx, gy = P(7.0, -1.6, 4.6)
        o.append(f'<text x="{gx-60:.1f}" y="{gy-12:.1f}" class="s">LASER GAUGE · Ø</text>')
        px_, py_ = P(11.0, -3.2, 1.6)
        o.append(f'<text x="{px_-40:.1f}" y="{py_-10:.1f}">PUSHER</text>')
        ix, iy = P(QC_X0 - 0.6, 0.9, 0)
        o.append(f'<text x="{ix-40:.1f}" y="{iy+20:.1f}">INFEED</text>')
    o.append("</svg>")
    return "".join(o), t_fire


def qc_chart(hero=False):
    S = qc_stats()
    W, H = 820, 210 if not hero else 300      # taller in the hero so limit labels never touch
    x0, x1, y0, y1 = 30, W - 150, 34, H - 34
    vmin, vmax = 24.94, 25.07
    Y = lambda v: y1 - (v - vmin) / (vmax - vmin) * (y1 - y0)
    X = lambda j: x0 + 18 + j * (x1 - x0 - 36) / (QC_N - 1)
    o = [f'<svg class="qcc" viewBox="0 0 {W} {H}" role="img" aria-label="Individuals control chart of shaft diameter">',
         f'<rect class="cbg" x="0" y="0" width="{W}" height="{H}" rx="10"/>']
    for v, cls, lab in [(S["usl"], "spec", "USL 25.05"), (S["lsl"], "spec", "LSL 24.95"),
                        (S["ucl"], "lim", f"UCL {S['ucl']:.3f}"), (S["lcl"], "lim", f"LCL {S['lcl']:.3f}"),
                        (S["mu"], "cl", f"CL {S['mu']:.3f}")]:
        o.append(f'<line class="{cls}" x1="{x0}" y1="{Y(v):.1f}" x2="{x1}" y2="{Y(v):.1f}"/>'
                 f'<text x="{x1+8}" y="{Y(v)+4:.1f}" class="{cls}t">{lab}</text>')
    o.append(f'<rect class="band" x="{x0}" y="{Y(S["ucl"]):.1f}" width="{x1-x0}" height="{Y(S["lcl"])-Y(S["ucl"]):.1f}"/>')
    o.append(f'<line class="ax" x1="{x0}" y1="{y0-6}" x2="{x0}" y2="{y1}"/><line class="ax" x1="{x0}" y1="{y1}" x2="{x1}" y2="{y1}"/>')
    o.append(f'<text class="ttl" x="{x0}" y="{y0-12}">I-CHART · SHAFT Ø (mm)</text>'
             + ("" if hero else f'<text x="{x1}" y="{H-8}" text-anchor="end">PART SEQUENCE →</text>'))
    tj = [S["t_insp"][k] for k in S["order"]]
    clear = 0.6
    css = []
    for j, v in enumerate(S["vals"]):
        t = tj[j]
        bad = j == S["j_bad"]
        kf = (f"0%,{pct(clear, QC_T)}{{opacity:1}}{pct(clear + 0.05, QC_T)},{pct(t, QC_T)}{{opacity:0}}"
              f"{pct(t + 0.15, QC_T)},100%{{opacity:1}}")
        css.append(f"@keyframes qp{j}{{{kf}}}.qcc .p{j}{{animation:qp{j} {QC_T}s linear infinite}}")
        seg = ""
        if j > 0:
            seg = f'<line class="ln" x1="{X(j-1):.1f}" y1="{Y(S["vals"][j-1]):.1f}" x2="{X(j):.1f}" y2="{Y(v):.1f}"/>'
        dot = f'<circle class="{"bad" if bad else "ok"}" cx="{X(j):.1f}" cy="{Y(v):.1f}" r="{6 if bad else 4.5}"/>'
        if bad:
            dot += (f'<circle class="ring" cx="{X(j):.1f}" cy="{Y(v):.1f}" r="12"/>'
                    f'<rect class="failbg" x="{X(j)+14:.1f}" y="{Y(v)-17:.1f}" width="214" height="22" rx="4"/>'
                    f'<text class="failt" x="{X(j)+22:.1f}" y="{Y(v)-2:.1f}">{v:.3f} mm · OUT OF CONTROL</text>')
        o.append(f'<g class="p{j}">{seg}{dot}</g>')
    o.append("</svg>")
    t_bad = tj[S["j_bad"]]
    return "".join(o), "".join(css), t_bad, S


QC_CSS_BASE = """
.orf .stage .qcc{margin-bottom:22px}
.orf polygon.chute{fill:var(--strong);fill-opacity:.18;stroke:var(--line2)}
.orf polygon.bin{fill:var(--strong);fill-opacity:.06;stroke:var(--line2)}
.orf polygon.binl{fill:var(--strong);fill-opacity:.13;stroke:var(--line2)}
.orf polygon.binr{fill:var(--strong);fill-opacity:.09;stroke:var(--line2)}
.orf polygon.laser{fill:#FF4B3E;fill-opacity:.0;stroke:none;animation:qcLaser 2s linear infinite}
.orf text.pass,.hcy text.pass{fill:#3FB47A}.orf text.fail,.hcy text.fail{fill:#E0524A}
.lampok{fill:#3FB47A;opacity:.25;animation:qcOk 2s linear infinite}
.lampbad{fill:#E0524A;opacity:0}
.qcc{display:block;width:100%;height:auto}
.qcc text{font:600 12px 'IBM Plex Mono',monospace;fill:var(--muted)}
.qcc .ax{stroke:var(--line2)}
.qcc .cbg{fill:var(--bg);fill-opacity:.0}
.hcy .qcc .cbg{fill-opacity:.82}
.qcc .spec{stroke:#E0524A;stroke-opacity:.38;stroke-dasharray:8 6}\n.qcc .band{fill:#3FB47A;fill-opacity:.07}\n.qcc text.ttl{fill:var(--body);letter-spacing:.08em}\n.qcc .failbg{fill:#E0524A;fill-opacity:.12;stroke:#E0524A;stroke-opacity:.5}
.qcc .lim{stroke:var(--strong);stroke-opacity:.45;stroke-dasharray:3 4}
.qcc .cl{stroke:var(--strong);stroke-opacity:.35}
.qcc .spect{fill:#E0524A;fill-opacity:.8}.qcc .limt,.qcc .clt{fill:var(--body)}
.qcc .ln{stroke:var(--strong);stroke-opacity:.45;stroke-width:1.6}
.qcc .ok{fill:var(--strong)}
.qcc .bad{fill:#E0524A}
.qcc .ring{fill:none;stroke:#E0524A;stroke-width:2;animation:qcRing 1.2s ease-out infinite}
.qcc text.failt{fill:#E0524A}
@keyframes qcRing{from{stroke-opacity:1}to{stroke-opacity:.15}}
.qcst{position:relative;height:22px}
.qcst b{position:absolute;left:0;top:0;font:600 13px 'IBM Plex Mono',monospace;letter-spacing:.08em;white-space:nowrap}
.qcst b.okc{color:#3FB47A}.qcst b.badc{color:#E0524A;opacity:0}
@media (prefers-reduced-motion:reduce){.qcc g{animation:none!important;opacity:1}.orf .rod,.lampok,.lampbad,.orf polygon.laser{animation:none!important}}
"""


def qc_css():
    _, css, t_bad, S = qc_chart()
    _, t_fire = qc_scene()
    T = QC_T
    insp0 = _doc(_local(QC_GAUGE), 0) % QC_GAP      # phase of every inspection
    out = [QC_CSS_BASE, css]
    out.append(f"@keyframes qcLaser{{0%,{pct(1.4,2)}{{fill-opacity:.06}}{pct(1.5,2)},{pct(1.75,2)}{{fill-opacity:.55}}{pct(1.9,2)},100%{{fill-opacity:.06}}}}"
               f".orf polygon.laser,.hcy polygon.laser{{animation-delay:{insp0-1.6:.2f}s}}")
    out.append(f"@keyframes qcOk{{0%{{opacity:.25}}10%{{opacity:1}}40%,100%{{opacity:.25}}}}.lampok{{animation-delay:{insp0:.2f}s}}")
    out.append(f"@keyframes qcBad{{0%,{pct(t_bad,T)}{{opacity:0}}{pct(t_bad+0.1,T)},{pct(t_bad+2.4,T)}{{opacity:1}}{pct(t_bad+2.6,T)},100%{{opacity:0}}}}"
               f".lampbad{{animation:qcBad {T}s linear infinite}}")
    out.append(f"@keyframes qcRod{{0%,{pct(t_fire-0.05,T)}{{transform:translate(0,0)}}{pct(t_fire+0.3,T)},{pct(t_fire+0.6,T)}{{transform:translate(var(--dx),var(--dy))}}"
               f"{pct(t_fire+1.1,T)},100%{{transform:translate(0,0)}}}}.orf .rod,.hcy .rod{{animation:qcRod {T}s linear infinite}}")
    out.append(f"@keyframes qcSb{{0%,{pct(t_bad,T)}{{opacity:0}}{pct(t_bad+0.1,T)},{pct(t_bad+3.4,T)}{{opacity:1}}{pct(t_bad+3.5,T)},100%{{opacity:0}}}}"
               f"@keyframes qcSo{{0%,{pct(t_bad,T)}{{opacity:1}}{pct(t_bad+0.1,T)},{pct(t_bad+3.4,T)}{{opacity:0}}{pct(t_bad+3.5,T)},100%{{opacity:1}}}}"
               f".qcst b.badc{{animation:qcSb {T}s linear infinite}}.qcst b.okc{{animation:qcSo {T}s linear infinite}}")
    return "\n".join(out)


def qc_fig():
    from or_figs4 import qc2_scene
    scene, _ = qc2_scene("q1")
    chart, _, _, S = qc_chart()
    return f'''<div class="orf">
      <div class="stage">{scene}<div class="qcleg"><span><i>1</i>Photo-eye (trigger)</span><span><i>2</i>Laser micrometer</span><span><i>3</i>Pneumatic pusher</span><span><i>4</i>NG tote (rejects)</span><span><i>5</i>OK tote (good parts)</span><span><i>6</i>HMI + stack light</span></div>{chart}<div class="tagl">AUTO-RUNS · ONE SHAFT EVERY 2 s · MEASURED, PLOTTED, SORTED</div></div>
      <div class="dash">
        <div class="ft">FIG. C · QUALITY CONTROL</div>
        <h3>Shaft inspection cell + SPC</h3>
        <div class="qcst"><b class="okc">● PROCESS IN CONTROL</b><b class="badc">● OUT OF CONTROL · NG</b></div>
        <div class="kp">
          <div><span class="k">NOMINAL Ø</span><b>25.00 mm</b></div>
          <div><span class="k">TOLERANCE</span><b>±0.05</b></div>
          <div><span class="k">Cpk</span><b class="a">{S["cpk"]:.2f}</b></div>
          <div><span class="k">THIS CYCLE</span><b>5 / 6 OK</b></div>
        </div>
        <div class="nt">A photo-eye triggers a through-beam laser micrometer as each turned shaft passes. Every diameter goes onto the individuals (I) control chart on the HMI. One shaft is oversize (25.062 mm): it breaks the control and spec limits, the stack light turns red and the pneumatic pusher sends it down the chute into the red NG tote. Good shafts reach the green OK tote. Demo data.</div>
      </div>
    </div>'''


# =====================================================================
# Optimization landscape v2: shaded surface instead of wireframe
# =====================================================================
LAND_T = 12.0               # one search cycle; 2 cycles = 24 s hero slot


def landscape2_svg(hero=False):
    th = math.radians(28)
    s, H, ox, oy = 240, 145, 430, 240

    def UV(x, y):
        return x * math.cos(th) - y * math.sin(th), x * math.sin(th) + y * math.cos(th)

    def P(x, y):
        u, v = UV(x, y)
        return ((u - v) * C30 * s + ox, (u + v) * S30 * s - land_f(x, y) * H + oy)

    N = 28
    g = [-1 + 2 * i / N for i in range(N + 1)]
    zs = [land_f(a, b) for a in g for b in g]
    lo, hi = min(zs), max(zs)
    quads = []
    for i in range(N):
        for j in range(N):
            xs = [(g[i], g[j]), (g[i + 1], g[j]), (g[i + 1], g[j + 1]), (g[i], g[j + 1])]
            zc = sum(land_f(x, y) for x, y in xs) / 4
            u, v = UV((g[i] + g[i + 1]) / 2, (g[j] + g[j + 1]) / 2)
            band = min(5, int((zc - lo) / (hi - lo + 1e-9) * 6))
            # simple light from top-left: compare heights across the quad
            shade = land_f(g[i], g[j]) - land_f(g[i + 1], g[j + 1])
            lit = "L" if shade > 0.01 else ("D" if shade < -0.01 else "")
            quads.append((u + v, [P(x, y) for x, y in xs], band, lit))
    quads.sort(key=lambda q: q[0])
    # hero: the surface's back corner rises to y = -53, so the viewBox starts higher and the figure never covers its title
    vb = "0 -64 860 584" if hero else "0 0 860 520"
    o = [f'<svg class="lsv" viewBox="{vb}" role="img" aria-label="Shaded 3D optimization landscape with three searches">']
    for _, pts, band, lit in quads:
        d = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
        o.append(f'<polygon class="ub" points="{d}"/><polygon class="q{band}{lit}" points="{d}"/>')
    starts = [(-0.95, 0.85), (0.95, -0.95), (0.98, 0.95)]
    runs = []
    for i, (sx, sy) in enumerate(starts):
        pts = descent(sx, sy)
        d = "M" + " L".join(f"{P(x, y)[0]:.1f},{P(x, y)[1]:.1f}" for x, y in pts[::4])
        runs.append((land_f(*pts[-1]), i, pts[-1], d))
    best = min(runs)[1]
    for fz, i, _, d in runs:
        o.append(f'<path class="trail{" g" if i == best else ""}" pathLength="1" d="{d}"/>')
    for fz, i, (ex, ey), d in runs:
        gcls = " g" if i == best else ""
        o.append(f'<circle class="ball{gcls}" r="8"><animateMotion dur="{LAND_T}s" repeatCount="indefinite" calcMode="spline" '
                 f'keyTimes="0;0.72;1" keyPoints="0;1;1" keySplines="0.42 0 0.58 1;0 0 1 1" path="{d}"/></circle>')
        px, py = P(ex, ey)
        lab = ("GLOBAL" if hero else "GLOBAL OPTIMUM") if i == best else ("LOCAL" if hero else "LOCAL MINIMUM")
        val = f"{fz:.2f}".replace("-", "\u2212")
        left = (i != best and px < 470 and not hero) or (hero and i != best and px > 560)
        tx, anc = (px - 8, "end") if left else (px + 8, "start")
        fh = (52 if i == best else (88 if i == 0 else 46)) if hero else 52
        if hero and i != best and i != 0:
            # hero: this label hangs BELOW its point; above, it ran into the other local search's end point
            o.append(f'<line class="flag" x1="{px:.1f}" y1="{py+10:.1f}" x2="{px:.1f}" y2="{py+40:.1f}"/>'
                     f'<text class="s fl" text-anchor="{anc}" x="{tx:.1f}" y="{py+58:.1f}">{lab} · f = {val}</text>')
        else:
            o.append(f'<line class="flag" x1="{px:.1f}" y1="{py-10:.1f}" x2="{px:.1f}" y2="{py-fh:.1f}"/>'
                     f'<text class="{"h" if i == best else "s"} fl" text-anchor="{anc}" x="{tx:.1f}" y="{py-fh+8:.1f}">{lab} · f = {val}</text>')
        if not hero:
            sx0, sy0 = P(*starts[i])
            o.append(f'<circle class="st0" cx="{sx0:.1f}" cy="{sy0:.1f}" r="4"/>'
                     f'<text class="fl" x="{sx0-18:.1f}" y="{sy0-12:.1f}">START {i+1}</text>')
    o.append("</svg>")
    return "".join(o), min(runs)[0]


LAND2_CSS = """
.lsv polygon{stroke:#FFFFFF;stroke-opacity:.60;stroke-width:.9}   /* white grid, option B (Zaid 2026-11-17) */
.lsv polygon.ub{fill:var(--bg);stroke:none}
.lsv .q0,.lsv .q0L,.lsv .q0D{fill:var(--acc);fill-opacity:.85}
.lsv .q1,.lsv .q1L,.lsv .q1D{fill:var(--acc);fill-opacity:.55}
.lsv .q2,.lsv .q2L,.lsv .q2D{fill:var(--acc);fill-opacity:.30}
.lsv .q3,.lsv .q3L,.lsv .q3D{fill:var(--strong);fill-opacity:.24}
.lsv .q4,.lsv .q4L,.lsv .q4D{fill:var(--strong);fill-opacity:.18}
.lsv .q5,.lsv .q5L,.lsv .q5D{fill:var(--strong);fill-opacity:.13}
.lsv [class$="L"]{filter:brightness(1.18)}
.lsv [class$="D"]{filter:brightness(.78)}
.lsv .ball{fill:var(--strong);stroke:var(--bg);stroke-width:2.5}
.lsv .ball.g{fill:var(--acc-t)}
.lsv .flag{stroke:var(--strong);stroke-width:1.4}
.lsv text.fl{paint-order:stroke;stroke:var(--bg);stroke-width:5px;stroke-linejoin:round}
.lsv .st0{fill:var(--bg);stroke:var(--strong);stroke-width:1.6}
.lsv .trail{animation-duration:12s!important}
"""


def landscape2_fig():
    svg, best = landscape2_svg()
    return f'''<div class="orf">
      <div class="stage"><div class="rock">{svg}</div><div class="tagl">AUTO-RUNS · ON THE REAL SITE, DRAG TO TURN, CLICK TO DROP A NEW START</div></div>
      <div class="dash">
        <div class="ft">FIG. A · OPTIMIZATION</div>
        <h3>Optimization landscape</h3>
        <div class="kp">
          <div><span class="k">METHOD</span><b style="font-size:15px">GRADIENT DESCENT</b></div>
          <div><span class="k">STARTS</span><b>3</b></div>
          <div><span class="k">BEST f</span><b class="a">{f"{best:.2f}".replace("-", "\u2212")}</b></div>
          <div><span class="k">STUCK IN LOCAL</span><b>2 of 3</b></div>
        </div>
        <div class="nt">The surface is a cost to minimise; low valleys are good. Three searches roll downhill from different starts. Two stop in a local valley, one reaches the global optimum. This is why OR uses multi-start and metaheuristics.</div>
      </div>
    </div>'''


# =====================================================================
# Sewing line v2: tables, machines, operators, garment bundles
# =====================================================================
SEW_OPS = [("S1", "SHOULDER JOIN", 21), ("S2", "SLEEVE ATTACH", 22), ("S3", "SIDE SEAM", 25), ("S4", "HEMMING", 24)]


def person(cx, cy, cz, P, hot=False):
    """Seated operator behind a table, facing +y (towards the viewer)."""
    o = box(cx - 0.45, cx + 0.45, cy - 0.45, cy + 0.45, cz, cz + 0.45, P)                 # stool
    o += box(cx - 0.5, cx + 0.5, cy - 0.3, cy + 0.3, cz + 0.45, cz + 1.8, P, "cloth", "clothl", "clothr")   # torso
    hx, hy = P(cx, cy, cz + 2.25)
    o += f'<circle class="headp" cx="{hx:.1f}" cy="{hy:.1f}" r="{0.36*27:.1f}"/>'
    return o


def sewing2_svg(hero=False):
    s, ox, oy = 27, 250, 150
    P = lambda x, y, z: iso(x, y, z, s, ox, oy)
    o = ['<svg class="sw2" viewBox="0 0 860 470" role="img" aria-label="Sewing line: four operators at sewing machines, garment bundles move on a conveyor">']
    o.append(poly([P(-2, -6, 0), P(23, -6, 0), P(23, 3.5, 0), P(-2, 3.5, 0)], "floor"))
    # floor tiles
    for x in range(-2, 24, 2):
        a, b = P(x, -6, 0), P(x, 3.5, 0)
        o.append(f'<line class="tile" x1="{a[0]:.1f}" y1="{a[1]:.1f}" x2="{b[0]:.1f}" y2="{b[1]:.1f}"/>')
    stations = [3, 8, 13, 18]
    # operators (furthest back)
    for i, c in enumerate(stations):
        o.append(person(c, -4.2, 0, P))
    # tables + machines + lamps
    for i, c in enumerate(stations):
        hot = i == 2
        o.append(box(c - 1.5, c + 1.5, -3.4, -1.2, 1.45, 1.6, P))                                   # table top
        for lx in (c - 1.4, c + 1.3):
            o.append(box(lx, lx + 0.12, -1.35, -1.23, 0, 1.45, P))                                  # front legs
        # industrial sewing machine: bed, pillar, arm, head
        o.append(box(c - 0.9, c + 0.9, -2.7, -1.9, 1.6, 1.85, P))
        o.append(box(c + 0.5, c + 0.85, -2.6, -2.0, 1.85, 2.9, P))
        o.append(box(c - 0.8, c + 0.85, -2.6, -2.0, 2.9, 3.25, P))
        o.append(box(c - 0.8, c - 0.45, -2.6, -2.0, 2.4, 2.9, P, *(("at", "al", "ar") if hot else ("ft", "fl", "fr"))))
        # fabric under the needle
        o.append(box(c - 1.1, c - 0.2, -2.0, -1.4, 1.6, 1.68, P, "fab", "fabl", "fabr"))
        px, py = P(c + 1.3, -3.2, 1.6)
        qx, qy = P(c + 1.3, -3.2, 3.9)
        o.append(f'<line x1="{px:.1f}" y1="{py:.1f}" x2="{qx:.1f}" y2="{qy:.1f}" stroke="var(--line2)" stroke-width="1.5"/>'
                 f'<circle class="lamp{" on" if hot else " ok"}" cx="{qx:.1f}" cy="{qy:.1f}" r="5"/>')
        if not hero:
            name = SEW_OPS[i][1]
            o.append(f'<text class="{"h" if hot else "s"}" x="{qx+10:.1f}" y="{qy+4:.1f}">{SEW_OPS[i][0]} · {name}</text>')
    # WIP bundles waiting on a cart in front of S3
    o.append(box(10.0, 11.6, 1.2, 2.4, 0.3, 0.45, P))
    for k, z in enumerate((0.45, 0.6, 0.75)):
        o.append(box(10.2, 11.3, 1.4, 2.2, z, z + 0.14, P, "fab", "fabl", "fabr"))
    if not hero:
        wx, wy = P(10.8, 2.6, 0)
        o.append(f'<text x="{wx-10:.1f}" y="{wy+16:.1f}">WIP · 3 BUNDLES</text>')
    # conveyor
    o.append(box(-1.5, 22, -0.6, 0.6, 0, 0.9, P, "belt", "fl", "fr"))
    a, b = P(-1.5, 0, 0.9), P(22, 0, 0.9)
    o.append(f'<line class="beltln" x1="{a[0]:.1f}" y1="{a[1]:.1f}" x2="{b[0]:.1f}" y2="{b[1]:.1f}"/>')
    bundle = box(-0.45, 0.45, -0.35, 0.35, 0, 0.18, lambda x, y, z: iso(x, y, z, s, 0, 0), "fab", "fabl", "fabr") + \
        box(-0.4, 0.4, -0.3, 0.3, 0.18, 0.32, lambda x, y, z: iso(x, y, z, s, 0, 0), "fab", "fabl", "fabr")
    start, end = P(-1.2, 0, 0.9), P(21.6, 0, 0.9)
    frac = lambda x: (x + 1.2) / 22.8
    seq, t = [(0.0, 0.0)], 0.0
    for c, dwell in zip(stations, [1.2, 1.25, 1.8, 1.4]):
        t += 1.3; seq.append((t, frac(c)))
        t += dwell; seq.append((t, frac(c)))
    t += 1.3; seq.append((t, 1.0))
    dur = t
    kt = ";".join(f"{x/dur:.4f}" for x, _ in seq)
    kp = ";".join(f"{p:.4f}" for _, p in seq)
    for k in range(6):
        o.append(f'<g>{bundle}<animateMotion dur="{dur:.2f}s" begin="-{k*dur/6:.2f}s" repeatCount="indefinite" '
                 f'calcMode="linear" keyTimes="{kt}" keyPoints="{kp}" path="M{start[0]:.1f},{start[1]:.1f} L{end[0]:.1f},{end[1]:.1f}"/></g>')
    if not hero:
        ix, iy = P(-1.5, 1.0, 0)
        o.append(f'<text x="{ix-50:.1f}" y="{iy+22:.1f}">CUT PANELS IN</text>')
        ex, ey = P(22, 1.0, 0)
        o.append(f'<text x="{ex-20:.1f}" y="{ey+22:.1f}">T-SHIRTS OUT →</text>')
    o.append("</svg>")
    return "".join(o), dur


SEW2_CSS = """
.orf polygon.cloth,.hcy polygon.cloth{fill:var(--strong);fill-opacity:.30;stroke:var(--line2)}
.orf polygon.clothl,.hcy polygon.clothl{fill:var(--strong);fill-opacity:.18;stroke:var(--line2)}
.orf polygon.clothr,.hcy polygon.clothr{fill:var(--strong);fill-opacity:.24;stroke:var(--line2)}
.orf polygon.fab,.hcy polygon.fab{fill:#5B7FB8;stroke:rgba(0,0,0,.25)}
.orf polygon.fabl,.hcy polygon.fabl{fill:#46679A;stroke:rgba(0,0,0,.25)}
.orf polygon.fabr,.hcy polygon.fabr{fill:#3D5C8C;stroke:rgba(0,0,0,.25)}
.headp{fill:var(--strong);fill-opacity:.55}
.orf .tile{stroke:var(--line);stroke-width:1}
.orf .lamp.ok{fill:#3FB47A;opacity:.85}
"""


def sewing2_fig():
    from or_figs4 import sewing5_svg
    svg = sewing5_svg()
    bars = "".join(f'<div class="r{" hot" if t == 25 else ""}"><span>{sn}</span><div class="bar"><i style="width:{t/25*100:.0f}%"></i></div><b>{t/25*100:.0f}%</b></div>'
                   for sn, _, t in SEW_OPS)
    return f'''<div class="orf">
      <div class="stage">{svg}<div class="tagl">AUTO-RUNS · ON THE REAL SITE, CLICK A STATION TO ADD AN OPERATOR</div></div>
      <div class="dash">
        <div class="ft">FIG. · SEWING LINE</div>
        <h3>T-shirt sewing line simulation</h3>
        <div class="kp">
          <div><span class="k">OUTPUT</span><b>144 pcs/h</b></div>
          <div><span class="k">LINE EFFICIENCY</span><b>92%</b></div>
          <div><span class="k">BOTTLENECK</span><b class="a">S3 · 25 s</b></div>
          <div><span class="k">WIP AT S3</span><b>3 bundles</b></div>
        </div>
        <div class="live">OPERATOR UTILIZATION</div>
        <div class="ut">{bars}</div>
        <div class="nt">Four operations, 92 s of sewing work per T-shirt. The side seam (S3, 25 s) is the slowest, so it sets the pace: 3600 / 25 = 144 pieces per hour, and bundles wait in front of it. Demo data.</div>
      </div>
    </div>'''


# =====================================================================
# FDM printer v2: Ender-3 style frame, bed-slinger motion, prints a gear
# =====================================================================
PR2_T, PR2_N, PR2_H = 14.0, 18, 0.12       # cycle s, layers, layer height (units)


def gear_outline(cx, cy, z, P, teeth=14, ro=2.0, rr=1.68, rb=0.55):
    pts = []
    for i in range(teeth):
        a0 = 2 * math.pi * i / teeth
        da = 2 * math.pi / teeth
        for a, r in ((a0, rr), (a0 + da * 0.18, ro), (a0 + da * 0.5, ro), (a0 + da * 0.68, rr)):
            pts.append(P(cx + r * math.cos(a), cy + r * math.sin(a), z))
    d = "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts) + " Z"
    bore = [P(cx + rb * math.cos(2 * math.pi * k / 20), cy + rb * math.sin(2 * math.pi * k / 20), z) for k in range(20)]
    d += " M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in bore) + " Z"
    return d


def printer2_svg(uid="p"):
    s, ox, oy = 24, 230, 330
    P = lambda x, y, z: iso(x, y, z, s, ox, oy)
    o = [f'<svg class="pr2" viewBox="0 0 520 520" role="img" aria-label="Ender-3 style printer printing a spur gear layer by layer">']
    sx, sy = P(4.5, 4.5, 0)
    o.append(f'<ellipse cx="{sx:.1f}" cy="{sy+20:.1f}" rx="190" ry="60" class="shdw"/>')
    o.append(box(0, 9, 0, 9, 0, 1.1, P, "fr1", "fr2", "fr3"))                       # base
    o.append(box(9.0, 9.9, 1.0, 5.0, 0.1, 1.5, P, "fr1", "fr2", "fr3"))             # PSU
    o.append(box(0.3, 0.9, 4.0, 4.9, 1.1, 11.5, P, "ext", "ext2", "ext3"))          # left Z extrusion
    # spool on top + holder
    o.append(box(0.3, 8.7, 4.0, 4.9, 11.5, 12.1, P, "ext", "ext2", "ext3"))         # top bar
    cx_, cz_ = 4.5, 13.6
    ring = [P(cx_ + 1.4 * math.cos(a), 4.45, cz_ + 1.4 * math.sin(a)) for a in [2 * math.pi * k / 36 for k in range(36)]]
    inner = [P(cx_ + 0.55 * math.cos(a), 4.45, cz_ + 0.55 * math.sin(a)) for a in [2 * math.pi * k / 36 for k in range(36)]]
    o.append(poly(ring, "spool"))
    o.append('<path class="spoolf" d="M' + " L".join(f"{x:.1f},{y:.1f}" for x, y in ring) + ' Z"/>')
    o.append(poly(inner, "spoolh"))
    # bed group: bed slinger moves along Y
    bed = box(1.0, 8.0, 1.0, 8.0, 1.5, 1.75, P, "bed", "bedl", "bedr")
    layers = []
    for i in range(PR2_N):
        z = 1.75 + (i + 1) * PR2_H
        layers.append(f'<path class="gl{i} gly" fill-rule="evenodd" d="{gear_outline(4.5, 4.5, z, P)}"/>')
    o.append(f'<g class="bedy">{bed}{"".join(layers)}</g>')
    # X gantry rises one layer at a time; head moves along X
    zb = 1.75 + 1.4
    head = (box(-0.6, 0.6, -0.5, 0.5, 0.25, 1.4, lambda x, y, z: iso(x, y, z, s, 0, 0), "hd", "hdl", "hdr")
            + poly([iso(-0.1, 0, 0.25, s, 0, 0), iso(0.1, 0, 0.25, s, 0, 0), iso(0, 0, 0, s, 0, 0)], "noz"))
    a, b = P(3.0, 4.45, zb - 1.3), P(6.0, 4.45, zb - 1.3)
    o.append(f'<g class="gz">{box(0.3, 8.7, 4.25, 4.65, zb, zb + 0.45, P, "ext", "ext2", "ext3")}'
             f'<g>{head}<animateMotion dur="0.9s" repeatCount="indefinite" keyTimes="0;0.5;1" keyPoints="0;1;0" '
             f'calcMode="spline" keySplines="0.45 0 0.55 1;0.45 0 0.55 1" path="M{a[0]:.1f},{a[1]:.1f} L{b[0]:.1f},{b[1]:.1f}"/></g></g>')
    o.append(box(8.1, 8.7, 4.0, 4.9, 1.1, 11.5, P, "ext", "ext2", "ext3"))          # right Z extrusion (front)
    # control box with screen on the front
    o.append(box(6.6, 8.6, 9.0, 9.4, 0.15, 1.0, P, "fr1", "scr", "fr3"))
    o.append("</svg>")
    return "".join(o)


def printer2_css():
    T, N, h = PR2_T, PR2_N, PR2_H * 24
    t_print = T * 0.78
    css = []
    for i in range(N):
        on = (i + 1) * t_print / N
        css.append(f"@keyframes pg{i}{{0%,{pct(on-0.02,T)}{{opacity:0}}{pct(on,T)},96%{{opacity:1}}100%{{opacity:0}}}}"
                   f".pr2 .gl{i}{{animation:pg{i} {T}s linear infinite}}")
    steps = []
    for i in range(N):
        t0 = i * t_print / N
        steps.append(f"{pct(t0,T)},{pct(t0 + t_print/N - 0.02,T)}{{transform:translateY({-i*h:.1f}px)}}")
    steps.append(f"{pct(t_print,T)},96%{{transform:translateY({-N*h:.1f}px)}}100%{{transform:translateY(0)}}")
    css.append("@keyframes pgz{" + "".join(steps) + "}" + f".pr2 .gz{{animation:pgz {T}s linear infinite}}")
    dx, dy = -C30 * 24 * 0.9, S30 * 24 * 0.9
    css.append(f"@keyframes bedy{{0%,100%{{transform:translate(0,0)}}50%{{transform:translate({dx:.1f}px,{dy:.1f}px)}}}}"
               ".pr2 .bedy{animation:bedy 1.3s ease-in-out infinite}")
    css.append(f"@keyframes pgBar{{0%{{transform:scaleX(0)}}78%,96%{{transform:scaleX(1)}}100%{{transform:scaleX(0)}}}}"
               f".prog2 i{{animation:pgBar {T}s linear infinite}}")
    css.append("""
.pr2{display:block;width:100%;height:auto;overflow:visible}
.pr2 .shdw{fill:#000;opacity:.28;filter:blur(10px)}
.pr2 .fr1{fill:#2A2E35;stroke:#151820;stroke-width:.8}.pr2 .fr2{fill:#1F232A;stroke:#151820;stroke-width:.8}.pr2 .fr3{fill:#262A31;stroke:#151820;stroke-width:.8}
.pr2 .ext{fill:#4A505A;stroke:#2B3038;stroke-width:.7}.pr2 .ext2{fill:#3A4049;stroke:#2B3038;stroke-width:.7}.pr2 .ext3{fill:#434952;stroke:#2B3038;stroke-width:.7}
.pr2 .bed{fill:#1C1F24;stroke:#5A606A;stroke-width:.8}.pr2 .bedl{fill:#8A919C}.pr2 .bedr{fill:#A7AEB8}
.pr2 .hd{fill:#3A3F47;stroke:#20242A;stroke-width:.7}.pr2 .hdl{fill:#2C3037}.pr2 .hdr{fill:#343940}
.pr2 .noz{fill:#C8A15A}
.pr2 .scr{fill:#0E2A3A;stroke:#5AA9D6;stroke-width:.8}
.pr2 .spool{fill:var(--acc);fill-opacity:.85;stroke:#1A1D22}
.pr2 .spoolf{fill:none;stroke:#FFFFFF;stroke-opacity:.35;stroke-width:1.2;stroke-dasharray:10 14;animation:spoolTurn 6s linear infinite}
@keyframes spoolTurn{to{stroke-dashoffset:-240}}
.pr2 .spoolh{fill:#1A1D22}
.pr2 .gly{fill:var(--acc);stroke:rgba(0,0,0,.35);stroke-width:.5}
@media (prefers-reduced-motion:reduce){.pr2 *{animation:none!important}.pr2 .gly{opacity:1}}
""")
    return "\n".join(css)


# =====================================================================
# Footer factory v2: sits in the empty space beside the revision table
# =====================================================================
def footer2_scene(dark=True):
    leaf, leaf2 = ("#3E9E6E", "#2F7D56") if dark else ("#3F9A6B", "#2C7A52")
    s, ox, oy = 26, 10, 176

    def O(x, y, z):
        return (ox + x * s + y * s * 0.55, oy - z * s - y * s * 0.32)

    def ob(x0, x1, y0, y1, z0, z1, f="wf", t="wt", r="ws"):
        F = [O(x0, y0, z0), O(x1, y0, z0), O(x1, y0, z1), O(x0, y0, z1)]
        T = [O(x0, y0, z1), O(x1, y0, z1), O(x1, y1, z1), O(x0, y1, z1)]
        R = [O(x1, y0, z0), O(x1, y1, z0), O(x1, y1, z1), O(x1, y0, z1)]
        return poly(F, f) + poly(R, r) + poly(T, t)

    W = 640
    o = [f'<svg class="fs2" viewBox="0 0 {W} 200" preserveAspectRatio="xMaxYMax meet" role="img" '
         'aria-label="Green factory with solar roof, wind turbines, conveyor and a delivery truck">',
         '<defs><linearGradient id="hill" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#3E9E6E" stop-opacity=".22"/>'
         '<stop offset="1" stop-color="#3E9E6E" stop-opacity="0"/></linearGradient>'
         '<linearGradient id="pv" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#2E4C78"/><stop offset="1" stop-color="#1B2E4D"/></linearGradient></defs>']
    # distant hills and ground
    o.append(f'<path d="M0 150 C80 112 150 118 220 136 C300 104 390 108 460 132 C520 116 590 112 {W} 128 L{W} 176 L0 176 Z" fill="url(#hill)"/>')
    o.append(poly([O(-1, -1.4, 0), O(24, -1.4, 0), O(24, 3.2, 0), O(-1, 3.2, 0)], "gnd"))
    # trees (back row)
    def tree(x, y, h=1.7, r=0.62):
        bx, by = O(x, y, 0); cx, cy = O(x, y, h)
        return (f'<ellipse cx="{bx+6:.1f}" cy="{by+2:.1f}" rx="{r*s*0.9:.1f}" ry="{r*s*0.25:.1f}" class="tsh"/>'
                f'<line x1="{bx:.1f}" y1="{by:.1f}" x2="{cx:.1f}" y2="{cy:.1f}" class="trunk"/>'
                f'<circle cx="{cx-r*s*0.35:.1f}" cy="{cy+2:.1f}" r="{r*s*0.75:.1f}" fill="{leaf2}"/>'
                f'<circle cx="{cx+r*s*0.3:.1f}" cy="{cy:.1f}" r="{r*s*0.8:.1f}" fill="{leaf2}"/>'
                f'<circle cx="{cx:.1f}" cy="{cy-r*s*0.45:.1f}" r="{r*s*0.85:.1f}" fill="{leaf}"/>')
    o.append(tree(0.4, 2.6) + tree(1.4, 1.5, 1.4, 0.5))
    # main hall with saw-tooth PV roof
    o.append(ob(2.2, 10.2, 0.4, 3.0, 0, 2.1))
    for k in range(9):                                                   # window band
        wx, wy = O(2.6 + k * 0.85, 0.4, 1.75)
        o.append(f'<rect x="{wx:.1f}" y="{wy:.1f}" width="{0.55*s:.1f}" height="{0.32*s:.1f}" class="win w{k%3}"/>')
    for k in range(2):                                                   # roll-up doors
        dx, dy = O(3.2 + k * 2.4, 0.4, 0)
        o.append(f'<rect x="{dx:.1f}" y="{dy-1.25*s:.1f}" width="{1.5*s:.1f}" height="{1.25*s:.1f}" class="door"/>')
        for r_ in range(1, 6):
            o.append(f'<line x1="{dx:.1f}" y1="{dy-r_*0.21*s:.1f}" x2="{dx+1.5*s:.1f}" y2="{dy-r_*0.21*s:.1f}" class="rib"/>')
    for k in range(4):                                                   # saw-tooth bays
        x0 = 2.2 + k * 2.0
        tri = [O(x0, 0.4, 2.1), O(x0 + 2.0, 0.4, 2.1), O(x0 + 2.0, 0.4, 2.9)]
        o.append(poly(tri, "wf"))
        pv = [O(x0, 0.4, 2.1), O(x0 + 2.0, 0.4, 2.9), O(x0 + 2.0, 3.0, 2.9), O(x0, 3.0, 2.1)]
        o.append(f'<polygon class="pv pv{k}" points="{" ".join(f"{a:.1f},{b:.1f}" for a, b in pv)}"/>')
        for c in range(1, 4):                                            # PV cell lines
            a = O(x0 + c * 0.5, 0.4, 2.1 + c * 0.2); b = O(x0 + c * 0.5, 3.0, 2.1 + c * 0.2)
            o.append(f'<line x1="{a[0]:.1f}" y1="{a[1]:.1f}" x2="{b[0]:.1f}" y2="{b[1]:.1f}" class="cell"/>')
        for c in range(1, 3):
            a = O(x0, 0.4 + c * 0.87, 2.1); b = O(x0 + 2.0, 0.4 + c * 0.87, 2.9)
            o.append(f'<line x1="{a[0]:.1f}" y1="{a[1]:.1f}" x2="{b[0]:.1f}" y2="{b[1]:.1f}" class="cell"/>')
    rr = [O(10.2, 0.4, 2.1), O(10.2, 3.0, 2.1), O(10.2, 3.0, 2.9), O(10.2, 0.4, 2.9)]
    o.append(poly(rr, "ws"))
    # conveyor bridge to the warehouse with moving crates
    o.append(ob(10.2, 13.0, 1.2, 1.9, 0.9, 1.1, "cvf", "cvt", "cvs"))
    pa, pb = O(10.3, 1.35, 1.1), O(12.6, 1.35, 1.1)
    crate = (f'<rect x="0" y="{-0.38*s:.1f}" width="{0.42*s:.1f}" height="{0.38*s:.1f}" class="crate"/>'
             f'<polygon points="0,{-0.38*s:.1f} {0.42*s:.1f},{-0.38*s:.1f} {0.42*s+0.35*s*0.55:.1f},{-0.38*s-0.35*s*0.32:.1f} {0.35*s*0.55:.1f},{-0.38*s-0.35*s*0.32:.1f}" class="cratet"/>')
    for k in range(3):
        o.append(f'<g>{crate}<animateMotion dur="4.2s" begin="-{k*1.4:.1f}s" repeatCount="indefinite" path="M{pa[0]:.1f},{pa[1]:.1f} L{pb[0]:.1f},{pb[1]:.1f}"/></g>')
    # warehouse with dock
    o.append(ob(13.0, 16.4, 0.4, 3.0, 0, 1.7))
    dx, dy = O(13.6, 0.4, 0)
    o.append(f'<rect x="{dx:.1f}" y="{dy-1.05*s:.1f}" width="{1.6*s:.1f}" height="{1.05*s:.1f}" class="door"/>')
    for r_ in range(1, 5):
        o.append(f'<line x1="{dx:.1f}" y1="{dy-r_*0.21*s:.1f}" x2="{dx+1.6*s:.1f}" y2="{dy-r_*0.21*s:.1f}" class="rib"/>')
    o.append(tree(17.0, 2.5) + tree(17.9, 1.3, 1.3, 0.48))
    # wind turbines (tapered towers, tapered blades)
    for k, (x, ht) in enumerate(((19.4, 4.9), (22.2, 4.4))):
        bx, by = O(x, 2.2, 0); hx, hy = O(x, 2.2, ht)
        o.append(f'<polygon class="tower" points="{bx-4:.1f},{by:.1f} {bx+4:.1f},{by:.1f} {hx+1.6:.1f},{hy:.1f} {hx-1.6:.1f},{hy:.1f}"/>')
        L = 1.55 * s
        blades = ""
        for a in (-90, 30, 150):
            ar = math.radians(a)
            tip = (hx + L * math.cos(ar), hy + L * math.sin(ar))
            n = (-math.sin(ar), math.cos(ar))
            blades += (f'<path d="M{hx + n[0]*3:.1f},{hy + n[1]*3:.1f} Q{hx + L*0.4*math.cos(ar) + n[0]*5:.1f},{hy + L*0.4*math.sin(ar) + n[1]*5:.1f} '
                       f'{tip[0]:.1f},{tip[1]:.1f} L{hx - n[0]*2:.1f},{hy - n[1]*2:.1f} Z"/>')
        o.append(f'<g class="blade2 b{k}" style="transform-origin:{hx:.1f}px {hy:.1f}px">{blades}</g>'
                 f'<circle cx="{hx:.1f}" cy="{hy:.1f}" r="3.2" class="hub"/>')
    # road + truck
    ra, rb = O(-1, -0.9, 0), O(24, -0.9, 0)
    o.append(f'<line class="road2" x1="{ra[0]:.1f}" y1="{ra[1]:.1f}" x2="{rb[0]:.1f}" y2="{rb[1]:.1f}"/>')
    tr = ('<rect x="0" y="-25" width="52" height="25" rx="1.5" class="trl"/>'
          + "".join(f'<line x1="{6+i*8}" y1="-24" x2="{6+i*8}" y2="-1" class="trrib"/>' for i in range(6))
          + '<path d="M54 -18 H66 L72 -10 V0 H54 Z" class="cab"/><path d="M58 -16 H65 L69 -10 H58 Z" class="cabw"/>'
          '<circle cx="11" cy="1" r="4.2" class="wh2"/><circle cx="40" cy="1" r="4.2" class="wh2"/><circle cx="64" cy="1" r="4.2" class="wh2"/>')
    o.append(f'<g>{tr}<animateMotion dur="14s" repeatCount="indefinite" path="M{ra[0]-90:.1f},{ra[1]-3:.1f} L{rb[0]+20:.1f},{rb[1]-3:.1f}"/></g>')
    o.append("</svg>")
    return "".join(o)


FOOT2_CSS = """
.fs2{display:block;width:100%;height:auto}
.fs2 .gnd{fill:var(--strong);fill-opacity:.04}
.fs2 .wf{fill:var(--strong);fill-opacity:.10;stroke:var(--line2);stroke-width:.8}
.fs2 .wt{fill:var(--strong);fill-opacity:.16;stroke:var(--line2);stroke-width:.8}
.fs2 .ws{fill:var(--strong);fill-opacity:.06;stroke:var(--line2);stroke-width:.8}
.fs2 .win{fill:#F2C46B;fill-opacity:.55}
.fs2 .win.w1{animation:winFlick 7s ease-in-out infinite}
@keyframes winFlick{0%,60%,100%{fill-opacity:.55}70%{fill-opacity:.2}}
.fs2 .door{fill:var(--strong);fill-opacity:.14;stroke:var(--line2);stroke-width:.8}
.fs2 .rib{stroke:var(--line2);stroke-width:.6}
.fs2 .pv{fill:url(#pv);stroke:#7FA3D8;stroke-opacity:.6;stroke-width:.7;animation:pvGlint 7s ease-in-out infinite}
.fs2 .pv1{animation-delay:.5s}.fs2 .pv2{animation-delay:1s}.fs2 .pv3{animation-delay:1.5s}
@keyframes pvGlint{0%,75%,100%{filter:brightness(1)}83%{filter:brightness(1.9)}}
.fs2 .cell{stroke:#9DB8E0;stroke-opacity:.35;stroke-width:.5}
.fs2 .cvf,.fs2 .cvt,.fs2 .cvs{fill:var(--strong);fill-opacity:.2;stroke:var(--line2);stroke-width:.6}
.fs2 .crate{fill:#B9895A;stroke:#7A5634;stroke-width:.6}.fs2 .cratet{fill:#D2A274;stroke:#7A5634;stroke-width:.6}
.fs2 .trunk{stroke:#6B5444;stroke-width:2.4}
.fs2 .tsh{fill:#000;opacity:.25}
.fs2 .tower{fill:var(--strong);fill-opacity:.55}
.fs2 .blade2 path{fill:var(--strong);fill-opacity:.85}
.fs2 .blade2{animation:bladeSpin 5s linear infinite}.fs2 .b1{animation-duration:6.4s}
.fs2 .hub{fill:var(--acc)}
.fs2 .road2{stroke:var(--line2);stroke-width:1.4;stroke-dasharray:12 9;animation:beltMove2 1.2s linear infinite}
.fs2 .trl{fill:var(--acc);fill-opacity:.9}.fs2 .trrib{stroke:#000;stroke-opacity:.18}
.fs2 .cab{fill:var(--strong);fill-opacity:.75}.fs2 .cabw{fill:#9CC3E6;fill-opacity:.8}
.fs2 .wh2{fill:#111;stroke:var(--strong);stroke-opacity:.6;stroke-width:1.6}
@media (prefers-reduced-motion:reduce){.fs2 *{animation:none!important}}
"""


# =====================================================================
# Hero rotation v2: A landscape -> B gear -> C QC, each runs twice
# =====================================================================
HERO_SLOT = 24.0      # every figure gets the same time: two full movements = 24 s
HERO_FADE = 1.0


def hero_cycle2(gear_html, compact=False):
    land, _ = landscape2_svg(hero=True)
    from or_figs4 import qc2_scene
    qc_s, _ = qc2_scene("qh", hero=True)
    qc_c, _, _, _ = qc_chart(hero=True)
    gear_html = gear_html.replace("FIG. A · SPUR GEAR PAIR · 3D", "FIG. B · SPUR GEAR PAIR · 3D")
    seq = [("A", "OPTIMIZATION LANDSCAPE",
            f'<div class="hcl">FIG. A · OPTIMIZATION LANDSCAPE</div><div class="hsv rock">{land}</div>'
            '<div class="hcn">3 searches · 2 stop in a local valley · 1 finds the global optimum</div>', "2 full searches (12 s each)"),
           ("B", "SPUR GEAR PAIR", gear_html, "2 turns of the pinion (12 s each)"),
           ("C", "QUALITY CONTROL",
            f'<div class="hcl">FIG. C · QUALITY CONTROL · INSPECTION AND SPC</div><div class="hsv">{qc_s}{qc_c}</div>', "2 inspection cycles (12 s each)")]
    n, T, F = len(seq), HERO_SLOT * len(seq), HERO_FADE
    P = lambda t: f"{t / T * 100:.3f}%"
    css, slides, prog = [], [], []
    for i, (k, name, html, note) in enumerate(seq):
        t0, t1 = i * HERO_SLOT, (i + 1) * HERO_SLOT
        # one figure at a time: the outgoing figure fades out, then the next fades in (no overlap,
        # so two titles are never visible together); 0.5 s each way
        h = F / 2
        kf = (f"0%,{P(t0)}{{opacity:0}}{P(t0 + h)},{P(t1 - h)}{{opacity:1}}{P(t1)},100%{{opacity:0}}")
        css.append(f"@keyframes hc3S{i}{{{kf}}}.hcy .sl{i}{{z-index:{i+1};opacity:0;animation:hc3S{i} {T:.0f}s linear infinite}}")
        css.append(f"@keyframes hc3P{i}{{0%,{P(t0)}{{transform:scaleX(0)}}{P(t1-0.01)}{{transform:scaleX(1)}}{P(t1)},100%{{transform:scaleX(0)}}}}"
                   f".hcy .pg{i} i{{animation:hc3P{i} {T:.0f}s linear infinite}}")
        slides.append(f'<div class="sl sl{i}">{html}</div>')
        prog.append(f'<div class="pg pg{i}"><span>FIG. {k} · {name}</span><em>{HERO_SLOT:.0f} s · {note}</em><b><i></i></b></div>')
    # the gear runs a little faster here so two pinion turns fit the same 24 s slot
    css.append(".hcy .g3d .r1{animation-duration:24s}.hcy .g3d .r2{animation-duration:12s}")
    if compact:   # homepage hero: figure only; FIG. A/B/C below are clickable (CSS radios, no JS)
        n = len(seq)
        radios = '<input type="radio" name="hfig" id="hf-auto" class="hfr" checked>' + "".join(
            f'<input type="radio" name="hfig" id="hf-{i}" class="hfr">' for i in range(n))
        mini = "".join(f'<label class="pg pg{i}" for="hf-{i}" title="Show FIG. {k}"><span>FIG. {k}</span><b><i></i></b></label>'
                       for i, (k, *_r) in enumerate(seq))
        mini += '<label class="pgauto" for="hf-auto" title="Back to automatic rotation">AUTO ↻</label>'
        pick = []
        for i in range(n):
            pick.append(f".hcy #hf-{i}:checked~.stg .sl{{animation:none;opacity:0;z-index:1}}"
                        f".hcy #hf-{i}:checked~.stg .sl{i}{{opacity:1;z-index:9}}"
                        f".hcy #hf-{i}:checked~.pgs .pg i{{animation:none;transform:scaleX(0)}}"
                        f".hcy #hf-{i}:checked~.pgs .pg{i} i{{transform:scaleX(1)}}"
                        f".hcy #hf-{i}:checked~.pgs .pg{i} span{{color:var(--acc-t)}}"
                        f".hcy #hf-{i}:checked~.pgs .pgauto{{opacity:1}}")
        return ("<style>" + "".join(css) + "".join(pick) + "</style>",
                f'<div class="hcy solo">{radios}<div class="stg">{"".join(slides)}</div><div class="pgs mini">{mini}</div></div>')
    return "<style>" + "".join(css) + "</style>", f'''<div class="hcy">
        <div class="stg">{"".join(slides)}</div>
        <div class="pgs">{"".join(prog)}<div class="hcn" style="margin-top:6px;padding:0">Equal time for each figure: 3 × 24 s = {T:.0f} s, then it starts again from FIG. A. Each change: 0.5 s fade out, then 0.5 s fade in, so two figures never overlap.</div></div>
      </div>'''


HERO2_CSS = """
.hcy .hfr{position:absolute;opacity:0;pointer-events:none}
.hcy .pgs.mini{position:relative;z-index:30}
.hcy .pgs.mini label.pg{cursor:pointer}
.hcy .pgs.mini label.pg:hover span{color:var(--strong)}
.hcy .pgs.mini .pgauto{position:relative;z-index:30;align-self:end;padding:2px 0 0;cursor:pointer;font:600 11.5px 'IBM Plex Mono',monospace;letter-spacing:.08em;color:var(--muted);opacity:.35;white-space:nowrap}
.hcy .pgs.mini .pgauto:hover{color:var(--acc-t)}
.hcy .g3d .pl3{transform:scale(.98) rotateX(57deg) rotateZ(-24deg)}
.hcy .stg{height:470px}
.hcy .hsv{padding:4px 8px}
.hcy .hsv svg{display:block;width:100%;height:auto;overflow:visible}
.hcy .hsv text{display:inline}
.hcy .hsv .lsv text{font:700 25px 'IBM Plex Mono',monospace}
.hcy .hsv .lsv .ball{r:11px}
.hcy .hsv .lsv .trail{stroke-width:3.4}
.hcy .hsv .qcs text{font:600 20px 'IBM Plex Mono',monospace}
.hcy .hsv .qcc text{font-size:24px}
.hcy .hsv .qcc .ln{stroke-width:3;stroke-opacity:.75}
.hcy .hsv .qcc .ok{r:7px}
.hcy .hsv .qcc .bad{r:9px}
.hcy .hsv .qcc .band{fill-opacity:.14}
.hcy .hsv .qcc .lim{stroke-opacity:.7;stroke-width:1.6}
.hcy .hsv .qcc .spec{stroke-opacity:.7;stroke-width:1.6}
.hcy .hsv .qcc .cl{stroke-opacity:.6;stroke-width:1.4}
.hcy .hcn{font-size:13.5px;color:var(--muted);padding:0 18px}
.hcy polygon.ft{fill:var(--strong);fill-opacity:.16;stroke:var(--line2);stroke-width:1}
.hcy polygon.fl{fill:var(--strong);fill-opacity:.07;stroke:var(--line2);stroke-width:1}
.hcy polygon.fr{fill:var(--strong);fill-opacity:.11;stroke:var(--line2);stroke-width:1}
.hcy polygon.at{fill:var(--acc);fill-opacity:.95}.hcy polygon.al{fill:var(--acc);fill-opacity:.55}.hcy polygon.ar{fill:var(--acc);fill-opacity:.75}
.hcy polygon.belt{fill:var(--strong);fill-opacity:.22;stroke:var(--line2)}
.hcy polygon.floor{fill:var(--strong);fill-opacity:.03;stroke:var(--line);stroke-dasharray:4 4}
.hcy .beltln{stroke:var(--strong);stroke-opacity:.35;stroke-width:1.4;stroke-dasharray:6 10;animation:beltMove 1s linear infinite}
.hcy polygon.chute{fill:var(--strong);fill-opacity:.18;stroke:var(--line2)}
.hcy polygon.bin{fill:var(--strong);fill-opacity:.06;stroke:var(--line2)}
.hcy polygon.binl{fill:var(--strong);fill-opacity:.13;stroke:var(--line2)}
.hcy polygon.binr{fill:var(--strong);fill-opacity:.09;stroke:var(--line2)}
.hcy polygon.laser{fill:#FF4B3E;fill-opacity:0;animation:qcLaser 2s linear infinite}
.hcy .trail{fill:none;stroke:var(--strong);stroke-width:2.2;stroke-linecap:round;stroke-dasharray:1 1;stroke-dashoffset:1;animation:trail 12s ease-in-out infinite}
.hcy .trail.g{stroke:var(--acc-t);stroke-width:2.6}
.hcy text{fill:var(--muted)}.hcy text.s{fill:var(--strong)}.hcy text.h{fill:var(--acc-t)}
"""
