"""Project detail pages from data (EV page pattern, 2026-11-20). One dict per project; page() builds it.
Hero: turning 3D model (72-frame sprite from the real STEP) with a 3D MODEL | RENDER switch, spec list, buttons, stats.
Sections are optional and numbered in order: how it works (clip), motion study (clip), in SOLIDWORKS, renders,
model files. Every group of photos opens as a slideshow (slideshow.py). Facts come only from the project folders
in his files (listed per project in `src`)."""
import build_ev as EV
import slideshow as S
import videoplayer as VP

BK = lambda t, a, href="#": f'<a class="bkb" href="{href}"><s></s><s></s><s></s><s></s><span>{t}</span><i>{a}</i></a>'

# ---------------------------------------------------------------- data
DIFFERENTIAL = dict(
    key="differential", no=10, slug="car-differential",
    crumb="CAR DIFFERENTIAL", tags=["PERSONAL", "SOLIDWORKS 2022 · KEYSHOT", "APR 2022"],
    title="Car differential gearbox",
    lead=("An open differential modelled part by part in SOLIDWORKS: a two-piece housing, the bevel gear set, splined output "
          "shafts and a coupling, put together with mates and animated in a motion study. Rendered in KeyShot in 2025."),
    turntable="/_blob/bc09129e9b501a4bd795f82738c59d23", render="/_blob/8194e722c0f5fad57275db72757e5aba",
    render_alt="Car differential with the nickel housing closed, KeyShot render", glb="GLB 0.3 MB",
    spec=[("TYPE", "Personal project <em>· practice in gear assemblies</em>"),
          ("DATE", "Apr 2022 <em>· modelled</em> · Mar 2025 <em>· rendered</em>"),
          ("SOFTWARE", "SOLIDWORKS Premium 2022 · KeyShot"),
          ("PARTS", "6 modelled <em>· plus 2 ISO bevel gears and 6 ISO flange bolts</em>"),
          ("OUTPUT", "Parts, assembly, motion study, STEP, KeyShot renders and animation")],
    stats=[("14", "components"), ("6", "parts I modelled"), ("22 s", "motion study"), ("0.3 MB", "web 3D model")],
    sections=[
        dict(kind="clip", tag="HOW IT WORKS", title="What a differential does",
             text=("In a corner the outer wheel travels further than the inner one. The differential lets the two output "
                   "shafts turn at different speeds while both still get drive: the bevel gears inside the housing roll "
                   "around each other instead of locking the shafts together. In the clip the housing fades out so the "
                   "gears inside can be seen."),
             video="/_blob/4bde3d5a7019b457a2392bbe9a9b950f", poster="/_blob/811788c558c9477709f5099b0340e239",
             cap="KEYSHOT · HOUSING FADES OUT · 5.5 S", wide=True),
        dict(kind="clip", tag="MOTION STUDY", title="Taken apart and put back",
             text=("SOLIDWORKS Motion Study 1: the coupling, the housing and its six flange bolts move out along the shaft "
                   "axis, then the assembly closes again. A rotary motor is set up in the same study to turn the gears."),
             video="/_blob/30dd34873979eec3a8914880117cf3d5", poster="/_blob/3b3b0a6f98ad0974a7d3faae391c843c",
             cap="SOLIDWORKS · MOTION STUDY 1 · 22 S"),
        dict(kind="photos", tag="IN SOLIDWORKS", title="The assembly in SOLIDWORKS", gid="pd-sw",
             photos=[("/_blob/95d078114f07431c32e8faa093c8e9fb", "Housing shown transparent: the bevel gears and the cross shaft inside"),
                     ("/_blob/b3c6d44be49a7fe8763570d26cb37225", "The closed assembly with its six flange bolts")]),
        dict(kind="photos", tag="RENDERS", title="KeyShot renders", gid="pd-ks",
             photos=[("/_blob/8194e722c0f5fad57275db72757e5aba", "Housing closed: nickel housing, brass splines, black coupling"),
                     ("/_blob/4214a6b03b42e9c44ad8fa2309878626", "Housing removed: the bevel gear set on the cross shaft")]),
        dict(kind="files", tag="MODEL FILES", title="What is in the folder",
             rows=[("MAIN ASSY", "Assem1.SLDASM"), ("RENDER ASSY", "Assem1, KeyShot copy · SLDASM"),
                   ("PARTS", "Cover1 · Cover2 · Shaft · Joint · Gear01 · Gear02"), ("STANDARD", "Straight bevel gear (ISO) × 2 · hex flange bolt (ISO) × 6"),
                   ("EXCHANGE", "STEP · whole assembly · 9.8 MB"), ("WEB MODEL", "GLB · 0.3 MB · 14 parts"),
                   ("RENDERS", "KeyShot · 2 stills · 5.5 s animation"), ("RECORDING", "6 min screen recording of the assembly work")]),
    ],
    prev=(9, "Rotor of a DC Motor"), next=(11, "Quadcopter Drone"),
)

ROTOR = dict(
    key="rotor", no=9, slug="dc-motor-rotor",
    crumb="DC MOTOR ROTOR", tags=["PERSONAL", "SOLIDWORKS · KEYSHOT", "APR 2023"],
    title="Rotor of a DC motor",
    lead=("The armature of a small DC motor, modelled as one detailed part in SOLIDWORKS: the laminated core, the copper "
          "windings and the commutator on its shaft. A month later it went into a full motor with housing, magnets, "
          "brush holders and a pinion, and both were rendered in KeyShot."),
    turntable="/_blob/1c462a2c5621da6c75b2fde36b08f6f7", render="/_blob/bb01c910dee55a5926acae3adf43a3a3",
    render_alt="Rotor of a DC motor on its shaft, KeyShot render", glb="GLB 0.3 MB",
    spec=[("TYPE", "Personal project <em>· practice in detailed part modelling</em>"),
          ("DATE", "Apr 2023 <em>· rotor</em> · May 2023 <em>· motor assembly</em>"),
          ("SOFTWARE", "SOLIDWORKS · KeyShot"),
          ("PARTS", "Rotor as one part <em>· the motor has 9 parts</em>"),
          ("LATER", "Scaled down for the servo motor <em>· Aug 2023</em>"),
          ("OUTPUT", "Rotor part, motor assembly, STEP files, 11 KeyShot renders")],
    stats=[("1", "detailed rotor part"), ("9", "parts in the motor"), ("11", "KeyShot renders"), ("0.3 MB", "web 3D model")],
    sections=[
        dict(kind="photos", tag="RENDERS", title="The rotor", gid="pr-r",
             photos=[("/_blob/644d08d35a2f508157e1f66204e03b43", "Close-up: windings over the laminated core"),
                     ("/_blob/bb01c910dee55a5926acae3adf43a3a3", "The rotor on its shaft"),
                     ("/_blob/c9eb53db03e6aa5dec5eadb1d809f4e2", "The commutator end")]),
        dict(kind="photos", tag="IN THE MOTOR", title="Inside a full DC motor", gid="pr-m",
             photos=[("/_blob/bfe5cbf58984f10d93408805b07636fa", "The motor closed, with its pinion"),
                     ("/_blob/fb0090f23c97a9a4e7ca767dfe7a9730", "Housing removed: magnets around the rotor"),
                     ("/_blob/6fa31615320373400616cefcc9dd56b0", "Magnets, rotor and brush terminal"),
                     ("/_blob/893db426fd75c56f86b6a3b7199b6aa8", "End contact and the rotor"),
                     ("/_blob/4701d22ed32f649bc34c1b6d9199652c", "Commutator end with the brush holder"),
                     ("/_blob/67dd33d76f804ca998a51ce05ad6179e", "Rotor, bush and pinion"),
                     ("/_blob/fca5fd7888d38d03ab4bde1f4d5986a1", "The back of the motor"),
                     ("/_blob/86e7ef4372cab38af862f62be764531a", "Front view with the pinion")]),
        dict(kind="files", tag="MODEL FILES", title="What is in the folder",
             rows=[("ROTOR", "Part1 rotor.SLDPRT · 7.3 MB"), ("MOTOR ASSY", "DC Motor Assem2.SLDASM"),
                   ("PARTS", "Housing · rotor · cover · end contact · magnet · spacer · two brush parts · spur gear"),
                   ("EXCHANGE", "STEP · rotor 10.3 MB · motor 15.6 MB"), ("WEB MODEL", "GLB · 0.3 MB · rotor"),
                   ("RENDERS", "KeyShot · 3 rotor and 8 motor stills"), ("SCENES", "KeyShot .bip for the rotor and the motor"),
                   ("RECORDING", "Screen recording of the work · May 2023")]),
    ],
    prev=(8, "HAAS VF-2 CNC Milling"), next=(10, "Car Differential Gearbox"),
)

