"""Extend the landscape pair photo (Unsplash d7jgsEdPcpw) to a full 9:16 still.
The pair is cropped at full width; the tiled wall is rebuilt above it from the photo's
own wall colour (painting columns filled from their neighbours, faint grout added back),
and the table edge is stretched below into a soft out-of-focus foreground."""
import sys
import numpy as np
from PIL import Image, ImageFilter

src, out = sys.argv[1], sys.argv[2]
W, H = 1215, 2160
X0, X1, TOP = 0.24, 0.83, 230              # crop (fraction of width), rows of wall added on top
im = Image.open(src).convert("RGB")
sw, sh = im.size
x0, x1 = round(X0 * sw), round(X1 * sw)
crop = im.crop((x0, 0, x1, sh))
ch = round(crop.height * W / crop.width)
crop = crop.resize((W, ch), Image.LANCZOS)
a = np.asarray(crop).astype(np.float32)
BOT = H - TOP - ch

# wall colour per column from the top rows, skipping the paintings (colourful or dark pixels)
band = a[:40]
sat = band.max(2) - band.min(2)
lum = band.mean(2)
plain = (sat < 22) & (lum > 150)
# one smooth light falloff across the wall: a quadratic fitted to the plain-wall columns only
xs = np.arange(W)
ok = plain.sum(0) > 20
cols = np.zeros((W, 3), np.float32)
for c in range(3):
    v = np.where(plain, band[..., c], 0).sum(0) / np.maximum(plain.sum(0), 1)
    cols[:, c] = np.polyval(np.polyfit(xs[ok], v[ok], 2), xs)
top = np.repeat(cols[None], TOP, 0)
# faint tile grout continuing the wall's grid, light falling off towards the ceiling
yy = np.arange(TOP)[:, None]
# vertical grout carried up from the visible tiles (lines at x 760 and 892, a 132 px grid)
gx = np.zeros(W, np.float32)
for x in range(760 % 132, W, 132):
    gx[max(0, x - 1):x + 2] = 6
top = top - gx[None, :, None]
fall = (0.93 + 0.07 * (yy / TOP) ** 0.7)[..., None]
top = top * fall
noise = np.random.default_rng(3).normal(0, 2.2, top.shape).astype(np.float32)
top = top + noise
# blend the seam over 24 rows into the photo's top
canvas = np.zeros((H, W, 3), np.float32)
canvas[:TOP] = top
canvas[TOP:TOP + ch] = a
# in plain-wall columns, fade the rebuilt wall into the photo's first rows so no seam shows
blend = 36
wallmask = np.asarray(Image.fromarray((plain.mean(0) > 0.6).astype(np.uint8) * 255).resize((W, 1)).filter(ImageFilter.GaussianBlur(0)))[0] / 255.0
wallmask = np.convolve(np.pad(wallmask, 15, mode="edge"), np.ones(31) / 31, "valid")
for i in range(blend):
    t = (i + 1) / (blend + 1)
    m = (wallmask * (1 - t))[:, None]
    canvas[TOP + i] = canvas[TOP + i] * (1 - m) + top[-1] * m

# foreground: stretch the bottom 170 rows of the photo down to fill, blurring and darkening as it goes
SRC_ROWS = 170
strip = crop.crop((0, ch - SRC_ROWS, W, ch))
fg = strip.resize((W, SRC_ROWS + BOT), Image.BICUBIC)
fga = np.asarray(fg).astype(np.float32)
levels = [np.asarray(fg.filter(ImageFilter.GaussianBlur(r))).astype(np.float32) for r in (0, 6, 14, 26, 40)]
n = fga.shape[0]
outfg = np.zeros_like(fga)
for y in range(n):
    t = min(1.0, max(0.0, (y - SRC_ROWS * 0.3) / (n - SRC_ROWS * 0.3))) * (len(levels) - 1)
    i = int(t); f = t - i
    row = levels[i][y] * (1 - f) + levels[min(i + 1, len(levels) - 1)][y] * f
    outfg[y] = row * (1 - 0.35 * (y / n) ** 1.3)
canvas[H - n:] = outfg
Image.fromarray(canvas.clip(0, 255).astype(np.uint8)).save(out, quality=92)
print("crop rows", ch, "top", TOP, "bottom ext", BOT)
