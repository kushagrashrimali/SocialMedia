"""WYSTAK palm-tree reveal: six storyboard frames and the 3x2 sheet.

One continuous shot of the seaside garden. The four palms (two crossing pairs that read as a W) bend, uncross and
turn navy from the ground up, become the navy W, the three passes fan out, and the shot ends on the exact logo.

How it is made (no generated images, no redrawn logo):
  * the seaside photo is the master plate; every frame starts from it, so the sky, sea, garden, fountains and people
    never change;
  * the palms are lifted off the plate: the sky behind them is rebuilt from a fitted sky model, each trunk is unwrapped
    into a bark texture strip, each crown is cut out and unmixed from the sky;
  * frames 2 and 3 redraw the trunks along new curves (the bases stay rooted) and carry the crowns on the trunk tops;
  * frames 4 to 6 use the supplied logo file, split into its navy, purple and teal layers (the colours, icons and
    angles come straight from the file). Frame 6 is the file itself.
  * the people, lamp posts and hedges in front of the trees are matted out of the plate and laid back on top.

  python3 build_storyboard.py [--plate photo.png] [--out frames_dir]
The default plate is frame 1 of the reference sheet in inbox/2026-10-10-palm-reveal/ (about 510 px, shown at 2x).
"""
import argparse, math, pathlib
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont
import plate as pl

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[2]
REF = ROOT / "inbox" / "2026-10-10-palm-reveal" / "reference-storyboard.webp"
LOGO = ROOT / "wystak" / "instagram" / "single-posts" / "prelaunch-billboard" / "assets" / "logo-mark.png"
SIZE = 1020

# where the logo sits in the shot (logo-file pixels -> plate pixels at SIZE): centred on the garden, standing in the
# hedge; the W's two bottom vertices sit close to where the palm pairs are rooted (the roots slide the rest)
LOGO_S = 0.64
LOGO_X0, LOGO_Y0 = 150.0, 268.0
# the W's stroke ends in logo-file pixels: each palm becomes one stroke
STROKE_TOP = {"T1": (110, 190), "T3": (485, 290), "T2": (485, 290), "T4": (830, 40)}
STROKE_BASE = {"T1": (318, 752), "T3": (330, 752), "T2": (676, 752), "T4": (696, 752)}
PIVOT = (820, 760)            # the passes fan around this point (logo-file pixels), tucked into the W's foot
PASS_ANGLE = {"purple": 13.5, "teal": 24.0}   # how far each pass is fanned out from the navy pass in the file (degrees)

# things standing in front of the trees between the horizon and the hedge line (fractions of the plate)
FRONT_BOXES = [(38, 622, 64, 752), (316, 648, 348, 752), (713, 648, 748, 752), (138, 708, 232, 752),
               (328, 704, 398, 752), (468, 700, 528, 752), (562, 708, 652, 752), (710, 708, 788, 752),
               (778, 714, 868, 752)]


# where a person stands right against a trunk's foot (their head and hands are in front of it)
KEEP_ON_TRUNK = [(348, 712, 380, 752), (598, 712, 646, 752)]


# ------------------------------------------------------------------------------------------------ sampling helpers
def bilinear(img, x, y):
    """Sample an (H, W, C) float image at float coordinates (any shape), clamped to the edges."""
    H, W = img.shape[:2]
    x = np.clip(x, 0, W - 1.001); y = np.clip(y, 0, H - 1.001)
    x0 = np.floor(x).astype(int); y0 = np.floor(y).astype(int)
    fx = (x - x0)[..., None]; fy = (y - y0)[..., None]
    a = img[y0, x0]; b = img[y0, x0 + 1]; c = img[y0 + 1, x0]; d = img[y0 + 1, x0 + 1]
    return (a * (1 - fx) + b * fx) * (1 - fy) + (c * (1 - fx) + d * fx) * fy


def over(base, rgb, a):
    return base * (1 - a[..., None]) + rgb * a[..., None]


def affine_layer(layer, M, out_hw):
    """Warp an RGBA float layer (premultiplied) by the 2x3 matrix M (layer pixels -> output pixels)."""
    H, W = out_hw
    A = np.vstack([M, [0, 0, 1]]); Ai = np.linalg.inv(A)
    # only work inside the bounding box of the warped layer
    h, w = layer.shape[:2]
    corners = A @ np.array([[0, w, w, 0], [0, 0, h, h], [1, 1, 1, 1]], float)
    x0 = int(max(0, np.floor(corners[0].min()) - 2)); x1 = int(min(W, np.ceil(corners[0].max()) + 2))
    y0 = int(max(0, np.floor(corners[1].min()) - 2)); y1 = int(min(H, np.ceil(corners[1].max()) + 2))
    out = np.zeros((H, W, 4), np.float32)
    if x1 <= x0 or y1 <= y0:
        return out
    yy, xx = np.mgrid[y0:y1, x0:x1].astype(np.float32)
    sx = Ai[0, 0] * xx + Ai[0, 1] * yy + Ai[0, 2]
    sy = Ai[1, 0] * xx + Ai[1, 1] * yy + Ai[1, 2]
    inside = (sx >= -0.5) & (sx <= w - 0.5) & (sy >= -0.5) & (sy <= h - 0.5)
    pad = np.pad(layer, ((1, 1), (1, 1), (0, 0)))
    v = bilinear(pad, sx + 1, sy + 1) * inside[..., None]
    out[y0:y1, x0:x1] = v
    return out


