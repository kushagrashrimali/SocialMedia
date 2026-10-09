"""Builds the WYSTAK launch carousel in the 'object' style: 8 slides at 1080x1350.

Each slide is built around one real-world object drawn in code (a delete dialog,
a wallet fan, a newspaper, a table tent, a lock screen, myth-vs-fact tape, an
order pad, an envelope). Type: Anton capitals, one handwritten Caveat word,
Poppins for small text. Grounds alternate Wystak violet and warm paper.
"""
import os, subprocess, pathlib, random, glob, shutil, sys
HERE = pathlib.Path(__file__).resolve().parent
OUT = HERE / "slides"; OUT.mkdir(exist_ok=True)


def find_chrome():
    """Return (path, is_headless_shell). Set the CHROME env var to override."""
    if os.environ.get("CHROME"):
        p = os.environ["CHROME"]; return p, "headless_shell" in p
    shells = glob.glob("/opt/pw-browsers/chromium_headless_shell-*/*/headless_shell")
    if shells:
        return shells[0], True
    home = os.path.expanduser("~")
    candidates = [
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
        "/Applications/Chromium.app/Contents/MacOS/Chromium",
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        os.path.join(home, r"AppData\Local\Google\Chrome\Application\chrome.exe"),
    ]
    candidates += [shutil.which(n) for n in ("google-chrome", "google-chrome-stable", "chromium", "chromium-browser", "chrome")]
    for c in candidates:
        if c and os.path.exists(c):
            return c, False
    raise SystemExit("Chrome not found. Install Google Chrome, or set CHROME=/path/to/chrome")


TOTAL = 5
GRAIN = ("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='600' height='600'>"
         "<filter id='n'><feTurbulence type='fractalNoise' baseFrequency='.85' numOctaves='3' stitchTiles='stitch'/>"
         "<feColorMatrix type='saturate' values='0'/></filter><rect width='100%' height='100%' filter='url(%23n)'/></svg>")

CSS = """
@font-face{font-family:A;src:url(assets/anton-latin-400-normal.woff2)}
@font-face{font-family:C;src:url(assets/caveat-latin-700-normal.woff2);font-weight:700}
@font-face{font-family:C;src:url(assets/caveat-latin-600-normal.woff2);font-weight:600}
@font-face{font-family:P;src:url(assets/poppins-latin-400-normal.woff2);font-weight:400}
@font-face{font-family:P;src:url(assets/poppins-latin-500-normal.woff2);font-weight:500}
@font-face{font-family:P;src:url(assets/poppins-latin-600-normal.woff2);font-weight:600}
@font-face{font-family:P;src:url(assets/poppins-latin-700-normal.woff2);font-weight:700}
:root{--navy:#0a2860;--violet:#6b2ba6;--deepv:#3a1166;--lilac:#c9a8f2;--teal:#06737c;--aqua:#5fd4cf;--ink:#14121a;--paper:#f3efe6}
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:1080px;height:1350px;overflow:hidden}
body{font-family:P,sans-serif;-webkit-font-smoothing:antialiased}
.slide{position:relative;width:1080px;height:1350px;overflow:hidden}
.v{background:radial-gradient(90% 70% at 50% 40%,#7d3cc0 0%,#5a1f95 45%,#3a1166 100%);color:#fff}
.p{background:var(--paper);color:var(--ink)}
.n{background:radial-gradient(90% 70% at 50% 40%,#16407f 0%,#0a2860 50%,#061a42 100%);color:#fff}
.grain{position:absolute;inset:0;background:url("GRAIN");pointer-events:none;z-index:50}
.v .grain,.n .grain{opacity:.22;mix-blend-mode:soft-light}
.p .grain{opacity:.16;mix-blend-mode:multiply}
.vig{position:absolute;inset:0;pointer-events:none;z-index:49;box-shadow:inset 0 0 220px rgba(20,0,40,.45)}
.p .vig{box-shadow:inset 0 0 200px rgba(90,70,40,.16)}
.d{font-family:A,sans-serif;text-transform:uppercase;line-height:1;letter-spacing:.005em;white-space:nowrap}
.s{font-family:C,cursive;font-weight:700;line-height:.8;white-space:nowrap}
.v .s,.n .s{color:var(--aqua)} .p .s{color:var(--violet)}
.sub{font-weight:500;font-size:36px;line-height:1.35}
.v .sub{color:rgba(255,255,255,.82)} .p .sub{color:#4a4552}
.tape{position:relative;display:inline-block;padding:0 .12em;z-index:0}
.tape:before{content:"";position:absolute;left:-.04em;right:-.06em;top:.12em;bottom:.04em;background:var(--aqua);transform:rotate(-1.6deg);z-index:-1;border-radius:3px 6px 4px 7px;opacity:.95}
.abs{position:absolute}
""".replace("GRAIN", GRAIN)

