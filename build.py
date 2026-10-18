#!/usr/bin/env python3
"""Build the static EveryoneCanShop site into docs/ (GitHub Pages).

Home page copy lives in content.py, the plain-language law guide (/eaa/) in guide.py.
"""
import html, json, pathlib, re, shutil
from urllib.parse import quote
from content import EAA, EU_DISABILITY, LANGS, LINKEDIN, T
from guide import G

ROOT = pathlib.Path(__file__).parent
OUT = ROOT / "docs"
BASE = "https://everyonecanshop.com"
EMAIL = "ivan@everyonecanshop.com"


def path_for(lang, page=""):
    base = "/" if lang == "en" else f"/{lang}/"
    return base + (f"{page}/" if page else "")


def esc(s):
    return html.escape(s, quote=True)


def mailto(subject):
    return f"mailto:{EMAIL}?subject=" + esc(quote(subject))


def svg(body, cls="ico", box="0 0 24 24"):
    return f'<svg class="{cls}" viewBox="{box}" aria-hidden="true" focusable="false">{body}</svg>'


S = 'fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"'
ICONS = {
    "keyboard": f'<rect x="3" y="6" width="18" height="12" rx="2" {S}/><path d="M7 10h.01M11 10h.01M15 10h.01M7 14h10" {S}/>',
    "voice": f'<path d="M4 9v6h4l5 4V5L8 9z" {S}/><path d="M16 9a4 4 0 0 1 0 6M18.5 6.5a8 8 0 0 1 0 11" {S}/>',
    "contrast": f'<circle cx="12" cy="12" r="8" {S}/><path d="M12 4a8 8 0 0 1 0 16z" fill="currentColor"/>',
    "form": f'<rect x="4" y="4" width="16" height="16" rx="2" {S}/><path d="M8 9h8M8 13h8M8 17h4" {S}/>',
    "doc": f'<path d="M7 3h7l4 4v14H7z" {S}/><path d="M10 13l2 2 4-4" {S}/>',
    "mobile": f'<rect x="7" y="3" width="10" height="18" rx="2" {S}/><path d="M11 18h2" {S}/>',
    "check": f'<path d="M5 12.5l4.5 4.5L19 7.5" {S}/>',
    "cross": f'<path d="M7 7l10 10M17 7L7 17" {S}/>',
    "clock": f'<circle cx="12" cy="12" r="8.5" {S}/><path d="M12 7.5V12l3 2" {S}/>',
    "shield": f'<path d="M12 3l7 3v5c0 4.5-3 8.3-7 10-4-1.7-7-5.5-7-10V6z" {S}/><path d="M9 12l2 2 4-4" {S}/>',
    "lock": f'<rect x="5" y="10.5" width="14" height="10" rx="2" {S}/><path d="M8 10.5V8a4 4 0 0 1 8 0v2.5" {S}/>',
    "users": f'<circle cx="9" cy="9" r="3" {S}/><path d="M3.5 19c.8-3 3-4.5 5.5-4.5s4.7 1.5 5.5 4.5M15.5 6.2a3 3 0 0 1 0 5.6M17 14.8c1.8.5 3 1.9 3.5 4.2" {S}/>',
    "tag": f'<path d="M3.5 12.5V4.5h8l9 9-8 8z" {S}/><circle cx="8" cy="9" r="1.3" fill="currentColor"/>',
    "scale": f'<path d="M12 4v16M7 20h10M5 7h14M5 7l-2.5 6a3 3 0 0 0 5 0zM19 7l-2.5 6a3 3 0 0 0 5 0z" {S}/>',
    "arrow": f'<path d="M5 12h14M13 6l6 6-6 6" {S}/>',
    "down": f'<path d="M12 5v14M6 13l6 6 6-6" {S}/>',
    "book": f'<path d="M4 5.5A2.5 2.5 0 0 1 6.5 3H20v15H6.5A2.5 2.5 0 0 0 4 20.5z" {S}/><path d="M4 20.5A2.5 2.5 0 0 0 6.5 23H20v-5" {S}/>',
    "info": f'<circle cx="12" cy="12" r="9" {S}/><path d="M12 11v6M12 7.5h.01" {S}/>',
    "flag": f'<path d="M5 21V4M5 4h11l-2 4 2 4H5" {S}/>',
    "pause": '<rect x="6" y="5" width="4" height="14" rx="1" fill="currentColor"/><rect x="14" y="5" width="4" height="14" rx="1" fill="currentColor"/>',
    "play": '<path d="M7 5l12 7-12 7z" fill="currentColor"/>',
    "cart": f'<path d="M3 4h2.5l2.2 10.5h10.6l2-7.5H7" {S}/><circle cx="10" cy="19" r="1.5" fill="currentColor"/><circle cx="17" cy="19" r="1.5" fill="currentColor"/>',
    "person": '<circle cx="12" cy="7" r="3.6" fill="currentColor"/><path d="M5 21c.6-4.6 3.4-7.2 7-7.2s6.4 2.6 7 7.2z" fill="currentColor"/>',
    "linkedin": '<path fill="currentColor" d="M4.98 3.5A2.5 2.5 0 1 1 5 8.5a2.5 2.5 0 0 1-.02-5zM3 9.75h4V21H3zM9.5 9.75h3.8v1.6h.06c.53-1 1.83-2.05 3.77-2.05 4.03 0 4.77 2.6 4.77 6V21h-4v-5.1c0-1.22-.02-2.8-1.7-2.8-1.72 0-1.98 1.33-1.98 2.7V21h-4z"/>',
}
TRUST_ICONS = ["scale", "lock", "users", "tag"]
POINT_ICONS = ["users", "shield", "check"]

