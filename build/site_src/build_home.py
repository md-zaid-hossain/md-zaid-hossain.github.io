#!/usr/bin/env python3
"""Generates the homepage mockup artboards (Light, Dark, Mobile) for the
Design canvas from one shared template, so all three stay in sync.
Review round 1 (2026-11-13) fixes are applied here."""
import re

import os as _os
SCR = _os.path.dirname(_os.path.abspath(__file__))
NAV_SRC = open(f"{SCR}/plnav.html").read()

import home_parts as HP
import edu_gantt as EG
import exp_list as XL
import res_list as RL
import skill_cards as SKC
from home_parts import THEMES, backdrop, gear3d, BACKDROP_CSS, GEAR3D_CSS

HP.G3D_ASSETS.update({
    'g1-top': '/_blob/931032c4e17049db3ce42629f5a674ea', 'g1-side-d': '/_blob/bb730d4ba85939bb85bd410e4cefa0f0',
    'g1-side-m': '/_blob/82883e437e75dee0c0fce71470fbd3c4', 'g1-side-l': '/_blob/f9647d9b376ca737061ef369282bb51a',
    'g1-shaft': '/_blob/b8d98af9939a45535c65bee0f452d9aa', 'g2-top': '/_blob/b15bbbea01866cf49f3a2942832c7bbe',
    'g2-side-d': '/_blob/d5cd6d0c47b42af590279d715cf06b3e', 'g2-side-m': '/_blob/b9a0ad4b9fcec840fc0683a9fafaa083',
    'g2-side-l': '/_blob/ee852859dd18ee43a7b13c42c3ca04c3', 'g2-shaft': '/_blob/15e94dbec980f29632a298030339ede5',
})

