"""WYSTAK palm reveal: the 10-second film, rendered frame by frame from the storyboard pipeline.

One locked-off shot on the seaside plate (storyboard/build_storyboard.py does the plate, the palms and the logo layers);
every parameter moves continuously between the six storyboard states:

  0.0-1.6  the familiar scene (fronds flutter, fountains and sea shimmer, a slow push-in starts)
  1.6-3.2  a gust bends the palms (frame 2)
  3.2-5.4  the crossing climbs to the peak, the trunks thicken, navy climbs from the roots, fronds fold (frame 3)
  5.4-6.6  fronds retract into the tips, the trunks swell into the strokes and hand over to the W (frame 4)
  6.6-7.8  the ticket appears, the purple then the teal pass swing out (frame 5)
  7.8-10.0 the supplied logo file, held (frame 6)

usage: python3 render_film.py [--workers 4] [--only 0.5,4.3,...]   -> ../renders/frames/f_0000.png ...
"""
import argparse, math, pathlib, sys
from multiprocessing import Pool
import numpy as np
from PIL import Image

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "storyboard"))
import build_storyboard as bs
import plate as pl

FPS, DUR = 30, 10.0
OUT_SIZE = 1080
FRAMES_DIR = HERE.parent / "renders" / "frames"

F2 = dict(q=0.16, bows={"T1": -14, "T2": 9, "T3": -9, "T4": 14}, sway={"T1": -4, "T2": 3, "T3": -3, "T4": 4})
F3 = dict(q=0.84, bows={"T1": -6, "T2": 4, "T3": -4, "T4": 6}, sway={"T1": -2, "T2": 6, "T3": -6, "T4": 2},
          widen=0.85, navy_rise=0.55, fold=(0.92, 0.62), sink=6)
# where each trunk ends up, inside the W (logo-file pixels, root then top): the tops stop short of the terminals so
# the rounded trunk ends stay inside the letter while it fills out around them
FINAL = {"T1": ((318, 752), (124, 265)), "T3": ((330, 752), (485, 350)),
         "T2": ((676, 752), (485, 350)), "T4": ((737, 752), (822, 120))}
PHASE = {"T1": 0.0, "T2": 0.37, "T3": 0.71, "T4": 0.19}


# ------------------------------------------------------------------------------------------------ easing
def clamp(x, a=0.0, b=1.0):
    return max(a, min(b, x))


def seg(t, t0, t1):
    return clamp((t - t0) / (t1 - t0))


def inout(x):           # sine in-out: physical, no snap
    return 0.5 - 0.5 * math.cos(math.pi * x)


def out3(x):            # cubic ease-out: things arriving
    return 1 - (1 - x) ** 3


def lerp(a, b, u):
    return a + (b - a) * u


# ------------------------------------------------------------------------------------------------ the state at time t
def tree_state(t):
    """Parameters of the palms at time t (None once the W has taken over)."""
    flutter = {k: 0.9 * math.sin(2 * math.pi * (0.42 * t + PHASE[k])) + 0.35 * math.sin(2 * math.pi * (1.13 * t + 2 * PHASE[k]))
               for k in PHASE}
    st = dict(q=0.0, bows={k: 0.0 for k in PHASE}, sway=dict(flutter), widen=0.0, navy_rise=0.0, fold=(1.0, 1.0),
              sink=0.0, lam=0.0, lam_w=0.0, crown_alpha=1.0)
    # 1.6-3.2: the gust
    u = inout(seg(t, 1.6, 3.2))
    st["q"] = lerp(0, F2["q"], u)
    for k in PHASE:
        st["bows"][k] = lerp(0, F2["bows"][k], u)
        st["sway"][k] += lerp(0, F2["sway"][k], inout(seg(t, 1.75, 3.3)))      # the fronds follow a beat late
    if t >= 3.2:
        ug = inout(seg(t, 3.2, 5.0))           # geometry: the crossing climbs, trunks straighten
        uw = inout(seg(t, 3.5, 5.4))           # thickening
        un = inout(seg(t, 3.9, 5.4))           # navy climbs
        uf = inout(seg(t, 4.2, 5.4))           # fronds fold
        st["q"] = lerp(F2["q"], F3["q"], ug)
        for k in PHASE:
            st["bows"][k] = lerp(F2["bows"][k], F3["bows"][k], ug)
            st["sway"][k] = flutter[k] * (1 - 0.6 * uf) + lerp(F2["sway"][k], F3["sway"][k], ug)
        st["widen"] = lerp(0, F3["widen"], uw)
        st["navy_rise"] = lerp(0, F3["navy_rise"], un)
        st["fold"] = (lerp(1, F3["fold"][0], uf), lerp(1, F3["fold"][1], uf))
        st["sink"] = lerp(0, F3["sink"], uf)
    if t >= 5.4:
        lam = inout(seg(t, 5.4, 5.95))         # onto the W's centre lines
        lam_w = inout(seg(t, 5.45, 5.95))      # most of the stroke width
        uf2 = inout(seg(t, 5.4, 5.9))          # fronds retract into the tips
        un2 = inout(seg(t, 5.4, 5.85))
        st["lam"], st["lam_w"] = lam, lam_w
        st["navy_rise"] = lerp(F3["navy_rise"], 1.05, un2)
        s = 1 - uf2
        st["fold"] = (F3["fold"][0] * s, F3["fold"][1] * s)
        st["sink"] = lerp(F3["sink"], 26, uf2)
        st["crown_alpha"] = clamp(s / 0.25)
        for k in PHASE:
            st["bows"][k] = F3["bows"][k] * (1 - lam)
            st["sway"][k] = F3["sway"][k] * (1 - lam) + flutter[k] * 0.4 * (1 - uf2)
    return st


