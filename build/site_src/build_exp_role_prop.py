#!/usr/bin/env python3
"""Proposal (2026-11-20): Experience role cards without the empty left column.
Zaid: the date column and the gear column leave a large void under them and the date breaks
onto two lines; looks dull. Shows NOW plus three layouts for the same three roles.
Writes ExpRoleProp* boards. Class prefix: zrl."""
import build_edu_detail_prop as P
import exp_data as X
import exp_list as XL

CSS = XL.CSS + """
/* ===== role card proposal (prefix zrl) ===== */
.zrlopt{margin-top:56px}
.zrlopt:first-child{margin-top:8px}
.zrlhd{display:flex;align-items:baseline;gap:12px;flex-wrap:wrap;margin-bottom:16px}
.zrlhd b{font:600 12px 'IBM Plex Mono',monospace;letter-spacing:.12em;color:var(--acc-t)}
.zrlhd span{font:600 17px 'Space Grotesk',sans-serif;color:var(--strong)}
.zrlhd em{font-style:normal;font-size:15px;line-height:1.55;color:var(--muted);flex-basis:100%;max-width:960px}
.zrlst{display:flex;flex-direction:column;gap:18px;max-width:980px}
.zrl-pin svg{fill:var(--surface);stroke:var(--muted);stroke-width:1.3}
.zrl-now .zrl-pin svg{animation:xspin 14s linear infinite;stroke:var(--acc-t)}
.zrl h3{margin:0;font:600 19px/1.35 'Space Grotesk',sans-serif;color:var(--strong)}
.zrl .zrlo{margin-top:4px;font-size:14px;color:var(--body)}
.zrl .zrln{margin-top:6px;font-size:13.5px;line-height:1.55;color:var(--muted)}
.zrl .zrlh{margin:0 0 8px;font:600 10.5px 'IBM Plex Mono',monospace;letter-spacing:.12em;color:var(--muted)}
.zrl ul{margin:0;padding:0;list-style:none;display:flex;flex-direction:column;gap:8px}
.zrl li{display:flex;gap:10px;font-size:14.5px;line-height:1.55;color:var(--body)}
.zrl li:before{content:"";flex:none;width:6px;height:6px;margin-top:8px;background:var(--acc-t);transform:rotate(45deg);opacity:.8}
.zrl .zrltl{display:flex;flex-wrap:wrap;gap:6px}
.zrl .zrltl span{font-size:12.5px;color:var(--body);border:1px solid var(--line2);border-radius:999px;padding:3px 10px;background:var(--surface);white-space:nowrap}
.zrl .zrllk{display:flex;flex-wrap:wrap;gap:8px 16px;margin-top:14px}
.zrl .zrllk a{font:600 11px 'IBM Plex Mono',monospace;letter-spacing:.08em;color:var(--muted);border-bottom:1px dotted var(--line2);padding-bottom:1px}
.zrl .zrllk a:hover{color:var(--acc-t)}
.zrl-dt{font:600 11.5px 'IBM Plex Mono',monospace;letter-spacing:.08em;color:var(--muted);white-space:nowrap}
.zrl-dt b{color:var(--strong);font-weight:600}
.zrl-now .zrl-dt b{color:var(--acc-t)}

/* A · header band: gear + dates + place in one strip on top; body below in two columns */
.zrlA{border:1px solid var(--line2);border-radius:12px;background:var(--surface);overflow:hidden;transition:border-color .3s ease}
.zrlA:hover{border-color:var(--muted)}
.zrlA .zrlbar{display:flex;flex-wrap:wrap;align-items:center;gap:6px 12px;padding:10px 20px;background:var(--surface2);border-bottom:1px solid var(--line2)}
.zrlA .zrlbar .zrlpl{margin-left:auto;font:600 10.5px 'IBM Plex Mono',monospace;letter-spacing:.1em;color:var(--muted)}
.zrlA .zrlbd{padding:18px 22px 20px}
.zrlA .zrlcols{display:grid;grid-template-columns:minmax(0,1.6fr) minmax(0,1fr);gap:26px;margin-top:16px;padding-top:16px;border-top:1px dashed var(--line)}

/* B · rack rail: one rack runs down the left of all roles, each role's gear sits on it */
.zrlB{position:relative;padding-left:46px}
.zrlB:before{content:"";position:absolute;left:14px;top:6px;bottom:6px;width:6px;border-radius:3px;
  background:repeating-linear-gradient(to bottom,var(--line2) 0 4px,transparent 4px 8px);opacity:.9}
.zrlB:after{content:"";position:absolute;left:19px;top:6px;bottom:6px;width:1px;background:var(--line2)}
.zrlB .zrlit{position:relative;border:1px solid var(--line2);border-radius:12px;background:var(--surface);padding:18px 22px 20px;transition:border-color .3s ease}
.zrlB .zrlit:hover{border-color:var(--muted)}
.zrlB .zrl-pin{position:absolute;left:-46px;top:16px;width:34px;height:34px;display:flex;align-items:center;justify-content:center;background:var(--bg);border-radius:50%;z-index:1}
.zrlB .zrlit:before{content:"";position:absolute;left:-14px;top:32px;width:14px;height:1px;background:var(--line2)}
.zrlB .zrltop{display:flex;align-items:baseline;justify-content:space-between;gap:12px;margin-bottom:6px}
.zrlB .zrltl{margin-top:14px;padding-top:12px;border-top:1px dashed var(--line)}
.zrlB .zrltl b{font:600 10.5px 'IBM Plex Mono',monospace;letter-spacing:.12em;color:var(--muted);margin-right:4px;align-self:center}

/* C · spec split: a filled left panel (dates, title, tools) beside the duties */
.zrlC{display:grid;grid-template-columns:minmax(0,.95fr) minmax(0,1.25fr);border:1px solid var(--line2);border-radius:12px;background:var(--surface);overflow:hidden;transition:border-color .3s ease}
.zrlC:hover{border-color:var(--muted)}
.zrlC .zrllp{background:var(--surface2);border-right:1px solid var(--line2);padding:20px 22px;display:flex;flex-direction:column;gap:6px}
.zrlC .zrllp .zrlzt{display:flex;align-items:center;gap:10px;margin-bottom:6px}
.zrlC .zrllp .zrltl{margin-top:auto;padding-top:14px}
.zrlC .zrlrp{padding:20px 22px}

/* D · rack rail + spec split: a toothed rack runs down the left, each role's gear meshes with it,
   and every card is a two-part data sheet (filled left panel, duties on the right) */
.zrlD{position:relative;padding-left:58px;display:flex;flex-direction:column;gap:22px;max-width:1040px}
.zrlD:before{content:"";position:absolute;left:18px;top:8px;bottom:8px;width:8px;border-radius:2px;background:var(--surface2);border:1px solid var(--line2)}
.zrlD:after{content:"";position:absolute;left:27px;top:10px;bottom:10px;width:6px;
  background:repeating-linear-gradient(to bottom,var(--line2) 0 5px,transparent 5px 10px)}
.zrlD .zrldc{position:relative;display:grid;grid-template-columns:minmax(0,.95fr) minmax(0,1.3fr);border:1px solid var(--line2);border-radius:14px;background:var(--surface);overflow:hidden;
  transition:border-color .35s ease,transform .35s ease,box-shadow .35s ease}
.zrlD .zrldw{position:relative}
.zrlD .zrldw:hover .zrldc{border-color:var(--muted);transform:translateX(3px);box-shadow:0 14px 30px rgba(0,0,0,.12)}
.zrlD .zrldg{position:absolute;left:-52px;top:20px;width:40px;height:40px;display:flex;align-items:center;justify-content:center;border-radius:50%;background:var(--bg);z-index:2}
.zrlD .zrldg svg{width:34px;height:34px;fill:var(--surface);stroke:var(--muted);stroke-width:1.2;transition:transform 1.2s ease,stroke .3s ease}
.zrlD .zrldw:hover .zrldg svg{transform:rotate(120deg);stroke:var(--acc-t)}
.zrlD .zrl-now .zrldg svg{animation:xspin 14s linear infinite;stroke:var(--acc-t)}
.zrlD .zrldw:before{content:"";position:absolute;left:-14px;top:40px;width:14px;height:1px;background:var(--line2)}
.zrlD .zrldl{position:relative;background:var(--surface2);border-right:1px solid var(--line2);padding:22px 24px 22px;display:flex;flex-direction:column;gap:6px}
.zrlD .zrldl:before{content:"";position:absolute;left:0;top:22px;width:3px;height:44px;border-radius:0 2px 2px 0;background:var(--line2);transition:background .3s ease,height .35s ease}
.zrlD .zrl-now .zrldl:before,.zrlD .zrldw:hover .zrldl:before{background:var(--acc-t)}
.zrlD .zrldw:hover .zrldl:before{height:64px}
.zrlD .zrldt{display:flex;align-items:center;flex-wrap:wrap;gap:8px 10px;margin-bottom:8px}
.zrlD .zrldt .zrl-dt{font-size:12.5px}
.zrlD .zrlnow{font:600 9.5px 'IBM Plex Mono',monospace;letter-spacing:.14em;color:var(--acc-t);border:1px solid var(--acc-t);border-radius:999px;padding:2px 8px;display:inline-flex;align-items:center;gap:6px}
.zrlD .zrlnow i{width:6px;height:6px;border-radius:50%;background:var(--acc-t);animation:zrlblink 2.4s ease-in-out infinite}
@keyframes zrlblink{0%,100%{opacity:1}50%{opacity:.25}}
.zrlD h3{font-size:20px}
.zrlD .zrldl .zrltl{margin-top:auto;padding-top:16px}
.zrlD .zrldl .zrlh{margin:14px 0 8px}
.zrlD .zrldr{padding:22px 26px 22px}
.zrlD .zrldr li{font-size:15px}
.zrlD .zrldr .zrllk{margin-top:16px;padding-top:12px;border-top:1px dashed var(--line)}
@media (prefers-reduced-motion:reduce){.zrlD .zrldw:hover .zrldc{transform:none}.zrlD .zrlnow i{animation:none}}
@media (max-width:900px){.zrlD .zrldc{grid-template-columns:1fr}.zrlD .zrldl{border-right:0;border-bottom:1px solid var(--line2)}}
@media (max-width:760px){
  .zrlD{padding-left:40px;gap:16px}.zrlD:before{left:9px;width:6px}.zrlD:after{left:16px;width:5px}
  .zrlD .zrldg{left:-40px;top:14px;width:32px;height:32px}.zrlD .zrldg svg{width:28px;height:28px}
  .zrlD .zrldw:before{left:-10px;width:10px;top:30px}
  .zrlD .zrldl,.zrlD .zrldr{padding:16px}
  .zrlD h3{font-size:17px}
}

/* tools variants for D */
.zrtg{display:grid;grid-template-columns:repeat(var(--zc),minmax(0,1fr));gap:8px;margin-top:2px}
.zrtt{display:flex;flex-direction:column;gap:8px;padding:10px 10px 9px;border:1px solid var(--line2);border-radius:10px;background:var(--surface);min-width:0;transition:border-color .3s ease,transform .3s ease}
.zrtt i{display:flex;width:30px;height:30px;align-items:center;justify-content:center;border-radius:8px;background:var(--surface2);color:var(--muted);transition:color .3s ease}
.zrtt b{font-weight:500;font-size:13px;line-height:1.3;color:var(--strong)}
.zrtt:hover{border-color:var(--acc-t);transform:translateY(-2px)}
.zrtt:hover i{color:var(--acc-t)}
.zrtls{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:0 18px;border-top:1px solid var(--line)}
.zrtl{display:flex;align-items:baseline;padding:7px 0;border-bottom:1px dashed var(--line);font-size:13.5px;color:var(--body);min-width:0}
.zrtl:before{content:attr(data-n);font:600 10px 'IBM Plex Mono',monospace;letter-spacing:.08em;color:var(--muted);margin-right:9px}
.zrldb{grid-column:1/-1;display:flex;align-items:center;gap:16px;padding:12px 24px;border-top:1px solid var(--line2);background:var(--surface)}
.zrldb .zrlh{margin:0;flex:none}
.zrtpb{flex:1;display:flex;flex-wrap:wrap;gap:7px;padding:8px 10px;border:1px solid var(--line2);border-radius:9px;
  background-color:var(--surface2);background-image:radial-gradient(var(--line2) 1.1px,transparent 1.2px);background-size:12px 12px;background-position:6px 6px}
.zrtp{display:inline-flex;align-items:center;gap:6px;padding:4px 10px 4px 8px;background:var(--surface);border:1px solid var(--line2);border-radius:6px;font-size:12.5px;color:var(--strong);white-space:nowrap;box-shadow:0 2px 6px rgba(0,0,0,.10);transition:transform .3s ease,border-color .3s ease}
.zrtp i{display:flex;color:var(--muted)}
.zrtp i svg{width:15px;height:15px}
.zrtp:hover{transform:rotate(-2deg);border-color:var(--acc-t)}
.zrtp:hover i{color:var(--acc-t)}
@media (max-width:760px){.zrtg{--zc:2!important}.zrtls{grid-template-columns:1fr 1fr}.zrldb{flex-direction:column;align-items:stretch;gap:8px;padding:12px 14px}}

@media (max-width:900px){.zrlA .zrlcols{grid-template-columns:1fr;gap:16px}.zrlC{grid-template-columns:1fr}.zrlC .zrllp{border-right:0;border-bottom:1px solid var(--line2)}}
@media (max-width:760px){
  .zrlA .zrlbar{padding:9px 14px}.zrlA .zrlbd{padding:14px}
  .zrlB{padding-left:36px}.zrlB:before{left:9px}.zrlB:after{left:14px}
  .zrlB .zrl-pin{left:-36px;width:30px;height:30px}.zrlB .zrlit{padding:14px}.zrlB .zrlit:before{left:-10px;width:10px}
  .zrlB .zrltop{flex-direction:column;gap:2px}
  .zrlC .zrllp,.zrlC .zrlrp{padding:14px}
  .zrl h3{font-size:17px}
}
"""


