#!/usr/bin/env python3
"""Build the static EveryoneCanShop site into docs/ (GitHub Pages). Content lives in content.py."""
import html, pathlib, shutil
from content import LANGS, T

ROOT = pathlib.Path(__file__).parent
OUT = ROOT / "docs"
BASE = "https://everyonecanshop.com"
EMAIL = "ivan@everyonecanshop.com"


def path_for(lang):
    return "/" if lang == "en" else f"/{lang}/"


def esc(s):
    return html.escape(s, quote=True)


ICONS = {
    "keyboard": '<path d="M3 6h18v12H3z" fill="none" stroke="#0b5f5f" stroke-width="2" rx="2"/><path d="M6 10h2M10 10h2M14 10h2M18 10h0M7 14h10" stroke="#0b5f5f" stroke-width="2" stroke-linecap="round"/>',
    "voice": '<path d="M4 9v6h4l5 4V5L8 9z" fill="none" stroke="#0b5f5f" stroke-width="2" stroke-linejoin="round"/><path d="M16 9a4 4 0 0 1 0 6M18.5 6.5a8 8 0 0 1 0 11" fill="none" stroke="#0b5f5f" stroke-width="2" stroke-linecap="round"/>',
    "contrast": '<circle cx="12" cy="12" r="8" fill="none" stroke="#0b5f5f" stroke-width="2"/><path d="M12 4a8 8 0 0 1 0 16z" fill="#0b5f5f"/>',
    "form": '<rect x="4" y="4" width="16" height="16" rx="2" fill="none" stroke="#0b5f5f" stroke-width="2"/><path d="M8 9h8M8 13h8M8 17h4" stroke="#0b5f5f" stroke-width="2" stroke-linecap="round"/>',
    "doc": '<path d="M7 3h7l4 4v14H7z" fill="none" stroke="#0b5f5f" stroke-width="2" stroke-linejoin="round"/><path d="M10 12l2 2 4-4" fill="none" stroke="#0b5f5f" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>',
    "mobile": '<rect x="7" y="3" width="10" height="18" rx="2" fill="none" stroke="#0b5f5f" stroke-width="2"/><path d="M11 18h2" stroke="#0b5f5f" stroke-width="2" stroke-linecap="round"/>',
}

LOGO = ('<svg class="logo-mark" viewBox="0 0 32 32" aria-hidden="true" focusable="false">'
        '<rect x="1" y="1" width="30" height="30" rx="9" fill="#13212c"/>'
        '<path d="M8 11h3l2.2 9h7.6l1.7-6.5H12" fill="none" stroke="#fff" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/>'
        '<circle cx="14" cy="24" r="1.6" fill="#ffbf47"/><circle cx="20" cy="24" r="1.6" fill="#ffbf47"/></svg>')


