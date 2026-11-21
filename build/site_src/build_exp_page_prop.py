"""Proposal: Experience page in full. Same frame as Education and Research (stats strip, sticky index).
Work roles with the rack-and-pinion marker from Home, the freelance job list (no client names),
campus leadership in detail (certificates shown here too), and hands-on training."""
import build_edu_detail_prop as P
import exp_data as X
import slideshow as S
import exp_list as XL

CERT = {"Certificate of Recognition": "/_blob/169902addf7f1a39bd48a849c875b850",
        "Certificate of Contribution": "/_blob/0bdd9adeab3f032d3ec45ef8f9758214",
        "Certificate of Achievement": "/_blob/446c08a24635e6e33fe257c41dbbdfcd"}

CSS = XL.CSS + """
/* ===== experience page (prefix xq) ===== */
.xqr{display:grid;grid-template-columns:150px 36px minmax(0,1fr);gap:0 16px;border:1px solid var(--line2);border-radius:12px;background:var(--surface);padding:22px 24px 20px;margin-top:16px}
.xqr+.xqr{margin-top:18px}
.xqd{font:600 11.5px 'IBM Plex Mono',monospace;letter-spacing:.08em;color:var(--muted);padding-top:3px}
.xqd b{color:var(--strong);font-weight:600}
.xqr .mk{display:flex;justify-content:center}
.xqr .mk svg{fill:var(--surface);stroke:var(--muted);stroke-width:1.3}
.xqr.nw .mk svg{animation:xspin 14s linear infinite;stroke:var(--acc-t)}
.xqr h3{margin:0;font:600 19px/1.35 'Space Grotesk',sans-serif;color:var(--strong)}
.xqo{margin-top:4px;font-size:14px;color:var(--body)}
.xqn{margin-top:6px;font-size:13.5px;line-height:1.55;color:var(--muted)}
.xqh{margin:16px 0 6px;font:600 10.5px 'IBM Plex Mono',monospace;letter-spacing:.12em;color:var(--muted)}
.xql{margin:0;padding:0;list-style:none;display:flex;flex-direction:column;gap:7px}
.xql li{display:flex;gap:10px;font-size:14.5px;line-height:1.55;color:var(--body)}
.xql li:before{content:"";flex:none;width:6px;height:6px;margin-top:8px;background:var(--acc-t);transform:rotate(45deg);opacity:.8}
.xqt{margin-top:14px;padding-top:10px;border-top:1px dashed var(--line);font-size:13.5px;color:var(--body)}
.xqt b{font:600 10.5px 'IBM Plex Mono',monospace;letter-spacing:.12em;color:var(--muted);margin-right:10px}
.xqk{display:flex;flex-wrap:wrap;gap:8px 18px;margin-top:12px}
.xqk a{font:600 11px 'IBM Plex Mono',monospace;letter-spacing:.08em;color:var(--muted);border-bottom:1px dotted var(--line2);padding-bottom:1px;transition:color .25s ease}
.xqk a:hover{color:var(--acc-t)}
.xqj{border:1px solid var(--line2);border-radius:12px;background:var(--surface);overflow:hidden;margin-top:16px}
.xqj>div{display:grid;grid-template-columns:70px minmax(0,1fr) minmax(0,1.25fr);gap:0 18px;padding:11px 18px;border-top:1px dashed var(--line);transition:background .25s ease}
.xqj>div:first-child{border-top:0;background:var(--surface2);font:600 10.5px 'IBM Plex Mono',monospace;letter-spacing:.12em;color:var(--muted)}
.xqj>div:not(:first-child):hover{background:var(--surface2)}
.xqj .xqy{font:600 12px 'IBM Plex Mono',monospace;color:var(--muted)}
.xqj .xqjj{font-size:14.5px;color:var(--strong);font-weight:500}
.xqj .xqw2{font-size:13.5px;line-height:1.5;color:var(--body)}
.xqj>div.xqny{border-top:1px solid var(--line2)}
.xqc{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:16px;margin-top:16px}
.xqc>article{border:1px solid var(--line2);border-radius:12px;background:var(--surface);padding:18px 20px;display:grid;grid-template-columns:minmax(0,1fr) auto;gap:14px;align-items:start}
.xqc .xqtg{font:600 10.5px 'IBM Plex Mono',monospace;letter-spacing:.1em;color:var(--acc-t)}
.xqc h4{margin:6px 0 0;font:600 16px/1.35 'Space Grotesk',sans-serif;color:var(--strong)}
.xqc .xqoo{margin-top:3px;font-size:13.5px;color:var(--muted)}
.xqc p{margin:8px 0 0;font-size:14px;line-height:1.55;color:var(--body)}
.xqc .xqth{display:block;width:132px;cursor:zoom-in;border-radius:6px;overflow:hidden;border:1px solid var(--line);background:#fff;box-shadow:0 1px 2px rgba(0,0,0,.08);transition:transform .35s ease,box-shadow .35s ease}
.xqc .xqth:hover{transform:translateY(-2px) rotate(-.6deg);box-shadow:0 8px 20px rgba(0,0,0,.16)}
.xqc .xqth img{display:block;width:100%;height:auto}
.xqc .xqth+small{display:block;margin-top:5px;font:600 9.5px 'IBM Plex Mono',monospace;letter-spacing:.08em;color:var(--muted);text-align:center}
.xqc>article.xqone{grid-template-columns:1fr}
.xqc>article.xqwide{grid-column:1/-1}
.xqgal{display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:18px 14px;margin-top:18px}
.xqg{display:flex;flex-direction:column;gap:6px;cursor:zoom-in;min-width:0}
.xqg img{display:block;width:100%;aspect-ratio:4/3;object-fit:cover;border-radius:6px;border:1px solid var(--line);transition:transform .35s ease,box-shadow .35s ease}
.xqg-bootcamp .xqg:first-child img{object-fit:contain;background:#fff}
.xqg:hover img{transform:translateY(-2px);box-shadow:0 8px 20px rgba(0,0,0,.18)}
.xqg span{font-size:13px;line-height:1.4;color:var(--muted)}
.xqg span b{display:block;font:600 9.5px 'IBM Plex Mono',monospace;letter-spacing:.1em;color:var(--body);margin-bottom:1px}
.xqg-cnc{grid-template-columns:repeat(4,minmax(0,1fr))}  /* 12 photos: 4 x 3, 3 x 4, 2 x 6, rows always full */
@media (max-width:1300px){.xqgal{grid-template-columns:repeat(3,minmax(0,1fr))}}
@media (max-width:760px){.xqgal{grid-template-columns:1fr 1fr;gap:10px 8px}}
@media (max-width:1100px){.xqc{grid-template-columns:1fr}}
@media (max-width:760px){
  .xqr{grid-template-columns:28px minmax(0,1fr);gap:4px 12px;padding:16px 14px}
  .xqr .mk{grid-row:1/4;grid-column:1;justify-content:flex-start}
  .xqr>.xqd{grid-column:2}.xqr>div:last-child{grid-column:2}
  .xqr h3{font-size:17px}
  .xqj>div{grid-template-columns:44px minmax(0,1fr);gap:2px 10px;padding:10px 12px}
  .xqj .xqw2{grid-column:2}
  .xqj>div:first-child{display:none}
  .xqc>article{grid-template-columns:1fr;padding:16px 14px}
  .xqc>article>div:last-child:has(.xqth){display:flex;flex-direction:column;align-items:center}
  .xqc .xqth{width:100%;max-width:300px;margin:4px auto 0}
  .xqc .xqth+small{text-align:center}
}
"""

