"""Weekly class routine for a term of the Education course map (proposal, Zaid 21 Nov 2026).
Redrawn from the department's routine sheets in the site's own style: only this batch's classes, teachers' full names
(linked to their KUET profile), sessional slots tinted. Hidden until the WEEKLY ROUTINE button in the term header
is clicked; then it opens in a full-screen viewer (CSS checkbox, same idea as the slideshow and video player).
Desktop: a Sunday to Thursday grid with only the time slots that term uses, tiffin and lunch breaks as thin bands.
Phone: one block per day, classes listed in time order.
Class prefix: rt."""
import edu_data as D

# time slots of the department routine: (start, end, kind); breaks sit between slot 3 and 4, and 6 and 7
SLOTS = [("8.00", "8.50"), ("8.50", "9.40"), ("9.40", "10.30"), ("10.40", "11.30"), ("11.30", "12.20"), ("12.20", "1.10"),
         ("2.30", "5.00"), ("10.40", "1.10")]      # 6: afternoon sessional, 7: morning lab over three periods
DAYS = ["SUN", "MON", "TUE", "WED", "THU"]
DAYN = {"SUN": "Sunday", "MON": "Monday", "TUE": "Tuesday", "WED": "Wednesday", "THU": "Thursday"}

SHORT = {"IPE 4227": "CAM and Robotics", "IPE 4059": "Project Management", "IPE 4027": "Computer Integrated Manufacturing",
         "IPE 4225": "Tool Engineering", "IPE 4219": "Human Factors and Safety",
         "IPE 4228": "CAM and Robotics", "IPE 4226": "Tool Engineering", "IPE 4220": "Human Factors"}

