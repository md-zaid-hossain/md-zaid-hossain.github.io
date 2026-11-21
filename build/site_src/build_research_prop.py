"""Proposal: Research page in full. Same page frame as the Education page (stats strip, sticky index),
one calm study card per paper: what was asked, how, what was found, key numbers, one figure from the paper."""
import videoplayer as VP
import build_edu_detail_prop as P
import research_data as R

CSS = """
/* ===== research page: study cards (prefix rz) ===== */
.rzth{margin:6px 0 0;font:600 11px 'IBM Plex Mono',monospace;letter-spacing:.1em;color:var(--muted)}
.rzth b{color:var(--body);font-weight:600}
.rzc{display:grid;grid-template-columns:minmax(0,1.25fr) minmax(0,1fr);gap:0;border:1px solid var(--line2);border-radius:12px;background:var(--surface);overflow:hidden;margin-top:16px}
.rzc+.rzc{margin-top:18px}
.rzt{padding:22px 24px 18px;min-width:0}
.rztg{font:600 11px 'IBM Plex Mono',monospace;letter-spacing:.1em;color:var(--muted)}
.rztg b{color:var(--strong);font-weight:600}
.rztg em{font-style:normal;color:var(--acc-t)}
.rzt h3{margin:8px 0 0;font:600 18px/1.38 'Space Grotesk',sans-serif;color:var(--strong)}
.rzv{margin-top:8px;font-size:13.5px;color:var(--body)}
.rza{margin-top:3px;font-size:13.5px;line-height:1.5;color:var(--muted)}
.rza b{color:var(--strong);font-weight:600}
.rzau{white-space:nowrap}
.rzs{margin:16px 0 0;display:flex;flex-direction:column;border-top:1px solid var(--line)}
.rzs>div{display:grid;grid-template-columns:78px minmax(0,1fr);gap:14px;padding:10px 0;border-bottom:1px dashed var(--line)}
.rzs dt{font:600 10.5px 'IBM Plex Mono',monospace;letter-spacing:.1em;color:var(--muted);padding-top:2px}
.rzs dd{margin:0;font-size:14px;line-height:1.55;color:var(--body)}
.rzk{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));margin-top:14px;border:1px solid var(--line);border-radius:8px;overflow:hidden}
.rzk.k3{grid-template-columns:repeat(3,minmax(0,1fr))}
.rzk.k2{grid-template-columns:1fr 1fr;margin-top:0;background:var(--surface)}.rzk.k2>div:nth-child(3){border-left:0}.rzk.k2>div:nth-child(n+3){border-top:1px solid var(--line)}
.rzk>div{padding:9px 12px;border-left:1px solid var(--line);min-width:0}
.rzk>div:first-child{border-left:0}
.rzk b{display:block;font:500 16px 'IBM Plex Mono',monospace;color:var(--strong);white-space:nowrap}
.rzk span{display:block;margin-top:2px;font-size:12px;line-height:1.3;color:var(--muted)}
.rzl{display:flex;flex-wrap:wrap;align-items:center;gap:8px 18px;margin-top:14px}
.rzl a{font:600 11px 'IBM Plex Mono',monospace;letter-spacing:.1em;color:var(--muted);border-bottom:1px dotted var(--line2);padding-bottom:1px;transition:color .25s ease,border-color .25s ease}
.rzl a:hover{color:var(--acc-t);border-bottom-color:var(--acc-t)}
.rzl .rzm{margin-left:auto;font:600 10.5px 'IBM Plex Mono',monospace;letter-spacing:.08em;color:var(--muted);white-space:nowrap}
.rzl .rzm b{font:500 12px 'IBM Plex Mono',monospace;color:var(--body);margin-left:4px}
details.rzab{margin-top:12px;border-top:1px solid var(--line)}
details.rzab summary{list-style:none;cursor:pointer;display:flex;justify-content:space-between;padding:10px 0 2px;font:600 10.5px 'IBM Plex Mono',monospace;letter-spacing:.1em;color:var(--muted)}
details.rzab summary::-webkit-details-marker{display:none}
details.rzab summary i{font-style:normal;transition:transform .25s ease}
details.rzab[open] summary i{transform:rotate(45deg);color:var(--acc-t)}
details.rzab summary:hover{color:var(--strong)}
details.rzab p{margin:8px 0 4px;font-size:13.5px;line-height:1.65;color:var(--body);text-align:justify;hyphens:auto;-webkit-hyphens:auto}
.rzf figure{margin:0;display:flex;flex-direction:column;gap:10px}
.rzf .rzl{margin-top:2px}.rzf .rzl .rzm{margin-left:0;width:100%}
.rzf{margin:0;border-left:1px solid var(--line2);background:var(--surface2);display:flex;flex-direction:column;justify-content:flex-start;padding:22px 20px;gap:16px;min-width:0}
.rzf figcaption{font:600 10px 'IBM Plex Mono',monospace;letter-spacing:.08em;line-height:1.5;color:var(--muted)}
.rzf figcaption b{color:var(--body);font-weight:600}
.rzo{border:1px solid var(--line2);border-radius:12px;background:var(--surface);padding:20px 24px 18px;margin-top:16px}
.rzo+.rzo{margin-top:18px}
.rzo .rztg em{color:var(--acc-t)}
.rzo p{margin:10px 0 0;font-size:14px;line-height:1.6;color:var(--body);max-width:900px}
.rzo p.rzn{color:var(--muted);font-size:13.5px}
.edw.rzw{timeline-scope:--q1,--q2,--r11,--r12,--r21}
.rzmd{display:flex;flex-direction:column;gap:10px;min-width:0;width:100%}
.rzpn,.rzp{min-width:0;width:100%}
.rzr{position:absolute;opacity:0;pointer-events:none}
.rztb{display:inline-flex;align-self:flex-start;border:1px solid var(--line2);border-radius:8px;padding:3px;gap:2px;background:var(--surface)}
.rztb label{cursor:pointer;padding:5px 12px;border-radius:5px;font:600 10.5px 'IBM Plex Mono',monospace;letter-spacing:.1em;color:var(--muted);transition:background .25s ease,color .25s ease}
.rztb label:hover{color:var(--strong)}
.rzr.v1:checked~.rztb .rzu1,.rzr.v2:checked~.rztb .rzu2,.rzr.v3:checked~.rztb .rzu3{background:var(--acc-soft);color:var(--acc-t)}
.rzp{display:none;flex-direction:column;gap:8px;animation:rzin .35s ease}
.rzr.v1:checked~.rzpn .rzq1,.rzr.v2:checked~.rzpn .rzq2,.rzr.v3:checked~.rzpn .rzq3{display:flex}
@keyframes rzin{from{opacity:0;transform:translateY(4px)}to{opacity:1;transform:none}}
.rzfr{display:flex;align-items:center;justify-content:center;aspect-ratio:16/10;padding:8px;border-radius:8px;overflow:hidden;background:#fff;border:1px solid var(--line);cursor:zoom-in;transition:box-shadow .35s ease}
.rzfr:hover{box-shadow:0 8px 22px rgba(0,0,0,.16)}
.rzfr img{display:block;max-width:100%;max-height:100%;object-fit:contain}
.rzfr.rzdk{background:#0B0D11;padding:0;cursor:default}.rzfr.rzdk:hover{box-shadow:none}
.rzfr video{display:block;width:100%;height:100%;object-fit:contain}
.rzcp{margin:0;font:600 10px 'IBM Plex Mono',monospace;letter-spacing:.08em;line-height:1.5;color:var(--muted)}
.rzcp b{color:var(--body);font-weight:600}
.rzlk{margin:0;padding:8px 10px;border-left:2px solid var(--acc-t);background:var(--surface);font-size:13px;line-height:1.5;color:var(--body);border-radius:0 6px 6px 0}
.rzlk b{display:block;font:600 9.5px 'IBM Plex Mono',monospace;letter-spacing:.12em;color:var(--muted);margin-bottom:2px}
.rzvd{position:relative;border-radius:8px;overflow:hidden;background:#0B0D11;border:1px solid var(--line)}
.rzvd video{display:block;width:100%;height:auto}
.rzvd span{position:absolute;left:10px;top:9px;font:600 10px 'IBM Plex Mono',monospace;letter-spacing:.1em;color:rgba(255,255,255,.78);background:rgba(10,12,16,.55);padding:3px 7px;border-radius:4px}
@media (max-width:1100px){.rzc{grid-template-columns:1fr}.rzf{border-left:0;border-top:1px solid var(--line2)}.rzf label{max-width:620px}}
@media (max-width:760px){
  .rzt{padding:16px 14px 12px}.rzt h3{font-size:16.5px}
  .rzs>div{grid-template-columns:1fr;gap:3px}
  .rzk,.rzk.k3{grid-template-columns:1fr 1fr}.rzk>div:nth-child(3){border-left:0}.rzk>div:nth-child(n+3){border-top:1px solid var(--line)}
  .rzl .rzm{margin-left:0}
  .rzf{padding:12px}
  .rzo{padding:16px 14px}
  .zh .rzcp{font-size:10px!important;line-height:1.5}
  .zh .rzlk{font-size:13px!important}
}
"""

