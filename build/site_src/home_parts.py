"""Shared parts for build_home.py:
- THEMES: colour tokens + the LOCKED page backdrop (approved by Zaid before review round 1)
- backdrop(): static drawing photo across the whole page
- gear_svg(): hero figure — spur gear + pinion, blueprint line-art, meshing rotation
"""
import math

# One static drawing photo (CR-3D, Pixabay) across the whole page.
# Dark = darkened photo + oxblood/brown tint (mix-blend-mode:color) + vignette.
# Light = same photo under a cream wash. Layers copied verbatim from the approved v19 artboards.
# The approved look was designed on a 1900px-tall board, so the backdrop is built from 1900px
# segments (every second one mirrored so seams are invisible) -> same scale and mood all the way down.
OLD_PHOTO = "/_blob/f1dcb9ccf4c97a4830322d7fb16b2294"
# dark mode: same photo pre-baked (bake_bg.py) into a very dark oxblood monochrome — tuned to the
# darkness of Zaid's own reference images (mean RGB ~ (29,2,3), max ~ (54,3,6))
DARK_BG = "/_blob/c22df97f30fa524b5d928314b54988a1"
SEG = 1900
NSEG = 5

THEMES = {
    "dark": dict(
        vars="--bg:#0C0F14;--surface:rgba(18,21,28,0.75);--surface2:rgba(255,255,255,0.05);--glass:blur(8px) saturate(115%);"
             "--line:rgba(255,255,255,0.12);--line2:rgba(255,255,255,0.22);--strong:#F4F5F7;--text:#E7E9EC;"
             "--body:#AEB6C2;--muted:#9AA4B2;--logo:rgba(238,226,224,0.84);--grid:rgba(255,255,255,0.035);"
             "--header:rgba(12,15,20,0.82);--acc:#C14B3C;--acc-t:#CD6A5C;--acc-soft:rgba(193,75,60,0.14);"
             "--acc-glow:rgba(193,75,60,0.55);--on-acc:#FFFFFF;--tog-on:#C14B3C;--tog-on-ic:#FFFFFF;--hatch:rgba(255,255,255,0.06)",
        seg_layers=[
            f'<div class="bl" style="background-image:url({DARK_BG});background-size:cover;background-position:center top;background-repeat:no-repeat"></div>',
        ],
    ),
    "light": dict(
        vars="--bg:#F7F5EF;--surface:rgba(251,250,246,0.94);--glass:none;--surface2:rgba(22,35,58,0.035);"
             "--line:rgba(22,35,58,0.14);--line2:rgba(22,35,58,0.3);--strong:#16233A;--text:#16233A;"
             "--body:#3E4A5C;--muted:#5B6475;--logo:rgba(22,35,58,0.80);--grid:rgba(22,35,58,0.05);"
             "--header:rgba(247,245,239,0.86);--acc:#B03F31;--acc-t:#A33A2D;--acc-soft:rgba(176,63,49,0.10);"
             "--acc-glow:rgba(176,63,49,0.45);--on-acc:#FFFFFF;--tog-on:#16233A;--tog-on-ic:#F7F5EF;--hatch:rgba(22,35,58,0.08)",
        seg_layers=[
            f'<div class="bl" style="background-image:url({OLD_PHOTO});background-size:cover;background-position:center top;background-repeat:no-repeat;filter:grayscale(10%) brightness(1.1) contrast(0.95) saturate(0.9)"></div>',
            '<div class="bl" style="background-image:linear-gradient(180deg, rgba(247,245,239,0.80) 0%, rgba(247,245,239,0.88) 35%, rgba(247,245,239,0.95) 72%, rgba(247,245,239,0.98) 100%), radial-gradient(900px 650px at 90% -10%, rgba(200,98,42,0.10), transparent 62%), radial-gradient(760px 600px at -10% 45%, rgba(22,35,58,0.05), transparent 62%)"></div>',
        ],
    ),
}

