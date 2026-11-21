#!/usr/bin/env python3
"""Proposal: Awards page. Same frame as Education, Research and Experience (stats strip, sticky index).
01 Competitions: CAD competition results as cards with an inspection-stamp rank mark and the certificate
"as paper" (click to enlarge); the ISCEA case-competition scholarship.
02 Certifications: a certificate register (like a drawing parts list), grouped by field.
Writes AwardsProp* boards. Class prefix: zaw."""
import build_edu_detail_prop as P
import awards_data as A

CSS = """
/* ===== awards page (prefix zaw) ===== */
.zawg{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:18px;margin-top:16px}
.zawc{border:1px solid var(--line2);border-radius:12px;background:var(--surface);padding:16px 16px 18px;display:flex;flex-direction:column;gap:16px;min-width:0}
.zawp{display:block;cursor:zoom-in;padding:8px;background:#fff;border-radius:3px;box-shadow:0 1px 0 rgba(0,0,0,.06),0 10px 24px rgba(0,0,0,.18);transition:transform .35s ease,box-shadow .35s ease}
.zawp img{display:block;width:100%;aspect-ratio:900/636;object-fit:contain;filter:brightness(.95) saturate(.92);transition:filter .35s ease}
.zawc,.zawx{transition:border-color .35s ease,transform .35s ease,box-shadow .35s ease}
.zawc:hover,.zawx:hover{border-color:var(--muted);transform:translateY(-2px);box-shadow:0 14px 30px rgba(0,0,0,.14)}
.zawc:hover .zawp,.zawx:hover .zawp{transform:translateY(-3px) rotate(-.4deg);box-shadow:0 1px 0 rgba(0,0,0,.06),0 16px 32px rgba(0,0,0,.26)}
.zawc:hover .zawp img,.zawx:hover .zawp img{filter:none}
@media (prefers-reduced-motion:reduce){.zawc,.zawx,.zawp{transition:none}.zawc:hover,.zawx:hover,.zawc:hover .zawp,.zawx:hover .zawp{transform:none}}
.zawls{display:flex;flex-wrap:wrap;gap:6px 16px;margin-top:8px}
.zawls .zawl{margin-top:0}
.zawnm2{white-space:nowrap}
.zawtm{display:flex;flex-wrap:wrap;gap:6px 8px;margin-top:10px}
.zawtm span{font-size:13px;color:var(--body);border:1px solid var(--line);border-radius:999px;padding:3px 10px;white-space:nowrap}
.zawtm b{font:600 10px 'IBM Plex Mono',monospace;letter-spacing:.1em;color:var(--muted);align-self:center;margin-right:2px}
/* certificate cards */
.zawxg{display:grid;grid-template-columns:repeat(var(--zc),minmax(0,1fr));gap:16px;margin-top:16px}
.zawx{border:1px solid var(--line2);border-radius:12px;background:var(--surface);padding:12px 12px 14px;display:flex;flex-direction:column;gap:12px;min-width:0}
.zawx .zawp{padding:6px}
.zawx .zawp img{aspect-ratio:1.414/1}
.zawxh{display:flex;justify-content:space-between;align-items:baseline;gap:8px}
.zawxc{font:600 10px 'IBM Plex Mono',monospace;letter-spacing:.1em;color:var(--acc-t);white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.zawxd{font:600 10px 'IBM Plex Mono',monospace;letter-spacing:.06em;color:var(--muted);white-space:nowrap}
.zawx h4{margin:4px 0 0;font:600 14.5px/1.35 'Space Grotesk',sans-serif;color:var(--strong)}
.zawx .zawo{font-size:12.5px;margin-top:3px}
.zawx.zaww2{grid-column:span 2;display:grid;grid-template-columns:minmax(0,1.05fr) minmax(0,1fr);gap:18px;align-items:start;padding:14px 16px}
.zawx.zaww2 h4{font-size:17px}
.zawx.zaww2 .zawo{font-size:13.5px}
.zawx.zaww2 .zawn3{margin-top:10px;font-size:13.5px;line-height:1.5;color:var(--body)}
.zawp.zawmd{padding:0;background:var(--surface2);overflow:hidden;cursor:pointer;border:1px solid var(--line)}
.zawp.zawmd img{object-fit:cover;filter:none}
.zawm{display:grid;grid-template-columns:58px minmax(0,1fr);gap:14px;align-items:start}
.zaws{position:relative;width:58px;height:58px;border-radius:50%;border:1.5px solid var(--line2);display:flex;flex-direction:column;align-items:center;justify-content:center;color:var(--muted);font-family:'IBM Plex Mono',monospace;line-height:1}
.zaws:before{content:"";position:absolute;inset:-5px;border-radius:50%;border:1px dashed var(--line2)}
.zaws b{font-size:14px;font-weight:600;letter-spacing:.04em;color:var(--strong)}
.zaws i{font-style:normal;font-size:8.5px;letter-spacing:.14em;margin-top:3px}
.zawc .zaws{border-color:var(--acc-t);color:var(--acc-t)}
.zawc .zaws b{color:var(--acc-t)}
.zawc .zaws:before{border-color:var(--acc-t);opacity:.55}
.zawc.zw1 .zaws:before{animation:zawspin 48s linear infinite}
@keyframes zawspin{to{transform:rotate(360deg)}}
@media (prefers-reduced-motion:reduce){.zawc.zw1 .zaws:before{animation:none}}
.zawk{font:600 10.5px 'IBM Plex Mono',monospace;letter-spacing:.12em;color:var(--acc-t)}
.zawc h4{margin:5px 0 0;font:600 16px/1.35 'Space Grotesk',sans-serif;color:var(--strong)}
.zawo{margin-top:4px;font-size:13.5px;line-height:1.5;color:var(--muted)}
.zawo b{white-space:nowrap;font:600 11px 'IBM Plex Mono',monospace;letter-spacing:.08em;color:var(--body)}
.zawl{display:inline-block;margin-top:8px;font:600 11px 'IBM Plex Mono',monospace;letter-spacing:.08em;color:var(--muted);border-bottom:1px dotted var(--line2);padding-bottom:1px;transition:color .25s ease}
.zawl:hover{color:var(--acc-t)}
.zawcs{display:grid;grid-template-columns:280px minmax(0,1fr);gap:28px;align-items:start;border:1px solid var(--line2);border-radius:12px;background:var(--surface);padding:22px;margin-top:16px;transition:border-color .35s ease,box-shadow .35s ease}
.zawcs:hover{border-color:var(--muted);box-shadow:0 14px 30px rgba(0,0,0,.14)}
.zawpf{margin:0}
.zawps{position:relative;display:block;cursor:zoom-in;border-radius:8px;overflow:hidden;box-shadow:0 14px 34px rgba(0,0,0,.35);transition:transform .35s ease}
.zawcs:hover .zawps{transform:translateY(-3px) rotate(-.5deg)}
.zawps img{display:block;width:100%;height:auto}
.zawhl{position:absolute;border:2px solid var(--acc-t);border-radius:999px;box-shadow:0 0 0 3px rgba(0,0,0,.35),0 0 18px var(--acc-t);animation:zawpulse 3.6s ease-in-out infinite}
@keyframes zawpulse{0%,100%{opacity:.95}50%{opacity:.45}}
.zawpf figcaption{margin-top:9px;font:600 10.5px 'IBM Plex Mono',monospace;letter-spacing:.1em;color:var(--muted);text-align:center}
.zawch{display:grid;grid-template-columns:72px minmax(0,1fr);gap:18px;align-items:center}
.zawch .zaws{width:72px;height:72px;border-color:var(--acc-t);color:var(--acc-t)}
.zawch .zaws b{font-size:20px;color:var(--acc-t)}
.zawch .zaws i{font-size:10px}
.zawch .zaws:before{border-color:var(--acc-t);opacity:.55;animation:zawspin 48s linear infinite}
.zawch h4{margin:5px 0 0;font:600 20px/1.3 'Space Grotesk',sans-serif;color:var(--strong)}
.zawev{margin-top:4px;font-size:15px;color:var(--body)}
.zawfs{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));border:1px solid var(--line2);border-radius:10px;margin-top:20px;overflow:hidden}
.zawfs>div{padding:12px 16px;background:var(--surface2)}
.zawfs>div+div{border-left:1px solid var(--line2)}
.zawfs b{display:block;font:600 18px 'Space Grotesk',sans-serif;color:var(--strong);white-space:nowrap}
.zawfs span{display:block;margin-top:2px;font-size:13px;line-height:1.45;color:var(--muted)}
.zawtb{margin-top:20px;border:1px solid var(--line2);border-radius:10px;overflow:hidden;background:var(--surface)}
.zawtbh{display:flex;align-items:baseline;gap:10px;padding:9px 16px;border-bottom:1px solid var(--line2);background:var(--surface2);font:600 10.5px 'IBM Plex Mono',monospace;letter-spacing:.12em;color:var(--muted)}
.zawtbh b{color:var(--acc-t);font-weight:600}
.zawtbh span:last-child{margin-left:auto}
.zawtg{display:grid;grid-template-columns:repeat(2,minmax(0,1fr))}
.zawmb{position:relative;display:flex;flex-direction:column;gap:3px;padding:12px 16px 13px;min-width:0;transition:background .3s ease}
.zawmb:nth-child(2n){border-left:1px solid var(--line)}
.zawmb:nth-child(n+3){border-top:1px solid var(--line)}
.zawmb:before{content:"";position:absolute;left:0;top:0;bottom:0;width:2px;background:var(--acc-t);transform:scaleY(0);transform-origin:bottom;transition:transform .35s ease}
.zawmb:hover{background:var(--surface2)}
.zawmb:hover:before{transform:scaleY(1)}
.zawno{font:600 10px 'IBM Plex Mono',monospace;letter-spacing:.12em;color:var(--muted)}
.zawmb:first-child .zawno{color:var(--acc-t)}
.zawmb .zawnm2{font-size:15.5px;color:var(--strong);font-weight:500;padding-right:22px;transition:color .25s ease}
.zawar{position:absolute;right:14px;bottom:13px;font-size:13px;color:var(--muted);opacity:0;transform:translate(-4px,4px);transition:opacity .3s ease,transform .3s ease,color .3s ease}
.zawmb:hover .zawnm2,.zawmb:hover .zawar{color:var(--acc-t)}
.zawmb:hover .zawar{opacity:1;transform:none}
.zawcs .zawls{margin-top:16px}
@media (prefers-reduced-motion:reduce){.zawhl{animation:none}.zawcs:hover .zawps{transform:none}}
@media (max-width:1100px){.zawcs{grid-template-columns:220px minmax(0,1fr);gap:20px}}
@media (max-width:760px){
  .zawcs{grid-template-columns:1fr;padding:14px}
  .zawpf{max-width:250px;margin:0 auto}
  .zawch{grid-template-columns:58px minmax(0,1fr);gap:14px}
  .zawch .zaws{width:58px;height:58px}.zawch .zaws b{font-size:16px}
  .zawch h4{font-size:17px}
  .zawfs{grid-template-columns:1fr}.zawfs>div+div{border-left:0;border-top:1px solid var(--line2)}
  .zawtbh span:last-child{display:none}
  .zawtg{grid-template-columns:1fr}
  .zawmb:nth-child(2n){border-left:0}
  .zawmb:nth-child(n+2){border-top:1px solid var(--line)}
}
.zawh.zw1 .zaws{border-color:var(--acc-t);color:var(--acc-t)}.zawh.zw1 .zaws b{color:var(--acc-t)}
.zawh{display:grid;grid-template-columns:58px minmax(0,1fr);gap:14px;align-items:start;border:1px solid var(--line2);border-radius:12px;background:var(--surface);padding:18px 20px;margin-top:16px}
.zawh h4{margin:5px 0 0;font:600 16px/1.35 'Space Grotesk',sans-serif;color:var(--strong)}
.zawh p{margin:8px 0 0;font-size:14px;line-height:1.55;color:var(--body)}
.zawt{border:1px solid var(--line2);border-radius:12px;background:var(--surface);overflow:hidden;margin-top:16px}
.zawt>div{display:grid;grid-template-columns:96px minmax(0,1.7fr) minmax(0,1fr) 92px 84px;gap:0 18px;padding:12px 18px;border-top:1px dashed var(--line);align-items:baseline;transition:background .25s ease}
.zawt>div:first-child{border-top:0;background:var(--surface2);font:600 10.5px 'IBM Plex Mono',monospace;letter-spacing:.12em;color:var(--muted)}
.zawt>div:not(:first-child):hover{background:var(--surface2)}
.zawt .zawn{font:600 11.5px 'IBM Plex Mono',monospace;letter-spacing:.04em;color:var(--acc-t);white-space:nowrap}
.zawt .zawnm{font-size:14.5px;color:var(--strong);font-weight:500}
.zawt .zawi,.zawt .zawy{font-size:13.5px;color:var(--body)}
.zawt .zawy{font-family:'IBM Plex Mono',monospace;font-size:12px;letter-spacing:.04em;white-space:nowrap}
.zawt .zawq{color:var(--muted);opacity:.55}
.zawt a{font:600 11px 'IBM Plex Mono',monospace;letter-spacing:.08em;color:var(--muted);border-bottom:1px dotted var(--line2);white-space:nowrap}
.zawt a:hover{color:var(--acc-t)}
@media (max-width:1300px){.zawxh{flex-direction:column;gap:2px}}
@media (max-width:1100px){.zawg{grid-template-columns:repeat(2,minmax(0,1fr))}.zawxg{--zc:2!important}}
@media (max-width:760px){
  .zawg{grid-template-columns:1fr;gap:14px}
  .zawc{padding:14px}
  .zawp{max-width:340px;width:100%;margin:0 auto}
  .zawh{padding:16px 14px}
  .zawxg{gap:10px}
  .zawx{padding:8px 8px 10px;gap:8px}
  .zawx .zawp{padding:3px;max-width:none}
  .zawx h4{font-size:13px}
  .zawx .zawo{font-size:11.5px}
  .zawxh{flex-direction:column;gap:2px}
  .zawx.zaww2{grid-template-columns:1fr;padding:10px 10px 12px;gap:10px}
  .zawx.zaww2 .zawp{max-width:340px;margin:0 auto}
  .zawt>div{grid-template-columns:minmax(0,1fr) auto;gap:3px 12px;padding:11px 14px}
  .zawt>div:first-child{display:none}
  .zawt .zawn{grid-column:1;grid-row:1}
  .zawt .zawy{grid-column:2;grid-row:1;text-align:right}
  .zawt .zawnm{grid-column:1/-1;grid-row:2}
  .zawt .zawi{grid-column:1;grid-row:3;color:var(--muted);font-size:13px}
  .zawt .zawv{grid-column:2;grid-row:3;text-align:right}
}
"""

