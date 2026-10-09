"""WYSTAK salon post (teal): 5 slides, 1080x1350.

Story: nobody knows when a client last visited. The appointment card's "last visit" is blank; every client has a
hair shade and now a pass; a tap on the desk bell joins; the mirror of polaroids shows who is drifting; a
reserved card on the desk invites the salon to Wystak.
Type: DM Serif Display + Allura script accent word + Poppins. Grounds: teal and blush.
"""
import sys, pathlib
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "_common"))
from common import RESET, qr, nfc, arrow, render

CSS = RESET + """
@font-face{font-family:DS;src:url(assets/dm-serif-display-latin-400-normal.woff2)}
@font-face{font-family:AL;src:url(assets/allura-latin-400-normal.woff2)}
@font-face{font-family:P;src:url(assets/poppins-latin-400-normal.woff2);font-weight:400}
@font-face{font-family:P;src:url(assets/poppins-latin-500-normal.woff2);font-weight:500}
@font-face{font-family:P;src:url(assets/poppins-latin-600-normal.woff2);font-weight:600}
@font-face{font-family:P;src:url(assets/poppins-latin-700-normal.woff2);font-weight:700}
:root{--teal:#06737c;--deep:#04484f;--blush:#f6e8df;--peach:#ffd7c2;--ink:#0a2860;--gold:#e5c58a}
body{font-family:P,sans-serif}
.t{background:radial-gradient(90% 70% at 50% 35%,#13a0a3 0%,#06737c 50%,#04484f 100%);color:#fff}
.b{background:radial-gradient(100% 80% at 50% 30%,#fbf1ea 0%,#f6e8df 60%,#ecd6ca 100%);color:#0f2a30}
.t .grain{opacity:.2;mix-blend-mode:soft-light}
.b .grain{opacity:.16;mix-blend-mode:multiply}
.t .vig{box-shadow:inset 0 0 220px rgba(0,30,35,.5)}
.b .vig{box-shadow:inset 0 0 200px rgba(120,70,50,.16)}
.d{font-family:DS,serif;line-height:1.0;letter-spacing:-.015em;white-space:nowrap}
.s{font-family:AL,cursive;white-space:nowrap;line-height:.9}
.t .s{color:var(--peach)} .b .s{color:var(--teal)}
.sub{font-weight:500;font-size:34px;line-height:1.38}
.t .sub{color:rgba(255,255,255,.86)} .b .sub{color:#2d4a50}
"""

SCISSORS = lambda w, rot: f'''<svg width="{w}" height="{w*1.1:.0f}" viewBox="0 0 200 220" style="transform:rotate({rot}deg);overflow:visible;filter:drop-shadow(8px 14px 10px rgba(0,0,0,.35))">
  <g transform="rotate(-18 100 110)"><path d="M100 118 L62 6 C58 -2 70 -4 76 6 L118 112 Z" fill="#dfe7ea" stroke="#8b9aa0" stroke-width="2.5"/>
  <path d="M100 118 L138 6 C142 -2 130 -4 124 6 L82 112 Z" fill="#cfd9dd" stroke="#8b9aa0" stroke-width="2.5"/></g>
  <circle cx="64" cy="176" r="26" fill="none" stroke="#e5c58a" stroke-width="14"/><circle cx="136" cy="176" r="26" fill="none" stroke="#e5c58a" stroke-width="14"/>
  <path d="M74 152 L96 118 M126 152 L104 118" stroke="#e5c58a" stroke-width="14" stroke-linecap="round"/><circle cx="100" cy="116" r="7" fill="#8b9aa0"/></svg>'''

# icon for the fictional salon (a pair of leaves)
LEAF = lambda s, c="#fff": (f'<svg width="{s}" height="{s}" viewBox="0 0 40 40" fill="none" stroke="{c}" stroke-width="2.6" stroke-linejoin="round" stroke-linecap="round">'
    '<path d="M20 34 C8 30 6 16 12 6 C22 10 26 22 20 34Z"/><path d="M20 34 C32 30 34 18 29 10 C21 13 17 24 20 34Z"/><path d="M20 34 L20 20"/></svg>')


def frame(cls, body):
    return f'''<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head><body>
    <div class="slide {cls}">{body}<div class="vig"></div><div class="grain"></div></div></body></html>'''


slides = []

