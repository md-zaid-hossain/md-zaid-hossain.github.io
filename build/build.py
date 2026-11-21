"""Build the site: content/*.yml + media/  ->  dist/  (static HTML, CSS and a little JavaScript).

  python3 build/build.py            # writes dist/
  python3 build/build.py --serve    # then opens a local preview on http://localhost:8000

How it works
1. The approved mockup's page builders (build/site_src/, same code as the design canvas) render every page
   once per colour theme (dark and light x red, blue, green). Their data comes from content/*.yml.
2. The six versions of a page are merged into one HTML file: shared CSS stays as it is, theme-only CSS is
   scoped to :root[data-theme="..."], and the few theme-only pieces of markup are kept per theme.
3. Canvas-only parts are removed, links get their real addresses, fonts are self-hosted, and site.js adds
   the theme picker, the live Dhaka clock and keyboard support.
"""
import datetime as _dt
import difflib
import hashlib
import html as _html
import json
import os
import re
import shutil
import subprocess
import sys

BUILD = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(BUILD)
SRC = os.path.join(BUILD, "site_src")
DIST = os.path.join(REPO, "dist")
os.environ.setdefault("SITE_CONTENT", os.path.join(REPO, "content"))
sys.path.insert(0, SRC)
sys.path.insert(0, BUILD)
os.chdir(SRC)  # some builders read files next to themselves

import yaml  # noqa: E402
import content_io as C  # noqa: E402

THEMES = ["dark", "dark_blue", "dark_green", "light", "light_blue", "light_green"]
SITE = yaml.safe_load(open(os.path.join(REPO, "content", "site.yml"), encoding="utf-8"))
URL = SITE["url"].rstrip("/")
BUILT = _dt.datetime.now(_dt.timezone(_dt.timedelta(hours=6)))


# ------------------------------------------------------------------ 1. render
def render_all():
    import build_home as H
    # one clock for the whole build, so every theme version shows the same time (site.js makes it live)
    fixed = H.clock_sample()
    H.clock_sample = lambda: fixed
    import type_scale as TS, slideshow as S
    import build_projects as BP, build_education as BE, build_research as BR, build_ev as EV, build_experience as BX
    import build_awards as BA, build_gallery as BG, build_notfound as BN, project_pages as PP
    pages = {
        "/": ("Md. Zaid Hossain · Industrial engineer", lambda t: TS.apply(H.page(t, "x"))),
        "/projects/": ("Projects", lambda t: TS.apply(BP.projects_page(t, "x"))),
        "/projects/ev-charging-station/": ("EV charging station", lambda t: TS.apply(EV.ev_page(t, "x"))),
        "/research/": ("Research", lambda t: TS.apply(S.from_lightboxes(BR.research_page(t, "x"), BR.GROUPS))),
        "/experience/": ("Experience", lambda t: TS.apply(BX.experience_page(t, "x"))),
        "/education/": ("Education", lambda t: TS.apply(S.from_lightboxes(BE.education_page(t, "x"), BE.GROUPS))),
        "/awards/": ("Awards and certificates", lambda t: TS.apply(S.from_lightboxes(BA.awards_page(t, "x"), BA.GROUPS))),
        "/gallery/": ("Gallery", lambda t: TS.apply(BG.gallery_page(t, "x"))),
        "/404.html": ("Page not found", lambda t: TS.apply(BN.notfound_page(t, "x"))),
    }
    for p in PP.PAGES:
        pages[f"/projects/{p['slug']}/"] = (p["title"][0].upper() + p["title"][1:], (lambda p: lambda t: TS.apply(PP.page(p, t, "x")))(p))
    out = {}
    for route, (title, f) in pages.items():
        out[route] = (title, {t: f(t) for t in THEMES})
    return out, fixed


# ------------------------------------------------------------------ 2. merge the six theme versions
def css_chunks(css):
    """Split CSS into top-level pieces (rules and at-rule blocks); comments dropped."""
    css = re.sub(r"/\*.*?\*/", "", css, flags=re.S)
    out, depth, start, i, q = [], 0, 0, 0, None
    while i < len(css):
        ch = css[i]
        if q:
            if ch == "\\":
                i += 1
            elif ch == q:
                q = None
        elif ch in "\"'":
            q = ch
        elif ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                out.append(css[start:i + 1].strip()); start = i + 1
        elif ch == ";" and depth == 0:
            out.append(css[start:i + 1].strip()); start = i + 1
        i += 1
    tail = css[start:].strip()
    if tail:
        out.append(tail)
    return [c for c in out if c]


