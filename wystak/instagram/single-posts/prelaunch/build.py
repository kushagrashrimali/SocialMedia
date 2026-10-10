"""WYSTAK pre-launch teaser: a single image, 1080x1350. A name reveal on a real city billboard.

A real photograph of a blank billboard (Unsplash, Photo by personalgraphic.com) is the base. The Wystak screen design
(black LED screen, "Something new is stacking up...", three lit cards, a white "COMING SOON" band with the supplied
wordmark) is rendered with headless Chromium and placed on the billboard face with perspective, then given the
glow, light spill and reflection a real LED screen has. No product information.

Steps: 1) render screen.png  2) composite on the photo  3) crop to 4:5 and save slides/wystak-prelaunch.png
"""
import sys, pathlib, subprocess
import numpy as np
from PIL import Image, ImageFilter, ImageChops
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent.parent / "carousels" / "_common"))
from common import find_chrome

PHOTO = HERE / "assets" / "billboard-photo-unsplash-t0lLGHhnh8w.jpg"
# corners of the white billboard face in the 2500x2500 photo: TL, TR, BR, BL
QUAD = [(760, 436), (1687, 439), (1693, 1461), (763, 1463)]
FACE_W, FACE_H = 932, 1026
SCREEN_W, SCREEN_H = FACE_W * 2, FACE_H * 2   # render at 2x for crisp text
CROP = (476, 150, 476 + 1500, 150 + 1875)      # 4:5 crop around the billboard
OUT = (1080, 1350)

CARD = lambda bg, glow, rot, x, y: (f'<div style="position:absolute;left:{x}px;top:{y}px;width:360px;height:560px;border-radius:70px;transform:rotate({rot}deg);'
    f'background:{bg};box-shadow:0 0 120px {glow},inset 0 0 0 3px rgba(255,255,255,.28),inset 14px 14px 40px rgba(255,255,255,.22),inset -20px -30px 50px rgba(0,0,0,.35)">'
    f'<div style="position:absolute;left:30px;top:26px;right:30px;height:150px;border-radius:50px;background:linear-gradient(180deg,rgba(255,255,255,.35),rgba(255,255,255,0))"></div></div>')

SCREEN_HTML = f"""<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{{font-family:P;src:url(assets/poppins-latin-500-normal.woff2);font-weight:500}}
@font-face{{font-family:P;src:url(assets/poppins-latin-600-normal.woff2);font-weight:600}}
@font-face{{font-family:P;src:url(assets/poppins-latin-700-normal.woff2);font-weight:700}}
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:{SCREEN_W}px;height:{SCREEN_H}px;overflow:hidden;background:#04040a;font-family:P,sans-serif;color:#fff}}
</style></head><body>
<div style="position:absolute;inset:0;background:radial-gradient(60% 45% at 50% 52%,rgba(120,60,200,.28),transparent 70%)"></div>
<div style="position:absolute;left:60px;right:60px;top:130px;text-align:center;font-weight:600;font-size:132px;line-height:1.16;letter-spacing:-.015em">Something new is<br>stacking up…</div>
<div style="position:absolute;left:0;top:0;width:{SCREEN_W}px;height:{SCREEN_H}px">
  {CARD("linear-gradient(160deg,#3a6ee0,#0a2860)", "rgba(40,90,220,.6)", -14, 470, 800)}
  {CARD("linear-gradient(160deg,#b86af0,#6b2ba6)", "rgba(150,70,220,.65)", 0, 750, 740)}
  {CARD("linear-gradient(160deg,#27d3d1,#06737c)", "rgba(30,200,200,.6)", 14, 1030, 800)}
</div>
<div style="position:absolute;left:0;right:0;bottom:0;height:380px;background:#f6f4ef;display:flex;align-items:center;justify-content:space-between;padding:0 110px 0 120px">
  <div style="font-weight:700;font-size:104px;line-height:1.08;letter-spacing:.02em;color:#6b2ba6">COMING<br>SOON</div>
  <img src="assets/logo-wordmark.png" style="width:640px"></div>
</body></html>"""