# 01 cover: an appointment card with the last visit left blank
slides.append(frame("t", f'''
  <div class="abs" style="left:84px;top:150px">
    <div class="d" style="font-size:140px">When did<br>your clients<br>last</div>
    <div class="s" style="font-size:250px;margin-top:-20px;margin-left:10px;transform:rotate(-5deg)">visit?</div>
  </div>
  <div class="sub abs" style="left:610px;top:690px;width:380px;font-size:32px">Most salons find out when a chair goes empty.</div>
  <div class="abs" style="left:300px;top:880px;width:690px;height:420px;background:#fbf4e8;border-radius:14px;transform:rotate(5deg);box-shadow:0 50px 80px -28px rgba(0,25,30,.7);padding:34px 42px;color:#16343a">
    <div style="display:flex;align-items:center;gap:14px;border-bottom:2px solid rgba(22,52,58,.35);padding-bottom:16px">{LEAF(44, "#06737c")}
      <div class="d" style="font-size:42px;letter-spacing:.01em">The Saffron Room</div>
      <div style="margin-left:auto;font-weight:600;font-size:18px;letter-spacing:.16em;opacity:.65">APPOINTMENT CARD</div></div>
    <div style="display:flex;align-items:flex-end;gap:16px;margin-top:34px"><div style="font-weight:600;font-size:24px;letter-spacing:.1em">CLIENT</div><div style="flex:1;border-bottom:2px solid rgba(22,52,58,.5);height:36px"></div></div>
    <div style="display:flex;align-items:flex-end;gap:16px;margin-top:30px"><div style="font-weight:600;font-size:24px;letter-spacing:.1em">LAST VISIT</div>
      <div style="flex:1;border-bottom:2px solid rgba(22,52,58,.5);height:62px;position:relative"><span class="s" style="position:absolute;left:18px;top:-8px;font-size:84px;color:#d3342a">???</span></div></div>
    <div style="display:flex;align-items:flex-end;gap:16px;margin-top:30px"><div style="font-weight:600;font-size:24px;letter-spacing:.1em">NEXT VISIT</div><div style="flex:1;border-bottom:2px solid rgba(22,52,58,.5);height:36px"></div></div>
  </div>
  <div class="abs" style="left:96px;top:1090px;z-index:5">{SCISSORS(190, -22)}</div>
  <div class="abs" style="right:84px;top:76px;display:flex;align-items:center;gap:6px;z-index:6">
    <span class="s" style="font-size:66px;color:#fff">swipe</span>{arrow(130, 60, "M6 36 C36 18 70 50 120 30", "#fff", 5, (120, 30, -22))}</div>'''))

# 02 colour-swatch ring: every client has a shade, and a pass
sw = [("#3b2417", "1.0"), ("#6d4430", "4.3"), ("#b0623a", "6.4"), ("#d79a56", "7.3"), ("#e8c98a", "9.3"), ("#b9aea0", "8.1"), ("#5a2a4d", "3.6")]
def swatch(rot, color, lab, last=False):
    if last:
        inner = f'''<div style="position:absolute;inset:0;border-radius:60px 60px 14px 14px;background:linear-gradient(170deg,#12a3a6,#06737c 60%,#04484f);box-shadow:0 18px 30px -14px rgba(0,0,0,.5),inset 0 0 0 4px rgba(255,255,255,.18)"></div>
        <div style="position:absolute;left:0;right:0;top:70px;text-align:center;color:#fff">{LEAF(56)}</div>
        <div style="position:absolute;left:50%;top:330px;width:400px;margin-left:-200px;transform:rotate(-90deg);text-align:center;color:#fff;font-weight:700;font-size:23px;letter-spacing:.16em;white-space:nowrap">THE SAFFRON ROOM</div>'''
    else:
        inner = f'''<div style="position:absolute;inset:0;border-radius:60px 60px 14px 14px;background:repeating-linear-gradient(94deg,{color} 0 5px,rgba(255,255,255,.14) 5px 7px,{color} 7px 12px),{color};box-shadow:0 18px 30px -14px rgba(60,30,20,.5)"></div>
        <div style="position:absolute;left:0;right:0;bottom:26px;text-align:center;font-weight:700;font-size:26px;color:rgba(255,255,255,.9);letter-spacing:.1em">{lab}</div>'''
    return f'<div class="abs" style="left:350px;top:640px;width:150px;height:640px;transform-origin:50% 94%;transform:rotate({rot}deg)">{inner}</div>'
fan = ''.join(swatch(-66 + i * 21, c, l) for i, (c, l) in enumerate(sw)) + swatch(-66 + 7 * 21, "", "", last=True)
slides.append(frame("b", f'''
  <div class="abs" style="left:84px;top:150px">
    <div class="d" style="font-size:152px">Every client</div>
    <div class="d" style="font-size:152px">has a</div>
    <div class="s" style="font-size:230px;position:absolute;left:420px;top:166px;transform:rotate(-5deg)">shade.</div>
  </div>
  <div class="sub abs" style="left:84px;top:560px;width:560px;font-size:32px">Now every client can carry a pass with the salon's own name on it.</div>
  {fan}
  <div class="abs" style="left:395px;top:1190px;width:60px;height:60px;border-radius:50%;background:radial-gradient(circle at 35% 30%,#fff,#bcb3a9 60%,#8f867c);box-shadow:0 6px 10px rgba(0,0,0,.4);z-index:5"></div>
  <div class="abs" style="left:640px;top:1252px;transform:rotate(-4deg)"><span class="s" style="font-size:80px">the new shade</span></div>'''))