LOGO = ('<svg class="logo-mark" viewBox="0 0 32 32" aria-hidden="true" focusable="false">'
        '<rect x="1" y="1" width="30" height="30" rx="9" fill="#13212c"/>'
        '<path d="M8 11h3l2.2 9h7.6l1.7-6.5H12" fill="none" stroke="#fff" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/>'
        '<circle cx="14" cy="24" r="1.6" fill="#ffbf47"/><circle cx="20" cy="24" r="1.6" fill="#ffbf47"/></svg>')
SWATCHES = ["#5b6b3a", "#2c5d86", "#d8c6a3"]


def icon(name, cls="ico"):
    return svg(ICONS[name], cls)


def picture(name, alt, cls=""):
    """Illustration from src/ill (800x800): webp with jpg fallback, lazy (all are below the fold)."""
    c = f' class="{cls}"' if cls else ""
    return (f'<picture{c}><source srcset="/ill/{name}.webp" type="image/webp">'
            f'<img src="/ill/{name}.jpg" width="800" height="800" alt="{esc(alt)}" loading="lazy" decoding="async"></picture>')


def people(cls="people"):
    """'1 in 4' graphic: four people, one highlighted (decorative)."""
    return f'<span class="{cls}" aria-hidden="true">' + "".join(
        icon("person", "ico pp" + (" pp-on" if i == 0 else "")) for i in range(4)) + "</span>"


# ---------------------------------------------------------------- shared page parts

def head(lang, title, desc, page):
    alts = "\n".join(f'<link rel="alternate" hreflang="{l}" href="{BASE}{path_for(l, page)}">' for l in LANGS)
    alts += f'\n<link rel="alternate" hreflang="x-default" href="{BASE}{path_for("en", page)}">'
    return f'''<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<meta name="color-scheme" content="light">
<meta name="theme-color" content="#fbf9f4">
<link rel="canonical" href="{BASE}{path_for(lang, page)}">
{alts}
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{BASE}{path_for(lang, page)}">
<meta property="og:type" content="website">
<meta property="og:image" content="{BASE}/ivan.jpg">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="/style.css">
<script>document.documentElement.className+=" js";</script>
</head>'''


def header(lang, t, page):
    home = path_for(lang)
    pre = "" if not page else home
    nav = "".join(f'<li><a href="{pre}{href}">{esc(label)}</a></li>' for href, label in t["nav"])
    langnav = "".join(
        f'<li><a href="{path_for(l, page)}" hreflang="{l}" lang="{l}"' + (' aria-current="page"' if l == lang else "") +
        f'><span aria-hidden="true">{l.upper()}</span><span class="sr">{esc(T[l]["lang_name"])}</span></a></li>' for l in LANGS)
    return f'''<body>
<a class="skip" href="#main">{esc(t["skip"])}</a>
<header class="site"><div class="wrap">
<a class="logo" href="{home}">{LOGO}<span>EveryoneCanShop</span></a>
<nav class="primary" aria-label="{esc(t["nav_label"])}"><ul>{nav}</ul></nav>
<div class="head-right">
<nav class="lang" aria-label="{esc(t["lang_label"])}"><ul>{langnav}</ul></nav>
<a class="btn btn-accent btn-sm head-cta" href="{pre}#check">{esc(t["header_cta"])}</a>
</div>
</div></header>'''


def footer(lang, t):
    return f'''<footer class="site"><div class="wrap">
<div class="foot-brand"><a class="logo" href="{path_for(lang)}">{LOGO}<span>EveryoneCanShop</span></a><p>{esc(t["footer_op"])}</p></div>
<div><h2 class="foot-h">{esc(t["footer_contact"])}</h2>
<ul class="foot-list"><li><a href="mailto:{EMAIL}">{EMAIL}</a></li><li><a href="{LINKEDIN}" rel="noopener">LinkedIn</a></li><li><a href="{path_for(lang, "eaa")}">{esc(t["footer_guide"])}</a></li></ul></div>
<div class="foot-small"><p>{esc(t["footer_privacy"])}</p><p>{esc(t["footer_a11y"])}</p></div>
</div></footer>
@@SCRIPT@@
</body>
</html>
'''


def finish(lang, doc):
    if lang == "fr":
        doc = fr_typo(doc)
    doc = doc.replace("@@SCRIPT@@", SCRIPT)
    assert "\u2014" not in doc, f"em dash in {lang}"
    return doc


# ---------------------------------------------------------------- home page parts

def check_form(t):
    """URL form. Without JS it submits as a mailto GET (subject + body fields); with JS it builds a nicer message."""
    return f'''<form class="check-form" action="mailto:{EMAIL}" method="get"
 data-to="{EMAIL}" data-subject="{esc(t["mail_subject"])}" data-body="{esc(t["mail_body"])}"
 data-err="{esc(t["form_error"])}" data-sent="{esc(t["form_sent"].format(email=EMAIL))}">
<input type="hidden" name="subject" value="{esc(t["mail_subject"])}">
<div class="field-row">
<input id="shop-url" name="body" type="text" inputmode="url" autocomplete="url" spellcheck="false" autocapitalize="off" required placeholder="{esc(t["form_placeholder"])}" aria-labelledby="check-h" aria-describedby="check-hint check-err">
<button type="submit" class="btn btn-accent">{esc(t["form_btn"])}{icon("arrow", "ico btn-ico")}</button>
</div>
<p class="form-hint" id="check-hint">{icon("lock", "ico")}{esc(t["form_hint"])}</p>
<p class="form-error" id="check-err" aria-live="assertive"></p>
<p class="form-status" role="status"></p>
</form>'''


