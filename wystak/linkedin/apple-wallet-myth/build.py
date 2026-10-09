"""WYSTAK LinkedIn post: the Apple Wallet myth. One image, 1080x1350.

Typography-led: a huge lowercase black headline, one tilted violet label with the answer, a pale lavender
ground and a quiet footer. Type: Inter Black. Nothing else on the page.
"""
import sys, pathlib
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent.parent / "instagram" / "carousels" / "_common"))
from common import RESET, render

CSS = RESET + """
@font-face{font-family:I;src:url(assets/inter-latin-500-normal.woff2);font-weight:500}
@font-face{font-family:I;src:url(assets/inter-latin-600-normal.woff2);font-weight:600}
@font-face{font-family:I;src:url(assets/inter-latin-900-normal.woff2);font-weight:900}
:root{--ink:#0b1530;--violet:#6b2ba6}
body{font-family:I,sans-serif;color:var(--ink)}
.slide{background:radial-gradient(70% 55% at 85% 45%,#e6e1f6 0%,transparent 70%),linear-gradient(160deg,#f0f3fc 0%,#e3e8f7 60%,#dbe1f3 100%)}
.grain{opacity:.05;mix-blend-mode:multiply}
.vig{box-shadow:inset 0 0 180px rgba(70,80,140,.08)}
.h{font-weight:900;letter-spacing:-.045em;word-spacing:.07em;line-height:.99;white-space:nowrap;font-size:140px}
"""

slides = [f'''<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head><body>
<div class="slide">
  <div class="abs" style="left:96px;top:250px">
    <div class="h">“apple</div>
    <div class="h">wallet doesn’t</div>
    <div class="h">work in</div>
    <div class="h">india.”</div>
    <div class="h" style="display:inline-block;margin-top:34px;margin-left:-14px;padding:6px 40px 24px;background:var(--violet);color:#fff;border:5px solid var(--ink);transform:rotate(-1.8deg);transform-origin:0 50%;font-size:126px;letter-spacing:-.04em">that’s a myth.</div>
  </div>
  <div class="abs" style="left:96px;right:96px;bottom:84px;display:flex;justify-content:space-between;align-items:center">
    <img src="assets/logo-wordmark.png" style="height:34px">
    <img src="assets/logo-tagline.png" style="height:17px;opacity:.75"></div>
  <div class="vig"></div><div class="grain"></div>
</div></body></html>''']

if __name__ == "__main__":
    render(slides, HERE, "wystak-linkedin-myth", sys.argv[1:])
