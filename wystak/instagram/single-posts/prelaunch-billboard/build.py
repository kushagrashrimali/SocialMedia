"""WYSTAK pre-launch billboard posters: four options, each 1080x1900 (the billboard screen is about 0.57 portrait).

A  The Slit      - a torn paper sheet with only slivers of the three card colours showing (flat 2D, reads as 3D).
B  Monoliths     - three glowing cards standing on a glossy black floor, "COMING SOON" in huge type.
C  Loading       - "STACKING UP..." with a chunky progress bar built from the three card colours.
D  Floating stack - an isometric stack of three cards (CSS 3D) with a "GUESS WHAT'S STACKING UP." headline.

Built for a billboard: very few words, huge type, high contrast, nothing about the product, and only slivers of the
brand (colours, the wordmark in the foot). Run: python3 build.py [a|b|c|d ...]
"""
import sys, math, random, pathlib, subprocess
from PIL import Image
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent.parent / "carousels" / "_common"))
from common import find_chrome

W, H = 1080, 1900
NAVY, VIOLET, TEAL = ("#2e63d6", "#0a2860"), ("#a65df0", "#6b2ba6"), ("#27d3d1", "#06737c")

FONTS = """
@font-face{font-family:K;src:url(assets/krona-one-latin-400-normal.woff2)}
@font-face{font-family:I9;src:url(assets/inter-latin-900-normal.woff2)}
@font-face{font-family:AB;src:url(assets/archivo-black-latin-400-normal.woff2)}
@font-face{font-family:P;src:url(assets/poppins-latin-500-normal.woff2);font-weight:500}
@font-face{font-family:P;src:url(assets/poppins-latin-600-normal.woff2);font-weight:600}
@font-face{font-family:P;src:url(assets/poppins-latin-700-normal.woff2);font-weight:700}
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:1080px;height:1900px;overflow:hidden}
.abs{position:absolute}
"""

def page(body, bg, extra_css=""):
    return f'<!doctype html><html><head><meta charset="utf-8"><style>{FONTS}body{{background:{bg}}}{extra_css}</style></head><body>{body}</body></html>'

GRAIN = ("data:image/svg+xml;utf8,<svg xmlns=%27http://www.w3.org/2000/svg%27 width=%27500%27 height=%27500%27><filter id=%27n%27><feTurbulence type=%27fractalNoise%27 "
         "baseFrequency=%27.85%27 numOctaves=%273%27 stitchTiles=%27stitch%27/><feColorMatrix type=%27saturate%27 values=%270%27/></filter><rect width=%27100%25%27 height=%27100%25%27 filter=%27url(%2523n)%27/></svg>")
grain = lambda op, blend: f"<div class='abs' style='inset:0;background:url(\"{GRAIN}\");opacity:{op};mix-blend-mode:{blend};pointer-events:none'></div>"

WORDMARK_PILL = '<div class="abs" style="left:0;right:0;bottom:92px;display:flex;justify-content:center"><div style="height:84px;padding:0 44px;border-radius:42px;background:#fff;display:flex;align-items:center;box-shadow:0 14px 40px rgba(0,0,0,.25)"><img src="assets/logo-wordmark.png" style="height:44px"></div></div>'


# =================================================== A  The Slit (torn paper) ====================
def fbm(x, seed, amp, base_freq=0.01, octaves=3):
    v, a, f = 0.0, amp, base_freq
    r = random.Random(seed)
    for _ in range(octaves):
        v += a * math.sin(x * f * 2 * math.pi + r.uniform(0, 6.28)); a *= 0.55; f *= 2.1
    return v
jag = lambda i, seed, amp: random.Random(i * 7919 + seed).uniform(-amp, amp)
fmt = lambda pts: " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)

