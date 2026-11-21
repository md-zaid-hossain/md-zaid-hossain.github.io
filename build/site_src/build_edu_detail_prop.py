#!/usr/bin/env python3
"""Proposal: detailed Education page (Zaid 2026-11-18: much more detail, certificates shown on the page,
course map from the syllabus, research before projects, CGPA only, no course grades).
Writes EduPgProp* boards (replaces the earlier A/B/C proposal)."""
import routine as R
import videoplayer as VP
import build_home as H
import edu_gantt as EG
import edu_data as D
import res_list as RL

B = {  # uploaded assets (redacted certificates, term project photos)
    "prov": "/_blob/38339a7fde1a204f40d382dfe684ba92", "eng": "/_blob/0b8fe33ab7f32cdc398563b4f4812dab",
    "grade": "/_blob/97413a30fa7900772561752e48d80dc9", "hsc": "/_blob/d9ccce495533682c61218bf6e5c95bfd",
    "ssc": "/_blob/f6493414b1576e6cb550f4fd00c2147a",
    "technomize": "/_blob/cbd94d83f1ab0a605f0d249d30cb4961", "cadrush": "/_blob/0f898711631101bcb558dd9fed527f5c",
    "mechcellence": "/_blob/1338cb7441a161527b9fde208cd3b677", "kitcad": "/_blob/88368f3764338751aa406b701e68b81a",
    "ignition": "/_blob/152b4e8af7817136567d6fdfe43e679f",
    "tp": "/_blob/2001a7139d7577d4fd22d88cf408df4b", "fig02": "/_blob/48da2943a1031ff7413ec0d091aa62bc", "video": "/_blob/3c9114ec1547ea77d65cc2c7f413c784", "poster": "/_blob/68d36bdc3ab43a793d0fc66ce81837cd",
    "fig01": "/_blob/52793cb3f20abc7da716cff99bd5b873", "fig06": "/_blob/1a60cfbe57a29484038e768951699d71", "fig10": "/_blob/a875678e430700b6051bcb6ef4155b95", "tpcad": "/_blob/0e9dec1acb5bd40b4b884c2bca2f16bb",
    "hall": "/_blob/169902addf7f1a39bd48a849c875b850", "dsw": "/_blob/0bdd9adeab3f032d3ec45ef8f9758214", "fablabc": "/_blob/446c08a24635e6e33fe257c41dbbdfcd",
}
LOCK = ('<svg width="11" height="11" viewBox="0 0 24 24" fill="none" aria-hidden="true"><rect x="5" y="11" width="14" height="10" rx="2" '
        'stroke="currentColor" stroke-width="2"/><path d="M8 11V8a4 4 0 0 1 8 0v3" stroke="currentColor" stroke-width="2"/></svg>')
ZOOM = ('<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true">'
        '<circle cx="11" cy="11" r="6"/><path d="M20 20l-4.5-4.5M11 8v6M8 11h6"/></svg>')