# term -> {day: {slot: (course code, [teacher keys] or None)}}. Slot 6 = 2.30 to 5.00 sessional, slot 7 = 10.40 to 1.10
# morning lab. None = initials not on the sheet's key: the course's own teachers (TEACH) are shown instead.
# Read from the department routine sheets Zaid sent on 21 Nov 2026 (only this batch's row of each sheet).
_ = None
ROUTINE = {
    # 1-1 · Class Routine 2019-2020 (1st Term), 1st year row. SSS Sikder, IA Idris Ali, RK Razia Khatun, SR Shahrear Roman,
    # MAY Abu Yousuf, MSH Saddam Hossain, MHR Habibur Rahman, MRZ Rafiquzzaman; MATH 1111 initials (Y, BR) are not
    # on any key, so its teachers come from the course folder.
    "1-1": {
        "SUN": {1: ("PHY 1111", ["sikder", "idris"]), 2: ("HUM 1111", ["razia"]), 3: ("CHEM 1111", ["yousuf", "saddam"]),
                4: ("MATH 1111", _), 5: ("IPE 1101", ["habibur"]), 6: ("IPE 1102", ["rafiq"])},
        "MON": {2: ("CHEM 1111", ["yousuf", "saddam"]), 3: ("MATH 1111", _), 4: ("HUM 1111", ["roman"]), 5: ("IPE 1101", ["rafiq", "habibur"])},
        "TUE": {0: ("MATH 1111", _), 2: ("PHY 1111", ["sikder", "idris"]), 7: ("PHY 1112", [])},
        "WED": {2: ("IPE 1101", ["rafiq"]), 3: ("CHEM 1111", ["yousuf", "saddam"]), 4: ("MATH 1111", _), 5: ("PHY 1111", ["sikder", "idris"]),
                6: ("IPE 1102", ["rafiq"])},
        "THU": {1: ("HUM 1111", ["roman", "razia"]), 2: ("PHY 1111", ["sikder", "idris"]), 7: ("CHEM 1112", [])},
    },
    # 2-1 · "2nd Year & 1st Term" sheet (initials only). ST Talapatra, MSI Saiful Islam, TH Tania Haque (HUM) and
    # M. M. Touhid Hossain (MATH), MA Amanullah, SI Shariful Islam, FIA Fahim Islam Anik, SA Shahabul Alam, EK Enamul Kabir, SR Selim Reza.
    "2-1": {
        "SUN": {2: ("CSE 2111", ["talapatra"]), 3: ("HUM 2111", ["tania"]), 4: ("ME 2111", _), 5: ("CSE 2111", ["saiful"])},
        "MON": {2: ("HUM 2111", ["amanullah"]), 3: ("CSE 2111", ["talapatra", "saiful"]), 4: ("ME 2111", ["msislam", "anik"]),
                5: ("EEE 2111", ["shahabul", "ekabir"]), 6: ("CSE 2112", [])},
        "TUE": {1: ("MATH 2111", ["selim"]), 2: ("EEE 2111", ["ekabir", "shahabul"]), 7: ("EEE 2112", []), 6: ("ME 2112", [])},
        "WED": {2: ("HUM 2111", ["tania", "amanullah"]), 3: ("ME 2111", ["msislam", "anik"]), 4: ("MATH 2111", ["touhid"]),
                5: ("EEE 2111", ["ekabir", "shahabul"]), 6: ("CSE 2112", [])},
        "THU": {0: ("EEE 2111", _), 1: ("MATH 2111", _), 2: ("ME 2111", ["msislam", "anik"]), 7: ("EEE 2112", [])},
    },
    # 2-2 · "2nd Year & 2nd Term" sheet with its key.
    "2-2": {
        "SUN": {2: ("ME 2213", ["shahidul", "raju"]), 4: ("EEE 2211", ["ekabir", "arefin"]), 6: ("ME 2216", ["msislam", "hasib"])},
        "MON": {2: ("EEE 2211", ["ekabir", "arefin"]), 3: ("ME 2215", ["faruk"]), 4: ("IPE 2229", ["hridoy", "nourin"]),
                5: ("IPE 2207", ["saiful", "farjana"]), 6: ("IPE 2200", ["parvez", "palash"])},
        "TUE": {1: ("EEE 2211", ["ekabir", "arefin"]), 2: ("ME 2215", ["dipayan"]), 3: ("ME 2213", ["shahidul", "raju"]),
                5: ("IPE 2229", ["hridoy", "nourin"]), 6: ("EEE 2212", ["ekabir", "tawabur"])},
        "WED": {2: ("ME 2213", ["shahidul", "raju"]), 3: ("ME 2215", ["faruk"]), 4: ("ME 2215", ["dipayan"]),
                5: ("IPE 2207", ["saiful", "farjana"]), 6: ("ME 2214", ["shahidul", "ridwan"])},
        "THU": {4: ("IPE 2229", ["hridoy", "nourin"]), 5: ("IPE 2207", ["saiful", "farjana"]), 6: ("ME 2216", ["msislam", "hasib"])},
    },
    # 3-1 · "3rd Year 1st Term" sheet with its key (MAW = Md. Abdul Wakil).
    "3-1": {
        "SUN": {1: ("IPE 3115", ["ridwan"]), 2: ("ME 3111", ["wakil"]), 4: ("IPE 3105", ["farjana"]), 5: ("IPE 3103", ["farjana"]),
                6: ("IPE 3100", ["saiful", "ismail"])},
        "MON": {2: ("ME 3111", ["zahir"]), 3: ("IPE 3115", ["nourin"]), 4: ("IPE 3119", ["palash"]), 6: ("IPE 3100", ["saiful", "ismail"])},
        "TUE": {2: ("ME 3111", ["zahir", "wakil"]), 3: ("IPE 3119", ["kibria"]), 4: ("IPE 3105", ["kibria", "farjana"]),
                5: ("IPE 3103", ["rafiq"]), 6: ("IPE 3104", ["rafiq", "farjana"])},
        "WED": {2: ("IPE 3115", ["nourin", "ridwan"]), 3: ("IPE 3103", ["rafiq", "farjana"]), 4: ("IPE 3105", ["kibria"]),
                5: ("IPE 3119", ["kibria", "palash"]), 6: ("IPE 3106", ["kibria", "farjana"])},
        "THU": {7: ("IPE 3106", ["kibria", "farjana"]), 6: ("ME 3112", ["zahir", "wakil"])},
    },
    # 3-2 · Class Routine 2021-22 (2nd Term), 3rd year row (classes from 20 Aug 2023). MNS Nazma Sultana, AS Asef Shahriar,
    # TA Tanvir Anzum, JZ Julfiker Zahid.
    "3-2": {
        "SUN": {2: ("IPE 3205", ["rafiq", "asef"]), 3: ("IPE 3217", ["saiful", "farjana"]), 4: ("IPE 3221", ["kibria", "farjana"]),
                5: ("IPE 3219", ["kibria", "nsultana"]), 6: ("IPE 3206", ["rafiq", "asef"])},
        "MON": {3: ("IPE 3217", ["saiful", "farjana"]), 4: ("IPE 3219", ["kibria", "nsultana"]), 5: ("IPE 3205", ["rafiq", "asef"]),
                6: ("IPE 3222", ["kibria", "farjana"])},
        "TUE": {1: ("IPE 3223", ["anzum", "zahid"]), 4: ("IPE 3217", ["saiful", "farjana"]), 5: ("IPE 3219", ["kibria", "nsultana"]),
                6: ("IPE 3220", ["kibria", "nsultana"])},
        "WED": {3: ("IPE 3221", ["kibria", "farjana"]), 4: ("IPE 3223", ["anzum", "zahid"]), 5: ("IPE 3205", ["rafiq", "asef"]),
                6: ("IPE 3218", ["saiful", "farjana"])},
        "THU": {3: ("IPE 3217", ["saiful", "farjana"]), 4: ("IPE 3223", ["anzum", "zahid"]), 5: ("IPE 3221", ["kibria", "farjana"]),
                6: ("IPE 3200", ["palash", "anzum"])},
    },
    # 4-1 · "4th Year 1st Term" sheet with its key (MHRM = Harun-Or-Rashid Mollah).
    "4-1": {
        "SUN": {2: ("IPE 4129", ["zahid"]), 3: ("IPE 4019", ["ismail"]), 4: ("IPE 4109", ["saiful", "ridwan"]), 5: ("IPE 4029", ["zahid"])},
        "MON": {3: ("IPE 4129", ["zahid"]), 4: ("IPE 4125", ["farjana"]), 5: ("IPE 4109", ["saiful"]), 6: ("IPE 4126", ["talapatra", "hrashid"])},
        "TUE": {3: ("IPE 4125", ["talapatra", "farjana"]), 4: ("IPE 4029", ["irfan"]), 5: ("IPE 4109", ["ridwan"]), 6: ("IPE 4110", ["saiful", "ridwan"])},
        "WED": {4: ("IPE 4129", ["anzum"]), 5: ("IPE 4019", ["palash"]), 6: ("IPE 4126", ["talapatra", "hrashid"])},
        "THU": {2: ("IPE 4029", ["irfan", "zahid"]), 3: ("IPE 4125", ["talapatra"]), 4: ("IPE 4129", ["anzum"]), 5: ("IPE 4019", ["palash", "ismail"])},
    },
    # 4-2 · "4th Year 2nd Term" sheet (Jan 2025). JHA Jahid Hasan Ashik, PS Palash Saha, THI Tanjid Hossen Irfan, ST Talapatra, MGK Kibria.
    "4-2": {
        "SUN": {3: ("IPE 4227", ["asef"]), 5: ("IPE 4059", ["palash"])},
        "MON": {3: ("IPE 4027", ["rafiq", "ashik"]), 4: ("IPE 4059", ["palash", "irfan"]), 5: ("IPE 4225", ["asef"]),
                6: ("IPE 4228", ["asef", "ashik"])},
        "TUE": {2: ("IPE 4227", ["asef", "ashik"]), 3: ("IPE 4225", ["talapatra", "asef"]), 4: ("IPE 4219", ["palash"]),
                5: ("IPE 4027", ["ashik"])},
        "WED": {3: ("IPE 4219", ["kibria"]), 4: ("IPE 4225", ["talapatra"]), 5: ("IPE 4059", ["irfan"]),
                6: ("IPE 4226", ["talapatra", "asef"])},
        "THU": {3: ("IPE 4227", ["ashik"]), 4: ("IPE 4027", ["rafiq"]), 5: ("IPE 4219", ["kibria", "palash"]),
                6: ("IPE 4220", ["kibria", "palash"])},
    },
}
TEACHERS_ONLY = {"1-2"}   # no class routine kept for this term: the button opens the course and teacher list only