BACKDROP_CSS = """
.pagebd{position:absolute;inset:0;z-index:0;pointer-events:none;overflow:hidden}
.seg{position:absolute;left:0;right:0;height:1900px}
.seg.flip{transform:scaleY(-1)}
.bl{position:absolute;inset:0}
"""


def backdrop(theme):
    segs = []
    for i in range(NSEG):
        flip = " flip" if i % 2 else ""
        segs.append(f'<div class="seg{flip}" style="top:{i*SEG}px">' + "".join(THEMES[theme]["seg_layers"]) + "</div>")
    grid = ('<div class="bl" style="background-image:linear-gradient(var(--grid) 1px,transparent 1px),'
            'linear-gradient(90deg,var(--grid) 1px,transparent 1px);background-size:32px 32px"></div>')
    return '<div class="pagebd" aria-hidden="true">' + "".join(segs) + grid + "</div>"


# ---------------- hero figure: gear + pinion ----------------
M = 6
Z1, Z2 = 32, 16
G1X, GY = 170, 200
A = M * (Z1 + Z2) / 2          # centre distance = 144
G2X = G1X + A

GEAR_CSS = """
.gearfig{display:block;width:100%;height:auto;overflow:visible}
.gearfig .cl path{fill:none;stroke:var(--muted);stroke-width:1;stroke-dasharray:14 4 2 4;opacity:.7}
.gearfig .body{fill:var(--acc-soft);stroke:var(--acc);stroke-width:1.8;stroke-linejoin:round}
.gearfig .body.p2{fill:rgba(128,128,128,0.06);stroke:var(--text);stroke-width:1.6}
.gearfig .pc{fill:none;stroke:var(--muted);stroke-width:.9;stroke-dasharray:5 4;opacity:.8}
.gearfig .hole circle,.gearfig .hub{fill:none;stroke:var(--acc);stroke-width:1.3}
.gearfig .g2 .hub{stroke:var(--text)}
.gearfig .bore,.gearfig .bore path{fill:var(--bg);stroke:var(--muted);stroke-width:1.2}
.gearfig .dim path{fill:none;stroke:var(--muted);stroke-width:1}
.gearfig .dim .ah{fill:var(--muted);stroke:none}
.gearfig .lab{font:500 12px 'IBM Plex Mono',monospace;fill:var(--muted);letter-spacing:.04em}
.gearfig .lab.t{fill:var(--acc-t);font-weight:600;letter-spacing:.1em}
.gearfig .g1{transform-origin:G1XPXpx GYPXpx;animation:gSpin 32s linear infinite}
.gearfig .g2{transform-origin:G2XPXpx GYPXpx;animation:gSpinR 16s linear infinite}
@keyframes gSpin{to{transform:rotate(360deg)}}
@keyframes gSpinR{to{transform:rotate(-360deg)}}
.gfwrap{position:relative;padding:18px 18px 10px}
.gfwrap s{position:absolute;width:16px;height:16px;border:0 solid var(--acc)}
.gfwrap s:nth-child(1){top:0;left:0;border-top-width:2px;border-left-width:2px}
.gfwrap s:nth-child(2){top:0;right:0;border-top-width:2px;border-right-width:2px}
.gfwrap s:nth-child(3){bottom:0;left:0;border-bottom-width:2px;border-left-width:2px}
.gfwrap s:nth-child(4){bottom:0;right:0;border-bottom-width:2px;border-right-width:2px}
""".replace("G1XPX", str(G1X)).replace("G2XPX", str(int(G2X))).replace("GYPX", str(GY))


