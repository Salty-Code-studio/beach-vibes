#!/usr/bin/env python3
"""Builds the Beachvibes concept site into ../site/*.html.
Content lives in this file (stores, products, brands, lookbook). Run: python3 tools/build.py
"""
import html, json, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
SITE = ROOT / "site"
ISLAND, KLEIN = (ROOT / "tools/island-paths.txt").read_text().split("\n")[:2]
WA = "5997009744"
PAL = json.loads((ROOT / "tools/palette.json").read_text())
def pc(img, k): return PAL[img][k]
_AN = json.loads((ROOT / "tools/analytics.json").read_text())
# PostHog (EU), cookieless. Visits, time on page, country, referrer; ?for=name tags a personal link.
ANALYTICS = """<script src="js/ph.js?v=1" defer></script>
<script>
addEventListener('DOMContentLoaded', function () {
  if (!window.posthog || !posthog.init) return;
  var off = false;
  try { off = localStorage.getItem('bv-optout') === '1'; } catch (e) {}
  if (off || navigator.doNotTrack === '1' || window.doNotTrack === '1' || navigator.globalPrivacyControl) return;
  var q = new URLSearchParams(location.search).get('for');
  try { if (q) sessionStorage.setItem('bv-for', q); q = q || sessionStorage.getItem('bv-for'); } catch (e) {}
  posthog.init('""" + _AN["posthog_token"] + """', { api_host: '""" + _AN["posthog_host"] + """', persistence: 'memory', person_profiles: 'identified_only', disable_surveys: true, disable_session_recording: true, capture_pageleave: true, property_denylist: ['$ip'] });
  posthog.register({ site: 'beach-vibes-mockup' });
  if (q) {
    posthog.register({ recipient: q }); posthog.identify('beachvibes:' + q, { name: q, site: 'beach-vibes-mockup' });
    var seen = false; try { seen = sessionStorage.getItem('bv-note') === '1'; } catch (e) {}
    if (!seen) {
      var n = document.createElement('div'); n.className = 'link-note'; n.setAttribute('role', 'status');
      n.innerHTML = '<p>This is your personal preview link, so we can see when it is opened and which pages are viewed. <a href="privacy.html">How we handle this</a></p><button type="button" aria-label="Close">×</button>';
      n.querySelector('button').onclick = function () { n.remove(); try { sessionStorage.setItem('bv-note', '1'); } catch (e) {} };
      document.body.appendChild(n);
    }
  }
});
</script>"""
e = html.escape

# ------------------------------------------------------------------ data
STORES = [
    dict(key="playa", n=1, name="Beachvibes Playa", area="Kralendijk", street="Kaya Grandi 34-c",
         hours="Mon–Sat 10:00–17:00", days=[None] + [(10, 17)] * 6, phone="+599 700 9744",
         maps="https://maps.app.goo.gl/fyhPpwQhxos6Yfyj6", xy=(378, 436),
         blurb="The flagship on Kralendijk's main shopping street, a short walk from the cruise pier. Swim, surf labels, our own Beachvibes tees and the handmade jewelry bar.",
         find=["Swim & bikinis", "Kulani Kinis", "H11 Hang Eleven", "Beachvibes tees", "Handmade jewelry"],
         photos=["store-playa", "jw-bracelets", "lb-30"]),
    dict(key="salty", n=2, name="Salty Crew Bonaire", area="Kralendijk", street="Kaya L.D. Gerharts 8",
         hours="Mon–Sat 10:00–17:00", days=[None] + [(10, 17)] * 6, phone="+599 700 9744",
         maps="https://maps.app.goo.gl/wudYQwenV5TNmC4S7", xy=(391, 437),
         blurb="Right around the corner from Playa. The island home of Salty Crew, with Vans footwear and new menswear from Anuanua.",
         find=["Salty Crew", "Vans", "Anuanua", "Menswear", "Caps & tees"],
         photos=["salty-shirt", "salty-truck", "vans-knu-close"]),
    dict(key="sorobon", n=3, name="Beachvibes Sorobon", area="Lac Bay", street="Kaminda Sorobon 10",
         hours="Every day 10:00–17:00", days=[(10, 17)] * 7, phone="+599 700 9744",
         maps="https://maps.app.goo.gl/JkyehBdrmAwRNgUM7", xy=(491, 600),
         blurb="On the windsurf beach at Lac Bay, open seven days. Swimwear, sun gear and everything you forgot to pack for a day on the lagoon.",
         find=["Swimwear", "Boardshorts", "Hats & sun care", "Beach basics", "Open on Sundays"],
         photos=["store-sorobon", "lb-08", "lb-16"]),
]
# ships photo, product records. packshot=True renders the image contained on white.
PRODUCTS = [
    dict(id="donkey", name="Beachvibes Donkey Tee", brand="Beachvibes", price="$39.95", cat="tees", img="hero-cacti",
         alt="Man walking between cacti wearing the white Beachvibes donkey tee, seen from the back",
         where="Beachvibes Playa and Sorobon", whereShort="Beachvibes Playa", tag="Our own",
         colors=[["Navy", "#1E2E4A"], ["Off-white", "#F1EDE3"], ["Charcoal", "#3A3D40"], ["Pink", "#F4B6C8"]],
         note="Our own design, printed with the Bonaire donkey on the back."),
    dict(id="knu-skool", name="Vans Knu Skool", brand="Vans", price="$109.95", cat="footwear", img="vans-knu-skool", packshot=True,
         alt="Vans Knu Skool sneaker in black and white", where="Salty Crew Bonaire", whereShort="Salty Crew Bonaire", tag="New"),
    dict(id="knu-stacked", name="Vans Knu Stacked", brand="Vans", price="$124.95", cat="footwear", img="vans-knu-stacked", packshot=True,
         alt="Vans Knu Stacked sneaker with a thick platform sole", where="Salty Crew Bonaire", whereShort="Salty Crew Bonaire", tag="New"),
    dict(id="slip-on", name="Vans Slip-On Checkerboard", brand="Vans", price="$89.95", cat="footwear", img="vans-slipon", packshot=True,
         alt="Vans checkerboard slip-on shoes in red and white", where="Salty Crew Bonaire", whereShort="Salty Crew Bonaire"),
    dict(id="knu-kids", name="Vans Knu Kids", brand="Vans", price="$79.95", cat="footwear kids", img="vans-knu-kids", packshot=True,
         alt="Kids' Vans Knu sneaker in burgundy", where="Salty Crew Bonaire", whereShort="Salty Crew Bonaire"),
    dict(id="kulani", name="Kulani Kinis, new colours", brand="Kulani Kinis", price="", cat="swim", img="lb-30",
         alt="Woman in a neon pink and yellow bikini and shirt leaning on a pink car", where="Beachvibes Playa", whereShort="Beachvibes Playa", tag="Out now",
         note="The new colourways just landed. Ask in store for sizes."),
    dict(id="anuanua", name="Anuanua menswear", brand="Anuanua", price="", cat="tees", img="lb-14",
         alt="Man in a khaki short-sleeve shirt and shorts leaning in a wooden doorway", where="Salty Crew Bonaire", whereShort="Salty Crew Bonaire", tag="New brand",
         note="A new label on the island, only at Salty Crew Bonaire."),
    dict(id="h11", name="H11 Hang Eleven", brand="Hang Eleven", price="", cat="swim tees", img="lb-08",
         alt="Woman holding a surfboard on the beach in a printed long-sleeve swim top", where="Beachvibes Playa", whereShort="Beachvibes Playa", tag="Out now"),
    dict(id="bracelet", name="Make-your-own bracelet", brand="Beachvibes", price="", cat="jewelry", img="jw-bracelets",
         alt="Handmade cord bracelets in many colours on a wooden counter", where="Beachvibes Playa", whereShort="Beachvibes Playa", tag="Handmade",
         note="Choose your colours and style and we make it for you. Design one on the jewelry page."),
]
BRANDS = [
    ("Anuanua", "New this season", "lb-14"), ("At Aloha Jewelry", "Jewelry", "jw-charms"), ("Billabong", "Surf & swim", "lb-20"),
    ("Bracha Jewelry", "Jewelry", "jw-necklace"), ("Bynouck Jewelry", "Jewelry", "jw-handchain"), ("Corkcicle", "Drinkware", "lb-11"),
    ("CUS Boutique", "", "lb-28"), ("Goorin", "Hats", "lb-02"), ("Haarlemmerbruin", "", "lb-15"), ("Hang Eleven", "Surf apparel", "lb-08"),
    ("Hurley", "Surf apparel", "lb-13"), ("Island Tribe", "Sun care", "lb-12"), ("It's Now Cool", "Swimwear", "lb-09"),
    ("Kulani Kinis", "Swimwear", "lb-30"), ("Lemonade The Brand", "", "lb-21"), ("Lotus and Luna", "Jewelry", "jw-beads-star"),
    ("Maaji", "Swimwear", "lb-06"), ("Mystic", "Watersports", "store-sorobon"), ("Phish Phaktory", "", "lb-23"),
    ("Protest", "Boardwear & swim", "lb-26"), ("Reef", "Sandals", "lb-11"), ("RVCA", "Surf & street", "lb-03"),
    ("Salty Crew", "Fishing & surf", "salty-shirt"), ("Vans", "Footwear", "vans-checker"),
]
TICKER = ["RVCA", "Billabong", "Vans", "Salty Crew", "Maaji", "Mystic", "Hurley", "Reef", "Protest", "Hang Eleven", "It's Now Cool",
          "Bynouck Jewelry", "Goorin", "Bracha Jewelry", "Lotus and Luna", "Corkcicle", "Island Tribe", "Phish Phaktory",
          "At Aloha Jewelry", "CUS Boutique", "Lemonade The Brand", "Haarlemmerbruin"]
