// The 3D stage: the user's iPhone 17 Pro model under studio light, shot in four product passes of the film.
// Everything is a pure function of time (renderAt(t)); no clocks, no animation loop.
import * as THREE from "three";
import { RoomEnvironment } from "three/addons/environments/RoomEnvironment.js";
import { loadPhone } from "./phone.js";
import { drawLock, drawStack, drawPassView, drawOff, clamp, ease, eo } from "./screens.js";

const T = window.REEL;
const lerp = (a, b, k) => a + (b - a) * k;
const inR = (t, r) => t >= r[0] && t < r[1];
const p4o = (x) => 1 - Math.pow(1 - clamp(x), 4);           // power4.out
const p4i = (x) => Math.pow(clamp(x), 4);                   // power4.in
const expoOut = (x) => (x >= 1 ? 1 : 1 - Math.pow(2, -10 * clamp(x)));

// a studio for reflections: the neutral room plus long strip lights and a lilac bounce, so the titanium and glass
// carry clean highlights and pick up the brand colour of the set
function studio(renderer) {
  const room = new RoomEnvironment();
  const strip = (w, h, x, y, z, ry, rx, c, k) => {
    const m = new THREE.Mesh(new THREE.PlaneGeometry(w, h), new THREE.MeshBasicMaterial({ color: new THREE.Color(c).multiplyScalar(k), side: THREE.DoubleSide }));
    m.position.set(x, y, z); m.rotation.set(rx || 0, ry, 0); room.add(m);
  };
  strip(1.2, 9, -6, 2, 3, Math.PI / 2.4, 0, 0xffffff, 14);
  strip(0.9, 9, 6.5, 2, 1, -Math.PI / 2.2, 0, 0xf1ebff, 10);
  strip(10, 2.2, 0, -4.5, 4, 0, -Math.PI / 3, 0xb99cff, 2.2);
  const pm = new THREE.PMREMGenerator(renderer);
  const env = pm.fromScene(room, 0.03).texture; pm.dispose();
  return env;
}