CSS = r"""
body{margin:0;background:var(--bg)}
.zh{VARS;position:relative;height:100vh;background:var(--bg);color:var(--text);font-family:'Inter',system-ui,sans-serif;-webkit-font-smoothing:antialiased;overflow:hidden}
.zh *{box-sizing:border-box}
.zh a{color:inherit;text-decoration:none}
.zh a:focus-visible,.zh button:focus-visible{outline:2px solid var(--acc-t);outline-offset:3px;border-radius:6px}
.mono{font-family:'IBM Plex Mono',monospace}
.head{font-family:'Space Grotesk',system-ui,sans-serif}
.wrap{max-width:1200px;margin:0 auto;padding:0 24px}

/* header */
.hdr{position:sticky;top:0;z-index:20;border-bottom:1px solid var(--line);background:var(--header);backdrop-filter:blur(8px)}
.hdr .wrap{height:72px;display:flex;align-items:center;justify-content:space-between;gap:24px}
.brand{display:flex;align-items:center;gap:10px;min-width:0}
.brand b{white-space:nowrap;min-width:0}
/* the ZH mark keeps the same size on every screen */
.brand i{flex:none;width:34px;height:34px;border:1.5px solid var(--strong);border-radius:6px;display:flex;align-items:center;justify-content:center;font:600 14px 'IBM Plex Mono',monospace;font-style:normal;color:var(--strong)}
.brand b{font:600 16px 'Space Grotesk',sans-serif;color:var(--strong)}
/* review fixes 2026-11-20: small phones */
@media (max-width:389px){.zh .brand b{display:none}}
@media (max-width:400px){.rev .rvp{display:none}}
@media (max-width:380px){.zh .est span,.zh .etm span,.zh .sb2 span{white-space:normal}.zh .etm b{white-space:nowrap}}
@media (max-width:340px){.zh .etm b{font-size:.8rem}.zh .etm div{padding:8px 7px}}
.nav{display:flex;gap:30px}
.nav a{font-size:14px;font-weight:500;color:var(--body);padding:6px 0;border-bottom:2px solid transparent;transition:color .2s,border-color .2s}
.nav a:hover{color:var(--strong);border-bottom-color:var(--acc)}
.nav a.on{color:var(--strong);border-bottom-color:var(--acc)}
.hact{display:flex;align-items:center;gap:12px}
.cvbtn{display:inline-flex;align-items:center;gap:7px;height:36px;padding:0 14px;border:1px solid var(--line2);border-radius:8px;font-size:13px;font-weight:600;color:var(--strong)}
.cvbtn:hover{border-color:var(--acc);color:var(--acc-t)}
.tog{display:flex;align-items:center;gap:4px;border:1px solid var(--line2);border-radius:999px;padding:4px;background:var(--surface)}
.tog button{width:28px;height:28px;border:0;border-radius:999px;display:flex;align-items:center;justify-content:center;background:transparent;color:var(--muted);cursor:pointer;transition:color .2s,background .2s}
.tog button:hover{color:var(--strong)}
.tog button.on{background:var(--tog-on);color:var(--tog-on-ic)}
/* accent colour picker = H lamp slider (Zaid 2026-11-18): three lens segments + a metal ring that slides;
   the chosen lens is lit and breathes softly. Real site: clicking a lens sets the accent and is remembered. */
.sw{position:relative;box-sizing:border-box;width:var(--sw-w,102px);height:var(--sw-h,38px);border:1px solid var(--line2);border-radius:999px;background:var(--surface)}
.sw .tr{position:absolute;left:12px;right:12px;top:12px;height:12px;display:flex;gap:2px;border-radius:3px;background:var(--line2);box-shadow:inset 0 0 0 1px rgba(0,0,0,.18)}
.sw button{flex:1;padding:0;border:0;cursor:pointer;border-radius:2px;background:linear-gradient(180deg,rgba(255,255,255,.35),rgba(255,255,255,0) 45%,rgba(0,0,0,.2)),var(--c);
  opacity:.5;filter:saturate(.85);transition:opacity .3s,filter .3s,box-shadow .3s}
.sw button:hover{opacity:.85}
.sw button.on{opacity:1;filter:brightness(1.15) saturate(1.1);animation:swp 2.4s ease-in-out infinite}
@keyframes swp{0%,100%{box-shadow:0 0 4px 1px var(--cg)}50%{box-shadow:0 0 10px 3px var(--cg)}}
.sw .rg{position:absolute;left:calc(12px + (var(--sw-w,102px) - 26px) / 6 - 12px);top:6px;width:24px;height:24px;border-radius:50%;pointer-events:none;
  background:radial-gradient(circle,transparent 7.5px,#5d636a 8px,#d9dde1 9.5px,#8d939a 11px,#4c5157 12px);
  box-shadow:0 1px 3px rgba(0,0,0,.5);transition:transform .45s cubic-bezier(.3,1.35,.5,1)}
.sw.at-b .rg{transform:translateX(calc((var(--sw-w,102px) - 26px + 2px) / 3))}
.sw.at-g .rg{transform:translateX(calc((var(--sw-w,102px) - 26px + 2px) * 2 / 3))}
/* header controls, approved by Zaid 2026-11-20 (R6 + T1): colour picker = slim colour bar over a ruler of
   fine ticks with a line-drawn pinion (14 teeth, 24 px) whose hub shows the chosen colour; theme toggle =
   the same pinion ringing the chosen icon, icon in the accent colour. Both pinions turn slowly at different speeds (picker 22 s per
   turn, toggle 32 s the other way; faster on hover) and roll to a new choice; motion stops for visitors who switch it off. */
.sw,.tog{border-color:color-mix(in srgb,var(--line2) 75%,transparent);
  box-shadow:inset 0 1px 0 rgba(255,255,255,.06),0 1px 2px rgba(0,0,0,.08),0 6px 14px rgba(0,0,0,.07)}
.sw .tr{top:15px;height:6px;gap:4px;background:transparent;box-shadow:none}
.sw .tr:after{content:"";position:absolute;left:0;right:0;bottom:-6px;height:3px;background:repeating-linear-gradient(90deg,var(--line2) 0 1px,transparent 1px 5px)}
.sw button{opacity:.5;filter:none;border-radius:999px;background:var(--c)}
.sw button:hover{opacity:.85;filter:none}
.sw button.on{opacity:1;filter:none;animation:none;box-shadow:none;background:transparent}
.sw .rg{width:24px;height:24px;top:7px;left:calc(12px + (var(--sw-w,102px) - 26px) / 6 - 12px);background:none;box-shadow:none;
  transform:translateX(0) rotate(0deg);transition:transform 1s cubic-bezier(.3,1,.4,1)}
.sw.at-b .rg{transform:translateX(calc((var(--sw-w,102px) - 26px + 2px) / 3)) rotate(130deg)}
.sw.at-g .rg{transform:translateX(calc((var(--sw-w,102px) - 26px + 2px) * 2 / 3)) rotate(260deg)}
.sw .rg svg,.tgk svg{display:block;width:24px;height:24px;animation:hgspin 22s linear infinite;transform-origin:50% 50%}
.tgk svg{animation-duration:32s;animation-direction:reverse}
.sw:hover .rg svg{animation-duration:9s}
.tog:hover .tgk svg{animation-duration:13s}
@keyframes hgspin{to{transform:rotate(360deg)}}
.sw .rg .gt,.tgk .gt{fill:var(--surface);stroke:var(--strong);stroke-width:1;stroke-linejoin:round;opacity:.85}
.sw .rg .gr,.tgk .gr{fill:none;stroke:var(--muted);stroke-width:.8}
.sw .rg .gh{fill:var(--zgh)}
.sw.at-r{--zgh:#C14B3C}.sw.at-b{--zgh:#2F6BD8}.sw.at-g{--zgh:#1E7F55}
.tog{position:relative}
.tog button{position:relative;z-index:2}
.tog button.on{background:transparent;box-shadow:none;color:var(--acc-t)}
.tog button svg{width:16px;height:16px;transition:transform .5s cubic-bezier(.3,1.2,.5,1),color .3s ease}
.tog button.on svg{width:16px;height:16px;transform:scale(.69)}
.tog button.on[title^="Dark"] svg{transform:scale(.69) translate(.43px,-.73px)}
.tog button.on[title^="Auto"] svg{transform:scale(.69) translate(-.55px,.52px)}
.tog button.on[title^="Light"] svg{transform:scale(.69) translate(.17px,.54px)}
.tog button svg :is(circle,rect,path){fill:transparent;transition:fill .35s ease}
.tog button.on svg :is(circle,rect,path){fill:currentColor}
.tog button:focus-visible{border-radius:999px;outline-offset:1px}
.tgk .gr{opacity:.45}
.tgk{position:absolute;z-index:1;left:6px;top:6px;width:24px;height:24px;pointer-events:none;transition:transform 1s cubic-bezier(.3,1,.4,1)}
.tog.at-d .tgk{transform:translateX(32px) rotate(150deg)}
.tog.at-a .tgk{transform:translateX(64px) rotate(300deg)}
.tgk .gd{display:none}
@media (prefers-reduced-motion:reduce){.sw .rg svg,.tgk svg{animation:none}.sw .rg,.tgk,.tog button svg,.tog button svg *{transition:none}}
@media (max-width:1120px){.nav{gap:22px}}
@media (max-width:960px){.nav,.cvbtn{display:none}.menu{display:flex}}
.menu{display:none;width:40px;height:40px;border:1px solid var(--line2);border-radius:8px;background:transparent;align-items:center;justify-content:center;cursor:pointer}

/* hero: static page backdrop shows through; right column = live gear figure */
.hero{position:relative}
.hin{position:relative;z-index:2;padding:88px 0 72px;display:grid;grid-template-columns:minmax(0,1fr) 440px;gap:48px;align-items:center}
.hc{display:flex;flex-direction:column;align-items:flex-start;gap:26px;min-width:0}
.hfig{position:relative}
.rev{position:relative;padding:8px 14px;font:500 12px 'IBM Plex Mono',monospace;letter-spacing:.08em;color:var(--muted)}
.rev s{position:absolute;width:14px;height:14px;border:0 solid var(--acc)}
.rev s:nth-child(1){top:0;left:0;border-top-width:2px;border-left-width:2px}
.rev s:nth-child(2){top:0;right:0;border-top-width:2px;border-right-width:2px}
.rev s:nth-child(3){bottom:0;left:0;border-bottom-width:2px;border-left-width:2px}
.rev s:nth-child(4){bottom:0;right:0;border-bottom-width:2px;border-right-width:2px}
.h1{margin:0;font:700 64px/1.02 'Space Grotesk',sans-serif;letter-spacing:-.02em;color:var(--strong)}
.lead{margin:0;font-size:21px;line-height:1.5;color:var(--body);max-width:640px}
.lead b{font-weight:600;color:var(--strong)}
.focus{display:flex;flex-wrap:wrap;gap:8px 22px;margin:0;padding:0;list-style:none}
.focus li{display:flex;align-items:center;gap:9px;font-size:15px;font-weight:500;color:var(--strong)}
.focus li:before{content:"";width:7px;height:7px;background:var(--acc);transform:rotate(45deg)}
.now{display:flex;align-items:center;flex-wrap:wrap;gap:10px 12px;padding:12px 16px;border:1px solid var(--line);border-left:3px solid var(--acc);border-radius:8px;background:var(--surface);backdrop-filter:var(--glass)}
.now .k{font:600 12px 'IBM Plex Mono',monospace;letter-spacing:.1em;color:var(--acc-t)}
.now .v{font-size:15px;color:var(--strong)}
.now .v em{font-style:normal;color:var(--muted)}
.pills{display:flex;gap:10px;flex-wrap:wrap}
.pill{font:500 12.5px 'IBM Plex Mono',monospace;border:1px solid var(--line2);border-radius:6px;padding:6px 12px;color:var(--text);background:var(--surface2)}
.ctas{display:flex;gap:12px;flex-wrap:wrap;margin-top:4px}
.btn{display:inline-flex;align-items:center;justify-content:center;gap:8px;height:46px;padding:0 20px;border-radius:8px;font-size:15px;font-weight:600;border:1px solid var(--line2);color:var(--strong);background:var(--surface);transition:border-color .2s,color .2s,background .2s}
.btn:hover{border-color:var(--acc);color:var(--acc-t)}
.btn.p{background:var(--acc);border-color:var(--acc);color:var(--on-acc)}
.btn.p:hover{color:#fff;filter:brightness(1.08)}
@keyframes tsPulse{0%{box-shadow:0 0 0 0 var(--acc-glow)}70%{box-shadow:0 0 0 7px transparent}100%{box-shadow:0 0 0 0 transparent}}
.dot{display:inline-block;width:8px;height:8px;border-radius:999px;background:var(--acc);animation:tsPulse 2s infinite;flex:none}
/* logo strip (compact) */
.pl{--ls:1;display:grid;grid-template-columns:repeat(6,minmax(0,1fr));background:var(--surface);backdrop-filter:var(--glass);border:1px solid var(--line);border-radius:10px;overflow:hidden;margin:40px 0 0}
.plc{display:flex;flex-direction:column;align-items:center;justify-content:center;gap:12px;padding:22px 10px 18px;background:transparent;box-shadow:-1px 0 0 var(--line),0 -1px 0 var(--line);color:var(--logo);transition:color .2s,background .2s}
.plc svg{display:block;width:auto;fill:currentColor}
.plg{height:40px;display:flex;align-items:center;justify-content:center}
.pll{font:600 12px 'IBM Plex Mono',monospace;letter-spacing:.14em;color:var(--muted);transition:color .2s}
.plc:hover{color:var(--acc-t);background:var(--surface2)}
.plc:hover .pll{color:var(--strong)}

/* stats */
.stats{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));background:var(--surface);backdrop-filter:var(--glass);border:1px solid var(--line);border-radius:10px;overflow:hidden;margin-top:24px}
.st{position:relative;display:block;background:transparent;box-shadow:-1px 0 0 var(--line),0 -1px 0 var(--line);padding:24px 24px 22px;transition:background .2s}
.st .n{font:600 40px/1 'IBM Plex Mono',monospace;color:var(--acc-t)}
.st .l{font:600 13px 'IBM Plex Mono',monospace;letter-spacing:.06em;color:var(--strong);margin-top:12px}
.st .s{font-size:14px;color:var(--muted);margin-top:6px}
.st .ar{position:absolute;top:22px;right:22px;font-size:18px;color:var(--muted);transition:transform .2s,color .2s}
.st:hover{background:var(--surface2)}
.st:hover .ar{color:var(--acc-t);transform:translateX(3px)}

/* sections */
.sec{position:relative;padding-top:104px}
.sh{margin-bottom:28px}
.shr{display:flex;align-items:flex-end;justify-content:space-between;gap:16px;flex-wrap:wrap}
.eb{display:flex;align-items:center;gap:12px;margin-bottom:16px}
.ebn{font:700 15px/1 'IBM Plex Mono',monospace;color:var(--on-acc);background:var(--acc);padding:7px 10px;border-radius:5px}
.ebt{font:700 15px/1 'IBM Plex Mono',monospace;letter-spacing:.18em;color:var(--strong)}
.ebl{flex:1;min-width:40px;height:1px;background:linear-gradient(90deg,var(--line2),transparent)}
.h2{margin:0;font:600 32px/1.15 'Space Grotesk',sans-serif;letter-spacing:-.01em;color:var(--strong)}
.more{font-size:14px;font-weight:600;color:var(--acc-t);border-bottom:1px solid currentColor;padding-bottom:2px}
.card{background:var(--surface);backdrop-filter:var(--glass);border:1px solid var(--line);border-radius:10px}

/* research */
.pubs{display:flex;flex-direction:column}
.pub{display:grid;grid-template-columns:76px 1fr auto;gap:24px;align-items:start;padding:24px;border-bottom:1px solid var(--line)}
.pub:last-child{border-bottom:none}
.pub .yr{font:600 15px 'IBM Plex Mono',monospace;color:var(--muted);padding-top:2px}
.bdg{display:flex;gap:8px;flex-wrap:wrap;margin-bottom:10px}
.bd{font:600 11.5px 'IBM Plex Mono',monospace;letter-spacing:.08em;padding:3px 8px;border-radius:4px;border:1px solid var(--line2);color:var(--muted)}
.bd.a{border-color:var(--acc);color:var(--acc-t);background:var(--acc-soft)}
.pub h3{margin:0 0 8px;font:600 18px/1.4 'Space Grotesk',sans-serif;color:var(--strong)}
.pub .vn{font-size:14px;color:var(--muted);line-height:1.5}
.pub .vn b{font-weight:600;color:var(--body)}
.lk{display:flex;gap:8px}
.lk a{font:600 12px 'IBM Plex Mono',monospace;letter-spacing:.06em;padding:7px 10px;border:1px solid var(--line2);border-radius:6px;color:var(--text);white-space:nowrap}
.lk a:hover{border-color:var(--acc);color:var(--acc-t)}
.pubfoot{padding:16px 24px;border-top:1px dashed var(--line2);font-size:14px;color:var(--muted);display:flex;align-items:center;gap:10px;flex-wrap:wrap}
.pubfoot b{font-weight:600;color:var(--body)}

/* projects */
.pgrid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:20px}
.pc{overflow:hidden;display:flex;flex-direction:column;transition:border-color .2s,transform .2s}
.pc:hover{border-color:var(--acc);transform:translateY(-2px)}
.th{position:relative;height:200px;border-bottom:1px solid var(--line);background-image:linear-gradient(var(--hatch) 1px,transparent 1px),linear-gradient(90deg,var(--hatch) 1px,transparent 1px);background-size:16px 16px;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:6px}
.th s{position:absolute;width:12px;height:12px;border:0 solid var(--muted);opacity:.6}
.th s:nth-child(1){top:12px;left:12px;border-top-width:2px;border-left-width:2px}
.th s:nth-child(2){bottom:12px;right:12px;border-bottom-width:2px;border-right-width:2px}
.th span{font:500 12px 'IBM Plex Mono',monospace;letter-spacing:.08em;color:var(--muted)}
.th span.k{font-size:11.5px;opacity:.75}
.th.has{background:#F4F5F7;overflow:hidden}
.th.has img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;transition:transform .4s ease}
.th.has s{z-index:1;border-color:rgba(22,35,58,.55)}
.pc:hover .th.has img{transform:scale(1.04)}
.pb{padding:18px 20px 20px;display:flex;flex-direction:column;gap:8px;flex:1}
.pb .c{font:600 12px 'IBM Plex Mono',monospace;letter-spacing:.08em;color:var(--acc-t)}
.pb h3{margin:0;font:600 19px 'Space Grotesk',sans-serif;color:var(--strong)}
.pb p{margin:0;font-size:14px;line-height:1.55;color:var(--muted)}
.tags{display:flex;gap:6px;flex-wrap:wrap;margin-top:auto;padding-top:10px}
.tag{font:500 12px 'IBM Plex Mono',monospace;padding:3px 8px;border-radius:4px;background:var(--surface2);border:1px solid var(--line);color:var(--body)}


/* credentials & honors strip */
.creds{margin-top:40px}
.ebd{width:10px;height:10px;background:var(--acc);transform:rotate(45deg);margin:0 4px}
.cgrid{display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:12px}
.cr{display:flex;flex-direction:column;gap:6px;padding:16px 16px 14px;transition:border-color .2s}
.cr:hover{border-color:var(--acc)}
.crk{align-self:flex-start;font:700 13px/1 'IBM Plex Mono',monospace;letter-spacing:.04em;color:var(--acc-t);border:1.5px solid var(--acc);background:var(--acc-soft);padding:6px 8px;border-radius:4px;margin-bottom:4px}
.cr .t{font:600 15px/1.3 'Space Grotesk',sans-serif;color:var(--strong)}
.cr .s{font-size:13px;line-height:1.45;color:var(--muted)}
.cr .v{margin-top:auto;padding-top:6px;font:600 12px 'IBM Plex Mono',monospace;letter-spacing:.06em;color:var(--acc-t)}

/* skills & tools */
.skgrid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:20px}
.sk{padding:22px 24px}
.sk .c{font:600 12.5px 'IBM Plex Mono',monospace;letter-spacing:.1em;color:var(--acc-t)}
.sk h3{margin:6px 0 14px;font:600 19px 'Space Grotesk',sans-serif;color:var(--strong)}
.chips{display:flex;flex-wrap:wrap;gap:8px}
.chip{font-size:13.5px;font-weight:500;padding:6px 11px;border-radius:6px;border:1px solid var(--line2);background:var(--surface2);color:var(--text)}
.chip b{font-weight:600;color:var(--acc-t)}

/* experience */
.dg{display:grid;grid-template-columns:1fr 1fr;gap:20px}
.dgc{padding:22px 24px;display:flex;flex-direction:column;gap:8px}
.dgc.on{border-left:3px solid var(--acc)}
.dgt{display:flex;align-items:center;gap:10px;flex-wrap:wrap}
.dgt .pd{font:600 13px 'IBM Plex Mono',monospace;letter-spacing:.04em;color:var(--muted)}
.dgc h3{margin:0;font:600 19px/1.3 'Space Grotesk',sans-serif;color:var(--strong)}
.dgc .org{font-size:15px;font-weight:500;color:var(--body)}
.dgc p{margin:0;font-size:15px;line-height:1.6;color:var(--muted)}

.xe{display:grid;grid-template-columns:1.55fr 1fr;gap:20px;align-items:start}
.xh{font:600 12.5px 'IBM Plex Mono',monospace;letter-spacing:.12em;color:var(--acc-t);padding:16px 0 4px}
.xe .ti{grid-template-columns:150px 22px 1fr}
.xe .ed .ti{grid-template-columns:22px 1fr}
.xe .ed .ti .pd{padding:0 0 4px}
.xe .ed h3{font-size:16.5px}
.xe .ed .org{font-size:14px}

.tl{padding:8px 24px}
.ti{display:grid;grid-template-columns:200px 22px 1fr;gap:18px;padding:20px 0;border-bottom:1px solid var(--line)}
.ti:last-child{border-bottom:none}
.ti .pd{font:600 13px 'IBM Plex Mono',monospace;letter-spacing:.04em;color:var(--muted);padding-top:3px}
.ti .mk{position:relative;display:flex;justify-content:center}
.ti .mk:before{content:"";position:absolute;top:0;bottom:-21px;width:1px;background:var(--line2)}
.ti:last-child .mk:before{bottom:50%}
.ti .mk i{position:relative;width:11px;height:11px;margin-top:5px;border:2px solid var(--muted);background:var(--bg);transform:rotate(45deg)}
.ti .mk i.on{border-color:var(--acc);background:var(--acc)}
.ti h3{margin:0 0 4px;font:600 18px 'Space Grotesk',sans-serif;color:var(--strong);display:flex;align-items:center;gap:10px;flex-wrap:wrap}
.ti .org{font-size:15px;font-weight:500;color:var(--body)}
.ti p{margin:6px 0 0;font-size:14px;line-height:1.55;color:var(--muted)}
.cur{font:600 11.5px 'IBM Plex Mono',monospace;letter-spacing:.08em;color:var(--acc-t);border:1px solid var(--acc);background:var(--acc-soft);padding:2px 8px;border-radius:999px}

/* tests (compact band while pending) */
.tb{display:grid;grid-template-columns:1fr 1fr 1.2fr;align-items:stretch}
.tbi{padding:22px 24px;border-right:1px solid var(--line);display:flex;flex-direction:column;gap:10px}
.tbi .t{font:600 13px 'IBM Plex Mono',monospace;letter-spacing:.08em;color:var(--strong)}
.tbi .s{display:flex;align-items:center;gap:10px;font-size:14px;color:var(--body)}
.tbi .sc{font:500 13px 'IBM Plex Mono',monospace;color:var(--muted)}
.tbn{padding:22px 24px;font-size:14px;line-height:1.6;color:var(--muted);display:flex;align-items:center;background:repeating-linear-gradient(-45deg,transparent 0 7px,var(--surface2) 7px 14px)}

/* contact */
.cta{position:relative;overflow:hidden;padding:48px;display:grid;grid-template-columns:1.4fr 1fr;gap:40px;align-items:center;border-left:3px solid var(--acc)}
.cta .h2{font-size:34px}
.cta p{margin:14px 0 0;font-size:16px;line-height:1.6;color:var(--body)}
.cta .mail{font:500 14px 'IBM Plex Mono',monospace;color:var(--muted);margin-top:14px}
.cta .act{display:flex;flex-direction:column;gap:12px}
.cta .act .btn{width:100%}

/* footer */
.ftr{position:relative;margin-top:104px;border-top:1px solid var(--line);background:var(--header)}
.ftr .wrap{display:grid;grid-template-columns:1fr auto auto;gap:32px;align-items:center;padding-top:28px;padding-bottom:28px}
.ftr .cp{font-size:14px;color:var(--muted)}
.ftr .cp b{font-weight:600;color:var(--strong)}
.ftr nav{display:flex;gap:18px;flex-wrap:wrap}
.ftr nav a{font:600 12px 'IBM Plex Mono',monospace;letter-spacing:.08em;color:var(--body)}
.ftr nav a:hover{color:var(--acc-t)}
.ftr .up{font:500 12px 'IBM Plex Mono',monospace;color:var(--muted)}

@media (prefers-reduced-motion:reduce){
  .gearfig .g1,.gearfig .g2{animation:none}
  .dot{animation:none}
  .pc,.st .ar{transition:none}
}

/* ---------- mobile ---------- */
@media (max-width:760px){
  .wrap{padding:0 16px}
  .hdr .wrap{height:64px}
  .nav,.cvbtn,.sw{display:none}
  .menu{display:flex}
  .hin{padding:48px 0 40px;grid-template-columns:1fr;gap:36px}
  .hfig{max-width:340px;width:100%;margin:0 auto}
  .hc{gap:20px}
  .rev{font-size:11.5px;letter-spacing:.06em}
  .h1{font-size:44px}
  .lead{font-size:18px}
  .focus{flex-direction:column;gap:10px}
  .now{width:100%}
  .ctas{width:100%}
  .ctas .btn{flex:1 1 0;padding:0 12px}
  .pl{--ls:.8;grid-template-columns:repeat(3,minmax(0,1fr));margin-top:28px}
  .plc{padding:18px 6px 14px;gap:10px}
  .plg{height:34px}
  .pll{font-size:11.5px;letter-spacing:.08em;text-align:center}
  .stats{grid-template-columns:1fr}
  .st{padding:20px}
  .st .n{font-size:34px}
  .sec{padding-top:72px}
  .h2{font-size:26px}
  .sh{margin-bottom:20px}
  .pub{grid-template-columns:1fr;gap:10px;padding:20px}
  .pub h3{font-size:17px}
  .pubfoot{padding:14px 20px}
  .pgrid{grid-template-columns:1fr;gap:16px}
  .th{height:180px}
  .tl{padding:4px 18px}
  .ti{grid-template-columns:18px 1fr;gap:14px}
  .ti .pd{grid-column:2;grid-row:1;padding:0}
  .ti .mk{grid-column:1;grid-row:1 / span 2}
  .ti .bx{grid-column:2}
  .tb{grid-template-columns:1fr}
  .xe{grid-template-columns:1fr}
  .dg{grid-template-columns:1fr}
  .xe .ti{grid-template-columns:18px 1fr}
  .ebt{letter-spacing:.1em}
  .cgrid{grid-template-columns:repeat(2,minmax(0,1fr))}
  .cgrid .cr:last-child{grid-column:1 / -1}
  .skgrid{grid-template-columns:1fr}
  .sk{padding:20px}
  .tbi{border-right:none;border-bottom:1px solid var(--line);padding:18px 20px}
  .tbn{padding:16px 20px}
  .cta{grid-template-columns:1fr;padding:28px 22px;gap:24px}
  .cta .h2{font-size:26px}
  .ftr{margin-top:72px}
  .ftr .wrap{grid-template-columns:1fr;gap:16px}
}
"""