def premul(rgba):
    out = rgba.copy(); out[..., :3] *= rgba[..., 3:4]; return out


def comp_premul(base, layer):
    return base * (1 - layer[..., 3:4]) + layer[..., :3]


# ------------------------------------------------------------------------------------------------ the plate
class Scene:
    def __init__(self, plate_path):
        if plate_path is None:
            ref = Image.open(REF).convert("RGB")
            im = ref.crop((0, 0, 508, 508)).resize((SIZE, SIZE), Image.LANCZOS)
        else:
            im = Image.open(plate_path).convert("RGB").resize((SIZE, SIZE), Image.LANCZOS)
        P = np.asarray(im).astype(np.float32) / 255
        self.P = P
        H, W, _ = P.shape
        self.H, self.W = H, W
        self.hz = int(pl.HORIZON * H)
        self.hedge = int(pl.HEDGE * H)
        self.sky, _, self.sky_sd = pl.sky_model(P)
        A = pl.tree_alpha(P, self.sky)
        A[self.hz:] = 0
        bx0, by0, bx1, by1 = pl.BADGE
        A[:int(by1 * H), :int(bx1 * W)] = 0
        self.A = A
        self.rng = np.random.default_rng(11)
        self.fit_trunks()
        self.make_clean_plate()
        self.make_crowns()
        self.make_front_matte()
        self.make_textures()

    # each trunk: x(y) as a quadratic and its width as a line, fitted on the rows where it stands alone in the sky
    def fit_trunks(self):
        H, W, A = self.H, self.W, self.A
        self.trunks = {}
        tops = {k: (t["top"][0] * W, t["top"][1] * H) for k, t in pl.TREES.items()}
        bases = {k: (t["base"][0] * W, t["base"][1] * H) for k, t in pl.TREES.items()}
        def guess(k, y):
            (tx, ty), (bx, by) = tops[k], bases[k]
            return tx + (bx - tx) * (y - ty) / (by - ty)
        for k in pl.TREES:
            (tx, ty), (bx, by) = tops[k], bases[k]
            ys, xs, ws = [], [], []
            for y in range(int(ty) + 25, self.hz - 2):
                ex = guess(k, y)
                if any(abs(guess(o, y) - ex) < 45 and y > tops[o][1] for o in pl.TREES if o != k):
                    continue
                x0 = int(ex - 24); row = A[y, x0:x0 + 48]
                if (row > 0.5).sum() < 4:
                    continue
                ys.append(y); xs.append(x0 + (row * np.arange(len(row))).sum() / row.sum()); ws.append(row.sum())
            c = np.polyfit(ys, xs, 2); cw = np.polyfit(ys, ws, 1)
            # over the sea the trunk is the only brown thing near its line: add those rows, and pin the root
            P = self.P
            xh = np.polyval(c, self.hz)
            wts = [1.0] * len(ys)
            for y in range(self.hz + 3, int(by) - 8):
                ex = xh + (bx - xh) * (y - self.hz) / (by - self.hz)
                x0 = int(ex - 16); seg = P[y, x0:x0 + 32]
                brown = (seg[:, 0] - seg[:, 2] > 0.06) & (seg[:, 0] > 0.2)
                if brown.sum() < 4 or brown.sum() > 26:
                    continue
                ys.append(y); xs.append(x0 + np.nonzero(brown)[0].mean()); wts.append(1.0)
            ys.append(by); xs.append(bx); wts.append(25.0)
            c = np.polyfit(ys, xs, 2, w=np.sqrt(wts))
            yv = np.linspace(ty, by, int(np.hypot(bx - tx, by - ty)))
            pts = np.stack([np.polyval(c, yv), yv], 1)
            hw = np.polyval(cw, yv) / 2 + 0.6
            self.trunks[k] = dict(pts=pts, hw=hw, top=pts[0], base=pts[-1])

    def corridor(self, pad):
        """Pixels within pad of any trunk."""
        H, W = self.H, self.W
        m = np.zeros((H, W), bool)
        for k, t in self.trunks.items():
            pts, hw = t["pts"], t["hw"]
            for (x, y), h in zip(pts[::2], hw[::2]):
                r = h + pad
                x0, x1 = int(max(0, x - r)), int(min(W, x + r + 1)); y0, y1 = int(max(0, y - r)), int(min(H, y + r + 1))
                yy, xx = np.mgrid[y0:y1, x0:x1]
                m[y0:y1, x0:x1] |= (xx - x) ** 2 + (yy - y) ** 2 <= r * r
        return m

    def make_clean_plate(self):
        """The garden without the palms: the sky model under the fronds and trunks, sea and bushes copied sideways
        under the trunk feet."""
        P, H, W = self.P, self.H, self.W
        C = P.copy()
        yy, xx = np.mgrid[0:H, 0:W]
        tree = pl.gblur((self.A > 0.02).astype(np.float32), 1.5) > 0.01
        bx0, by0, bx1, by1 = pl.BADGE
        badge = (xx < bx1 * W) & (yy < by1 * H)
        hole = (tree | badge) & (yy < self.hz)
        noise = pl.gblur(self.rng.normal(0, self.sky_sd * 0.9, (H, W, 3)).astype(np.float32), 0.6)
        C[hole] = (self.sky + noise)[hole]
        # below the horizon: copy from beside the trunk
        cor = self.corridor(6) & (yy >= self.hz - 2) & (yy < self.hedge + 6)
        for y in np.unique(np.nonzero(cor)[0]):
            row = cor[y]
            xs = np.nonzero(row)[0]
            for x in xs:
                for dx in (36, -36, 60, -60, 90):
                    sx = x + dx
                    if 0 <= sx < W and not row[sx]:
                        C[y, x] = P[y, sx]; break
        # soften the copied seams a touch
        soft = pl.gblur(cor.astype(np.float32), 1.2)[..., None]
        C = C * (1 - soft * 0.5) + pl.gblur(C, 0.8) * soft * 0.5
        self.C = np.clip(C, 0, 1)
        # frame 1 is the photograph itself, with only the reference sheet's frame number painted out of the sky
        F1 = P.copy(); F1[badge] = (self.sky + noise)[badge]
        self.F1 = np.clip(F1, 0, 1)

    def make_crowns(self):
        """Each palm's crown as its own layer (colour unmixed from the sky), with the point where it sits on the trunk."""
        P, A, H, W = self.P, self.A, self.H, self.W
        yy, xx = np.mgrid[0:H, 0:W]
        tops = {k: t["top"] for k, t in self.trunks.items()}
        names = list(tops)
        # each frond pixel belongs to the palm it is connected to: grow labels out from the crown tops through the
        # frond pixels (first to arrive wins); pixels nothing reaches fall back to the nearest top
        zone_y = int(max(t[1] for t in tops.values()) + 70)
        M = (A[:zone_y] > 0.04)
        lab = np.full(M.shape, -1, np.int16)
        for i, k in enumerate(names):
            x, y = tops[k]
            lab[max(0, int(y) - 6):int(y) + 6, max(0, int(x) - 6):int(x) + 6] = i
        lab[~M & (lab < 0)] = -2
        for _ in range(900):
            changed = False
            for dy, dx in ((0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)):
                sh = np.roll(np.roll(lab, dy, 0), dx, 1)
                take = (lab == -1) & (sh >= 0)
                if take.any():
                    lab[take] = sh[take]; changed = True
            if not changed:
                break
        dist = np.stack([(xx - tops[k][0]) ** 2 + (yy - (tops[k][1] - 60)) ** 2 for k in names])
        nearest = np.argmin(dist, 0)
        full = np.full((H, W), -1, np.int16); full[:zone_y] = lab
        nearest = np.where(full >= 0, full, nearest)
        self.crowns = {}
        for i, k in enumerate(names):
            ty = tops[k][1]
            m = (A > 0.02) & (yy < ty + 40) & (nearest == i)
            m &= (xx - tops[k][0]) ** 2 + (yy - (tops[k][1] - 70)) ** 2 < 175 ** 2
            m &= ~self.corridor_one(k, 2, below=ty + 4)
            for o in names:
                if o != k:
                    m &= ~self.corridor_one(o, 3, below=tops[o][1] + 30)
            a = A * m
            fg = self.sky + (P - self.sky) / np.maximum(a, 0.12)[..., None]
            fg = np.clip(fg, 0, 1)
            ys, xs = np.nonzero(a > 0.01)
            x0, x1, y0, y1 = max(0, xs.min() - 2), min(W, xs.max() + 3), max(0, ys.min() - 2), min(H, ys.max() + 3)
            layer = np.concatenate([fg[y0:y1, x0:x1], a[y0:y1, x0:x1, None]], -1)
            self.crowns[k] = dict(layer=premul(layer), origin=(x0, y0), attach=tops[k])

    def corridor_one(self, k, pad, below=0):
        H, W = self.H, self.W
        m = np.zeros((H, W), bool)
        t = self.trunks[k]
        for (x, y), h in zip(t["pts"][::2], t["hw"][::2]):
            if y < below:
                continue
            r = h + pad
            x0, x1 = int(max(0, x - r)), int(min(W, x + r + 1)); y0, y1 = int(max(0, y - r)), int(min(H, y + r + 1))
            yy, xx = np.mgrid[y0:y1, x0:x1]
            m[y0:y1, x0:x1] |= (xx - x) ** 2 + (yy - y) ** 2 <= r * r
        return m

    def make_front_matte(self):
        """What stands in front of the trees: everything below the hedge line, plus the people's heads and the lamp
        posts that rise into the sea between the horizon and the hedge."""
        P, H, W = self.P, self.H, self.W
        r, g, b = P[..., 0], P[..., 1], P[..., 2]
        sea = (b > r + 0.08) & (b >= g - 0.03)
        bush = (g > r + 0.04) & (g > b - 0.01)
        sky = (b > r + 0.15)
        cand = ~(sea | bush | sky)
        yy0 = np.mgrid[0:H, 0:W][0]
        box = np.zeros((H, W), bool)
        k = SIZE / 1020
        for x0, y0, x1, y1 in FRONT_BOXES:
            box[int(y0 * k):int(y1 * k), int(x0 * k):int(x1 * k)] = True
        # on the trunks' own line only clearly dark (lamp iron, hair) or white (lamp glass) pixels can be in front
        cor = self.corridor(3)
        strict = ((P.max(-1) < 0.2) & (r - b < 0.04)) | (P.min(-1) > 0.8)
        keep = np.zeros((H, W), bool)
        for x0, y0, x1, y1 in KEEP_ON_TRUNK:
            keep[int(y0 * k):int(y1 * k), int(x0 * k):int(x1 * k)] = True
        F = cand & box & (~cor | (strict & keep))
        self.trunk_px = cor & ~strict & (yy0 >= self.hz - 2)
        img = Image.fromarray((F * 255).astype(np.uint8)).filter(ImageFilter.MaxFilter(3)).filter(ImageFilter.MinFilter(3))
        F = np.asarray(img, np.float32) / 255
        yy = np.mgrid[0:H, 0:W][0]
        F = np.maximum(F, (yy >= self.hedge).astype(np.float32))
        # hedge tops in front: walking up each column from the hedge line, everything until the sea shows through
        # is hedge (leaves, flowers and the shadows between them)
        fb = np.zeros((H, W), bool)
        fb[self.hedge:] = True
        open_sea = sea & (P.max(-1) > 0.3)
        for y in range(self.hedge - 1, self.hedge - 30, -1):
            below = fb[y + 1] & (np.roll(fb[y + 1], 1) | np.roll(fb[y + 1], -1))
            fb[y] = ~open_sea[y] & below
        near_bush = fb & (yy < self.hedge)
        nb = np.asarray(Image.fromarray((near_bush * 255).astype(np.uint8)).filter(ImageFilter.MinFilter(3)).filter(ImageFilter.MaxFilter(3)), np.float32) / 255
        people = F.copy()
        F = np.maximum(F, nb)
        # the palms' own feet are never in front of themselves (except where a person stands against them)
        F[cor & ~keep & (yy < self.hedge)] = 0
        # for the wider W the hedge must close over the old feet too: the hedge-top line across the trunk feet is
        # interpolated from the columns either side
        top = np.where(fb.any(0), fb.argmax(0), self.hedge).astype(np.float32)
        bad = cor[self.hedge - 12]
        bad = np.convolve(bad.astype(float), np.ones(9), "same") > 0
        xs = np.arange(W)
        top[bad] = np.interp(xs[bad], xs[~bad], top[~bad])
        hedge_w = (yy >= top[None, :]).astype(np.float32)
        Fw = np.maximum(np.where(cor & ~keep, 0, people), hedge_w)
        self.Fm_w = np.clip(pl.gblur(Fw, 0.7), 0, 1)
        self.Fm = np.clip(pl.gblur(F, 0.7), 0, 1)

    def make_textures(self):
        """Unwrap each trunk into a bark strip (rows from the crown down to the root, columns across the trunk)."""
        T = 40
        for k, t in self.trunks.items():
            pts, hw = t["pts"], t["hw"]
            d = np.gradient(pts, axis=0); d /= np.linalg.norm(d, axis=1, keepdims=True)
            n = np.stack([-d[:, 1], d[:, 0]], 1)
            tt = np.linspace(-1, 1, T)
            off = tt[None, :] * (hw[:, None] * 0.82)
            X = pts[:, 0:1] + n[:, 0:1] * off; Y = pts[:, 1:2] + n[:, 1:2] * off
            t["tex"] = bilinear(self.P, X, Y)