# 03 desk bell: tap to join
slides.append(frame("t", f'''
  <div class="abs" style="left:84px;top:150px">
    <div class="d" style="font-size:190px">Tap the</div>
    <div class="s" style="font-size:330px;margin-top:-34px;margin-left:30px;transform:rotate(-5deg)">bell.</div>
  </div>
  <div class="sub abs" style="left:84px;top:690px;width:560px;font-size:32px">Tap the bell or scan the card at the front desk. A member in seconds, no app.</div>
  <!-- desk -->
  <div class="abs" style="left:-20px;right:-20px;top:1130px;height:300px;background:linear-gradient(180deg,#0a3b42,#04272d);box-shadow:0 -20px 40px rgba(0,0,0,.25)"></div>
  <!-- bell -->
  <div class="abs" style="left:120px;top:880px;width:380px;height:260px;border-radius:190px 190px 14px 14px;background:radial-gradient(120% 140% at 30% 20%,#fff7e0 0%,#e5c58a 38%,#b9894a 78%,#8a6030 100%);box-shadow:0 40px 50px -20px rgba(0,0,0,.6),inset 0 -14px 20px rgba(80,40,10,.35);z-index:3"></div>
  <div class="abs" style="left:278px;top:850px;width:64px;height:44px;border-radius:30px 30px 6px 6px;background:linear-gradient(90deg,#c79b5a,#f6e2b0 50%,#b98a4c);z-index:3"></div>
  <div class="abs" style="left:96px;top:1124px;width:428px;height:46px;border-radius:50%;background:linear-gradient(180deg,#d9b274,#8a6030);box-shadow:0 22px 30px -8px rgba(0,0,0,.6);z-index:3"></div>
  <div class="abs" style="left:230px;top:960px;z-index:4;opacity:.75">{nfc(100, "#7a5424")}</div>
  <!-- waves -->
  <svg class="abs" style="left:380px;top:760px;z-index:6" width="220" height="180" viewBox="0 0 200 160" fill="none" stroke="#ffd7c2" stroke-width="7" stroke-linecap="round"><path d="M40 130 C52 108 70 98 92 102"/><path d="M26 106 C44 72 80 60 112 68"/><path d="M12 82 C36 36 92 20 132 34"/></svg>
  <!-- phone -->
  <div class="abs" style="left:530px;top:900px;width:340px;height:640px;border-radius:56px;padding:12px;background:linear-gradient(145deg,#4a4f5a,#1a1d23 40%,#3a3e47 70%,#15171c);transform:rotate(-16deg);box-shadow:-30px 50px 80px -30px rgba(0,0,0,.7);z-index:5">
    <div style="position:relative;width:100%;height:100%;border-radius:46px;overflow:hidden;background:linear-gradient(180deg,#f2e3da,#e2c9bb)">
      <div style="position:absolute;left:50%;top:16px;width:96px;height:28px;margin-left:-48px;border-radius:14px;background:#000"></div>
      <div style="position:absolute;left:14px;right:14px;top:96px;bottom:14px;border-radius:34px;background:#fff;padding:28px 22px;text-align:center;color:#111">
        <div style="width:92px;height:92px;margin:0 auto;border-radius:24px;background:linear-gradient(160deg,#12a3a6,#06737c);display:flex;align-items:center;justify-content:center">{LEAF(56)}</div>
        <div style="font-weight:700;font-size:25px;margin-top:16px">The Saffron Room</div>
        <div style="font-weight:500;font-size:19px;color:#666;margin-top:4px">Welcome. Join as a member</div>
        <div style="margin-top:28px;height:60px;border-radius:30px;background:#111;color:#fff;display:flex;align-items:center;justify-content:center;font-weight:600;font-size:21px">Add to Wallet</div></div>
    </div></div>
  <!-- scan card -->
  <div class="abs" style="left:810px;top:690px;width:210px;height:270px;border-radius:18px;background:#fff;transform:rotate(7deg);box-shadow:0 30px 40px -18px rgba(0,0,0,.6);padding:20px 20px;text-align:center;color:#0b3b40;z-index:2">
    {qr(140, 11, "#0b3b40")}<div style="font-weight:700;font-size:20px;letter-spacing:.14em;margin-top:12px">SCAN</div></div>'''))

