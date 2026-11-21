#!/usr/bin/env python3
"""Project detail page: EV charging station (Energy Fest CAD competition, Dec 2024).
Proposal boards, all themes + phone. Facts come from the competition question PDF and the
team report (ESE Energy Fest1.docx) in his files"""
import build_home as H

IMG = {
    "hero": "/_blob/f20860bbff9c8bd3b26add9a1bff6e34", "front": "/_blob/b78791ef237bad8695e47345ca333ed6",
    "street": "/_blob/e20aa20d43dfab39dddf79f586cc1688", "bench": "/_blob/23e964d4427fd20bd01bb98b1c33c7b2",
    "solar": "/_blob/8edc8718f2993bf6820503c208e18f35", "panel": "/_blob/3297f6d849677231ad69b30e6ec42526",
    "sos": "/_blob/fc855c7234e5451cc0fb180dac487058", "cctv": "/_blob/0b8ddd2f5bf8e381a506ab4061d22f10",
    "wifi": "/_blob/2ed6aae08c8774780ab6bf4661be96f9", "cad": "/_blob/64ba91ac0d251c6e73c745e26501c96b",
    "tracker": "/_blob/804e78a3065b873bbc9ef497c28fcbad", "diode": "/_blob/e9d6134b1f3171969e202564cdfa416d",
    "drawing": "/_blob/f2686bd41f55b13691bb8d266aba836e", "ccs": "/_blob/6e742a8ec23b912c317302f2249edcee",
    "coffee": "/_blob/8ea8e36e07f8faa8fdb36da3b53d2c74",
    "question": "/_blob/7d384efb390fe9a83b69b59fc9ad572b",
    "turntable": "/_blob/7354b6d1f66aa17916ba6ea4471bf0c1",
}

_SV = '<svg viewBox="0 0 24 24" width="15" height="15" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{}</svg>'
ICO_ORBIT = _SV.format('<path d="M20 12a8 4 0 1 1-3-3.1"/><path d="M17 5v4h-4"/><circle cx="12" cy="12" r="1.6"/>')
ICO_PLUS = _SV.format('<circle cx="11" cy="11" r="6"/><path d="M11 8v6M8 11h6M20 20l-4.5-4.5"/>')
ICO_MINUS = _SV.format('<circle cx="11" cy="11" r="6"/><path d="M8 11h6M20 20l-4.5-4.5"/>')
ICO_FULL = _SV.format('<path d="M4 9V4h5M20 9V4h-5M4 15v5h5M20 15v5h-5"/>')
ICO_AR = _SV.format('<path d="M12 3 20 7.5v9L12 21l-8-4.5v-9Z M12 12l8-4.5 M12 12v9 M12 12 4 7.5"/>')


