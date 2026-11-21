"""Education page data. Sources: KUET transcript + details of academic record (courses, terms),
KUET IPE syllabus (topics, shortened), HSC/SSC marksheets (subjects), term project report.
No grades here on purpose: the page shows CGPA only (Zaid, 2026-11-18)."""

AREAS = [  # key, label · grouped after the IISE ISE Body of Knowledge areas (iise.org/iebok)
    ("mfg", "Manufacturing &amp; materials"), ("des", "Product design &amp; CAD"), ("ops", "Operations, quality &amp; SCM"),
    ("ora", "OR &amp; statistics"), ("hf", "Human factors &amp; safety"), ("mgt", "Management &amp; economics"),
    ("dat", "Computing &amp; info systems"), ("eng", "Engineering science"), ("sci", "Math &amp; basic science"),
    ("com", "Communication"), ("prj", "Projects &amp; thesis"),
]

# term key, label, period
TERMS = [
    ("1-1", "YEAR 1 · TERM 1", "FEB 2020 → MAR 2022 *"),
    ("1-2", "YEAR 1 · TERM 2", "FEB 2020 → MAR 2022 *"),
    ("2-1", "YEAR 2 · TERM 1", "MAR → AUG 2022"),
    ("2-2", "YEAR 2 · TERM 2", "SEP 2022 → JAN 2023"),
    ("3-1", "YEAR 3 · TERM 1", "FEB → AUG 2023"),
    ("3-2", "YEAR 3 · TERM 2", "AUG 2023 → JAN 2024"),
    ("4-1", "YEAR 4 · TERM 1", "JAN → OCT 2024"),
    ("4-2", "YEAR 4 · TERM 2", "OCT 2024 → AUG 2025"),
]