LB = []


def authors(s):
    """Author list; each name kept whole on one line, Zaid in bold."""
    head, _, tail = s.partition(" · ")
    out = ", ".join(f'<span class="rzau">{"<b>" + n + "</b>" if n == R.ME else n}</span>' for n in head.split(", "))
    return out + (f" · {tail}" if tail else "")


def tagline(p):
    t = [f"<b>{p['year']}</b>"]
    for x in p["tags"]:
        t.append(f"<em>{x}</em>" if x in ("Q1", "IEEE") else x)
    return " · ".join(t)


def nums(rows, k=""):
    k = k or (" k3" if len(rows) == 3 else "")
    return f'<div class="rzk{k}">' + "".join(f"<div><b>{a}</b><span>{b}</span></div>" for a, b in rows) + "</div>"


def lb(lid, src, alt):
    LB.append(f'<input type="checkbox" class="elbc" id="{lid}"><label class="elb" for="{lid}"><img src="{src}" alt="{alt}"><span>CLOSE ×</span></label>')


def capt(c):
    head, *rest = c.split(" · ")
    return f"<b>{head}</b> · {' · '.join(rest)}"


def media(p):
    """Media switch: VIDEO (thesis only) | HOW (paper's own workflow diagram) | RESULT (paper's key chart)."""
    k = p["key"]
    lic = " · CC BY 4.0" if p["kind"] == "j" else ""
    views = []
    if p.get("video"):
        v = R.B[p["video"]]
        views.append(("VIDEO", f'<div class="rzfr rzdk">{VP.panel("res-" + k, f"<video src=\"{v[0]}\" poster=\"{v[1]}\" autoplay muted loop playsinline preload=\"metadata\" aria-label=\"{p['vidcap']}\"></video>", v[0], v[1], p["vidcap"], "STUDY VIDEO")}</div>'
                      f'<p class="rzcp"><b>STUDY VIDEO</b> · {p["vidcap"]}</p>'))
    lb(f"lb-{k}-how", R.B[p["how"]], p["howcap"])
    views.append(("HOW", f'<label class="rzfr" for="lb-{k}-how"><img src="{R.B[p["how"]]}" alt="{p["howcap"]}"></label>'
                  f'<p class="rzcp">{capt(p["howcap"])}{lic} · click to enlarge</p>'))
    lb(f"lb-{k}-res", R.B[p["fig"]], p["figcap"])
    views.append(("RESULT", f'<label class="rzfr" for="lb-{k}-res"><img src="{R.B[p["fig"]]}" alt="{p["figcap"]}"></label>'
                  f'<p class="rzcp">{capt(p["figcap"])}{lic} · click to enlarge</p><p class="rzlk"><b>WHAT TO SEE</b>{p["look"]}</p>'))
    ins = "".join(f'<input type="radio" class="rzr v{i+1}" name="mv-{k}" id="mv-{k}-{i+1}"{" checked" if i == 0 else ""}>' for i in range(len(views)))
    tabs = '<div class="rztb">' + "".join(f'<label for="mv-{k}-{i+1}" class="rzu{i+1}">{n}</label>' for i, (n, _) in enumerate(views)) + "</div>"
    pans = '<div class="rzpn">' + "".join(f'<div class="rzp rzq{i+1}">{h}</div>' for i, (_, h) in enumerate(views)) + "</div>"
    return f'<div class="rzmd">{ins}{tabs}{pans}</div>'


