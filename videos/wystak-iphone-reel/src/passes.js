// Wallet passes as real objects: a thin rounded slab (credit-card proportions) with a printed face and a glossy
// coat. Faces are drawn once to canvases. Merchants are fictional (brand rule: no real company names).
import * as THREE from "three";

export const PASS = { w: 8.56, h: 5.4, d: 0.07, r: 0.42 };

export const MERCHANTS = [
  { name: "Paper Crane", sub: "COFFEE", kind: "Café", c0: "#3a2418", c1: "#130905", ink: "#f3e6d6", accent: "#e8b77a", pts: "132", next: "Free cappuccino", glyph: "crane" },
  { name: "Lumen", sub: "SALON", kind: "Salon", c0: "#7c2a54", c1: "#2a0b1d", ink: "#ffe9f2", accent: "#ff9cc8", pts: "48", next: "Free blow-dry", glyph: "drop" },
  { name: "Ironfold", sub: "GYM", kind: "Gym", c0: "#1d2b22", c1: "#070d09", ink: "#e9ffe9", accent: "#b6f36a", pts: "21", next: "Guest pass", glyph: "bolt" },
  { name: "Reel House", sub: "CINEMA", kind: "Cinema", c0: "#5c0f17", c1: "#1c0306", ink: "#fff0e6", accent: "#ffcf6e", pts: "6", next: "Free popcorn", glyph: "reel" },
  { name: "Monsoon", sub: "FEST", kind: "Events", c0: "#123a5a", c1: "#06121f", ink: "#e6f6ff", accent: "#72e3ff", pts: "3", next: "Backstage", glyph: "wave" },
];

function rr(ctx, x, y, w, h, r) { ctx.beginPath(); ctx.roundRect(x, y, w, h, r); }

function glyph(ctx, kind, x, y, s, col) {
  ctx.save(); ctx.translate(x, y); ctx.fillStyle = col; ctx.strokeStyle = col; ctx.lineWidth = s * 0.09; ctx.lineJoin = "round";
  if (kind === "crane") { ctx.beginPath(); ctx.moveTo(-s * .5, s * .15); ctx.lineTo(0, -s * .45); ctx.lineTo(s * .12, -s * .02); ctx.lineTo(s * .5, -s * .1); ctx.lineTo(s * .1, s * .2); ctx.lineTo(0, s * .45); ctx.closePath(); ctx.fill(); }
  if (kind === "drop") { ctx.beginPath(); ctx.moveTo(0, -s * .5); ctx.bezierCurveTo(s * .45, 0, s * .4, s * .45, 0, s * .45); ctx.bezierCurveTo(-s * .4, s * .45, -s * .45, 0, 0, -s * .5); ctx.fill(); }
  if (kind === "bolt") { ctx.beginPath(); ctx.moveTo(s * .1, -s * .5); ctx.lineTo(-s * .3, s * .08); ctx.lineTo(-s * .02, s * .08); ctx.lineTo(-s * .12, s * .5); ctx.lineTo(s * .32, -s * .1); ctx.lineTo(s * .04, -s * .1); ctx.closePath(); ctx.fill(); }
  if (kind === "reel") { ctx.beginPath(); ctx.arc(0, 0, s * .45, 0, Math.PI * 2); ctx.stroke(); for (let i = 0; i < 6; i++) { const a = i * Math.PI / 3; ctx.beginPath(); ctx.arc(Math.cos(a) * s * .24, Math.sin(a) * s * .24, s * .08, 0, Math.PI * 2); ctx.fill(); } }
  if (kind === "wave") { ctx.beginPath(); for (let k = 0; k < 3; k++) { const yy = (k - 1) * s * .28; ctx.moveTo(-s * .5, yy); ctx.bezierCurveTo(-s * .2, yy - s * .2, s * .2, yy + s * .2, s * .5, yy); } ctx.stroke(); }
  ctx.restore();
}

// a deterministic QR-like code (finder squares + seeded modules): drawn, not a real payload
export function drawQR(ctx, x, y, size, seed) {
  const n = 29, m = size / n; let s = seed;
  const rnd = () => (s = (s * 16807) % 2147483647) / 2147483647;
  ctx.fillStyle = "#fff"; ctx.fillRect(x - m * 2, y - m * 2, size + m * 4, size + m * 4);
  ctx.fillStyle = "#0b0410";
  for (let i = 0; i < n; i++) for (let j = 0; j < n; j++) {
    const inF = (a, b) => i >= a && i < a + 7 && j >= b && j < b + 7;
    if (inF(0, 0) || inF(0, n - 7) || inF(n - 7, 0)) continue;
    if (rnd() > 0.52) ctx.fillRect(x + i * m, y + j * m, m + 0.4, m + 0.4);
  }
  [[0, 0], [0, n - 7], [n - 7, 0]].forEach(([a, b]) => {
    ctx.fillRect(x + a * m, y + b * m, m * 7, m * 7);
    ctx.fillStyle = "#fff"; ctx.fillRect(x + (a + 1) * m, y + (b + 1) * m, m * 5, m * 5);
    ctx.fillStyle = "#0b0410"; ctx.fillRect(x + (a + 2) * m, y + (b + 2) * m, m * 3, m * 3);
  });
}

