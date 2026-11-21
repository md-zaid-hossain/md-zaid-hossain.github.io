#!/usr/bin/env python3
"""QC inspection cell v2 (Zaid: deeper, more realistic environment and components).
Same timing as or_figs3 (one shaft every 2 s, one oversize shaft per 20 s cycle), so the
I-chart, lamps and pusher stay in sync. Pure SVG + CSS/SMIL."""
import math
from or_figs import iso, poly, box, C30, S30
from or_figs3 import (QC_T, QC_N, QC_GAP, QC_TRAVEL, QC_X0, QC_X1, QC_GAUGE, QC_PUSH, QC_BAD,
                      _local, _doc, pct)

BZ = 0.9            # belt top height (units)
S = 26


def _defs(uid):
    return (f'<defs>'
            f'<linearGradient id="sh{uid}" x1="0" x2="1"><stop offset="0" stop-color="#5E6570"/><stop offset=".32" stop-color="#E4E8ED"/>'
            f'<stop offset=".55" stop-color="#A3AAB5"/><stop offset="1" stop-color="#4F5560"/></linearGradient>'
            f'<radialGradient id="st{uid}" cx=".4" cy=".4"><stop offset="0" stop-color="#F4F6F9"/><stop offset="1" stop-color="#8E96A2"/></radialGradient>'
            f'<pattern id="hz{uid}" width="14" height="14" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">'
            f'<rect width="14" height="14" fill="#E8B83A"/><rect width="7" height="14" fill="#1E2126"/></pattern>'
            f'</defs>')


def _cyl(r, h, uid, z0=0.0):
    """Upright cylinder drawn at the origin (screen units), bottom at height z0."""
    rx, ry, H, b = 1.2247 * r * S, 0.7071 * r * S, h * S, -z0 * S
    return (f'<path fill="url(#sh{uid})" stroke="rgba(0,0,0,.4)" stroke-width=".5" '
            f'd="M{-rx:.1f},{b:.1f} A{rx:.1f},{ry:.1f} 0 0 0 {rx:.1f},{b:.1f} L{rx:.1f},{b-H:.1f} '
            f'A{rx:.1f},{ry:.1f} 0 0 0 {-rx:.1f},{b-H:.1f} Z"/>'
            f'<ellipse cx="0" cy="{b-H:.1f}" rx="{rx:.1f}" ry="{ry:.1f}" fill="url(#st{uid})" stroke="rgba(0,0,0,.35)" stroke-width=".5"/>')


def shaft(uid):
    """Stepped turned shaft: Ø25 body + Ø16 journal, with a chamfer ring."""
    return _cyl(0.32, 0.55, uid) + _cyl(0.21, 0.42, uid, 0.55)


def qc2_scene(uid="q", hero=False):
    ox, oy = 250, 150
    P = lambda x, y, z: iso(x, y, z, S, ox, oy)
    o = [f'<svg class="qcs qc2" viewBox="0 0 820 450" role="img" '
         f'aria-label="Inspection cell: a through-beam laser micrometer measures every shaft, a pneumatic pusher rejects the oversize one">',
         _defs(uid)]
    # ---- floor: concrete, aisle line, hazard zone around the pusher
    o.append(poly([P(-2, -5, 0), P(22.5, -5, 0), P(22.5, 4.8, 0), P(-2, 4.8, 0)], "conc"))
    for x in range(-2, 23, 3):
        a, b = P(x, -5, 0), P(x, 4.8, 0)
        o.append(f'<line class="joint" x1="{a[0]:.1f}" y1="{a[1]:.1f}" x2="{b[0]:.1f}" y2="{b[1]:.1f}"/>')
    o.append(poly([P(-2, 4.2, 0), P(22.5, 4.2, 0), P(22.5, 4.45, 0), P(-2, 4.45, 0)], "aisle"))
    o.append(f'<polygon fill="url(#hz{uid})" opacity=".55" points="'
             + " ".join(f"{x:.1f},{y:.1f}" for x, y in [P(9.6, -3.6, 0), P(12.4, -3.6, 0), P(12.4, -3.3, 0), P(9.6, -3.3, 0)]) + '"/>')
    # ---- back row: control cabinet with HMI + stack light, pusher, emitter head
    o.append(box(13.4, 15.6, -4.4, -3.0, 0, 2.7, P, "ca1", "ca2", "ca3"))
    hmi = [P(13.8, -3.0, 1.2), P(15.2, -3.0, 1.2), P(15.2, -3.0, 2.3), P(13.8, -3.0, 2.3)]
    o.append(poly(hmi, "hmi"))
    # tiny live-looking trace on the HMI
    pts = [(13.95 + i * 0.13, -3.0, 1.55 + (0.25 if i == 6 else 0.08 * math.sin(i * 1.7))) for i in range(10)]
    o.append('<polyline class="hmit" points="' + " ".join(f"{P(*p)[0]:.1f},{P(*p)[1]:.1f}" for p in pts) + '"/>')
    hx, hy = P(14.73, -3.0, 1.8)
    o.append(f'<circle cx="{hx:.1f}" cy="{hy:.1f}" r="2.4" fill="#E0524A"/>')
    # stack light on the cabinet
    sx, sy = P(15.0, -3.7, 2.7)
    o.append(f'<rect x="{sx-1.5:.1f}" y="{sy-50:.1f}" width="3" height="50" fill="#3A3F47"/>')
    for k, cls in enumerate(("lampok", "amb", "lampbad")):   # green bottom, red top
        cy_ = sy - 50 - k * 13
        o.append(f'<rect x="{sx-6:.1f}" y="{cy_-12:.1f}" width="12" height="12" rx="2" class="sl-base"/>'
                 f'<rect x="{sx-6:.1f}" y="{cy_-12:.1f}" width="12" height="12" rx="2" class="{cls}"/>')
    # cable tray from cabinet to the gauge
    o.append(box(7.2, 13.4, -3.75, -3.45, 2.3, 2.42, P, "mt1", "mt2", "mt3"))
    # pneumatic pusher on a bracket, behind the belt
    o.append(box(10.55, 11.45, -2.9, -2.6, 0, BZ + 0.35, P, "mt1", "mt2", "mt3"))
    o.append(box(10.6, 11.4, -2.9, -1.05, BZ + 0.2, BZ + 0.7, P, "pn1", "pn2", "pn3"))
    hz_ = P(11.0, -2.9, BZ + 0.45)
    o.append(f'<path class="hose" d="M{hz_[0]:.1f},{hz_[1]:.1f} q-30,-6 -44,24"/>')
    # through-beam laser micrometer: emitter on the far side
    o.append(box(6.75, 7.25, -1.6, -1.3, 0, BZ + 0.15, P, "mt1", "mt2", "mt3"))
    o.append(box(6.6, 7.4, -1.75, -1.05, BZ + 0.15, BZ + 1.25, P, "dk1", "dk2", "dk3"))
    # photo-eye that triggers the measurement
    o.append(box(5.9, 6.2, -1.15, -0.85, BZ + 0.1, BZ + 0.45, P, "dk1", "dk2", "dk3"))
    # ---- conveyor: legs, side frame, belt, end drums, drive motor
    for lx in (0.0, 5.0, 10.0, 15.0, 19.0):
        o.append(box(lx, lx + 0.25, -0.8, -0.6, 0, BZ - 0.15, P, "mt1", "mt2", "mt3"))
    o.append(box(QC_X0 - 0.7, QC_X1 + 0.5, -0.85, -0.7, BZ - 0.25, BZ + 0.18, P, "mt1", "mt2", "mt3"))   # back rail
    o.append(box(QC_X0 - 0.7, QC_X1 + 0.5, -0.7, 0.7, BZ - 0.18, BZ, P, "rb1", "rb2", "rb3"))           # belt
    a, b = P(QC_X0 - 0.6, 0, BZ), P(QC_X1 + 0.4, 0, BZ)
    o.append(f'<line class="beltln2" x1="{a[0]:.1f}" y1="{a[1]:.1f}" x2="{b[0]:.1f}" y2="{b[1]:.1f}"/>')
    o.append(box(QC_X1 + 0.5, QC_X1 + 1.3, -0.9, -0.2, BZ - 0.6, BZ - 0.05, P, "dk1", "dk2", "dk3"))     # gear motor
    # reject chute (under the parts) and the NG tote's back + floor
    o.append(poly([P(10.35, 0.7, BZ - 0.02), P(11.65, 0.7, BZ - 0.02), P(11.65, 2.0, 0.55), P(10.35, 2.0, 0.55)], "chute2"))
    o.append(poly([P(9.9, 2.0, 0), P(12.1, 2.0, 0), P(12.1, 3.7, 0), P(9.9, 3.7, 0)], "ng2"))
    o.append(poly([P(9.9, 2.0, 0), P(12.1, 2.0, 0), P(12.1, 2.0, 0.85), P(9.9, 2.0, 0.85)], "ng3"))
    # OK tote's back + floor at the outfeed, with parts already inside
    o.append(poly([P(QC_X1 + 0.6, -1.0, 0), P(QC_X1 + 2.6, -1.0, 0), P(QC_X1 + 2.6, 1.1, 0), P(QC_X1 + 0.6, 1.1, 0)], "ok2"))
    for k, (dx, dy) in enumerate([(0.9, -0.4), (1.5, -0.3), (1.2, 0.3), (1.9, 0.4)]):
        px, py = P(QC_X1 + dx, dy, 0)
        o.append(f'<g transform="translate({px:.1f},{py:.1f}) rotate(-62)">{shaft(uid)}</g>')
    # ---- moving shafts
    pa, pb = P(QC_X0, 0, BZ), P(QC_X1, 0, BZ)
    l_push, l_end = _local(QC_PUSH) / QC_T, QC_TRAVEL / QC_T
    pp, pch, pbin = P(QC_PUSH, 0, BZ), P(QC_PUSH, 2.0, 0.55), P(QC_PUSH, 2.9, 0.05)
    for k in range(QC_N):
        bad = k == QC_BAD
        mark = ""
        if bad:
            ti = _local(QC_GAUGE) / QC_T
            mark = (f'<ellipse cx="0" cy="{-0.55*S:.1f}" rx="{0.62*S:.1f}" ry="{0.34*S:.1f}" fill="none" stroke="#E0524A" stroke-width="2.4" opacity="0">'
                    f'<animate attributeName="opacity" dur="{QC_T}s" begin="-{QC_GAP*k:.2f}s" repeatCount="indefinite" '
                    f'keyTimes="0;{ti:.4f};{ti+0.005:.4f};1" values="0;0;1;1"/></ellipse>')
        part = shaft(uid) + mark
        beg = f'dur="{QC_T}s" begin="-{QC_GAP*k:.2f}s" repeatCount="indefinite"'
        if not bad:
            mot = (f'<animateMotion {beg} calcMode="linear" keyTimes="0;{l_end:.4f};1" keyPoints="0;1;1" '
                   f'path="M{pa[0]:.1f},{pa[1]:.1f} L{pb[0]:.1f},{pb[1]:.1f}"/>')
            vis = f'<animate attributeName="opacity" {beg} keyTimes="0;0.02;{l_end:.4f};{l_end+0.02:.4f};1" values="0;1;1;0;0"/>'
        else:
            t1, t2, t3 = l_push, l_push + 0.5 / QC_T, l_push + 1.0 / QC_T
            L1, L2, L3 = math.dist(pa, pp), math.dist(pp, pch), math.dist(pch, pbin)
            Lt = L1 + L2 + L3
            mot = (f'<animateMotion {beg} calcMode="linear" keyTimes="0;{t1:.4f};{t2:.4f};{t3:.4f};1" '
                   f'keyPoints="0;{L1/Lt:.4f};{(L1+L2)/Lt:.4f};1;1" '
                   f'path="M{pa[0]:.1f},{pa[1]:.1f} L{pp[0]:.1f},{pp[1]:.1f} L{pch[0]:.1f},{pch[1]:.1f} L{pbin[0]:.1f},{pbin[1]:.1f}"/>')
            vis = f'<animate attributeName="opacity" {beg} keyTimes="0;0.02;{t3+0.06:.4f};{t3+0.09:.4f};1" values="0;1;1;0;0"/>'
        o.append(f'<g opacity="0">{part}{mot}{vis}</g>')
    # pusher rod + push pad (fires when the oversize shaft arrives)
    dx, dy = -C30 * S * 1.25, S30 * S * 1.25
    o.append(f'<g class="rod" style="--dx:{dx:.1f}px;--dy:{dy:.1f}px">'
             f'{box(10.88, 11.12, -1.05, -0.75, BZ + 0.33, BZ + 0.57, P, "mt1", "mt2", "mt3")}'
             f'{box(10.6, 11.4, -0.8, -0.68, BZ + 0.12, BZ + 0.75, P, "yl1", "yl2", "yl3")}</g>')
    # laser beam across the belt (flashes at every measurement)
    e1, e2 = P(7.0, -1.05, BZ + 0.55), P(7.0, 1.05, BZ + 0.55)
    o.append(f'<line class="beam" x1="{e1[0]:.1f}" y1="{e1[1]:.1f}" x2="{e2[0]:.1f}" y2="{e2[1]:.1f}"/>')
    # ---- front row: front rail (gap at the pusher), receiver head, NG tote front walls, OK tote front
    for xa, xb in ((QC_X0 - 0.7, 10.3), (11.7, QC_X1 + 0.5)):
        o.append(box(xa, xb, 0.7, 0.85, BZ - 0.25, BZ + 0.18, P, "mt1", "mt2", "mt3"))
    o.append(box(6.75, 7.25, 1.3, 1.6, 0, BZ + 0.15, P, "mt1", "mt2", "mt3"))
    o.append(box(6.6, 7.4, 1.05, 1.75, BZ + 0.15, BZ + 1.25, P, "dk1", "dk2", "dk3"))
    rx_, ry_ = P(7.4, 1.4, BZ + 0.7)
    o.append(f'<circle cx="{rx_:.1f}" cy="{ry_:.1f}" r="3" class="lampok"/><circle cx="{rx_:.1f}" cy="{ry_:.1f}" r="3" class="lampbad"/>')
    o.append(poly([P(9.9, 3.7, 0), P(12.1, 3.7, 0), P(12.1, 3.7, 0.85), P(9.9, 3.7, 0.85)], "ng1"))
    o.append(poly([P(12.1, 2.0, 0), P(12.1, 3.7, 0), P(12.1, 3.7, 0.85), P(12.1, 2.0, 0.85)], "ng4"))
    o.append(poly([P(QC_X1 + 0.6, 1.1, 0), P(QC_X1 + 2.6, 1.1, 0), P(QC_X1 + 2.6, 1.1, 0.75), P(QC_X1 + 0.6, 1.1, 0.75)], "ok1"))
    o.append(poly([P(QC_X1 + 2.6, -1.0, 0), P(QC_X1 + 2.6, 1.1, 0), P(QC_X1 + 2.6, 1.1, 0.75), P(QC_X1 + 2.6, -1.0, 0.75)], "ok3"))
    # tote labels
    nx, ny = P(11.0, 3.7, 0.42)
    o.append(f'<text class="tl" x="{nx-9:.1f}" y="{ny+4:.1f}">NG</text>')
    kx, ky = P(QC_X1 + 1.6, 1.1, 0.38)
    o.append(f'<text class="tl" x="{kx-9:.1f}" y="{ky+4:.1f}">OK</text>')
    if not hero:
        # numbered callouts (legend sits under the scene) instead of loose labels
        marks = [(1, (6.05, -1.0, BZ + 1.0)), (2, (7.0, -1.4, BZ + 1.75)), (3, (11.0, -2.0, BZ + 1.15)),
                 (4, (11.0, 3.7, 1.45)), (5, (QC_X1 + 1.6, 1.1, 1.3)), (6, (14.5, -3.0, 3.1))]
        for n, (x, y, z) in marks:
            px, py = P(x, y, z)
            o.append(f'<g class="cm"><circle cx="{px:.1f}" cy="{py:.1f}" r="10"/><text x="{px:.1f}" y="{py+4.2:.1f}" text-anchor="middle">{n}</text></g>')
    o.append("</svg>")
    t_fire = _doc(_local(QC_PUSH), QC_BAD)
    return "".join(o), t_fire