def hero_mock(t):
    """Fictional product page (SVG, decorative). Auto-plays a calm scan of three barriers, then turns into the
    fixed version. Callouts are real text. Reduced motion / no JS: a manual Problems/Fixed toggle instead."""
    good_names = t["demo_items_after"][1:4]
    sw = "".join(f'<circle cx="{258 + i * 38}" cy="166" r="13" fill="{c}"/>' for i, c in enumerate(SWATCHES))
    sw += '<circle cx="258" cy="166" r="17" fill="none" stroke="#13212c" stroke-width="2"/>'

    def mark(n, x, y):
        return (f'<g class="m-mark m-mark-{n}" transform="translate({x} {y})"><circle class="m-pulse" r="12"/>'
                f'<circle class="m-dot" r="12"/><text class="m-bad" y="4.5" text-anchor="middle">{n}</text>'
                f'<path class="m-good" d="M-5 0l3.5 3.5L5.5-4" fill="none" stroke="#fff" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/></g>')

    mock = f'''<svg class="mock" viewBox="0 0 480 290" aria-hidden="true" focusable="false">
<rect x="1" y="1" width="478" height="288" rx="16" fill="#fff" stroke="#d4cdbd" stroke-width="2"/>
<path d="M1 17a16 16 0 0 1 16-16h446a16 16 0 0 1 16 16v17H1z" fill="#f4f0e6"/>
<circle cx="20" cy="18" r="4.5" fill="#d4cdbd"/><circle cx="34" cy="18" r="4.5" fill="#d4cdbd"/><circle cx="48" cy="18" r="4.5" fill="#d4cdbd"/>
<rect x="70" y="9" width="200" height="18" rx="9" fill="#fff"/><text x="82" y="22" class="m-url">{esc(t["mock_url"])}</text>
<rect x="20" y="52" width="180" height="210" rx="12" fill="#eef3ef"/>
<rect x="44" y="102" width="132" height="112" rx="26" fill="#c9b28a"/>
<rect x="56" y="114" width="108" height="88" rx="18" fill="none" stroke="#f4eadb" stroke-width="2" stroke-dasharray="5 5"/>
<text x="242" y="84" class="m-title">{esc(t["mock_product"])}</text>
<text x="242" y="112" class="m-price">{esc(t["mock_price"])}</text>
<text x="242" y="138" class="m-desc">{esc(t["mock_desc"])}</text>
{sw}
<text x="242" y="200" class="m-good m-say">“{esc(good_names[0])}”</text>
<rect class="m-good" x="235" y="211" width="232" height="56" rx="28" fill="none" stroke="#13212c" stroke-width="4"/>
<rect class="m-good" x="239" y="215" width="224" height="48" rx="24" fill="none" stroke="#ffbf47" stroke-width="4"/>
<rect x="243" y="219" width="216" height="40" rx="20" fill="#d9611c"/>
<text x="351" y="244" text-anchor="middle" class="m-btn">{esc(t["mock_btn"])}</text>
<rect class="m-scan" x="234" y="121" width="232" height="24" rx="10"/>
{mark(1, 217, 134)}{mark(2, 217, 166)}{mark(3, 217, 239)}
</svg>'''
    lis = "".join(
        f'<li class="co co-{i + 1}"><span class="c-num" aria-hidden="true">{i + 1}</span><span class="c-txt c-bad"><strong>{esc(b[0])}</strong> {esc(b[1])}</span>'
        f'<span class="c-txt c-good"><strong>{esc(g[0])}</strong> {esc(g[1])}</span></li>'
        for i, (b, g) in enumerate(zip(t["callouts_bad"], t["callouts_good"])))
    labels = esc(json.dumps({"bad": t["mock_state_bad"], "good": t["mock_state_good"], "pause": t["mock_pause"], "play": t["mock_play"]}, ensure_ascii=False))
    return f'''<figure class="peek" data-peek="{labels}" aria-labelledby="peek-cap">
<div class="peek-top"><figcaption id="peek-cap">{esc(t["mock_caption"])}</figcaption>
<div class="seg js-only" role="group" aria-label="{esc(t["mock_show"])}">
<button type="button" data-mode="bad" aria-pressed="true">{esc(t["mock_bad"])}</button>
<button type="button" data-mode="good" aria-pressed="false">{esc(t["mock_good"])}</button>
</div>
<div class="peek-ctl"><span class="state-pill"><span class="state-dot" aria-hidden="true"></span><span class="state-t">{esc(t["mock_state_bad"])}</span></span>
<button type="button" class="mini-btn peek-toggle">{icon("pause", "ico ico-pause")}{icon("play", "ico ico-play")}<span class="sr peek-toggle-t">{esc(t["mock_pause"])}</span></button></div>
</div>
{mock}
<ol class="callouts">{lis}</ol>
</figure>'''


