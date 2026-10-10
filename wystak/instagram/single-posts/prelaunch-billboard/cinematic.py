"""WYSTAK pre-launch poster, cinematic option: the supplied logo standing on a dark stone table in window light.

The scene is built in code with numpy and PIL (no stock photo): a dark stone table, a warm window-light pool with the
shadow of a window frame and of leaves, an out-of-focus plant, mug and phone in the corners, and the supplied logo
(assets/logo-mark.png, never redrawn) with a contact shadow, a cast shadow, a faint reflection and a rim light.
Text is laid over it in HTML. Output 1080x1900. Run: python3 cinematic.py
"""
import math, pathlib, random
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageChops
import build  # render_html, W, H

HERE = pathlib.Path(__file__).resolve().parent
W, H = build.W, build.H
rng = np.random.default_rng(7)
random.seed(7)


def blur(img, r):
    return img.filter(ImageFilter.GaussianBlur(r))


def fnoise(w, h, scales, weights=None, seed=0):
    r = np.random.default_rng(seed)
    out = np.zeros((h, w), np.float32)
    weights = weights or [1.0] * len(scales)
    for s, wt in zip(scales, weights):
        a = r.random((h // s + 3, w // s + 3)).astype(np.float32)
        out += wt * np.asarray(Image.fromarray((a * 255).astype(np.uint8)).resize((w + 2 * s, h + 2 * s), Image.BICUBIC), np.float32)[:h, :w] / 255
    return out / sum(weights)


def arr(img):
    return np.asarray(img, np.float32) / 255


# ---------------------------------------------------------------- light: window frame + leaf shadows
def window_mask():
    m = Image.new("L", (W, H), 0)
    d = ImageDraw.Draw(m)
    ox, oy = 40, 120
    ux, uy = 1.0, 0.13            # window "right" direction
    vx, vy = 0.42, 1.0            # window "down" direction
    pw, ph, gap = 250, 330, 38
    for r in range(3):
        for c in range(3):
            u0, v0 = c * (pw + gap), r * (ph + gap)
            pts = [(u0, v0), (u0 + pw, v0), (u0 + pw, v0 + ph), (u0, v0 + ph)]
            d.polygon([(ox + u * ux + v * vx, oy + u * uy + v * vy) for u, v in pts], fill=255)
    return blur(m, 8)


def leaf_shadow_mask():
    m = Image.new("L", (W, H), 0)
    d = ImageDraw.Draw(m)
    def leaf(cx, cy, length, width, ang):
        pts = []
        for t in np.linspace(0, math.pi, 24):
            pts.append((t / math.pi * length, math.sin(t) * width))
        for t in np.linspace(math.pi, 0, 24):
            pts.append((t / math.pi * length, -math.sin(t) * width * 0.9))
        ca, sa = math.cos(ang), math.sin(ang)
        d.polygon([(cx + x * ca - y * sa, cy + x * sa + y * ca) for x, y in pts], fill=255)
    for i in range(9):
        a = math.radians(150 + i * 9 + random.uniform(-6, 6))
        leaf(1040 - i * 38, 80 + i * 42, random.uniform(260, 360), random.uniform(46, 64), a)
    for i in range(6):
        a = math.radians(130 + i * 14)
        leaf(1100, 520 + i * 70, random.uniform(220, 300), random.uniform(34, 46), a)
    return blur(m, 9)


def build_light():
    win = arr(window_mask())
    leaf = arr(leaf_shadow_mask())
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    pool = np.exp(-(((xx - 330) / 780) ** 2 + ((yy - 780) / 980) ** 2))
    gobo = (0.16 + 0.84 * win) * (1 - 0.72 * leaf)
    return pool, gobo


# ---------------------------------------------------------------- the stone table and the wall
def build_base(pool, gobo):
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    horizon = 330
    # stone albedo: broad mottling, fine speckle and a few veins
    mott = fnoise(W, H, [220, 90, 38, 14], [1, .8, .6, .4], seed=1)
    speck = fnoise(W, H, [3, 2], [1, 1], seed=2)
    vein = np.abs(fnoise(W, H, [160, 70], [1, .6], seed=3) - 0.5) * 2
    vein = np.clip(1 - vein * 14, 0, 1) ** 3
    alb = 0.075 + 0.07 * mott + 0.03 * (speck - 0.5) + 0.012 * vein
    alb = alb[..., None] * np.array([1.0, 1.0, 1.04], np.float32)

    # polished sheen: a broad highlight band that follows the light
    sheen = np.exp(-(((xx - 420) / 620) ** 2 + ((yy - 820) / 520) ** 2)) * (0.5 + 0.5 * fnoise(W, H, [260, 90], [1, .7], seed=4))

    warm = np.array([1.0, 0.80, 0.58], np.float32)
    cool = np.array([0.42, 0.50, 0.62], np.float32)
    lit = (pool * gobo)[..., None]
    table = alb * (cool * 0.55 + warm * 3.4 * lit) + (sheen * lit[..., 0] * 0.16)[..., None] * warm
    table = table + (sheen * 0.05)[..., None] * cool

    # wall: darker, more matte, the window light climbs it in the upper left
    wallv = 0.045 + 0.04 * fnoise(W, H, [300, 100], [1, .6], seed=5)
    wall_lit = np.exp(-(((xx - 160) / 520) ** 2 + ((yy - 140) / 280) ** 2)) * gobo
    wall = wallv[..., None] * (cool * 0.9 + warm * 4.2 * wall_lit[..., None])
    t = np.clip((yy - horizon) / 26, 0, 1)[..., None]
    t = t * t * (3 - 2 * t)
    img = wall * (1 - t) + table * t
    # a thin catch-light on the table's back edge
    edge = np.exp(-((yy - horizon - 2) / 3.2) ** 2)[..., None] * (0.05 + 0.2 * (pool * gobo)[..., None]) * warm
    img = img + edge
    # depth: the table falls into darkness towards the viewer
    img = img * (1 - 0.30 * np.clip((yy - 1100) / 800, 0, 1))[..., None]
    return img


# ---------------------------------------------------------------- foreground, out of focus
def leaf_poly(d, cx, cy, length, width, ang, fill):
    pts = []
    for t in np.linspace(0, math.pi, 28):
        pts.append((t / math.pi * length, math.sin(t) * width))
    for t in np.linspace(math.pi, 0, 28):
        pts.append((t / math.pi * length, -math.sin(t) * width * 0.92))
    ca, sa = math.cos(ang), math.sin(ang)
    d.polygon([(cx + x * ca - y * sa, cy + x * sa + y * ca) for x, y in pts], fill=fill)


def plant_layer():
    L = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(L)
    greens = [(26, 52, 30, 255), (34, 70, 38, 255), (20, 40, 26, 255), (46, 88, 44, 255)]
    spec = [(520, -40, 330, 74, 80), (640, 10, 360, 80, 105), (760, -30, 320, 70, 125), (860, 40, 300, 72, 150),
            (980, 90, 280, 66, 165), (1060, 190, 240, 60, 178), (900, 260, 220, 52, 110), (1040, 330, 190, 46, 140),
            (700, 190, 200, 54, 60)]
    for i, (cx, cy, ln, wd, deg) in enumerate(spec):
        leaf_poly(d, cx, cy, ln, wd, math.radians(deg), greens[i % 4])
    L = blur(L, 20)
    # warm light catching the leaf tops
    glow = blur(ImageChops.offset(L.split()[3], -10, -12), 14)
    rim = ImageChops.subtract(L.split()[3], ImageChops.offset(L.split()[3], 22, 26))
    rim = blur(rim, 10).point(lambda v: min(255, v * 1))
    return L, rim


def mug_layer():
    L = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(L)
    cx, cy, rx, ry = 70, 1740, 270, 165
    d.ellipse((cx - rx, cy - ry, cx + rx, cy + ry), fill=(44, 40, 42, 255))
    d.ellipse((cx - rx + 18, cy - ry + 12, cx + rx - 18, cy + ry - 12), fill=(20, 18, 19, 255))
    d.ellipse((cx - rx + 54, cy - ry + 40, cx + rx - 54, cy + ry - 40), fill=(70, 44, 26, 255))
    rim = Image.new("L", (W, H), 0)
    rd = ImageDraw.Draw(rim)
    rd.arc((cx - rx, cy - ry, cx + rx, cy + ry), 200, 310, fill=255, width=9)
    return blur(L, 16), blur(rim, 8)


def phone_layer():
    L = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(L)
    body = Image.new("RGBA", (460, 960), (0, 0, 0, 0))
    bd = ImageDraw.Draw(body)
    bd.rounded_rectangle((0, 0, 459, 959), 70, fill=(70, 72, 78, 255))
    bd.rounded_rectangle((12, 12, 447, 947), 60, fill=(14, 15, 19, 255))
    body = body.rotate(8, expand=True, resample=Image.BICUBIC)
    L.alpha_composite(body, (730, 1470))
    rim = Image.new("L", (W, H), 0)
    rd = ImageDraw.Draw(rim)
    rd.line([(742, 1560), (790, 1478), (930, 1456)], fill=255, width=8)
    return blur(L, 13), blur(rim, 7)


def layer_over(img, L, rim=None, rim_col=(1.0, 0.8, 0.55), rim_gain=0.9):
    a = arr(L.split()[3])[..., None]
    rgb = arr(L.convert("RGB"))
    out = img * (1 - a) + rgb * a
    if rim is not None:
        out = out + arr(rim)[..., None] * np.array(rim_col, np.float32) * rim_gain * a
    return out


# ---------------------------------------------------------------- the logo
def place_logo(img, pool, gobo):
    logo = Image.open(HERE / "assets" / "logo-mark.png").convert("RGBA")
    lw = 640
    lh = round(logo.height * lw / logo.width)
    logo = logo.resize((lw, lh), Image.LANCZOS)
    x0, base = (W - lw) // 2 - 6, 1130
    y0 = base - lh
    alpha = logo.split()[3]

    # full-canvas alpha for the shadow work
    A = Image.new("L", (W, H), 0)
    A.paste(alpha, (x0, y0))

    # contact shadow: tight and dark right under the base
    cs = Image.new("L", (W, H), 0)
    ImageDraw.Draw(cs).ellipse((x0 + 20, base - 22, x0 + lw - 70, base + 30), fill=255)
    cs = arr(blur(cs, 15))[..., None]
    img = img * (1 - 0.8 * cs)

    # cast shadow: the logo flattened onto the table, sheared away from the window (light from the upper left)
    k, sy = 0.62, 0.42
    # output y = base + (base - y_in) * sy, so y_in = base - (y_out - base) / sy
    ay = -1 / sy
    sh = A.transform((W, H), Image.AFFINE, (1, 0, 0, 0, ay, base - ay * base), resample=Image.BICUBIC)
    # shear by shifting rows proportional to distance below the base
    sh_a = np.asarray(sh, np.float32) / 255
    shifted = np.zeros_like(sh_a)
    for yrow in range(base, min(H, base + int(lh * sy) + 4)):
        s = int((yrow - base) / sy * k * 0.55)
        shifted[yrow, s:] = sh_a[yrow, : W - s] if s > 0 else sh_a[yrow]
    shadow = Image.fromarray((shifted * 255).astype(np.uint8))
    near = arr(blur(shadow, 7))
    far = arr(blur(shadow, 26))
    yy = np.arange(H, dtype=np.float32)[:, None]
    mix = np.clip((yy - base) / (lh * sy), 0, 1)
    sh_final = (near * (1 - mix) + far * mix) * (0.62 - 0.30 * mix)
    img = img * (1 - sh_final[..., None] * 0.95)

    # reflection on the polished stone: faint, fading, a little blurred
    rl = logo.transpose(Image.FLIP_TOP_BOTTOM)
    R = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    R.paste(rl, (x0, base + 3))
    Ra = arr(R.split()[3]) * np.clip(1 - (np.arange(H, dtype=np.float32)[:, None] - base) / (lh * 0.55), 0, 1) ** 1.6 * 0.22
    Ra = arr(blur(Image.fromarray((Ra * 255).astype(np.uint8)), 4))
    img = img * (1 - Ra[..., None]) + arr(R.convert("RGB")) * Ra[..., None]

    # the logo itself, lit by the window: a gentle gradient, the local light pattern, a warm rim on the lit edges
    lg = arr(logo.convert("RGB"))
    yy2, xx2 = np.mgrid[0:lh, 0:lw].astype(np.float32)
    grad = 1.12 - 0.34 * (xx2 / lw) * 0.8 - 0.30 * (yy2 / lh) * 0.9
    local = (pool * gobo)[y0:y0 + lh, x0:x0 + lw]
    local = np.asarray(blur(Image.fromarray((np.clip(local, 0, 1) * 255).astype(np.uint8)), 30), np.float32) / 255
    shade = grad * (0.62 + 0.55 * local)
    lg = lg * shade[..., None]
    lg = lg + (local[..., None] * np.array([0.05, 0.03, 0.0], np.float32)) * (lg.mean(axis=2, keepdims=True) > 0.2)
    a = arr(alpha)
    rim = np.clip(a - np.asarray(ImageChops.offset(alpha, 5, 6), np.float32) / 255, 0, 1)
    rim = np.asarray(blur(Image.fromarray((rim * 255).astype(np.uint8)), 2.2), np.float32) / 255
    lg = lg + rim[..., None] * np.array([1.0, 0.82, 0.6], np.float32) * (0.45 + 0.6 * local[..., None])
    # darken the foot where it meets the stone (ambient occlusion)
    ao = np.clip((yy2 - lh * 0.88) / (lh * 0.12), 0, 1) ** 1.5
    lg = lg * (1 - 0.35 * ao)[..., None]
    sub = img[y0:y0 + lh, x0:x0 + lw]
    img[y0:y0 + lh, x0:x0 + lw] = sub * (1 - a[..., None]) + np.clip(lg, 0, 1.2) * a[..., None]
    return img


# ---------------------------------------------------------------- grade
def grade(img):
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    # bloom
    hi = np.clip(img - 0.55, 0, None)
    bl = np.asarray(blur(Image.fromarray((np.clip(hi, 0, 1) * 255).astype(np.uint8)), 40), np.float32) / 255
    img = img + bl * 0.55
    # vignette
    v = ((xx - W / 2) / (W * 0.78)) ** 2 + ((yy - H * 0.5) / (H * 0.7)) ** 2
    img = img * np.clip(1 - 0.55 * v, 0, 1)[..., None]
    # tone: soft shoulder and a touch of teal in the shadows
    img = img / (1 + 0.55 * img)
    img = img ** 0.86
    img = img + np.array([-0.004, 0.003, 0.012], np.float32) * (1 - img)
    # film grain
    g = rng.normal(0, 0.017, (H, W, 1)).astype(np.float32)
    img = img + g * (0.6 + 0.8 * (1 - img.mean(axis=2, keepdims=True)))
    return np.clip(img, 0, 1)


def make_scene(out):
    pool, gobo = build_light()
    img = build_base(pool, gobo)
    img = place_logo(img, pool, gobo)
    L, rim = plant_layer()
    img = layer_over(img, L, rim)
    L, rim = mug_layer()
    img = layer_over(img, L, rim, rim_gain=1.4)
    L, rim = phone_layer()
    img = layer_over(img, L, rim, rim_col=(0.9, 0.85, 0.8), rim_gain=1.2)
    img = grade(img)
    Image.fromarray((img * 255).astype(np.uint8)).save(out, quality=95)


# ---------------------------------------------------------------- the poster: scene plus type
def poster_html(scene_name):
    return f'''<!doctype html><html><head><meta charset="utf-8"><style>
{build.FONTS}
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:{W}px;height:{H}px;overflow:hidden;background:#000}}
.p{{position:relative;width:{W}px;height:{H}px;background:url({scene_name}) center/cover;font-family:P,sans-serif;color:#e9e6e0}}
.top{{position:absolute;left:86px;top:112px;font-weight:500;font-size:34px;letter-spacing:.42em;line-height:1.7;text-shadow:0 2px 18px rgba(0,0,0,.5)}}
.top b{{font-weight:600;color:#4f86ff}}
.word{{position:absolute;left:0;right:0;top:1262px;display:flex;justify-content:center}}
.word img{{width:560px;filter:brightness(0) invert(1);opacity:.95;filter:brightness(0) invert(1) drop-shadow(0 6px 22px rgba(0,0,0,.55))}}
.soon{{position:absolute;left:0;right:0;top:1470px;text-align:center;font-weight:500;font-size:26px;letter-spacing:.62em;padding-left:.62em;color:rgba(233,230,224,.78)}}
</style></head><body><div class="p">
<div class="top">LOYALTY,<br>IN YOUR <b>WALLET.</b></div>
<div class="word"><img src="assets/logo-wordmark.png"></div>
<div class="soon">COMING SOON</div>
</div></body></html>'''


if __name__ == "__main__":
    out = HERE / "slides"; out.mkdir(exist_ok=True)
    scene = HERE / "_scene.jpg"
    make_scene(scene)
    build.render_html(poster_html(scene.name), out / "wystak-billboard-cinematic.png")
    print("ok")
