#!/usr/bin/env python3
"""Home 01 EDUCATION as a Gantt chart (approved by Zaid 2026-11-18, option A).
SSC/HSC as milestones, B.Sc. as a done bar, M.Sc. as a live striped bar, tests as dashed bars, TODAY line.
On the real site TODAY is computed from the visitor's date."""

Y0, Y1 = 2017, 2028          # time axis
TODAY = 2026 + 10.5 / 12      # mid Nov 2026 for the mockup


def x(year):
    """Year (decimal) -> percent across the Gantt track."""
    return round((year - Y0) / (Y1 - Y0) * 100, 2)


CSS = """
.qmono{font:600 11.5px 'IBM Plex Mono',monospace;letter-spacing:.08em;color:var(--muted)}
/* ===== A · Gantt chart ===== */
.qg{display:grid;grid-template-columns:420px 1fr;border:1px solid var(--line2);border-radius:10px;background:var(--surface);overflow:hidden}
.qg .ql{border-right:1px solid var(--line2)}
.qg .qr{position:relative}
.qg .qhd{height:38px;border-bottom:1px solid var(--line2);display:flex;align-items:center;padding:0 16px}
.qg .qrow{height:80px;border-bottom:1px solid var(--line);position:relative}
.qg .qrow:last-child{border-bottom:0}
.qg .ql .qrow{padding:12px 16px;display:flex;flex-direction:column;justify-content:center;gap:3px}
.qg .ql h3{font-size:15px;line-height:1.3;margin:0}
.qg .ql .o{font-size:13px;line-height:1.35;color:var(--body);margin:0}
.qg .qloc{font:600 10.5px 'IBM Plex Mono',monospace;letter-spacing:.1em;color:var(--muted)}
.qg .qmo,.qg .qtt{display:none}
.qg .qax span{position:absolute;top:0;height:38px;display:flex;align-items:center;transform:translateX(-50%);font:600 11.5px 'IBM Plex Mono',monospace;color:var(--muted)}
.qg .qgl{position:absolute;top:38px;bottom:0;width:1px;background:var(--line)}
.qg .qbar{position:absolute;top:50%;height:22px;margin-top:-11px;border-radius:4px;background:var(--acc);box-shadow:inset 0 0 0 1px rgba(255,255,255,.15)}
.qg .qbar.qdone{background:color-mix(in srgb,var(--acc) 55%,var(--surface2))}
.qg .qbar.qnow{background:repeating-linear-gradient(135deg,var(--acc) 0 6px,color-mix(in srgb,var(--acc) 70%,#000) 6px 12px);background-size:17px 17px;animation:qstripe 1.2s linear infinite}
@keyframes qstripe{to{background-position:17px 0}}
.qg .qbar.qplan{background:transparent;border:1.5px dashed var(--acc-t);opacity:.9}
.qg .qbar.qfade{-webkit-mask:linear-gradient(90deg,#000 55%,transparent);mask:linear-gradient(90deg,#000 55%,transparent)}
.qg .qdm{position:absolute;top:50%;width:14px;height:14px;margin:-7px 0 0 -7px;transform:rotate(45deg);background:color-mix(in srgb,var(--acc) 55%,var(--surface2));box-shadow:0 0 0 2px var(--surface)}
.qg .qlab{position:absolute;top:50%;transform:translateY(-50%);font:600 11.5px 'IBM Plex Mono',monospace;letter-spacing:.06em;color:var(--body);white-space:nowrap}
.qg .qlab b{color:var(--acc-t);font-weight:600}
@media (max-width:900px){.qg .qcg{display:none}}
.qg .qin{position:absolute;top:50%;transform:translateY(-50%);font:600 11.5px 'IBM Plex Mono',monospace;letter-spacing:.06em;color:#fff;white-space:nowrap;padding-left:10px}
.qg .qtd{position:absolute;top:38px;bottom:0;width:2px;margin-left:-1px;background:var(--acc-t);animation:qtd 2.4s ease-in-out infinite}
.qg .qtd:before{content:"TODAY";position:absolute;top:6px;right:6px;padding:1px 5px;border-radius:3px;background:var(--acc);color:#fff;font:600 10.5px 'IBM Plex Mono',monospace;letter-spacing:.08em}
@keyframes qtd{0%,100%{opacity:1}50%{opacity:.45}}


@media (max-width:760px){
  /* phone: a text block on top of every row, a thin time strip at its foot */
  .qg{grid-template-columns:1fr}
  .qg .ql{display:none}
  .qg .qax span{font-size:10px}
  .qg .qax span:nth-child(even){display:none}
  .qg .qgl{opacity:.55}
  .qg .qr .qrow{height:auto;padding:11px 12px 30px}
  .qg .qmo{display:flex;flex-direction:column;gap:2px;position:relative;z-index:1}
  /* phone: the TODAY line only crosses the time strips, never the text */
  .qg .qtd{top:auto;bottom:0;height:0;background:none;animation:none}
  .qg .qtt{display:block;position:absolute;bottom:4px;height:24px;width:2px;margin-left:-1px;background:var(--acc-t);animation:qtd 2.4s ease-in-out infinite}
  .qg .qmo .t{font:600 14px/1.3 'Space Grotesk',sans-serif;color:var(--strong)}
  .qg .qmo .o{font-size:12.5px;line-height:1.35;color:var(--body)}
  .qg .qmo .m{margin-top:2px;font:600 10.5px 'IBM Plex Mono',monospace;letter-spacing:.06em;color:var(--muted)}
  .qg .qmo .m b{color:var(--acc-t);font-weight:600}
  .qg .qlab,.qg .qin{display:none}
  .qg .qbar{top:auto;bottom:12px;margin-top:0;height:8px;border-radius:3px}
  .qg .qbar.qplan{border-width:1px}
  .qg .qdm{top:auto;bottom:11px;width:10px;height:10px;margin:0 0 0 -5px}
  .qg .qtd:before{top:auto;bottom:6px;right:6px;font-size:9.5px}
}
"""


