"""The supplied horizontal WYSTAK logo, prepared for the v11 introduction (nothing redrawn).

1. Cut out its white background: only the white connected to the image border goes; whites inside the logo stay.
   The rim is un-blended against white so there is no halo.          -> assets/brand/logo-lockup-horizontal.png
2. Split it into layers by colour so the passes can move: the purple pass, the teal pass (each with its icon and its own
   dark outline), the mark (the W and the navy pass) and the wordmark.  -> assets/brand/lockup-parts/*.png
   Stacked unmoved (teal, purple, mark, wordmark) the layers are pixel-identical to step 1.
usage (from the project folder): python3 -I storyboard/split_lockup_v11.py
"""
import pathlib
import numpy as np
from PIL import Image
from scipy import ndimage as nd

B = pathlib.Path(__file__).resolve().parent.parent / "assets/brand"
im = np.asarray(Image.open(B / "logo-lockup-horizontal.jpg").convert("RGB")).astype(np.float64) / 255
white = im.min(axis=2) > 0.90
lab, _ = nd.label(white)
bg = np.isin(lab, list(set(np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]]))) - {0}))
band = nd.binary_dilation(bg, iterations=3) & ~bg
a = np.ones(im.shape[:2]); a[bg] = 0
a[band] = np.clip((1 - im).max(axis=2)[band] / 0.55, 0, 1)
rgb = im.copy(); m = band & (a > 0) & (a < 1)
rgb[m] = np.clip((im[m] - (1 - a[m])[:, None]) / a[m][:, None], 0, 1)
cut = (np.dstack([rgb, a]) * 255 + 0.5).astype(np.uint8)
Image.fromarray(cut, "RGBA").save(B / "logo-lockup-horizontal.png", optimize=True)

px = cut.astype(np.float64); R, G, Bc, al = px[..., 0], px[..., 1], px[..., 2], px[..., 3]
op = al > 128
mark = np.zeros(al.shape, bool); mark[:, :770] = True
def largest_filled(m):
    lab, n = nd.label(m); keep = np.argmax(nd.sum(m, lab, range(1, n + 1))) + 1
    return nd.binary_fill_holes(lab == keep)
purple = largest_filled(op & mark & (R > Bc * 0.42) & (R > G + 25) & (Bc > G + 40))
teal = largest_filled(op & mark & (G > R + 35) & (G > Bc * 0.62))
navyish = op & (Bc > R + 30) & (G < R + 40) & ~purple & ~teal
grow = lambda m, other: m | (nd.binary_dilation(m, iterations=3) & ~m & ~other & ~navyish & mark)
p = grow(purple, teal); t = grow(teal, p)
base = mark & ~p & ~t
# each pass's thin dark outline sits on the base layer after the colour split: hand it to the nearest pass
st = np.ones((7, 7), bool); body = nd.binary_opening(base, structure=st)
mov = base & ~body & (nd.binary_dilation(p, iterations=10) | nd.binary_dilation(t, iterations=10))
lab, n = nd.label(mov)
for i in range(1, n + 1):
    comp = lab == i
    if (nd.binary_dilation(comp, iterations=2) & body).sum() > 0.6 * comp.sum():
        mov[comp] = False
dp, dt = nd.distance_transform_edt(~p), nd.distance_transform_edt(~t)
p |= mov & (dp <= dt); t |= mov & (dt < dp); base &= ~mov
(B / "lockup-parts").mkdir(exist_ok=True)
for mask, name in ((base, "mark-base"), (p, "card-purple"), (t, "card-teal"), (~mark, "wordmark")):
    o = cut.copy(); o[..., 3] = np.where(mask, cut[..., 3], 0)
    Image.fromarray(o, "RGBA").save(B / "lockup-parts" / f"{name}.png", optimize=True)
print("wrote logo-lockup-horizontal.png and lockup-parts/")
