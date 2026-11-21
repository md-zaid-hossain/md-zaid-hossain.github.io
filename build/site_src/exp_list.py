#!/usr/bin/env python3
"""Home 02 EXPERIENCE: the calm list with a rack-and-pinion marker column (approved by Zaid 2026-11-18, option M1).
- Current roles: the date reads "START → NOW" and their pinion turns slowly (one turn in 14 s). No red, no pill.
- Hover: soft row tint, title moves 3 px, date brightens, the pinion turns 36°."""
import math

ROLES = [  # role, organisation, period start text, end text (None = ongoing), description
    ("Fab Lab Program Engineer (Instrumentation)",
     "Institute of Appropriate Technology (IAT), Bangladesh University of Engineering and Technology (BUET)",
     "JUL 2026", None, "Instrumentation and fabrication-lab programme work under the HEAT sub-project."),
    ("Freelance CAD Designer", "Independent · 16 client projects", "2023", None,
     "Process-plant layouts, a mining machine, servo mechanisms, composite parts and product renderings."),
    ("FabLab Assistant · Student Operator", "FabLab, Khulna University of Engineering &amp; Technology (KUET)",
     "MAR 2024", "SEP 2025", "3D-printer operation and calibration, printer repair, and CAD / print support for students."),
]


def gear_path(cx, cy, teeth, ro, ri, hole):
    """Spur-gear outline (trapezoid teeth) plus a centre hole, as one SVG path (use fill-rule evenodd)."""
    pts = []
    step = 2 * math.pi / teeth
    for i in range(teeth):
        a = step * i
        for frac, r in [(0.0, ri), (0.18, ro), (0.42, ro), (0.6, ri)]:
            pts.append((cx + r * math.cos(a + frac * step), cy + r * math.sin(a + frac * step)))
    d = "M" + " L".join(f"{px:.2f},{py:.2f}" for px, py in pts) + " Z"
    d += f" M{cx + hole},{cy} A{hole},{hole} 0 1,0 {cx - hole},{cy} A{hole},{hole} 0 1,0 {cx + hole},{cy} Z"
    return d


PINION = (f'<svg viewBox="0 0 24 24" width="26" height="26" aria-hidden="true"><path d="{gear_path(12, 12, 10, 10.5, 8, 2.6)}" '
          f'fill-rule="evenodd"/></svg>')

CSS = """
/* ===== 02 Experience: calm list + rack and pinion ===== */
.xl{border:1px solid var(--line2);border-radius:12px;background:var(--surface);padding:6px 12px}
.xl .it{position:relative;display:grid;grid-template-columns:200px 36px 1fr;gap:0 16px;padding:18px 12px;border-bottom:1px solid var(--line);border-radius:8px;transition:background .25s ease}
.xl .it:last-child{border-bottom-color:transparent}
.xl .xpd{font:600 11.5px 'IBM Plex Mono',monospace;letter-spacing:.08em;color:var(--muted);transition:color .25s ease}
.xl .xpd b{color:var(--strong);font-weight:600}
.xl h3{font-size:16px;line-height:1.3;margin:0;transition:transform .25s ease}
.xl .o{font-size:13.5px;color:var(--body);margin-top:3px}
.xl p{font-size:14px;color:var(--body);margin:6px 0 0;line-height:1.5}
.xl .it:hover{background:var(--surface2)}
.xl .it:hover h3{transform:translateX(3px)}
.xl .it:hover .xpd{color:var(--strong)}
.xl .mk{position:relative;display:flex;justify-content:center;align-self:stretch}
.xl .mk svg{position:relative;z-index:1;left:-2px;margin-top:1px;fill:var(--surface);stroke:var(--muted);stroke-width:1.3;transition:transform .5s ease,stroke .25s ease}
.xl .it:hover .mk svg{stroke:var(--acc-t);transform:rotate(36deg)}
.xl .it.nw .mk svg{animation:xspin 14s linear infinite}
.xl .it.nw:hover .mk svg{animation-duration:5s}
@keyframes xspin{to{transform:rotate(360deg)}}
/* the rack: teeth on the left edge, a solid back on the right; it runs on to the next pinion */
.xl .mk:before{content:"";position:absolute;top:26px;bottom:-38px;left:calc(50% + 10px);width:5px;
  background:repeating-linear-gradient(180deg,var(--line2) 0 2px,transparent 2px 5px) left/3px 100% no-repeat,linear-gradient(var(--line2),var(--line2)) right/2px 100% no-repeat}
.xl .it:last-child .mk:before{bottom:auto;height:16px}
@media (max-width:760px){
  .xl{padding:4px 6px}
  .xl .it{grid-template-columns:28px 1fr;gap:4px 12px;padding:14px 8px}
  .xl .it>.pd{grid-column:2}
  .xl .mk{grid-row:1/3;grid-column:1}
  .xl .it>div:last-child{grid-column:2}
  .xl h3{font-size:15.5px}
}
"""


def html():
    items = ""
    for role, org, start, end, desc in ROLES:
        per = f'{start} → <b>NOW</b>' if end is None else f'{start} → {end}'
        items += (f'<div class="it{" nw" if end is None else ""}"><div class="pd"><span class="xpd">{per}</span></div>'
                  f'<div class="mk">{PINION}</div><div><h3>{role}</h3><div class="o">{org}</div><p>{desc}</p></div></div>')
    return f'<div class="xl">{items}</div>'