CRANE = lambda s, c="#fff": f'<svg width="{s}" height="{s}" viewBox="0 0 34 34" fill="none" stroke="{c}" stroke-width="2.6" stroke-linejoin="round"><path d="M3 21 L17 6 L31 21 L17 17 Z"/><path d="M17 17 L17 29"/></svg>'


def qr(size, seed, color="#0a2860"):
    N = 25; m = size / N; r = random.Random(seed); s = ""
    def f(x, y): return 0 <= x < 7 and 0 <= y < 7
    for y in range(N):
        for x in range(N):
            if f(x, y) or f(x - (N - 7), y) or f(x, y - (N - 7)): continue
            if r.random() > .52: s += f'<rect x="{x*m:.2f}" y="{y*m:.2f}" width="{m+.4:.2f}" height="{m+.4:.2f}"/>'
    def fp(x, y): return (f'<rect x="{x*m}" y="{y*m}" width="{7*m}" height="{7*m}" rx="{m}"/>'
        f'<rect x="{(x+1)*m}" y="{(y+1)*m}" width="{5*m}" height="{5*m}" rx="{m*.6}" fill="#fff"/>'
        f'<rect x="{(x+2)*m}" y="{(y+2)*m}" width="{3*m}" height="{3*m}" rx="{m*.4}"/>')
    return f'<svg width="{size}" height="{size}" viewBox="0 0 {size} {size}" fill="{color}">{s}{fp(0,0)}{fp(N-7,0)}{fp(0,N-7)}</svg>'


def arrow(w, h, d, color, sw=7, head=(0, 0, 0)):
    """A hand-drawn arrow: path d in a w x h box, with a two-stroke head at (x, y) pointing at angle a (deg)."""
    x, y, a = head
    return (f'<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}" fill="none" stroke="{color}" stroke-width="{sw}" '
            f'stroke-linecap="round" stroke-linejoin="round"><path d="{d}"/>'
            f'<g transform="translate({x} {y}) rotate({a})"><path d="M0 0 L-34 -16 M0 0 L-30 20"/></g></svg>')


