"""Shape a string with HarfBuzz and emit outlined SVG path data."""
import io, os
from fontTools.ttLib import TTFont
from fontTools.varLib import instancer
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.boundsPen import BoundsPen
from fontTools.misc.transform import Transform
import uharfbuzz as hb

_cache = {}

def load(path, **axes):
    key = (path, tuple(sorted(axes.items())))
    if key in _cache: return _cache[key]
    f = TTFont(path)
    if "fvar" in f:
        f = instancer.instantiateVariableFont(f, axes, inplace=False, updateFontNames=False)
    buf = io.BytesIO(); f.save(buf); data = buf.getvalue()
    face = hb.Face(data); font = hb.Font(face)
    _cache[key] = (f, data, font)
    return _cache[key]

def shape(text, path, tracking=0.0, **axes):
    """tracking in 1/1000 em. Returns (glyphs, upem, advance_total)."""
    tt, data, hbfont = load(path, **axes)
    upem = tt["head"].unitsPerEm
    buf = hb.Buffer(); buf.add_str(text); buf.guess_segment_properties()
    hb.shape(hbfont, buf, {"kern": True, "liga": True})
    order = tt.getGlyphOrder()
    out, x = [], 0.0
    track = tracking / 1000.0 * upem
    for info, pos in zip(buf.glyph_infos, buf.glyph_positions):
        out.append({"name": order[info.codepoint],
                    "x": x + pos.x_offset, "y": pos.y_offset})
        x += pos.x_advance + track
    # trailing tracking must NOT count toward the width (this is the classic
    # letterspaced-and-looks-off-centre bug)
    total = x - track if text else 0.0
    return out, upem, total, tt

def outline(text, path, cap_height=None, font_size=None, tracking=0.0,
            x=0.0, y=0.0, decimals=2, **axes):
    """Emit SVG path 'd' for `text`, positioned with baseline origin at (x, y),
    y growing DOWN (SVG convention). Scale by cap_height or font_size."""
    glyphs, upem, adv, tt = shape(text, path, tracking, **axes)
    cap = tt["OS/2"].sCapHeight if hasattr(tt["OS/2"], "sCapHeight") and tt["OS/2"].sCapHeight else None
    if cap_height is not None:
        if not cap:  # derive from H
            bp = BoundsPen(tt.getGlyphSet()); tt.getGlyphSet()["H"].draw(bp); cap = bp.bounds[3]
        s = cap_height / cap
    else:
        s = font_size / upem
    gs = tt.getGlyphSet()
    parts = []
    for g in glyphs:
        pen = SVGPathPen(gs, ntos=lambda v: str(round(v, decimals)).rstrip("0").rstrip("."))
        t = Transform(s, 0, 0, -s, x + g["x"] * s, y - g["y"] * s)
        gs[g["name"]].draw(TransformPen(pen, t))
        d = pen.getCommands()
        if d: parts.append(d)
    # ink bounds
    bp = BoundsPen(gs); mnx=mny=1e9; mxx=mxy=-1e9
    for g in glyphs:
        b = BoundsPen(gs); gs[g["name"]].draw(b)
        if not b.bounds: continue
        x0,y0,x1,y1 = b.bounds
        mnx=min(mnx,x0+g["x"]); mxx=max(mxx,x1+g["x"])
        mny=min(mny,y0+g["y"]); mxy=max(mxy,y1+g["y"])
    ink = {"x0": x+mnx*s, "x1": x+mxx*s, "y0": y-mxy*s, "y1": y-mny*s,
           "w": (mxx-mnx)*s, "h": (mxy-mny)*s}
    return {"d": " ".join(parts), "advance": adv*s, "ink": ink, "scale": s, "upem": upem}
