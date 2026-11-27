"""Beachvibes logo patterns, redrawn as seamless SVG tiles.
Run: python3 tools/patterns.py  ->  patterns/svg/*.svg (+ patterns/index.html preview)
Each tile uses currentColor-free fills so it works as a background-image; colour is set per file (ink / white).
"""
import math, pathlib

OUT = pathlib.Path(__file__).resolve().parent.parent / "patterns"
SW = 3  # stroke width in tile units


def svg(w, h, body, col):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">'
            f'<g fill="none" stroke="{col}" stroke-width="{SW}" stroke-linecap="round" stroke-linejoin="round">{body}</g></svg>')


def dot(x, y, r, col):
    return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{col}" stroke="none"/>'


def triangle_band(col):
    """'h' + 'a': rules with a row of alternating triangles, solid and open."""
    w, h = 48, 48
    b = f'<path d="M0 6H48M0 42H48"/>'
    b += f'<path d="M0 36L12 12L24 36Z" fill="{col}"/><path d="M24 12L36 36L48 12"/>'
    return svg(w, h, b, col)


def x_lattice(col):
    """first 'e': crossing diagonals with a dot in each diamond."""
    w = h = 40
    b = '<path d="M0 0L40 40M40 0L0 40M-20 20L0 40M20 -20L60 20M20 60L60 20M-20 20L20 -20"/>'
    b += "".join(dot(x, y, 3, col) for x, y in ((20, 0), (20, 40), (0, 20), (40, 20)))  # one dot per diamond, split over tile edges
    return svg(w, h, b, col)


def spirals(col):
    """'b': stacked spirals, offset every other row."""
    def spiral(cx, cy, turns=2.25, r=11):
        pts = []
        n = 60
        for i in range(n + 1):
            t = i / n
            a = t * turns * 2 * math.pi
            rr = r * t
            pts.append(f"{cx + rr * math.cos(a):.2f} {cy + rr * math.sin(a):.2f}")
        return '<path d="M' + " L".join(pts) + '"/>'
    w, h = 56, 56
    b = spiral(14, 14) + spiral(42, 42) + spiral(-14, 42) + spiral(70, 14)
    return svg(w, h, b, col)


def chevron_heart(col):
    """'v': nested downward chevrons with a small heart in the gap."""
    w, h = 48, 56
    b = '<path d="M0 4L24 30L48 4M0 16L24 42L48 16"/>'
    b += ('<path d="M24 52c-5-4-8-6.5-8-9.5a3.6 3.6 0 0 1 8-1.4a3.6 3.6 0 0 1 8 1.4c0 3-3 5.5-8 9.5Z" '
          f'fill="{col}" stroke="none" transform="translate(0 -38) scale(1)"/>')
    b += dot(6, 44, 2.4, col) + dot(42, 44, 2.4, col)
    return svg(w, h, b, col)


def diagonal_stripes(col):
    """second 'e': even diagonal hatching."""
    w = h = 24
    b = '<path d="M-6 6L6 -6M-6 30L30 -6M18 30L30 18"/>'
    return svg(w, h, b, col)


def ladder_band(col):
    """'s': framed band of short vertical bars."""
    w, h = 36, 40
    b = '<path d="M0 8H36M0 32H36"/>'
    b += "".join(f'<path d="M{x} 13V27"/>' for x in (3, 12, 21, 30))
    return svg(w, h, b, col)


def dot_rule(col):
    """'a' / 'h' bands: double rule with dots and small squares between."""
    w, h = 40, 32
    b = '<path d="M0 6H40M0 26H40"/>'
    b += dot(10, 16, 2.6, col) + dot(30, 16, 2.6, col)
    b += f'<rect x="17" y="13" width="6" height="6" fill="{col}" stroke="none"/>'
    b += '<path d="M0 16H4M36 16H40"/>'
    return svg(w, h, b, col)


def tribal_border(col):
    """All the bands stacked into one horizontal border strip (repeats left to right)."""
    w, h = 48, 132
    b = '<path d="M0 4H48M0 128H48"/>'
    # triangles
    b += f'<path d="M0 34L12 12L24 34Z" fill="{col}"/><path d="M24 12L36 34L48 12"/>'
    b += '<path d="M0 42H48"/>'
    # dots + squares
    b += dot(12, 54, 2.6, col) + dot(36, 54, 2.6, col) + f'<rect x="21" y="51" width="6" height="6" fill="{col}" stroke="none"/>'
    b += '<path d="M0 66H48"/>'
    # ladder
    b += "".join(f'<path d="M{x} 72V88"/>' for x in (4, 16, 28, 40))
    b += '<path d="M0 94H48"/>'
    # zigzag
    b += '<path d="M0 120L12 100L24 120L36 100L48 120"/>'
    return svg(w, h, b, col)


PATTERNS = {
    "triangle-band": (triangle_band, "Rules with a row of solid and open triangles (from the h and a)"),
    "x-lattice": (x_lattice, "Crossing diagonals with a dot in every diamond (from the first e)"),
    "spirals": (spirals, "Offset rows of spirals (from the b)"),
    "chevron-heart": (chevron_heart, "Nested chevrons with a heart (from the v)"),
    "diagonal-stripes": (diagonal_stripes, "Even diagonal hatching (from the second e)"),
    "ladder-band": (ladder_band, "Framed band of short bars (from the s)"),
    "dot-rule": (dot_rule, "Double rule with dots and squares (from the a)"),
    "tribal-border": (tribal_border, "All bands stacked into one border strip"),
}
COLOURS = {"ink": "#0E2A3B", "white": "#FFFFFF", "char": "#242328"}

if __name__ == "__main__":
    d = OUT / "svg"; d.mkdir(parents=True, exist_ok=True)
    cards = ""
    for key, (fn, desc) in PATTERNS.items():
        for cname, col in COLOURS.items():
            (d / f"{key}-{cname}.svg").write_text(fn(col))
        cards += (f'<figure><div class="sw" style="background-image:url(svg/{key}-ink.svg)"></div>'
                  f'<div class="sw dark" style="background-image:url(svg/{key}-white.svg)"></div>'
                  f'<figcaption><b>{key}</b><br>{desc}</figcaption></figure>')
    (OUT / "index.html").write_text(f"""<!doctype html><meta charset="utf-8"><title>Beachvibes patterns</title>
<style>body{{margin:0;padding:32px;background:#F3EEE4;font:15px/1.4 system-ui;color:#242328}}h1{{font-weight:800;margin:0 0 24px}}
main{{display:grid;grid-template-columns:repeat(4,1fr);gap:20px}}figure{{margin:0}}.sw{{height:170px;border-radius:6px;background-color:#F8F4EC;background-size:auto 56px;border:1px solid #e0d8c8}}
.sw.dark{{background-color:#242328;margin-top:8px;border-color:#242328}}figcaption{{margin-top:8px;font-size:13px}}</style>
<h1>Beachvibes patterns</h1><main>{cards}</main>""")
    print("wrote", len(PATTERNS) * len(COLOURS), "svgs")
