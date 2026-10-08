// The phone's screen, drawn to a 1179 x 2556 canvas (the real iPhone panel) at the exact time of each frame.
// iOS details kept faithful: Dynamic Island size and place, the lock glyph that opens when Face ID recognises
// you, the date and clock, the flashlight and camera buttons, the home indicator, the Wallet pass view.
import { drawPassFace, drawQR, MERCHANTS } from "./passes.js";

const W = 1179, H = 2556;
export const clamp = (v, a = 0, b = 1) => Math.max(a, Math.min(b, v));
export const ease = (x) => { x = clamp(x); return x < 0.5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2; };
export const eo = (x) => 1 - Math.pow(1 - clamp(x), 3);
const spring = (x) => { x = clamp(x); return 1 - Math.exp(-6 * x) * Math.cos(9 * x); };

let wall = null;
function wallpaper() {
  if (wall) return wall;
  wall = document.createElement("canvas"); wall.width = W; wall.height = H;
  const c = wall.getContext("2d");
  c.fillStyle = "#07040e"; c.fillRect(0, 0, W, H);
  const blob = (x, y, r, col) => { const g = c.createRadialGradient(x, y, 0, x, y, r); g.addColorStop(0, col); g.addColorStop(1, "rgba(0,0,0,0)"); c.fillStyle = g; c.fillRect(0, 0, W, H); };
  blob(W * 0.15, H * 0.30, W * 1.0, "rgba(107,43,166,0.85)");
  blob(W * 0.95, H * 0.62, W * 0.95, "rgba(15,143,138,0.70)");
  blob(W * 0.45, H * 0.95, W * 0.9, "rgba(31,47,117,0.85)");
  blob(W * 0.70, H * 0.12, W * 0.6, "rgba(160,110,255,0.35)");
  // fine grain so the gradient never bands
  const id = c.getImageData(0, 0, W, H), d = id.data; let s = 9;
  for (let i = 0; i < d.length; i += 4) { s = (s * 16807) % 2147483647; const n = (s / 2147483647 - 0.5) * 8; d[i] += n; d[i + 1] += n; d[i + 2] += n; }
  c.putImageData(id, 0, 0);
  return wall;
}

function island(c, wpx, hpx) {
  c.fillStyle = "#000"; c.beginPath(); c.roundRect(W / 2 - wpx / 2, 33, wpx, hpx, hpx / 2); c.fill();
}

function statusBar(c, alpha, dark) {
  c.save(); c.globalAlpha = alpha; c.fillStyle = dark ? "#000" : "#fff";
  // right: signal, wifi, battery
  const y = 96, x = W - 250;
  for (let i = 0; i < 4; i++) c.fillRect(x + i * 17, y - 10 - i * 7, 11, 12 + i * 7);
  c.beginPath(); c.arc(x + 108, y + 2, 30, Math.PI * 1.25, Math.PI * 1.75); c.lineWidth = 7; c.strokeStyle = c.fillStyle; c.stroke();
  c.beginPath(); c.arc(x + 108, y + 2, 16, Math.PI * 1.25, Math.PI * 1.75); c.stroke();
  c.beginPath(); c.roundRect(x + 150, y - 22, 72, 34, 10); c.globalAlpha = alpha * 0.45; c.stroke(); c.globalAlpha = alpha;
  c.beginPath(); c.roundRect(x + 155, y - 17, 54, 24, 6); c.fill();
  c.restore();
}

// the lock glyph: closed shackle, then it lifts and swings open (Face ID success)
function lockGlyph(c, x, y, open, alpha) {
  c.save(); c.globalAlpha = alpha; c.translate(x, y); c.fillStyle = "#fff"; c.strokeStyle = "#fff"; c.lineWidth = 9; c.lineCap = "round";
  c.beginPath(); c.roundRect(-30, -4, 60, 48, 10); c.fill();
  const lift = 14 * spring(open), swing = 22 * ease((open - 0.25) / 0.75);
  c.beginPath(); c.moveTo(-18, -4); c.lineTo(-18, -18 - lift); c.arc(0 + swing * 0.0, -18 - lift, 18, Math.PI, 0); c.lineTo(18, -4 - lift * 0.15 - (open > 0 ? 6 * ease(open) : 0)); c.stroke();
  c.restore();
}