CSS = """
.crumb{font:600 12.5px 'IBM Plex Mono',monospace;letter-spacing:.1em;color:var(--muted)}
.ph{position:relative;padding:52px 0 4px}
.ph .h1{font-size:42px;margin-top:14px}
.ph .lead{margin-top:12px;max-width:900px;font-size:17px}
.dnote{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px;margin-top:28px}
.dnote div{border:1px solid var(--line);border-radius:10px;padding:12px 14px;background:var(--surface);font-size:14px;line-height:1.5;color:var(--body)}
.dnote b{display:block;font:600 11.5px 'IBM Plex Mono',monospace;letter-spacing:.1em;color:var(--acc-t);margin-bottom:4px}
.epg{padding-top:56px}
@media (max-width:760px){.epg{padding-top:30px}}
.dopt{margin-top:40px;padding:26px 28px 34px;border:1px solid var(--line2);border-radius:12px}

/* ---------- page frame ---------- */
.epz .eph h1{font-size:44px;margin:10px 0 0}
.epz .eph p{margin-top:10px;max-width:820px;font-size:16.5px;line-height:1.6;color:var(--body)}
.est{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));margin-top:24px;border:1px solid var(--line2);border-radius:10px;background:var(--surface);overflow:hidden}
.est>div{padding:13px 16px;border-left:1px solid var(--line)}
.est>div:first-child{border-left:0}
.est b{display:block;font:500 20px 'IBM Plex Mono',monospace;color:var(--strong)}
.est span{display:block;margin-top:2px;font-size:13px;color:var(--muted);white-space:nowrap}
.egt{margin-top:22px}
.edw{display:grid;grid-template-columns:168px minmax(0,1fr);gap:40px;margin-top:44px}
.eix{position:sticky;top:96px;align-self:start;display:flex;flex-direction:column;border-left:1px solid var(--line2)}
.eix .ixl{cursor:pointer;display:flex;gap:10px;align-items:baseline;padding:7px 0 7px 14px;margin-left:-1px;border-left:2px solid transparent;font:600 11.5px 'IBM Plex Mono',monospace;letter-spacing:.08em;color:var(--muted);transition:color .25s ease,border-color .25s ease}
.eix .ixl i{font-style:normal;opacity:.7}
.eix .ixl:hover{color:var(--strong)}
.eix .ixl.ion,nav.eix .ixg>.ixl.ion{color:var(--acc-t);border-left-color:var(--acc-t)}
.eix .ixg{display:flex;flex-direction:column}
.eix .ixs{display:grid;grid-template-rows:0fr;transition:grid-template-rows .3s ease}
.eix .ixs>div{overflow:hidden;min-height:0;display:flex;flex-direction:column}
nav.eix .ixg>.ixl{color:var(--muted)}
nav.eix .ixg>.ixl:hover{color:var(--strong)}
.eix .ixs .ixl{padding:4px 0 4px 32px;font:500 12px 'Inter',sans-serif;letter-spacing:0;color:var(--muted);border-left:2px solid transparent}
.eix .ixs .ixl b{font:600 10px 'IBM Plex Mono',monospace;margin-right:6px;opacity:.7}
.eix .ixg.ion .ixs{grid-template-rows:1fr}
.eix .ixs .ixl.ion{color:var(--strong);border-left-color:var(--line2)}
@supports (animation-timeline: view()){
  .edw{timeline-scope:--s1,--s2,--s3,--s4,--s5,--b1,--b2,--b3,--b4,--b5,--m1,--m2,--h1,--h2,--c1,--c2}
  .esc,.ebk{view-timeline-axis:block;view-timeline-inset:28% 71%}
  .eix .ixl.ion,.eix .ixg.ion .ixs,.eix .ixs .ixl.ion{color:inherit}
  .eix .ixg>.ixl{animation:ixon linear both;animation-range:cover 0% cover 100%;animation-fill-mode:none}
  .eix .ixg.ion .ixs{grid-template-rows:0fr}
  .eix .ixg .ixs{animation:ixopen linear both;animation-range:cover 0% cover 100%;animation-fill-mode:none;grid-template-rows:0fr}
  .eix .ixs .ixl{animation:ixsub linear both;animation-range:cover 0% cover 100%;animation-fill-mode:none}
  .eix .ixs .ixl.ion{color:var(--muted);border-left-color:transparent}
  nav.eix .ixg>.ixl.ion{color:var(--muted);border-left-color:transparent}
}
@keyframes ixon{from,to{color:var(--acc-t);border-left-color:var(--acc-t)}}
@keyframes ixopen{from,to{grid-template-rows:1fr}}
@keyframes ixsub{from,to{color:var(--strong);border-left-color:var(--line2)}}
.eix .ixh{padding:0 0 8px 14px;font:600 10px 'IBM Plex Mono',monospace;letter-spacing:.14em;color:var(--muted);opacity:.8}
.esc+.esc{margin-top:64px}
.esc .sh{margin-bottom:6px}
.ess{display:flex;align-items:center;gap:12px;margin:34px 0 14px;font:600 11.5px 'IBM Plex Mono',monospace;letter-spacing:.12em;color:var(--muted)}
.ess:after{content:"";flex:1;height:1px;background:var(--line)}
.ess b{color:var(--strong);font-weight:600}

/* record table + certificates */
.erw{display:grid;grid-template-columns:minmax(0,1fr) 330px;gap:28px;align-items:start}
.erec{display:grid;grid-template-columns:132px minmax(0,1fr);border-top:1px solid var(--line2)}
.erec>span{padding:10px 0;border-bottom:1px solid var(--line);font-size:14.5px;color:var(--strong)}
.erec>span.ek{font:600 11px 'IBM Plex Mono',monospace;letter-spacing:.1em;color:var(--muted);padding-top:12px}
.erec em{font-style:normal;color:var(--muted)}
.erec .vsc{margin-top:6px}
.enote{margin-top:10px;font-size:13px;line-height:1.55;color:var(--muted)}
.ecs{display:grid;grid-template-columns:1fr 1fr;gap:12px}
.ecs .ecrt:first-child{grid-column:1/3}
.ecrt{position:relative;display:block;cursor:zoom-in}
.ecrt .pp{display:block;padding:7px;background:#F7F6F2;border-radius:3px;box-shadow:0 1px 0 rgba(0,0,0,.06),0 10px 26px rgba(0,0,0,.22);transition:transform .35s ease,box-shadow .35s ease}
.ecrt img{display:block;width:100%;filter:brightness(.93) saturate(.9);transition:filter .35s ease}
.ecrt .ecp{display:flex;justify-content:space-between;align-items:center;gap:8px;margin-top:8px;font:600 10.5px 'IBM Plex Mono',monospace;letter-spacing:.08em;color:var(--muted)}
.ecrt .ecp i{font-style:normal;display:inline-flex;opacity:.8}
.ecrt:hover .pp{transform:translateY(-3px);box-shadow:0 1px 0 rgba(0,0,0,.06),0 16px 34px rgba(0,0,0,.28)}
.ecrt:hover img{filter:none}
.ecrt:hover .ecp{color:var(--acc-t)}
/* lightbox: checkbox + label, no JS */
.elbc{position:absolute;opacity:0;pointer-events:none}
.elb{display:none;position:fixed;inset:0;z-index:300;background:rgba(8,10,14,.86);align-items:center;justify-content:center;padding:40px;cursor:zoom-out}
.elb img{max-width:min(980px,92vw);max-height:84vh;box-shadow:0 20px 60px rgba(0,0,0,.5);border-radius:3px;background:#F7F6F2;padding:8px}
.elb span{position:absolute;top:20px;right:24px;font:600 11px 'IBM Plex Mono',monospace;letter-spacing:.12em;color:#E7E9EE}
.elbc:checked+.elb{display:flex}

/* course map */
.ecm{position:relative}
.ecm>input{position:absolute;opacity:0;pointer-events:none}
.ecf{display:grid;grid-template-columns:repeat(6,minmax(0,1fr));gap:6px;margin-bottom:14px}
.ecf label{display:flex;align-items:center;justify-content:space-between;gap:8px;min-width:0;height:34px;border:1px solid var(--line);border-radius:7px;padding:0 11px;background:var(--surface);font-size:12.5px;color:var(--body);cursor:pointer;transition:color .25s ease,border-color .25s ease,background .25s ease}
.ecf label span{white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.ecf label small{flex:none;font:600 10.5px 'IBM Plex Mono',monospace;color:var(--muted)}
.ecf label:hover{border-color:var(--muted)}
@media (max-width:1100px){.ecf{grid-template-columns:repeat(4,minmax(0,1fr))}}
.ecg{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:12px}
.etb{border:1px solid var(--line2);border-radius:10px;background:var(--surface);padding:12px 12px 10px;display:flex;flex-direction:column}
.etb .eth{display:flex;flex-direction:column;gap:3px;padding:0 2px 9px;border-bottom:1px solid var(--line)}
.etb .eth b{font:600 11px 'IBM Plex Mono',monospace;letter-spacing:.1em;color:var(--strong)}
.etb .eth span{font:600 9.5px 'IBM Plex Mono',monospace;letter-spacing:.06em;color:var(--muted);white-space:nowrap}
.etb .elst{display:flex;flex-direction:column;margin-top:4px}
.egl{display:flex;align-items:baseline;gap:8px;padding:9px 2px 3px}
.egl b{font:600 9.5px 'IBM Plex Mono',monospace;letter-spacing:.12em;color:var(--muted)}
.egl small{font:600 9.5px 'IBM Plex Mono',monospace;color:var(--muted);opacity:.7}
.egl.egs{margin-top:10px;padding-top:12px;border-top:1px solid var(--line2)}
.ec-c{transition:opacity .35s ease}
details.ec-c{border-bottom:1px dashed var(--line)}
details.ec-c summary{list-style:none;display:grid;grid-template-columns:66px minmax(0,1fr) 12px;gap:6px;align-items:baseline;padding:7px 2px;cursor:pointer;border-radius:5px;transition:background .25s ease}
details.ec-c summary::-webkit-details-marker{display:none}
details.ec-c summary code{font:600 10px 'IBM Plex Mono',monospace;color:var(--muted)}
details.ec-c summary span{font-size:13px;line-height:1.35;color:var(--strong)  /* course names white in dark themes (Zaid, 21 Nov) */}
details.ec-c summary span em{font-style:normal;font:600 9px 'IBM Plex Mono',monospace;letter-spacing:.08em;color:var(--muted);margin-left:5px}
details.ec-c summary i{font-style:normal;font:500 12px 'IBM Plex Mono',monospace;color:var(--muted);transition:transform .25s ease}
details.ec-c summary:hover{background:var(--surface2)}
details.ec-c summary:hover span{color:var(--strong)}
details.ec-c[open] summary i{transform:rotate(45deg);color:var(--acc-t)}
details.ec-c[open] summary span{color:var(--strong)}
.ect{margin:0 2px 12px 74px;padding:2px 0 2px 12px;border-left:1px solid var(--line2);font-size:12.5px;line-height:1.7;color:var(--body)}
.ect>b{display:block;font:600 9.5px 'IBM Plex Mono',monospace;letter-spacing:.12em;color:var(--muted);margin-bottom:1px}
.ect>span+span:before{content:"·";margin:0 7px;color:var(--muted)}
.ect>span{white-space:nowrap;display:inline-block}
.etc{grid-column:2/4;display:grid;grid-template-columns:auto minmax(0,1fr);align-items:baseline;column-gap:10px;margin-top:2px;font-size:11.5px;line-height:1.45;color:var(--muted)}
.etc a{white-space:nowrap;color:var(--muted);border-bottom:1px dotted var(--line2);transition:color .25s ease,border-color .25s ease}
.etc a:hover{color:var(--acc-t);border-bottom-color:var(--acc-t)}
.etc i{font-style:normal;margin:0 6px}
.etc>b{font:600 9px 'IBM Plex Mono',monospace;letter-spacing:.12em;color:var(--muted);opacity:.8}
.etc>span{display:flex;flex-wrap:wrap;column-gap:14px;row-gap:3px}
details.ec-c summary span.esl,.enx .sm span.esl{display:block;margin-top:3px;font:500 10px 'IBM Plex Mono',monospace;letter-spacing:.06em;color:var(--muted)}
.enx{border-bottom:1px dashed var(--line)}
.enx .sm{display:grid;grid-template-columns:66px minmax(0,1fr) 12px;gap:6px;align-items:baseline;padding:7px 2px}
.enx .sm code{font:600 10px 'IBM Plex Mono',monospace;color:var(--muted)}
.enx .sm>span{font-size:13px;line-height:1.35;color:var(--strong)}
.enx .sm>span em{font-style:normal;font:600 9px 'IBM Plex Mono',monospace;letter-spacing:.08em;color:var(--muted);margin-left:5px}
.ecl{display:flex;flex-wrap:wrap;align-items:center;gap:5px;margin-top:auto;padding-top:10px}
.ecl>b{font:600 9.5px 'IBM Plex Mono',monospace;letter-spacing:.1em;color:var(--muted);margin-right:2px}
.ecl>span{font:600 10px 'IBM Plex Mono',monospace;color:var(--muted)}
.ecl>span+span:before{content:"·";margin:0 6px 0 1px}
.ecm .efn{margin-top:12px;font-size:12.5px;color:var(--muted);line-height:1.5}

/* research cards */
.ers{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:14px}
.erc{display:flex;flex-direction:column;border:1px solid var(--line2);border-radius:10px;background:var(--surface);padding:16px 16px 12px;transition:border-color .25s ease}
.erc:hover{border-color:var(--muted)}
.erc .tg{font:600 10.5px 'IBM Plex Mono',monospace;letter-spacing:.1em;color:var(--muted)}
.erc .tg em{font-style:normal;color:var(--acc-t)}
.erc h3{font-size:15px;line-height:1.4;margin:8px 0 0}
.erc .evn{margin-top:8px;font-size:13px;color:var(--body)}
.erc .wh{margin-top:8px;font-size:13px;line-height:1.5;color:var(--muted)}
.erc .eft{display:flex;justify-content:space-between;align-items:center;margin-top:auto;padding-top:12px;border-top:1px solid var(--line);font:600 10.5px 'IBM Plex Mono',monospace;letter-spacing:.1em;color:var(--muted)}
.erc .eft b{font-weight:500;color:var(--body)}
.erc .eft a{border-bottom:1px dotted var(--line2)}
.erc .eft a:hover{color:var(--acc-t);border-bottom-color:var(--acc-t)}
.erc>div.sp{height:12px}
.emore{margin-top:12px;font:600 11px 'IBM Plex Mono',monospace;letter-spacing:.1em;color:var(--muted)}
.emore a{border-bottom:1px dotted var(--line2)}.emore a:hover{color:var(--acc-t)}

/* B.Sc. record in two pairs per row, certificates in one row below */
.erec.e2{grid-template-columns:120px minmax(0,1fr) 120px minmax(0,1fr)}
.erec.e2>span:nth-child(4n+3){padding-left:26px}
.erec.e2>span:nth-child(4n+2){padding-right:20px}
.ecs3{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:16px;margin-top:20px}
.ecs3 .ecrt img{aspect-ratio:1296/1845;object-fit:cover}
/* thesis */
.eths{display:grid;grid-template-columns:minmax(0,1.15fr) minmax(0,1fr);border:1px solid var(--line2);border-radius:12px;background:var(--surface);overflow:hidden}
.eths .evd{position:relative;background:#0B0D11;display:flex;align-items:center;border-right:1px solid var(--line2)}
.eths video{display:block;width:100%;height:auto}
.eths .evd>span{pointer-events:none;position:absolute;left:10px;top:9px;font:600 10px 'IBM Plex Mono',monospace;letter-spacing:.1em;color:rgba(255,255,255,.75);background:rgba(10,12,16,.55);padding:3px 7px;border-radius:4px}
.eths .tx{padding:18px 20px}
.eths .tg{font:600 10.5px 'IBM Plex Mono',monospace;letter-spacing:.1em;color:var(--muted)}
.eths .tg em{font-style:normal;color:var(--acc-t)}
.eths h3{font-size:17px;line-height:1.4;margin:8px 0 0}
.eths .evn{margin-top:6px;font-size:13.5px;color:var(--body)}
.eths .eau{margin-top:2px;font-size:13px;color:var(--muted)}
.eths .eau b{color:var(--strong);font-weight:600}
.eths p{margin-top:10px;font-size:13.5px;line-height:1.6;color:var(--body)}
.eths .erec{margin-top:10px;grid-template-columns:100px minmax(0,1fr)}
.eths .erec>span{font-size:13px;padding:7px 0}.eths .erec>span.ek{font-size:10.5px;padding-top:9px}
.eths .eft{display:flex;justify-content:space-between;align-items:center;margin-top:12px;font:600 10.5px 'IBM Plex Mono',monospace;letter-spacing:.1em;color:var(--muted)}
.eths .eft b{font-weight:500;color:var(--body)}
.eths .eft a{border-bottom:1px dotted var(--line2)}.eths .eft a:hover{color:var(--acc-t);border-bottom-color:var(--acc-t)}
.efg{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:12px;margin-top:12px}
.efg .ecrt .pp{background:#fff;padding:8px}
.efg .ecrt img{height:150px;object-fit:contain}
.etm3{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));margin-top:12px;border:1px solid var(--line);border-radius:8px;overflow:hidden}
.etm3 div{padding:8px 11px;border-left:1px solid var(--line)}.etm3 div:first-child{border-left:0}
.etm3 b{display:block;font:500 15px 'IBM Plex Mono',monospace;color:var(--strong)}
.etm3 span{font-size:11.5px;color:var(--muted)}
/* subject groups (HSC / SSC) */
.esg{display:grid;grid-template-columns:132px minmax(0,1fr);border-top:1px solid var(--line2)}
.esg>span{padding:10px 0;border-bottom:1px solid var(--line);font-size:14px;line-height:1.6;color:var(--strong)}
.esg>span.ek{font:600 11px 'IBM Plex Mono',monospace;letter-spacing:.1em;color:var(--muted);padding-top:12px}
.esg>span i{font-style:normal;display:inline!important;white-space:normal}
.esg>span i+i:before{content:"·";margin:0 8px 0 0;color:var(--muted)}
/* M.Sc. courses */
.emcl{border:1px solid var(--line2);border-radius:10px;background:var(--surface);padding:6px 12px 4px}
.emcl .mh{display:flex;justify-content:space-between;padding:6px 2px 8px;border-bottom:1px solid var(--line);font:600 10.5px 'IBM Plex Mono',monospace;letter-spacing:.1em;color:var(--muted)}
.emcl .mh b{color:var(--strong);font-weight:600}
.emcl details.ec-c:last-child{border-bottom:0}
.emcl .ec-c.nx summary{cursor:default}.emcl .ec-c.nx summary i{visibility:hidden}

/* term project */
.epj{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1.15fr);border:1px solid var(--line2);border-radius:12px;background:var(--surface);overflow:hidden}
.epj .eph2{position:relative;background-color:var(--surface2);background-image:linear-gradient(var(--line) 1px,transparent 1px),linear-gradient(90deg,var(--line) 1px,transparent 1px);background-size:26px 26px;
  display:flex;flex-direction:column;justify-content:center;align-items:center;gap:14px;padding:30px 24px;border-right:1px solid var(--line2)}
.epj .eph2 img.im1{width:86%;filter:drop-shadow(0 14px 18px rgba(0,0,0,.28));animation:epjf 6s ease-in-out infinite}
@keyframes epjf{0%,100%{transform:translateY(0)}50%{transform:translateY(-5px)}}
.epj .eph2 img.im2{width:62%;opacity:.92}
.epj .eph2 .lb{position:absolute;left:12px;top:10px;font:600 10px 'IBM Plex Mono',monospace;letter-spacing:.1em;color:var(--muted)}
.epj .eph2 .lb2{position:absolute;left:12px;bottom:10px;font:600 10px 'IBM Plex Mono',monospace;letter-spacing:.1em;color:var(--muted)}
.epj .tx{padding:20px 22px}
.epj .tg{font:600 10.5px 'IBM Plex Mono',monospace;letter-spacing:.1em;color:var(--muted)}
.epj h3{font-size:21px;margin:8px 0 0}
.epj p{margin-top:8px;font-size:14px;line-height:1.6;color:var(--body)}
.epj .erec{margin-top:12px;grid-template-columns:104px minmax(0,1fr)}
.epj .erec>span{font-size:13.5px;padding:8px 0}
.epj .erec>span.ek{font-size:10.5px;padding-top:10px}
.etm{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:0;margin-top:14px;border:1px solid var(--line);border-radius:8px;overflow:hidden}
.etm div{padding:9px 12px;border-left:1px solid var(--line)}.etm div:first-child{border-left:0}
.etm b{display:block;font:500 16px 'IBM Plex Mono',monospace;color:var(--strong)}
.etm span{font-size:12px;color:var(--muted);white-space:nowrap}
.edc{margin-top:14px;font-size:13.5px;line-height:1.55;color:var(--muted)}
.edc b{color:var(--body);font-weight:600}

/* beyond the classroom */
.ebx{border:1px solid var(--line2);border-radius:10px;background:var(--surface);padding:4px 12px}
.ebr{display:grid;grid-template-columns:150px minmax(0,1fr) auto;gap:4px 20px;padding:13px 6px;border-bottom:1px solid var(--line);align-items:baseline}
.ebr:last-child{border-bottom:0}
.ebr .edd{font:600 11px 'IBM Plex Mono',monospace;letter-spacing:.06em;color:var(--muted)}
.ebr b{font-size:14.5px;color:var(--strong);font-weight:600}
.ebr .eo{font-size:13.5px;color:var(--body)}
.ebr .et{font:600 10.5px 'IBM Plex Mono',monospace;letter-spacing:.1em;color:var(--muted)}
.ecw{display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:12px;margin-top:14px}
.ecw .ecrt .ecp{display:block}
.ecw .ecrt .ecp b{display:block;font:600 10.5px 'IBM Plex Mono',monospace;letter-spacing:.08em;color:var(--acc-t)}
.ecw .ecrt .ecp em{display:block;font-style:normal;font:500 12.5px 'Inter',sans-serif;letter-spacing:0;color:var(--body);margin-top:2px}
.ecw .ecrt .ecp small{display:block;font:600 10px 'IBM Plex Mono',monospace;color:var(--muted);margin-top:2px}

/* recognition certificates */
.exl{margin:12px 0 0}.exl a{font:600 11px 'IBM Plex Mono',monospace;letter-spacing:.08em;color:var(--muted);border-bottom:1px dotted var(--line2);padding-bottom:1px;transition:color .25s ease}.exl a:hover{color:var(--acc-t)}
.esm{margin:22px 0 0;font:600 10.5px 'IBM Plex Mono',monospace;letter-spacing:.12em;color:var(--muted)}
.ecw.ecr{grid-template-columns:repeat(3,minmax(0,1fr));gap:16px}
.ecw .ecrt .ecp .why{display:block;margin-top:3px;font:400 12.5px/1.45 'Inter',sans-serif;letter-spacing:0;color:var(--muted)}
/* lower degrees */
.elow{display:grid;grid-template-columns:minmax(0,1fr) 400px;gap:28px;align-items:start}
.esj{display:flex;flex-wrap:wrap;gap:6px;margin-top:12px}
.esj span{border:1px solid var(--line);border-radius:999px;padding:4px 11px;font-size:13px;color:var(--body)}
.esj span.ad{border-style:dashed;color:var(--muted)}
.esj span.ad b{font:600 9.5px 'IBM Plex Mono',monospace;letter-spacing:.08em;margin-left:6px;font-weight:600}
.emc{border:1px solid var(--line2);border-radius:10px;background:var(--surface);padding:14px 16px}
.emc .tg{font:600 10.5px 'IBM Plex Mono',monospace;letter-spacing:.1em;color:var(--muted)}
.emc .tg em{font-style:normal;color:var(--acc-t)}
.emc h3{font-size:16px;margin:6px 0 0}
.etl2{border:1px solid var(--line2);border-radius:10px;background:var(--surface);padding:4px 12px}
.etl2 .ebr{grid-template-columns:150px minmax(0,1fr) 220px}

/* vernier scale */
.vsc{position:relative;width:190px;height:22px}
.vsc .vtk{position:absolute;left:0;right:0;bottom:0;height:10px;
  background:repeating-linear-gradient(90deg,var(--line2) 0 1px,transparent 1px var(--minor)) left bottom/100% 5px no-repeat,
             repeating-linear-gradient(90deg,var(--muted) 0 1px,transparent 1px var(--major)) left bottom/100% 10px no-repeat;opacity:.8}
.vsc .vtk:after{content:"";position:absolute;right:0;bottom:0;width:1px;height:10px;background:var(--muted)}
.vsc .vfl{position:absolute;left:0;bottom:0;height:2px;background:var(--body);opacity:.55}
.vsc .vpt{position:absolute;bottom:11px;width:0;height:0;margin-left:-5px;border:5px solid transparent;border-top:7px solid var(--acc-t);border-bottom:0}
.vsc.vpd .vpt{animation:vsw 7s ease-in-out infinite}
.vsc.vpd .vtk{opacity:.5}
@keyframes vsw{0%,100%{left:12%}50%{left:70%}}

@media (max-width:1100px){.ers{grid-template-columns:1fr}.ecw{grid-template-columns:repeat(3,minmax(0,1fr))}}
@media (max-width:960px){.erec.e2{grid-template-columns:118px minmax(0,1fr)}.erec.e2>span:nth-child(4n+3){padding-left:0}.erec.e2>span:nth-child(4n+2){padding-right:0}.efg{grid-template-columns:1fr 1fr}.eths{grid-template-columns:1fr}.eths .evd{border-right:0;border-bottom:1px solid var(--line2)}.dnote{grid-template-columns:1fr}.edw{grid-template-columns:1fr;gap:0}
  .eix{position:static;flex-direction:row;flex-wrap:wrap;gap:6px;border-left:0;margin-bottom:28px}
  .eix .ixh{display:none}.eix .ixs{display:none!important}.eix .ixg{display:contents}.eix .ixl{border:1px solid var(--line)!important;border-radius:999px;padding:5px 11px;margin:0}.eix .ixl.ion{border-color:var(--acc-t)!important}
  .erw,.elow,.epj{grid-template-columns:1fr}.epj .eph2{border-right:0;border-bottom:1px solid var(--line2)}}
@media (max-width:760px){
  .ph{padding-top:28px}.ph .h1{font-size:26px!important}.ph .lead{font-size:15px!important}
  .dopt{margin-top:28px;padding:16px 10px 22px}
  .epz .eph h1{font-size:28.6px}   /* phone: 30 px after the type scale, same as every page title (21 Nov) */
  .est{grid-template-columns:1fr 1fr}.est>div:nth-child(3){border-left:0}.est>div:nth-child(n+3){border-top:1px solid var(--line)}
  .est b{font-size:17px}.est span{font-size:12px}
  .ecg{grid-template-columns:1fr}
  .etc{grid-template-columns:1fr;row-gap:1px}.etc>span{column-gap:12px}
  .etc a{white-space:normal}
  .eths .evd span{font-size:9px;right:10px}
  .ecs3{grid-template-columns:1fr 1fr}.ecs3 .ecrt:first-child{grid-column:1/3}
  .erec.e2{grid-template-columns:104px minmax(0,1fr)}
  .ect{margin-left:2px}
  .esg{grid-template-columns:104px minmax(0,1fr)}
  .etm3 span{font-size:10.5px}
  .efg .ecrt img{height:auto}
  .erec{grid-template-columns:104px minmax(0,1fr)}.erec>span{font-size:14px}
  .ecw{grid-template-columns:1fr 1fr}.ecw.ecr{grid-template-columns:1fr}
  .ebr,.etl2 .ebr{grid-template-columns:1fr;gap:2px}
  .etm span{font-size:11px}.etm b{font-size:14px}.etm div{padding:8px 9px}
  .ect{padding-left:2px}
  .ecf{grid-template-columns:repeat(2,minmax(0,1fr));gap:5px}.ecf label{height:32px;padding:0 10px;font-size:12px}
}

/* index targets: a hidden, viewport-tall input at the top of each section; clicking an index label focuses it, so the browser scrolls it to the top */
.ego{position:absolute;left:0;top:-96px;width:1px;height:100vh;opacity:0;pointer-events:none;border:0;margin:0;padding:0}
.esc,.ebk{position:relative}
html{scroll-behavior:smooth}
/* panels answer the cursor (Zaid, 22 Nov 2026): lift, accent edge, rows react */
.etb,.eths,.epj,.ebx{position:relative;transition:transform .35s ease,border-color .35s ease,box-shadow .35s ease}
.etb:before,.eths:before,.epj:before,.ebx:before{content:"";position:absolute;top:-1px;left:14px;right:14px;height:2px;border-radius:2px;background:var(--acc);transform:scaleX(0);transform-origin:left;transition:transform .45s ease;z-index:2;pointer-events:none}
.etb .eth b,.etb .eth span{transition:color .3s ease}
.ec-c code,.enx .sm code{transition:color .25s ease}
details.ec-c summary>span,.enx .sm>span{transition:transform .25s ease}
.enx .sm{border-radius:5px;transition:background .25s ease}
.eths .evd video,.epj img{transition:transform .5s ease,filter .5s ease}
.ebr{transition:background .25s ease}.ebr b{transition:color .25s ease}
@media (hover:hover){
  .etb:hover,.eths:hover,.epj:hover,.ebx:hover{transform:translateY(-3px);border-color:color-mix(in srgb,var(--acc-t) 45%,var(--line2));box-shadow:0 1px 0 rgba(0,0,0,.06),0 16px 34px rgba(0,0,0,.22)}
  .etb:hover:before,.eths:hover:before,.epj:hover:before,.ebx:hover:before{transform:scaleX(1)}
  .etb:hover .eth b{color:var(--acc-t)}
  details.ec-c summary:hover code,.enx .sm:hover code{color:var(--acc-t)}
  details.ec-c summary:hover>span,.enx .sm:hover>span{transform:translateX(3px)}
  .enx .sm:hover{background:var(--surface2)}
  .eths:hover .evd video{transform:scale(1.02)}
  .epj:hover img{transform:scale(1.02)}
  .ebr:hover{background:var(--surface2)}.ebr:hover b{color:var(--acc-t)}
}
@media (prefers-reduced-motion:reduce){.etb,.eths,.epj,.ebx,.etb:before,.eths:before,.epj:before,.ebx:before,details.ec-c summary>span,.enx .sm>span,.eths .evd video,.epj img{transition:none}
  .etb:hover,.eths:hover,.epj:hover,.ebx:hover,details.ec-c summary:hover>span,.enx .sm:hover>span,.eths:hover .evd video,.epj:hover img{transform:none}}
"""


