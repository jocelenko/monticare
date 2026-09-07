#!/usr/bin/env python3
"""MontiCare brand preview — print-ready A4, rendered to PDF by headless Chrome."""
import json, os, re, base64, subprocess

HERE = os.path.dirname(os.path.abspath(__file__))


def prepare():
    """Regenerate derived assets from source so a fresh clone just works.

    assets/fonts.json <- brand/fonts/PublicSans.ttf, instanced and compressed
    assets/svgs.json  <- brand/out/*.svg
    Needs: fonttools, brotli, Pillow  (see requirements.txt)
    """
    import io
    from fontTools.ttLib import TTFont
    from fontTools.varLib import instancer
    os.makedirs(f"{HERE}/assets", exist_ok=True)
    fonts = {}
    for w in (400, 500, 600, 700):
        f = instancer.instantiateVariableFont(
            TTFont(f"{HERE}/../brand/fonts/PublicSans.ttf"),
            {"wght": w}, inplace=False, updateFontNames=True)
        f.flavor = "woff2"
        buf = io.BytesIO(); f.save(buf)
        fonts[str(w)] = base64.b64encode(buf.getvalue()).decode()
    json.dump(fonts, open(f"{HERE}/assets/fonts.json", "w"))
    svgs = {n[:-4]: open(f"{HERE}/../brand/out/{n}").read().strip()
            for n in sorted(os.listdir(f"{HERE}/../brand/out")) if n.endswith(".svg")}
    json.dump(svgs, open(f"{HERE}/assets/svgs.json", "w"))


prepare()
FONTS = json.load(open(f"{HERE}/assets/fonts.json"))
SVGS  = json.load(open(f"{HERE}/assets/svgs.json"))
DATE  = "2 September 2026"

def face(w):
    return (f"@font-face{{font-family:'Public Sans';font-style:normal;font-weight:{w};"
            f"font-display:block;src:url(data:font/woff2;base64,{FONTS[str(w)]}) format('woff2')}}")

def svg(name, style="", cls=""):
    s = SVGS[name].strip()
    s = re.sub(r'\swidth="[\d.]+"\s+height="[\d.]+"', '', s, count=1)
    extra = f' class="{cls}"' if cls else ""
    return s.replace('<svg ', f'<svg{extra} style="{style}" preserveAspectRatio="xMidYMid meet" ', 1)

SRC_B64 = base64.b64encode(open(f"{HERE}/../canvas/source-cropped.png", "rb").read()).decode()