def hero_svg(t):
    return f'''<svg viewBox="0 0 440 380" role="img" aria-labelledby="hero-title">
<title id="hero-title">{esc(t["hero_img_alt"])}</title>
<rect x="20" y="20" width="400" height="340" rx="22" fill="#fff" stroke="#e3ded2" stroke-width="2"/>
<rect x="44" y="44" width="160" height="190" rx="14" fill="#eef5f3"/>
<path d="M92 200h64l-8 26h-48z" fill="#0b5f5f"/><path d="M124 196c-24-30-30-62-10-92 4 30 18 54 10 92z" fill="#4c9a7a"/>
<path d="M124 196c20-24 36-40 46-70-20 14-38 34-46 70z" fill="#6bb391"/>
<rect x="228" y="56" width="168" height="16" rx="8" fill="#13212c"/>
<rect x="228" y="84" width="120" height="12" rx="6" fill="#c9c3b6"/>
<text x="228" y="140" font-family="-apple-system,Segoe UI,Arial,sans-serif" font-size="30" font-weight="800" fill="#13212c">€ 24,90</text>
<rect x="228" y="160" width="40" height="40" rx="10" fill="#fff" stroke="#c9c3b6" stroke-width="2"/>
<text x="248" y="186" text-anchor="middle" font-family="-apple-system,Arial,sans-serif" font-size="18" fill="#13212c">1</text>
<rect x="276" y="152" width="128" height="56" rx="16" fill="none" stroke="#13212c" stroke-width="5"/>
<rect x="281" y="157" width="118" height="46" rx="12" fill="none" stroke="#ffbf47" stroke-width="6"/>
<rect x="286" y="162" width="108" height="36" rx="9" fill="#0b5f5f"/>
<text x="340" y="186" text-anchor="middle" font-family="-apple-system,Segoe UI,Arial,sans-serif" font-size="14" font-weight="700" fill="#fff">{esc(t["hero_img_btn"])}</text>
<rect x="44" y="262" width="352" height="74" rx="14" fill="#fbf9f4" stroke="#e3ded2" stroke-width="2"/>
<rect x="62" y="280" width="64" height="38" rx="8" fill="#fff" stroke="#13212c" stroke-width="2.5"/>
<text x="94" y="305" text-anchor="middle" font-family="-apple-system,Arial,sans-serif" font-size="16" font-weight="800" fill="#13212c">Tab</text>
<text x="142" y="296" font-family="-apple-system,Segoe UI,Arial,sans-serif" font-size="15" font-weight="700" fill="#13212c">{esc(t["hero_img_cap1"])}</text>
<text x="142" y="318" font-family="-apple-system,Segoe UI,Arial,sans-serif" font-size="14" fill="#3c4b57">{esc(t["hero_img_cap2"])}</text>
</svg>'''


def icon(name):
    return f'<div class="icon" aria-hidden="true"><svg viewBox="0 0 24 24" focusable="false">{ICONS[name]}</svg></div>'


