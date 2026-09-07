# MontiCare

Brand and website work for **MontiCare**, a registered NDIS provider in Burpengary
East, Queensland, rebranding from Purpose Support Program.

> **Status: draft.** Nothing here is approved. The company name is still awaiting
> confirmation from ASIC, the logo and colours are with the client for sign-off, and
> the site is at homepage-concept stage. Treat every asset as provisional.

Product truth is in [PRODUCT.md](PRODUCT.md). Durable visual decisions are in
[DESIGN.md](DESIGN.md). Read those before changing anything.

## What is in here

| Path | What it is |
|---|---|
| `brand/build-logo.py` | Generates the whole logo family. Edit the constants at the top and re-run. |
| `brand/type2path.py` | Shapes text with HarfBuzz and emits outlined SVG paths. |
| `brand/out/` | The delivered logo files, plus `spec.json` (geometry and palette). |
| `brand/source/` | The client's original draft, kept for the before/after comparison. |
| `pdf/build.py` | Builds the 4-page client brand preview. |
| `MontiCare-brand-preview-DRAFT.pdf` | The logo concept as sent to the client. |
| `site/build.py` | Builds the homepage concepts. |
| `site/parts/` | Shared CSS plus one HTML partial per concept. |
| `canvas/` | Artboard sources for the design canvas. |
| `monticare-homepages.html` | All three concepts with a switcher. |
| `monticare-concept-a.html` | Concept A on its own, for presenting. |

## Rebuilding

```bash
pip3 install -r requirements.txt
python3 brand/build-logo.py          # logo SVGs -> brand/out/
python3 pdf/build.py                 # -> MontiCare-brand-preview-DRAFT.pdf
python3 site/build.py                # -> monticare-homepages.html
python3 site/build.py --only a       # -> monticare-concept-a.html
```

The PDF step drives headless Chrome, so Chrome must be installed at the usual macOS
path. Everything else is pure Python.

Derived caches (`*/parts/*.json`, `pdf/assets/*.json`) are gitignored and rebuilt
automatically, so a fresh clone works with no extra steps.

## The three homepage concepts

They differ in what the homepage leads with, not in styling.

- **A · Front Door** — explains the business, then asks who you are and opens a
  tailored path. Serves the client's stated priority, easy reading, most directly.
- **B · Capability** — the clinical capability register is the hero, with current
  capacity and the operating commitments. Built to win Support Coordinator referrals.
- **C · The Path** — the referral journey as a wayfinding spine, with the real 24 and
  48 hour timings. Answers the question families actually have.

## Assets and licensing

- **Typeface: Public Sans**, SIL Open Font Licence. Free to use, outline and modify,
  with no per-seat fee. It confers no trade mark rights.
- **Photography: Unsplash Licence**, sourced mainly from Age Cymru and the Centre for
  Ageing Better. Placeholder only — replace with real photographs of the client's team
  and participants once consent forms are signed. The current set skews elderly and
  NDIS spans all ages.
- Logo type is converted to outlines, so nothing depends on a font being installed.

## Non-negotiables

The audience is disabled people, so these are requirements rather than preferences:

- WCAG 2.1 AA as a floor. Every text colour clears it on the ground it sits on;
  `--grey-500` and lighter never carry text.
- No parallax, no scroll-jacking, no autoplay, nothing that flashes. Vestibular
  conditions and seizure risk are real in this audience.
- `prefers-reduced-motion` strips every animation, and the page must be complete
  without them.
- Touch targets 44px and up. Usable at 320px wide and at 200% zoom.
- The phone number is a component, not a footer detail. Most referrals arrive by voice.

## Still outstanding

1. ASIC confirmation of the company name, then the new ABN.
2. Client sign-off on the logo, the deepened aqua, and the `M` monogram favicon.
3. The NDIS registration number, to be displayed on the site.
4. Real photography with signed participant consent.
5. Privacy policy and a complaints/feedback page — both required and both missing
   from the current live site.
6. Referral form handling. It collects health information, so the Privacy Act and
   NDIS Practice Standards apply. Preference is a direct email to their Google
   Workspace inbox with no third-party storage.
