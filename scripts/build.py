#!/usr/bin/env python3
"""
Pinnacle Digest static site generator.

Reads every content/YYYY-MM-DD.json edition and renders a static site into
_site/ : a dated homepage/archive with category filtering, one page per daily
edition (contents + categorised stories + charts), an RSS feed, and the
supporting files GitHub Pages needs (CNAME, .nojekyll, 404).

Usage:  python3 scripts/build.py
"""

import json
import os
import re
import glob
import shutil
import html
from datetime import datetime

from charts import render_chart, esc

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
CONTENT_DIR = os.path.join(ROOT, "content")
ASSETS_DIR = os.path.join(ROOT, "assets")
OUT = os.path.join(ROOT, "_site")

SITE_NAME = "Pinnacle Digest"
SITE_KICKER = "the"

# Hosting URL is resolved at build time so the same code works on the generic
# GitHub Pages URL now and the custom domain later:
#   - PD_DOMAIN set  -> custom-domain mode (writes a CNAME file too)
#   - PD_SITE_URL set (e.g. from actions/configure-pages) -> use it as-is
#   - neither set    -> relative/unknown host (still works, just no absolute URLs)
CUSTOM_DOMAIN = os.environ.get("PD_DOMAIN", "").strip()
if CUSTOM_DOMAIN:
    SITE_URL = f"https://{CUSTOM_DOMAIN}"
else:
    SITE_URL = os.environ.get("PD_SITE_URL", "").strip().rstrip("/")


def canon(path):
    """Absolute URL for a path, or '' when the host is unknown (skips the tag)."""
    return f"{SITE_URL}{path}" if SITE_URL else ""
TAGLINE = "A daily briefing for UK & Ireland accountancy, tax and advisory firms."
COMPANY_URL = "https://www.pinnacleglobalgroup.com"
DISCLAIMER = "Compiled from published third-party reporting. Not professional advice."

TAG_COLORS = ["blue", "green", "red", "cyan", "sage"]

FONTS_LINK = (
    '<link rel="preconnect" href="https://fonts.googleapis.com">'
    '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
    '<link href="https://fonts.googleapis.com/css2?'
    'family=Newsreader:ital,opt@0,400;0,500;0,600;1,400&'
    'family=Poppins:wght@400;500;600;700&'
    'family=Caveat:wght@600;700&display=swap" rel="stylesheet">'
)
# (fix the accidental token above)
FONTS_LINK = (
    '<link rel="preconnect" href="https://fonts.googleapis.com">'
    '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
    '<link href="https://fonts.googleapis.com/css2?'
    'family=Newsreader:ital,wght@0,400;0,500;0,600;1,400&'
    'family=Poppins:wght@400;500;600;700&'
    'family=Caveat:wght@600;700&display=swap" rel="stylesheet">'
)

THEME_SCRIPT = """
<script>
(function(){
  try{
    var t = localStorage.getItem('pd-theme');
    if(t){ document.documentElement.setAttribute('data-theme', t); }
  }catch(e){}
  window.__toggleTheme = function(){
    var el = document.documentElement;
    var cur = el.getAttribute('data-theme');
    if(!cur){
      cur = window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
    }
    var next = cur === 'dark' ? 'light' : 'dark';
    el.setAttribute('data-theme', next);
    try{ localStorage.setItem('pd-theme', next); }catch(e){}
  };
})();
</script>
"""

FILTER_SCRIPT = """
<script>
(function(){
  var chips = document.querySelectorAll('.filter-chip');
  var cards = document.querySelectorAll('[data-cats]');
  chips.forEach(function(chip){
    chip.addEventListener('click', function(){
      chips.forEach(function(c){ c.classList.remove('active'); });
      chip.classList.add('active');
      var f = chip.getAttribute('data-filter');
      cards.forEach(function(card){
        var show = (f === '__all__') || card.getAttribute('data-cats').split('|').indexOf(f) !== -1;
        card.style.display = show ? '' : 'none';
      });
    });
  });
})();
</script>
"""


def slugify(text):
    s = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return s or "section"


def fmt_date(iso, weekday=True):
    d = datetime.strptime(iso, "%Y-%m-%d")
    day = d.day
    base = d.strftime("%B %Y")
    core = f"{day} {base}"
    return d.strftime("%A, ") + core if weekday else core