# brand logo wall, in the order the shop lists them. file=None renders a typeset name (no logo file yet).
LOGOS = [("RVCA", "rvca"), ("Billabong", "billabong"), ("Vans", "vans"), ("Salty Crew", "salty-crew"), ("Maaji", "maaji"),
         ("Mystic", "mystic"), ("Hurley", "hurley"), ("Reef", "reef"), ("Protest", "protest"), ("Hang Eleven", "hang-eleven"),
         ("It's Now Cool", "its-now-cool"), ("Bynouck Jewelry", "bynouck-jewelry"), ("Goorin", "goorin"), ("Bracha Jewelry", None),
         ("Lotus and Luna", "lotus-and-luna"), ("Corkcicle", "corkcicle"), ("Island Tribe", "island-tribe"), ("Phish Phaktory", "phish-phaktory"),
         ("At Aloha Jewelry", "at-aloha-jewelry"), ("CUS Boutique", "cus-boutique"), ("Lemonade The Brand", None), ("Haarlemmerbruin", None)]

def logo_wall():
    import struct
    out = ""
    for name, f in LOGOS:
        if f:
            w, h = struct.unpack(">II", (SITE / "img" / "brands" / f"{f}.png").read_bytes()[16:24])
            ar = w / h; hh = max(22, min(62, (2600 / ar) ** .5)); ww = min(150, hh * ar); hh = ww / ar
            out += f'<li><img src="img/brands/{f}.png" alt="{e(name)}" width="{ww:.0f}" height="{hh:.0f}" loading="lazy"></li>'
        else:
            out += f'<li><span class="logo-type">{e(name)}</span></li>'
    return f'<ul class="logo-wall" aria-label="Brands we carry">{out}</ul>'

# lookbook: (file, set, alt)
LOOK = [
    ("lb-01", "beachvibes", "Woman in a linen shirt and shorts among tropical leaves"),
    ("lb-02", "beachvibes", "Woman in a straw hat sitting on a sea wall"),
    ("lb-04", "beachvibes", "Smiling woman in a rust zip-up on a cliff by the sea"),
    ("lb-13", "salty", "Man in a cream short-sleeve shirt in a garden"),
    ("lb-06", "beachvibes", "Two women in floral swimwear by the sea"),
    ("lb-07", "beachvibes", "Woman in a white linen shirt and shorts under palms"),
    ("lb-15", "salty", "Man in green palm-print boardshorts"),
    ("lb-09", "beachvibes", "Woman with a surfboard in a printed bikini"),
    ("lb-05", "beachvibes", "Three friends lounging in earth-tone beachwear"),
    ("lb-11", "salty beachvibes", "Couple laughing on the beach with drinks"),
    ("lb-12", "beachvibes", "Woman in a blue bikini on a bed eating an ice lolly"),
    ("lb-14", "salty", "Man in a khaki shirt leaning in a wooden doorway"),
    ("lb-16", "beachvibes", "Woman in a tropical long-sleeve swimsuit on the sand"),
    ("salty-truck", "salty", "Man in a Salty Crew tee by a pickup truck at the coast"),
    ("lb-18", "beachvibes", "Woman in a pink swimsuit and patchwork cover-up"),
    ("lb-19", "beachvibes", "Three friends in tees and denim shorts on a wall"),
    ("lb-20", "beachvibes", "Three women in colour-block swimwear under palm trees"),
    ("salty-boys", "salty", "Two friends laughing after a surf"),
    ("lb-21", "beachvibes", "Woman in printed wide-leg trousers on the beach"),
    ("lb-22", "beachvibes", "Friends in tie-dye bikinis and beaded necklaces"),
    ("lb-23", "beachvibes", "Woman in an oversized Vans tee dress"),
    ("salty-shirt", "salty", "Man in a fish-print shirt holding fresh greens"),
    ("lb-24", "beachvibes", "Two women in tropical swim and sarongs"),
    ("lb-25", "beachvibes", "Woman in a pastel bikini on a boat ladder"),
    ("lb-26", "beachvibes", "Woman on a boat deck in blue print swimwear"),
    ("vans-checker", "salty", "Checkerboard Vans resting on a car door"),
    ("lb-27", "beachvibes", "Woman in yellow sunglasses by the pool"),
    ("lb-28", "beachvibes", "Two women in crochet and knit dresses in a street"),
    ("lb-29", "beachvibes", "Woman in a yellow bikini by a washing line"),
    ("lb-30", "beachvibes", "Woman in neon swimwear leaning on a pink car"),
    ("jw-beads-star", "jewelry", "Beaded necklaces with a gold star pendant"),
    ("jw-charms", "jewelry", "Gold charm bracelet with enamel suns"),
    ("jw-earring", "jewelry", "Silver drop earring"),
    ("jw-cuban", "jewelry", "Gold chain bracelets on a tanned wrist"),
    ("jw-handchain", "jewelry", "Delicate gold hand chain"),
    ("jw-necklace", "jewelry", "Layered gold necklaces with a cross pendant"),
    ("lb-17", "beachvibes", "Woman in a patchwork shirt and trousers on stairs"),
    ("lb-10", "beachvibes", "Woman in a lilac shirt and printed bikini"),
]

# ------------------------------------------------------------------ icons
I = {
    "left": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M15 18l-6-6 6-6"/></svg>',
    "right": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M9 18l6-6-6-6"/></svg>',
    "close": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><path d="M6 6l12 12M18 6L6 18"/></svg>',
    "pin": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 21s-7-6.2-7-11.5A7 7 0 0 1 19 9.5C19 14.8 12 21 12 21Z"/><circle cx="12" cy="9.5" r="2.5"/></svg>',
    "phone": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1 1 .4 1.9.7 2.8a2 2 0 0 1-.5 2.1L8 9.9a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.8.7a2 2 0 0 1 1.7 2Z"/></svg>',
    "wa": '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2Zm0 18.2a8.2 8.2 0 0 1-4.2-1.1l-.3-.2-3 .8.8-2.9-.2-.3A8.2 8.2 0 1 1 12 20.2Zm4.5-6.1c-.2-.1-1.5-.7-1.7-.8-.2-.1-.4-.1-.6.1l-.8 1c-.1.2-.3.2-.5.1a6.7 6.7 0 0 1-3.3-2.9c-.3-.4.3-.4.7-1.3.1-.2 0-.3 0-.4l-.8-1.8c-.2-.5-.4-.4-.6-.4h-.5a1 1 0 0 0-.7.3 3 3 0 0 0-.9 2.2 5.2 5.2 0 0 0 1.1 2.7 11.8 11.8 0 0 0 4.5 4c1.7.7 2.3.8 3.2.6.5-.1 1.5-.6 1.7-1.2.2-.6.2-1.1.2-1.2-.1-.1-.3-.2-.5-.3Z"/></svg>',
    "ig": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.5" cy="6.5" r="1" fill="currentColor"/></svg>',
    "fb": '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M14 8.5V6.8c0-.8.5-1 .9-1H17V2.1L14 2c-3.3 0-4 2.4-4 4v2.5H8V12h2v10h4V12h2.7l.4-3.5H14Z"/></svg>',
}

NAV = [("new-in.html", "New in"), ("lookbook.html", "Lookbook"), ("jewelry.html", "Jewelry"), ("brands.html", "Brands"), ("stores.html", "Stores")]

def wa(msg): return f"https://wa.me/{WA}?text=" + html.escape(__import__("urllib.parse").parse.quote(msg))

