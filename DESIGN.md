# Design

The MontiCare visual world, and how it extends to the website.

## Origin

The identity came first (see `brand/`). The website inherits it rather than
inventing a new world. Anything here that contradicts `brand/out/spec.json` is
wrong and the spec wins.

## Colour

One aqua hue (OKLCH h≈190) and one grey hue (h≈248). Both ramps were derived
from the colours already in the client's own logo draft, so the palette is
theirs, corrected for contrast rather than replaced.

| Token | Hex | Role |
|---|---|---|
| `--aqua-900` | `#005B57` | Pressed states, deepest accent |
| `--aqua-700` | `#1A847F` | Primary. Links, buttons, "Care" in the wordmark |
| `--aqua-500` | `#46A49E` | Secondary accent, icon strokes |
| `--aqua-400` | `#80BFBA` | Logo ring, dividers on aqua ground |
| `--aqua-300` | `#A9D5D1` | Bullets, quiet marks |
| `--aqua-100` | `#D6ECEA` | Panel fill |
| `--aqua-50`  | `#E7F5F4` | Section wash |
| `--grey-900` | `#1B252F` | Dark ground, headings on light |
| `--grey-700` | `#4A5560` | Body text |
| `--grey-600` | `#65707C` | Secondary text. The lightest grey allowed on text |
| `--grey-300` | `#B6BFC8` | Borders on dark |
| `--grey-200` | `#D5DCE2` | Rules and borders |
| `--grey-50`  | `#F3F7FB` | Page tint |

Colour strategy is Restrained: neutral ground, aqua carries action. Aqua owns
whole regions only where a section is genuinely a different job (the referral
band, the proof band), never as scattered accent.

**Contrast is a hard floor, not a guideline.** Every text colour clears WCAG AA
on the ground it actually sits on. `--grey-500` and lighter never carry text.
Aqua on white is 4.52:1, which passes, so aqua may be a link colour.

## Type

Public Sans (SIL OFL) throughout, the same face as the wordmark. One family, not
a pairing: hierarchy comes from weight, scale and colour. A second face would add
cognitive load for readers who already find dense text hard.

Weights in use: 400 body, 600 emphasis and labels, 700 headings, 800 display.
Body never below 17px on desktop or 16px on mobile. Line height 1.6 for body,
1.1 to 1.2 for display. Measure held to 62-72 characters.

## Motion

The audience includes people with vestibular conditions and people who have
seizures. This constrains motion more than taste does.

- No parallax, no scroll-jacking, no autoplaying video, no carousels that move
  on their own, nothing that flashes.
- Content is visible by default and animation only refines its arrival.
- `prefers-reduced-motion: reduce` removes all transforms and transitions, and
  the page must be complete and correct with every animation stripped.
- One authored moment per page, not scattered hover effects.

## Layout

Container 1200px. Reading columns 640-720px. An 8px spacing scale.
More space above a heading than below it. Touch targets never below 44px.
The page must reflow to 320px and stay usable at 200% zoom.

## Components

Buttons are solid aqua or outlined grey, 48px min height, 2px focus ring offset
2px in `--aqua-900`. Cards carry a 1px `--grey-200` border and a soft shadow
with real offset, never a coloured halo and never a coloured left border.
Links underline on hover and are underlined in body copy by default.

The phone number is a first-class component, not a footer detail. Most referrals
arrive by voice, so it appears in the header, at every decision point, and in the
footer, always as a real `tel:` link.

## Prohibitions

- No stock-photo grid of smiling strangers used as decoration. Photography earns
  its place by showing the work being done.
- No testimonial section until real, attributed testimonials exist. The previous
  site shipped invented names against stock portraits; that must not recur.
- No claimed statistics. The only numbers on the site are the operating
  commitments the business actually makes (24 hours, 48 hours).