def demo(t):
    """Scene-based screen reader story. The animated stage is decorative (aria-hidden); the same texts are in the
    static before/after block, which is what assistive tech, no-JS and reduced-motion users get."""
    before, after = t["demo_items_before"], t["demo_items_after"]
    sw = "".join(f'<span class="st-sw" data-i="{i + 1}" style="background:{c}"></span>' for i, c in enumerate(SWATCHES))
    checks = "".join(f'<li data-c="{i}">{icon("check")}<span>{esc(x)}</span></li>' for i, x in enumerate(t["demo_checks"]))
    static = "".join(
        f'<div class="ds-col ds-{k}"><p class="ds-h">{icon("cross" if k == "before" else "check")}{esc(t["demo_" + k])}</p>'
        f'<p class="ds-says">{esc(t["demo_says"])}:</p><ol>{"".join(f"<li>“{esc(x)}”</li>" for x in items)}</ol>'
        f'<p class="ds-verdict">{esc(verdict)}</p></div>'
        for k, items, verdict in (("before", before, t["demo_question"] + " " + t["demo_leaves"] + "."),
                                  ("after", after, t["demo_ordered"] + ".")))
    data = esc(json.dumps({"before": before, "after": after, "chip": t["demo_chip"], "la": t["demo_after"],
                           "pause": t["demo_pause"], "play": t["demo_play"]}, ensure_ascii=False))
    return f'''<div class="demo" data-demo="{data}">
<div class="demo-bar"><button type="button" class="demo-toggle">{icon("pause", "ico ico-pause")}{icon("play", "ico ico-play")}<span class="demo-toggle-t">{esc(t["demo_pause"])}</span></button></div>
<div class="stage" aria-hidden="true" data-scene="shop">
<div class="sc sc-shop">
<p class="chip">{icon("voice")}<span class="chip-t">{esc(t["demo_chip"])}</span></p>
<div class="shop">
<div class="st-img" data-i="0"><span class="st-cushion"></span></div>
<div class="st-info">
<p class="st-title">{esc(t["mock_product"])}</p><p class="st-price">{esc(t["mock_price"])}</p>
<div class="st-sws">{sw}</div>
<span class="st-buy" data-i="4">{icon("cart")}<span class="st-buy-t">{esc(t["mock_btn"])}</span></span>
</div>
</div>
<div class="caption">{icon("voice")}<span class="cap-t"></span><span class="caret"></span></div>
<div class="outcome"><span class="oc-q">{esc(t["demo_question"])}</span><span class="oc-badge oc-bad">{icon("cross")}{esc(t["demo_leaves"])}</span><span class="oc-badge oc-ok">{icon("check")}{esc(t["demo_ordered"])}</span></div>
</div>
<div class="sc sc-report">
<div class="rc">
<p class="rc-k">{LOGO}<span>{esc(t["report_title"])}</span></p>
<p class="rc-t">{esc(t["f_title"])}</p>
<ul class="rc-list">{checks}</ul>
</div>
</div>
<div class="sc sc-end">
<p class="end-logo">{LOGO}<span>EveryoneCanShop</span></p>
<p class="end-t">{esc(t["demo_end"])}</p>
<p class="end-s">{esc(t["cta_note"][2])}</p>
</div>
</div>
<div class="demo-static">{static}</div>
</div>'''


def stat_block(t):
    """Verified numbers. Large amounts count up on first view (visual only; the real value is in the DOM)."""
    out = ""
    for i, (n, txt, src, url) in enumerate(t["stats"]):
        digits = re.sub(r"\D", "", n)
        if len(digits) >= 4:
            tpl = re.sub(r"[\d.,\u00a0 ]*\d", "{n}", n, count=1)
            num = f'<span class="sr">{esc(n)}</span><span class="count" aria-hidden="true" data-to="{digits}" data-tpl="{esc(tpl)}">{esc(n)}</span>'
            art = f'<span class="stat-art" aria-hidden="true">{icon("scale")}</span>'
        elif "%" in n:
            num = esc(n)
            pct = int(digits)
            art = (f'<span class="stat-art" aria-hidden="true"><svg class="ring" viewBox="0 0 36 36" width="40" height="40">'
                   f'<circle cx="18" cy="18" r="15.9" pathLength="100" class="ring-bg"/>'
                   f'<circle cx="18" cy="18" r="15.9" pathLength="100" class="ring-fg" stroke-dasharray="{pct} 100"/></svg></span>')
        else:
            num = esc(n)
            art = people("people stat-art")
        out += (f'<div class="big-stat rv">{art}<p class="big-n">{num}</p><p class="big-t">{esc(txt)}</p>'
                f'<p class="big-s">{esc(t["src_label"])} <a href="{url}" rel="noopener">{esc(src)}</a></p></div>')
    return out


def compare(t):
    heads = "".join(f'<th scope="col"{" class=\"ours\"" if c.get("ours") else ""}>{esc(c["name"])}</th>' for c in t["cmp_cols"])
    rows = ""
    for r, label in enumerate(t["cmp_rows"]):
        cells = ""
        for c in t["cmp_cols"]:
            v = c["vals"][r]
            if isinstance(v, list):
                v = f'<span class="yn yn-{v[0]}">{icon("check" if v[0] == "yes" else "cross")}{esc(v[1])}</span>'
            else:
                v = esc(v)
            cells += f'<td{" class=\"ours\"" if c.get("ours") else ""}>{v}</td>'
        rows += f'<tr><th scope="row">{esc(label)}</th>{cells}</tr>'
    table = f'<div class="cmp-table-wrap rv"><table class="cmp-table"><caption class="sr">{esc(t["cmp_h"])}</caption><thead><tr><td></td>{heads}</tr></thead><tbody>{rows}</tbody></table></div>'
    cards = ""
    for c in t["cmp_cols"]:
        dl = ""
        for label, v in zip(t["cmp_rows"], c["vals"]):
            if isinstance(v, list):
                v = f'<span class="yn yn-{v[0]}">{icon("check" if v[0] == "yes" else "cross")}{esc(v[1])}</span>'
            else:
                v = esc(v)
            dl += f"<div><dt>{esc(label)}</dt><dd>{v}</dd></div>"
        cards += f'<div class="card cmp{" cmp-ours" if c.get("ours") else ""}"><h3>{esc(c["name"])}</h3><dl>{dl}</dl></div>'
    return table + f'<div class="cmp-cards">{cards}</div>'


def packages(t):
    main_pk, side_pk = "", ""
    for p in t["packages"]:
        lis = "".join(f"<li>{icon('check', 'ico tick')}<span>{esc(x)}</span></li>" for x in p["items"])
        kind = p["kind"]
        badge = {"free": f'<p class="badge badge-free">{esc(t["badge_free"])}</p>',
                 "rec": f'<p class="badge">{esc(t["badge_rec"])}</p>'}.get(kind, "")
        time = f'<p class="pk-time">{icon("clock")}{esc(p["time"])}</p>' if p["time"] else ""
        extra = f'<p class="pk-extra">{esc(t["audit_note"])}</p>' if kind == "rec" else ""
        cta = ""
        if kind == "free":
            cta = (f'<p class="pk-assure">{icon("shield")}<span>{esc(t["pk_free_note"])}</span></p>'
                   f'<a class="btn btn-accent btn-block" href="#check">{esc(p["cta"])}</a>')
        elif kind == "rec":
            cta = f'<a class="btn btn-ghost btn-block" href="{mailto(p["subject"])}">{esc(p["cta"])}</a>'
        card = (f'<div class="card pk pk-{kind or "plain"} lift spot rv">{badge}<h3>{esc(p["name"])}</h3>'
                f'<p class="price">{esc(p["price"])} <small>{esc(p["per"])}</small></p>'
                f'<p class="pk-desc">{esc(p["desc"])}</p>{time}<ul class="ticks">{lis}</ul>{extra}{cta}</div>')
        if kind:
            main_pk += card
        else:
            side_pk += card
    return f'<div class="pk-main">{main_pk}</div><div class="pk-side">{side_pk}</div>'