L = "lab"
# term, code, title, area, kind ("" theory / lab / prj), topics
COURSES = [
    ("1-1", "IPE 1101", "Manufacturing Process I", "mfg", "", ["Casting", "Welding and joining", "Metal forming", "Plastic product processes"]),
    ("1-1", "CHEM 1111", "Chemistry", "sci", "", ["Chemical bonding", "Kinetics", "Electrochemistry", "Phase diagrams"]),
    ("1-1", "HUM 1111", "Economics", "mgt", "", ["Consumer behaviour", "Theory of the firm", "Cost functions", "Market equilibrium"]),
    ("1-1", "MATH 1111", "Mathematics I", "sci", "", ["Differential calculus", "Partial differentiation", "Integral calculus"]),
    ("1-1", "PHY 1111", "Modern and Solid State Physics", "sci", "", ["Atomic structure", "X-rays", "States of matter", "Solid state physics"]),
    ("1-1", "IPE 1102", "Manufacturing Process I Sessional", "mfg", L, []),
    ("1-1", "CHEM 1112", "Chemistry Sessional", "sci", L, []),
    ("1-1", "PHY 1112", "Physics Sessional", "sci", L, []),

    ("1-2", "IPE 1201", "Manufacturing Process II", "mfg", "", ["Theory of metal cutting", "Machining processes", "Modern machining"]),
    ("1-2", "IPE 1203", "Engineering Materials", "mfg", "", ["Material behaviour in service", "Ceramics and glasses", "Polymers", "Composites"]),
    ("1-2", "IPE 1209", "Computer Fundamentals and Programming Language", "dat", "", ["Hardware and software", "Flowcharts and algorithms", "Structured programming", "Functions"]),
    ("1-2", "HUM 1211", "Professional English", "com", "", ["Grammar and usage", "Vocabulary", "Professional writing"]),
    ("1-2", "MATH 1211", "Mathematics II", "sci", "", ["Matrices", "Linear algebra", "2D and 3D coordinate geometry"]),
    ("1-2", "IPE 1202", "Manufacturing Process II Sessional", "mfg", L, []),
    ("1-2", "IPE 1210", "Computer Programming Sessional", "dat", L, []),
    ("1-2", "HUM 1212", "English Language Sessional", "com", L, []),
    ("1-2", "IPE 1200", "Engineering Drawing", "des", L, ["First and third angle projection", "Orthographic and isometric views", "Sectional views", "Assembly drawing"]),

    ("2-1", "CSE 2111", "Data Structures and Algorithms", "dat", "", ["Arrays, lists, stacks, queues", "Trees and graphs", "Searching and sorting", "Complexity"]),
    ("2-1", "EEE 2111", "Electrical Circuits and Machines", "eng", "", ["AC circuits", "DC machines", "Transformers", "Induction and servo motors"]),
    ("2-1", "HUM 2111", "Financial, Cost and Management Accounting", "mgt", "", ["Final accounts", "Depreciation", "Process costing", "Standard costing"]),
    ("2-1", "MATH 2111", "Mathematics III", "sci", "", ["Differential equations", "Laplace transform", "Complex variables"]),
    ("2-1", "ME 2111", "Engineering Mechanics and Theory of Machines", "eng", "", ["Equilibrium", "Trusses and frames", "Friction", "Mechanisms"]),
    ("2-1", "CSE 2112", "Data Structures and Algorithms Sessional", "dat", L, []),
    ("2-1", "EEE 2112", "Electrical Circuits and Machines Sessional", "eng", L, []),
    ("2-1", "ME 2112", "Engineering Mechanics and Theory of Machines Sessional", "eng", L, []),

    ("2-2", "IPE 2207", "Probability and Statistical Analysis", "ora", "", ["Distributions", "Expectation and moments", "Central limit theorem", "Confidence intervals"]),
    ("2-2", "IPE 2229", "Industrial Psychology and Law", "hf", "", ["Individual and group psychology", "Attitudes and cognition", "Industrial law", "Factory Act"]),
    ("2-2", "EEE 2211", "Electronics", "eng", "", ["Diodes and transistors", "Op-amps", "Logic and digital circuits", "Industrial electronics"]),
    ("2-2", "ME 2213", "Mechanics of Solids", "eng", "", ["Beams", "Torsion", "Combined stresses", "Columns", "Riveted and welded joints"]),
    ("2-2", "ME 2215", "Thermal Engineering and Heat Transfer", "eng", "", ["Thermodynamics", "Engines and turbines", "Refrigeration", "Heat transfer"]),
    ("2-2", "IPE 2200", "Computer Aided Design Sessional I", "des", L, ["2D drafting in AutoCAD", "Layers and blocks", "Dimensioning", "Plotting"]),
    ("2-2", "EEE 2212", "Electronics Sessional", "eng", L, []),
    ("2-2", "ME 2214", "Mechanics of Solids Sessional", "eng", L, []),
    ("2-2", "ME 2216", "Thermal Engineering and Heat Transfer Sessional", "eng", L, []),

    ("3-1", "IPE 3103", "Engineering Metallurgy", "mfg", "", ["Crystal structure", "Metallography", "Fe-C phase diagram", "Heat treatment"]),
    ("3-1", "IPE 3105", "Product Design I", "des", "", ["Product planning and specs", "Concept generation and selection", "Prototyping", "Product architecture"]),
    ("3-1", "IPE 3115", "Engineering Economy", "mgt", "", ["Present worth", "Rate of return", "Depreciation", "Inflation"]),
    ("3-1", "IPE 3119", "Operations Management", "ops", "", ["Demand forecasting", "Aggregate planning", "Inventory models", "Scheduling"]),
    ("3-1", "ME 3111", "Fluid Mechanics and Machinery", "eng", "", ["Fluid statics", "Fluid dynamics", "Pipe flow", "Pumps and turbines"]),
    ("3-1", "IPE 3100", "Computer Aided Design Sessional II", "des", L, ["3D modelling", "Rendering", "Animation", "SOLIDWORKS"]),
    ("3-1", "IPE 3104", "Engineering Metallurgy Sessional", "mfg", L, []),
    ("3-1", "IPE 3106", "Product Design I Sessional", "des", L, []),
    ("3-1", "ME 3112", "Fluid Mechanics and Machinery Sessional", "eng", L, []),

    ("3-2", "IPE 3205", "Product Design II", "des", "", ["Stress and strain analysis", "Shafts, springs, bearings", "Gears", "Belt, rope and chain drives"]),
    ("3-2", "IPE 3217", "Operations Research", "ora", "", ["Linear programming", "Simplex and duality", "Transportation and assignment", "Dynamic programming"]),
    ("3-2", "IPE 3219", "Production Systems Design", "ops", "", ["Capacity planning", "Method and motion study", "Work measurement", "Facility layout and location"]),
    ("3-2", "IPE 3221", "Quality Management", "ops", "", ["Statistical quality control", "Six Sigma", "Design of experiments", "Acceptance sampling"]),
    ("3-2", "IPE 3223", "Material Handling and Maintenance Management", "ops", "", ["Handling systems", "Cranes and forklifts", "Packaging tests", "Maintenance"]),
    ("3-2", "IPE 3200", "Business Communication Seminar", "com", L, []),
    ("3-2", "IPE 3206", "Product Design II Sessional", "des", L, []),
    ("3-2", "IPE 3218", "Operations Research Sessional", "ora", L, []),
    ("3-2", "IPE 3220", "Production Systems Design Sessional", "ops", L, []),
    ("3-2", "IPE 3222", "Quality Management Sessional", "ops", L, []),

    ("4-1", "IPE 4109", "Management Information System Analysis and Design", "dat", "", ["Information needs", "System development life cycle", "Requirements and planning"]),
    ("4-1", "IPE 4125", "Machine Tools", "mfg", "", ["Drive systems", "Speed and feed gearboxes", "Machine tool design"]),
    ("4-1", "IPE 4129", "Industrial Management and Entrepreneurship Development", "mgt", "", ["Human resource management", "Strategic management", "Entrepreneurship"]),
    ("4-1", "IPE 4019", "Logistics and Supply Chain Management", "ops", "", ["Supply chain planning", "Transportation", "IT in the supply chain", "Coordination"]),
    ("4-1", "IPE 4029", "Marketing Management", "mgt", "", ["Market segmentation", "Buyer behaviour", "Marketing planning"]),
    ("4-1", "IPE 4110", "MIS Sessional", "dat", L, []),
    ("4-1", "IPE 4126", "Machine Tools Sessional", "mfg", L, []),
    ("4-1", "IPE 4002", "Term Project", "prj", "prj", ["Weight-based sorting machine", "Arduino and load cell", "Servo sorting arms"]),

    ("4-2", "IPE 4219", "Human Factors Engineering and Safety Management", "hf", "", ["Workplace design", "Anthropometry", "Biomechanics and manual lifting", "Safety management"]),
    ("4-2", "IPE 4225", "Tool Engineering", "mfg", "", ["Locating and clamping", "Jigs and fixtures", "Die design", "Gauges"]),
    ("4-2", "IPE 4227", "CAM and Robotics", "mfg", "", ["NC and CNC", "CNC part programming", "CAPP", "Industrial robots"]),
    ("4-2", "IPE 4027", "Computer Integrated Manufacturing", "mfg", "", ["Automation", "Group technology", "Automated handling", "AS/RS"]),
    ("4-2", "IPE 4059", "Project Management", "mgt", "", ["Project life cycle", "Scope and planning", "Cost and time estimating"]),
    ("4-2", "IPE 4000", "Project and Thesis", "prj", "prj", ["ML risk prediction for WMSD", "RULA posture scores", "Video data"]),
    ("4-2", "IPE 4220", "Human Factors Engineering Sessional", "hf", L, []),
    ("4-2", "IPE 4226", "Tool Engineering Sessional", "mfg", L, []),
    ("4-2", "IPE 4228", "CAM and Robotics Sessional", "mfg", L, []),
]

