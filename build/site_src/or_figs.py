#!/usr/bin/env python3
"""Two auto-running 3D OR figures for the proposal board.
G1: isometric sewing-line simulation with a live-looking dashboard.
G2: 3D optimization landscape with three gradient-descent searches.
Pure SVG + CSS/SMIL, no JavaScript (the real site adds JS for clicks)."""
import math

# ---------- shared isometric helpers ----------
C30, S30 = math.cos(math.pi / 6), 0.5


def iso(x, y, z, s, ox, oy):
    return ((x - y) * C30 * s + ox, (x + y) * S30 * s - z * s + oy)


def poly(pts, cls):
    d = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
    return f'<polygon class="{cls}" points="{d}"/>'


def box(x0, x1, y0, y1, z0, z1, P, top="ft", left="fl", right="fr"):
    t = [P(x0, y0, z1), P(x1, y0, z1), P(x1, y1, z1), P(x0, y1, z1)]
    r = [P(x1, y0, z0), P(x1, y1, z0), P(x1, y1, z1), P(x1, y0, z1)]
    l = [P(x0, y1, z0), P(x1, y1, z0), P(x1, y1, z1), P(x0, y1, z1)]
    return poly(l, left) + poly(r, right) + poly(t, top)


CSS = """
/* ===== G. auto-running 3D OR figures ===== */
.orf{display:grid;grid-template-columns:1fr 300px;border:1px solid var(--line2);border-radius:10px;overflow:hidden;background:var(--surface);backdrop-filter:var(--glass)}
.orf .stage{position:relative;padding:18px 18px 10px;min-width:0}
.orf .stage svg{display:block;width:100%;height:auto;overflow:visible}
.orf .dash{border-left:1px solid var(--line2);padding:20px;display:flex;flex-direction:column;gap:14px}
.orf .ft{font:600 12.5px 'IBM Plex Mono',monospace;letter-spacing:.1em;color:var(--acc-t)}
.orf h3{margin:0;font:600 20px/1.25 'Space Grotesk',sans-serif;color:var(--strong)}
.orf .kp{display:grid;grid-template-columns:1fr 1fr;border-top:1px solid var(--line2)}
.orf .kp>div{padding:9px 0;border-bottom:1px solid var(--line);display:flex;flex-direction:column;gap:3px}
.orf .kp .k{font:600 11.5px 'IBM Plex Mono',monospace;letter-spacing:.1em;color:var(--muted)}
.orf .kp b{font:600 20px 'IBM Plex Mono',monospace;color:var(--strong)}
.orf .kp b.a{color:var(--acc-t)}
.orf .ut{display:flex;flex-direction:column;gap:7px}
.orf .ut .r{display:grid;grid-template-columns:28px 1fr 44px;align-items:center;gap:8px;font:600 12px 'IBM Plex Mono',monospace;color:var(--muted)}
.orf .ut .r b{color:var(--strong);font-weight:600;text-align:right}
.orf .ut .bar{height:7px;border-radius:999px;background:var(--line);overflow:hidden}
.orf .ut .bar i{display:block;height:100%;background:var(--acc);opacity:.55;animation:utWob 3.2s ease-in-out infinite alternate}
.orf .ut .r.hot .bar i{opacity:1}
.orf .ut .r.hot b{color:var(--acc-t)}
@keyframes utWob{from{transform:translateX(-4%)}to{transform:translateX(0)}}
.orf .nt{font-size:13.5px;line-height:1.55;color:var(--muted)}
.orf .live{display:flex;align-items:center;gap:8px;font:600 12px 'IBM Plex Mono',monospace;letter-spacing:.1em;color:var(--muted)}
.orf .tagl{position:absolute;left:18px;bottom:12px;font:600 11.5px 'IBM Plex Mono',monospace;letter-spacing:.1em;color:var(--muted)}

/* isometric faces (theme-aware through opacity) */
.orf polygon.ft{fill:var(--strong);fill-opacity:.16;stroke:var(--line2);stroke-width:1}
.orf polygon.fl{fill:var(--strong);fill-opacity:.07;stroke:var(--line2);stroke-width:1}
.orf polygon.fr{fill:var(--strong);fill-opacity:.11;stroke:var(--line2);stroke-width:1}
.orf polygon.at{fill:var(--acc);fill-opacity:.95;stroke:none}
.orf polygon.al{fill:var(--acc);fill-opacity:.55;stroke:none}
.orf polygon.ar{fill:var(--acc);fill-opacity:.75;stroke:none}
.orf polygon.belt{fill:var(--strong);fill-opacity:.22;stroke:var(--line2)}
.orf polygon.floor{fill:var(--strong);fill-opacity:.03;stroke:var(--line);stroke-dasharray:4 4}
.orf .beltln{stroke:var(--strong);stroke-opacity:.35;stroke-width:1.4;stroke-dasharray:6 10;animation:beltMove 1s linear infinite}
@keyframes beltMove{to{stroke-dashoffset:-16}}
.orf .lamp{fill:var(--line2)}
.orf .lamp.on{fill:var(--acc);animation:lampGlow 1.4s ease-in-out infinite}
@keyframes lampGlow{0%,100%{opacity:.35}50%{opacity:1}}
.orf text{font:600 12.5px 'IBM Plex Mono',monospace;fill:var(--muted)}
.orf text.s{fill:var(--strong)}
.orf text.h{fill:var(--acc-t)}

/* G2 landscape */
.rock{transform-origin:50% 55%;animation:rock 14s ease-in-out infinite alternate}
@keyframes rock{from{transform:perspective(1400px) rotateX(10deg) rotateY(-9deg)}to{transform:perspective(1400px) rotateX(4deg) rotateY(9deg)}}
.orf .w0{stroke:var(--acc);stroke-opacity:.95;fill:none;stroke-width:1.3}
.orf .w1{stroke:var(--acc);stroke-opacity:.55;fill:none;stroke-width:1.1}
.orf .w2{stroke:var(--strong);stroke-opacity:.32;fill:none;stroke-width:1}
.orf .w3{stroke:var(--strong);stroke-opacity:.16;fill:none;stroke-width:1}
.orf .trail{fill:none;stroke:var(--strong);stroke-width:2.2;stroke-linecap:round;stroke-dasharray:1 1;stroke-dashoffset:1;animation:trail 8s ease-in-out infinite}
.orf .trail.g{stroke:var(--acc-t);stroke-width:2.6}
@keyframes trail{0%{stroke-dashoffset:1}72%,100%{stroke-dashoffset:0}}
.orf .ball{fill:var(--strong);stroke:var(--bg);stroke-width:2}
.orf .ball.g{fill:var(--acc)}
.orf .flag{stroke:var(--acc-t);stroke-width:1.4}

@media (prefers-reduced-motion:reduce){.orf *{animation:none!important}.rock{animation:none}}
@media (max-width:760px){
  .orf{grid-template-columns:1fr}.orf .dash{border-left:0;border-top:1px solid var(--line2)}
  .orf .stage{padding:10px 6px 12px}
  .orf text{font-size:28px}
  .orf .tagl{position:static;padding:8px 12px 0}
}
"""


