"""Awards page content (proposal, 2026-11-20). Maps 1:1 to JSON for the real site.
Competitions: edu_data.CAD_WINS (from the certificates).
Certificates: read from his files (Certification.zip, 20 Nov 2026):
names and dates as printed on each certificate; verify links from the certificate QR codes / printed URLs.
RapidMiner, Ostad: dates and badge / share links from Zaid's certificate list PDF (Issued Apr 2025, Nov 2022).
CSWA exam score from "Exam Results.png" (225 of 240).
Case competition and philosophy facts from Zaid's LinkedIn posts (31 Oct 2024, 26 Dec 2024)."""
import json, os
import edu_data as D

_B = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "awards_blobs.json")))
_B["philosophy"] = "/_blob/112b4c0589818f9c1880d77460fe3e79"

CERT_IMG = {
    "technomize": "/_blob/cbd94d83f1ab0a605f0d249d30cb4961", "cadrush": "/_blob/0f898711631101bcb558dd9fed527f5c",
    "mechcellence": "/_blob/1338cb7441a161527b9fde208cd3b677", "kitcad": "/_blob/88368f3764338751aa406b701e68b81a",
    "ignition": "/_blob/152b4e8af7817136567d6fdfe43e679f",
}
EV_RENDER = "/_blob/e20aa20d43dfab39dddf79f586cc1688"   # Energy Fest entry (no certificate): show the model instead
STAMP = {"Champion": ("1ST", "PLACE"), "2nd runner-up": ("3RD", "PLACE"), "Top 20 finalist": ("TOP", "20")}
COMPETITIONS = D.CAD_WINS          # rank, event, organiser, date, certificate key

SCHOLARSHIP = dict(
    when="OCT 2024", title="70 % scholarship winner", event="ISCEA Prize · Global Supply Chain Case Competition 2024",
    org="International Supply Chain Education Alliance (ISCEA)", team="KUET 0101-24",
    team_members=[("Md. Zaid Hossain", "https://www.linkedin.com/in/md-zaid-hossain"),
                  ("Meer Al Amin Islam", "https://www.linkedin.com/in/meer-alamin-islam/"),
                  ("Saleh Akram Naife", "https://www.linkedin.com/in/saleh-akram-naife-97b3ab227/"),
                  ("Sadman Sadik", "https://www.linkedin.com/in/sadman-sadik-csca%E2%84%A2-83433a1b1/")],
    post="https://lnkd.in/p/g-_VaCJH",
    # poster sent by Zaid (ISCEA winners' list, part 2); his team's tag box in % of the poster (441 x 788)
    poster="/_blob/ae4ab0deeb88e65658f5582a01b2673b", tag_box=(10.2, 67.1, 25.0, 4.8),
    amount="US$ 770", amount_note="per person, toward ISCEA's global CSCA certification")

VSW = "https://cv.virtualtester.com/qr/?b=SLDWRKS&i="
CV = "https://www.coursera.org/account/accomplishments/verify/"
OB = "https://openbadgepassport.com/app/badge/info/"
DS = "Dassault Systèmes"