def card(p):
    links = f'<a href="https://doi.org/{p["doi"]}" target="_blank" rel="noopener">DOI ↗</a>'
    if p["kind"] == "j":
        links += f'<a href="https://doi.org/{p["doi"]}" target="_blank" rel="noopener">FULL TEXT · OPEN ACCESS ↗</a>'
    if p.get("pdf"):
        links += f'<a href="{p["pdf"]}" target="_blank" rel="noopener">PDF ↗</a>'
    met = f'<span class="rzm">IF<b>{p["metric"][0]}</b> &nbsp; CITESCORE<b>{p["metric"][1]}</b></span>' if p["metric"] else ""
    abst = (f'<details class="rzab"><summary>ABSTRACT <i>+</i></summary><p>{p["abstract"]}</p></details>' if p.get("abstract") else "")
    return f"""
      <article class="rzc">
        <div class="rzt">
          <div class="rztg">{tagline(p)}</div>
          <h3>{p['title']}</h3>
          <div class="rzv">{p['venue']}</div>
          <div class="rza">{authors(p['authors'])}</div>
          <dl class="rzs"><div><dt>QUESTION</dt><dd>{p['q']}</dd></div><div><dt>METHOD</dt><dd>{p['m']}</dd></div><div><dt>FINDING</dt><dd>{p['f']}</dd></div></dl>
          {abst}
        </div>
        <div class="rzf">{media(p)}
          {nums(p['nums'], ' k2')}
          <div class="rzl">{links}{met}</div></div>
      </article>"""


