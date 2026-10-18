# everyonecanshop.com

Static site for EveryoneCanShop (accessibility audits for EU webshops).
Copy lives in `content.py` (EN, NL, FR, DE), layout in `build.py`, styles in `src/style.css`.
Build with `python3 build.py` (needs Pillow for the portrait thumbnails); output goes to `docs/`, which GitHub Pages serves.

## QA
Serve `docs/` (`python3 -m http.server 8765 -d docs`), then:

```
cd qa && npm install
node qa.js ../review en,nl,fr,de
```

This runs axe-core (WCAG 2.0/2.1 A and AA) on all four languages at 1440, 390 and 320 px, tabs through the page
checking for a visible focus ring, checks horizontal overflow at 320 px and 200% zoom, and writes full-page
screenshots to `review/`. Latest results: `review/axe-results.md`.
