#!/usr/bin/env python3
"""Assemble the three MontiCare homepage prototypes into one presentable file."""
import json, os, re, base64, subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
P    = lambda n: open(f"{HERE}/parts/{n}").read()


def prepare():
    """Regenerate the derived caches from source, so a fresh clone just works.

    parts/logo.json  <- brand/out/monticare-wordmark-positive.svg
    parts/images.json <- site/img/*.webp
    """
    svg = open(f"{HERE}/../brand/out/monticare-wordmark-positive.svg").read()
    paths = re.findall(r'<path fill="(#[0-9A-Fa-f]{6})" d="([^"]+)"/>', svg)
    json.dump({"viewBox":   re.search(r'viewBox="([^"]+)"', svg).group(1),
               "transform": re.search(r'<g transform="([^"]+)"', svg).group(1),
               "monti": paths[0][1], "care": paths[1][1], "tag": paths[2][1]},
              open(f"{HERE}/parts/logo.json", "w"))
    imgs = {}
    for f in sorted(os.listdir(f"{HERE}/img")):
        if f.endswith(".webp"):
            imgs[f[:-5]] = base64.b64encode(open(f"{HERE}/img/{f}", "rb").read()).decode()
    json.dump(imgs, open(f"{HERE}/parts/images.json", "w"))


prepare()
LOGO = json.load(open(f"{HERE}/parts/logo.json"))
IMGS = json.load(open(f"{HERE}/parts/images.json"))

IMG_TOKENS = "\n".join(
    f'  --img-{k}:url("data:image/webp;base64,{v}");' for k, v in sorted(IMGS.items()))

FOOTER = """
<footer class="ftr">
  <div class="wrap">
    <div class="ftr-grid">
      <div>
        <svg viewBox="0 0 690.18 234.25" style="height:38px;width:auto" role="img">
          <title>MontiCare</title><use href="#mc-monti-neg"/><use href="#mc-care-neg"/><use href="#mc-tag-neg"/></svg>
        <p style="margin-top:18px;max-width:38ch;font-size:15.5px;line-height:1.6">
          Registered NDIS provider delivering in-home, community and high intensity
          complex care across Brisbane, Moreton Bay and the Sunshine Coast.</p>
      </div>
      <div>
        <h3>Get in touch</h3>
        <p style="font-size:15.5px;line-height:2">
          <a href="tel:0447334958">0447 334 958</a><br>
          <a href="mailto:admin@purposesupportprogram.com.au">admin@purposesupportprogram.com.au</a><br>
          12 Thomson Street<br>Burpengary East QLD 4505</p>
      </div>
      <div>
        <h3>Supports</h3>
        <p style="font-size:15.5px;line-height:2">
          High intensity &amp; complex care<br>In-home support<br>Domestic assistance<br>
          Community access<br>Transport<br>Daily living support</p>
      </div>
    </div>
    <div class="ftr-base">
      <span>&copy; 2026 MontiCare. NDIS registration number to be displayed here.</span>
      <span><a href="#">Privacy policy</a> &nbsp;&middot;&nbsp; <a href="#">Feedback &amp; complaints</a></span>
    </div>
  </div>
</footer>
"""

# the outlines are authored in badge coordinates; the flat wordmark carries a
# translate to bring them back to its own viewBox. Bake it into each symbol.
T = LOGO["transform"]
SYMBOLS = f"""
<svg width="0" height="0" style="position:absolute" aria-hidden="true" focusable="false"><defs>
  <g id="mc-monti"><path transform="{T}" fill="#4A5560" d="{LOGO['monti']}"/></g>
  <g id="mc-care"><path transform="{T}" fill="#1A847F" d="{LOGO['care']}"/></g>
  <g id="mc-tag"><path transform="{T}" fill="#65707C" d="{LOGO['tag']}"/></g>
  <g id="mc-monti-neg"><path transform="{T}" fill="#FFFFFF" d="{LOGO['monti']}"/></g>
  <g id="mc-care-neg"><path transform="{T}" fill="#A9D5D1" d="{LOGO['care']}"/></g>
  <g id="mc-tag-neg"><path transform="{T}" fill="#B6BFC8" d="{LOGO['tag']}"/></g>
</defs></svg>
"""