LB = []
KEY = {"Champion": "zw1", "2nd runner-up": "zw3", "Top 20 finalist": "zw20"}


def stamp(rank):
    a, b = A.STAMP[rank]
    return f'<span class="zaws" aria-hidden="true"><b>{a}</b><i>{b}</i></span>'


def competitions():
    out = ""
    for rank, ev, org, date, key in A.COMPETITIONS:
        if key:
            lid = f"zlb-{key}"
            LB.append(f'<input type="checkbox" class="elbc" id="{lid}"><label class="elb" for="{lid}"><img src="{A.CERT_IMG[key]}" alt="{ev} certificate"><span>CLOSE ×</span></label>')
            pic = f'<label class="zawp" for="{lid}" title="Click to enlarge"><img src="{A.CERT_IMG[key]}" alt="{ev} certificate"></label>'
            link = '<div class="zawls"><a class="zawl" href="#">PHOTOS IN GALLERY →</a></div>'
        else:
            pic = f'<a class="zawp zawmd" href="#"><img src="{A.EV_RENDER}" alt="EV charging station model made for {ev}"></a>'
            link = '<div class="zawls"><a class="zawl" href="#">PROJECT PAGE →</a><a class="zawl" href="#">PHOTOS IN GALLERY →</a></div>'
        out += (f'<article class="zawc {KEY[rank]}">{pic}<div class="zawm">{stamp(rank)}<div>'
                f'<div class="zawk">{rank.upper()}</div><h4>{ev}</h4><div class="zawo">{org} · <b>{date}</b></div>{link}</div></div></article>')
    return f'<div class="zawg">{out}</div>'


