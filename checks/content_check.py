"""Checks content/*.yml before every build (GitHub Actions runs it; run it yourself too):
  python3 checks/content_check.py
Fails (exit 1) on: a missing media file, an em or en dash, "/" or "+" used as shorthand in text,
a phone number, a roll number, a client name that must stay hidden, or a photo with GPS location data. Prints each problem with its file."""
import glob, hashlib, os, re, sys
import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
HIDDEN = {"b6750d994f8db799", "0a4f997fc65ecfb1", "fc962003ba1aa86a"}   # client names and the roll number, kept as hashes so they are not written here
BANNED = [r"\bNID\b"]
PHONE = re.compile(r"(\+?880[\s-]?1\d{3}|\b01[3-9]\d{2}[\s-]?\d{6}\b)")
DASH = re.compile(r"[—–]| - | -- ")
SLASH = re.compile(r"(?<![\w./:])([A-Za-z]{2,})/([A-Za-z]{2,})(?![\w./])")
PLUS = re.compile(r"\w \+ \w|\b[A-Za-z]{2,}\+[A-Za-z]{2,}\b")
OK_SLASH = {"CAD/CAM", "AS/RS"}          # standard names kept as written
OK_PLUS = {"Sensor + Zone"}             # a model name from a published paper
SKIP_KEYS = {"url", "doi", "focus"}
problems = []


def text_ok(where, s):
    if re.match(r"^(media/|https?://|mailto:)", s):
        if s.startswith("media/") and not os.path.exists(s):
            problems.append((where, "missing file", s))
        return
    for pat in BANNED:
        if re.search(pat, s):
            problems.append((where, "must stay hidden", s[:90]))
    for w in re.findall(r"\w+", s.lower()):
        if hashlib.sha256(w.encode()).hexdigest()[:16] in HIDDEN:
            problems.append((where, "a name or number that must stay hidden", s[:90]))
    if PHONE.search(s):
        problems.append((where, "phone number", s[:90]))
    if DASH.search(s):
        problems.append((where, "dash: use a period, comma, colon or ·", s[:90]))
    for m in SLASH.finditer(s):
        if m.group(0) not in OK_SLASH:
            problems.append((where, f'"{m.group(0)}": write "and" or "or"', s[:90]))
    if any(m.group(0) not in "".join(OK_PLUS) for m in PLUS.finditer(s)):
        problems.append((where, '"+" shorthand: write "and" or "with"', s[:90]))


def walk(where, x, key=""):
    if isinstance(x, dict):
        for k, v in x.items():
            walk(where, v, str(k))
    elif isinstance(x, list):
        for v in x:
            walk(where, v, key)
    elif isinstance(x, str) and key not in SKIP_KEYS:
        text_ok(where, x)
    elif isinstance(x, str) and key == "url" and x.startswith("media/"):
        text_ok(where, x)


for f in sorted(glob.glob("content/**/*.yml", recursive=True)):
    try:
        walk(f, yaml.safe_load(open(f, encoding="utf-8")))
    except yaml.YAMLError as e:
        problems.append((f, "YAML error (check indentation and quotes)", str(e).splitlines()[0]))
# photos straight from a phone may carry the place they were taken (GPS): that must not be published
try:
    from PIL import Image
    for f in glob.glob("media/**/*", recursive=True):
        if f.lower().endswith((".jpg", ".jpeg", ".png", ".webp", ".tif", ".tiff")):
            try:
                with Image.open(f) as im:
                    if 34853 in im.getexif():
                        problems.append((f, "photo has GPS location data: remove it (Claude can) and upload again", ""))
            except Exception:
                pass
except ImportError:
    pass

for p in problems:
    print(" · ".join(p))
print(len(problems), "problems" if len(problems) != 1 else "problem")
sys.exit(1 if problems else 0)