# ------------------------------------------------------------------------------------------------ logo layers
class Logo:
    def __init__(self):
        im = Image.open(LOGO).convert("RGBA")
        L = np.asarray(im).astype(np.float32) / 255
        self.size = im.size
        rgb, a = L[..., :3], L[..., 3]
        r, g, b = rgb[..., 0], rgb[..., 1], rgb[..., 2]
        H, W = a.shape
        yy, xx = np.mgrid[0:H, 0:W]
        white = (rgb.min(-1) > 0.62) & (a > 0.5)
        mx, mn = rgb.max(-1), rgb.min(-1)
        sat = (mx - mn) / np.maximum(mx, 1e-4)
        hue = np.degrees(np.arctan2(np.sqrt(3) * (g - b), 2 * r - g - b)) % 360
        coloured = (sat > 0.25) & ~white & (a > 0.02)
        teal = coloured & (hue > 150) & (hue <= 205)
        navy = coloured & (hue > 205) & (hue <= 252)
        purple = coloured & (hue > 252) & (hue <= 330)
        def body(mask, seed):
            im = Image.fromarray((mask * 255).astype(np.uint8)).copy()
            ImageDraw.floodfill(im, seed, 128)
            return np.asarray(im) == 128
        def opened(mask, r=5):
            im = Image.fromarray((mask * 255).astype(np.uint8))
            return np.asarray(im.filter(ImageFilter.MinFilter(r)).filter(ImageFilter.MaxFilter(r))) > 127
        navy = body(opened(navy), (110, 300)); purple = body(purple, (900, 450)); teal = body(teal, (1040, 420))
        lab = np.full((H, W), -1, int)
        lab[navy] = 0; lab[purple] = 1; lab[teal] = 2
        # the white icons belong to the pass they are printed on
        icon_ticket = white & (xx < 880) & (yy < 320)
        lab[white & (xx >= 880) & (xx < 1040) & (yy < 380)] = 1
        lab[white & (xx >= 1030)] = 2
        lab[icon_ticket] = 0
        # unlabelled dark edge pixels take their nearest label
        known = lab >= 0
        for _ in range(12):
            if (known | (a < 0.02)).all():
                break
            for dy, dx in ((0, 1), (0, -1), (1, 0), (-1, 0)):
                sh = np.roll(np.roll(lab, dy, 0), dx, 1)
                take = (lab < 0) & (sh >= 0) & (a > 0.02)
                lab[take] = sh[take]
        # the navy pass's right edge, where the purple pass sits behind it, is a straight line in the file: fit it,
        # so the navy layer ends on a clean antialiased edge instead of the colour boundary's stair-steps
        nb = (lab == 0) & ((np.roll(lab, -1, 1) == 1) | (np.roll(lab, -2, 1) == 1)) & (xx > 700) & (yy > 140) & (yy < 690)
        by, bx = np.nonzero(nb)
        ca = np.polyfit(by, bx, 1)
        edge_x = np.polyval(ca, yy)
        zone = (yy > 120) & (yy < 720) & (xx > 700) & (np.abs(xx - edge_x) < 14)
        self.navy_edge = (ca, zone)
        self.layers = {"full": L.copy()}          # the file itself, for the last frame
        for i, name in enumerate(("navy", "purple", "teal")):
            m = (lab == i).astype(np.float32)
            m = np.asarray(Image.fromarray((m * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(0.6)), np.float32) / 255
            self.layers[name] = np.concatenate([rgb, (a * m)[..., None]], -1)
        nav = self.layers["navy"]
        cut = np.clip(edge_x - xx + 0.5, 0, 1)
        nav[..., 3] = np.where(zone, a * cut * ((lab == 0) | (xx < edge_x - 1)), nav[..., 3])
        beyond = (yy > 120) & (yy < 720) & (xx > edge_x + 1) & (lab != 0)
        nav[..., 3][beyond] = 0
        # edge pixels take the colour just inside the pass (no purple fringe)
        inside = bilinear(rgb, np.clip(xx - 5, 0, W - 1).astype(np.float32), yy.astype(np.float32))
        band = zone & (xx > edge_x - 4)
        nav[..., :3][band] = inside[band]
        # the navy pass without its ticket: the W's fourth stroke before it reveals itself as a pass
        tk = np.asarray(Image.fromarray((icon_ticket * 255).astype(np.uint8)).filter(ImageFilter.MaxFilter(9)), np.float32) / 255
        tk = (pl.gblur(tk, 3) > 0.02)
        ticket_area = np.zeros_like(tk)
        ys, xs = np.nonzero(icon_ticket)
        y0, y1, x0, x1 = ys.min() - 6, ys.max() + 7, xs.min() - 6, xs.max() + 7
        ticket_area[y0:y1, x0:x1] = True
        hole = ticket_area & (lab == 0)
        hole = np.asarray(Image.fromarray((hole * 255).astype(np.uint8)).filter(ImageFilter.MaxFilter(7)), np.float32) > 0
        known_card = (lab == 0) & ~hole & (a > 0.95) & (xx > 640)
        filled = pl.fill_from(rgb, known_card, sigmas=(4, 10, 25, 60))
        blank = self.layers["navy"].copy()
        blank[..., :3] = np.where(hole[..., None], filled, rgb)
        self.layers["navy_blank"] = blank
        # the navy stroke's cross-section (for the trunks turning navy): across stroke A, averaged along its length
        p0, p1 = np.array([110., 190.]), np.array([320., 740.])
        dvec = (p1 - p0) / np.linalg.norm(p1 - p0); nvec = np.array([-dvec[1], dvec[0]])
        prof = []
        for f in np.linspace(0.35, 0.7, 30):
            c = p0 + (p1 - p0) * f
            ts = np.linspace(-110, 110, 221)
            pts = c[None, :] + ts[:, None] * nvec[None, :]
            prof.append(np.concatenate([bilinear(rgb, pts[:, 0], pts[:, 1]), bilinear(a[..., None], pts[:, 0], pts[:, 1])], -1))
        prof = np.mean(prof, 0)
        inside = np.nonzero(prof[:, 3] > 0.5)[0]
        self.stroke_profile = prof[inside[0] + 3:inside[-1] - 2, :3]
        self.stroke_hw = (inside[-1] - inside[0]) / 2 * LOGO_S

    def placed(self, name, out_hw, angle=0.0):
        """The layer at its place in the shot, rotated about the fan pivot by angle (degrees, counter-clockwise)."""
        lay = premul(self.layers[name])
        th = math.radians(angle)
        c, s = math.cos(th), math.sin(th)
        px, py = PIVOT
        # rotate about the pivot (counter-clockwise on screen = negative angle in image coordinates)
        R = np.array([[c, s, px - c * px - s * py], [-s, c, py + s * px - c * py]])
        S = np.array([[LOGO_S, 0, LOGO_X0], [0, LOGO_S, LOGO_Y0]])
        M = S @ np.vstack([R, [0, 0, 1]])
        return affine_layer(lay, M, out_hw)


def to_scene(p):
    return np.array([LOGO_X0 + LOGO_S * p[0], LOGO_Y0 + LOGO_S * p[1]])


# ------------------------------------------------------------------------------------------------ trunk renderer
def render_trunk(scene, k, pts, hw, navy=None, logo=None, smooth=0.0, roundness=0.0):
    """Draw trunk k along the polyline pts (crown end first) with half-widths hw. navy: per-point 0..1 amount of the
    navy material (the logo's stroke cross-section) replacing the bark."""
    H, W = scene.H, scene.W
    t = scene.trunks[k]
    tex = t["tex"]
    if smooth > 0:
        tex = pl.gblur(tex, smooth * 3.0)
        tex = tex * (1 - smooth) + tex.mean(1, keepdims=True) * smooth
    N = len(pts)
    m = max(hw) + 3
    full_pts = pts
    pts = np.vstack([full_pts[::4], full_pts[-1:]])      # a lighter polyline for the nearest-point search
    Nd = len(pts)
    x0, x1 = int(max(0, pts[:, 0].min() - m)), int(min(W, pts[:, 0].max() + m + 1))
    y0, y1 = int(max(0, pts[:, 1].min() - m)), int(min(H, pts[:, 1].max() + m + 1))
    yy, xx = np.mgrid[y0:y1, x0:x1].astype(np.float32)
    P = np.stack([xx.ravel(), yy.ravel()], 1)
    A, B = pts[:-1], pts[1:]
    best_d = np.full(len(P), 1e9, np.float32); best_u = np.zeros(len(P), np.float32); best_s = np.zeros(len(P), np.float32)
    for i in range(Nd - 1):
        ab = B[i] - A[i]; L2 = (ab ** 2).sum()
        ap = P - A[i]
        u = np.clip((ap @ ab) / L2, 0, 1)
        q = A[i] + u[:, None] * ab
        dv = P - q
        d = np.sqrt((dv ** 2).sum(1))
        better = d < best_d
        best_d[better] = d[better]
        best_u[better] = (i + u[better]) / (Nd - 1)
        cr = ab[0] * ap[:, 1] - ab[1] * ap[:, 0]
        best_s[better] = np.sign(cr[better])
    u = best_u.reshape(xx.shape); d = (best_d * best_s).reshape(xx.shape)
    h = np.interp(u, np.linspace(0, 1, N), hw)
    alpha = np.clip(h - np.abs(d) + 0.5, 0, 1)
    tn = np.clip(d / h, -1, 1)
    Ns, T = tex.shape[:2]
    col = bilinear(tex, (tn + 1) / 2 * (T - 1), u * (Ns - 1))
    if roundness > 0:
        # a thicker trunk gets its own bark at full resolution: the trunk's colour down its length, ring grooves
        # that curve round the cylinder, fine fibres, and sun from the upper left
        seg = np.sqrt((np.diff(full_pts, axis=0) ** 2).sum(1)); L = seg.sum()
        spx = u * L
        mid = pl.gblur(tex[:, T // 4: 3 * T // 4].mean(1)[:, None, :], 5)[:, 0]
        base = bilinear(mid[:, None, :], np.zeros_like(u), u * (Ns - 1))
        rng = np.random.default_rng(int(k[1]) * 17)
        n1 = pl.gblur(rng.normal(0, 1, (int(L) + 8, 1)).astype(np.float32), 6)[:, 0] * 2.2
        jitter = np.interp(spx, np.arange(len(n1)), n1)
        period = 11.0
        phase = spx / period + 0.22 * (1 - tn ** 2) + 0.35 * jitter
        groove = (0.5 + 0.5 * np.cos(2 * np.pi * phase)) ** 10
        ridge = (0.5 + 0.5 * np.cos(2 * np.pi * (phase - 0.18))) ** 6
        fib = pl.gblur(rng.normal(0, 1, (int(L / 4) + 8, 96)).astype(np.float32), 0.8)
        fv = bilinear(fib[..., None], (tn + 1) / 2 * 95, spx / 4)[..., 0]
        synth = base * (1 - 0.34 * groove[..., None] + 0.10 * ridge[..., None] + 0.05 * fv[..., None])
        shade = 1 - 0.36 * np.clip(tn, 0, 1) ** 1.2 + 0.10 * (1 - tn ** 2) - 0.06 * np.clip(-tn - 0.75, 0, 1) * 4
        synth = synth * shade[..., None]
        col = col * (1 - roundness) + np.clip(synth, 0, 1) * roundness
        self_phase = phase
    else:
        self_phase = None
    if navy is not None and logo is not None:
        prof = logo.stroke_profile
        pc = bilinear(prof[None], (tn + 1) / 2 * (len(prof) - 1), np.zeros_like(tn))
        nv = np.interp(u, np.linspace(0, 1, N), navy)
        if self_phase is not None:
            ring = (self_phase % 1.0)
            nv = np.clip(nv + (ring - 0.5) * 0.5 * (nv * (1 - nv)) * 4, 0, 1)
        pc = pc * (1 + 0.10 * np.exp(-((tn + 0.5) / 0.22) ** 2))[..., None]
        lum = col.mean(-1, keepdims=True)
        grain = (lum - pl.gblur(lum, 4)) * (1 - nv[..., None]) * 2.2
        col = col * (1 - nv[..., None]) + np.clip(pc * (1 + grain), 0, 1) * nv[..., None]
    layer = np.zeros((H, W, 4), np.float32)
    layer[y0:y1, x0:x1, :3] = col * alpha[..., None]
    layer[y0:y1, x0:x1, 3] = alpha
    return layer


def bezier(p0, c, p1, n):
    s = np.linspace(0, 1, n)[:, None]
    return (1 - s) ** 2 * p0 + 2 * (1 - s) * s * c + s * s * p1


def trunk_path(scene, k, q, bow):
    """The trunk's curve from crown to root: the original curve moved a fraction q of the way to its W stroke (the root
    stays put), plus a sideways bow in pixels (positive = to the trunk's right as seen walking up it)."""
    t = scene.trunks[k]
    pts = t["pts"]
    N = len(pts)
    s = np.linspace(0, 1, N)[:, None]           # 0 at the crown, 1 at the root
    target_top = to_scene(STROKE_TOP[k])
    target_base = to_scene(STROKE_BASE[k])
    line = target_base[None, :] * s + target_top[None, :] * (1 - s)
    path = pts * (1 - q) + line * q
    d = target_base - target_top; d /= np.linalg.norm(d)
    nrm = np.array([-d[1], d[0]])
    path = path + nrm[None, :] * bow * np.sin(np.pi * s) ** 1.1
    tail = path[-1] + (path[-1] - path[-8]) / np.linalg.norm(path[-1] - path[-8]) * np.arange(1, 25)[:, None]
    return np.vstack([path, tail])


def place_crown(scene, k, path, angle_extra=0.0, fold=(1.0, 1.0), sink=0.0, out_hw=None):
    """Carry crown k to the new trunk top: it turns with the trunk's top and can fold in (fold = (along, across))."""
    c = scene.crowns[k]
    t = scene.trunks[k]
    old_dir = t["pts"][0] - t["pts"][6]; new_dir = path[0] - path[6]
    rot = math.atan2(new_dir[1], new_dir[0]) - math.atan2(old_dir[1], old_dir[0]) + math.radians(angle_extra)
    ax = old_dir / np.linalg.norm(old_dir)
    # fold: scale along the trunk axis and across it, about the attach point (in the crown's original frame)
    U = np.array([ax, [-ax[1], ax[0]]])
    Sf = U.T @ np.diag(fold) @ U
    cr, sr = math.cos(rot), math.sin(rot)
    R = np.array([[cr, -sr], [sr, cr]])
    Mlin = R @ Sf
    att = np.array(c["attach"]); new_att = path[0] - (new_dir / np.linalg.norm(new_dir)) * sink
    ox, oy = c["origin"]
    # layer pixel (u,v) -> scene: new_att + Mlin @ ((u+ox, v+oy) - att)
    tvec = new_att + Mlin @ (np.array([ox, oy]) - att)
    M = np.hstack([Mlin, tvec[:, None]])
    return affine_layer(c["layer"], M, out_hw)


# ------------------------------------------------------------------------------------------------ the frames
def finish(scene, img, wide=False, drawn=None):
    """Lay the garden, people and lamp posts back in front, and add a gentle unsharp mask for the 2x plate.
    drawn: the alpha of what was drawn into the shot; it gets the plate's grain, and the hedge in front of it a little
    contact shading."""
    if drawn is not None:
        g = pl.gblur(scene.rng.normal(0, scene.sky_sd * 0.8, img.shape).astype(np.float32), 0.6)
        img = img + g * drawn[..., None]
    F = scene.Fm_w if wide else scene.Fm
    front = np.where(scene.trunk_px[..., None], scene.C, scene.P)
    if drawn is not None:
        H = scene.H
        ao = pl.gblur(np.roll(drawn, 8, 0), 9) * F
        yy = np.mgrid[0:H, 0:scene.W][0]
        ao *= np.clip(1 - (yy - scene.hedge) / 40, 0, 1)
        front = front * (1 - 0.22 * ao[..., None])
    out = over(img, front, F)
    blur = pl.gblur(out, 1.2)
    return np.clip(out + (out - blur) * 0.35, 0, 1)


def frame_trees(scene, logo, q, bows, sway, widen=0.0, navy_rise=0.0, smooth=0.0, fold=(1, 1), sink=0.0):
    H, W = scene.H, scene.W
    img = scene.C.copy()
    paths = {k: trunk_path(scene, k, q, bows[k]) for k in scene.trunks}
    drawn = np.zeros((H, W), np.float32)
    for k in ("T2", "T1", "T4", "T3"):          # T3 crosses in front of T2, as in the photo
        t = scene.trunks[k]
        s = np.linspace(0, 1, len(t["hw"]))
        navy = None
        # the trunk swells evenly towards the stroke width (a little more near the root)
        hw = t["hw"] * (1 - widen) + logo.stroke_hw * 0.44 * widen * (0.9 + 0.2 * s)
        if navy_rise > 0:
            # the navy finish climbs from the root with a long, soft edge
            edge = 1 - navy_rise
            z = np.clip((s - edge) / 0.10 + 0.5, 0, 1)
            navy = z * z * (3 - 2 * z)
        hw = np.concatenate([hw, np.full(24, hw[-1])])
        if navy is not None:
            navy = np.concatenate([navy, np.full(24, navy[-1])])
        lay = render_trunk(scene, k, paths[k], hw, navy=navy, logo=logo, smooth=smooth, roundness=widen)
        img = comp_premul(img, lay)
        drawn = np.maximum(drawn, lay[..., 3])
    for k in ("T1", "T2", "T3", "T4"):
        img = comp_premul(img, place_crown(scene, k, paths[k], sway[k], fold, sink, (H, W)))
    return finish(scene, img, wide=widen > 0, drawn=drawn)


def frame_logo(scene, logo, stage):
    H, W = scene.H, scene.W
    img = scene.C.copy()
    if stage == "w":
        lay = logo.placed("navy_blank", (H, W))
        img = comp_premul(img, lay)
        drawn = lay[..., 3]
    else:
        if stage == "fan":
            p_purple, p_teal = 0.62, 0.42
        else:
            p_purple, p_teal = 1.0, 1.0
        back_t = (1 - p_teal) * PASS_ANGLE["teal"]
        back_p = (1 - p_purple) * PASS_ANGLE["purple"]
        # a little rotational blur on the moving passes
        def blurred(name, ang, spread):
            if spread == 0:
                return logo.placed(name, (H, W), ang)
            acc = None
            n = 11
            for f in np.linspace(-0.5, 0.5, n):
                l = logo.placed(name, (H, W), ang + f * spread)
                acc = l if acc is None else acc + l
            return acc / n
        moving = stage == "fan"
        teal = blurred("teal", back_t, 0.9 if moving else 0)
        purple = blurred("purple", back_p, 0.7 if moving else 0)
        navy = logo.placed("navy", (H, W))
        if moving:
            # new contact shadows where a pass now overlaps the one behind it
            def shade(on, occ, k):
                sh = pl.gblur(np.roll(np.roll(occ[..., 3], 3, 0), 7, 1), 6) * k
                on = on.copy(); on[..., :3] *= (1 - sh)[..., None]; return on
            teal = shade(teal, purple, 0.45)
            purple = shade(purple, navy, 0.45)
        if stage == "final":
            # the end frame is the supplied logo file as it is, in one piece
            full = logo.placed("full", (H, W))
            img = comp_premul(img, full)
            drawn = full[..., 3]
        else:
            img = comp_premul(img, teal)
            img = comp_premul(img, purple)
            img = comp_premul(img, navy)
            drawn = np.maximum(np.maximum(teal[..., 3], purple[..., 3]), navy[..., 3])
    return finish(scene, img, wide=True, drawn=drawn)


FRAMES = [
    ("frame-01-familiar-scene", "The familiar scene"),
    ("frame-02-something-shifts", "Something feels different"),
    ("frame-03-nature-forms-the-mark", "Nature begins forming the mark"),
    ("frame-04-the-w-takes-shape", "The W takes shape"),
    ("frame-05-the-passes-emerge", "The loyalty passes emerge"),
    ("frame-06-wystak-logo", "The Wystak logo"),
]


def build(plate_path, out_dir):
    out_dir.mkdir(parents=True, exist_ok=True)
    scene = Scene(plate_path)
    logo = Logo()
    zero = {k: 0.0 for k in scene.trunks}
    frames = [
        scene.F1,
        frame_trees(scene, logo, q=0.16, bows={"T1": -14, "T2": 9, "T3": -9, "T4": 14},
                    sway={"T1": -4, "T2": 3, "T3": -3, "T4": 4}),
        frame_trees(scene, logo, q=0.84, bows={"T1": -6, "T2": 4, "T3": -4, "T4": 6},
                    sway={"T1": -2, "T2": 6, "T3": -6, "T4": 2}, widen=0.85, navy_rise=0.55, smooth=0.0,
                    fold=(0.92, 0.62), sink=6),
        frame_logo(scene, logo, "w"),
        frame_logo(scene, logo, "fan"),
        frame_logo(scene, logo, "final"),
    ]
    paths = []
    for (name, _), f in zip(FRAMES, frames):
        p = out_dir / f"{name}.png"
        Image.fromarray((np.clip(f, 0, 1) * 255 + 0.5).astype(np.uint8)).save(p)
        paths.append(p)
    sheet(paths, out_dir / "wystak-palm-reveal-storyboard.png")
    return paths


def sheet(paths, out):
    gut, n = 24, SIZE
    Wd, Hd = 3 * n + 4 * gut, 2 * n + 3 * gut
    S = Image.new("RGB", (Wd, Hd), (255, 255, 255))
    d = ImageDraw.Draw(S)
    try:
        font = ImageFont.truetype("/usr/share/fonts/opentype/inter/Inter-SemiBold.otf", 30)
    except OSError:
        font = ImageFont.load_default()
    for i, p in enumerate(paths):
        x = gut + (i % 3) * (n + gut); y = gut + (i // 3) * (n + gut)
        S.paste(Image.open(p), (x, y))
        cx, cy = x + 44, y + 44
        d.ellipse((cx - 24, cy - 24, cx + 24, cy + 24), fill=(28, 36, 60))
        d.text((cx, cy + 1), str(i + 1), font=font, fill=(255, 255, 255), anchor="mm")
    S.save(out)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--plate", default=None)
    ap.add_argument("--out", default=str(HERE / "frames"))
    a = ap.parse_args()
    for p in build(a.plate, pathlib.Path(a.out)):
        print(p)