def head(title, desc, page):
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<meta name="robots" content="noindex, nofollow">
<meta name="theme-color" content="#F4F6F3">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:image" content="img/store-playa.webp">
<link rel="icon" href="img/logo-bv-ink.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Anybody:wdth,wght@50..150,400..900&family=Raleway:ital,wght@0,300..800;1,300..600&family=Spinnaker&display=swap">
<link rel="stylesheet" href="css/site.css?v=46">
<script src="js/site.js?v=16" defer></script>
{ANALYTICS}
</head>
<body data-page="{page}" class="has-hero">
<a class="skip" href="#main">Skip to content</a>
<header class="site-header">
  <div class="wrap header-grid">
    <nav class="nav nav--left" aria-label="Shop">
      {''.join(f'<a href="{h}"{" aria-current=page" if h.startswith(page) else ""}>{t}</a>' for h, t in NAV[:3])}
    </nav>
    <a class="brand" href="index.html" aria-label="Beachvibes Surfshop, home"><img class="logo-ink" src="img/logo-bv-ink.png" alt="" width="60" height="64"><img class="logo-white" src="img/logo-bv-white.png" alt="" width="60" height="64"></a>
    <div class="header-right">
      <nav class="nav" aria-label="Visit">
        {''.join(f'<a href="{h}"{" aria-current=page" if h.startswith(page) else ""}>{t}</a>' for h, t in NAV[3:])}
      </nav>
      <button class="menu-btn" aria-expanded="false" aria-controls="mobile-nav"><i></i><span>Menu</span></button>
    </div>
  </div>
</header>
<nav class="mobile-nav" id="mobile-nav" aria-label="Main">
  <a href="index.html"{" aria-current=page" if page == "index" else ""}>Home</a>
  {''.join(f'<a href="{h}"{" aria-current=page" if h.startswith(page) else ""}>{t}</a>' for h, t in NAV)}
  <div class="mobile-meta">
    <span data-status="playa" data-prefix="Playa"><span data-status-text></span></span>
    <span data-status="salty" data-prefix="Salty Crew"><span data-status-text></span></span>
    <span data-status="sorobon" data-prefix="Sorobon"><span data-status-text></span></span>
  </div>
</nav>
<main id="main">
"""

def foot():
    stores = "".join(f'<div><strong>{s["name"]}</strong>{s["street"]}<br>{s["hours"]}</div>' for s in STORES)
    return f"""</main>
<div class="checker" aria-hidden="true"></div>
<footer class="site-footer">
<svg class="footer-big" viewBox="0 0 1000 132" aria-hidden="true" focusable="false"><text x="12" y="118" textLength="976" lengthAdjust="spacingAndGlyphs">Beachvibes</text></svg>
  <div class="wrap">
    <div class="footer-top">
      <div>
        <div class="footer-logos"><img src="img/logo-bv-white.png" alt="Beachvibes clothing and accessories" width="68" height="72"><img src="img/logo-salty-white.png" alt="Salty Crew Bonaire" width="82" height="46"></div>
        <p class="muted small" style="margin-top:18px;max-width:30ch">Laid-back luxury for the beach, the bar and every stop in between. Three stores on Bonaire.</p>
        <div class="socials">
          <a href="http://instagram.com/BEACHVIBESSURFSHOP" aria-label="Beachvibes on Instagram">{I['ig']}</a>
          <a href="http://www.facebook.com/BEACHVIBESSURFSHOP" aria-label="Beachvibes on Facebook">{I['fb']}</a>
          <a href="http://instagram.com/SALTYCREWBONAIRE" aria-label="Salty Crew Bonaire on Instagram">{I['ig']}</a>
        </div>
      </div>
      <div><h2>Visit</h2><address>{stores}</address></div>
      <div><h2>Shop</h2><ul>{''.join(f'<li><a href="{h}">{t}</a></li>' for h, t in NAV)}</ul></div>
      <div><h2>Talk to us</h2><ul>
        <li><a href="tel:+5997009744">+599 700 9744</a></li>
        <li><a href="https://wa.me/{WA}">WhatsApp the shop</a></li>
        <li><a href="http://instagram.com/BEACHVIBESSURFSHOP">Follow us on Instagram</a></li>
      </ul></div>
    </div>
    <p class="footer-legal">Design concept by Salty Code Studio for Beachvibes Surfshop. This is a preview, not the official Beachvibes website: nothing is sold or booked here. Brand names and logos belong to their owners and show the labels the stores carry. This preview counts visits with privacy-friendly analytics, without cookies. <a href="privacy.html">Privacy</a></p>
    <div class="footer-bottom"><span>© <span data-year>2026</span> Beachvibes Surfshop, Bonaire</span><span>Concept by Salty Code Studio · <a href="privacy.html">Privacy</a></span></div>
  </div>
</footer>
</body>
</html>
"""

def product_card(p):
    data = dict(name=p["name"], brand=p["brand"], price=p["price"], where=p["where"], whereShort=p["whereShort"],
                img=f"img/{p['img']}.webp", alt=p["alt"], packshot=p.get("packshot", False), colors=p.get("colors", []), note=p.get("note", ""))
    tag = p.get("tag")
    tagcls = " product-tag--new-brand" if tag in ("New brand", "Handmade") else ""
    sw = ""
    if p.get("colors"):
        sw = '<ul class="swatches" aria-label="' + str(len(p["colors"])) + ' colours">' + "".join(f'<li style="background:{c[1]}" title="{c[0]}"></li>' for c in p["colors"]) + "</ul>"
    return f"""<article class="product" data-cat="{p['cat']}">
  <button class="product-open" data-product='{e(json.dumps(data))}' aria-label="Quick view: {e(p['name'])}">
    <div class="product-media{' is-packshot' if p.get('packshot') else ''}">{f'<span class="product-tag{tagcls}">{tag}</span>' if tag else ''}<img src="img/{p['img']}.webp" alt="{e(p['alt'])}" loading="lazy" width="640" height="800"></div>
  </button>
  <div class="product-row"><h3>{e(p['name'])}</h3><span class="price">{p['price'] or 'In store'}</span></div>
  <div class="product-row"><p class="where">{e(p['where'])}</p>{sw}</div>
</article>"""

QUICKVIEW = f"""<dialog id="quickview" aria-labelledby="qv-title">
  <button class="icon-btn qv-close" data-close aria-label="Close">{I['close']}</button>
  <div class="qv">
    <div class="qv-media"><img src="" alt=""></div>
    <div class="qv-body">
      <h2 id="qv-title">Product</h2>
      <p data-qv-note class="muted" style="margin:0"></p>
      <dl><dt>Brand</dt><dd data-qv-brand></dd><dt>Price</dt><dd data-qv-price></dd><dt>Find it at</dt><dd data-qv-where></dd></dl>
      <fieldset class="opt-group" data-qv-opts hidden></fieldset>
      <a class="btn btn--wa" data-qv-wa href="#" target="_blank" rel="noopener">{I['wa']}Ask us to put it aside</a>
      <p class="small muted" style="margin:0">We don't ship online. Message the store on WhatsApp and we'll keep it at the counter for you.</p>
    </div>
  </div>
</dialog>"""

def island_map(id_suffix=""):
    pins = ""
    for s in STORES:
        x, y = s["xy"]
        if s["key"] == "playa":
            lx, anchor = x - 22, "end"
        elif s["key"] == "salty":
            lx, anchor = x + 22, "start"
        else:
            lx, anchor = x - 22, "end"
        ly = y + 5 if s["key"] != "salty" else y + 36
        if s["key"] == "playa": ly = y - 26
        label = s["name"].replace("Beachvibes ", "")
        w = len(label) * 8.6 + 20
        bx = lx - w + 10 if anchor == "end" else lx - 10
        pins += f"""<g class="pin" data-store="{s['key']}" tabindex="0" role="button" aria-label="{e(s['name'])}, {e(s['street'])}">
  <circle class="halo" cx="{x}" cy="{y}" r="18"/><circle class="core" cx="{x}" cy="{y}" r="9"/>
  <rect class="label-bg" x="{bx:.0f}" y="{ly - 17}" width="{w:.0f}" height="26" rx="13"/>
  <text class="label" x="{lx}" y="{ly}" text-anchor="{anchor}">{s['n']}  {e(label)}</text></g>"""
    return f"""<figure class="map-figure">
  <svg class="map-svg" viewBox="-20 -10 650 800" role="img" aria-labelledby="map-t{id_suffix} map-d{id_suffix}">
    <title id="map-t{id_suffix}">Map of Bonaire with our three stores</title>
    <desc id="map-d{id_suffix}">Beachvibes Playa and Salty Crew Bonaire sit side by side in Kralendijk on the west coast. Beachvibes Sorobon is on Lac Bay on the east coast, about a 20 minute drive.</desc>
    <path class="reef" d="{ISLAND}"/><path class="reef" d="{KLEIN}"/>
    <path class="land" d="{ISLAND}"/><path class="land" d="{KLEIN}"/>
    <text class="place" x="70" y="40">Washington Slagbaai</text>
    <text class="place" x="232" y="190">Rincon</text>
    <text class="place" x="236" y="470" text-anchor="middle">Klein Bonaire</text>
    <text class="place place--big" x="404" y="414">Kralendijk</text>
    <text class="water" x="548" y="560">Lac Bay</text>
    <text class="place" x="402" y="742" text-anchor="middle">Pekelmeer salt flats</text>
    <text class="water" x="150" y="620">Caribbean Sea</text>
    <path class="route" d="M392 446 C 420 520, 440 560, 486 596"/>
    {pins}
    <g class="scale" transform="translate(20 760)"><line x1="0" y1="0" x2="122" y2="0"/><line x1="0" y1="-5" x2="0" y2="5"/><line x1="122" y1="-5" x2="122" y2="5"/><text x="61" y="-10" text-anchor="middle">5 km</text></g>
    <g transform="translate(590 30)" class="scale"><line x1="0" y1="14" x2="0" y2="-10"/><path d="M-6 -2 0 -14 6 -2Z" fill="#F4F6F3"/><text x="0" y="32" text-anchor="middle">N</text></g>
  </svg>
