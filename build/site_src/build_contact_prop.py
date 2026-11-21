#!/usr/bin/env python3
"""Proposal board: Contact section, NOW vs PROPOSED (all themes + phone). Not applied to the home page yet."""
import math
import build_home as H
import site_parts as SP

CSS = """
/* focus + open slot */
.focus2{display:flex;flex-wrap:wrap;align-items:center;gap:8px;margin-top:14px}
.focus2 .fk{font:600 12px 'IBM Plex Mono',monospace;letter-spacing:.1em;color:var(--muted);margin-right:4px}
.focus2 .fc{font-size:14px;padding:6px 11px;border:1px solid var(--line2);color:var(--strong);background:var(--surface2)}
.focus2 .fc.open{border-style:dashed;border-color:var(--acc);color:var(--acc-t);background:transparent}
.tol{display:flex;align-items:center;gap:10px;font:600 14px 'IBM Plex Mono',monospace;letter-spacing:.06em;color:var(--strong)}
.tol b{font:600 26px 'IBM Plex Mono',monospace;color:var(--acc-t)}
.tol .t2{color:var(--acc-t)}
.opts3{display:grid;grid-template-columns:repeat(3,1fr);gap:16px}
.o3{padding:18px;border:1px dashed var(--line2);border-radius:10px;display:flex;flex-direction:column;gap:14px;background:var(--surface);backdrop-filter:var(--glass)}
.o3.rec{border-style:solid;border-color:var(--acc)}
.o3 .ol{font:600 12px 'IBM Plex Mono',monospace;letter-spacing:.1em;color:var(--acc-t)}
.o3 p{margin:0;font-size:14px;line-height:1.55;color:var(--body)}
.o3 .csheet{margin-top:0}
.cact.col{flex-direction:column;align-items:flex-start;gap:14px}
/* 1 · bracket buttons */
.bkb{position:relative;display:inline-flex;align-items:center;gap:9px;height:40px;padding:0 16px;font:600 12.5px 'IBM Plex Mono',monospace;letter-spacing:.1em;color:var(--strong);background:var(--surface2);transition:background .2s,color .2s}
.bkb s{position:absolute;width:8px;height:8px;border:0 solid var(--line2);transition:all .2s}
.bkb s:nth-child(1){top:0;left:0;border-top-width:2px;border-left-width:2px}
.bkb s:nth-child(2){top:0;right:0;border-top-width:2px;border-right-width:2px}
.bkb s:nth-child(3){bottom:0;left:0;border-bottom-width:2px;border-left-width:2px}
.bkb s:nth-child(4){bottom:0;right:0;border-bottom-width:2px;border-right-width:2px}
.bkb i{font-style:normal;transition:transform .2s}
.bkb span{padding-bottom:2px;background:linear-gradient(var(--acc-t),var(--acc-t)) left bottom/0 2px no-repeat;transition:background-size .3s ease}   /* no line at rest (Zaid, 21 Nov); on hover a theme-colour line draws in from the left */
.bkb:hover span,.bkb:focus-visible span{background-size:100% 2px}
.bkb.p{background:var(--acc);color:var(--on-acc)}
.bkb.p s{border-color:var(--acc-t)}
.bkb:hover s:nth-child(1){top:-5px;left:-5px}.bkb:hover s:nth-child(2){top:-5px;right:-5px}
.bkb:hover s:nth-child(3){bottom:-5px;left:-5px}.bkb:hover s:nth-child(4){bottom:-5px;right:-5px}
.bkb:hover s{border-color:var(--acc)}
.bkb:hover i{transform:translateX(4px)}
.bkb:not(.p):hover{color:var(--acc-t)}
/* 2 · control-panel push buttons */
.panel{display:flex;align-items:center;gap:22px;padding:14px 18px;border-radius:8px;background:linear-gradient(180deg,#9AA1AB,#6F7682);box-shadow:inset 0 1px 0 rgba(255,255,255,.35),0 2px 6px rgba(0,0,0,.35);width:max-content}
.panel em{font:700 10px 'IBM Plex Mono',monospace;font-style:normal;letter-spacing:.12em;color:#1E2126;opacity:.7;writing-mode:vertical-rl;transform:rotate(180deg)}
.pb{display:flex;flex-direction:column;align-items:center;gap:6px}
.pb b{display:block;width:44px;height:44px;border-radius:999px;background:radial-gradient(circle at 35% 30%,#E6E9ED,#7D848F 70%);box-shadow:0 0 0 4px #2A2E34,0 4px 0 #1A1D21,0 6px 8px rgba(0,0,0,.4);transition:transform .12s,box-shadow .12s}
.pb.p b{background:radial-gradient(circle at 35% 30%,#FF8A7A,var(--acc) 70%)}
.pb span{font:700 11px 'IBM Plex Mono',monospace;letter-spacing:.12em;color:#1E2126;padding:2px 6px;background:#E9ECEF;border:1px solid #4A4F57}
.pb:hover b{transform:translateY(3px);box-shadow:0 0 0 4px #2A2E34,0 1px 0 #1A1D21,0 2px 3px rgba(0,0,0,.4)}
/* 3 · leader-line links */
.ldr{display:inline-flex;align-items:center;gap:12px;font:600 14px 'IBM Plex Mono',monospace;letter-spacing:.1em;color:var(--strong)}
.ldr i{position:relative;display:block;width:60px;height:1.5px;background:var(--line2);transition:width .25s,background .25s}
.ldr i:after{content:"";position:absolute;right:-1px;top:-4px;border-left:9px solid var(--line2);border-top:4.75px solid transparent;border-bottom:4.75px solid transparent;transition:border-color .25s}
.ldr.p{color:var(--acc-t)}.ldr.p i{background:var(--acc)}.ldr.p i:after{border-left-color:var(--acc)}
.ldr:hover i{width:96px;background:var(--acc)}.ldr:hover i:after{border-left-color:var(--acc)}
@media (max-width:760px){.opts3{grid-template-columns:1fr}}

/* ===== contact proposal ===== */
.crumb{font:600 12.5px 'IBM Plex Mono',monospace;letter-spacing:.1em;color:var(--muted)}
.ph{position:relative;padding:56px 0 4px}
.ph .h1{font-size:46px;margin-top:16px}
.ph .lead{margin-top:14px;max-width:820px;font-size:18px}
.row{margin-top:44px}
.cap{font:600 12.5px 'IBM Plex Mono',monospace;letter-spacing:.12em;color:var(--muted);margin-bottom:10px}
.cap.new{color:var(--acc-t)}
.row .sec{padding-top:0}
.rv{display:grid;grid-template-columns:repeat(2,1fr);gap:10px 28px;margin-top:18px;padding:18px 20px;border:1px dashed var(--line2);border-radius:10px}
.rv div{display:flex;gap:10px;font-size:14.5px;line-height:1.55;color:var(--body)}
.rv b{flex:none;font:700 12.5px 'IBM Plex Mono',monospace;color:var(--acc-t);padding-top:2px}

/* proposed contact */
.ctx{position:relative;padding:44px 48px;display:grid;grid-template-columns:minmax(0,1.35fr) 300px;gap:48px;align-items:start}
.ctx .h2{font-size:34px}
.ctx .sub{margin:12px 0 0;font-size:16px;line-height:1.6;color:var(--body)}
.csheet{display:grid;grid-template-columns:120px 1fr;margin-top:22px;border-top:1px solid var(--line2);max-width:620px}
.csheet>span{padding:10px 0;border-bottom:1px solid var(--line);font-size:15px;color:var(--strong);display:flex;align-items:center;gap:10px;flex-wrap:wrap}
.csheet>span.k{font:600 12px 'IBM Plex Mono',monospace;letter-spacing:.1em;color:var(--muted)}
.csheet .em{font:600 15.5px 'IBM Plex Mono',monospace;color:var(--strong)}
.csheet .cp2{font:600 11.5px 'IBM Plex Mono',monospace;letter-spacing:.08em;padding:4px 9px;border:1px solid var(--line2);border-radius:5px;color:var(--body);cursor:pointer}
.csheet .cp2:hover{border-color:var(--acc);color:var(--acc-t)}
.csheet a.plk{font:600 12.5px 'IBM Plex Mono',monospace;letter-spacing:.06em;color:var(--body);white-space:nowrap}
.csheet a.plk:hover{color:var(--acc-t)}
.csheet em{font-style:normal;color:var(--muted)}
.cact{display:flex;gap:12px;flex-wrap:wrap;margin-top:24px}
.inst{border:1px solid var(--line);border-radius:12px;background:var(--surface2);padding:18px 18px 16px;display:flex;flex-direction:column;align-items:center;gap:10px}
.inst .ih{align-self:stretch;display:flex;justify-content:space-between;font:600 12px 'IBM Plex Mono',monospace;letter-spacing:.1em;color:var(--muted)}
.dial{width:210px;height:210px;display:block}
.dial .face{fill:var(--bg);stroke:var(--line2);stroke-width:1.5}
.dial .tk{stroke:var(--muted);stroke-width:1.2}
.dial .tk.b{stroke:var(--strong);stroke-width:2.4}
.dial .num{font:600 13px 'IBM Plex Mono',monospace;fill:var(--body)}
.dial .work{fill:none;stroke:var(--acc);stroke-width:7;stroke-opacity:.55;stroke-linecap:round}
.dial .hh{stroke:var(--strong);stroke-width:5;stroke-linecap:round}
.dial .mh{stroke:var(--strong);stroke-width:3;stroke-linecap:round}
.dial .sh{stroke:var(--acc-t);stroke-width:1.4;stroke-linecap:round}
.dial .hub{fill:var(--acc)}
.dial .lab{font:600 9.5px 'IBM Plex Mono',monospace;letter-spacing:.08em;fill:var(--acc-t)}
.inst .dig{display:flex;align-items:baseline;gap:8px}
.inst .dig b{font:600 30px/1 'IBM Plex Mono',monospace;color:var(--strong)}
.inst .dig span{font:500 13px 'IBM Plex Mono',monospace;color:var(--muted)}
.inst .stt{display:flex;align-items:center;gap:8px;font-size:14px;color:var(--body);text-align:center}
.inst .stt b{color:var(--strong);font-weight:600}
.inst .yt{font:500 12.5px 'IBM Plex Mono',monospace;color:var(--muted);text-align:center}
@media (max-width:960px){.ctx{grid-template-columns:1fr}.inst{max-width:340px}}
@media (max-width:760px){
  .ph .h1{font-size:32px}.rv{grid-template-columns:1fr}
  .ctx{padding:26px 20px;gap:28px}.ctx .h2{font-size:26px}
  .csheet{grid-template-columns:96px 1fr}
}
"""


