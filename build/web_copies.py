"""Smaller copies of the pictures, kept in the repository so jsDelivr can serve them:
  media/_thumbs/<path>.webp        800 px wide copy of every picture wider than 900 px (grids use it)
  media/_thumbs/<path>-frame0.webp first frame of each 3D turntable sprite (shown at once while the sprite loads)
  media/_avif/<path>.avif          AVIF copy of every picture and thumb (about half the size of WebP)
GitHub Actions runs this before every build and commits the new copies, so pictures added later
(Pages CMS, GitHub Desktop or Claude) get them too. Run by hand:  python3 build/web_copies.py"""
import gc
import os
import sys

from PIL import Image

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MEDIA = os.path.join(REPO, "media")
RASTER = (".webp", ".jpg", ".jpeg", ".png")
THUMB_W = 800
AVIF_Q = 55          # checked by eye on 21 Nov 2026: same look as the WebP at about half the size


def rel_files(sub=""):
    root = os.path.join(MEDIA, sub)
    for a, dirs, fs in os.walk(root):
        dirs[:] = [d for d in dirs if not (sub == "" and a == MEDIA and d in ("_avif", "_thumbs"))]
        for f in fs:
            if f.lower().endswith(RASTER):
                yield os.path.relpath(os.path.join(a, f), MEDIA).replace(os.sep, "/")


def thumb_rel(rel):
    return "_thumbs/" + os.path.splitext(rel)[0] + ".webp"


def frame0_rel(rel):
    return "_thumbs/" + os.path.splitext(rel)[0] + "-frame0.webp"


def avif_rel(rel):
    return "_avif/" + os.path.splitext(rel)[0] + ".avif"


def _rgb(im):
    return im.convert("RGBA" if im.mode in ("RGBA", "LA", "P") else "RGB")


def make_all(verbose=True):
    made = 0
    for rel in list(rel_files()):
        src = os.path.join(MEDIA, rel)
        with Image.open(src) as im:
            w, h = im.size
            if w > THUMB_W + 100:
                out = os.path.join(MEDIA, thumb_rel(rel))
                if not os.path.exists(out):
                    os.makedirs(os.path.dirname(out), exist_ok=True)
                    _rgb(im).resize((THUMB_W, round(h * THUMB_W / w)), Image.LANCZOS).save(out, "WEBP", quality=82, method=5)
                    made += 1
            if os.path.basename(rel).startswith("turntable") or rel.endswith("-turntable.webp"):
                out = os.path.join(MEDIA, frame0_rel(rel))
                if not os.path.exists(out):     # sprite is 9 x 8 frames; frame 0 is the top-left one
                    os.makedirs(os.path.dirname(out), exist_ok=True)
                    # cut the frame first, then convert: only 600 x 480 px in memory, not the whole 5400 x 3840 sprite
                    # (run #9 on 21 Nov stopped here with "can't allocate picture frame"); one retry after freeing memory
                    for attempt in (1, 2):
                        try:
                            _rgb(im.crop((0, 0, w // 9, h // 8))).save(out, "WEBP", quality=85, method=5)
                            break
                        except MemoryError:
                            if attempt == 2:
                                raise
                            gc.collect()
                    made += 1
    for rel in list(rel_files()) + [r for r in rel_files("_thumbs") if not r.endswith("-frame0.webp")]:
        out = os.path.join(MEDIA, avif_rel(rel))
        if os.path.exists(out):
            continue
        os.makedirs(os.path.dirname(out), exist_ok=True)
        with Image.open(os.path.join(MEDIA, rel)) as im:
            _rgb(im).save(out, "AVIF", quality=AVIF_Q, speed=6)
        made += 1
        if verbose:
            print("  avif:", rel)
    return made


if __name__ == "__main__":
    n = make_all("-q" not in sys.argv)
    print(n, "new copies")
