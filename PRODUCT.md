# Product

MontiCare (rebranding from Purpose Support Program) — a registered NDIS provider
in Burpengary East, Queensland, specialising in high-intensity and complex care.
This file records product truth for the website build.

## Platform

web

## Users

Three audiences share one site, and Webster (the owner) has explicitly refused to
narrow it:

- **Support Coordinators** — the commercial engine. They place participants with
  providers and carry the risk when a placement fails. They are assessing
  capability and reliability: can you take a PEG-fed participant next week, will
  you document properly, will you answer the phone. They compare providers fast
  and leave fast.
- **Participants** — people living with disability, many with complex needs.
  Range of literacy and cognitive ability. Some use screen readers, switch access
  or voice control. Some will be reading on an old Android phone.
- **Families and carers** — often the ones who actually search, usually stressed,
  frequently at a crisis point. They want reassurance before they want detail.
- **Allied health (OTs, nurses)** — refer occasionally, want clinical credibility.

Webster himself is non-technical and will not edit the site. He judges it by
whether his own people can read it.

## Product Purpose

Turn website visitors into referrals. Today the site produces almost none and
Webster cannot measure them. Referrals arrive two ways: the web form emails the
office, or the person phones the intake number. Most arrive by phone.

## Positioning

The differentiator is clinical capability that most NDIS providers cannot offer:
PEG feeding, epilepsy management, complex bowel management, wound management,
diabetes support including BSL monitoring and insulin administration, hoist and
transfer, pressure care, continence care, pain management under clinical guidance.

Paired with operational commitments aimed squarely at Support Coordinators:
24-hour referral acknowledgement, 48-hour intake and commencement planning,
consistent staffing model, shift documentation every service, incident reporting
inside NDIS timeframes, escalation protocols, monthly participant reports.

Service area: Brisbane, Moreton Bay, Sunshine Coast. Based Burpengary East.

## Operating Context

Read on a phone more often than a desktop, frequently one-handed, often while
the reader is stressed or mid-crisis. Some readers are in a hospital discharge
meeting trying to find a provider before the participant goes home. Support
Coordinators skim on a laptop between appointments with fifteen tabs open.

## Capabilities and Constraints

- Services: High-Intensity & Complex Needs, In-Home Support, Domestic Assistance,
  Daily Living Support, Community Participation, Transport, Household Tasks,
  Daily Personal Activities, Community Access.
- Phone 0447 334 958. Email admin@purposesupportprogram.com.au.
  12 Thomson Street, Burpengary East QLD 4505.
- Static site (Astro) on Hostinger. No CMS — content changes go through Joceli
  roughly every 6-12 months. No CRM, no NDIS system integration.
- The referral form collects health information about participants, so the
  Privacy Act and NDIS Practice Standards apply. Preference is to email straight
  to their Google Workspace inbox with no third-party storage.
- Behaviour support is a planned future service, not current.

## Brand Commitments

- MontiCare wordmark, no symbol. Aqua and light grey. See `brand/` and
  `brand/out/spec.json` for the built palette and logo files.
- Typeface Public Sans (SIL OFL), already used for the logo.
- Aqua #1A847F, grey #4A5560 for text, #E7F5F4 and #F3F7FB for surfaces.

## Evidence on Hand

- Seven pages of Webster's own copy (welcome, about, mission, why choose,
  high intensity, in-home, community access) — real, specific, and better than
  the current live site.
- The current site at purposesupportprogram.com.au, built by a previous supplier.
- No real photography. No testimonials — the current site's testimonial section
  contains placeholder text and invented names, which must not carry over.
- No NDIS registration number is displayed anywhere; it needs to be obtained
  and shown.

## Product Principles

- Easy read is Webster's stated number one priority, above design.
- Phone number visible everywhere. Most referrals come by voice.
- Services explained in detail and in point form, not marketing prose.
- Proof of NDIS registration must be visible.

## Accessibility & Inclusion

Non-negotiable and the strongest differentiator. Australian DDA 1992 applies and
the audience is disabled people. Target WCAG 2.1 AA as a floor.

Specific to this audience: vestibular triggers must be avoided, so no parallax,
no autoplaying motion, no scroll-jacking. Everything honours
`prefers-reduced-motion`. Touch targets no smaller than 44px. Plain language
over clinical jargon wherever a participant might read it. Content must remain
usable at 200% zoom and reflow to 320px.
