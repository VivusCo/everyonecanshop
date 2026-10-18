#!/usr/bin/env python3
"""Build the static EveryoneCanShop site into docs/ (GitHub Pages). Content lives in content.py."""
import html, pathlib, re, shutil
from urllib.parse import quote
from content import LANGS, LINKEDIN, T

ROOT = pathlib.Path(__file__).parent
OUT = ROOT / "docs"
BASE = "https://everyonecanshop.com"
EMAIL = "ivan@everyonecanshop.com"


def path_for(lang):
    return "/" if lang == "en" else f"/{lang}/"


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
    "person": f'<circle cx="12" cy="8.5" r="3.5" {S}/><path d="M5 20c1-3.5 3.8-5.5 7-5.5s6 2 7 5.5" {S}/>',
    "tag": f'<path d="M3.5 12.5V4.5h8l9 9-8 8z" {S}/><circle cx="8" cy="9" r="1.3" fill="currentColor"/>',
    "users": f'<circle cx="9" cy="9" r="3" {S}/><path d="M3.5 19c.8-3 3-4.5 5.5-4.5s4.7 1.5 5.5 4.5M15.5 6.2a3 3 0 0 1 0 5.6M17 14.8c1.8.5 3 1.9 3.5 4.2" {S}/>',
    "letter": f'<rect x="3" y="5.5" width="18" height="13" rx="2" {S}/><path d="M3.5 7l8.5 6 8.5-6" {S}/>',
    "scale": f'<path d="M12 4v16M7 20h10M5 7h14M5 7l-2.5 6a3 3 0 0 0 5 0zM19 7l-2.5 6a3 3 0 0 0 5 0z" {S}/>',
    "arrow": f'<path d="M5 12h14M13 6l6 6-6 6" {S}/>',
    "linkedin": '<path fill="currentColor" d="M4.98 3.5A2.5 2.5 0 1 1 5 8.5a2.5 2.5 0 0 1-.02-5zM3 9.75h4V21H3zM9.5 9.75h3.8v1.6h.06c.53-1 1.83-2.05 3.77-2.05 4.03 0 4.77 2.6 4.77 6V21h-4v-5.1c0-1.22-.02-2.8-1.7-2.8-1.72 0-1.98 1.33-1.98 2.7V21h-4z"/>',
}
TRUST_ICONS = ["scale", "lock", "person", "tag"]
COST_ICONS = ["users", "letter", "shield"]

LOGO = ('<svg class="logo-mark" viewBox="0 0 32 32" aria-hidden="true" focusable="false">'
        '<rect x="1" y="1" width="30" height="30" rx="9" fill="#13212c"/>'
        '<path d="M8 11h3l2.2 9h7.6l1.7-6.5H12" fill="none" stroke="#fff" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/>'
        '<circle cx="14" cy="24" r="1.6" fill="#ffbf47"/><circle cx="20" cy="24" r="1.6" fill="#ffbf47"/></svg>')


def icon(name, cls="ico"):
    return svg(ICONS[name], cls)


def sev_chip(t, sev):
    return f'<span class="sev sev-{sev}">{esc(t["sev"][sev])}</span>'


def check_form(t, uid, dark=False):
    """URL form. Without JS it submits as a mailto GET (subject + body fields); with JS it builds a nicer message."""
    return f'''<form class="check-form{" on-dark" if dark else ""}" action="mailto:{EMAIL}" method="get"
 data-to="{EMAIL}" data-subject="{esc(t["mail_subject"])}" data-body="{esc(t["mail_body"])}"
 data-err="{esc(t["form_error"])}" data-sent="{esc(t["form_sent"].format(email=EMAIL))}">
<input type="hidden" name="subject" value="{esc(t["mail_subject"])}">
<label for="url-{uid}">{esc(t["form_label"])}</label>
<div class="field-row">
<input id="url-{uid}" name="body" type="text" inputmode="url" autocomplete="url" spellcheck="false" autocapitalize="off" required placeholder="{esc(t["form_placeholder"])}" aria-describedby="hint-{uid} err-{uid}">
<button type="submit" class="btn btn-primary">{esc(t["form_btn"])}{icon("arrow", "ico btn-ico")}</button>
</div>
<p class="form-hint" id="hint-{uid}">{icon("check", "ico tick")}{esc(t["form_hint"])}</p>
<p class="form-error" id="err-{uid}" aria-live="assertive"></p>
<p class="form-status" role="status"></p>
<p class="form-alt">{esc(t["or_email"])} <a href="{mailto(t["mail_subject"])}">{EMAIL}</a></p>
</form>'''