QC2_CSS = """
.qc2 .cm circle{fill:var(--bg);stroke:var(--acc-t);stroke-width:1.4}
.qc2 .cm text{font:700 11.5px 'IBM Plex Mono',monospace;fill:var(--strong)}
.qcleg{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:6px 18px;margin:2px 6px 12px;padding:10px 12px;border:1px solid var(--line);border-radius:8px}
.qcleg span{display:flex;align-items:center;gap:8px;font-size:13px;color:var(--body)}
.qcleg i{flex:none;width:20px;height:20px;border-radius:999px;border:1.4px solid var(--acc-t);display:flex;align-items:center;justify-content:center;font:700 11px 'IBM Plex Mono',monospace;font-style:normal;color:var(--strong)}
@media (max-width:760px){.qcleg{grid-template-columns:1fr 1fr}.qc2 .cm text{font-size:22px}.qc2 .cm circle{r:16px}}
@media (max-width:760px){.orf .qc2 text:not(.tl){display:none}.orf .qcc text{font-size:24px}.orf .qc2 text.tl{font-size:22px}}
.qc2 .conc{fill:var(--strong);fill-opacity:.045;stroke:var(--line);stroke-width:1}
.qc2 .joint{stroke:var(--line);stroke-width:.8}
.qc2 .aisle{fill:#E8B83A;fill-opacity:.75}
.qc2 .mt1{fill:#B9BFC8;stroke:#5E646D;stroke-width:.5}.qc2 .mt2{fill:#8B929C;stroke:#5E646D;stroke-width:.5}.qc2 .mt3{fill:#A1A8B2;stroke:#5E646D;stroke-width:.5}
.qc2 .rb1{fill:#3A3F47;stroke:#1E2126;stroke-width:.6}.qc2 .rb2{fill:#24272C;stroke:#1E2126;stroke-width:.6}.qc2 .rb3{fill:#2D3137;stroke:#1E2126;stroke-width:.6}
.qc2 .ca1{fill:#7A818C;stroke:#454A52;stroke-width:.6}.qc2 .ca2{fill:#5F656F;stroke:#454A52;stroke-width:.6}.qc2 .ca3{fill:#6B717B;stroke:#454A52;stroke-width:.6}
.qc2 .dk1{fill:#3D424A;stroke:#1A1D22;stroke-width:.6}.qc2 .dk2{fill:#2A2E34;stroke:#1A1D22;stroke-width:.6}.qc2 .dk3{fill:#33373E;stroke:#1A1D22;stroke-width:.6}
.qc2 .pn1{fill:#C9CED6;stroke:#6A7079;stroke-width:.6}.qc2 .pn2{fill:#9AA1AB;stroke:#6A7079;stroke-width:.6}.qc2 .pn3{fill:#B0B6BF;stroke:#6A7079;stroke-width:.6}
.qc2 .yl1{fill:#F0C24A;stroke:#8C6A12;stroke-width:.5}.qc2 .yl2{fill:#C8961E;stroke:#8C6A12;stroke-width:.5}.qc2 .yl3{fill:#DDAA30;stroke:#8C6A12;stroke-width:.5}
.qc2 .hmi{fill:#0D1B26;stroke:#4FA3D1;stroke-width:.8}
.qc2 .hmit{fill:none;stroke:#7CC4EA;stroke-width:1.2}
.qc2 .hose{fill:none;stroke:#3C82C4;stroke-width:2}
.qc2 .chute2{fill:#A9B0BA;fill-opacity:.85;stroke:#5E646D;stroke-width:.6}
.qc2 .ng1{fill:#C9473E;fill-opacity:.92;stroke:#7E2A24;stroke-width:.6}.qc2 .ng2{fill:#7E2A24}.qc2 .ng3{fill:#A63A33}.qc2 .ng4{fill:#B23D35;fill-opacity:.95;stroke:#7E2A24;stroke-width:.6}
.qc2 .ok1{fill:#3E9E6E;fill-opacity:.92;stroke:#245E42;stroke-width:.6}.qc2 .ok2{fill:#245E42}.qc2 .ok3{fill:#348A5F;fill-opacity:.95;stroke:#245E42;stroke-width:.6}
.qc2 text.tl{font:700 12px 'IBM Plex Mono',monospace;fill:#FFFFFF}
.qc2 .beltln2{stroke:#FFFFFF;stroke-opacity:.12;stroke-width:1.4;stroke-dasharray:4 12;animation:beltMove 1s linear infinite}
.qc2 .beam{stroke:#FF3B30;stroke-width:2;stroke-opacity:.15}
.qc2 .sl-base{fill:#2A2E34}
.qc2 .amb{fill:#E8A23A;opacity:.25}
"""


def qc2_css():
    insp0 = _doc(_local(QC_GAUGE), 0) % QC_GAP
    return (QC2_CSS
            + f"@keyframes qcBeam{{0%{{stroke-opacity:.15;stroke-width:2}}6%{{stroke-opacity:1;stroke-width:3.4}}22%,100%{{stroke-opacity:.15;stroke-width:2}}}}"
            + f".qc2 .beam{{animation:qcBeam 2s linear infinite;animation-delay:{insp0-0.05:.2f}s}}"
            + "@media (prefers-reduced-motion:reduce){.qc2 .beam{animation:none}}")


# =====================================================================
# Sewing line v3: solid bodies (Zaid: "solid korle valo"), wire only for floor grid
# =====================================================================
from or_figs3 import SEW_OPS


def sewing3_svg(hero=False):
    s, ox, oy = 27, 250, 150
    P = lambda x, y, z: iso(x, y, z, s, ox, oy)
    o = ['<svg class="sw3" viewBox="0 0 860 470" role="img" aria-label="Sewing line: four operators at industrial sewing machines; garment bundles move on a conveyor">']
    o.append(poly([P(-2, -6, 0), P(23, -6, 0), P(23, 3.5, 0), P(-2, 3.5, 0)], "floor3"))
    for x in range(-2, 24, 2):                      # floor grid stays as wire
        a, b = P(x, -6, 0), P(x, 3.5, 0)
        o.append(f'<line class="tile" x1="{a[0]:.1f}" y1="{a[1]:.1f}" x2="{b[0]:.1f}" y2="{b[1]:.1f}"/>')
    for y in range(-6, 4, 2):
        a, b = P(-2, y, 0), P(23, y, 0)
        o.append(f'<line class="tile" x1="{a[0]:.1f}" y1="{a[1]:.1f}" x2="{b[0]:.1f}" y2="{b[1]:.1f}"/>')
    items = []                                      # (depth, svg) painter's list

    def add(x0, x1, y0, y1, z0, z1, c):
        items.append(((x0 + x1) / 2 + (y0 + y1) / 2 + z0 * 0.01, box(x0, x1, y0, y1, z0, z1, P, c + "1", c + "2", c + "3")))

    stations = [3, 8, 13, 18]
    for i, c in enumerate(stations):
        hot = i == 2
        # operator on a stool, behind the table, facing the line
        add(c - 0.45, c + 0.45, -4.65, -3.75, 0, 1.0, "st")                 # stool
        add(c - 0.55, c + 0.55, -4.5, -3.9, 1.0, 1.25, "pt")                # lap
        add(c - 0.55, c + 0.55, -4.45, -3.95, 1.25, 2.6, "cl")              # torso
        add(c - 0.6, c - 0.35, -3.95, -3.1, 2.0, 2.25, "cl")                # left forearm to table
        add(c + 0.35, c + 0.6, -3.95, -3.1, 2.0, 2.25, "cl")                # right forearm
        hx, hy = P(c, -4.2, 3.0)
        items.append((c - 4.2 + 0.05, f'<circle class="skin" cx="{hx:.1f}" cy="{hy:.1f}" r="{0.38*s:.1f}"/>'
                      f'<path class="hair" d="M{hx-0.38*s:.1f},{hy-2:.1f} a{0.38*s:.1f},{0.38*s:.1f} 0 0 1 {0.76*s:.1f},0 Z"/>'))
        # table: top + legs
        for lx in (c - 1.45, c + 1.3):
            for ly in (-3.35, -1.35):
                add(lx, lx + 0.12, ly, ly + 0.12, 0, 1.45, "lg")
        add(c - 1.5, c + 1.5, -3.4, -1.2, 1.45, 1.6, "tb")
        # industrial sewing machine: bed, pillar, arm, head, hand wheel
        add(c - 0.9, c + 0.9, -2.7, -1.9, 1.6, 1.85, "mc")
        add(c + 0.5, c + 0.85, -2.6, -2.0, 1.85, 2.9, "mc")
        add(c - 0.8, c + 0.85, -2.6, -2.0, 2.9, 3.25, "mc")
        add(c - 0.8, c - 0.45, -2.6, -2.0, 2.4, 2.9, "hd" if hot else "mc")
        wx, wy = P(c + 0.95, -2.3, 2.75)
        items.append((c - 2.3 + 1.0, f'<ellipse class="wheel" cx="{wx:.1f}" cy="{wy:.1f}" rx="4" ry="7"/>'))
        add(c - 1.1, c - 0.2, -2.0, -1.4, 1.6, 1.68, "fb")                   # fabric under the needle
        # andon lamp on a pole (thin parts stay as lines)
        px, py = P(c + 1.3, -3.2, 1.6)
        qx, qy = P(c + 1.3, -3.2, 3.9)
        lab = ""
        if not hero:
            lab = f'<text class="{"h" if hot else "s"} lb3" x="{qx+10:.1f}" y="{qy+4:.1f}">{SEW_OPS[i][0]} · {SEW_OPS[i][1]}</text>'
        items.append((c + 1.3 - 3.2 + 2, f'<line x1="{px:.1f}" y1="{py:.1f}" x2="{qx:.1f}" y2="{qy:.1f}" class="pole"/>'
                      f'<circle class="lamp{" on" if hot else " ok"}" cx="{qx:.1f}" cy="{qy:.1f}" r="5"/>{lab}'))
    # WIP cart in front of S3
    add(10.0, 11.6, 1.2, 2.4, 0.3, 0.45, "lg")
    for z in (0.45, 0.6, 0.75):
        add(10.2, 11.3, 1.4, 2.2, z, z + 0.14, "fb")
    if not hero:
        wx_, wy_ = P(10.8, 2.6, 0)
        items.append((20, f'<text class="lb3" x="{wx_-10:.1f}" y="{wy_+16:.1f}">WIP · 3 BUNDLES</text>'))
    # conveyor: legs + frame + belt (drawn in depth order with the rest)
    for lx in (0, 5, 10, 15, 20):
        add(lx, lx + 0.2, -0.5, -0.3, 0, 0.6, "lg")
        add(lx, lx + 0.2, 0.3, 0.5, 0, 0.6, "lg")
    items.append((10.25, box(-1.5, 22, -0.6, 0.6, 0.6, 0.9, P, "bt1", "bt2", "bt3")))
    items.sort(key=lambda t: t[0])
    o += [svg for _, svg in items]
    a, b = P(-1.5, 0, 0.9), P(22, 0, 0.9)
    o.append(f'<line class="beltln3" x1="{a[0]:.1f}" y1="{a[1]:.1f}" x2="{b[0]:.1f}" y2="{b[1]:.1f}"/>')
    bundle = (box(-0.45, 0.45, -0.35, 0.35, 0, 0.18, lambda x, y, z: iso(x, y, z, s, 0, 0), "fb1", "fb2", "fb3")
              + box(-0.4, 0.4, -0.3, 0.3, 0.18, 0.32, lambda x, y, z: iso(x, y, z, s, 0, 0), "fb1", "fb2", "fb3"))
    start, end = P(-1.2, 0, 0.9), P(21.6, 0, 0.9)
    frac = lambda x: (x + 1.2) / 22.8
    seq, t = [(0.0, 0.0)], 0.0
    for c, dwell in zip(stations, [1.2, 1.25, 1.8, 1.4]):
        t += 1.3; seq.append((t, frac(c)))
        t += dwell; seq.append((t, frac(c)))
    t += 1.3; seq.append((t, 1.0))
    kt = ";".join(f"{x/t:.4f}" for x, _ in seq)
    kp = ";".join(f"{p:.4f}" for _, p in seq)
    for k in range(6):
        o.append(f'<g>{bundle}<animateMotion dur="{t:.2f}s" begin="-{k*t/6:.2f}s" repeatCount="indefinite" '
                 f'calcMode="linear" keyTimes="{kt}" keyPoints="{kp}" path="M{start[0]:.1f},{start[1]:.1f} L{end[0]:.1f},{end[1]:.1f}"/></g>')
    if not hero:
        ix, iy = P(-1.5, 1.0, 0)
        o.append(f'<text class="lb3" x="{ix-50:.1f}" y="{iy+22:.1f}">CUT PANELS IN</text>')
        ex, ey = P(22, 1.0, 0)
        o.append(f'<text class="lb3" x="{ex-20:.1f}" y="{ey+22:.1f}">T-SHIRTS OUT →</text>')
    o.append("</svg>")
    return "".join(o)