def rss_date(iso):
    d = datetime.strptime(iso, "%Y-%m-%d")
    return d.strftime("%a, %d %b %Y 06:00:00 +0000")


def load_editions():
    editions = []
    for path in glob.glob(os.path.join(CONTENT_DIR, "*.json")):
        with open(path, encoding="utf-8") as fh:
            editions.append(json.load(fh))
    editions.sort(key=lambda e: e["date"], reverse=True)
    return editions


# --------------------------------------------------------------------------- #
# Shared chrome
# --------------------------------------------------------------------------- #
def page_shell(title, description, body, root, canonical=""):
    canonical_tag = f'<link rel="canonical" href="{canonical}">' if canonical else ""
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(description)}">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(description)}">
<meta property="og:type" content="website">
<meta property="og:image" content="{SITE_URL}/assets/icon-512.png">
<meta name="theme-color" content="#003399">
{canonical_tag}
<link rel="icon" type="image/png" sizes="180x180" href="{root}assets/favicon.png">
<link rel="apple-touch-icon" href="{root}assets/favicon.png">
{FONTS_LINK}
<link rel="stylesheet" href="{root}assets/styles.css">
{THEME_SCRIPT}
</head>
<body>
{topbar(root)}
{body}
{site_footer(root)}
</body>
</html>"""


def topbar(root):
    return f"""<header class="topbar"><div class="topbar-inner">
  <a class="brand-lockup" href="{root}index.html">
    <img src="{root}assets/logo.png" alt="Pinnacle Global">
    <span class="brand-names"><span class="kicker">{SITE_KICKER}</span><span class="name">Pinnacle Digest</span></span>
  </a>
  <span class="spacer"></span>
  <a class="nav-link hide-sm" href="{root}index.html">Archive</a>
  <a class="nav-link hide-sm" href="{root}feed.xml">RSS</a>
  <button class="theme-toggle" onclick="window.__toggleTheme()" aria-label="Toggle dark mode">Theme</button>
</div></header>"""


def site_footer(root):
    year = datetime.now().year
    return f"""<footer class="site-foot"><div class="wrap">
  <span>&copy; {year} Pinnacle Global Group &middot; <a href="{COMPANY_URL}">pinnacleglobalgroup.com</a></span>
  <span class="disclaimer">{esc(DISCLAIMER)}</span>
</div></footer>"""


# --------------------------------------------------------------------------- #
# Story / category rendering
# --------------------------------------------------------------------------- #
def render_tags(tags):
    if not tags:
        return ""
    items = []
    for i, t in enumerate(tags):
        color = TAG_COLORS[i % len(TAG_COLORS)]
        items.append(f'<span class="tag tag--{color}">{esc(t)}</span>')
    return f'<div class="tags">{"".join(items)}</div>'


def render_story(story):
    parts = [f'<h3>{esc(story["headline"])}</h3>']
    parts.append(render_tags(story.get("tags")))
    for para in story.get("body", []):
        parts.append(f"<p>{esc(para)}</p>")
    for chart in story.get("charts", []):
        parts.append(render_chart(chart))
    if story.get("meaning"):
        parts.append(
            '<div class="callout"><span class="lead">What this means for firms.</span> '
            f'{esc(story["meaning"])}</div>'
        )
    if story.get("source"):
        parts.append(f'<p class="source">{esc(story["source"])}</p>')
    return f'<article class="story">{"".join(parts)}</article>'


def render_category(cat, index):
    slug = slugify(cat["name"])
    num = f"{index:02d}"
    badge = f'<span class="cat-badge">{esc(cat["badge"])}</span>' if cat.get("badge") else ""
    head = (
        f'<div class="cat-head"><span class="num">{num}</span>'
        f'<h2>{esc(cat["name"])}</h2>{badge}<span class="cat-rule"></span></div>'
    )
    stories = "".join(render_story(s) for s in cat.get("stories", []))
    return f'<section class="category" id="cat-{slug}">{head}{stories}</section>'


def render_contents(categories):
    items = []
    for i, cat in enumerate(categories, start=1):
        slug = slugify(cat["name"])
        n = len(cat.get("stories", []))
        label = "story" if n == 1 else "stories"
        items.append(
            f'<li><a class="num" href="#cat-{slug}">{i:02d}</a>'
            f'<a class="toc-cat" href="#cat-{slug}">{esc(cat["name"])}</a>'
            f'<span class="toc-count">{n} {label}</span></li>'
        )
    return (
        '<nav class="contents"><h2>In this edition</h2>'
        f'<ol>{"".join(items)}</ol></nav>'
    )


# --------------------------------------------------------------------------- #
# Pages
# --------------------------------------------------------------------------- #
def render_edition(edition, prev_ed, next_ed):
    root = "../../"
    date_long = fmt_date(edition["date"])
    region = edition.get("region", "")
    cats_html = "".join(
        render_category(cat, i) for i, cat in enumerate(edition["categories"], start=1)
    )
    masthead = f"""<div class="wrap">
  <div class="edition-top"><a class="backlink" href="{root}index.html">&larr; All editions</a>
    <span class="backlink">{esc(region)}</span></div>
  <div class="masthead">
    <div class="kicker">{esc(edition.get("kicker", SITE_KICKER))}</div>
    <h1>{esc(edition["masthead"])}</h1>
    <div class="meta">{esc(date_long)}<span class="dot">&bull;</span>{esc(region)}</div>
    <p class="summary">{esc(edition.get("summary", ""))}</p>
  </div>
  {render_contents(edition["categories"])}
  {cats_html}
  {edition_pager(prev_ed, next_ed, root)}