QUADCOPTER = dict(
    key="quadcopter", no=11, slug="quadcopter-drone",
    crumb="QUADCOPTER DRONE", tags=["PERSONAL", "SOLIDWORKS · KEYSHOT", "NOV 2022"],
    title="Quadcopter drone",
    lead=("A small quadcopter modelled in SOLIDWORKS: a two-plate spider frame with truss arms, four motors and propellers, "
          "the battery pack, a distribution board and the electronics between the plates, held with standard screws and nuts. "
          "Animated in a motion study in 2022 and rendered in KeyShot in 2025."),
    turntable="/_blob/76f58a21cc8c2ed5061960485d73f8cc", render="/_blob/d5f691053d2440b363e7c428d955d6a3",
    render_alt="Quadcopter drone with white propellers and a mint battery pack, KeyShot render", glb="GLB 0.2 MB",
    spec=[("TYPE", "Personal project <em>· practice in assemblies</em>"),
          ("DATE", "Nov 2022 <em>· modelled</em> · Mar 2025 <em>· rendered</em>"),
          ("SOFTWARE", "SOLIDWORKS · KeyShot"),
          ("PARTS", "13 modelled <em>· plus standard M2 and M3 screws, M3 and M4 nuts</em>"),
          ("OUTPUT", "Parts, assembly, motion study, STEP, KeyShot render")],
    stats=[("13", "parts I modelled"), ("4", "motors and propellers"), ("77 s", "motion study recording"), ("0.2 MB", "web 3D model")],
    sections=[
        dict(kind="clip", tag="MOTION STUDY", title="Around the drone in SOLIDWORKS",
             text=("A SOLIDWORKS motion study takes the camera around the drone and in close to the frame, the electronics "
                   "between the plates and a motor mount. The clip is 24 seconds from a 77-second recording."),
             video="/_blob/bc42084e55e357838de5a9dc27c208db", poster="/_blob/487ff1d7e841e8aaa90454787cb32bda",
             cap="SOLIDWORKS · MOTION STUDY · 24 S"),
        dict(kind="photos", tag="IN SOLIDWORKS", title="The assembly in SOLIDWORKS", gid="pq-sw",
             photos=[("/_blob/4766a1eb8f05e4ae559ee483736eaa5b", "The full assembly"),
                     ("/_blob/1dbb4c2acba68c50562bea0b5d2eb5b9", "Close views: the electronics stack and a motor mount")]),
        dict(kind="files", tag="MODEL FILES", title="What is in the folder",
             rows=[("MAIN ASSY", "Quadcopter Drone.SLDASM"), ("PARTS", "Drone01 to Drone13: spider base and tops, board, spinner, spacer, connector, pillar, fan, motor, battery, two electrical units"),
                   ("STANDARD", "ASME pan head screws M2, M3 · hex nuts M3, M4"), ("EXCHANGE", "STEP · whole assembly · 5.2 MB"),
                   ("WEB MODEL", "GLB · 0.2 MB"), ("RENDER", "KeyShot · 1 still · scene .bip"),
                   ("RECORDING", "Motion study · 77 s · Nov 2022"), ("VIDEO", "Edited showcase video · Mar 2025")]),
    ],
    prev=(10, "Car Differential Gearbox"), next=(12, "Servo Motor"),
)

SERVO = dict(
    key="servo", no=12, slug="servo-motor",
    crumb="SERVO MOTOR", tags=["PERSONAL", "SOLIDWORKS", "AUG 2023"],
    title="Servo motor",
    lead=("A micro servo modelled in SOLIDWORKS with a clear housing, so the gear train, the DC motor and the output horn "
          "can be seen together. The gears are ISO spur gears with a 0.25 mm module, and the motor inside reuses my DC "
          "motor model, scaled down."),
    turntable="/_blob/4cf513e299491772f1bb1b64dd730de5", render="/_blob/a32827d757242f59c0357ef67276e6e3", render_label="SOLIDWORKS",
    render_alt="Servo motor in SOLIDWORKS with a clear housing showing the gear train", glb="GLB 0.6 MB",
    spec=[("TYPE", "Personal project <em>· gear trains and small mechanisms</em>"),
          ("DATE", "Aug 2023"),
          ("SOFTWARE", "SOLIDWORKS"),
          ("GEARS", "ISO spur gears, module 0.25 mm, 39 and 10 teeth <em>· plus one modelled gear</em>"),
          ("PARTS", "3 housing covers, shaft, horn, screw, motor <em>· 3 gear sub-assemblies</em>"),
          ("OUTPUT", "Parts, assembly, STEP, 4 views, LinkedIn post")],
    stats=[("0.25 mm", "gear module"), ("3", "gear sub-assemblies"), ("17 s", "recording"), ("0.6 MB", "web 3D model")],
    sections=[
        dict(kind="clip", tag="IN MOTION", title="Through the clear housing",
             text=("A 17-second recording of the assembly in SOLIDWORKS, seen through the clear housing: the horn on top, "
                   "the gear stages under it and the small DC motor at the bottom, all in one compact case."),
             video="/_blob/4408a44280772d9a9ad11460cd5939b0", poster="/_blob/a54bd35fd3b4199587de4487fb5b1662",
             cap="SOLIDWORKS · AUG 2023 · 17 S"),
        dict(kind="photos", tag="IN SOLIDWORKS", title="Four views", gid="ps-sw",
             photos=[("/_blob/a32827d757242f59c0357ef67276e6e3", "Horn, gear train and motor"),
                     ("/_blob/5136a879f2c4d36cd44cd231b262de2c", "Front view"),
                     ("/_blob/f36363734aae5b56046aa1d613036386", "Gear stages and motor from the side"),
                     ("/_blob/c8e300d195694ea5d7f702332cd4a101", "The housing from below")]),
        dict(kind="photos", tag="SHARED", title="The LinkedIn post", gid="ps-li",
             photos=[("/_blob/9e97bd57fe68b8e19a8a77651d07ef05", "Cover image of my LinkedIn post on the servo motor")]),
        dict(kind="files", tag="MODEL FILES", title="What is in the folder",
             rows=[("MAIN ASSY", "Assem1.SLDASM"), ("SUB-ASSY", "gear_sub1 · gear_sub2 · gear_sub3"),
                   ("PARTS", "Top, middle and bottom cover · shaft · gear4 · screw · horn · two more parts"),
                   ("MOTOR", "DC Motor as part · Rotor Scaling (from the DC motor model)"),
                   ("STANDARD", "ISO spur gears 0.25M · 39T and 10T"), ("EXCHANGE", "STEP · whole assembly · 23 MB"),
                   ("WEB MODEL", "GLB · 0.6 MB"), ("VIDEO", "Post video · Aug 2023 · edited version Mar 2025")]),
    ],
    prev=(11, "Quadcopter Drone"), next=(13, "Payloader"),
)