</figure>"""

def store_cards():
    out = ""
    for s in STORES:
        out += f"""<li class="store-card" data-store="{s['key']}">
  <span class="store-num" aria-hidden="true">{s['n']}</span>
  <h3 class="h3">{s['name']}</h3>
  <p class="meta"><span>{s['street']}, {s['area']}</span><span class="status" data-status="{s['key']}"><span class="dot"></span><span data-status-text>{s['hours']}</span></span></p>
  <div class="actions"><a class="icon-btn" href="{s['maps']}" target="_blank" rel="noopener" aria-label="Directions to {s['name']} in Google Maps">{I['pin']}</a></div>
</li>"""
    return out

def island_section(heading_tag="h2"):
    return f"""<section class="section on-ink on-sea" data-island aria-labelledby="island-h" style="--sec-bg:{pc('lb-26','deep')}">
  <div class="wrap island">
    {island_map()}
    <div>
      <p class="kicker">Three stores, one island</p>
      <{heading_tag} id="island-h" class="display h2">Find us in town or on the lagoon.</{heading_tag}>
      <p class="lede" style="margin:22px 0 32px">Two shops side by side on Kralendijk's shopping street, one on the windsurf beach at Sorobon. Open times update live in Bonaire time.</p>
      <ul class="store-list">{store_cards()}</ul>
      <p class="drive-note muted">Kralendijk to Sorobon is about a 20 minute drive.</p>
    </div>
  </div>
</section>"""

STORE_PHOTO = {"playa": ("store-playa", "Beachvibes Playa: thatched roof, turquoise bench and beach bags by the door"),
               "salty": ("store-front", "Shop window with Beachvibes and Salty Crew signs under a thatched roof"),
               "sorobon": ("store-sorobon", "Tees hanging at the door of the wooden Sorobon beach shop")}
def shop_cards():
    cards = ""
    for s in STORES:
        img, alt = STORE_PHOTO[s["key"]]
        label = "Salty Crew" if s["key"] == "salty" else "Beachvibes"
        cards += f"""<li class="shop" data-store="{s['key']}"><a href="stores.html#{s['key']}">
  <img src="img/{img}.webp" alt="{e(alt)}" loading="lazy" width="900" height="900">
  <span class="shop-label">{label}</span>
  <span class="shop-body"><span class="shop-name">{s['name']}</span><span class="shop-addr">{s['street']}, {s['area']}</span></span>
</a></li>"""
    return f'<ul class="shops">{cards}</ul>'

def three_stores():
    return f"""<section class="stores3" aria-labelledby="stores3-h">
  <div class="stores3-head"><div class="wrap"><h2 id="stores3-h" class="display h2">Three stores on Bonaire.</h2><p class="lede">Two side by side on Kralendijk's shopping street, one on the windsurf beach at Lac Bay.</p></div></div>
  <div class="stores3-body">{shop_cards()}</div>
</section>"""

def signup():
    days = "".join(f"<option>{i}</option>" for i in range(1, 32))
    months = "".join(f"<option>{m}</option>" for m in ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"])
    return f"""<section class="section signup-sec" id="signup" aria-labelledby="signup-h" style="background:{pc('lb-30','soft')}">
  <div class="wrap signup">
    <div class="stack-s">
      <img class="signup-photo" src="img/lb-30.webp" alt="Woman in neon swimwear leaning on a pink car" loading="lazy">
      <h2 id="signup-h" class="display h2">Get on the list.</h2>
      <p class="lede">New arrivals, restocks and the odd island event. A few emails a month, never more.</p>
    </div>
    <form class="form" data-signup novalidate>
      <div class="field"><label for="f-first">First name</label><input id="f-first" name="first" autocomplete="given-name"></div>
      <div class="field"><label for="f-last">Last name</label><input id="f-last" name="last" autocomplete="family-name"></div>
      <div class="field field--full"><label for="f-email">Email</label><input id="f-email" name="email" type="email" autocomplete="email" required aria-describedby="f-email-err"><span class="error" id="f-email-err" data-email-error hidden></span></div>
      <fieldset class="field field--full" style="border:0;padding:0;margin:0"><legend style="font-size:.9rem;font-weight:600;margin-bottom:6px">Birthday <span class="hint">(optional, so we can say hi)</span></legend>
        <div class="bday"><select name="bday-d" aria-label="Day"><option value="">Day</option>{days}</select><select name="bday-m" aria-label="Month"><option value="">Month</option>{months}</select></div>
      </fieldset>
      <div class="field--full"><button class="btn" type="submit">Sign me up</button></div>
    </form>
  </div>