def _gear_path(cx, cy, z, m, off):
    r = m * z / 2
    ra, rr = r + m, r - 1.25 * m
    p = 2 * math.pi / z

    def pt(rad, a):
        return cx + rad * math.cos(a), cy + rad * math.sin(a)

    d = ""
    for k in range(z):
        c = off + k * p
        x0, y0 = pt(rr, c - 0.5 * p)
        x1, y1 = pt(rr, c - 0.29 * p)
        x2, y2 = pt(ra, c - 0.16 * p)
        x3, y3 = pt(ra, c + 0.16 * p)
        x4, y4 = pt(rr, c + 0.29 * p)
        x5, y5 = pt(rr, c + 0.5 * p)
        if k == 0:
            d += f"M{x0:.2f},{y0:.2f}"
        d += (f"A{rr:.2f},{rr:.2f} 0 0 1 {x1:.2f},{y1:.2f}L{x2:.2f},{y2:.2f}"
              f"A{ra:.2f},{ra:.2f} 0 0 1 {x3:.2f},{y3:.2f}L{x4:.2f},{y4:.2f}"
              f"A{rr:.2f},{rr:.2f} 0 0 1 {x5:.2f},{y5:.2f}")
    return d + "Z", r, ra


def gear_svg():
    # big gear: a tooth GAP faces the pinion (angle 0); pinion: a TOOTH faces the gear (angle 180)
    d1, r1, ra1 = _gear_path(G1X, GY, Z1, M, math.pi / Z1)
    d2, r2, ra2 = _gear_path(G2X, GY, Z2, M, 0.0)
    holes = "".join(
        f'<circle cx="{G1X + 0.56*r1*math.cos(math.radians(30+60*i)):.2f}" '
        f'cy="{GY + 0.56*r1*math.sin(math.radians(30+60*i)):.2f}" r="{0.15*r1:.2f}"/>'
        for i in range(6))
    k1 = f'<path d="M{G1X-5},{GY-0.13*r1+1:.2f}v-6h10v6Z"/>'
    k2 = f'<path d="M{G2X-4},{GY-0.22*r2+1:.2f}v-5h8v5Z"/>'
    g2x = G2X
    return (
        '<div class="gfwrap"><s></s><s></s><s></s><s></s>'
        '<svg class="gearfig" viewBox="0 0 470 410" role="img" aria-label="Animated spur gear pair: 32-tooth gear driving a 16-tooth pinion">'
        f'<text class="lab t" x="20" y="34">FIG. A · SPUR GEAR PAIR</text>'
        f'<g class="cl"><path d="M40 {GY}H450M{G1X} 74V326M{g2x:g} 122V278"/></g>'
        f'<g class="g1"><path class="body" d="{d1}"/>'
        f'<circle class="pc" cx="{G1X}" cy="{GY}" r="{r1:g}"/>'
        f'<g class="hole">{holes}</g>'
        f'<circle class="hub" cx="{G1X}" cy="{GY}" r="{0.24*r1:.2f}"/>'
        f'<circle class="bore" cx="{G1X}" cy="{GY}" r="{0.13*r1:.2f}"/><g class="bore">{k1}</g></g>'
        f'<g class="g2"><path class="body p2" d="{d2}"/>'
        f'<circle class="pc" cx="{g2x:g}" cy="{GY}" r="{r2:g}"/>'
        f'<circle class="hub" cx="{g2x:g}" cy="{GY}" r="{0.44*r2:.2f}"/>'
        f'<circle class="bore" cx="{g2x:g}" cy="{GY}" r="{0.22*r2:.2f}"/><g class="bore">{k2}</g></g>'
        f'<g class="dim"><path d="M{G1X} 340V356M{g2x:g} 340V356M{G1X+7} 348H{g2x-7:g}"/>'
        f'<path class="ah" d="M{G1X} 348l8-3.5v7ZM{g2x:g} 348l-8-3.5v7Z"/></g>'
        f'<text class="lab" x="{(G1X+g2x)/2:g}" y="340" text-anchor="middle">a = {A:g}</text>'
        f'<text class="lab" x="20" y="392">z₁ = {Z1} · z₂ = {Z2} · m = {M} · i = 2 : 1</text>'
        '</svg></div>'
    )


# ---------------- hero figure v2: pseudo-3D gear pair (CSS 3D stacked layers) ----------------
# Textures come from render_gears.py (uploaded as canvas assets). Each gear = side silhouettes
# stacked along Z (dark→light = depth shading) + a machined top face; shafts stick out of the bores.
G3D_ASSETS = {}   # filled by build_home.py: name -> url