BICYCLE = dict(
    key="bicycle", no=14, slug="bicycle",
    crumb="BICYCLE", tags=["PERSONAL", "SOLIDWORKS", "OCT 2021"],
    title="Bicycle",
    lead=("A BMX-style bicycle assembled in SOLIDWORKS from nine parts: frame, steering with the handlebar, two spoked "
          "wheels with tyres, sprocket, chain, pedal and seat. Started in October 2021; the STEP file was exported in 2025."),
    turntable="/_blob/1b9b6a57ba2665a9bc57424e35eb23ff", render="/_blob/9846adf37faa287c927695fbdc3ab900", render_label="SOLIDWORKS",
    render_alt="BMX-style bicycle in SOLIDWORKS with purple tyres and seat", glb="GLB 0.7 MB",
    spec=[("TYPE", "Personal project <em>· practice in assemblies</em>"),
          ("DATE", "Oct 2021 <em>· first parts</em> · Mar 2025 <em>· STEP export</em>"),
          ("SOFTWARE", "SOLIDWORKS"),
          ("PARTS", "9 <em>· steering, frame, two tyres, sprocket, seat, pedal, chain, pin</em>"),
          ("OUTPUT", "Parts, assembly, STEP, 3 views")],
    stats=[("9", "parts I modelled"), ("2", "spoked wheels"), ("30 MB", "STEP assembly"), ("0.7 MB", "web 3D model")],
    sections=[
        dict(kind="photos", tag="IN SOLIDWORKS", title="Three views", gid="pb-sw",
             photos=[("/_blob/b48f202b18653d59b6ac1e1e712d3ecf", "The full bicycle"),
                     ("/_blob/259148513cca80139a3b6e6c73f5dea1", "Rear wheel, pedal and frame"),
                     ("/_blob/41a93d171e2d5635f3505e94cdc7918b", "Handlebar, seat and pedal from the front")]),
        dict(kind="files", tag="MODEL FILES", title="What is in the folder",
             rows=[("MAIN ASSY", "Bicycle.SLDASM"), ("PARTS", "Steering · frame · tyre · front tyre · sprocket · seat · paddle · inner chain · pin"),
                   ("EXCHANGE", "STEP · whole assembly · 30 MB"), ("WEB MODEL", "GLB · 0.7 MB")]),
    ],
    prev=(13, "Payloader"), next=(1, "Aluminium Foil Plant (50 TPD)"),
)

FOIL = dict(
    key="foil-plant", no=1, slug="aluminium-foil-plant",
    crumb="ALUMINIUM FOIL PLANT", tags=["CLIENT", "SOLIDWORKS 2024 · C# API", "NOV 2026"],
    title="Aluminium foil plant, 50 TPD",
    lead=("A full 3D layout of a 50-tonne-per-day aluminium foil plant for a client: the 2.3 ha site, 12 buildings, "
          "roads and utilities, and the 12-step production line from melting to dispatch. The model was built through "
          "the SOLIDWORKS API by PlantBuilder, a C# tool in my SOLIDWORKS automation workspace, from a written plant "
          "specification, then turned into renders and walk-through videos."),
    turntable="/_blob/e64ab056c535242ad30565e00da6ecd1", render="/_blob/9b03896b9ba60793c47be3f65d32f26f",
    render_alt="Aluminium foil plant 3D layout, overview", glb="GLB 1.5 MB",
    spec=[("TYPE", "Client project <em>· plant layout, client name kept private</em>"),
          ("DATE", "Oct to Nov 2026 <em>· delivered 1 Nov 2026</em>"),
          ("SOFTWARE", "SOLIDWORKS 2024 · C# on the SOLIDWORKS API · motion studies"),
          ("SITE", "230 m × 100 m <em>· 2.3 ha, 12 buildings</em>"),
          ("OUTPUT", "CAD, coloured STEP, eDrawings, 7 images, 4 videos, README")],
    stats=[("50 TPD", "plant capacity"), ("12", "process steps"), ("2.3 ha", "site"), ("4", "videos")],
    sections=[
        dict(kind="clip", tag="THE REEL", title="The plant in 30 seconds",
             text=("The portfolio reel: in through the main gate, along the 12 process steps in order, past dispatch, then "
                   "up and back over the whole site. Cut from three longer videos made for the client: a 60 s overview, "
                   "a 120 s drive-through and a 3 min site walk, all filmed in SOLIDWORKS with motion studies."),
             video="/_blob/4e16d486d765c8148527f8185bf6cb3a", poster="/_blob/e2988699a4f1bb4e85f7ffb00cf19683",
             cap="PORTFOLIO REEL · 30 S", wide=True),
        dict(kind="steps", tag="PROCESS LINE", title="Twelve steps, melting to dispatch",
             steps=["Melting and holding furnace", "Continuous casting machine", "Hot rolling mill", "Cold rolling mill",
                    "Foil rolling mill", "Finished goods store", "Annealing furnace", "Foil nerving mill",
                    "Slitting and rewinding", "Laminating and embossing", "Foil separation and inspection", "Packing and dispatch"],
             note="Twelve machine cells in one 154 m production hall: steps 1 to 6 along the north row, 7 to 12 along the south row."),
        dict(kind="photos", tag="CLIENT IMAGES", title="What the client received", gid="pf-img",
             photos=[("/_blob/9b03896b9ba60793c47be3f65d32f26f", "Overview of the site"),
                     ("/_blob/05685a5c4a55f4e3479105d4e01a6de2", "Overview with the material flow"),
                     ("/_blob/cba30de8b3fc5a6ef8fcdfa98c0e0ced", "Overview with labels and legend"),
                     ("/_blob/7a25d750f142746b9dc6f99d5267f031", "Production hall close-up"),
                     ("/_blob/2904388e9d27b221686be5ef53c1626b", "Top view with labels"),
                     ("/_blob/846c07b7717497ea3ac3af9343515176", "Production hall from above")]),
        dict(kind="files", tag="DELIVERED", title="What was in the package",
             rows=[("CAD", "Plant part, three label layers, presentation assembly · SOLIDWORKS 2024"),
                   ("EXCHANGE", "Coloured STEP, clean and labelled · eDrawings EASM"),
                   ("IMAGES", "7 stills: overviews, flow, hall, top views, legend"),
                   ("VIDEOS", "60 s overview · 120 s drive-through · 3 min site walk · 30 s highlights"),
                   ("SPEC", "Plant specification: site, buildings, machine cells, colours"),
                   ("TOOL", "PlantBuilder · C# console app on the SOLIDWORKS API"),
                   ("WEB MODEL", "GLB · 1.5 MB · coloured, roofs see-through"),
                   ("README", "Client package guide · PDF")]),
    ],
    prev=(14, "Bicycle"), next=(2, "Distillation Plant"),
)