ICON_CV = '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M12 3v12m0 0-5-5m5 5 5-5M4 19h16" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>'
ICON_MAIL = '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" aria-hidden="true"><rect x="3" y="5" width="18" height="14" rx="2" stroke="currentColor" stroke-width="2"/><path d="m4 7 8 6 8-6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>'
SUN = '<svg width="13" height="13" viewBox="0 0 24 24" fill="none" aria-hidden="true"><circle cx="12" cy="12" r="5" stroke="C" stroke-width="2"/><path d="M12 1v3M12 20v3M4.2 4.2l2.1 2.1M17.7 17.7l2.1 2.1M1 12h3M20 12h3M4.2 19.8l2.1-2.1M17.7 6.3l2.1-2.1" stroke="C" stroke-width="2" stroke-linecap="round"/></svg>'
MOON = '<svg width="13" height="13" viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M20 14.5A8.5 8.5 0 1 1 9.5 4a7 7 0 0 0 10.5 10.5Z" stroke="C" stroke-width="2" stroke-linejoin="round"/></svg>'
MENU = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M4 7h16M4 12h16M4 17h16" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>'


def logo_strip():
    nav = NAV_SRC
    # compact sizes: scale the hand-tuned optical heights by 0.82, and make them respond to --ls (mobile)
    def sc(m):
        h = round(int(m.group(1)) * 0.82)
        return f'style="height:calc({h}px * var(--ls))"'
    nav = re.sub(r'style="height:(\d+)px"', sc, nav)
    nav = re.sub(r'aria-label="(\w+) profile"', lambda m: f'aria-label="{m.group(1).capitalize() if m.group(1) not in ("Github","Linkedin","Researchgate","Orcid","Grabcad") else {"Github":"GitHub","Linkedin":"LinkedIn","Researchgate":"ResearchGate","Orcid":"ORCID","Grabcad":"GrabCAD"}[m.group(1)]} profile"', nav)
    return nav


