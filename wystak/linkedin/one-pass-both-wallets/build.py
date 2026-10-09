"""WYSTAK LinkedIn post: iPhone or Android, one loyalty pass works on both. One image, 1080x1350.

Style: a dense field of identical dark, embossed wallet passes (soft depth of field), with one glowing Wystak pass
standing out in the middle. Almost no text: a three-line headline with one accented word, and the web address.
Type: Poppins. Palette: charcoal-navy ground, a white and teal glowing pass, teal accent word.
"""
import sys, pathlib
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent.parent / "instagram" / "carousels" / "_common"))
from common import RESET, render

CSS = RESET + """
@font-face{font-family:P;src:url(assets/poppins-latin-500-normal.woff2);font-weight:500}
@font-face{font-family:P;src:url(assets/poppins-latin-600-normal.woff2);font-weight:600}
:root{--aqua:#5fd4cf}
body{font-family:P,sans-serif;color:#fff}
.slide{background:radial-gradient(80% 70% at 50% 38%,#2b2d3a 0%,#1a1b25 55%,#0e0f16 100%)}
.grain{opacity:.14;mix-blend-mode:soft-light}
"""

# ---- the field of dark passes --------------------------------------------------
ROWS = 11
field = ""
y = -150.0
HERO_ROW = 4
hero_geom = None
for r in range(ROWS):
    s = 0.66 + 0.105 * r
    w, h = 176 * s, 262 * s
    pitch = w * 1.13
    off = (r % 2) * pitch / 2
    blur = {0: 2.5, 1: 1.6, 2: 0.8, 3: 0.4, 4: 0.3, 5: 0.9, 6: 1.8, 7: 2.8, 8: 4.2, 9: 5.6, 10: 7}.get(r, 6)
    cards = ""
    x = -pitch + off - ((540 % pitch) if False else 0)
    # centre the middle column on x = 540
    x0 = 540 - w / 2 + off
    k = int(x0 // pitch) + 2
    x = x0 - k * pitch
    while x < 1100:
        shade = 36 + int(6 * ((x * 7 + r * 13) % 5) / 5)
        cards += (f'<div class="abs" style="left:{x:.1f}px;top:0;width:{w:.1f}px;height:{h:.1f}px;border-radius:{w*.2:.1f}px;'
                  f'background:linear-gradient(160deg,rgb({shade+18},{shade+19},{shade+30}),rgb({shade-4},{shade-3},{shade+6}));'
                  f'box-shadow:inset {w*.02:.1f}px {w*.02:.1f}px {w*.04:.1f}px rgba(255,255,255,.10),inset 0 -{h*.06:.1f}px {h*.1:.1f}px rgba(0,0,0,.55),0 {h*.07:.1f}px {h*.12:.1f}px rgba(0,0,0,.65)">'
                  f'<div class="abs" style="left:{w*.5-w*.15:.1f}px;top:{h*.1:.1f}px;width:{w*.3:.1f}px;height:{w*.3:.1f}px;border-radius:50%;'
                  f'background:linear-gradient(160deg,rgb({shade-2},{shade-1},{shade+8}),rgb({shade+14},{shade+15},{shade+26}));'
                  f'box-shadow:inset 0 {w*.02:.1f}px {w*.04:.1f}px rgba(0,0,0,.6),0 1px 0 rgba(255,255,255,.08)"></div></div>')
        x += pitch
    field += f'<div class="abs" style="left:0;top:{y:.1f}px;width:1080px;height:{h:.1f}px;filter:blur({blur}px);z-index:{r * 10}">{cards}</div>'
    if r == HERO_ROW:
        hero_geom = (y, h, s)
    y += h * 0.60

hy, hh, hs = hero_geom
hero_w, hero_h = 250, 372
hero = f'''<div class="abs" style="left:{540 - hero_w/2:.1f}px;top:{hy + hh*0.5 - hero_h*0.5 - 10:.1f}px;width:{hero_w}px;height:{hero_h}px;border-radius:{hero_w*.2:.1f}px;z-index:{HERO_ROW * 10 + 5};
  background:linear-gradient(165deg,#ffffff 0%,#d9f7f5 55%,#8fe3df 100%);
  box-shadow:0 0 120px 30px rgba(95,212,207,.45),0 0 40px rgba(255,255,255,.55),inset 0 -22px 36px rgba(6,115,124,.35);
  display:flex;flex-direction:column;align-items:center;padding-top:30px">
  <div style="width:46px;height:46px;border-radius:50%;background:rgba(6,115,124,.18);box-shadow:inset 0 4px 6px rgba(6,60,70,.35)"></div>
  <img src="assets/logo-mark.png" style="width:168px;margin-top:22px"></div>'''

GLOBE = ('<svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="1.7" stroke-linecap="round" style="opacity:.8">'
         '<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c3 3 3 15 0 18M12 3c-3 3-3 15 0 18"/></svg>')

slides = [f'''<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head><body>
<div class="slide">
  {field}
  {hero}
  <!-- soft shade so the type sits calmly on the field -->
  <div class="abs" style="left:0;right:0;bottom:0;height:560px;background:linear-gradient(180deg,rgba(10,11,18,0) 0%,rgba(10,11,18,.78) 55%,rgba(10,11,18,.92) 100%);z-index:300"></div>
  <svg class="abs" style="left:0;top:0;z-index:310" width="1080" height="1350" viewBox="0 0 1080 1350" fill="none" stroke="rgba(255,255,255,.35)" stroke-width="1.6"><path d="M0 340 A560 560 0 0 0 470 0"/></svg>

  <div class="abs" style="left:96px;top:930px;z-index:320;font-weight:600;font-size:64px;line-height:1.16;letter-spacing:-.015em">
    iPhone or Android.<br>One loyalty pass<br>works on <span style="color:var(--aqua)">both.</span></div>
  <div class="abs" style="left:96px;right:96px;bottom:84px;z-index:320;display:flex;justify-content:space-between;align-items:center;font-weight:500;font-size:26px;opacity:.85">
    <span style="display:flex;align-items:center;gap:12px">{GLOBE}www.wystak.com</span></div>
  <div class="grain"></div>
</div></body></html>''']

if __name__ == "__main__":
    render(slides, HERE, "wystak-linkedin-both-wallets", sys.argv[1:])