PAYLOADER = dict(
    key="payloader", no=13, slug="payloader",
    crumb="PAYLOADER", tags=["PERSONAL", "SOLIDWORKS", "JAN 2024 TO SEP 2025"],
    title="Payloader",
    lead=("A wheel loader modelled in SOLIDWORKS: the rear loader frame with its cab, the front body, the boom with two "
          "hydraulic cylinders, a rocker arm linkage for the bucket, the bucket, two axles with differentials and four "
          "rims with lettered tyres. Started in January 2024 and finished in September 2025."),
    turntable="/_blob/a3b5a343110e71489033e13d48ef6aea", render="/_blob/26ef04f5b28f358034472d175065bf8b", render_label="STILL",
    render_alt="Wheel loader 3D model with the bucket lowered", glb="GLB 0.3 MB",
    spec=[("TYPE", "Personal project <em>· practice in linkages and assemblies</em>"),
          ("DATE", "Jan 2024 <em>· first parts</em> · Sep 2025 <em>· final assembly</em>"),
          ("SOFTWARE", "SOLIDWORKS"),
          ("PARTS", "15 modelled <em>· 48 components in the assembly, with 20 screws</em>"),
          ("OUTPUT", "Parts, sub-assembly, two assemblies, STEP")],
    stats=[("15", "parts I modelled"), ("48", "components"), ("2", "hydraulic linkages"), ("0.3 MB", "web 3D model")],
    sections=[
        dict(kind="photos", tag="VIEWS", title="Three views of the model", gid="pp-v",
             photos=[("/_blob/94f70093a3e8e46c23ac2216c4bb231e", "Front three-quarter: bucket, boom and rocker arms"),
                     ("/_blob/818755ed82965aa71accf817dd228067", "From the front: bucket, axle and differential"),
                     ("/_blob/5e4a219355966f86adadb2266870e6ac", "Rear three-quarter: engine cover, cab and lift linkage")]),
        dict(kind="files", tag="MODEL FILES", title="What is in the folder",
             rows=[("MAIN ASSY", "2 Payloader Assem 2.SLDASM <em>· earlier: 1 Payloader Assem</em>"), ("SUB-ASSY", "SUP ASSEMPLY.SLDASM"),
                   ("BODY", "Loader · front body · bucket"), ("LINKAGE", "Boom · boom cylinder and rod · rocker arm, its cylinder and rod · connecting rod"),
                   ("RUNNING GEAR", "Differential · axle rod · rim · tyre"), ("FASTENERS", "Screw × 20"),
                   ("EXCHANGE", "STEP · whole assembly · 12.5 MB · Nov 2026"), ("WEB MODEL", "GLB · 0.3 MB")]),
    ],
    prev=(12, "Servo Motor"), next=(14, "Bicycle"),
)

GEARHOLDER = dict(
    key="gear-holder", no=5, slug="gear-pinion-phone-holder",
    crumb="GEAR-PINION PHONE HOLDER", tags=["3D PRINTING", "SOLIDWORKS · CREALITY PRINT", "SEP 2023"],
    title="Gear-pinion phone holder",
    lead=("A phone stand where a curved rack holder sits in a toothed base, so the phone can be set upright or tilted back. "
          "The idea comes from an open design on Thingiverse; I modelled my own version in SOLIDWORKS, added my Z mark "
          "and a personalised version for a friend, sliced it in Creality Print and printed it on an Ender-3 V2 Neo."),
    turntable="/_blob/4dcd2ff03122f14bbeb9dc4d434406a9", render="/_blob/f61d32bd14801c4126a1644d9e18d3ea", render_label="PRINT",
    render_alt="The printed gear-pinion phone holder on a desk", glb="GLB 0.04 MB",
    spec=[("TYPE", "Personal 3D printing project"),
          ("CONCEPT", 'Geared smartphone holder, Thingiverse 4982411 <a class="evl" href="https://www.thingiverse.com/thing:4982411" target="_blank" rel="noopener">ORIGINAL ↗</a>'),
          ("MY PART", "Own SOLIDWORKS model, Z mark, personalised version, slicing and printing"),
          ("PRINTER", "Ender-3 V2 Neo <em>· 0.4 mm nozzle, PLA 1.75 mm</em>"),
          ("PRINT TIME", "Base 5 h 22 min <em>· personalised base 6 h 56 min</em>"),
          ("DATE", "Sep 2023")],
    stats=[("2", "printed parts"), ("6 h 56 min", "longest print"), ("2", "printed versions"), ("0.04 MB", "web 3D model")],
    sections=[
        dict(kind="photos", tag="THE PRINTS", title="Printed and in use", gid="pg-pr",
             photos=[("/_blob/1f61d2471a0d7f961bbe6477477391a5", "The first print, pink and silver PLA"),
                     ("/_blob/8835d897a0624db9e48bcf013ee2f7df", "Holding a phone upright"),
                     ("/_blob/c3881cf5d0a99f1699c2ccd930dddb61", "Tilted back for a phone on its side"),
                     ("/_blob/dedcc19d237f3b1113e5881cb0e65570", "In hand: the rack teeth on the holder"),
                     ("/_blob/d7d52b99623aa59179d0bb103a612996", "The personalised green version"),
                     ("/_blob/739c4cfe6771954b4a1bbed3c27b5ad7", "The green version from the back")]),
        dict(kind="photos", tag="IN SOLIDWORKS", title="My model of the two parts", gid="pg-sw",
             photos=[("/_blob/9a3e6dde0092160f43cb6bf0cdb02e22", "Holder and base, plain"),
                     ("/_blob/80b2655c013d757d10e08648dc2357a7", "The rack teeth along the curved holder"),
                     ("/_blob/54b47002be7556abd9476f22d3b7ceda", "With my Z mark cut through the holder"),
                     ("/_blob/517f062bdc0fb5d473a56b0f84a838fc", "Z marks on the holder and the base")]),
        dict(kind="photos", tag="SLICING", title="Ready for the printer", gid="pg-sl",
             photos=[("/_blob/d459bbf3cc86367a726e5e2a6b93ca26", "Sliced in Creality Print: the layers"),
                     ("/_blob/da93b41c974d2334b5806dd4974229e5", "Sliced in Creality Print: walls and infill")]),
        dict(kind="files", tag="MODEL FILES", title="What is in the folder",
             rows=[("MODEL", "Assem1.SLDASM · Base.SLDPRT · Holder.SLDPRT"), ("EXCHANGE", "STEP · 3.2 MB · STL for both parts"),
                   ("SLICING", "Creality Print projects · G-code for the Ender-3 V2 Neo"), ("VERSIONS", "Plain, Z mark, personalised"),
                   ("ORIGINAL", "Thingiverse 4982411 files kept apart, for reference"), ("WEB MODEL", "GLB · 0.04 MB")]),
    ],
    prev=(4, "Lathe Head-stock Gearbox"), next=(6, "3-2-1 Pin Locator"),
)

