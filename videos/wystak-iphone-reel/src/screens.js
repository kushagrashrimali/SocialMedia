// The phone's screen, drawn at the exact time of each frame onto a canvas the size of the model's display
// (1179 px wide, the display's own aspect). iOS-faithful details: Dynamic Island, status bar, the lock screen clock,
// the Wallet stack and the pass view. Merchants and people are fictional; no real company marks.
import { drawPassFace, drawQR, MERCHANTS } from "./passes.js";
import { SCREEN_PX } from "./phone.js";

const W = SCREEN_PX.w, H = SCREEN_PX.h;
export const clamp = (v, a = 0, b = 1) => Math.max(a, Math.min(b, v));
export const ease = (x) => { x = clamp(x); return x < 0.5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2; };
export const eo = (x) => 1 - Math.pow(1 - clamp(x), 3);
const spring = (x) => { x = clamp(x); return 1 - Math.exp(-6 * x) * Math.cos(9 * x); };

// a bright brand wallpaper: violet sky, lilac light, a teal glow low down (drawn once)
let wall = null;
function wallpaper() {
  if (wall) return wall;
  wall = document.createElement("canvas"); wall.width = W; wall.height = H;
  const c = wall.getContext("2d");
  const g = c.createLinearGradient(0, 0, 0, H); g.addColorStop(0, "#b99cff"); g.addColorStop(0.45, "#7b48e6"); g.addColorStop(1, "#3d1f9a");
  c.fillStyle = g; c.fillRect(0, 0, W, H);
  const blob = (x, y, r, col) => { const gr = c.createRadialGradient(x, y, 0, x, y, r); gr.addColorStop(0, col); gr.addColorStop(1, "rgba(0,0,0,0)"); c.fillStyle = gr; c.fillRect(0, 0, W, H); };
  blob(W * 0.2, H * 0.18, W * 0.9, "rgba(255,226,250,0.55)");
  blob(W * 0.95, H * 0.7, W * 0.9, "rgba(40,210,190,0.45)");
  blob(W * 0.1, H * 0.92, W * 0.8, "rgba(31,47,117,0.55)");
  const id = c.getImageData(0, 0, W, H), d = id.data; let s = 9;
  for (let i = 0; i < d.length; i += 4) { s = (s * 16807) % 2147483647; const n = (s / 2147483647 - 0.5) * 7; d[i] += n; d[i + 1] += n; d[i + 2] += n; }
  c.putImageData(id, 0, 0);
  return wall;
}

function island(c) { c.fillStyle = "#000"; c.beginPath(); c.roundRect(W / 2 - 186, 36, 372, 108, 54); c.fill(); }

function statusBar(c, alpha, ink = "#fff") {
  c.save(); c.globalAlpha = alpha; c.fillStyle = ink; c.strokeStyle = ink;
  c.font = "600 50px UI"; c.textAlign = "center"; c.fillText("9:41", 210, 112);
  const y = 100, x = W - 270;
  for (let i = 0; i < 4; i++) c.fillRect(x + i * 17, y - 10 - i * 7, 11, 12 + i * 7);
  c.lineWidth = 7; c.beginPath(); c.arc(x + 108, y + 2, 30, Math.PI * 1.25, Math.PI * 1.75); c.stroke();
  c.beginPath(); c.arc(x + 108, y + 2, 16, Math.PI * 1.25, Math.PI * 1.75); c.stroke();
  c.globalAlpha = alpha * 0.45; c.beginPath(); c.roundRect(x + 150, y - 22, 72, 34, 10); c.stroke(); c.globalAlpha = alpha;
  c.beginPath(); c.roundRect(x + 155, y - 17, 54, 24, 6); c.fill();
  c.restore();
}

function homeBar(c, ink = "#fff") { c.save(); c.fillStyle = ink; c.globalAlpha = 0.9; c.beginPath(); c.roundRect(W / 2 - 200, H - 44, 400, 15, 8); c.fill(); c.restore(); }

// the merchant's tile: the pass's colour with its glyph (Wallet shows the pass logo in a push)
function tile(c, x, y, s, m) {
  const g = c.createLinearGradient(x, y, x + s, y + s); g.addColorStop(0, m.c0); g.addColorStop(1, m.c1);
  c.fillStyle = g; c.beginPath(); c.roundRect(x, y, s, s, s * 0.23); c.fill();
  c.fillStyle = m.accent; const u = s / 130;
  c.beginPath(); c.moveTo(x + 30 * u, y + 75 * u); c.lineTo(x + 65 * u, y + 30 * u); c.lineTo(x + 75 * u, y + 62 * u); c.lineTo(x + 105 * u, y + 56 * u); c.lineTo(x + 72 * u, y + 80 * u); c.lineTo(x + 65 * u, y + 100 * u); c.closePath(); c.fill();
}

function notification(c, p, y0, m, title, body) {
  if (p <= 0) return;
  const k = spring(p), y = y0 + (1 - k) * 170, a = clamp(p * 3);
  c.save(); c.globalAlpha = a;
  const x = 45, w = W - 90, h = 236;
  c.fillStyle = "rgba(255,255,255,0.78)"; c.beginPath(); c.roundRect(x, y, w, h, 66); c.fill();
  tile(c, x + 40, y + 52, 132, m);
  c.fillStyle = "#14082a"; c.textAlign = "left";
  c.font = "700 54px UI"; c.fillText(title, x + 205, y + 104);
  c.font = "500 44px UI"; c.globalAlpha = a * 0.75; c.fillText(body, x + 205, y + 170);
  c.textAlign = "right"; c.font = "500 38px UI"; c.globalAlpha = a * 0.5; c.fillText("now", x + w - 46, y + 104);
  c.restore();
}