HSC_SUBJECTS = ["Bangla", "English", "Physics", "Chemistry", "Higher Mathematics", "ICT"]
HSC_EXTRA = ["Biology"]
SSC_SUBJECTS = ["Bangla", "English", "Mathematics", "Higher Mathematics", "Physics", "Chemistry",
                "Bangladesh and Global Studies", "Islam and Moral Education", "ICT", "Physical Education, Health and Sports", "Career Education"]
SSC_EXTRA = ["Biology"]

CAD_WINS = [  # title, event, organiser, date, certificate key
    ("Champion", "Technomize 1.0 · National Tech Fest", "IEM Robotics and CAD Club, KUET", "2 NOV 2024", "technomize"),
    ("Champion", "CAD Rush 1.0", "CADers, KUET", "13 MAR 2024", "cadrush"),
    ("Champion", "MECHCELLENCE 1.0 · CAD competition", "AUST Mechanical Society", "FEB 2023", "mechcellence"),
    ("2nd runner-up", "KitCAD · Autofest 2024", "BUET Automobile Club", "25 JAN 2024", "kitcad"),
    ("2nd runner-up", "IGNITION 2023 · CAD segment", "Dept. of ME, KUET", "OCT 2023", "ignition"),
    ("Top 20 finalist", "Energy Fest 1.0 · CAD competition", "Dept. of ESE, KUET", "DEC 2024", ""),
]