CSS = """
/* Hero 3D: a 72-frame turntable of the real assembly (600 x 480 frames, sprite 9 x 8) with a 3D MODEL | RENDER switch.
   Real site: Google model-viewer with the same GLB (orbit, zoom, full screen, AR). */
/* 3D stage in the hero: same frame as the render, model turns on its own */
.h3s{position:relative;border:1px solid var(--line2);border-radius:10px;overflow:hidden;aspect-ratio:5/4;
  background-color:var(--surface);background-image:linear-gradient(var(--line) 1px,transparent 1px),linear-gradient(90deg,var(--line) 1px,transparent 1px);background-size:30px 30px;background-position:center}
.h3s .tt3{position:absolute;inset:0;background-size:900% 800%;background-repeat:no-repeat;transition:opacity .35s ease;
  animation:h3x 1.8s steps(9,jump-none) infinite,h3y 14.4s steps(8,jump-none) infinite}
@keyframes h3x{from{background-position-x:0%}to{background-position-x:100%}}
@keyframes h3y{from{background-position-y:0%}to{background-position-y:100%}}
.h3s .rimg{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;opacity:0;transition:opacity .35s ease}
.h3s .h3b{position:absolute;right:12px;bottom:12px;display:flex;gap:6px;z-index:2;transition:opacity .3s ease}
.h3s .h3b i{display:inline-flex;width:30px;height:30px;align-items:center;justify-content:center;border:1px solid var(--line2);border-radius:8px;background:var(--surface);color:var(--muted);transition:color .25s ease,border-color .25s ease}
.h3s .h3b i:hover{color:var(--acc-t);border-color:var(--acc-t)}
.h3s .h3c{position:absolute;left:12px;bottom:12px;font:600 10.5px 'IBM Plex Mono',monospace;letter-spacing:.08em;color:var(--muted)}

/* A: view switch, 3D MODEL | RENDER (CSS radio, no JS) */
.h3w{position:relative}
.h3w > input{position:absolute;opacity:0;pointer-events:none}
.h3t{position:absolute;left:12px;top:12px;z-index:3;display:flex;padding:3px;gap:2px;border:1px solid var(--line2);border-radius:8px;background:var(--surface)}
.h3t label{font:600 10.5px 'IBM Plex Mono',monospace;letter-spacing:.1em;color:var(--muted);padding:6px 10px;border-radius:5px;cursor:pointer;white-space:nowrap;transition:color .25s ease,background .25s ease}
.h3t label:hover{color:var(--strong)}
.h3w .v1:checked ~ .h3t .l1,.h3w .v2:checked ~ .h3t .l2{background:var(--acc-soft);color:var(--acc-t)}
.h3w .v2:checked ~ .h3s .rimg{opacity:1}
.h3w .v2:checked ~ .h3s .tt3,.h3w .v2:checked ~ .h3s .h3b,.h3w .v2:checked ~ .h3s .h3c{opacity:0}

@media (max-width:760px){
  .h3t label{padding:5px 8px;font-size:10px}
  .h3s .h3b{right:8px;bottom:8px;gap:4px}.h3s .h3b i{width:28px;height:28px}
  .h3s .h3c{display:none}
  .h3w .h3s{aspect-ratio:1/1.1}
  .h3w .h3s .tt3{inset:42px 0 auto 0;aspect-ratio:5/4}
}
/* 05 model files: full width, two pairs per row on desktop */
.files.fw{grid-template-columns:150px minmax(0,1fr) 150px minmax(0,1fr);column-gap:0}
.files.fw>span:nth-child(4n+3){padding-left:28px}
.files.fw>span:nth-child(4n+2){padding-right:24px}
@media (max-width:960px){.files.fw{grid-template-columns:118px 1fr}.files.fw>span:nth-child(4n+3){padding-left:0}.files.fw>span:nth-child(4n+2){padding-right:0}}
@media (max-width:760px){.files.fw{grid-template-columns:100px 1fr}}

/* brief: summary + the attached question (calm) */
.qwrap{display:grid;grid-template-columns:1fr 250px;gap:16px;align-items:stretch}
.qdoc{display:flex;flex-direction:column;border:1px solid var(--line2);border-radius:10px;overflow:hidden;background:var(--surface2);transition:border-color .25s ease}
.qdoc .qim{display:block;height:170px;overflow:hidden;padding:8px 8px 0}
.qdoc .qim img{width:100%;display:block;border-radius:4px 4px 0 0;filter:brightness(.92);transition:transform .6s ease,filter .4s ease;transform-origin:top center}
.qdoc .qft{display:flex;align-items:center;gap:8px;padding:10px 12px;border-top:1px solid var(--line);font:600 10.5px 'IBM Plex Mono',monospace;letter-spacing:.1em;color:var(--muted)}
.qdoc .qft b{color:var(--strong);font-weight:600}
.qdoc .qft em{font-style:normal;flex:1;white-space:nowrap}
.qdoc .qft i{font-style:normal;transition:transform .25s ease}
.qdoc:hover{border-color:var(--strong)}
.qdoc:hover .qim img{filter:none;transform:scale(1.03)}
.qdoc:hover .qft{color:var(--acc-t)}
.qdoc:hover .qft i{transform:translate(2px,-2px)}
.qlinks{display:flex;gap:18px;margin-top:12px}
.qlinks a{font:600 11px 'IBM Plex Mono',monospace;letter-spacing:.1em;color:var(--muted);border-bottom:1px dotted var(--line2);padding-bottom:1px;transition:color .25s ease,border-color .25s ease}
.qlinks a:hover{color:var(--acc-t);border-bottom-color:var(--acc-t)}
.evcadfix .cv{background:var(--surface2);padding:8px}
.evcadfix .cv img{border-radius:5px;filter:brightness(.9) saturate(.88);transition:filter .4s ease}
.evcadfix .cv:hover img{filter:none}
@media (max-width:760px){.qwrap{grid-template-columns:1fr}.qdoc .qim{height:150px}}
.spec2 .evl{margin-left:6px;font:600 10.5px 'IBM Plex Mono',monospace;letter-spacing:.1em;color:var(--muted);border-bottom:1px dotted var(--line2);white-space:nowrap}
.spec2 .evl:hover{color:var(--acc-t);border-bottom-color:var(--acc-t)}

/* ===== EV project detail ===== */
.crumb{font:600 12.5px 'IBM Plex Mono',monospace;letter-spacing:.1em;color:var(--muted)}
.crumb a:hover{color:var(--acc-t)}
.evh{padding:44px 0 0}
.evh .pn{display:flex;flex-wrap:wrap;gap:8px 18px;margin-top:18px;font:600 12.5px 'IBM Plex Mono',monospace;letter-spacing:.08em;color:var(--muted)}
.evh .pn b{color:var(--acc-t);font-weight:600}
.evh .h1{font-size:44px;margin-top:10px;max-width:900px}   /* 44 -> 46 px after the type scale, the same as the section pages */
.evh .lead{margin-top:14px;max-width:780px;font-size:16.7px}   /* -> 18 px after the type scale */
.evhero{display:grid;grid-template-columns:minmax(0,1.6fr) minmax(0,1fr);gap:22px;margin-top:28px}
.evhero .im{position:relative;border:1px solid var(--line2);border-radius:10px;overflow:hidden;background:#15181E;aspect-ratio:5/4}
.evhero .im img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}
.evhero .im .cap2{position:absolute;left:12px;bottom:12px;font:600 11.5px 'IBM Plex Mono',monospace;letter-spacing:.08em;color:#fff;background:rgba(12,15,20,.72);padding:5px 9px;border-radius:5px}
.spec2{display:grid;grid-template-columns:118px 1fr;border-top:1px solid var(--line2);align-self:start}
.spec2>span{padding:10px 0;border-bottom:1px solid var(--line);font-size:14.5px;color:var(--strong)}
.spec2>span.k{font:600 12px 'IBM Plex Mono',monospace;letter-spacing:.1em;color:var(--muted);padding-top:12px}
.spec2 em{font-style:normal;color:var(--muted)}
.spec2 .ok{color:var(--strong)}
.evside{display:flex;flex-direction:column;gap:16px}
.evside .acts{display:flex;gap:10px;flex-wrap:wrap}
.sb2{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));border:1px solid var(--line2);border-radius:10px;overflow:hidden;background:var(--surface);backdrop-filter:var(--glass)}
.sb2>div{padding:14px 16px;border-left:1px solid var(--line)}
.sb2>div:first-child{border-left:0}
.sb2 b{display:block;font:600 22px 'IBM Plex Mono',monospace;color:var(--strong)}
.sb2 span{font-size:13px;color:var(--body)}
.qbox{padding:22px 24px;border:1px dashed var(--line2);border-radius:10px;background:var(--surface);backdrop-filter:var(--glass)}
.qbox .qh{font:600 12.5px 'IBM Plex Mono',monospace;letter-spacing:.1em;color:var(--acc-t)}
.qbox p{margin:10px 0 0;font-size:15.5px;line-height:1.65;color:var(--body);max-width:880px}
.rq{width:100%;border-collapse:collapse;margin-top:18px;border:1px solid var(--line2);background:var(--surface);backdrop-filter:var(--glass)}
.rq th{font:600 11.5px 'IBM Plex Mono',monospace;letter-spacing:.1em;color:var(--muted);text-align:left;padding:10px 14px;border-bottom:1px solid var(--line2)}
.rq td{padding:12px 14px;border-top:1px solid var(--line);font-size:14.5px;line-height:1.5;color:var(--text);vertical-align:top}
.rq td:first-child{font-weight:600;color:var(--strong);width:24%}
.rq td.t{font:500 13px 'IBM Plex Mono',monospace;color:var(--body);width:20%}
.feat3{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:18px}
.fgp{padding:20px;display:flex;flex-direction:column;gap:12px}
.fgp .n{font:600 12.5px 'IBM Plex Mono',monospace;letter-spacing:.1em;color:var(--muted)}
.fgp h3{margin:0;font:600 19px 'Space Grotesk',sans-serif;color:var(--strong)}
.fgp .ph3{border-radius:8px;overflow:hidden;aspect-ratio:5/4;background:#15181E}
.fgp .ph3 img{width:100%;height:100%;object-fit:cover;display:block}
.fgp ul{margin:0;padding:0;list-style:none;display:flex;flex-direction:column;gap:8px}
.fgp li{display:flex;gap:10px;font-size:14.5px;line-height:1.5;color:var(--body)}
.fgp li:before{content:"";flex:none;width:8px;height:1.5px;margin-top:11px;background:var(--muted)}
.fgp li b{color:var(--strong);font-weight:600}
.sol{display:grid;grid-template-columns:minmax(0,1.25fr) minmax(0,1fr);gap:22px;align-items:stretch}
.solfig{padding:16px 18px 12px}
.solfig .ft{font:600 12.5px 'IBM Plex Mono',monospace;letter-spacing:.1em;color:var(--acc-t)}
.solfig svg{display:block;width:100%;height:auto;margin-top:6px}
.solfig text{font:600 12px 'IBM Plex Mono',monospace;fill:var(--muted)}
.solfig .grd{stroke:var(--line2);stroke-width:1.2}
.solfig .arc{fill:none;stroke:var(--line2);stroke-dasharray:4 6}
.solfig .sun{fill:#F2B84B}
.solfig .ray{stroke:#F2B84B;stroke-opacity:.35;stroke-width:1.4;stroke-dasharray:5 6}
.solfig .pole{fill:var(--strong);fill-opacity:.55}
.solfig .pnl{fill:#2E4C78;stroke:#9DB8E0;stroke-width:1}
.solfig .cell{stroke:#9DB8E0;stroke-opacity:.45}
.solfig .dio{fill:#C77DDB}
.solfig .bar{fill:var(--acc)}
.solfig .barbg{fill:var(--line)}
.solfig .sv{fill:var(--strong);fill-opacity:.8}
.solfig .mv{transform-box:view-box}
.solfig .sunm{animation:sunMove 12s ease-in-out infinite}
.solfig .tilt{transform-origin:240px 196px;animation:tilt 12s ease-in-out infinite}
@keyframes sunMove{0%{transform:translate(-170px,70px)}50%{transform:translate(0,-10px)}100%{transform:translate(170px,70px)}}
@keyframes tilt{0%{transform:rotate(-38deg)}50%{transform:rotate(0deg)}100%{transform:rotate(38deg)}}
.solfig .bw{animation:bw 12s ease-in-out infinite;transform-origin:0 0}
.solfig .be{animation:be 12s ease-in-out infinite;transform-origin:0 0}
@keyframes be{0%{transform:scaleX(1)}50%{transform:scaleX(.55)}100%{transform:scaleX(.12)}}
@keyframes bw{0%{transform:scaleX(.12)}50%{transform:scaleX(.55)}100%{transform:scaleX(1)}}
.solfig .lbl{animation:lbl 12s steps(1) infinite}
@media (prefers-reduced-motion:reduce){.solfig *{animation:none!important}}
.soltx{padding:20px;display:flex;flex-direction:column;gap:12px}
.soltx p{margin:0;font-size:15px;line-height:1.6;color:var(--body)}
.soltx .pr{display:grid;grid-template-columns:1fr 1fr;gap:10px}
.soltx .pr figure{margin:0;border:1px solid var(--line);border-radius:8px;overflow:hidden;background:#fff}
.soltx .pr img{width:100%;height:120px;object-fit:cover;display:block}
.soltx .pr figcaption{font:600 11px 'IBM Plex Mono',monospace;letter-spacing:.06em;color:#3E4A5C;padding:6px 8px;background:#F4F5F7}
.gal{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));grid-auto-rows:180px;gap:12px}
.gal figure{margin:0;position:relative;border-radius:8px;overflow:hidden;border:1px solid var(--line);background:#15181E}
.gal figure.w2{grid-column:span 2;grid-row:span 2}
.gal img{width:100%;height:100%;object-fit:cover;display:block;filter:brightness(.9) saturate(.88);transition:transform .6s ease,filter .4s ease}
.gal figure:hover img{transform:scale(1.03);filter:none}
.gal figcaption{position:absolute;left:8px;bottom:8px;font:600 11px 'IBM Plex Mono',monospace;letter-spacing:.06em;color:#fff;background:rgba(12,15,20,.7);padding:4px 7px;border-radius:4px}
.cad2{display:grid;grid-template-columns:minmax(0,1.3fr) minmax(0,1fr);gap:22px}
.cad2 .cv{border:1px solid var(--line2);border-radius:10px;overflow:hidden;background:#EEF1F4}
.cad2 .cv img{width:100%;display:block}
.files{display:grid;grid-template-columns:118px 1fr;border-top:1px solid var(--line2)}
.files>span{padding:10px 0;border-bottom:1px solid var(--line);font-size:14px;color:var(--strong)}
.files>span.k{font:600 12px 'IBM Plex Mono',monospace;letter-spacing:.1em;color:var(--muted);padding-top:12px}
.nxt{display:grid;grid-template-columns:1fr 1fr;gap:16px;margin-top:8px}
.nxt a{padding:18px 20px;display:flex;flex-direction:column;gap:6px}
.nxt a .k{font:600 12px 'IBM Plex Mono',monospace;letter-spacing:.1em;color:var(--muted)}
.nxt a b{font:600 17px 'Space Grotesk',sans-serif;color:var(--strong)}
.nxt a:last-child{text-align:right}
.nxt a:hover b{color:var(--acc-t)}
@media (max-width:960px){.evhero,.sol,.cad2{grid-template-columns:1fr}.feat3{grid-template-columns:1fr 1fr}}
@media (max-width:760px){
  .zh .evh{padding-top:26px}
  .zh .evh .h1{font-size:28.6px!important}
  /* phone: stats 2 x 2, each cell = figure + one-line label; buttons stay side by side */
  .sb2{grid-template-columns:1fr 1fr}.sb2>div{padding:10px 12px;border-left:1px solid var(--line);border-top:1px solid var(--line)}
  .sb2>div:nth-child(odd){border-left:0}.sb2>div:nth-child(-n+2){border-top:0}
  .sb2 b{font-size:18px;line-height:1.2}.sb2 span{display:block;margin-top:2px;font-size:12px;white-space:nowrap}
  .evside .acts{flex-wrap:nowrap}.evside .acts .bkb{flex:1 1 auto;justify-content:center;padding:0 10px;letter-spacing:.06em;min-width:0}
  .sb2 b{font-size:18px}
  .feat3{grid-template-columns:1fr}
  .rq thead{display:none}.rq,.rq tbody,.rq tr,.rq td{display:block;width:auto!important}
  .rq tr{padding:12px 14px;border-top:1px solid var(--line)}.rq td{border:0;padding:2px 0}
  .rq td.t{margin-bottom:4px}
  .gal{grid-template-columns:1fr 1fr;grid-auto-rows:130px}
  /* phone: previous and next stay side by side on one line */
  .nxt{grid-template-columns:1fr 1fr;gap:10px}.nxt a{padding:12px 14px;gap:4px}.nxt a .k{font-size:10px;letter-spacing:.06em}.nxt a b{font-size:14.5px;line-height:1.3}.nxt a .pn{display:none}
  .spec2,.files{grid-template-columns:100px 1fr}
  .spec2>span.k,.files>span.k{font-size:11px}
  .qbox p{font-size:14px}
  .soltx .pr img{height:96px}
  .solfig text{font-size:19px}
}
"""