</section>"""

def ticker():
    ul = "".join(f"<li>{e(b)}</li>" for b in TICKER)
    return f"""<div class="ticker" aria-label="Brands we carry"><div class="ticker-track"><ul>{ul}</ul><ul aria-hidden="true">{ul}</ul></div></div>"""

# ------------------------------------------------------------------ pages

import random
def torn_edge(seed=11, fill="var(--salt)"):
    # paper tear: a slow random walk for the big shape plus fine fibre jitter
    r = random.Random(seed); pts = []; x = 0; base = 52.0
    while x <= 1440:
        base += r.uniform(-5, 5); base = max(30, min(72, base))
        y = base + r.uniform(-4, 4) + (r.random() < .08) * r.uniform(-16, -8)
        pts.append(f"{x:.0f},{y:.1f}"); x += r.uniform(5, 16)
    pts.append(f"1440,{base:.1f}")  # finish exactly on the right edge
    return f'<svg class="torn" viewBox="0 0 1440 100" preserveAspectRatio="none" aria-hidden="true"><path fill="{fill}" d="M0,100 L{" L".join(pts)} L1440,100 Z"/></svg>'

LI = {  # line icons
 "store": '<svg viewBox="0 0 48 48" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round" aria-hidden="true"><path d="M6 20 9 8h30l3 12M6 20h36M6 20c0 3 2.5 5 5.5 5S17 23 17 20c0 3 2.5 5 5.5 5h3c3 0 5.5-2 5.5-5 0 3 2.5 5 5.5 5S42 23 42 20M9 25v15h30V25M20 40V31h8v9"/></svg>',
 "tag": '<svg viewBox="0 0 48 48" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round" aria-hidden="true"><path d="M26 6h16v16L22 42 6 26Z"/><circle cx="34" cy="14" r="3"/></svg>',
 "sun": '<svg viewBox="0 0 48 48" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><circle cx="24" cy="24" r="8"/><path d="M24 4v6M24 38v6M4 24h6M38 24h6M9.9 9.9l4.2 4.2M33.9 33.9l4.2 4.2M9.9 38.1l4.2-4.2M33.9 14.1l4.2-4.2"/></svg>',
 "swim": '<svg viewBox="0 0 48 48" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round" stroke-linecap="round" aria-hidden="true"><path d="M14 6v8c0 4 4 6 10 6s10-2 10-6V6M14 14c-4 2-6 6-6 10 0 2 4 4 16 4s16-2 16-4c0-4-2-8-6-10M4 38c4 0 4 3 8 3s4-3 8-3 4 3 8 3 4-3 8-3 4 3 8 3"/></svg>',
 "shoe": '<svg viewBox="0 0 48 48" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round" stroke-linecap="round" aria-hidden="true"><path d="M4 32V16h10c2 5 8 8 14 9l12 3c3 1 4 3 4 5v3H4ZM4 36h40M16 22l3-2M20 25l3-2"/></svg>',
 "beads": '<svg viewBox="0 0 48 48" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><ellipse cx="24" cy="22" rx="16" ry="12"/><circle cx="8" cy="22" r="3" fill="currentColor"/><circle cx="40" cy="22" r="3" fill="currentColor"/><circle cx="24" cy="10" r="3" fill="currentColor"/><circle cx="14" cy="31" r="3" fill="currentColor"/><circle cx="34" cy="31" r="3" fill="currentColor"/><path d="M24 34v4M20 42l4-4 4 4-4 3Z" stroke-linejoin="round"/></svg>',
 "chat": '<svg viewBox="0 0 48 48" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round" aria-hidden="true"><path d="M8 10h32v22H22l-8 7v-7H8Z"/><path d="M16 21h16M16 26h10" stroke-linecap="round"/></svg>',
}

def brush_x(cls=""):
    # hand-painted X: two tapered strokes, roughened with a displacement filter
    return f'''<svg class="brush-x {cls}" viewBox="0 0 200 200" aria-hidden="true" focusable="false"><defs><filter id="rough{cls.replace(' ','')}" x="-10%" y="-10%" width="120%" height="120%"><feTurbulence type="fractalNoise" baseFrequency=".045" numOctaves="3" seed="4"/><feDisplacementMap in="SourceGraphic" scale="9"/></filter></defs>
<g fill="currentColor" filter="url(#rough{cls.replace(' ','')})"><path d="M34 22c8-6 16-4 24 6 34 44 70 92 116 140 6 7 4 15-4 18-9 3-15-1-22-9C108 132 72 90 40 46c-6-9-12-18-6-24Z"/><path d="M172 30c7 5 6 13 0 20-38 42-78 84-124 128-7 6-15 7-20 0-4-6-1-12 6-18 44-44 84-86 118-126 6-7 13-9 20-4Z"/></g></svg>'''

FLAMINGO = '''<svg class="flamingo" viewBox="0 0 110 170" aria-hidden="true" focusable="false"><g fill="currentColor" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round">
<path stroke="none" d="M36 78c10-14 44-16 58-6 9 6 6 17-7 20-16 4-36 2-48-4-5-3-6-6-3-10Z"/><path stroke="none" d="M90 72l17-6-8 14Z"/>
<path fill="none" stroke-width="5.5" d="M40 82c-12-6-15-20-8-32 7-11 14-16 12-28-1-9-10-12-16-7"/>
<circle stroke="none" cx="27" cy="16" r="5.6"/><path stroke="none" d="M22 13c-7 1-10 8-6 14l2-1c-2-5 0-8 5-9Z"/>
<path fill="none" stroke-width="2.4" d="M62 92v70M62 162l-9 3"/><path fill="none" stroke-width="2.4" d="M68 92l5 26-15-5"/></g></svg>'''
CACTUS = '''<svg class="cactus" viewBox="0 0 60 90" aria-hidden="true" focusable="false"><path fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" d="M24 88V18a6 6 0 0 1 12 0v70M24 54H14a4 4 0 0 1-4-4V34M36 44h9a4 4 0 0 0 4-4V26M6 88h48"/></svg>'''

def halftone_island():
    import re
    nums = [float(n) for n in re.findall(r"-?\d+\.?\d*", ISLAND)]
    xs, ys = nums[0::2], nums[1::2]
    x0, y0, x1, y1 = min(xs), min(ys), max(xs), max(ys)
    return f'''<svg class="halftone-island" viewBox="{x0 - 10:.0f} {y0 - 10:.0f} {x1 - x0 + 20:.0f} {y1 - y0 + 20:.0f}" aria-hidden="true" focusable="false"><defs>
<pattern id="dots" width="9" height="9" patternUnits="userSpaceOnUse" patternTransform="rotate(30)"><circle cx="4.5" cy="4.5" r="2.3" fill="currentColor"/></pattern>
<clipPath id="isl"><path d="{ISLAND}"/></clipPath></defs><rect x="{x0 - 10:.0f}" y="{y0 - 10:.0f}" width="{x1 - x0 + 20:.0f}" height="{y1 - y0 + 20:.0f}" fill="url(#dots)" clip-path="url(#isl)"/></svg>'''

def brand_band(label="Brands we carry", reverse=False):
    import struct
    out = ""
    for name, f in LOGOS:
        if f:
            f2 = "billabong-stack" if f == "billabong" else f
            w, h = struct.unpack(">II", (SITE / "img" / "brands" / f"{f2}.png").read_bytes()[16:24])
            ar = w / h; hh = max(26, min(50, (2300 / ar) ** .5)); ww = min(130, hh * ar); hh = ww / ar
            out += f'<li><a href="brands.html"><img src="img/brands/{f2}.png" alt="{e(name)}" width="{ww:.0f}" height="{hh:.0f}" loading="lazy"></a></li>'
        else:
            out += f'<li><a href="brands.html" class="band-type">{e(name)}</a></li>'
    dup = out.replace('<li>', '<li aria-hidden="true">').replace('<a href', '<a tabindex="-1" href')
    return f'<div class="brand-band{" brand-band--rev" if reverse else ""}"><ul class="band-track" aria-label="{label}">{out}{dup}</ul></div>'

def paper_edge(seed=7):
    r = random.Random(seed); pts = ["0,0"]; y = 0
    x = 88.0
    while y < 100:
        x = max(80, min(97, x + r.uniform(-2.2, 2.2))); pts.append(f"{x + r.uniform(-.8, .8):.1f}% {y:.1f}%"); y += r.uniform(1.2, 3.2)
    pts.append(f"{x:.1f}% 100%"); pts.append("0 100%")
    return "polygon(0 0," + ",".join(pts[1:]) + ")"

def page_index():
    order = ["kulani", "anuanua", "h11", "bracelet", "donkey", "knu-skool", "knu-stacked", "slip-on", "knu-kids"]
    rail = "".join(product_card(next(p for p in PRODUCTS if p["id"] == k)) for k in order[:6])
    strip = [("lb-10", "Woman in a lime bikini and white shirt"), ("salty-boys", "Two friends laughing after a surf"), ("lb-07", "Woman in a white linen shirt and shorts"),
             ("lb-20", "Three women in colour-block swimwear under palm trees"), ("salty-shirt", "Man in a fish-print shirt"), ("vans-knu-close", "Vans Knu Skool sneakers up close"), ("lb-11", "Couple laughing on the beach with drinks")]
    pills = "".join(f'<li><a class="pill" href="stores.html#{s["key"]}">{e(s["name"])}</a></li>' for s in STORES)
    return head("Beachvibes Surfshop | Bonaire", "Surf, swim and island wear across three stores on Bonaire: Beachvibes Playa, Salty Crew Bonaire and Beachvibes Sorobon.", "index").replace('<header class="site-header">', '<p class="announce">From the beach to the bar and everywhere you stop between</p>\n<header class="site-header">', 1) + f"""
<section class="hero hero--full hero--duo">
  <div class="hero-duo" aria-hidden="true">
    <img src="img/lb-24.webp" alt="" width="1100" height="1375" fetchpriority="high" style="object-position:50% 30%">
    <img src="img/salty-truck.webp" alt="" width="1000" height="1333" fetchpriority="high" style="object-position:40% 35%">
  </div>
  <div class="hero-shade"></div>
  {brush_x("bx-hero")}
  <div class="wrap hero-inner">
    <h1 class="sr-only">Beachvibes Surfshop and Salty Crew Bonaire, three stores on Bonaire</h1>
    <div class="hero-logo-slot" aria-hidden="true"><img class="hero-logo" src="img/logo-bv-white.png" alt="" width="359" height="383"></div>
  </div>
</section>
{brand_band()}
<section class="dark-sec houses-dark" aria-labelledby="houses-h">
  {brush_x("bx-dark")}
  <div class="wrap">
    <h2 id="houses-h" class="sr-only">Our stores: Beachvibes and Salty Crew Bonaire</h2>
    <div class="store-pills-row"><a class="pills-label" href="stores.html">Our 3 stores <span aria-hidden="true">→</span></a><ul class="store-pills" aria-label="Go to a store">{pills}</ul></div>
    <div class="houses">
      <a class="house" href="stores.html#playa" style="--deep:{pc('lb-20','deep')}">
        <img class="house-bg" src="img/lb-20.webp" alt="" loading="lazy">
        <div class="house-body">
          <img class="house-logo" src="img/logo-bv-white.png" alt="Beachvibes" width="120" height="128" loading="lazy">
          <p>Swim, surf labels, island wear, our own donkey tees and handmade jewelry. For her, for him, for the beach.</p>
          <p class="house-where">Beachvibes Playa, Kralendijk<br>Beachvibes Sorobon, Lac Bay</p>
          <span class="btn btn--glass">Visit Beachvibes</span>
        </div>
      </a>
      <a class="house" href="stores.html#salty" style="--deep:{pc('salty-truck','deep')}">
        <img class="house-bg" src="img/salty-truck.webp" alt="" loading="lazy">
        <div class="house-body">
          <img class="house-logo house-logo--wide" src="img/logo-salty-white.png" alt="Salty Crew" width="200" height="113" loading="lazy">
          <p>Fishing and surf wear from Salty Crew, Vans footwear and Anuanua menswear. Built for days on the water.</p>
          <p class="house-where">Salty Crew Bonaire<br>Kaya L.D. Gerharts 8, Kralendijk</p>
          <span class="btn btn--glass">Visit Salty Crew Bonaire</span>
        </div>
      </a>
    </div>
  </div>
