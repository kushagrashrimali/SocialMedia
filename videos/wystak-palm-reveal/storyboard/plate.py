"""Plate analysis for the palm-tree reveal: the seaside photo, its sky model, the tree layers and a clean plate.

Everything is measured on the master plate (the seaside garden photo) and kept in fractions of its size, so a
higher-resolution copy of the same photo can be dropped in later (python3 build_storyboard.py --plate <file>).
"""
import numpy as np
from PIL import Image, ImageFilter

HORIZON = 639 / 1020          # sea horizon, as a fraction of the plate height
HEDGE = 752 / 1020            # below this line everything belongs to the garden (in front of the trees)

# the four palms (fractions of width, height): top = where the crown sits on the trunk, base = where it meets the hedge
TREES = {
    "T1": dict(top=(180 / 1020, 326 / 1020), base=(388 / 1020, 745 / 1020)),
    "T2": dict(top=(416 / 1020, 276 / 1020), base=(644 / 1020, 742 / 1020)),
    "T3": dict(top=(630 / 1020, 290 / 1020), base=(390 / 1020, 745 / 1020)),
    "T4": dict(top=(836 / 1020, 350 / 1020), base=(650 / 1020, 745 / 1020)),
}
BADGE = (0.0, 0.0, 0.115, 0.11)   # the reference sheet's frame number sits here; it is painted out of the sky


def load(path, size=None):
    im = Image.open(path).convert("RGB")
    if size:
        im = im.resize(size, Image.LANCZOS)
    return np.asarray(im).astype(np.float32) / 255


def gblur(a, sigma):
    """Separable gaussian blur of an (H, W) or (H, W, C) float array."""
    squeeze = a.ndim == 2
    if squeeze:
        a = a[..., None]
    r = max(1, int(sigma * 3))
    k = np.exp(-0.5 * (np.arange(-r, r + 1) / sigma) ** 2); k /= k.sum()
    out = a.astype(np.float32)
    for ax in (0, 1):
        pad = [(0, 0)] * 3; pad[ax] = (r, r)
        p = np.pad(out, pad, mode="edge")
        acc = np.zeros_like(out)
        n = out.shape[ax]
        for i, kv in enumerate(k):
            acc += kv * (p[i:i + n] if ax == 0 else p[:, i:i + n])
        out = acc
    return out[..., 0] if squeeze else out


def fill_from(img, known, sigmas=(2, 5, 12, 30, 80)):
    """Normalized-convolution fill: unknown pixels take the blurred average of the known pixels around them."""
    out = img.copy()
    done = known.astype(bool).copy()
    for s in sigmas:
        w = gblur(known.astype(np.float32), s)
        v = gblur(img * known[..., None], s) / np.maximum(w[..., None], 1e-5)
        take = (~done) & (w > 0.02)
        out[take] = v[take]
        done |= take
    return out


def sky_model(P):
    """A smooth model of the sky (cubic polynomial in x, y per channel), fitted on clear-sky pixels."""
    H, W, _ = P.shape
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    r, g, b = P[..., 0], P[..., 1], P[..., 2]
    hz = int(HORIZON * H)
    sky = (b > r + 0.17) & (b > g + 0.03) & (yy < hz - 3)
    sky &= gblur(sky.astype(np.float32), 2) > 0.98            # away from fronds and trunks
    bx0, by0, bx1, by1 = BADGE
    sky &= ~((xx < bx1 * W) & (yy < by1 * H))
    X, Y = xx / W, yy / H
    terms = [np.ones_like(X), X, Y, X * Y, X * X, Y * Y, X * X * Y, X * Y * Y, X ** 3, Y ** 3]
    A = np.stack([t[sky] for t in terms], 1)
    model = np.zeros_like(P)
    for c in range(3):
        coef, *_ = np.linalg.lstsq(A, P[..., c][sky], rcond=None)
        model[..., c] = sum(cf * t for cf, t in zip(coef, terms))
    resid = (P - model)[sky]
    return model, sky, float(resid.std())


def tree_alpha(P, sky):
    """How much of each sky-region pixel is tree (fronds and trunks), by distance from the sky colour."""
    d = np.sqrt(((P - sky) ** 2).sum(-1))
    return np.clip((d - 0.035) / 0.30, 0, 1)
