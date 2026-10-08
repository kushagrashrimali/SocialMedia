// A photoreal phone, modelled in code (no third-party model): a natural-titanium band with a polished chamfer,
// a ceramic-glass front over a live screen, a frosted-glass back with a three-lens camera plateau, and the
// side buttons. Units are centimetres (70.6 x 146.6 x 8.25 mm). The screen is a canvas texture redrawn per frame.
import * as THREE from "three";

const W = 7.06, H = 14.66, D = 0.825, R = 1.12;       // outline and corner radius
export const SCREEN = { w: 6.62, h: 14.22, r: 0.98, px: 1179, py: 2556 };

function roundedRect(w, h, r) {
  const s = new THREE.Shape(), x = -w / 2, y = -h / 2;
  s.moveTo(x + r, y);
  s.lineTo(x + w - r, y); s.absarc(x + w - r, y + r, r, -Math.PI / 2, 0, false);
  s.lineTo(x + w, y + h - r); s.absarc(x + w - r, y + h - r, r, 0, Math.PI / 2, false);
  s.lineTo(x + r, y + h); s.absarc(x + r, y + h - r, r, Math.PI / 2, Math.PI, false);
  s.lineTo(x, y + r); s.absarc(x + r, y + r, r, Math.PI, Math.PI * 1.5, false);
  return s;
}

// a rounded-rect plane whose UVs run 0..1 across its bounds (for the screen texture)
function roundedPlane(w, h, r) {
  const g = new THREE.ShapeGeometry(roundedRect(w, h, r), 24);
  const p = g.attributes.position, uv = g.attributes.uv;
  for (let i = 0; i < p.count; i++) uv.setXY(i, p.getX(i) / w + 0.5, p.getY(i) / h + 0.5);
  return g;
}

export function buildPhone(env) {
  const phone = new THREE.Group();

  // titanium band: a rounded-rect extrusion with a small bevel = the flat sides and the polished chamfer
  const bandGeo = new THREE.ExtrudeGeometry(roundedRect(W - 0.12, H - 0.12, R - 0.06), {
    depth: D - 0.12, bevelEnabled: true, bevelThickness: 0.06, bevelSize: 0.06, bevelSegments: 4, curveSegments: 32,
  });
  bandGeo.translate(0, 0, -(D - 0.12) / 2);
  const titanium = new THREE.MeshPhysicalMaterial({
    color: 0x8f8a84, metalness: 1, roughness: 0.32, envMap: env, envMapIntensity: 1.15,
    clearcoat: 0.25, clearcoatRoughness: 0.4,
  });
  const band = new THREE.Mesh(bandGeo, titanium);
  phone.add(band);

  // front: black glass with a thin border, then the screen, then the cover glass that carries the reflections
  const blackGlass = new THREE.MeshPhysicalMaterial({ color: 0x020203, roughness: 0.08, metalness: 0, clearcoat: 1, clearcoatRoughness: 0.03, envMap: env, envMapIntensity: 1.2 });
  const front = new THREE.Mesh(new THREE.ShapeGeometry(roundedRect(W - 0.14, H - 0.14, R - 0.07), 32), blackGlass);
  front.position.z = D / 2 + 0.002;
  phone.add(front);

  const canvas = document.createElement("canvas");
  canvas.width = SCREEN.px; canvas.height = SCREEN.py;
  const tex = new THREE.CanvasTexture(canvas);
  tex.colorSpace = THREE.SRGBColorSpace;
  tex.anisotropy = 4;
  const screenMat = new THREE.MeshBasicMaterial({ map: tex, toneMapped: false });
  const screen = new THREE.Mesh(roundedPlane(SCREEN.w, SCREEN.h, SCREEN.r), screenMat);
  screen.position.z = D / 2 + 0.004;
  phone.add(screen);

  // cover glass: clear, only its reflections show (additive specular sheen)
  const cover = new THREE.Mesh(new THREE.ShapeGeometry(roundedRect(W - 0.14, H - 0.14, R - 0.07), 32),
    new THREE.MeshPhysicalMaterial({ color: 0x000000, roughness: 0.02, metalness: 0, clearcoat: 1, clearcoatRoughness: 0.02,
      envMap: env, envMapIntensity: 1.15, transparent: true, opacity: 1, blending: THREE.AdditiveBlending, depthWrite: false }));
  cover.position.z = D / 2 + 0.008;
  phone.add(cover);

  // back: frosted glass in the band's colour, a camera plateau with three lenses, a flash and a LiDAR dot
  const back = new THREE.Mesh(new THREE.ShapeGeometry(roundedRect(W - 0.14, H - 0.14, R - 0.07), 32),
    new THREE.MeshPhysicalMaterial({ color: 0x2b2a29, roughness: 0.55, metalness: 0.2, clearcoat: 0.6, clearcoatRoughness: 0.5, envMap: env }));
  back.position.z = -D / 2 - 0.002; back.rotation.y = Math.PI;
  phone.add(back);
  const plate = new THREE.Mesh(new THREE.ExtrudeGeometry(roundedRect(3.5, 3.6, 0.9), { depth: 0.08, bevelEnabled: true, bevelThickness: 0.03, bevelSize: 0.03, bevelSegments: 3, curveSegments: 24 }),
    new THREE.MeshPhysicalMaterial({ color: 0x2f2e2d, roughness: 0.2, metalness: 0.3, clearcoat: 1, clearcoatRoughness: 0.08, envMap: env }));
  plate.position.set(-W / 2 + 0.3 + 1.75, H / 2 - 0.3 - 1.8, -D / 2 - 0.1); plate.rotation.y = Math.PI;
  phone.add(plate);
  const ringMat = new THREE.MeshPhysicalMaterial({ color: 0x9a948d, metalness: 1, roughness: 0.18, envMap: env });
  const lensMat = new THREE.MeshPhysicalMaterial({ color: 0x050608, metalness: 0.2, roughness: 0.02, clearcoat: 1, clearcoatRoughness: 0, envMap: env, envMapIntensity: 2.2, iridescence: 0.6, iridescenceIOR: 1.6 });
  [[-0.85, 0.85], [-0.85, -0.85], [0.85, 0]].forEach(([dx, dy]) => {
    const g = new THREE.Group();
    const ring = new THREE.Mesh(new THREE.CylinderGeometry(0.66, 0.68, 0.22, 48), ringMat); ring.rotation.x = Math.PI / 2;
    const lens = new THREE.Mesh(new THREE.CylinderGeometry(0.5, 0.5, 0.24, 48), lensMat); lens.rotation.x = Math.PI / 2;
    g.add(ring, lens);
    g.position.set(-W / 2 + 0.3 + 1.75 - dx, H / 2 - 0.3 - 1.8 + dy, -D / 2 - 0.25);
    phone.add(g);
  });

  // side buttons (action + volume on the left, side button on the right)
  const btn = (x, y, h) => {
    const m = new THREE.Mesh(new THREE.CapsuleGeometry(0.09, h, 6, 12), titanium);
    m.position.set(x, y, 0); m.scale.set(1, 1, 1.6);
    phone.add(m);
  };
  btn(-W / 2 - 0.02, 4.1, 0.55); btn(-W / 2 - 0.02, 2.75, 0.95); btn(-W / 2 - 0.02, 1.45, 0.95); btn(W / 2 + 0.02, 2.4, 1.6);

  return { phone, canvas, ctx: canvas.getContext("2d"), tex, screen, cover };
}