SEW3_CSS = """
@media (max-width:760px){.sw3 text{display:none}}
.sw3 .floor3{fill:var(--strong);fill-opacity:.035;stroke:var(--line2);stroke-width:1}
.sw3 .tile{stroke:var(--line);stroke-width:.8}
.sw3 .st1{fill:#3B3F46}.sw3 .st2{fill:#2B2E34}.sw3 .st3{fill:#33373D}
.sw3 .pt1{fill:#3E4656}.sw3 .pt2{fill:#2E3441}.sw3 .pt3{fill:#363D4B}
.sw3 .cl1{fill:#2F8C86}.sw3 .cl2{fill:#21665F}.sw3 .cl3{fill:#287A73}
.sw3 .skin{fill:#C99A74}.sw3 .hair{fill:#2A221D}
.sw3 .lg1{fill:#A7AEB8}.sw3 .lg2{fill:#7F8690}.sw3 .lg3{fill:#959CA6}
.sw3 .tb1{fill:#D8CCB4;stroke:#9C8F78;stroke-width:.5}.sw3 .tb2{fill:#B4A78E;stroke:#9C8F78;stroke-width:.5}.sw3 .tb3{fill:#C6B9A0;stroke:#9C8F78;stroke-width:.5}
.sw3 .mc1{fill:#ECE8DF;stroke:#A39D90;stroke-width:.5}.sw3 .mc2{fill:#C9C3B6;stroke:#A39D90;stroke-width:.5}.sw3 .mc3{fill:#DAD5CA;stroke:#A39D90;stroke-width:.5}
.sw3 .hd1{fill:var(--acc)}.sw3 .hd2{fill:var(--acc);filter:brightness(.7)}.sw3 .hd3{fill:var(--acc);filter:brightness(.85)}
.sw3 .fb1{fill:#5B7FB8;stroke:rgba(0,0,0,.25);stroke-width:.5}.sw3 .fb2{fill:#46679A;stroke:rgba(0,0,0,.25);stroke-width:.5}.sw3 .fb3{fill:#3D5C8C;stroke:rgba(0,0,0,.25);stroke-width:.5}
.sw3 .bt1{fill:#3A3F47;stroke:#1E2126;stroke-width:.6}.sw3 .bt2{fill:#9AA1AB;stroke:#5E646D;stroke-width:.5}.sw3 .bt3{fill:#B1B7C0;stroke:#5E646D;stroke-width:.5}
.sw3 .beltln3{stroke:#FFFFFF;stroke-opacity:.14;stroke-width:1.4;stroke-dasharray:4 12;animation:beltMove 1s linear infinite}
.sw3 .wheel{fill:#55595F;stroke:#2B2E33}
.sw3 .pole{stroke:var(--line2);stroke-width:1.5}
.sw3 .lamp{fill:var(--line2)}.sw3 .lamp.ok{fill:#3FB47A;opacity:.85}.sw3 .lamp.on{fill:#E0524A;animation:lampGlow 1.4s ease-in-out infinite}
.sw3 text.lb3{paint-order:stroke;stroke:var(--bg);stroke-width:4px;stroke-linejoin:round}
"""


# =====================================================================
# FDM printer v3: more realistic Ender-3 style printer; prints a 3-2-1
# locating fixture (Zaid's own project) instead of a gear
# =====================================================================
PR3_T, PR3_N, PR3_H = 15.0, 20, 0.11


def _rect(x0, x1, y0, y1, z, P):
    return [P(x0, y0, z), P(x1, y0, z), P(x1, y1, z), P(x0, y1, z)]


def _circ(cx, cy, r, z, P, n=18):
    return [P(cx + r * math.cos(2 * math.pi * k / n), cy + r * math.sin(2 * math.pi * k / n), z) for k in range(n)]


def _d(pts):
    return "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts) + " Z"


def fixture_layer(i, z, P):
    """Layer i of a 3-2-1 locating fixture: base plate with two bolt holes, then three locating pins
    and an L-shaped side stop."""
    if i < 9:   # base plate
        return _d(_rect(2.2, 6.8, 2.6, 6.4, z, P)) + " " + _d(_circ(2.9, 5.7, 0.28, z, P)) + " " + _d(_circ(6.1, 3.3, 0.28, z, P))
    d = ""
    for cx, cy in ((3.0, 3.2), (6.0, 3.2), (4.5, 5.6)):           # the "3" primary locators
        d += _d(_circ(cx, cy, 0.32, z, P)) + " "
    d += _d([P(2.2, 6.0, z), P(6.8, 6.0, z), P(6.8, 6.4, z), P(2.2, 6.4, z)])     # back stop ("2")
    if i < 16:
        d += " " + _d([P(6.4, 2.6, z), P(6.8, 2.6, z), P(6.8, 4.2, z), P(6.4, 4.2, z)])  # side stop ("1")
    return d


def printer3_svg():
    s, ox, oy = 24, 232, 336
    P = lambda x, y, z: iso(x, y, z, s, ox, oy)
    o = ['<svg class="pr3" viewBox="0 0 520 540" role="img" aria-label="Ender-3 style printer printing a 3-2-1 locating fixture layer by layer">',
         '<defs><linearGradient id="vsl" x1="0" x2="1"><stop offset="0" stop-color="#2A2E35"/><stop offset=".5" stop-color="#3D424A"/><stop offset="1" stop-color="#24272D"/></linearGradient>'
         '<pattern id="pei" width="5" height="5" patternUnits="userSpaceOnUse"><rect width="5" height="5" fill="#16181C"/><circle cx="2.5" cy="2.5" r=".7" fill="#2C3036"/></pattern></defs>']
    sx, sy = P(4.5, 4.5, 0)
    o.append(f'<ellipse cx="{sx:.1f}" cy="{sy+22:.1f}" rx="200" ry="62" class="shdw"/>')
    # base frame + Y extrusion + PSU + feet
    for fx, fy in ((0.3, 0.3), (8.4, 0.3), (0.3, 8.4), (8.4, 8.4)):
        o.append(box(fx, fx + 0.4, fy, fy + 0.4, 0, 0.25, P, "ft1", "ft2", "ft3"))
    o.append(box(0, 9, 0, 9, 0.25, 1.15, P, "fr1", "fr2", "fr3"))
    o.append(box(9.0, 9.9, 0.8, 5.2, 0.25, 1.6, P, "fr1", "fr2", "fr3"))
    # left Z extrusion with V-slot groove + lead screw
    o.append(box(0.3, 0.9, 4.0, 4.9, 1.15, 11.6, P, "ex1", "ex2", "ex3"))
    g1, g2 = P(0.6, 4.9, 1.2), P(0.6, 4.9, 11.5)
    o.append(f'<line class="groove" x1="{g1[0]:.1f}" y1="{g1[1]:.1f}" x2="{g2[0]:.1f}" y2="{g2[1]:.1f}"/>')
    l1, l2 = P(1.15, 4.45, 1.15), P(1.15, 4.45, 11.0)
    o.append(f'<line class="screw" x1="{l1[0]:.1f}" y1="{l1[1]:.1f}" x2="{l2[0]:.1f}" y2="{l2[1]:.1f}"/>')
    o.append(box(0.9, 1.4, 4.2, 4.7, 1.15, 1.6, P, "mo1", "mo2", "mo3"))          # Z motor
    # top bar + spool holder + spool + filament to the extruder
    o.append(box(0.3, 8.7, 4.0, 4.9, 11.6, 12.2, P, "ex1", "ex2", "ex3"))
    cx_, cz_ = 4.5, 13.7
    ring = [P(cx_ + 1.45 * math.cos(a), 4.45, cz_ + 1.45 * math.sin(a)) for a in [2 * math.pi * k / 40 for k in range(40)]]
    hub = [P(cx_ + 0.5 * math.cos(a), 4.45, cz_ + 0.5 * math.sin(a)) for a in [2 * math.pi * k / 24 for k in range(24)]]
    o.append(poly(ring, "spool"))
    o.append(f'<path class="spoolf" d="{_d(ring)}"/>')
    o.append(poly(hub, "spoolh"))
    e1, e2 = P(4.5, 4.45, cz_ - 1.45), P(0.3, 4.45, 9.3)
    o.append(f'<path class="fil" d="M{e1[0]:.1f},{e1[1]:.1f} Q{e1[0]-60:.1f},{e1[1]+10:.1f} {e2[0]:.1f},{e2[1]:.1f}"/>')
    o.append(box(-0.25, 0.3, 4.1, 4.8, 8.8, 9.6, P, "mo1", "mo2", "mo3"))         # extruder on the frame
    # bed group (bed slinger): carriage, springs, PEI sheet, printed part
    bed = box(1.0, 8.0, 1.0, 8.0, 1.55, 1.7, P, "bd1", "bd2", "bd3")
    for kx, ky in ((1.4, 1.4), (7.6, 1.4), (1.4, 7.6), (7.6, 7.6)):
        kx_, ky_ = P(kx, ky, 1.4)
        bed = f'<ellipse cx="{kx_:.1f}" cy="{ky_:.1f}" rx="7" ry="4" class="knob"/>' + bed
    sheet = poly(_rect(1.15, 7.85, 1.15, 7.85, 1.72, P), "pei")
    layers = []
    for i in range(PR3_N):
        z = 1.72 + (i + 1) * PR3_H
        layers.append(f'<path class="ly{i} lyr" fill-rule="evenodd" d="{fixture_layer(i, z, P)}"/>')
    o.append(f'<g class="bedy3">{bed}{sheet}{"".join(layers)}</g>')
    # X gantry + print head (fan, heater block, glowing nozzle) + Bowden tube
    zb = 1.72 + 1.35
    hd = lambda x, y, z: iso(x, y, z, s, 0, 0)
    head = (box(-0.65, 0.65, -0.55, 0.55, 0.45, 1.6, hd, "hd1", "hd2", "hd3")
            + box(-0.25, 0.25, -0.2, 0.2, 0.18, 0.45, hd, "hb1", "hb2", "hb3"))
    fc = iso(0, 0.55, 1.05, s, 0, 0)
    head += f'<ellipse cx="{fc[0]:.1f}" cy="{fc[1]:.1f}" rx="9" ry="10" class="fan"/><ellipse cx="{fc[0]:.1f}" cy="{fc[1]:.1f}" rx="3" ry="3.4" class="fanh"/>'
    head += poly([iso(-0.1, 0, 0.18, s, 0, 0), iso(0.1, 0, 0.18, s, 0, 0), iso(0, 0, 0, s, 0, 0)], "noz3")
    a, b = P(2.9, 4.45, zb - 1.35), P(6.1, 4.45, zb - 1.35)
    ex_ = P(0.0, 4.45, 9.2)
    top_a, top_b = (a[0], a[1] - 1.6 * s), (b[0], b[1] - 1.6 * s)
    tube = (f'<path class="tube" d="M{ex_[0]:.1f},{ex_[1]:.1f} C{ex_[0]+40:.1f},{ex_[1]-40:.1f} {top_a[0]:.1f},{top_a[1]-90:.1f} {top_a[0]:.1f},{top_a[1]:.1f}">'
            f'<animate attributeName="d" dur="1s" repeatCount="indefinite" keyTimes="0;0.5;1" calcMode="spline" keySplines="0.45 0 0.55 1;0.45 0 0.55 1" '
            f'values="M{ex_[0]:.1f},{ex_[1]:.1f} C{ex_[0]+40:.1f},{ex_[1]-40:.1f} {top_a[0]:.1f},{top_a[1]-90:.1f} {top_a[0]:.1f},{top_a[1]:.1f};'
            f'M{ex_[0]:.1f},{ex_[1]:.1f} C{ex_[0]+40:.1f},{ex_[1]-40:.1f} {top_b[0]:.1f},{top_b[1]-90:.1f} {top_b[0]:.1f},{top_b[1]:.1f};'
            f'M{ex_[0]:.1f},{ex_[1]:.1f} C{ex_[0]+40:.1f},{ex_[1]-40:.1f} {top_a[0]:.1f},{top_a[1]-90:.1f} {top_a[0]:.1f},{top_a[1]:.1f}"/></path>')
    o.append(f'<g class="gz3">{box(0.3, 8.7, 4.25, 4.65, zb, zb + 0.5, P, "ex1", "ex2", "ex3")}{tube}'
             f'<g>{head}<animateMotion dur="1s" repeatCount="indefinite" keyTimes="0;0.5;1" keyPoints="0;1;0" '
             f'calcMode="spline" keySplines="0.45 0 0.55 1;0.45 0 0.55 1" path="M{a[0]:.1f},{a[1]:.1f} L{b[0]:.1f},{b[1]:.1f}"/></g></g>')
    # right Z extrusion (front) + control box with knob
    o.append(box(8.1, 8.7, 4.0, 4.9, 1.15, 11.6, P, "ex1", "ex2", "ex3"))
    g1, g2 = P(8.4, 4.9, 1.2), P(8.4, 4.9, 11.5)
    o.append(f'<line class="groove" x1="{g1[0]:.1f}" y1="{g1[1]:.1f}" x2="{g2[0]:.1f}" y2="{g2[1]:.1f}"/>')
    o.append(box(6.5, 8.7, 9.0, 9.45, 0.3, 1.15, P, "fr1", "scr3", "fr3"))
    kx_, ky_ = P(8.3, 9.45, 0.7)
    o.append(f'<circle cx="{kx_:.1f}" cy="{ky_:.1f}" r="4.5" class="knob2"/>')
    o.append("</svg>")
    return "".join(o)


