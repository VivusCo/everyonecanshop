# v4 review loop

Four independent reviewer agents judged only the rendered result: screenshots at 1440 and 390 px (EN and NL), the visible page text, and the animation frames. The accessibility auditor also tested the live pages in a browser.

1. **Geralt**: a cautious German/Dutch webshop owner with 25 employees who had never heard of the European Accessibility Act.
2. **Designer**: a senior conversion and visual designer.
3. **Plain-language checker**: B1 level, for non-technical shop owners.
4. **Accessibility auditor**: WCAG 2.1 A/AA, testing all 8 pages live with Playwright and axe.

Three rounds ran. Round 3 was needed only for the auditor, who had one must-fix left after round 2.

## Final verdicts

**Geralt (round 2): "NOTHING IMPORTANT LEFT."**
- 5-second test: "Someone checks whether disabled customers can actually buy in my shop, because of a new EU law. I get a list of what to fix. The first check is free. What I should do is type in my shop address and press 'Get my free mini check'."
- On the illustrations: "Yes, they help. Three real-looking people, one sentence each, and the sling makes 'can't use a mouse' obvious without words. They make the page warmer, not cluttered."
- On length: "The home page is long, but each block is short and calm. Nowhere is it overloaded."

**Designer (round 2): "NOTHING IMPORTANT LEFT."**
"The page is calm and trustworthy, and each block carries one idea. The copy is plain, the three sourced stats look credible, and the CTA path is clear. The hero animation reads in about 3 seconds, and the demo now ends cleanly." On the illustrations: "Consistent style, short human captions, no clutter. Illustrations appear only in two places."

**Plain-language checker (round 2): "NOTHING IMPORTANT LEFT."**
No em dashes or en dashes. No WCAG criterion numbers on home. On the guide, WCAG, EN 301 549 and level AA are each explained once in plain words. The three optional polish notes were applied anyway.

**Accessibility auditor (round 3): "NOTHING IMPORTANT LEFT."**
"The round-2 must-fix is resolved and no WCAG A/AA problems remain on the 8 pages." Clipping was checked on every card at 320 and 640 px, axe was run after scrolling each page, and focus showed a visible 4 px outline on every element reached by Tab. Its earlier rounds also confirmed:
- Both animations pause and play.
- Reduced motion gives a static version.
- Alt text is in the page language.
- The 61% ring is decorative.
- Breadcrumb names are translated.
- Nothing overflows at 320 px or 200% zoom.

## What changed between rounds

**Round 1 (all four reviewers)**
- Plain language:
  - "Widget" explained as a toolbar add-on.
  - The comparison row now reads "Removes the real problems?" instead of "Fixes the code?".
  - "Finding" replaced by "problem"; "assistive tools" replaced by keyboard and screen reader.
  - "Level AA" explained as "the level the law requires", and the ACM as "the Dutch consumer authority".
  - "Silent images" replaced by "have no name, so the screen reader can't say them".
  - Clearer turnover wording.
  - "A first version of your accessibility statement, written for you".
  - The founder background now reads "building and testing software".
  - The overlapping guide card headings were renamed ("Use it" / "Hear it read aloud").
- Home "Why it matters": a third sourced stat, ACM March 2026, 61% of about 100 large Dutch webshops.
- The guide's France card now cites the June 2026 order by the court in Caen against Carrefour (source link in all four languages and in the sources list).
- Demo: scenes now crossfade one after another, so the end card never overlaps the shop scene.
- Guide breadcrumb: a short label on mobile ("The law" / "De wet" / "La loi" / "Das Gesetz"). The breadcrumb's accessible name is now translated (auditor advisory).
- Separate names for the two pause buttons: "Pause example animation" vs "Pause animation" (auditor advisory).
- Illustrations (founder request):
  - A "Who gets stuck in your shop" block with three customer cards (low vision, blind, keyboard only), one sentence each.
  - The owner illustration beside the free mini check form.
  - Each image is a `<picture>` with webp and a jpg fallback, has width and height set, loads lazily, and has short alt text in four languages. The build copies `src/ill/` into `docs/ill/`.
- QA: waits for the FAQ close transition and for lazy images before screenshots. This fixes the "FAQ peeking" capture artefact both visual reviewers reported in round 1.
- A broken CSS rule (a missing closing brace in the 900 px footer rule) was found and fixed while checking the 320 px overflow.

**Round 2**
- Plain-language polish:
  - "Who not" became "Not for".
  - "issues" became "problems".
  - "Microenterprise" became "very small business" in the guide.
  - The accessibility statement is explained in a few words on home.
- Designer nice-to-have: the customer-card grid is narrower on desktop, so the images no longer outweigh the captions. The owner tile got a soft edge.
- Auditor must-fix: at 320 px on /nl/, the long word "Toegankelijkheidsverklaring" was cut off inside its card. The fix adds `min-width: 0` on the text column and `overflow-wrap: anywhere` on card text. QA now has a clipped-text check that would have caught this (verified against the old build).

**Round 3**
- The auditor found a cosmetic French-only bug: the French typography pass had put a non-breaking space inside the hero SVG's `viewBox`, so the French hero picture did not scale at 320 px. The typography pass now touches text nodes only, never tags or attributes.

## Requests deliberately not applied

- **"Your shop URL" heading**: kept, because Ivan requested it explicitly. Other places now say "web address".
- **Testimonials, client logos, headcount, invented numbers**: not applied (founder rules).
- **Company registration details / Impressum**: not provided. Recommended to Ivan, especially for German visitors.
- **Different clothing or seating for the three illustrated customers**: this needs new images (designer nice-to-have).
- **A visible "Pause" text label on the hero control**: the round icon button has an accessible name and a 36 px target. It was left as is to keep the hero calm.
- **"Reviewed by our team" while only Ivan is shown** (Geralt, minor doubt): kept as the founder's wording. Flagged to Ivan.

## Files

- `review/screens/`: full-page screenshots of home and guide, EN and NL, at 1440 and 390 px.
- `review/frames/`: hero animation frames (`hero-frames.png`), report demo frames (`demo-frames.png`), single frames, and the reduced-motion versions of both.
- `review/axe-results.md`: axe, overflow, clipped-text and keyboard results for all 8 pages.
