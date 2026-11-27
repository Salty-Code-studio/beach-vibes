"""Samples colours from each photo -> tools/palette.json. Needs Pillow.
Per image: dom (most common), deep (dark, saturated: for text-safe backgrounds), soft (light tint), accent (most saturated)."""
import json, colorsys, pathlib
from PIL import Image
ROOT = pathlib.Path(__file__).resolve().parent.parent
out = {}
def hexc(c): return "#%02x%02x%02x" % tuple(int(v) for v in c)
for f in sorted((ROOT / "site/img").glob("*.webp")):
    im = Image.open(f).convert("RGB"); im.thumbnail((160, 160))
    q = im.quantize(colors=8, method=Image.Quantize.MEDIANCUT)
    pal = q.getpalette()[:24]; counts = sorted(q.getcolors(), reverse=True)
    cols = [(n, tuple(pal[i*3:i*3+3])) for n, i in counts]
    hls = lambda c: colorsys.rgb_to_hls(*(v/255 for v in c))
    dom = cols[0][1]
    acc = max(cols, key=lambda nc: hls(nc[1])[2] * (1 - abs(hls(nc[1])[1] - .5)) * (nc[0] ** .3))[1]
    h, l, s = hls(acc); hd, ld, sd = hls(dom)
    deep = colorsys.hls_to_rgb(h, .2, min(.55, s))
    soft = colorsys.hls_to_rgb(hd, .93, min(.35, sd + .05))
    mid = colorsys.hls_to_rgb(h, .78, min(.45, s))
    out[f.stem] = dict(dom=hexc(dom), accent=hexc(acc), deep=hexc([v*255 for v in deep]), soft=hexc([v*255 for v in soft]), mid=hexc([v*255 for v in mid]))
(ROOT / "tools/palette.json").write_text(json.dumps(out, indent=1))
for k in ["hero-cacti-xl","store-playa","store-sorobon","jw-bracelets","lb-30","lb-26","lb-20","lb-08","jw-charms","lb-19","salty-truck","lb-16","lb-01"]:
    print(k, out[k])