def hero_peek(t):
    rows = "".join(
        f'<li>{sev_chip(t, s)}<span class="peek-text">{esc(txt)}</span><span class="peek-ref">{esc(ref)}</span></li>'
        for s, txt, ref in t["peek_rows"])
    return f'''<figure class="peek" aria-labelledby="peek-cap">
<div class="peek-doc">
<div class="peek-bar" aria-hidden="true"><span></span><span></span><span></span></div>
<p class="kicker">{esc(t["peek_kicker"])}</p>
<p class="peek-title">{esc(t["peek_title"])}</p>
<ol class="peek-list">{rows}</ol>
<div class="peek-foot">
<span>{icon("check", "ico tick")}{esc(t["peek_reviewed"])}</span>
<span>{icon("clock", "ico")}{esc(t["peek_time"])}</span>
</div>
</div>
<figcaption id="peek-cap">{esc(t["peek_caption"])}</figcaption>
</figure>'''


def finding(t, i, f):
    n = i + 1
    if n == 1:
        visual = f'''<figure class="shot">
<div class="shot-frame"><img src="/sample-nofocus.jpg" width="612" height="115" alt="{esc(f["img_alt"])}" decoding="async">
<span class="shot-ring" aria-hidden="true"></span><span class="shot-tag" aria-hidden="true">{esc(f["marker"])}</span></div>
</figure>'''
    else:
        if n == 2:
            mock = ('<div class="mock" aria-hidden="true"><span class="sw" style="background:#5b6b3a"></span>'
                    '<span class="sw sw-on" style="background:#2c5d86"></span><span class="sw" style="background:#d8c6a3"></span></div>')
        else:
            mock = ('<div class="mock" aria-hidden="true"><span class="qty"><span>-</span><span class="qv">1</span><span>+</span></span></div>')
        visual = f'''<div class="sr-demo">{mock}
<dl class="sr-out">
<div><dt>{esc(t["lbl_sr"])}</dt><dd class="bad">{icon("cross", "ico")}<span>{esc(f["sr_before"])}</span></dd></div>
<div><dt>{esc(t["lbl_after"])}</dt><dd class="good">{icon("check", "ico")}<span>{esc(f["sr_after"])}</span></dd></div>
</dl></div>'''
    return f'''<article class="finding" aria-labelledby="f{n}">
<header class="finding-head">
<p class="finding-num">{esc(t["lbl_finding"])} {n}</p>
<h3 id="f{n}">{esc(f["title"])}</h3>
<dl class="finding-meta">
<div><dt class="sr">{esc(t["lbl_sev"])}</dt><dd>{sev_chip(t, f["sev"])}</dd></div>
<div><dt>{esc(t["lbl_wcag"])}</dt><dd>{esc(f["wcag"])}</dd></div>
<div><dt>{esc(t["lbl_where"])}</dt><dd>{esc(f["where"])}</dd></div>
</dl>
</header>
<div class="finding-body">
<div class="finding-col">
<h4>{esc(t["lbl_saw"])}</h4><p>{esc(f["saw"])}</p>
{visual}
<h4>{esc(t["lbl_affected"])}</h4><p>{esc(f["affected"])}</p>
</div>
<div class="finding-col fix">
<h4>{esc(t["lbl_fix"])}</h4><p>{esc(f["fix"])}</p>
<pre><code>{esc(f["code"])}</code></pre>
</div>
</div>
</article>'''


SCRIPT = r'''<script>
(function(){
  var forms=document.querySelectorAll("form.check-form");
  for(var k=0;k<forms.length;k++){(function(f){
    f.noValidate=true;
    var input=f.querySelector("input[name=body]"),err=f.querySelector(".form-error"),st=f.querySelector(".form-status");
    f.addEventListener("submit",function(e){
      e.preventDefault();
      var v=input.value.trim();
      if(!/^[^\s]+\.[a-z]{2,}/i.test(v.replace(/^https?:\/\//i,""))){
        err.textContent=f.getAttribute("data-err");input.setAttribute("aria-invalid","true");st.textContent="";input.focus();return;
      }
      err.textContent="";input.removeAttribute("aria-invalid");
      var href="mailto:"+f.getAttribute("data-to")+"?subject="+encodeURIComponent(f.getAttribute("data-subject"))+"&body="+encodeURIComponent(f.getAttribute("data-body").replace("{url}",v));
      st.textContent=f.getAttribute("data-sent");
      window.location.href=href;
    });
  })(forms[k]);}
  var links=document.querySelectorAll('a[href="#check"]'),first=document.getElementById("url-hero");
  for(var j=0;j<links.length;j++){links[j].addEventListener("click",function(){setTimeout(function(){first.focus({preventScroll:true});},0);});}
})();
</script>'''


