#!/usr/bin/env python3
"""Build the static EveryoneCanShop site into docs/ (GitHub Pages). Content lives in content.py."""
import html, json, pathlib, re, shutil
from urllib.parse import quote
from content import EAA, LANGS, LINKEDIN, T

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
    "users": f'<circle cx="9" cy="9" r="3" {S}/><path d="M3.5 19c.8-3 3-4.5 5.5-4.5s4.7 1.5 5.5 4.5M15.5 6.2a3 3 0 0 1 0 5.6M17 14.8c1.8.5 3 1.9 3.5 4.2" {S}/>',
    "tag": f'<path d="M3.5 12.5V4.5h8l9 9-8 8z" {S}/><circle cx="8" cy="9" r="1.3" fill="currentColor"/>',
    "scale": f'<path d="M12 4v16M7 20h10M5 7h14M5 7l-2.5 6a3 3 0 0 0 5 0zM19 7l-2.5 6a3 3 0 0 0 5 0z" {S}/>',
    "arrow": f'<path d="M5 12h14M13 6l6 6-6 6" {S}/>',
    "down": f'<path d="M12 5v14M6 13l6 6 6-6" {S}/>',
    "pause": '<rect x="6" y="5" width="4" height="14" rx="1" fill="currentColor"/><rect x="14" y="5" width="4" height="14" rx="1" fill="currentColor"/>',
    "play": '<path d="M7 5l12 7-12 7z" fill="currentColor"/>',
    "cart": f'<path d="M3 4h2.5l2.2 10.5h10.6l2-7.5H7" {S}/><circle cx="10" cy="19" r="1.5" fill="currentColor"/><circle cx="17" cy="19" r="1.5" fill="currentColor"/>',
    "linkedin": '<path fill="currentColor" d="M4.98 3.5A2.5 2.5 0 1 1 5 8.5a2.5 2.5 0 0 1-.02-5zM3 9.75h4V21H3zM9.5 9.75h3.8v1.6h.06c.53-1 1.83-2.05 3.77-2.05 4.03 0 4.77 2.6 4.77 6V21h-4v-5.1c0-1.22-.02-2.8-1.7-2.8-1.72 0-1.98 1.33-1.98 2.7V21h-4z"/>',
}
TRUST_ICONS = ["scale", "lock", "users", "tag"]

LOGO = ('<svg class="logo-mark" viewBox="0 0 32 32" aria-hidden="true" focusable="false">'
        '<rect x="1" y="1" width="30" height="30" rx="9" fill="#13212c"/>'
        '<path d="M8 11h3l2.2 9h7.6l1.7-6.5H12" fill="none" stroke="#fff" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/>'
        '<circle cx="14" cy="24" r="1.6" fill="#ffbf47"/><circle cx="20" cy="24" r="1.6" fill="#ffbf47"/></svg>')
SWATCHES = ["#5b6b3a", "#2c5d86", "#d8c6a3"]


def icon(name, cls="ico"):
    return svg(ICONS[name], cls)