// the studio the product reflects: the same lilac set the film shows (held low so glass stays deep), with long, bright
// strip lights (Apple-style product light) so metal and glass carry clean highlights; a wide soft top box keeps the
// titanium readable from every angle, and a lilac floor bounce lifts the lower edges
export function buildStudioEnv(renderer) {
  const s = new THREE.Scene();
  s.background = new THREE.Color(0xcbbcf3).multiplyScalar(0.26);
  const strip = (w, h, x, y, z, ry, rx, c, k) => {
    const m = new THREE.Mesh(new THREE.PlaneGeometry(w, h), new THREE.MeshBasicMaterial({ color: new THREE.Color(c).multiplyScalar(k), side: THREE.DoubleSide }));
    m.position.set(x, y, z); m.rotation.set(rx || 0, ry, 0); s.add(m);
  };
  strip(3.2, 22, -8, 0, 4, Math.PI / 2.5, 0, 0xffffff, 6.5);      // long key strip, front left
  strip(2.2, 22, 8, 0, 2, -Math.PI / 2.3, 0, 0xe3dcff, 6);         // cool rim strip, right
  strip(2.0, 22, 0, 0, -9, 0, 0, 0xffffff, 3.5);                  // back strip (edges, rims)
  strip(18, 5, 0, 9, 1, 0, Math.PI / 2, 0xffffff, 2.2);           // top softbox
  strip(10, 1.6, 0, -7, 7, 0, -Math.PI / 4, 0xffe6cc, 1.4);       // warm floor bounce
  strip(4, 4, 6, 6, 8, -Math.PI / 4, 0, 0x9f7bff, 2.5);            // a violet kicker (brand light)
  strip(40, 40, 0, -11, 0, 0, Math.PI / 2, 0xd9ccfb, 0.7);          // the lilac floor of the set
  const pm = new THREE.PMREMGenerator(renderer);
  const env = pm.fromScene(s, 0.035).texture;
  pm.dispose();
  return env;
}