# ---------- G1: sewing line simulation ----------
def factory_svg():
    s, ox, oy = 27, 250, 118
    P = lambda x, y, z: iso(x, y, z, s, ox, oy)
    out = ['<svg viewBox="0 0 860 470" role="img" aria-label="Isometric sewing line: parts move through four stations">']
    # floor
    out.append(poly([P(-2, -4.5, 0), P(23, -4.5, 0), P(23, 3.5, 0), P(-2, 3.5, 0)], "floor"))
    stations = [3, 8, 13, 18]
    # machines behind the belt (drawn first)
    for i, c in enumerate(stations):
        hot = i == 2
        out.append(box(c - 1.2, c + 1.2, -3.4, -1.0, 0, 1.9, P))
        # sewing head on top
        out.append(box(c - 0.9, c + 0.3, -2.6, -1.4, 1.9, 2.6, P, *(("at", "al", "ar") if hot else ("ft", "fl", "fr"))))
        # andon pole + lamp
        px, py = P(c + 0.9, -3.0, 1.9)
        qx, qy = P(c + 0.9, -3.0, 3.3)
        out.append(f'<line x1="{px:.1f}" y1="{py:.1f}" x2="{qx:.1f}" y2="{qy:.1f}" stroke="var(--line2)" stroke-width="1.5"/>')
        out.append(f'<circle class="lamp{" on" if hot else ""}" cx="{qx:.1f}" cy="{qy:.1f}" r="5"/>')
        lx, ly = P(c, -3.4, 3.6)
        out.append(f'<text class="{"h" if hot else "s"}" x="{lx-30:.1f}" y="{ly-6:.1f}">S{i+1}{" · BOTTLENECK" if hot else ""}</text>')
    # belt
    out.append(box(-1.5, 22, -0.6, 0.6, 0, 0.5, P, "belt", "fl", "fr"))
    a, b = P(-1.5, 0, 0.5), P(22, 0, 0.5)
    out.append(f'<line class="beltln" x1="{a[0]:.1f}" y1="{a[1]:.1f}" x2="{b[0]:.1f}" y2="{b[1]:.1f}"/>')
    # WIP buffer in front of S3 (parts waiting on a pallet)
    out.append(box(9.9, 11.8, 1.2, 2.2, 0, 0.15, P))
    for k, (bx, bz) in enumerate([(10.2, 0.15), (10.9, 0.15), (10.2, 0.75)]):
        out.append(box(bx, bx + 0.6, 1.4, 2.0, bz, bz + 0.6, P, "at", "al", "ar"))
    wx, wy = P(10.6, 2.4, 0)
    out.append(f'<text x="{wx-10:.1f}" y="{wy+18:.1f}">WIP · 3</text>')
    # moving parts: a small cube drawn at the origin, moved along the belt with dwell at each station
    cube = box(-0.3, 0.3, -0.3, 0.3, 0, 0.6, lambda x, y, z: iso(x, y, z, s, 0, 0), "at", "al", "ar")
    start, end = P(-1.2, 0, 0.5), P(21.6, 0, 0.5)
    frac = lambda x: (x + 1.2) / 22.8
    seq, t = [(0.0, 0.0)], 0.0
    for c, dwell in zip(stations, [1.2, 1.2, 1.8, 1.2]):
        t += 1.3
        seq.append((t, frac(c)))
        t += dwell
        seq.append((t, frac(c)))
    t += 1.3
    seq.append((t, 1.0))
    dur = t
    kt = ";".join(f"{x/dur:.4f}" for x, _ in seq)
    kp = ";".join(f"{p:.4f}" for _, p in seq)
    path = f"M{start[0]:.1f},{start[1]:.1f} L{end[0]:.1f},{end[1]:.1f}"
    n = 6
    for k in range(n):
        out.append(f'<g>{cube}<animateMotion dur="{dur:.1f}s" begin="-{k*dur/n:.2f}s" repeatCount="indefinite" '
                   f'calcMode="linear" keyTimes="{kt}" keyPoints="{kp}" path="{path}"/></g>')
    ix, iy = P(-1.5, 1.2, 0)
    out.append(f'<text x="{ix-40:.1f}" y="{iy+22:.1f}">IN</text>')
    ex, ey = P(22, 1.2, 0)
    out.append(f'<text x="{ex-6:.1f}" y="{ey+22:.1f}">OUT →</text>')
    out.append("</svg>")
    return "".join(out)


