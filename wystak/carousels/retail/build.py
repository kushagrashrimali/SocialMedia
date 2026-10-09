"""WYSTAK retail post (navy): 5 slides, 1080x1350.

Story: the billing counter. Shoppers refuse to give a phone number; the shop knows what sold but not who
bought it; a tap at the card machine fixes it; the owner sees who stopped; Wystak goes in the shopping bag.
Type: Archivo Black capitals + Permanent Marker accent word + Poppins. Grounds: navy and cream.
Objects: speech bubbles with a sticky note, a swing tag, a card machine, a khata ledger with a rubber stamp, a kraft bag.
"""
import sys, pathlib
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "_common"))
from common import RESET, qr, nfc, arrow, render

CSS = RESET + """
@font-face{font-family:AB;src:url(assets/archivo-black-latin-400-normal.woff2)}
@font-face{font-family:PM;src:url(assets/permanent-marker-latin-400-normal.woff2)}
@font-face{font-family:P;src:url(assets/poppins-latin-400-normal.woff2);font-weight:400}
@font-face{font-family:P;src:url(assets/poppins-latin-500-normal.woff2);font-weight:500}
@font-face{font-family:P;src:url(assets/poppins-latin-600-normal.woff2);font-weight:600}
@font-face{font-family:P;src:url(assets/poppins-latin-700-normal.woff2);font-weight:700}
:root{--navy:#0a2860;--aqua:#5fd4cf;--red:#e0382e;--ink:#101a33;--cream:#f2ede1;--kraft:#cfa970}
body{font-family:P,sans-serif}
.n{background:radial-gradient(90% 70% at 50% 35%,#17408a 0%,#0a2860 52%,#061a42 100%);color:#fff}
.c{background:var(--cream);color:var(--ink);background-image:radial-gradient(rgba(16,26,51,.13) 2.2px,transparent 2.6px);background-size:46px 46px}
.n .grain{opacity:.22;mix-blend-mode:soft-light}
.c .grain{opacity:.18;mix-blend-mode:multiply}
.n .vig{box-shadow:inset 0 0 220px rgba(0,10,40,.5)}
.c .vig{box-shadow:inset 0 0 200px rgba(90,70,40,.18)}
.d{font-family:AB,sans-serif;text-transform:uppercase;line-height:1.04;letter-spacing:-.012em;white-space:nowrap}
.s{font-family:PM,cursive;white-space:nowrap;line-height:1}
.n .s{color:var(--aqua)} .c .s{color:var(--red)}
.sub{font-weight:500;font-size:34px;line-height:1.35}
.n .sub{color:rgba(255,255,255,.82)} .c .sub{color:#3d4560}
"""

# icon for the fictional shop (a marigold)
FLOWER = lambda s, c="#fff": (f'<svg width="{s}" height="{s}" viewBox="0 0 40 40" fill="none" stroke="{c}" stroke-width="2.4" stroke-linejoin="round">'
    + ''.join(f'<ellipse cx="20" cy="9.5" rx="4.6" ry="7.5" transform="rotate({a} 20 20)"/>' for a in range(0, 360, 60))
    + '<circle cx="20" cy="20" r="3.2"/></svg>')


def frame(cls, body):
    return f'''<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head><body>
    <div class="slide {cls}">{body}<div class="vig"></div><div class="grain"></div></div></body></html>'''


slides = []

