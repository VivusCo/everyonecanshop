# Redesign brief: everyonecanshop.com (v2, selling and trustworthy)

You are redesigning the static site in this repo. Read `build.py`, `content.py`, `src/style.css` first; v1 is live at http://everyonecanshop.com (GitHub Pages serves `docs/`).

## Business in one paragraph
EveryoneCanShop sells accessibility audits to EU webshops that must comply with the European Accessibility Act (EAA, since 28 June 2025; in Germany implemented as BFSG). Buyers: owners, e-commerce managers and marketing leads of mid-size webshops (10+ employees; microenterprises are exempt). Entry offer: a free mini check (2-3 real barriers with screenshots in 48 hours). Paid: full audit from EUR 490, re-test EUR 200, monitoring EUR 79/month. First outreach goes to the Netherlands and France, Germany comes inbound via the German page.

## Goal of v2
The page must SELL and build TRUST with a cautious, non-technical shop owner who has never heard of us. Today it is clean but generic. Make a visitor think: "these people are real, competent, specific, and the free check costs me nothing".

## Who is behind it (use this positioning, NOT "QA engineer")
Ivan Raylyan, Engineering & Delivery Manager. Leads engineering and delivery across several IT projects (product development and outsourcing). Started in QA: manual testing, then test automation (Selenium, Cypress, Pytest). 6+ years in compliance-heavy SaaS (legal, regulatory, financial tech). Uses AI agents as a working part of his job to automate recurring work. Based in Bucharest, Romania. LinkedIn: https://www.linkedin.com/in/ivan-raylyan-672204320
Photo: `src/ivan.jpg` (480x480, real portrait, use it prominently: hero or a visible "your auditor" card, plus the about section).
Honest angle that sells: AI-assisted testing (fast, covers every page) + a manager who has run releases and quality for years reviews every report personally. That is why we are faster and cheaper than agencies (EUR 1,500-5,000 per audit) without being a robot report.

## Must-have sections (order is a suggestion, improve it)
1. Hero: sharp promise, sub-line, primary CTA (free mini check), secondary CTA (see a sample report), trust strip under it (e.g. "WCAG 2.1 AA · EN 301 549 · EAA / BFSG", "No logins or code access", "Reviewed by a person", "Fixed prices"). Show Ivan's face near the CTA ("Ivan, your auditor") so it feels human.
2. Problem / why now: EAA facts with sources (keep the three stats from v1 with their links: Digital Trust Index 2026 9/10 homepages fail, ACM March 2026 61% of the largest Dutch shops blocked ordering with assistive tech, Directive (EU) 2019/882). Make the cost of doing nothing concrete (lost customers, regulator letters, warning letters in Germany) without fear-mongering or invented numbers.
3. Sample report preview: a realistic, styled excerpt of what the client receives. Use `src/sample-nofocus.jpg` (real screenshot from a real Dutch shop, brand-free crop: the "In winkelwagen" button has keyboard focus but no visible focus indicator) as finding #1 with severity, WCAG reference (2.4.7 Focus Visible), "who is affected", "how to fix" (CSS :focus-visible outline example). Add 1-2 more findings rendered in HTML/SVG (e.g. product option images without alt text, WCAG 1.1.1; quantity field without label, 1.3.1). This section is the strongest trust builder: make it look like a real document.
4. What we check (the 6 items from v1, keep).
5. Packages and prices (keep prices; make the free mini check and the full audit the visual focus; add "what you get" clarity, delivery times, "no obligation" on the free check).
6. How it works (4 steps, keep).
7. About Ivan (new positioning above, photo, LinkedIn link).
8. Why us vs agencies vs widgets: a small honest comparison (agency audit EUR 1,500-5,000 and weeks; overlay widgets do not fix code; EveryoneCanShop: fixed price, days, real fix list). No competitor names.
9. FAQ (keep the 5, add: "How do you test without access?", "Is our data safe?" (we only visit the public site like a customer, stop before payment, no cookies on our site), "What if you find nothing?").
10. Final CTA.
11. Footer: email ivan@everyonecanshop.com, LinkedIn, "Run by Ivan Raylyan · Bucharest, Romania", "No cookies, no tracking", accessibility note.

## Conversion
- Primary CTA: a small inline form "Your shop URL" + button "Get my free mini check". No backend exists: on submit, JS opens a prefilled mailto to ivan@everyonecanshop.com (subject + body with the URL). Without JS the button must still work (make it a mailto link fallback). Label the input properly.
- Keep the mailto CTA buttons as well. Phone number: none.

## Hard rules
- The site of an accessibility auditor must itself pass: run axe-core (WCAG 2.0/2.1 A and AA tags) on all 4 language pages with Playwright: ZERO violations. Visible focus on every interactive element (keep the yellow + dark double ring). Skip link, landmarks, correct heading order, lang per page, hreflang, reduced motion respected, contrast AA, works at 200% zoom and 320 px width.
- 4 languages: EN (/), NL (/nl/), FR (/fr/), DE (/de/). Keep all copy in `content.py`, translate every new string properly (NL informal "je", FR "vous", DE "Sie"; DE mentions BFSG). Native-sounding, not machine-like.
- No fake testimonials, no fake client logos, no invented numbers, no badges implying certification or regulator endorsement. Only facts from this brief.
- Never use the em dash character anywhere (copy, code comments). Use commas, colons, parentheses.
- Static only: Python build script -> `docs/`, no frameworks, no external fonts or trackers, no cookies. Keep `docs/CNAME` (everyonecanshop.com) and `.nojekyll`.
- Visual quality: modern, calm, premium, trustworthy (think Stripe / Linear documentation calm, warm paper background is fine). Generous whitespace, strong typographic hierarchy, consistent radius and shadows, mobile first. The hero illustration from v1 can stay or be improved.

## Process
1. Work on branch `redesign` (create it). Build, serve `docs/` locally, take full-page screenshots at 1440 px and 390 px for EN and NL, look at them critically, iterate at least twice on layout and copy.
2. Run the axe + keyboard checks, fix everything.
3. Commit with clear messages (end each commit message with: Co-Authored-By: Claude <noreply@anthropic.com>), push the `redesign` branch. Do NOT merge into main and do NOT touch DNS or GitHub Pages settings.
4. In your final message: what changed, screenshots paths in the repo (put them under `review/` on the branch), axe results per language.