CSS = """
*{box-sizing:border-box}
html,body{margin:0;padding:0}
body{font-family:'Public Sans',Helvetica,Arial,sans-serif;color:#4A5560;
     -webkit-print-color-adjust:exact;print-color-adjust:exact}
@page{size:A4;margin:0}

.page{position:relative;width:210mm;height:297mm;overflow:hidden;background:#fff;
      page-break-after:always;break-after:page}
.page:last-child{page-break-after:auto;break-after:auto}

/* watermark: stroke-only, tinted so body copy over it still clears 5.5:1 */
.wm{position:absolute;inset:0;z-index:1;pointer-events:none;overflow:hidden}
.wm svg{position:absolute;left:50%;top:52%;transform:translate(-50%,-50%) rotate(-30deg)}
.wm.low svg{top:78%}
.wm text{font-family:'Public Sans';font-weight:700;font-size:96px;letter-spacing:.2em;
         fill:none;stroke:#C4E3E0;stroke-width:1.4}

.inner{position:relative;z-index:2;height:100%;padding:17mm 16mm 14mm 18mm;
       display:flex;flex-direction:column}

.hdr{display:flex;justify-content:space-between;align-items:center;
     padding-bottom:3.6mm;border-bottom:1px solid #D5DCE2;margin-bottom:9mm;flex-shrink:0}
.chip{font-size:6.8pt;font-weight:700;letter-spacing:.15em;color:#1A847F;
      border:1px solid #A9D5D1;border-radius:1mm;padding:1mm 2.4mm;white-space:nowrap}

/* full-height rail + reading column; the rail never drives row height */
.body{display:grid;grid-template-columns:36mm 132mm;gap:0 8mm;align-items:start;flex-grow:1}
.rail{display:flex;flex-direction:column;gap:0}
.railhead{font-size:7.2pt;font-weight:700;letter-spacing:.15em;color:#1A847F;
          text-transform:uppercase;line-height:1.5}
.railnote{font-size:8pt;line-height:1.6;color:#65707C;margin-top:3.2mm}
.railnote b{color:#4A5560;font-weight:600}
.data{margin-top:4mm;border-top:1px solid #D5DCE2;padding-top:2.6mm;
      display:flex;flex-direction:column;gap:2mm}
.data div{font-size:7.2pt;line-height:1.45;color:#65707C}
.data span{font-family:ui-monospace,Menlo,monospace;font-size:6.9pt;color:#1A847F}
.railgap{margin-top:11mm}

h1{font-size:32pt;font-weight:700;letter-spacing:-.022em;color:#1B252F;margin:0;line-height:1.06}
h2{font-size:18pt;font-weight:700;letter-spacing:-.016em;color:#1B252F;margin:0 0 4mm;line-height:1.15}
h3{font-size:10.5pt;font-weight:700;color:#1B252F;margin:0 0 2mm;line-height:1.3}
p{font-size:10.5pt;line-height:1.62;margin:0 0 3.6mm}
p:last-child{margin-bottom:0}
strong{font-weight:600;color:#1B252F}
.lead{font-size:12pt;line-height:1.5;color:#1B252F}

.ftr{margin-top:auto;padding-top:4.5mm;border-top:1px solid #D5DCE2;flex-shrink:0;
     display:flex;justify-content:space-between;font-size:7.4pt;color:#65707C}

ul{margin:0;padding:0;list-style:none;display:flex;flex-direction:column;gap:2.6mm}
ul li{font-size:10.2pt;line-height:1.5;padding-left:6mm;position:relative}
ul li::before{content:'';position:absolute;left:0;top:1.9mm;width:2.4mm;height:2.4mm;
              border-radius:50%;background:#A9D5D1}
ol{margin:0;padding:0;list-style:none;counter-reset:a;display:flex;flex-direction:column;gap:3.3mm}
ol li{counter-increment:a;padding-left:8.5mm;position:relative;font-size:10.2pt;line-height:1.5}
ol li::before{content:counter(a);position:absolute;left:0;top:0.2mm;width:5.6mm;height:5.6mm;
   border-radius:50%;background:#1A847F;color:#fff;font-size:7.6pt;font-weight:700;
   text-align:center;line-height:5.6mm}

.note{background:#E7F5F4;padding:4.5mm 5.5mm}
.note p{font-size:9.8pt;margin:0}

.specimens{display:flex;gap:7mm;align-items:stretch}
.spec{display:flex;flex-direction:column;gap:3.2mm;align-items:center;flex:1}
.art{height:30mm;width:100%;display:flex;align-items:center;justify-content:center}
.cap{font-size:7.4pt;line-height:1.38;color:#65707C;text-align:center}
.cap b{display:block;color:#1B252F;font-weight:600;font-size:8pt;margin-bottom:.6mm}
.dark{background:#1B252F;padding:6.5mm 7mm;display:flex;gap:8mm;align-items:center}

.swatches{display:flex;gap:2mm}
.sw{flex:1;display:flex;flex-direction:column;gap:1.6mm}
.chipc{height:15mm;border-radius:.8mm}
.nm{font-size:7pt;font-weight:600;color:#1B252F;line-height:1.2}
.hx{font-family:ui-monospace,Menlo,monospace;font-size:6.6pt;color:#65707C}

.mock{border:1px solid #D5DCE2;border-radius:1mm;overflow:hidden}
.mocktop{background:#fff;padding:3.4mm 4.5mm;border-bottom:1px solid #D5DCE2;
         display:flex;justify-content:space-between;align-items:center}
.btn{background:#1A847F;color:#fff;font-size:7.6pt;font-weight:600;
     padding:1.9mm 3.8mm;border-radius:1mm}
.mockbody{background:#F3F7FB;padding:5mm 4.5mm}

/* before / after, with the true centre marked on both */
.ba{display:flex;gap:9mm}
.ba figure{margin:0;display:flex;flex-direction:column;gap:2.4mm;align-items:center}
.xh{position:relative;width:42mm;height:42mm}
.xh img,.xh svg{width:42mm;height:42mm;display:block}
.xh::before,.xh::after{content:'';position:absolute;background:#E11D48;opacity:.85;z-index:3}
.xh::before{left:50%;top:0;bottom:0;width:.3mm;margin-left:-.15mm}
.xh::after{top:50%;left:0;right:0;height:.3mm;margin-top:-.15mm}
.lab{font-size:7.4pt;font-weight:700;letter-spacing:.09em;text-transform:uppercase}

.toc{display:flex;flex-direction:column;gap:2.4mm;border-top:1px solid #D5DCE2;padding-top:3.4mm}
.toc div{display:flex;gap:4mm;font-size:9pt;color:#4A5560;line-height:1.4}
.toc b{color:#1A847F;font-weight:700;font-size:8pt;width:4mm;flex-shrink:0}
"""