G3D_T1, G3D_T2, G3D_STEP = 18, 26, 1.5
G3D_PLANE_W, G3D_PLANE_H = 470, 340
G3D_C1 = (150, 172)
G3D_C2 = (150 + A, 172)
G3D_SIZE1, G3D_SIZE2 = 210, 114
G3D_SH1, G3D_SH2 = 24.96, 21.12

GEAR3D_CSS = """
.g3dwrap{position:relative;padding:18px 18px 12px}
.g3dwrap s{position:absolute;width:16px;height:16px;border:0 solid var(--acc)}
.g3dwrap s:nth-child(1){top:0;left:0;border-top-width:2px;border-left-width:2px}
.g3dwrap s:nth-child(2){top:0;right:0;border-top-width:2px;border-right-width:2px}
.g3dwrap s:nth-child(3){bottom:0;left:0;border-bottom-width:2px;border-left-width:2px}
.g3dwrap s:nth-child(4){bottom:0;right:0;border-bottom-width:2px;border-right-width:2px}
.g3dlab{font:600 12px 'IBM Plex Mono',monospace;letter-spacing:.1em;color:var(--acc-t)}
.g3dspec{font:500 12px 'IBM Plex Mono',monospace;letter-spacing:.04em;color:var(--muted);margin-top:6px}
.g3d{position:relative;height:340px;perspective:1100px;perspective-origin:50% 20%}
.g3d .pl3{position:absolute;left:50%;top:50%;width:PWpx;height:PHpx;margin:-PH2px 0 0 -PW2px;transform-style:preserve-3d;transform:scale(1.2) rotateX(57deg) rotateZ(-24deg)}
.g3d .floor{position:absolute;inset:-60px;background-image:linear-gradient(var(--line) 1px,transparent 1px),linear-gradient(90deg,var(--line) 1px,transparent 1px);background-size:24px 24px;-webkit-mask-image:radial-gradient(closest-side,#000 55%,transparent);mask-image:radial-gradient(closest-side,#000 55%,transparent)}
.g3d .fsvg{position:absolute;inset:0;overflow:visible}
.g3d .fsvg path,.g3d .fsvg circle{fill:none;stroke:var(--muted);stroke-width:1}
.g3d .fsvg .cl{stroke-dasharray:14 4 2 4;opacity:.75}
.g3d .fsvg .pc{stroke-dasharray:5 4;opacity:.7}
.g3d .fsvg .dm{stroke:var(--acc-t);opacity:.9}
.g3d .shd{position:absolute;border-radius:50%;background:radial-gradient(closest-side,rgba(0,0,0,.55),rgba(0,0,0,0));filter:blur(4px)}
.g3d .gr{position:absolute;transform-style:preserve-3d}
.g3d .gr img{position:absolute;inset:0;width:100%;height:100%;display:block;-webkit-user-drag:none;user-select:none}
.g3d .sh{position:absolute;transform-style:preserve-3d}
.g3d .sh img{position:absolute;inset:0;width:100%;height:100%}
.g3d .r1{animation:g3dSpin 32s linear infinite}
.g3d .r2{animation:g3dSpinR 16s linear infinite}
@keyframes g3dSpin{to{transform:rotateZ(360deg)}}
@keyframes g3dSpinR{to{transform:rotateZ(-360deg)}}
@media (prefers-reduced-motion:reduce){.g3d .r1,.g3d .r2{animation:none}}
@media (max-width:760px){.g3d{height:250px}.g3d .pl3{transform:scale(.78) rotateX(57deg) rotateZ(-24deg)}}
""".replace("PW2", str(G3D_PLANE_W // 2)).replace("PH2", str(G3D_PLANE_H // 2)).replace("PW", str(G3D_PLANE_W)).replace("PH", str(G3D_PLANE_H))


def _stack(prefix, size, cx, cy, T, rot):
    u = G3D_ASSETS
    n = int(T / G3D_STEP)
    layers = []
    for i in range(n):
        tag = "d" if i < n / 3 else ("m" if i < 2 * n / 3 else "l")
        layers.append(f'<img alt="" src="{u[prefix + "-side-" + tag]}" style="transform:translateZ({i*G3D_STEP:g}px)">')
    layers.append(f'<img alt="" src="{u[prefix + "-top"]}" style="transform:translateZ({T}px)">')
    sh = G3D_SH1 if prefix == "g1" else G3D_SH2
    shaft = "".join(f'<img alt="" src="{u[prefix + "-shaft"]}" style="transform:translateZ({z}px)">' for z in range(0, T + 16, 2))
    left, top = cx - size / 2, cy - size / 2
    return (f'<div class="gr {rot}" style="left:{left:g}px;top:{top:g}px;width:{size:g}px;height:{size:g}px">'
            + "".join(layers)
            + f'<div class="sh" style="left:{size/2-sh/2:g}px;top:{size/2-sh/2:g}px;width:{sh:g}px;height:{sh:g}px">{shaft}</div>'
            + "</div>")


def gear3d():
    (x1, y1), (x2, y2) = G3D_C1, G3D_C2
    r1, r2 = M * Z1 / 2, M * Z2 / 2
    floor = (f'<svg class="fsvg" viewBox="0 0 {G3D_PLANE_W} {G3D_PLANE_H}" aria-hidden="true">'
             f'<path class="cl" d="M-30 {y1}H{G3D_PLANE_W+30}M{x1} {y1-140}V{y1+140}M{x2:g} {y2-90}V{y2+90}"/>'
             f'<circle class="pc" cx="{x1}" cy="{y1}" r="{r1+22:g}"/><circle class="pc" cx="{x2:g}" cy="{y2}" r="{r2+18:g}"/>'
             f'<path class="dm" d="M{x1} {y1+128}H{x2:g}M{x1} {y1+120}V{y1+136}M{x2:g} {y2+120}V{y2+136}"/>'
             '</svg>')
    shadows = (f'<div class="shd" style="left:{x1-110+10}px;top:{y1-110+14}px;width:220px;height:220px"></div>'
               f'<div class="shd" style="left:{x2-62+10:g}px;top:{y2-62+14}px;width:124px;height:124px"></div>')
    return ('<div class="g3dwrap"><s></s><s></s><s></s><s></s>'
            '<div class="g3dlab">FIG. A · SPUR GEAR PAIR · 3D</div>'
            '<div class="g3d" role="img" aria-label="Rotating 3D spur gear pair: a 32-tooth gear driving a 16-tooth pinion">'
            '<div class="pl3"><div class="floor"></div>' + floor + shadows
            + _stack("g1", G3D_SIZE1, x1, y1, G3D_T1, "r1")
            + _stack("g2", G3D_SIZE2, x2, y2, G3D_T2, "r2")
            + '</div></div>'
            f'<div class="g3dspec">z₁ = {Z1} · z₂ = {Z2} · m = {M} · i = 2:1</div>'
            '</div>')


# ---------------- extra dark variants (Zaid 2026-11-14: reddish = current, + bluish, + greenish) ----------------
def _dark_variant(bg_blob, acc, acc_t, soft, glow):
    v = dict(THEMES["dark"])
    v["vars"] = (THEMES["dark"]["vars"]
                 .replace("--acc:#C14B3C", f"--acc:{acc}")
                 .replace("--acc-t:#CD6A5C", f"--acc-t:{acc_t}")
                 .replace("--acc-soft:rgba(193,75,60,0.14)", f"--acc-soft:{soft}")
                 .replace("--acc-glow:rgba(193,75,60,0.55)", f"--acc-glow:{glow}")
                 .replace("--tog-on:#C14B3C", f"--tog-on:{acc}"))
    v["seg_layers"] = [f'<div class="bl" style="background-image:url({bg_blob});background-size:cover;background-position:center top;background-repeat:no-repeat"></div>']
    return v


THEMES["dark_blue"] = _dark_variant("/_blob/efc33505bf99a47df76b8d31667e6c11", "#2F6BD8", "#6E9EF2",
                                    "rgba(47,107,216,0.16)", "rgba(47,107,216,0.55)")
THEMES["dark_green"] = _dark_variant("/_blob/895ae2ccb7c6f3f27c4c1becc3e0b200", "#1E7F55", "#4FC08A",
                                     "rgba(30,127,85,0.18)", "rgba(30,127,85,0.55)")

# big-gear textures per theme (pinion stays bright steel in every theme)
G1_BY_THEME = {
    "dark_blue": {"g1-top": "/_blob/07e41bb3400ba37bf69b87c5c4a909db", "g1-side-d": "/_blob/326f8f7d5d88fc1107e912433153f5bf",
                  "g1-side-m": "/_blob/02ff38ead97c157142ff1141dd62bb67", "g1-side-l": "/_blob/0b05db935c3ff652565de176f650095e"},
    "dark_green": {"g1-top": "/_blob/f8273ff9351436ee312c4f9dbb3961fd", "g1-side-d": "/_blob/88d75d32556a551dc2ce597baa0cba40",
                   "g1-side-m": "/_blob/3aa1e2e727780bdbfb51e23efd52dfca", "g1-side-l": "/_blob/11e59b57e39d11d78a830fedf0638a87"},
}


# ---------------- extra light variants (Zaid 2026-11-14: light also in red, blue, green) ----------------
def _light_variant(bg, rgb, acc, acc_t, soft, glow, glow_rgb):
    r, g, b = rgb
    v = dict(THEMES["light"])
    v["vars"] = (THEMES["light"]["vars"]
                 .replace("--bg:#F7F5EF", f"--bg:{bg}")
                 .replace("--header:rgba(247,245,239,0.86)", f"--header:rgba({r},{g},{b},0.86)")
                 .replace("--acc:#B03F31", f"--acc:{acc}")
                 .replace("--acc-t:#A33A2D", f"--acc-t:{acc_t}")
                 .replace("--acc-soft:rgba(176,63,49,0.10)", f"--acc-soft:{soft}")
                 .replace("--acc-glow:rgba(176,63,49,0.45)", f"--acc-glow:{glow}")
                 .replace("--tog-on-ic:#F7F5EF", f"--tog-on-ic:{bg}"))
    gr, gg, gb = glow_rgb
    v["seg_layers"] = [
        f'<div class="bl" style="background-image:url({OLD_PHOTO});background-size:cover;background-position:center top;background-repeat:no-repeat;filter:grayscale(100%) brightness(1.1) contrast(0.95)"></div>',
        f'<div class="bl" style="background-image:linear-gradient(180deg, rgba({r},{g},{b},0.80) 0%, rgba({r},{g},{b},0.88) 35%, rgba({r},{g},{b},0.95) 72%, rgba({r},{g},{b},0.98) 100%), radial-gradient(900px 650px at 90% -10%, rgba({gr},{gg},{gb},0.12), transparent 62%), radial-gradient(760px 600px at -10% 45%, rgba(22,35,58,0.05), transparent 62%)"></div>',
    ]
    return v


THEMES["light_blue"] = _light_variant("#F2F5FA", (242, 245, 250), "#2558B8", "#1F4FA8",
                                      "rgba(37,88,184,0.10)", "rgba(37,88,184,0.45)", (47, 107, 216))
THEMES["light_green"] = _light_variant("#F1F6F2", (241, 246, 242), "#1B6E49", "#17603F",
                                       "rgba(27,110,73,0.10)", "rgba(27,110,73,0.45)", (30, 127, 85))
G1_BY_THEME["light_blue"] = G1_BY_THEME["dark_blue"]
G1_BY_THEME["light_green"] = G1_BY_THEME["dark_green"]


# ---------------- SCREEN-FIXED background (Zaid 2026-11-17) ----------------
# The photo is a wallpaper locked to the screen: one image fills the viewport (cover, focal point on the
# caliper + circular drawing) and never scrolls; only the page content moves over it.
# Real site: .fixbg is position:fixed (height 100lvh so phones don't jump when the address bar hides).
# Canvas mockup: each board is one screen; .fixbg sits in the frame and the content scrolls in .scr.
import re as _re

PORTRAIT = {
    "dark": "/_blob/243da27966ae9d1882fdc73f17ddcbb1",
    "dark_blue": "/_blob/0b00bf9a3f7e4d3f3b4e9b7e8cf2444a",
    "dark_green": "/_blob/e5f77657747adcdb0d95e918912b4cad",
    "light": "/_blob/e7fa0707b3df8cfea862d6fa2adb55fe",
    "light_blue": "/_blob/e7fa0707b3df8cfea862d6fa2adb55fe",
    "light_green": "/_blob/e7fa0707b3df8cfea862d6fa2adb55fe",
}

BACKDROP_CSS = """
.fixbg{position:absolute;inset:0;z-index:0;pointer-events:none;overflow:hidden}
.bl{position:absolute;inset:0}
.ph-l,.ph-p{background-size:cover;background-repeat:no-repeat}
.ph-l{background-position:center 58%}
.ph-p{display:none;background-position:center}
@media (orientation:portrait){.ph-l{display:none}.ph-p{display:block}}
.scr{position:absolute;inset:0;z-index:1;overflow-y:auto;overflow-x:hidden;scrollbar-width:thin;scrollbar-color:var(--line2) transparent}
.zh.stat .scr{overflow:hidden}
.zh.stat .hdr{position:absolute;top:0;left:0;right:0}
.zh.stat .scc{padding-top:72px}
@media (max-width:760px){.zh.stat .scc{padding-top:64px}}
"""


def backdrop(theme):
    layers = list(THEMES[theme]["seg_layers"])
    photo = layers[0]
    m = _re.search(r"background-image:url\(([^)]+)\)", photo)
    url = m.group(1)
    filt = _re.search(r"filter:([^\"]+)", photo)
    f = f";filter:{filt.group(1)}" if filt else ""
    out = [f'<div class="bl ph-l" style="background-image:url({url}){f}"></div>',
           f'<div class="bl ph-p" style="background-image:url({PORTRAIT[theme]}){f}"></div>']
    for extra in layers[1:]:
        # light wash: tuned for one screen instead of a 5000px page (photo stays visible behind cards)
        extra = _re.sub(r",\s*0\.95\) 72%", ",0.86) 72%", extra)
        extra = _re.sub(r",\s*0\.98\) 100%", ",0.90) 100%", extra)
        out.append(extra)
    grid = ('<div class="bl" style="background-image:linear-gradient(var(--grid) 1px,transparent 1px),'
            'linear-gradient(90deg,var(--grid) 1px,transparent 1px);background-size:32px 32px"></div>')
    return '<div class="fixbg" aria-hidden="true">' + "".join(out) + grid + "</div>"


# ---------------- ROTATING screen-fixed wallpaper (Zaid 2026-11-17: "change slowly over time") ----------------
# Same fixed wallpaper, but the photo slowly crossfades: drawing -> refinery -> gears -> ... (10 s each,
# ~1.6 s fade). More photos from Zaid can be appended to WALL. prefers-reduced-motion: first photo only.
WALL = [
    # name, landscape position, {theme-group: (landscape, portrait)}
    ("drawing", "center 58%", {
        "dark": ("/_blob/c22df97f30fa524b5d928314b54988a1", "/_blob/243da27966ae9d1882fdc73f17ddcbb1"),
        "dark_blue": ("/_blob/efc33505bf99a47df76b8d31667e6c11", "/_blob/0b00bf9a3f7e4d3f3b4e9b7e8cf2444a"),
        "dark_green": ("/_blob/895ae2ccb7c6f3f27c4c1becc3e0b200", "/_blob/e5f77657747adcdb0d95e918912b4cad"),
        "light": (OLD_PHOTO, "/_blob/e7fa0707b3df8cfea862d6fa2adb55fe")}),
    ("refinery", "center 62%", {
        "dark": ("/_blob/f3bf6a079fb3ae98c3c09d08bc891880", "/_blob/6054643cd7a06a3461277d477a77ba0e"),
        "dark_blue": ("/_blob/c9c381879fb437f5116709403532b7e5", "/_blob/113fe048791619300945d2c15d20a407"),
        "dark_green": ("/_blob/5cdc47755d365e4cdb2d8a267dddebce", "/_blob/cbcff61a46438c4c1be456c6ac74c4b8"),
        "light": ("/_blob/4e20976f846f9f965d8930619703757d", "/_blob/aae7e871c2ae96852b4283a6152f4b9b")}),
    ("gears", "center 45%", {
        "dark": ("/_blob/4757e4801612bfa4fe24e87c5cfd1e39", "/_blob/a55846287bf68df343ab5c8f4d8a58a4"),
        "dark_blue": ("/_blob/d2103170ba9568e3ee03c5d445d9bf00", "/_blob/df4b186981fcfb4b94cdd8a272006df1"),
        "dark_green": ("/_blob/d0aff155870412971ae40b7a84723de1", "/_blob/e0d070242addc746c091d643fb709991"),
        "light": ("/_blob/47d71a28a6d02eef745ea18c41cb2f23", "/_blob/fee2a08264828c4482836ab8eb582100")}),
]
HOLD, FADE = 10.0, 1.6

_n = len(WALL)
_cycle = _n * HOLD
_on = HOLD / _cycle * 100
_fd = FADE / _cycle * 100
BACKDROP_CSS += (
    ".wslide{position:absolute;inset:0;opacity:0;animation:wFade %(c)gs infinite}\n"
    ".wslide.w0{opacity:1}\n"
    "@keyframes wFade{0%%{opacity:0}%(a).3f%%{opacity:1}%(b).3f%%{opacity:1}%(d).3f%%{opacity:0}100%%{opacity:0}}\n"
    "@media (prefers-reduced-motion:reduce){.wslide{animation:none;opacity:0}.wslide.w0{opacity:1}}\n"
) % dict(c=_cycle, a=_fd, b=_on, d=_on + _fd)


def backdrop(theme):
    group = theme if theme.startswith("dark") else "light"
    layers = list(THEMES[theme]["seg_layers"])
    filt = _re.search(r"filter:([^\"]+)", layers[0])
    f = f";filter:{filt.group(1)}" if filt else ""
    slides = []
    for i, (name, pos, imgs) in enumerate(WALL):
        land, por = imgs[group]
        delay = -FADE + i * HOLD   # first photo is fully visible at load
        slides.append(
            f'<div class="wslide w{i}" style="animation-delay:{delay:g}s" data-photo="{name}">'
            f'<div class="bl ph-l" style="background-image:url({land});background-position:{pos}{f}"></div>'
            f'<div class="bl ph-p" style="background-image:url({por}){f}"></div></div>')
    out = slides
    for extra in layers[1:]:
        # light wash raised 2026-11-17 (Zaid: text over the photo was hard to read)
        extra = _re.sub(r",\s*0\.80\) 0%", ",0.90) 0%", extra)
        extra = _re.sub(r",\s*0\.88\) 35%", ",0.92) 35%", extra)
        extra = _re.sub(r",\s*0\.95\) 72%", ",0.93) 72%", extra)
        extra = _re.sub(r",\s*0\.98\) 100%", ",0.95) 100%", extra)
        out.append(extra)
    if theme.startswith("dark"):
        # extra dim on the dark photos for the same reason
        out.append('<div class="bl" style="background:var(--bg);opacity:.32"></div>')
    grid = ('<div class="bl" style="background-image:linear-gradient(var(--grid) 1px,transparent 1px),'
            'linear-gradient(90deg,var(--grid) 1px,transparent 1px);background-size:32px 32px"></div>')
    return '<div class="fixbg" aria-hidden="true">' + "".join(out) + grid + "</div>"