def solar_svg():
    """Auto-running sketch of the sun-tracking panel: sun moves east to west, panel follows,
    the two photodiode readings swap. Simplified, not to scale."""
    cells = "".join(f'<line class="cell" x1="{x}" y1="186" x2="{x}" y2="196"/>' for x in range(170, 311, 20))
    return f'''<svg viewBox="0 0 480 300" role="img" aria-label="Sun-tracking solar panel: the panel turns to follow the sun from east to west">
      <path class="arc" d="M70 200 Q240 -40 410 200"/>
      <g class="mv sunm"><circle class="sun" cx="240" cy="90" r="16"/></g>
      <text x="40" y="220">EAST</text><text x="400" y="220">WEST</text>
      <line class="grd" x1="20" y1="282" x2="460" y2="282"/>
      <rect class="pole" x="233" y="200" width="14" height="82"/>
      <rect class="sv" x="226" y="196" width="28" height="14" rx="2"/>
      <g class="tilt">
        <rect class="pnl" x="160" y="186" width="160" height="10" rx="1"/>{cells}
        <rect class="dio" x="164" y="180" width="8" height="6"/><rect class="dio" x="308" y="180" width="8" height="6"/>
      </g>
      <text x="20" y="40">BPW34 · EAST</text>
      <rect class="barbg" x="20" y="48" width="120" height="8" rx="2"/><rect class="bar be" x="20" y="48" width="120" height="8" rx="2"/>
      <text x="340" y="40">BPW34 · WEST</text>
      <rect class="barbg" x="340" y="48" width="120" height="8" rx="2"/><rect class="bar bw" x="340" y="48" width="120" height="8" rx="2"/>
      <text x="196" y="300">SERVO</text>
    </svg>'''