SWITCH_CSS = """
/* ---- presentation switcher: a tool, not part of any prototype ---- */
.sw{position:fixed;left:50%;bottom:18px;transform:translateX(-50%);z-index:300;
    display:flex;align-items:center;gap:5px;padding:6px;border-radius:999px;
    background:rgba(20,28,36,.93);backdrop-filter:blur(12px) saturate(1.5);
    box-shadow:0 6px 14px rgba(0,0,0,.18),0 22px 50px rgba(0,0,0,.30);
    font-family:var(--font);max-width:calc(100vw - 24px)}
.sw button{appearance:none;border:0;cursor:pointer;font:inherit;font-weight:650;
  font-size:14px;color:#C7D2DC;background:none;padding:11px 17px;border-radius:999px;
  min-height:44px;white-space:nowrap;transition:color .18s var(--ease),background .18s var(--ease)}
.sw button:hover{color:#fff;background:rgba(255,255,255,.09)}
.sw button[aria-pressed="true"]{background:#fff;color:#141C24}
.sw .swlab{color:#7E8B98;font-size:11.5px;font-weight:700;letter-spacing:.13em;
  text-transform:uppercase;padding:0 12px 0 14px;white-space:nowrap}
.sw-hide{position:fixed;right:16px;bottom:18px;z-index:300;width:44px;height:44px;
  border-radius:50%;border:0;cursor:pointer;background:rgba(20,28,36,.93);color:#C7D2DC;
  display:grid;place-items:center;box-shadow:0 6px 14px rgba(0,0,0,.18)}
.sw-hide:hover{color:#fff}
body.sw-off .sw{display:none}
@media(max-width:620px){.sw .swlab{display:none}.sw button{padding:11px 13px;font-size:13.5px}}
@media print{.sw,.sw-hide{display:none}}
.proto[hidden]{display:none}
"""