</section>
<section class="vibe" aria-labelledby="vibe-h">
  <div class="wrap vibe-wrap">
    <div class="vibe-art" aria-hidden="true">{halftone_island()}{FLAMINGO}{CACTUS}</div>
    <h2 id="vibe-h" class="vibe-title"><span class="vibe-small">Here to</span> <span class="vibe-big">Catch the vibe.</span></h2>
    <div class="vibe-grid">
      <figure class="vc vc1"><img src="img/lb-02.webp" alt="Woman in a straw hat and bikini sitting on a sea wall" loading="lazy"><figcaption class="vc-brand">Goorin</figcaption></figure>
      <div class="vc vc2"><figure><img src="img/salty-boys.webp" alt="Two friends laughing after a surf" loading="lazy"><figcaption class="vc-brand">Salty Crew</figcaption></figure><a class="vibe-link" href="lookbook.html">Lookbook</a></div>
      <figure class="vc vc3"><img src="img/lb-27.webp" alt="Woman in yellow sunglasses" loading="lazy"><figcaption class="vc-brand">Beachvibes</figcaption></figure>
      <div class="vc vc4"><figure><img src="img/jw-cuban.webp" alt="Hands wearing gold chain bracelets and rings" loading="lazy"><figcaption class="vc-brand">Bynouck Jewelry</figcaption></figure><a class="vibe-link" href="brands.html">Brands</a></div>
    </div>
  </div>
</section>
<section class="section justin" aria-labelledby="new-h">
  <div class="wrap">
    <div class="section-head">
      <div><h2 id="new-h" class="display h2">Just in.</h2><p class="lede">Fresh on the rails this month. Tap anything to see where it is and ask us to hold it.</p></div>
      <div class="rail-controls"><a class="btn btn--ghost" href="new-in.html">All new in</a></div>
    </div>
  </div>
  <div class="justin-grid">{rail}</div>
</section>
{three_stores()}
<section class="section bracelet-sec" aria-labelledby="jw-h">
  {brush_x("bx-mint")}
  <div class="wrap split">
    <div class="split-media"><img src="img/jw-bracelets.webp" alt="Rows of handmade cord bracelets in bright colours on a wooden counter" loading="lazy" width="1000" height="1328"></div>
    <div class="split-body">
      <p class="kicker">Your colours, your bracelet</p>
      <h2 id="jw-h" class="display h2">Handmade at Beachvibes Playa.</h2>
      <p class="lede">Pick a cord, a bead palette and a charm. We make it for you in the shop, and you wear it home.</p>
      <a class="btn" href="jewelry.html">Design yours</a>
    </div>
  </div>
</section>
<section class="photo-strip" aria-label="From the lookbook">
  <ul>{''.join(f'<li><a href="lookbook.html"><img src="img/{f}.webp" alt="{e(a)}" loading="lazy"></a></li>' for f, a in strip)}</ul>
</section>
<div class="checker" aria-hidden="true"></div>
<section class="paper-panel" aria-labelledby="signup-h">
  <img src="img/lb-18.webp" alt="Woman in a pink swimsuit and patchwork flower shirt on a sandy garden path" loading="lazy">
  <div class="paper" style="clip-path:{paper_edge()}"><div class="paper-inner">
    <h2 id="signup-h" class="paper-h">Get on the list.</h2>
    <p class="paper-sub">New arrivals, restocks and the odd island event. A few emails a month, never more.</p>
    <form class="paper-form" id="signup" data-signup novalidate>
      <label class="sr-only" for="f-first">First name</label><input id="f-first" name="first" placeholder="First name" autocomplete="given-name">
      <label class="sr-only" for="f-email">Email</label><input id="f-email" name="email" type="email" placeholder="Email address" autocomplete="email" required aria-describedby="f-email-err">
      <button class="btn" type="submit">Sign me up</button>
      <span class="error" id="f-email-err" data-email-error hidden></span>
      <p class="form-demo">Preview only: this form doesn't send or store anything yet.</p>
    </form>
  </div></div>
</section>
{QUICKVIEW}
""" + foot()

def page_new():
    cats = [("all", "All"), ("footwear", "Footwear"), ("tees", "Tees & tops"), ("swim", "Swim"), ("jewelry", "Jewelry"), ("kids", "Kids")]
    def count(c): return len(PRODUCTS) if c == "all" else sum(c in p["cat"].split() for p in PRODUCTS)
    chips = "".join(f'<li><button class="chip" data-filter="{c}" aria-pressed="{str(c == "all").lower()}">{t}<span class="count">{count(c)}</span></button></li>' for c, t in cats)
    return head("New in | Beachvibes Surfshop", "New arrivals at Beachvibes and Salty Crew Bonaire: Vans, Kulani Kinis, H11, Anuanua and our own Beachvibes tees.", "new-in") + f"""
<section class="page-hero" style="--deep:{pc('hero-newin','deep')}">
  <img class="hero-bg" src="img/hero-newin.webp" alt="" style="object-position:50% 40%" fetchpriority="high">
  <div class="hero-shade"></div>
  <div class="wrap page-hero-inner">
    <p class="crumbs"><a href="index.html">Home</a> / New in</p>
    <h1 class="display h1">New in.</h1>
    <p class="lede">What landed on the island lately. We don't sell online, so message us and we'll keep it at the counter.</p>
  </div>
  {torn_edge(seed=7)}
</section>
<section class="section" style="padding-top:0"><div class="wrap">
  <ul class="filters" data-filters aria-label="Filter by category">{chips}</ul>
  <p class="sr-only" aria-live="polite" data-result-count></p>
  <div class="grid-products">{''.join(product_card(p) for p in PRODUCTS)}</div>
</div></section>
<section class="section on-ink photo-band" style="--sec-bg:{pc('lb-23','deep')}"><img class="band-bg" src="img/lb-23.webp" alt="" loading="lazy"><div class="wrap cta-band">
  <div><h2 class="display h2">Can't see your size?</h2><p class="lede" style="margin-top:16px">Stock moves fast in season. Send us a message and we'll check all three stores for you.</p></div>
  <a class="btn btn--lagoon" href="https://wa.me/{WA}?text={e(__import__('urllib.parse').parse.quote('Hi Beachvibes! Could you check if you have this in my size: '))}" target="_blank" rel="noopener">{I['wa']}Ask on WhatsApp</a>
</div></section>
{QUICKVIEW}
""" + foot()

def page_lookbook():
    PAIRS = [(14, 10), (10, 14), (12, 12), (15, 9), (9, 15), (13, 11), (11, 13)]
    spans = [x for pr in PAIRS * 6 for x in pr]
    tiles = "".join(f'<button data-set="{s}" aria-label="Enlarge: {e(a)}"><img src="img/{f}.webp" alt="{e(a)}" loading="lazy"></button>' for i, (f, s, a) in enumerate(LOOK))
    tabs = [("all", "Everything"), ("beachvibes", "Beachvibes"), ("salty", "Salty Crew Bonaire"), ("jewelry", "Jewelry")]
    tabh = "".join(f'<button class="tab" role="tab" data-set="{k}" aria-selected="{str(k == "all").lower()}" tabindex="{0 if k == "all" else -1}">{t}</button>' for k, t in tabs)
    return head("Lookbook | Beachvibes Surfshop", "The Beachvibes and Salty Crew Bonaire lookbook: swim, surf and island wear for this season.", "lookbook") + f"""
<section class="page-hero" style="--deep:{pc('hero-lookbook','deep')}">
  <img class="hero-bg" src="img/hero-lookbook.webp" alt="" style="object-position:50% 35%" fetchpriority="high">
  <div class="hero-shade"></div>
  <div class="wrap page-hero-inner">
    <p class="crumbs"><a href="index.html">Home</a> / Lookbook</p>
    <h1 class="display h1">Lookbook.</h1>
    <p class="lede">Shot on film, worn on the island. Everything here is on our rails, so ask in store for the piece you like.</p>
  </div>
  {torn_edge(seed=9)}
</section>
<section class="section look-sec" style="padding-top:0"><div class="wrap">
  <div class="look-bar"><div class="tabs" role="tablist" aria-label="Collections">{tabh}</div></div>
