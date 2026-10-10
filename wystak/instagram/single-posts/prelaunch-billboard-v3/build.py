"""WYSTAK pre-launch billboard poster, v3: "Something new is स्टैकिंग अप…" in the user's palette (1080x2100).

Palette: #006199 deep blue, #8ACFF8 sky, #F4EB6C pale yellow, #FFD444 yellow. Bold black outlines frame the two sections.
Upper: the headline (Titan One, the closest free match to Boldum; Baloo 2 ExtraBold for the Devanagari) and the card holder
with the supplied logo, cut out of its white ground (assets/holder-cut.png, made from ../prelaunch-billboard-v2).
Lower: COMING SOON in one corner, www.wystak.com in the other (Poppins). Run: python3 build.py
"""
import sys, pathlib
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "prelaunch-billboard-v2"))
import build as v2
from PIL import Image

W, H = v2.W, v2.H
B = 22                      # black outline
UPPER = 1560

def html():
    hs = Image.open(HERE / "assets" / "holder-cut.png").size
    hw = 1120; hh = round(hs[1] * hw / hs[0])
    return f'''<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{{font-family:TO;src:url(assets/titan-one-latin-400-normal.woff2)}}
@font-face{{font-family:BL;src:url(assets/baloo-2-devanagari-800-normal.woff2);font-weight:800}}
@font-face{{font-family:BL;src:url(assets/baloo-2-latin-800-normal.woff2);font-weight:800}}
@font-face{{font-family:P;src:url(assets/poppins-latin-600-normal.woff2);font-weight:600}}
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:{W}px;height:{H}px;overflow:hidden;background:#000}}
.sec{{position:absolute;left:{B}px;right:{B}px;overflow:hidden}}
.up{{top:{B}px;height:{UPPER - B - B // 2}px;background:radial-gradient(62% 32% at 50% 76%,rgba(255,255,255,.55) 0%,rgba(255,255,255,0) 100%),#8ACFF8}}
.low{{top:{UPPER + B // 2}px;bottom:{B}px;background:#006199}}
.h{{position:absolute;left:0;right:0;top:92px;text-align:center;font-family:TO,sans-serif;font-size:150px;line-height:1.02;color:#006199;white-space:nowrap;letter-spacing:-.01em}}
.hi{{display:block;margin-top:58px;font-family:BL,sans-serif;font-weight:800;font-size:172px;line-height:1.0;color:#FFD444;
  -webkit-text-stroke:14px #006199;paint-order:stroke fill;text-shadow:0 12px 0 #006199}}
.img{{position:absolute;left:{(W - 2 * B - hw) // 2}px;bottom:-4px;width:{hw}px;height:{hh}px;filter:drop-shadow(0 26px 30px rgba(0,60,100,.35))}}
.cs{{position:absolute;left:58px;top:58px;font-family:TO,sans-serif;font-size:104px;line-height:1.0;color:#FFD444}}
.url{{position:absolute;right:58px;bottom:62px;font-family:P,sans-serif;font-weight:600;font-size:62px;color:#F4EB6C;letter-spacing:.01em}}
</style></head><body>
<div class="sec up"><div class="h">Something<br>new is<span class="hi">स्टैकिंग अप…</span></div>
<img class="img" src="assets/holder-cut.png"></div>
<div class="sec low"><div class="cs">COMING<br>SOON</div><div class="url">www.wystak.com</div></div>
</body></html>'''

if __name__ == "__main__":
    out = HERE / "slides"; out.mkdir(exist_ok=True)
    v2.HERE = HERE
    v2.render(html(), out / "wystak-poster-v3.png")
    print("ok")