def ongoing(o):
    return f"""
      <article class="rzo">
        <div class="rztg"><em>{o['tag']}</em></div>
        <h3 style="margin:8px 0 0;font:600 17px/1.4 'Space Grotesk',sans-serif;color:var(--strong)">{o['title']}</h3>
        <div class="rza">{authors(o['who'])}</div>
        <p>{o['text']}</p>
        {nums(o['nums'])}
        <p class="rzn">{o['note']}</p>
      </article>"""


def page_body():
    LB.clear()
    jr = "".join(card(p) for p in R.PAPERS if p["kind"] == "j")
    cf = "".join(card(p) for p in R.PAPERS if p["kind"] == "c")
    pub = (P.head("01", "PUBLISHED", "Four papers, 2025 to 2026", "pub")
           + P.sub("--r11", "1.1", "JOURNAL PAPERS · 2", jr)
           + P.sub("--r12", "1.2", "CONFERENCE PAPERS · 2", cf)
           + f'<p class="rzth">IF · Journal Impact Factor (JCR) &nbsp;·&nbsp; CITESCORE · Scopus &nbsp;·&nbsp; <b>2026 releases</b></p>')
    ong = (P.head("02", "IN PROGRESS", "Work in progress", "ong")
           + P.sub("--r21", "2.1", "STUDY IN PREPARATION · 1", "".join(ongoing(o) for o in R.ONGOING)))
    nav = [("--q1", "pub", "01", "PUBLISHED", [("--r11", "1.1", "Journal papers"), ("--r12", "1.2", "Conference papers")]),
           ("--q2", "ong", "02", "IN PROGRESS", [("--r21", "2.1", "Study in preparation")])]
    idx = '<nav class="eix" aria-label="On this page"><span class="ixh">ON THIS PAGE</span>'
    for k, (tl, hid, n, lab, subs) in enumerate(nav):
        on = " ion" if k == 0 else ""
        sl = "".join(f'<label for="go-{t[2:]}" style="animation-timeline:{t}" class="ixl{" ion" if (k == 0 and j == 0) else ""}"><b>{sn}</b>{sl_}</label>'
                     for j, (t, sn, sl_) in enumerate(subs))
        idx += (f'<div class="ixg{on}"><label for="go-{hid}" class="ixl{on}" style="animation-timeline:{tl}"><i>{n}</i>{lab}</label>'
                + (f'<div class="ixs" style="animation-timeline:{tl}"><div>{sl}</div></div>' if subs else "") + "</div>")
    idx += "</nav>"
    secs = "".join(f'<section class="esc" style="view-timeline-name:{tl}">{P.GO(hid)}{body}</section>'
                   for tl, hid, body in (("--q1", "pub", pub), ("--q2", "ong", ong)))
    return f"""
    <div class="epz">
      <div class="eph"><div class="crumb">HOME / RESEARCH</div><h1 class="h1">Research</h1>
        <p>Ergonomics and worker safety in garment factories, operations on RMG sewing lines, and machine learning for industrial decisions. Each study below says what was asked, how it was done and what was found.</p></div>
      <div class="est"><div><b>4</b><span>published papers</span></div><div><b>2</b><span>Q1 journal papers</span></div>
        <div><b>2</b><span>as first author</span></div><div><b>1</b><span>in progress</span></div></div>
      <div class="rzl" style="margin-top:14px"><a href="https://orcid.org/0009-0003-3301-3609" target="_blank" rel="noopener">ORCID ↗</a><a href="https://scholar.google.com/citations?user=Fu6JmxIAAAAJ" target="_blank" rel="noopener">GOOGLE SCHOLAR ↗</a><a href="https://www.researchgate.net/profile/Md-Zaid-Hossain" target="_blank" rel="noopener">RESEARCHGATE ↗</a></div>
      <div class="edw rzw">{idx}<div>{secs}</div></div>
      {"".join(LB)}
    </div>"""