def thumb(w, rot, ink="#1b1530"):
    """A halftone collage thumb, cut out with a white sticker edge. Points up before rotation."""
    return f'''<svg width="{w}" height="{w*2.2:.0f}" viewBox="-30 -30 300 660" style="transform:rotate({rot}deg);overflow:visible">
  <defs>
    <pattern id="ht" width="9" height="9" patternUnits="userSpaceOnUse" patternTransform="rotate(30)"><circle cx="4.5" cy="4.5" r="2.6" fill="{ink}"/></pattern>
    <pattern id="ht2" width="9" height="9" patternUnits="userSpaceOnUse" patternTransform="rotate(30)"><circle cx="4.5" cy="4.5" r="1.4" fill="{ink}"/></pattern>
    <linearGradient id="sh" x1="0" x2="1"><stop offset="0" stop-color="#fff" stop-opacity="1"/><stop offset=".55" stop-color="#fff" stop-opacity=".15"/><stop offset="1" stop-color="#fff" stop-opacity=".9"/></linearGradient>
    <mask id="mk"><rect x="-30" y="-30" width="300" height="660" fill="url(#sh)"/></mask>
    <filter id="ds" x="-30%" y="-30%" width="160%" height="160%"><feDropShadow dx="-10" dy="18" stdDeviation="14" flood-color="#000" flood-opacity=".35"/></filter>
  </defs>
  <g filter="url(#ds)">
    <path id="th" d="M40 640 L40 120 C40 30 80 0 120 0 C160 0 200 30 200 120 L200 300 C230 330 250 380 250 640 Z" fill="#fff" stroke="#fff" stroke-width="22" stroke-linejoin="round"/>
    <path d="M40 640 L40 120 C40 30 80 0 120 0 C160 0 200 30 200 120 L200 300 C230 330 250 380 250 640 Z" fill="#efe9e0"/>
    <path d="M40 640 L40 120 C40 30 80 0 120 0 C160 0 200 30 200 120 L200 300 C230 330 250 380 250 640 Z" fill="url(#ht)" mask="url(#mk)"/>
    <rect x="68" y="14" width="104" height="128" rx="48" fill="#fbf8f3" stroke="{ink}" stroke-width="3" stroke-opacity=".55"/>
    <rect x="68" y="14" width="104" height="128" rx="48" fill="url(#ht2)" opacity=".35"/>
    <path d="M70 236 C100 248 140 248 172 236 M78 258 C108 268 134 268 164 258" stroke="{ink}" stroke-width="3.4" fill="none" stroke-linecap="round" opacity=".7"/>
    <path d="M40 640 L40 120 C40 30 80 0 120 0 C160 0 200 30 200 120 L200 300 C230 330 250 380 250 640" fill="none" stroke="{ink}" stroke-width="4" stroke-opacity=".75"/>
  </g></svg>'''


def frame(cls, body):
    return f'''<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head><body>
    <div class="slide {cls}">{body}<div class="vig"></div><div class="grain"></div></div></body></html>'''


slides = []

# 01 cover: delete dialog, halftone thumb on Delete
slides.append(frame("v", f'''
  <div class="abs" style="left:84px;top:210px;width:920px">
    <div class="d" style="font-size:140px;line-height:1.2">Nobody is<br>downloading<br>your café's</div>
    <div class="s abs" style="font-size:220px;left:620px;top:390px;transform:rotate(-7deg)">app.</div>
    <div class="sub" style="margin-top:22px;font-size:38px">Not one regular.</div>
  </div>
  <div class="abs" style="left:100px;top:790px;width:660px;border-radius:44px;background:rgba(246,244,250,.97);color:#111;transform:rotate(-4deg);box-shadow:0 50px 90px -30px rgba(10,0,30,.75),0 0 0 1px rgba(255,255,255,.6) inset;overflow:hidden">
    <div style="display:flex;flex-direction:column;align-items:center;padding:42px 50px 30px;text-align:center">
      <div style="width:116px;height:116px;border-radius:28px;background:linear-gradient(160deg,#0a8a8f,#06646c);display:flex;align-items:center;justify-content:center;box-shadow:0 6px 16px rgba(0,0,0,.18)">{CRANE(66)}</div>
      <div style="font-weight:600;font-size:32px;margin-top:22px;letter-spacing:-.01em;white-space:nowrap">Delete “Paper Crane Coffee”?</div>
      <div style="font-weight:400;font-size:24px;color:#555;margin-top:10px;line-height:1.35">This will also delete its data.</div>
    </div>
    <div style="border-top:1.5px solid #d9d6de;height:92px;display:flex;align-items:center;justify-content:center;font-weight:600;font-size:32px;color:#e5332a;background:rgba(229,51,42,.07)">Delete App</div>
    <div style="border-top:1.5px solid #d9d6de;height:92px;display:flex;align-items:center;justify-content:center;font-weight:500;font-size:32px;color:#2f6fe4">Cancel</div>
  </div>
  <div class="abs" style="left:600px;top:1035px;z-index:5">{thumb(230, -38)}</div>
  <div class="abs" style="right:84px;top:66px;display:flex;align-items:center;gap:6px;z-index:6">
    <span class="s" style="font-size:64px;color:#fff">swipe</span>
    {arrow(150, 70, "M8 40 C40 20 80 58 138 34", "#fff", 6, (138, 34, -22))}
  </div>'''))