</div>"""
    title = f'{edition["masthead"]}, {fmt_date(edition["date"], weekday=False)} · {SITE_NAME}'
    return page_shell(title, edition.get("summary", TAGLINE), masthead, root, canon(f'/editions/{edition["date"]}/'))


def edition_pager(prev_ed, next_ed, root):
    left = ""
    right = ""
    if next_ed:  # newer
        left = f'<a class="pager" href="{root}editions/{next_ed["date"]}/">&larr; Newer: {fmt_date(next_ed["date"], weekday=False)}</a>'
    if prev_ed:  # older
        right = f'<a class="pager" href="{root}editions/{prev_ed["date"]}/">Older: {fmt_date(prev_ed["date"], weekday=False)} &rarr;</a>'
    return f'<div class="edition-foot">{left or "<span></span>"}{right or "<span></span>"}</div>'


LAPTOP_SVG = '''<svg viewBox="0 0 600 470" role="img" aria-label="A laptop showing the Pinnacle Digest daily briefing">
  <defs>
    <linearGradient id="deck" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#2c2f39"/><stop offset="1" stop-color="#1a1c23"/></linearGradient>
    <linearGradient id="frame" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#2a2d37"/><stop offset="1" stop-color="#20222b"/></linearGradient>
    <clipPath id="screenClip"><rect x="104" y="40" width="392" height="264" rx="7"/></clipPath>
  </defs>
  <path d="M60 326 L540 326 L590 366 L10 366 Z" fill="url(#deck)"/>
  <path d="M10 366 L590 366 L578 380 L22 380 Z" fill="#14151b"/>
  <rect x="250" y="330" width="100" height="9" rx="4.5" fill="#3b3e49"/>
  <rect x="88" y="22" width="424" height="306" rx="16" fill="url(#frame)"/>
  <rect x="104" y="40" width="392" height="264" rx="7" fill="#ffffff"/>
  <circle cx="300" cy="31" r="2.6" fill="#565a66"/>
  <g clip-path="url(#screenClip)" font-family="Poppins, sans-serif">
    <circle cx="126" cy="60" r="4" fill="#cc0000"/><circle cx="137" cy="60" r="4" fill="#003399"/><circle cx="148" cy="60" r="4" fill="#009900"/>
    <text x="162" y="64" font-size="13" font-weight="700" fill="#17203a">Pinnacle Digest</text>
    <text x="476" y="64" font-size="10" fill="#8a93a8" text-anchor="end">2 Sep 2026</text>
    <line x1="104" y1="76" x2="496" y2="76" stroke="#e3e8f2"/>
    <text x="300" y="101" font-family="Caveat, cursive" font-size="17" fill="#009900" text-anchor="middle">the</text>
    <text x="300" y="120" font-size="17" font-weight="700" fill="#003399" text-anchor="middle">Daily Accountancy Briefing</text>
    <text x="300" y="135" font-size="8.5" letter-spacing="1.4" fill="#8a93a8" text-anchor="middle">WEDNESDAY, 2 SEPTEMBER 2026 &#183; UK &amp; IRELAND</text>
    <text x="124" y="166" font-size="13.5" font-weight="700" fill="#17203a">UK M&amp;A value up eight-fold</text>
    <text x="124" y="183" font-size="13.5" font-weight="700" fill="#17203a">in H1 2026</text>
    <rect x="124" y="193" width="66" height="19" rx="9.5" fill="#e7edfb"/><text x="157" y="206" font-size="10" font-weight="600" fill="#0a327e" text-anchor="middle">£33.7bn</text>
    <rect x="196" y="193" width="70" height="19" rx="9.5" fill="#e3f5e3"/><text x="231" y="206" font-size="10" font-weight="600" fill="#157a15" text-anchor="middle">135 deals</text>
    <line x1="124" y1="286" x2="252" y2="286" stroke="#d2d9e8"/>
    <rect x="132" y="252" width="26" height="34" rx="3" fill="#4d7bff"/>
    <rect x="176" y="240" width="26" height="46" rx="3" fill="#4d7bff"/>
    <rect x="220" y="216" width="26" height="70" rx="3" fill="#009900"/>
    <g fill="#dfe4ee">
      <rect x="272" y="150" width="204" height="8" rx="4"/><rect x="272" y="166" width="204" height="8" rx="4"/>
      <rect x="272" y="182" width="188" height="8" rx="4"/><rect x="272" y="198" width="204" height="8" rx="4"/>
      <rect x="272" y="214" width="164" height="8" rx="4"/><rect x="272" y="238" width="204" height="8" rx="4"/>
      <rect x="272" y="254" width="180" height="8" rx="4"/><rect x="272" y="270" width="204" height="8" rx="4"/>
    </g>
  </g>
  <g transform="translate(454 42)" style="filter:drop-shadow(0 12px 22px rgba(16,30,60,.20))">
    <rect x="0" y="0" width="118" height="66" rx="14" fill="#ffffff" stroke="#e3e8f2"/>
    <circle cx="27" cy="33" r="16" fill="#e3f5e3"/>
    <path d="M21 37 L27 29 L33 37" fill="none" stroke="#009900" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>
    <text x="53" y="30" font-family="Poppins,sans-serif" font-size="18" font-weight="700" fill="#17203a">8x</text>
    <text x="53" y="46" font-family="Poppins,sans-serif" font-size="9" fill="#8a93a8">H1 deal value</text>
  </g>
  <g transform="translate(20 250)" style="filter:drop-shadow(0 12px 22px rgba(16,30,60,.20))">
    <rect x="0" y="0" width="124" height="60" rx="14" fill="#ffffff" stroke="#e3e8f2"/>
    <text x="15" y="40" font-family="Poppins,sans-serif" font-size="23" font-weight="700" fill="#003399">52%</text>
    <text x="66" y="27" font-family="Poppins,sans-serif" font-size="9" fill="#5a657d">of gains from</text>
    <text x="66" y="40" font-family="Poppins,sans-serif" font-size="9" fill="#5a657d">240 filers</text>
  </g>
</svg>'''

NEWS_CARD_SVG = '''<svg viewBox="0 0 360 300" role="img" aria-label="A Pinnacle Digest briefing card">
  <g style="filter:drop-shadow(0 16px 30px rgba(16,30,60,.16))">
    <rect x="20" y="18" width="320" height="264" rx="16" fill="#ffffff" stroke="#e3e8f2"/>
  </g>
  <g font-family="Poppins, sans-serif">
    <circle cx="44" cy="46" r="4" fill="#cc0000"/><circle cx="55" cy="46" r="4" fill="#003399"/><circle cx="66" cy="46" r="4" fill="#009900"/>
    <text x="80" y="50" font-size="12" font-weight="700" fill="#17203a">Pinnacle Digest</text>
    <line x1="40" y1="62" x2="320" y2="62" stroke="#e3e8f2"/>
    <text x="180" y="86" font-family="Caveat, cursive" font-size="15" fill="#009900" text-anchor="middle">the</text>
    <text x="180" y="104" font-size="15" font-weight="700" fill="#003399" text-anchor="middle">Daily Accountancy Briefing</text>
    <rect x="40" y="120" width="24" height="16" rx="4" fill="#003399"/><text x="52" y="132" font-size="9" font-weight="700" fill="#fff" text-anchor="middle">01</text>
    <text x="72" y="132" font-size="12" font-weight="700" fill="#003399">HMRC</text>
    <line x1="118" y1="128" x2="320" y2="128" stroke="#dbe6d9"/>
    <text x="40" y="156" font-size="11.5" font-weight="700" fill="#17203a">First crypto-gains dataset lands</text>
    <rect x="40" y="164" width="60" height="17" rx="8.5" fill="#e7edfb"/><text x="70" y="176" font-size="9" font-weight="600" fill="#0a327e" text-anchor="middle">£1.38bn</text>
    <rect x="106" y="164" width="52" height="17" rx="8.5" fill="#fbe7e7"/><text x="132" y="176" font-size="9" font-weight="600" fill="#b01414" text-anchor="middle">240 = 52%</text>
    <g fill="#eef1f7">
      <rect x="40" y="198" width="140" height="30" rx="6"/><rect x="188" y="198" width="132" height="30" rx="6"/>
    </g>
    <text x="55" y="217" font-size="16" font-weight="700" fill="#003399">£168m</text>
    <text x="203" y="217" font-size="16" font-weight="700" fill="#009900">17,600</text>
    <line x1="40" y1="250" x2="120" y2="250" stroke="#d2d9e8"/>
    <rect x="46" y="238" width="14" height="12" rx="2" fill="#4d7bff"/>
    <rect x="70" y="232" width="14" height="18" rx="2" fill="#4d7bff"/>
    <rect x="94" y="226" width="14" height="24" rx="2" fill="#009900"/>
  </g>
</svg>'''

ICONS = {
    "calendar": '<svg viewBox="0 0 24 24" fill="none" stroke="#003399" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="18" rx="2"/><line x1="3" y1="9" x2="21" y2="9"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="16" y1="2" x2="16" y2="6"/></svg>',
    "layers": '<svg viewBox="0 0 24 24" fill="none" stroke="#009900" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="12 2 22 8.5 12 15 2 8.5 12 2"/><polyline points="2 15.5 12 22 22 15.5"/></svg>',
    "chart": '<svg viewBox="0 0 24 24" fill="none" stroke="#cc0000" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="4" y1="20" x2="4" y2="12"/><line x1="10" y1="20" x2="10" y2="4"/><line x1="16" y1="20" x2="16" y2="9"/><line x1="22" y1="20" x2="2" y2="20"/></svg>',
}

ABOUT_TEXT = ("Pinnacle Global is a London-headquartered offshore staffing and professional services firm "
              "with a delivery centre in Mumbai. We give UK and Ireland accountancy, tax and advisory practices "
              "the people they need, from auditors, accountants and bookkeepers to virtual finance controllers, "
              "insolvency administrators, paraplanners and automation specialists.")


def pinnacle_banner():
    stats = [
        ("300+", "Specialists across the group"),
        ("150+", "Clients in the UK &amp; Ireland"),
        ("4", "Specialist divisions"),
        ("2", "Delivery hubs: London &amp; Mumbai"),
    ]
    tiles = "".join(
        f'<div><div class="s-num">{n}</div><div class="s-lab">{l}</div></div>' for n, l in stats
    )
    return f"""<section class="stat-banner">
  <div class="eyebrow" style="font-family:var(--font-ui);font-weight:600;font-size:12.5px;letter-spacing:.12em;text-transform:uppercase;">Brought to you by Pinnacle Global</div>
  <h2>The team behind the briefing</h2>
  <p>{ABOUT_TEXT}</p>
  <div class="stat-grid">{tiles}</div>
  <div style="margin-top:24px;position:relative;">
    <a class="btn" style="background:#fff;color:#003399;" href="{COMPANY_URL}">Learn more about Pinnacle &rarr;</a>
  </div>