LB = []
VIEW = []   # slideshow viewers; the page shell puts them before </body>


def role_d(r):
    """Approved 2026-11-20: rack rail + spec split card with a compact tools pegboard strip."""
    import build_exp_role_prop as RP
    now = " zrl-now" if r["end"] is None else ""
    strip = f'<div class="zrldb"><span class="zrlh">TOOLS</span>{RP.tool_block(r, "pegboard")}</div>'
    return (f'<div class="zrlD zrl1"><div class="zrl zrldw{now}"><span class="zrldg" aria-hidden="true">{XL.PINION}</span><article class="zrldc">'
            f'<div class="zrldl"><div class="zrldt"><span class="zrl-dt">{RP.per(r)}</span></div>{RP.head(r)}</div>'
            f'<div class="zrldr"><div class="zrlh">WHAT I DO</div><ul>{RP.lis(r)}</ul>{RP.links(r)}</div>{strip}</article></div></div>')


def role(r):
    per = f'{r["start"]} → <b>NOW</b>' if r["end"] is None else f'{r["start"]} → {r["end"]}'
    lis = "".join(f"<li>{d}</li>" for d in r["do"])
    links = "".join(f'<a href="{u}">{t} →</a>' for t, u in r["links"])
    return (f'<article class="xqr{" nw" if r["end"] is None else ""}"><div class="xqd">{per}</div><div class="mk">{XL.PINION}</div><div>'
            f'<h3>{r["title"]}</h3><div class="xqo">{r["org"]} · {r["place"]}</div><div class="xqn">{r["note"]}</div>'
            f'<div class="xqh">WHAT I DO</div><ul class="xql">{lis}</ul>'
            f'<div class="xqt"><b>TOOLS</b>{r["tools"]}</div>'
            + (f'<div class="xqk">{links}</div>' if links else "") + "</div></article>")


