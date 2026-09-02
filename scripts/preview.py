"""Build self-contained, single-file preview pages from _site for sharing.

Inlines CSS and the logo (data URI) and rewrites internal links so the pages
work as standalone files opened directly (no server). Output -> preview/.
"""
import os, re, base64, glob

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SITE = os.path.join(ROOT, "_site")
OUT = os.path.join(ROOT, "preview")
os.makedirs(OUT, exist_ok=True)

css = open(os.path.join(SITE, "assets", "styles.css"), encoding="utf-8").read()

def data_uri(path):
    b = open(path, "rb").read()
    return "data:image/png;base64," + base64.b64encode(b).decode()

logo_uri = data_uri(os.path.join(SITE, "assets", "logo.png"))
fav_uri = data_uri(os.path.join(SITE, "assets", "favicon.png"))

dates = sorted([os.path.basename(os.path.dirname(p)) for p in glob.glob(os.path.join(SITE, "editions", "*", "index.html"))], reverse=True)

def transform(htmlstr):
    # inline stylesheet
    htmlstr = re.sub(r'<link rel="stylesheet" href="[^"]*assets/styles\.css">',
                     f"<style>{css}</style>", htmlstr)
    # logo + favicons -> data URIs
    htmlstr = re.sub(r'(src|href)="[^"]*assets/logo\.png"', rf'\1="{logo_uri}"', htmlstr)
    htmlstr = re.sub(r'href="[^"]*assets/favicon\.png"', f'href="{fav_uri}"', htmlstr)
    htmlstr = re.sub(r'href="[^"]*assets/favicon-\d+\.png"', f'href="{fav_uri}"', htmlstr)
    # home links
    htmlstr = re.sub(r'href="(\.\./\.\./)?index\.html"', 'href="preview_home.html"', htmlstr)
    # edition links -> flat preview files
    htmlstr = re.sub(r'href="(\.\./\.\./)?editions/(\d{4}-\d{2}-\d{2})/"', r'href="preview_\2.html"', htmlstr)
    # feed / sitemap -> disabled in preview
    htmlstr = re.sub(r'href="[^"]*feed\.xml"', 'href="#"', htmlstr)
    return htmlstr

# home
home = open(os.path.join(SITE, "index.html"), encoding="utf-8").read()
open(os.path.join(OUT, "preview_home.html"), "w", encoding="utf-8").write(transform(home))
# editions
for d in dates:
    h = open(os.path.join(SITE, "editions", d, "index.html"), encoding="utf-8").read()
    open(os.path.join(OUT, f"preview_{d}.html"), "w", encoding="utf-8").write(transform(h))

print("preview files:", ", ".join(sorted(os.listdir(OUT))))