def render_screen():
    chrome, is_shell = find_chrome()
    html = HERE / "_screen.html"; html.write_text(SCREEN_HTML)
    png = HERE / "screen.png"
    args = [chrome, f"--window-size={SCREEN_W},{SCREEN_H}"] if is_shell else [chrome, "--headless=new", f"--window-size={SCREEN_W},{SCREEN_H + 400}"]
    subprocess.run(args + ["--no-sandbox", "--disable-gpu", "--hide-scrollbars", "--force-device-scale-factor=1", "--allow-file-access-from-files",
                           "--virtual-time-budget=3000", f"--screenshot={png}", html.as_uri()], check=True, capture_output=True, timeout=120)
    img = Image.open(png).convert("RGB").crop((0, 0, SCREEN_W, SCREEN_H))
    html.unlink()
    return img


def perspective_coeffs(dst, src):
    """Coefficients for PIL's PERSPECTIVE transform mapping output points (dst) to input points (src)."""
    A, b = [], []
    for (x, y), (u, v) in zip(dst, src):
        A.append([x, y, 1, 0, 0, 0, -u * x, -u * y]); b.append(u)
        A.append([0, 0, 0, x, y, 1, -v * x, -v * y]); b.append(v)
    return np.linalg.solve(np.array(A, float), np.array(b, float))


def composite():
    photo = Image.open(PHOTO).convert("RGB")
    W, H = photo.size
    screen = render_screen().resize((FACE_W, FACE_H), Image.LANCZOS)

    # 1) warp the screen onto the billboard face
    coeffs = perspective_coeffs(QUAD, [(0, 0), (FACE_W, 0), (FACE_W, FACE_H), (0, FACE_H)])
    warped = screen.transform((W, H), Image.PERSPECTIVE, coeffs, Image.BICUBIC)
    mask = Image.new("L", (W, H), 0)
    from PIL import ImageDraw
    ImageDraw.Draw(mask).polygon(QUAD, fill=255)
    mask = mask.filter(ImageFilter.MinFilter(7)).filter(ImageFilter.GaussianBlur(1.2))   # keep the frame untouched, soft edge

    # 2) the original face shading (slight gradients) modulates the screen a little
    gray = np.asarray(photo.convert("L").filter(ImageFilter.GaussianBlur(40)), float) / 255.0
    shade = 0.9 + 0.1 * np.clip(gray / max(gray[800:1100, 1000:1500].mean(), 1e-3), 0, 1.1)
    w_arr = np.asarray(warped, float) * shade[..., None]

    base = np.asarray(photo, float)
    m = (np.asarray(mask, float) / 255.0)[..., None]
    comp = base * (1 - m) + w_arr * m

    # 3) light spill: the screen's glow blooms onto the frame and the surroundings
    emit = Image.fromarray(np.clip(w_arr * m, 0, 255).astype(np.uint8))
    spill = np.asarray(emit.filter(ImageFilter.GaussianBlur(70)), float) * 0.7 + np.asarray(emit.filter(ImageFilter.GaussianBlur(22)), float) * 0.3
    outside = 1.0 - np.asarray(mask.filter(ImageFilter.GaussianBlur(6)), float)[..., None] / 255.0   # spill only lands outside the face
    spill = np.clip(spill, 0, 255) * outside
    comp = 255 - (255 - comp) * (255 - spill) / 255.0                              # screen blend

    # 4) a soft diagonal reflection of the sky on the glass
    yy, xx = np.mgrid[0:H, 0:W]
    refl = np.exp(-(((xx - 0.55 * yy) - 880) / 230.0) ** 2) * 0.07
    comp = comp + (255 - comp) * (refl * (np.asarray(mask, float) / 255.0))[..., None]

    # 5) a touch of grain over everything, then crop to 4:5
    rng = np.random.default_rng(3)
    comp = comp + rng.normal(0, 2.2, comp.shape)
    out = Image.fromarray(np.clip(comp, 0, 255).astype(np.uint8)).crop(CROP).resize(OUT, Image.LANCZOS)
    return out


if __name__ == "__main__":
    slides = HERE / "slides"; slides.mkdir(exist_ok=True)
    img = composite()
    img.save(slides / "wystak-prelaunch.png")
    print("ok", slides / "wystak-prelaunch.png", img.size)