def body():
    i = IMG
    rq = [
        ("Compact footprint", "≤ 1 m × 0.8 m base", "Charger body sized from a standard commercial DC charger (700 × 240 mm), with the bench, coffee unit and canopy built around it."),
        ("Charging", "≥ 2 EVs at once, managed cables", "DC fast charging through CCS guns on both sides; each gun parks in its own holder so cables stay off the pavement."),
        ("Modular, scalable", "add features without replacing", "Solar canopy, coffee unit, humidifier and CCTV are separate assemblies that bolt on to the charger body."),
        ("Weatherproof", "rain, heat, dust", "Roof canopy over the user side, weather-resistant bench, rear ventilation to cool the charger."),
        ("Bonus: renewable energy", "use solar effectively", "Sun-tracking solar panel (BPW34 photodiodes and a servo) charging a 300 Wh battery."),
    ]
    rq_rows = "".join(f"<tr><td>{a}</td><td class='t'>{b}</td><td>{c}</td></tr>" for a, b, c in rq)
    gal = [("hero", "Station on the street", "w2"), ("street", "With a parked EV", ""), ("front", "Front three-quarter", ""),
           ("bench", "Bench and coffee unit", ""), ("panel", "Customer screen and ports", ""), ("cctv", "CCTV, 360° IR", ""), ("sos", "Emergency SOS", ""),
           ("wifi", "Wi-Fi QR", ""), ("solar", "Solar canopy", "")]
    gal_html = "".join(f'<figure class="{c}"><img src="{i[k]}" alt="{t} · KeyShot render"><figcaption>{t}</figcaption></figure>' for k, t, c in gal)
    return f"""
  <main class="wrap" style="position:relative;z-index:1">
    <section class="evh">
      <div class="crumb"><a href="#">HOME</a> / <a href="#">PROJECTS</a> / EV CHARGING STATION</div>
      <div class="pn"><span>PART NO. <b>MZH-P-003</b></span><span>COMPETITION</span><span>ENERGY FEST 1.0 · CAD COMPETITION</span><span>DEC 2024</span></div>
      <h1 class="h1">Multi-purpose EV charging station for urban streets</h1>
      <p class="lead">A compact DC fast-charging point for street-side parking in Dhaka that also gives the street a bench, shade, solar power, Wi-Fi, tea and a safety point. Designed in SOLIDWORKS and rendered in KeyShot by team Isometric Illuminators 4.0, which I led.</p>
      <div class="evhero">
        <div class="h3w"><input type="radio" class="v1" name="hv" id="hv1" checked><input type="radio" class="v2" name="hv" id="hv2">
          <div class="h3t"><label class="l1" for="hv1">3D MODEL</label><label class="l2" for="hv2">RENDER</label></div>
          <div class="h3s" role="img" aria-label="3D model of the EV charging station turning slowly"><span class="tt3" style="background-image:url({i['turntable']})"></span>
            <img class="rimg" src="{i['hero']}" alt="EV charging station with solar canopy, bench and coffee unit, KeyShot render">
            <span class="h3c">FIG. 01 · 3D MODEL · GLB 0.9 MB</span>
            <span class="h3b"><i title="Turn">{ICO_ORBIT}</i><i title="Zoom in">{ICO_PLUS}</i><i title="Zoom out">{ICO_MINUS}</i><i title="Full screen">{ICO_FULL}</i><i title="View in your room (AR)">{ICO_AR}</i></span></div></div>
        <div class="evside">
          <div class="spec2">
            <span class="k">EVENT</span><span>Energy Fest 1.0 · CAD competition <em>· Dept. of ESE, KUET</em> <a class="evl" href="https://www.facebook.com/profile.php?id=61567715310601" target="_blank" rel="noopener">EVENT PAGE ↗</a></span>
            <span class="k">TEAM</span><span>Isometric Illuminators 4.0</span>
            <span class="k">MY ROLE</span><span>Team lead <em>· planned the work, split tasks across the team, broke the brief into sub-problems</em></span>
            <span class="k">DATE</span><span>Dec 2024</span>
            <span class="k">SOFTWARE</span><span>SOLIDWORKS · KeyShot</span>
            <span class="k">OUTPUT</span><span>Parts, assemblies, drawing, STEP and IGS files, renders, feature report</span>
            <span class="k">RESULT</span><span class="ok">Top 20 finalist <em>· selection round, advanced to the final round · 13 Dec 2024</em> <a class="evl" href="https://www.facebook.com/share/p/1a1m7p9byG/" target="_blank" rel="noopener">RESULT POST ↗</a></span>
          </div>
          <div class="acts"><a class="bkb" href="#model"><s></s><s></s><s></s><s></s><span>MODEL FILES</span><i>↓</i></a><a class="bkb" href="#"><s></s><s></s><s></s><s></s><span>FEATURE REPORT</span><i>↓</i></a></div>
        </div>
      </div>
      <div class="sb2" style="margin-top:22px">
        <div><b>2</b><span>CCS fast-charge guns</span></div>
        <div><b>300 Wh</b><span>solar battery</span></div>
        <div><b>3</b><span>pay by QR, cash, card</span></div>
        <div><b>360°</b><span>CCTV, IR night vision</span></div>
      </div>
    </section>

    <section class="sec" aria-labelledby="s-brief">
      <div class="sh"><div class="eb"><span class="ebn">01</span><span class="ebt">THE BRIEF</span><span class="ebl"></span></div>
        <div class="shr"><h2 class="h2" id="s-brief">The question we were given</h2></div></div>
      <div class="qwrap"><div class="qbox"><div class="qh">SELECTION-ROUND QUESTION · SUMMARY</div>
        <p>Street-side parking in dense cities like Dhaka has little space, and a bulky charger blocks pedestrians while adding nothing else. Design a compact, multi-purpose EV charging station that charges at least two cars, manages its cables, can be extended later, survives rain, heat and dust, blends into the street, and ideally runs on renewable energy.</p></div>
        <a class="qdoc" href="#" title="Selection-round question (PDF, 2 pages)"><span class="qim"><img src="{i['question']}" alt="First page of the Energy Fest 1.0 CAD competition selection-round question"></span>
          <span class="qft"><b>THE QUESTION</b><em>PDF · 2 PAGES</em><i>↗</i></span></a></div>
      <div class="qlinks"><a href="#">RULEBOOK · PDF ↗</a><a href="https://www.facebook.com/profile.php?id=61567715310601" target="_blank" rel="noopener">EVENT PAGE ↗</a><a href="https://www.facebook.com/share/p/1a1m7p9byG/" target="_blank" rel="noopener">RESULT POST ↗</a></div>
      <table class="rq"><thead><tr><th>REQUIREMENT</th><th>TARGET</th><th>OUR ANSWER</th></tr></thead><tbody>{rq_rows}</tbody></table>
    </section>

    <section class="sec" aria-labelledby="s-feat">
      <div class="sh"><div class="eb"><span class="ebn">02</span><span class="ebt">FEATURES</span><span class="ebl"></span></div>
        <div class="shr"><h2 class="h2" id="s-feat">What the station does</h2></div></div>
      <div class="feat3">
        <article class="card fgp"><div class="n">CORE</div><h3>Charging and the street</h3>
          <div class="ph3"><img src="{i['panel']}" alt="Customer screen and charging indicators"></div>
          <ul><li><span><b>CCS fast charging</b>, AC and DC in one port; about 30 min for a fast charge.</span></li>
          <li><span><b>Customer screen</b>: payment, ads, coffee choice, FAQs, and lights for power, charging and faults.</span></li>
          <li><span><b>Bench</b>, mobile charging ports and a <b>Wi-Fi hotspot</b> while the car charges.</span></li></ul></article>
        <article class="card fgp"><div class="n">COMFORT</div><h3>For people waiting</h3>
          <div class="ph3"><img src="{i['bench']}" alt="Bench with tea-coffee maker and humidifier"></div>
          <ul><li><span><b>Tea-coffee maker</b> running on the station's solar energy.</span></li>
          <li><span><b>Mist humidifier</b> for Bangladesh's hot weather.</span></li>
          <li><span><b>Advertisement screen</b> for promotions, events and public alerts.</span></li></ul></article>
        <article class="card fgp"><div class="n">SAFETY AND PAYMENT</div><h3>Safe and easy to pay</h3>
          <div class="ph3"><img src="{i['sos']}" alt="Emergency SOS button"></div>
          <ul><li><span><b>CCTV</b> with 360° view and IR night vision, <b>SOS button</b>, heat monitoring, fire-extinguisher ball, audible alerts.</span></li>
          <li><span>Pay by <b>QR</b> (mobile banking), <b>cash</b> in and out, or <b>debit, credit or fuel card</b>.</span></li></ul></article>
      </div>
    </section>

    <section class="sec" aria-labelledby="s-solar">
      <div class="sh"><div class="eb"><span class="ebn">03</span><span class="ebt">SOLAR TRACKING</span><span class="ebl"></span></div>
        <div class="shr"><h2 class="h2" id="s-solar">A panel that follows the sun</h2></div></div>
      <div class="sol">
        <div class="card solfig"><div class="ft">FIG. E1 · SUN-TRACKING PANEL</div>{solar_svg()}</div>
        <div class="card soltx">
          <p>Two <b>BPW34 photodiodes</b> on the panel measure light. A <b>servo</b> turns the panel toward the brighter side: east in the morning, west in the afternoon. Extra energy is stored in a <b>300 Wh battery</b> that runs the screens, lights and coffee unit.</p>
          <div class="pr"><figure><img src="{i['tracker']}" alt="Tracker mechanism inside the canopy"><figcaption>TRACKER GEAR AND SERVO</figcaption></figure>
          <figure><img src="{i['diode']}" alt="BPW34 photodiode on the panel"><figcaption>BPW34 PHOTODIODE</figcaption></figure></div>
        </div>
      </div>
    </section>

    <section class="sec" aria-labelledby="s-gal">
      <div class="sh"><div class="eb"><span class="ebn">04</span><span class="ebt">RENDERS</span><span class="ebl"></span></div>
        <div class="shr"><h2 class="h2" id="s-gal">KeyShot renders</h2></div></div>
      <div class="gal">{gal_html}</div>
    </section>

    <section class="sec" id="model" aria-labelledby="s-cad">
      <div class="sh"><div class="eb"><span class="ebn">05</span><span class="ebt">MODEL FILES</span><span class="ebl"></span></div>
        <div class="shr"><h2 class="h2" id="s-cad">What was delivered</h2></div></div>
      <div class="files fw">
        <span class="k">MAIN ASSY</span><span>1 EV Charging Station.SLDASM</span>
        <span class="k">DRAWING</span><span>1 EV Charging Station.SLDDRW</span>
        <span class="k">SUB-ASSY</span><span>Solar (tracker), coffee maker, humidifier, CCTV</span>
        <span class="k">KEY PARTS</span><span>CCS type 1 gun and holder, seating, roof, Wi-Fi unit, panel, battery, circuit</span>
        <span class="k">EXCHANGE</span><span>STEP · IGS for every part</span>
        <span class="k">WEB MODEL</span><span>GLB · 0.9 MB · 38 parts</span>
        <span class="k">RENDERS</span><span>KeyShot · 9 views (04 Renders)</span>
        <span class="k">REPORT</span><span>Feature justification (≤ 500 words)</span>
      </div>
    </section>

    <section class="sec" style="padding-top:56px">
      <div class="nxt">
        <a class="card" href="#"><span class="k">← PREVIOUS<span class="pn"> · MZH-P-002</span></span><b>Distillation Plant</b></a>
        <a class="card" href="#"><span class="k">NEXT<span class="pn"> · MZH-P-004</span> →</span><b>Lathe Head-stock Gearbox</b></a>
      </div>
    </section>
  </main>
"""


def ev_page(theme, title):
    html = H.page(theme, title)
    html = html.replace("<style>", "<style>" + CSS, 1)
    a = html.index("  <!-- Hero: static page backdrop")
    b = html.index("  </main>") + len("  </main>")
    html = html[:a] + body() + html[b:]
    return html.replace('<a href="#">Projects</a>', '<a href="#" class="on" aria-current="page">Projects</a>', 1)


if __name__ == "__main__":
    import type_scale as TS
    out = __import__("os").environ.get("PORTFOLIO_OUT", "/home/claude/zaid/project")
    for key, name in [("dark", "EvProp"), ("dark_blue", "EvPropBlue"), ("dark_green", "EvPropGreen"),
                      ("light", "EvPropLight"), ("light_blue", "EvPropLightBlue"), ("light_green", "EvPropLightGreen")]:
        open(f"{out}/{name}.dc.html", "w").write(TS.apply(ev_page(key, f"EV project · {key}")))
    open(f"{out}/EvPropMobile.dc.html", "w").write(TS.apply(ev_page("dark", "EV project · Mobile")))
    print("ev written")