def wm(cls=""):
    return (f'<div class="wm {cls}"><svg width="820" height="180" viewBox="0 0 820 180">'
            '<text x="410" y="128" text-anchor="middle">DRAFT</text></svg></div>')
WM = wm()

def hdr():
    return (f'<div class="hdr">{svg("monticare-wordmark-positive","height:7mm;width:auto")}'
            f'<div class="chip">DRAFT &middot; PREVIEW</div></div>')

def ftr(n):
    return (f'<div class="ftr"><div>MontiCare brand preview. Draft, not for publication</div>'
            f'<div>{DATE} &nbsp;&middot;&nbsp; {n} of 4</div></div>')

def sw(h, name):
    b = ';border:1px solid #D5DCE2' if h in ('#E7F5F4', '#F3F7FB') else ''
    return f'<div class="sw"><div class="chipc" style="background:{h}{b}"></div><div class="nm">{name}</div><div class="hx">{h}</div></div>'


P1 = f"""
<div class="page">
  <div style="position:absolute;inset:0 0 auto 0;height:134mm;background:#E7F5F4;z-index:0"></div>
  <div style="position:absolute;left:0;right:0;top:0;height:134mm;z-index:0;
              display:flex;align-items:center;justify-content:center">
    {svg("monticare-badge-positive","width:84mm;height:84mm")}
  </div>
  {wm("low")}
  <div class="inner" style="padding-top:0">
    <div style="height:134mm;flex-shrink:0"></div>
    <div class="body" style="margin-top:13mm">
      <div class="rail">
        <div class="railhead">Preview</div>
        <div class="railnote">Prepared for<br><b>MontiCare</b></div>
        <div class="data">
          <div>Issued<br><span>{DATE}</span></div>
          <div>Status<br><span>Draft, for review</span></div>
        </div>
      </div>
      <div>
        <h1>Logo and colours</h1>
        <p class="lead" style="margin:4.5mm 0 5mm">A first look at your new brand, rebuilt from
        the draft you sent through.</p>
        <p>Nothing in here is final. I have kept the direction you chose and fixed the things
        that would have caused trouble later: making sure the words are dark enough to read
        comfortably, and rebuilding the artwork so it stays sharp at any size.</p>
        <p style="margin-bottom:7mm">Have a read, and tell me what you would like changed. Once
        you are happy with the logo and the colours, they become the base for the website.</p>
        <div style="font-size:7.2pt;font-weight:700;letter-spacing:.15em;color:#1A847F;
                    text-transform:uppercase;margin-bottom:3mm">In this preview</div>
        <div class="toc">
          <div><b>2</b><div>The logo, and where each version gets used</div></div>
          <div><b>3</b><div>Aqua and light grey, and one change worth explaining</div></div>
          <div><b>4</b><div>What I changed, and the four things I need from you</div></div>
        </div>
      </div>
    </div>
    {ftr(1)}
  </div>
</div>"""

