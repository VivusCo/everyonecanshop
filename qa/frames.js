// Capture frames of the screen reader demo and both states of the hero illustration.
// Usage: node frames.js <outdir> [lang]
const { chromium } = require('playwright');
const path = require('path');
const out = process.argv[2]; const lang = process.argv[3] || 'en';
const url = 'http://localhost:8765' + (lang === 'en' ? '/' : `/${lang}/`);
(async () => {
  const browser = await chromium.launch(process.env.CHROME ? { executablePath: process.env.CHROME } : {});
  const page = await browser.newPage({ viewport: { width: 1440, height: 1000 } });
  await page.goto(url, { waitUntil: 'networkidle' });
  const peek = page.locator('[data-peek]');
  await peek.screenshot({ path: path.join(out, `${lang}-hero-problems.png`) });
  await page.click('[data-peek] button[data-mode="good"]');
  await page.waitForTimeout(500);
  await peek.screenshot({ path: path.join(out, `${lang}-hero-fixed.png`) });
  const report = page.locator('.report');
  await report.scrollIntoViewIfNeeded();
  // timeline: 5 steps x 1.5s, verdict 2.6s, then the same after the fix
  const shots = [[700, 'before-1-image'], [3100, 'before-3-swatch'], [6100, 'before-5-button'], [8300, 'before-stuck'], [11000, 'after-2-colour'], [15800, 'after-5-button'], [18000, 'after-done']];
  let t0 = Date.now();
  for (const [at, name] of shots) {
    const wait = at - (Date.now() - t0); if (wait > 0) await page.waitForTimeout(wait);
    await report.screenshot({ path: path.join(out, `${lang}-demo-${name}.png`) });
  }
  // reduced motion: static before/after must show and nothing animates
  const rm = await browser.newPage({ viewport: { width: 1440, height: 1000 }, reducedMotion: 'reduce' });
  await rm.goto(url, { waitUntil: 'networkidle' });
  await rm.locator('.report').scrollIntoViewIfNeeded(); await rm.waitForTimeout(600);
  await rm.locator('.report').screenshot({ path: path.join(out, `${lang}-demo-reduced-motion.png`) });
  console.log('animating with reduced motion:', await rm.evaluate(() => document.querySelector('[data-demo]').classList.contains('animating')));
  await browser.close();
})();