</section>"""


def features_block():
    feats = [
        ("calendar", "Daily and dated", "A fresh edition every weekday, each one dated and archived so nothing gets lost and you can always trace when something landed."),
        ("layers", "Split by topic", "Every briefing is broken into the areas that matter to a practice: HMRC, MTD, practice, corporate finance, the FCA, Ireland and software."),
        ("chart", "Built on the numbers", "The figures that count are pulled out as charts, stat tiles and clear 'what this means for firms' takeaways, so the point is obvious at a glance."),
    ]
    cards = "".join(
        f'<div class="feature-card"><div class="f-ico">{ICONS[i]}</div>'
        f'<h3>{esc(t)}</h3><p>{d}</p></div>'
        for i, t, d in feats
    )
    return f"""<section class="section"><div class="section-head center">
    <div class="eyebrow">Why Pinnacle Digest</div>
    <h2>The day's news, decoded by breakfast</h2>
    <p>Not another inbox of raw headlines. A single, structured read designed for busy accountants and advisers.</p>
  </div><div class="feature-grid">{cards}</div></section>"""


def featured_block(latest):
    cat_names = [c["name"] for c in latest["categories"]]
    n_stories = sum(len(c.get("stories", [])) for c in latest["categories"])
    topics = "".join(f"<span>{esc(c)}</span>" for c in cat_names[:6])
    return f"""<section class="section"><div class="section-head">
    <div class="eyebrow">Latest edition</div>
    <h2>Today's briefing</h2>
  </div>
  <a class="featured" href="editions/{latest['date']}/" style="text-decoration:none;color:inherit;">
    <div class="f-body">
      <span class="f-flag">New today</span>
      <div class="f-date">{esc(fmt_date(latest['date']))} &middot; {esc(latest.get('region',''))}</div>
      <h3>{esc(latest['masthead'])}</h3>
      <p>{esc(latest.get('summary',''))}</p>
      <div class="f-topics">{topics}</div>
      <span class="btn btn-primary">Read the full briefing &rarr;</span>
    </div>
    <div class="f-media">{NEWS_CARD_SVG}</div>
  </a></section>"""


def render_home(editions):
    root = ""
    latest = editions[0]
    n_topics = len(latest["categories"])

    # unique category names across all editions for filter chips
    cat_names = []
    for ed in editions:
        for cat in ed["categories"]:
            if cat["name"] not in cat_names:
                cat_names.append(cat["name"])
    cat_names.sort()
    chips = ['<button class="filter-chip active" data-filter="__all__">All topics</button>']
    for name in cat_names:
        chips.append(f'<button class="filter-chip" data-filter="{esc(name)}">{esc(name)}</button>')

    cards = []
    current_year = None
    for ed in editions:
        y = ed["date"][:4]
        if y != current_year:
            current_year = y
            cards.append(f'<div class="year-head" data-cats="__year__">{y}</div>')
        cards.append(render_edition_card(ed))

    hero = f"""<section class="site-hero"><div class="hero-grid">
  <div class="hero-copy">
    <span class="hero-eyebrow">Pinnacle Digest</span>
    <h1>The daily accountancy briefing, <span class="accent">built for busy firms.</span></h1>
    <p class="hero-lead">Every weekday we turn the regulatory, technical and market news across the UK and Ireland into one fast, categorised read, with the numbers that matter pulled out as charts.</p>
    <div class="hero-cta">
      <a class="btn btn-primary" href="editions/{latest['date']}/">Read today's briefing &rarr;</a>
      <a class="btn btn-ghost" href="#archive">Browse the archive</a>
    </div>
    <div class="hero-trust">
      <span>Latest: <b>{esc(fmt_date(latest['date'], weekday=False))}</b></span>
      <span><b>{n_topics} topics</b> covered today</span>
      <span>New every <b>weekday</b></span>
    </div>
  </div>
  <div class="hero-art">{LAPTOP_SVG}</div>