# Each certificate: (image key, code, name, issuer, date, [(link label, url)], wide?)
GROUPS = [
    ("--y21", "2.1", "CAD · SOLIDWORKS", "CAD", 4, [
        ("cswp", "CSWP", "SOLIDWORKS CAD Design Professional", DS, "20 APR 2025", [("VERIFY ↗", VSW + "C-3WTCQ4G7A5")]),
        ("cswa", "CSWA", "SOLIDWORKS Mechanical Design Associate", DS + " · exam score 225 / 240", "1 MAR 2023", [("VERIFY ↗", VSW + "C-W3TXBEQKF8")]),
        ("cswa-am", "CSWA-AM", "Additive Manufacturing Associate", DS, "22 JUN 2025", [("VERIFY ↗", VSW + "C-5H3EULBY96")]),
        ("cswa-s", "CSWA-S", "Simulation Associate", DS, "22 JUN 2025", [("VERIFY ↗", VSW + "C-ZPU2EHY9AK")]),
        ("cswa-sd", "CSWA-SD", "Sustainability Associate", DS, "22 JUN 2025", [("VERIFY ↗", VSW + "C-W9RDH3MULK")]),
        ("3dx-creator", "3DEXPERIENCE", "3D Creator Associate", DS, "22 JUN 2025", [("VERIFY ↗", VSW + "C-65KWQAXSMB")]),
        ("3dx-mold", "3DEXPERIENCE", "3D Mold Creator Associate", DS, "22 JUN 2025", [("VERIFY ↗", VSW + "C-4EL3NBZ52Q")]),
        ("3dx-swymer", "3DEXPERIENCE", "3DSwymer Associate", DS, "22 JUN 2025", [("VERIFY ↗", VSW + "C-9HVTP3E8GX")]),
    ]),
    ("--y22", "2.2", "SUPPLY CHAIN", "Supply chain", 4, [
        ("csca", "CSCA™", "Certified Supply Chain Analyst", "International Supply Chain Education Alliance (ISCEA)",
         "10 JAN 2025", [("VERIFY ↗", "https://www.iscea.org/verify-certification"), ("LINKEDIN POST ↗", "https://lnkd.in/p/gbXxUrnR")],
         "Conferred in Cleveland, Ohio, USA · valid to 31 Jan 2028"),
        ("lh-basic", "LOG-HUB", "Supply Chain Apps · Basic", "Log-hub", "25 JUN 2026", []),
        ("lh-advanced", "LOG-HUB", "Supply Chain Apps · Advanced", "Log-hub", "26 JUN 2026", []),
        ("lh-network", "LOG-HUB", "Network Design", "Log-hub", "26 JUN 2026", []),
        ("lh-transport", "LOG-HUB", "Transport and Route Optimization", "Log-hub", "28 JUN 2026", []),
        ("lh-inventory", "LOG-HUB", "Inventory Optimization", "Log-hub", "30 JUN 2026", []),
        ("lh-expert", "LOG-HUB", "Supply Chain Apps · Expert", "Log-hub", "30 JUN 2026", []),
    ]),
    ("--y23", "2.3", "DATA AND QUALITY", "Data &amp; quality", 3, [
        ("rm-ml", "RAPIDMINER", "Machine Learning Professional", "RapidMiner · Altair", "APR 2025", [("VERIFY ↗", OB + "917735")]),
        ("rm-apps", "RAPIDMINER", "Applications &amp; Use Cases Professional", "RapidMiner · Altair", "APR 2025", [("VERIFY ↗", OB + "912646")]),
        ("rm-data", "RAPIDMINER", "Data Engineering Professional", "RapidMiner · Altair", "APR 2025", [("VERIFY ↗", OB + "913202")]),
        ("ibm-ml", "IBM", "Machine Learning with Python", "IBM · Coursera", "2 APR 2024", [("VERIFY ↗", CV + "HMNDY4ECTDGK")]),
        ("lss-white", "CSSC", "Lean Six Sigma White Belt", "The Council for Six Sigma Certification", "24 MAR 2025", []),
        ("ss-white", "CSSC", "Six Sigma White Belt", "The Council for Six Sigma Certification", "9 MAR 2025", []),
    ]),
    ("--y24", "2.4", "COURSES", "Courses", 4, [
        ("udemy-sw", "UDEMY", "SolidWorks Essentials: A Beginner's Guide to 3D Design", "Udemy · 4.5 hours", "10 MAY 2025",
         [("VERIFY ↗", "https://www.udemy.com/certificate/UC-a4d9fa8a-1fce-4763-91d9-cbcda0fe4f37/")]),
        ("philosophy", "PHI101", "Introduction to Philosophy · passed with distinction", "Mahtab Academy", "DEC 2024",
         [("LINKEDIN POST ↗", "https://lnkd.in/p/gJkt_YUN")]),
        ("ibm-py", "IBM", "Python for Data Science, AI &amp; Development", "IBM · Coursera", "9 MAR 2024", [("VERIFY ↗", CV + "FYMYU6ZXFVAZ")]),
        ("sl-python", "SIMPLILEARN", "Python for Beginners", "Simplilearn SkillUp", "5 MAR 2024", []),
        ("cp-python", "PROJECT", "Create Your First Python Program", "UST · Coursera Project Network", "21 FEB 2024", [("VERIFY ↗", CV + "ZXWNP7RTD5K7")]),
        ("ms-excel", "MICROSOFT", "Work Smarter with Microsoft Excel", "Microsoft · Coursera", "30 JAN 2024", [("VERIFY ↗", CV + "HNXDLTRZMWM3")]),
        ("cp-excel", "PROJECT", "Introduction to Data Analysis using Microsoft Excel", "Coursera Project Network", "30 AUG 2023", [("VERIFY ↗", CV + "4NRQWNG3ZDBA")]),
        ("ostad-sw", "OSTAD", "Product Design with SolidWorks", "Ostad", "NOV 2022", [("VERIFY ↗", "https://ostad.app/share/certificate/c22701-md.-zaid-hossain")]),
    ]),
]
IMG = _B

# ---- real site: the lists above are replaced by content/*.yml (build/content_io.py) ----
import content_io as _C
globals().update(_C.load_awards())