HEADSTOCK = dict(
    key="headstock", no=4, slug="lathe-headstock-gearbox",
    crumb="LATHE HEAD-STOCK GEARBOX", tags=["ACADEMIC LAB · IPE 4126", "SOLIDWORKS", "FEB 2024"],
    title="Lathe head-stock gearbox",
    lead=("The speed gearbox in the head-stock of the lab lathe, modelled in SOLIDWORKS for the first 4-1 lab: the box, "
          "four shafts, eleven spur gears and an internal gear with a 0.25 mm module, and the levers that shift the gears "
          "for each speed. A SOLIDWORKS motion study turns the whole gear train."),
    turntable="/_blob/b8cd3443e48a2c29d3e16c6ef715bce7", render="/_blob/363982d405b93925a2ced6d0bc8dca90", render_label="SOLIDWORKS",
    render_alt="Lathe head-stock gearbox in SOLIDWORKS with a see-through box", glb="GLB 0.2 MB",
    spec=[("TYPE", "Academic lab <em>· 4-1 lab 01, KUET</em>"),
          ("DATE", "Feb 2024 <em>· modelled</em> · Jun 2024 <em>· motion study video</em>"),
          ("SOFTWARE", "SOLIDWORKS <em>· motion study</em>"),
          ("GEARS", "11 spur gears, 72 to 25 teeth, and 1 internal gear <em>· module 0.25 mm</em>"),
          ("PARTS", "Box, four shafts, internal gear cap, two gear changers, motor belt holder, power transmission changer"),
          ("OUTPUT", "Parts, assembly, STEP, STL for every part, motion study video")],
    stats=[("12", "gears"), ("0.25 mm", "gear module"), ("4", "shafts"), ("0.2 MB", "web 3D model")],
    sections=[
        dict(kind="clip", tag="MOTION STUDY", title="The gear train turning",
             text=("A SOLIDWORKS motion study drives the input shaft and turns every gear in the box, with the box shown "
                   "see-through. The clip is 20 seconds from the 2 min 17 s motion study video."),
             video="/_blob/20f13d6f11bb59e5260b8298821821ec", poster="/_blob/e126cfe01f581a85c87a884e376cadae",
             cap="SOLIDWORKS · MOTION STUDY · 20 S", wide=True),
        dict(kind="files", tag="MODEL FILES", title="What is in the folder",
             rows=[("MAIN ASSY", "1.Assem.SLDASM"), ("PARTS", "Box · Shaft1 to Shaft4 · CapInternlGear · GearChanger01, 02 · Motor Belt Holder · Power Transmition Changer"),
                   ("STANDARD", "Metric spur gears 0.25M, 25T to 72T · internal spur gear 40T"), ("EXCHANGE", "STEP · 5.5 MB · STL for every part"),
                   ("WEB MODEL", "GLB · 0.2 MB"), ("VIDEOS", "Motion study 2 min 17 s · edited animation · two screen recordings")]),
    ],
    prev=(3, "EV Charging Station"), next=(5, "Gear-Pinion Phone Holder"),
)

PINLOCATOR = dict(
    key="pin-locator", no=6, slug="3-2-1-pin-locator",
    crumb="3-2-1 PIN LOCATOR", tags=["ACADEMIC LAB · IPE 4226", "SOLIDWORKS · CURA", "DEC 2024"],
    title="3-2-1 pin locator",
    lead=("A fixture that locates a cube workpiece against three faces, following the 3-2-1 locating principle, with pins "
          "on three axes. Modelled and drawn on A3 sheets in SOLIDWORKS for the Tool Engineering sessional by our group "
          "B1, then sliced in Cura and printed on the lab's Ultimaker 3 Extended."),
    turntable="/_blob/4ecd22e66f8a8cc534fcf31fb99cee7e", render="/_blob/e787032859e903f564318cdc5857e494", render_label="PRINT",
    render_alt="The printed 3-2-1 pin locator with its pins, on its drawing", glb="GLB 0.02 MB",
    spec=[("TYPE", "Academic lab <em>· group B1</em>"),
          ("COURSE", "IPE 4226 Tool Engineering Sessional, lab 01 <em>· KUET</em>"),
          ("DATE", "Dec 2024"),
          ("SOFTWARE", "SOLIDWORKS · Cura 5.3"),
          ("PRINTER", "Ultimaker 3 Extended <em>· 0.4 mm nozzle</em>"),
          ("PRINT TIME", "Locator body 4 h 26 min")],
    stats=[("3", "locating axes"), ("2", "A3 drawings"), ("4 h 26 min", "print of the body"), ("0.02 MB", "web 3D model")],
    sections=[
        dict(kind="photos", tag="THE PRINT", title="Printed fixture and workpiece", gid="pl-pr",
             photos=[("/_blob/6f68c03107264a5a3f9e257e792b0ade", "The fixture with the workpiece and pins in place"),
                     ("/_blob/56f8556ad43476e5715e2d4b26479e06", "Fixture, workpiece and the three pins apart")]),
        dict(kind="photos", tag="DRAWINGS", title="A3 drawing sheets", gid="pl-dr",
             photos=[("/_blob/00a99f88128cf01f6fe4227cf2080ba5", "Assembly sheet with the parts list"),
                     ("/_blob/baede386ec93ce6b39c69aec52d7081a", "Detail sheet with all dimensions")]),
        dict(kind="photos", tag="MODEL AND SLICING", title="From model to printer", gid="pl-sl",
             photos=[("/_blob/596ab3612dacf8bad986241453372155", "Four views of the assembly in SOLIDWORKS"),
                     ("/_blob/7233321cb1818a160b80c5e621e6109f", "Sliced for printing, with supports")]),
        dict(kind="files", tag="MODEL FILES", title="What is in the folder",
             rows=[("MAIN ASSY", "Ass 3 2 1 Pin Locator.SLDASM"), ("PARTS", "PIN locator body · WP workpiece · Axis pin"),
                   ("DRAWINGS", "A3 assembly and A3 detail sheets · SLDDRW and PDF"), ("EXCHANGE", "STEP · STL for each part"),
                   ("G-CODE", "Ultimaker 3 Extended · body and workpiece"), ("WEB MODEL", "GLB · 0.02 MB")]),
    ],
    prev=(5, "Gear-Pinion Phone Holder"), next=(7, "3D-Printed Bench Vice"),
)