</div></section>

<div class="wrap">
  {pinnacle_banner()}
  {featured_block(latest)}
  {features_block()}
  <section class="section" id="archive"><div class="section-head">
    <div class="eyebrow">The archive</div>
    <h2>Every edition</h2>
    <p>Browse the full run of briefings, or filter to the topics you care about.</p>
  </div>
  <div class="filters">{"".join(chips)}</div>
  {"".join(cards)}
  </section>
  <section class="cta-strip">
    <div>
      <h2>Never miss a briefing</h2>
      <p>A new edition lands every weekday. Add the feed to your reader, or bookmark the archive.</p>
    </div>
    <div class="cta-actions">
      <a class="btn btn-primary" href="editions/{latest['date']}/">Read the latest</a>
      <a class="btn btn-ghost" href="feed.xml">Subscribe via RSS</a>
    </div>
  </section>
</div>
{FILTER_SCRIPT}"""
    return page_shell(SITE_NAME, TAGLINE, hero, root, canon("/"))


def render_edition_card(ed):
    cat_names = [c["name"] for c in ed["categories"]]
    n_stories = sum(len(c.get("stories", [])) for c in ed["categories"])
    chips = "".join(f'<span class="cat-chip">{esc(c)}</span>' for c in cat_names[:6])
    data_cats = esc("|".join(cat_names))
    return f"""<a class="edition-card" href="editions/{ed['date']}/" data-cats="{data_cats}">
  <div class="date-row"><span class="date">{esc(fmt_date(ed['date']))}</span>
    <span class="region">{esc(ed.get('region',''))} &middot; {n_stories} updates across {len(cat_names)} topics</span></div>
  <h3>{esc(ed['masthead'])}</h3>
  <p>{esc(ed.get('summary',''))}</p>
  <div class="cat-chips">{chips}</div>
  <div class="readmore">Read the briefing &rarr;</div>