# ---- teachers (course folder names matched to KUET faculty pages, 2026-11-18) ----
K = "https://kuet.ac.bd/"
T = {  # key: (full name, profile url, sure?)
    "habibur": ("Dr. Md. Habibur Rahman", K + "iem/habibur091", True),
    "rafiq": ("Dr. Md. Rafiquzzaman", K + "iem/rafiq123", True),
    "alamin": ("Dr. Md. Al Amin", K + "iem/m.alamin", True),
    "saiful": ("Dr. Md. Saiful Islam", K + "iem/saifuliem", True),
    "kibria": ("Md. Golam Kibria", K + "iem/kibria", True),
    "farjana": ("Farjana Parvin", K + "iem/farjanamousumi17", True),
    "tamanna": ("Tamanna Kamal", K + "iem/tamanna", True),
    "parvez": ("Md. Shohel Parvez", K + "iem/msp.ipe", True),
    "nsultana": ("Dr. Mst. Nazma Sultana", K + "iem/n.sultana", True),
    "palash": ("Palash Saha", K + "iem/palash", True),
    "ridwan": ("Ridwan Mustofa", K + "iem/ridwanmustofa", True),
    "zahid": ("S M Julfiker Zahid", K + "iem/julfiker", True),
    "anzum": ("Kazi Md. Tanvir Anzum", K + "iem/tanvir", True),
    "ismail": ("Md. Ismail Hossain", K + "iem/ismail", True),
    "irfan": ("Md. Tanjid Hossen Irfan", K + "iem/irfan", True),
    "talapatra": ("Dr. Subrata Talapatra", K + "iem/subrata", True),
    "asef": ("Asef Shahriar", K + "iem/asef", True),
    "ashik": ("Jahid Hasan Ashik", K + "iem/jhashik", True),
    "saddam": ("Dr. Md. Saddam Hossain", K + "chem/saddam", True),
    "yousuf": ("Dr. Mohammad Abu Yousuf", K + "chem/yousuf", True),
    "razia": ("Dr. Razia Khatun", K + "hum/rkhatun", True),
    "shahin": ("Dr. Md. Shahinur Alam Sarker", K + "hum/shahin", True),
    "tauhid": ("Munshi Tauhiduzzaman", K + "hum/mtzaman", True),
    "amanullah": ("Md. Amanullah", K + "hum/maaman", True),
    "tania": ("Tania Haque", K + "hum/tania438834", True),
    "arif": ("S.M. Arif Hossen", K + "math/smarif", True),
    "asraful": ("Dr. Md. Asraful Alom", K + "math/asraful", True),
    "jamali": ("Dr. A. R. M. Jalal Uddin Jamali", K + "math/jamali", True),
    "idris": ("Md. Idris Ali", K + "phy/idrisali", True),
    "ekabir": ("A. N. M. Enamul Kabir", K + "eee/ekabir", True),
    "shahabul": ("Md. Shahabul Alam", K + "eee/shahabul", True),
    "arefin": ("Arefin Ahamed Shuvo", K + "eee/arefin", True),
    "anik": ("Fahim Islam Anik", K + "me/anik", True),
    "raju": ("Raju Ahammad", K + "me/rajuahammad", True),
    "shahidul": ("Dr. Md. Shahidul Islam", K + "me/shahidulbitk", True),
    "faruk": ("Dr. Abdullah Al-Faruk", K + "me/alfaruk", True),
    "dipayan": ("Dr. Dipayan Mondal", K + "me/dipkuet", True),
    "zahir": ("Dr. Zahir Uddin Ahmed", K + "me/zuahmed", True),
    "shakil": ("Md. Shakil Hossain", K + "math/shakil", True),
    "touhid": ("Dr. M. M. Touhid Hossain", K + "math/mthosain", True),
    "selim": ("A.K.M. Selim Reza", K + "math/selim_1992", True),
    "wakil": ("Dr. Md. Abdul Wakil", K + "me/wakil", True),
    "roman": ("Shahrear Roman", "https://www.linkedin.com/in/shahrear-roman-a63089b7/", True),
    "sikder": ("Dr. Shibendra Shekher Sikder", "https://www.kuet.ac.bd/phy/sssikder", True),
    "msislam": ("Dr. Md. Shariful Islam", K + "me/msislam", True),
    "nourin": ("Nourin Mohsin", "https://www.linkedin.com/in/nourinmohsin/", True),
    "hridoy": ("Rafat Mahmud Hridoy", K + "iem/rafathridoy", True),
    "mahbub": ("Dr. Md. Mahbubur Rahman", "https://www.linkedin.com/in/md-rahman-robotics/", True),
    # added 21 Nov from the class routines Zaid sent (sessional teachers)
    "hasib": ("Dr. Md. Abdul Hasib", "https://www.kuet.ac.bd/me/ahasib", True),
    "tawabur": ("Dr. Md. Tawabur Rahman", "https://www.kuet.ac.bd/eee/tawabur", True),
    "hrashid": ("Md. Harun-Or-Rashid Mollah", "https://kuet.ac.bd/me/hrashid", True),
}
TEACH = {  # course code -> teacher keys (from the teacher folders in each course)
    "IPE 1101": ["habibur", "rafiq"], "CHEM 1111": ["saddam", "yousuf"], "HUM 1111": ["razia", "roman"],
    "MATH 1111": ["arif", "shakil"], "PHY 1111": ["idris", "sikder"],
    "IPE 1201": ["alamin", "rafiq"], "IPE 1203": ["alamin", "mahbub"], "IPE 1209": ["mahbub", "saiful"],
    "HUM 1211": ["shahin", "tauhid"], "MATH 1211": ["asraful", "jamali"],
    "CSE 2111": ["saiful", "talapatra"], "EEE 2111": ["ekabir", "shahabul"], "HUM 2111": ["amanullah", "tania"], "ME 2111": ["anik", "msislam"],
    "IPE 2207": ["farjana", "saiful"], "IPE 2229": ["hridoy", "nourin"], "EEE 2211": ["arefin", "ekabir"],
    "ME 2213": ["raju", "shahidul"], "ME 2215": ["dipayan", "faruk"],
    "IPE 3103": ["farjana", "rafiq"], "IPE 3105": ["kibria", "farjana"], "IPE 3115": ["nourin", "ridwan"], "IPE 3119": ["kibria", "palash"], "ME 3111": ["wakil", "zahir"],
    "IPE 3217": ["farjana", "saiful"], "IPE 3219": ["kibria", "nsultana"], "IPE 3221": ["farjana", "kibria"], "IPE 3223": ["zahid", "anzum"],
    "IPE 4109": ["ridwan", "saiful"], "IPE 4125": ["farjana", "talapatra"], "IPE 4129": ["zahid", "anzum"],
    "IPE 4019": ["ismail", "palash"], "IPE 4029": ["irfan", "zahid"],
    "IPE 4219": ["kibria", "palash"], "IPE 4225": ["asef", "talapatra"], "IPE 4227": ["asef", "ashik"],
    "IPE 4027": ["ashik", "rafiq"], "IPE 4059": ["irfan", "palash"],
    "MATH 2111": ["selim", "touhid"], "IPE 3205": ["asef", "rafiq"], "IPE 1200": ["shahidul", "mahbub"], "IPE 3100": ["saiful", "ismail"], "IPE 3200": ["palash", "anzum"], "IEM 6115": ["saiful"], "IEM 6123": ["anzum"], "IEM 6211": ["rafiq"], "IPE 4002": ["kibria"], "IPE 4000": ["kibria"],
    # sessionals, from the class routines (checked 21 Nov 2026)
    "IPE 2200": ["parvez", "palash"], "ME 2214": ["shahidul", "ridwan"], "ME 2216": ["msislam", "hasib"], "EEE 2212": ["ekabir", "tawabur"],
    "IPE 3104": ["rafiq", "farjana"], "IPE 3106": ["kibria", "farjana"], "ME 3112": ["zahir", "wakil"],
    "IPE 3206": ["rafiq", "asef"], "IPE 3218": ["saiful", "farjana"], "IPE 3220": ["kibria", "nsultana"], "IPE 3222": ["kibria", "farjana"],
    "IPE 4110": ["saiful", "ridwan"], "IPE 4126": ["talapatra", "hrashid"],
    "IPE 4220": ["kibria", "palash"], "IPE 4226": ["talapatra", "asef"], "IPE 4228": ["asef", "ashik"],
}

MSC_COURSES = [  # code, title, topics
    ("IEM 6115", "Stochastic Decision Models", ["Probability", "Conditional probability", "Mathematical expectation", "Poisson process", "Exponential distribution", "Simulation"]),
    ("IEM 6123", "Numerical Methods for Optimization", []),
    ("IEM 6211", "Computer Integrated Manufacturing Systems", []),
]

# HSC / SSC subjects grouped the way the board lists them
HSC_GROUPS = [("COMPULSORY", ["Bangla", "English", "ICT"]),
              ("SCIENCE GROUP", ["Physics", "Chemistry", "Higher Mathematics"]),
              ("4TH SUBJECT", ["Biology"])]
SSC_GROUPS = [("COMPULSORY", ["Bangla", "English", "Mathematics", "ICT", "Bangladesh and Global Studies",
                              "Islam and Moral Education", "Physical Education, Health and Sports", "Career Education"]),
              ("SCIENCE GROUP", ["Physics", "Chemistry", "Higher Mathematics"]),
              ("4TH SUBJECT", ["Biology"])]

# ---- real site: the lists above are replaced by content/*.yml (build/content_io.py) ----
import content_io as _C
globals().update(_C.load_education())