P2 = f"""
<div class="page">
  {WM}
  <div class="inner">
    {hdr()}
    <div class="body">
      <div class="rail">
        <div class="railhead">The logo</div>
        <div class="railnote">Drawn as vector artwork, so it stays sharp from a browser tab
        to a shopfront sign.</div>
        <div class="data">
          <div>Typeface<br><span>Public Sans</span></div>
          <div>Licence<br><span>Open, free to use</span></div>
          <div>Smallest safe width<br><span>160&nbsp;px &middot; 50&nbsp;mm</span></div>
        </div>
      </div>
      <div>
        <h2>Your logo, rebuilt</h2>
        <p>The file you sent was a picture. That works on screen, but it blurs when it is
        enlarged and it will not print cleanly. I have redrawn it as artwork that stays crisp
        at any size.</p>
        <p style="margin-bottom:9mm">The lettering is now shapes rather than typed text, so it
        looks identical on every computer, and nobody needs a particular font installed to use it.</p>

        {svg("monticare-wordmark-positive","width:100mm;height:auto;display:block")}
        <p style="font-size:8.6pt;color:#65707C;margin:4mm 0 10mm">
          <strong>The main one.</strong> Website header, letterhead, quotes and your email signature.</p>

        <div class="specimens">
          <div class="spec"><div class="art">{svg("monticare-badge-positive","width:29mm;height:29mm")}</div>
            <div class="cap"><b>Round badge</b>When the logo stands on its own</div></div>
          <div class="spec"><div class="art">{svg("monticare-badge-solid","width:29mm;height:29mm")}</div>
            <div class="cap"><b>Solid</b>Social profiles and small spaces</div></div>
          <div class="spec"><div class="art">{svg("monticare-favicon","width:18mm;height:18mm")}</div>
            <div class="cap"><b>Browser tab</b>A proposal. See page 4</div></div>
          <div class="spec"><div class="art">
              <div style="border:1px solid #D5DCE2;padding:4mm 4.5mm;display:flex;align-items:center">
                {svg("monticare-mono-black","width:24mm;height:auto")}</div></div>
            <div class="cap"><b>One colour</b>Forms, stamps and invoices</div></div>
        </div>

        <div class="dark" style="margin-top:13mm;flex-direction:column;gap:6.5mm;align-items:stretch">
          <div style="display:flex;gap:11mm;align-items:center">
            {svg("monticare-badge-negative","width:26mm;height:26mm;flex-shrink:0")}
            {svg("monticare-wordmark-negative","width:58mm;height:auto;flex-shrink:0")}
          </div>
          <div style="color:#B6BFC8;font-size:8.6pt;line-height:1.55;border-top:1px solid #3A4550;padding-top:5mm">
            <b style="color:#fff;font-weight:600">On dark backgrounds.</b>
            A separate version for dark panels and photographs, so the grey half of the name
            never disappears. Swap the file rather than inverting the image.</div>
        </div>
      </div>
    </div>
    {ftr(2)}
  </div>
</div>"""


P3 = f"""
<div class="page">
  {WM}
  <div class="inner">
    {hdr()}
    <div class="body">
      <div class="rail">
        <div class="railhead">Colours</div>
        <div class="railnote">Aqua and light grey, as you asked, built out from the two colours
        already in your draft.</div>
        <div class="data">
          <div>Aqua for text<br><span>#1A847F</span></div>
          <div>Grey for text<br><span>#4A5560</span></div>
          <div>Readability standard<br><span>WCAG 2.1 AA, met</span></div>
        </div>
      </div>
      <div>
        <h2>Aqua and light grey</h2>
        <p style="margin-bottom:8mm">I have kept the aqua from your draft and built a small
        range around it, so there is a version for every job: a strong one for words and buttons,
        softer ones for backgrounds and panels.</p>

        <h3 style="margin-bottom:2.6mm">Aqua</h3>
        <div class="swatches">
          {sw('#005B57','Deep')}{sw('#1A847F','Main')}{sw('#46A49E','Mid')}{sw('#80BFBA','Soft')}
          {sw('#A9D5D1','Pale')}{sw('#D6ECEA','Tint')}{sw('#E7F5F4','Wash')}
        </div>
        <h3 style="margin:7mm 0 2.6mm">Light grey</h3>
        <div class="swatches">
          {sw('#1B252F','Darkest')}{sw('#4A5560','Text')}{sw('#65707C','Quiet')}{sw('#7D8892','Muted')}
          {sw('#B6BFC8','Line')}{sw('#D5DCE2','Rule')}{sw('#F3F7FB','Page')}
        </div>

        <h3 style="margin:10mm 0 2mm">One change worth explaining</h3>
        <p>In your draft the small grey line under the name sat too light against its
        background. For most businesses that is a minor thing. For you it is not. A good number of
        the people reading your site have low vision or find pale text hard going, and there is a
        published standard that sets the minimum.</p>
        <p style="margin-bottom:9mm">So I darkened that grey and deepened the aqua by a single
        step. You can still see it is your palette. It just holds up now, and the same aqua is
        safe for buttons and links across the whole site.</p>

        <div class="mock">
          <div class="mocktop">
            {svg("monticare-wordmark-positive","height:7mm;width:auto")}
            <div style="display:flex;gap:4.5mm;font-size:7.6pt;color:#4A5560;align-items:center">
              <span>Our supports</span><span>Referrals</span><span>Contact</span>
              <span class="btn">Make a referral</span></div>
          </div>
          <div class="mockbody">
            <div style="font-size:13pt;font-weight:700;color:#1B252F;letter-spacing:-.015em">
              NDIS supports across Moreton Bay</div>
            <div style="font-size:9pt;line-height:1.55;color:#4A5560;margin-top:2.2mm;max-width:100mm">
              Registered provider supporting participants of all ages, including
              high&#8209;intensity and complex needs.</div>
          </div>
        </div>
        <p style="font-size:8pt;color:#65707C;margin-top:2.8mm">A rough sense of how the two
        families sit together. Layout comes later.</p>
      </div>
    </div>
    {ftr(3)}
  </div>
</div>"""

