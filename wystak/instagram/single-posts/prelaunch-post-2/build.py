"""WYSTAK pre-launch post 2 (1080x1350): the palms that became the W, in three marketing styles.

Concept (from videos/wystak-palm-reveal): four seaside palms already read as a W; one day they become the Wystak mark.
  a  Then / Soon   the palms over the mark, split, with one line between them
  b  The landmark  huge type set behind the mark in the sky (the mark and the visitors stand in front of it)
  c  Postcard      a seaside postcard on paper, with a stamp and a postmark
Layers come from the storyboard pipeline (videos/wystak-palm-reveal/storyboard): the clean garden, the supplied logo
placed in the shot, and the matte of everything standing in front of it. The 1020-square plate is scaled to 1080 and its
sky is extended upward for the 4:5 frame. Run: python3 build.py [a|b|c ...]
"""
import sys, pathlib, importlib.util
import numpy as np
from PIL import Image, ImageFilter

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[3]
SB = ROOT / "videos" / "wystak-palm-reveal" / "storyboard"
sys.path.insert(0, str(SB))
spec = importlib.util.spec_from_file_location("v2", HERE.parent / "prelaunch-billboard-v2" / "build.py")
v2 = importlib.util.module_from_spec(spec); spec.loader.exec_module(v2)

W, H = 1080, 1350
EXT = H - W
NAVY, VIOLET, TEAL, IVORY = "#0a2860", "#6b2ba6", "#06737c", "#FBF6EC"