def fr_typo(doc):
    """French typography: non-breaking space before ? ! : ; and inside amounts like '490 €'. Skips script/style."""
    parts = re.split(r"(<script.*?</script>|<style.*?</style>|<pre.*?</pre>)", doc, flags=re.S)
    for i in range(0, len(parts), 2):
        parts[i] = re.sub(r" ([?!:;])", "\u00a0\\1", parts[i])
        parts[i] = re.sub(r"(\d) €", "\\1\u00a0€", parts[i])
    return "".join(parts)


def page(lang):
    t = T[lang]
    alts = "\n".join(f'<link rel="alternate" hreflang="{l}" href="{BASE}{path_for(l)}">' for l in LANGS)
    alts += f'\n<link rel="alternate" hreflang="x-default" href="{BASE}/">'
    langnav = "".join(
        f'<li><a href="{path_for(l)}" hreflang="{l}" lang="{l}"' + (' aria-current="page"' if l == lang else "") +
        f'><span aria-hidden="true">{l.upper()}</span><span class="sr">{esc(T[l]["lang_name"])}</span></a></li>' for l in LANGS)
    nav = "".join(f'<li><a href="#{a}">{esc(label)}</a></li>' for a, label in t["nav"])
    trust = "".join(f"<li>{icon(i)}<span>{esc(x)}</span></li>" for i, x in zip(TRUST_ICONS, t["trust"]))
    stats = "".join(
        f'<div class="card stat-card"><p class="stat">{esc(n)}</p><p>{esc(p)}</p>'
        f'<p class="src">{esc(t["src_label"])} <a href="{u}" rel="noopener">{esc(s)}</a></p></div>'
        for n, p, s, u in t["stats"])
    costs = "".join(f'<li>{icon(i, "ico cost-ico")}<div><h3>{esc(h)}</h3><p>{esc(p)}</p></div></li>'
                    for i, (h, p) in zip(COST_ICONS, t["costs"]))
    meta = "".join(f"<div><dt>{esc(k)}</dt><dd>{esc(v)}</dd></div>" for k, v in t["doc_meta"])
    findings = "".join(finding(t, i, f) for i, f in enumerate(t["findings"]))
    checks = "".join(f'<li class="card check-card"><span class="icon-tile">{icon(i)}</span><h3>{esc(h)}</h3><p>{esc(p)}</p></li>'
                     for i, h, p in t["checks"])

    main_pk, side_pk = "", ""
    for p in t["packages"]:
        lis = "".join(f"<li>{icon('check', 'ico tick')}<span>{esc(x)}</span></li>" for x in p["items"])
        kind = p["kind"]
        badge = ""
        if kind == "free":
            badge = f'<p class="badge badge-free">{esc(t["badge_free"])}</p>'
        elif kind == "rec":
            badge = f'<p class="badge">{esc(t["badge_rec"])}</p>'
        time = f'<p class="pk-time">{icon("clock")}{esc(p["time"])}</p>' if p["time"] else ""
        cta = ""
        if kind == "free":
            cta = (f'<p class="pk-assure">{icon("shield")}<span>{esc(t["pk_free_note"])}</span></p>'
                   f'<a class="btn btn-primary btn-block" href="#check">{esc(p["cta"])}</a>')
        elif kind == "rec":
            cta = f'<a class="btn btn-ghost btn-block" href="{mailto(p["subject"])}">{esc(p["cta"])}</a>'
        card = (f'<div class="card pk pk-{kind or "plain"}">{badge}<h3>{esc(p["name"])}</h3>'
                f'<p class="price">{esc(p["price"])} <small>{esc(p["per"])}</small></p>'
                f'<p class="pk-desc">{esc(p["desc"])}</p>{time}<ul class="ticks">{lis}</ul>{cta}</div>')
        if kind:
            main_pk += card
        else:
            side_pk += card

    steps = "".join(f"<li><h3>{esc(h)}</h3><p>{esc(p)}</p></li>" for h, p in t["steps"])
    who_p = "".join(f"<p>{esc(p)}</p>" for p in t["who_p"])
    facts = "".join(f"<li>{icon('check', 'ico tick')}<span>{esc(x)}</span></li>" for x in t["who_facts"])

    cols = ""
    for c in t["cmp_cols"]:
        rows = ""
        for label, v in zip(t["cmp_rows"], c["vals"]):
            if isinstance(v, tuple):
                ok, txt = v
                val = f'<span class="yn yn-{ok}">{icon("check" if ok == "yes" else "cross")}{esc(txt)}</span>'
            else:
                val = esc(v)
            rows += f"<div><dt>{esc(label)}</dt><dd>{val}</dd></div>"
        cols += f'<div class="card cmp{" cmp-ours" if c.get("ours") else ""}"><h3>{esc(c["name"])}</h3><dl>{rows}</dl></div>'

    faq = "".join(f"<details><summary>{esc(q)}</summary><p>{a}</p></details>" for q, a in t["faq"])

    doc = f'''<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(t["title"])}</title>
<meta name="description" content="{esc(t["description"])}">
<meta name="color-scheme" content="light">
<meta name="theme-color" content="#fbf9f4">
<link rel="canonical" href="{BASE}{path_for(lang)}">
{alts}
<meta property="og:title" content="{esc(t["title"])}">
<meta property="og:description" content="{esc(t["description"])}">
<meta property="og:url" content="{BASE}{path_for(lang)}">
<meta property="og:type" content="website">
<meta property="og:image" content="{BASE}/ivan.jpg">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="/style.css">
</head>
<body>
<a class="skip" href="#main">{esc(t["skip"])}</a>
<header class="site"><div class="wrap">
<a class="logo" href="{path_for(lang)}">{LOGO}<span>EveryoneCanShop</span></a>
<nav class="primary" aria-label="{esc(t["nav_label"])}"><ul>{nav}</ul></nav>
<div class="head-right">
<nav class="lang" aria-label="{esc(t["lang_label"])}"><ul>{langnav}</ul></nav>
<a class="btn btn-primary btn-sm head-cta" href="#check">{esc(t["header_cta"])}</a>
</div>
</div></header>

<main id="main">
<section class="hero" aria-labelledby="h1"><div class="wrap">
<div class="hero-grid">
<div class="hero-copy">
<p class="eyebrow">{esc(t["eyebrow"])}</p>
<h1 id="h1">{esc(t["h1"])}</h1>
<p class="lead">{esc(t["lead"])}</p>
<div class="form-card" id="check">
{check_form(t, "hero")}
</div>
<div class="auditor">
<img src="/ivan-sm.jpg" width="72" height="72" alt="{esc(t["photo_alt"])}">
<div><p class="auditor-name">Ivan Raylyan <span>· {esc(t["auditor_role"])}</span></p>
<p class="auditor-line">{esc(t["auditor_line"])}</p>
<p class="auditor-link"><a href="#sample">{esc(t["cta2"])}</a></p></div>
</div>
</div>
<div class="hero-visual">{hero_peek(t)}</div>
</div>
<ul class="trust" aria-label="{esc(t["trust_label"])}">{trust}</ul>
</div></section>

<section class="alt" id="why" aria-labelledby="why-h"><div class="wrap">
<h2 id="why-h">{esc(t["why_h"])}</h2>
<p class="section-lead">{esc(t["why_p"])}</p>
<div class="grid-3">{stats}</div>
<div class="costs">
<h3 class="costs-h">{esc(t["cost_h"])}</h3>
<ul>{costs}</ul>
<p class="costs-note">{esc(t["cost_note"])}</p>
</div>
</div></section>

<section id="sample" aria-labelledby="sample-h"><div class="wrap">
<h2 id="sample-h">{esc(t["sample_h"])}</h2>
<p class="section-lead">{esc(t["sample_p"])}</p>
<div class="report">
<div class="report-head">
<div><p class="kicker">{esc(t["doc_kicker"])}</p><p class="report-title">{esc(t["doc_title"])}</p></div>
<span class="report-mark" aria-hidden="true">{LOGO}</span>
</div>
<dl class="report-meta">{meta}</dl>
{findings}
</div>
<p class="note sample-note">{esc(t["sample_note"])}</p>
</div></section>

<section class="alt" aria-labelledby="what-h"><div class="wrap">
<h2 id="what-h">{esc(t["what_h"])}</h2>
<p class="section-lead">{esc(t["what_p"])}</p>
<ul class="grid-3 plain">{checks}</ul>
</div></section>

<section id="packages" aria-labelledby="pk-h"><div class="wrap">
<h2 id="pk-h">{esc(t["pk_h"])}</h2>
<p class="section-lead">{esc(t["pk_p"])}</p>
<div class="pk-main">{main_pk}</div>
<div class="pk-side">{side_pk}</div>
<p class="note">{esc(t["pk_note"])}</p>
</div></section>

<section class="alt" aria-labelledby="how-h"><div class="wrap">
<h2 id="how-h">{esc(t["how_h"])}</h2>
<ol class="steps">{steps}</ol>
</div></section>

<section id="about" aria-labelledby="about-h"><div class="wrap">
<div class="about">
<div class="about-photo">
<img src="/ivan.jpg" width="480" height="480" alt="{esc(t["photo_alt"])}" decoding="async">
<p class="about-li"><a href="{LINKEDIN}" rel="noopener">{icon("linkedin")}<span>{esc(t["linkedin"])}</span></a></p>
</div>
<div class="about-text">
<h2 id="about-h">{esc(t["who_h"])}</h2>
<p class="about-role">{esc(t["who_role"])}</p>
{who_p}
<blockquote><p>{esc(t["who_quote"])}</p></blockquote>
<h3 class="facts-h">{esc(t["who_facts_label"])}</h3>
<ul class="ticks facts">{facts}</ul>
</div>
</div>
</div></section>

<section class="alt" aria-labelledby="cmp-h"><div class="wrap">
<h2 id="cmp-h">{esc(t["cmp_h"])}</h2>
<p class="section-lead">{esc(t["cmp_p"])}</p>
<div class="grid-3 cmp-grid">{cols}</div>
</div></section>

<section id="faq" aria-labelledby="faq-h"><div class="wrap narrow">
<h2 id="faq-h">{esc(t["faq_h"])}</h2>
{faq}
</div></section>

<section class="final-wrap" aria-labelledby="fin-h"><div class="wrap"><div class="final">
<div class="final-copy">
<h2 id="fin-h">{esc(t["final_h"])}</h2>
<p>{esc(t["final_p"])}</p>
<div class="final-auditor"><img src="/ivan-sm.jpg" width="48" height="48" alt=""><span>Ivan Raylyan · {esc(t["auditor_role"])}</span></div>
</div>
{check_form(t, "final", dark=True)}
</div></div></section>
</main>

<footer class="site"><div class="wrap">
<div class="foot-brand"><a class="logo" href="{path_for(lang)}">{LOGO}<span>EveryoneCanShop</span></a><p>{esc(t["footer_op"])}</p></div>
<div><h2 class="foot-h">{esc(t["footer_contact"])}</h2>
<ul class="foot-list"><li><a href="mailto:{EMAIL}">{EMAIL}</a></li><li><a href="{LINKEDIN}" rel="noopener">LinkedIn</a></li></ul></div>
<div class="foot-small"><p>{esc(t["footer_privacy"])}</p><p>{esc(t["footer_a11y"])}</p></div>
</div></footer>
@@SCRIPT@@
</body>
</html>
'''
    if lang == "fr":
        doc = fr_typo(doc)
    doc = doc.replace("@@SCRIPT@@", SCRIPT)
    assert "\u2014" not in doc, f"em dash in {lang}"
    return doc


def images():
    from PIL import Image
    src = Image.open(ROOT / "src/ivan.jpg").convert("RGB")
    src.save(OUT / "ivan.jpg", quality=82, optimize=True, progressive=True)
    src.resize((144, 144), Image.LANCZOS).save(OUT / "ivan-sm.jpg", quality=85, optimize=True)


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
    images()
    (OUT / "CNAME").write_text("everyonecanshop.com")
    (OUT / ".nojekyll").write_text("")
    (OUT / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {BASE}/sitemap.xml\n")
    urls = "".join(f"<url><loc>{BASE}{path_for(l)}</loc></url>" for l in LANGS)
    (OUT / "sitemap.xml").write_text(f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>\n')
    print("built", [path_for(l) for l in LANGS])


if __name__ == "__main__":
    main()