</div>
  <div class="masonry masonry--wide">{tiles}</div>
</section>
<dialog class="lightbox" id="lightbox" aria-label="Photo viewer">
  <div class="lb-top"><span data-lb-count class="small"></span><button class="icon-btn" data-close aria-label="Close">{I['close']}</button></div>
  <div class="lb-stage"><img src="" alt=""></div>
  <div class="lb-nav"><button class="icon-btn" data-lb-prev aria-label="Previous photo">{I['left']}</button><button class="icon-btn" data-lb-next aria-label="Next photo">{I['right']}</button></div>
</dialog>
""" + foot()

def page_jewelry():
    cords = [("#0E2A3B", "Reef navy"), ("#F4F6F3", "Salt white"), ("#3CC8B4", "Lagoon"), ("#F27BA6", "Flamingo"), ("#C8A27A", "Sand"), ("#111111", "Black")]
    pals = [("lagoon", "Lagoon"), ("flamingo", "Flamingo"), ("sunset", "Sunset"), ("reef", "Reef"), ("salt", "Salt & gold")]
    palc = {"lagoon": ['#3CC8B4', '#F4F6F3', '#8FE0D3', '#0C766B'], "flamingo": ['#F27BA6', '#FCE6EE', '#F6C343', '#F4F6F3'], "sunset": ['#F6C343', '#F2905A', '#F27BA6', '#B83467'], "reef": ['#0E2A3B', '#3CC8B4', '#F4F6F3', '#5B8FA8'], "salt": ['#F4F6F3', '#E9DCC8', '#D4AF6A', '#FFFFFF']}
    charms = [("none", "No charm", ""), ("star", "Star", '<path d="M0-15 4.4-4.8 15.6-4.6 6.8 2.4 10 13.2 0 6.9-10 13.2-6.8 2.4-15.6-4.6-4.4-4.8Z"/>'),
              ("shell", "Shell", '<path d="M0 14C-9 14-15 6-15-2-15-9-8-15 0-15S15-9 15-2C15 6 9 14 0 14Z"/>'), ("sun", "Sun", '<circle r="8"/><circle r="13" fill="none" stroke-width="2.5" stroke-dasharray="3 4.2"/>'),
              ("wave", "Wave", '<path d="M-15 6C-15-4-7-12 2-12 10-12 15-6 12 0 9 5 2 3 3-2 4-6 9-5 9-2" fill="none" stroke-width="4" stroke-linecap="round"/>'),
              ("donkey", "Donkey", '<path d="M-12 10V-1C-12-6-8-8-3-8H6L8-14 10-8C14-7 15-3 15 0L11 2V10H8V3H-6V10Z"/>')]
    cord_h = "".join(f'<label class="swatch-opt"><input type="radio" name="cord" value="{c}" data-label="{n}" {"checked" if i == 0 else ""}><span style="background:{c}"></span><span class="sr-only">{n}</span></label>' for i, (c, n) in enumerate(cords))
    pal_h = "".join(f'<label class="swatch-opt palette-opt"><input type="radio" name="palette" value="{k}" data-label="{n}" {"checked" if i == 1 else ""}><span>{"".join(f"<i style=background:{c}></i>" for c in palc[k])}<em>{n}</em></span></label>' for i, (k, n) in enumerate(pals))
    ch_h = "".join(f'<label class="swatch-opt charm-opt"><input type="radio" name="charm" value="{k}" data-label="{n}" {"checked" if k == "star" else ""}><span title="{n}">' + (f'<svg viewBox="-18 -18 36 36" fill="#D4AF37" stroke="#D4AF37" aria-hidden="true">{p}</svg>' if p else '<span class="small" style="font-weight:600">None</span>') + f'</span><span class="sr-only">{n}</span></label>' for k, n, p in charms)
    gallery = [("jw-charms", "Gold charm bracelet with enamel suns"), ("jw-beads-star", "Beaded necklaces with a star pendant"), ("jw-handchain", "Delicate gold hand chain"), ("jw-earring", "Silver drop earring")]
    return head("Handmade jewelry | Beachvibes Surfshop", "Design your own bracelet with Beachvibes Playa: choose a cord, bead palette and charm, and we make it for you on Bonaire.", "jewelry") + f"""
<section class="page-hero" style="--deep:{pc('hero-jewelry','deep')}">
  <img class="hero-bg" src="img/hero-jewelry.webp" alt="" style="object-position:50% 50%" fetchpriority="high">
  <div class="hero-shade"></div>
  <div class="wrap page-hero-inner">
    <p class="crumbs"><a href="index.html">Home</a> / Jewelry</p>
    <h1 class="display h1">Make your own.</h1>
    <p class="lede">Choose your favourite colours and style and we'll make it for you at Beachvibes Playa. Try it here first.</p>
  </div>
  {torn_edge(seed=14)}
</section>
<section class="section" style="padding-top:0" aria-label="Bracelet designer"><div class="wrap builder">
  <div class="builder-stage">
    <svg id="bracelet" viewBox="0 0 520 470" role="img" aria-describedby="bracelet-desc">
      <ellipse cx="260" cy="250" rx="200" ry="150" fill="none" id="cord" stroke="#0E2A3B" stroke-width="5"/>
      <g id="beads"></g>
      <g transform="translate(260 412)"><circle id="knot" r="10" fill="#0E2A3B"/><path d="M-6 8-14 42M6 8 14 42" stroke="currentColor" stroke-width="0" /></g>
      <g id="charm" transform="translate(260 440)"></g>
    </svg>
    <p class="sr-only" id="bracelet-desc"></p>
    <p class="stage-note">Preview. Every bracelet is made by hand, so yours will be one of a kind.</p>
  </div>
  <form id="builder" class="builder-form" onsubmit="return false">
    <fieldset style="border:0;padding:0;margin:0"><legend class="step-title"><b>1</b>Cord colour</legend><div class="swatch-opts">{cord_h}</div></fieldset>
    <fieldset style="border:0;padding:0;margin:0"><legend class="step-title"><b>2</b>Bead palette</legend><div class="swatch-opts">{pal_h}</div></fieldset>
    <fieldset style="border:0;padding:0;margin:0"><legend class="step-title"><b>3</b>Charm</legend><div class="swatch-opts">{ch_h}</div>
      <div class="opt-group" style="margin-top:14px">
        <label class="opt"><input type="radio" name="metal" value="gold" data-label="Gold" checked><span><i style="background:#D4AF37"></i>Gold</span></label>
        <label class="opt"><input type="radio" name="metal" value="silver" data-label="Silver"><span><i style="background:#C9CED3"></i>Silver</span></label>
      </div></fieldset>
    <div><label class="step-title" for="size"><b>4</b>Wrist size <span class="muted" data-size-out style="margin-left:auto;font-weight:600">17 cm</span></label>
      <input class="range" id="size" name="size" type="range" min="14" max="22" value="17" step="1"><p class="small muted" style="margin:6px 0 0">Not sure? Measure your wrist with a string and add 1 cm.</p></div>
    <div class="summary" aria-live="polite"><p class="small muted">Your bracelet</p><p data-summary style="font-weight:600"></p>
      <a class="btn btn--wa" data-builder-wa href="#" target="_blank" rel="noopener">{I['wa']}Send my design to the shop</a></div>
  </form>
</div></section>
<section class="section" aria-labelledby="jb-h" style="background:{pc('jw-charms','soft')}"><div class="wrap">
  <div class="section-head"><div><h2 id="jb-h" class="display h2">Also on the counter.</h2><p class="lede">Ready-to-wear pieces from Bynouck, Bracha, At Aloha and Lotus and Luna.</p></div><a class="btn btn--ghost" href="brands.html">All brands</a></div>
  <div class="grid-products">{''.join(f'<figure style="margin:0" class="product"><div class="product-media"><img src="img/{f}.webp" alt="{a}" loading="lazy"></div></figure>' for f, a in gallery)}</div>
</div></section>
""" + foot()

def page_brands():
    half = (len(BRANDS) + 1) // 2
    def col(items):
        return '<ul class="az-list">' + "".join(f'<li data-img="img/{im}.webp" data-name="{e(n)}" tabindex="0"><div class="az-item"><span class="name">{e(n)}</span><span class="tag">{e(t)}</span></div></li>' for n, t, im in items) + "</ul>"
    return head("Brands | Beachvibes Surfshop", "The 24 brands we carry at Beachvibes and Salty Crew Bonaire, from RVCA and Billabong to Vans, Salty Crew and Maaji.", "brands") + f"""