def sev_chip(t):
    return f'<span class="sev sev-high">{esc(t["sev"]["high"])}</span>'


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
    """Illustrated fictional product page (SVG, decorative) plus real-text callouts and a Problems/Fixed toggle."""
    good_names = t["demo_items_after"][1:4]
    sw = "".join(f'<circle cx="{258 + i * 38}" cy="166" r="13" fill="{c}"/>' for i, c in enumerate(SWATCHES))
    sw += '<circle cx="258" cy="166" r="17" fill="none" stroke="#13212c" stroke-width="2"/>'

    def mark(n, x, y):
        return (f'<g class="m-mark" transform="translate({x} {y})"><circle class="m-pulse" r="12"/>'
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
{mark(1, 217, 166)}{mark(2, 217, 239)}{mark(3, 217, 134)}
</svg>'''
    lis = "".join(
        f'<li><span class="c-num" aria-hidden="true">{i + 1}</span><span class="c-txt c-bad"><strong>{esc(b[0])}</strong> {esc(b[1])}</span>'
        f'<span class="c-txt c-good"><strong>{esc(g[0])}</strong> {esc(g[1])}</span></li>'
        for i, (b, g) in enumerate(zip(t["callouts_bad"], t["callouts_good"])))
    return f'''<figure class="peek" data-peek aria-labelledby="peek-cap">
<div class="peek-top"><figcaption id="peek-cap">{esc(t["mock_caption"])}</figcaption>
<div class="seg js-only" role="group" aria-label="{esc(t["mock_show"])}">
<button type="button" data-mode="bad" aria-pressed="true">{esc(t["mock_bad"])}</button>
<button type="button" data-mode="good" aria-pressed="false">{esc(t["mock_good"])}</button>
</div></div>
{mock}
<ol class="callouts">{lis}</ol>
</figure>'''


def demo(t):
    before, after = t["demo_items_before"], t["demo_items_after"]
    sw = "".join(f'<span class="st-sw" data-i="{i + 1}" style="background:{c}"></span>' for i, c in enumerate(SWATCHES))
    static = "".join(
        f'<div class="ds-col ds-{k}"><p class="ds-h">{icon("cross" if k == "before" else "check")}{esc(t["demo_" + k])}</p>'
        f'<p class="ds-says">{esc(t["demo_says"])}:</p><ol>{"".join(f"<li>“{esc(x)}”</li>" for x in items)}</ol>'
        f'<p class="ds-verdict">{esc(t["demo_stuck"] if k == "before" else t["demo_ok"])}</p></div>'
        for k, items in (("before", before), ("after", after)))
    data = esc(json.dumps({"before": before, "after": after, "lb": t["demo_before"], "la": t["demo_after"],
                           "stuck": t["demo_stuck"], "ok": t["demo_ok"], "pause": t["demo_pause"], "play": t["demo_play"]},
                          ensure_ascii=False))
    return f'''<div class="demo" data-demo="{data}">
<div class="demo-bar">
<p class="demo-phase"><span class="demo-dot" aria-hidden="true"></span><span class="demo-phase-t">{esc(t["demo_before"])}</span></p>
<button type="button" class="demo-toggle">{icon("pause", "ico ico-pause")}{icon("play", "ico ico-play")}<span class="demo-toggle-t">{esc(t["demo_pause"])}</span></button>
</div>
<div class="demo-live" aria-hidden="true">
<div class="stage">
<div class="st-img" data-i="0"><span class="st-cushion"></span></div>
<div class="st-info">
<p class="st-title">{esc(t["mock_product"])}</p><p class="st-price">{esc(t["mock_price"])}</p>
<div class="st-sws">{sw}</div>
<span class="st-buy" data-i="4">{icon("cart")}<span class="st-buy-t">{esc(t["mock_btn"])}</span></span>
</div>
</div>
<div class="caption">{icon("voice")}<span class="cap-l">{esc(t["demo_says"])}</span><span class="cap-t">“{esc(before[0])}”</span></div>
<p class="verdict"></p>
</div>
<div class="demo-static">{static}</div>
</div>'''


SCRIPT = r'''<script>
(function(){
  var reduce=window.matchMedia&&window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  // URL form: build a friendly mailto message
  var f=document.querySelector("form.check-form");
  if(f){
    f.noValidate=true;
    var input=f.querySelector("input[name=body]"),err=f.querySelector(".form-error"),st=f.querySelector(".form-status");
    f.addEventListener("submit",function(e){
      e.preventDefault();
      var v=input.value.trim();
      if(!/^[^\s]+\.[a-z]{2,}/i.test(v.replace(/^https?:\/\//i,""))){
        err.textContent=f.getAttribute("data-err");input.setAttribute("aria-invalid","true");st.textContent="";input.focus();return;
      }
      err.textContent="";input.removeAttribute("aria-invalid");
      st.textContent=f.getAttribute("data-sent");
      window.location.href="mailto:"+f.getAttribute("data-to")+"?subject="+encodeURIComponent(f.getAttribute("data-subject"))+"&body="+encodeURIComponent(f.getAttribute("data-body").replace("{url}",v));
    });
    var links=document.querySelectorAll('a[href="#check"]');
    for(var j=0;j<links.length;j++){links[j].addEventListener("click",function(){setTimeout(function(){input.focus({preventScroll:true});},reduce?0:450);});}
  }
  // Hero illustration: Problems / Fixed toggle
  var peek=document.querySelector("[data-peek]");
  if(peek){
    var bs=peek.querySelectorAll(".seg button");
    for(var b=0;b<bs.length;b++){bs[b].addEventListener("click",function(){
      for(var k=0;k<bs.length;k++){bs[k].setAttribute("aria-pressed",bs[k]===this?"true":"false");}
      peek.classList.toggle("is-good",this.getAttribute("data-mode")==="good");
    });}
  }
  // Reveal on scroll
  var rv=document.querySelectorAll(".rv");
  if(!reduce&&"IntersectionObserver" in window){
    var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add("in");io.unobserve(e.target);}});},{rootMargin:"0px 0px -8% 0px"});
    for(var r=0;r<rv.length;r++){io.observe(rv[r]);}
  }else{for(var r2=0;r2<rv.length;r2++){rv[r2].classList.add("in");}}
  // Screen reader demo (static before/after stays for reduced motion and as text for assistive tech)
  var d=document.querySelector("[data-demo]");
  if(d&&!reduce){
    var cfg=JSON.parse(d.getAttribute("data-demo")),steps=[],phase=d.querySelector(".demo-phase-t"),
        cap=d.querySelector(".cap-t"),verdict=d.querySelector(".verdict"),btn=d.querySelector(".demo-toggle"),
        bt=d.querySelector(".demo-toggle-t"),els=d.querySelectorAll("[data-i]"),pos=0,timer=null,playing=false;
    ["before","after"].forEach(function(p){
      for(var i=0;i<5;i++){steps.push({p:p,i:i,t:1500});}
      steps.push({p:p,i:-1,t:2600});
    });
    function show(s){
      d.classList.toggle("phase-after",s.p==="after");
      phase.textContent=s.p==="after"?cfg.la:cfg.lb;
      for(var k=0;k<els.length;k++){els[k].classList.toggle("sr-on",+els[k].getAttribute("data-i")===s.i);}
      if(s.i>=0){cap.textContent="\u201c"+cfg[s.p][s.i]+"\u201d";verdict.textContent="";verdict.className="verdict";}
      else{verdict.textContent=s.p==="after"?cfg.ok:cfg.stuck;verdict.className="verdict "+(s.p==="after"?"ok":"bad");}
    }
    function tick(){show(steps[pos]);timer=setTimeout(function(){pos=(pos+1)%steps.length;tick();},steps[pos].t);}
    function play(){if(playing)return;playing=true;d.classList.remove("paused");bt.textContent=cfg.pause;tick();}
    function pause(){playing=false;clearTimeout(timer);d.classList.add("paused");bt.textContent=cfg.play;}
    d.classList.add("animating");show(steps[0]);
    btn.addEventListener("click",function(){playing?pause():play();});
    if("IntersectionObserver" in window){
      var started=false,dio=new IntersectionObserver(function(es){if(es[0].isIntersecting&&!started){started=true;play();}},{threshold:0.35});
      dio.observe(d);
    }else{play();}
  }
})();
</script>'''


def fr_typo(doc):
    """French typography: non-breaking space before ? ! : ; and » after «, and inside amounts. Skips script/style/pre."""
    parts = re.split(r"(<script.*?</script>|<style.*?</style>|<pre.*?</pre>)", doc, flags=re.S)
    for i in range(0, len(parts), 2):
        parts[i] = re.sub(r" ([?!:;»])", "\u00a0\\1", parts[i])
        parts[i] = re.sub(r"« ", "«\u00a0", parts[i])
        parts[i] = re.sub(r"(\d) €", "\\1\u00a0€", parts[i])
        parts[i] = re.sub(r"(\d) (\d{3})", "\\1\u00a0\\2", parts[i])
    return "".join(parts)


def page(lang):
    t = T[lang]
    alts = "\n".join(f'<link rel="alternate" hreflang="{l}" href="{BASE}{path_for(l)}">' for l in LANGS)
    alts += f'\n<link rel="alternate" hreflang="x-default" href="{BASE}/">'
    langnav = "".join(
        f'<li><a href="{path_for(l)}" hreflang="{l}" lang="{l}"' + (' aria-current="page"' if l == lang else "") +
        f'><span aria-hidden="true">{l.upper()}</span><span class="sr">{esc(T[l]["lang_name"])}</span></a></li>' for l in LANGS)
    nav = "".join(f'<li><a href="#{a}">{esc(label)}</a></li>' for a, label in t["nav"])
    note = "".join(f"<li>{icon('check', 'ico tick')}{esc(x)}</li>" for x in t["cta_note"])
    stats = "".join(
        f'<div class="stat"><p class="stat-n">{f"<small>{esc(pre)}</small> " if pre else ""}{esc(n)}</p>'
        f'<p class="stat-t">{esc(txt)}</p><p class="stat-s">{esc(t["src_label"])} <a href="{u}" rel="noopener">{esc(s)}</a></p></div>'
        for pre, n, txt, s, u in t["stats"])
    trust = "".join(f"<li>{icon(i)}<span>{esc(x)}</span></li>" for i, x in zip(TRUST_ICONS, t["trust"]))
    law = "".join(f"<li>{icon('scale', 'ico li-ico')}<span>{esc(x)}</span></li>" for x in t["law"])
    stakes = "".join(f"<li>{icon('arrow', 'ico li-ico')}<span>{esc(x)}</span></li>" for x in t["stakes"])
    checks = "".join(f'<li class="chk rv"><span class="icon-tile">{icon(i)}</span><div><h3>{esc(h)}</h3><p>{esc(p)}</p></div></li>'
                     for i, h, p in t["checks"])

    main_pk, side_pk = "", ""
    for p in t["packages"]:
        lis = "".join(f"<li>{icon('check', 'ico tick')}<span>{esc(x)}</span></li>" for x in p["items"])
        kind = p["kind"]
        badge = {"free": f'<p class="badge badge-free">{esc(t["badge_free"])}</p>',
                 "rec": f'<p class="badge">{esc(t["badge_rec"])}</p>'}.get(kind, "")
        time = f'<p class="pk-time">{icon("clock")}{esc(p["time"])}</p>' if p["time"] else ""
        cta = ""
        if kind == "free":
            cta = (f'<p class="pk-assure">{icon("shield")}<span>{esc(t["pk_free_note"])}</span></p>'
                   f'<a class="btn btn-primary btn-block" href="#check">{esc(p["cta"])}</a>')
        elif kind == "rec":
            cta = f'<a class="btn btn-ghost btn-block" href="{mailto(p["subject"])}">{esc(p["cta"])}</a>'
        card = (f'<div class="card pk pk-{kind or "plain"} rv">{badge}<h3>{esc(p["name"])}</h3>'
                f'<p class="price">{esc(p["price"])} <small>{esc(p["per"])}</small></p>'
                f'<p class="pk-desc">{esc(p["desc"])}</p>{time}<ul class="ticks">{lis}</ul>{cta}</div>')
        if kind:
            main_pk += card
        else:
            side_pk += card

    steps = "".join(f'<li class="rv"><h3>{esc(h)}</h3><p>{esc(p)}</p></li>' for h, p in t["steps"])
    about_p = "".join(f"<p>{esc(p)}</p>" for p in t["about_p"])

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
        cols += f'<div class="card cmp{" cmp-ours" if c.get("ours") else ""} rv"><h3>{esc(c["name"])}</h3><dl>{rows}</dl></div>'

    faq = "".join(f'<details class="rv"><summary>{esc(q)}</summary><p>{esc(a)}</p></details>' for q, a in t["faq"])
    code = esc(t["f_code"])

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
<script>document.documentElement.className+=" js";</script>
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
<h1 id="h1">{esc(t["h1"])}</h1>
<p class="lead">{esc(t["lead"])}</p>
<div class="stats">{stats}</div>
<a class="btn btn-accent btn-lg" href="#check">{esc(t["cta"])}{icon("down", "ico btn-ico")}</a>
<ul class="cta-note">{note}</ul>
</div>
<div class="hero-visual">{hero_mock(t)}</div>
</div>
<ul class="trust" aria-label="{esc(t["trust_label"])}">{trust}</ul>
</div></section>

<section class="alt" aria-labelledby="law-h"><div class="wrap">
<div class="law-grid">
<div class="law-box rv"><h2 id="law-h">{esc(t["law_h"])}</h2><ul class="li-list">{law}</ul>
<p class="src-note">{esc(t["src_label"])} <a href="{EAA}" rel="noopener">{esc(t["law_src"])}</a></p></div>
<div class="law-box stake rv"><h2>{esc(t["stake_h"])}</h2><ul class="li-list">{stakes}</ul>
<a class="text-cta" href="#check">{esc(t["cta"])}{icon("arrow", "ico")}</a></div>
</div>
</div></section>

<section id="example" aria-labelledby="ex-h"><div class="wrap">
<h2 id="ex-h" class="rv">{esc(t["ex_h"])}</h2>
<p class="section-lead rv">{esc(t["ex_p"])}</p>
<div class="report rv">
<div class="report-head"><span class="report-mark" aria-hidden="true">{LOGO}</span><p class="report-title">{esc(t["report_title"])}</p></div>
<div class="report-body">
{demo(t)}
<article class="finding" aria-labelledby="f-h">
<div class="finding-top"><h3 id="f-h">{esc(t["f_title"])}</h3><p class="finding-meta"><span class="sr">{esc(t["lbl_sev"])}: </span>{sev_chip(t)}<span class="wcag">{esc(t["f_wcag"])}</span></p></div>
<dl class="finding-grid">
<div><dt>{esc(t["lbl_problem"])}</dt><dd>{esc(t["f_problem"])}</dd></div>
<div><dt>{esc(t["lbl_who"])}</dt><dd>{esc(t["f_who"])}</dd></div>
<div class="fix"><dt>{esc(t["lbl_fix"])}</dt><dd>{esc(t["f_fix"])}<pre><code>{code}</code></pre></dd></div>
</dl>
</article>
</div>
</div>
<p class="note">{esc(t["ex_note"])}</p>
</div></section>

<section class="alt" aria-labelledby="what-h"><div class="wrap">
<h2 id="what-h" class="rv">{esc(t["what_h"])}</h2>
<ul class="checks">{checks}</ul>
</div></section>

<section id="packages" aria-labelledby="pk-h"><div class="wrap">
<h2 id="pk-h" class="rv">{esc(t["pk_h"])}</h2>
<p class="section-lead rv">{esc(t["pk_p"])}</p>
<div class="pk-main">{main_pk}</div>
<div class="pk-side">{side_pk}</div>
<p class="note">{esc(t["pk_note"])}</p>
</div></section>

<section class="alt" aria-labelledby="how-h"><div class="wrap">
<h2 id="how-h" class="rv">{esc(t["how_h"])}</h2>
<ol class="steps">{steps}</ol>
</div></section>

<section id="about" aria-labelledby="about-h"><div class="wrap">
<div class="about rv">
<img src="/ivan.jpg" width="480" height="480" alt="{esc(t["photo_alt"])}" decoding="async">
<div class="about-text">
<h2 id="about-h">{esc(t["about_h"])}</h2>
<p class="about-role"><strong>Ivan Raylyan</strong> · {esc(t["about_role"])}</p>
{about_p}
<p class="about-li"><a href="{LINKEDIN}" rel="noopener">{icon("linkedin")}<span>{esc(t["linkedin"])}</span></a></p>
</div>
</div>
</div></section>

<section class="alt" aria-labelledby="cmp-h"><div class="wrap">
<h2 id="cmp-h" class="rv">{esc(t["cmp_h"])}</h2>
<div class="grid-3">{cols}</div>
</div></section>

<section id="faq" aria-labelledby="faq-h"><div class="wrap narrow">
<h2 id="faq-h" class="rv">{esc(t["faq_h"])}</h2>
{faq}
</div></section>

<section id="check" class="check" aria-labelledby="check-h"><div class="wrap">
<div class="check-box rv">
<h2 id="check-h">{esc(t["check_h"])}</h2>
<p class="check-p">{esc(t["check_p"])}</p>
{check_form(t)}
<p class="contact">{esc(t["contact"])} <a href="{mailto(t["mail_subject"])}">{EMAIL}</a></p>
</div>
</div></section>
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


def main():
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir()
    for lang in LANGS:
        d = OUT if lang == "en" else OUT / lang
        d.mkdir(exist_ok=True)
        (d / "index.html").write_text(page(lang))
    shutil.copy(ROOT / "src/style.css", OUT / "style.css")
    for f in (ROOT / "src").glob("*.svg"):
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
