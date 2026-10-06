"""Builds the WYSTAK launch carousel: 8 slides at 1080x1350, rendered with headless Chromium."""
import os, subprocess, pathlib, random
HERE = pathlib.Path(__file__).resolve().parent
OUT = HERE / "slides"; OUT.mkdir(exist_ok=True)
import glob
CHROME = glob.glob("/opt/pw-browsers/chromium_headless_shell-1194/*/headless_shell")[0]
TOTAL = 8

CSS = """
@font-face{font-family:I;src:url(assets/inter-latin-400-normal.woff2);font-weight:400}
@font-face{font-family:I;src:url(assets/inter-latin-500-normal.woff2);font-weight:500}
@font-face{font-family:I;src:url(assets/inter-latin-600-normal.woff2);font-weight:600}
@font-face{font-family:I;src:url(assets/inter-latin-700-normal.woff2);font-weight:700}
@font-face{font-family:I;src:url(assets/inter-latin-800-normal.woff2);font-weight:800}
:root{--navy:#0a2860;--deep:#06122c;--purple:#6b2ba6;--lilac:#b58cf0;--teal:#06737c;--aqua:#5fd4cf;--ink:#111318;--grey:#6b6f78;--paper:#f5f5f7}
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:1080px;height:1350px;overflow:hidden}
body{font-family:I,sans-serif;-webkit-font-smoothing:antialiased}
.slide{position:relative;width:1080px;height:1350px;overflow:hidden}
.dark{background:radial-gradient(120% 80% at 50% 105%,#13336f 0%,#0a1d45 38%,#050c1f 75%);color:#fff}
.light{background:var(--paper);color:var(--ink)}
.badge{position:absolute;left:96px;top:92px;height:64px;padding:0 22px;border-radius:32px;background:#fff;display:flex;align-items:center;box-shadow:0 6px 20px rgba(0,0,0,.08)}
.badge img{height:40px}
.count{position:absolute;right:96px;top:110px;font-weight:600;font-size:24px;letter-spacing:.08em;opacity:.55}
.eyebrow{font-weight:700;font-size:26px;letter-spacing:.2em;text-transform:uppercase}
.h{font-weight:800;letter-spacing:-.035em;line-height:1.02}
.sub{font-weight:500;font-size:36px;line-height:1.32;letter-spacing:-.01em}
.dark .sub{color:rgba(255,255,255,.72)} .light .sub{color:#4b4f57}
.acc-d{color:var(--aqua)} .acc-l{color:var(--purple)}
.block{position:absolute;left:96px;right:96px}
.swipe{position:absolute;right:96px;bottom:92px;font-weight:600;font-size:26px;opacity:.6;display:flex;gap:10px;align-items:center}
/* phone */
.phone{position:absolute;border-radius:78px;padding:14px;background:linear-gradient(145deg,#4a4f5a,#1a1d23 40%,#3a3e47 70%,#15171c);box-shadow:0 60px 120px -30px rgba(0,0,0,.55),0 20px 40px -20px rgba(0,0,0,.4)}
.screen{position:relative;width:100%;height:100%;border-radius:64px;overflow:hidden;background:#f3f4f1}
.island{position:absolute;left:50%;top:20px;width:130px;height:38px;margin-left:-65px;border-radius:19px;background:#000;z-index:9}
.wallet-t{position:absolute;left:36px;top:96px;font-weight:800;font-size:46px;letter-spacing:-.02em;color:#111}
.pass{position:absolute;left:24px;right:24px;border-radius:28px;padding:26px 28px;color:#fff;overflow:hidden}
.pass .row{display:flex;justify-content:space-between;align-items:center;font-weight:700;font-size:24px;letter-spacing:.04em}
.pass .lbl{font-weight:600;font-size:17px;letter-spacing:.14em;opacity:.8}
.pass .big{font-weight:800;font-size:66px;letter-spacing:-.02em;margin-top:6px}
.qrbox{background:#fff;border-radius:16px;padding:12px}
.notif{position:absolute;left:22px;right:22px;border-radius:30px;background:rgba(246,246,243,.94);padding:22px 24px;display:flex;gap:18px;color:#111}
.ni{width:66px;height:66px;border-radius:16px;background:var(--teal);flex:none;display:flex;align-items:center;justify-content:center}
.chip{height:72px;padding:0 30px;border-radius:36px;display:inline-flex;align-items:center;gap:14px;font-weight:600;font-size:30px}
"""