def printer3_css():
    T, N, h = PR3_T, PR3_N, PR3_H * 24
    tp = T * 0.8
    css = []
    for i in range(N):
        on = (i + 1) * tp / N
        css.append(f"@keyframes l3_{i}{{0%,{pct(on-0.02,T)}{{opacity:0}}{pct(on,T)},96%{{opacity:1}}100%{{opacity:0}}}}"
                   f".pr3 .ly{i}{{animation:l3_{i} {T}s linear infinite}}")
    steps = []
    for i in range(N):
        t0 = i * tp / N
        steps.append(f"{pct(t0,T)},{pct(t0 + tp/N - 0.02,T)}{{transform:translateY({-i*h:.1f}px)}}")
    steps.append(f"{pct(tp,T)},96%{{transform:translateY({-N*h:.1f}px)}}100%{{transform:translateY(0)}}")
    css.append("@keyframes gz3{" + "".join(steps) + "}" + f".pr3 .gz3{{animation:gz3 {T}s linear infinite}}")
    dx, dy = -C30 * 24 * 0.9, S30 * 24 * 0.9
    css.append(f"@keyframes bedy3{{0%,100%{{transform:translate(0,0)}}50%{{transform:translate({dx:.1f}px,{dy:.1f}px)}}}}"
               ".pr3 .bedy3{animation:bedy3 1.4s ease-in-out infinite}")
    css.append(f"@keyframes pg3Bar{{0%{{transform:scaleX(0)}}80%,96%{{transform:scaleX(1)}}100%{{transform:scaleX(0)}}}}"
               f".prog3 i{{animation:pg3Bar {T}s linear infinite}}")
    css.append("""
.pr3{display:block;width:100%;height:auto;overflow:visible}
.pr3 .shdw{fill:#000;opacity:.3;filter:blur(10px)}
.pr3 .ft1,.pr3 .ft2,.pr3 .ft3{fill:#111317}
.pr3 .fr1{fill:#2C3037;stroke:#15171B;stroke-width:.7}.pr3 .fr2{fill:#1F2228;stroke:#15171B;stroke-width:.7}.pr3 .fr3{fill:#262A30;stroke:#15171B;stroke-width:.7}
.pr3 .ex1{fill:#3B4048;stroke:#1C1F24;stroke-width:.6}.pr3 .ex2{fill:url(#vsl);stroke:#1C1F24;stroke-width:.6}.pr3 .ex3{fill:#33373F;stroke:#1C1F24;stroke-width:.6}
.pr3 .groove{stroke:#15171B;stroke-width:2}
.pr3 .screw{stroke:#B9BEC6;stroke-width:2.4;stroke-dasharray:2 2;animation:screwTurn .6s linear infinite}
@keyframes screwTurn{to{stroke-dashoffset:-4}}
.pr3 .mo1{fill:#2A2D33}.pr3 .mo2{fill:#1C1E22}.pr3 .mo3{fill:#24272C}
.pr3 .bd1{fill:#B7BDC6;stroke:#6B717A;stroke-width:.6}.pr3 .bd2{fill:#8C939D}.pr3 .bd3{fill:#A2A9B3}
.pr3 .pei{fill:url(#pei);stroke:#3A3E45;stroke-width:.6}
.pr3 .knob{fill:#D9B44A;stroke:#8A6E1E}
.pr3 .hd1{fill:#2F343B;stroke:#15171B;stroke-width:.6}.pr3 .hd2{fill:#23272D;stroke:#15171B;stroke-width:.6}.pr3 .hd3{fill:#2A2E34;stroke:#15171B;stroke-width:.6}
.pr3 .hb1,.pr3 .hb2,.pr3 .hb3{fill:#C7CCD3;stroke:#6B717A;stroke-width:.4}
.pr3 .fan{fill:#121417;stroke:#4A4F57;stroke-width:1}.pr3 .fanh{fill:#4A4F57}
.pr3 .noz3{fill:#E8A23A;filter:drop-shadow(0 0 3px #FF7A2A)}
.pr3 .tube{fill:none;stroke:#E9EEF3;stroke-opacity:.75;stroke-width:2.4}
.pr3 .fil{fill:none;stroke:var(--acc);stroke-width:1.4;stroke-opacity:.9}
.pr3 .spool{fill:var(--acc);fill-opacity:.9;stroke:#121417}
.pr3 .spoolf{fill:none;stroke:#FFFFFF;stroke-opacity:.35;stroke-width:1.2;stroke-dasharray:10 14;animation:spoolTurn 6s linear infinite}
.pr3 .spoolh{fill:#121417}
.pr3 .lyr{fill:var(--acc);stroke:rgba(0,0,0,.4);stroke-width:.45}
.pr3 .scr3{fill:#0E2A3A;stroke:#5AA9D6;stroke-width:.8}
.pr3 .knob2{fill:#1A1D21;stroke:#6B717A}
@media (prefers-reduced-motion:reduce){.pr3 *{animation:none!important}.pr3 .lyr{opacity:1}}
""")
    return "\n".join(css)