def body():
    return f"""
  <main class="wrap" style="position:relative;z-index:1">
    <section class="ph">
      <div class="crumb">PROPOSAL / RESEARCH PAGE · FOR REVIEW, NOT APPLIED</div>
      <h1 class="h1">Research page · in full</h1>
      <p class="lead">Same frame as the Education page. Everything inside the box is the page itself.</p>
    </section>
    <div class="dnote">
      <div><b>ONE CARD PER STUDY</b>Question, method and finding in plain words, four key numbers, DOI and open-access links, the abstract folded away. The thesis study shows its face-blurred video.</div>
      <div><b>HOW | RESULT SWITCH</b>Each study shows the paper's own workflow diagram and its key result chart, with one line on what to see. The thesis study adds its face-blurred video. Click any figure to enlarge.</div>
      <div><b>THESIS LIVES ON EDUCATION</b>The B.Sc. thesis video stays on the Education page; this page holds the published papers and the work in progress.</div>
    </div>
    <div class="dopt">{page_body()}</div>
  </main>
"""


def page(theme, title):
    html = P.H.page(theme, title)
    html = html.replace("<style>", "<style>" + P.EG.CSS + P.CSS + CSS, 1)
    a = html.index("  <!-- Hero: static page backdrop")
    e = html.index("  </main>") + len("  </main>")
    html = html[:a] + body() + html[e:]
    return html.replace('<a href="#">Research</a>', '<a href="#" class="on" aria-current="page">Research</a>', 1)


if __name__ == "__main__":
    out = "/home/claude/zaid/project"
    for key, name in [("dark", "ResPgProp"), ("dark_blue", "ResPgPropBlue"), ("dark_green", "ResPgPropGreen"),
                      ("light", "ResPgPropLight"), ("light_blue", "ResPgPropLightBlue"), ("light_green", "ResPgPropLightGreen"),
                      ("dark", "ResPgPropMobile")]:
        open(f"{out}/{name}.dc.html", "w").write(page(key, f"Research page proposal · {name}"))
    print("research proposal written")