def page_home(lang):
    t = T[lang]
    note = "".join(f"<li>{icon('check', 'ico tick')}{esc(x)}</li>" for x in t["cta_note"])
    trust = "".join(f"<li>{icon(i)}<span>{esc(x)}</span></li>" for i, x in zip(TRUST_ICONS, t["trust"]))
    timeline = "".join(f'<li class="rv"><p class="tl-when">{esc(w)}</p><p class="tl-what">{esc(x)}</p></li>' for w, x in t["eaa_timeline"])
    points = "".join(f'<li class="pt lift spot rv"><span class="icon-tile">{icon(i)}</span><h3>{esc(h)}</h3><p>{esc(p)}</p></li>'
                     for i, (h, p) in zip(POINT_ICONS, t["eaa_points"]))
    checks = "".join(f'<li class="chk lift spot rv"><span class="icon-tile">{icon(i)}</span><div><h3>{esc(h)}</h3><p>{esc(p)}</p></div></li>'
                     for i, h, p in t["checks"])
    steps = "".join(f'<li class="rv"><h3>{esc(h)}</h3><p>{esc(p)}</p></li>' for h, p in t["steps"])
    about_p = "".join(f"<p>{esc(p)}</p>" for p in t["about_p"])
    stuck = "".join(f'<li class="stuck-card lift rv">{picture(k, alt)}<p>{esc(x)}</p></li>' for k, alt, x in t["stuck"])
    faq = "".join(f'<details class="rv"><summary>{esc(q)}</summary><div class="faq-a"><p>{esc(a)}</p></div></details>' for q, a in t["faq"])

    doc = head(lang, t["title"], t["description"], "") + header(lang, t, "") + f'''
<main id="main">
<section class="hero" aria-labelledby="h1"><div class="wrap">
<div class="hero-grid">
<div class="hero-copy">
<p class="law-chip">{icon("scale")}{esc(t["law_chip"])}</p>
<h1 id="h1">{esc(t["h1"])}</h1>
<p class="lead">{esc(t["lead"])}</p>
<a class="btn btn-accent btn-lg" href="#check">{esc(t["cta"])}{icon("down", "ico btn-ico")}</a>
<ul class="cta-note">{note}</ul>
</div>
<div class="hero-visual">{hero_mock(t)}</div>
</div>
</div></section>

<section class="trust-band" aria-label="{esc(t["trust_label"])}"><div class="wrap"><ul class="trust">{trust}</ul></div></section>

<section class="why" aria-labelledby="why-h"><div class="wrap">
<h2 id="why-h" class="rv center">{esc(t["why_h"])}</h2>
<div class="big-stats">{stat_block(t)}</div>
<p class="why-line rv">{esc(t["why_line"])}</p>
</div></section>

<section class="stuck-sec alt" aria-labelledby="stuck-h"><div class="wrap">
<h2 id="stuck-h" class="rv">{esc(t["stuck_h"])}</h2>
<p class="section-lead rv">{esc(t["stuck_p"])}</p>
<ul class="stuck">{stuck}</ul>
</div></section>

<section id="eaa" aria-labelledby="eaa-h"><div class="wrap">
<h2 id="eaa-h" class="rv">{esc(t["eaa_h"])}</h2>
<p class="section-lead rv">{esc(t["eaa_p"])}</p>
<ol class="timeline">{timeline}</ol>
<ul class="points">{points}</ul>
<p class="guide-link rv"><a class="btn btn-ghost" href="{path_for(lang, "eaa")}">{icon("book")}{esc(t["eaa_link"])}{icon("arrow", "ico btn-ico")}</a></p>
</div></section>

<section id="example" class="alt" aria-labelledby="ex-h"><div class="wrap">
<h2 id="ex-h" class="rv">{esc(t["ex_h"])}</h2>
<p class="section-lead rv">{esc(t["demo_intro"])}</p>
<div class="report rv">
<div class="report-head"><span class="report-mark" aria-hidden="true">{LOGO}</span><p class="report-title">{esc(t["report_title"])}</p></div>
<div class="report-body">{demo(t)}</div>
</div>
<article class="finding rv" aria-labelledby="f-h">
<div class="finding-top"><h3 id="f-h">{esc(t["f_title"])}</h3><p class="prio">{esc(t["prio"])}</p></div>
<dl class="finding-grid">
<div><dt>{icon("cross")}{esc(t["lbl_problem"])}</dt><dd>{esc(t["f_problem"])}</dd></div>
<div><dt>{icon("users")}{esc(t["lbl_who"])}</dt><dd>{esc(t["f_who"])}</dd></div>
<div class="fix"><dt>{icon("check")}{esc(t["lbl_after"])}</dt><dd>{esc(t["f_after"])}</dd></div>
</dl>
</article>
<p class="note center">{esc(t["ex_note"])}</p>
</div></section>

<section aria-labelledby="what-h"><div class="wrap">
<h2 id="what-h" class="rv">{esc(t["what_h"])}</h2>
<ul class="checks">{checks}</ul>
</div></section>

<section class="alt" aria-labelledby="cmp-h"><div class="wrap">
<h2 id="cmp-h" class="rv">{esc(t["cmp_h"])}</h2>
{compare(t)}
</div></section>

<section id="packages" aria-labelledby="pk-h"><div class="wrap">
<h2 id="pk-h" class="rv">{esc(t["pk_h"])}</h2>
<p class="section-lead rv">{esc(t["pk_p"])}</p>
{packages(t)}
<p class="note">{esc(t["pk_note"])}</p>
</div></section>

<section class="alt" aria-labelledby="how-h"><div class="wrap">
<h2 id="how-h" class="rv">{esc(t["how_h"])}</h2>
<ol class="steps">{steps}</ol>
</div></section>

<section id="faq" aria-labelledby="faq-h"><div class="wrap narrow">
<h2 id="faq-h" class="rv">{esc(t["faq_h"])}</h2>
<div class="faq">{faq}</div>
</div></section>

<section id="about" class="alt" aria-labelledby="about-h"><div class="wrap">
<div class="about rv">
<img src="/ivan.jpg" width="480" height="480" alt="{esc(t["photo_alt"])}" decoding="async" loading="lazy">
<div class="about-text">
<h2 id="about-h">{esc(t["about_h"])}</h2>
<p class="about-role"><strong>Ivan Raylyan</strong> · {esc(t["about_role"])}</p>
{about_p}
<p class="about-li"><a href="{LINKEDIN}" rel="noopener">{icon("linkedin")}<span>{esc(t["linkedin"])}</span></a></p>
</div>
</div>
</div></section>

<section id="check" class="check" aria-labelledby="check-h"><div class="wrap">
<div class="check-box rv">
<div class="check-grid">
<div class="check-main">
<p class="check-kicker">{esc(t["check_kicker"])}</p>
<h2 id="check-h">{esc(t["check_h"])}</h2>
<p class="check-p">{esc(t["check_p"])}</p>
{check_form(t)}
<p class="contact">{esc(t["contact"])} <a href="{mailto(t["mail_subject"])}">{EMAIL}</a></p>
</div>
{picture("owner", t["owner_alt"], "check-ill")}
</div>
</div>
</div></section>
</main>
''' + footer(lang, t)
    return finish(lang, doc)


