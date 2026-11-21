"""Photo slideshow for any group of photos (Gallery albums, Experience galleries). CSS only, no JS (canvas rule).

How it works
- Each group gets one set of radio buttons (one per photo + a hidden "closed" radio that is checked at first).
  The radios sit fixed at the top-left corner, invisible, so focusing one never scrolls the page.
- A thumbnail is a <label for=radio i>. Clicking it checks radio i (that slide shows) and focuses it.
- Because the focused element is a radio of the group, the keyboard arrows (left/right/up/down) move to the
  previous/next photo natively. Moving past the last photo (or before the first) lands on the "closed" radio,
  which closes the viewer.
- Each slide has PREV / NEXT arrow labels (wrapping round), a CLOSE label, a click-outside backdrop to close,
  a "03 / 10" counter and the caption. Clicking the photo itself goes to the next one.
On the real site (coding stage) the same markup gets a few lines of JS for Esc and swipe.
Class prefix: ss."""

MAX = 30

CSS = """
/* ===== slideshow (prefix ss) ===== */
.ssr{position:fixed;top:0;left:0;width:1px;height:1px;opacity:0;pointer-events:none;margin:0}
.sss{display:none;position:fixed;inset:0;z-index:400;align-items:center;justify-content:center;padding:56px 84px 40px}
.sss>.ssb{position:absolute;inset:0;background:rgba(8,10,14,.9);cursor:zoom-out}
.sss figure{position:relative;margin:0;display:flex;flex-direction:column;align-items:center;gap:12px;max-width:min(1200px,100%);z-index:1}
.sss figure label{cursor:pointer;display:block}
.sss img{display:block;max-width:min(1200px,calc(100vw - 168px));max-height:calc(100vh - 170px);border-radius:4px;box-shadow:0 20px 60px rgba(0,0,0,.5);background:#111}
.sss figcaption{font-family:Inter,system-ui,sans-serif;max-width:min(900px,calc(100vw - 168px));text-align:center;font-size:15px;line-height:1.5;color:#E7E9EE}
.sss figcaption b{display:block;font:600 10.5px 'IBM Plex Mono',monospace;letter-spacing:.14em;color:#A9B0BC;margin-bottom:3px}
.ssa{position:absolute;top:50%;transform:translateY(-50%);z-index:2;width:48px;height:48px;border-radius:50%;border:1px solid rgba(231,233,238,.35);
  display:flex;align-items:center;justify-content:center;color:#E7E9EE;font:500 20px 'IBM Plex Mono',monospace;cursor:pointer;background:rgba(20,23,30,.55);transition:background .25s ease,border-color .25s ease}
.ssa:hover{background:rgba(231,233,238,.14);border-color:#E7E9EE}
.ssp{left:20px}.ssn{right:20px}
.ssx{position:absolute;top:16px;right:22px;z-index:2;font:600 11px 'IBM Plex Mono',monospace;letter-spacing:.12em;color:#E7E9EE;cursor:pointer;padding:6px 8px}
.ssk{position:absolute;top:20px;left:24px;z-index:2;font:600 10.5px 'IBM Plex Mono',monospace;letter-spacing:.12em;color:#A9B0BC}
@media (max-width:760px){
  .sss{padding:52px 10px 24px}
  .sss img{max-width:calc(100vw - 20px);max-height:calc(100vh - 210px)}
  .sss figcaption{max-width:calc(100vw - 24px);font-size:14px}
  .ssa{top:auto;bottom:22px;transform:none;width:44px;height:44px}
  .ssp{left:calc(50% - 56px)}.ssn{right:calc(50% - 56px)}
  .sss figure{margin-bottom:62px}
  .ssk{display:none}
}
""" + "".join(f".ssg>input:nth-of-type({k}):checked~.sss:nth-of-type({k}){{display:flex}}" for k in range(1, MAX + 1)) + "\n"


def group(gid, items, tag=""):
    """items: [(src, caption)]. Returns (labels_for, html):
    labels_for(i) -> the radio id a thumbnail label must point at; html -> radios + slides (put it once per group)."""
    n = len(items)
    assert n <= MAX
    rid = lambda i: f"ss-{gid}-{i}"
    radios = "".join(f'<input type="radio" class="ssr" name="ss-{gid}" id="{rid(i)}" tabindex="-1">' for i in range(n))
    radios += f'<input type="radio" class="ssr" name="ss-{gid}" id="{rid("x")}" checked tabindex="-1">'
    slides = ""
    for i, (src, cap) in enumerate(items):
        prev, nxt = rid((i - 1) % n), rid((i + 1) % n)
        count = f"{tag + ' · ' if tag else ''}{i + 1:02d} / {n:02d}"
        slides += (f'<div class="sss" role="dialog" aria-label="{cap}"><label class="ssb" for="{rid("x")}" aria-hidden="true"></label>'
                   f'<span class="ssk">{count}</span><label class="ssx" for="{rid("x")}">CLOSE ×</label>'
                   + (f'<label class="ssa ssp" for="{prev}" aria-label="Previous photo">←</label><label class="ssa ssn" for="{nxt}" aria-label="Next photo">→</label>' if n > 1 else "")
                   + f'<figure><label for="{nxt if n > 1 else rid("x")}"><img src="{src}" alt="{cap}"></label>'
                   f'<figcaption><b>{count}</b>{cap}</figcaption></figure></div>')
    return rid, f'<div class="ssg">{radios}{slides}</div>'


_LBX = None


def from_lightboxes(html, groups):
    """Turn single-photo lightboxes (input.elbc + label.elb, used on Education, Awards and Research) into slideshows.
    groups: [(gid, tag, [lightbox ids in order])]. Groups with one photo stay as they are.
    The thumbnails keep their markup; only their for="..." moves to the slideshow radios."""
    import re
    global _LBX
    _LBX = _LBX or re.compile(r'<input type="checkbox" class="elbc" id="([^"]+)"><label class="elb" for="\1">'
                              r'<img src="([^"]+)" alt="([^"]*)"><span>CLOSE ×</span></label>')
    boxes = {m.group(1): (m.group(0), m.group(2), m.group(3)) for m in _LBX.finditer(html)}
    viewers = ""
    for gid, tag, lids in groups:
        lids = [l for l in lids if l in boxes]
        if len(lids) < 2:
            continue
        rid, viewer = group(gid, [(boxes[l][1], boxes[l][2]) for l in lids], tag)
        for i, l in enumerate(lids):
            html = html.replace(boxes[l][0], "", 1)
            html = html.replace(f'for="{l}"', f'for="{rid(i)}"')
        viewers += viewer
    if viewers:      # viewers go before </body>, outside <main>, so they sit above the sticky header
        if ".ssr{" not in html:
            html = html.replace("</style>", CSS + "</style>", 1)
        i = html.rindex("</body>")
        html = html[:i] + viewers + html[i:]
    return html
