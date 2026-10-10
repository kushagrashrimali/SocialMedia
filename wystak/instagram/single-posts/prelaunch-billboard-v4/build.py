"""WYSTAK pre-launch billboard poster, v4: "Every story has a moment. This is ours." (1080x2100, the billboard screen).

Built in the style of the user's reference (a Blinkit outdoor poster): one rich colour field, a chat-screen header that tells
the story in two bubbles, a huge heavy headline with one accent line, the product hero with a real shadow, and a brand foot
row. Premium palette: midnight navy with a violet glow, ivory type, a champagne-gold accent.
The card holder with the supplied logo is assets/holder-dark.png (made in ../prelaunch-billboard-v2 and v3).
Run: python3 build.py
"""
import sys, pathlib
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "prelaunch-billboard-v2"))
import build as v2
from PIL import Image

W, H = v2.W, v2.H
INK, IVORY, GOLD, MINT = "#0B1238", "#FBF3E6", "#F4C66E", "#9FF0D2"

ICON = lambda d, w=46: f'<svg width="{w}" height="{w}" viewBox="0 0 24 24" fill="none" stroke="{IVORY}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">{d}</svg>'
PHONE = ICON('<path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1.9.4 1.8.7 2.7a2 2 0 0 1-.5 2.1L8 9.8a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.7.7a2 2 0 0 1 1.7 2z"/>')
VIDEO = ICON('<rect x="2" y="6" width="14" height="12" rx="2"/><path d="M16 10l6-3v10l-6-3z"/>')
DOTS = ICON('<circle cx="12" cy="5" r="1.2" fill="#FBF3E6"/><circle cx="12" cy="12" r="1.2" fill="#FBF3E6"/><circle cx="12" cy="19" r="1.2" fill="#FBF3E6"/>')
BACK = ICON('<path d="M19 12H5M11 6l-6 6 6 6"/>')
TICKS = '<svg width="34" height="20" viewBox="0 0 34 20" fill="none" stroke="#3B82F6" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="M2 11l5 5 10-11"/><path d="M14 15l2 1 10-11"/></svg>'


def html():
    hs = Image.open(HERE / "assets" / "holder-dark.png").size
    hw = 900; hh = round(hs[1] * hw / hs[0])
    return f'''<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{{font-family:I;src:url(assets/inter-latin-500-normal.woff2);font-weight:500}}
@font-face{{font-family:I;src:url(assets/inter-latin-600-normal.woff2);font-weight:600}}
@font-face{{font-family:I;src:url(assets/inter-latin-700-normal.woff2);font-weight:700}}
@font-face{{font-family:I;src:url(assets/inter-latin-800-normal.woff2);font-weight:800}}
@font-face{{font-family:I;src:url(assets/inter-latin-900-normal.woff2);font-weight:900}}
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:{W}px;height:{H}px;overflow:hidden}}
body{{font-family:I,sans-serif;color:{IVORY};
  background:radial-gradient(60% 32% at 68% 72%,rgba(150,255,210,.30) 0%,rgba(150,255,210,0) 100%),
             radial-gradient(80% 40% at 10% 0%,rgba(120,230,190,.22) 0%,rgba(120,230,190,0) 100%),
             linear-gradient(180deg,#0E6B4F 0%,#0A5540 55%,#063A2C 100%)}}
.abs{{position:absolute}}
.grain{{position:absolute;inset:0;opacity:.07;mix-blend-mode:overlay;background-image:url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='300' height='300'><filter id='n'><feTurbulence type='fractalNoise' baseFrequency='.9' numOctaves='2' stitchTiles='stitch'/></filter><rect width='300' height='300' filter='url(%23n)'/></svg>")}}
.time{{left:0;right:0;top:46px;text-align:center;font-weight:600;font-size:30px;opacity:.75}}
.head{{left:64px;right:64px;top:112px;height:96px;display:flex;align-items:center;gap:26px}}
.av{{width:92px;height:92px;border-radius:50%;background:#FFFFFF;display:flex;align-items:center;justify-content:center;box-shadow:0 6px 18px rgba(0,0,0,.35)}}
.name{{font-weight:700;font-size:40px;line-height:1.1}} .on{{font-weight:500;font-size:26px;color:{MINT}}}
.icons{{margin-left:auto;display:flex;gap:44px;align-items:center}}
.b{{position:absolute;padding:26px 34px 22px;border-radius:30px;font-weight:500;font-size:42px;line-height:1.2;box-shadow:0 14px 30px rgba(0,30,20,.35)}}
.b small{{display:block;text-align:right;font-size:22px;margin-top:6px;opacity:.6;font-weight:500}}
.in{{left:64px;top:282px;background:#FFFFFF;color:#141833;border-bottom-left-radius:8px}}
.out{{right:64px;top:452px;background:#CDEFE3;color:#0D2A22;border-bottom-right-radius:8px}}
.out small{{display:flex;justify-content:flex-end;align-items:center;gap:8px}}
.hl{{left:64px;top:666px;font-weight:900;font-size:136px;line-height:.98;letter-spacing:-.055em;white-space:nowrap}}
.hl .g{{color:{GOLD}}}
.sub{{left:68px;top:1110px;font-weight:500;font-size:40px;opacity:.82;letter-spacing:-.01em}}
.sub b{{color:{GOLD};font-weight:700}}
.hero{{left:{W - hw + 10}px;top:1120px;width:{hw}px;height:{hh}px;-webkit-mask-image:linear-gradient(180deg,#000 94%,transparent 100%);
  filter:drop-shadow(0 40px 44px rgba(0,25,15,.55))}}
.foot{{left:64px;right:64px;bottom:64px;height:120px;border-top:3px solid rgba(251,243,230,.22);padding-top:28px;height:150px;display:flex;align-items:center;gap:34px}}
.foot img{{height:96px}}
.div{{width:3px;height:92px;background:rgba(11,18,56,.3)}}
.cs{{font-weight:800;font-size:44px;letter-spacing:.14em;color:{GOLD}}}
.url{{font-weight:800;font-size:58px;letter-spacing:-.02em;line-height:1.05}}
.fade{{left:0;right:0;bottom:0;height:330px;background:linear-gradient(180deg,rgba(6,8,25,0) 0%,rgba(6,8,25,.92) 55%,#060819 100%)}}
</style></head><body>
<div class="abs time">12:47 PM</div>
<div class="abs head">{BACK}<div class="av"><img src="assets/logo-mark.png" style="width:66px"></div>
  <div><div class="name">Wystak</div><div class="on">online</div></div>
  <div class="icons">{PHONE}{VIDEO}{DOTS}</div></div>
<div class="b in">So… what’s Wystak?<small>12:47 PM</small></div>
<div class="b out">Soon. Very soon.<small>12:47 PM {TICKS}</small></div>
<div class="abs hl">Every story<br>has a moment.<br><span class="g">This is ours.</span></div>
<img class="abs hero" src="assets/holder-dark.png">
<div class="abs foot" style="justify-content:center"><div class="url" style="font-size:72px">www.wystak.com</div></div>
<div class="grain"></div>
</body></html>'''


if __name__ == "__main__":
    out = HERE / "slides"; out.mkdir(exist_ok=True)
    v2.HERE = HERE
    v2.render(html(), out / "wystak-poster-v4.png")
    print("ok")