<section class="page-hero" style="--deep:{pc('hero-brands','deep')}">
  <img class="hero-bg" src="img/hero-brands.webp" alt="" style="object-position:50% 30%" fetchpriority="high">
  <div class="hero-shade"></div>
  <div class="wrap page-hero-inner">
    <p class="crumbs"><a href="index.html">Home</a> / Brands</p>
    <h1 class="display h1">24 brands.</h1>
    <p class="lede">From A to Z: surf labels, swim specialists and small jewelry makers, picked for island life.</p>
  </div>
  {torn_edge(seed=18)}
</section>
<section class="section" style="padding-top:0"><div class="wrap az">
  <div>{col(BRANDS)}</div>
  <figure class="az-preview" style="margin:0"><img src="img/{BRANDS[-1][2]}.webp" alt="" ><figcaption>{BRANDS[-1][0]}</figcaption></figure>
</div></section>
""" + foot()

def page_stores():
    DAYN = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
    blocks = ""
    for s in STORES:
        val = lambda d: "Closed" if not s["days"][d] else f"{s['days'][d][0]}:00 – {s['days'][d][1]}:00"
        groups = []
        for d in [1, 2, 3, 4, 5, 6, 0]:
            if groups and groups[-1][1] == val(d): groups[-1][0].append(d)
            else: groups.append(([d], val(d)))
        def lab(ds):
            if len(ds) == 7: return "Every day"
            return DAYN[ds[0]] if len(ds) == 1 else f"{DAYN[ds[0]]} – {DAYN[ds[-1]]}"
        rows = "".join(f'<tr data-days="{" ".join(map(str, ds))}"><th scope="row">{lab(ds)}</th><td>{v}</td></tr>' for ds, v in groups)
        p = s["photos"]
        blocks += f"""<article class="store-block" id="{s['key']}" aria-labelledby="{s['key']}-h">
  <div class="store-photos">
    <img class="tall" src="img/{p[0]}.webp" alt="{e(s['name'])} store" loading="lazy">
    <img class="sq" src="img/{p[1]}.webp" alt="" loading="lazy"><img class="sq" src="img/{p[2]}.webp" alt="" loading="lazy">
  </div>
  <div class="store-info">
    <h2 id="{s['key']}-h" class="display h2">{s['name'].replace('Beachvibes ', 'Beachvibes<br>')}</h2>
    <p class="status-line" data-status="{s['key']}"><span class="dot"></span><span data-status-text>{s['hours']}</span></p>
    <p class="muted" style="margin:0">{s['blurb']}</p>
    <address class="addr">{s['street']}<br>{s['area']}, Bonaire</address>
    <table class="hours"><caption class="sr-only">Opening hours, {e(s['name'])}</caption><tbody>{rows}</tbody></table>
    <ul class="find-here" aria-label="What you'll find here">{''.join(f'<li>{e(x)}</li>' for x in s['find'])}</ul>
    <div class="store-actions">
      <a class="btn" href="{s['maps']}" target="_blank" rel="noopener">{I['pin']}Get directions</a>
      <a class="btn btn--ghost" href="tel:+5997009744">{I['phone']}Call</a>
    </div>
  </div>
</article>"""
    faqs = [
        ("Which currency do you take?", "Prices are in US dollars, Bonaire's currency."),
        ("I'm on a cruise. How far are you from the pier?", "Beachvibes Playa and Salty Crew Bonaire are on Kralendijk's main shopping street, a few minutes' walk from the cruise pier."),
        ("Can you put something aside for me?", "Yes. Send us a WhatsApp message with what you'd like and which store you'll visit, and we'll keep it at the counter."),
        ("Do you ship online orders?", "Not at the moment. Everything is sold in our three stores on Bonaire."),
        ("Is Sorobon open on Sundays?", "Yes. Beachvibes Sorobon is open every day from 10:00 to 17:00. Playa and Salty Crew are closed on Sundays."),
        ("How do I order a handmade bracelet?", "Design it on our jewelry page and send it via WhatsApp, or pick your colours at the counter in Beachvibes Playa."),
    ]
    faq_h = "".join(f"<details><summary>{q}</summary><p>{a}</p></details>" for q, a in faqs)
    return head("Our stores | Beachvibes Surfshop", "Visit Beachvibes Playa and Salty Crew Bonaire in Kralendijk, and Beachvibes Sorobon at Lac Bay. Opening hours, directions and what you'll find.", "stores") + f"""
<section class="page-hero" style="--deep:{pc('store-front-xl','deep')}">
  <img class="hero-bg" src="img/store-front-xl.webp" alt="" style="object-position:50% 55%" fetchpriority="high">
  <div class="hero-shade"></div>
  <div class="wrap page-hero-inner">
    <p class="crumbs"><a href="index.html">Home</a> / Stores</p>
    <h1 class="display h1">Come say hi.</h1>
    <p class="lede">Laid-back luxury, clothing and goods to take you from the beach to the bar and everywhere in between.</p>
  </div>
  {torn_edge(seed=12)}
</section>
<section class="stores-first" aria-label="Our three stores">{shop_cards()}</section>
{island_section()}
<div class="wrap">{blocks}</div>
<section class="section" aria-labelledby="faq-h" style="background:{pc('store-playa','mid')}"><div class="wrap">
  <h2 id="faq-h" class="display h2" style="margin-bottom:28px">Good to know.</h2>
  <div class="faq">{faq_h}</div>
</div></section>
""" + foot()


def page_privacy():
    return head("Privacy | Beachvibes preview", "How this Beachvibes website preview handles visit data.", "privacy").replace('class="has-hero"', 'class="no-hero"', 1) + """
<section class="section legal" aria-labelledby="pv-h"><div class="wrap legal-wrap">
  <h1 id="pv-h" class="display h2">Privacy.</h1>
  <p class="lede">This website is a design preview made by Salty Code Studio for Beachvibes Surfshop. It is not the official Beachvibes website and nothing is sold here.</p>

  <h2>Who is responsible</h2>
  <p>Salty Code Studio is responsible for the data collected on this preview. Questions or requests: <a href="mailto:info@saltycodestudio.com">info@saltycodestudio.com</a>.</p>

  <h2>What we collect, and why</h2>
  <p>We use PostHog, an analytics service with servers in the EU, to see how the preview is used: which pages are opened, for how long, the approximate country and city, the type of device and browser, and the page you came from. We use this to follow up on the design and improve it. We do not store your IP address.</p>
  <p>If you opened a personal link (one ending in <code>?for=</code> and a name), visits are linked to that name, so we know the person we sent it to has seen the preview. We tell you this when the link opens.</p>
  <p>Our legal basis is legitimate interest: presenting and improving a design proposal.</p>

  <h2>No cookies, no recordings</h2>
  <p>This preview sets no cookies and stores nothing on your device for analytics. We do not record sessions. The sign-up form is a demo and sends nothing.</p>

  <h2>How long we keep it</h2>
  <p>Visit data is kept for as long as the design project runs and deleted within 12 months.</p>

  <h2>Your choices and rights</h2>
  <p>If your browser sends a Do Not Track or Global Privacy Control signal, nothing is counted. You can also switch analytics off for this browser:</p>
  <p><button class="btn" type="button" data-optout>Turn off analytics</button> <span class="small" data-optout-state role="status"></span></p>
  <p>You can ask us to see, correct or delete data about you, or object to its use, by emailing <a href="mailto:info@saltycodestudio.com">info@saltycodestudio.com</a>. You can also complain to your data protection authority.</p>

  <h2>Brands and photos</h2>
  <p>Brand names and logos belong to their owners. They are shown only to illustrate the labels Beachvibes and Salty Crew Bonaire carry. Photos are shown only to preview the design and remain the property of their owners.</p>
</div></section>
<script>
(function () {
  var b = document.querySelector('[data-optout]'), s = document.querySelector('[data-optout-state]');
  function show() { var off = false; try { off = localStorage.getItem('bv-optout') === '1'; } catch (e) {} b.textContent = off ? 'Turn analytics back on' : 'Turn off analytics'; s.textContent = off ? 'Analytics is off in this browser.' : ''; }
  b.addEventListener('click', function () { try { var off = localStorage.getItem('bv-optout') === '1'; if (off) localStorage.removeItem('bv-optout'); else { localStorage.setItem('bv-optout', '1'); if (window.posthog && posthog.opt_out_capturing) posthog.opt_out_capturing(); } } catch (e) {} show(); });
  show();
})();
</script>
""" + foot()

PAGES = {"index.html": page_index, "new-in.html": page_new, "lookbook.html": page_lookbook, "jewelry.html": page_jewelry, "brands.html": page_brands, "stores.html": page_stores, "privacy.html": page_privacy}
for name, fn in PAGES.items():
    (SITE / name).write_text(fn(), encoding="utf-8")
(SITE / "robots.txt").write_text("User-agent: *\nDisallow: /\n")
print("built", ", ".join(PAGES))