def vernier(val, lo, hi, step, pending=False):
    n = round((hi - lo) / step)
    minor = 100 / n
    major = 100 / (n / 4) if n % 4 == 0 else 25
    st = f"--minor:{minor:.4f}%;--major:{major:.4f}%"
    if pending:
        return f'<div class="vsc vpd" style="{st}"><i class="vtk"></i><i class="vpt"></i></div>'
    p = (float(val) - lo) / (hi - lo) * 100
    return (f'<div class="vsc" style="{st}"><i class="vtk"></i><i class="vfl" style="width:{p:.1f}%"></i>'
            f'<i class="vpt" style="left:{p:.1f}%"></i></div>')


_LB = []  # lightboxes, written once at the end of the page


def cert(key, cap, cls=""):
    lid = f"lb-{key}"
    _LB.append(f'<input type="checkbox" class="elbc" id="{lid}"><label class="elb" for="{lid}"><img src="{B[key]}" alt="{cap}"><span>CLOSE ×</span></label>')
    return (f'<label class="ecrt {cls}" for="{lid}"><span class="pp"><img src="{B[key]}" alt="{cap}{' (personal numbers hidden)' if key in ('prov','eng','grade','hsc','ssc') else ''}"></span>'
            f'<span class="ecp">{cap}<i>{ZOOM}</i></span></label>')