def extend_sky(a):
    """a: (1080, 1080, 3) float. Returns (1350, 1080, 3) with a smooth sky model carried up from the top rows."""
    yy, xx = np.mgrid[10:170, 0:W].astype(np.float32)
    T = lambda X, Y: [np.ones_like(X), X, X * X, Y, X * Y]
    A = np.stack([t.ravel() for t in T(xx / W, yy / W)], 1)
    coef = [np.linalg.lstsq(A, a[10:170, :, c].ravel(), rcond=None)[0] for c in range(3)]
    def sky(y0, y1):
        yy, xx = np.mgrid[y0:y1, 0:W].astype(np.float32)
        return np.stack([sum(k * t for k, t in zip(cf, T(xx / W, yy / W * 0.6))) for cf in coef], -1)
    rng = np.random.default_rng(4)
    noise = np.asarray(Image.fromarray(rng.normal(128, 4.5, (EXT + 40, W, 3)).clip(0, 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(0.6)), np.float32) / 255 - 0.5
    out = np.concatenate([np.clip(sky(-EXT, 0), 0, 1) + noise[:EXT], a], 0)
    w = np.linspace(0, 1, 40)[:, None, None]
    out[EXT:EXT + 40] = (sky(0, 40) + noise[EXT:]) * (1 - w) + a[:40] * w
    return np.clip(out, 0, 1)


def save(arr, name, alpha=None):
    im = Image.fromarray((np.clip(arr, 0, 1) * 255 + 0.5).astype(np.uint8))
    if alpha is not None:
        im.putalpha(Image.fromarray((np.clip(alpha, 0, 1) * 255 + 0.5).astype(np.uint8)))
    im.save(HERE / "assets" / name)


def up(a):  # 1020 -> 1080
    ch = a.shape[2] if a.ndim == 3 else 1
    im = Image.fromarray((np.clip(a, 0, 1) * 255).astype(np.uint8) if ch > 1 else (np.clip(a, 0, 1) * 255).astype(np.uint8))
    return np.asarray(im.resize((W, W), Image.LANCZOS), np.float32) / 255


def layers():
    """_bg (garden without the mark, sky extended), _logo (the mark, RGBA), _front (people, hedges, lamps, RGBA),
    _palms (the photo before, sky extended), _garden (the photo after, sky extended)."""
    import build_storyboard as bs
    sc = bs.Scene(None); lg = bs.Logo()
    full = lg.placed("full", (sc.H, sc.W))
    a = full[..., 3]
    rgb = full[..., :3] / np.maximum(a[..., None], 1e-4)
    clean = bs.finish(sc, sc.C, wide=True, drawn=None)
    F = sc.Fm_w
    front = np.where(sc.trunk_px[..., None], sc.C, sc.P)
    pad = lambda x: np.concatenate([np.zeros((EXT,) + x.shape[1:], np.float32), x], 0)
    save(extend_sky(up(clean)), "_bg.png")
    save(pad(up(rgb)), "_logo.png", pad(up(a)))
    save(pad(up(front)), "_front.png", pad(up(F)))
    for src, name in (("palms.jpg", "_palms.png"), ("garden.jpg", "_garden.png")):
        p = np.asarray(Image.open(HERE / "assets" / src).convert("RGB"), np.float32) / 255
        save(extend_sky(up(p)), name)


FONTS = """
@font-face{font-family:I;src:url(assets/inter-latin-500-normal.woff2);font-weight:500}
@font-face{font-family:I;src:url(assets/inter-latin-700-normal.woff2);font-weight:700}
@font-face{font-family:I;src:url(assets/inter-latin-900-normal.woff2);font-weight:900}
@font-face{font-family:A;src:url(assets/anton-latin-400-normal.woff2)}
@font-face{font-family:C;src:url(assets/caveat-latin-700-normal.woff2)}
@font-face{font-family:D;src:url(assets/dm-serif-display-latin-400-normal.woff2)}
@font-face{font-family:D;src:url(assets/dm-serif-display-latin-400-italic.woff2);font-style:italic}
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:1080px;height:1350px;overflow:hidden}
body{font-family:I,sans-serif}
.abs{position:absolute}
.grain{position:absolute;inset:0;opacity:.06;mix-blend-mode:multiply;pointer-events:none;background-image:url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='300' height='300'><filter id='n'><feTurbulence type='fractalNoise' baseFrequency='.9' numOctaves='2' stitchTiles='stitch'/></filter><rect width='300' height='300' filter='url(%23n)'/></svg>")}
"""


def page(css, body):
    return f'<!doctype html><html><head><meta charset="utf-8"><style>{FONTS}{css}</style></head><body>{body}</body></html>'


def opt_a():
    """Then / Soon: the palms over the mark, two strips, and the line between them."""
    css = f"""
body{{background:{IVORY}}}
.strip{{left:0;width:1080px;height:600px;background-size:1080px 1350px;overflow:hidden}}
.t{{top:0;background-image:url(assets/_palms.png);background-position:0 -470px}}
.s{{top:750px;background-image:url(assets/_garden.png);background-position:0 -500px}}
.chip{{position:absolute;left:40px;padding:12px 24px;border-radius:40px;background:rgba(10,18,56,.82);color:#fff;font-weight:700;font-size:28px;letter-spacing:.18em}}
.mid{{left:0;right:0;top:600px;height:150px;display:flex;align-items:center;justify-content:center;gap:28px;font-family:D;font-size:78px;color:{NAVY};letter-spacing:-.01em}}
.mid i{{color:{VIOLET}}}
.arrow{{width:70px;height:70px;border-radius:50%;background:{NAVY};display:flex;align-items:center;justify-content:center}}
"""
    body = f"""<div class="abs strip t"><div class="chip" style="top:36px">THEN</div></div>
<div class="abs mid">Nature drew the <i>W.</i><div class="arrow"><svg width="34" height="34" viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="2.6" stroke-linecap="round"><path d="M12 4v16M5 13l7 7 7-7"/></svg></div></div>
<div class="abs strip s"><div class="chip" style="top:36px;background:{VIOLET}">SOON</div>
  <div class="abs" style="right:40px;bottom:34px;font-family:D;font-style:italic;font-size:46px;color:#fff;text-shadow:0 2px 14px rgba(0,0,0,.45)">We just finished it.</div></div>
<div class="grain"></div>"""
    return page(css, body)


def opt_b():
    """The landmark: huge type behind the mark."""
    css = f"""
body{{background:url(assets/_bg.png) 0 0/1080px 1350px}}
.big{{left:0;right:0;top:290px;text-align:center;font-family:A;font-size:300px;line-height:1;letter-spacing:.02em;color:rgba(255,255,255,.92);
  text-shadow:0 10px 40px rgba(20,60,120,.18)}}
.kick{{left:0;right:0;top:120px;text-align:center;font-weight:700;font-size:30px;letter-spacing:.42em;color:{NAVY};padding-left:.42em}}
.foot{{left:0;right:0;bottom:44px;text-align:center;font-family:D;font-style:italic;font-size:54px;color:#fff;text-shadow:0 2px 18px rgba(0,0,0,.55)}}
.layer{{left:0;top:0;width:1080px;height:1350px}}
.shade{{left:0;right:0;bottom:0;height:300px;background:linear-gradient(180deg,rgba(0,0,0,0),rgba(0,0,0,.42))}}
"""
    body = """<div class="abs kick">THE NEW LANDMARK</div>
<div class="abs big">WYSTAK</div>
<img class="abs layer" src="assets/_logo.png"><img class="abs layer" src="assets/_front.png">
<div class="abs shade"></div>
<div class="abs foot">Some things are worth the wait.</div>
<div class="grain"></div>"""
    return page(css, body)


def opt_c():
    """Postcard: the photo as a seaside postcard on a paper ground, a stamp and a postmark."""
    stamp = f'''<div class="abs stamp"><div class="perf"><img src="assets/logo-mark.png" style="width:150px"><div style="font-weight:700;font-size:18px;letter-spacing:.2em;color:{NAVY};margin-top:8px">WYSTAK</div></div></div>'''
    css = f"""
body{{background:radial-gradient(90% 70% at 50% 40%,#F6EBD7 0%,#EBDCC0 100%)}}
.card{{left:70px;top:170px;width:940px;height:1050px;background:#FFFDF8;padding:34px 34px 0;transform:rotate(-2.2deg);box-shadow:0 30px 60px rgba(90,60,20,.30),0 2px 0 rgba(0,0,0,.05)}}
.ph{{width:872px;height:820px;background:url(assets/_garden.png) 0 -270px/872px 1090px}}
.cap{{display:flex;justify-content:space-between;align-items:center;height:196px;padding:0 6px}}
.hello{{font-family:C;font-size:92px;color:{NAVY};line-height:.95}}
.hello b{{color:{VIOLET};font-weight:700}}
.right{{text-align:right;font-weight:700;font-size:24px;letter-spacing:.24em;color:{TEAL};line-height:1.6}}
.stamp{{left:790px;top:200px;transform:rotate(6deg);filter:drop-shadow(0 8px 12px rgba(90,60,20,.35))}}
.perf{{width:200px;height:240px;background:#fff;display:flex;flex-direction:column;align-items:center;justify-content:center;
  outline:8px dotted #FFFDF8;outline-offset:-4px;border:10px solid #fff;box-shadow:inset 0 0 0 3px rgba(10,40,96,.25)}}
.pm{{left:590px;top:250px;width:250px;height:250px;border-radius:50%;border:5px solid rgba(10,40,96,.55);transform:rotate(-14deg);display:flex;align-items:center;justify-content:center;
  font-weight:900;font-size:30px;letter-spacing:.16em;color:rgba(10,40,96,.6);text-align:center;line-height:1.25}}
.waves{{left:470px;top:330px}}
.top{{left:0;right:0;text-align:center;top:52px;font-family:D;font-size:62px;color:{NAVY}}}
.top i{{color:{VIOLET}}}
"""
    waves = '<svg class="abs waves" width="200" height="90" viewBox="0 0 200 90" fill="none" stroke="rgba(10,40,96,.5)" stroke-width="5">' + "".join(
        f'<path d="M0 {12 + i * 22} q25 -14 50 0 t50 0 t50 0 t50 0"/>' for i in range(4)) + "</svg>"
    body = f"""<div class="abs top">The palms finally <i>spelled it out.</i></div>
<div class="abs card"><div class="ph"></div><div class="cap"><div class="hello">Greetings from<br><b>the new landmark</b></div>
<div class="right">ARRIVING<br>SOON</div></div></div>
<div class="abs pm">COMING<br>SOON</div>{waves}{stamp}
<div class="grain"></div>"""
    return page(css, body)


OPTIONS = {"a": opt_a, "b": opt_b, "c": opt_c}

if __name__ == "__main__":
    if not (HERE / "assets" / "_bg.png").exists() or "--layers" in sys.argv:
        layers()
    out = HERE / "slides"; out.mkdir(exist_ok=True)
    v2.HERE = HERE; v2.H = H
    for k in [a for a in sys.argv[1:] if a in OPTIONS] or list(OPTIONS):
        v2.render(OPTIONS[k](), out / f"wystak-prelaunch-post-2-{k}.png"); print("ok", k)