def qr(size, seed, color="#0a2860"):
    N=25; m=size/N; r=random.Random(seed); s=""
    def f(x,y): return 0<=x<7 and 0<=y<7
    for y in range(N):
        for x in range(N):
            if f(x,y) or f(x-(N-7),y) or f(x,y-(N-7)): continue
            if r.random()>.52: s+=f'<rect x="{x*m:.2f}" y="{y*m:.2f}" width="{m+.4:.2f}" height="{m+.4:.2f}"/>'
    def fp(x,y): return (f'<rect x="{x*m}" y="{y*m}" width="{7*m}" height="{7*m}" rx="{m}"/>'
        f'<rect x="{(x+1)*m}" y="{(y+1)*m}" width="{5*m}" height="{5*m}" rx="{m*.6}" fill="#fff"/>'
        f'<rect x="{(x+2)*m}" y="{(y+2)*m}" width="{3*m}" height="{3*m}" rx="{m*.4}"/>')
    return f'<svg width="{size}" height="{size}" viewBox="0 0 {size} {size}" fill="{color}">{s}{fp(0,0)}{fp(N-7,0)}{fp(0,N-7)}</svg>'

CRANE = '<svg width="34" height="34" viewBox="0 0 34 34" fill="none" stroke="#fff" stroke-width="2.6" stroke-linejoin="round"><path d="M3 21 L17 6 L31 21 L17 17 Z"/><path d="M17 17 L17 29"/></svg>'

def cafe_pass(top, height, pts="132", extra=""):
    return f'''<div class="pass" style="top:{top}px;height:{height}px;background:linear-gradient(160deg,#0a8a8f,#06646c)">
      <div class="row"><span style="display:flex;gap:12px;align-items:center">{CRANE}PAPER CRANE COFFEE</span><span>{pts} PTS</span></div>
      <div style="margin-top:34px" class="lbl">NEXT REWARD</div><div class="big">{pts} / 150</div>
      <div style="display:flex;gap:46px;margin-top:20px"><div><div class="lbl">MEMBER</div><div style="font-weight:700;font-size:28px;margin-top:4px">Aarav</div></div>
      <div><div class="lbl">REWARD</div><div style="font-weight:700;font-size:28px;margin-top:4px">Free cold coffee</div></div></div>
      {extra}</div>'''

def frame(cls, n, body, badge=True):
    b = '<div class="badge"><img src="assets/logo-wordmark.png"></div>' if badge else ''
    return f'''<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head><body>
    <div class="slide {cls}">{b}<div class="count">{n:02d} / {TOTAL:02d}</div>{body}</div></body></html>'''

ICONS = {'Pay': '<svg width="56" height="56" viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="1.8" stroke-linecap="round"><path d="M7 5h10M7 9h10M7 5c5 0 5 8 0 8l7 6"/></svg>', 'Order': '<svg width="56" height="56" viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="1.8" stroke-linejoin="round"><path d="M5 8h14l-1 12H6z"/><path d="M9 8a3 3 0 0 1 6 0"/></svg>', 'Chat': '<svg width="56" height="56" viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="1.8" stroke-linejoin="round"><path d="M4 5h16v11H9l-5 4z"/></svg>', 'Ride': '<svg width="56" height="56" viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="1.8" stroke-linejoin="round"><path d="M4 15l2-6h12l2 6v3H4z"/><circle cx="8" cy="18" r="1.5"/><circle cx="16" cy="18" r="1.5"/></svg>'}
slides = []

# 01 cover
slides.append(frame("dark", 1, f'''
  <div class="block" style="top:250px"><div class="eyebrow acc-d">Introducing Wystak</div>
  <div class="h" style="font-size:112px;margin-top:30px">Is your café<br>on their <span class="acc-d">phone?</span></div></div>
  <div class="phone" style="left:300px;top:690px;width:480px;height:900px;transform:rotate(-6deg)"><div class="island"></div><div class="screen">
    <div class="wallet-t">Wallet</div>
    <div class="pass" style="top:180px;height:120px;background:#2e3a59"><div class="row"><span>CITY METRO</span><span>₹240</span></div></div>
    <div class="pass" style="top:250px;height:120px;background:#8a5a2b"><div class="row"><span>BOOK CLUB</span><span>6 / 10</span></div></div>
    {cafe_pass(320, 420)}
  </div></div>
  <div class="swipe">Swipe <span style="font-size:30px">→</span></div>'''))