def initials(n):
    w = [x for x in n.replace("Md.", "").split() if x[0].isalpha()]
    return (w[0][0] + w[-1][0]).upper()


def scholarship():
    s = A.SCHOLARSHIP
    l, t, w, h = s["tag_box"]
    LB.append(f'<input type="checkbox" class="elbc" id="zlb-iscea"><label class="elb" for="zlb-iscea"><img src="{s["poster"]}" alt="ISCEA Prize 2024 scholarship winners, Bangladesh teams, part 2"><span>CLOSE ×</span></label>')
    team = "".join(f'<a class="zawmb" href="{u}" target="_blank" rel="noopener" title="{n} on LinkedIn"><span class="zawno">{i+1:02d}{" · ME" if i == 0 else ""}</span><span class="zawnm2">{n}</span><span class="zawar" aria-hidden="true">↗</span></a>'
                   for i, (n, u) in enumerate(s["team_members"]))
    return f"""<div class="zawcs">
      <figure class="zawpf"><label class="zawps" for="zlb-iscea" title="Click to enlarge"><img src="{s["poster"]}" alt="ISCEA Prize 2024 scholarship winners, Bangladesh teams, part 2, with team KUET-0101-24 on the list">
        <span class="zawhl" style="left:{l}%;top:{t}%;width:{w}%;height:{h}%" aria-hidden="true"></span></label>
        <figcaption>WINNERS' LIST · ISCEA · PART 2</figcaption></figure>
      <div class="zawcb">
        <div class="zawch"><span class="zaws" aria-hidden="true"><b>70</b><i>%</i></span><div>
          <div class="zawk">SCHOLARSHIP · {s["when"]}</div><h4>{s["title"]}</h4>
          <div class="zawev">{s["event"]}</div><div class="zawo">{s["org"]}</div></div></div>
        <div class="zawfs"><div><b>{s["team"]}</b><span>team, on the winners' list</span></div><div><b>{s["amount"]}</b><span>{s["amount_note"]}</span></div></div>
        <div class="zawtb"><div class="zawtbh"><span>TEAM</span><b>{s["team"]}</b><span>ISCEA PRIZE 2024</span></div><div class="zawtg">{team}</div></div>
        <div class="zawls"><a class="zawl" href="{s["post"]}" target="_blank" rel="noopener">LINKEDIN POST ↗</a><a class="zawl" href="#y22">MY CSCA CERTIFICATE ↓</a></div>
      </div></div>"""


