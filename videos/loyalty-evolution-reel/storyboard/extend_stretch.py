"""Extend a landscape photo to a full 9:16 still (1215x2160) by stretching its own top and
bottom edges: the top band is stretched upward (good for windows, walls, vertical frames) and
the bottom band is stretched downward into a soft out-of-focus foreground.
usage: extend_stretch.py SRC OUT X0 X1 TOP [TOP_SRC_ROWS BOT_SRC_ROWS]"""
import sys
import numpy as np
from PIL import Image, ImageFilter

src, out, X0, X1, TOP = sys.argv[1], sys.argv[2], float(sys.argv[3]), float(sys.argv[4]), int(sys.argv[5])
TSRC = int(sys.argv[6]) if len(sys.argv) > 6 else 140
BSRC = int(sys.argv[7]) if len(sys.argv) > 7 else 170
W, H = 1215, 2160
im = Image.open(src).convert("RGB")
crop = im.crop((round(X0 * im.width), 0, round(X1 * im.width), im.height))
ch = round(crop.height * W / crop.width)
crop = crop.resize((W, ch), Image.LANCZOS)
BOT = H - TOP - ch
canvas = np.zeros((H, W, 3), np.float32)


def ramp(strip_img, n_src, n_out, flip):
    """Stretch a strip to n_out rows, blurring more the further it gets from the photo."""
    fg = strip_img.resize((W, n_out), Image.BICUBIC)
    levels = [np.asarray(fg.filter(ImageFilter.GaussianBlur(r))).astype(np.float32) for r in (0, 5, 12, 22, 34)]
    res = np.zeros((n_out, W, 3), np.float32)
    for y in range(n_out):
        d = (n_out - 1 - y) if flip else y           # distance from the photo edge
        t = min(1.0, max(0.0, (d - n_src * 0.3) / (n_out - n_src * 0.3))) * (len(levels) - 1)
        i = int(t); f = t - i
        res[y] = levels[i][y] * (1 - f) + levels[min(i + 1, len(levels) - 1)][y] * f
    return res


if TOP > 0:
    top = ramp(crop.crop((0, 0, W, TSRC)), TSRC, TSRC + TOP, flip=True)
    canvas[:TSRC + TOP] = top
canvas[TOP + TSRC:TOP + ch] = np.asarray(crop).astype(np.float32)[TSRC:]
if BOT > 0:
    bot = ramp(crop.crop((0, ch - BSRC, W, ch)), BSRC, BSRC + BOT, flip=False)
    yy = np.arange(bot.shape[0])[:, None, None] / bot.shape[0]
    canvas[H - bot.shape[0]:] = bot * (1 - 0.3 * yy ** 1.3)
Image.fromarray(canvas.clip(0, 255).astype(np.uint8)).save(out, quality=92)
print("photo rows", ch, "top", TOP, "bottom", BOT)