function clockText(c, alpha, y = 0) {
  c.save(); c.globalAlpha = alpha; c.fillStyle = "#fff"; c.textAlign = "center";
  c.font = "600 64px UI"; c.fillText("Wednesday 8 October", W / 2, 360 + y);
  c.font = "700 318px UI"; c.fillText("9:41", W / 2, 676 + y);
  c.restore();
}

function lockButtons(c, alpha) {
  c.save(); c.globalAlpha = alpha;
  [[170, 2330], [W - 170, 2330]].forEach(([x, y], i) => {
    c.fillStyle = "rgba(30,24,44,0.55)"; c.beginPath(); c.arc(x, y, 76, 0, Math.PI * 2); c.fill();
    c.fillStyle = "#fff";
    if (i === 0) { c.beginPath(); c.roundRect(x - 15, y - 34, 30, 22, 6); c.fill(); c.fillRect(x - 9, y - 12, 18, 46); }
    else { c.beginPath(); c.roundRect(x - 34, y - 22, 68, 48, 10); c.fill(); c.fillStyle = "rgba(30,24,44,1)"; c.beginPath(); c.arc(x, y + 2, 14, 0, Math.PI * 2); c.fill(); }
  });
  c.fillStyle = "#fff"; c.globalAlpha = alpha * 0.92; c.beginPath(); c.roundRect(W / 2 - 200, H - 42, 400, 15, 8); c.fill();
  c.restore();
}

function notification(c, p, y0) {
  if (p <= 0) return;
  const k = spring(p), y = y0 + (1 - k) * 160, a = clamp(p * 3);
  c.save(); c.globalAlpha = a;
  const x = 45, w = W - 90, h = 230;
  c.fillStyle = "rgba(245,240,255,0.22)"; c.beginPath(); c.roundRect(x, y, w, h, 66); c.fill();
  c.strokeStyle = "rgba(255,255,255,0.35)"; c.lineWidth = 2; c.stroke();
  // app tile: the pass's own glyph on its colour (Wallet shows the pass logo)
  const m = MERCHANTS[0];
  const g = c.createLinearGradient(x + 40, y + 50, x + 170, y + 180); g.addColorStop(0, m.c0); g.addColorStop(1, m.c1);
  c.fillStyle = g; c.beginPath(); c.roundRect(x + 40, y + 50, 130, 130, 30); c.fill();
  c.fillStyle = m.accent; c.beginPath(); c.moveTo(x + 70, y + 125); c.lineTo(x + 105, y + 80); c.lineTo(x + 115, y + 112); c.lineTo(x + 145, y + 106); c.lineTo(x + 112, y + 130); c.lineTo(x + 105, y + 150); c.closePath(); c.fill();
  c.fillStyle = "#fff"; c.textAlign = "left";
  c.font = "700 52px UI"; c.fillText("+18 points", x + 205, y + 100);
  c.font = "500 44px UI"; c.globalAlpha = a * 0.85; c.fillText("Paper Crane Coffee · 132 of 150", x + 205, y + 165);
  c.textAlign = "right"; c.font = "500 38px UI"; c.globalAlpha = a * 0.6; c.fillText("now", x + w - 46, y + 100);
  c.restore();
}

/**
 * Lock screen.
 * wake 0..1: off -> dim always-on -> full brightness; unlock 0..1: Face ID lock glyph opens;
 * notif 0..1: a Wallet push springs in; hint: "Swipe up to open"
 */
export function drawLock(c, s) {
  c.fillStyle = "#000"; c.fillRect(0, 0, W, H);
  const wake = clamp(s.wake ?? 1);
  if (wake > 0) {
    c.save(); c.globalAlpha = 0.25 + 0.75 * wake; c.drawImage(wallpaper(), 0, 0); c.restore();
    if (wake < 1) { c.fillStyle = `rgba(0,0,0,${0.6 * (1 - wake)})`; c.fillRect(0, 0, W, H); }
    clockText(c, 0.55 + 0.45 * wake, (s.clockY || 0));
    statusBar(c, wake, false);
    lockGlyph(c, W / 2, 230, s.unlock || 0, wake);
    lockButtons(c, wake);
    if (s.hint) { c.save(); c.globalAlpha = s.hint * 0.85; c.fillStyle = "#fff"; c.textAlign = "center"; c.font = "500 44px UI"; c.fillText("Swipe up to open", W / 2, H - 150); c.restore(); }
    notification(c, s.notif || 0, 1540);
  }
  island(c, s.islandW || 378, s.islandH || 111);
}