def logo_state(t):
    """The logo's state at time t: how much of the W is on, ticket, fan progress, settle, file hold."""
    grow = inout(seg(t, 5.95, 6.40))
    w_on = 1.0 if t >= 6.40 else 0.0
    d = t - 6.40
    settle = 1 + (0.010 * math.sin(2 * math.pi * d / 0.55) * math.exp(-d / 0.22) if d > 0 else 0.0)
    ticket = inout(seg(t, 6.62, 6.82))
    pp = out3(seg(t, 6.70, 7.40))
    pt = out3(seg(t, 6.82, 7.57))
    started_p = t >= 6.70
    started_t = t >= 6.82
    # angular speeds for the motion blur (degrees per second)
    def speed(t0, d0, ang):
        x = seg(t, t0, t0 + d0)
        return 0 if x <= 0 or x >= 1 else ang * 3 * (1 - x) ** 2 / d0
    vp = speed(6.70, 0.70, bs.PASS_ANGLE["purple"]); vt = speed(6.82, 0.75, bs.PASS_ANGLE["teal"])
    full = seg(t, 7.62, 7.80)
    return dict(w_on=w_on, grow=grow, settle=settle, ticket=ticket, pp=pp, pt=pt, started_p=started_p, started_t=started_t,
                vp=vp, vt=vt, full=full)


# ------------------------------------------------------------------------------------------------ drawing
def placed(logo, name, out_hw, angle=0.0, zoom=1.0):
    """The logo layer in the shot, rotated about the fan pivot, and scaled about the W's foot by zoom (the settle)."""
    lay = bs.premul(logo.layers[name])
    th = math.radians(angle)
    c, s = math.cos(th), math.sin(th)
    px, py = bs.PIVOT
    R = np.array([[c, s, px - c * px - s * py], [-s, c, py + s * px - c * py], [0, 0, 1]])
    zx, zy = 500.0, 760.0
    Z = np.array([[zoom, 0, zx - zoom * zx], [0, zoom, zy - zoom * zy], [0, 0, 1]])
    S = np.array([[bs.LOGO_S, 0, bs.LOGO_X0], [0, bs.LOGO_S, bs.LOGO_Y0]])
    return bs.affine_layer(lay, S @ Z @ R, out_hw)


def card_hw(logo):
    """Half the navy pass's width, in shot pixels (from its two long edges in the file)."""
    ca, _ = logo.navy_edge
    y = 300.0
    left = 715 - 65 * (y - 20) / 540
    right = np.polyval(ca, y)
    ang = math.atan2(65, 540)
    return (right - left) * math.cos(ang) / 2 * bs.LOGO_S