def factory_fig():
    util = [("S1", 84), ("S2", 88), ("S3", 100), ("S4", 96)]
    bars = "".join(f'<div class="r{" hot" if p == 100 else ""}"><span>{n}</span><div class="bar"><i style="width:{p}%"></i></div><b>{p}%</b></div>'
                   for n, p in util)
    return f'''<div class="orf">
      <div class="stage">{factory_svg()}<div class="tagl">AUTO-RUNS · ON THE REAL SITE, CLICK A STATION TO ADD A WORKER</div></div>
      <div class="dash">
        <div class="ft">FIG. B · OPTION 1</div>
        <h3>Sewing line simulation</h3>
        <div class="kp">
          <div><span class="k">THROUGHPUT</span><b>144 /h</b></div>
          <div><span class="k">BOTTLENECK</span><b class="a">S3</b></div>
          <div><span class="k">WIP</span><b>3</b></div>
          <div><span class="k">TAKT</span><b>25 s</b></div>
        </div>
        <div class="live">STATION UTILIZATION</div>
        <div class="ut">{bars}</div>
        <div class="nt">Parts flow through four sewing stations. S3 is the slowest, so work waits in front of it. Demo data.</div>
      </div>
    </div>'''


# ---------- G2: optimization landscape ----------
def f(x, y):
    g = lambda cx, cy, a, w: a * math.exp(-((x - cx) ** 2 + (y - cy) ** 2) / w)
    return -g(0.45, 0.35, 1.0, 0.09) - g(-0.5, -0.3, 0.62, 0.07) - g(0.05, -0.62, 0.5, 0.05) + 0.28 * (x * x + y * y)


def grad(x, y, h=1e-4):
    return ((f(x + h, y) - f(x - h, y)) / (2 * h), (f(x, y + h) - f(x, y - h)) / (2 * h))