def split_selectors(sel):
    parts, depth, cur = [], 0, ""
    for ch in sel:
        if ch in "([":
            depth += 1
        elif ch in ")]":
            depth -= 1
        if ch == "," and depth == 0:
            parts.append(cur); cur = ""
        else:
            cur += ch
    parts.append(cur)
    return [p.strip() for p in parts if p.strip()]


def scope(chunk, themes):
    """Limit one CSS chunk to some themes."""
    pre = ":root:is(" + ",".join(f'[data-theme="{t}"]' for t in themes) + ")"
    head, body = chunk.split("{", 1)
    head = head.strip()
    if head.startswith("@"):
        name = head.split()[0].lower()
        if name in ("@media", "@supports", "@container", "@layer"):
            inner = body.rsplit("}", 1)[0]
            return head + "{" + "".join(scope(c, themes) for c in css_chunks(inner)) + "}"
        raise ValueError(f"theme-only {name} block cannot be scoped: {chunk[:80]}")
    sels = []
    for s in split_selectors(head):
        if s.startswith(":root"):
            sels.append(pre + s[5:])
        elif s.startswith("html"):
            sels.append(pre + s[4:])
        elif s.startswith("body"):
            sels.append(pre + " " + s)
        else:
            sels.append(pre + " " + s)
    return ",".join(sels) + "{" + body


def merge_css(per_theme):
    """per_theme: {theme: css text}. Returns one stylesheet."""
    merged = [[c, {THEMES[0]}] for c in css_chunks(per_theme[THEMES[0]])]
    for t in THEMES[1:]:
        cur = css_chunks(per_theme[t])
        sm = difflib.SequenceMatcher(None, [m[0] for m in merged], cur, autojunk=False)
        new = []
        for op, i1, i2, j1, j2 in sm.get_opcodes():
            if op == "equal":
                for k in range(i1, i2):
                    merged[k][1].add(t); new.append(merged[k])
            else:
                new += merged[i1:i2]
                new += [[c, {t}] for c in cur[j1:j2]]
        merged = new
    out = []
    for c, ts in merged:
        out.append(c if len(ts) == len(THEMES) else scope(c, sorted(ts, key=THEMES.index)))
    return "\n".join(out)


STATE_LINES = ('class="sw ', 'class="tog ', 'class="mnu"')   # theme picker state: site.js sets it


class _Attrs(__import__("html.parser").parser.HTMLParser):
    """Attribute values of a piece of markup, in source order, and how many top-level elements it has."""
    VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "source", "track", "wbr"}

    def __init__(self, s):
        super().__init__(convert_charrefs=True)
        self.vals, self.tags, self.depth, self.roots = [], [], 0, 0
        self.feed(s); self.close()

    def handle_starttag(self, tag, attrs):
        if self.depth == 0:
            self.roots += 1
        self.tags.append(tag)
        self.vals += [v if v is not None else "" for _, v in attrs]
        if tag not in self.VOID:
            self.depth += 1

    def handle_startendtag(self, tag, attrs):
        if self.depth == 0:
            self.roots += 1
        self.tags.append(tag)
        self.vals += [v if v is not None else "" for _, v in attrs]

    def handle_endtag(self, tag):
        if tag not in self.VOID:
            self.depth -= 1


def merge_body(per_theme):
    """Line by line. Theme-picker lines: the dark version (site.js sets the state). A line whose versions differ
    only in attribute values (picture links, colours): the dark version plus a list of the values each theme
    changes, applied by site.js. Anything else: one copy per theme, shown by CSS."""
    lines = {t: per_theme[t].split("\n") for t in THEMES}
    n = len(lines[THEMES[0]])
    assert all(len(v) == n for v in lines.values()), "theme versions differ in line count"
    out, swaps = [], {}
    for i in range(n):
        vs = {t: lines[t][i] for t in THEMES}
        base = vs[THEMES[0]]
        if len(set(vs.values())) == 1 or any(s in base for s in STATE_LINES):
            out.append(base); continue
        parsed = {t: _Attrs(v) for t, v in vs.items()}
        b = parsed[THEMES[0]]
        shell = lambda v: re.sub(r'"[^"]*"', '""', v)
        if b.roots == 1 and all(p.tags == b.tags and len(p.vals) == len(b.vals) and shell(vs[t]) == shell(base) for t, p in parsed.items()):
            k = str(len(swaps))
            swaps[k] = {t: {j: v for j, (a, v) in enumerate(zip(b.vals, p.vals)) if a != v} for t, p in parsed.items() if t != THEMES[0]}
            swaps[k] = {t: m for t, m in swaps[k].items() if m}
            m = re.match(r"(\s*<[a-zA-Z][^\s/>]*)", base)
            # data-zs goes last in the first tag, so attribute numbers stay the same
            first_end = base.index(">", m.end())
            close = "/>" if base[first_end - 1] == "/" else ">"
            cut = first_end - (1 if close == "/>" else 0)
            out.append(base[:cut] + f' data-zs="{k}"' + base[cut:]); continue
        groups = {}
        for t, v in vs.items():
            groups.setdefault(v, []).append(t)
        for v, ts in groups.items():
            out.append(f'<div class="thv" data-th="{" ".join(ts)}">{v}</div>')
    return "\n".join(out), swaps