import content_io as _C
globals().update(_C.load_routines())   # real site: routines from content/routines.yml

AREA = {c[1]: c[3] for c in D.COURSES}

CSS = """
/* ===== weekly routine (prefix rt) ===== */
.rtb{height:30px!important;padding:0 11px!important;font-size:10.5px!important;gap:7px!important;cursor:pointer;flex:none}
.rtb span{border-bottom:0!important;padding-bottom:0!important}
.rtb:hover,.rtb:hover span,.rtb:hover i{color:var(--acc-t)!important}   /* label and arrow take the theme colour on hover */
.rtb:hover i{transform:translate(2px,-2px)}
.etb .eth.rth2{flex-direction:row;align-items:center;justify-content:space-between;gap:10px}
.etb .eth.rth2>div{display:flex;flex-direction:column;gap:3px;min-width:0}
@media (max-width:400px){.etb .eth.rth2{flex-wrap:wrap}}
@media (max-width:760px){.eb .rtb{display:none!important}}
.rtc{position:fixed;top:0;left:0;width:1px;height:1px;opacity:0;pointer-events:none;margin:0}
.rtv{display:none;position:fixed;inset:0;z-index:400;align-items:center;justify-content:center;padding:40px}
.rtc:checked+.rtv{display:flex}
.rtv>.rtk{position:absolute;inset:0;background:rgba(8,10,14,.86);cursor:zoom-out}
.rtp{position:relative;z-index:1;width:min(1180px,100%);max-height:calc(100vh - 80px);overflow:auto;background:var(--bg);font-family:Inter,system-ui,sans-serif;text-align:left;border:1px solid var(--line2);border-radius:12px;padding:22px 24px 18px;box-shadow:0 24px 70px rgba(0,0,0,.45)}
.rth{display:flex;align-items:flex-start;justify-content:space-between;gap:16px;padding-bottom:14px;border-bottom:1px solid var(--line)}
.rth b{display:block;font:600 11px 'IBM Plex Mono',monospace;letter-spacing:.12em;color:var(--acc-t)}
.rth h3{margin:4px 0 0;font:600 20px/1.25 'Space Grotesk',sans-serif;color:var(--strong)}
.rth p{margin:4px 0 0;font-size:13px;color:var(--muted)}
.rtx{flex:none;font:600 11px 'IBM Plex Mono',monospace;letter-spacing:.12em;color:var(--muted);cursor:pointer;padding:6px 8px;border:1px solid var(--line2);border-radius:6px}
.rtx:hover{color:var(--strong);border-color:var(--muted)}
.rtgw{position:relative;margin-top:16px;border:1px solid var(--line2);border-radius:10px;overflow-x:auto;overscroll-behavior-x:contain;-webkit-overflow-scrolling:touch;
  background:linear-gradient(to left,var(--bg) 40%,transparent) right/34px 100% no-repeat local,
             radial-gradient(farthest-side at 100% 50%,rgba(0,0,0,.28),transparent) right/14px 100% no-repeat scroll}   /* a soft shadow on the right while more of the week is off screen */
.rtg{display:grid;gap:0;width:min-content;min-width:100%}   /* as wide as the week needs, so the sticky day column holds while scrolling */
.rtg>.rtt{padding:9px 12px;background:var(--surface2);border-bottom:1px solid var(--line2);font:600 10px 'IBM Plex Mono',monospace;letter-spacing:.06em;color:var(--muted);line-height:1.3}
.rtg>.rtt b{display:block;font-size:11.5px;color:var(--strong);letter-spacing:.04em}
.rtg>.rtd{display:flex;align-items:center;padding-left:12px;border-top:1px solid var(--line);background:var(--surface2);font:600 11px 'IBM Plex Mono',monospace;letter-spacing:.12em;color:var(--strong)}
.rtg>.rtt:nth-child(1){border-bottom-color:var(--line2)}
.rtg>.rtt:nth-child(1),.rtg>.rtd{position:sticky;left:0;z-index:3;background:linear-gradient(var(--surface2),var(--surface2)) var(--bg);border-right:1px solid var(--line2)}  /* days stay in view while the week scrolls sideways */
.rtgw{container-type:scroll-state}
.rtsw{display:none;position:sticky;left:0;width:max-content;padding:8px 12px;font:600 10px 'IBM Plex Mono',monospace;letter-spacing:.12em;color:var(--muted)}
@container scroll-state(scrollable: inline){.rtsw{display:block}}   /* the hint shows only while part of the week is off screen */
.rtg>.rtbr{display:flex;align-items:center;justify-content:center;border-left:1px solid var(--line);background:repeating-linear-gradient(135deg,var(--surface2) 0 5px,transparent 5px 10px);
  font:600 9px 'IBM Plex Mono',monospace;letter-spacing:.24em;color:var(--muted);writing-mode:vertical-rl;transform:rotate(180deg)}
.rte{min-height:86px;border-top:1px solid var(--line);border-left:1px solid var(--line)}
.rtcl{position:relative;display:flex;flex-direction:column;gap:3px;min-height:86px;padding:11px 12px 10px;border-top:1px solid var(--line);border-left:1px solid var(--line);
  transition:background .25s ease,opacity .25s ease}
.rtcl:before{content:"";position:absolute;left:-1px;top:-1px;bottom:0;width:2px;background:var(--acc);transform:scaleY(0);transform-origin:top;transition:transform .3s ease}
.rtcl code{font:600 10px 'IBM Plex Mono',monospace;letter-spacing:.04em;color:var(--muted);transition:color .25s ease}
.rtcl span{font-size:13px;font-weight:500;line-height:1.3;color:var(--strong)}
.rtcl small{display:flex;flex-direction:column;gap:1px;margin-top:auto;padding-top:5px;font-size:11px;line-height:1.35;color:var(--muted)}
.rtcl small a{white-space:nowrap;color:var(--muted);border-bottom:1px dotted var(--line2);align-self:flex-start}
.rtcl small a:hover{color:var(--acc-t);border-bottom-color:var(--acc-t)}
.rtcl:hover,.rtcl.on{background:var(--surface2)}
.rtcl:hover:before,.rtcl.on:before{transform:scaleY(1)}
.rtcl:hover code,.rtcl.on code{color:var(--acc-t)}
.rtcl.rts code:after{content:" · SESSIONAL";font-weight:500;color:var(--muted);letter-spacing:.06em}
.rtf{display:flex;flex-wrap:wrap;justify-content:space-between;gap:8px 18px;margin-top:14px;padding-top:12px;border-top:1px solid var(--line);font-size:12px;color:var(--muted)}


.rtpv .rtp{max-height:none;box-shadow:none}
@media (max-width:760px){
  .rtv{padding:12px 8px}
  .rtp{padding:16px 14px 14px;max-height:calc(100vh - 24px)}
  .rth h3{font-size:17px}
}
.rtp.wide{width:min(1500px,100%)}
.rtp.wide .rtcl{padding:10px 9px 9px}
.rtp.wide .rtcl small{font-size:10.5px}
@media (max-width:760px){
  .rtcl{min-height:80px;padding:9px 10px 8px}
  .rtcl span{font-size:12.5px}
  .rtcl small{font-size:10.5px}
  .rtg>.rtd{padding-left:9px;font-size:10px}
}
.rtlg.only{margin-top:4px;border-top:0}
"""