# 01 cover: the billing-counter ask
slides.append(frame("n", f'''
  <div class="abs" style="left:84px;top:170px">
    <div class="d" style="font-size:98px">Nobody wants<br>to say their<br>number at</div>
    <div class="s" style="font-size:210px;margin-top:-6px;margin-left:6px;transform:rotate(-4deg)">billing.</div>
  </div>
  <!-- sticky note taped to the screen -->
  <div class="abs" style="left:84px;top:830px;width:400px;height:400px;background:linear-gradient(160deg,#ffe36a,#f6c92f);transform:rotate(-6deg);box-shadow:0 36px 50px -22px rgba(0,0,0,.6);padding:42px 36px">
    <div class="abs" style="left:150px;top:-26px;width:110px;height:46px;background:rgba(255,255,255,.55);transform:rotate(3deg)"></div>
    <div class="s" style="color:#3a2c00;font-size:62px;line-height:1.1;white-space:normal">ASK FOR<br>PHONE<br>NUMBER!!</div>
    <div style="position:absolute;right:34px;bottom:24px;font-weight:600;font-size:22px;color:#6a5200">- the owner</div>
  </div>
  <!-- the ask -->
  <div class="abs" style="left:520px;top:820px;width:470px;padding:34px 38px;border-radius:44px 44px 44px 8px;background:#fff;color:#101a33;box-shadow:0 30px 50px -20px rgba(0,0,0,.55);transform:rotate(2deg)">
    <div style="font-weight:700;font-size:42px;line-height:1.2">Phone number, please?</div></div>
  <!-- the answer -->
  <div class="abs" style="left:610px;top:1060px;width:400px;padding:30px 36px;border-radius:44px 44px 8px 44px;background:var(--aqua);color:#06223f;box-shadow:0 30px 50px -20px rgba(0,0,0,.55);transform:rotate(-2deg)">
    <div style="font-weight:700;font-size:40px;line-height:1.2">No, it's okay.</div></div>
  <div class="abs" style="right:84px;top:76px;display:flex;align-items:center;gap:6px;z-index:6">
    <span class="s" style="font-size:44px;color:#fff">swipe</span>{arrow(130, 60, "M6 36 C36 18 70 50 120 30", "#fff", 5, (120, 30, -22))}</div>'''))

# 02 swing tag
slides.append(frame("c", f'''
  <div class="abs" style="left:84px;top:130px">
    <div class="d" style="font-size:96px">You know<br>what sold.</div>
    <div class="d" style="font-size:96px;margin-top:14px">Who bought<br>it?</div>
    <div class="s" style="font-size:140px;margin-top:6px;margin-left:10px;transform:rotate(-5deg)">no idea.</div>
  </div>
  <div class="sub abs" style="left:84px;top:1130px;width:380px;font-size:30px">The bill records the sale. Nothing records the shopper.</div>
  <svg class="abs" style="left:790px;top:-20px;z-index:3" width="200" height="800" viewBox="0 0 200 800" fill="none" stroke="#7a5a2a" stroke-width="7" stroke-linecap="round"><path d="M100 0 C120 260 50 540 70 790"/></svg>
  <div class="abs" style="left:640px;top:690px;width:400px;height:680px;transform:rotate(5deg);transform-origin:50% 8%;filter:drop-shadow(0 40px 36px rgba(40,25,5,.45))">
    <div style="position:absolute;inset:0;background:var(--kraft);clip-path:polygon(18% 0,82% 0,100% 11%,100% 100%,0 100%,0 11%);padding:140px 30px 30px;color:#2a1c08">
      <div class="abs" style="left:50%;top:44px;width:54px;height:54px;margin-left:-27px;border-radius:50%;background:#f2ede1;box-shadow:inset 0 5px 8px rgba(0,0,0,.35)"></div>
      <div style="text-align:center;font-weight:700;font-size:21px;letter-spacing:.2em">MARIGOLD LANE</div>
      <div style="text-align:center;font-weight:600;font-size:24px;margin-top:22px;letter-spacing:.06em">LINEN SHIRT · SKY BLUE</div>
      <div class="d" style="text-align:center;font-size:80px;margin-top:20px;letter-spacing:0">₹1,299</div>
      <div style="height:84px;margin:24px 16px 0;background:repeating-linear-gradient(90deg,#2a1c08 0 4px,transparent 4px 9px,#2a1c08 9px 11px,transparent 11px 18px,#2a1c08 18px 24px,transparent 24px 28px)"></div>
      <div style="margin:30px 14px 0;border-top:3px dashed rgba(42,28,8,.55);padding-top:26px">
        <div style="font-weight:600;font-size:23px;letter-spacing:.12em">SOLD TO:</div>
        <div class="s" style="font-size:96px;color:var(--red);margin-top:8px;transform:rotate(-6deg)">???</div></div>
    </div>
  </div>'''))