def poster_a():
    XR = 744                                   # where the slit meets the roll
    top_y = lambda x: 890 + fbm(x, 3, 11) + 7 * math.sin(x / 83.0)
    bot_y = lambda x: 1236 - 0.05 * x + fbm(x, 9, 9) + 5 * math.sin(x / 61.0)
    xs = list(range(-10, XR + 1, 4))
    tp = [(x, top_y(x) + jag(x, 1, 1.2)) for x in xs]
    bp = [(x, bot_y(x) + jag(x, 2, 1.2)) for x in xs]
    hole = "M " + fmt(tp[:1]) + " L " + fmt(tp) + f" L {XR+40},{tp[-1][1]:.1f} L {XR+40},{bp[-1][1]+20:.1f} L " + fmt(list(reversed(bp))) + " Z"
    above = f"M -20,-20 L {W+20},-20 L {W+20},{tp[-1][1]:.1f} L {XR},{tp[-1][1]:.1f} L " + fmt(list(reversed(tp))) + " Z"
    below = f"M -20,{H+20} L {W+20},{H+20} L {W+20},{bp[-1][1]:.1f} L {XR},{bp[-1][1]:.1f} L " + fmt(list(reversed(bp))) + " Z"
    def rim(pts, d, seed, a, b):
        inner = [(x, y + d * (a + (b - a) * (0.5 + 0.5 * math.sin(x / 31.0 + seed)) + abs(jag(x, seed, 4)))) for x, y in pts]
        return "M " + fmt(pts) + " L " + fmt(list(reversed(inner))) + " Z"
    rim_t, rim_b = rim(tp, -1, 1.3, 9, 24), rim(bp, +1, 4.1, 7, 18)
    RX0, RX1, RT, RB = 706, 1008, 842, 1296
    rtp = [(x, RT + 14 * math.sin(x / 40.0) + fbm(x, 21, 7, 0.02, 3) + jag(x, 4, 3)) for x in range(RX0, RX1 + 1, 5)]
    ys = list(range(RT, RB + 1, 10))
    lp = [(RX0 + 12 * math.sin(y / 120.0) + fbm(y, 31, 6, 0.012, 2) - 8 * (1 - (y - RT) / (RB - RT)), y) for y in ys]
    rp = [(RX1 - 10 * (y - RT) / (RB - RT) + 7 * math.sin(y / 97.0) + fbm(y, 41, 5, 0.012, 2), y) for y in ys]
    roll = "M " + fmt(rtp) + " L " + fmt(rp[2:]) + f" L {rp[-1][0]-10:.1f},{RB+8} L {lp[-1][0]+10:.1f},{RB+8} L " + fmt(list(reversed(lp[2:]))) + " Z"
    roll_rim = "M " + fmt(rtp) + " L " + fmt([(x, y + 20 + abs(jag(x, 12, 6))) for x, y in reversed(rtp)]) + " Z"
    cx = (RX0 + RX1) / 2 - 8
    card = lambda c, x, y, rot, w=240, h=470: (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="52" fill="url(#g{c[1][1:]})" transform="rotate({rot} {x + w/2} {y + h/2})"/>')
    defs = "".join(f'<linearGradient id="g{c[1][1:]}" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{c[0]}"/><stop offset="1" stop-color="{c[1]}"/></linearGradient>' for c in (NAVY, VIOLET, TEAL))
    svg = f"""<svg class="abs" style="left:0;top:0" width="{W}" height="{H}" viewBox="0 0 {W} {H}"><defs>{defs}
      <filter id="paper" x="0" y="0" width="100%" height="100%"><feTurbulence type="fractalNoise" baseFrequency="0.035" numOctaves="3" seed="5" result="broad"/>
        <feTurbulence type="fractalNoise" baseFrequency="0.85 0.55" numOctaves="3" seed="8" result="fine"/>
        <feComposite in="broad" in2="fine" operator="arithmetic" k1="0" k2="0.55" k3="0.45" k4="0" result="mix"/>
        <feDiffuseLighting in="mix" lighting-color="#ffffff" surfaceScale="1.6" diffuseConstant="1.05"><feDistantLight azimuth="225" elevation="62"/></feDiffuseLighting></filter>
      <filter id="b14" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="14"/></filter>
      <filter id="b6" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="5"/></filter>
      <filter id="b24" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="22"/></filter>
      <filter id="b60" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="46"/></filter>
      <filter id="rough" x="-5%" y="-30%" width="110%" height="160%"><feTurbulence type="fractalNoise" baseFrequency="0.05 0.13" numOctaves="3" seed="2" result="n"/>
        <feDisplacementMap in="SourceGraphic" in2="n" scale="17" xChannelSelector="R" yChannelSelector="G"/></filter>
      <mask id="hm" maskUnits="userSpaceOnUse" x="0" y="0" width="{W}" height="{H}"><path d="{hole}" fill="#fff" filter="url(#rough)"/></mask>
      <linearGradient id="sheet" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#f1eaf7"/><stop offset=".55" stop-color="#e6dcef"/><stop offset="1" stop-color="#d6c9e4"/></linearGradient>
      <linearGradient id="rollg" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#bfb1d0"/><stop offset=".10" stop-color="#e2d9ee"/><stop offset=".26" stop-color="#fcf9ff"/><stop offset=".48" stop-color="#ebe3f4"/><stop offset=".74" stop-color="#cdc0df"/><stop offset=".92" stop-color="#a99bc0"/><stop offset="1" stop-color="#b8abcb"/></linearGradient>
      <radialGradient id="void" cx="50%" cy="50%" r="70%"><stop offset="0" stop-color="#1b1236"/><stop offset="1" stop-color="#07040f"/></radialGradient></defs>
      <rect width="{W}" height="{H}" fill="url(#sheet)"/>
      <g mask="url(#hm)">
        <rect x="0" y="780" width="{W}" height="560" fill="url(#void)"/>
        <ellipse cx="400" cy="1090" rx="420" ry="260" fill="#6b2ba6" opacity=".35" filter="url(#b60)"/>
        {card(NAVY, 90, 930, -10)}{card(VIOLET, 290, 905, -2)}{card(TEAL, 490, 935, 9)}
        <path d="{above}" fill="#05030c" opacity=".75" filter="url(#b14)" transform="translate(0,26)"/>
        <path d="{above}" fill="#05030c" opacity=".6" filter="url(#b6)" transform="translate(0,8)"/>
        <path d="{below}" fill="#05030c" opacity=".35" filter="url(#b14)" transform="translate(0,-10)"/>
        <path d="{roll}" fill="#05030c" opacity=".6" filter="url(#b24)" transform="translate(-26,16)"/></g>
      <path d="{rim_t}" fill="#fcf9ff" filter="url(#rough)"/><path d="{rim_b}" fill="#faf7fe" filter="url(#rough)"/>
      <path d="{roll}" fill="#150b2a" opacity=".35" filter="url(#b24)" transform="translate(14,34)"/>
      <path d="{roll}" fill="url(#rollg)"/><path d="{roll_rim}" fill="#fdfbff" filter="url(#rough)"/>
      <path d="M {RX0+40},{RT+40} C {RX0+90},{RT+4} {RX1-70},{RT+4} {RX1-36},{RT+44}" stroke="#cabcdc" stroke-width="3" fill="none" opacity=".8"/>
      <ellipse cx="{RX0+105}" cy="{(RT+RB)/2}" rx="26" ry="330" fill="#fff" opacity=".35" filter="url(#b14)"/>
      <ellipse cx="{cx}" cy="{RB-6}" rx="150" ry="40" fill="#efe8f7" stroke="#bfb1d2" stroke-width="3"/>
      <ellipse cx="{cx+6}" cy="{RB-4}" rx="118" ry="30" fill="none" stroke="#c9bcda" stroke-width="2.6"/>
      <ellipse cx="{cx+14}" cy="{RB-2}" rx="84" ry="21" fill="none" stroke="#d3c7e2" stroke-width="2.4"/>
      <ellipse cx="{cx+22}" cy="{RB}" rx="46" ry="11" fill="#d9cde7" stroke="#bfb1d2" stroke-width="2"/>
      <rect width="{W}" height="{H}" filter="url(#paper)" style="mix-blend-mode:multiply" opacity=".55"/></svg>"""
    body = svg + """
    <div class="abs" style="left:96px;top:250px;font-family:K;font-size:96px;line-height:1.14;letter-spacing:-.01em;color:#6b2ba6;white-space:nowrap">SOMETHING<br>IS STACKING<br>UP…</div>
    <div class="abs" style="left:96px;top:1420px;font-family:K;font-size:84px;line-height:1.1;color:#150b2a;white-space:nowrap">COMING<br>SOON.</div>
    <div class="abs" style="left:100px;top:1700px;font-family:P;font-weight:600;font-size:34px;letter-spacing:.16em;color:#150b2a">WWW.WYSTAK.COM</div>
    <div class="abs" style="inset:0;background:radial-gradient(120% 90% at 15% 8%,rgba(255,255,255,.35),transparent 55%),radial-gradient(110% 80% at 100% 100%,rgba(70,40,110,.22),transparent 60%);pointer-events:none"></div>"""
    return page(body, "#e9e1f1")


# =================================================== B  Monoliths ================================
def poster_b():
    def mono(c, x, rot, lift):
        w, h = 270, 760
        return (f'<div class="abs" style="left:{x}px;top:{440 + lift}px;width:{w}px;height:{h}px;border-radius:64px;transform:rotate({rot}deg);'
                f'background:linear-gradient(160deg,{c[0]},{c[1]});box-shadow:0 0 140px 20px {c[0]}88,0 0 40px {c[0]}aa,inset 0 0 0 4px rgba(255,255,255,.35),inset 22px 22px 60px rgba(255,255,255,.28),inset -24px -40px 70px rgba(0,0,0,.4)">'
                f'<div class="abs" style="left:34px;top:30px;right:34px;height:200px;border-radius:44px;background:linear-gradient(180deg,rgba(255,255,255,.4),rgba(255,255,255,0))"></div></div>')
    def refl(c, x, rot, lift):
        w, h = 270, 760
        return (f'<div class="abs" style="left:{x}px;top:{440 + lift + h + 20}px;width:{w}px;height:{h}px;border-radius:64px;transform:scaleY(-1) rotate({rot}deg);'
                f'background:linear-gradient(160deg,{c[0]},{c[1]});opacity:.28;-webkit-mask-image:linear-gradient(180deg,#000 0%,transparent 45%);filter:blur(3px)"></div>')
    cards = [(NAVY, 105, -9, 40), (VIOLET, 405, 0, 0), (TEAL, 705, 9, 40)]
    body = ('<div class="abs" style="inset:0;background:radial-gradient(70% 38% at 50% 52%,#241448 0%,#0c0718 55%,#040208 100%)"></div>'
            '<div class="abs" style="left:0;right:0;top:1340px;bottom:0;background:linear-gradient(180deg,#0a0614,#030107)"></div>'
            + "".join(refl(c, x - 0, r, l) for c, x, r, l in cards) + "".join(mono(c, x, r, l) for c, x, r, l in cards) +
            '<div class="abs" style="left:0;right:0;top:140px;text-align:center;font-family:P;font-weight:600;font-size:40px;letter-spacing:.34em;color:rgba(255,255,255,.8)">SOMETHING IS STACKING UP</div>'
            '<div class="abs" style="left:0;right:0;top:1250px;text-align:center;font-family:I9;font-size:232px;line-height:.92;letter-spacing:-.045em;color:#fff;text-shadow:0 0 60px rgba(150,110,255,.55)">COMING<br>SOON</div>'
            + WORDMARK_PILL.replace("bottom:92px", "bottom:70px") + grain(.14, "soft-light"))
    return page(body, "#05030a")


# =================================================== C  Loading ==================================
def poster_c():
    seg = lambda c, w, r: f'<div style="height:100%;width:{w}px;background:linear-gradient(180deg,{c[0]},{c[1]});{r}"></div>'
    bar = ('<div class="abs" style="left:96px;top:1040px;width:888px;height:150px;border-radius:75px;background:#fff;box-shadow:0 30px 60px rgba(40,10,80,.45),inset 0 6px 14px rgba(40,10,80,.25);padding:14px">'
           '<div style="height:100%;width:640px;border-radius:61px;overflow:hidden;display:flex;position:relative;box-shadow:0 0 40px rgba(255,255,255,.5)">'
           + seg(NAVY, 215, "") + seg(VIOLET, 215, "") + seg(TEAL, 210, "") +
           '<div class="abs" style="left:0;right:0;top:0;height:46%;background:linear-gradient(180deg,rgba(255,255,255,.45),rgba(255,255,255,0))"></div></div></div>')
    body = ('<div class="abs" style="inset:0;background:radial-gradient(90% 55% at 30% 20%,#9446d6 0%,#6b2ba6 45%,#3a1166 100%)"></div>'
            '<div class="abs" style="left:96px;top:330px;font-family:AB;font-size:158px;line-height:1.0;letter-spacing:-.02em;color:#fff;text-shadow:0 14px 0 rgba(30,6,60,.35)">STACKING<br>UP…</div>'
            + bar +
            '<div class="abs" style="left:96px;top:1290px;font-family:AB;font-size:112px;line-height:1;color:#5fd4cf;white-space:nowrap">COMING SOON</div>'
            + WORDMARK_PILL + grain(.16, "soft-light"))
    return page(body, "#6b2ba6")


# =================================================== D  Floating stack (CSS 3D) ===================
def poster_d():
    def card(c, z, label):
        layers = "".join(f'<div class="abs" style="inset:0;border-radius:44px;background:{c[1]};transform:translateZ({z - k * 2}px)"></div>' for k in range(1, 9))
        face = (f'<div class="abs" style="inset:0;border-radius:44px;transform:translateZ({z}px);background:linear-gradient(150deg,{c[0]},{c[1]});'
                f'box-shadow:inset 0 0 0 4px rgba(255,255,255,.35),inset 24px 24px 60px rgba(255,255,255,.25)">'
                f'<div class="abs" style="left:44px;top:40px;width:84px;height:84px;border-radius:50%;background:rgba(255,255,255,.28)"></div>'
                f'<div class="abs" style="left:44px;right:44px;bottom:48px;height:14px;border-radius:7px;background:rgba(255,255,255,.35)"></div>'
                f'<div class="abs" style="left:44px;width:46%;bottom:80px;height:14px;border-radius:7px;background:rgba(255,255,255,.28)"></div></div>')
        return f'<div class="abs" style="left:0;top:0;width:560px;height:360px;transform-style:preserve-3d">{layers}{face}</div>'
    body = ('<div class="abs" style="inset:0;background:radial-gradient(80% 50% at 50% 62%,#ffffff 0%,#efe6fb 45%,#dccbf3 100%)"></div>'
            '<div class="abs" style="left:96px;top:150px;font-family:P;font-weight:700;font-size:120px;line-height:1.04;letter-spacing:-.03em;color:#26104f;white-space:nowrap">GUESS WHAT’S<br>STACKING UP.</div>'
            '<div class="abs" style="left:120px;top:1450px;width:840px;height:200px;border-radius:50%;background:radial-gradient(closest-side,rgba(60,20,110,.55),rgba(60,20,110,0));filter:blur(14px)"></div>'
            '<div class="abs" style="left:260px;top:880px;width:560px;height:360px;perspective:2200px;perspective-origin:50% 40%;transform:scale(1.38)">'
            '<div class="abs" style="left:0;top:0;width:560px;height:360px;transform-style:preserve-3d;transform:rotateX(58deg) rotateZ(-34deg)">'
            + card(TEAL, 0, "") + card(VIOLET, 120, "") + card(NAVY, 240, "") + '</div></div>'
            '<div class="abs" style="left:96px;top:1640px;font-family:P;font-weight:700;font-size:64px;letter-spacing:.02em;color:#6b2ba6">COMING SOON</div>'
            '<div class="abs" style="left:98px;top:1730px;font-family:P;font-weight:600;font-size:32px;letter-spacing:.16em;color:#26104f">WWW.WYSTAK.COM</div>'
            + grain(.10, "multiply"))
    return page(body, "#efe6fb")


OPTIONS = {"a": poster_a, "b": poster_b, "c": poster_c, "d": poster_d}


def render_html(html, out):
    chrome, is_shell = find_chrome()
    f = HERE / "_poster.html"; f.write_text(html)
    args = [chrome, f"--window-size={W},{H}"] if is_shell else [chrome, "--headless=new", f"--window-size={W},{H + 400}"]
    subprocess.run(args + ["--no-sandbox", "--disable-gpu", "--hide-scrollbars", "--force-device-scale-factor=1", "--allow-file-access-from-files",
                           "--virtual-time-budget=5000", f"--screenshot={out}", f.as_uri()], check=True, capture_output=True, timeout=240)
    Image.open(out).convert("RGB").crop((0, 0, W, H)).save(out); f.unlink()


if __name__ == "__main__":
    which = [a for a in sys.argv[1:] if a in OPTIONS] or list(OPTIONS)
    out = HERE / "slides"; out.mkdir(exist_ok=True)
    for k in which:
        render_html(OPTIONS[k](), out / f"wystak-billboard-{k}.png"); print("ok", k)
