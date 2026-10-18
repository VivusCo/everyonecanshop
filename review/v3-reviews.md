# v3 review loop

Two independent reviewer agents saw only the rendered result (screenshots at 1440 and 390 px in EN and NL, hero toggle states, demo frames, page text):

- **Geralt**: a German/Dutch webshop owner (25 employees) who had never heard of the European Accessibility Act.
- **Designer**: a senior conversion and visual designer.

Three rounds ran. Each round's must-fix items were applied, then the page was rebuilt and checked again.

## Final verdicts (round 3)

**Geralt:** "NOTHING IMPORTANT LEFT."

5-second test: "New EU law since 28 June 2025: people with disabilities must be able to buy in my shop. These people check it and tell me what to fix. 1 in 4 adults, up to €100,000 fine in Germany. I'd click 'Get my free mini check': free, no obligation, 48 hours."

Demo retold: "A blind customer's screen reader only says 'image… image… button', so they can't pick a colour or find the buy button, and they leave. The report names the problem and a small fix; after the fix it says 'Moss green, selected… Add to cart, button' and the order goes through."

Verdict: "Yes, I would request the free mini check. It's clear, costs nothing, nobody needs my logins."

**Designer:** "NOTHING IMPORTANT LEFT."

"Every round 2 must-fix is correctly reflected in EN and NL, desktop and mobile. The page now reads as calm, credible and focused on one conversion path; nothing visible hurts trust or conversion."

## What changed between rounds

**Round 1 (both reviewers)**
- Sections looked blank. This was a capture artefact: smooth scrolling stopped the reveal animation from firing during the full-page capture. The QA script now scrolls instantly. The page itself was fine.
- Hero: added an "EU law since 28 June 2025" chip, numbered the markers 1-2-3 top to bottom, tightened the headline, kept the CTA in the mobile header.
- Trust strip without jargon ("Tested against the EU standard EN 301 549").
- The form now explains how the reply arrives.
- The demo was rebuilt as a short story in scenes, following Ivan's reference-style brief. It uses the same focus-ring style as the rest of the site.

**Round 2**
- Geralt: "what makes the audit cost more than €490" (now answered under the full audit); FAQ icons on mobile changed to +/−.
- Designer:
  - "Free mini check" kicker above the URL section.
  - Stacked field and button.
  - Clickable email fallback after submit.
  - Shorter NL/FR/DE button labels.
  - One CTA colour for the mini check.
  - Centred demo scenes and About block.
  - Duplicate "no obligation" removed.

## Requests deliberately not applied (founder constraints)

- Testimonials, client logos, a named client.
- A Dutch fine figure (not verified).
- Headcount, or switching to "I" instead of "our team".
- A company registration number and address (not provided).
- Replacing the section heading "Your shop URL", which Ivan requested explicitly. A kicker was added above it instead.

## Remaining nice-to-haves (not blocking)

- Desktop demo: some empty space under the caption line before the outcome badge appears.
- Hero illustration text is small on mobile (decorative; the callout list below carries the meaning).
- Designer note on trust: make sure "our team" stays accurate as the team grows.