def split_doc(h):
    styles = re.findall(r"<style>(.*?)</style>", h, flags=re.S)
    m = re.search(r"</helmet>(.*)</body>", h, flags=re.S)
    body = re.sub(r'<script type="text/x-dc".*?</script>', "", m.group(1), flags=re.S)   # canvas-only script
    body = body.replace("</x-dc>", "")   # viewers (slideshows, video players) sit after it: keep them
    body = re.sub(r"<style>.*?</style>", "", body, flags=re.S)
    return "\n".join(styles), body


# ------------------------------------------------------------------ 3. finish one page
def media_paths(h):
    m = json.load(open(os.path.join(REPO, "media", "blob_to_media.json")))
    return re.sub(r"/_blob/([0-9a-f]{32})", lambda x: "/" + m[x.group(1)], h)


NAV = {"Research": "/research/", "Projects": "/projects/", "Experience": "/experience/", "Awards": "/awards/",
       "Gallery": "/gallery/", "Education": "/education/", "Contact": "/#s-contact", "Home": "/"}


def link_for(text, route, ctx):
    t = re.sub(r"<[^>]+>", " ", text)
    t = " ".join(_html.unescape(t).split())
    cv = "/" + SITE["cv"]
    rules = [
        (r"^(\d\d )?(Research|Projects|Experience|Awards|Gallery|Education|Contact)( →)?$", lambda m: NAV[m.group(2)]),
        (r"^(HOME|ZH Md\. Zaid Hossain)$", "/"), (r"^PROJECTS$", "/projects/"),
        (r"^(CV|DOWNLOAD CV ↓|DOWNLOAD CV)$", cv),
        (r"^ALL REVISIONS →$", "https://github.com/md-zaid-hossain/md-zaid-hossain.github.io/commits/main"),
        (r"^All projects →$|^Projects page →$|^Selected client work", "/projects/"),
        (r"^All publications →$|^RESEARCH PAGE →$|^→ 04 PUBLICATIONS", "/research/"),
        (r"^Full timeline →$|^Roles and recognition", "/experience/"),
        (r"^Results & certificates →$|^Certificate of Achievement", "/education/"),
        (r"^→ 21 CERTIFICATIONS|^4× CSWA|^3× CHAMPION|^CAD competition results", "/awards/"),
        (r"^DSW · KUET", "/education/#b5"),
        (r"^→ 30\+ CAD", "/projects/"),
        (r"^PHOTOS IN GALLERY", "/gallery/#g-comp"),
        (r"^PROJECT PAGE →$|^3D MODEL →$", "/projects/ev-charging-station/"),
        (r"^\+17 more projects", "https://grabcad.com/md.zaid.hossain-1/models"),
        (r"^BACK TO HOME", "/"), (r"^CONTACT →$", "/#s-contact"), (r"^SEE PROJECTS", "/projects/"),
        (r"^$", "/projects/ev-charging-station/"),       # Awards: the EV picture
        (r"^(FEATURE REPORT|RULEBOOK · PDF|THE QUESTION PDF)", "HIDE"),   # EV files: add them to media/ev/ and link them here
    ]
    for pat, dest in rules:
        m = re.search(pat, t)
        if m:
            return dest(m) if callable(dest) else dest
    m = re.match(r"^(← PREVIOUS|NEXT) · MZH-P-(\d{3})", t)
    if m:
        return ctx["by_no"].get(int(m.group(2)))
    if t.startswith("3D MODEL"):
        return ctx.get("model")
    return None


