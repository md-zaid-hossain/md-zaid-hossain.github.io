"""Experience page content. Sources: CV (Instrumentation Engineer CV, Jun 2026), HEAT PIN-14011 job flyer,
FabLab / DSW / hall certificates, and the 01_Client_Projects folder (client names left out on purpose)."""

ROLES = [
    dict(key="iat", start="JUL 2026", end=None, title="Fab Lab Program Engineer (Instrumentation)",
         org="Institute of Appropriate Technology (IAT), BUET", place="Dhaka",
         note="Under the HEAT project of the University Grants Commission (sub-project PIN 14011), an 18-month appointment.",
         do=["Install, calibrate, maintain and troubleshoot lab equipment: 3D printers, CNC machines, laser cutters, PCB tools, oscilloscopes, and AI and IoT kits.",
             "Give technical support for prototyping, testing and product development.",
             "Keep the lab on its safety standards and standard operating procedures (SOPs).",
             "Run routine calibration, preventive maintenance and performance monitoring."],
         tools="3D printers · CNC · laser cutter · PCB tools · oscilloscope · IoT kits", links=[]),
    dict(key="fab", start="MAR 2024", end="SEP 2025", title="FabLab Assistant · Student Operator",
         org="FabLab, Khulna University of Engineering &amp; Technology (KUET)", place="Khulna",
         note="Certified student operator from Mar 2024 to Mar 2025, then stayed on as a volunteer to Sep 2025.",
         do=["Operated and calibrated the 3D printers and digital fabrication machines used for prototyping, course projects and research.",
             "Helped students improve their CAD models, prepare slicing and check whether a part could be made.",
             "Diagnosed machine and print faults to cut machine downtime and keep projects on time.",
             "Worked around the lab's 3D printers, CNC machines and laser cutter."],
         tools="FDM 3D printers · slicers · CNC · laser cutter · SOLIDWORKS · Fusion 360",
         links=[("Certificate of Achievement on the Education page", "#")]),
    dict(key="free", start="2023", end=None, title="Freelance CAD Designer",
         org="Independent · remote and local clients", place="Bangladesh",
         note="Part-time alongside study and work. Client names are left out; the jobs are listed below by type.",
         do=["Model parts and full assemblies in SOLIDWORKS from sketches, photos or existing parts.",
             "Lay out process plants in 3D, from single machines to a complete 50 TPD line.",
             "Deliver STEP and IGES files, 2D drawings, renders and short walk-through videos.",
             "Prepare models for 3D printing (STL, slicing) when the client needs a physical part."],
         tools="SOLIDWORKS · KeyShot · Fusion 360 · Photoshop", links=[("Selected client work on the Projects page", "#")]),
]

# (year, job type, what was delivered) - one line per client folder, no client names
JOBS = [
    ("2026", "Aluminium foil plant, 50 TPD", "Full 3D site layout of the process line, utilities and material flow; walk-through video"),
    ("2026", "Perforated brick wall study", "15 wall variants (brick gap and angle), each with STEP export and views"),
    ("2026", "Layered cell models", "Two layered stack assemblies with wiring, parts and images"),
    ("2025", "Mining machine: spiral and cutter", "Full assembly, pipe sections, 2D drawing set and motion videos"),
    ("2025", "Servo mechanism", "Servo motor and connector assembly"),
    ("2025", "Pipe model", "Parts delivered as IGES"),
    ("2024", "Soap process plant (distillation, cooling tower, filter press)", "Plant section assemblies, layouts before and after, STEP files"),
    ("2024", "Dry-fruit product rendering", "Product models, KeyShot renders and animated GIFs"),
    ("2024", "Waste-to-power plant model", "Feedstock unit, tower and generator set in one assembly, STEP export"),
    ("2024", "Composite part designs", "Four assemblies with STEP files and images"),
    ("2024", "Reactor vessel", "Assembly of three parts with STEP files"),
    ("2024", "Hand tool part", "Lever part modelled from photos of the tool"),
    ("2023", "3D printer extruder (Prusa i3 MK2)", "Full printer assembly of 150+ parts and printable STL files"),
    ("2023", "Mechanical parts for printing", "Parts, assemblies, STL and G-code"),
    ("2023", "Gear and rack mechanism", "Mechanism model"),
    ("2023", "Wooden aquarium stand", "Assembly with STEP export and images"),
]