def _names(keys):
    return "".join(f'<a href="{D.T[k][1]}" target="_blank" rel="noopener">{D.T[k][0]}</a>' for k in keys)


def _key(code):
    """Theory course and its sessional share one key, so pointing at one lights up both across the week."""
    p, n = code.split()
    n = int(n)
    return f"k{n - 1 if n % 2 == 0 else n}"


TITLE = {c[1]: c[2].replace(" Sessional", "") for c in D.COURSES}


def _title(code):
    return SHORT.get(code, TITLE.get(code, code))


def _who(code, keys):
    """Teachers of one class: the sheet's initials, or the course's own teachers when the sheet's key lacks them."""
    return _names(D.TEACH.get(code, []) if keys is None else keys)


def _cell(code, keys, slot, span=""):
    ses = slot >= 6
    return (f'<div class="rtcl {_key(code)}{" rts" if ses else ""}"{span}><code>{code}</code>'
            f'<span>{_title(code)}</span><small>{_who(code, keys)}</small></div>')


def _hover_css(term):
    """Point at a class: the same course (and its sessional) lights up across the week, the rest steps back."""
    ks = sorted({_key(c) for d in ROUTINE[term].values() for c, _ in d.values()})
    g = f"#rtg-{term}"
    return ("<style>" + "".join(f"{g}:has(.{k}:hover) .rtcl:not(.{k}){{opacity:.38}}{g}:has(.{k}:hover) .{k}{{background:var(--surface2)}}"
                                f"{g}:has(.{k}:hover) .{k}:before{{transform:scaleY(1)}}{g}:has(.{k}:hover) .{k} code{{color:var(--acc-t)}}" for k in ks)
            + "</style>")