AUTO_ICON = '<svg width="13" height="13" viewBox="0 0 24 24" fill="none" aria-hidden="true"><rect x="3" y="4" width="18" height="12" rx="2" stroke="currentColor" stroke-width="2"/><path d="M8 20h8M12 16v4" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>'


def toggle(theme):
    """Light / Dark / Auto segmented switch. Site default = Dark; Auto follows the device setting."""
    opts = [("light", "Light theme", SUN.replace("C", "currentColor")),
            ("dark", "Dark theme (default)", MOON.replace("C", "currentColor")),
            ("auto", "Auto: follow device setting", AUTO_ICON)]
    theme = "dark" if theme.startswith("dark") else ("light" if theme.startswith("light") else theme)
    btns = "".join(
        f'<button type="button" role="radio" aria-checked="{"true" if k == theme else "false"}" '
        f'title="{label}" aria-label="{label}" class="{"on" if k == theme else ""}">{icon}</button>'
        for k, label, icon in opts)
    return f'<div class="tog at-{theme[0]}" role="radiogroup" aria-label="Colour theme">{btns}<span class="tgk" aria-hidden="true">{PINION_TG}</span></div>'




# ---------------- local time + working hours (Fajr to Asr, Dhaka) ----------------
import sys as _sys
_sys.path.insert(0, _os.path.join(SCR, "lib"))
from prayer_hours import times as _prayer_times
from datetime import datetime as _dt, timedelta as _td, timezone as _tz


