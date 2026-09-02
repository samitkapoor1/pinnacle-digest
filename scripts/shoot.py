import os, threading, functools, http.server, socketserver
from playwright.sync_api import sync_playwright

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SITE = os.path.join(ROOT, "_site")
SHOTS = os.path.join(ROOT, "shots")
os.makedirs(SHOTS, exist_ok=True)
PORT = 8138

Handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=SITE)
httpd = socketserver.TCPServer(("127.0.0.1", PORT), Handler)
threading.Thread(target=httpd.serve_forever, daemon=True).start()
base = f"http://127.0.0.1:{PORT}"

def shoot(page, url, path, theme=None, full=True):
    page.goto(url, wait_until="networkidle")
    if theme:
        page.evaluate(f"document.documentElement.setAttribute('data-theme','{theme}')")
    page.wait_for_timeout(500)
    page.screenshot(path=os.path.join(SHOTS, path), full_page=full)
    print("shot", path)

with sync_playwright() as p:
    b = p.chromium.launch()
    ctx = b.new_context(viewport={"width": 1200, "height": 900}, device_scale_factor=2)
    pg = ctx.new_page()
    shoot(pg, base + "/", "home-light.png")
    shoot(pg, base + "/", "home-dark.png", theme="dark")
    shoot(pg, base + "/editions/2026-09-02/", "edition-dark.png", theme="dark")
    ctx.close()
    ctx = b.new_context(viewport={"width": 390, "height": 844}, device_scale_factor=2)
    pg = ctx.new_page()
    shoot(pg, base + "/", "home-mobile.png", full=False)
    ctx.close()
    b.close()
httpd.shutdown()
print("done")
