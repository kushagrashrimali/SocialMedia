"""WYSTAK LinkedIn post: Apple Pay is not live, wallet passes still work. One image, 1080x1350.

Style: a soft gradient ground with a faint grid, a bold two-line headline with small corner text, and a hero of
dark wallet passes standing in a receding row, with one white Wystak pass stepping out of the line.
Type: Inter. Palette: Wystak violet and navy, a white pass with a teal edge.
"""
import sys, pathlib
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent.parent / "instagram" / "carousels" / "_common"))
from common import RESET, render

CSS = RESET + """
@font-face{font-family:I;src:url(assets/inter-latin-500-normal.woff2);font-weight:500}
@font-face{font-family:I;src:url(assets/inter-latin-600-normal.woff2);font-weight:600}
@font-face{font-family:I;src:url(assets/inter-latin-900-normal.woff2);font-weight:900}
:root{--ink:#26104f;--violet:#6b2ba6}
body{font-family:I,sans-serif;color:var(--ink)}
.slide{background:
  radial-gradient(60% 40% at 96% 60%,rgba(255,255,255,.85) 0%,rgba(255,226,250,.55) 38%,transparent 72%),
  linear-gradient(180deg,#f4ebff 0%,#e6d4fc 26%,#cfb0f6 46%,#a574de 62%,#5a2a92 78%,#1f0f45 100%)}
.gridbg{position:absolute;inset:0;background-image:linear-gradient(rgba(107,43,166,.13) 1.5px,transparent 1.5px),linear-gradient(90deg,rgba(107,43,166,.13) 1.5px,transparent 1.5px);background-size:28px 28px;-webkit-mask-image:linear-gradient(180deg,#000 0%,#000 38%,transparent 62%)}
.grain{opacity:.07;mix-blend-mode:multiply}
.vig{box-shadow:inset 0 0 160px rgba(30,10,70,.18)}
"""

# --- row of dark passes, receding to a vanishing point on the right -------------
VPX, VPY = 1040, 770          # vanishing point
P0X, P0Y = 40, 930            # centre of the nearest pass
W0, H0 = 330, 600             # nearest pass size
K = 0.865                     # scale step
N = 17
row = ""
for i in range(N):
    s = K ** i
    cx = VPX + (P0X - VPX) * s
    cy = VPY + (P0Y - VPY) * s
    w, h = W0 * s, H0 * s
    edge = max(2, 18 * s)
    tone = int(34 + 22 * (1 - s))           # farther passes slightly lighter
    row += (f'<div class="abs" style="left:{cx - w/2:.1f}px;top:{cy - h/2:.1f}px;width:{w:.1f}px;height:{h:.1f}px;border-radius:{44*s:.1f}px;'
            f'background:linear-gradient(160deg,rgb({tone+20},{tone+22},{tone+40}),rgb({tone-6},{tone-4},{tone+10}));'
            f'box-shadow:{edge:.1f}px 0 0 #8d94b3,{edge+3*s:.1f}px 0 0 #5d6486,{edge*1.6:.1f}px {22*s:.1f}px {40*s:.1f}px rgba(8,4,30,.55);'
            f'z-index:{100 - i}"></div>')

hero = f'''<div class="abs" style="left:330px;top:690px;width:370px;height:520px;border-radius:54px;transform:rotate(-8deg);transform-origin:50% 100%;z-index:200;
  background:linear-gradient(165deg,#ffffff 0%,#f1ecfb 100%);
  box-shadow:22px 0 0 #12a3a6,25px 0 0 #06737c,30px 36px 70px rgba(6,60,70,.55),0 0 90px rgba(95,212,207,.55);
  display:flex;flex-direction:column;align-items:center;padding-top:52px">
  <img src="assets/logo-full.png" style="width:270px">
  <div style="margin-top:26px;font-weight:600;font-size:19px;letter-spacing:.24em;color:#6b6f90">LOYALTY PASS</div>
  <div style="position:absolute;left:44px;right:44px;bottom:46px;height:8px;border-radius:4px;background:#e4def2"></div>
  <div style="position:absolute;left:44px;width:46%;bottom:70px;height:8px;border-radius:4px;background:#e4def2"></div></div>'''

GLOBE = ('<svg width="30" height="30" viewBox="0 0 24 24" fill="none" stroke="#5fd4cf" stroke-width="1.8" stroke-linecap="round">'
         '<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c3 3 3 15 0 18M12 3c-3 3-3 15 0 18"/></svg>')

slides = [f'''<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head><body>
<div class="slide">
  <div class="gridbg"></div>

  <!-- header -->
  <div class="abs" style="left:96px;top:92px;font-weight:600;font-size:23px;line-height:1.3;color:var(--ink)">Loyalty passes for<br>India’s small merchants</div>
  <img class="abs" src="assets/logo-wordmark.png" style="right:96px;top:98px;height:36px">

  <!-- headline -->
  <div class="abs" style="left:96px;top:210px;font-weight:900;letter-spacing:-.032em;word-spacing:.08em;line-height:1.04;color:var(--ink);font-size:82px;white-space:nowrap">
    Apple Pay isn’t live.<br>Passes still work.</div>
  <div class="abs" style="left:96px;top:420px;width:560px;font-weight:500;font-size:31px;line-height:1.35;color:#3e2a72">Apple Wallet and Google Wallet. One loyalty pass for every phone.</div>

  <!-- hero -->
  {row}
  {hero}

  <!-- footer -->
  <div class="abs" style="left:96px;bottom:70px;display:flex;align-items:center;gap:14px;font-weight:600;font-size:28px;color:#fff;z-index:300">{GLOBE}www.wystak.com</div>
  <div class="abs" style="right:96px;bottom:78px;z-index:300"><img src="assets/logo-tagline.png" style="height:16px;filter:brightness(0) invert(1);opacity:.85"></div>
  <div class="vig"></div><div class="grain"></div>
</div></body></html>''']

if __name__ == "__main__":
    render(slides, HERE, "wystak-linkedin-myth", sys.argv[1:])