export async function buildStage(canvas) {
  await document.fonts.load("700 100px UI"); await document.fonts.load("600 100px UI"); await document.fonts.load("500 100px UI");
  const renderer = new THREE.WebGLRenderer({ canvas, antialias: true, alpha: true, preserveDrawingBuffer: true });
  renderer.setPixelRatio(1); renderer.setSize(1080, 1920, false);
  renderer.toneMapping = THREE.ACESFilmicToneMapping; renderer.toneMappingExposure = 1.0;
  renderer.outputColorSpace = THREE.SRGBColorSpace;
  const env = studio(renderer);
  const scene = new THREE.Scene();
  const P = await loadPhone(env);
  scene.add(P.phone);
  // lenses and the camera plateau: glassier than the shared body material
  // each lens: the model's titanium ring stays; a disc of coated lens glass is laid over its centre (a drawn lens
  // texture: black aperture, blue-violet element rings) so close-ups read as real optics
  const lensTex = (() => {
    const cv = document.createElement("canvas"); cv.width = cv.height = 512; const c = cv.getContext("2d");
    const g = c.createRadialGradient(256, 256, 0, 256, 256, 256);
    g.addColorStop(0, "#000000"); g.addColorStop(0.32, "#04050a"); g.addColorStop(0.36, "#121833"); g.addColorStop(0.42, "#06070d");
    g.addColorStop(0.62, "#0b0e1c"); g.addColorStop(0.66, "#171d36"); g.addColorStop(0.7, "#07080f"); g.addColorStop(0.94, "#0d0f18"); g.addColorStop(1, "#2a2d36");
    c.fillStyle = g; c.fillRect(0, 0, 512, 512);
    const t = new THREE.CanvasTexture(cv); t.colorSpace = THREE.SRGBColorSpace; return t;
  })();
  const glass = new THREE.MeshPhysicalMaterial({ map: lensTex, metalness: 0, roughness: 0.05, clearcoat: 1, clearcoatRoughness: 0.02,
    envMap: env, envMapIntensity: 1.1, iridescence: 0.4, iridescenceIOR: 1.6, iridescenceThicknessRange: [180, 520] });
  P.phone.traverse((o) => {
    if (!o.isMesh || !/polySurface(4|6|7)$/.test(o.name)) return;
    o.geometry.computeBoundingBox(); const bb = o.geometry.boundingBox, c = bb.getCenter(new THREE.Vector3()), R = (bb.max.x - bb.min.x) / 2;
    const disc = new THREE.Mesh(new THREE.CircleGeometry(R * 0.77, 64), glass);
    disc.position.set(c.x, c.y, bb.max.z + 0.002);          // the back faces +z in model space
    o.parent.add(disc);
  });
  const mats = [P.body, glass, ...P.mats.slice(1)];
  scene.add(new THREE.HemisphereLight(0xf3eeff, 0x6b4bc4, 0.35));
  const key = new THREE.DirectionalLight(0xffffff, 1.2); key.position.set(-8, 10, 12); scene.add(key);
  const camera = new THREE.PerspectiveCamera(30, 1080 / 1920, 0.1, 500);
  const look = new THREE.Vector3(), tmp = new THREE.Vector3();

  function cam(x, y, z, tx, ty, tz, fov = 30) { camera.position.set(x, y, z); look.set(tx, ty, tz); camera.lookAt(look); camera.fov = fov; camera.updateProjectionMatrix(); }
  function envTurn(r) { mats.forEach((m) => m.envMapRotation && m.envMapRotation.set(0, r, 0)); }
  function screen(fn, s) { fn(P.ctx, s); P.screenTex.needsUpdate = true; }
  function pose(px, py, pz, rx, ry, rz, s = 1) { P.phone.position.set(px, py, pz); P.phone.rotation.set(rx, ry, rz); P.phone.scale.setScalar(s); }
  // where a point on the phone's screen lands on the frame (for the HTML cards that rise out of it)
  function project(lx, ly) {
    tmp.set(lx, ly, 0.5); P.phone.localToWorld(tmp); tmp.project(camera);
    return { x: (tmp.x + 1) / 2 * 1080, y: (1 - tmp.y) / 2 * 1920 };
  }

  // ---------------------------------------------------------------- shots
  // S1 · the phone lies back on the lilac set; it wakes, three Wallet pushes rise out of it, and the camera
  // pushes into the top one (a zoom-through into the first card)
  function shotOpen(t) {
    const k = (t - T.s1_open[0]) / (T.s1_open[1] - T.s1_open[0]);
    pose(0, 0, 0, -1.02, 0.3, 0.18);
    screen(drawLock, { wake: eo((t - T.wake) / 0.35), notif: 0 });
    envTurn(lerp(-0.9, 0.4, ease(k)));
    const push = p4i((t - 1.55) / 0.45);                       // the zoom-through at the end
    const d = lerp(lerp(46, 40, eo(k)), 22, push);
    cam(lerp(3, 1.2, k), lerp(9, 7.5, k) * (d / 40), d, 0, lerp(1.5, 3.5, push), 0, 30);
    const top = project(0, 7.0);
    return { anchor: top, push };
  }

  // S5 · the phone turns in on the violet ground (still pushing in after the mark's press), the lock screen
  // gets its push on the beat, the camera travels up to it; then the phone whips out left
  function shotLock(t) {
    const s0 = T.s5_lock[0], k = (t - s0) / 3.0;
    const inK = expoOut((t - s0) / 0.8);
    const out = p4i((t - (T.s5_lock[1] - 0.35)) / 0.35);
    pose(lerp(0, -16, out), 0, 0, 0.04, lerp(-0.75, 0.12, inK) - out * 0.9, lerp(0.06, 0, inK), lerp(0.84, 1, inK));
    screen(drawLock, { wake: 1, notif: (t - T.notif) / 0.55 });
    envTurn(lerp(1.1, -0.2, ease(k)));
    const up = ease((t - (T.notif + 0.3)) / 1.1);               // travel to the notification
    cam(0, lerp(0.4, -3.3, up), lerp(44, 25, up), 0, lerp(0.2, -3.6, up), 0, 30);
  }

  // S10 · macro cuts on the drop: lenses, titanium edge, the pass on screen, the island, lenses, a whole-phone spin
  function shotMacro(t) {
    const c = T.cuts; let i = 0; c.forEach((x, j) => { if (t >= x) i = j; });
    const a = c[i], b = i + 1 < c.length ? c[i + 1] : T.s10_macro[1], q = (t - a) / (b - a);
    screen(drawPassView, {});
    if (i === 0) { pose(0, 0, 0, 0.18, Math.PI + lerp(0.55, 0.3, q), 0.05); envTurn(lerp(-2.6, -2.0, q)); cam(-2.8, 7.4, lerp(15, 12.5, q), -2.2, 5.6, 0, 26); }
    else if (i === 1) { pose(0, 0, 0, 0.05, lerp(1.2, 1.05, q), 0.12); envTurn(lerp(0.8, -0.8, q)); cam(-5.5, 3.2, lerp(16, 14, q), -1.6, 2.6, 2.5, 26); }
    else if (i === 2) { pose(0, 0, 0, 0.06, lerp(-0.42, -0.3, q), 0.02); envTurn(lerp(-0.4, 0.5, q)); cam(0.5, -1.2, lerp(30, 26, q), 0, -1.6, 0, 30); }
    else if (i === 3) { pose(0, 0, 0, 0.04, lerp(0.2, 0.1, q), 0); envTurn(lerp(0.6, -0.6, q)); cam(0.4, 7.4, lerp(12, 10, q), 0, 6.9, 0, 26); }
    else if (i === 4) { pose(0, 0, 0, 0.12, Math.PI + lerp(0.15, 0.3, q), -0.04); envTurn(lerp(-2.4, -1.9, q)); cam(-1.4, 6.0, lerp(10.5, 9.2, q), -1.7, 5.6, 0, 26); }
    else { pose(0, 0, 0, 0.08, lerp(-Math.PI * 1.15, 0.15, p4o(q)), 0); envTurn(lerp(-2, 0.3, q)); cam(0, 0.3, lerp(52, 44, q), 0, 0, 0, 30); }
  }

  // S12 · front-on hero: the passes file into the Wallet stack, sooner each time; then the phone rises out (upward seam)
  function shotStack(t) {
    const s0 = T.s12_stack[0], k = (t - s0) / 3.0;
    const up = p4i((t - (T.s12_stack[1] - 0.35)) / 0.35);
    pose(0, lerp(0, 26, up), 0, 0.05, lerp(-0.32, 0.18, ease(k)), 0.0, 1);
    screen(drawStack, { k: T.stackIn.map((x) => (t - x) / 0.4) });
    envTurn(lerp(-0.6, 0.6, k));
    cam(0, lerp(3.2, 2.6, k), lerp(47, 42, eo(k)), 0, lerp(2.6, 2.2, k), 0, 30);   // the phone sits low, under its line
  }

  function renderAt(t) {
    renderer.toneMappingExposure = 1.0;
    let live = true, info = null;
    if (inR(t, T.s1_open)) info = shotOpen(t);
    else if (inR(t, T.s5_lock)) shotLock(t);
    else if (inR(t, T.s10_macro)) shotMacro(t);
    else if (inR(t, T.s12_stack)) shotStack(t);
    else live = false;
    canvas.style.visibility = live ? "visible" : "hidden";
    if (canvas.width !== 1080 || canvas.height !== 1920) renderer.setSize(1080, 1920, false);
    renderer.setViewport(0, 0, 1080, 1920);
    camera.aspect = 1080 / 1920; camera.updateProjectionMatrix();
    if (live) renderer.render(scene, camera);
    // the opening's pushes ride on the phone: place them where its screen is on this frame
    const n = document.getElementById("notifs");
    if (n) {
      if (info) {
        n.style.display = "block";
        n.style.transformOrigin = "0px -110px";   // the zoom-through goes into the newest push
        n.style.transform = `translate(${info.anchor.x}px, ${info.anchor.y}px) scale(${1 + info.push * 2.4})`;
        n.style.opacity = String(1 - clamp((info.push - 0.7) / 0.3));
        // iOS-style: each new push lands in the bottom slot and lifts the earlier ones by one slot
        const kids = [...n.children], E = kids.map((_, i) => 1 - Math.pow(1 - clamp((t - T.notifs[i]) / 0.42), 3));
        kids.forEach((el, i) => {
          const lift = E.slice(i + 1).reduce((a, b) => a + b, 0);
          el.style.opacity = String(clamp(E[i] * 2.5));
          el.style.transform = `translate(-50%, ${-190 - 178 * lift + (1 - E[i]) * 90}px) scale(${lerp(0.6, 1, E[i])})`;
        });
      } else n.style.display = "none";
    }
    return canvas.width + "x" + canvas.height;
  }
  return { renderAt };
}