def jobs():
    rows = '<div><span>YEAR</span><span>JOB</span><span>WHAT WAS DELIVERED</span></div>'
    last = None
    for y, j, w in X.JOBS:
        ny = " xqny" if (last is not None and y != last) else ""
        rows += f'<div class="{ny.strip()}"><span class="xqy">{y if y != last else ""}</span><span class="xqjj">{j}</span><span class="xqw2">{w}</span></div>'
        last = y
    return f'<div class="xqj">{rows}</div>'


def campus(items):
    out = ""
    for c in items:
        th = ""
        if c.get("cert"):
            lid = "xlb-" + c["cert"].split()[-1].lower()
            LB.append(f'<input type="checkbox" class="elbc" id="{lid}"><label class="elb" for="{lid}"><img src="{CERT[c["cert"]]}" alt="{c["cert"]}"><span>CLOSE ×</span></label>')
            th = f'<div><label class="xqth" for="{lid}"><img src="{CERT[c["cert"]]}" alt="{c["cert"]}"></label><small>CLICK TO ENLARGE</small></div>'
        if c.get("photos"):
            th = ""
            gal = ""
            key = c["photos"]
            rid, viewer = S.group("x" + key, [(src, f"{step.capitalize()}: {cap}") for src, step, cap in X.PHOTOS[key]], {"cnc": "HAAS VF-2", "bootcamp": "SOLIDWORKS BOOTCAMP"}.get(key, ""))
            VIEW.append(viewer)
            for i, (src, step, cap) in enumerate(X.PHOTOS[key]):
                gal += f'<label class="xqg" for="{rid(i)}" title="Click to open the slideshow"><img src="{src}" alt="{cap}"><span><b>{i+1:02d} · {step}</b>{cap}</span></label>'
            out += (f'<article class="xqone xqwide"><div><div class="xqtg">{c["when"]}</div><h4>{c["title"]}</h4><div class="xqoo">{c["org"]}</div>'
                    f'<p>{c["text"]}</p><div class="xqgal xqg-{key}">{gal}</div></div></article>')
            continue
        out += (f'<article class="{"" if th else "xqone"}"><div><div class="xqtg">{c["when"]}</div><h4>{c["title"]}</h4><div class="xqoo">{c["org"]}</div>'
                f'<p>{c["text"]}</p></div>{th}</article>')
    return f'<div class="xqc">{out}</div>'