# =====================================================================
# Footer factory v3 (deep review): correct saw-tooth roof with glazing,
# office annex, loading dock, warehouse with pitched roof, conveyor in
# the gap, tank, road with verge, lamps, shadows, distant turbines.
# =====================================================================
def footer3_scene(dark=True):
    s, ox, oy = 24, 6, 186
    leaf, leaf2 = ("#3E9E6E", "#2C7350") if dark else ("#4BA373", "#2F7A54")

    def O(x, y, z):
        return (ox + x * s + y * s * 0.5, oy - z * s - y * s * 0.3)

    def pts(lst):
        return " ".join(f"{a:.1f},{b:.1f}" for a, b in lst)

    def pg(lst, cls):
        # building faces get an opaque underlay so walls are solid, not see-through
        under = f'<polygon class="bgf" points="{pts(lst)}"/>' if cls.split()[0] in ("w-f", "w-f2", "w-s", "w-t", "o-f", "o-s", "o-t", "rf1", "glz") else ""
        return under + f'<polygon class="{cls}" points="{pts(lst)}"/>'

    def blk(x0, x1, y0, y1, z0, z1, f="w-f", r="w-s", t="w-t"):
        F = [O(x0, y0, z0), O(x1, y0, z0), O(x1, y0, z1), O(x0, y0, z1)]
        R = [O(x1, y0, z0), O(x1, y1, z0), O(x1, y1, z1), O(x1, y0, z1)]
        T = [O(x0, y0, z1), O(x1, y0, z1), O(x1, y1, z1), O(x0, y1, z1)]
        return pg(F, f) + pg(R, r) + pg(T, t)

    def shadow(x0, x1, y0, y1, h):            # soft shadow thrown to the right/back
        k = 0.55 * h
        return pg([O(x1, y0, 0), O(x1 + k, y0 + 0.2, 0), O(x1 + k, y1 + 0.2, 0), O(x1, y1, 0)], "shd")

    def tree(x, y, h=1.5, r=0.55):
        bx, by = O(x, y, 0); cx, cy = O(x, y, h)
        R = r * s
        return (f'<ellipse cx="{bx+7:.1f}" cy="{by+1:.1f}" rx="{R*0.95:.1f}" ry="{R*0.28:.1f}" class="shd"/>'
                f'<line x1="{bx:.1f}" y1="{by:.1f}" x2="{cx:.1f}" y2="{cy:.1f}" class="trunk"/>'
                f'<circle cx="{cx-R*0.38:.1f}" cy="{cy+R*0.15:.1f}" r="{R*0.72:.1f}" fill="{leaf2}"/>'
                f'<circle cx="{cx+R*0.38:.1f}" cy="{cy+R*0.1:.1f}" r="{R*0.75:.1f}" fill="{leaf2}"/>'
                f'<circle cx="{cx:.1f}" cy="{cy-R*0.35:.1f}" r="{R*0.8:.1f}" fill="{leaf}"/>'
                f'<circle cx="{cx-R*0.25:.1f}" cy="{cy-R*0.6:.1f}" r="{R*0.3:.1f}" fill="#FFFFFF" fill-opacity=".12"/>')

    W = 640
    o = [f'<svg class="fs3" viewBox="0 0 {W} 210" preserveAspectRatio="xMaxYMax meet" role="img" '
         'aria-label="Green factory: solar saw-tooth roof, office, loading dock, warehouse, conveyor, rain-water tank, wind turbines and a delivery truck">',
         '<defs><linearGradient id="hl3" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#3E9E6E" stop-opacity=".30"/>'
         '<stop offset="1" stop-color="#3E9E6E" stop-opacity=".04"/></linearGradient>'
         '<linearGradient id="pv3" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#34557F"/><stop offset="1" stop-color="#1A2C49"/></linearGradient>'
         '<linearGradient id="glint3" x1="0" x2="1"><stop offset="0" stop-color="#FFFFFF" stop-opacity="0"/>'
         '<stop offset=".5" stop-color="#FFFFFF" stop-opacity=".55"/><stop offset="1" stop-color="#FFFFFF" stop-opacity="0"/></linearGradient>'
         '<clipPath id="pvclip3"><rect x="0" y="0" width="640" height="210"/></clipPath></defs>']
    # ---- far: hills with three small turbines (distance = smaller)
    o.append(f'<path d="M250 118 C320 92 380 96 430 108 C480 86 560 84 {W} 100 L{W} 150 L250 150 Z" fill="url(#hl3)"/>')
    for k, (tx, ty, th) in enumerate(((470, 104, 50), (540, 96, 58), (606, 100, 46))):
        L = th * 0.42
        blades = "".join(
            f'<path d="M{tx:.1f},{ty-th:.1f} L{tx + L*math.cos(math.radians(a)) + 1.6*math.sin(math.radians(a)):.1f},{ty-th + L*math.sin(math.radians(a)) - 1.6*math.cos(math.radians(a)):.1f} '
            f'L{tx + L*math.cos(math.radians(a)):.1f},{ty-th + L*math.sin(math.radians(a)):.1f} Z"/>' for a in (-90, 30, 150))
        o.append(f'<polygon class="tw3" points="{tx-2:.1f},{ty:.1f} {tx+2:.1f},{ty:.1f} {tx+0.8:.1f},{ty-th:.1f} {tx-0.8:.1f},{ty-th:.1f}"/>'
                 f'<g class="bl3 b{k}" style="transform-origin:{tx:.1f}px {ty-th:.1f}px">{blades}</g>'
                 f'<circle cx="{tx:.1f}" cy="{ty-th:.1f}" r="2" class="hub3"/>')
    # ---- ground: yard, verge, sidewalk, road
    o.append(pg([O(-1, -2.2, 0), O(26, -2.2, 0), O(26, 5, 0), O(-1, 5, 0)], "yard"))
    o.append(pg([O(-1, -0.9, 0), O(26, -0.9, 0), O(26, -0.35, 0), O(-1, -0.35, 0)], "verge"))
    o.append(pg([O(-1, -2.2, 0), O(26, -2.2, 0), O(26, -0.9, 0), O(-1, -0.9, 0)], "road3"))
    ra, rb = O(-1, -1.55, 0), O(26, -1.55, 0)
    o.append(f'<line class="lane" x1="{ra[0]:.1f}" y1="{ra[1]:.1f}" x2="{rb[0]:.1f}" y2="{rb[1]:.1f}"/>')
    # ---- shadows first (on the ground)
    o.append(shadow(1.5, 10, 1.2, 4.2, 2.6) + shadow(12.2, 17, 1.4, 4.0, 2.3))
    # ---- main hall with a correct saw-tooth roof
    H, D0, D1 = 2.2, 1.2, 4.2
    o.append(blk(1.5, 10, D0, D1, 0, H))
    w, h = 2.125, 0.85
    for k in range(4):
        x0, x1 = 1.5 + k * w, 1.5 + (k + 1) * w
        glass = [O(x1, D0, H), O(x1, D1, H), O(x1, D1, H + h), O(x1, D0, H + h)]        # north glazing
        o.append(pg(glass, "glz"))
        slope = [O(x0, D0, H), O(x1, D0, H + h), O(x1, D1, H + h), O(x0, D1, H)]          # PV slope
        o.append(f'<polygon class="pv3" points="{pts(slope)}"/>')
        for c in range(1, 4):
            a = O(x0 + c * w / 4, D0, H + c * h / 4); b = O(x0 + c * w / 4, D1, H + c * h / 4)
            o.append(f'<line class="cell3" x1="{a[0]:.1f}" y1="{a[1]:.1f}" x2="{b[0]:.1f}" y2="{b[1]:.1f}"/>')
        for c in range(1, 4):
            yy = D0 + c * (D1 - D0) / 4
            a = O(x0, yy, H); b = O(x1, yy, H + h)
            o.append(f'<line class="cell3" x1="{a[0]:.1f}" y1="{a[1]:.1f}" x2="{b[0]:.1f}" y2="{b[1]:.1f}"/>')
        o.append(f'<polygon class="glint g{k}" points="{pts(slope)}"/>')
        o.append(pg([O(x0, D0, H), O(x1, D0, H), O(x1, D0, H + h)], "w-f2"))             # front gable
    # roll-up doors with dock bumpers on the hall front
    for k, dx in enumerate((5.4, 7.7)):
        a, b = O(dx, D0, 0), O(dx + 1.6, D0, 1.45)
        o.append(f'<rect x="{a[0]:.1f}" y="{b[1]:.1f}" width="{b[0]-a[0]:.1f}" height="{a[1]-b[1]:.1f}" class="door3"/>')
        for r_ in range(1, 7):
            yy = a[1] - r_ * (a[1] - b[1]) / 7
            o.append(f'<line x1="{a[0]:.1f}" y1="{yy:.1f}" x2="{b[0]:.1f}" y2="{yy:.1f}" class="rib3"/>')
        o.append(f'<rect x="{a[0]-3:.1f}" y="{a[1]-8:.1f}" width="3" height="8" class="bump"/><rect x="{b[0]:.1f}" y="{a[1]-8:.1f}" width="3" height="8" class="bump"/>')
    # high window band on the hall
    for k in range(6):
        a = O(5.3 + k * 0.75, D0, 1.75)
        o.append(f'<rect x="{a[0]:.1f}" y="{a[1]-6:.1f}" width="{0.5*s:.1f}" height="6" class="hw"/>')
    # office annex in front of the hall
    o.append(blk(1.5, 4.6, 0.15, D0, 0, 1.65, "o-f", "o-s", "o-t"))
    for row in range(2):
        for col in range(4):
            a = O(1.75 + col * 0.72, 0.15, 0.45 + row * 0.6)
            o.append(f'<rect x="{a[0]:.1f}" y="{a[1]-0.38*s:.1f}" width="{0.48*s:.1f}" height="{0.38*s:.1f}" class="win3 w{(row+col)%3}"/>')
    e1 = O(4.0, 0.15, 0)
    o.append(f'<rect x="{e1[0]:.1f}" y="{e1[1]-0.85*s:.1f}" width="{0.45*s:.1f}" height="{0.85*s:.1f}" class="entry"/>')
    o.append(pg([O(3.8, -0.25, 1.0), O(4.75, -0.25, 1.0), O(4.75, 0.15, 1.0), O(3.8, 0.15, 1.0)], "canopy"))
    # conveyor in the gap between hall and warehouse (moving crates)
    for lx in (10.4, 11.9):
        o.append(blk(lx, lx + 0.12, 2.35, 2.47, 0, 0.8, "m-f", "m-s", "m-t"))
    o.append(blk(10.0, 12.2, 2.2, 2.75, 0.8, 0.95, "m-f", "m-s", "b-t"))
    pa, pb = O(10.05, 2.3, 0.95), O(11.75, 2.3, 0.95)
    cw, ch, cd = 0.42 * s, 0.32 * s, 0.35
    crate = (f'<rect x="0" y="{-ch:.1f}" width="{cw:.1f}" height="{ch:.1f}" class="cr-f"/>'
             f'<polygon class="cr-t" points="0,{-ch:.1f} {cw:.1f},{-ch:.1f} {cw+cd*s*0.5:.1f},{-ch-cd*s*0.3:.1f} {cd*s*0.5:.1f},{-ch-cd*s*0.3:.1f}"/>'
             f'<polygon class="cr-s" points="{cw:.1f},0 {cw+cd*s*0.5:.1f},{-cd*s*0.3:.1f} {cw+cd*s*0.5:.1f},{-ch-cd*s*0.3:.1f} {cw:.1f},{-ch:.1f}"/>')
    for k in range(2):
        o.append(f'<g>{crate}<animateMotion dur="3.6s" begin="-{k*1.8:.1f}s" repeatCount="indefinite" path="M{pa[0]:.1f},{pa[1]:.1f} L{pb[0]:.1f},{pb[1]:.1f}"/></g>')
    # warehouse with a pitched roof
    WX0, WX1, WY0, WY1, WH, RH = 12.2, 17.0, 1.4, 4.0, 1.8, 0.55
    o.append(blk(WX0, WX1, WY0, WY1, 0, WH))
    ym = (WY0 + WY1) / 2
    o.append(pg([O(WX0, WY0, WH), O(WX1, WY0, WH), O(WX1, ym, WH + RH), O(WX0, ym, WH + RH)], "rf1"))
    o.append(pg([O(WX1, WY0, WH), O(WX1, WY1, WH), O(WX1, ym, WH + RH)], "w-s"))
    for k in range(1, 8):                                   # standing-seam lines
        a, b = O(WX0 + k * 0.6, WY0, WH), O(WX0 + k * 0.6, ym, WH + RH)
        o.append(f'<line x1="{a[0]:.1f}" y1="{a[1]:.1f}" x2="{b[0]:.1f}" y2="{b[1]:.1f}" class="seam"/>')
    a, b = O(13.0, WY0, 0), O(14.8, WY0, 1.3)
    o.append(f'<rect x="{a[0]:.1f}" y="{b[1]:.1f}" width="{b[0]-a[0]:.1f}" height="{a[1]-b[1]:.1f}" class="door3"/>')
    for r_ in range(1, 6):
        yy = a[1] - r_ * (a[1] - b[1]) / 6
        o.append(f'<line x1="{a[0]:.1f}" y1="{yy:.1f}" x2="{b[0]:.1f}" y2="{yy:.1f}" class="rib3"/>')
    # rain-water tank
    tx, ty = O(18.4, 2.6, 0)
    rx, ry, th = 0.6 * s * 0.9, 0.6 * s * 0.35, 1.5 * s
    o.append(f'<ellipse cx="{tx+10:.1f}" cy="{ty+2:.1f}" rx="{rx*1.2:.1f}" ry="{ry:.1f}" class="shd"/>'
             f'<path class="tank" d="M{tx-rx:.1f},{ty:.1f} A{rx:.1f},{ry:.1f} 0 0 0 {tx+rx:.1f},{ty:.1f} V{ty-th:.1f} A{rx:.1f},{ry:.1f} 0 0 0 {tx-rx:.1f},{ty-th:.1f} Z"/>'
             f'<ellipse cx="{tx:.1f}" cy="{ty-th:.1f}" rx="{rx:.1f}" ry="{ry:.1f}" class="tanktop"/>')
    for k in range(1, 4):
        o.append(f'<path class="tankr" d="M{tx-rx:.1f},{ty-k*th/4:.1f} A{rx:.1f},{ry:.1f} 0 0 0 {tx+rx:.1f},{ty-k*th/4:.1f}"/>')
    # front trees and street lamps along the verge
    for x in (1.0, 10.9, 21.4, 24.6):      # kept clear of the edge and of the tank
        o.append(tree(x, -0.6))
    for x in (6.2, 15.6):
        a, b = O(x, -0.55, 0), O(x, -0.55, 2.2)
        o.append(f'<line x1="{a[0]:.1f}" y1="{a[1]:.1f}" x2="{b[0]:.1f}" y2="{b[1]:.1f}" class="lp"/>'
                 f'<line x1="{b[0]:.1f}" y1="{b[1]:.1f}" x2="{b[0]+8:.1f}" y2="{b[1]+2:.1f}" class="lp"/>'
                 f'<circle cx="{b[0]+8:.1f}" cy="{b[1]+3:.1f}" r="2.2" class="lpl"/>')
    # delivery truck on the road (with a shadow)
    rp1, rp2 = O(-6, -1.35, 0), O(28, -1.35, 0)
    truck = ('<ellipse cx="30" cy="3" rx="36" ry="3.5" class="shd"/>'
             '<rect x="0" y="-21" width="44" height="21" rx="1.5" class="trl3"/>'
             '<rect x="0" y="-9" width="44" height="2.4" class="trs3"/>'
             + "".join(f'<line x1="{5+i*7}" y1="-20" x2="{5+i*7}" y2="-1" class="trrib3"/>' for i in range(6))
             + '<path d="M46 -15 H56 L61 -8 V0 H46 Z" class="cab3"/><path d="M49 -13 H55 L58.5 -8 H49 Z" class="cabw3"/>'
             '<circle cx="9" cy="1" r="3.6" class="wh3"/><circle cx="34" cy="1" r="3.6" class="wh3"/><circle cx="54" cy="1" r="3.6" class="wh3"/>')
    o.append(f'<g>{truck}<animateMotion dur="15s" repeatCount="indefinite" path="M{rp1[0]:.1f},{rp1[1]:.1f} L{rp2[0]:.1f},{rp2[1]:.1f}"/></g>')
    o.append("</svg>")
    return "".join(o)


FOOT3_CSS = """
.fs3 .bgf{fill:var(--bg);stroke:none}
.fs3{display:block;width:100%;height:auto}
.fs3 .yard{fill:var(--strong);fill-opacity:.045}
.fs3 .verge{fill:#3E9E6E;fill-opacity:.28}
.fs3 .road3{fill:var(--strong);fill-opacity:.10}
.fs3 .lane{stroke:#E8C15A;stroke-opacity:.7;stroke-width:1.2;stroke-dasharray:10 9}   /* road is still; only the truck moves */
.fs3 .shd{fill:#000;fill-opacity:.22}
.fs3 .w-f{fill:var(--strong);fill-opacity:.13;stroke:var(--line2);stroke-width:.7}
.fs3 .w-f2{fill:var(--strong);fill-opacity:.15;stroke:var(--line2);stroke-width:.7}
.fs3 .w-s{fill:var(--strong);fill-opacity:.07;stroke:var(--line2);stroke-width:.7}
.fs3 .w-t{fill:var(--strong);fill-opacity:.2;stroke:var(--line2);stroke-width:.7}
.fs3 .o-f{fill:var(--strong);fill-opacity:.2;stroke:var(--line2);stroke-width:.7}
.fs3 .o-s{fill:var(--strong);fill-opacity:.1;stroke:var(--line2);stroke-width:.7}
.fs3 .o-t{fill:var(--strong);fill-opacity:.26;stroke:var(--line2);stroke-width:.7}
.fs3 .glz{fill:#8FB8E0;fill-opacity:.35;stroke:var(--line2);stroke-width:.6}
.fs3 .pv3{fill:url(#pv3);stroke:#7FA3D8;stroke-opacity:.55;stroke-width:.6}
.fs3 .cell3{stroke:#A9C2E6;stroke-opacity:.28;stroke-width:.5}
.fs3 .glint{fill:url(#glint3);opacity:0;animation:glint3 8s ease-in-out infinite}
.fs3 .g1{animation-delay:.35s}.fs3 .g2{animation-delay:.7s}.fs3 .g3{animation-delay:1.05s}
@keyframes glint3{0%,72%,100%{opacity:0}80%{opacity:.7}88%{opacity:0}}
.fs3 .door3{fill:var(--strong);fill-opacity:.16;stroke:var(--line2);stroke-width:.6}
.fs3 .rib3{stroke:var(--line2);stroke-width:.5}
.fs3 .bump{fill:#1E2126}
.fs3 .hw{fill:#F2C46B;fill-opacity:.5}
.fs3 .win3{fill:#F2C46B;fill-opacity:.62}
.fs3 .win3.w1{fill-opacity:.3}.fs3 .win3.w2{animation:winFlick 9s ease-in-out infinite}
.fs3 .entry{fill:#8FB8E0;fill-opacity:.55;stroke:var(--line2);stroke-width:.5}
.fs3 .canopy{fill:var(--acc);fill-opacity:.85}
.fs3 .m-f,.fs3 .m-s,.fs3 .m-t{fill:#9AA1AB;stroke:#5E646D;stroke-width:.4}
.fs3 .b-t{fill:#2B2F36;stroke:#1E2126;stroke-width:.5}
.fs3 .cr-f{fill:#B9895A;stroke:#7A5634;stroke-width:.5}.fs3 .cr-t{fill:#D2A274;stroke:#7A5634;stroke-width:.5}.fs3 .cr-s{fill:#9E7349;stroke:#7A5634;stroke-width:.5}
.fs3 .rf1{fill:var(--strong);fill-opacity:.22;stroke:var(--line2);stroke-width:.7}
.fs3 .seam{stroke:var(--line2);stroke-width:.5}
.fs3 .tank{fill:#A9BCCF;stroke:#5F7287;stroke-width:.6}
.fs3 .tanktop{fill:#C9D6E3;stroke:#5F7287;stroke-width:.6}
.fs3 .tankr{fill:none;stroke:#5F7287;stroke-width:.7;stroke-opacity:.8}
.fs3 .trunk{stroke:#6B5444;stroke-width:2.2}
.fs3 .lp{stroke:var(--strong);stroke-opacity:.55;stroke-width:1.4}
.fs3 .lpl{fill:#F2C46B}
.fs3 .tw3{fill:var(--strong);fill-opacity:.5}
.fs3 .bl3 path{fill:var(--strong);fill-opacity:.75}
.fs3 .bl3{animation:bladeSpin 5s linear infinite}.fs3 .b1{animation-duration:6.2s}.fs3 .b2{animation-duration:5.6s}
.fs3 .hub3{fill:var(--strong)}
.fs3 .trl3{fill:#E9ECEF;stroke:#9AA1AB;stroke-width:.6}.fs3 .trs3{fill:var(--acc)}.fs3 .trrib3{stroke:#000;stroke-opacity:.12}
.fs3 .cab3{fill:var(--acc)}.fs3 .cabw3{fill:#9CC3E6;fill-opacity:.85}
.fs3 .wh3{fill:#16181B;stroke:#8A9099;stroke-width:1.3}
@media (prefers-reduced-motion:reduce){.fs3 *{animation:none!important}}
"""