VICE = dict(
    key="vice", no=7, slug="bench-vice",
    crumb="3D-PRINTED BENCH VICE", tags=["ACADEMIC LAB · IPE 4226", "SOLIDWORKS · CREALITY SLICER", "JAN 2025"],
    title="3D-printed bench vice",
    lead=("A working vice for accurate alignment, made for the Tool Engineering sessional by our group B1: a body with a "
          "fixed jaw, a sliding jaw driven by a printed lead screw, and a handle. Modelled and drawn in SOLIDWORKS, sliced "
          "in Creality Slicer and printed in PLA on the lab's Creality CR-10 Smart."),
    turntable="/_blob/ab5124e4d050789f84ece7e1a12b2828", render="/_blob/8028db101e8077d300e015a6936bfc0f", render_label="PRINT",
    render_alt="The printed vice, white body with a green sliding jaw and screw", glb="GLB 0.2 MB",
    spec=[("TYPE", "Academic lab <em>· group B1</em>"),
          ("COURSE", "IPE 4226 Tool Engineering Sessional, lab 03 <em>· KUET</em>"),
          ("DATE", "Jan 2025"),
          ("SOFTWARE", "SOLIDWORKS · Creality Slicer 4.8"),
          ("PRINT", "Creality CR-10 Smart <em>· PLA, 0.3 mm layers, about 13 h and 84 m of filament</em>"),
          ("DRAWINGS", "Three sheets: assembly, body, screw and jaw details")],
    stats=[("7", "components"), ("3", "drawing sheets"), ("13 h", "print time"), ("0.2 MB", "web 3D model")],
    sections=[
        dict(kind="photos", tag="THE PRINT", title="The printed vice", gid="pv-pr",
             photos=[("/_blob/3f85c731a80e815474d5a23cd6682f0c", "Body, sliding jaw and screw"),
                     ("/_blob/85b13fb86896f2d847982c3fbe519e24", "The jaw closed on the screw"),
                     ("/_blob/8b89ed58705691ff79194a912553bb6c", "From above, with the handle"),
                     ("/_blob/d1c37efecefce318d9eb69235cae24a5", "On the desk, side view")]),
        dict(kind="photos", tag="IN SOLIDWORKS", title="The assembly", gid="pv-sw",
             photos=[("/_blob/0977b5e8cf498ed5ae512c8cf0bcf095", "Body, jaw, screw and handle"),
                     ("/_blob/802985fbbbcd8755e7de6a3456c07620", "From the handle side"),
                     ("/_blob/f770a6e2546628894e5da5bc7bf9a484", "Top view")]),
        dict(kind="photos", tag="DRAWINGS", title="Three drawing sheets", gid="pv-dr",
             photos=[("/_blob/0dd0b28731ecb68fdc1c5fa49a1a66c4", "Sheet 1: assembly with the parts list"),
                     ("/_blob/1f9675f917a10bab34f4fc54c17f2725", "Sheet 2: the body"),
                     ("/_blob/245a0e5a2567f5f971313e4b80409b87", "Sheet 3: screw, jaw and small parts")]),
        dict(kind="files", tag="MODEL FILES", title="What is in the folder",
             rows=[("MAIN ASSY", "Assemble, vice for accurate alignment · SLDASM"), ("PARTS", "Part2 × 2 · Part3 · Part6 · Part7 · Part9 · Part10"),
                   ("DRAWINGS", "Sheet01 to Sheet03 · SLDDRW and PDF"), ("EXCHANGE", "STEP · 2.9 MB · STL for each part"),
                   ("G-CODE", "Creality Slicer · one print job"), ("WEB MODEL", "GLB · 0.2 MB")]),
    ],
    prev=(6, "3-2-1 Pin Locator"), next=(8, "HAAS VF-2 CNC Milling"),
)

DISTILLATION = dict(
    key="distillation", no=2, slug="distillation-plant",
    crumb="DISTILLATION PLANT", tags=["CLIENT · SOAP PROCESS PLANT", "SOLIDWORKS", "OCT 2024"],
    title="Distillation plant",
    lead=("The distillation section of a soap manufacturer's process plant, laid out in SOLIDWORKS to the client's process "
          "requirements: vessels, condensers, receivers and tanks on three floor levels, the pumps between them, every pipe "
          "run, two cooling towers, platforms and stairs. For the same client I also modelled the evaporator plant and the "
          "lye treatment area."),
    turntable="/_blob/368bfdc7ccaf96b4471403fd6ff07835", render="/_blob/eb0f5b5fc7064eaaa764a3c50344044d", render_label="STILL",
    render_alt="Distillation plant 3D layout on three floor levels with stainless vessels, pumps and two cooling towers", glb="GLB 1.5 MB",
    spec=[("TYPE", "Client project <em>· soap manufacturer, name kept private</em>"),
          ("DATE", "Oct to Nov 2024 <em>· modelled</em> · Mar 2025 <em>· revised</em>"),
          ("SOFTWARE", "SOLIDWORKS"),
          ("SCOPE", "Distillation plant layout <em>· plus the evaporator plant and the lye treatment area</em>"),
          ("CONTENTS", "Vessels, condensers, receivers, tanks, pumps, piping, cooling towers, platforms, stairs"),
          ("OUTPUT", "SOLIDWORKS part and assembly, STEP, STL, screenshots for the client")],
    stats=[("3", "plant areas"), ("3", "floor levels"), ("2", "cooling towers"), ("1.5 MB", "web 3D model")],
    sections=[
        dict(kind="photos", tag="DISTILLATION", title="The distillation plant in SOLIDWORKS", gid="pdi-d",
             photos=[("/_blob/c9fe275d9ad5db21396c7b7ea7d9c943", "The whole plant on its three floor levels"),
                     ("/_blob/2dcd52961e0ed299ab4383579ccdb0fa", "From above, with see-through floors"),
                     ("/_blob/25b9d5b7220cfa50776db8aede4f6b43", "Main vessel, condensers and receivers"),
                     ("/_blob/70ade6cc718a18ef847cfe97e3963ff4", "Cooling tower, stairs and the pipe runs"),
                     ("/_blob/1480e3726b5922397120a22c31a322ba", "Pumps and valves under the main vessel"),
                     ("/_blob/148d6d9dd8ab73ed4c468c3ec7c8e08a", "Top floor with the second cooling tower")]),
        dict(kind="photos", tag="EVAPORATOR", title="Same client: the evaporator plant", gid="pdi-e",
             photos=[("/_blob/79168cb3b70ebe9dc4b6fb7af2a1c0b6", "Evaporator plant with its cooling tower"),
                     ("/_blob/a5805229be21a6f66dfd8f1f9edce3df", "Effect vessels and heat exchangers"),
                     ("/_blob/c1a03fb992f0e3bca11f2ce47c03c372", "Close view of the effect vessels and the salt side")]),
        dict(kind="photos", tag="TREATMENT AREA", title="Same client: the lye treatment area", gid="pdi-t",
             photos=[("/_blob/43becc656ce48fc0eae388c20f3d1f85", "Treatment tanks below, filter presses on the platform"),
                     ("/_blob/6c699a882d8850c1fb2a2772f42e6f61", "The treatment area from above"),
                     ("/_blob/284e0dcec71ea507109c2c77ae327803", "Treatment tanks with their feed pumps"),
                     ("/_blob/d1d52a3b8fd937d6d23f644594cbdbe7", "Platform, lye storage tank and stairs")]),
        dict(kind="files", tag="MODEL FILES", title="What is in the folder",
             rows=[("MAIN", "Distilation Plant · SLDPRT and SLDASM"),
                   ("EQUIPMENT", "Vessel · Condenser · Receiver · drop tank · Seal Tank · Entrainment · Barometric Shower · Curde Tank 9, 10 · Salt Box · Stair"),
                   ("EXCHANGE", "STEP · 324 MB · STL"), ("OTHER AREAS", "Evaporator Plant · SLDASM · Treatment Area Assembley · SLDASM"),
                   ("WEB MODEL", "GLB · 1.5 MB"), ("CLIENT", "Name kept private")]),
    ],
    prev=(1, "Aluminium Foil Plant (50 TPD)"), next=(3, "EV Charging Station"),
)