def page(lang):
    t = T[lang]
    mail = f'mailto:{EMAIL}?subject={esc(t["mail_subject"])}'
    alts = "\n".join(f'<link rel="alternate" hreflang="{l}" href="{BASE}{path_for(l)}">' for l in LANGS)
    alts += f'\n<link rel="alternate" hreflang="x-default" href="{BASE}/">'
    langnav = "".join(
        f'<li><a href="{path_for(l)}" hreflang="{l}" lang="{l}"' + (' aria-current="page"' if l == lang else "") +
        f'><span aria-hidden="true">{l.upper()}</span><span class="sr">{esc(T[l]["lang_name"])}</span></a></li>' for l in LANGS)
    checks = "".join(f'<div class="card">{icon(i)}<h3>{esc(h)}</h3><p>{esc(p)}</p></div>' for i, h, p in t["checks"])
    stats = "".join(f'<div class="card"><div class="stat">{esc(n)}</div><p>{esc(p)}</p><p class="src"><a href="{u}">{esc(s)}</a></p></div>'
                    for n, p, s, u in t["stats"])
    prices = ""
    for i, (name, price, per, items, featured) in enumerate(t["packages"]):
        lis = "".join(f"<li>{esc(x)}</li>" for x in items)
        badge = f'<span class="badge">{esc(t["popular"])}</span>' if featured else ""
        prices += (f'<div class="card price-card{" featured" if featured else ""}">{badge}<h3>{esc(name)}</h3>'
                   f'<p class="price">{esc(price)} <small>{esc(per)}</small></p><ul>{lis}</ul></div>')
    steps = "".join(f"<li><h3>{esc(h)}</h3><p>{esc(p)}</p></li>" for h, p in t["steps"])
    faq = "".join(f"<details><summary>{esc(q)}</summary><p>{a}</p></details>" for q, a in t["faq"])
    return f'''<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(t["title"])}</title>
<meta name="description" content="{esc(t["description"])}">
<link rel="canonical" href="{BASE}{path_for(lang)}">
{alts}
<meta property="og:title" content="{esc(t["title"])}">
<meta property="og:description" content="{esc(t["description"])}">
<meta property="og:url" content="{BASE}{path_for(lang)}">
<meta property="og:type" content="website">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="/style.css">
<style>.sr{{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap}}</style>
</head>
<body>
<a class="skip" href="#main">{esc(t["skip"])}</a>
<header class="site"><div class="wrap">
<a class="logo" href="{path_for(lang)}">{LOGO}<span>EveryoneCanShop</span></a>
<nav class="lang" aria-label="{esc(t["lang_label"])}"><ul>{langnav}</ul></nav>
</div></header>
<main id="main">
<section class="hero" aria-labelledby="h1"><div class="wrap">
<div>
<span class="eyebrow">{esc(t["eyebrow"])}</span>
<h1 id="h1">{esc(t["h1"])}</h1>
<p class="lead">{esc(t["lead"])}</p>
<div class="cta-row"><a class="btn btn-primary" href="{mail}">{esc(t["cta"])}</a><a class="btn btn-ghost" href="#packages">{esc(t["cta2"])}</a></div>
<p class="note">{esc(t["cta_note"])}</p>
</div>
<div>{hero_svg(t)}</div>
</div></section>

<section class="alt" aria-labelledby="why"><div class="wrap">
<h2 id="why">{esc(t["why_h"])}</h2>
<p class="section-lead">{esc(t["why_p"])}</p>
<div class="grid-3">{stats}</div>
</div></section>

<section aria-labelledby="what"><div class="wrap">
<h2 id="what">{esc(t["what_h"])}</h2>
<p class="section-lead">{esc(t["what_p"])}</p>
<div class="grid-3">{checks}</div>
</div></section>

<section class="alt" id="packages" aria-labelledby="pk"><div class="wrap">
<h2 id="pk">{esc(t["pk_h"])}</h2>
<p class="section-lead">{esc(t["pk_p"])}</p>
<div class="grid-4">{prices}</div>
<p class="note">{esc(t["pk_note"])}</p>
</div></section>

<section aria-labelledby="how"><div class="wrap">
<h2 id="how">{esc(t["how_h"])}</h2>
<ol class="steps">{steps}</ol>
</div></section>

<section class="alt" aria-labelledby="who"><div class="wrap about">
<img src="/ivan.jpg" alt="{esc(t["photo_alt"])}" width="140" height="140">
<div><h2 id="who">{esc(t["who_h"])}</h2>{"".join(f"<p>{esc(p)}</p>" for p in t["who_p"])}</div>
</div></section>

<section aria-labelledby="faqh"><div class="wrap">
<h2 id="faqh">{esc(t["faq_h"])}</h2>
{faq}
</div></section>

<section aria-labelledby="fin"><div class="wrap"><div class="final">
<div><h2 id="fin">{esc(t["final_h"])}</h2><p>{esc(t["final_p"])}</p></div>
<a class="btn btn-primary" href="{mail}">{esc(t["cta"])}</a>
</div></div></section>
</main>
<footer class="site"><div class="wrap">
<div><p><strong>EveryoneCanShop</strong></p><p>{esc(t["footer_op"])}</p><p><a href="mailto:{EMAIL}">{EMAIL}</a></p></div>
<div><p>{esc(t["footer_privacy"])}</p><p>{esc(t["footer_a11y"])}</p></div>
</div></footer>
</body>
</html>
'''


def main():
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir()
    for lang in LANGS:
        d = OUT if lang == "en" else OUT / lang
        d.mkdir(exist_ok=True)
        (d / "index.html").write_text(page(lang))
    shutil.copy(ROOT / "src/style.css", OUT / "style.css")
    for f in (ROOT / "src").glob("*"):
        if f.suffix in (".svg", ".jpg", ".png"):
            shutil.copy(f, OUT / f.name)
    (OUT / "CNAME").write_text("everyonecanshop.com\n")
    (OUT / ".nojekyll").write_text("")
    (OUT / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {BASE}/sitemap.xml\n")
    urls = "".join(f"<url><loc>{BASE}{path_for(l)}</loc></url>" for l in LANGS)
    (OUT / "sitemap.xml").write_text(f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>\n')
    print("built", [path_for(l) for l in LANGS])


if __name__ == "__main__":
    main()
