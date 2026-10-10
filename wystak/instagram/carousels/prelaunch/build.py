"""WYSTAK pre-launch teaser: three slides, 1080x1350. A name reveal on a city billboard. No product information.

Slide 1: the billboard in the sky, "Something new is stacking up..." with three unlit cards and a "?" tile.
Slide 2: zoom into the screen, the three cards light up: "...and it has a name."
Slide 3: the reveal: "Say hello to" and the supplied Wystak logo, with "COMING SOON" and the web address.
Type: Poppins. Drawn in code: sky, clouds, buildings, trees, scaffold and screen.
"""
import sys, pathlib
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "_common"))
from common import RESET, render

CSS = RESET + """
@font-face{font-family:P;src:url(assets/poppins-latin-500-normal.woff2);font-weight:500}
@font-face{font-family:P;src:url(assets/poppins-latin-600-normal.woff2);font-weight:600}
@font-face{font-family:P;src:url(assets/poppins-latin-700-normal.woff2);font-weight:700}
body{font-family:P,sans-serif}
.slide{background:linear-gradient(180deg,#2f78d6 0%,#5ea3ea 30%,#a9d0f5 58%,#e3f0fc 82%,#f6fafe 100%)}
.grain{opacity:.10;mix-blend-mode:soft-light}
.vig{box-shadow:inset 0 0 220px rgba(10,30,80,.22)}
"""

# ---------------------------------------------------------------- scenery
CLOUD = """
<svg class="abs" style="left:-120px;top:20px" width="1320" height="760" viewBox="0 0 1320 760">
  <defs>
    <filter id="puff" x="-20%" y="-20%" width="140%" height="140%">
      <feTurbulence type="fractalNoise" baseFrequency=".011" numOctaves="4" seed="9" result="n"/>
      <feDisplacementMap in="SourceGraphic" in2="n" scale="70" xChannelSelector="R" yChannelSelector="G"/><feGaussianBlur stdDeviation="3"/></filter>
    <radialGradient id="cg" cx="40%" cy="25%" r="85%"><stop offset="0" stop-color="#ffffff"/><stop offset=".55" stop-color="#f2f6fc"/><stop offset="1" stop-color="#b9c9e6"/></radialGradient></defs>
  <g filter="url(#puff)" fill="url(#cg)">
    <circle cx="300" cy="360" r="190"/><circle cx="520" cy="300" r="230"/><circle cx="760" cy="270" r="210"/><circle cx="980" cy="330" r="200"/>
    <circle cx="420" cy="470" r="200"/><circle cx="690" cy="470" r="220"/><circle cx="930" cy="480" r="190"/><circle cx="1140" cy="420" r="150"/></g></svg>"""

WINDOWS = lambda w, h, col: (f'<div class="abs" style="left:0;top:0;width:{w}px;height:{h}px;background-image:linear-gradient({col} 0 14px,transparent 14px 46px),'
                             f'linear-gradient(90deg,transparent 0 22px,{col} 22px 40px);background-size:100% 46px,44px 100%;opacity:.55"></div>')