# 02 stake
slides.append(frame("light", 2, f'''
  <div class="block" style="top:270px"><div class="h" style="font-size:100px">Every app on<br>their phone is<br><span class="acc-l">someone else's.</span></div>
  <div class="sub" style="margin-top:44px;max-width:820px">Payments, delivery, chats. Your regulars see your café every week. Their phone never does.</div></div>
  <div style="position:absolute;left:96px;right:96px;top:900px;display:grid;grid-template-columns:repeat(4,1fr);gap:28px">
    {''.join(f'<div style="height:214px;border-radius:48px;background:{c};display:flex;flex-direction:column;justify-content:space-between;padding:26px;font-weight:700;font-size:24px;color:#fff">{ICONS[t]}<span>{t}</span></div>' for c,t in [("#3b4252","Pay"),("#7a5230","Order"),("#2f6b4f","Chat"),("#4a3a6e","Ride")])}
  </div>
  <div style="position:absolute;left:96px;top:1170px;font-weight:700;font-size:40px;letter-spacing:-.02em;color:#111318">None of them are yours.</div>'''))

# 03 insight
slides.append(frame("dark", 3, f'''
  <div class="block" style="top:250px"><div class="eyebrow acc-d">The insight</div>
  <div class="h" style="font-size:100px;margin-top:28px">One place they<br>keep what<br><span class="acc-d">matters.</span></div>
  <div class="sub" style="margin-top:40px;max-width:800px">Boarding passes. Tickets. The wallet is already on every phone.</div></div>
  <div style="position:absolute;left:96px;right:96px;top:910px;height:330px">
    <div class="pass" style="left:0;right:0;top:0;height:150px;background:#2b3550"><div class="row"><span>BOARDING PASS</span><span>BLR → BOM</span></div></div>
    <div class="pass" style="left:0;right:0;top:80px;height:150px;background:#5b2d86"><div class="row"><span>CONCERT TICKET</span><span>GATE 4</span></div></div>
    <div class="pass" style="left:0;right:0;top:160px;height:170px;background:linear-gradient(160deg,#0a8a8f,#06646c);box-shadow:0 -10px 40px rgba(0,0,0,.35)"><div class="row"><span style="display:flex;gap:12px;align-items:center">{CRANE}YOUR CAFÉ</span><span>132 PTS</span></div><div class="lbl" style="margin-top:22px">NOW IN THE WALLET</div></div>
  </div>'''))

# 04 meet
slides.append(frame("light", 4, f'''
  <div class="block" style="top:250px"><div class="h" style="font-size:108px">Meet <span class="acc-l">Wystak.</span></div>
  <div class="sub" style="margin-top:34px;max-width:860px">Your loyalty pass in Apple Wallet and Google Wallet. Your name. Your colours. Your rewards.</div></div>
  <div style="position:absolute;left:150px;right:150px;top:720px;height:470px;transform:rotate(-3deg)">
    {cafe_pass(0, 470, extra='<div class="qrbox" style="position:absolute;right:28px;bottom:28px">'+qr(120,5,"#111")+'</div>').replace('left:24px;right:24px','left:0;right:0').replace('class="pass"','class="pass" ',1)}
  </div>
  <div style="position:absolute;left:0;right:0;top:1230px;display:flex;justify-content:center;gap:22px">
    <div class="chip" style="background:#111;color:#fff;height:62px;font-size:26px">Apple Wallet</div><div class="chip" style="background:#111;color:#fff;height:62px;font-size:26px">Google Wallet</div></div>'''))

# 05 one scan
slides.append(frame("dark", 5, f'''
  <div class="block" style="top:250px"><div class="h" style="font-size:104px">One scan.<br><span class="acc-d">No app.</span></div>
  <div class="sub" style="margin-top:36px;max-width:820px">A QR at your counter. A name and a number. The pass is in their wallet in seconds.</div></div>
  <div style="position:absolute;left:96px;top:820px;width:400px;height:430px;border-radius:44px;background:#fff;display:flex;flex-direction:column;align-items:center;padding-top:34px;color:#111">
    <div style="font-weight:800;font-size:28px">Join our rewards</div><div style="margin-top:22px">{qr(250,29)}</div>
    <div style="font-weight:500;font-size:22px;color:#555;margin-top:18px">Paper Crane Coffee</div></div>
  <div style="position:absolute;left:560px;right:96px;top:840px;display:flex;flex-direction:column;gap:30px">
    {''.join(f'<div style="display:flex;gap:22px;align-items:center"><div style="width:64px;height:64px;border-radius:50%;border:2px solid rgba(255,255,255,.35);display:flex;align-items:center;justify-content:center;font-weight:700;font-size:28px">{i}</div><div style="font-weight:600;font-size:34px">{t}</div></div>' for i,t in [(1,"Scan the QR"),(2,"Name and number"),(3,"Add to wallet")])}
  </div>'''))

