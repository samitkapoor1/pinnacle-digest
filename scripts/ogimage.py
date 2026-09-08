"""
Per-edition social share (Open Graph) image generator for Pinnacle Digest.

Renders a 1200x630 PNG for each edition showing the publication label, the
date, the edition's own headline, and the topics it covers, in Pinnacle
brand colours. Uses Pillow and the bundled Outfit / handwriting fonts, so
the build stays deterministic and needs no network at build time.

render_og(out_path, headline, date_label, topics, home=False)
"""

import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(__file__)
FONTS = os.path.join(HERE, "fonts")
ASSETS = os.path.join(HERE, "..", "assets")

W, H = 1200, 630
BLUE = (0, 51, 153)
BLUE_DEEP = (0, 34, 110)
GREEN = (0, 153, 0)
GREEN_LT = (154, 230, 160)
WHITE = (255, 255, 255)
INK_SOFT = (206, 216, 240)

_font_cache = {}


def font(name, size):
    key = (name, size)
    if key not in _font_cache:
        _font_cache[key] = ImageFont.truetype(os.path.join(FONTS, name), size)
    return _font_cache[key]


def _bg():
    """Diagonal blue gradient with a soft green glow in the corner."""
    base = Image.new("RGB", (W, H), BLUE)
    top = Image.new("RGB", (W, H), BLUE_DEEP)
    mask = Image.new("L", (W, H))
    md = mask.load()
    for y in range(H):
        for x in range(0, W, 4):
            v = int(255 * ((x / W) * 0.45 + (y / H) * 0.55))
            c = 255 - min(255, v)
            md[x, y] = c
            if x + 1 < W: md[x + 1, y] = c
            if x + 2 < W: md[x + 2, y] = c
            if x + 3 < W: md[x + 3, y] = c
    img = Image.composite(top, base, mask)
    # green glow, bottom-right
    glow = Image.new("RGB", (W, H), (10, 120, 40))
    gmask = Image.new("L", (W, H), 0)
    gd = ImageDraw.Draw(gmask)
    gd.ellipse([W - 520, H - 360, W + 260, H + 300], fill=90)
    img = Image.composite(glow, img, gmask)
    return img


def _wrap(draw, text, fnt, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def _fit_headline(draw, text, max_w, max_lines=3, hi=76, lo=44):
    """Largest Outfit-Bold size where the headline fits in max_lines."""
    for size in range(hi, lo - 1, -2):
        fnt = font("Outfit-Bold.ttf", size)
        lines = _wrap(draw, text, fnt, max_w)
        if len(lines) <= max_lines:
            return fnt, lines, size
    fnt = font("Outfit-Bold.ttf", lo)
    return fnt, _wrap(draw, text, fnt, max_w)[:max_lines], lo


def _pill(draw, x, y, text, fnt):
    pad_x, pad_y = 18, 9
    tw = draw.textlength(text, font=fnt)
    asc, desc = fnt.getmetrics()
    th = asc + desc
    w = tw + pad_x * 2
    h = th + pad_y * 2
    draw.rounded_rectangle([x, y, x + w, y + h], radius=h // 2,
                           fill=(255, 255, 255, 255), outline=None)
    draw.text((x + pad_x, y + pad_y - 1), text, font=fnt, fill=BLUE)
    return w, h


def render_og(out_path, headline, date_label, topics, home=False):
    img = _bg().convert("RGBA")
    draw = ImageDraw.Draw(img)

    MX = 72          # left/right margin
    top_y = 66

    # logo monogram (top-left)
    try:
        mono = Image.open(os.path.join(ASSETS, "icon-512.png")).convert("RGBA")
        mono.thumbnail((78, 78), Image.LANCZOS)
        # white-rounded plate behind it for contrast on blue
        plate = 96
        draw.rounded_rectangle([MX, top_y, MX + plate, top_y + plate], radius=20, fill=WHITE)
        img.alpha_composite(mono, (MX + (plate - mono.width) // 2, top_y + (plate - mono.height) // 2))
    except Exception:
        plate = 0

    tx = MX + (plate + 22 if plate else 0)
    draw.text((tx, top_y + 8), "the", font=font("NothingYouCouldDo-Regular.ttf", 34), fill=GREEN_LT)
    draw.text((tx, top_y + 40), "PINNACLE DIGEST", font=font("Outfit-Bold.ttf", 30), fill=WHITE)

    # kicker line (date + region)
    kicker = ("DAILY ACCOUNTANCY BRIEFING" if not home else "UK & IRELAND")
    meta = f"{kicker}   •   {date_label}   •   UK & IRELAND" if not home else "A DAILY BRIEFING FOR UK & IRELAND FIRMS"
    draw.text((MX, 210), meta, font=font("Outfit-Regular.ttf", 22), fill=GREEN_LT)

    # headline
    max_w = W - MX * 2
    fnt, lines, size = _fit_headline(draw, headline, max_w, max_lines=3)
    line_h = int(size * 1.16)
    y = 250
    for ln in lines:
        draw.text((MX, y), ln, font=fnt, fill=WHITE)
        y += line_h

    # topic pills, placed a consistent gap below the headline
    if topics:
        py = min(516, y + 18)
        px = MX
        pill_font = font("Outfit-Regular.ttf", 22)
        line_used = 0
        for t in topics:
            tw = draw.textlength(t, font=pill_font) + 36
            if px + tw > W - MX:
                break
            w, h = _pill(draw, px, py, t, pill_font)
            px += w + 12
            line_used += 1
            if line_used >= 6:
                break

    # footer
    draw.line([(MX, 566), (W - MX, 566)], fill=(255, 255, 255, 60), width=1)
    draw.text((MX, 582), "pinnacleglobalgroup.com", font=font("Outfit-Regular.ttf", 22), fill=INK_SOFT)
    tag = "New every weekday"
    tw = draw.textlength(tag, font=font("Outfit-Regular.ttf", 22))
    draw.text((W - MX - tw, 582), tag, font=font("Outfit-Regular.ttf", 22), fill=INK_SOFT)

    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    img.convert("RGB").save(out_path, "PNG", optimize=True)
    return out_path