def clock_sample():
    """Mockup sample = the real Dhaka time when the board is built. On the live site the same values
    are recalculated in the visitor's browser every minute (no server needed)."""
    now = _dt.now(_tz(_td(hours=6)))
    t = _prayer_times(now.date())
    hm = now.strftime("%H:%M")
    on = t["fajr"] <= hm < t["asr"]
    visitor = (now - _td(hours=11)).strftime("%H:%M")          # example visitor: New York (GMT-5)
    return dict(now=hm, fajr=t["fajr"], asr=t["asr"], on=on, visitor=visitor, diff="11 h behind")


CLOCK_CSS = """
.clk{margin-top:18px;padding:14px 16px;border:1px solid var(--line);border-radius:8px;background:var(--surface2);max-width:460px}
.clk-h{font:600 12.5px 'IBM Plex Mono',monospace;letter-spacing:.1em;color:var(--muted)}
.clk-t{display:flex;align-items:baseline;flex-wrap:wrap;gap:6px 10px;margin-top:6px}
.clk-t b{font:600 28px/1 'IBM Plex Mono',monospace;color:var(--strong)}
.clk-t span{font:500 13px 'IBM Plex Mono',monospace;color:var(--muted)}
.clk-t em{font-style:normal;font-size:14px;color:var(--body)}
.clk-s{display:flex;align-items:center;gap:9px;margin-top:10px;font-size:14px;color:var(--body)}
.clk-s b{font-weight:600;color:var(--strong)}
.clk-s .off{width:8px;height:8px;border-radius:999px;border:1.5px solid var(--muted);flex:none}
.ftr .cp .tm{font-family:'IBM Plex Mono',monospace;font-size:13px;color:var(--muted);white-space:nowrap}
"""


def clock_block():
    c = clock_sample()
    if c["on"]:
        status = (f'<div class="clk-s"><span class="dot"></span><span><b>Working hours</b> · Fajr to Asr · '
                  f'today {c["fajr"]} to {c["asr"]}</span></div>')
    else:
        status = (f'<div class="clk-s"><span class="off"></span><span><b>Off hours</b> · replies after Fajr '
                  f'({c["fajr"]})</span></div>')
    return (f'<div class="clk" aria-label="Local time in Dhaka"><div class="clk-h">LOCAL TIME · DHAKA</div>'
            f'<div class="clk-t"><b>{c["now"]}</b><span>GMT+6</span><em>Your time {c["visitor"]} · {c["diff"]}</em></div>'
            f'{status}</div>')

PINION_SW = '''<svg viewBox="0 0 24 24" aria-hidden="true"><path class="gt" d="M10.79 2.07 L11.38 0.42 L12.62 0.42 L13.21 2.07 L15.22 2.53 L16.46 1.29 L17.59 1.83 L17.40 3.58 L19.01 4.87 L20.67 4.29 L21.45 5.27 L20.51 6.76 L21.41 8.61 L23.15 8.81 L23.43 10.03 L21.95 10.97 L21.95 13.03 L23.43 13.97 L23.15 15.19 L21.41 15.39 L20.51 17.24 L21.45 18.73 L20.67 19.71 L19.01 19.13 L17.40 20.42 L17.59 22.17 L16.46 22.71 L15.22 21.47 L13.21 21.93 L12.62 23.58 L11.38 23.58 L10.79 21.93 L8.78 21.47 L7.54 22.71 L6.41 22.17 L6.60 20.42 L4.99 19.13 L3.33 19.71 L2.55 18.73 L3.49 17.24 L2.59 15.39 L0.85 15.19 L0.57 13.97 L2.05 13.03 L2.05 10.97 L0.57 10.03 L0.85 8.81 L2.59 8.61 L3.49 6.76 L2.55 5.27 L3.33 4.29 L4.99 4.87 L6.60 3.58 L6.41 1.83 L7.54 1.29 L8.78 2.53 Z"/><circle class="gr" cx="12" cy="12" r="6.8"/><circle class="gh" cx="12" cy="12" r="4.2"/></svg>'''
PINION_TG = '''<svg viewBox="0 0 24 24" aria-hidden="true"><path class="gt" d="M10.79 2.07 L11.38 0.42 L12.62 0.42 L13.21 2.07 L15.22 2.53 L16.46 1.29 L17.59 1.83 L17.40 3.58 L19.01 4.87 L20.67 4.29 L21.45 5.27 L20.51 6.76 L21.41 8.61 L23.15 8.81 L23.43 10.03 L21.95 10.97 L21.95 13.03 L23.43 13.97 L23.15 15.19 L21.41 15.39 L20.51 17.24 L21.45 18.73 L20.67 19.71 L19.01 19.13 L17.40 20.42 L17.59 22.17 L16.46 22.71 L15.22 21.47 L13.21 21.93 L12.62 23.58 L11.38 23.58 L10.79 21.93 L8.78 21.47 L7.54 22.71 L6.41 22.17 L6.60 20.42 L4.99 19.13 L3.33 19.71 L2.55 18.73 L3.49 17.24 L2.59 15.39 L0.85 15.19 L0.57 13.97 L2.05 13.03 L2.05 10.97 L0.57 10.03 L0.85 8.81 L2.59 8.61 L3.49 6.76 L2.55 5.27 L3.33 4.29 L4.99 4.87 L6.60 3.58 L6.41 1.83 L7.54 1.29 L8.78 2.53 Z"/><circle class="gd" cx="12" cy="12" r="8.6"/><circle class="gr" cx="12" cy="12" r="8.6"/></svg>'''


def swatches(theme):
    """Accent picker: H lamp slider. Lens order red / blue / green; the ring sits on the chosen lens."""
    hue = "blue" if theme.endswith("_blue") else ("green" if theme.endswith("_green") else "red")
    opts = [("red", "#C14B3C", "rgba(193,75,60,0.55)", "Red"),
            ("blue", "#2F6BD8", "rgba(47,107,216,0.55)", "Blue"),
            ("green", "#1E7F55", "rgba(30,127,85,0.55)", "Green")]
    b = "".join(
        f'<button type="button" role="radio" aria-checked="{"true" if k == hue else "false"}" '
        f'aria-label="{name} accent" class="{"on" if k == hue else ""}" style="--c:{c};--cg:{glow}"></button>'
        for k, c, glow, name in opts)
    return f'<div class="sw at-{hue[0]}" role="radiogroup" aria-label="Accent colour"><div class="tr">{b}</div><span class="rg" aria-hidden="true">{PINION_SW}</span></div>'


def swatches_dots(theme):
    """Colour picker: red (default) / blue / green. Dots only - no visible names (Zaid).
    The active dot sits in a small highlighted ring with a soft glow."""
    hue = "blue" if theme.endswith("_blue") else ("green" if theme.endswith("_green") else "red")
    opts = [("red", "#C14B3C", "rgba(193,75,60,0.45)", "Red"),
            ("blue", "#2F6BD8", "rgba(47,107,216,0.45)", "Blue"),
            ("green", "#1E7F55", "rgba(30,127,85,0.45)", "Green")]
    b = "".join(
        f'<button type="button" role="radio" aria-checked="{"true" if k == hue else "false"}" '
        f'aria-label="{name} colour" class="{"on" if k == hue else ""}" style="--c:{c};--cg:{glow}"><i></i></button>'
        for k, c, glow, name in opts)
    return f'<div class="sw" role="radiogroup" aria-label="Accent colour">{b}</div>'