</a>"""


def render_feed(editions):
    items = []
    for ed in editions:
        link = f'{SITE_URL}/editions/{ed["date"]}/'
        title = f'{ed["masthead"]}, {fmt_date(ed["date"], weekday=False)}'
        items.append(f"""  <item>
    <title>{html.escape(title)}</title>
    <link>{link}</link>
    <guid isPermaLink="true">{link}</guid>
    <pubDate>{rss_date(ed["date"])}</pubDate>
    <description>{html.escape(ed.get("summary", ""))}</description>
  </item>""")
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0"><channel>
  <title>{SITE_NAME}</title>
  <link>{SITE_URL}/</link>
  <description>{html.escape(TAGLINE)}</description>
  <language>en-gb</language>
{chr(10).join(items)}
</channel></rss>"""


def render_404():
    body = """<div class="wrap"><section class="hero">
    <div class="eyebrow">404</div>
    <h1>Page not found</h1>
    <p>That edition or page does not exist. Head back to the archive for the latest briefing.</p>
    <p><a href="/index.html">&larr; Back to Pinnacle Digest</a></p>
  </section></div>"""
    return page_shell("Not found · " + SITE_NAME, "Page not found", body, "/")


# --------------------------------------------------------------------------- #
def build():
    if os.path.exists(OUT):
        shutil.rmtree(OUT)
    os.makedirs(OUT)
    shutil.copytree(ASSETS_DIR, os.path.join(OUT, "assets"))

    editions = load_editions()
    if not editions:
        raise SystemExit("No editions found in content/. Add a YYYY-MM-DD.json first.")

    # homepage
    with open(os.path.join(OUT, "index.html"), "w", encoding="utf-8") as fh:
        fh.write(render_home(editions))

    # editions (newest-first list; prev = older, next = newer)
    for idx, ed in enumerate(editions):
        newer = editions[idx - 1] if idx > 0 else None
        older = editions[idx + 1] if idx + 1 < len(editions) else None
        d = os.path.join(OUT, "editions", ed["date"])
        os.makedirs(d, exist_ok=True)
        with open(os.path.join(d, "index.html"), "w", encoding="utf-8") as fh:
            fh.write(render_edition(ed, prev_ed=older, next_ed=newer))

    with open(os.path.join(OUT, "feed.xml"), "w", encoding="utf-8") as fh:
        fh.write(render_feed(editions))
    with open(os.path.join(OUT, "404.html"), "w", encoding="utf-8") as fh:
        fh.write(render_404())
    if CUSTOM_DOMAIN:
        with open(os.path.join(OUT, "CNAME"), "w", encoding="utf-8") as fh:
            fh.write(CUSTOM_DOMAIN + "\n")
    open(os.path.join(OUT, ".nojekyll"), "w").close()

    # sitemap
    urls = [SITE_URL + "/"] + [f'{SITE_URL}/editions/{e["date"]}/' for e in editions]
    sm = ['<?xml version="1.0" encoding="UTF-8"?>',
          '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for u in urls:
        sm.append(f"  <url><loc>{u}</loc></url>")
    sm.append("</urlset>")
    with open(os.path.join(OUT, "sitemap.xml"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(sm))

    print(f"Built {len(editions)} edition(s) -> {os.path.relpath(OUT, ROOT)}/")
    for e in editions:
        print(f"  /editions/{e['date']}/  ({fmt_date(e['date'])})")


if __name__ == "__main__":
    build()