def rec(rows):
    return '<div class="erec">' + "".join(f'<span class="ek">{k}</span><span>{v}</span>' for k, v in rows) + "</div>"


COLLAPSE = True   # approved 21 Nov: course map shows Year 4 only, the rest behind SHOW ALL 8 TERMS

COLLAPSE_CSS = """
.ecg .ecx{display:none}
.ecm #cm-more:checked~.ecg .ecx,#b2:target .ecg .ecx{display:flex}
.cmb{position:relative;display:flex;align-items:center;justify-content:center;gap:10px;margin-top:12px;height:44px;border:1px dashed var(--line2);border-radius:10px;
  font:600 11px 'IBM Plex Mono',monospace;letter-spacing:.1em;color:var(--strong);cursor:pointer;background:var(--surface);transition:border-color .25s,color .25s,background .25s}
.cmb:hover{border-color:var(--acc-t);color:var(--acc-t);background:var(--surface2)}
.cmb i{font-style:normal;transition:transform .3s ease}
.cmb .c{display:none}
.ecm #cm-more:checked~.cmb .o{display:none}
.ecm #cm-more:checked~.cmb .c{display:inline}
.ecm #cm-more:checked~.cmb i{transform:rotate(180deg)}
@media (max-width:760px){.cmb{font-size:10px;letter-spacing:.06em;height:auto;padding:12px 10px;text-align:center}}
"""