# =====================================================================
# Sewing line v4 (Zaid: "aro realistic"): seated operators with arms on
# the work, lockstitch machines with thread stands and hand wheels, servo
# motors under the tables, pendant lights, chairs and mats, a bundle
# trolley at the bottleneck and a tote of finished T-shirts.
# =====================================================================
def sewing4_svg(hero=False):
    s, ox, oy = 26, 250, 205
    P = lambda x, y, z: iso(x, y, z, s, ox, oy)
    o = ['<svg class="sw4" viewBox="0 0 860 515" role="img" aria-label="T-shirt sewing line: four seated operators at lockstitch machines; bundles move on a conveyor and wait at the bottleneck">',
         '<defs><radialGradient id="pool4"><stop offset="0" stop-color="#FFE7B0" stop-opacity=".55"/><stop offset="1" stop-color="#FFE7B0" stop-opacity="0"/></radialGradient></defs>']
    o.append(poly([P(-2, -6.5, 0), P(23.5, -6.5, 0), P(23.5, 3.8, 0), P(-2, 3.8, 0)], "fl4"))
    for x in range(-2, 24, 2):
        a, b = P(x, -6.5, 0), P(x, 3.8, 0)
        o.append(f'<line class="tile" x1="{a[0]:.1f}" y1="{a[1]:.1f}" x2="{b[0]:.1f}" y2="{b[1]:.1f}"/>')
    for y in (-6.5, -4.5, -2.5, -0.5, 1.5):
        a, b = P(-2, y, 0), P(23.5, y, 0)
        o.append(f'<line class="tile" x1="{a[0]:.1f}" y1="{a[1]:.1f}" x2="{b[0]:.1f}" y2="{b[1]:.1f}"/>')
    o.append(poly([P(-2, 3.0, 0), P(23.5, 3.0, 0), P(23.5, 3.25, 0), P(-2, 3.25, 0)], "aisle4"))
    items = []

    def add(x0, x1, y0, y1, z0, z1, c, depth=None):
        d = depth if depth is not None else (x0 + x1) / 2 + (y0 + y1) / 2 + z0 * 0.02
        items.append((d, box(x0, x1, y0, y1, z0, z1, P, c + "1", c + "2", c + "3")))

    def raw(depth, svg):
        items.append((depth, svg))

    stations = [3, 8, 13, 18]
    for i, c in enumerate(stations):
        hot = i == 2
        # anti-fatigue mat + chair
        raw(c - 5.0 - 2, poly([P(c - 0.9, -5.3, 0.01), P(c + 0.9, -5.3, 0.01), P(c + 0.9, -3.6, 0.01), P(c - 0.9, -3.6, 0.01)], "mat4"))
        add(c - 0.45, c + 0.45, -5.0, -4.85, 1.0, 2.2, "ch")              # backrest
        add(c - 0.08, c + 0.08, -4.5, -4.35, 0, 0.9, "mt")                 # chair column
        add(c - 0.5, c + 0.5, -4.85, -4.0, 0.9, 1.02, "ch")                # seat
        # operator: legs under the table, torso, arms on the work, head
        add(c - 0.42, c - 0.08, -4.1, -3.15, 1.02, 1.28, "pt")             # left thigh
        add(c + 0.08, c + 0.42, -4.1, -3.15, 1.02, 1.28, "pt")             # right thigh
        add(c - 0.4, c - 0.1, -3.3, -3.05, 0, 1.02, "pt")                  # left shin
        add(c + 0.1, c + 0.4, -3.3, -3.05, 0, 1.02, "pt")                  # right shin
        add(c - 0.52, c + 0.52, -4.55, -3.95, 1.28, 2.55, "cl", depth=c - 4.25 + 0.4)   # torso
        add(c - 0.62, c - 0.42, -4.3, -3.7, 1.95, 2.45, "cl", depth=c - 4.0 + 0.45)    # upper arms
        add(c + 0.42, c + 0.62, -4.3, -3.7, 1.95, 2.45, "cl", depth=c - 4.0 + 0.45)
        fa = (box(c - 0.62, c - 0.42, -3.75, -2.7, 1.8, 1.98, P, "sk1", "sk2", "sk3")
              + box(c + 0.2, c + 0.4, -3.75, -2.7, 1.8, 1.98, P, "sk1", "sk2", "sk3"))
        raw(c - 3.2 + 0.6, f'<g class="hands h{i}">{fa}</g>')                 # forearms guide the fabric
        hx, hy = P(c, -4.25, 2.95)
        nx, ny = P(c, -4.25, 2.55)
        raw(c - 4.25 + 0.5, f'<line x1="{nx:.1f}" y1="{ny:.1f}" x2="{hx:.1f}" y2="{hy+6:.1f}" class="neck4"/>'
                            f'<circle class="skin4" cx="{hx:.1f}" cy="{hy:.1f}" r="{0.36*s:.1f}"/>'
                            f'<path class="hair4" d="M{hx-0.37*s:.1f},{hy+1:.1f} a{0.37*s:.1f},{0.37*s:.1f} 0 0 1 {0.74*s:.1f},0 q{-0.1*s:.1f},{-0.12*s:.1f} {-0.37*s:.1f},{-0.14*s:.1f} q{-0.27*s:.1f},{0.02*s:.1f} {-0.37*s:.1f},{0.14*s:.1f} Z"/>')
        # table: legs, under-table servo motor, top with a warm light pool
        for lx in (c - 1.45, c + 1.33):
            for ly in (-3.35, -1.37):
                add(lx, lx + 0.12, ly, ly + 0.12, 0, 1.5, "mt")
        add(c + 0.55, c + 1.05, -2.45, -1.95, 1.08, 1.42, "mo")
        add(c - 1.5, c + 1.5, -3.4, -1.25, 1.5, 1.62, "tb", depth=c - 2.3 + 0.3)
        pc = P(c - 0.1, -2.3, 1.63)
        raw(c - 2.3 + 0.31, f'<ellipse cx="{pc[0]:.1f}" cy="{pc[1]:.1f}" rx="{1.5*s:.1f}" ry="{0.75*s:.1f}" fill="url(#pool4)"/>')
        # lockstitch machine: bed, pillar, arm, head, needle, hand wheel, thread stand with cones
        dm = c - 2.3 + 0.35
        raw(dm, box(c - 0.95, c + 0.95, -2.78, -1.95, 1.62, 1.78, P, "mc1", "mc2", "mc3"))
        raw(dm + 0.01, box(c + 0.42, c + 0.85, -2.68, -2.05, 1.78, 2.95, P, "mc1", "mc2", "mc3"))
        raw(dm + 0.02, box(c - 0.85, c + 0.85, -2.66, -2.08, 2.72, 3.12, P, "mc1", "mc2", "mc3"))
        raw(dm + 0.03, box(c - 0.85, c - 0.45, -2.68, -2.05, 2.28, 2.75, P, "mc1", "mc2", "mc3"))
        n1, n2 = P(c - 0.65, -2.36, 2.28), P(c - 0.65, -2.36, 1.8)
        raw(dm + 0.04, f'<line class="needle" x1="{n1[0]:.1f}" y1="{n1[1]:.1f}" x2="{n2[0]:.1f}" y2="{n2[1]:.1f}"/>')
        raw(dm + 0.05, box(c - 1.05, c - 0.15, -2.15, -1.55, 1.78, 1.83, P, "fb1", "fb2", "fb3"))
        wx, wy = P(c + 0.9, -2.36, 2.6)
        raw(dm + 0.06, f'<ellipse class="wheel4" cx="{wx:.1f}" cy="{wy:.1f}" rx="4.5" ry="8"/><line class="spoke4" x1="{wx:.1f}" y1="{wy-7:.1f}" x2="{wx:.1f}" y2="{wy+7:.1f}" style="transform-origin:{wx:.1f}px {wy:.1f}px"/>')
        t1, t2 = P(c + 1.25, -3.15, 1.62), P(c + 1.25, -3.15, 3.9)
        cones = ""
        for k, col in enumerate(("#E9D7A8", "#7FA7D9")):
            cx_, cy_ = P(c + 1.0 + k * 0.5, -3.15, 3.55)
            cones += f'<path class="cone" fill="{col}" d="M{cx_-4:.1f},{cy_:.1f} L{cx_+4:.1f},{cy_:.1f} L{cx_+2.2:.1f},{cy_-11:.1f} L{cx_-2.2:.1f},{cy_-11:.1f} Z"/>'
        a1, a2 = P(c + 0.9, -3.15, 3.55), P(c + 1.6, -3.15, 3.55)
        raw(c - 3.15 + 1.9, f'<line class="pole4" x1="{t1[0]:.1f}" y1="{t1[1]:.1f}" x2="{t2[0]:.1f}" y2="{t2[1]:.1f}"/>'
                            f'<line class="pole4" x1="{a1[0]:.1f}" y1="{a1[1]:.1f}" x2="{a2[0]:.1f}" y2="{a2[1]:.1f}"/>{cones}')
        # andon lamp + label
        px, py = P(c + 1.45, -1.4, 1.62)
        qx, qy = P(c + 1.45, -1.4, 2.9)
        lab = ""
        raw(c - 1.4 + 1.6, f'<line class="pole4" x1="{px:.1f}" y1="{py:.1f}" x2="{qx:.1f}" y2="{qy:.1f}"/>'
                           f'<circle class="lamp4{" on" if hot else ""}" cx="{qx:.1f}" cy="{qy:.1f}" r="5"/>{lab}')
    # bundle trolley at the bottleneck
    add(10.0, 11.7, 1.25, 2.45, 0.35, 0.45, "mt")
    for wx_ in (10.15, 11.45):
        for wy_ in (1.35, 2.25):
            c0 = P(wx_, wy_, 0.12)
            raw(wx_ + wy_ - 0.2, f'<circle class="cast" cx="{c0[0]:.1f}" cy="{c0[1]:.1f}" r="3"/>')
    add(10.05, 10.12, 1.3, 2.4, 0.45, 1.3, "mt")
    for k, z in enumerate((0.45, 0.62, 0.79)):
        add(10.25, 11.4, 1.45, 2.25, z, z + 0.15, "fb")
        tk = P(10.9, 2.25, z + 0.09)
        raw(10.9 + 2.25 + z + 0.1, f'<rect class="ticket" x="{tk[0]-4:.1f}" y="{tk[1]-3:.1f}" width="8" height="5"/>')
    if not hero:
        wx2, wy2 = P(10.8, 2.7, 0)
        raw(30, f'<text class="lb4" x="{wx2-12:.1f}" y="{wy2+16:.1f}">WIP · 3 BUNDLES</text>')
    # finished-goods tote at the outfeed
    add(21.9, 23.3, -0.9, 0.9, 0, 0.7, "tt")
    for k in range(3):
        add(22.1, 23.1, -0.7 + k * 0.5, -0.35 + k * 0.5, 0.7, 0.78 + k * 0.02, "ts")
    # conveyor: legs, side rails, rollers, belt
    for lx in (0, 5, 10, 15, 20):
        add(lx, lx + 0.15, -0.55, -0.4, 0, 0.75, "mt")
        add(lx, lx + 0.15, 0.4, 0.55, 0, 0.75, "mt")
    items.append((10.4, box(-1.5, 21.6, -0.65, 0.65, 0.75, 0.95, P, "bt1", "bt2", "bt3")))
    items.sort(key=lambda t: t[0])
    o += [svg for _, svg in items]
    a, b = P(-1.5, 0, 0.95), P(21.6, 0, 0.95)
    o.append(f'<line class="beltln4" x1="{a[0]:.1f}" y1="{a[1]:.1f}" x2="{b[0]:.1f}" y2="{b[1]:.1f}"/>')
    hd = lambda x, y, z: iso(x, y, z, s, 0, 0)
    bundle = (box(-0.45, 0.45, -0.35, 0.35, 0, 0.12, hd, "fb1", "fb2", "fb3")
              + box(-0.43, 0.43, -0.33, 0.33, 0.12, 0.24, hd, "fb1", "fb2", "fb3")
              + box(-0.4, 0.4, -0.3, 0.3, 0.24, 0.36, hd, "fb1", "fb2", "fb3"))
    tk = hd(0.1, 0.35, 0.18)
    bundle += f'<rect class="ticket" x="{tk[0]-4:.1f}" y="{tk[1]-3:.1f}" width="8" height="5"/>'
    start, end = P(-1.2, 0, 0.95), P(21.4, 0, 0.95)
    frac = lambda x: (x + 1.2) / 22.6
    seq, t = [(0.0, 0.0)], 0.0
    for c, dwell in zip(stations, [1.2, 1.25, 1.8, 1.4]):
        t += 1.3; seq.append((t, frac(c)))
        t += dwell; seq.append((t, frac(c)))
    t += 1.3; seq.append((t, 1.0))
    kt = ";".join(f"{x/t:.4f}" for x, _ in seq)
    kp = ";".join(f"{p:.4f}" for _, p in seq)
    for k in range(6):
        o.append(f'<g>{bundle}<animateMotion dur="{t:.2f}s" begin="-{k*t/6:.2f}s" repeatCount="indefinite" '
                 f'calcMode="linear" keyTimes="{kt}" keyPoints="{kp}" path="M{start[0]:.1f},{start[1]:.1f} L{end[0]:.1f},{end[1]:.1f}"/></g>')
    # pendant lights over each station (drawn last: they hang above everything)
    for i, c in enumerate(stations):
        top, lamp = P(c - 0.1, -2.3, 6.4), P(c - 0.1, -2.3, 4.7)
        if not hero:   # station names sit at the top of each lamp cord, clear of the machines
            o.append(f'<text class="{"h" if i == 2 else "s"} lb4" x="{top[0]+8:.1f}" y="{top[1]-12:.1f}">{SEW_OPS[i][0]} · {SEW_OPS[i][1]}</text>')
        o.append(f'<line class="cord" x1="{top[0]:.1f}" y1="{top[1]-20:.1f}" x2="{lamp[0]:.1f}" y2="{lamp[1]:.1f}"/>'
                 f'<path class="shade" d="M{lamp[0]-5:.1f},{lamp[1]:.1f} L{lamp[0]+5:.1f},{lamp[1]:.1f} L{lamp[0]+12:.1f},{lamp[1]+9:.1f} L{lamp[0]-12:.1f},{lamp[1]+9:.1f} Z"/>'
                 f'<ellipse class="bulb" cx="{lamp[0]:.1f}" cy="{lamp[1]+9:.1f}" rx="9" ry="2.4"/>')
    if not hero:
        ix, iy = P(-1.5, 1.0, 0)
        o.append(f'<text class="lb4" x="{ix-50:.1f}" y="{iy+22:.1f}">CUT PANELS IN</text>')
        ex, ey = P(22.6, 1.0, 0)
        o.append(f'<text class="lb4" x="{ex-24:.1f}" y="{ey+24:.1f}">T-SHIRTS OUT</text>')
    o.append("</svg>")
    return "".join(o)


