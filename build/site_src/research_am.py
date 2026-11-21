"""Study page: FDM print settings and PLA bending bars, with Tonoy Chowdhury (PROPOSAL 21 Nov 2026).
Built on the project page template (project_pages.py): hero with two photos, spec list, stats, numbered sections
(clips, photo groups that open as slideshows, a study design table). It shows how the work was done, never results:
the paper is still being written. Facts from his files
(photos, videos, G-code) and Zaid's experiment sheet. Photos picked by Zaid's rule: one best
photo per topic, one best clip per test (two for printing)."""
import project_pages as PP

NM = lambda n: f'<span class="nowrap" style="white-space:nowrap">{n}</span>'
B = "/_blob/"

STUDY = dict(
    key="fdm-pla", no=0, slug="fdm-pla-study",
    crumb="FDM PRINT SETTINGS STUDY", tags=["WITH TONOY CHOWDHURY, MIST", "FDM · PLA · ASTM D790"],
    title="FDM print settings and the bending, roughness and hardness of PLA",
    lead=(f"With my classmate {NM('Tonoy Chowdhury')}, now a lecturer at MIST, I printed PLA bending bars while changing four "
          "settings: infill pattern, infill density, nozzle diameter and raster angle. The bars then went through a three-point "
          "bending test, a surface roughness reading and a Shore D hardness check. The analysis and the paper are still in "
          "progress, so this page shows how the work was done, not the results."),
    still=("BENDING", B + "d6f768e9fea7047e80efcfb34895f8c3", "A printed PLA bar bent under the centre nose of the bending fixture"),
    still_cap="PHOTO · THREE-POINT BENDING",
    render=B + "2d65eab0d3030230f4f08a28d42eb0be", render_label="PRINTING",
    render_alt="Three PLA bending bars printed on the bed, the print head above them",
    spec=[("TYPE", "Research <em>· in progress</em>"),
          ("TEAM", f"{NM('Md. Zaid Hossain')} · {NM('Tonoy Chowdhury')} <em>· Lecturer, MIST</em>"),
          ("MATERIAL", "White PLA, 1.75 mm <em>· FDM printed</em>"),
          ("SPECIMEN", "ASTM D790 bar <em>· 127 × 12.7 × 3.2 mm</em>"),
          ("TESTS", "Three-point bending · surface roughness · Shore D hardness"),
          ("STATUS", "Bars printed and tested <em>· analysis and writing ongoing</em>")],
    stats=[("108", "printed runs"), ("4", "settings varied"), ("3", "kinds of test"), ("0.2 to 0.5 mm", "nozzle sizes")],
    sections=[
        dict(kind="photos", tag="THE SET-UP", title="Printers, filament and nozzles", gid="am-su",
             photos=[(B + "f15516e840549d65893d77ac3b1304c6", "Creality CR-10 Smart Pro, the main printer"),
                     (B + "2b188bbe4ba2a3f1512b5a6a5d88b0d0", "Finished bars on the table beside a printer"),
                     (B + "01dedaebd4161b62f9734c5c3314353c", "White PLA filament, 1.75 mm"),
                     (B + "1c93169072c96298e152fdd66850a96f", "Nozzles from 0.2 to 0.5 mm, one of the four settings")]),
        dict(kind="clip", tag="PRINTING", title="Three bars to a plate",
             text=("Each plate carries three ASTM D790 bars, printed flat with a brim at 210 °C on a 60 °C bed, in 0.1 mm layers, with three walls "
                   "and three solid layers at the top and the bottom. For every run the weight of the bars, the filament "
                   "length and the print time were noted."),
             video=B + "897f6b99bf324884b408b2fd2b54d8bb", poster=B + "5cfb6fdd82dc8682e6b008748e1f4ef0",
             cap="PRINTING · THREE BARS PER PLATE", wide=True),
        dict(kind="clip", tag="INFILL", title="The infill being laid down",
             text=("A close look along the bars while the nozzle fills them in: the infill lines go down inside the walls, "
                   "line by line, before the top layers close them. The clip ends on a wider view of the printer."),
             video=B + "e66110ea4ed24706810a2a2bd0b6bb69", poster=B + "eed8f1d64e4460be1e10e6b69e95b5cc",
             cap="PRINTING · INFILL CLOSE-UP · 35 S", wide=True),
        dict(kind="photos", tag="PRINTER REPAIR", title="A break in the printing: thermistor and extruder repaired", gid="am-rp",
             photos=[(B + "f69ca5774a92977a6dbeeecebd143ccf", "The old hotend, crusted with burnt filament"),
                     (B + "08915f75554b9a9c4da28d73d3fcf0e5", "Taken apart for cleaning"),
                     (B + "64901be8a264058e1d1ededb4eaaf69e", "The thermistor and heater cartridge"),
                     (B + "5db845e815e7edd086f35f10889d95a3", "The hotend going back in after the repair")]),
        dict(kind="photos", tag="SPECIMENS", title="108 runs, numbered and grouped", gid="am-sp",
             photos=[(B + "0ceadb773feeaf81fa5ba37af64e2ebb", "Top surface of the printed bars, close up"),
                     (B + "f9de45bc29f617263c1e263e35ea6332", "Plates of three bars, numbered by run"),
                     (B + "f8a93a9c766be334f82c87362fafeeb9", "Bars sorted into groups with coloured thread")]),
        dict(kind="clip", tag="THREE-POINT BENDING", title="Flexural test on a universal testing machine",
             text=("Each bar rests on two supports while the centre nose pushes it down at 2 mm per minute, on a Shimadzu "
                   "universal testing machine run from Trapezium X. The test gives the flexural strength, the flexural "
                   "modulus and how far a bar bends before it breaks."),
             video=B + "342006fa4507ef21d144914559eeadc5", poster=B + "ba4c225cb4b5fc6ad36d5f135d32d076",
             cap="SHIMADZU UTM · THREE-POINT BENDING"),
        dict(kind="photos", tag="BENDING SET-UP", title="Machine, fixture and the live curve", gid="am-bd",
             photos=[(B + "ec72df09e7d13287e92ced09bc2d2e34", "Shimadzu universal testing machine"),
                     (B + "e96b4788697ba8df5d68ef8ab6ffa1ba", "A bar on the supports before loading"),
                     (B + "f54dd03f293030f54ef90fa5ff5408be", "Force curve building up live in Trapezium X")]),
        dict(kind="clip", tag="SURFACE ROUGHNESS", title="Roughness across the top surface",
             text=("A Taylor Hobson stylus tester travels across the top of each bar and reads the average roughness, Ra, "
                   "several times per bar. A TR200 tester was used as well."),
             video=B + "d56dacfb1925775ad66f56ad9273cdad", poster=B + "c09c6b17df4018ac8d2c6c6f8fdf80a6",
             cap="TAYLOR HOBSON · Ra", wide=True),
        dict(kind="clip", tag="HARDNESS", title="Shore D on every bar",
             text=("An INSIZE Shore D durometer is pressed onto the bar and read from the dial, at more than one point on "
                   "each bar."),
             video=B + "27cd70915128a700ee37bca26cd952d8", poster=B + "95f327de20d2f754338a6360203f45b6",
             cap="SHORE D DUROMETER", wide=True),
        dict(kind="photos", tag="MEASURING TOOLS", title="Roughness, hardness and the printed surface", gid="am-ms",
             photos=[(B + "38ed4a0ec9898f1faf610a6a4d377bb7", "Taylor Hobson roughness tester with a bar"),
                     (B + "9e2c68421ce9992838361fb22f91c48c", "TR200 roughness tester"),
                     (B + "970d2f31b72265683f66f2676d750d43", "INSIZE Shore D durometer"),
                     (B + "c75c329b4557837d4339bbf1a7075af0", "Printed surface under close light")]),
        dict(kind="files", tag="STUDY DESIGN", title="What changes and what stays fixed",
             rows=[("INFILL PATTERN", "Stars · Hilbert curve · Octagram spiral"),
                   ("INFILL DENSITY", "30 · 50 · 70 %"),
                   ("NOZZLE", "0.2 · 0.3 · 0.4 · 0.5 mm"),
                   ("RASTER ANGLE", "15° · 45° · 75°"),
                   ("FIXED", "0.1 mm layers · 210 °C nozzle · 60 °C bed · full fan · brim · printed flat"),
                   ("SHELLS", "3 walls · 3 solid layers top and bottom"),
                   ("SPECIMEN", "ASTM D790 bar · 127 × 12.7 × 3.2 mm · PLA"),
                   ("RUNS", "108 · weight, filament length and print time noted for each"),
                   ("MEASURED", "Flexural strength and modulus · elongation at break · Ra · Shore D · surface analysis"),
                   ("STATUS", "Tests done · analysis and paper in progress · no results shown here yet")]),
    ],
    prev=(0, ""), next=(0, ""),
)


