"""WYSTAK pre-launch billboard poster, v2: "Something new is stacking up..." (1080x2100, the billboard's 1:1.94 screen).

Upper rectangle: the headline and the card-holder image from the user's reference (inbox/2026-10-10-billboard-v2/16.webp),
with its stand-in W painted out of the holder and the supplied logo (assets/logo-mark.png) set in its place.
Lower rectangle: an embossed plate, COMING SOON on the left and www.wystak.com on the right.
Then the poster is laid into the billboard photo (17.png) on the screen's exact quad: python3 build.py
"""
import sys, pathlib, subprocess
import numpy as np
from PIL import Image, ImageFilter
HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[3]
sys.path.insert(0, str(HERE.parent.parent / "carousels" / "_common"))
sys.path.insert(0, str(ROOT / "videos" / "wystak-palm-reveal" / "storyboard"))
from common import find_chrome
import plate as pl

INBOX = ROOT / "inbox" / "2026-10-10-billboard-v2"
W, H = 1080, 2100
UPPER = 1560                       # the image rectangle; the embossed plate fills the rest

# the screen inside the billboard's bezel, in the photo's pixels (360x640): TL, TR, BR, BL
QUAD = [(100.6, 160.5), (283.2, 198.4), (285.6, 547.0), (100.6, 533.7)]
SCALE = 3                          # the delivered billboard image is the photo at 3x (1080x1920)