SEW4_CSS = """
.sw4{display:block;width:100%;height:auto;overflow:visible}
.sw4 .fl4{fill:var(--strong);fill-opacity:.04;stroke:var(--line2);stroke-width:1}
.sw4 .tile{stroke:var(--line);stroke-width:.8}
.sw4 .aisle4{fill:#E8B83A;fill-opacity:.7}
.sw4 .mat4{fill:#1C1F24;fill-opacity:.85}
.sw4 .ch1{fill:#3A3F47}.sw4 .ch2{fill:#2A2E34}.sw4 .ch3{fill:#32363D}
.sw4 .mt1{fill:#B3B9C2}.sw4 .mt2{fill:#868D97}.sw4 .mt3{fill:#9CA3AD}
.sw4 .pt1{fill:#3E4656}.sw4 .pt2{fill:#2C3240}.sw4 .pt3{fill:#353C4A}
.sw4 .cl1{fill:#36A39B}.sw4 .cl2{fill:#21665F}.sw4 .cl3{fill:#2B857E}
.sw4 .sk1{fill:#D7A983}.sw4 .sk2{fill:#B9875F}.sw4 .sk3{fill:#C99A74}
.sw4 .skin4{fill:#C99A74}.sw4 .hair4{fill:#2A221D}.sw4 .neck4{stroke:#B9875F;stroke-width:5}
.sw4 .tb1{fill:#DCCFB5;stroke:#9C8F78;stroke-width:.5}.sw4 .tb2{fill:#B2A58C;stroke:#9C8F78;stroke-width:.5}.sw4 .tb3{fill:#C6B9A0;stroke:#9C8F78;stroke-width:.5}
.sw4 .mo1{fill:#2E3238}.sw4 .mo2{fill:#1F2227}.sw4 .mo3{fill:#272A30}
.sw4 .mc1{fill:#F1EEE6;stroke:#A39D90;stroke-width:.5}.sw4 .mc2{fill:#CBC5B8;stroke:#A39D90;stroke-width:.5}.sw4 .mc3{fill:#DDD8CD;stroke:#A39D90;stroke-width:.5}
.sw4 .needle{stroke:#4A4F57;stroke-width:1.6;stroke-dasharray:3 2;animation:needle4 .25s linear infinite}
@keyframes needle4{to{stroke-dashoffset:-5}}
.sw4 .wheel4{fill:#4D5258;stroke:#25282C}
.sw4 .spoke4{stroke:#9AA1AB;stroke-width:1.4;animation:wheel4 .5s linear infinite}
@keyframes wheel4{to{transform:rotate(360deg)}}
.sw4 .pole4{stroke:#8A9099;stroke-width:1.4}
.sw4 .cone{stroke:rgba(0,0,0,.3);stroke-width:.5}
.sw4 .fb1{fill:#5B7FB8;stroke:rgba(0,0,0,.25);stroke-width:.5}.sw4 .fb2{fill:#46679A;stroke:rgba(0,0,0,.25);stroke-width:.5}.sw4 .fb3{fill:#3D5C8C;stroke:rgba(0,0,0,.25);stroke-width:.5}
.sw4 .ticket{fill:#F4F1E8;stroke:#9C8F78;stroke-width:.5}
.sw4 .tt1{fill:#3E9E6E;fill-opacity:.9}.sw4 .tt2{fill:#2C7350}.sw4 .tt3{fill:#348A5F}
.sw4 .ts1{fill:#ECEFF3;stroke:#9AA1AB;stroke-width:.5}.sw4 .ts2,.sw4 .ts3{fill:#C9CED6}
.sw4 .bt1{fill:#2F343B;stroke:#1E2126;stroke-width:.6}.sw4 .bt2{fill:#9AA1AB;stroke:#5E646D;stroke-width:.5}.sw4 .bt3{fill:#B1B7C0;stroke:#5E646D;stroke-width:.5}
.sw4 .beltln4{stroke:#FFFFFF;stroke-opacity:.14;stroke-width:1.4;stroke-dasharray:4 12;animation:beltMove 1s linear infinite}
.sw4 .cast{fill:#1E2126}
.sw4 .lamp4{fill:#3FB47A;opacity:.9}.sw4 .lamp4.on{fill:#E0524A;animation:lampGlow 1.4s ease-in-out infinite}
.sw4 .hands{animation:hands4 1.1s ease-in-out infinite alternate}
.sw4 .h1{animation-delay:-.3s}.sw4 .h2{animation-delay:-.6s}.sw4 .h3{animation-delay:-.9s}
@keyframes hands4{from{transform:translate(-2px,1px)}to{transform:translate(3px,-1px)}}
.sw4 .cord{stroke:var(--strong);stroke-opacity:.35;stroke-width:1}
.sw4 .shade{fill:#3A3F47;stroke:#1E2126;stroke-width:.6}
.sw4 .bulb{fill:#FFE7B0}
.sw4 text.lb4{paint-order:stroke;stroke:var(--bg);stroke-width:4px;stroke-linejoin:round}
@media (prefers-reduced-motion:reduce){.sw4 *{animation:none!important}}
@media (max-width:760px){.sw4 text{display:none}}
"""