JS = """
var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

/* ---- switcher ---- */
(function(){
  var order=['a','b','c'];
  var btns=[].slice.call(document.querySelectorAll('.sw button[data-go]'));
  function show(id){
    order.forEach(function(k){
      var s=document.getElementById('proto-'+k);
      if(s) s.hidden = (k!==id);
    });
    btns.forEach(function(b){ b.setAttribute('aria-pressed', String(b.dataset.go===id)); });
    try{ localStorage.setItem('mc-proto', id); }catch(e){}
    window.scrollTo(0,0);
    boot();
  }
  btns.forEach(function(b){ b.addEventListener('click', function(){ show(b.dataset.go); }); });
  // ?p=b or #b deep-links a concept, so a single one can be shared or captured
  var q=(location.search.match(/[?&]p=([abc])/)||[])[1];
  var h=(location.hash.match(/^#(?:proto-)?([abc])$/)||[])[1];
  var saved=null; try{ saved=localStorage.getItem('mc-proto'); }catch(e){}
  show(q||h||(order.indexOf(saved)>-1?saved:'a'));

  var hide=document.querySelector('.sw-hide');
  hide.addEventListener('click', function(){
    document.body.classList.toggle('sw-off');
    var off=document.body.classList.contains('sw-off');
    hide.setAttribute('aria-label', off?'Show prototype switcher':'Hide prototype switcher');
    hide.setAttribute('aria-pressed', String(off));
  });
})();

/* ---- one authored moment: content rises as it arrives. Never hides content. ---- */
var failsafe=null;
/* Content safety only. The spine's fill is scroll-driven decoration and must not
   be forced here, or the draw never happens. */
function revealContent(){
  [].forEach.call(document.querySelectorAll('.rise, .c-stop, .at-stop'), function(el){
    el.classList.add('in'); });
}
function boot(){
  if(failsafe) clearTimeout(failsafe);
  if(reduce){
    revealContent();
    [].forEach.call(document.querySelectorAll('.c-line, .at-line'), function(l){
      l.style.setProperty('--fill','1'); });
    return;
  }
  var els=[].slice.call(document.querySelectorAll('.proto:not([hidden]) .rise'));
  var io=new IntersectionObserver(function(es){
    es.forEach(function(e){
      if(e.isIntersecting){ e.target.classList.add('in'); io.unobserve(e.target); }
    });
  }, {rootMargin:'0px 0px -10% 0px', threshold:0.1});
  var vh=window.innerHeight, armed=0;
  els.forEach(function(el){
    if(el.getBoundingClientRect().top < vh*0.94){ el.classList.add('in'); return; }
    el.classList.add('armed');
    el.style.transitionDelay=(Math.min(armed++,6)*55)+'ms';
    io.observe(el);
  });
  // if anything goes wrong with the observer, the page still shows its content
  failsafe=setTimeout(revealContent, 2500);
  rail();
}

/* ---- the spine fills as you travel down it (concepts A and C) ---- */
var railHandler=null;
function rail(){
  if(railHandler){ window.removeEventListener('scroll', railHandler);
                   window.removeEventListener('resize', railHandler); railHandler=null; }
  var rails=[].slice.call(document.querySelectorAll('.proto:not([hidden]) [data-rail]'));
  if(!rails.length) return;
  var parts=rails.map(function(wrap){
    return { wrap: wrap,
             line: wrap.querySelector('.c-line, .at-line'),
             stops: [].slice.call(wrap.querySelectorAll('.c-stop, .at-stop')) };
  });
  function draw(){
    var anchor=window.innerHeight*0.55;
    parts.forEach(function(p){
      var r=p.wrap.getBoundingClientRect();
      var frac=(anchor-r.top)/r.height;
      // setProperty needs a string; a bare number is silently ignored for custom props
      if(p.line) p.line.style.setProperty('--fill', String(Math.max(0,Math.min(1,frac))));
      p.stops.forEach(function(s){
        if(s.getBoundingClientRect().top < anchor) s.classList.add('in');
      });
    });
  }
  // draw() reads a handful of rects and writes one custom property. Calling it
  // straight from a passive listener is cheap and, unlike a rAF latch or a clock
  // throttle, has nothing that can stick and leave the spine frozen.
  railHandler=draw;
  window.addEventListener('scroll', railHandler, {passive:true});
  window.addEventListener('resize', railHandler, {passive:true});
  // Belt and braces: each stage also nudges the spine as it comes into view, so
  // the fill still advances if scroll events are being throttled or coalesced.
  if(typeof IntersectionObserver==='function'){
    var sio=new IntersectionObserver(draw, {rootMargin:'0px 0px -45% 0px', threshold:[0,.25,.5,1]});
    parts.forEach(function(p){ p.stops.forEach(function(st){ sio.observe(st); }); });
  }
  draw();
}

/* ---- mobile menu ---- */
document.addEventListener('click', function(e){
  var b=e.target.closest('.menu-btn');
  if(b){
    var panel=document.getElementById(b.getAttribute('aria-controls'));
    var open=panel.getAttribute('data-open')==='true';
    panel.setAttribute('data-open', String(!open));
    b.setAttribute('aria-expanded', String(!open));
    return;
  }
  var link=e.target.closest('.menu-panel a');
  if(link){
    var pnl=link.closest('.menu-panel');
    pnl.setAttribute('data-open','false');
    var ctrl=document.querySelector('[aria-controls="'+pnl.id+'"]');
    if(ctrl) ctrl.setAttribute('aria-expanded','false');
  }
});
document.addEventListener('keydown', function(e){
  if(e.key!=='Escape') return;
  [].forEach.call(document.querySelectorAll('.menu-panel[data-open="true"]'), function(pnl){
    pnl.setAttribute('data-open','false');
    var ctrl=document.querySelector('[aria-controls="'+pnl.id+'"]');
    if(ctrl){ ctrl.setAttribute('aria-expanded','false'); ctrl.focus(); }
  });
});

/* ---- prototype A doors ---- */
document.addEventListener('click', function(e){
  var b=e.target.closest('.a-dbtn'); if(!b) return;
  var door=b.closest('.a-door');
  var open=door.getAttribute('data-open')==='true';
  [].forEach.call(document.querySelectorAll('.a-door'), function(d){
    d.setAttribute('data-open','false');
    d.querySelector('.a-dbtn').setAttribute('aria-expanded','false');
  });
  if(!open){ door.setAttribute('data-open','true'); b.setAttribute('aria-expanded','true'); }
});
"""