def fix_links(h, route, ctx):
    missing = []

    def a(m):
        tag, inner = m.group(1), m.group(2)
        if "data-cite" in tag:       # CITE: site.js copies the citation
            return m.group(0)
        dest = link_for(inner, route, ctx)
        if dest is None:
            missing.append(re.sub(r"<[^>]+>", " ", inner).strip()[:50])
            return m.group(0)
        if dest == "HIDE":           # a file that is not in media/ yet: leave the button out
            return ""
        extra = ' download' if dest.endswith((".pdf", ".glb")) else ""
        if dest.startswith("http"):
            extra += ' target="_blank" rel="noopener"'
        new_href = ' href="' + dest + '"'
        return "<a" + tag.replace(' href="#"', new_href) + extra + ">" + inner + "</a>"
    h = re.sub(r'<a((?:\s[^>]*)?\shref="#"[^>]*)>(.*?)</a>', a, h, flags=re.S)
    return h, missing


FONTS = [("Inter", 400, "inter-latin-400-normal"), ("Inter", 500, "inter-latin-500-normal"), ("Inter", 600, "inter-latin-600-normal"),
         ("Space Grotesk", 500, "space-grotesk-latin-500-normal"), ("Space Grotesk", 600, "space-grotesk-latin-600-normal"),
         ("Space Grotesk", 700, "space-grotesk-latin-700-normal"),
         ("IBM Plex Mono", 500, "ibm-plex-mono-latin-500-normal"), ("IBM Plex Mono", 600, "ibm-plex-mono-latin-600-normal")]
FONT_CSS = "".join(f"@font-face{{font-family:'{f}';font-style:normal;font-weight:{w};font-display:swap;src:url(/assets/fonts/{n}.woff2) format('woff2')}}"
                   for f, w, n in FONTS)

# the canvas board scrolls inside .scr; the real page scrolls the document
REAL_CSS = """
html{scroll-padding-top:84px;-webkit-text-size-adjust:100%}
body{margin:0}
.zh{height:auto!important;min-height:100vh;overflow:visible!important;overflow-x:clip!important}
.zh .scr{position:relative!important;inset:auto!important;overflow:visible!important}
.thv{display:contents}
.skip{position:absolute;left:-9999px;top:8px;z-index:100;padding:10px 14px;border-radius:6px;background:var(--acc,#C14B3C);color:#fff;font:600 14px 'Inter',sans-serif;text-decoration:none}
.skip:focus{left:12px}
@media (prefers-reduced-motion:reduce){*,*::before,*::after{animation-duration:.001ms!important;animation-iteration-count:1!important;transition-duration:.001ms!important;scroll-behavior:auto!important}}
"""


def theme_css(per_theme_css):
    """Hide other themes' copies; give <html> the page colour so overscroll matches."""
    css = "".join(f':root[data-theme="{t}"] .thv:not([data-th~="{t}"]){{display:none}}' for t in THEMES)
    for t in THEMES:
        m = re.search(r"\.zh\{--bg:(#[0-9A-Fa-f]{3,8})", per_theme_css[t])
        if m:
            css += f':root[data-theme="{t}"]{{background:{m.group(1)};color-scheme:{"dark" if t.startswith("dark") else "light"}}}'
    return css


INIT_JS = ("(function(){try{var m=localStorage.getItem('zh-mode')||'dark',a=localStorage.getItem('zh-accent')||'red';"
           "if(m==='auto')m=matchMedia('(prefers-color-scheme: light)').matches?'light':'dark';"
           "document.documentElement.setAttribute('data-theme',m+(a==='red'?'':'_'+(a==='blue'?'blue':'green')));}catch(e){}})();")


def head(title, route, desc, image):
    full = title if route == "/" else f"{title} · Md. Zaid Hossain"
    canon = URL + (route if route != "/404.html" else "/")
    pre = "".join(f'<link rel="preload" href="/assets/fonts/{n}.woff2" as="font" type="font/woff2" crossorigin>'
                  for n in ("inter-latin-400-normal", "space-grotesk-latin-600-normal", "ibm-plex-mono-latin-600-normal"))
    return f"""<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{_html.escape(full)}</title>
<meta name="description" content="{_html.escape(desc)}">
<link rel="canonical" href="{canon}">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<meta name="theme-color" content="#0C0F14">
<meta property="og:type" content="website"><meta property="og:site_name" content="Md. Zaid Hossain">
<meta property="og:title" content="{_html.escape(full)}"><meta property="og:description" content="{_html.escape(desc)}">
<meta property="og:url" content="{canon}"><meta property="og:image" content="{URL}/{image}">
<meta name="twitter:card" content="summary_large_image">
{pre}
<script>{INIT_JS}</script>"""