# =====================================================================
# Sewing line v5: every part drawn to one real-world scale (1 unit = 0.4 m)
#   table 1.2 x 0.55 m, top 0.75 m · machine bed 0.48 x 0.18 m, arm 0.3 m high
#   seated operator: seat 0.45 m, shoulders 0.42 m wide, head top ~1.3 m
#   conveyor 0.4 m wide, belt 0.8 m high · bundle 0.4 x 0.3 x 0.1 m
#   station pitch 1.6 m · lamp 2.2 m · tote 0.6 x 0.4 x 0.35 m
# =====================================================================
def sewing5_svg(hero=False):
    U = 0.4
    m = lambda v: v / U                       # metres -> drawing units
    s, ox, oy = 26, 196, 228
    P = lambda x, y, z: iso(x, y, z, s, ox, oy)
    o = ['<svg class="sw4" viewBox="0 0 860 590" role="img" aria-label="T-shirt sewing line drawn to scale: four seated operators at lockstitch machines; bundles move on a conveyor and wait at the bottleneck">',
         '<defs><radialGradient id="pool5"><stop offset="0" stop-color="#FFE7B0" stop-opacity=".5"/><stop offset="1" stop-color="#FFE7B0" stop-opacity="0"/></radialGradient></defs>']
    X0, X1, Y0, Y1 = -1.5, 20.5, -5.0, 3.4
    o.append(poly([P(X0, Y0, 0), P(X1, Y0, 0), P(X1, Y1, 0), P(X0, Y1, 0)], "fl4"))
    step = m(1.2)                                                     # 1.2 m floor tiles
    x = X0
    while x <= X1 + 1e-6:
        a, b = P(x, Y0, 0), P(x, Y1, 0)
        o.append(f'<line class="tile" x1="{a[0]:.1f}" y1="{a[1]:.1f}" x2="{b[0]:.1f}" y2="{b[1]:.1f}"/>'); x += step
    y = Y0
    while y <= Y1 + 1e-6:
        a, b = P(X0, y, 0), P(X1, y, 0)
        o.append(f'<line class="tile" x1="{a[0]:.1f}" y1="{a[1]:.1f}" x2="{b[0]:.1f}" y2="{b[1]:.1f}"/>'); y += step
    o.append(poly([P(X0, 2.75, 0), P(X1, 2.75, 0), P(X1, 2.95, 0), P(X0, 2.95, 0)], "aisle4"))

    items = []
    L = [0]          # drawing layer: back to front (operator, table, machine, conveyor, front items)

    def add(x0, x1, y0, y1, z0, z1, c, depth=None):
        d = depth if depth is not None else (x0 + x1) / 2 + (y0 + y1) / 2 + z0 * 0.01
        items.append((L[0] * 1000 + d, box(x0, x1, y0, y1, z0, z1, P, c + "1", c + "2", c + "3")))

    def raw(depth, svg):
        items.append((L[0] * 1000 + depth, svg))

    TOP = m(0.75)                     # table top height
    BELT = m(0.80)                    # belt height
    CY0, CY1 = -m(0.2), m(0.2)        # conveyor 0.4 m wide, centred on y = 0
    TY1 = CY0 - m(0.35)               # table front edge, 0.35 m behind the conveyor
    TY0 = TY1 - m(0.55)               # table depth 0.55 m
    stations = [2.5, 2.5 + m(1.6), 2.5 + 2 * m(1.6), 2.5 + 3 * m(1.6)]
    for i, c in enumerate(stations):
        hot = i == 2
        tw = m(1.2) / 2
        L[0] = 1
        # chair (behind the table), seat 0.45 m high
        sy = TY0 - m(0.30)
        raw(c + sy - 3, poly([P(c - m(0.45), sy - m(0.45), 0.01), P(c + m(0.45), sy - m(0.45), 0.01),
                              P(c + m(0.45), sy + m(0.35), 0.01), P(c - m(0.45), sy + m(0.35), 0.01)], "mat4"))
        add(c - m(0.04), c + m(0.04), sy - m(0.04), sy + m(0.04), 0, m(0.42), "mt")
        add(c - m(0.22), c + m(0.22), sy - m(0.24), sy + m(0.2), m(0.42), m(0.46), "ch")
        add(c - m(0.2), c + m(0.2), sy - m(0.27), sy - m(0.23), m(0.5), m(0.82), "ch")       # backrest
        # operator: thighs to knees under the table, shins, torso, arms, head
        hip_z, knee_y = m(0.48), TY0 + m(0.25)
        for sx in (-1, 1):
            x0_, x1_ = (c - m(0.17), c - m(0.03)) if sx < 0 else (c + m(0.03), c + m(0.17))
            add(x0_, x1_, sy - m(0.08), knee_y, hip_z, hip_z + m(0.13), "pt")
            add(x0_, x1_, knee_y - m(0.1), knee_y, 0, hip_z, "pt")
        add(c - m(0.21), c + m(0.21), sy - m(0.13), sy + m(0.05), hip_z, m(1.05), "cl", depth=c + sy + 0.6)      # torso
        for sx in (-1, 1):
            xa, xb = (c - m(0.25), c - m(0.19)) if sx < 0 else (c + m(0.19), c + m(0.25))
            add(xa, xb, sy - m(0.05), sy + m(0.2), m(0.78), m(1.02), "cl", depth=c + sy + 0.7)        # upper arms
        fa = (box(c - m(0.24), c - m(0.17), sy + m(0.18), TY0 + m(0.22), m(0.76), m(0.81), P, "sk1", "sk2", "sk3")
              + box(c + m(0.08), c + m(0.15), sy + m(0.18), TY0 + m(0.22), m(0.76), m(0.81), P, "sk1", "sk2", "sk3"))
        raw(c + TY0 + 0.05, f'<g class="hands h{i}">{fa}</g>')
        hx, hy = P(c, sy - m(0.04), m(1.17))
        r = m(0.11) * s
        raw(c + sy + 0.8, f'<circle class="skin4" cx="{hx:.1f}" cy="{hy:.1f}" r="{r:.1f}"/>'
                          f'<path class="hair4" d="M{hx-r:.1f},{hy+0.5:.1f} a{r:.1f},{r:.1f} 0 0 1 {2*r:.1f},0 q{-0.3*r:.1f},{-0.35*r:.1f} {-r:.1f},{-0.4*r:.1f} q{-0.7*r:.1f},{0.05*r:.1f} {-r:.1f},{0.4*r:.1f} Z"/>')
        # table: four legs, servo motor under it, top, light pool
        L[0] = 2
        for lx in (c - tw + m(0.03), c + tw - m(0.07)):
            for ly in (TY0 + m(0.03), TY1 - m(0.07)):
                add(lx, lx + m(0.04), ly, ly + m(0.04), 0, TOP - m(0.03), "mt")
        add(c + m(0.18), c + m(0.38), TY0 + m(0.15), TY0 + m(0.3), TOP - m(0.22), TOP - m(0.06), "mo")
        L[0] = 3
        add(c - tw, c + tw, TY0, TY1, TOP - m(0.03), TOP, "tb", depth=c + (TY0 + TY1) / 2 + 0.2)
        pc = P(c - m(0.1), (TY0 + TY1) / 2, TOP + 0.01)
        raw(c + (TY0 + TY1) / 2 + 0.21, f'<ellipse cx="{pc[0]:.1f}" cy="{pc[1]:.1f}" rx="{m(0.7)*s:.1f}" ry="{m(0.32)*s:.1f}" fill="url(#pool5)"/>')
        # lockstitch machine (bed 0.48 x 0.18 m; arm 0.3 m above the bed)
        L[0] = 4
        by0, by1 = TY0 + m(0.12), TY0 + m(0.30)
        dm = c + (by0 + by1) / 2 + 0.3
        raw(dm, box(c - m(0.24), c + m(0.24), by0, by1, TOP, TOP + m(0.03), P, "mc1", "mc2", "mc3"))
        raw(dm + 0.01, box(c + m(0.13), c + m(0.24), by0 + m(0.02), by1 - m(0.04), TOP + m(0.03), TOP + m(0.30), P, "mc1", "mc2", "mc3"))
        raw(dm + 0.02, box(c - m(0.22), c + m(0.24), by0 + m(0.02), by1 - m(0.04), TOP + m(0.24), TOP + m(0.33), P, "mc1", "mc2", "mc3"))
        raw(dm + 0.03, box(c - m(0.22), c - m(0.14), by0 + m(0.02), by1 - m(0.04), TOP + m(0.13), TOP + m(0.24), P, "mc1", "mc2", "mc3"))
        n1, n2 = P(c - m(0.18), (by0 + by1) / 2, TOP + m(0.13)), P(c - m(0.18), (by0 + by1) / 2, TOP + m(0.035))
        raw(dm + 0.04, f'<line class="needle" x1="{n1[0]:.1f}" y1="{n1[1]:.1f}" x2="{n2[0]:.1f}" y2="{n2[1]:.1f}"/>')
        raw(dm + 0.05, box(c - m(0.32), c - m(0.02), by1 - m(0.02), by1 + m(0.18), TOP + m(0.03), TOP + m(0.045), P, "fb1", "fb2", "fb3"))
        wx, wy = P(c + m(0.26), (by0 + by1) / 2, TOP + m(0.24))
        raw(dm + 0.06, f'<ellipse class="wheel4" cx="{wx:.1f}" cy="{wy:.1f}" rx="{m(0.035)*s:.1f}" ry="{m(0.07)*s:.1f}"/>'
                       f'<line class="spoke4" x1="{wx:.1f}" y1="{wy-m(0.06)*s:.1f}" x2="{wx:.1f}" y2="{wy+m(0.06)*s:.1f}" style="transform-origin:{wx:.1f}px {wy:.1f}px"/>')
        t1, t2 = P(c + m(0.45), TY0 + m(0.05), TOP), P(c + m(0.45), TY0 + m(0.05), TOP + m(0.55))
        cones = ""
        for k, col in enumerate(("#E9D7A8", "#7FA7D9")):
            cx_, cy_ = P(c + m(0.38) + k * m(0.14), TY0 + m(0.05), TOP + m(0.45))
            cones += f'<path class="cone" fill="{col}" d="M{cx_-3:.1f},{cy_:.1f} L{cx_+3:.1f},{cy_:.1f} L{cx_+1.6:.1f},{cy_-8:.1f} L{cx_-1.6:.1f},{cy_-8:.1f} Z"/>'
        a1, a2 = P(c + m(0.35), TY0 + m(0.05), TOP + m(0.45)), P(c + m(0.55), TY0 + m(0.05), TOP + m(0.45))
        raw(c + TY0 + 0.45, f'<line class="pole4" x1="{t1[0]:.1f}" y1="{t1[1]:.1f}" x2="{t2[0]:.1f}" y2="{t2[1]:.1f}"/>'
                            f'<line class="pole4" x1="{a1[0]:.1f}" y1="{a1[1]:.1f}" x2="{a2[0]:.1f}" y2="{a2[1]:.1f}"/>{cones}')
        # andon lamp on a short pole at the back-left corner of the table
        px, py = P(c - tw + m(0.06), TY0 + m(0.06), TOP)
        qx, qy = P(c - tw + m(0.06), TY0 + m(0.06), TOP + m(0.5))
        raw(c - tw + TY0 + 0.2, f'<line class="pole4" x1="{px:.1f}" y1="{py:.1f}" x2="{qx:.1f}" y2="{qy:.1f}"/>'
                               f'<circle class="lamp4{" on" if hot else ""}" cx="{qx:.1f}" cy="{qy:.1f}" r="4.2"/>')
    L[0] = 8
    # bundle trolley in front of S3 (0.8 x 0.5 m, platform 0.3 m) with 3 waiting bundles
    tx0 = stations[2] - m(0.95)
    add(tx0, tx0 + m(0.8), CY1 + m(0.35), CY1 + m(0.85), m(0.26), m(0.30), "mt")
    for wx_ in (tx0 + m(0.05), tx0 + m(0.75)):
        for wy_ in (CY1 + m(0.4), CY1 + m(0.8)):
            add(wx_ - m(0.015), wx_ + m(0.015), wy_ - m(0.015), wy_ + m(0.015), m(0.06), m(0.26), "mt", depth=wx_ + wy_ - 0.3)
            c0 = P(wx_, wy_, m(0.05))
            raw(wx_ + wy_ - 0.2, f'<circle class="cast" cx="{c0[0]:.1f}" cy="{c0[1]:.1f}" r="2.6"/>')
    add(tx0, tx0 + m(0.03), CY1 + m(0.35), CY1 + m(0.85), m(0.30), m(0.95), "mt")
    for k in range(3):
        z = m(0.30) + k * m(0.10)
        add(tx0 + m(0.15), tx0 + m(0.55), CY1 + m(0.45), CY1 + m(0.75), z, z + m(0.10), "fb")
    if not hero:
        wx2, wy2 = P(tx0 + m(0.4), CY1 + m(0.95), 0)
        raw(40, f'<text class="lb4" x="{wx2-14:.1f}" y="{wy2+16:.1f}">WIP · 3 BUNDLES</text>')
    # finished-goods tote (0.6 x 0.4 x 0.35 m) after the last station
    ex0 = stations[-1] + m(1.1)
    add(ex0, ex0 + m(0.6), CY1 + m(0.3), CY1 + m(0.7), 0, m(0.35), "tt")
    for k in range(2):
        add(ex0 + m(0.08), ex0 + m(0.52), CY1 + m(0.34), CY1 + m(0.66), m(0.35) + k * m(0.03), m(0.38) + k * m(0.03), "ts")
    # conveyor: legs every 1.2 m, frame, belt (0.8 m high)
    L[0] = 5
    xa, xb = -1.0, ex0 - m(0.2)
    lx = xa + 0.2
    while lx < xb:
        add(lx, lx + m(0.05), CY0 + m(0.02), CY0 + m(0.07), 0, BELT - m(0.06), "mt")
        lx += m(1.2)
    L[0] = 6
    items.append((6000, box(xa, xb, CY0, CY1, BELT - m(0.06), BELT, P, "bt1", "bt2", "bt3")))
    L[0] = 7
    lx = xa + 0.2
    while lx < xb:
        add(lx, lx + m(0.05), CY1 - m(0.07), CY1 - m(0.02), 0, BELT - m(0.06), "mt")
        lx += m(1.2)
    items.sort(key=lambda t: t[0])
    o += [svg for _, svg in items]
    a, b = P(xa, 0, BELT), P(xb, 0, BELT)
    o.append(f'<line class="beltln4" x1="{a[0]:.1f}" y1="{a[1]:.1f}" x2="{b[0]:.1f}" y2="{b[1]:.1f}"/>')
    hd = lambda x, y, z: iso(x, y, z, s, 0, 0)
    bw, bd, bh = m(0.4) / 2, m(0.3) / 2, m(0.1)
    bundle = (box(-bw, bw, -bd, bd, 0, bh * 0.5, hd, "fb1", "fb2", "fb3")
              + box(-bw * 0.95, bw * 0.95, -bd * 0.95, bd * 0.95, bh * 0.5, bh, hd, "fb1", "fb2", "fb3"))
    tk = hd(bw * 0.2, bd, bh * 0.5)
    bundle += f'<rect class="ticket" x="{tk[0]-3:.1f}" y="{tk[1]-2:.1f}" width="6" height="4"/>'
    start, end = P(xa + 0.3, 0, BELT), P(xb - 0.3, 0, BELT)
    span = (xb - 0.3) - (xa + 0.3)
    frac = lambda x: (x - (xa + 0.3)) / span
    seq, t = [(0.0, 0.0)], 0.0
    for c, dwell in zip(stations, [1.2, 1.25, 1.8, 1.4]):
        t += 1.3; seq.append((t, frac(c)))
        t += dwell; seq.append((t, frac(c)))
    t += 1.3; seq.append((t, 1.0))
    kt = ";".join(f"{x/t:.4f}" for x, _ in seq)
    kp = ";".join(f"{p:.4f}" for _, p in seq)
    for k in range(6):
        o.append(f'<g>{bundle}<animateMotion dur="{t:.2f}s" begin="-{k*t/6:.2f}s" repeatCount="indefinite" '
                 f'calcMode="linear" keyTimes="{kt}" keyPoints="{kp}" path="M{start[0]:.1f},{start[1]:.1f} L{end[0]:.1f},{end[1]:.1f}"/></g>')
    # pendant lights 2.2 m above the floor, labels at the top of each cord
    for i, c in enumerate(stations):
        lamp = P(c - m(0.1), (TY0 + TY1) / 2, m(2.1))
        top = P(c - m(0.1), (TY0 + TY1) / 2, m(2.6))
        o.append(f'<line class="cord" x1="{top[0]:.1f}" y1="{top[1]:.1f}" x2="{lamp[0]:.1f}" y2="{lamp[1]:.1f}"/>'
                 f'<path class="shade" d="M{lamp[0]-3.5:.1f},{lamp[1]:.1f} L{lamp[0]+3.5:.1f},{lamp[1]:.1f} L{lamp[0]+9:.1f},{lamp[1]+7:.1f} L{lamp[0]-9:.1f},{lamp[1]+7:.1f} Z"/>'
                 f'<ellipse class="bulb" cx="{lamp[0]:.1f}" cy="{lamp[1]+7:.1f}" rx="7" ry="1.8"/>')
        if not hero:
            o.append(f'<text class="{"h" if i == 2 else "s"} lb4" x="{top[0]+7:.1f}" y="{top[1]-6:.1f}">{SEW_OPS[i][0]} · {SEW_OPS[i][1]}</text>')
    if not hero:
        ix, iy = P(xa, CY1 + 0.6, 0)
        o.append(f'<text class="lb4" x="{ix-60:.1f}" y="{iy+20:.1f}">CUT PANELS IN</text>')
        ex, ey = P(ex0 + m(0.3), CY1 + m(0.7), 0)
        o.append(f'<text class="lb4" x="{ex-20:.1f}" y="{ey+20:.1f}">T-SHIRTS OUT</text>')
    o.append("</svg>")
    # crop the view box to the drawn scene so it is larger, mainly on phones
    xs = [P(x, y, 0)[0] for x in (X0, X1) for y in (Y0, Y1)]
    ys = [P(x, y, 0)[1] for x in (X0, X1) for y in (Y0, Y1)]
    top = min(P(c - m(0.1), (TY0 + TY1) / 2, m(2.6))[1] for c in stations) - 24
    vx0, vx1 = min(xs) - 10, max(xs) + 6
    vy0, vy1 = top, max(ys) + 28
    svg = "".join(o).replace('viewBox="0 0 860 590"', f'viewBox="{vx0:.0f} {vy0:.0f} {vx1-vx0:.0f} {vy1-vy0:.0f}"', 1)
    return svg
