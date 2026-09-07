"""MontiCare logo generator — outlines Public Sans (SIL OFL) to paths.
Re-runnable: edit the constants, re-run, the whole family regenerates."""
import sys, os, json
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from type2path import outline, shape

FONT = os.path.join(HERE, "fonts", "PublicSans.ttf")
AXW  = {"wght": 700}     # wordmark
AXT  = {"wght": 600}     # tagline

P = dict(
    aqua900="#005B57", aqua700="#1A847F", aqua500="#46A49E", aqua400="#80BFBA",
    aqua300="#A9D5D1", aqua100="#D6ECEA", aqua50="#E7F5F4",
    grey900="#1B252F", grey700="#4A5560", grey600="#65707C", grey500="#7D8892",
    grey300="#B6BFC8", grey200="#D5DCE2", grey100="#E8EDF3", grey50="#F3F7FB",
    white="#FFFFFF", black="#000000",
)

D          = 1024.0
WORD_W     = 0.67400 * D    # 690.18  wordmark ink width  (source proportion kept)
TAG_CAP    = 0.02930 * D    #  30.00  tagline cap height
GAP        = 0.09766 * D    # 100.00  wordmark baseline -> tagline cap top
RING_W     = 0.01563 * D    #  16.00  ring stroke
BLOCK_DY   = 0.01563 * D    #  16.00  block dropped: balances top-heavy ink mass
OPTICAL_DX = 4.0            #  flat 'M' stem vs round 'e' terminal
TAG_FILL   = 0.72           #  tagline width as a fraction of the wordmark

def _solve_tracking(text, cap, target_w):
    lo, hi = 0.0, 900.0
    for _ in range(70):
        m = (lo + hi) / 2
        if outline(text, FONT, cap_height=cap, tracking=m, **AXT)["ink"]["w"] < target_w: lo = m
        else: hi = m
    return (lo + hi) / 2

def lockup(cx, cy):
    probe = outline("MontiCare", FONT, cap_height=100.0, **AXW)
    cap   = 100.0 * WORD_W / probe["ink"]["w"]
    block = cap + GAP + TAG_CAP
    top   = cy - block / 2.0 + BLOCK_DY
    base_w, base_t = top + cap, top + cap + GAP + TAG_CAP

    p  = outline("MontiCare", FONT, cap_height=cap, **AXW)
    x0 = cx - p["ink"]["w"] / 2.0 - p["ink"]["x0"] + OPTICAL_DX
    g, _, _, _ = shape("MontiCare", FONT, 0.0, **AXW)
    split = x0 + g[5]["x"] * p["scale"]                    # advance origin of 'C'
    monti = outline("Monti", FONT, cap_height=cap, x=x0,    y=base_w, **AXW)
    care  = outline("Care",  FONT, cap_height=cap, x=split, y=base_w, **AXW)

    tr = _solve_tracking("NDIS ELEVATED", TAG_CAP, WORD_W * TAG_FILL)
    tp = outline("NDIS ELEVATED", FONT, cap_height=TAG_CAP, tracking=tr, **AXT)
    xt = cx - tp["ink"]["w"] / 2.0 - tp["ink"]["x0"]
    tag = outline("NDIS ELEVATED", FONT, cap_height=TAG_CAP, tracking=tr, x=xt, y=base_t, **AXT)

    # the flat wordmark's viewBox must wrap the INK, not the cap line and baseline:
    # round letters (C, o, a, e) overshoot both, and a cap-to-baseline box clips them.
    ink_y0 = min(monti["ink"]["y0"], care["ink"]["y0"], tag["ink"]["y0"])
    ink_y1 = max(monti["ink"]["y1"], care["ink"]["y1"], tag["ink"]["y1"])
    ink_x0 = min(monti["ink"]["x0"], care["ink"]["x0"], tag["ink"]["x0"])
    ink_x1 = max(monti["ink"]["x1"], care["ink"]["x1"], tag["ink"]["x1"])
    return dict(monti=monti["d"], care=care["d"], tag=tag["d"], cap=cap, tracking=tr,
                x0=monti["ink"]["x0"], x1=care["ink"]["x1"], top=top, bottom=base_t,
                ink_x0=ink_x0, ink_x1=ink_x1, ink_y0=ink_y0, ink_y1=ink_y1,
                tag_x0=tag["ink"]["x0"], tag_x1=tag["ink"]["x1"], baseline=base_w)

L = lockup(D / 2, D / 2)

def _svg(body, w, h, label, desc):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w:g} {h:g}" '
            f'width="{w:g}" height="{h:g}" role="img" aria-label="{label}">'
            f'<title>{label}</title><desc>{desc}</desc>{body}</svg>\n')