def person_ld():
    d = {"@context": "https://schema.org", "@type": "Person", "name": SITE["name"], "url": URL + "/",
         "jobTitle": "Industrial Engineer", "email": "mailto:" + SITE["email"],
         "address": {"@type": "PostalAddress", "addressLocality": "Dhaka", "addressCountry": "BD"},
         "sameAs": [p["url"] for p in SITE["profiles"]]}
    return f'<script type="application/ld+json">{json.dumps(d, ensure_ascii=False)}</script>'


def finish(route, title, variants, ctx, status_html):
    css_t, body_t = {}, {}
    for t, h in variants.items():
        css_t[t], body_t[t] = split_doc(media_paths(h))
    css = merge_css(css_t)
    body, swaps = merge_body(body_t)
    body, missing = fix_links(body, route, ctx)
    # canvas-only bits
    body = body.replace(' class="zh', ' id="top" class="zh', 1)
    desc = ctx["desc"].get(route, SITE["description"])
    swap_js = f"<script>window.ZH_SWAP={json.dumps(swaps)};</script>" if swaps else ""
    page = f"""<!doctype html>
<html lang="en" data-theme="dark" data-built="{int(BUILT.timestamp())}">
<head>
{head(title, route, desc, SITE["share_image"])}
<style>{FONT_CSS}{css}{REAL_CSS}{theme_css(css_t)}</style>
{person_ld() if route == "/" else ""}
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
{body}
<template id="zh-on">{status_html[0]}</template><template id="zh-off">{status_html[1]}</template>
{swap_js}<script src="/assets/site.js" defer></script>
</body>
</html>
"""
    # first <main> gets the skip-link target
    page = re.sub(r"<main\b(?![^>]*\bid=)", '<main id="main"', page, count=1)
    if 'id="main"' not in page:
        page = page.replace('href="#main"', 'href="#top"')
    return page, missing


def shrink_photos(folder, longest=2400):
    """Photos added straight from a phone or camera: make them web size and drop their EXIF data in dist/ (media/ keeps the original)."""
    from PIL import Image, ImageOps
    for a, _, fs in os.walk(folder):
        for f in fs:
            if not f.lower().endswith((".jpg", ".jpeg", ".png")):
                continue
            p = os.path.join(a, f)
            with Image.open(p) as im:
                if max(im.size) <= longest and os.path.getsize(p) < 900_000 and not len(im.getexif()):
                    continue
                im = ImageOps.exif_transpose(im)
                im.thumbnail((longest, longest))
                if f.lower().endswith(".png"):
                    im.save(p, optimize=True)
                else:
                    im.convert("RGB").save(p, quality=84, optimize=True, progressive=True)
            print("  made web size:", os.path.relpath(p, DIST))


# ------------------------------------------------------------------ loading speed
VIEWER_CLASSES = {"sss", "elb", "vpv", "ssg", "vpvs"}   # full-screen viewers: their pictures stay full size
THUMB_W = 800


class _ImgSpots(__import__("html.parser").parser.HTMLParser):
    """Character offsets of every <img> and <video> tag, and whether it sits inside a full-screen viewer."""
    VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "source", "track", "wbr"}

    def __init__(self, text):
        super().__init__(convert_charrefs=False)
        self.lines = [0]
        for ln in text.split("\n"):
            self.lines.append(self.lines[-1] + len(ln) + 1)
        self.stack, self.spots = [], []
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        cls = set((a.get("class") or "").split()) | ({"@zs"} if "data-zs" in a else set())
        if tag in ("img", "video"):
            line, col = self.getpos()
            inside = set().union(*self.stack, cls) if self.stack else cls
            # pieces whose attributes site.js swaps per theme (data-zs) are left exactly as built
            if "@zs" not in inside:
                self.spots.append((self.lines[line - 1] + col, tag, bool(inside & VIEWER_CLASSES)))
        if tag not in self.VOID:
            self.stack.append(cls)

    def handle_endtag(self, tag):
        if tag not in self.VOID and self.stack:
            self.stack.pop()