def cert_card(c):
    key, code, name, iss, date, links = c[:6]
    note = c[6] if len(c) > 6 else ""
    lid = f"zlb-c-{key}"
    LB.append(f'<input type="checkbox" class="elbc" id="{lid}"><label class="elb" for="{lid}"><img src="{A.IMG[key]}" alt="{name} certificate"><span>CLOSE ×</span></label>')
    pic = f'<label class="zawp" for="{lid}" title="Click to enlarge"><img src="{A.IMG[key]}" alt="{name} certificate"></label>'
    ls = "".join(f'<a class="zawl" href="{u}">{t}</a>' for t, u in links)
    ls = f'<div class="zawls">{ls}</div>' if ls else ""
    dt = f'<span class="zawxd">{date}</span>' if date else ""
    info = (f'<div><div class="zawxh"><span class="zawxc">{code}</span>{dt}</div><h4>{name}</h4><div class="zawo">{iss}</div>'
            + (f'<div class="zawn3">{note}</div>' if note else "") + ls + "</div>")
    return f'<article class="zawx{" zaww2" if note else ""}">{pic}{info}</article>'


def cert_grid(cols, items):
    return f'<div class="zawxg" style="--zc:{cols}">' + "".join(cert_card(c) for c in items) + "</div>"


def register(rows):
    h = '<div><span>CODE</span><span>CERTIFICATION</span><span>ISSUER</span><span>YEAR</span><span>PROOF</span></div>'
    q = '<span class="zawq">—</span>'
    for code, name, iss, yr, url in rows:
        h += (f'<div><span class="zawn">{code}</span><span class="zawnm">{name}</span>'
              f'<span class="zawi">{iss or q}</span><span class="zawy">{yr or q}</span>'
              f'<span class="zawv">{f"<a href={chr(34)}{url}{chr(34)}>VERIFY ↗</a>" if url else q}</span></div>')
    return f'<div class="zawt">{h}</div>'