def descent(x, y, lr=0.03, n=400):
    pts = [(x, y)]
    for _ in range(n):
        gx, gy = grad(x, y)
        x, y = x - lr * gx, y - lr * gy
        pts.append((x, y))
    return pts


def landscape_svg():
    th = math.radians(28)
    s, H, ox, oy = 240, 145, 430, 240

    def P(x, y):
        u = x * math.cos(th) - y * math.sin(th)
        v = x * math.sin(th) + y * math.cos(th)
        return ((u - v) * C30 * s + ox, (u + v) * S30 * s - f(x, y) * H + oy)

    zs = [f(-1 + 2 * i / 40, -1 + 2 * j / 40) for i in range(41) for j in range(41)]
    lo, hi = min(zs), max(zs)
    band = lambda z: min(3, int((z - lo) / (hi - lo + 1e-9) * 4.6))
    N = 26
    paths = {0: [], 1: [], 2: [], 3: []}
    grid = [-1 + 2 * i / N for i in range(N + 1)]
    for fixed_is_x in (True, False):
        for a in grid:
            prev = None
            for bb in grid:
                x, y = (a, bb) if fixed_is_x else (bb, a)
                p = P(x, y)
                if prev:
                    zm = f((x + prev[2]) / 2, (y + prev[3]) / 2)
                    paths[band(zm)].append(f"M{prev[0]:.1f},{prev[1]:.1f}L{p[0]:.1f},{p[1]:.1f}")
                prev = (p[0], p[1], x, y)
    out = ['<svg viewBox="0 0 860 520" role="img" aria-label="3D optimization landscape with three searches">']
    for k in (3, 2, 1, 0):
        out.append(f'<path class="w{k}" d="{"".join(paths[k])}"/>')
    starts = [(-0.95, 0.85), (0.95, -0.95), (0.98, 0.95)]
    runs = []
    for i, (sx, sy) in enumerate(starts):
        pts = descent(sx, sy)
        d = "M" + " L".join(f"{P(x, y)[0]:.1f},{P(x, y)[1]:.1f}" for x, y in pts[::4])
        runs.append((f(*pts[-1]), i, pts[-1], d))
    best = min(runs)[1]
    for fz, i, (ex, ey), d in runs:
        g = " g" if i == best else ""
        out.append(f'<path class="trail{g}" pathLength="1" d="{d}"/>')
    for fz, i, (ex, ey), d in runs:
        g = " g" if i == best else ""
        out.append(f'<circle class="ball{g}" r="7"><animateMotion dur="8s" repeatCount="indefinite" calcMode="spline" '
                   f'keyTimes="0;0.72;1" keyPoints="0;1;1" keySplines="0.42 0 0.58 1;0 0 1 1" path="{d}"/></circle>')
        px, py = P(ex, ey)
        lab = "GLOBAL OPTIMUM" if i == best else "LOCAL"
        out.append(f'<line class="flag" x1="{px:.1f}" y1="{py-10:.1f}" x2="{px:.1f}" y2="{py-46:.1f}"/>'
                   f'<text class="{"h" if i == best else ""}" x="{px+6:.1f}" y="{py-38:.1f}">{lab} · f={fz:.2f}</text>')
        sx0, sy0 = P(*starts[i])
        out.append(f'<text x="{sx0-18:.1f}" y="{sy0-12:.1f}">START {i+1}</text>')
    ends = runs
    out.append("</svg>")
    return "".join(out), min(ends)[0]


def landscape_fig():
    svg, best = landscape_svg()
    return f'''<div class="orf">
      <div class="stage"><div class="rock">{svg}</div><div class="tagl">AUTO-RUNS · ON THE REAL SITE, DRAG TO TURN, CLICK TO DROP A NEW START</div></div>
      <div class="dash">
        <div class="ft">FIG. B · OPTION 2</div>
        <h3>Optimization landscape</h3>
        <div class="kp">
          <div><span class="k">METHOD</span><b style="font-size:15px">GRADIENT DESCENT</b></div>
          <div><span class="k">STARTS</span><b>3</b></div>
          <div><span class="k">BEST f</span><b class="a">{best:.2f}</b></div>
          <div><span class="k">LOCAL TRAPS</span><b>2</b></div>
        </div>
        <div class="nt">The surface is a cost to minimise. Three searches roll downhill from different starts: two stop in local valleys, one reaches the global optimum. This is why OR uses multi-start and metaheuristics.</div>
      </div>
    </div>'''