# 03 card machine tap
slides.append(frame("n", f'''
  <div class="abs" style="left:84px;top:130px">
    <div class="d" style="font-size:132px">Tap at</div>
    <div class="d" style="font-size:132px;margin-top:6px">billing.</div>
    <div class="s" style="font-size:170px;margin-top:-4px;margin-left:8px;transform:rotate(-5deg)">done.</div>
  </div>
  <div class="sub abs" style="left:84px;top:590px;width:700px;font-size:32px">Tap or scan while the bill prints. The pass lands in Apple Wallet or Google Wallet. No app.</div>
  <!-- card machine -->
  <div class="abs" style="left:110px;top:830px;width:430px;height:700px;border-radius:44px;background:linear-gradient(160deg,#2b3550,#10162a);transform:rotate(-8deg);box-shadow:0 60px 90px -30px rgba(0,0,0,.7),inset 0 0 0 3px rgba(255,255,255,.07);padding:34px 34px">
    <div style="height:330px;border-radius:24px;background:linear-gradient(180deg,#e9fbf9,#bfeae6);color:#06323a;text-align:center;padding-top:26px;box-shadow:inset 0 0 0 4px #0b1224">
      <div style="display:flex;gap:10px;align-items:center;justify-content:center;font-weight:700;font-size:23px;letter-spacing:.1em">{FLOWER(34, "#06323a")}MARIGOLD LANE</div>
      <div style="display:flex;justify-content:center;margin-top:14px">{nfc(118, "#06323a")}</div>
      <div style="font-weight:700;font-size:30px;margin-top:6px">Tap to join</div>
      <div style="font-weight:500;font-size:19px;opacity:.75;margin-top:2px">Apple Wallet · Google Wallet</div></div>
    <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:16px;margin-top:30px">
      {''.join('<div style="height:56px;border-radius:14px;background:#1f2944;box-shadow:inset 0 -4px 0 rgba(0,0,0,.35)"></div>' for _ in range(9))}</div>
  </div>
  <!-- phone -->
  <svg class="abs" style="left:560px;top:700px;z-index:5" width="200" height="160" viewBox="0 0 200 160" fill="none" stroke="#5fd4cf" stroke-width="7" stroke-linecap="round"><path d="M40 130 C52 108 70 98 92 102"/><path d="M26 106 C44 72 80 60 112 68"/><path d="M12 82 C36 36 92 20 132 34"/></svg>
  <div class="abs" style="left:560px;top:880px;width:340px;height:700px;border-radius:56px;padding:12px;background:linear-gradient(145deg,#4a4f5a,#1a1d23 40%,#3a3e47 70%,#15171c);transform:rotate(-14deg);box-shadow:-30px 50px 80px -30px rgba(0,0,0,.7);z-index:4">
    <div style="position:relative;width:100%;height:100%;border-radius:46px;overflow:hidden;background:linear-gradient(180deg,#e4dcf3,#c1b4de)">
      <div style="position:absolute;left:50%;top:16px;width:96px;height:28px;margin-left:-48px;border-radius:14px;background:#000"></div>
      <div style="position:absolute;left:14px;right:14px;top:100px;bottom:14px;border-radius:34px;background:#fff;padding:30px 24px;text-align:center;color:#111">
        <div style="width:96px;height:96px;margin:0 auto;border-radius:24px;background:#0a2860;display:flex;align-items:center;justify-content:center">{FLOWER(60, "#ffd24a")}</div>
        <div style="font-weight:700;font-size:26px;margin-top:18px">Marigold Lane</div>
        <div style="font-weight:500;font-size:19px;color:#666;margin-top:4px">Member pass</div>
        <div style="margin-top:34px;height:62px;border-radius:31px;background:#111;color:#fff;display:flex;align-items:center;justify-content:center;font-weight:600;font-size:21px">Add to Wallet</div></div>
    </div></div>'''))

# 04 khata ledger with a rubber stamp
rows = [("Isha", "3 days ago", "14"), ("Dev", "5 days ago", "9"), ("Nisha", "8 days ago", "11"), ("Kabir", "26 days ago", "6"), ("Tara", "yesterday", "17")]
trs = ''.join(f'''<div style="opacity:{.5 if n == "Kabir" else 1};display:flex;align-items:center;height:104px;border-bottom:2px solid rgba(180,60,60,.35);font-family:PM;font-size:54px;color:#1c2f6b">
  <div style="flex:1.2">{n}</div><div style="flex:1.3;font-size:44px">{d}</div><div style="flex:.5;text-align:right">{v}</div></div>''' for n, d, v in rows)