def stats(term):
    r = ROUTINE[term]
    lec = sum(1 for d in r.values() for s in d if s < 6)
    ses = sum(1 for d in r.values() for s in d if s >= 6)
    return lec, ses


def panel(term, label, period):
    """The routine card itself (used inside the viewer and, on the proposal board, shown open)."""
    r = ROUTINE[term]
    used = {s for d in r.values() for s in d}
    if 7 in used:                                    # a morning lab spans the three periods 10.40 to 1.10
        used |= {3, 4, 5}
    used = sorted(used - {7})
    cols, head = [], '<div class="rtt"></div>'
    for s in used:
        if s >= 3 and "T" not in cols and any(c < 3 for c in used):
            cols.append("T")
        if s == 6:
            cols.append("L")
        cols.append(s)
    tmpl = " ".join("26px" if c in ("T", "L") else "minmax(min-content,1fr)" for c in cols)   # a column is never narrower than its longest teacher name
    for c in cols:
        head += '<div class="rtt"></div>' if c in ("T", "L") else f'<div class="rtt"><b>{SLOTS[c][0]}</b>to {SLOTS[c][1]}</div>'
    body = ""
    pos = {c: j + 2 for j, c in enumerate(cols)}      # grid column of each slot or break (column 1 = day)
    for i, d in enumerate(DAYS):
        body += f'<div class="rtd">{d}</div>'
        for c in cols:
            if c in ("T", "L"):
                if i == 0:
                    body += f'<div class="rtbr" style="grid-column:{pos[c]};grid-row:2 / span {len(DAYS)}">{"TIFFIN" if c == "T" else "LUNCH"}</div>'
                continue
            if 7 in r[d] and c in (4, 5):
                continue
            if 7 in r[d] and c == 3:
                body += _cell(r[d][7][0], r[d][7][1], 7, ' style="grid-column:span 3"')
                continue
            body += _cell(r[d][c][0], r[d][c][1], c) if c in r[d] else '<div class="rte"></div>'
    nslot = sum(1 for c in cols if c not in ("T", "L"))
    grid = (_hover_css(term) + f'<div class="rtgw"><div class="rtg" id="rtg-{term}" style="grid-template-columns:58px {tmpl}">'
            f'{head}{body}</div><div class="rtsw" id="rtsw-{term}">SWIPE SIDEWAYS FOR THE WHOLE WEEK →</div></div>')
    lec, ses = stats(term)
    wide = " wide" if sum(1 for c in cols if c not in ("T", "L")) >= 6 else ""
    return (f'<div class="rtp{wide}"><div class="rth"><div><b>{label} · ROUTINE &amp; TEACHERS</b><h3>Classes, Sunday to Thursday</h3>'
            f'<p>{period.replace(" *", "")} · {lec} lectures of 50 minutes and {ses} sessionals of 2.5 hours a week</p></div>'
            f'<label class="rtx" for="rt-{term}">CLOSE ×</label></div>{grid}'
            f'{legend(term)}'
            f'<div class="rtf"><span>Point at a class to see that course across the week. Redrawn from the department class routine, and teacher names open their KUET profile.</span>'
            f'</div></div>')


