"""WYSTAK pre-launch post 2 (1080x1350): the Wystak mark standing in the seaside garden, as a photo post on its own.

The picture is frame 6 of videos/wystak-palm-reveal (assets/garden.jpg, 1020 square). For the 4:5 feed frame it is scaled
to 1080 wide and the sky is extended upward: each column's sky colour is fitted on the top rows of the photo and carried
up with the same vertical gradient, plus matching grain. A light grade and sharpen finish it. Run: python3 build.py
"""
import pathlib
import numpy as np
from PIL import Image, ImageFilter

HERE = pathlib.Path(__file__).resolve().parent
W, H = 1080, 1350

if __name__ == "__main__":
    im = Image.open(HERE / "assets" / "garden.jpg").convert("RGB").resize((W, W), Image.LANCZOS)
    a = np.asarray(im).astype(np.float32) / 255
    ext = H - W
    # a smooth sky model (quadratic across, linear down) fitted on the photo's top rows, carried upward
    yy, xx = np.mgrid[10:170, 0:W].astype(np.float32)
    X, Y = xx / W, yy / W
    T = lambda X, Y: [np.ones_like(X), X, X * X, Y, X * Y]
    A = np.stack([t.ravel() for t in T(X, Y)], 1)
    coef = [np.linalg.lstsq(A, a[10:170, :, c].ravel(), rcond=None)[0] for c in range(3)]
    def sky(y0, y1):
        yy, xx = np.mgrid[y0:y1, 0:W].astype(np.float32)
        X, Y = xx / W, yy / W * 0.6
        return np.stack([sum(k * t for k, t in zip(cf, T(X, Y))) for cf in coef], -1)
    top = np.clip(sky(-ext, 0), 0, 1)
    rng = np.random.default_rng(4)
    noise = np.asarray(Image.fromarray((rng.normal(128, 4.5, (ext, W, 3))).clip(0, 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(0.6)), np.float32) / 255 - 0.5
    top = top + noise
    out = np.concatenate([top, a], 0)
    # blend the seam over 40 rows
    s = ext; b = 40
    w = np.linspace(0, 1, b)[:, None, None]
    pred = sky(0, b)
    out[s:s + b] = pred * (1 - w) + a[:b] * w + noise[:b] * (1 - w)
    # grade: a touch more contrast and warmth in the garden, a cleaner sky
    out = np.clip((out - 0.5) * 1.05 + 0.5, 0, 1)
    out[..., 0] *= 1.01
    img = Image.fromarray((np.clip(out, 0, 1) * 255 + 0.5).astype(np.uint8))
    img = img.filter(ImageFilter.UnsharpMask(radius=1.4, percent=55, threshold=2))
    d = HERE / "slides"; d.mkdir(exist_ok=True)
    img.save(d / "wystak-prelaunch-post-2.png")
    print("ok")
