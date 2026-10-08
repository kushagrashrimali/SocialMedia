// Export lossless 2160x3840 PNG stills straight from the composition (no video compression):
// the Story cover (t=0) and the final frame (the 9-10s hold).
// usage (from the project folder): node tools/stills.mjs <out-dir> [t=seconds ...]
import { chromium } from "/opt/node22/lib/node_modules/playwright/index.mjs";
import path from "path";
const out = process.argv[2] || "renders";
const times = process.argv.slice(3).length ? process.argv.slice(3).map(Number) : [0, 9.97];
const names = { 0: "wystak-launch-intro-cover.png", 9.97: "wystak-launch-intro-final-frame.png" };
const b = await chromium.launch();
const p = await b.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 2 });
await p.goto("file://" + path.resolve("index.html"));
await p.evaluate(async () => { await document.fonts.ready; await Promise.all([...document.images].map(i => i.decode().catch(() => {}))); });
await p.waitForTimeout(500);
for (const t of times) {
  await p.evaluate((t) => window.__timelines.main.seek(t, false), t);
  await p.waitForTimeout(250);
  const f = path.join(out, names[t] || `wystak-launch-intro-${t}s.png`);
  await p.screenshot({ path: f, clip: { x: 0, y: 0, width: 1080, height: 1920 } });
  console.log("wrote", f);
}
await b.close();