def page(theme, title):
    html = PP.page(STUDY, theme, title)
    html = html.replace("</style>", ".evhero .h3c{background:rgba(12,15,20,.72);color:#fff;padding:4px 8px;border-radius:5px}</style>", 1)
    # research study, not a project: research crumb, no part number, Research marked in the menu, a single way back
    html = html.replace('<a href="#">HOME</a> / <a href="#">PROJECTS</a> /', '<a href="#">HOME</a> / <a href="#">RESEARCH</a> /', 1)
    html = html.replace('<span>PART NO. <b>MZH-P-000</b></span>', '<span>STUDY · <b>IN PROGRESS</b></span>', 1)
    html = html.replace('<a href="#" class="on" aria-current="page">Projects</a>', '<a href="#">Projects</a>', 1)
    html = html.replace('<a href="#">Research</a>', '<a href="#" class="on" aria-current="page">Research</a>', 1)
    html = html.replace('<span>MODEL FILES</span>', '<span>STUDY DESIGN</span>', 1)
    a = html.index('<div class="nxt">')
    e = html.index("</div>", html.index("</a>", html.index("</a>", a) + 4)) + len("</div>")
    html = html[:a] + ('<div class="nxt" style="grid-template-columns:minmax(0,1fr)"><a class="card" href="#" style="text-align:left;align-items:flex-start">'
                       '<span class="k">← BACK TO</span><b>Research</b></a></div>') + html[e:]
    return html