def course_map(split=False):
    counts = {k: 0 for k, _ in D.AREAS}
    for c in D.COURSES:
        counts[c[3]] += 1
    inputs = '<input type="radio" name="cmf" id="cf-all" checked>' + "".join(f'<input type="radio" name="cmf" id="cf-{k}">' for k, _ in D.AREAS)
    short = {"mfg": "Manufacturing", "des": "Design &amp; CAD", "ops": "Ops, QM &amp; SCM", "ora": "OR &amp; statistics",
             "hf": "Human factors", "mgt": "Management", "dat": "Computing &amp; IS", "eng": "Eng. science",
             "sci": "Math &amp; science", "com": "Communication", "prj": "Projects &amp; thesis"}
    chips = (f'<label for="cf-all" class="l-all"><span>All courses</span><small>{len(D.COURSES)}</small></label>'
             + "".join(f'<label for="cf-{k}" class="l-{k}" title="{lab}"><span>{short[k]}</span><small>{counts[k]}</small></label>' for k, lab in D.AREAS))
    blocks = ""
    nterm = 0
    for tk, tl, per in reversed(D.TERMS):          # newest term first
        items = [c for c in D.COURSES if c[0] == tk]
        codes = {c[1]: c for c in items}
        def lab_of(code):                            # sessional = same prefix, number + 1
            p, n = code.split()
            return codes.get(f"{p} {int(n) + 1}")
        paired = set()
        for c in items:
            if c[4] == "" and lab_of(c[1]) and lab_of(c[1])[4] == "lab":
                paired.add(lab_of(c[1])[1])
        if split:
            blk = split_term(tl, per, items, codes)
            if COLLAPSE and nterm >= 2:                # proposal: only the two newest terms show until SHOW ALL is clicked
                blk = blk.replace('<div class="etb">', '<div class="etb ecx">', 1)
            nterm += 1
            blocks += blk
            continue
        rows = ""
        for term, code, title, area, kind, topics in items:
            if code in paired:
                continue
            lab = lab_of(code) if kind == "" else None
            tag = " <em>LAB</em>" if kind == "lab" else (" <em>PROJECT</em>" if kind == "prj" else "")
            sess = (f'<span class="esl">+ SESSIONAL · {lab[1]}</span>' if lab and lab[1] in paired else "")
            opened = " open" if code in ("IPE 4225",) else ""
            if topics:
                ch = "".join(f"<span>{t}</span>" for t in topics)
                rows += (f'<details class="ec-c a-{area}"{opened}><summary><code>{code}</code><span>{title}{tag}{sess}</span><i>+</i>{teachers(code)}</summary>'
                         f'<div class="ect"><b>TOPICS</b>{ch}</div></details>')
            else:
                rows += (f'<div class="ec-c a-{area} enx"><div class="sm"><code>{code}</code><span>{title}{tag}{sess}</span><i></i>{teachers(code)}</div></div>')
        blocks += f'<div class="etb"><div class="eth"><b>{tl}</b><span>{per}</span></div><div class="elst">{rows}</div></div>'
    more = ""
    if COLLAPSE and split:
        rest = [c for c in D.COURSES if c[0] in [k for k, _, _ in D.TERMS][:-2]]
        inputs += '<input type="checkbox" id="cm-more">'
        more = (f'<label class="cmb" for="cm-more"><span class="o">SHOW ALL {len(D.TERMS)} TERMS · {len(D.TERMS) - 2} MORE, {len(rest)} COURSES</span>'
                f'<span class="c">SHOW ONLY YEAR 4</span><i>↓</i></label>')
    return (f'<div class="ecm">{inputs}<div class="ecf">{chips}</div><div class="ecg">{blocks}</div>{more}'
            '<p class="efn">* Because of COVID-19, both Year 1 terms ran together from Feb 2020 to Mar 2022. '
            'Topics come from the KUET IPE syllabus. Each term\'s button shows its class routine and teachers; teacher names open their KUET profile (LinkedIn for former faculty). '
            'Areas follow the IISE Industrial &amp; Systems Engineering Body of Knowledge.</p></div>')