def draw_trees(scene, logo, st):
    H, W = scene.H, scene.W
    img = scene.C.copy()
    drawn = np.zeros((H, W), np.float32)
    paths = {}
    for k in scene.trunks:
        p = bs.trunk_path(scene, k, st["q"], st["bows"][k])
        if st["lam"] > 0:
            # onto the final stroke line (the fourth trunk onto the navy pass's axis)
            b, tp = FINAL[k]
            b, tp = bs.to_scene(b), bs.to_scene(tp)
            n = len(scene.trunks[k]["pts"])
            s = np.linspace(0, 1, n)[:, None]
            line = b[None, :] * s + tp[None, :] * (1 - s)
            d = (b - tp) / np.linalg.norm(b - tp)
            tail = b[None, :] + d[None, :] * np.arange(1, 25)[:, None]
            final = np.vstack([line, tail])
            p = p * (1 - st["lam"]) + final * st["lam"]
        paths[k] = p
    full_hw = {k: logo.stroke_hw * 0.8 for k in PHASE}
    full_hw["T4"] = card_hw(logo) * 0.8
    for k in ("T2", "T1", "T4", "T3"):          # T3 crosses in front of T2, as in the photo
        t = scene.trunks[k]
        s = np.linspace(0, 1, len(t["hw"]))
        w = st["widen"]
        hw = t["hw"] * (1 - w) + logo.stroke_hw * 0.44 * w * (0.9 + 0.2 * s)
        hw = hw * (1 - st["lam_w"]) + full_hw[k] * st["lam_w"]
        navy = None
        if st["navy_rise"] > 0:
            edge = 1 - st["navy_rise"]
            z = np.clip((s - edge) / 0.10 + 0.5, 0, 1)
            navy = z * z * (3 - 2 * z)
        hw = np.concatenate([hw, np.full(24, hw[-1])])
        if navy is not None:
            navy = np.concatenate([navy, np.full(24, navy[-1])])
        lay = bs.render_trunk(scene, k, paths[k], hw, navy=navy, logo=logo, roundness=max(w, st["lam_w"]))
        img = bs.comp_premul(img, lay)
        drawn = np.maximum(drawn, lay[..., 3])
    if st["crown_alpha"] > 0.002:
        for k in ("T1", "T2", "T3", "T4"):
            cr = bs.place_crown(scene, k, paths[k], st["sway"][k], st["fold"], st["sink"], (H, W)) * st["crown_alpha"]
            img = bs.comp_premul(img, cr)
    return img, drawn


def draw_logo(scene, logo, ls):
    H, W = scene.H, scene.W
    img = scene.C.copy()
    z = ls["settle"]
    blank = placed(logo, "navy_blank", (H, W), zoom=z)
    if ls["ticket"] > 0:
        navy = placed(logo, "navy", (H, W), zoom=z)
        navy = blank * (1 - ls["ticket"]) + navy * ls["ticket"]
    else:
        navy = blank
    layers = []

    def blurred(name, ang, speed):
        spread = speed / FPS / 2                 # a 180-degree shutter
        if spread < 0.05:
            return placed(logo, name, (H, W), ang, z)
        acc = None
        n = 9
        for f in np.linspace(-0.5, 0.5, n):
            l = placed(logo, name, (H, W), ang + f * spread, z)
            acc = l if acc is None else acc + l
        return acc / n

    def shade(on, occ, k):
        sh = pl.gblur(np.roll(np.roll(occ[..., 3], 3, 0), 7, 1), 6) * k
        on = on.copy(); on[..., :3] *= (1 - sh)[..., None]; return on

    drawn = navy[..., 3].copy()
    if ls["started_p"]:
        purple = blurred("purple", (1 - ls["pp"]) * bs.PASS_ANGLE["purple"], ls["vp"])
        purple = shade(purple, navy, 0.45 * (1 - ls["pp"]))
        if ls["started_t"]:
            teal = blurred("teal", (1 - ls["pt"]) * bs.PASS_ANGLE["teal"], ls["vt"])
            teal = shade(teal, purple, 0.45 * (1 - ls["pt"]))
            img = bs.comp_premul(img, teal); drawn = np.maximum(drawn, teal[..., 3])
        img = bs.comp_premul(img, purple); drawn = np.maximum(drawn, purple[..., 3])
    img = bs.comp_premul(img, navy)
    if ls["full"] > 0:
        # the hold is the supplied file itself
        full = placed(logo, "full", (H, W), zoom=z)
        alt = bs.comp_premul(scene.C.copy(), full)
        img = img * (1 - ls["full"]) + alt * ls["full"]
        drawn = drawn * (1 - ls["full"]) + full[..., 3] * ls["full"]
    return img, drawn