def per(r):
    return f'{r["start"]} → <b>NOW</b>' if r["end"] is None else f'{r["start"]} → <b>{r["end"]}</b>'


def lis(r):
    return "".join(f"<li>{d}</li>" for d in r["do"])


def tools(r):
    return "".join(f"<span>{t.strip()}</span>" for t in r["tools"].split("·"))


def links(r):
    ls = "".join(f'<a href="{u}">{t} →</a>' for t, u in r["links"])
    return f'<div class="zrllk">{ls}</div>' if ls else ""


def head(r):
    return f'<h3>{r["title"]}</h3><div class="zrlo">{r["org"]} · {r["place"]}</div><div class="zrln">{r["note"]}</div>'


def opt_a(r):
    now = " zrl-now" if r["end"] is None else ""
    return (f'<article class="zrl zrlA{now}"><div class="zrlbar"><span class="zrl-pin">{XL.PINION}</span><span class="zrl-dt">{per(r)}</span>'
            f'<span class="zrlpl">{r["place"].upper()}</span></div><div class="zrlbd">{head(r)}'
            f'<div class="zrlcols"><div><div class="zrlh">WHAT I DO</div><ul>{lis(r)}</ul></div>'
            f'<div><div class="zrlh">TOOLS</div><div class="zrltl">{tools(r)}</div>{links(r)}</div></div></div></article>')


