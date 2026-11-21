#!/usr/bin/env python3
"""Location map of Bangladesh for the contact section.
Boundaries: Natural Earth 1:10m via the world-atlas npm package (public domain).
Equirectangular projection scaled by cos(latitude) so shapes keep their real proportions."""
import json, math, os

GEO = json.load(open(os.path.join(os.path.dirname(__file__), "bd_geo.json")))
DHAKA = (90.4125, 23.8103)            # lon, lat (city level only, not an address)
BOX = (87.6, 93.1, 20.4, 26.9)         # lon0, lon1, lat0, lat1


def _proj(W, H):
    lon0, lon1, lat0, lat1 = BOX
    k = math.cos(math.radians((lat0 + lat1) / 2))
    sx = W / ((lon1 - lon0) * k)
    sy = H / (lat1 - lat0)
    sc = min(sx, sy)
    ox = (W - (lon1 - lon0) * k * sc) / 2
    oy = (H - (lat1 - lat0) * sc) / 2
    return lambda lon, lat: (ox + (lon - lon0) * k * sc, oy + (lat1 - lat) * sc)


def _path(geom, P, minstep=0.6):
    polys = geom["coordinates"] if geom["type"] == "MultiPolygon" else [geom["coordinates"]]
    d = []
    for poly in polys:
        for ring in poly:
            pts, last = [], None
            for lon, lat in ring:
                if not (BOX[0] - 3 < lon < BOX[1] + 3 and BOX[2] - 3 < lat < BOX[3] + 3):
                    continue
                x, y = P(lon, lat)
                if last and abs(x - last[0]) + abs(y - last[1]) < minstep:
                    continue
                pts.append((x, y)); last = (x, y)
            if len(pts) > 2:
                d.append("M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts) + " Z")
    return " ".join(d)


def _scale_px_per_km(W, H):
    lon0, lon1, lat0, lat1 = BOX
    P = _proj(W, H)
    x1, _ = P(90.0, 23.8); x2, _ = P(91.0, 23.8)
    return (x2 - x1) / (111.32 * math.cos(math.radians(23.8)))


def map_svg(W=360, H=240):
    """Map with CSS-only zoom (1x / 2x / 4x around Dhaka). On the real site this becomes a
    pan-and-zoom OpenStreetMap (Leaflet) view; the canvas mock-up cannot run JavaScript."""
    P = _proj(W, H)
    dx, dy = P(*DHAKA)
    o = ['<div class="mapw">',
         f'<svg class="bdmap" viewBox="0 0 {W} {H}" role="img" aria-label="Map of Bangladesh with Dhaka marked">',
         f'<defs><clipPath id="mclip"><rect x="0" y="0" width="{W}" height="{H}" rx="6"/></clipPath></defs><g clip-path="url(#mclip)">',
         f'<rect class="sea" x="0" y="0" width="{W}" height="{H}"/>',
         f'<g class="mz" style="transform-origin:{dx:.1f}px {dy:.1f}px">']
    for c in ("IND", "MMR", "BTN", "NPL"):
        o.append(f'<path class="nb" fill-rule="evenodd" d="{_path(GEO[c], P, 0.3)}"/>')
    for lon in range(88, 94):
        x, _ = P(lon, BOX[2])
        o.append(f'<line class="gr" x1="{x:.1f}" y1="-400" x2="{x:.1f}" y2="{H+400}"/>')
    for lat in range(21, 27):
        _, y = P(BOX[0], lat)
        o.append(f'<line class="gr" x1="-400" y1="{y:.1f}" x2="{W+400}" y2="{y:.1f}"/>')
    o.append(f'<path class="bd" fill-rule="evenodd" d="{_path(GEO["BGD"], P, 0.15)}"/>')
    o.append("</g>")
    # labels that only make sense at the full view
    lab = ['<g class="z1only">']
    for lon in range(88, 94):
        x, _ = P(lon, BOX[2])
        lab.append(f'<text class="gl" x="{x+2:.1f}" y="{H-4}">{lon}°E</text>')
    for lat in range(21, 27):
        _, y = P(BOX[0], lat)
        lab.append(f'<text class="gl" x="3" y="{y-3:.1f}">{lat}°N</text>')
    sx, sy = P(90.3, 21.0)
    lab.append(f'<text class="sea-l" x="{sx:.1f}" y="{sy:.1f}" text-anchor="middle">BAY OF BENGAL</text>')
    ix, iy = P(91.0, 25.75)          # India label sits over Meghalaya, north of the border
    lab.append(f'<text class="nb-l" x="{ix:.1f}" y="{iy:.1f}" text-anchor="middle">INDIA</text>')
    mx, my = P(92.75, 21.25)
    lab.append(f'<text class="nb-l" x="{mx:.1f}" y="{my:.1f}" text-anchor="middle">MYANMAR</text>')
    lab.append("</g>")
    o += lab
    # Dhaka target stays the same size at every zoom (it is the zoom centre)
    o.append(f'<g class="pin"><circle class="ring" cx="{dx:.1f}" cy="{dy:.1f}" r="11"/>'
             f'<line x1="{dx-17:.1f}" y1="{dy:.1f}" x2="{dx-5:.1f}" y2="{dy:.1f}"/><line x1="{dx+5:.1f}" y1="{dy:.1f}" x2="{dx+17:.1f}" y2="{dy:.1f}"/>'
             f'<line x1="{dx:.1f}" y1="{dy-17:.1f}" x2="{dx:.1f}" y2="{dy-5:.1f}"/><line x1="{dx:.1f}" y1="{dy+5:.1f}" x2="{dx:.1f}" y2="{dy+17:.1f}"/>'
             f'<circle class="core" cx="{dx:.1f}" cy="{dy:.1f}" r="3"/>'
             f'<rect class="tagbg" x="{dx+20:.1f}" y="{dy-12:.1f}" width="56" height="18" rx="3"/>'
             f'<text class="tag" x="{dx+48:.1f}" y="{dy+1:.1f}" text-anchor="middle">DHAKA</text></g>')
    # scale bars (one per zoom level)
    k = _scale_px_per_km(W, H)
    for z, km in ((1, 100), (2, 50), (4, 20)):
        L = km * k * z
        o.append(f'<g class="sb sb{z}"><rect class="sbbg" x="{W-L-22:.1f}" y="8" width="{L+14:.1f}" height="20" rx="3"/>'
                 f'<line x1="{W-L-15:.1f}" y1="22" x2="{W-15:.1f}" y2="22"/><line x1="{W-L-15:.1f}" y1="18" x2="{W-L-15:.1f}" y2="25"/>'
                 f'<line x1="{W-15:.1f}" y1="18" x2="{W-15:.1f}" y2="25"/>'
                 f'<text x="{W-15-L/2:.1f}" y="17" text-anchor="middle">{km} km</text></g>')
    o.append("</g></svg>")
    o.append("</div>")
    return "".join(o)


MAP_CSS = """
/* Mock-up: the map zooms in and out on its own (no buttons). Real site: Leaflet + OpenStreetMap,
   mouse-wheel / pinch zoom and drag; wheel zoom turns on after the first click so page scrolling is not trapped. */
.mapw{position:relative;width:100%;align-self:stretch}
.bdmap .mz{transform-box:view-box;animation:mapZoom 18s ease-in-out infinite}
.bdmap .mz path,.bdmap .mz line{vector-effect:non-scaling-stroke}
@keyframes mapZoom{0%,22%{transform:scale(1)}45%,62%{transform:scale(4)}85%,100%{transform:scale(1)}}
.bdmap .z1only{animation:mapLab 18s ease-in-out infinite}
@keyframes mapLab{0%,18%{opacity:1}26%,80%{opacity:0}88%,100%{opacity:1}}
.bdmap .sb1{animation:sb1 18s linear infinite}.bdmap .sb4{animation:sb4 18s linear infinite}.bdmap .sb2{display:none}
@keyframes sb1{0%,22%{opacity:1}23%,84%{opacity:0}85%,100%{opacity:1}}
@keyframes sb4{0%,44%{opacity:0}45%,62%{opacity:1}63%,100%{opacity:0}}
.mzn{margin-top:6px;text-align:right;font:600 10px 'IBM Plex Mono',monospace;letter-spacing:.1em;color:var(--muted)}
@media (prefers-reduced-motion:reduce){.bdmap .mz,.bdmap .z1only,.bdmap .sb1,.bdmap .sb4{animation:none}.bdmap .sb4{opacity:0}}
.bdmap .sb line{stroke:var(--strong);stroke-width:1.4}
.bdmap .sb text{font:600 9px 'IBM Plex Mono',monospace;fill:var(--strong)}
.bdmap .sbbg{fill:var(--bg);fill-opacity:.85}
.bdmap{display:block;width:100%;height:auto;border:1px solid var(--line);border-radius:6px}
.bdmap .sea{fill:#3D6E9E;fill-opacity:.16}
.bdmap .nb{fill:var(--strong);fill-opacity:.07;stroke:var(--line2);stroke-width:.7}
.bdmap .bd{fill:#3E9E6E;fill-opacity:.32;stroke:#3E9E6E;stroke-width:1.1;stroke-linejoin:round}
.bdmap .gr{stroke:var(--strong);stroke-opacity:.08;stroke-width:.6;stroke-dasharray:3 3}
.bdmap .gl{font:500 8.5px 'IBM Plex Mono',monospace;fill:var(--muted)}
.bdmap .sea-l{font:600 9px 'IBM Plex Mono',monospace;letter-spacing:.18em;fill:#5B8DBE;fill-opacity:.9}
.bdmap .nb-l{font:600 9px 'IBM Plex Mono',monospace;letter-spacing:.14em;fill:var(--muted)}
.bdmap .pin line{stroke:var(--acc-t);stroke-width:1.4}
.bdmap .pin .ring{fill:none;stroke:var(--acc-t);stroke-width:1.4}
.bdmap .pin .core{fill:var(--acc)}
.bdmap .tagbg{fill:var(--bg);stroke:var(--acc-t);stroke-width:1}
.bdmap .tag{font:700 10px 'IBM Plex Mono',monospace;letter-spacing:.1em;fill:var(--strong)}
"""