def finish(scene, img, wide, drawn, t, rng):
    """The garden in front (matte blended from the palms' to the W's), grain, contact shading, sharpening."""
    g = pl.gblur(rng.normal(0, scene.sky_sd * 0.8, img.shape).astype(np.float32), 0.6)
    img = img + g * drawn[..., None]
    F = scene.Fm * (1 - wide) + scene.Fm_w * wide
    front = np.where(scene.trunk_px[..., None], scene.C, scene.P)
    H = scene.H
    ao = pl.gblur(np.roll(drawn, 8, 0), 9) * F
    yy = np.mgrid[0:H, 0:scene.W][0]
    ao *= np.clip(1 - (yy - scene.hedge) / 40, 0, 1)
    front = front * (1 - 0.22 * ao[..., None])
    out = bs.over(img, front, F)
    blur = pl.gblur(out, 1.2)
    return np.clip(out + (out - blur) * 0.35, 0, 1)


def dist_to_line(p0, p1, H, W):
    """Distance from every pixel to the segment p0-p1 (plus its 24 px tail below the root)."""
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    d = (p0 - p1) / np.linalg.norm(p0 - p1)
    a, b = p1, p0 + d * 24
    ab = b - a; L2 = (ab ** 2).sum()
    u = np.clip(((xx - a[0]) * ab[0] + (yy - a[1]) * ab[1]) / L2, 0, 1)
    return np.sqrt((xx - (a[0] + u * ab[0])) ** 2 + (yy - (a[1] + u * ab[1])) ** 2)


class Growth:
    """The W filling out from the four trunks: per trunk a distance field to its final line, and the radius at which
    every pixel of the W that is nearest to it is covered."""
    def __init__(self, scene, logo):
        H, W = scene.H, scene.W
        self.D = {k: dist_to_line(bs.to_scene(FINAL[k][0]), bs.to_scene(FINAL[k][1]), H, W) for k in FINAL}
        wa = bs.affine_layer(bs.premul(logo.layers["navy_blank"]), np.array([[bs.LOGO_S, 0, bs.LOGO_X0], [0, bs.LOGO_S, bs.LOGO_Y0]]), (H, W))[..., 3]
        keys = list(FINAL)
        stack = np.stack([self.D[k] for k in keys])
        near = np.argmin(stack, 0)
        inside = (wa > 0.5) & (np.mgrid[0:H, 0:W][0] < scene.hedge)
        self.R = {k: float(np.percentile(self.D[k][inside & (near == i)], 99.5)) + 3 for i, k in enumerate(keys)}
        self.r0 = {k: logo.stroke_hw * 0.8 for k in keys}; self.r0["T4"] = card_hw(logo) * 0.8

    def mask(self, g):
        m = None
        for k, D in self.D.items():
            r = self.r0[k] + (self.R[k] - self.r0[k]) * g
            mk = np.clip(r - D + 0.75, 0, 1)
            m = mk if m is None else np.maximum(m, mk)
        return m