def holder_image():
    """The reference's card holder with the supplied logo on it."""
    im = Image.open(INBOX / "16.webp").convert("RGB")
    a = np.asarray(im).astype(np.float32) / 255
    yy, xx = np.mgrid[0:a.shape[0], 0:a.shape[1]]
    box = (xx > 480) & (xx < 675) & (yy > 900) & (yy < 1034)
    mx, mn = a.max(-1), a.min(-1)
    mark = box & (((mx - mn) > 0.08) | (mx < 0.8))
    mark = np.asarray(Image.fromarray((mark * 255).astype(np.uint8)).filter(ImageFilter.MaxFilter(9))) > 0
    filled = pl.fill_from(a, ~mark & box | ~box, sigmas=(3, 8, 20, 50))
    a = np.where(mark[..., None], filled, a)
    out = Image.fromarray((np.clip(a, 0, 1) * 255).astype(np.uint8))
    logo = Image.open(HERE / "assets" / "logo-mark.png").convert("RGBA")
    lw = 222; logo = logo.resize((lw, round(logo.height * lw / logo.width)), Image.LANCZOS)
    out.paste(logo, (577 - lw // 2, 968 - logo.height // 2), logo)
    # only the holder and cards (the reference's headline and foot are set again in the poster)
    out = out.crop((110, 330, 1144, 1044))
    out.save(HERE / "assets" / "holder.png")
    return out.size


def poster_html(hsize):
    hw = 1160
    hh = round(hsize[1] * hw / hsize[0])
    return f'''<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{{font-family:P;src:url(assets/poppins-latin-500-normal.woff2);font-weight:500}}
@font-face{{font-family:P;src:url(assets/poppins-latin-700-normal.woff2);font-weight:700}}
@font-face{{font-family:P;src:url(assets/poppins-latin-800-normal.woff2);font-weight:800}}
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:{W}px;height:{H}px;overflow:hidden;background:#fff}}
body{{font-family:P,sans-serif}}
.up{{position:absolute;left:0;top:0;width:{W}px;height:{UPPER}px;background:#fff}}
.h{{position:absolute;left:0;right:0;top:110px;text-align:center;font-weight:800;font-size:142px;line-height:1.04;letter-spacing:-.045em;color:#0b1238;white-space:nowrap}}
.g{{background:linear-gradient(90deg,#7b2ff7 0%,#5b3df5 35%,#2f86ee 70%,#1fc4d8 100%);-webkit-background-clip:text;background-clip:text;color:transparent}}
.img{{position:absolute;left:-40px;-webkit-mask-image:radial-gradient(75% 80% at 50% 55%,#000 70%,transparent 100%);top:{UPPER - hh}px;width:{hw}px;height:{hh}px}}
.line{{position:absolute;left:0;right:0;top:{UPPER}px;height:3px;background:#dcdde5}}
.low{{position:absolute;left:0;right:0;top:{UPPER + 3}px;bottom:0;background:linear-gradient(180deg,#f1f2f6,#e7e8ee)}}
.plate{{position:absolute;left:48px;right:48px;top:44px;bottom:44px;border-radius:34px;background:linear-gradient(160deg,#f4f5f8,#e9eaf0);
  box-shadow:inset 6px 6px 14px rgba(150,152,175,.35),inset -6px -6px 14px rgba(255,255,255,.95)}}
.cs{{position:absolute;left:64px;top:50%;transform:translateY(-50%);font-weight:800;font-size:84px;line-height:.98;letter-spacing:-.01em;color:#7a2fe6;
  text-shadow:-2px -2px 1px rgba(255,255,255,.95),3px 3px 2px rgba(70,20,130,.55),6px 7px 12px rgba(60,30,110,.28)}}
.url{{position:absolute;right:64px;top:50%;transform:translateY(-50%);font-weight:700;font-size:45px;letter-spacing:.005em;color:#0b1238;
  text-shadow:-2px -2px 1px rgba(255,255,255,.95),2px 3px 2px rgba(10,18,56,.45),5px 6px 10px rgba(10,18,56,.22)}}
</style></head><body>
<div class="up"><div class="h">Something<br>new is<br><span class="g">stacking up…</span></div>
<img class="img" src="assets/holder.png"></div>
<div class="line"></div>
<div class="low"><div class="plate"><div class="cs">COMING<br>SOON</div><div class="url">www.wystak.com</div></div></div>
</body></html>'''


def render(html, out):
    chrome, is_shell = find_chrome()
    f = HERE / "_poster.html"; f.write_text(html)
    args = [chrome, f"--window-size={W},{H}"] if is_shell else [chrome, "--headless=new", f"--window-size={W},{H + 400}"]
    subprocess.run(args + ["--no-sandbox", "--disable-gpu", "--hide-scrollbars", "--force-device-scale-factor=1", "--allow-file-access-from-files",
                           "--virtual-time-budget=5000", f"--screenshot={out}", f.as_uri()], check=True, capture_output=True, timeout=240)
    Image.open(out).convert("RGB").crop((0, 0, W, H)).save(out); f.unlink()


def coeffs(dst, src):
    A, b = [], []
    for (x, y), (u, v) in zip(dst, src):
        A.append([x, y, 1, 0, 0, 0, -u * x, -u * y]); b.append(u)
        A.append([0, 0, 0, x, y, 1, -v * x, -v * y]); b.append(v)
    return np.linalg.solve(np.array(A, float), np.array(b, float)).tolist()


def on_billboard(poster_path, out):
    """The poster on the billboard's screen, same angle: warped at 2x, matched to the photo's softness and light."""
    photo = Image.open(INBOX / "17.png").convert("RGB")
    big = photo.resize((photo.width * SCALE, photo.height * SCALE), Image.LANCZOS)
    BW, BH = big.size
    ss = 2
    q = [(x * SCALE * ss, y * SCALE * ss) for x, y in QUAD]
    poster = Image.open(poster_path).convert("RGB")
    co = coeffs(q, [(0, 0), (W, 0), (W, H), (0, H)])
    warped = poster.transform((BW * ss, BH * ss), Image.PERSPECTIVE, co, Image.BICUBIC).resize((BW, BH), Image.LANCZOS)
    mask = Image.new("L", poster.size, 255).transform((BW * ss, BH * ss), Image.PERSPECTIVE, co, Image.BILINEAR).resize((BW, BH), Image.LANCZOS)
    p = np.asarray(warped.filter(ImageFilter.GaussianBlur(0.9)), np.float32) / 255
    m = np.asarray(mask, np.float32)[..., None] / 255
    b = np.asarray(big, np.float32) / 255
    # a lit screen in daylight: a touch less contrast, a slight warm cast from the sky, a faint sheen from top left
    p = 0.035 + p * 0.94
    yy, xx = np.mgrid[0:BH, 0:BW].astype(np.float32)
    x0, y0 = QUAD[0][0] * SCALE, QUAD[0][1] * SCALE
    sheen = np.clip(1 - ((xx - x0) * 0.6 + (yy - y0) * 0.8) / 900, 0, 1) ** 2 * 0.05
    p = p + sheen[..., None]
    p = p + np.random.default_rng(3).normal(0, 0.012, p.shape).astype(np.float32)
    # leaves or lamps in front of the screen stay in front (green, or the lamp globes outside the original white plate)
    orig = b
    g = orig[..., 1] - np.maximum(orig[..., 0], orig[..., 2])
    front = ((g > 0.06) & (orig.max(-1) > 0.2)).astype(np.float32)
    front = np.asarray(Image.fromarray((front * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(1.0)), np.float32)[..., None] / 255
    a = m * (1 - front)
    outimg = b * (1 - a) + np.clip(p, 0, 1) * a
    Image.fromarray((np.clip(outimg, 0, 1) * 255 + 0.5).astype(np.uint8)).save(out)


if __name__ == "__main__":
    out = HERE / "slides"; out.mkdir(exist_ok=True)
    size = holder_image()
    render(poster_html(size), out / "wystak-billboard-poster.png")
    on_billboard(out / "wystak-billboard-poster.png", out / "wystak-billboard-mockup.png")
    print("ok")