def page_body():
    LB.clear()
    VIEW.clear()
    work = (P.head("01", "WORK", "Roles, newest first", "work")
            + P.sub("--x11", "1.1", "IAT, BUET · NOW", role_d(X.ROLES[0]))
            + P.sub("--x12", "1.2", "FABLAB, KUET", role_d(X.ROLES[1])))
    free = (P.head("02", "FREELANCE", "CAD for clients, since 2023", "free")
            + P.sub("--x21", "2.1", "THE ROLE", role_d(X.ROLES[2]))
            + P.sub("--x22", "2.2", f"CLIENT JOBS · {len(X.JOBS)}", jobs()))
    camp = (P.head("03", "CAMPUS", "Leadership and service at KUET", "camp")
            + P.sub("--x31", "3.1", "ROLES AND RECOGNITION · 4", campus(X.CAMPUS)))
    trn = (P.head("04", "TRAINING", "Hands-on training", "trn")
           + P.sub("--x41", "4.1", "MACHINES AND SOFTWARE · 2", campus(X.TRAINING)))
    nav = [("--w1", "work", "01", "WORK", [("--x11", "1.1", "IAT, BUET"), ("--x12", "1.2", "FabLab, KUET")]),
           ("--w2", "free", "02", "FREELANCE", [("--x21", "2.1", "The role"), ("--x22", "2.2", "Client jobs")]),
           ("--w3", "camp", "03", "CAMPUS", [("--x31", "3.1", "Roles &amp; recognition")]),
           ("--w4", "trn", "04", "TRAINING", [("--x41", "4.1", "Machines &amp; software")])]
    idx = '<nav class="eix" aria-label="On this page"><span class="ixh">ON THIS PAGE</span>'
    for k, (tl, hid, n, lab, subs) in enumerate(nav):
        on = " ion" if k == 0 else ""
        sl = "".join(f'<label for="go-{t[2:]}" style="animation-timeline:{t}" class="ixl{" ion" if (k == 0 and j == 0) else ""}"><b>{sn}</b>{sl_}</label>'
                     for j, (t, sn, sl_) in enumerate(subs))
        idx += (f'<div class="ixg{on}"><label for="go-{hid}" class="ixl{on}" style="animation-timeline:{tl}"><i>{n}</i>{lab}</label>'
                + (f'<div class="ixs" style="animation-timeline:{tl}"><div>{sl}</div></div>' if subs else "") + "</div>")
    idx += "</nav>"
    secs = "".join(f'<section class="esc" style="view-timeline-name:{tl}">{P.GO(hid)}{body}</section>'
                   for tl, hid, body in (("--w1", "work", work), ("--w2", "free", free), ("--w3", "camp", camp), ("--w4", "trn", trn)))
    return f"""
    <div class="epz">
      <div class="eph"><div class="crumb">HOME / EXPERIENCE</div><h1 class="h1">Experience</h1>
        <p>Fabrication labs, CAD for clients and service on campus: a lab programme engineer at IAT, BUET now, after a year and a half running the FabLab machines at KUET, with freelance CAD work alongside since 2023.</p></div>
      <div class="est"><div><b>3</b><span>roles since 2023</span></div><div><b>{len(X.JOBS)}</b><span>client CAD jobs</span></div>
        <div><b>18</b><span>months in the KUET FabLab</span></div><div><b>4</b><span>campus roles</span></div></div>
      <div class="edw xqw">{idx}<div>{secs}</div></div>
      {"".join(LB)}
    </div>"""


def body():
    return f"""
  <main class="wrap" style="position:relative;z-index:1">
    <section class="ph">
      <div class="crumb">PROPOSAL / EXPERIENCE PAGE · FOR REVIEW, NOT APPLIED</div>
      <h1 class="h1">Experience page · in full</h1>
      <p class="lead">Same frame as Education and Research. Everything inside the box is the page itself.</p>
    </section>
    <div class="dnote">
      <div><b>ROLES IN DETAIL</b>Each role: dates with the turning pinion from Home, what I do, tools, and links to proof. IAT duties follow the HEAT job description.</div>
      <div><b>CLIENT JOBS, NO NAMES</b>All {len(X.JOBS)} jobs from the client-projects folder by year and type, with what was delivered. Client names are left out.</div>
      <div><b>CAMPUS IN FULL</b>Leadership and recognition live here in detail with their certificates; Education keeps the short version and links here.</div>
    </div>
    <div class="dopt">{page_body()}</div>
  </main>
"""


def page(theme, title):
    html = P.H.page(theme, title)
    html = html.replace("<style>", "<style>" + P.EG.CSS + P.CSS + CSS + "\n.edw.xqw{timeline-scope:--w1,--w2,--w3,--w4,--x11,--x12,--x21,--x22,--x31,--x41}", 1)
    a = html.index("  <!-- Hero: static page backdrop")
    e = html.index("  </main>") + len("  </main>")
    html = html[:a] + body() + html[e:]
    return html.replace('<a href="#">Experience</a>', '<a href="#" class="on" aria-current="page">Experience</a>', 1)


if __name__ == "__main__":
    out = "/home/claude/zaid/project"
    for key, name in [("dark", "ExpPgProp"), ("dark_blue", "ExpPgPropBlue"), ("dark_green", "ExpPgPropGreen"),
                      ("light", "ExpPgPropLight"), ("light_blue", "ExpPgPropLightBlue"), ("light_green", "ExpPgPropLightGreen"),
                      ("dark", "ExpPgPropMobile")]:
        open(f"{out}/{name}.dc.html", "w").write(page(key, f"Experience page proposal · {name}"))
    print("experience proposal written")