# 02 newspaper
col = lambda n, w: ''.join(f'<div style="height:9px;margin:9px 0;background:#cfc7b6;border-radius:2px;width:{w if i < n-1 else w*0.6:.0f}px"></div>' for i in range(n))
slides.append(frame("n", f'''
  <div class="abs" style="left:120px;top:250px;width:840px;height:990px;perspective:1600px">
   <div style="position:absolute;inset:0;transform:rotateX(9deg) rotateY(-10deg) rotateZ(-3deg);transform-origin:50% 60%">
    <div style="position:absolute;inset:0;background:#f1ebdd;box-shadow:0 70px 120px -30px rgba(10,0,30,.8);padding:46px 52px;color:#16131c">
      <div style="display:flex;justify-content:space-between;font-weight:600;font-size:17px;letter-spacing:.14em;border-bottom:2px solid #16131c;padding-bottom:10px">
        <span>VOL. 1 · LAUNCH EDITION</span><span>FOR CAFÉS, RESTAURANTS AND SHOPS</span></div>
      <div class="d" style="font-size:94px;text-align:center;margin:16px 0 8px;letter-spacing:.03em">The Counter Times</div>
      <div style="border-top:5px double #16131c;border-bottom:2px solid #16131c;height:12px"></div>
      <div style="display:flex;align-items:center;gap:18px;margin-top:26px">
        <div class="d" style="font-size:44px;background:#16131c;color:#f1ebdd;padding:6px 16px 4px">Extra</div>
        <div style="font-weight:600;font-size:22px;letter-spacing:.12em">LOYALTY, WITHOUT THE APP</div></div>
      <div class="d" style="font-size:118px;margin-top:18px;line-height:.95">Cafés move<br>into the wallet</div>
      <div style="display:flex;gap:34px;margin-top:34px">
        <div style="flex:1.35;background:#fff;border:2px solid #16131c;height:290px;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:10px">
          <img src="assets/logo-full.png" style="width:270px">
        </div>
        <div style="flex:1">
          <div style="font-weight:700;font-size:30px;line-height:1.15">Introducing Wystak.</div>
          <div style="font-weight:500;font-size:19px;line-height:1.4;margin-top:10px;color:#3b3640">Your loyalty pass in Apple Wallet and Google Wallet. Tap or scan at the counter to join. No app.</div>
          {col(3, 300)}
        </div>
      </div>
      <div style="display:flex;gap:30px;margin-top:18px"><div style="flex:1">{col(3, 340)}</div><div style="flex:1">{col(3, 340)}</div></div>
    </div>
    <div style="position:absolute;left:49%;top:0;bottom:0;width:4%;background:linear-gradient(90deg,rgba(0,0,0,0),rgba(0,0,0,.09) 45%,rgba(255,255,255,.35) 55%,rgba(0,0,0,0))"></div>
   </div>
  </div>
  <div class="abs" style="left:560px;top:150px;transform:rotate(-6deg);z-index:6"><span class="s" style="font-size:84px">read all about it</span></div>'''))