def theory_of(code, codes):
    """Theory course a sessional belongs to: same prefix, number - 1."""
    p, n = code.split()
    t = codes.get(f"{p} {int(n) - 1}")
    return t if t and t[4] == "" else None


def course_row(code, title, area, tag, extra, topics, tcode=None):
    who = ""        # teachers now live in each term's ROUTINE & TEACHERS panel (Zaid, 21 Nov 2026)
    if topics:
        ch = "".join(f"<span>{t}</span>" for t in topics)
        return (f'<details class="ec-c a-{area}"><summary><code>{code}</code><span>{title}{tag}{extra}</span><i>+</i>{who}</summary>'
                f'<div class="ect"><b>TOPICS</b>{ch}</div></details>')
    return f'<div class="ec-c a-{area} enx"><div class="sm"><code>{code}</code><span>{title}{tag}{extra}</span><i></i>{who}</div></div>'


def split_term(tl, per, items, codes):
    """One term: theory courses on top, sessionals and labs below."""
    th = [c for c in items if c[4] == ""]
    se = [c for c in items if c[4] == "lab"] + [c for c in items if c[4] == "prj"]
    rows = ""
    for _, code, title, area, kind, topics in th:
        rows += course_row(code, title, area, "", "", topics)
    if se:
        rows += '<div class="egl egs"><b>SESSIONAL &amp; LAB</b></div>'
    for _, code, title, area, kind, topics in se:
        t = theory_of(code, codes)
        tag = " <em>PROJECT</em>" if kind == "prj" else ""
        extra = f'<span class="esl">WITH THEORY · {t[1]}</span>' if t else ""
        # a sessional tied to a theory course is run by the same teachers
        tcode = code if D.TEACH.get(code) else (t[1] if t else code)
        rows += course_row(code, title.replace(" Sessional", ""), area, tag, extra, topics, tcode)
    return f'<div class="etb">{R.header(items[0][0], tl, per)}<div class="elst">{rows}</div></div>'


def teachers(code):
    keys = D.TEACH.get(code, [])
    if not keys:
        return ""
    links = "".join(f'<a href="{D.T[k][1]}" target="_blank" rel="noopener">{D.T[k][0]}</a>' for k in keys)
    return f'<span class="etc"><b>TAUGHT BY</b><span>{links}</span></span>'


def area_css():
    s = ".ecm #cf-all:checked~.ecf .l-all"
    out = []
    for k, _ in D.AREAS:
        out.append(f".ecm #cf-{k}:checked~.ecg .ec-c:not(.a-{k}){{opacity:.2}}")
        s += f",.ecm #cf-{k}:checked~.ecf .l-{k}"
    out.append(s + "{border-color:var(--acc-t);color:var(--acc-t);background:var(--acc-soft)}")
    if COLLAPSE:        # picking an area opens every term, so no filtered course stays hidden
        out += [f".ecm #cf-{k}:checked~.ecg .ecx{{display:flex}}.ecm #cf-{k}:checked~.cmb{{display:none}}" for k, _ in D.AREAS]
    return "\n".join(out)


def thesis():
    p = RL.PUBS[0]
    year, kind, tier, first, title, venue, pub, auth, doi, jif, cs = p
    figs = (cert("fig01", "FIG. 1 · STUDY FRAMEWORK") + cert("fig02", "FIG. 2 · DATA PREPARATION AND WORKER RECORDS") + cert("fig06", "FIG. 6 · WHERE OPERATORS REPORT PAIN")
            + cert("fig10", "FIG. 10 · EIGHT CLASSIFIERS COMPARED"))
    return f"""<div class="eths">
      <div class="evd">{VP.panel("thesis", f'<video src="{B["video"]}" poster="{B["poster"]}" autoplay muted loop playsinline preload="metadata" aria-label="Two-camera recording of a sewing-machine operator with joint-angle markers; face blurred"></video>', B["video"], B["poster"], "Two-camera recording of a sewing-machine operator with joint-angle markers from Kinovea; face blurred", "B.SC. THESIS VIDEO")}
        <span>BILATERAL VIDEO · KINOVEA JOINT ANGLES · FACE BLURRED</span></div>
      <div class="tx"><div class="tg">B.SC. THESIS · IPE 4000 → PUBLISHED · <em>{tier}</em> · 1ST AUTHOR</div>
        <h3>{title}</h3>
        <div class="evn">{venue} · {pub}</div>
        <div class="eau">{auth.replace("Md. Zaid Hossain", "<b>Md. Zaid Hossain</b>")}</div>
        <p>Sewing-machine operators were filmed from both sides, their joint angles measured frame by frame in Kinovea and turned into RULA posture scores and combined them with a body-pain questionnaire. Eight machine-learning models were then tested with a leakage-controlled, nested cross-validation to classify each worker's musculoskeletal risk.</p>
        <div class="etm3"><div><b>60</b><span>operators</span></div><div><b>8</b><span>classifiers tested</span></div><div><b>0.94</b><span>best balanced accuracy</span></div></div>
        <div class="eft"><span>IF <b>{jif}</b> · CITESCORE <b>{cs}</b></span><a href="https://doi.org/{doi}" target="_blank" rel="noopener">DOI ↗</a></div>
      </div></div>
    <div class="efg">{figs}</div>
    <div class="emore">Other papers written during the degree: Array (2026) · IEEE QPAIN (2025) · ICMERE (2025) · <a href="#">RESEARCH PAGE →</a></div>"""