// the printed face of a store-card pass (Apple Wallet layout: logo + name, header field, strip, fields)
export function drawPassFace(ctx, W, H, m, opts = {}) {
  const g = ctx.createLinearGradient(0, 0, W, H); g.addColorStop(0, m.c0); g.addColorStop(1, m.c1);
  ctx.fillStyle = g; ctx.fillRect(0, 0, W, H);
  // soft printed light falloff + fine texture
  const rg = ctx.createRadialGradient(W * .2, H * .1, 0, W * .2, H * .1, W * .9); rg.addColorStop(0, "rgba(255,255,255,0.10)"); rg.addColorStop(1, "rgba(255,255,255,0)");
  ctx.fillStyle = rg; ctx.fillRect(0, 0, W, H);
  const u = W / 1000;
  glyph(ctx, m.glyph, 70 * u, 78 * u, 64 * u, m.accent);
  ctx.fillStyle = m.ink; ctx.textBaseline = "alphabetic";
  ctx.font = `700 ${40 * u}px UI`; ctx.fillText(m.name, 122 * u, 78 * u);
  ctx.font = `600 ${20 * u}px UI`; ctx.globalAlpha = 0.7; ctx.fillText(m.sub, 124 * u, 106 * u); ctx.globalAlpha = 1;
  ctx.textAlign = "right"; ctx.font = `600 ${18 * u}px UI`; ctx.globalAlpha = 0.7; ctx.fillText("POINTS", W - 60 * u, 66 * u); ctx.globalAlpha = 1;
  ctx.font = `700 ${46 * u}px UI`; ctx.fillText(m.pts, W - 60 * u, 112 * u); ctx.textAlign = "left";
  // strip: a band of the accent colour with a subtle pattern
  const sy = 150 * u, sh = 210 * u;
  const sg = ctx.createLinearGradient(0, sy, W, sy + sh); sg.addColorStop(0, m.accent); sg.addColorStop(1, m.c0);
  ctx.globalAlpha = 0.85; ctx.fillStyle = sg; ctx.fillRect(0, sy, W, sh); ctx.globalAlpha = 1;
  ctx.save(); ctx.globalAlpha = 0.16; ctx.strokeStyle = m.ink; ctx.lineWidth = 2 * u;
  for (let k = -6; k < 26; k++) { ctx.beginPath(); ctx.moveTo(k * 48 * u, sy); ctx.lineTo(k * 48 * u + sh, sy + sh); ctx.stroke(); }
  ctx.restore();
  glyph(ctx, m.glyph, W - 150 * u, sy + sh / 2, 150 * u, "rgba(255,255,255,0.22)");
  ctx.fillStyle = m.ink; ctx.font = `600 ${17 * u}px UI`; ctx.globalAlpha = 0.65;
  ctx.fillText("MEMBER", 60 * u, 410 * u); ctx.fillText("NEXT REWARD", 470 * u, 410 * u); ctx.globalAlpha = 1;
  ctx.font = `600 ${30 * u}px UI`; ctx.fillText("Aarav M.", 60 * u, 452 * u); ctx.fillText(m.next, 470 * u, 452 * u);
  if (opts.qr !== false) {
    ctx.fillStyle = "rgba(255,255,255,0.95)"; rr(ctx, W / 2 - 70 * u, 488 * u, 140 * u, 118 * u, 14 * u); ctx.fill();
    drawQR(ctx, W / 2 - 46 * u, 500 * u, 92 * u, 7 + m.name.length);
  }
}

function roundedRect(w, h, r) {
  const s = new THREE.Shape(), x = -w / 2, y = -h / 2;
  s.moveTo(x + r, y); s.lineTo(x + w - r, y); s.absarc(x + w - r, y + r, r, -Math.PI / 2, 0, false);
  s.lineTo(x + w, y + h - r); s.absarc(x + w - r, y + h - r, r, 0, Math.PI / 2, false);
  s.lineTo(x + r, y + h); s.absarc(x + r, y + h - r, r, Math.PI / 2, Math.PI, false);
  s.lineTo(x, y + r); s.absarc(x + r, y + r, r, Math.PI, Math.PI * 1.5, false);
  return s;
}
function roundedPlane(w, h, r) {
  const g = new THREE.ShapeGeometry(roundedRect(w, h, r), 16);
  const p = g.attributes.position, uv = g.attributes.uv;
  for (let i = 0; i < p.count; i++) uv.setXY(i, p.getX(i) / w + 0.5, p.getY(i) / h + 0.5);
  return g;
}

export function buildPass(m, env) {
  const cv = document.createElement("canvas"); cv.width = 1000; cv.height = 631;
  drawPassFace(cv.getContext("2d"), cv.width, cv.height, m);
  const tex = new THREE.CanvasTexture(cv); tex.colorSpace = THREE.SRGBColorSpace; tex.anisotropy = 8;
  const g = new THREE.Group();
  const body = new THREE.Mesh(new THREE.ExtrudeGeometry(roundedRect(PASS.w - 0.04, PASS.h - 0.04, PASS.r - 0.02), { depth: PASS.d - 0.04, bevelEnabled: true, bevelThickness: 0.02, bevelSize: 0.02, bevelSegments: 2, curveSegments: 16 }),
    new THREE.MeshPhysicalMaterial({ color: new THREE.Color(m.c1), roughness: 0.35, metalness: 0.1, clearcoat: 1, envMap: env }));
  body.position.z = -(PASS.d - 0.04) / 2;
  const face = new THREE.Mesh(roundedPlane(PASS.w, PASS.h, PASS.r), new THREE.MeshPhysicalMaterial({ map: tex, roughness: 0.3, metalness: 0.0, clearcoat: 0.5, clearcoatRoughness: 0.1, envMap: env, envMapIntensity: 0.4 }));
  face.position.z = PASS.d / 2 + 0.001;
  const backFace = new THREE.Mesh(roundedPlane(PASS.w, PASS.h, PASS.r), new THREE.MeshPhysicalMaterial({ color: new THREE.Color(m.c1), roughness: 0.4, clearcoat: 1, envMap: env }));
  backFace.position.z = -PASS.d / 2 - 0.001; backFace.rotation.y = Math.PI;
  g.add(body, face, backFace);
  return { group: g, canvas: cv, tex };
}
