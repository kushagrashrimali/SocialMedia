// The 3D stage: one renderer, one phone, five passes, a set of camera shots cut on the music's grid.
// Everything is a pure function of time (renderAt(t)); no clocks, no animation loop.
import * as THREE from "three";
import { buildPhone, buildStudioEnv, SCREEN } from "./phone.js";
import { buildPass, MERCHANTS, PASS } from "./passes.js";
import { drawLock, drawWalletPass, drawOff, clamp, ease, eo } from "./screens.js";

const T = window.HYPE;
const lerp = (a, b, k) => a + (b - a) * k;
const inR = (t, r) => t >= r[0] && t < r[1];
const expoOut = (x) => (x >= 1 ? 1 : 1 - Math.pow(2, -10 * clamp(x)));
const expoIn = (x) => (x <= 0 ? 0 : Math.pow(2, 10 * clamp(x) - 10));
const backOut = (x, s = 1.4) => { x = clamp(x) - 1; return x * x * ((s + 1) * x + s) + 1; };

export async function buildStage(canvas) {
  await document.fonts.load("700 100px UI"); await document.fonts.load("600 100px UI"); await document.fonts.load("500 100px UI");
  const renderer = new THREE.WebGLRenderer({ canvas, antialias: true, alpha: true, preserveDrawingBuffer: true });
  renderer.setPixelRatio(1); renderer.setSize(1080, 1920, false);
  renderer.toneMapping = THREE.ACESFilmicToneMapping; renderer.toneMappingExposure = 1.05;
  renderer.outputColorSpace = THREE.SRGBColorSpace;
  const env = buildStudioEnv(renderer);
  const scene = new THREE.Scene();
  scene.background = null;
  const P = buildPhone(env); scene.add(P.phone);
  const mats = []; P.phone.traverse((o) => { if (o.material && !mats.includes(o.material)) mats.push(o.material); });
  const key = new THREE.DirectionalLight(0xffffff, 1.0); key.position.set(-6, 8, 10); scene.add(key);
  const rim = new THREE.DirectionalLight(0xb9a6ff, 1.4); rim.position.set(8, 2, -6); scene.add(rim);
  scene.add(new THREE.HemisphereLight(0xe6ddfb, 0x8b6fd6, 0.3));   // the lilac set lights the product from all round
  const passes = MERCHANTS.map((m) => { const p = buildPass(m, env); scene.add(p.group); return p; });
  passes.forEach((p) => p.group.traverse((o) => { if (o.material && !mats.includes(o.material)) mats.push(o.material); }));
  const camera = new THREE.PerspectiveCamera(30, 1080 / 1920, 0.1, 400);
  const look = new THREE.Vector3();

  function setCam(x, y, z, tx, ty, tz, fov = 30) { camera.position.set(x, y, z); look.set(tx, ty, tz); camera.lookAt(look); camera.fov = fov; camera.updateProjectionMatrix(); }
  function envSweep(r) { mats.forEach((m) => { if (m.envMapRotation) m.envMapRotation.set(0, r, 0); }); }
  function showPasses(v) { passes.forEach((p) => (p.group.visible = v)); }
  function screen(fn, s) { fn(P.ctx, s); P.tex.needsUpdate = true; }

  // ------------------------------------------------------------------ shots
  function shotEdge(t) {                       // on the bright set: a light runs across the black glass and the titanium
    const k = (t - T.edge[0]) / (T.edge[1] - T.edge[0]);
    screen(drawOff, {}); showPasses(false); P.phone.visible = true;
    renderer.toneMappingExposure = lerp(0.75, 1.1, eo(k * 2.2));
    P.phone.position.set(0, 0, 0); P.phone.rotation.set(0.1, lerp(0.95, 0.7, ease(k)), -0.05);
    envSweep(lerp(-2.2, 1.0, ease(k)));
    const d = lerp(33, 27, eo(k));
    setCam(lerp(1.5, 0.5, k), lerp(5.0, 4.0, k), d, 0, lerp(2.6, 2.0, k), 0, 28);
  }
  function shotWake(t) {                       // the phone turns to camera, wakes; Face ID opens the lock (we push in to see it)
    const k = (t - T.wake[0]) / (T.wake[1] - T.wake[0]);
    showPasses(false);
    P.phone.position.set(0, 0, 0); P.phone.rotation.set(0.06, lerp(0.5, 0.06, eo(k * 1.2)), 0);
    envSweep(lerp(1.0, 0.2, eo(k)));
    screen(drawLock, { wake: eo((t - T.wakeOn) / 0.35), unlock: (t - T.unlock) / 0.45, hint: clamp((t - T.hint) / 0.3) });
    // wide -> a push toward the top of the screen as the lock opens -> settle back
    const push = ease(clamp((t - (T.unlock - 0.35)) / 0.45)) * (1 - ease(clamp((t - (T.hint + 0.05)) / 0.5)));
    const d = lerp(lerp(46, 34, eo(k)), 17, push);
    setCam(0, lerp(0.6, 4.6, push), d, 0, lerp(0.3, 4.4, push), 0);
  }
  function shotStack(t) {                      // every kind of pass flies in, faster and faster, into one stack
    P.phone.visible = false; showPasses(true);
    envSweep(lerp(-0.6, 0.8, (t - T.stack[0]) / 1.5));
    const from = [[-24, 14, -30, 2.2], [26, -8, -26, -2.6], [-20, -22, -20, 3.1], [22, 24, -24, -1.7], [0, -30, -18, 2.6]];
    passes.forEach((p, i) => {
      const t0 = T.lands[i] - (i < 2 ? 0.45 : 0.3), k = clamp((t - t0) / (T.lands[i] - t0));
      const f = from[i], e = expoOut(k), er = expoOut(k * 1.7);   // each pass is square to the stack before it arrives
      const sx = 0, sy = (i - 2) * 0.2, sz = i * 0.3;                 // spaced so no pass cuts through its neighbour
      p.group.position.set(lerp(f[0], sx, e), lerp(f[1], sy, e), lerp(f[2], sz, e));
      p.group.rotation.set(lerp(f[3], -0.3, er), lerp(-f[3] * 0.8, 0.5, er), lerp(f[3] * 0.6, -0.08, er));
      p.group.visible = t >= t0;
    });
    // the stack whips away toward camera-left at the end
    const w = clamp((t - T.whip) / (T.stack[1] - T.whip));
    const grp = expoIn(w);
    passes.forEach((p) => { p.group.position.x += -grp * 30; p.group.rotation.y += grp * 2.4; p.group.position.z += grp * 8; });
    const k = (t - T.stack[0]) / 1.5;
    setCam(lerp(-3, 2, k), lerp(6, 4, k), lerp(36, 31, eo(k)), 0, 0.4, 0, 32);
  }
  function shotPass(t) {                       // the pass, presented on the phone: camera keeps pushing in
    const k = (t - T.pass[0]) / (T.pass[1] - T.pass[0]);
    showPasses(false); P.phone.visible = true;
    P.phone.position.set(0, 0, 0); P.phone.rotation.set(0.05, lerp(-0.5, 0.18, ease(k)), 0.02);
    envSweep(lerp(-1.0, 0.6, k));
    screen(drawWalletPass, { scan: 0 });
    const d = lerp(52, 32, eo(k * 1.15));
    setCam(0, 0.4, d, 0, 0.2, 0);
  }
  function shotScan(t) {                       // macro on the code; a scanner's light runs over it
    showPasses(false); P.phone.visible = true;
    const k = (t - T.scan[0]) / (T.scan[1] - T.scan[0]);
    P.phone.position.set(0, 0, 0); P.phone.rotation.set(-0.12, 0.22, 0.04);
    envSweep(lerp(0.4, -0.4, k));
    const sr = T.scanRun, s = (t - sr[0]) / (sr[1] - sr[0]);
    screen(drawWalletPass, { scan: s < 0 ? 0 : s });
    const qy = -1.6, d = lerp(15.5, 13.5, eo(k));
    setCam(2.2, qy + 2.2, d, 0.1, qy, 0.4, 28);
  }
  function shotPush(t) {                       // lock screen; the Wallet push springs in: +18 points
    showPasses(false); P.phone.visible = true;
    const k = (t - T.push[0]) / (T.push[1] - T.push[0]);
    P.phone.position.set(0, 0, 0); P.phone.rotation.set(0.04, lerp(-0.22, -0.08, k), 0);
    envSweep(lerp(0.8, 0.2, k));
    screen(drawLock, { wake: 1, unlock: 1, notif: (t - T.notif) / 0.55 });
    const d = lerp(38, 35, k);
    setCam(0, -0.2, d, 0, -0.6, 0);
  }
  function shotSpin(t) {                       // everything accelerates: the phone spins, passes orbit faster, then flash cuts
    const s0 = T.spin[0], k = (t - s0) / (T.spin[1] - s0);
    P.phone.visible = true; showPasses(true);
    screen(drawLock, { wake: 1, unlock: 1, notif: 1 });
    let cam = 0; T.flashes.forEach((f, i) => { if (t >= f) cam = i + 1; });
    if (cam === 0) {
      const kk = (t - s0) / (T.flashes[0] - s0);
      const ang = 0.15 + Math.pow(kk, 2.2) * Math.PI * 2.6;     // spin speeds up (quadratic)
      P.phone.position.set(0, 0, 0); P.phone.rotation.set(0.1, ang, 0);
      envSweep(ang * 0.3);
      const orb = Math.pow(kk, 2) * Math.PI * 3 + 0.4;
      passes.forEach((p, i) => {
        const a = orb + i * (Math.PI * 2 / 5), r = 12.5;
        p.group.position.set(Math.cos(a) * r, Math.sin(a * 0.5 + i) * 1.2, Math.sin(a) * r);
        p.group.rotation.set(0.1, -a + Math.PI / 2, 0.15 * Math.sin(a));
        p.group.scale.setScalar(0.9);
      });
      setCam(lerp(-6, 6, kk), lerp(9, 4, kk), lerp(48, 40, kk), 0, 0, 0, 34);
      return;
    }
    // flash cuts on the roll: each a short macro of a real detail, each pushing in
    const f0 = T.flashes[cam - 1], f1 = cam < T.flashes.length ? T.flashes[cam] : T.spin[1], q = (t - f0) / (f1 - f0);
    passes.forEach((p) => (p.group.visible = false));
    P.phone.position.set(0, 0, 0);
    if (cam === 1) { P.phone.rotation.set(0.12, Math.PI + 0.5, 0); envSweep(lerp(-1, 1, q)); setCam(2.4, 6.4, lerp(13, 11, q), 1.5, 5.1, 0, 26); }        // the lenses
    else if (cam === 2) { P.phone.rotation.set(0.0, 1.25, 0.1); envSweep(lerp(2.6, 1.6, q)); setCam(-3.5, 3.4, lerp(13.5, 12, q), -1.1, 2.8, 3.2, 26); }          // buttons and the titanium edge
    else if (cam === 3) { P.phone.visible = false; const p = passes[1].group; p.visible = true; p.position.set(0, 0, 0); p.rotation.set(-0.2, lerp(-0.5, -0.3, q), 0.05); envSweep(lerp(-1, 1, q)); setCam(0, 0.6, lerp(15, 12, q), 0, 0, 0, 30); }
    else if (cam === 4) { P.phone.rotation.set(0.05, 0.25, 0); envSweep(lerp(0.5, -0.5, q)); setCam(0.5, 6.5, lerp(10, 8, q), 0, 6.2, 0, 26); }           // the island
    else if (cam === 5) { P.phone.visible = false; const p = passes[3].group; p.visible = true; p.position.set(0, 0, 0); p.rotation.set(-0.3, lerp(0.6, 0.4, q), -0.05); envSweep(lerp(1, -1, q)); setCam(0, 0.4, lerp(15, 12, q), 0, 0, 0, 30); }
    else { P.phone.rotation.set(0.05, lerp(0.6, 0.1, q), 0); passes.forEach((p, i) => { p.group.visible = true; p.group.position.set(-0.6 + i * 0.3, 1.5 + i * 0.35, -2 - i * 0.6); p.group.rotation.set(-0.1, 0.2, 0.05 * i); }); envSweep(lerp(-0.4, 0.4, q)); setCam(0, 0.5, lerp(40, 32, eo(q)), 0, 0.5, 0, 32); }
  }

  function renderAt(t) {
    passes.forEach((p) => p.group.scale.setScalar(1));
    renderer.toneMappingExposure = 1.1; P.phone.visible = true;
    let live = true;
    if (inR(t, T.edge)) shotEdge(t);
    else if (inR(t, T.wake)) shotWake(t);
    else if (inR(t, T.stack)) shotStack(t);
    else if (inR(t, T.pass)) shotPass(t);
    else if (inR(t, T.scan)) shotScan(t);
    else if (inR(t, T.push)) shotPush(t);
    else if (inR(t, T.spin)) shotSpin(t);
    else live = false;
    canvas.style.visibility = live ? "visible" : "hidden";
    // the capture pipeline may touch the canvas between frames: pin its buffer and viewport on every render
    if (canvas.width !== 1080 || canvas.height !== 1920) renderer.setSize(1080, 1920, false);
    renderer.setViewport(0, 0, 1080, 1920);
    camera.aspect = 1080 / 1920; camera.updateProjectionMatrix();
    if (live) renderer.render(scene, camera);
    return canvas.width + "x" + canvas.height;
  }
  return { renderAt };
}