slides.append(frame("c", f'''
  <div class="abs" style="left:84px;top:130px">
    <div class="d" style="font-size:100px">See who</div>
    <div class="s" style="font-size:230px;margin-top:-4px;margin-left:10px;transform:rotate(-4deg)">stopped</div>
    <div class="d" style="font-size:100px;margin-top:6px">coming.</div>
  </div>
  <div class="abs" style="left:150px;top:640px;width:800px;height:900px;transform:rotate(-3deg);background:#fbf7ec;box-shadow:0 60px 100px -30px rgba(40,25,5,.55);border-radius:6px">
    <div style="height:84px;background:#9c1c24;border-radius:6px 6px 0 0;display:flex;align-items:center;padding:0 40px;color:#fff;font-weight:700;font-size:25px;letter-spacing:.16em;justify-content:space-between"><span>MARIGOLD LANE · REGULARS</span></div>
    <div style="display:flex;padding:18px 40px 4px 90px;font-weight:700;font-size:21px;letter-spacing:.16em;color:#9c1c24;border-bottom:3px solid #9c1c24"><div style="flex:1.2">NAME</div><div style="flex:1.3">LAST BILL</div><div style="flex:.5;text-align:right">BILLS</div></div>
    <div style="position:absolute;left:70px;top:84px;bottom:0;width:3px;background:rgba(180,60,60,.6)"></div>
    <div style="padding:0 40px 0 90px">{trs}</div>
    <!-- stamp -->
    <svg width="0" height="0"><filter id="rough"><feTurbulence type="fractalNoise" baseFrequency=".9" numOctaves="2" seed="4" result="n"/><feColorMatrix in="n" type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 -2.2 1.7" result="m"/><feComposite in="SourceGraphic" in2="m" operator="in"/></filter></svg>
    <div class="abs" style="left:300px;top:450px;transform:rotate(-8deg);filter:url(#rough);mix-blend-mode:multiply;opacity:.92">
      <div style="border:8px solid #d3202a;border-radius:18px;padding:10px 30px 4px;color:#d3202a;text-align:center">
        <div class="d" style="font-size:66px;letter-spacing:.03em">GONE QUIET</div></div></div>
  </div>'''))

# 05 shopping bag
slides.append(frame("n", f'''
  <div class="abs" style="left:84px;top:130px">
    <div class="d" style="font-size:132px">Put us in</div>
    <div class="d" style="font-size:132px;margin-top:6px">the</div>
    <div class="s" style="font-size:240px;position:absolute;left:260px;top:158px;transform:rotate(-5deg)">bag.</div>
  </div>
  <!-- card poking out of the bag -->
  <div class="abs" style="left:300px;top:540px;width:520px;height:440px;border-radius:30px;background:#fff;transform:rotate(-7deg);box-shadow:0 30px 50px -20px rgba(0,0,0,.5);display:flex;align-items:flex-start;justify-content:center;padding-top:38px;z-index:2">
    <img src="assets/logo-full.png" style="width:330px"></div>
  <!-- bag handles -->
  <svg class="abs" style="left:250px;top:700px;z-index:1" width="640" height="300" viewBox="0 0 640 300" fill="none" stroke="#e8d4a8" stroke-width="12" stroke-linecap="round"><path d="M150 260 C130 80 250 40 320 150"/><path d="M490 260 C510 80 390 40 320 150"/></svg>
  <!-- bag body -->
  <div class="abs" style="left:160px;top:880px;width:760px;height:620px;background:linear-gradient(90deg,#b98f55,#d3ae76 35%,#c79e63 70%,#a98048);box-shadow:0 60px 90px -30px rgba(0,0,0,.7);z-index:3">
    <div class="abs" style="left:0;right:0;top:0;height:46px;background:rgba(0,0,0,.14)"></div>
    <div class="abs" style="left:50%;top:0;bottom:0;width:4px;margin-left:-2px;background:rgba(0,0,0,.08)"></div>
    <div class="abs" style="left:150px;top:150px;display:flex;align-items:center;gap:20px;color:#3a2810;font-weight:700;font-size:40px;letter-spacing:.14em">{FLOWER(70, "#3a2810")}MARIGOLD LANE</div>
    <div class="abs" style="left:150px;top:250px;width:520px;font-weight:600;font-size:34px;line-height:1.35;color:#3a2810">Bring Wystak to the billing counter. DM us <b>“STACK”</b>.</div></div>
'''))

if __name__ == "__main__":
    render(slides, HERE, "wystak-retail", sys.argv[1:])
