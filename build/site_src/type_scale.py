"""Site-wide type scale (2026-11-20).

Zaid asked for font sizes that are easy to read and calm: not too small, not too big, in a steady ratio,
following what most websites use. Common guidance (Smashing Magazine, Penn State accessibility, USWDS-style
design systems): body text about 16 px with line height near 1.5, nothing below 12 px, and headings on a
1.2-1.25 step scale. Measured before this change: body text mostly 13-14.5 px, mono labels 8.5-10 px.

apply(html) rewrites every font size in the page's CSS (style blocks and style attributes) through one
mapping, and writes the result in rem so the browser's own text-size setting still works.
Result on PC: labels 12-13 px, small text 14-15 px, body 15.5-16 px, card titles 17-19 px, headings as before
plus a little. Phone values move up the same way (phone body about 15.5 px).
SVG drawings are not touched: their text scales with the drawing."""
import re

# old px -> new px anchor points; values in between are interpolated, then rounded to 0.5 px
ANCHORS = [(8, 10), (9, 11), (10, 12), (10.5, 12), (11, 12.5), (12, 13.5), (12.5, 14), (13, 14.5),
           (13.5, 15), (14, 15.5), (14.5, 16), (16, 17), (17, 18.5), (19, 20.5), (22, 23), (26, 27),
           (32, 34), (48, 50), (64, 66)]


def new_px(v):
    if v <= ANCHORS[0][0]:
        return ANCHORS[0][1]
    for (a, x), (b, y) in zip(ANCHORS, ANCHORS[1:]):
        if a <= v <= b:
            r = x + (y - x) * (v - a) / (b - a)
            return round(r * 2) / 2
    return v + 2


def _rem(px):
    return f"{new_px(px) / 16:.4f}".rstrip("0").rstrip(".") + "rem"


_FS = re.compile(r"(font-size\s*:\s*)(\d+(?:\.\d+)?)px")
_FONT = re.compile(r"(\bfont\s*:\s*[^;{}\"']*?)(\d+(?:\.\d+)?)px")


def _css(s):
    s = _FS.sub(lambda m: m.group(1) + _rem(float(m.group(2))), s)
    return _FONT.sub(lambda m: m.group(1) + _rem(float(m.group(2))), s)


# selectors kept at their tuned sizes: the footer line (must stay on one row), the education Gantt
# (fixed row heights), the small stat captions under the term-project numbers and the index sub-items
KEEP = (".ftr", "footer", ".qg", ".etm span", ".ixs")

# small fixes after scaling (narrow phones)
EXTRA = """
@media (max-width:420px){.est>div{padding:12px 12px}.est span{font-size:.75rem}}
"""


def _rules(css):
    def one(m):
        sel, body = m.group(1), m.group(2)
        if any(k in sel for k in KEEP):
            return sel + body
        return sel + _css(body)
    return re.sub(r"([^{}]+)(\{[^{}]*\})", one, css)


def apply(html):
    # never touch SVG content: cut SVGs out, rescale the rest, put them back
    svgs = []

    def keep(m):
        svgs.append(m.group(0))
        return f"\x00SVG{len(svgs) - 1}\x00"
    h = re.sub(r"<svg\b.*?</svg>", keep, html, flags=re.S)
    h = re.sub(r"(<style[^>]*>)(.*?)(</style>)", lambda m: m.group(1) + _rules(m.group(2)) + m.group(3), h, flags=re.S)
    h = h.replace("</style>", EXTRA + "</style>", 1)
    h = re.sub(r'(style=")([^"]*)(")', lambda m: m.group(1) + _css(m.group(2)) + m.group(3), h)
    h = re.sub(r"\x00SVG(\d+)\x00", lambda m: svgs[int(m.group(1))], h)
    import site_extras as SX        # mark the current page in the phone menu too
    import videoplayer as VP        # full-screen players for the video panels on this page
    return VP.inject(SX.mark_current(h))