def opt_b(roles):
    out = ""
    for r in roles:
        now = " zrl-now" if r["end"] is None else ""
        out += (f'<article class="zrl zrlit{now}"><span class="zrl-pin">{XL.PINION}</span>'
                f'<div class="zrltop"><span class="zrl-dt">{per(r)}</span></div>{head(r)}'
                f'<div class="zrlh" style="margin-top:14px">WHAT I DO</div><ul>{lis(r)}</ul>'
                f'<div class="zrltl"><b>TOOLS</b>{tools(r)}</div>{links(r)}</article>')
    return f'<div class="zrlB zrlst">{out}</div>'


def opt_c(r):
    now = " zrl-now" if r["end"] is None else ""
    return (f'<article class="zrl zrlC{now}"><div class="zrllp"><div class="zrlzt"><span class="zrl-pin">{XL.PINION}</span><span class="zrl-dt">{per(r)}</span></div>'
            f'{head(r)}<div class="zrltl">{tools(r)}</div></div>'
            f'<div class="zrlrp"><div class="zrlh">WHAT I DO</div><ul>{lis(r)}</ul>{links(r)}</div></article>')


TICON = {
    "printer": '<path d="M4 3h16v18H4z M4 8h16 M11 8v4l1 2 1-2V8 M7 17h10"/>',
    "cnc": '<path d="M9 3h6v6H9z M12 9v5 M10 14h4 M4 18h16 M6 18v3 M18 18v3"/>',
    "laser": '<path d="M3 5h18v5H3z M12 10v5 M8 19h8 M9 15l3 4 3-4"/>',
    "pcb": '<rect x="7" y="7" width="10" height="10" rx="1"/><path d="M10 3v4 M14 3v4 M10 17v4 M14 17v4 M3 10h4 M3 14h4 M17 10h4 M17 14h4"/>',
    "scope": '<rect x="3" y="5" width="18" height="12" rx="2"/><path d="M5 12h3l2-4 3 8 2-4h4 M9 21h6"/>',
    "iot": '<path d="M5 11a10 10 0 0 1 14 0 M8 14a5.5 5.5 0 0 1 8 0"/><circle cx="12" cy="18" r="1.3"/>',
    "layers": '<path d="M12 3l9 5-9 5-9-5z M3 13l9 5 9-5"/>',
    "cad": '<path d="M12 3 20 7.5v9L12 21l-8-4.5v-9Z M12 3v18 M4 7.5l8 4.5 8-4.5"/>',
    "render": '<circle cx="12" cy="12" r="4"/><path d="M12 2v3 M12 19v3 M2 12h3 M19 12h3 M5 5l2 2 M17 17l2 2 M5 19l2-2 M17 7l2-2"/>',
    "image": '<rect x="3" y="5" width="18" height="14" rx="2"/><circle cx="9" cy="10" r="1.5"/><path d="M21 16l-5-5-8 8"/>',
}
TMAP = {"3D printers": "printer", "FDM 3D printers": "printer", "CNC": "cnc", "laser cutter": "laser", "PCB tools": "pcb",
        "oscilloscope": "scope", "IoT kits": "iot", "slicers": "layers", "SOLIDWORKS": "cad", "Fusion 360": "cad",
        "KeyShot": "render", "Photoshop": "image"}