def term_project():
    return f"""<div class="epj">
      <div class="eph2"><span class="lb">FIG. 01 · BUILT PROTOTYPE</span><img class="im1" src="{B['tp']}" alt="Weight-based sorting machine prototype">
        <img class="im2" src="{B['tpcad']}" alt="CAD model of the sorting machine"><span class="lb2">FIG. 02 · CAD MODEL</span></div>
      <div class="tx"><div class="tg">TERM PROJECT · IPE 4002 · JUN 2024</div>
        <h3>Weight-based sorting machine</h3>
        <p>A low-cost prototype that weighs each item on a load cell, moves it on a small conveyor and pushes it into the right bin with servo arms, so small parts are sorted without manual checking.</p>
        <div class="etm"><div><b>3</b><span>weight classes</span></div><div><b>≤ 2 s</b><span>to sort one item</span></div><div><b>35 to 40</b><span>items per minute</span></div></div>
        {rec([("TEAM", "Md. Zaid Hossain, Md. Shahriar Islam"),
              ("SUPERVISOR", "Md. Golam Kibria <em>· Associate Professor, IEM, KUET</em>"),
              ("PARTS", "Arduino Uno, load cell with HX711, gear-motor conveyor, SQ90 servo arms, OLED display"),
              ("TESTS", "2 to 8 g in 0.57 s · 8 to 14 g in 1.27 s · 14 to 20 g in 1.86 s <em>(average of 3 runs)</em>"),
              ("CAD", "Adapted from a senior's base model and edited by me <em>· May 2024</em>"), ("REPORT", "46 pages, written in LaTeX <em>· 2 Jun 2024</em>")])}
      </div></div>
    <p class="edc"><b>Design coursework:</b> Engineering Drawing · CAD Sessional I (2D, AutoCAD) · CAD Sessional II (3D, SOLIDWORKS) · Product Design I and II. The CAD work from these and my own projects is on the <a href="#">Projects page →</a></p>"""


def beyond():
    rows = [
        ("MAR 2024 → SEP 2025", "FabLab Assistant · Student Operator", "FabLab, KUET · certified student operator from Mar 2024 to Mar 2025, then stayed on as a volunteer to Sep 2025 · ran 3D printers and digital fabrication machines; helped students make their CAD designs printable", "WORK"),
        ("AUG 2025", "Award of Excellence · Certificate of Contribution", "Directorate of Students' Welfare (DSW), KUET · the Award of Excellence crest, and a certificate for outstanding contribution to extracurricular activities", "AWARD"),
        ("2024", "Hall Committee Member · Mosque Committee", "Amar Ekushey Hall, KUET · student affairs, the hall mosque and the annual hall feast", "LEADERSHIP"),
        ("OCT 2024", "Dining Manager", "Amar Ekushey Hall, KUET · meal planning, purchasing and budget for the hall", "LEADERSHIP"),
        ("2023 → 2024", "CAD competitions", "3 times champion, 2 times 2nd runner-up, 1 top-20 finalist", "CAD"),
    ]
    rr = "".join(f'<div class="ebr"><span class="edd">{d}</span><span><b>{t}</b><br><span class="eo">{o}</span></span><span class="et">{g}</span></div>' for d, t, o, g in rows)
    cw = ""
    for title, ev, org, date, key in D.CAD_WINS:
        if not key:
            continue
        lid = f"lb-{key}"
        _LB.append(f'<input type="checkbox" class="elbc" id="{lid}"><label class="elb" for="{lid}"><img src="{B[key]}" alt="{ev} certificate"><span>CLOSE ×</span></label>')
        cw += (f'<label class="ecrt" for="{lid}"><span class="pp"><img src="{B[key]}" alt="{ev} certificate"></span>'
               f'<span class="ecp"><b>{title.upper()}</b><em>{ev}</em><small>{org} · {date}</small></span></label>')
    rec_c = [("fablabc", "STUDENT OPERATOR", "Certificate of Achievement", "For contributions to FabLab KUET as a student operator · Mar 2024 to Mar 2025", "FabLab KUET · AASDC"),
             ("dsw", "CONTRIBUTION", "Certificate of Contribution", "For outstanding contribution to extracurricular activities · 12 Aug 2025", "Directorate of Students' Welfare, KUET"),
             ("hall", "RECOGNITION", "Certificate of Recognition", "For service in the Mosque Committee of the Amar Ekushey Hall committee 2024 · 9 Sep 2025", "Amar Ekushey Hall, KUET")]
    rc = ""
    for key, tag, title, why, org in rec_c:
        lid = f"lb-{key}"
        _LB.append(f'<input type="checkbox" class="elbc" id="{lid}"><label class="elb" for="{lid}"><img src="{B[key]}" alt="{title}"><span>CLOSE ×</span></label>')
        rc += (f'<label class="ecrt" for="{lid}"><span class="pp"><img src="{B[key]}" alt="{title}{" (roll number hidden)" if key != "hall" else ""}"></span>'
               f'<span class="ecp"><b>{tag}</b><em>{title}</em><span class="why">{why}</span><small>{org}</small></span></label>')
    return (f'<div class="ebx">{rr}</div><p class="exl"><a href="#">Roles and recognition in detail on the Experience page →</a></p><div class="esm">RECOGNITION</div><div class="ecw ecr">{rc}</div>'
            f'<p class="exl"><a href="#">CAD competition results and certificates on the Awards page →</a></p>')


def lower(level, rows, groups, key, year):
    sg = "".join(f'<span class="ek">{g}</span><span>' + " ".join(f"<i>{x}</i>" for x in items) + "</span>" for g, items in groups)
    return (f'<div class="elow"><div>{rec(rows)}</div><div class="ecs" style="grid-template-columns:1fr">{cert(key, f"{level} CERTIFICATE · {year}")}</div></div>',
            f'<div class="esg">{sg}</div>')


def GO(k):
    """Hidden focus target for the index (see .ego)."""
    return f'<input class="ego" type="checkbox" id="go-{k}" tabindex="-1" aria-hidden="true">'


def sub(tl, n, label, body):
    """A sub-section with its own scroll timeline (drives the index)."""
    return f'<div class="ebk" id="{tl[2:]}" style="view-timeline-name:{tl}">{GO(tl[2:])}<div class="ess"><b>{n}</b> {label}</div>{body}</div>'


def head(n, eb, h2, hid):
    return (f'<div class="sh" id="{hid}"><div class="eb"><span class="ebn">{n}</span><span class="ebt">{eb}</span><span class="ebl"></span></div>'
            f'<div class="shr"><h2 class="h2">{h2}</h2></div></div>')