# ---------------------------------------------------------------- guide page

def page_guide(lang):
    t, g = T[lang], G[lang]
    home = path_for(lang)
    what_p = "".join(f"<p>{esc(p)}</p>" for p in g["s_what_p"])
    mean = "".join(f'<li class="lift spot rv"><span class="icon-tile">{icon(i)}</span><h3>{esc(h)}</h3><p>{esc(p)}</p></li>' for i, h, p in g["mean"])
    countries = "".join(
        f'<li class="country lift spot rv"><h3>{icon("flag")}{esc(n)}</h3><p>{esc(x)}</p>'
        + (f'<p class="src-note">{esc(t["src_label"])} <a href="{u}" rel="noopener">{esc(s)}</a></p>' if u else "") + "</li>"
        for n, x, s, u in g["countries"])
    now = "".join(f'<li class="rv"><p>{esc(x)}</p></li>' for x in g["now"])
    sources = "".join(f'<li><a href="{u}" rel="noopener">{esc(lbl)}</a></li>' for lbl, u in g["sources"])

    doc = head(lang, g["title"], g["description"], "eaa") + header(lang, t, "eaa") + f'''
<main id="main" class="guide">
<section class="g-hero" aria-labelledby="h1"><div class="wrap narrow">
<nav class="crumb" aria-label="{esc(g["crumb_label"])}"><ol><li><a href="{home}">{esc(g["crumb"])}</a></li><li aria-current="page"><span class="crumb-full">{esc(g["h1"])}</span><span class="crumb-short">{esc(g["crumb_short"])}</span></li></ol></nav>
<h1 id="h1">{esc(g["h1"])}</h1>
<p class="lead">{esc(g["intro"])}</p>
<p class="g-note">{icon("info")}<span>{esc(g["not_legal"])}</span></p>
</div></section>

<section aria-labelledby="g-what"><div class="wrap narrow">
<div class="g-split">
<div class="rv"><h2 id="g-what">{esc(g["s_what_h"])}</h2>{what_p}</div>
<div class="g-fact rv">{people("people")}<p class="big-n">{esc(g["fact_n"])}</p><p class="big-t">{esc(g["fact_t"])}</p>
<p class="big-s">{esc(t["src_label"])} <a href="{EU_DISABILITY}" rel="noopener">{esc(g["fact_src"])}</a></p></div>
</div>
</div></section>

<section class="alt" aria-labelledby="g-who"><div class="wrap narrow">
<h2 id="g-who" class="rv">{esc(g["s_who_h"])}</h2>
<div class="yesno">
<div class="yn-card yes lift rv"><p class="yn-h">{icon("check")}{esc(g["who_yes_h"])}</p><p>{esc(g["who_yes"])}</p></div>
<div class="yn-card no lift rv"><p class="yn-h">{icon("cross")}{esc(g["who_no_h"])}</p><p>{esc(g["who_no"])}</p></div>
</div>
</div></section>

<section aria-labelledby="g-mean"><div class="wrap narrow">
<h2 id="g-mean" class="rv">{esc(g["s_mean_h"])}</h2>
<p class="section-lead rv">{esc(g["s_mean_p"])}</p>
<ul class="mean">{mean}</ul>
<div class="g-callouts">
<div class="g-callout rv"><h3>{icon("doc")}{esc(g["statement_h"])}</h3><p>{esc(g["statement_p"])}</p></div>
<div class="g-callout rv"><h3>{icon("scale")}{esc(g["measure_h"])}</h3><p>{esc(g["measure_p"])}</p></div>
</div>
</div></section>

<section class="alt" aria-labelledby="g-check"><div class="wrap narrow">
<h2 id="g-check" class="rv">{esc(g["s_check_h"])}</h2>
<p class="section-lead rv">{esc(g["s_check_p"])}</p>
<ul class="countries">{countries}</ul>
</div></section>

<section aria-labelledby="g-now"><div class="wrap narrow">
<h2 id="g-now" class="rv">{esc(g["s_now_h"])}</h2>
<ol class="now">{now}</ol>
<div class="g-cta rv"><h3>{esc(g["cta_h"])}</h3><p>{esc(g["cta_p"])}</p>
<a class="btn btn-accent btn-lg" href="{home}#check">{esc(g["cta_btn"])}{icon("arrow", "ico btn-ico")}</a></div>
</div></section>

<section class="alt sources" aria-labelledby="g-src"><div class="wrap narrow">
<h2 id="g-src">{esc(g["sources_h"])}</h2>
<ul class="src-list">{sources}</ul>
<p class="g-note">{icon("info")}<span>{esc(g["not_legal"])}</span></p>
</div></section>
</main>
''' + footer(lang, t)
    return finish(lang, doc)