LABEL = "MontiCare — NDIS Elevated"

def badge(fill, ring, monti, care, tag, desc, ring_w=RING_W):
    r = D / 2 - ring_w / 2
    b = (f'<circle cx="512" cy="512" r="{r:g}" fill="{fill}"'
         + (f' stroke="{ring}" stroke-width="{ring_w:g}"' if ring else '') + '/>'
         + f'<path fill="{monti}" d="{L["monti"]}"/><path fill="{care}" d="{L["care"]}"/>'
         + f'<path fill="{tag}" d="{L["tag"]}"/>')
    return _svg(b, D, D, LABEL, desc)

def wordmark(monti, care, tag, desc):
    x0, y0 = L["ink_x0"], L["ink_y0"]
    w, h = L["ink_x1"] - x0, L["ink_y1"] - y0
    b = (f'<g transform="translate({-x0:.2f} {-y0:.2f})">'
         f'<path fill="{monti}" d="{L["monti"]}"/><path fill="{care}" d="{L["care"]}"/>'
         f'<path fill="{tag}" d="{L["tag"]}"/></g>')
    return _svg(b, round(w, 2), round(h, 2), LABEL, desc)

def monogram(fill, ink, desc):
    m = outline("M", FONT, cap_height=D * 0.46, **AXW)
    x = D / 2 - m["ink"]["w"] / 2 - m["ink"]["x0"]
    y = D / 2 + (m["ink"]["y1"] - m["ink"]["y0"]) / 2
    m = outline("M", FONT, cap_height=D * 0.46, x=x, y=y, **AXW)
    b = f'<circle cx="512" cy="512" r="512" fill="{fill}"/><path fill="{ink}" d="{m["d"]}"/>'
    return _svg(b, D, D, "MontiCare", desc)

OUT = "brand/out"; os.makedirs(OUT, exist_ok=True)
FILES = {
 "monticare-badge-positive.svg":    badge(P["aqua50"],  P["aqua400"], P["grey700"], P["aqua700"], P["grey600"], "Primary badge, positive — light backgrounds."),
 "monticare-badge-negative.svg":    badge(P["grey900"], P["aqua700"], P["white"],   P["aqua300"], P["grey300"], "Primary badge, negative — dark backgrounds."),
 "monticare-badge-solid.svg":       badge(P["aqua700"], None,         P["white"],   P["white"],   P["white"],   "Solid aqua badge, single colour — social profiles and small sizes."),
 "monticare-wordmark-positive.svg": wordmark(P["grey700"], P["aqua700"], P["grey600"], "Primary stacked wordmark, positive."),
 "monticare-wordmark-negative.svg": wordmark(P["white"],   P["aqua300"], P["grey300"], "Primary stacked wordmark, negative."),
 "monticare-mono-black.svg":        wordmark(P["black"], P["black"], P["black"], "Single-colour black — forms, faxes, stamps, embroidery."),
 "monticare-mono-white.svg":        wordmark(P["white"], P["white"], P["white"], "Single-colour white — photography, dark print."),
 "monticare-favicon.svg":           monogram(P["aqua700"], P["white"], "Monogram favicon for the browser tab."),
}
for n, s in FILES.items(): open(os.path.join(OUT, n), "w").write(s)

spec = dict(diameter=D, wordmark_cap=round(L["cap"],2), wordmark_width=round(L["x1"]-L["x0"],2),
            tagline_cap=TAG_CAP, tagline_tracking=round(L["tracking"]), gap=GAP, ring=RING_W,
            block_dy=BLOCK_DY, optical_dx=OPTICAL_DX,
            wordmark_centre=round((L["x0"]+L["x1"])/2,2), tagline_centre=round((L["tag_x0"]+L["tag_x1"])/2,2),
            flat_viewbox=[round(L["ink_x1"]-L["ink_x0"],2), round(L["ink_y1"]-L["ink_y0"],2)],
            block_centre=round((L["top"]+L["bottom"])/2,2), palette=P)
json.dump(spec, open(os.path.join(OUT, "spec.json"), "w"), indent=2)
for f in ("_measure-lockup.svg","_measure-word.svg","_measure-tag.svg"):
    p=os.path.join(OUT,f)
    if os.path.exists(p): os.remove(p)
print(json.dumps({k: os.path.getsize(os.path.join(OUT,k)) for k in FILES}, indent=1))
print(f"\nwordmark centre {spec['wordmark_centre']}  tagline centre {spec['tagline_centre']}  block centre {spec['block_centre']}")