def pub(year, badges, title, venue, author, doi):
    b = "".join(f'<span class="bd{" a" if a else ""}">{t}</span>' for t, a in badges)
    return f'''
        <article class="pub">
          <div class="yr">{year}</div>
          <div>
            <div class="bdg">{b}</div>
            <h3>{title}</h3>
            <div class="vn">{venue} · <b>{author}</b></div>
          </div>
          <div class="lk"><a href="https://doi.org/{doi}" target="_blank" rel="noopener">DOI ↗</a><a href="#">PDF</a><a href="#">CITE</a></div>
        </article>'''


PIMG = {
    "foil-plant": "/_blob/964361454498ee5c321de9b3542ea4ec", "distillation": "/_blob/648f9329e77cd0023278f64f1538d6a1", "ev-station": "/_blob/1dbfb8ccffbd500fec178fe948c376b8",
    "ev-station-cad": "/_blob/b35cc36ceec7ac5d856cfa9793264aea", "gear-holder": "/_blob/ef1bc2ccaded9bc0424f971be8e4620f",
    "vice": "/_blob/5515f314c95fa529e7f9f748308193ee", "pin-locator": "/_blob/ec8fd9a414b565b382074b992c0313fc", "headstock": "/_blob/6b4b094ea0d95713eacd7aed7356d505",
    "quadcopter": "/_blob/a7a51d7622df2ba6d817bda6c6a8e8d7", "rotor": "/_blob/ecbe4cf7669d13f12f9c124e7e354d94",
    "servo": "/_blob/926ce37a797eff10f9e78a1c535f94b9", "differential": "/_blob/46b1fafa0d8c7f8f595af1ee6b21477f",
    "payloader": "/_blob/d4557ed067c352dfc967f684cf71fe09", "haas-vf2": "/_blob/242f51a5e184a9d47f9868d67e06b3d3",
    "bicycle": "/_blob/4f19edecbe20b5d822c036aeabd796cf",
}


def project(cat, title, desc, tags, img=None, pos="center"):
    """Project card (approved 2026-11-17): same frame + hover, part number and spec rows."""
    import site_parts as SP
    if img:
        th = f'<div class="th has"><img src="{PIMG[img]}" alt="{title} · CAD render" style="object-position:{pos}"><s></s><s></s></div>'
    else:
        th = '<div class="th"><s></s><s></s><span>RENDER TO BE ADDED</span><span class="k">STEP · GLB · 3D VIEWER</span></div>'
    card = SP.part_card(img or "", cat, title, tags, th)
    # quiet next step at the foot of every card (approved 2026-11-18)
    return card.replace("\n        </a>", '<div class="pvw"><span>VIEW PROJECT</span><i>→</i></div>\n        </a>', 1)



def edu(period, deg, inst, note="", current=False):
    cur = '<span class="cur">ONGOING</span>' if current else ""
    n = f"<p>{note}</p>" if note else ""
    return f'''
        <div class="ti">
          <div class="mk"><i class="{"on" if current else ""}"></i></div>
          <div class="bx">
            <div class="pd">{period}</div>
            <h3>{deg} {cur}</h3>
            <div class="org">{inst}</div>{n}
          </div>
        </div>'''


def exp(period, role, org, desc, current=False):
    cur = '<span class="cur">CURRENT</span>' if current else ""
    return f'''
        <div class="ti">
          <div class="pd">{period}</div>
          <div class="mk"><i class="{"on" if current else ""}"></i></div>
          <div class="bx">
            <h3>{role} {cur}</h3>
            <div class="org">{org}</div>
            <p>{desc}</p>
          </div>
        </div>'''



# Readability polish — approved by Zaid 2026-11-14, applied to all homepage boards
POLISH_CSS = """
/* ===== readability polish (proposal) ===== */
.rev,.now .k,.pll,.lk a,.tag,.pb .c,.cr .v,.g3dlab,.g3dspec,.tbi .sc,.pill{font-size:12.5px}
.bd,.cur,.th span.k{font-size:12.5px}
.th span{font-size:12.5px}
.pub .vn,.pb p,.ti p,.st .s,.pubfoot,.tbn{font-size:15px;line-height:1.6}
.cr .s{font-size:14px;line-height:1.5}
.chip{font-size:14px}
.pub h3{max-width:70ch}
.ftr nav a{font:600 13px 'Inter',system-ui,sans-serif;letter-spacing:.04em}
.ftr .up{font:500 13px 'Inter',system-ui,sans-serif;letter-spacing:.02em}
.ftr .cp{font-size:15px}
@media (max-width:760px){
  .rev{font-size:12px;letter-spacing:.02em}
  .pll{font-size:12px;letter-spacing:.06em}
}
"""
POLISH_DARK_VARS = ".zh{--muted:#A7B0BD}"
# dark themes: header pinions drawn in white so they stand out (Zaid 2026-11-20)
POLISH_DARK_VARS += ".zh .sw .rg .gt,.zh .tgk .gt{stroke:#fff;stroke-width:1.15;opacity:1}.zh .sw .rg .gr,.zh .tgk .gr{stroke:rgba(255,255,255,.55)}"