SCRIPT = r'''<script>
(function(){
  var reduce=window.matchMedia&&window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  function $(s,r){return (r||document).querySelector(s);} function $$(s,r){return (r||document).querySelectorAll(s);}
  // URL form: build a friendly mailto message, with a clickable fallback address
  var f=$("form.check-form");
  if(f){
    f.noValidate=true;
    var input=$("input[name=body]",f),err=$(".form-error",f),st=$(".form-status",f);
    f.addEventListener("submit",function(e){
      e.preventDefault();
      var v=input.value.trim();
      if(!/^[^\s]+\.[a-z]{2,}/i.test(v.replace(/^https?:\/\//i,""))){
        err.textContent=f.getAttribute("data-err");input.setAttribute("aria-invalid","true");st.textContent="";input.focus();return;
      }
      err.textContent="";input.removeAttribute("aria-invalid");
      var href="mailto:"+f.getAttribute("data-to")+"?subject="+encodeURIComponent(f.getAttribute("data-subject"))+"&body="+encodeURIComponent(f.getAttribute("data-body").replace("{url}",v));
      st.textContent=f.getAttribute("data-sent")+" ";var ml=document.createElement("a");ml.href=href;ml.textContent=f.getAttribute("data-to");st.appendChild(ml);
      window.location.href=href;
    });
    var links=$$('a[href="#check"]');
    for(var j=0;j<links.length;j++){links[j].addEventListener("click",function(){setTimeout(function(){input.focus({preventScroll:true});},reduce?0:450);});}
  }
  // Hero illustration: auto-playing scan of three barriers, then the fixed version (manual toggle for reduced motion)
  var peek=$("[data-peek]");
  if(peek){
    var bs=$$(".seg button",peek);
    for(var b=0;b<bs.length;b++){bs[b].addEventListener("click",function(){
      for(var k=0;k<bs.length;k++){bs[k].setAttribute("aria-pressed",bs[k]===this?"true":"false");}
      peek.classList.toggle("is-good",this.getAttribute("data-mode")==="good");
    });}
    if(!reduce){
      var pl=JSON.parse(peek.getAttribute("data-peek")),scan=$(".m-scan",peek),stT=$(".state-t",peek),
          pbtn=$(".peek-toggle",peek),pt=$(".peek-toggle-t",peek),pos=0,ptimer=null,pplay=false,
          boxes=[null,[234,121,232,24],[236,144,116,44],[237,213,228,52]],
          seq=[{a:0,g:0,t:1200},{a:1,g:0,t:2100},{a:2,g:0,t:2100},{a:3,g:0,t:2100},{a:9,g:0,t:1500},{a:0,g:1,t:4200}];
      peek.classList.add("auto");
      function pshow(s){
        peek.classList.toggle("is-good",!!s.g);
        stT.textContent=s.g?pl.good:pl.bad;
        for(var n=1;n<=3;n++){peek.classList.toggle("act-"+n,s.a===n||s.a===9);}
        var bx=boxes[s.a]||null;
        if(bx){scan.style.x=bx[0]+"px";scan.style.y=bx[1]+"px";scan.style.width=bx[2]+"px";scan.style.height=bx[3]+"px";
          scan.setAttribute("x",bx[0]);scan.setAttribute("y",bx[1]);scan.setAttribute("width",bx[2]);scan.setAttribute("height",bx[3]);}
        peek.classList.toggle("scanning",!!bx);
      }
      function ptick(){pshow(seq[pos]);ptimer=setTimeout(function(){pos=(pos+1)%seq.length;ptick();},seq[pos].t);}
      function pgo(){if(pplay)return;pplay=true;peek.classList.remove("paused");pt.textContent=pl.pause;ptick();}
      function pstop(){pplay=false;clearTimeout(ptimer);peek.classList.add("paused");pt.textContent=pl.play;}
      pbtn.addEventListener("click",function(){pplay?pstop():pgo();});
      pgo();
    }
  }
  // Reveal on scroll
  var rv=$$(".rv");
  if(!reduce&&"IntersectionObserver" in window){
    var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add("in");io.unobserve(e.target);}});},{rootMargin:"0px 0px -6% 0px"});
    for(var r=0;r<rv.length;r++){io.observe(rv[r]);}
  }else{for(var r2=0;r2<rv.length;r2++){rv[r2].classList.add("in");}}
  // Count up large numbers once (visual only; the real value is in a visually hidden span)
  var cs=$$(".count");
  if(!reduce&&cs.length&&"IntersectionObserver" in window){
    var cio=new IntersectionObserver(function(es){es.forEach(function(e){
      if(!e.isIntersecting)return;cio.unobserve(e.target);
      var el=e.target,to=+el.getAttribute("data-to"),tpl=el.getAttribute("data-tpl"),t0=null,lang=document.documentElement.lang;
      var fmt=window.Intl?new Intl.NumberFormat(lang==="en"?"en-GB":lang+"-"+lang.toUpperCase()):null;
      function step(ts){if(!t0)t0=ts;var p=Math.min(1,(ts-t0)/1400),v=Math.round(to*(1-Math.pow(1-p,3)));
        el.textContent=tpl.replace("{n}",fmt?fmt.format(v):v);if(p<1)requestAnimationFrame(step);}
      requestAnimationFrame(step);
    });},{threshold:0.6});
    for(var c=0;c<cs.length;c++){cio.observe(cs[c]);}
  }
  // Soft light that follows the pointer on cards (decorative)
  var spots=$$(".spot");
  for(var sp=0;sp<spots.length;sp++){spots[sp].addEventListener("pointermove",function(e){
    var rc=this.getBoundingClientRect();this.style.setProperty("--mx",(e.clientX-rc.left)+"px");this.style.setProperty("--my",(e.clientY-rc.top)+"px");
  });}
  // Screen reader demo: a short story in scenes (static before/after stays for reduced motion and assistive tech)
  var d=$("[data-demo]");
  if(d&&!reduce){
    var cfg=JSON.parse(d.getAttribute("data-demo")),stage=$(".stage",d),cap=$(".cap-t",d),
        chip=$(".chip-t",d),btn=$(".demo-toggle",d),bt=$(".demo-toggle-t",d),
        els=$$("[data-i]",d),ch=$$("[data-c]",d),dpos=0,timer=null,typer=null,playing=false,steps=[];
    function focus(i){for(var k=0;k<els.length;k++){els[k].classList.toggle("sr-on",+els[k].getAttribute("data-i")===i);}}
    function type(txt){clearInterval(typer);var n=0;cap.textContent="";if(!txt)return;txt="\u201c"+txt+"\u201d";
      typer=setInterval(function(){n++;cap.textContent=txt.slice(0,n);if(n>=txt.length)clearInterval(typer);},42);}
    function outcome(o){stage.setAttribute("data-outcome",o||"");}
    function checks(n){for(var k=0;k<ch.length;k++){ch[k].classList.toggle("on",+ch[k].getAttribute("data-c")<n);}}
    function scene(sc,after){stage.setAttribute("data-scene",sc);stage.classList.toggle("after",!!after);chip.textContent=after?cfg.la:cfg.chip;}
    function pass(items){items.forEach(function(x,i){steps.push({f:function(){focus(i);type(x);},t:650+x.length*42+500});});}
    steps.push({f:function(){scene("shop",false);focus(-1);type("");outcome("");checks(0);},t:1700});
    pass(cfg.before);
    steps.push({f:function(){focus(-1);outcome("q");},t:1400});
    steps.push({f:function(){outcome("bad");},t:2000});
    steps.push({f:function(){scene("report",false);checks(0);},t:800});
    for(var cc=1;cc<=3;cc++){(function(cc){steps.push({f:function(){checks(cc);},t:cc<3?900:2600});})(cc);}
    steps.push({f:function(){scene("shop",true);focus(-1);type("");outcome("");},t:1400});
    pass(cfg.after);
    steps.push({f:function(){focus(-1);outcome("ok");},t:2200});
    steps.push({f:function(){scene("end",true);},t:2800});
    function tick(){steps[dpos].f();timer=setTimeout(function(){dpos=(dpos+1)%steps.length;tick();},steps[dpos].t);}
    function play(){if(playing)return;playing=true;d.classList.remove("paused");bt.textContent=cfg.pause;tick();}
    function pause(){playing=false;clearTimeout(timer);clearInterval(typer);d.classList.add("paused");bt.textContent=cfg.play;}
    d.classList.add("animating");steps[0].f();
    btn.addEventListener("click",function(){playing?pause():play();});
    if("IntersectionObserver" in window){
      var started=false,dio=new IntersectionObserver(function(es){if(es[0].isIntersecting&&!started){started=true;play();}},{threshold:0.35});
      dio.observe(d);
    }else{play();}
  }
})();
</script>'''