def _ang(hm):
    """24-hour dial: midnight at the top, noon at the bottom (so Fajr to Asr is one clear arc)."""
    h, m = map(int, hm.split(":"))
    return (h + m / 60) * 15, m * 6


def dial(c):
    cx = cy = 105
    R = 92
    o = ['<svg class="dial" viewBox="0 0 210 210" role="img" aria-label="24-hour dial showing Dhaka time; the arc marks working hours, Fajr to Asr">',
         f'<circle class="face" cx="{cx}" cy="{cy}" r="{R}"/>']
    # working-hours arc (Fajr -> Asr) just inside the rim
    a1, _ = _ang(c["fajr"]); a2, _ = _ang(c["asr"])
    span = (a2 - a1) % 360
    r = R - 9
    p = lambda a, rr: (cx + rr * math.sin(math.radians(a)), cy - rr * math.cos(math.radians(a)))
    s1, s2 = p(a1, r), p(a2, r)
    o.append(f'<path class="work" d="M{s1[0]:.1f},{s1[1]:.1f} A{r},{r} 0 {1 if span > 180 else 0} 1 {s2[0]:.1f},{s2[1]:.1f}"/>')
    for k in range(48):          # a tick every 30 min, long tick every 3 h
        a = k * 7.5
        big = k % 6 == 0
        q1, q2 = p(a, R - 2), p(a, R - (12 if big else 6))
        o.append(f'<line class="tk{" b" if big else ""}" x1="{q1[0]:.1f}" y1="{q1[1]:.1f}" x2="{q2[0]:.1f}" y2="{q2[1]:.1f}"/>')
    for n, a in (('00', 0), ('06', 90), ('12', 180), ('18', 270)):
        q = p(a, R - 26)
        o.append(f'<text class="num" x="{q[0]:.1f}" y="{q[1]+4.5:.1f}" text-anchor="middle">{n}</text>')
    q = p(a1, R + 0.0)
    o.append(f'<text class="lab" x="{p(a1, r-18)[0]:.1f}" y="{p(a1, r-18)[1]+3:.1f}" text-anchor="middle">FAJR</text>')
    o.append(f'<text class="lab" x="{p(a2, r-18)[0]:.1f}" y="{p(a2, r-18)[1]+3:.1f}" text-anchor="middle">ASR</text>')
    ha, ma = _ang(c["now"])
    # hands turn at real speed from the build time (hour 24 h, minute 1 h, second 1 min per turn)
    o.append(f'<g style="transform-origin:{cx}px {cy}px;transform:rotate({ha:.1f}deg);animation:hHand 86400s linear infinite">'
             f'<line class="hh" x1="{cx}" y1="{cy+10}" x2="{cx}" y2="{cy-48}"/></g>')
    o.append(f'<g style="transform-origin:{cx}px {cy}px;transform:rotate({ma:.1f}deg);animation:mHand 3600s linear infinite">'
             f'<line class="mh" x1="{cx}" y1="{cy+14}" x2="{cx}" y2="{cy-70}"/></g>')
    o.append(f'<g style="transform-origin:{cx}px {cy}px;animation:sHand 60s steps(60) infinite">'
             f'<line class="sh" x1="{cx}" y1="{cy+18}" x2="{cx}" y2="{cy-80}"/></g>')
    o.append(f'<circle class="hub" cx="{cx}" cy="{cy}" r="5"/>')
    o.append("</svg>")
    kf = (f"@keyframes hHand{{from{{transform:rotate({ha:.1f}deg)}}to{{transform:rotate({ha+360:.1f}deg)}}}}"
          f"@keyframes mHand{{from{{transform:rotate({ma:.1f}deg)}}to{{transform:rotate({ma+360:.1f}deg)}}}}"
          "@keyframes sHand{from{transform:rotate(0deg)}to{transform:rotate(360deg)}}"
          "@media (prefers-reduced-motion:reduce){.dial g{animation:none!important}}")
    return "".join(o), kf


