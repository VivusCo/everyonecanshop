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
  // hero: auto-playing scan of three barriers, then the fixed version (see seq in build.py)
  const peek = page.locator('[data-peek]');
  const heroShots = [[400, '1-start'], [2300, '2-scan-text'], [4400, '3-scan-colours'], [6500, '4-scan-button'], [8300, '5-all'], [11000, '6-fixed']];
  let h0 = Date.now();
  for (const [at, name] of heroShots) {
    const wait = at - (Date.now() - h0); if (wait > 0) await page.waitForTimeout(wait);
    await peek.screenshot({ path: path.join(out, `${lang}-hero-${name}.png`) });
  }
  const report = page.locator('.report');
  await report.scrollIntoViewIfNeeded();
  // timeline (ms after the demo starts), see the steps in build.py
  const shots = [[1200, '1-intro'], [5300, '2-before-swatch'], [10900, '3-customer-leaves'], [14600, '4-report'], [21600, '5-after-colour'], [27100, '6-order-placed'], [30400, '7-end']];
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
  await rm.locator('[data-peek]').screenshot({ path: path.join(out, `${lang}-hero-reduced-motion.png`) });
  console.log('animating with reduced motion:', await rm.evaluate(() => document.querySelector('[data-demo]').classList.contains('animating')));
  await browser.close();
})();