HAAS = dict(
    key="haas-vf2", no=8, slug="haas-vf2-cnc-milling",
    crumb="HAAS VF-2 CNC MILLING", tags=["TRAINING · IEM, KUET", "FUSION CAM · HAAS VF-2", "SEP 2025"],
    title="HAAS VF-2 CNC milling",
    lead=("When the department installed a HAAS VF-2 milling machine, HAAS ran a five-day hands-on training. I modelled a "
          "test plate, planned its toolpaths in Fusion CAM, posted the NC program for the VF-2 and cut the part in aluminium: "
          "the first design of mine to come off a CNC machine. The CAM steps were the ones I had practised in simulation in "
          "the CAM sessional that January."),
    still=("THE PART", "/_blob/a1c64945495b41f6e83b904454073bea", "The finished aluminium test plate with its pockets and drilled holes"),
    still_cap="PHOTO · CUT IN ALUMINIUM",
    render="/_blob/e66636836070410b811493a23bf16b77", render_label="AT THE VF-2",
    render_alt="Zaid holding the finished part in front of the HAAS VF-2",
    spec=[("TYPE", "Hands-on training <em>· five days, run by HAAS</em>"),
          ("WHERE", "Department of IEM, KUET"),
          ("DATE", "Sep 2025 <em>· CAM sessional practice Jan 2025</em>"),
          ("MACHINE", "HAAS VF-2 vertical machining centre <em>· BT40 tool holders, vise on the table</em>"),
          ("SOFTWARE", "Fusion 360 <em>· CAM, simulation, HAAS post processor</em>"),
          ("TOOLS", "50 mm face mill, 4 mm bull nose and flat end mills, 8 mm drill")],
    stats=[("5", "days of training"), ("4", "cutting tools"), ("6", "toolpaths in the lab part"), ("Aluminium", "first CNC part")],
    sections=[
        dict(kind="photos", tag="PLAN", title="From CAM to the machine", gid="ph-pl",
             photos=[("/_blob/17b9e602b5b32b84c904c6cef400551e", "HAAS VF-2 set up as the machine in Fusion CAM"),
                     ("/_blob/534b3cc47712ad99707ed5b0b49529c5", "Toolpath simulation: face, pockets, drills, adaptive clearing"),
                     ("/_blob/3f9e5f779905e58783fede123b55dbdf", "The posted NC program for the VF-2")]),
        dict(kind="photos", tag="SET UP AND CUT", title="On the machine", gid="ph-ct",
             photos=[("/_blob/5eabe120f0c300a1c0025edd43f7276f", "The VF-2 with the vise on the table"),
                     ("/_blob/3a9de8f2d1a6f78048ee8ed3f73ccc68", "BT40 tool holder"),
                     ("/_blob/b765fff7edb53a1ce1341813117b7ed3", "4 mm end mill in its collet"),
                     ("/_blob/2958665e5921d2853297db91e6e1e562", "The program running on the HAAS control"),
                     ("/_blob/89ef557c7d7ae6f3c66a824269e0a0be", "Face milling the stock"),
                     ("/_blob/e10c8610b05fffef4943fb68e8430839", "Pocketing with flood coolant"),
                     ("/_blob/21aabb9acd788e0ac336323d2e583bdc", "Detail work with the small end mill"),
                     ("/_blob/9e26b9ca40d80999fdecf51d4d901720", "Taking the cut part out of the vise")]),
        dict(kind="clip", tag="CAM SESSIONAL · JAN 2025", title="Practice first: a toolpath simulation",
             text=("Lab 01 of the CAM and Robotics sessional (IPE 4228): a bracket machined in Fusion simulation with six "
                   "toolpaths (three facing passes, a 2D contour and two adaptive clearing passes) and three tools, a 30 mm face "
                   "mill and 10 mm and 3 mm flat end mills, at 5000 rpm. The posted program runs to 11,849 lines. The clip plays "
                   "the 75 second recording at double speed."),
             video="/_blob/a50ca80b7bae92bc315ef2545efc23a1", poster="/_blob/1d4bf7b592a85cba7d5e521a7ad284d0",
             cap="FUSION CAM · SIMULATION · 2× SPEED", wide=True),
        dict(kind="files", tag="FILES", title="What is in the folder",
             rows=[("FUSION", "Experiment 01.00 v1 · f3d <em>· setup, toolpaths, simulation</em>"),
                   ("NC PROGRAM", "01.eia · 11,849 lines"), ("RECORDING", "Toolpath simulation · 1 min 21 s"),
                   ("TRAINING PART", "NC program 5001 for the VF-2 · 4 tools"),
                   ("PHOTOS", "31 from the training, 11 on this page"), ("MACHINE", "HAAS VF-2 · Department of IEM, KUET")]),
    ],
    prev=(7, "3D-Printed Bench Vice"), next=(9, "Rotor of a DC Motor"),
)

PAGES = [FOIL, DISTILLATION, HEADSTOCK, GEARHOLDER, PINLOCATOR, VICE, HAAS, ROTOR, DIFFERENTIAL, QUADCOPTER, SERVO, PAYLOADER, BICYCLE]


CSS = """
/* ===== project pages (prefix pp) ===== */
.ppclip{display:grid;grid-template-columns:minmax(0,1.35fr) minmax(0,1fr);gap:22px;align-items:start}
.ppclip.wide{grid-template-columns:minmax(0,1.6fr) minmax(0,1fr)}
.ppv{position:relative;border:1px solid var(--line2);border-radius:10px;overflow:hidden;background:#EDEEF0}
.ppv video{display:block;width:100%;height:auto}
.ppv:hover{border-color:var(--acc)}.ppv{transition:border-color .3s ease}
.ppv>span{pointer-events:none;position:absolute;left:10px;bottom:10px;font:600 10.5px 'IBM Plex Mono',monospace;letter-spacing:.08em;color:#fff;background:rgba(12,15,20,.72);padding:4px 8px;border-radius:5px}
.pptx p{margin:0;font-size:15.5px;line-height:1.65;color:var(--body)}
.ppg{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:14px}
.ppg.n1{grid-template-columns:minmax(0,1fr);max-width:880px}.ppg.n1 label{aspect-ratio:16/9}
.ppg.n3,.ppg.n6{grid-template-columns:repeat(3,minmax(0,1fr))}
.ppg.n8{grid-template-columns:repeat(4,minmax(0,1fr))}.ppg.n8 label{aspect-ratio:4/3}
.ppg label{position:relative;display:block;margin:0;border:1px solid var(--line);border-radius:8px;overflow:hidden;background:#15181E;aspect-ratio:16/10;cursor:zoom-in}
.ppg img{width:100%;height:100%;object-fit:cover;display:block;transition:transform .6s ease}
.ppg label:hover img{transform:scale(1.03)}
.ppg label span{position:absolute;left:8px;bottom:8px;right:8px;font:500 12.5px Inter,sans-serif;color:#fff;background:rgba(12,15,20,.72);padding:5px 8px;border-radius:5px}
.ppst{display:grid;grid-template-columns:repeat(6,minmax(0,1fr));border:1px solid var(--line2);border-radius:10px;overflow:hidden;background:var(--surface)}
.ppst>div{padding:14px 14px 16px;border-left:1px solid var(--line);border-top:1px solid var(--line);display:flex;flex-direction:column;gap:6px}
.ppst>div:nth-child(6n+1){border-left:0}.ppst>div:nth-child(-n+6){border-top:0}
.ppst b{font:600 18px 'IBM Plex Mono',monospace;color:var(--acc-t)}
.ppst span{font-size:14px;line-height:1.4;color:var(--strong)}
.ppsn{margin:12px 0 0;font-size:14.5px;color:var(--body)}
@media (max-width:960px){.ppclip,.ppclip.wide{grid-template-columns:1fr}.ppst{grid-template-columns:repeat(3,minmax(0,1fr))}
  .ppst>div{border-left:1px solid var(--line);border-top:1px solid var(--line)}.ppst>div:nth-child(3n+1){border-left:0}.ppst>div:nth-child(-n+3){border-top:0}}
@media (max-width:760px){.ppst{grid-template-columns:1fr 1fr}.ppst>div{border-left:1px solid var(--line);border-top:1px solid var(--line)}.ppst>div:nth-child(odd){border-left:0}.ppst>div:nth-child(-n+2){border-top:0}}
@media (max-width:960px){.ppg.n6{grid-template-columns:1fr 1fr}.ppg.n3{grid-template-columns:1fr 1fr}.ppg.n3 label:first-child{grid-column:span 2}.ppg.n8{grid-template-columns:1fr 1fr}}
@media (max-width:760px){.ppg,.ppg.n3{grid-template-columns:1fr}.ppg.n3 label:first-child{grid-column:auto}.ppg.n4,.ppg.n6,.ppg.n8{grid-template-columns:1fr 1fr}.ppg.n4 label span,.ppg.n6 label span,.ppg.n8 label span{display:none}}
"""