BTN_BRACKET = ('<a class="bkb" href="mailto:mdzaideng@gmail.com"><s></s><s></s><s></s><s></s><span>EMAIL ME</span><i>→</i></a>'
               '<a class="bkb" href="#"><s></s><s></s><s></s><s></s><span>DOWNLOAD CV</span><i>↓</i></a>')
BTN_PANEL = ('<div class="panel"><a class="pb p" href="mailto:mdzaideng@gmail.com"><b></b><span>EMAIL</span></a>'
             '<a class="pb" href="#"><b></b><span>CV</span></a><em>PRESS TO START</em></div>')
BTN_LEADER = ('<a class="ldr p" href="mailto:mdzaideng@gmail.com"><span>EMAIL ME</span><i></i></a>'
              '<a class="ldr" href="#"><span>DOWNLOAD CV</span><i></i></a>')


def proposed():
    c = H.clock_sample()
    d, kf = dial(c)
    status = (f'{SP.gear_icon()}<span><b>Working hours now</b> · replies today</span>' if c["on"]
              else '<span class="off2">○</span><span><b>Off hours</b> · replies after Fajr</span>')
    return kf, f'''
    <section class="sec" aria-labelledby="s-contact2">
      <div class="card ctx">
        <div>
          <div class="eb"><span class="ebn">06</span><span class="ebt">CONTACT</span><span class="ebl"></span></div>
          <h2 class="h2" id="s-contact2">Open to PhD positions and research collaborations.</h2>
          <div class="focus2"><span class="fc">Operations research</span><span class="fc">Ergonomics &amp; worker safety</span><span class="fc">Additive manufacturing</span><span class="fc open">+ your field · open to discuss</span></div>
          <div class="csheet">
            <span class="k">EMAIL</span><span><span class="em">mdzaideng@gmail.com</span><span class="cp2" title="Copy address">COPY</span></span>
            <span class="k">BASED IN</span><span>Dhaka, Bangladesh <em>· GMT+6</em></span>
            <span class="k">REPLIES</span><span>Fajr to Asr, Dhaka time <em>· today {c["fajr"]} to {c["asr"]}</em></span>
            <span class="k">PROFILES</span><span><a class="plk" href="#">LINKEDIN ↗</a><a class="plk" href="#">ORCID ↗</a><a class="plk" href="#">SCHOLAR ↗</a></span>
          </div>
          <div class="cact">{BTN_BRACKET}</div>
        </div>
        <div class="inst">
          <div class="ih"><span>LOCAL TIME · DHAKA</span><span>GMT+6</span></div>
          {d}
          <div class="dig"><b>{c["now"]}</b><span>DHAKA</span></div>
          <div class="stt">{status}</div>
          <div class="yt">YOUR TIME {c["visitor"]} · {c["diff"].upper()}</div>
        </div>
      </div>
    </section>'''