def thumb(src):
    """A THUMB_W-wide copy of a big picture in dist/media/_thumbs/ (made once per build). Returns its path or None."""
    from PIL import Image
    if not re.match(r"^/media/[^?#]+\.(webp|jpe?g|png)$", src, re.I):
        return None, 0
    full = os.path.join(DIST, src.lstrip("/"))
    if not os.path.exists(full):
        return None, 0
    with Image.open(full) as im:
        w, h = im.size
        if w <= THUMB_W + 100:
            return None, w
        rel = os.path.splitext(src[len("/media/"):])[0] + ".webp"
        out = os.path.join(DIST, "media", "_thumbs", rel)
        if not os.path.exists(out):
            os.makedirs(os.path.dirname(out), exist_ok=True)
            im2 = im.convert("RGBA" if im.mode in ("RGBA", "LA", "P") else "RGB").resize((THUMB_W, round(h * THUMB_W / w)), Image.LANCZOS)
            im2.save(out, "WEBP", quality=82, method=5)
        return "/media/_thumbs/" + rel, w


def fast_loading(html):
    """Pictures load when they come near the screen, grids get a smaller copy, moving videos start when seen,
    and the hero's 3D sprite is fetched first."""
    spots = _ImgSpots(html).spots
    out, last = [], 0
    for pos, tag, in_viewer in spots:
        end = html.index(">", pos) + 1
        t = html[pos:end]
        if tag == "img":
            add = ""
            if "loading=" not in t:
                add += ' loading="lazy"'
            if "decoding=" not in t:
                add += ' decoding="async"'
            m = re.search(r'\ssrc="([^"]+)"', t)
            if m and not in_viewer and "srcset=" not in t:
                small, w = thumb(m.group(1))
                if small:
                    add += f' srcset="{small} {THUMB_W}w, {m.group(1)} {w}w" sizes="(max-width: 760px) 100vw, 50vw"'
            t = t[:-1].rstrip("/") + add + ">"
        elif tag == "video" and " autoplay" in t:
            # a moving preview starts only when it is on screen (site.js), so it does not slow the page down
            t = t.replace(" autoplay", " data-autoplay").replace(' preload="metadata"', "")
            t = t[:-1] + ' preload="none">'
        elif tag == "video" and 'preload="metadata"' in t:
            t = t.replace('preload="metadata"', 'preload="none"')
        out.append(html[last:pos] + t)
        last = end
    html = "".join(out) + html[last:]
    m = re.search(r"url\((/media/[^)]*turntable[^)]*\.webp)\)", html)
    if m:
        html = html.replace("</head>", f'<link rel="preload" as="image" href="{m.group(1)}" fetchpriority="high">\n</head>', 1)
    return html


# GitHub Pages is very slow from Bangladesh (about 20 KB/s on 21 Nov 2026), while jsDelivr answers from Dhaka
# (about 500 KB/s). So on GitHub Actions the pictures, clips, fonts and site.js are served by jsDelivr straight from
# this repository at the commit being published; the pages themselves stay on github.io. Download links (<a href>)
# stay on github.io so the file keeps its name. A local build keeps every path local.
SHA = os.environ.get("GITHUB_SHA", "")
CDN = f"https://cdn.jsdelivr.net/gh/{os.environ.get('GITHUB_REPOSITORY', 'md-zaid-hossain/md-zaid-hossain.github.io')}@{SHA}" if SHA else ""
CDN_MAX = 20_000_000    # jsDelivr serves files up to 20 MB


def via_cdn(html):
    if not CDN:
        return html

    def same_in_repo(rel):
        a, b = os.path.join(REPO, rel), os.path.join(DIST, rel)
        return os.path.exists(a) and os.path.exists(b) and os.path.getsize(a) == os.path.getsize(b) and os.path.getsize(a) < CDN_MAX

    def swap(m):
        path = m.group(0)
        if path.startswith("/media/") and same_in_repo(path.lstrip("/")):
            return CDN + path
        if path.startswith("/assets/") and os.path.exists(os.path.join(BUILD, path.lstrip("/"))):
            return CDN + "/build" + path
        return path
    pat = re.compile(r"(?<=[\"'(\s,])/(?:media|assets)/[\w./%-]+\.(?:webp|jpe?g|png|gif|svg|mp4|webm|woff2|js)\b")
    # keep <a href> download links on github.io: cut them out, swap the rest, put them back
    links = []

    def keep(m):
        links.append(m.group(0))
        return f"\x00{len(links) - 1}\x00"
    html = re.sub(r"<a\b[^>]*>", keep, html)
    html = pat.sub(swap, html)
    html = re.sub(r"\x00(\d+)\x00", lambda m: links[int(m.group(1))], html)
    return html.replace("<head>", f'<head>\n<link rel="preconnect" href="https://cdn.jsdelivr.net" crossorigin>', 1)