def header(term, label, period):
    """Term header of the course map with the WEEKLY ROUTINE button on the right."""
    return f'<div class="eth rth2"><div><b>{label}</b><span>{period}</span></div>{button(term)}</div>'


def button(term):
    if term in ROUTINE:
        return (f'<label class="bkb rtb" for="rt-{term}" title="Show the class routine and the teachers"><s></s><s></s><s></s><s></s>'
                f'<span>ROUTINE &amp; TEACHERS</span><i>↗</i></label>')
    if term in TEACHERS_ONLY:
        return (f'<label class="bkb rtb" for="rt-{term}" title="Show the teachers of this term"><s></s><s></s><s></s><s></s>'
                f'<span>TEACHERS</span><i>↗</i></label>')
    return ""


def panel_teachers(term, label, period):
    """Terms without a kept routine: only the courses and their teachers."""
    return (f'<div class="rtp"><div class="rth"><div><b>{label} · TEACHERS</b><h3>Courses and teachers</h3>'
            f'<p>{period.replace(" *", "")} · the class routine of this term was not kept</p></div>'
            f'<label class="rtx" for="rt-{term}">CLOSE ×</label></div>{legend(term).replace('<div class="rtlg"><b>COURSES AND TEACHERS</b>', '<div class="rtlg only">', 1)}'
            f'<div class="rtf"><span>Teacher names open their KUET profile.</span></div></div>')


def viewer(term, label, period):
    """Checkbox + full-screen viewer; goes before </body> so it sits above the sticky header."""
    return (f'<input type="checkbox" class="rtc" id="rt-{term}" tabindex="-1" aria-hidden="true">'
            f'<div class="rtv" role="dialog" aria-label="{label} weekly routine"><label class="rtk" for="rt-{term}" aria-hidden="true"></label>'
            f'{panel(term, label, period) if term in ROUTINE else panel_teachers(term, label, period)}</div>')


def viewers():
    """All viewers of the Education course map."""
    return "".join(viewer(k, l, p) for k, l, p in D.TERMS if k in ROUTINE or k in TEACHERS_ONLY)


def inject(html, viewers):
    """Put the viewers inside the theme wrapper (div.zh holds the colour variables), after <main>, so they get the
    theme colours and still sit above the sticky header."""
    if not viewers:
        return html
    end = html.rindex("</x-dc>") if "</x-dc>" in html else html.rindex("</body>")
    i = html.rindex("</div>", 0, end)
    return html[:i] + viewers + html[i:]


