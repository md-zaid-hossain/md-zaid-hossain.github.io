"""Visible-text check on the built site: no em dash, en dash or spaced hyphen in text, title, alt or aria-label.
  python3 checks/dashinv.py dist        (prints 0 and exits 0 when clean)"""
import glob, os, re, sys
from html.parser import HTMLParser
PAT = re.compile(r"[—–]| - | -- ")


class P(HTMLParser):
    def __init__(s):
        super().__init__(); s.skip = 0; s.out = []

    def handle_starttag(s, t, a):
        if t in ("script", "style", "template"):
            s.skip += 1
        for k, v in a:
            if k in ("title", "alt", "aria-label", "placeholder") and v and PAT.search(v):
                s.out.append(f"@{k}: {v[:120]}")

    def handle_endtag(s, t):
        if t in ("script", "style", "template"):
            s.skip -= 1

    def handle_data(s, d):
        if not s.skip and PAT.search(d):
            s.out.append(d.strip()[:120])


bad = 0
for f in sorted(glob.glob(os.path.join(sys.argv[1] if len(sys.argv) > 1 else "dist", "**", "*.html"), recursive=True)):
    if "/_t/" in f:
        continue
    p = P(); p.feed(open(f, encoding="utf-8").read())
    for x in sorted(set(p.out)):
        bad += 1; print(f, "·", x)
print(bad)
sys.exit(1 if bad else 0)