SWITCHER = """
<div class="sw" role="group" aria-label="Prototype switcher">
  <span class="swlab">Concept</span>
  <button data-go="a" aria-pressed="true">A &middot; Front Door</button>
  <button data-go="b" aria-pressed="false">B &middot; Capability</button>
  <button data-go="c" aria-pressed="false">C &middot; The Path</button>
</div>
<button class="sw-hide" aria-label="Hide prototype switcher" aria-pressed="false">
  <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"><path d="M2 12s3.6-7 10-7 10 7 10 7-3.6 7-10 7-10-7-10-7Z"/><circle cx="12" cy="12" r="3"/><path d="m3 3 18 18"/></svg>
</button>
"""

html = f"""<meta charset="utf-8">
<title>MontiCare — three homepage concepts</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Public+Sans:wght@400;500;600;700;800&display=swap">
<style>
:root{{
{IMG_TOKENS}
}}
{P('base.css')}
{SWITCH_CSS}
</style>
{SYMBOLS}
<div class="proto" id="proto-a">{P('a.html')}{FOOTER}</div>
<div class="proto" id="proto-b" hidden>{P('b.html')}{FOOTER}</div>
<div class="proto" id="proto-c" hidden>{P('c.html')}{FOOTER}</div>
{SWITCHER}
<script>{JS}</script>
"""

out = f"{HERE}/../monticare-homepages.html"
open(out, "w").write(html)
print(f"  {os.path.basename(out)}  {len(html)/1024/1024:.2f} MB")

# ============================================================
#  Standalone single-concept build — a real page, no switcher
# ============================================================
CONCEPT_META = {
    "a": ("MontiCare — NDIS support across Brisbane, Moreton Bay and the Sunshine Coast",
          "Registered NDIS provider in Burpengary East. In-home support, community "
          "access and high-intensity complex care."),
    "b": ("MontiCare — high intensity and complex NDIS care",
          "Registered NDIS provider delivering complex care across Brisbane, Moreton "
          "Bay and the Sunshine Coast."),
    "c": ("MontiCare — NDIS support at home and in the community",
          "Registered NDIS provider in Burpengary East. Ring us and here is exactly "
          "what happens next."),
}

def build_standalone(key):
    body = P(f"{key}.html") + FOOTER
    used = sorted(set(re.findall(r"var\(--img-([a-z0-9-]+)\)", body)))
    tokens = "\n".join(
        f'  --img-{k}:url("data:image/webp;base64,{IMGS[k]}");' for k in used if k in IMGS)
    title, desc = CONCEPT_META[key]
    js = JS.split("/* ---- one authored moment", 1)[1]
    js = "/* ---- one authored moment" + js          # drop the switcher block
    js = ("var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;\n"
          + js + "\nboot();\n")
    doc = f"""<!doctype html>
<html lang="en-AU">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Public+Sans:wght@400;500;600;700;800&display=swap">
<style>
:root{{
{tokens}
}}
{P('base.css')}
</style>
</head>
<body>
{SYMBOLS}
<div class="proto" id="proto-{key}">{body}</div>
<script>{js}</script>
</body>
</html>
"""
    out = f"{HERE}/../monticare-concept-{key}.html"
    open(out, "w").write(doc)
    print(f"  {os.path.basename(out)}  {len(doc)/1024/1024:.2f} MB  ({len(used)} images)")

import sys
if "--only" in sys.argv:
    for k in sys.argv[sys.argv.index("--only") + 1].split(","):
        build_standalone(k.strip())
