"""Video panels for every video on the site (Zaid, 2026-11-20): the inline clip keeps playing silently; pointing at it
shows a play button and a hint; clicking opens a full-screen player with a seek bar (click anywhere on the timeline
to jump), pause, speed and the browser's own full-screen button. Same feel as the photo slideshow.
Mockup: CSS only (checkbox per video, viewer written before </body> by inject(), called from type_scale.apply).
Real site: the same markup plus a few lines of JS (Esc to close, pause the clip when the player closes).
Class prefix: vp."""
import re

VIEWERS = []

PLAY = ('<svg viewBox="0 0 24 24" width="22" height="22" aria-hidden="true"><path d="M8 5.5v13l11-6.5z" fill="currentColor"/></svg>')
EXPAND = ('<svg viewBox="0 0 24 24" width="13" height="13" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true">'
          '<path d="M4 9V4h5M20 9V4h-5M4 15v5h5M20 15v5h-5"/></svg>')

CSS = """
/* ===== video panels and player (prefix vp) ===== */
.vpw{position:relative;display:block;width:100%;height:100%;cursor:pointer;overflow:hidden}
.vpw video{transition:transform .6s cubic-bezier(.2,.7,.2,1),filter .4s ease}
.vpw:hover video{transform:scale(1.025);filter:brightness(.78)}
.vpo{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:12px;opacity:0;transition:opacity .3s ease;pointer-events:none;
  background:radial-gradient(circle at center,rgba(8,10,14,.35),rgba(8,10,14,0) 60%)}
.vpw:hover .vpo,.vpw:focus-visible .vpo{opacity:1}
.eths .evd>.vpw{height:auto}   /* thesis panel: the video sits centred in a taller dark panel, so the panel is only as tall as the video */
.vpo i{position:relative;display:flex;align-items:center;justify-content:center;width:62px;height:62px;border-radius:50%;background:var(--acc);color:#fff;
  box-shadow:0 10px 30px rgba(0,0,0,.35);transform:scale(.86);transition:transform .35s cubic-bezier(.3,1.4,.5,1)}
.vpo i svg{margin-left:3px}
.vpo i:after{content:"";position:absolute;inset:-7px;border-radius:50%;border:2px solid var(--acc);opacity:0}
.vpw:hover .vpo i{transform:scale(1)}
.vpw:hover .vpo i:after{animation:vpring 1.6s ease-out infinite}
@keyframes vpring{from{transform:scale(.9);opacity:.8}to{transform:scale(1.5);opacity:0}}
.vpo b{position:absolute;top:calc(50% + 42px);display:flex;align-items:center;gap:7px;font:600 10.5px 'IBM Plex Mono',monospace;letter-spacing:.12em;color:#fff;background:rgba(10,12,16,.72);padding:5px 9px;border-radius:5px}
.vpc{position:fixed;top:0;left:0;width:1px;height:1px;opacity:0;pointer-events:none;margin:0}
.vpv{display:none;position:fixed;inset:0;z-index:400;align-items:center;justify-content:center;padding:56px 40px 40px}
.vpc:checked+.vpv{display:flex}
.vpv>.vpb{position:absolute;inset:0;background:rgba(8,10,14,.92);cursor:zoom-out}
.vpv figure{position:relative;z-index:1;margin:0;display:flex;flex-direction:column;align-items:center;gap:12px;max-width:min(1280px,100%)}
.vpv video{display:block;max-width:min(1280px,calc(100vw - 80px));max-height:calc(100vh - 170px);border-radius:6px;background:#000;box-shadow:0 20px 60px rgba(0,0,0,.5)}
.vpv figcaption{font-family:Inter,system-ui,sans-serif;max-width:min(900px,calc(100vw - 80px));text-align:center;font-size:15px;line-height:1.5;color:#E7E9EE}
.vpv figcaption b{display:block;font:600 10.5px 'IBM Plex Mono',monospace;letter-spacing:.14em;color:#A9B0BC;margin-bottom:3px}
.vpv .vpx{position:absolute;top:16px;right:22px;z-index:2;font:600 11px 'IBM Plex Mono',monospace;letter-spacing:.12em;color:#E7E9EE;cursor:pointer;padding:6px 8px}
.vpv .vph{position:absolute;top:20px;left:24px;z-index:2;font:600 10.5px 'IBM Plex Mono',monospace;letter-spacing:.12em;color:#A9B0BC}
@media (max-width:760px){.vpo b{top:calc(50% + 36px)}.vpv{padding:52px 10px 24px}.vpv video{max-width:calc(100vw - 20px);max-height:calc(100vh - 200px)}.vpv .vph{display:none}.vpo i{width:52px;height:52px}}
"""


def panel(vid, video_html, src, poster, cap, tag="VIDEO"):
    """Wrap an inline <video> in a clickable panel and register its full-screen player."""
    rid = f"vp-{vid}"
    VIEWERS.append(
        f'<input type="checkbox" class="vpc" id="{rid}" tabindex="-1" aria-hidden="true">'
        f'<div class="vpv" role="dialog" aria-label="{cap}"><label class="vpb" for="{rid}" aria-hidden="true"></label>'
        f'<span class="vph">{tag} · CLICK THE TIMELINE TO JUMP</span><label class="vpx" for="{rid}">CLOSE ×</label>'
        f'<figure><video src="{src}" poster="{poster}" controls preload="metadata" playsinline muted loop></video>'
        f'<figcaption><b>{tag}</b>{cap}</figcaption></figure></div>')
    return (f'<label class="vpw" for="{rid}" title="Open the player">{video_html}'
            f'<span class="vpo" aria-hidden="true"><i>{PLAY}</i><b>{EXPAND}PLAY · SEEK · FULL SCREEN</b></span></label>')


def inject(html):
    """Put the collected players before </body> (above the sticky header) and the CSS into the page; then reset."""
    if not VIEWERS:
        return html
    v = "".join(VIEWERS)
    VIEWERS.clear()
    html = html.replace("</style>", CSS + "</style>", 1)
    i = html.rindex("</body>")
    return html[:i] + f'<div class="vpvs">{v}</div>' + html[i:]