# 04 mirror with polaroids: who is drifting
def polaroid(x, y, rot, ini, col, cap, faded=False):
    op = ".42" if faded else "1"
    return f'''<div class="abs" style="left:{x}px;top:{y}px;width:230px;height:280px;background:#fff;padding:16px 16px 0;transform:rotate({rot}deg);box-shadow:0 24px 30px -14px rgba(60,30,20,.5);opacity:{op};{'filter:grayscale(.9);' if faded else ''}z-index:6">
      <div style="height:182px;background:{col};display:flex;align-items:center;justify-content:center"><div style="width:96px;height:96px;border-radius:50%;background:rgba(255,255,255,.35);display:flex;align-items:center;justify-content:center;color:#fff;font-family:DS;font-size:56px">{ini}</div></div>
      <div class="s" style="font-size:46px;color:#0f2a30;text-align:center;margin-top:12px;line-height:1">{cap}</div></div>'''
slides.append(frame("b", f'''
  <div class="abs" style="left:84px;top:150px">
    <div class="d" style="font-size:150px">See who's</div>
    <div class="s" style="font-size:300px;margin-top:-30px;margin-left:20px;transform:rotate(-5deg)">drifting.</div>
  </div>
  <!-- mirror -->
  <div class="abs" style="left:150px;top:540px;width:780px;height:860px;border-radius:50%;background:linear-gradient(150deg,#e6c98f,#b88a4a 55%,#e9d2a2);box-shadow:0 60px 90px -30px rgba(60,30,20,.55);padding:26px">
    <div style="width:100%;height:100%;border-radius:50%;background:radial-gradient(120% 90% at 30% 20%,#ffffff 0%,#cfe6e6 35%,#9cc5c6 100%);box-shadow:inset 0 0 60px rgba(0,60,70,.35);position:relative;overflow:hidden">
      <div class="abs" style="left:-10%;top:10%;width:70%;height:30%;background:linear-gradient(100deg,rgba(255,255,255,.7),rgba(255,255,255,0));transform:rotate(-24deg)"></div>
      <div class="abs" style="left:-5%;top:34%;width:50%;height:12%;background:linear-gradient(100deg,rgba(255,255,255,.5),rgba(255,255,255,0));transform:rotate(-24deg)"></div></div></div>
  {polaroid(190, 640, -9, "A", "#d28a63", "3 days ago")}
  {polaroid(700, 650, 8, "M", "#4e9aa0", "yesterday")}
  {polaroid(160, 960, 6, "R", "#8a6ab0", "6 days ago")}
  {polaroid(700, 990, -7, "T", "#c7a15a", "2 days ago")}
  {polaroid(430, 830, 2, "K", "#8aa0a8", "41 days ago", faded=True)}
  <svg class="abs" style="left:380px;top:800px;z-index:7" width="320" height="340" viewBox="0 0 320 340" fill="none" stroke="#d3342a" stroke-width="7" stroke-linecap="round"><path d="M70 60 C150 10 280 30 296 150 C310 260 230 330 130 322 C40 314 6 220 20 140 C28 100 60 70 120 50"/></svg>'''))

# 05 reserved card on the front desk
slides.append(frame("t", f'''
  <div class="abs" style="left:84px;top:150px">
    <div class="d" style="font-size:128px">Reserve a</div>
    <div class="d" style="font-size:128px">spot in every</div>
    <div class="s" style="font-size:230px;position:absolute;left:330px;top:310px;transform:rotate(-5deg)">wallet.</div>
  </div>
  <div class="abs" style="left:-20px;right:-20px;top:1060px;height:400px;background:linear-gradient(180deg,#0a3b42,#04272d)"></div>
  <!-- reserved tent card -->
  <div class="abs" style="left:190px;top:700px;width:700px;height:480px;transform:rotate(-3deg);filter:drop-shadow(0 50px 40px rgba(0,20,25,.65))">
    <div style="position:absolute;inset:0 0 70px 0;background:linear-gradient(180deg,#fbf4e8,#efe3d2);border-radius:10px;text-align:center;padding-top:34px;color:#16343a">
      <div class="d" style="font-size:100px;letter-spacing:.06em">RESERVED</div>
      <div style="width:120px;height:3px;background:var(--teal);margin:10px auto 0"></div>
      <img src="assets/logo-full.png" style="width:240px;margin-top:20px"></div>
    <div style="position:absolute;left:0;right:0;bottom:0;height:70px;background:linear-gradient(180deg,#d9ccb8,#bfae93);transform:perspective(300px) rotateX(-18deg);transform-origin:50% 0;border-radius:0 0 10px 10px"></div></div>
  <div class="abs" style="left:770px;top:1050px;z-index:5">{SCISSORS(140, 28)}</div>
  <div class="sub abs" style="left:84px;top:1210px;width:600px;font-size:32px;z-index:6">Bring Wystak to the front desk.<br>DM us <b style="color:var(--peach)">“STACK”</b>.</div>'''))

if __name__ == "__main__":
    render(slides, HERE, "wystak-salon", sys.argv[1:])
