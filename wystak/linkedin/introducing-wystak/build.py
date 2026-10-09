"""WYSTAK LinkedIn post: Introducing Wystak. One image, 1080x1350.

Clean light ground with blueprint hairlines, one big headline with a single highlighted word, and one hero
object: a row of wallet passes receding in perspective, with a Wystak pass (Bean Theory) at the front.
Type: Plus Jakarta Sans. Light, restrained, lots of space.
"""
import sys, pathlib
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent.parent / "instagram" / "carousels" / "_common"))
from common import RESET, render

CSS = RESET + """
@font-face{font-family:J;src:url(assets/plus-jakarta-sans-latin-300-normal.woff2);font-weight:300}
@font-face{font-family:J;src:url(assets/plus-jakarta-sans-latin-500-normal.woff2);font-weight:500}
@font-face{font-family:J;src:url(assets/plus-jakarta-sans-latin-600-normal.woff2);font-weight:600}
@font-face{font-family:J;src:url(assets/plus-jakarta-sans-latin-800-normal.woff2);font-weight:800}
@font-face{font-family:J;src:url(assets/plus-jakarta-sans-latin-300-italic.woff2);font-weight:300;font-style:italic}
@font-face{font-family:J;src:url(assets/plus-jakarta-sans-latin-600-italic.woff2);font-weight:600;font-style:italic}
:root{--ink:#0b1530;--violet:#6b2ba6;--tint:#ece2f8;--navy:#0a2860;--teal:#06737c;--line:#d7def0}
body{font-family:J,sans-serif;color:var(--ink)}
.slide{background:radial-gradient(120% 90% at 50% 20%,#ffffff 0%,#f6f8fd 55%,#eef2fa 100%)}
.grain{opacity:.06;mix-blend-mode:multiply}
.vig{box-shadow:inset 0 0 160px rgba(60,70,120,.07)}
.h{font-weight:800;letter-spacing:-.032em;line-height:.98;white-space:nowrap}
"""

CRANE_FREE_BEAN = ('<svg width="30" height="30" viewBox="0 0 34 34" fill="none" stroke="#fff" stroke-width="2.6" stroke-linecap="round">'
                   '<g transform="rotate(35 17 17)"><ellipse cx="17" cy="17" rx="9.5" ry="14"/><path d="M17 3.5 C11 11 23 23 17 30.5"/></g></svg>')


def generic_pass(label, glyph):
    return f'''<div style="width:100%;height:100%;border-radius:30px;background:linear-gradient(160deg,#ffffff,#f1f4fb);box-shadow:inset 0 0 0 2px rgba(120,135,190,.22);padding:28px 26px;position:relative;overflow:hidden">
      <div style="font-weight:600;font-size:15px;letter-spacing:.18em;color:#8a94b4">{label}</div>
      <div style="margin-top:22px;width:46px;height:46px;border-radius:14px;background:#e6ebf7;display:flex;align-items:center;justify-content:center">{glyph}</div>
      <div style="position:absolute;left:26px;right:26px;bottom:34px;height:6px;border-radius:3px;background:#e3e8f5"></div>
      <div style="position:absolute;left:26px;width:46%;bottom:54px;height:6px;border-radius:3px;background:#e3e8f5"></div></div>'''


G = lambda d: f'<svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="#8a94b4" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">{d}</svg>'
GLYPHS = [G('<path d="M3 12 L21 5 L16 21 L11 14 Z"/>'), G('<rect x="4" y="6" width="16" height="12" rx="2"/><path d="M4 11h16"/>'),
          G('<path d="M5 8h14l-1 12H6z"/><path d="M9 8a3 3 0 0 1 6 0"/>'), G('<circle cx="12" cy="12" r="8"/><path d="M12 7v5l3 2"/>'),
          G('<path d="M4 15l2-6h12l2 6v3H4z"/><circle cx="8" cy="18" r="1.5"/><circle cx="16" cy="18" r="1.5"/>')]