# ------------------------------------------------------------------ 4. whole site
def main():
    t0 = _dt.datetime.now()
    shutil.rmtree(DIST, ignore_errors=True)
    os.makedirs(DIST)
    pages, clock = render_all()
    import project_pages as PP, site_parts as SP
    projs = C.load_projects()[0]
    by_no = {p["no"]: f"/projects/{p['slug']}/" for p in projs}
    by_no[3] = "/projects/ev-charging-station/"
    desc = {f"/projects/{p['slug']}/": re.sub(r"<[^>]+>", "", p["lead"])[:155].rsplit(" ", 1)[0] + "…" for p in projs}
    status = (f'{SP.gear_icon()}<span><b>Working hours</b> · replies today</span>',
              '<span>○</span><span><b>Off hours</b> · replies after Fajr</span>')
    report, done = [], {}
    for route, (title, variants) in pages.items():
        model = None
        for p in projs:
            if route == f"/projects/{p['slug']}/" and p.get("glb"):
                d = C.read(f"projects/{p['slug']}.yml")
                model = d.get("hero", {}).get("model")
                model = "/" + model.lstrip("/") if model else None
        ctx = dict(by_no=by_no, model=model, desc=desc)
        html, missing = finish(route, title, variants, ctx, status)
        if missing:
            report.append((route, sorted(set(missing))))
        done[route] = html
    # static files
    shutil.copytree(os.path.join(REPO, "media"), os.path.join(DIST, "media"), ignore=shutil.ignore_patterns("blob_to_media.json"))
    shutil.copytree(os.path.join(BUILD, "assets"), os.path.join(DIST, "assets"))
    shutil.copy2(os.path.join(BUILD, "assets", "favicon.svg"), os.path.join(DIST, "favicon.svg"))
    open(os.path.join(DIST, ".nojekyll"), "w").close()
    shrink_photos(os.path.join(DIST, "media"))
    for route, html in done.items():
        dst = os.path.join(DIST, route.lstrip("/"), "index.html") if route.endswith("/") else os.path.join(DIST, route.lstrip("/"))
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        open(dst, "w", encoding="utf-8").write(via_cdn(fast_loading(html)))
    new_thumbs = [os.path.relpath(os.path.join(a, f), os.path.join(DIST, "media")) for a, _, fs in os.walk(os.path.join(DIST, "media", "_thumbs")) for f in fs
                  if not os.path.exists(os.path.join(REPO, "media", os.path.relpath(os.path.join(a, f), os.path.join(DIST, "media"))))]
    if new_thumbs:
        print(f"  {len(new_thumbs)} small copies are not in media/_thumbs yet (run: python3 build/build.py --keep-thumbs, then commit)")
        if "--keep-thumbs" in sys.argv:
            for r in new_thumbs:
                os.makedirs(os.path.dirname(os.path.join(REPO, "media", r)), exist_ok=True)
                shutil.copy2(os.path.join(DIST, "media", r), os.path.join(REPO, "media", r))
    routes = [r for r in pages if r != "/404.html"]
    day = BUILT.date().isoformat()
    open(os.path.join(DIST, "sitemap.xml"), "w").write(
        '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "".join(f"  <url><loc>{URL}{r}</loc><lastmod>{day}</lastmod></url>\n" for r in routes) + "</urlset>\n")
    open(os.path.join(DIST, "robots.txt"), "w").write(f"User-agent: *\nAllow: /\nSitemap: {URL}/sitemap.xml\n")
    for route, miss in report:
        print("  links still '#' on", route, ":", "; ".join(miss))
    size = sum(os.path.getsize(os.path.join(a, f)) for a, _, fs in os.walk(DIST) for f in fs)
    print(f"built {len(pages)} pages into dist/ ({size / 1e6:.0f} MB) in {(_dt.datetime.now() - t0).seconds} s")


if __name__ == "__main__":
    main()
    if "--serve" in sys.argv:
        os.chdir(DIST)
        subprocess.run([sys.executable, "-m", "http.server", "8000"])
