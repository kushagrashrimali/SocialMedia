// The hero phone: the iPhone 17 Pro model the user supplied (assets/model, FBX + PBR maps, Apple logo painted
// out of the maps), with our own live screen laid exactly over the model's display.
// Model units are centimetres. After centring, the screen faces +z, the camera plateau faces -z.
import * as THREE from "three";
import { FBXLoader } from "three/addons/loaders/FBXLoader.js";

// the display's rectangle in the model's texture atlas (pixels in the 2048 maps, measured from BaseColor)
const ATLAS = 2048, SCR = { x0: 19, x1: 581, y0: 801, y1: 2032, r: 36 };
export const SCREEN_PX = { w: 1179, h: Math.round(1179 * (SCR.y1 - SCR.y0) / (SCR.x1 - SCR.x0)) };

function tex(loader, f, srgb) {
  const t = loader.load("./assets/model/" + f);
  if (srgb) t.colorSpace = THREE.SRGBColorSpace;
  t.anisotropy = 8;
  return t;
}

function roundedPlane(w, h, r, seg = 12) {
  const s = new THREE.Shape(), x = -w / 2, y = -h / 2;
  s.moveTo(x + r, y); s.lineTo(x + w - r, y); s.absarc(x + w - r, y + r, r, -Math.PI / 2, 0, false);
  s.lineTo(x + w, y + h - r); s.absarc(x + w - r, y + h - r, r, 0, Math.PI / 2, false);
  s.lineTo(x + r, y + h); s.absarc(x + r, y + h - r, r, Math.PI / 2, Math.PI, false);
  s.lineTo(x, y + r); s.absarc(x + r, y + r, r, Math.PI, Math.PI * 1.5, false);
  const g = new THREE.ShapeGeometry(s, seg), p = g.attributes.position, uv = g.attributes.uv;
  for (let i = 0; i < p.count; i++) uv.setXY(i, p.getX(i) / w + 0.5, p.getY(i) / h + 0.5);
  return g;
}

export async function loadPhone(envMap) {
  const tl = new THREE.TextureLoader();
  const body = new THREE.MeshPhysicalMaterial({
    map: tex(tl, "pro_BaseColor.png", true), metalnessMap: tex(tl, "pro_Metallic.png"), roughnessMap: tex(tl, "pro_Roughness.png"),
    normalMap: tex(tl, "pro_Normal.png"), metalness: 1, roughness: 0.9, envMap, envMapIntensity: 1.0, clearcoat: 0.35, clearcoatRoughness: 0.25,
  });
  const fbx = await new FBXLoader().loadAsync("./assets/model/iphone17pro.fbx");
  let main = null;
  fbx.traverse((o) => { if (o.isMesh) { o.material = body; if (!main || o.geometry.attributes.position.count > main.geometry.attributes.position.count) main = o; } });

  // fit the atlas -> model mapping on the front face (the display side is the model's -z face)
  const g = main.geometry, P = g.attributes.position, N = g.attributes.normal, UV = g.attributes.uv;
  let zmin = Infinity; for (let i = 0; i < P.count; i++) zmin = Math.min(zmin, P.getZ(i));
  const pts = [];
  for (let i = 0; i < P.count; i++) {
    if (P.getZ(i) < zmin + 0.004 && N.getZ(i) < -0.95) pts.push([UV.getX(i), UV.getY(i), P.getX(i), P.getY(i)]);
  }
  const fit = (k) => {                                             // least squares: pos[k] = a*uv + b
    let n = pts.length, su = 0, sp = 0, suu = 0, sup = 0, j = k === 2 ? 0 : 1;
    pts.forEach((q) => { su += q[j]; sp += q[k]; suu += q[j] * q[j]; sup += q[j] * q[k]; });
    const a = (n * sup - su * sp) / (n * suu - su * su); return [a, (sp - a * su) / n];
  };
  const [ax, bx] = fit(2), [ay, by] = fit(3);
  const u0 = SCR.x0 / ATLAS, u1 = SCR.x1 / ATLAS, v0 = 1 - SCR.y1 / ATLAS, v1 = 1 - SCR.y0 / ATLAS;
  const X0 = ax * u0 + bx, X1 = ax * u1 + bx, Y0 = ay * v0 + by, Y1 = ay * v1 + by;
  const sw = Math.abs(X1 - X0), sh = Math.abs(Y1 - Y0), cx = (X0 + X1) / 2, cy = (Y0 + Y1) / 2;

  // live screen + a clear cover glass that only adds reflections
  const canvas = document.createElement("canvas"); canvas.width = SCREEN_PX.w; canvas.height = SCREEN_PX.h;
  const screenTex = new THREE.CanvasTexture(canvas); screenTex.colorSpace = THREE.SRGBColorSpace; screenTex.anisotropy = 8;
  const rr = SCR.r / (SCR.x1 - SCR.x0) * sw;
  const screen = new THREE.Mesh(roundedPlane(sw, sh, rr), new THREE.MeshBasicMaterial({ map: screenTex, toneMapped: false }));
  screen.position.set(cx, cy, zmin - 0.003); screen.rotation.y = Math.PI;      // face -z, like the display
  const cover = new THREE.Mesh(roundedPlane(sw * 1.004, sh * 1.002, rr), new THREE.MeshPhysicalMaterial({
    color: 0x000000, roughness: 0.03, metalness: 0, clearcoat: 1, clearcoatRoughness: 0.02, envMap, envMapIntensity: 1.2,
    transparent: true, blending: THREE.AdditiveBlending, depthWrite: false }));
  cover.position.set(cx, cy, zmin - 0.006); cover.rotation.y = Math.PI;
  fbx.add(screen, cover);

  // centre the model on the screen's centre and turn it so the display faces +z
  const box = new THREE.Box3().setFromObject(fbx), c = box.getCenter(new THREE.Vector3());
  fbx.position.set(-cx, -cy, -c.z);
  const phone = new THREE.Group(); const turn = new THREE.Group();
  turn.rotation.y = Math.PI; turn.add(fbx); phone.add(turn);
  const size = box.getSize(new THREE.Vector3());
  return { phone, canvas, ctx: canvas.getContext("2d"), screenTex, body, size, screenSize: { w: sw, h: sh }, mats: [body, cover.material] };
}