def _section(n, s, views):
    head = (f'<div class="sh"><div class="eb"><span class="ebn">{n:02d}</span><span class="ebt">{s["tag"]}</span><span class="ebl"></span></div>'
            f'<div class="shr"><h2 class="h2">{s["title"]}</h2></div></div>')
    if s["kind"] == "clip":
        vid = (f'<video src="{s["video"]}" poster="{s["poster"]}" autoplay muted loop playsinline aria-label="{s["cap"]}"></video>')
        body = (f'<div class="ppclip{" wide" if s.get("wide") else ""}"><div class="ppv">'
                f'{VP.panel(__import__("hashlib").md5(s["video"].encode()).hexdigest()[:8], vid, s["video"], s["poster"], s["title"], s["cap"])}<span>{s["cap"]}</span></div>'
                f'<div class="card pptx" style="padding:20px 22px"><p>{s["text"]}</p></div></div>')
    elif s["kind"] == "photos":
        rid, html = S.group(s["gid"], [(src, cap) for src, cap in s["photos"]], s["tag"])
        views.append(html)
        body = f'<div class="ppg n{len(s["photos"])}">' + "".join(f'<label for="{rid(i)}"><img src="{src}" alt="{cap}"><span>{cap}</span></label>'
                                             for i, (src, cap) in enumerate(s["photos"])) + "</div>"
    elif s["kind"] == "steps":
        body = ('<div class="ppst">' + "".join(f'<div><b>{i:02d}</b><span>{t}</span></div>' for i, t in enumerate(s["steps"], 1))
                + f'</div><p class="ppsn">{s["note"]}</p>')
    else:
        body = '<div class="files fw">' + "".join(f'<span class="k">{k}</span><span>{v}</span>' for k, v in s["rows"]) + "</div>"
    sid = ' id="model"' if s["kind"] == "files" else ""
    return f'<section class="sec"{sid}>{head}{body}</section>'


def body(p):
    views = []
    tags = "".join(f"<span>{t}</span>" for t in p["tags"])
    spec = "".join(f'<span class="k">{k}</span><span>{v}</span>' for k, v in p["spec"])
    stats = "".join(f"<div><b>{n}</b><span>{t}</span></div>" for n, t in p["stats"])
    secs = "".join(_section(i, s, views) for i, s in enumerate(p["sections"], 1))
    (pn, pt), (nn, nt) = p["prev"], p["next"]
    if p.get("turntable"):      # turning 3D model first, render second
        l1 = "3D MODEL"
        first = (f'<div class="h3s" role="img" aria-label="3D model of the {p["title"].lower()} turning slowly">'
                 f'<span class="tt3" style="background-image:url({p["turntable"]})"></span>')
        cap = (f'<span class="h3c">FIG. 01 · 3D MODEL · {p["glb"]}</span><span class="h3b"><i title="Turn">{EV.ICO_ORBIT}</i>'
               f'<i title="Zoom in">{EV.ICO_PLUS}</i><i title="Zoom out">{EV.ICO_MINUS}</i><i title="Full screen">{EV.ICO_FULL}</i>'
               f'<i title="View in your room (AR)">{EV.ICO_AR}</i></span>')
    else:                       # no 3D model kept (training work): two photos, same switch
        l1, (src1, alt1) = p["still"][0], p["still"][1:]
        first = ('<style>@media (max-width:760px){.h3w .h3s.ph .tt3{inset:42px 0 0 0;aspect-ratio:auto}}</style>'
                 f'<div class="h3s ph"><span class="tt3" role="img" aria-label="{alt1}" style="background-image:url({src1});'
                 f'background-size:cover;background-position:center;animation:none"></span>')
        cap = f'<span class="h3c">FIG. 01 · {p["still_cap"]}</span>'
    return f"""
  <main class="wrap" style="position:relative;z-index:1">
    <section class="evh">
      <div class="crumb"><a href="#">HOME</a> / <a href="#">PROJECTS</a> / {p["crumb"]}</div>
      <div class="pn"><span>PART NO. <b>MZH-P-{p["no"]:03d}</b></span>{tags}</div>
      <h1 class="h1">{p["title"]}</h1>
      <p class="lead">{p["lead"]}</p>
      <div class="evhero">
        <div class="h3w"><input type="radio" class="v1" name="hv" id="hv1" checked><input type="radio" class="v2" name="hv" id="hv2">
          <div class="h3t"><label class="l1" for="hv1">{l1}</label><label class="l2" for="hv2">{p.get("render_label", "RENDER")}</label></div>
          {first}
            <img class="rimg" src="{p["render"]}" alt="{p["render_alt"]}">
            {cap}</div></div>
        <div class="evside">
          <div class="spec2">{spec}</div>
          <div class="acts">{BK("MODEL FILES", "↓", "#model")}{BK("3D MODEL", "↓") if p.get("turntable") else ""}</div>
        </div>
      </div>
      <div class="sb2" style="margin-top:22px">{stats}</div>
    </section>
    {secs}
    <section class="sec" style="padding-top:56px">
      <div class="nxt">
        <a class="card" href="#"><span class="k">← PREVIOUS<span class="pn"> · MZH-P-{pn:03d}</span></span><b>{pt}</b></a>
        <a class="card" href="#"><span class="k">NEXT<span class="pn"> · MZH-P-{nn:03d}</span> →</span><b>{nt}</b></a>
      </div>
    </section>
  </main>
""", "".join(views)


def page(p, theme, title, wrap=None):
    """wrap(main_html) lets a proposal board put the page inside its own frame."""
    import build_home as H
    html = H.page(theme, title)
    html = html.replace("<style>", "<style>" + EV.CSS + S.CSS + CSS, 1)
    main, views = body(p)
    if wrap:
        main = wrap(main)
    a = html.index("  <!-- Hero: static page backdrop")
    e = html.index("  </main>") + len("  </main>")
    html = html[:a] + main + html[e:]
    html = html.replace("</body>", f'<div class="ssv">{views}</div>\n</body>', 1)
    return html.replace('<a href="#">Projects</a>', '<a href="#" class="on" aria-current="page">Projects</a>', 1)

# ---- real site: the lists above are replaced by content/*.yml (build/content_io.py) ----
import content_io as _C
PAGES = _C.load_projects()[0]