def ticon(name):
    k = TMAP.get(name, "cad")
    return (f'<svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="1.5" '
            f'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{TICON[k]}</svg>')


def tool_block(r, mode):
    names = [t.strip() for t in r["tools"].split("·")]
    if mode == "tiles":
        cols = 3 if len(names) % 3 == 0 else 2
        cells = "".join(f'<span class="zrtt"><i>{ticon(n)}</i><b>{n}</b></span>' for n in names)
        return f'<div class="zrtg" style="--zc:{cols}">{cells}</div>'
    if mode == "list":
        cells = "".join(f'<span class="zrtl" data-n="{i+1:02d}">{n}</span>' for i, n in enumerate(names))
        return f'<div class="zrtls">{cells}</div>'
    cells = "".join(f'<span class="zrtp"><i>{ticon(n)}</i>{n}</span>' for n in names)
    return f'<div class="zrtpb">{cells}</div>'


def opt_d(roles, mode="pegboard"):
    out = ""
    for r in roles:
        now = " zrl-now" if r["end"] is None else ""
        left_tools = "" if mode == "pegboard" else f'<div class="zrlh">TOOLS</div>{tool_block(r, mode)}'
        strip = f'<div class="zrldb"><span class="zrlh">TOOLS</span>{tool_block(r, mode)}</div>' if mode == "pegboard" else ""
        out += (f'<div class="zrl zrldw{now}"><span class="zrldg" aria-hidden="true">{XL.PINION}</span><article class="zrldc">'
                f'<div class="zrldl"><div class="zrldt"><span class="zrl-dt">{per(r)}</span></div>{head(r)}{left_tools}</div>'
                f'<div class="zrldr"><div class="zrlh">WHAT I DO</div><ul>{lis(r)}</ul>{links(r)}</div>{strip}</article></div>')
    return f'<div class="zrlD">{out}</div>'