def page_body():
    LB.clear()
    n_champ = sum(1 for c in A.COMPETITIONS if c[0] == "Champion")
    n_cert = sum(len(g[5]) for g in A.GROUPS[:3])
    n_course = len(A.GROUPS[3][5])
    comp = (P.head("01", "COMPETITIONS", "Results, with the certificates", "comp")
            + P.sub("--y11", "1.1", f"CAD COMPETITIONS · {len(A.COMPETITIONS)}", competitions())
            + P.sub("--y12", "1.2", "CASE COMPETITION", scholarship()))
    subs = "".join(P.sub(tl, n, f"{g} · {len(items)}", cert_grid(cols, items)) for tl, n, g, _, cols, items in A.GROUPS)
    cert = P.head("02", "CERTIFICATIONS", "Certificates, with proof", "cert") + subs
    nav = [("--a1", "comp", "01", "COMPETITIONS", [("--y11", "1.1", "CAD competitions"), ("--y12", "1.2", "Case competition")]),
           ("--a2", "cert", "02", "CERTIFICATIONS", [(tl, n, sh) for tl, n, _, sh, _, _ in A.GROUPS])]
    idx = '<nav class="eix" aria-label="On this page"><span class="ixh">ON THIS PAGE</span>'
    for k, (tl, hid, n, lab, sb) in enumerate(nav):
        on = " ion" if k == 0 else ""
        sl = "".join(f'<label for="go-{t[2:]}" style="animation-timeline:{t}" class="ixl{" ion" if (k == 0 and j == 0) else ""}"><b>{sn}</b>{s_}</label>'
                     for j, (t, sn, s_) in enumerate(sb))
        idx += (f'<div class="ixg{on}"><label for="go-{hid}" class="ixl{on}" style="animation-timeline:{tl}"><i>{n}</i>{lab}</label>'
                f'<div class="ixs" style="animation-timeline:{tl}"><div>{sl}</div></div></div>')
    idx += "</nav>"
    secs = "".join(f'<section class="esc" style="view-timeline-name:{tl}">{P.GO(hid)}{b}</section>'
                   for tl, hid, b in (("--a1", "comp", comp), ("--a2", "cert", cert)))
    return f"""
    <div class="epz">
      <div class="eph"><div class="crumb">HOME / AWARDS</div><h1 class="h1">Awards</h1>
        <p>CAD competitions won at KUET, BUET and AUST, a scholarship from ISCEA's global case competition, and certifications in CAD, supply chain, data and quality, each shown with its certificate.</p></div>
      <div class="est"><div><b>{n_champ}</b><span>times champion</span></div><div><b>70 %</b><span>ISCEA scholarship</span></div>
        <div><b>{n_cert}</b><span>certifications</span></div><div><b>{n_course}</b><span>courses</span></div></div>
      <div class="edw zaww">{idx}<div>{secs}</div></div>
      {"".join(LB)}
    </div>"""