def fr_typo(doc):
    """French typography: non-breaking space before ? ! : ; and » after «, and inside amounts. Text nodes only:
    skips script/style/pre and every tag, so attributes such as an SVG viewBox are never touched."""
    parts = re.split(r"(<script.*?</script>|<style.*?</style>|<pre.*?</pre>|<[^>]+>)", doc, flags=re.S)
    for i in range(0, len(parts), 2):
        parts[i] = re.sub(r" ([?!:;»])", "\u00a0\\1", parts[i])
        parts[i] = re.sub(r"« ", "«\u00a0", parts[i])
        parts[i] = re.sub(r"(\d) €", "\\1\u00a0€", parts[i])
        parts[i] = re.sub(r"(\d) (\d{3})", "\\1\u00a0\\2", parts[i])
    return "".join(parts)


def images():
    from PIL import Image
    src = Image.open(ROOT / "src/ivan.jpg").convert("RGB")
    src.save(OUT / "ivan.jpg", quality=82, optimize=True, progressive=True)
    shutil.copytree(ROOT / "src/ill", OUT / "ill")


def main():
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir()
    for lang in LANGS:
        d = OUT if lang == "en" else OUT / lang
        d.mkdir(exist_ok=True)
        (d / "index.html").write_text(page_home(lang))
        (d / "eaa").mkdir()
        (d / "eaa" / "index.html").write_text(page_guide(lang))
    shutil.copy(ROOT / "src/style.css", OUT / "style.css")
    for f in (ROOT / "src").glob("*.svg"):
        shutil.copy(f, OUT / f.name)
    images()
    (OUT / "CNAME").write_text("everyonecanshop.com")
    (OUT / ".nojekyll").write_text("")
    (OUT / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {BASE}/sitemap.xml\n")
    urls = "".join(f"<url><loc>{BASE}{path_for(l, p)}</loc></url>" for l in LANGS for p in ("", "eaa"))
    (OUT / "sitemap.xml").write_text(f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>\n')
    print("built", [path_for(l, p) for l in LANGS for p in ("", "eaa")])


if __name__ == "__main__":
    main()