# 03 tap or scan: NFC + QR stand on the counter, a phone tapping it
NFC = lambda s, c: f'<svg width="{s}" height="{s}" viewBox="0 0 48 48" fill="none" stroke="{c}" stroke-width="4" stroke-linecap="round"><path d="M14 16 C18 20 18 28 14 32"/><path d="M21 11 C28 18 28 30 21 37"/><path d="M28 6 C38 16 38 32 28 42"/></svg>'
slides.append(frame("p", f'''
  <div class="abs" style="left:0;right:0;top:0;height:1350px;background-image:linear-gradient(rgba(60,40,20,.07) 2px,transparent 2px),linear-gradient(90deg,rgba(60,40,20,.07) 2px,transparent 2px);background-size:135px 135px"></div>
  <div class="abs" style="left:84px;top:150px;width:920px">
    <div class="d" style="font-size:170px">Tap. Or scan.</div>
    <div class="d" style="font-size:170px">No <span class="s" style="font-size:240px;text-transform:none;display:inline-block;transform:rotate(-6deg) translateY(16px)">app.</span></div>
    <div class="sub" style="margin-top:60px;max-width:600px;font-size:32px">Tap the stand or scan the QR. They're a member, with the pass in Apple Wallet or Google Wallet, in seconds.</div>
  </div>
  <div class="abs" style="left:96px;top:800px;width:500px;height:500px;border-radius:28px;background:linear-gradient(165deg,#0a8a8f,#06646c);transform:rotate(-6deg);box-shadow:0 50px 80px -30px rgba(40,30,20,.6);color:#fff;padding:36px 36px;text-align:center">
    <div style="display:flex;gap:12px;align-items:center;justify-content:center;font-weight:700;font-size:21px;letter-spacing:.08em;white-space:nowrap">{CRANE(30)}PAPER CRANE COFFEE</div>
    <div style="display:flex;gap:24px;margin-top:26px">
      <div style="flex:1;height:240px;border-radius:22px;background:#fff;color:#0b3b40;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:6px">
        {qr(150, 7, "#0b3b40")}<div style="font-weight:700;font-size:26px;letter-spacing:.14em">SCAN</div></div>
      <div style="flex:1;height:240px;border-radius:22px;background:#fff;color:#0b3b40;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:8px;box-shadow:inset 0 0 0 4px rgba(6,115,124,.25)">
        {NFC(120, "#0b3b40")}<div style="font-weight:700;font-size:26px;letter-spacing:.14em">TAP</div></div>
    </div>
    <div style="text-align:left;padding-left:6px"><div style="font-weight:700;font-size:32px;margin-top:28px;white-space:nowrap">Become a member.</div>
    <div style="font-weight:500;font-size:19px;opacity:.8;margin-top:4px;letter-spacing:.04em">Apple Wallet · Google Wallet</div></div>
  </div>
  <svg class="abs" style="left:500px;top:810px;z-index:5" width="200" height="160" viewBox="0 0 200 160" fill="none" stroke="#6b2ba6" stroke-width="7" stroke-linecap="round"><path d="M40 120 C52 100 70 92 92 96"/><path d="M26 98 C44 66 80 54 112 62"/><path d="M12 76 C36 32 92 16 132 30"/></svg>
  <div class="abs" style="left:470px;top:975px;width:340px;height:680px;border-radius:56px;padding:12px;background:linear-gradient(145deg,#4a4f5a,#1a1d23 40%,#3a3e47 70%,#15171c);transform:rotate(-24deg);transform-origin:0 0;box-shadow:-30px 60px 90px -30px rgba(40,30,20,.6);z-index:4">
    <div style="position:relative;width:100%;height:100%;border-radius:46px;overflow:hidden;background:linear-gradient(180deg,#d9d3e6,#b9aed0)">
      <div style="position:absolute;left:50%;top:16px;width:96px;height:28px;margin-left:-48px;border-radius:14px;background:#000"></div>
      <div style="position:absolute;left:12px;right:12px;top:96px;bottom:12px;border-radius:34px;background:#fff;padding:26px 24px;text-align:center;color:#111">
        <div style="width:96px;height:96px;margin:0 auto;border-radius:24px;background:linear-gradient(160deg,#0a8a8f,#06646c);display:flex;align-items:center;justify-content:center">{CRANE(54)}</div>
        <div style="font-weight:700;font-size:26px;margin-top:18px">Paper Crane Coffee</div>
        <div style="font-weight:500;font-size:19px;color:#666;margin-top:4px">Become a member</div>
        <div style="margin-top:34px;height:62px;border-radius:31px;background:#111;color:#fff;display:flex;align-items:center;justify-content:center;font-weight:600;font-size:21px">Add to Wallet</div>
      </div>
    </div>
  </div>
  <div class="abs" style="left:740px;top:700px;transform:rotate(-6deg)"><span class="s" style="font-size:80px">tap to join</span></div>
  <div class="abs" style="left:680px;top:780px;z-index:6">{arrow(130, 120, "M100 10 C96 50 76 80 24 96", "#6b2ba6", 6, (24, 96, 165))}</div>'''))