def body(now_html):
    global BTN_BRACKET
    kf, prop = proposed()
    return kf, f"""
  <main class="wrap" style="position:relative;z-index:1">
    <section class="ph">
      <div class="crumb">PROPOSAL / CONTACT SECTION · FOR REVIEW, NOT APPLIED</div>
      <h1 class="h1">Contact · now vs proposed</h1>
      <p class="lead">Same facts, clearer order: one main action, the email easy to copy, and the working-hours clock turned into a real instrument dial.</p>
      <div class="rv">
        <div><b>1</b>Heading said "MS / PhD", but the M.Sc. is already running. Proposed: PhD positions and research collaborations.</div>
        <div><b>2</b>"happy to talk" read like template copy, and the three areas sounded like the only ones. Proposed: three research-area boxes plus an open dashed slot for other fields.</div>
        <div><b>3</b>The email was small grey text. Proposed: first row of a contact table, with a COPY button.</div>
        <div><b>4</b>Three equal rounded buttons looked common. Proposed: square drawing-bracket buttons in one style with a dotted accent underline; LinkedIn moves to the profiles row.</div>
        <div><b>5</b>The right side was half empty and the pulsing dot is a template habit. Proposed: a 24-hour instrument dial (00 at the top, 12 at the bottom) with the Fajr to Asr arc, hands that turn, and the same turning gear as the hero.</div>
        <div><b>6</b>"Your time … behind" stays, computed from the visitor's clock on the live site.</div>
      </div>
    </section>
    <div class="row"><div class="cap">NOW</div>{now_html}</div>
    <div class="row"><div class="cap new">PROPOSED</div>{prop}</div>
    <div class="row"><div class="cap new">OPTION SET 1 · SHOWING YOU ARE OPEN TO OTHER FIELDS</div>
      <div class="opts3">
        <div class="o3 rec"><div class="ol">A · OPEN SLOT (USED ABOVE, RECOMMENDED)</div>
          <div class="focus2"><span class="fc">Operations research</span><span class="fc">Ergonomics &amp; worker safety</span><span class="fc">Additive manufacturing</span><span class="fc open">+ your field · open to discuss</span></div>
          <p>Three solid boxes are the research areas; the dashed box is an empty slot waiting for a new field. Says "open" without a sentence.</p></div>
        <div class="o3"><div class="ol">B · TABLE ROW</div>
          <div class="csheet"><span class="k">FOCUS</span><span>OR · ergonomics &amp; worker safety · additive mfg</span><span class="k">ALSO OPEN TO</span><span>Other fields, in industry or academia <em>· tell me what you have in mind</em></span></div>
          <p>Plain and direct, inside the contact table.</p></div>
        <div class="o3"><div class="ol">C · TOLERANCE</div>
          <div class="tol"><span>OR · ERGONOMICS · AM</span><b>±</b><span class="t2">OTHER FIELDS</span></div>
          <p>Engineering joke: the focus has a tolerance. A tooltip explains "other fields welcome". Clever, but needs the reader to get it.</p></div>
      </div>
    </div>
    <div class="row"><div class="cap new">OPTION SET 2 · BUTTONS THAT ARE NOT THE USUAL ROUNDED BOXES (HOVER THEM)</div>
      <div class="opts3">
        <div class="o3 rec"><div class="ol">1 · DRAWING BRACKETS (USED ABOVE, RECOMMENDED)</div>
          <div class="cact">{BTN_BRACKET}</div>
          <p>Both buttons now share one style (like Download CV) with a dotted accent line under the label. On hover the brackets open outwards, the arrow moves and the dotted line turns solid.</p></div>
        <div class="o3"><div class="ol">2 · CONTROL-PANEL BUTTONS</div>
          {BTN_PANEL}
          <p>Round industrial push buttons on a steel plate, like a machine panel. They press down on hover. Fun, matches the factory figures.</p></div>
        <div class="o3"><div class="ol">3 · LEADER LINES</div>
          <div class="cact col">{BTN_LEADER}</div>
          <p>Text with a drafting leader line and arrowhead. On hover the line extends. Quiet and very "drawing".</p></div>
      </div>
    </div>
  </main>
"""