/** The Wallet pass view: the Paper Crane Coffee pass presented full screen; scan 0..1 runs a scanner light over the QR. */
export function drawWalletPass(c, s) {
  c.fillStyle = "#000"; c.fillRect(0, 0, W, H);
  // blurred wallpaper behind, as iOS does
  c.save(); c.globalAlpha = 0.35; c.filter = "blur(40px)"; c.drawImage(wallpaper(), 0, 0); c.restore(); c.filter = "none";
  c.fillStyle = "rgba(0,0,0,0.35)"; c.fillRect(0, 0, W, H);
  statusBar(c, 1, false);
  c.fillStyle = "#fff"; c.font = "600 52px UI"; c.textAlign = "left"; c.fillText("Done", 60, 260);
  c.beginPath(); c.arc(W - 90, 242, 44, 0, Math.PI * 2); c.fillStyle = "rgba(255,255,255,0.18)"; c.fill();
  c.fillStyle = "#fff"; [-16, 0, 16].forEach((d) => { c.beginPath(); c.arc(W - 90 + d, 242, 6, 0, Math.PI * 2); c.fill(); });
  // the pass card, tall store-card layout
  const px = 50, py = 340, pw = W - 100, ph = 1720;
  c.save(); c.beginPath(); c.roundRect(px, py, pw, ph, 44); c.clip();
  const m = MERCHANTS[0];
  const pass = document.createElement("canvas"); pass.width = pw; pass.height = Math.round(pw * 0.631);
  drawPassFace(pass.getContext("2d"), pass.width, pass.height, m, { qr: false });
  c.fillStyle = m.c1; c.fillRect(px, py, pw, ph);
  c.drawImage(pass, px, py);
  const g = c.createLinearGradient(0, py + pass.height, 0, py + ph); g.addColorStop(0, m.c0); g.addColorStop(1, m.c1);
  c.fillStyle = g; c.fillRect(px, py + pass.height, pw, ph - pass.height);
  // barcode panel
  const qs = 520, qx = W / 2 - qs / 2, qy = py + ph - qs - 230;
  c.fillStyle = "#fff"; c.beginPath(); c.roundRect(qx - 40, qy - 40, qs + 80, qs + 150, 28); c.fill();
  drawQR(c, qx, qy, qs, 21);
  c.fillStyle = "#0b0410"; c.font = "600 34px UI"; c.textAlign = "center"; c.fillText("PCC 0042 7781", W / 2, qy + qs + 70);
  // scanner light: a teal line with glow sweeping down the code
  if (s.scan > 0 && s.scan < 1) {
    const ly = qy - 30 + (qs + 60) * ease(s.scan);
    const lg = c.createLinearGradient(0, ly - 120, 0, ly + 20); lg.addColorStop(0, "rgba(0,224,190,0)"); lg.addColorStop(1, "rgba(0,224,190,0.45)");
    c.fillStyle = lg; c.fillRect(qx - 40, ly - 120, qs + 80, 140);
    c.fillStyle = "rgba(160,255,240,1)"; c.fillRect(qx - 50, ly, qs + 100, 8);
  }
  if (s.scan >= 1) { // scanned: the code panel glows once and a check lands
    const k = clamp((s.scan - 1) * 3);
    c.strokeStyle = `rgba(0,224,190,${0.9 * (1 - k * 0.6)})`; c.lineWidth = 10; c.beginPath(); c.roundRect(qx - 40, qy - 40, qs + 80, qs + 150, 28); c.stroke();
  }
  c.restore();
  island(c, 378, 111);
  c.fillStyle = "#fff"; c.globalAlpha = 0.9; c.beginPath(); c.roundRect(W / 2 - 200, H - 42, 400, 15, 8); c.fill(); c.globalAlpha = 1;
}

export function drawOff(c) { c.fillStyle = "#000"; c.fillRect(0, 0, W, H); island(c, 378, 111); }
