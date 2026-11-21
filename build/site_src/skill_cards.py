#!/usr/bin/env python3
"""Home 05 SKILLS: calm cards with line icons (approved by Zaid 2026-11-18, option C).
Items as a spec-sheet list (approved 2026-11-20, alignment option C): numbered lines with dashed rules,
always two columns (long names wrap inside their cell on narrow screens); the certified tag sits right after the name; a five-item
group leaves its last cell empty. A small line icon per group turns a little on hover."""

GROUPS = [  # code, short, title, items as (name, certified note or "")
    ("CAD / CAM", "CAD", "Design &amp; manufacturing software",
     [("SOLIDWORKS", "CSWP"), ("3DEXPERIENCE", ""), ("Fusion 360 CAM", ""), ("NC programming", ""),
      ("Assemblies &amp; drawings", ""), ("Product rendering", "")]),
    ("OR &amp; DATA", "DATA", "Optimization &amp; analytics",
     [("Python", ""), ("Machine learning", ""), ("Explainable ML", ""), ("Optimization modelling", ""),
      ("Simulation", ""), ("Excel analytics", "")]),
    ("MANUFACTURING", "MFG", "Fabrication &amp; production",
     [("3D printing (FDM)", ""), ("Printer calibration &amp; repair", ""), ("CNC milling · HAAS VF-2", ""),
      ("Fixture design", ""), ("Lean · Six Sigma", ""), ("FabLab operations", "")]),
    ("SUPPLY CHAIN", "SCM", "Logistics &amp; supply chain",
     [("CSCA™ · ISCEA", "CERTIFIED"), ("Network design", ""), ("Route optimization", ""),
      ("Inventory optimization", ""), ("Log-hub Supply Chain Apps", "")]),
]

# simple line icons (24 px grid, stroke = currentColor)
ICONS = {
    "CAD": '<path d="M12 3 20 7.5v9L12 21l-8-4.5v-9Z M12 3v18 M4 7.5l8 4.5 8-4.5"/>',
    "DATA": '<path d="M3 20h18 M5 16l4-5 4 3 6-8"/><circle cx="9" cy="11" r="1.2"/><circle cx="13" cy="14" r="1.2"/><circle cx="19" cy="6" r="1.2"/>',
    "MFG": '<path d="M7 3h10v5H7Z M9 8h6l-1.5 5h-3Z M12 13v3 M5 21h14 M8 18h8"/>',
    "SCM": '<circle cx="5" cy="6" r="2"/><circle cx="19" cy="6" r="2"/><circle cx="12" cy="18" r="2"/><path d="M7 6h10 M6 7.8l5 8.4 M18 7.8l-5 8.4"/>',
}


def icon(k):
    return (f'<svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="1.5" '
            f'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{ICONS[k]}</svg>')


CSS = """
/* ===== 05 Skills: calm cards + icons ===== */
.scert{font:600 9.5px 'IBM Plex Mono',monospace;letter-spacing:.12em;color:var(--acc-t);border:1px solid var(--line2);border-radius:3px;padding:1px 5px;margin-left:8px;vertical-align:1px}
/* C · calm cards with line icons */
.skc{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:16px}
.scard{border:1px solid var(--line2);border-radius:12px;padding:18px 20px;background:var(--surface);transition:border-color .25s ease}
.scard:hover{border-color:var(--strong)}
.scard .top{display:flex;align-items:center;gap:12px}
.scard .ic{display:flex;width:40px;height:40px;border-radius:10px;align-items:center;justify-content:center;background:var(--surface2);color:var(--muted);transition:color .25s ease,transform .5s ease}
.scard:hover .ic{color:var(--acc-t);transform:rotate(-8deg)}
.scard .k{font:600 10.5px 'IBM Plex Mono',monospace;letter-spacing:.12em;color:var(--muted)}
.scard h3{font-size:15.5px;margin:2px 0 0}
.scard .chips{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:0 22px;margin:14px 0 0 52px;border-top:1px solid var(--line)}
.scard .c2{display:grid;grid-template-columns:auto minmax(0,1fr);align-items:baseline;border-bottom:1px dashed var(--line);padding:8px 0;font-size:13.5px;line-height:1.4;color:var(--body);min-width:0}
.scard .c2:before{content:attr(data-n);font:600 10px 'IBM Plex Mono',monospace;letter-spacing:.08em;color:var(--muted);margin-right:10px}
.scard .c2 .scert{margin-left:8px;white-space:nowrap;display:inline-block}
@media (max-width:1300px){.scard .chips{margin-left:0}}
@media (max-width:760px){.scard .chips{gap:0 14px}.scard .c2{font-size:13px}.scard .c2:before{margin-right:7px}}

@media (max-width:760px){.skc{grid-template-columns:1fr}.scard{padding:16px}}
"""


def item(name, note):
    return name + (f'<span class="scert">{note}</span>' if note else "")


def html():
    cards = "".join(f'<div class="scard"><div class="top"><span class="ic">{icon(g[1])}</span><div><div class="k">{g[0]}</div>'
                    f'<h3>{g[2]}</h3></div></div><div class="chips">{"".join(f'<span class="c2" data-n="{i+1:02d}"><span>{n}' + (f'<span class="scert">{c}</span>' if c else "") + "</span></span>" for i, (n, c) in enumerate(g[3]))}</div></div>'
                    for g in GROUPS)
    return f'<div class="skc">{cards}</div>'