def now_cards():
    import build_exp_page_prop as XP
    return '<div class="zrlst">' + "".join(XP.role(r) for r in X.ROLES) + "</div>"


OPTS = [
    ("D3", "Pegboard, compact", "The pegboard you liked, made smaller: no peg dots, smaller tags, and the board moves out of the left panel into one thin strip across the bottom of the card. The left panel no longer grows taller than the duties, so neither side is left empty. On phone the strip stacks under the card."),
]


def page_body():
    out = ""
    for code, title, note in OPTS:
        mode = "pegboard"
        out += (f'<div class="zrlopt"><div class="zrlhd"><b>OPTION {code}</b>'
                f'<span>{title}</span><em>{note}</em></div>{opt_d(X.ROLES, mode)}</div>')
    return out


def body():
    return f"""
  <main class="wrap" style="position:relative;z-index:1">
    <section class="ph">
      <div class="crumb">PROPOSAL / EXPERIENCE · ROLE CARDS · OPTION D</div>
      <h1 class="h1">Role cards · tools</h1>
      <p class="lead">Option D (rack rail + spec split) with the tools on a compact pegboard strip. If this is right, it goes into the Experience page.</p>
    </section>
    <div class="dopt">{page_body()}</div>
  </main>
"""


def page(theme, title):
    import build_exp_page_prop as XP
    html = P.H.page(theme, title)
    html = html.replace("<style>", "<style>" + P.EG.CSS + P.CSS + XP.CSS + CSS, 1)
    a = html.index("  <!-- Hero: static page backdrop")
    e = html.index("  </main>") + len("  </main>")
    return html[:a] + body() + html[e:]


if __name__ == "__main__":
    import type_scale as TS
    out = "/home/claude/zaid/project"
    for key, name in [("dark", "ExpRoleProp"), ("light", "ExpRolePropLight"), ("dark", "ExpRolePropMobile"), ("light", "ExpRolePropMobileLight")]:
        open(f"{out}/{name}.dc.html", "w").write(TS.apply(page(key, f"Role card proposal · {name}")))
    print("role card proposal written")