# ------------------------------------------------------------------------------------------------ life in the still
class Life:
    """Water and air: the fountains' spray and the sea shimmer, film grain over everything, the slow push-in."""
    def __init__(self, scene):
        H, W = scene.H, scene.W
        P = scene.P
        rng = np.random.default_rng(5)
        self.n = [pl.gblur(rng.normal(0, 1, (H, W)).astype(np.float32), s) for s in (2.0, 2.0, 3.0)]
        for i in range(3):
            self.n[i] /= self.n[i].std()
        yy, xx = np.mgrid[0:H, 0:W]
        whiteish = (P.min(-1) > 0.55) & ((P.max(-1) - P.min(-1)) < 0.22)
        boxes = np.zeros((H, W), bool)
        for x0, y0, x1, y1 in ((430, 770, 615, 935), (880, 640, 945, 825)):
            boxes[y0:y1, x0:x1] = True
        water = pl.gblur((whiteish & boxes).astype(np.float32), 2.0)
        self.water = np.clip(water * 2.0, 0, 1)
        r, g, b = P[..., 0], P[..., 1], P[..., 2]
        sea = (b > r + 0.08) & (b >= g - 0.03) & (yy > scene.hz + 1) & (yy < scene.hedge)
        self.sea = pl.gblur(sea.astype(np.float32), 1.0) * (1 - scene.Fm)
        self.H, self.W = H, W
        self.yy, self.xx = yy.astype(np.float32), xx.astype(np.float32)

    def apply(self, img, t, rng):
        H, W = self.H, self.W
        n0, n1, n2 = self.n
        # spray rising and falling: a displacement field scrolling upward, plus a little sparkle
        off = (self.yy + 70 * t) % H
        dx = bs.bilinear(n0[..., None], self.xx, off)[..., 0] * 1.3
        dy = bs.bilinear(n1[..., None], self.xx, off)[..., 0] * 1.8
        warped = bs.bilinear(img, self.xx + dx * self.water, self.yy + dy * self.water)
        spark = bs.bilinear(n2[..., None], self.xx, (self.yy + 110 * t) % H)[..., 0]
        warped = warped * (1 + 0.05 * spark[..., None] * self.water[..., None])
        img = img * (1 - self.water[..., None]) + warped * self.water[..., None]
        # the sea: a slow sideways shimmer
        offx = (self.xx + 18 * t) % W
        sdx = bs.bilinear(n2[..., None], offx, self.yy * 0.5)[..., 0] * 0.6
        sh = bs.bilinear(img, self.xx + sdx * self.sea, self.yy)
        glint = np.clip(bs.bilinear(n0[..., None], offx, self.yy * 0.5)[..., 0] - 1.6, 0, None) * 0.05
        sh = sh + glint[..., None] * self.sea[..., None]
        img = img * (1 - self.sea[..., None]) + sh * self.sea[..., None]
        # live film grain over the whole picture
        img = img + pl.gblur(rng.normal(0, 0.008, img.shape).astype(np.float32), 0.5)
        return np.clip(img, 0, 1)


def push_in(img, t):
    """A slow 3% push-in over the whole shot, resampled straight to the delivery size."""
    z = 1.014 + 0.03 * inout(clamp(t / DUR))       # starts just inside the plate (its outer pixels are soft)
    H, W = img.shape[:2]
    cx, cy = 510.0, 505.0
    im = Image.fromarray((np.clip(img, 0, 1) * 255 + 0.5).astype(np.uint8))
    w = W / z; h = H / z
    cx = min(max(cx, w / 2), W - w / 2); cy = min(max(cy, h / 2), H - h / 2)
    box = (cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2)
    return im.resize((OUT_SIZE, OUT_SIZE), Image.LANCZOS, box=box)


# ------------------------------------------------------------------------------------------------ workers
_S = {}


def init():
    sc = bs.Scene(None)
    lg = bs.Logo()
    _S["scene"], _S["logo"], _S["life"], _S["growth"] = sc, lg, Life(sc), Growth(sc, lg)


def render(i):
    t = i / FPS
    sc, logo, life = _S["scene"], _S["logo"], _S["life"]
    rng = np.random.default_rng(1000 + i)
    ls = logo_state(t)
    st = tree_state(t)
    if ls["w_on"] < 1:
        img, drawn = draw_trees(sc, logo, st)
        if ls["grow"] > 0:
            # the W fills out around the trunks, never past its own outline
            wl = placed(logo, "navy_blank", (sc.H, sc.W)) * _S["growth"].mask(ls["grow"])[..., None]
            img = bs.comp_premul(img, wl)
            drawn = np.maximum(drawn, wl[..., 3])
    else:
        img, drawn = draw_logo(sc, logo, ls)
    wide = clamp(max(st["widen"] / 0.3, ls["w_on"]))
    out = finish(sc, img, wide, drawn, t, rng)
    out = life.apply(out, t, rng)
    push_in(out, t).save(FRAMES_DIR / f"f_{i:04d}.png")
    return i


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--only", default=None, help="comma-separated times in seconds")
    a = ap.parse_args()
    FRAMES_DIR.mkdir(parents=True, exist_ok=True)
    idx = [int(round(float(x) * FPS)) for x in a.only.split(",")] if a.only else list(range(int(DUR * FPS)))
    with Pool(a.workers, initializer=init) as pool:
        for n, i in enumerate(pool.imap_unordered(render, idx)):
            if n % 20 == 0:
                print(f"{n}/{len(idx)}", flush=True)
    print("done", len(idx))