def page_body():
    _LB.clear()
    # 01 M.Sc.
    # M.Sc. courses in the same card as a B.Sc. term (Zaid, 22 Nov 2026): header, TEACHERS button, rows without TAUGHT BY
    msc_rows = "".join(course_row(c, t, "ms", "", "", tp) for c, t, tp in D.MSC_COURSES)
    msc_card = (f'<div class="etb emsc"><div class="eth rth2"><div><b>{R.MSC_LABEL}</b><span>{R.MSC_PER}</span></div>{R.msc_button()}</div>'
                f'<div class="elst">{msc_rows}</div></div>')
    msc = f"""
      {head("01", "MASTER'S", "M.Sc. Eng. in Industrial Engineering &amp; Management", "msc")}
      {sub("--m1", "1.1", "RECORD", rec([
          ("UNIVERSITY", "Khulna University of Engineering &amp; Technology (KUET)"),
          ("DEPARTMENT", "Industrial Engineering and Management (IEM)"),
          ("STARTED", "July 2026 semester <em>· part-time</em>"),
          ("FOCUS", "Operations research · supply chain management · machine-learning integration"),
          ("CGPA", f'<em>Results pending</em>{vernier(None, 0, 4, 0.25, True)}')]))}
      {sub("--m2", "1.2", "COURSES · 9 CREDITS", msc_card)}"""
    # 02 B.Sc.
    bsc_rec = rec([
        ("UNIVERSITY", "Khulna University of Engineering &amp; Technology (KUET) <em>· Khulna</em>"),
        ("DEPARTMENT", "Industrial Engineering and Management (IEM)"),
        ("SESSIONS", "2019-20 → 2022-23 <em>· enrolled 1 Dec 2019</em>"),
        ("COMPLETED", "24 Sep 2025"),
        ("CREDITS", "161.75 earned <em>· 160 required · 70 courses</em>"),
        ("CGPA", f'3.45 <em>/ 4.00</em>{vernier("3.45", 0, 4, 0.25)}'),
        ("MEDIUM", "English"),
        ("TRANSCRIPT", f'<em style="display:inline-flex;align-items:center;gap:6px">{LOCK} On request by email</em>'),
    ])
    bsc_rec2 = bsc_rec.replace('class="erec"', 'class="erec e2"')
    certs = (f'<div class="ecs3">{cert("prov", "PROVISIONAL CERTIFICATE")}{cert("eng", "ENGLISH PROFICIENCY")}'
             f'{cert("grade", "GRADE CONVERSION")}</div>')
    bsc = f"""
      {head("02", "BACHELOR'S", "B.Sc. Eng. in Industrial &amp; Production Engineering", "bsc")}
      {sub("--b1", "2.1", "RECORD &amp; CERTIFICATES", f'{bsc_rec2}{certs}<p class="enote">Personal numbers (roll, registration, serial) and parents&#39; names are hidden on every certificate shown here.</p>')}
      {sub("--b2", "2.2", "COURSE MAP · 8 TERMS · 70 COURSES", course_map(split=True))}
      {sub("--b3", "2.3", "THESIS", thesis())}
      {sub("--b4", "2.4", "PROJECTS", term_project())}
      {sub("--b5", "2.5", "BEYOND THE CLASSROOM", beyond())}"""
    hrec, hsub = lower("HSC", [("COLLEGE", "Dhaka College <em>· Dhaka</em>"), ("BOARD", "Dhaka"), ("GROUP", "Science"),
                               ("YEAR", "2019 <em>· result published 17 Jul 2019</em>"), ("GPA", f'5.00 <em>/ 5.00</em>{vernier("5.00", 0, 5, 0.25)}')],
                       D.HSC_GROUPS, "hsc", "2019")
    srec, ssub = lower("SSC", [("SCHOOL", "Armanitola Govt. High School <em>· Dhaka</em>"), ("BOARD", "Dhaka"), ("GROUP", "Science"),
                               ("YEAR", "2017 <em>· result published 4 May 2017</em>"), ("GPA", f'5.00 <em>/ 5.00</em>{vernier("5.00", 0, 5, 0.25)}')],
                       D.SSC_GROUPS, "ssc", "2017")
    hsc = f"""
      {head("03", "HIGHER SECONDARY", "Higher Secondary Certificate (HSC)", "hsc")}
      {sub("--h1", "3.1", "RECORD &amp; CERTIFICATE", hrec)}
      {sub("--h2", "3.2", "SUBJECTS", hsub)}"""
    ssc = f"""
      {head("04", "SECONDARY", "Secondary School Certificate (SSC)", "ssc")}
      {sub("--c1", "4.1", "RECORD &amp; CERTIFICATE", srec)}
      {sub("--c2", "4.2", "SUBJECTS", ssub)}"""
    tests = f"""
      {head("05", "TESTS", "Language &amp; graduate tests", "tests")}
      <div class="etl2" style="margin-top:22px">
        <div class="ebr"><span class="edd">2026 → NOW</span><span><b>IELTS Academic</b><br><span class="eo">In preparation · score added when the result is out</span></span><span>{vernier(None, 0, 9, 0.5, True)}</span></div>
        <div class="ebr"><span class="edd">2026 → NOW</span><span><b>GRE General</b><br><span class="eo">In preparation · score added when the result is out</span></span><span>{vernier(None, 260, 340, 5, True)}</span></div>
      </div>"""
    nav = [("--s1", "msc", "01", "M.Sc.", [("--m1", "1.1", "Record"), ("--m2", "1.2", "Courses")]),
           ("--s2", "bsc", "02", "B.Sc.", [("--b1", "2.1", "Record"), ("--b2", "2.2", "Course map"),
                                           ("--b3", "2.3", "Thesis"), ("--b4", "2.4", "Projects"), ("--b5", "2.5", "Beyond class")]),
           ("--s3", "hsc", "03", "HSC", [("--h1", "3.1", "Record"), ("--h2", "3.2", "Subjects")]),
           ("--s4", "ssc", "04", "SSC", [("--c1", "4.1", "Record"), ("--c2", "4.2", "Subjects")]),
           ("--s5", "tests", "05", "TESTS", [])]
    idx = '<nav class="eix" aria-label="On this page"><span class="ixh">ON THIS PAGE</span>'
    for k, (tl, hid, n, lab, subs) in enumerate(nav):
        on = " ion" if k == 0 else ""
        sl = "".join(f'<label for="go-{t[2:]}" style="animation-timeline:{t}" class="ixl{" ion" if (k == 0 and j == 0) else ""}"><b>{sn}</b>{sl_}</label>'
                     for j, (t, sn, sl_) in enumerate(subs))
        idx += (f'<div class="ixg{on}"><label for="go-{hid}" class="ixl{on}" style="animation-timeline:{tl}"><i>{n}</i>{lab}</label>'
                + (f'<div class="ixs" style="animation-timeline:{tl}"><div>{sl}</div></div>' if subs else "") + "</div>")
    idx += "</nav>"
    secs = "".join(f'<section class="esc" style="view-timeline-name:{tl}">{GO(hid)}{body}</section>'
                   for tl, hid, body in (("--s1", "msc", msc), ("--s2", "bsc", bsc), ("--s3", "hsc", hsc), ("--s4", "ssc", ssc), ("--s5", "tests", tests)))
    return f"""
    <div class="epz">
      <div class="eph"><div class="crumb">HOME / EDUCATION</div><h1 class="h1">Education</h1>
        <p>A part-time master's in industrial engineering and management at KUET, after a bachelor's in industrial and production engineering there, where I also did my first research and ran the FabLab's machines. School and college in Dhaka.</p></div>
      <div class="est"><div><b>3.45 / 4.00</b><span>B.Sc. CGPA</span></div><div><b>70</b><span>courses · 161.75 credits</span></div>
        <div><b>2</b><span>Q1 journal papers</span></div><div><b>5</b><span>CAD competition podiums</span></div></div>
      <div class="egt">{EG.gantt()}</div>
      <div class="edw">{idx}<div>{secs}</div></div>
      {"".join(_LB)}
    </div>"""


def body():
    inner = page_body()
    return f"""
  <main class="wrap" style="position:relative;z-index:1">
    <section class="ph">
      <div class="crumb">PROPOSAL / EDUCATION PAGE · DETAILED · FOR REVIEW, NOT APPLIED</div>
      <h1 class="h1">Education page · in full</h1>
      <p class="lead">Opens from "Results &amp; certificates →" on Home. Everything below the line is the page itself.</p>
    </section>
    <div class="dnote">
      <div><b>CERTIFICATES ON THE PAGE</b>Shown as paper, click to enlarge. Roll, registration and serial numbers, parents' names and date of birth are covered.</div>
      <div><b>COURSE MAP</b>All 70 courses, two terms per row, with the teachers (names open their KUET profile). Areas follow the IISE body of knowledge; open a course for its syllabus topics. CGPA only.</div>
      <div><b>THESIS, THEN PROJECTS</b>Only the thesis here: the face-blurred two-camera video plays on its own, with three figures from the paper. Other papers link to the Research page.</div>
    </div>
    <div class="dopt">{inner}</div>
  </main>
"""


def page(theme, title):
    html = H.page(theme, title)
    html = html.replace("<style>", "<style>" + EG.CSS + CSS + area_css(), 1)
    a = html.index("  <!-- Hero: static page backdrop")
    e = html.index("  </main>") + len("  </main>")
    html = html[:a] + body() + html[e:]
    return html


if __name__ == "__main__":
    out = "/home/claude/zaid/project"
    for key, name in [("dark", "EduPgProp"), ("dark_blue", "EduPgPropBlue"), ("dark_green", "EduPgPropGreen"),
                      ("light", "EduPgPropLight"), ("light_blue", "EduPgPropLightBlue"), ("light_green", "EduPgPropLightGreen"),
                      ("dark", "EduPgPropMobile")]:
        open(f"{out}/{name}.dc.html", "w").write(page(key, f"Education page detailed proposal · {name}"))
    print("education detail proposal written")