SCOPE = "\n.edw.zaww{timeline-scope:--a1,--a2,--y11,--y12,--y21,--y22,--y23,--y24}"


def body():
    return f"""
  <main class="wrap" style="position:relative;z-index:1">
    <section class="ph">
      <div class="crumb">PROPOSAL / AWARDS PAGE · FOR REVIEW, NOT APPLIED</div>
      <h1 class="h1">Awards page · in full</h1>
      <p class="lead">Same frame as Education, Research and Experience. Everything inside the box is the page itself.</p>
    </section>
    <div class="dnote">
      <div><b>RESULTS AS CARDS</b>Each CAD result has an inspection-stamp mark (1ST, 3RD, TOP 20) and the certificate as paper. The whole card reacts to the cursor; every result links to its photos in the Gallery, Energy Fest also to its project page.</div>
      <div><b>EVERY CERTIFICATE SHOWN</b>All {sum(len(g[5]) for g in A.GROUPS)} certificates from the Certification folder as paper cards (click to enlarge), with date, issuer and a VERIFY link where the issuer offers one. Rows are always full.</div>
      <div><b>EDUCATION GETS SHORTER</b>After this is applied, Education can keep one CAD line with a link here (as with Experience) instead of showing all five certificates twice.</div>
    </div>
    <div class="dopt">{page_body()}</div>
  </main>
"""


def page(theme, title):
    html = P.H.page(theme, title)
    html = html.replace("<style>", "<style>" + P.EG.CSS + P.CSS + CSS + SCOPE, 1)
    a = html.index("  <!-- Hero: static page backdrop")
    e = html.index("  </main>") + len("  </main>")
    html = html[:a] + body() + html[e:]
    return html.replace('<a href="#">Awards</a>', '<a href="#" class="on" aria-current="page">Awards</a>', 1)


if __name__ == "__main__":
    import type_scale as TS
    out = "/home/claude/zaid/project"
    for key, name in [("dark", "AwardsProp"), ("dark_blue", "AwardsPropBlue"), ("dark_green", "AwardsPropGreen"),
                      ("light", "AwardsPropLight"), ("light_blue", "AwardsPropLightBlue"), ("light_green", "AwardsPropLightGreen"),
                      ("dark", "AwardsPropMobile")]:
        open(f"{out}/{name}.dc.html", "w").write(TS.apply(page(key, f"Awards page proposal · {name}")))
    print("awards proposal written")
