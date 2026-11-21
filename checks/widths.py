"""Layout check on the built site with Playwright (Chromium): every page at phone, tablet and desktop widths
in a dark and a light theme. Fails on horizontal scrolling and on page errors.
  python3 checks/widths.py dist"""
import functools, glob, http.server, os, re, sys, threading
from playwright.sync_api import sync_playwright

DIST = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else "dist")
WIDTHS = [320, 360, 390, 768, 1024, 1280, 1440, 1920]
class Quiet(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a):
        pass

    def handle(self):
        try:
            super().handle()
        except (ConnectionResetError, BrokenPipeError):
            pass


srv = http.server.ThreadingHTTPServer(("127.0.0.1", 0), functools.partial(Quiet, directory=DIST))
threading.Thread(target=srv.serve_forever, daemon=True).start()
base = f"http://127.0.0.1:{srv.server_address[1]}"
pages = sorted("/" + os.path.relpath(f, DIST).replace("index.html", "") for f in glob.glob(os.path.join(DIST, "**", "*.html"), recursive=True) if "/_t/" not in f)
bad = 0
with sync_playwright() as pw:
    b = pw.chromium.launch()
    for mode in ("dark", "light"):
        ctx = b.new_context(viewport={"width": 1440, "height": 900})
        # files the pages load from the CDN branches are answered from dist/ (same files), so the check does not
        # depend on the CDN having fetched a brand-new commit yet
        ctx.route(re.compile(r"https://cdn\.jsdelivr\.net/gh/[^@]+@[0-9a-f]+/(.*)"),
                  lambda route: route.fulfill(path=os.path.join(DIST, re.match(r"https://cdn\.jsdelivr\.net/gh/[^@]+@[0-9a-f]+/([^?#]*)", route.request.url).group(1)))
                  if os.path.exists(os.path.join(DIST, re.match(r"https://cdn\.jsdelivr\.net/gh/[^@]+@[0-9a-f]+/([^?#]*)", route.request.url).group(1))) else route.abort())
        ctx.add_init_script(f"try{{localStorage.setItem('zh-mode','{mode}')}}catch(e){{}}")
        page = ctx.new_page()
        errors = []
        page.on("pageerror", lambda e: errors.append(str(e)))
        for w in WIDTHS:
            page.set_viewport_size({"width": w, "height": 900})
            for u in pages:
                page.goto(base + u, wait_until="load")
                sw = page.evaluate("document.documentElement.scrollWidth")
                if sw > w:
                    bad += 1; print(f"{mode} {w}px {u}: page is {sw}px wide (horizontal scroll)")
        for e in sorted(set(errors)):
            bad += 1; print(f"{mode}: script error: {e}")
        ctx.close()
    b.close()
print(bad, "problems")
sys.exit(1 if bad else 0)