LABELS = ["BOARDING PASS", "BANK CARD", "GIFT CARD", "EVENT TICKET", "METRO CARD", "MEMBERSHIP", "COUPON", "TICKET", "PASS"]

STACK = [  # back to front: (label, background, text colour, glyph)
    ("BOARDING PASS", "linear-gradient(160deg,#3a4a73,#27345a)", "#fff", GLYPHS[0]),
    ("EVENT TICKET", "linear-gradient(160deg,#9a80c4,#7d63aa)", "#fff", GLYPHS[3]),
    ("BANK CARD", "linear-gradient(160deg,#eceff6,#dde2ee)", "#2b3552", GLYPHS[1]),
    ("GIFT CARD", "linear-gradient(160deg,#f1e6d4,#e4d3b8)", "#4a3a22", GLYPHS[2]),
]
TOP0, STEP = 742, 56
cards = ""
for i, (label, bg, fg, glyph) in enumerate(STACK):
    y = TOP0 + i * STEP
    g = glyph.replace("#8a94b4", fg)
    cards += f'''<div class="abs" style="left:96px;top:{y}px;width:888px;height:274px;border-radius:36px;background:{bg};color:{fg};
      box-shadow:0 -14px 34px -10px rgba(30,40,90,.22),inset 0 0 0 2px rgba(255,255,255,.18);padding:22px 40px;z-index:{i + 1}">
      <div style="display:flex;justify-content:space-between;align-items:center;font-weight:600;font-size:20px;letter-spacing:.2em;opacity:.92"><span>{label}</span>{g}</div></div>'''
FY = TOP0 + len(STACK) * STEP
cards += f'''<div class="abs" style="left:96px;top:{FY}px;width:888px;height:274px;border-radius:36px;overflow:hidden;color:#fff;
  background:radial-gradient(90% 140% at 12% 0%,#27c4c4 0%,#0e9a9f 38%,#06737c 70%,#04484f 100%);
  box-shadow:0 -16px 40px -10px rgba(6,80,90,.38),0 44px 64px -26px rgba(6,60,70,.55),inset 0 0 0 2px rgba(255,255,255,.22);z-index:9">
  <!-- watermark bean and arcs -->
  <svg class="abs" style="right:-30px;top:-70px" width="420" height="420" viewBox="0 0 34 34" fill="none" stroke="#fff" stroke-opacity=".10" stroke-width=".7" stroke-linecap="round"><g transform="rotate(35 17 17)"><ellipse cx="17" cy="17" rx="9.5" ry="14"/><path d="M17 3.5 C11 11 23 23 17 30.5"/></g></svg>
  <svg class="abs" style="left:0;top:0" width="888" height="274" viewBox="0 0 888 274" fill="none" stroke="#fff" stroke-opacity=".09" stroke-width="1.6"><circle cx="760" cy="300" r="190"/><circle cx="760" cy="300" r="250"/><circle cx="760" cy="300" r="310"/></svg>
  <div class="abs" style="left:0;top:0;right:0;height:120px;background:linear-gradient(180deg,rgba(255,255,255,.14),transparent)"></div>
  <div class="abs" style="left:40px;right:40px;top:26px;display:flex;justify-content:space-between;align-items:center">
    <div style="display:flex;align-items:center;gap:14px;font-weight:600;font-size:21px;letter-spacing:.18em"><span style="width:48px;height:48px;border-radius:15px;background:rgba(255,255,255,.18);display:flex;align-items:center;justify-content:center">{CRANE_FREE_BEAN}</span>BEAN THEORY</div>
    <div style="height:38px;padding:0 18px;border-radius:19px;border:1.5px solid rgba(255,255,255,.5);display:flex;align-items:center;font-weight:600;font-size:15px;letter-spacing:.22em">MEMBER</div></div>
  <div class="abs" style="left:40px;top:112px">
    <div style="font-weight:600;font-size:15px;letter-spacing:.24em;opacity:.78">POINTS</div>
    <div style="font-weight:800;font-size:72px;letter-spacing:-.035em;line-height:1;margin-top:4px;white-space:nowrap">132<span style="font-weight:300;opacity:.7;font-size:46px"> / 150</span></div></div>
  <div class="abs" style="left:40px;bottom:30px;width:360px;height:10px;border-radius:5px;background:rgba(255,255,255,.22)"><div style="width:88%;height:100%;border-radius:5px;background:#fff"></div></div>
  <div class="abs" style="right:40px;bottom:26px;height:62px;padding:0 24px 0 18px;border-radius:31px;background:rgba(255,255,255,.96);color:#06545b;display:flex;align-items:center;gap:12px;font-weight:700;font-size:23px;box-shadow:0 12px 24px -10px rgba(0,40,45,.5)">
    <svg width="30" height="30" viewBox="0 0 24 24" fill="none" stroke="#06737c" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="9" width="18" height="12" rx="2"/><path d="M12 9v12M3 13h18"/><path d="M12 9C9 9 7 7.5 7.5 6s3 0 4.5 3C13.500 6 16 4.500 16.500 6S15 9 12 9z"/></svg>200 cashback points</div></div>'''