def page(theme, title, polish=True, scroll=None):  # readability polish approved by Zaid 2026-11-14
    T = THEMES[theme]
    STAT = " stat" if scroll is not None else ""
    SCC = f' style="margin-top:-{scroll}px"' if scroll else ""
    _saved = dict(HP.G3D_ASSETS)
    HP.G3D_ASSETS.update(HP.G1_BY_THEME.get(theme, {}))
    css = CSS
    css = BACKDROP_CSS + GEAR3D_CSS + CLOCK_CSS + css.replace("VARS", T["vars"])
    if polish:
        css += POLISH_CSS + (POLISH_DARK_VARS if theme.startswith("dark") else "")
    import site_parts as SP
    css += SP.css()
    css += EG.CSS
    css += XL.CSS
    css += RL.CSS
    css += SKC.CSS

    pubs = "".join([
        pub("2026", [("JOURNAL · Q1", True), ("1ST AUTHOR", False)],
            "Leakage-controlled machine learning for work-related musculoskeletal disorder risk classification among garment sewing-machine operators",
            "Results in Engineering 32 (2026) 113789 · Elsevier", "Md. Zaid Hossain, et al.", "10.1016/j.rineng.2026.113789"),
        pub("2026", [("JOURNAL · Q1", True)],
            "A simulation-based context-aware multimodal ML framework for proactive worker safety monitoring in resource-constrained factories",
            "Array 31 (2026) 101198 · Elsevier", "N. Morshed, M. S. I. Seam, Md. Zaid Hossain, M. A. Amin", "10.1016/j.array.2026.101198"),
        pub("2025", [("CONFERENCE · IEEE", True), ("1ST AUTHOR", False)],
            "AI-Driven Early Warning System for Industrial Shutdowns on High-Risk Pollution Days: A Case Study on Dhaka Air Quality",
            "IEEE QPAIN 2025 · BAUST, Saidpur", "Md. Zaid Hossain, N. Morshed, S. I. Seam", "10.1109/QPAIN66474.2025.11171883"),
    ])

    projects = "".join([
        project("COMPETITION · ENERGY FEST 1.0", "EV Charging Station", "Multi-purpose charging station for urban streets, with a solar canopy, CCS port, seating and safety systems.", ["SOLIDWORKS", "KeyShot"], "ev-station"),
        project("3D PRINTING", "Gear-Pinion Phone Holder", "Designed for printing. Modelled in SOLIDWORKS, sliced in Creality and printed on an Ender-3 V2 Neo.", ["SOLIDWORKS", "Creality Slicer", "FDM print"], "gear-holder"),
        project("MACHINE TOOLS · IPE 4126", "Lathe Head-stock Gearbox", "Speed gearbox modelled from the lab lathe: gear train, shafts and housing.", ["SOLIDWORKS", "Gear design"], "headstock"),
    ])

    edus = "".join([
        edu("2025 → NOW", "M.Sc. in Industrial Engineering &amp; Management", "KUET · Khulna University of Engineering &amp; Technology", "Part-time, alongside current role.", True),
        edu("2019 → 2025", "B.Sc. Eng. in Industrial &amp; Production Engineering", "KUET · Khulna University of Engineering &amp; Technology"),
        edu("YYYY", "Higher Secondary Certificate (HSC)", "DC · full college name to confirm"),
        edu("YYYY", "Secondary School Certificate (SSC)", "AGHS · full school name to confirm"),
    ])

    exps = "".join([
        exp("JUL 2026 → NOW", "Fab Lab Program Engineer (Instrumentation)", "IAT, BUET · HEAT Sub-Project",
            "Instrumentation and fabrication-lab programme work under the HEAT sub-project.", True),
        exp("2023 → NOW", "Freelance CAD Designer", "Independent · 16 client projects",
            "Process-plant layouts, a mining machine, servo mechanisms, composite parts and product renderings."),
        exp("MAR 2024 → SEP 2025", "FabLab Assistant · Student Operator", "FabLab, KUET",
            "3D-printer operation and calibration, printer repair, and CAD and print support for students."),
    ])

    menu = f'<button class="menu" aria-label="Open menu" style="color:var(--strong)">{MENU}</button>'

    body = f'''
<div class="zh{STAT}">
  {backdrop(theme)}
  <div class="scr"><div class="scc"{SCC}>

  <header class="hdr">
    <div class="wrap">
      <a class="brand" href="#" aria-label="Home"><i>ZH</i><b>Md. Zaid Hossain</b></a>
      <nav class="nav" aria-label="Main">
        <a href="#">Research</a><a href="#">Projects</a><a href="#">Experience</a><a href="#">Awards</a><a href="#">Gallery</a><a href="#">Contact</a>
      </nav>
      <div class="hact">
        <a class="cvbtn" href="#">{ICON_CV}CV</a>
        {swatches(theme)}
        {toggle(theme)}
        {menu}
      </div>
    </div>
  </header>

  <!-- Hero: static page backdrop (locked look) shows through; right column = live CAD figure -->
  <section class="hero">
    <div class="wrap"><div class="hin">
      <div class="hc">
        <div class="rev"><s></s><s></s><s></s><s></s><span class="rvp">PORTFOLIO </span>REV. 2026.11 · IE · OR · CAD</div>
        <h1 class="h1">Md. Zaid Hossain</h1>
        <p class="lead">Industrial engineer working where <b>optimization</b>, <b>data</b> and <b>manufacturing</b> meet.</p>
        <ul class="focus">
          <li>Operations Research &amp; Optimization</li>
          <li>Additive Manufacturing &amp; CAD/CAM</li>
          <li>Ergonomics &amp; Worker Safety</li>
        </ul>
        {SP.hero_facts()}
        <div class="ctas">
          {SP.BTN_CV}
        </div>
      </div>
      <div class="hfig">{SP.hero_figure(gear3d())}</div>
    </div></div>
  </section>

  <main class="wrap" style="position:relative;z-index:1">

    {logo_strip()}

    <section class="stats" aria-label="Highlights">
      <a class="st" href="#"><span class="ar" aria-hidden="true">→</span><div class="n">04</div><div class="l">PUBLICATIONS</div><div class="s">2 journal · 2 conference</div></a>
      <a class="st" href="#"><span class="ar" aria-hidden="true">→</span><div class="n">30+</div><div class="l">CAD AND 3D PROJECTS</div><div class="s">academic · competition · self-practice</div></a>
      <a class="st" href="#"><span class="ar" aria-hidden="true">→</span><div class="n">21</div><div class="l">CERTIFICATIONS</div><div class="s">plus 3 CAD championships and an ISCEA scholarship</div></a>
    </section>


    <!-- Credentials & honors -->
    <section class="creds" aria-labelledby="s-creds">
      <div class="eb"><span class="ebd"></span><span class="ebt" id="s-creds">CREDENTIALS &amp; HONORS</span><span class="ebl"></span></div>
      <div class="cgrid">
        <a class="card cr" href="https://cv.virtualtester.com/qr/?b=SLDWRKS&amp;i=C-3WTCQ4G7A5"><span class="crk">CSWP</span><span class="t">Certified SOLIDWORKS Professional</span><span class="s">Dassault Systèmes · 2025</span><span class="v">VERIFY ↗</span></a>
        <a class="card cr" href="https://www.iscea.org/verify-certification"><span class="crk">CSCA™</span><span class="t">Certified Supply Chain Analyst</span><span class="s">ISCEA · 2025</span><span class="v">VERIFY ↗</span></a>
        <a class="card cr" href="#"><span class="crk">4× CSWA</span><span class="t">SOLIDWORKS Associate</span><span class="s">Mechanical Design · Simulation · Additive Mfg · Sustainability</span><span class="v">ALL FOUR, WITH VERIFY LINKS →</span></a>
        <a class="card cr" href="#"><span class="crk">3× CHAMPION</span><span class="t">National CAD competitions</span><span class="s">Technomize 1.0 · CAD Rush 1.0 · MECHCELLENCE 1.0</span><span class="v">ALL AWARDS →</span></a>
        <a class="card cr" href="#"><span class="crk">DSW · KUET</span><span class="t">Award of Excellence</span><span class="s">and a Certificate of Contribution for extracurricular work · 2025</span><span class="v">CAMPUS ROLES →</span></a>
      </div>
    </section>

    <!-- 01 Education: degrees + language / graduate tests (Zaid: education first; school results live on the Education page) -->
    <section class="sec" aria-labelledby="s-edu">
      <div class="sh">
        <div class="eb"><span class="ebn">01</span><span class="ebt">EDUCATION</span><span class="ebl"></span></div>
        <div class="shr"><h2 class="h2" id="s-edu">Education</h2>
        <a class="more" href="#">Results &amp; certificates →</a>
      </div></div>
      {EG.gantt()}
    </section>

    <!-- 02 Experience -->
    <section class="sec" aria-labelledby="s-exp">
      <div class="sh">
        <div class="eb"><span class="ebn">02</span><span class="ebt">EXPERIENCE</span><span class="ebl"></span></div>
        <div class="shr"><h2 class="h2" id="s-exp">Experience</h2>
        <a class="more" href="#">Full timeline →</a>
      </div></div>
      {XL.html()}
    </section>

    <!-- 03 Research -->
    <section class="sec" aria-labelledby="s-research">
      <div class="sh">
        <div class="eb"><span class="ebn">03</span><span class="ebt">RESEARCH</span><span class="ebl"></span></div>
        <div class="shr"><h2 class="h2" id="s-research">Selected publications</h2>
        <a class="more" href="#">All publications →</a>
      </div></div>
      {RL.html()}
    </section>

    <!-- 04 Projects -->
    <section class="sec" aria-labelledby="s-projects">
      <div class="sh">
        <div class="eb"><span class="ebn">04</span><span class="ebt">PROJECTS</span><span class="ebl"></span></div>
        <div class="shr"><h2 class="h2" id="s-projects">CAD &amp; 3D printing projects</h2>
        <a class="more" href="#">All projects →</a>
      </div></div>
      <div class="pgrid">{projects}
      </div>
    </section>

    <!-- 05 Skills & tools -->
    <section class="sec" aria-labelledby="s-skills">
      <div class="sh">
        <div class="eb"><span class="ebn">05</span><span class="ebt">SKILLS</span><span class="ebl"></span></div>
        <div class="shr"><h2 class="h2" id="s-skills">Skills &amp; tools</h2>
      </div></div>
      {SKC.html()}
    </section>

    <!-- 06 Contact (approved 2026-11-17) -->
{SP.contact(clock_sample())}

  </main>

{SP.footer(clock_sample()["now"], theme.startswith("dark"))}
  </div></div>
</div>'''

    HP.G3D_ASSETS.clear(); HP.G3D_ASSETS.update(_saved)
    # site-wide pieces approved 2026-11-20: phone menu, favicon and share-image tags
    import site_extras as SX
    css += SX.MENU_CSS
    body = SX.add_menu(body, None, theme)
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
{SX.head_tags()}<script src="./support.js"></script>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;600;700&family=Inter:wght@400;500;600&family=IBM+Plex+Mono:wght@500;600&display=swap">
</head>
<body>
<x-dc>
<helmet>
<style>{css}</style>
</helmet>
{body}
</x-dc>
<script type="text/x-dc" data-dc-script data-props='{{"accent":{{"editor":"color","default":"#C14B3C","options":["#C14B3C","#E87D3E","#4C8DFF","#2DD4BF"]}}}}'>
class Component extends DCLogic {{
  renderVals() {{
    return {{ accent: this.props.accent ?? '#C14B3C' }};
  }}
}}
</script>
</body>
</html>
'''


# ---------------- "after results" sample board (IELTS / GRE filled in) ----------------
TS_CSS = """
.note{display:inline-block;font:600 12.5px 'IBM Plex Mono',monospace;letter-spacing:.04em;color:var(--acc-t);background:var(--acc-soft);border:1px solid var(--acc);border-radius:6px;padding:8px 12px}
.sub{font:600 12.5px 'IBM Plex Mono',monospace;letter-spacing:.1em;color:var(--muted);margin:28px 0 10px}
.tsgrid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:20px}
.tscard{padding:24px 26px}
.tshead{display:flex;justify-content:space-between;align-items:center;gap:12px;flex-wrap:wrap}
.tsname{font:600 13px 'IBM Plex Mono',monospace;letter-spacing:.08em;color:var(--strong)}
.tsstatus{display:inline-flex;align-items:center;gap:6px;font:600 12.5px 'IBM Plex Mono',monospace;letter-spacing:.06em;color:var(--acc-t);border:1px solid var(--acc);background:var(--acc-soft);border-radius:999px;padding:4px 11px}
.tsbig{display:flex;align-items:baseline;gap:8px;margin:20px 0 4px}
.tsbig b{font:600 46px/1 'IBM Plex Mono',monospace;color:var(--strong)}
.tsbig span{font:500 15px 'IBM Plex Mono',monospace;color:var(--muted)}
.tscap{font-size:15px;color:var(--muted);margin-bottom:18px}
.tsrow{display:grid;grid-template-columns:200px 1fr 56px;align-items:center;gap:14px;padding:7px 0}
.tsrow span{font-size:15px;color:var(--body)}
.tsbar{height:8px;border-radius:999px;background:var(--surface2);border:1px solid var(--line);overflow:hidden}
.tsbar i{display:block;height:100%;background:var(--acc);border-radius:999px}
.tsrow em{font:600 15px 'IBM Plex Mono',monospace;font-style:normal;text-align:right;color:var(--strong)}
.tsfoot{margin-top:16px;padding-top:14px;border-top:1px solid var(--line);font:500 12.5px 'IBM Plex Mono',monospace;letter-spacing:.04em;color:var(--muted)}
.tsfoot b{font-weight:600;color:var(--body)}
@media (max-width:760px){.tsgrid{grid-template-columns:1fr}.tsrow{grid-template-columns:150px 1fr 48px}}
"""


def scores_page(theme, title):
    T = THEMES[theme]
    STAT, SCC = "", ""
    css = BACKDROP_CSS + CSS.replace("VARS", T["vars"]) + POLISH_CSS + (POLISH_DARK_VARS if theme.startswith("dark") else "") + TS_CSS

    def row(label, val, pct):
        return f'<div class="tsrow"><span>{label}</span><div class="tsbar"><i style="width:{pct:.1f}%"></i></div><em>{val}</em></div>'

    ielts = "".join(row(l, v, float(v) / 9 * 100) for l, v in [("Listening", "8.0"), ("Reading", "7.5"), ("Writing", "7.0"), ("Speaking", "7.0")])
    gre = (row("Verbal Reasoning", "155", (155 - 130) / 40 * 100) + row("Quantitative Reasoning", "165", (165 - 130) / 40 * 100)
           + row("Analytical Writing", "4.0", 4.0 / 6 * 100))
    which = "dark mode" if theme.startswith("dark") else "light mode"
    body = f"""
<div class="zh{STAT}">
  {backdrop(theme)}
  <div class="scr"><div class="scc"{SCC}>
  <main class="wrap" style="position:relative;z-index:1;padding-top:56px;padding-bottom:72px">
    <span class="note">SAMPLE NUMBERS: how the tests section fills in once real IELTS and GRE results are added ({which})</span>

    <div class="sub">HERO PILLS AFTER RESULTS (OPTIONAL)</div>
    <div class="pills">
      <span class="pill">B.Sc. Eng. in IPE · KUET · 2025</span>
      <span class="pill">M.Sc. Eng. in IEM · KUET · ongoing</span>
      <span class="pill">IELTS Academic · 7.5</span>
      <span class="pill">GRE · 320</span>
    </div>

    <section class="sec" style="padding-top:56px" aria-labelledby="s-tests">
      <div class="sh">
        <div class="eb"><span class="ebn">05</span><span class="ebt">TESTS</span><span class="ebl"></span></div>
        <div class="shr"><h2 class="h2" id="s-tests">Language &amp; graduate tests</h2></div>
      </div>
      <div class="tsgrid">
        <div class="card tscard">
          <div class="tshead"><span class="tsname">IELTS ACADEMIC</span><span class="tsstatus">✓ RESULT PUBLISHED</span></div>
          <div class="tsbig"><b>7.5</b><span>/ 9.0</span></div>
          <div class="tscap">Overall band</div>
          {ielts}
          <div class="tsfoot">TEST DATE · <b>DD MMM YYYY</b> · VALID UNTIL · <b>DD MMM YYYY</b></div>
        </div>
        <div class="card tscard">
          <div class="tshead"><span class="tsname">GRE GENERAL</span><span class="tsstatus">✓ RESULT PUBLISHED</span></div>
          <div class="tsbig"><b>320</b><span>/ 340</span></div>
          <div class="tscap">Total score</div>
          {gre}
          <div class="tsfoot">TEST DATE · <b>DD MMM YYYY</b> · VALID UNTIL · <b>DD MMM YYYY</b></div>
        </div>
      </div>
    </section>
  </main>
  </div></div>
</div>"""
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<script src="./support.js"></script>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;600;700&family=Inter:wght@400;500;600&family=IBM+Plex+Mono:wght@500;600&display=swap">
</head>
<body>
<x-dc>
<helmet>
<style>{css}</style>
</helmet>
{body}
</x-dc>
<script type="text/x-dc" data-dc-script data-props='{{"accent":{{"editor":"color","default":"#C14B3C"}}}}'>
class Component extends DCLogic {{
  renderVals() {{
    return {{ accent: this.props.accent ?? '#C14B3C' }};
  }}
}}
</script>
</body>
</html>
"""


# ---- real site: the lists above are replaced by content/*.yml (build/content_io.py) ----
import content_io as _C
PIMG.update(_C.load_projects()[2])


if __name__ == "__main__":
    import type_scale as TS
    out = __import__("os").environ.get("PORTFOLIO_OUT", "/home/claude/zaid/project")
    open(f"{out}/Light.dc.html", "w").write(TS.apply(page("light", "Home: Light mode")))
    open(f"{out}/Dark.dc.html", "w").write(TS.apply(page("dark", "Home: Dark mode")))
    open(f"{out}/Mobile.dc.html", "w").write(TS.apply(page("dark", "Home: Mobile (dark)")))
    open(f"{out}/MobileLight.dc.html", "w").write(TS.apply(page("light", "Home: Mobile (light)")))
    open(f"{out}/DarkBlue.dc.html", "w").write(TS.apply(page("dark_blue", "Home: Dark (blue)")))
    open(f"{out}/DarkGreen.dc.html", "w").write(TS.apply(page("dark_green", "Home: Dark (green)")))
    open(f"{out}/LightBlue.dc.html", "w").write(TS.apply(page("light_blue", "Home: Light (blue)")))
    open(f"{out}/LightGreen.dc.html", "w").write(TS.apply(page("light_green", "Home: Light (green)")))
    open(f"{out}/Scores.dc.html", "w").write(TS.apply(scores_page("dark", "Tests: after results (dark)")))
    open(f"{out}/ScoresLight.dc.html", "w").write(TS.apply(scores_page("light", "Tests: after results (light)")))
    print("written")
