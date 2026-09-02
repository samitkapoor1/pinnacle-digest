"""
Build-time chart engine for Pinnacle Digest.

Each function takes a chart spec (see scripts/seed_content.py) and returns an
HTML string: a <figure class="chart"> wrapping an inline SVG for the plotted
part plus HTML for prose (titles, captions, notes). Inline SVG means the
charts are crisp, dependency-free, work offline and on GitHub Pages, and are
styled by the site stylesheet so they adapt to light and dark themes.

Colours come from the site CSS via classes (cx-fill-*, cx-label, cx-axis,
cx-value ...) so the Pinnacle palette lives in one place.
"""

import html

# Brand palette, mirrored in styles.css. Order used to colour multi-bar charts.
PALETTE = ["blue", "green", "cyan", "sage", "red"]


def esc(text):
    return html.escape(str(text), quote=True)


def render_chart(spec):
    kind = spec.get("type")
    fn = {
        "stat_row": stat_row,
        "compare_bars": compare_bars,
        "bars": bars,
        "gauge": gauge,
    }.get(kind)
    if not fn:
        return ""
    return fn(spec)


def _head(spec):
    title = spec.get("title")
    unit = spec.get("unit")
    if not title and not unit:
        return ""
    left = f'<span class="chart-title">{esc(title)}</span>' if title else "<span></span>"
    right = f'<span class="chart-unit">{esc(unit)}</span>' if unit else ""
    return f'<div class="chart-head">{left}{right}</div>'


def _note(spec):
    note = spec.get("note")
    return f'<p class="chart-note">{esc(note)}</p>' if note else ""


def stat_row(spec):
    items = spec.get("items", [])
    tiles = []
    for it in items:
        tiles.append(
            '<div class="stat-tile">'
            f'<div class="stat-value">{esc(it.get("value",""))}</div>'
            f'<div class="stat-label">{esc(it.get("label",""))}</div>'
            "</div>"
        )
    return f'<figure class="chart chart-stats"><div class="stat-row">{"".join(tiles)}</div></figure>'


def _bar_svg(bar_specs, highlight_last=False, force_colors=None):
    """Vertical bars. bar_specs: list of dicts with label, value, display, caption."""
    W, H = 640, 300
    pad_l, pad_r, pad_t, pad_b = 24, 24, 52, 74
    plot_w = W - pad_l - pad_r
    plot_h = H - pad_t - pad_b
    n = len(bar_specs)
    if n == 0:
        return ""
    vals = [max(0.0, float(b.get("value", 0))) for b in bar_specs]
    vmax = max(vals) or 1.0
    # bar sizing
    slot = plot_w / n
    bar_w = min(slot * 0.52, 120)
    baseline = pad_t + plot_h
    parts = [f'<svg viewBox="0 0 {W} {H}" class="cx-svg" role="img" preserveAspectRatio="xMidYMid meet">']
    # baseline
    parts.append(f'<line x1="{pad_l}" y1="{baseline:.1f}" x2="{W-pad_r}" y2="{baseline:.1f}" class="cx-axis"/>')
    for i, b in enumerate(bar_specs):
        cx = pad_l + slot * (i + 0.5)
        h = (vals[i] / vmax) * plot_h
        y = baseline - h
        x = cx - bar_w / 2
        if force_colors:
            color = force_colors[i % len(force_colors)]
        elif highlight_last:
            color = "green" if i == n - 1 else "blue"
        else:
            color = PALETTE[i % len(PALETTE)]
        parts.append(
            f'<rect x="{x:.1f}" y="{y:.1f}" width="{bar_w:.1f}" height="{max(h,2):.1f}" '
            f'rx="6" class="cx-fill-{color}"/>'
        )
        display = b.get("display") or b.get("value")
        parts.append(
            f'<text x="{cx:.1f}" y="{y-12:.1f}" class="cx-value" text-anchor="middle">{esc(display)}</text>'
        )
        parts.append(
            f'<text x="{cx:.1f}" y="{baseline+26:.1f}" class="cx-label" text-anchor="middle">{esc(b.get("label",""))}</text>'
        )
        cap = b.get("caption")
        if cap:
            parts.append(
                f'<text x="{cx:.1f}" y="{baseline+46:.1f}" class="cx-caption" text-anchor="middle">{esc(cap)}</text>'
            )
    parts.append("</svg>")
    return "".join(parts)


def compare_bars(spec):
    svg = _bar_svg(spec.get("bars", []), force_colors=["blue", "green", "cyan", "sage"])
    return f'<figure class="chart">{_head(spec)}{svg}{_note(spec)}</figure>'


def bars(spec):
    svg = _bar_svg(spec.get("bars", []), highlight_last=True)
    return f'<figure class="chart">{_head(spec)}{svg}{_note(spec)}</figure>'


def gauge(spec):
    value = float(spec.get("value", 0))
    pct = max(0.0, min(100.0, value))
    W, H = 640, 120
    pad = 24
    num_w = 150
    track_x = pad + num_w
    track_w = W - pad - track_x
    track_y = H / 2 - 16
    track_h = 32
    fill_w = track_w * pct / 100.0
    display = spec.get("display") or f"{int(value)}%" if value == int(value) else f"{value}%"
    svg = (
        f'<svg viewBox="0 0 {W} {H}" class="cx-svg cx-gauge" role="img" preserveAspectRatio="xMidYMid meet">'
        f'<text x="{pad}" y="{H/2+22:.1f}" class="cx-bignum">{esc(display)}</text>'
        f'<rect x="{track_x}" y="{track_y}" width="{track_w}" height="{track_h}" rx="16" class="cx-track"/>'
        f'<rect x="{track_x}" y="{track_y}" width="{fill_w:.1f}" height="{track_h}" rx="16" class="cx-fill-green"/>'
        f'</svg>'
    )
    head = _head(spec)
    label = spec.get("label")
    lbl = f'<p class="chart-note">{esc(label)}</p>' if label else ""
    return f'<figure class="chart chart-gauge">{head}{svg}{lbl}</figure>'