CITY = f"""
  <!-- left curved building -->
  <div class="abs" style="left:-170px;top:760px;width:330px;height:640px;border-radius:0 160px 0 0;background:linear-gradient(90deg,#c9c5c0,#e9e6e1 60%,#d4d0ca);overflow:hidden;box-shadow:inset -18px 0 30px rgba(0,0,0,.12)">{WINDOWS(330, 640, '#5a6577')}</div>
  <!-- right building -->
  <div class="abs" style="left:800px;top:700px;width:340px;height:700px;background:linear-gradient(90deg,#b49a86,#cdb7a2 55%,#a98f7b);overflow:hidden;box-shadow:inset 18px 0 30px rgba(0,0,0,.14)">{WINDOWS(340, 700, '#4c4038')}
    <div class="abs" style="left:0;right:0;top:0;height:34px;background:linear-gradient(180deg,#78907a,#5f7a62)"></div></div>
  <div class="abs" style="left:880px;top:1010px;width:260px;height:12px;background:#6d5d50"></div>
  <div class="abs" style="left:880px;top:1090px;width:260px;height:12px;background:#6d5d50"></div>
  <!-- trees -->
  <div class="abs" style="left:-60px;top:1090px;width:360px;height:300px;border-radius:50%;background:radial-gradient(circle at 40% 30%,#6cbf5c,#2f7a36 70%);filter:blur(1px)"></div>
  <div class="abs" style="left:120px;top:1170px;width:300px;height:260px;border-radius:50%;background:radial-gradient(circle at 40% 30%,#78c864,#2f7a36 70%);filter:blur(1px)"></div>
  <!-- street lamp -->
  <div class="abs" style="left:955px;top:1100px;width:8px;height:260px;background:#e8e8ec"></div>
  <div class="abs" style="left:925px;top:1070px;width:30px;height:30px;border-radius:50%;background:#fff;box-shadow:0 0 14px rgba(255,255,255,.9)"></div>
  <div class="abs" style="left:963px;top:1070px;width:30px;height:30px;border-radius:50%;background:#fff;box-shadow:0 0 14px rgba(255,255,255,.9)"></div>"""

# ---------------------------------------------------------------- the billboard
SX, SY, SW, SH = 300, 170, 480, 800        # screen rectangle (slide-1 coordinates)

SCAFFOLD = f"""
<svg class="abs" style="left:{SX-100}px;top:{SY+10}px" width="120" height="{SH+200}" viewBox="0 0 120 {SH+200}" fill="none" stroke="#2b2f38" stroke-width="5">
  <rect x="6" y="0" width="70" height="{SH+190}"/>
  {''.join(f'<path d="M6 {y} L76 {y+60} M76 {y} L6 {y+60}"/>' for y in range(20, SH+120, 120))}
  {''.join(f'<path d="M6 {y} L76 {y}" stroke-width="4"/>' for y in range(20, SH+180, 60))}
  <path d="M76 80 L112 80 M76 400 L112 400" stroke-width="6"/></svg>"""

LEGS = f"""
<div class="abs" style="left:{SX+110}px;top:{SY+SH}px;width:34px;height:520px;background:linear-gradient(90deg,#1c1f27,#3a3f4b 50%,#1c1f27)"></div>
<div class="abs" style="left:{SX+SW-150}px;top:{SY+SH}px;width:34px;height:520px;background:linear-gradient(90deg,#1c1f27,#3a3f4b 50%,#1c1f27)"></div>
<div class="abs" style="left:{SX+110}px;top:{SY+SH+160}px;width:{SW-260+34}px;height:14px;background:#252932"></div>
<div class="abs" style="left:{SX-10}px;top:{SY+SH+6}px;width:{SW+20}px;height:26px;background:#14161c"></div>"""

CARD = lambda color, rot, x, y, lit: (f'<div class="abs" style="left:{x}px;top:{y}px;width:150px;height:240px;border-radius:30px;transform:rotate({rot}deg);'
    f'background:{color if lit else "linear-gradient(160deg,#2a2d38,#171920)"};'
    f'box-shadow:{"0 0 50px " + color.split(",")[1].strip() + "99, inset 0 0 0 2px rgba(255,255,255,.2)" if lit else "inset 0 0 0 2px rgba(255,255,255,.07)"}"></div>')
NAVY, VIOLET, TEAL = ("linear-gradient(160deg,#2457c0,#0a2860)", "linear-gradient(160deg,#9a52d6,#6b2ba6)", "linear-gradient(160deg,#18b7b7,#06737c)")