# ---------- courses and teachers (shown under both versions, so the course map can drop its TAUGHT BY lines) ----------
LEG_CSS = """
.rtlg{margin-top:16px;padding-top:12px;border-top:1px solid var(--line)}
.rtlg>b{display:block;font:600 10px 'IBM Plex Mono',monospace;letter-spacing:.12em;color:var(--acc-t);margin-bottom:8px}
.rtlg>div{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:6px 22px}
.rtlr{display:grid;grid-template-columns:88px minmax(0,1fr);gap:8px;align-items:baseline;padding:5px 0;border-bottom:1px dashed var(--line)}
.rtlr code{font:600 10.5px 'IBM Plex Mono',monospace;color:var(--muted);display:flex;align-items:center;gap:6px;white-space:nowrap}
.rtlr code i{width:9px;height:9px;border-radius:2px;background:var(--rtc,var(--muted));flex:none}
.rtlr span{font-size:13px;color:var(--strong);line-height:1.35}
.rtlr small{display:flex;flex-wrap:wrap;column-gap:14px;font-size:11.5px;color:var(--muted);margin-top:2px}
.rtlr small a{white-space:nowrap;color:var(--muted);border-bottom:1px dotted var(--line2)}
.rtlr small a:hover{color:var(--acc-t);border-bottom-color:var(--acc-t)}
@media (max-width:760px){.rtlg>div{grid-template-columns:1fr}}
"""


def legend(term):
    rows = ""
    for t, code, title, area, kind, topics in D.COURSES:
        if t != term:
            continue
        keys = D.TEACH.get(code) or (D.TEACH.get(f"{code.split()[0]} {int(code.split()[1]) - 1}", []) if kind == "lab" else [])
        rows += (f'<div class="rtlr"><code>{code}</code><span>{title}'
                 + (f'<small>{_names(keys)}</small>' if keys else "") + '</span></div>')
    return f'<div class="rtlg"><b>COURSES AND TEACHERS</b><div>{rows}</div></div>'


# ---------- version 3: by course. One row per course (with its teachers), the days across, the class times in the cells ----------
V3_CSS = """
.rt3{margin-top:16px;display:grid;grid-template-columns:minmax(0,2.3fr) repeat(5,minmax(0,1fr)) 118px;border:1px solid var(--line2);border-radius:10px;overflow:hidden}
.rt3>div{padding:9px 10px;border-top:1px solid var(--line);display:flex;flex-direction:column;justify-content:center;gap:4px;min-width:0}
.rt3>.h{border-top:0;background:var(--surface2);font:600 10px 'IBM Plex Mono',monospace;letter-spacing:.12em;color:var(--muted);padding:8px 10px}
.rt3>.d{border-left:1px dashed var(--line);align-items:flex-start}
.rt3>.n{border-left:1px dashed var(--line);font:600 11px 'IBM Plex Mono',monospace;color:var(--strong);align-items:flex-start;white-space:nowrap}
.rt3>.n small{font:500 10px 'IBM Plex Mono',monospace;color:var(--muted)}
.rt3 .c code{font:600 10.5px 'IBM Plex Mono',monospace;color:var(--muted)}
.rt3 .c b{font:500 13.5px/1.3 Inter,system-ui,sans-serif;color:var(--strong)}
.rt3 .c small{display:flex;flex-wrap:wrap;column-gap:12px;font-size:11.5px;color:var(--muted)}
.rt3 .c small a{white-space:nowrap;color:var(--muted);border-bottom:1px dotted var(--line2)}
.rt3 .c small a:hover{color:var(--acc-t);border-bottom-color:var(--acc-t)}
.rt3 .t{display:inline-flex;flex-direction:column;padding:4px 7px;border-radius:6px;border:1px solid var(--line2);background:var(--bg);font:600 11px 'IBM Plex Mono',monospace;color:var(--strong);white-space:nowrap}
.rt3 .t small{font:500 9.5px 'IBM Plex Mono',monospace;color:var(--muted)}
.rt3 .s .t,.rt3 .t.s{border-color:var(--acc-t);background:var(--acc-soft)}
.rt3>.sg{grid-column:1/-1;background:var(--surface2);font:600 9.5px 'IBM Plex Mono',monospace;letter-spacing:.12em;color:var(--muted);padding:6px 10px}
.rt3>.x{color:var(--muted);font-size:12px;align-items:flex-start}
.rt3w{display:none}
@media (max-width:760px){
  .rt3{display:none}
  .rt3w{display:flex;flex-direction:column;gap:8px;margin-top:12px}
  .rt3w>div{padding:10px 12px;border:1px solid var(--line2);border-radius:8px;background:var(--bg)}
  .rt3w>div.s{border-color:var(--acc-t);background:var(--acc-soft)}
  .rt3w code{font:600 10.5px 'IBM Plex Mono',monospace;color:var(--muted)}
  .rt3w b{display:block;font:500 14px/1.3 Inter,system-ui,sans-serif;color:var(--strong);margin-top:2px}
  .rt3w small{display:flex;flex-wrap:wrap;column-gap:12px;font-size:11.5px;color:var(--muted);margin-top:3px}
  .rt3w small a{white-space:nowrap;color:var(--muted);border-bottom:1px dotted var(--line2)}
  .rt3w p{display:flex;flex-wrap:wrap;gap:6px;margin:8px 0 0}
  .rt3w p span{font:600 10.5px 'IBM Plex Mono',monospace;color:var(--strong);padding:3px 7px;border:1px solid var(--line2);border-radius:5px;white-space:nowrap}
}
"""