# 04 order pad of regulars
rows = [("Aarav", "14 visits", True), ("Meera", "11 visits", True), ("Rohan", "9 visits", True), ("Kabir", "last seen 26 days ago", False)]
pad_rows = ''.join(f'''<div style="position:relative;height:96px;display:flex;align-items:center;justify-content:space-between;border-bottom:2px solid #c9d8e8">
  <span class="s" style="font-size:66px;color:#1d2a6b">{n}</span><span class="s" style="font-size:48px;color:#1d2a6b;opacity:.85">{v}</span>
  {'<span class="s" style="position:absolute;right:-84px;font-size:70px;color:#06737c">✓</span>' if ok else ''}</div>''' for n, v, ok in rows)
slides.append(frame("v", f'''
  <div class="abs" style="left:84px;top:210px;width:930px">
    <div class="d" style="font-size:104px">Know who came back.</div>
    <div class="d" style="font-size:104px">And who <span class="s" style="font-size:170px;text-transform:none;display:inline-block;transform:rotate(-6deg) translateY(14px)">stopped.</span></div>
  </div>
  <div class="abs" style="left:170px;top:560px;width:720px;height:820px;background:#fbf7ec;transform:rotate(-4deg);box-shadow:0 60px 110px -30px rgba(10,0,30,.8)">
    <div style="height:70px;background:#0a2860;display:flex;align-items:center;justify-content:center;gap:12px;color:#fff;font-weight:700;font-size:22px;letter-spacing:.14em">{CRANE(28)}PAPER CRANE COFFEE · REGULARS</div>
    <div style="height:14px;background:radial-gradient(circle at 7px 7px,#3a1166 0 4px,transparent 5px) 0 0/22px 14px"></div>
    <div style="position:relative;padding:20px 120px 0 60px;border-left:3px solid #e8a3a3;margin-left:44px">{pad_rows}
      <div style="height:96px;border-bottom:2px solid #c9d8e8;display:flex;align-items:center;justify-content:flex-end"><span class="s" style="font-size:60px;color:#6b2ba6;transform:rotate(-3deg)">↑ quietly stopped</span></div><div style="height:96px;border-bottom:2px solid #c9d8e8"></div>
      <svg style="position:absolute;left:10px;top:290px" width="600" height="130" viewBox="0 0 600 130" fill="none" stroke="#06a3a0" stroke-width="6" stroke-linecap="round"><path d="M60 30 C180 4 470 6 560 34 C620 64 540 116 300 120 C120 122 10 100 20 64 C30 40 90 26 160 20"/></svg></div>
  </div>
  <div class="abs" style="left:660px;top:1310px;width:520px;height:34px;transform:rotate(-40deg);transform-origin:0 50%;z-index:6;filter:drop-shadow(10px 18px 12px rgba(0,0,0,.35))">
    <div style="position:absolute;left:0;top:0;width:70px;height:34px;background:#f0c98a;clip-path:polygon(0 50%,100% 0,100% 100%)"></div>
    <div style="position:absolute;left:0;top:12px;width:18px;height:10px;background:#333;clip-path:polygon(0 50%,100% 0,100% 100%)"></div>
    <div style="position:absolute;left:70px;top:0;width:390px;height:34px;background:linear-gradient(#f7c53c,#e2a51e 55%,#c98d12)"></div>
    <div style="position:absolute;left:460px;top:0;width:24px;height:34px;background:linear-gradient(#ddd,#999)"></div>
    <div style="position:absolute;left:484px;top:0;width:36px;height:34px;border-radius:0 10px 10px 0;background:#e98a9a"></div>
  </div>'''))