def screen(top_text, mid, tile, band_text="COMING<br>SOON", extra=""):
    return f'''
  <div class="abs" style="left:{SX-16}px;top:{SY-16}px;width:{SW+32}px;height:{SH+32}px;background:linear-gradient(135deg,#3a3f4b,#14161c);border-radius:12px;box-shadow:0 30px 60px rgba(0,20,60,.35)"></div>
  <div class="abs" style="left:{SX}px;top:{SY}px;width:{SW}px;height:{SH}px;background:#050507;overflow:hidden;color:#fff">
    <div class="abs" style="left:0;right:0;top:0;bottom:0;background-image:radial-gradient(rgba(255,255,255,.05) 1px,transparent 1.4px);background-size:6px 6px"></div>
    <div class="abs" style="left:30px;right:30px;top:52px;text-align:center;font-weight:600;font-size:42px;line-height:1.22;letter-spacing:-.01em">{top_text}</div>
    {mid}
    <div class="abs" style="left:0;right:0;bottom:0;height:148px;background:#f7f5f1;display:flex;align-items:center;justify-content:space-between;padding:0 34px 0 38px">
      <div style="font-weight:700;font-size:30px;line-height:1.12;letter-spacing:.02em;color:#6b2ba6">{band_text}</div>{tile}</div>{extra}
  </div>
  <div class="abs" style="left:{SX-16}px;top:{SY-16}px;width:{SW+32}px;height:{SH+32}px;border-radius:12px;background:linear-gradient(120deg,rgba(255,255,255,.14),transparent 30%);pointer-events:none"></div>'''


Q_TILE = '<div style="width:84px;height:84px;border-radius:18px;background:#6b2ba6;color:#fff;display:flex;align-items:center;justify-content:center;font-weight:700;font-size:56px">?</div>'
MARK_TILE = '<div style="width:84px;height:84px;border-radius:18px;background:#fff;box-shadow:inset 0 0 0 2px #e6e1f0;display:flex;align-items:center;justify-content:center"><img src="assets/logo-mark.png" style="width:66px"></div>'


def scene(screen_html, zoom=1.0, cx=SX + SW / 2, cy=SY + SH / 2, to_x=540, to_y=675):
    """Whole scene as one group so slides 2 and 3 can zoom into the screen."""
    dx, dy = to_x - cx * zoom, to_y - cy * zoom
    return f'''<div class="abs" style="left:0;top:0;width:1080px;height:1350px;transform-origin:0 0;transform:translate({dx:.1f}px,{dy:.1f}px) scale({zoom})">
    {CLOUD}{CITY}{SCAFFOLD}{LEGS}{screen_html}</div>'''


def page(body):
    return f'''<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head><body>
<div class="slide">{body}<div class="vig"></div><div class="grain"></div></div></body></html>'''


# ---------------------------------------------------------------- the three slides
cards_dim = CARD(NAVY, -14, 60, 330, False) + CARD(VIOLET, 0, 165, 300, False) + CARD(TEAL, 14, 270, 330, False)
cards_lit = CARD(NAVY, -14, 60, 330, True) + CARD(VIOLET, 0, 165, 300, True) + CARD(TEAL, 14, 270, 330, True)
logo_card = ('<div class="abs" style="left:50px;top:210px;width:380px;height:380px;border-radius:30px;background:#fff;transform:rotate(-3deg);'
             'box-shadow:0 0 90px rgba(255,255,255,.35);display:flex;align-items:center;justify-content:center"><img src="assets/logo-full.png" style="width:310px"></div>')

s1 = page(scene(screen("Something new is<br>stacking up…", cards_dim, Q_TILE)))
s2 = page(scene(screen("…and it has<br>a name.", cards_lit, Q_TILE), zoom=1.5, to_y=690))
s3 = page(scene(screen("Say hello to", logo_card, MARK_TILE, band_text="COMING<br>SOON",
                       extra='<div class="abs" style="left:0;right:0;bottom:156px;text-align:center;font-weight:500;font-size:22px;letter-spacing:.14em;color:rgba(255,255,255,.8)">WWW.WYSTAK.COM</div>'),
               zoom=1.5, to_y=690))
slides = [s1, s2, s3]

if __name__ == "__main__":
    render(slides, HERE, "wystak-prelaunch", sys.argv[1:])
