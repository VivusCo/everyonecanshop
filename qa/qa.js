const { chromium } = require('playwright');
const fs = require('fs'); const path = require('path');
const axeSrc = fs.readFileSync(require.resolve('axe-core/axe.min.js'), 'utf8');
const BASE = 'http://localhost:8765';
const LANGS = { en: '/', nl: '/nl/', fr: '/fr/', de: '/de/' };
const shotDir = process.argv[2];
const shotLangs = (process.argv[3] || 'en,nl').split(',');
(async () => {
  const browser = await chromium.launch(process.env.CHROME ? { executablePath: process.env.CHROME } : {});
  const summary = {};
  for (const [lang, p] of Object.entries(LANGS)) {
    const res = { axe: {}, overflow: {}, focus: null };
    for (const [w, h] of [[1440, 900], [390, 844], [320, 640]]) {
      const page = await browser.newPage({ viewport: { width: w, height: h }, reducedMotion: 'reduce' });
      await page.goto(BASE + p, { waitUntil: 'networkidle' });
      // open all details so their content is checked too
      await page.evaluate(() => document.querySelectorAll('details').forEach(d => d.open = true));
      await page.addScriptTag({ content: axeSrc });
      const r = await page.evaluate(async () => await axe.run(document, { runOnly: { type: 'tag', values: ['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa'] }, resultTypes: ['violations', 'incomplete'] }));
      res.axe[w] = { violations: r.violations.map(v => ({ id: v.id, n: v.nodes.length, t: v.nodes.slice(0, 3).map(x => x.target.join(' ') + ' :: ' + (x.failureSummary || '').slice(0, 160)) })), incomplete: r.incomplete.map(v => v.id + ':' + v.nodes.length) };
      res.overflow[w] = await page.evaluate(() => document.documentElement.scrollWidth - window.innerWidth);
      await page.evaluate(() => document.querySelectorAll('details').forEach(d => d.open = false));
      if (shotDir && shotLangs.includes(lang) && w !== 320) {
        await page.screenshot({ path: path.join(shotDir, `${lang}-${w}.png`), fullPage: true });
      }
      if (w === 1440) {
        // keyboard: Tab through everything, check each focused element has visible outline
        const issues = []; const seen = [];
        for (let i = 0; i < 80; i++) {
          await page.keyboard.press('Tab');
          const info = await page.evaluate(() => {
            const el = document.activeElement; if (!el || el === document.body) return null;
            const cs = getComputedStyle(el); const r = el.getBoundingClientRect();
            return { tag: el.tagName, txt: (el.innerText || el.value || el.getAttribute('aria-label') || el.id || '').trim().slice(0, 40), outline: cs.outlineStyle + ' ' + cs.outlineWidth, shadow: cs.boxShadow, visible: r.width > 0 && r.height > 0 && r.bottom > 0 && r.top < innerHeight };
          });
          if (!info) break;
          seen.push(info.tag + ':' + info.txt);
          if (info.outline.startsWith('none') || !info.visible) issues.push(info);
        }
        res.focus = { count: seen.length, first: seen.slice(0, 3), issues };
      }
      await page.close();
    }
    // 200% zoom: 1280 css px at zoom 2 == 640 viewport
    const z = await browser.newPage({ viewport: { width: 640, height: 400 }, deviceScaleFactor: 2 });
    await z.goto(BASE + p); res.overflow['zoom200'] = await z.evaluate(() => document.documentElement.scrollWidth - window.innerWidth); await z.close();
    summary[lang] = res;
  }
  console.log(JSON.stringify(summary, null, 1));
  await browser.close();
})();