CAMPUS = [
    dict(when="OCT 2024", title="Dining Manager", org="Amar Ekushey Hall, KUET",
         text="Ran the hall dining: meal planning, purchasing and the budget, service, and keeping residents informed."),
    dict(when="2024", title="Hall Committee Member · Mosque Committee", org="Amar Ekushey Hall, KUET",
         text="Member of the Amar Ekushey Hall committee 2024, serving on the mosque committee and in student affairs; recognised with a Certificate of Recognition (Sep 2025).",
         cert="Certificate of Recognition"),
    dict(when="MAR 2024 → SEP 2025", title="FabLab student operator and volunteer", org="FabLab, KUET",
         text="Beyond the operator role: helped run the lab as a volunteer after the certified year ended; recognised with a Certificate of Achievement.",
         cert="Certificate of Achievement"),
    dict(when="AUG 2025", title="Award of Excellence and Certificate of Contribution", org="Directorate of Students' Welfare (DSW), KUET",
         text="The Award of Excellence crest, and a Certificate of Contribution for outstanding contribution and dedication to extracurricular activities.",
         cert="Certificate of Contribution"),
]

CNC_PHOTOS = [  # (blob, step, caption) - own photos from the HAAS training at IEM, KUET, Sep 2025
    ("/_blob/17b9e602b5b32b84c904c6cef400551e", "PLAN", "HAAS VF-2 set up as the machine in Fusion CAM"),
    ("/_blob/534b3cc47712ad99707ed5b0b49529c5", "PLAN", "Toolpath simulation: face, pockets, drills, adaptive clearing"),
    ("/_blob/3f9e5f779905e58783fede123b55dbdf", "PLAN", "The posted NC program for the VF-2"),
    ("/_blob/5eabe120f0c300a1c0025edd43f7276f", "SET UP", "The VF-2 with the vise on the table"),
    ("/_blob/3a9de8f2d1a6f78048ee8ed3f73ccc68", "SET UP", "BT40 tool holder"),
    ("/_blob/2958665e5921d2853297db91e6e1e562", "RUN", "The program running on the HAAS control"),
    ("/_blob/89ef557c7d7ae6f3c66a824269e0a0be", "CUT", "Face milling the stock"),
    ("/_blob/e10c8610b05fffef4943fb68e8430839", "CUT", "Pocketing with flood coolant"),
    ("/_blob/21aabb9acd788e0ac336323d2e583bdc", "CUT", "Detail work with the small end mill"),
    ("/_blob/9e26b9ca40d80999fdecf51d4d901720", "RESULT", "Taking the cut part out of the vise"),
    ("/_blob/32a35aeded5b9508e6b7831a5e91b88e", "RESULT", "The finished aluminium part"),
    ("/_blob/e95beaa8fb9ddcea2220ace52fd9acf0", "RESULT", "With the part at the machine"),
]

BOOTCAMP_PHOTOS = [
    ("/_blob/0cb2e3e9f2c4bae635119c0483ec48fa", "CERTIFICATE", "Certificate of Participation"),
    ("/_blob/709f514d2e066a9fdd1bb7ed22ad6b73", "TASK 1", "Sketching, draft angles and fillets, with a mass check"),
    ("/_blob/1e870f048445ad482e915d21369311de", "TASK 2", "Stepped part for the stress and displacement study"),
    ("/_blob/9b0f3d3c15e2a73be049ce21d30684fa", "TASK 3", "Welding-neck flange with its 2D drawing"),
    ("/_blob/2b613be5a8929c03eae595ef8f26f7db", "TASK 4", "Hybrid surface and solid modelling"),
]

PHOTOS = {"cnc": CNC_PHOTOS, "bootcamp": BOOTCAMP_PHOTOS}

TRAINING = [
    dict(when="SEP 2025", title="CNC and CAM on a HAAS VF-2 milling machine", org="Department of IEM, KUET",
         text="Hands-on training when the department's HAAS VF-2 and desktop lathe came in: machine operation, tool holders and offsets, graphical simulation and shop-floor safety. I modelled a test part, planned its face, pocket, drill and adaptive toolpaths in Fusion CAM, posted the NC program and cut it in aluminium.",
         photos="cnc"),
    dict(when="APR 2025", title="International SOLIDWORKS Bootcamp 2025", org="ASME QUEST Chapter with the Islamabad SOLIDWORKS User Group (ISUG) and the SOLIDWORKS MUET Club · online",
         text="An international online bootcamp on advanced part and assembly modelling, simulation (FEA), surface and hybrid modelling, design for manufacturing and engineering drawings. I completed all five graded tasks: sketching with draft angles and fillets, a stress and displacement study, a flange with its 2D drawing, hybrid surface and solid modelling, and a multi-body part with mass checks.",
         photos="bootcamp"),
]

# ---- real site: the lists above are replaced by content/*.yml (build/content_io.py) ----
import content_io as _C
globals().update(_C.load_experience())