def _slots_of(term, code):
    """[(day, slot index)] of one course in the week."""
    return [(d, s) for d in DAYS for s, (c, k) in sorted(ROUTINE[term][d].items()) if c == code]


def panel3(term, label, period, close_id=None):
    items = [c for c in D.COURSES if c[0] == term]
    theory = [c for c in items if c[4] == ""]
    other = [c for c in items if c[4] != ""]
    grid = '<div class="h">COURSE AND TEACHERS</div>' + "".join(f'<div class="h">{d}</div>' for d in DAYS) + '<div class="h">A WEEK</div>'
    cards = ""

    def row(c):
        code, title, kind = c[1], c[2], c[4]
        ses = kind == "lab"
        sl = _slots_of(term, code)
        who = _names(D.TEACH.get(code, []))
        out = (f'<div class="c{" s" if ses else ""}"><code>{code}</code><b>{title.replace(" Sessional", "")}</b>'
               f'<small>{who}</small></div>')
        for d in DAYS:
            ts = "".join(f'<span class="t{" s" if s == 6 else ""}">{SLOTS[s][0]}<small>to {SLOTS[s][1]}</small></span>' for dd, s in sl if dd == d)
            out += f'<div class="d">{ts}</div>'
        if sl:
            lec = sum(1 for _, s in sl if s < 6)
            ss = sum(1 for _, s in sl if s == 6)
            out += f'<div class="n">{f"{lec} × 50 min" if lec else ""}{f"{ss} × 2.5 h" if ss else ""}<small>{"lectures" if lec else "lab"}</small></div>'
        else:
            out += '<div class="n"><small>no fixed time</small></div>'
        chips = "".join(f'<span>{d} {SLOTS[s][0]}</span>' for d, s in sl) or '<span>no fixed class time</span>'
        card = (f'<div class="{"s" if ses else ""}"><code>{code}</code><b>{title.replace(" Sessional", "")}</b><small>{who}</small>'
                f'<p>{chips}</p></div>')
        return out, card

    for c in theory:
        a, b = row(c)
        grid += a
        cards += b
    if other:
        grid += '<div class="sg">SESSIONAL, LAB AND THESIS</div>'
        for c in other:
            a, b = row(c)
            grid += a
            cards += b
    lec, ses = stats(term)
    cid = close_id or f"rt-{term}"
    return (f'<div class="rtp"><div class="rth"><div><b>{label} · ROUTINE &amp; TEACHERS</b><h3>Each course, its teachers and its class times</h3>'
            f'<p>{period} · {lec} lectures of 50 minutes and {ses} sessionals of 2.5 hours a week</p></div>'
            f'<label class="rtx" for="{cid}">CLOSE ×</label></div>'
            f'<div class="rt3">{grid}</div><div class="rt3w">{cards}</div>'
            f'<div class="rtf"><span>Redrawn from the department class routine. Teacher names open their KUET profile.</span>'
            f'</div></div>')


def viewer3(term, label, period):
    vid = f"rt3-{term}"
    return (f'<input type="checkbox" class="rtc" id="{vid}" tabindex="-1" aria-hidden="true">'
            f'<div class="rtv" role="dialog" aria-label="{label} weekly routine, by course"><label class="rtk" for="{vid}" aria-hidden="true"></label>'
            f'{panel3(term, label, period, vid)}</div>')
