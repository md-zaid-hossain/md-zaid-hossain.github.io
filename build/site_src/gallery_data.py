"""Gallery page content (proposal v2, 20 Nov 2026). Stories from Zaid's LinkedIn posts, his story cards and his answers.
Each album: key, code, title, place, date, story, photos [(stem or /_blob/ src, caption, crop position)],
optional ratio (thumbnail aspect, default 4/3) and credit.
Images: photos/gallery/<stem>.webp (originals listed in photos/gallery/SOURCES.json); GAL_IMG maps stem -> /_blob/<id>."""
import json, os
import exp_data as X

P = lambda key, caps, pos="50% 45%": [(f"{key}-{i}", c, pos) for i, c in enumerate(caps, 1)]

CHAPTERS = [
    ("pro", "PROFESSIONAL", "Sessions and seminars", [
        dict(key="d2", code="GAL-D1", title="Special session on BRACU FabLab", place="BRAC University Research Conference 2026 · Central Auditorium, Dhaka",
             date="14 NOV 2026",
             story="The BRAC University Silver Jubilee Research Conference 2026 held a special session on BRACU FabLab, with the "
                   "Project Director of the HEAT Project, UGC, as chief guest. FabLab teams from the universities funded under HEAT "
                   "talked about building a FabLab network across universities. I attended with the BUET FabLab team, at the "
                   "invitation of BRACU FabLab.",
             credit="Photos: BRACU FabLab",
             photos=P("d2", ["Guests, speakers and panelists on stage", "BRACU FabLab: progress report", "The BRACU FabLab booth",
                             "Panel: building a FabLab network across universities", "A token of appreciation",
                             "Panel: FabLab collaboration", "Attending the session with the BUET FabLab team",
                             "Session discussion with the FabLab teams", "Networking after the session",
                             "Guests at the BRACU FabLab booth"])),
        dict(key="d1", code="GAL-D2", title="CAD and CAM for 4IR seminar", place="IAT, BUET", date="SEP 2026",
             story="\"CAD and CAM for 4IR: 3D Modelling and Smart Manufacturing\", a seminar organised by IAT, BUET, "
                   "where I now work as FabLab Program Engineer. I attended the sessions.",
             photos=P("d1", ["A talk at the seminar", "Speakers and guests", "Session in progress", "The audience",
                             "The venue before the start"], "50% 50%")),
    ]),
    ("making", "MAKING", "Hands on the machines", [
        dict(key="a1", code="GAL-A1", title="Bringing the CR-10 Smart back to life", place="FabLab KUET", date="MAY 2025",
             story="The lab's Creality CR-10 Smart had been down for a long time with a damaged thermistor and extruder. "
                   "A compatible extruder set came from China through KUET alumnus Nahid Al Mahmud. I replaced the parts, "
                   "rewired the connectors, aligned the hotend with the Bowden tube and tested it until it printed smoothly again.",
             photos=P("a1", ["The new extruder set, fan and wiring, unpacked", "The old wiring inside the printer, traced connector by connector",
                             "Fitting the new extruder on the carriage", "Lining up the hotend with the Bowden tube",
                             "Final checks before the first test print"], "50% 35%")),
        dict(key="a2", code="GAL-A2", title="From CAD to a printed part", place="FabLab KUET", date="2024 TO 2025",
             story="Small parts I designed in SOLIDWORKS, sliced, printed on the lab's Creality CR-10 Smart and Ultimaker 3 Extended, "
                   "then finished by hand: a quick acting knob, a vice for accurate alignment, a hand spinning top and a 3-2-1 pin locator.",
             photos=P("a2", ["Quick acting knob, the finished part on its drawing", "The knob printing on the CR-10 Smart",
                             "Breaking away the support material", "Knob and screw after post-processing",
                             "Vice for accurate alignment, assembled", "The vice from above: screw, sliding jaw and handle",
                             "Hand spinning top, printed on the Ultimaker", "The top on the build plate, before the supports came off",
                             "First layers going down", "3-2-1 pin locator for the Tool Engineering sessional"], "50% 50%")),
        dict(key="a5", code="GAL-A3", title="First part on the HAAS VF-2", place="Dept. of IEM, KUET", date="SEP 2025",
             story="The department installed a HAAS VF-2 milling machine and a CNC table lathe, followed by a five-day hands-on "
                   "training with HAAS, led by Mr. Sunil Patil. I modelled a test part, planned its toolpaths in Fusion CAM, posted "
                   "the NC program and, for the first time, saw my own design cut in aluminium.",
             photos=[(src, f"{step.capitalize()}: {cap}", "50% 50%") for src, step, cap in X.CNC_PHOTOS]),
        dict(key="a3", code="GAL-A4", title="Certificate day at FabLab KUET", place="FabLab KUET", date="SEP 2025",
             story="FabLab KUET's farewell and certificate ceremony for its student operators. I received the Certificate of "
                   "Achievement for my year as a student operator (Mar 2024 to Mar 2025), and stayed on as a volunteer until Sep 2025.",
             photos=P("a3", ["Receiving the student operator certificate", "Certificate holders with the FabLab team",
                             "Student operators of FabLab KUET"], "50% 40%")),
        dict(key="a4", code="GAL-A5", title="Setting up the CAD/CAM and Robotics Lab", place="Dept. of IEM, KUET", date="NOV 2024",
             story="The department's CAD/CAM and Robotics Lab got new computers. My teacher asked me to set them up and install "
                   "and configure the CAD software on each one, since installing and fixing engineering software is something I do well.",
             photos=P("a4", ["Bringing up a new workstation", "Installing and configuring the CAD software",
                             "Testing beside the lab's robot work cell"], "50% 40%")),
    ]),
    ("comp", "COMPETITIONS", "Contest days", [
        dict(key="b1", code="GAL-B1", title="Technomize 1.0: champions of the CAD contest", place="National Tech Fest · IEM Robotics and CAD Club, KUET",
             date="2 NOV 2024",
             story="Our team Isometric Illuminators 3.0, with Md. Shahriar Santo and Fazle Rabbi, won the CAD contest at "
                   "Technomize 1.0, the national tech fest of the Department of IEM, KUET.",
             photos=P("b1", ["On stage with the champion's board", "Prize-giving with the guests", "With a teammate after the final",
                             "The champion's board, BDT 14,000", "The team selfie after the result"], "50% 40%")),
        dict(key="b2", code="GAL-B2", title="CAD Rush 1.0: champions", place="CADers, KUET", date="13 MAR 2024",
             story="Team Isometric Illuminators 1.0 won CAD Rush 1.0, the CAD contest of CADers at KUET.",
             photos=P("b2", ["Modelling against the clock", "Champions with the crest"], "50% 45%")),
        dict(key="b3", code="GAL-B3", title="MECHCELLENCE 1.0: champions", place="AUST Mechanical Society, Dhaka", date="FEB 2023",
             story="Team Dimensionless won the CAD competition at Ispahani presents MECHCELLENCE 1.0, organised by the "
                   "Department of Mechanical Engineering, AUST.",
             photos=P("b3", ["Champions at the 12-year celebration of AUST Mechanical", "With the champion's board, BDT 12,000"], "50% 35%")),
        dict(key="b4", code="GAL-B4", title="IGNITION 2023: 2nd runner-up", place="Dept. of ME, KUET", date="OCT 2023",
             story="Our team took 2nd runner-up in the CAD segment of IGNITION 2023, the national mechanical festival of the "
                   "Department of Mechanical Engineering, KUET.",
             photos=P("b4", ["2nd runner-up in the CAD segment"], "50% 40%")),
        dict(key="b5", code="GAL-B5", title="KitCAD, AutoFest 2024: 2nd runner-up", place="ME Building, BUET · BUET Automobile Club", date="26 JAN 2024",
             story="KitCAD, the SOLIDWORKS-based CAD contest of AutoFest 2024 by BUET Automobile Club. Team Isometric Illuminators "
                   "went deep into the modelling tasks and took 2nd runner-up.",
             credit="Photos 01 and 02: BUET Automobile Club",
             photos=[("b5-3", "KitCAD 2024 at the ME Building, BUET", "50% 50%"),
                     ("b5-2", "Deep in the contest tasks", "50% 45%"),
                     ("b5-1", "2nd runner-up at KitCAD", "50% 40%")]),
        dict(key="b6", code="GAL-B6", title="MindSparks 24 at AUST", place="AUST, Dhaka", date="14 DEC 2024",
             story="The grand inter-university tech-biz competition at AUST. Our team took part in the CAD segment. "
                   "No prize this time, but a good day of modelling and meeting other teams.",
             photos=[("b6-4", "Our team in the AUSTIDC frame", "50% 45%"), ("b6-5", "Our team at the MindSparks 24 wall", "50% 40%")]),
    ]),
    ("campus", "CAMPUS", "KUET moments", [
        dict(key="c4", code="GAL-C1", title="B.Sc. thesis defence day", place="Dept. of IEM, KUET", date="FEB 2025",
             story='The day I defended my B.Sc. thesis, supervised by <a class="zgl" href="https://www.kuet.ac.bd/iem/kibria" target="_blank" rel="noopener">Md. Golam Kibria</a>. Classmates and friends from 2K19 came by for a photo, '
                   'among them <a class="zgl" href="https://www.linkedin.com/in/md-saiful-islam-seam/" target="_blank" rel="noopener">Md. Saiful Islam Seam</a> and <a class="zgl" href="https://www.linkedin.com/in/nasif-morshed-889766206/" target="_blank" rel="noopener">Nasif Morshed</a>.',
             ratio="3/4", featured=3, rest_label="CLASSMATES AND FRIENDS", rest_caption="Defence day, with classmates and friends from 2K19",
             photos=[("c4-1", "With my supervisor, Md. Golam Kibria", "50% 30%"), ("c4-2", "On defence day", "50% 30%"),
                     ("c4-3", "With Seam and Nasif, toppers of our batch", "50% 35%")]
                    + [(f"c4-{i}", "", "50% 30%") for i in range(4, 18)]),
        dict(key="c1", code="GAL-C2", title="Award of Excellence from DSW", place="KUET", date="AUG 2025",
             story="The Directorate of Students' Welfare, KUET honoured 51 students of the 2K19 batch for their contribution "
                   "to extracurricular activities. I received the Award of Excellence and a Certificate of Contribution.",
             photos=P("c1", ["Receiving the award on stage", "A handshake with the guests", "The Award of Excellence crest",
                             "The award-giving ceremony"], "50% 50%")),
        dict(key="c2", code="GAL-C3", title="Farewell of 2K19", place="Dept. of IEM, KUET", date="AUG 2025",
             story="Farewell of 2K19 and reception of 2K23 and 2K24. Walked in as a dreamer, walked out as an engineer: "
                   "the first graduate in my family line.",
             photos=P("c2", ["Receiving the farewell crest", "On stage at the farewell", "The 2K19 graduation crest"], "50% 40%")),
        dict(key="c3", code="GAL-C4", title="Term project presentation", place="Dept. of IEM, KUET", date="JUN 2024",
             story="Presenting our weight-based sorting machine (IPE 4002), built with Md. Shahriar Islam under the "
                   "supervision of Md. Golam Kibria.",
             photos=P("c3", ["Presenting the design and the test results", "With the working model after the presentation",
                             "With my project partner"], "50% 45%")),
    ]),
]

_bl = os.path.join(os.path.dirname(os.path.abspath(__file__)), "gallery_blobs.json")
GAL_IMG = json.load(open(_bl)) if os.path.exists(_bl) else {}

# ---- real site: the lists above are replaced by content/*.yml (build/content_io.py) ----
import content_io as _C
CHAPTERS, GAL_IMG = _C.load_gallery()
