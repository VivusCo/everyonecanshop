# axe-core results (v4)

axe-core 4.10.2 via Playwright (Chromium), tags wcag2a, wcag2aa, wcag21a, wcag21aa. Each page is scrolled through first so every section is revealed, and all FAQ items are opened so their content is checked too. Run: `python3 build.py`, serve `docs/` on port 8765, `cd qa && node qa.js <screenshot-dir>`.

| Page | 1440 px | 390 px | 320 px | Horizontal overflow (320 px / 200% zoom) | Clipped text | Keyboard focus issues |
|---|---|---|---|---|---|---|
| / | 0 | 0 | 0 | 0 px / 0 px | 0 | 0 |
| /eaa/ | 0 | 0 | 0 | 0 px / 0 px | 0 | 0 |
| /nl/ | 0 | 0 | 0 | 0 px / 0 px | 0 | 0 |
| /nl/eaa/ | 0 | 0 | 0 | 0 px / 0 px | 0 | 0 |
| /fr/ | 0 | 0 | 0 | 0 px / 0 px | 0 | 0 |
| /fr/eaa/ | 0 | 0 | 0 | 0 px / 0 px | 0 | 0 |
| /de/ | 0 | 0 | 0 | 0 px / 0 px | 0 | 0 |
| /de/eaa/ | 0 | 0 | 0 | 0 px / 0 px | 0 | 0 |

**0 violations on all 8 pages, in all four languages.**

axe lists "incomplete" color-contrast items for text on gradients and on the decorative pointer-light layer, which it cannot compute automatically. Those were checked by hand by the accessibility reviewer (lowest measured ratio about 5.7:1).

The clipped-text check is new in v4: it flags any text that runs past its card or past an overflow container. It was added after the round 2 audit found a long Dutch word cut off at 320 px.