/** Lock screen. wake 0..1 brings the screen up; notif 0..1 springs the Wallet push in. */
export function drawLock(c, s) {
  c.fillStyle = "#000"; c.fillRect(0, 0, W, H);
  const wake = clamp(s.wake ?? 1);
  if (wake > 0) {
    c.save(); c.globalAlpha = wake; c.drawImage(wallpaper(), 0, 0);
    statusBar(c, 1);
    c.fillStyle = "#fff"; c.textAlign = "center";
    c.font = "600 64px UI"; c.fillText("Wednesday 8 October", W / 2, 360);
    c.font = "700 330px UI"; c.fillText("9:41", W / 2, 690);
    c.restore();
    notification(c, s.notif || 0, 1500, MERCHANTS[0], "+18 points", "Paper Crane Coffee · 132 of 150");
    if (wake > 0.5) homeBar(c);
  }
  island(c);
}

/**
 * The Wallet: passes file into one stack, one after another (k[i] 0..1 per pass), the newest in front.
 * Generic Wallet chrome, no platform marks.
 */
export function drawStack(c, s) {
  const g = c.createLinearGradient(0, 0, 0, H); g.addColorStop(0, "#f4f0fb"); g.addColorStop(1, "#e6ddf8");
  c.fillStyle = g; c.fillRect(0, 0, W, H);
  statusBar(c, 1, "#14082a");
  c.fillStyle = "#14082a"; c.textAlign = "left"; c.font = "700 92px UI"; c.fillText("Wallet", 64, 330);
  c.beginPath(); c.arc(W - 104, 300, 52, 0, Math.PI * 2); c.fillStyle = "rgba(20,8,42,0.08)"; c.fill();
  c.fillStyle = "#14082a"; c.fillRect(W - 128, 296, 48, 8); c.fillRect(W - 108, 276, 8, 48);
  const order = [4, 3, 2, 1, 0];                        // back to front: the café pass lands last, in front
  const pw = W - 120, phh = Math.round(pw * 0.631), top = 420, step = 205;
  order.forEach((mi, j) => {
    const k = clamp(s.k ? s.k[j] : 1); if (k <= 0) return;
    const e = 1 - Math.pow(1 - k, 4);
    const y = top + j * step + (1 - e) * 1400, rot = (1 - e) * 0.08;
    const m = MERCHANTS[mi];
    c.save(); c.translate(W / 2, y + phh / 2); c.rotate(rot); c.translate(-W / 2, -(y + phh / 2));
    c.shadowColor = "rgba(40,10,90,0.28)"; c.shadowBlur = 50; c.shadowOffsetY = 18;
    c.beginPath(); c.roundRect(60, y, pw, phh, 40); c.fillStyle = m.c1; c.fill(); c.shadowColor = "transparent";
    c.clip();
    c.drawImage(passCanvas(mi, pw, phh), 60, y);
    c.restore();
  });
  homeBar(c, "#14082a");
  island(c);
}

const _pc = {};
export function passCanvas(mi, w, h, qr = true) {
  const key = mi + "_" + w + "_" + h + "_" + qr;
  if (_pc[key]) return _pc[key];
  const cv = document.createElement("canvas"); cv.width = w; cv.height = h;
  drawPassFace(cv.getContext("2d"), w, h, MERCHANTS[mi], { qr });
  return (_pc[key] = cv);
}

/** The Paper Crane Coffee pass presented full screen, ready to scan at the counter. */
export function drawPassView(c, s) {
  const g = c.createLinearGradient(0, 0, 0, H); g.addColorStop(0, "#f4f0fb"); g.addColorStop(1, "#e6ddf8");
  c.fillStyle = g; c.fillRect(0, 0, W, H);
  statusBar(c, 1, "#14082a");
  c.fillStyle = "#6b2ba6"; c.font = "600 52px UI"; c.textAlign = "left"; c.fillText("Done", 64, 270);
  const m = MERCHANTS[0], px = 50, py = 360, pw = W - 100, ph = 1760;
  c.save(); c.shadowColor = "rgba(40,10,90,0.3)"; c.shadowBlur = 60; c.shadowOffsetY = 24;
  c.beginPath(); c.roundRect(px, py, pw, ph, 44); c.fillStyle = m.c1; c.fill(); c.shadowColor = "transparent"; c.clip();
  const ptop = passCanvas(0, pw, Math.round(pw * 0.631), false);
  const gg = c.createLinearGradient(0, py, 0, py + ph); gg.addColorStop(0, m.c0); gg.addColorStop(1, m.c1);
  c.fillStyle = gg; c.fillRect(px, py, pw, ph); c.drawImage(ptop, px, py);
  const qs = 540, qx = W / 2 - qs / 2, qy = py + ph - qs - 240;
  c.fillStyle = "#fff"; c.beginPath(); c.roundRect(qx - 40, qy - 40, qs + 80, qs + 150, 30); c.fill();
  drawQR(c, qx, qy, qs, 21);
  c.fillStyle = "#0b0410"; c.font = "600 36px UI"; c.textAlign = "center"; c.fillText("PCC 0042 7781", W / 2, qy + qs + 72);
  c.restore();
  homeBar(c, "#14082a");
  island(c);
}

export function drawOff(c) { c.fillStyle = "#000"; c.fillRect(0, 0, W, H); island(c); }