slides = []
slides.append(f'''<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head><body>
<div class="slide">
  <!-- blueprint hairlines -->
  <svg class="abs" style="left:0;top:0" width="1080" height="1350" viewBox="0 0 1080 1350" fill="none" stroke="#d7def0" stroke-width="1.6">
    <line x1="96" y1="0" x2="96" y2="1350"/><line x1="984" y1="0" x2="984" y2="1350"/>
    <line x1="0" y1="168" x2="1080" y2="168"/>
    <path d="M520 0 A560 560 0 0 0 1080 560" stroke="#cfd8f0"/><path d="M0 760 A520 520 0 0 1 520 1350" stroke="#cfd8f0"/>
  </svg>
  <svg class="abs" style="left:0;top:0" width="1080" height="1350" viewBox="0 0 1080 1350">
    <circle cx="96" cy="168" r="7" fill="#6b2ba6"/><circle cx="984" cy="168" r="7" fill="#6b2ba6"/></svg>

  <!-- header -->
  <img class="abs" src="assets/logo-wordmark.png" style="left:96px;top:76px;height:38px">
  <div class="abs" style="right:96px;top:68px;height:56px;padding:0 26px;border-radius:28px;border:2px solid #cdbcea;background:rgba(255,255,255,.7);display:flex;align-items:center;gap:14px;font-weight:600;font-size:19px;letter-spacing:.2em;color:#4a2a78">
    <span style="width:14px;height:14px;border-radius:50%;background:#6b2ba6"></span>INTRODUCING</div>

  <!-- headline -->
  <div class="abs" style="left:96px;top:208px">
    <div class="h" style="font-size:104px">every phone</div>
    <div class="h" style="font-size:104px;margin-top:6px">already has a</div>
    <div class="h" style="font-size:104px;margin-top:16px;display:inline-block;padding:6px 26px 14px;border-radius:22px;background:var(--tint);color:var(--violet);margin-left:-26px">WALLET.</div>
  </div>
  <div class="abs" style="left:96px;top:626px;font-weight:300;font-size:46px;letter-spacing:-.02em;line-height:1.2">is your <b style="font-weight:600;font-style:italic;color:var(--violet)">business</b> in it?</div>

  <!-- hero: the wallet stack -->
  {cards}
  <div class="abs" style="left:0;right:0;top:1276px;display:flex;justify-content:center"><img src="assets/logo-tagline.png" style="width:460px;opacity:.8"></div>

  <div class="vig"></div><div class="grain"></div>
</div></body></html>''')

if __name__ == "__main__":
    render(slides, HERE, "wystak-linkedin-introducing", sys.argv[1:])
