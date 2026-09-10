"""Derive complete, contrast-checked token sets from the client's 7 new colours.

The supplied palette has no neutral and no pale ground, so body ink, rules and
section washes are derived from its own hues rather than invented.
"""
import json, math

def lin(v):
    v/=255.0
    return v/12.92 if v<=0.04045 else ((v+0.055)/1.055)**2.4
def L(c): r,g,b=[lin(x) for x in c]; return .2126*r+.7152*g+.0722*b
def cr(a,b):
    x,y=L(a),L(b); return (max(x,y)+.05)/(min(x,y)+.05)
def h(s): s=s.lstrip('#'); return tuple(int(s[i:i+2],16) for i in (0,2,4))
def hx(c): return "#%02X%02X%02X"%tuple(int(round(v)) for v in c)

def to_lab(rgb):
    r,g,b=[lin(v) for v in rgb]
    l=0.4122214708*r+0.5363325363*g+0.0514459929*b
    m=0.2119034982*r+0.6806995451*g+0.1073969566*b
    s=0.0883024619*r+0.2817188376*g+0.6299787005*b
    l_,m_,s_=l**(1/3),m**(1/3),s**(1/3)
    return (0.2104542553*l_+0.7936177850*m_-0.0040720468*s_,
            1.9779984951*l_-2.4285922050*m_+0.4505937099*s_,
            0.0259040371*l_+0.7827717662*m_-0.8086757660*s_)
def to_rgb(lab):
    Lv,A,B=lab
    l_=Lv+0.3963377774*A+0.2158037573*B; m_=Lv-0.1055613458*A-0.0638541728*B
    s_=Lv-0.0894841775*A-1.2914855480*B
    l,m,s=l_**3,m_**3,s_**3
    r= 4.0767416621*l-3.3077115913*m+0.2309699292*s
    g=-1.2684380046*l+2.6097574011*m-0.3413193965*s
    b=-0.0041960863*l-0.7034186147*m+1.7076147010*s
    def g8(v):
        v = 12.92*v if v<=0.0031308 else 1.055*(v**(1/2.4))-0.055
        return max(0.0,min(255.0,v*255))
    return tuple(g8(v) for v in (r,g,b))

def shift(hexs, lightness, chroma=1.0):
    Lv,A,B = to_lab(h(hexs))
    return hx(to_rgb((lightness, A*chroma, B*chroma)))

CLIENT = {"pink":"DEB7D5","mauve":"B783AA","indigo":"202544",
          "navy":"021428","deepteal":"0B3143","teal":"1D5864","lightteal":"4D909A"}

# Body ink: the palette offers no neutral, so it comes off the indigo, lifted
# until it reads as text rather than as a heading.
BODY  = shift("202544", 0.42, 0.85)
QUIET = shift("202544", 0.525, 0.75)
RULE  = shift("202544", 0.88, 0.35)
LINE  = shift("202544", 0.80, 0.40)
WASH_T = shift("1D5864", 0.965, 0.28)
TINT_T = shift("1D5864", 0.925, 0.34)
WASH_P = shift("B783AA", 0.965, 0.30)
TINT_P = shift("B783AA", 0.928, 0.36)
PAGE   = shift("202544", 0.975, 0.20)
# Section grounds. These carry most of the page's coloured surface, so they are
# what makes a scheme read as the new palette rather than as the old one.
SECT_T = shift("1D5864", 0.955, 0.45)
SECT_P = shift("B783AA", 0.955, 0.45)

TOKENS = {
  "body": BODY, "quiet": QUIET, "rule": RULE, "line": LINE,
  "wash_teal": WASH_T, "tint_teal": TINT_T,
  "wash_pink": WASH_P, "tint_pink": TINT_P, "page": PAGE,
  "sect_teal": SECT_T, "sect_pink": SECT_P,
  **{k:"#"+v for k,v in CLIENT.items()},
}

if __name__ == "__main__":
    W=(255,255,255)
    print("  derived neutrals and washes")
    for k in ("body","quiet","line","rule","page","wash_teal","tint_teal","wash_pink","tint_pink"):
        v=TOKENS[k]; print(f"    {k:11s} {v}   on white {cr(h(v),W):6.2f}:1")
    print("\n  text pairs that must clear AA")
    checks = [("body on white", BODY, "#FFFFFF"), ("body on page", BODY, PAGE),
              ("body on teal wash", BODY, WASH_T), ("body on pink wash", BODY, WASH_P),
              ("quiet on white", QUIET, "#FFFFFF"), ("quiet on teal wash", QUIET, WASH_T),
              ("teal link on white", "#1D5864", "#FFFFFF"),
              ("teal link on page", "#1D5864", PAGE),
              ("teal link on teal wash", "#1D5864", WASH_T),
              ("teal link on pink wash", "#1D5864", WASH_P),
              ("white on teal btn", "#FFFFFF", "#1D5864"),
              ("white on indigo", "#FFFFFF", "#202544"),
              ("white on navy", "#FFFFFF", "#021428"),
              ("headings on white", "#202544", "#FFFFFF")]
    bad=0
    for n,f,b in checks:
        r=cr(h(f),h(b)); ok = r>=4.5
        if not ok: bad+=1
        print(f"    {n:24s} {r:6.2f}:1  {'ok' if ok else 'FAIL'}")
    print(f"\n  {bad} failing pair(s)")
    json.dump(TOKENS, open("brand/newpalette.json","w"), indent=1)