P4 = f"""
<div class="page">
  {WM}
  <div class="inner">
    {hdr()}
    <div class="body">
      <div class="rail">
        <div class="railhead">What changed</div>
        <div class="railnote">Measured against the draft you sent.</div>
        <div class="data">
          <div>Name sat off centre by<br><span>5% of the circle</span></div>
          <div>Small grey text was<br><span>too pale to pass</span></div>
          <div>Ring vanished below<br><span>64&nbsp;px</span></div>
        </div>
        <div class="railgap">
          <div class="railhead">Over to you</div>
          <div class="railnote">Reply with anything you want changed. There is no cost to changing
          your mind at this stage.</div>
        </div>
      </div>
      <div>
        <h2>What I changed, and why</h2>
        <div class="ba" style="margin-bottom:6.5mm">
          <figure>
            <div class="xh"><img src="data:image/png;base64,{SRC_B64}" alt="The draft as supplied"></div>
            <div class="lab" style="color:#65707C">Your draft</div>
          </figure>
          <figure>
            <div class="xh">{svg("monticare-badge-positive","width:42mm;height:42mm;display:block")}</div>
            <div class="lab" style="color:#1A847F">Rebuilt</div>
          </figure>
        </div>
        <p style="font-size:9.4pt;color:#65707C;margin-bottom:5mm">The red lines mark the true
        centre. In your draft the name sits left of it, and low.</p>
        <ul style="margin-bottom:8mm">
          <li>The name was not centred in the circle. It sat slightly left, and slightly low.</li>
          <li>The small grey line beneath it was too pale to read comfortably.</li>
          <li>The thin ring around the circle disappeared at small sizes.</li>
          <li>The circle had a faint gradient, which does not print or embroider cleanly.</li>
          <li>The whole thing was a picture file, so it could not be enlarged without blurring.</li>
        </ul>

        <h2>What I need from you</h2>
        <ol>
          <li><strong>The logo.</strong> Happy with it as it stands, or is there something you
          would like adjusted?</li>
          <li><strong>The colours.</strong> The aqua is one shade deeper than your draft, for the
          reason on page&nbsp;3. Comfortable with that?</li>
          <li><strong>The browser tab.</strong> You asked for the name on its own, with no symbol,
          and I have stuck to that everywhere. A browser tab is the one place the full name cannot
          be read, so I have drawn a single <strong>M</strong> for it. Say the word if you would
          rather not.</li>
          <li><strong>The company name.</strong> Once ASIC confirms it, I will apply it across
          everything and update the domain registration.</li>
        </ol>
        <div class="note" style="margin-top:7mm;margin-bottom:7mm">
          <p>Once you are happy, this becomes the base for the website: same colours, same type,
          same logo files. You own all of it.</p>
        </div>
      </div>
    </div>
    {ftr(4)}
  </div>
</div>"""

faces = "".join(face(w) for w in (400, 500, 600, 700))
HTML = (f"<!doctype html><html lang='en-AU'><head><meta charset='utf-8'>"
        f"<title>MontiCare brand preview</title><style>{faces}{CSS}</style></head>"
        f"<body>{P1}{P2}{P3}{P4}</body></html>")
open(f"{HERE}/preview.html", "w").write(HTML)
print(f"  html {len(HTML)//1024} KiB")

CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
OUT = os.path.abspath(f"{HERE}/../MontiCare-brand-preview-DRAFT.pdf")
subprocess.run([CHROME, "--headless", "--disable-gpu", "--no-pdf-header-footer",
                "--run-all-compositor-stages-before-draw", "--virtual-time-budget=9000",
                f"--print-to-pdf={OUT}", f"file://{HERE}/preview.html"],
               check=True, capture_output=True)
print(f"  pdf  {os.path.getsize(OUT)//1024} KiB -> {OUT}")