KUET = "Khulna University of Engineering &amp; Technology (KUET)"

# one row per stage: title, institution, location, desktop track html, phone meta line
def _rows():
    return [
        dict(t="M.Sc. Eng. · Industrial Engineering &amp; Management", tm="M.Sc. Eng. · Industrial Eng. &amp; Management",
             o=KUET, loc="KHULNA · BANGLADESH", m="JUL 2026 → <b>ONGOING</b> · PART-TIME",
             tr=f'<div class="qbar qnow" style="left:{x(2026.5)}%;width:{x(TODAY)-x(2026.5)}%"></div>'
                f'<div class="qbar qplan qfade" style="left:{x(TODAY)}%;width:{x(2028)-x(TODAY)}%"></div>'
                f'<span class="qlab" style="right:{100-x(2026.5)+1}%">JUL 2026 → <b>ONGOING</b> · PART-TIME</span>'),
        dict(t="IELTS Academic · GRE General", tm="IELTS Academic · GRE General",
             o="Language &amp; graduate tests", loc="", m="<b>IN PREPARATION</b> · SCORES ADDED WHEN OUT",
             tr=f'<div class="qbar qplan qfade" style="left:{x(2026.6)}%;width:{x(2028)-x(2026.6)}%"></div>'
                f'<span class="qlab" style="right:{100-x(2026.6)+1}%"><b>IN PREPARATION</b> · scores added when out</span>'),
        dict(t="B.Sc. Eng. · Industrial &amp; Production Engineering", tm="B.Sc. Eng. · Industrial &amp; Production Eng.",
             o=KUET, loc="KHULNA · BANGLADESH", m="BATCH \'19 → SEP 2025 · <b>CGPA 3.45 / 4.00</b>",
             tr=f'<div class="qbar qdone" style="left:{x(2019.9)}%;width:{x(2025.7)-x(2019.9)}%"><span class="qin">BATCH \'19 → SEP 2025<span class="qcg"> · CGPA 3.45 / 4.00</span></span></div>'),
        dict(t="HSC · Science", tm="HSC · Science", o="Dhaka College", loc="DHAKA · BANGLADESH", m="2019 · <b>GPA 5.00</b>",
             tr=f'<div class="qdm" style="left:{x(2019.5)}%"></div><span class="qlab" style="left:{x(2019.5)+1.5}%">2019 · <b>GPA 5.00</b></span>'),
        dict(t="SSC · Science", tm="SSC · Science", o="Armanitola Govt. High School", loc="DHAKA · BANGLADESH", m="2017 · <b>GPA 5.00</b>",
             tr=f'<div class="qdm" style="left:{x(2017.45)}%"></div><span class="qlab" style="left:{x(2017.45)+1.5}%">2017 · <b>GPA 5.00</b></span>'),
    ]


def gantt():
    rows = _rows()
    left = '<div class="qhd qmono">STAGE</div>' + "".join(
        f'<div class="qrow"><h3>{r["t"]}</h3><div class="o">{r["o"]}</div>'
        + (f'<div class="qloc">{r["loc"]}</div>' if r["loc"] else "") + '</div>' for r in rows)
    ax = "".join(f'<span style="left:{x(y)}%">{y}</span>' for y in range(Y0 + 1, Y1))
    gl = "".join(f'<i class="qgl" style="left:{x(y)}%"></i>' for y in range(Y0 + 1, Y1))
    # phone shows a text block (.qmo) on top of each track row; desktop hides it
    right = (f'<div class="qhd qax" style="padding:0;position:relative">{ax}</div>{gl}'
             + "".join(f'<div class="qrow"><div class="qmo"><b class="t">{r["tm"]}</b><span class="o">{r["o"].replace(" (KUET)", "")}'
                       + (f' · {r["loc"].split(" · ")[0].title()}' if r["loc"] and "KUET" not in r["o"] else "")
                       + f'</span><span class="m">{r["m"]}</span></div>{r["tr"]}<i class="qtt" style="left:{x(TODAY)}%"></i></div>' for r in rows)
             + f'<i class="qtd" style="left:{x(TODAY)}%"></i>')
    return f'<div class="qg"><div class="ql">{left}</div><div class="qr">{right}</div></div>'