def page(theme, title):
    html = H.page(theme, title)
    a0 = html.index('<section class="sec" aria-labelledby="s-contact">')
    b0 = html.index("</section>", a0) + len("</section>")
    now_html = html[a0:b0]
    kf, b = body(now_html)
    html = html.replace("<style>", "<style>" + CSS + kf, 1)
    a = html.index("  <!-- Hero: static page backdrop")
    e = html.index("  </main>") + len("  </main>")
    return html[:a] + b + html[e:]


if __name__ == "__main__":
    out = "/home/claude/zaid/project"
    for key, name in [("dark", "ContactProp"), ("dark_blue", "ContactPropBlue"), ("dark_green", "ContactPropGreen"),
                      ("light", "ContactPropLight"), ("light_blue", "ContactPropLightBlue"), ("light_green", "ContactPropLightGreen")]:
        open(f"{out}/{name}.dc.html", "w").write(page(key, f"Contact proposal · {key}"))
    open(f"{out}/ContactPropMobile.dc.html", "w").write(page("dark", "Contact proposal · Mobile"))
    print("contact proposal written")


# ---------------- round 2 (map + clock review), shown before applying to the home page ----------------
def page2(theme, title):
    import site_parts as SP
    html = H.page(theme, title)
    a0 = html.index('<section class="sec" aria-labelledby="s-contact">')
    a0 = html.rindex("<style>", 0, a0)          # keep the clock keyframes that sit just before the section
    b0 = html.index("</section>", a0) + len("</section>")
    new_html = html[a0:b0]
    body2 = f"""
  <main class="wrap" style="position:relative;z-index:1">
    <section class="ph">
      <div class="crumb">PROPOSAL / CONTACT · ROUND 2 · MAP + CLOCK · FOR REVIEW, NOT APPLIED</div>
      <h1 class="h1">Contact · map and clock review</h1>
      <div class="rv">
        <div><b>1</b>INDIA label sat on Bangladesh. Now it sits over Meghalaya, north of the border; MYANMAR moved inside Myanmar.</div>
        <div><b>2</b>No zoom buttons. On the canvas the map zooms in to Dhaka and back out on its own (18 s); lines stay thin and the scale bar changes 100 → 20 km.</div>
        <div><b>3</b>Real site: mouse-wheel / pinch zoom and drag (OpenStreetMap, streets at high zoom). Wheel zoom turns on after the first click on the map, so scrolling the page never gets stuck inside it.</div>
        <div><b>4</b>Auto update: Dhaka clock, Fajr/Asr times and working-hours status are recalculated every minute; YOUR TIME comes from the visitor's device.</div>
        <div><b>5</b>If you move city, one setting (city, lat/lon, time zone) moves the pin, clock and prayer times together. No live GPS tracking (privacy).</div>
        <div><b>6</b>Round 3: hint text under the map removed; clock hands run again (proposal board was dropping the clock animation); COPY is a real button; status on one line; "+ your field · open to discuss" in full.</div>
      </div>
    </section>
    <div class="row"><div class="cap new">PROPOSED · ROUND 2</div>{new_html}</div>
  </main>
"""
    html = html.replace("<style>", "<style>" + CSS, 1)
    a = html.index("  <!-- Hero: static page backdrop")
    e = html.index("  </main>") + len("  </main>")
    return html[:a] + body2 + html[e:]


if __name__ == "__main__":
    out = "/home/claude/zaid/project"
    for key, name in [("dark", "ContactProp"), ("dark_blue", "ContactPropBlue"), ("dark_green", "ContactPropGreen"),
                      ("light", "ContactPropLight"), ("light_blue", "ContactPropLightBlue"), ("light_green", "ContactPropLightGreen")]:
        open(f"{out}/{name}.dc.html", "w").write(page2(key, f"Contact proposal round 2 · {key}"))
    open(f"{out}/ContactPropMobile.dc.html", "w").write(page2("dark", "Contact proposal round 2 · Mobile"))
    print("contact proposal round 2 written")