# 06 lock screen
slides.append(frame("light", 6, f'''
  <div class="block" style="top:250px"><div class="h" style="font-size:96px">Every visit, on<br>their <span class="acc-l">lock screen.</span></div>
  <div class="sub" style="margin-top:34px;max-width:860px">Seconds after they pay, the points update. No cost per message.</div></div>
  <div class="phone" style="left:290px;top:720px;width:500px;height:900px"><div class="island"></div><div class="screen" style="background:linear-gradient(170deg,#1b2a55,#2d2257 55%,#133f4c)">
    <div style="position:absolute;left:0;right:0;top:92px;text-align:center;color:rgba(255,255,255,.85);font-weight:500;font-size:26px">Tuesday, 6 October</div>
    <div style="position:absolute;left:0;right:0;top:128px;text-align:center;color:#fff;font-weight:600;font-size:140px;letter-spacing:-.03em">10:24</div>
    <div class="notif" style="top:360px"><div class="ni">{CRANE}</div><div style="flex:1;min-width:0">
      <div style="display:flex;justify-content:space-between;font-weight:700;font-size:23px">Paper Crane Coffee <span style="color:#777;font-weight:500">now</span></div>
      <div style="font-weight:800;font-size:32px;margin-top:6px">+18 points</div>
      <div style="font-weight:500;font-size:22px;color:#444;margin-top:4px;line-height:1.3">You're at 132 of 150. One more visit and it's on the house.</div></div></div>
  </div></div>'''))

# 07 know regulars
rows = [("A","Aarav S.","Yesterday","14 visits","#0a2860",False),("M","Meera K.","2 days ago","11 visits","#06737c",False),("R","Rohan D.","4 days ago","9 visits","#8a5a2b",False),("K","Kabir J.","26 days ago","Stopped coming","#6b2ba6",True)]
rh = ''.join(f'''<div style="display:flex;align-items:center;gap:24px;height:118px;padding:0 26px;border-radius:26px;{'background:#efe7f8;' if hl else ''}">
  <div style="width:76px;height:76px;border-radius:50%;background:{c};color:#fff;display:flex;align-items:center;justify-content:center;font-weight:800;font-size:30px">{a}</div>
  <div><div style="font-weight:700;font-size:32px">{n}</div><div style="font-weight:500;font-size:22px;color:#6b6f78;margin-top:2px">Last visit · {d}</div></div>
  <div style="margin-left:auto;font-weight:700;font-size:{'24' if hl else '28'}px;color:{'#6b2ba6' if hl else '#06737c'}">{v}</div></div>''' for a,n,d,v,c,hl in rows)
slides.append(frame("dark", 7, f'''
  <div class="block" style="top:250px"><div class="h" style="font-size:100px">Know your<br><span class="acc-d">regulars.</span></div>
  <div class="sub" style="margin-top:34px;max-width:820px">See who keeps coming back. And who quietly stopped.</div></div>
  <div style="position:absolute;left:96px;right:96px;top:690px;border-radius:48px;background:#fff;color:#111;padding:36px 30px 30px">
    <div style="padding:0 26px 18px;font-weight:800;font-size:36px">Your regulars <span style="font-weight:500;font-size:24px;color:#6b6f78;margin-left:10px">Paper Crane Coffee</span></div>{rh}</div>'''))

# 08 end
slides.append(frame("light", 8, f'''
  <div style="position:absolute;left:0;right:0;top:250px;display:flex;justify-content:center"><img src="assets/logo-full.png" style="width:640px"></div>
  <div style="position:absolute;left:0;right:0;top:880px;text-align:center"><div class="h" style="font-size:72px">Be in their <span class="acc-l">wallet.</span></div>
  <div class="sub" style="margin-top:26px">Bring Wystak to your counter.</div>
  <div class="chip" style="margin-top:44px;background:var(--navy);color:#fff;height:86px;font-size:32px;padding:0 44px">DM us “STACK”</div></div>''', badge=False))

for i, html in enumerate(slides, 1):
    p = HERE / f"_slide{i:02d}.html"; p.write_text(html)
    png = OUT / f"wystak-launch-{i:02d}.png"
    subprocess.run([CHROME, "--no-sandbox", "--disable-gpu", "--hide-scrollbars", "--force-device-scale-factor=1",
                    "--window-size=1080,1350", "--allow-file-access-from-files", f"--screenshot={png}", p.as_uri()],
                   check=True, capture_output=True, timeout=120)
    p.unlink()
    print("ok", png.name)