# 05 envelope invitation
slides.append(frame("p", f'''
  <div class="abs" style="left:0;right:0;top:100px;text-align:center">
    <div class="d" style="font-size:190px">Open this.</div>
    <div class="d" style="font-size:72px;margin-top:6px"><span class="s" style="font-size:118px;text-transform:none;display:inline-block;transform:rotate(-5deg) translateY(8px)">Your</span> counter is invited.</div>
  </div>
  <div class="abs" style="left:170px;top:600px;width:740px;height:580px">
    <div style="position:absolute;left:0;right:0;top:170px;height:430px;background:#4c1a85;border-radius:8px"></div>
    <div style="position:absolute;left:0;right:0;top:-150px;height:320px;background:linear-gradient(180deg,#5b2299,#4c1a85);clip-path:polygon(0 100%,50% 0,100% 100%)"></div>
    <div style="position:absolute;left:298px;top:-176px;width:144px;height:144px;border-radius:50%;background:radial-gradient(circle at 38% 34%,#3fb3b0 0,#06737c 55%,#044a50 100%);box-shadow:0 8px 16px rgba(0,0,0,.35),inset 0 -6px 12px rgba(0,0,0,.3);display:flex;align-items:center;justify-content:center">
      <div style="width:96px;height:96px;border-radius:50%;border:4px solid rgba(255,255,255,.28);box-shadow:inset 0 3px 6px rgba(0,0,0,.25)"></div></div>
    <div style="position:absolute;left:90px;right:90px;top:30px;height:420px;background:#fff;border-radius:22px;box-shadow:0 -10px 40px rgba(0,0,0,.2);display:flex;flex-direction:column;align-items:center;padding-top:44px">
      <img src="assets/logo-full.png" style="width:330px"></div>
    <div style="position:absolute;left:0;right:0;top:300px;height:300px;background:linear-gradient(180deg,#6b2ba6,#56208f);clip-path:polygon(0 0,50% 55%,100% 0,100% 100%,0 100%);border-radius:0 0 8px 8px;box-shadow:0 -4px 0 rgba(0,0,0,.05)"></div>
    <div style="position:absolute;left:0;right:0;top:300px;height:300px;clip-path:polygon(0 0,50% 55%,100% 0,100% 100%,0 100%);background:linear-gradient(160deg,rgba(255,255,255,.08),rgba(0,0,0,.15))"></div>
    <div style="position:absolute;left:-40px;right:-40px;bottom:-60px;height:80px;background:radial-gradient(50% 50% at 50% 50%,rgba(40,10,70,.35),transparent);z-index:-1"></div>
  </div>
  <div class="abs" style="left:0;right:0;top:1236px;text-align:center">
    <div style="font-weight:600;font-size:36px">Bring Wystak to your counter. DM us <span style="color:var(--violet);font-weight:700">“STACK”</span>.</div>
  </div>'''))


CHROME, IS_SHELL = find_chrome()
only = {int(a) for a in sys.argv[1:]}
for i, html in enumerate(slides, 1):
    if only and i not in only: continue
    p = HERE / f"_slide{i:02d}.html"; p.write_text(html)
    png = OUT / f"wystak-launch-{i:02d}.png"
    if IS_SHELL:
        args = [CHROME, "--window-size=1080,1350"]
    else:
        args = [CHROME, "--headless=new", "--window-size=1080,1700"]
    subprocess.run(args + ["--no-sandbox", "--disable-gpu", "--hide-scrollbars", "--force-device-scale-factor=1",
                    "--allow-file-access-from-files", "--virtual-time-budget=3000", f"--screenshot={png}", p.as_uri()],
                   check=True, capture_output=True, timeout=120)
    if not IS_SHELL:
        from PIL import Image
        Image.open(png).crop((0, 0, 1080, 1350)).save(png)
    p.unlink()
    print("ok", png.name)
