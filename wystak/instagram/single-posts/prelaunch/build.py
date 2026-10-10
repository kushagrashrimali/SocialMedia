"""WYSTAK pre-launch teaser: a single image, 1080x1350. A torn-paper reveal: flat 2D, but it reads as 3D.

A pale lilac paper sheet is torn open and rolled back, and the supplied Wystak logo peeks through the opening.
The depth is an illusion built from: a ragged tear with a fibre rim, soft cast shadows under both torn edges,
a cylindrical roll of paper with layered ends, a paper-grain overlay, and a light falloff across the sheet.
Type: Krona One (headline), Poppins. No product information.
"""
import sys, math, random, pathlib, subprocess
from PIL import Image
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent.parent / "carousels" / "_common"))
from common import find_chrome

W, H = 1080, 1350
rnd = random.Random(11)


def fbm(x, seed, amp, base_freq=0.02, octaves=4):
    """Smooth fractal noise built from a few sines, for ragged edges."""
    v = 0.0; a = amp; f = base_freq
    r = random.Random(seed)
    for _ in range(octaves):
        v += a * math.sin(x * f * 2 * math.pi + r.uniform(0, 6.28))
        a *= 0.55; f *= 2.1
    return v


def jag(i, seed, amp):
    """Per-point jitter so the edge is fibrous rather than smooth."""
    return random.Random(i * 7919 + seed).uniform(-amp, amp)


# ---- the two torn edges across the opening --------------------------------------------------
X_ROLL = 748                                        # where the opening meets the roll
def top_y(x):
    return 512 + fbm(x, 3, 11, 0.010, 3) + 7 * math.sin(x / 83.0)
def bot_y(x):
    return 998 - 0.05 * x + fbm(x, 9, 9, 0.011, 3) + 5 * math.sin(x / 61.0)

STEP = 4
xs = list(range(-10, X_ROLL + 1, STEP))
top_pts = [(x, top_y(x) + jag(x, 1, 1.2)) for x in xs]
bot_pts = [(x, bot_y(x) + jag(x, 2, 1.2)) for x in xs]
fmt = lambda pts: " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)

hole_path = ("M " + fmt(top_pts[:1]) + " L " + fmt(top_pts) + f" L {X_ROLL + 40},{top_pts[-1][1]:.1f} L {X_ROLL + 40},{bot_pts[-1][1] + 20:.1f} L " + fmt(list(reversed(bot_pts))) + " Z")
above_top = f"M -20,-20 L {W + 20},-20 L {W + 20},{top_pts[-1][1]:.1f} L {X_ROLL},{top_pts[-1][1]:.1f} L " + fmt(list(reversed(top_pts))) + " Z"
below_bot = f"M -20,{H + 20} L {W + 20},{H + 20} L {W + 20},{bot_pts[-1][1]:.1f} L {X_ROLL},{bot_pts[-1][1]:.1f} L " + fmt(list(reversed(bot_pts))) + " Z"


def rim(pts, direction, seed, wmin=8, wmax=20):
    """A lighter, fibrous strip along a torn edge. direction -1 = into the paper above, +1 = into the paper below."""
    inner = [(x, y + direction * (wmin + (wmax - wmin) * (0.5 + 0.5 * math.sin(x / 31.0 + seed)) + abs(jag(x, seed, 4)))) for x, y in pts]
    return "M " + fmt(pts) + " L " + fmt(list(reversed(inner))) + " Z"


rim_top = rim(top_pts, -1, 1.3, 9, 24)
rim_bot = rim(bot_pts, +1, 4.1, 7, 18)
fibres_top = ""
fibres_bot = ""

# ---- the roll ----------------------------------------------------------------------------------
RX0, RX1 = 700, 1004                                   # roll left and right edges
RT, RB = 478, 1158                                     # roll top and bottom
roll_top_pts = [(x, RT + 14 * math.sin(x / 40.0) + fbm(x, 21, 7) + jag(x, 4, 3)) for x in range(RX0, RX1 + 1, 5)]
ys = list(range(int(RT), int(RB) + 1, 10))
left_pts = [(RX0 + 12 * math.sin(y / 120.0) + fbm(y, 31, 6, 0.012, 2) + 8 * (1 - (y - RT) / (RB - RT)) * -1, y) for y in ys]
right_pts = [(RX1 - 10 * (y - RT) / (RB - RT) + 7 * math.sin(y / 97.0) + fbm(y, 41, 5, 0.012, 2), y) for y in ys]
roll_body = ("M " + fmt(roll_top_pts) + " L " + fmt(right_pts[2:]) + " L " + f"{right_pts[-1][0] - 10:.1f},{RB + 8} L {left_pts[-1][0] + 10:.1f},{RB + 8} L " + fmt(list(reversed(left_pts[2:]))) + " Z")
roll_rim = "M " + fmt(roll_top_pts) + " L " + fmt([(x, y + 20 + abs(jag(x, 12, 6))) for x, y in reversed(roll_top_pts)]) + " Z"
roll_fibres = ""

CSS = f"""
@font-face{{font-family:K;src:url(assets/krona-one-latin-400-normal.woff2)}}
@font-face{{font-family:P;src:url(assets/poppins-latin-500-normal.woff2);font-weight:500}}
@font-face{{font-family:P;src:url(assets/poppins-latin-600-normal.woff2);font-weight:600}}
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:{W}px;height:{H}px;overflow:hidden;background:#e9e1f1}}
.abs{{position:absolute}}
"""

HTML = f"""<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head><body>
<svg class="abs" style="left:0;top:0" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
  <defs>
    <!-- paper grain: broad mottling plus fine fibres, lit from the top left -->
    <filter id="paper" x="0" y="0" width="100%" height="100%">
      <feTurbulence type="fractalNoise" baseFrequency="0.035" numOctaves="3" seed="5" result="broad"/>
      <feTurbulence type="fractalNoise" baseFrequency="0.85 0.55" numOctaves="3" seed="8" result="fine"/>
      <feComposite in="broad" in2="fine" operator="arithmetic" k1="0" k2="0.55" k3="0.45" k4="0" result="mix"/>
      <feDiffuseLighting in="mix" lighting-color="#ffffff" surfaceScale="1.6" diffuseConstant="1.05"><feDistantLight azimuth="225" elevation="62"/></feDiffuseLighting></filter>
    <filter id="blur14" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="14"/></filter>
    <filter id="blur6" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="5"/></filter>
    <filter id="blur24" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="22"/></filter>
    <filter id="rough" x="-5%" y="-30%" width="110%" height="160%">
      <feTurbulence type="fractalNoise" baseFrequency="0.05 0.13" numOctaves="3" seed="2" result="n"/>
      <feDisplacementMap in="SourceGraphic" in2="n" scale="17" xChannelSelector="R" yChannelSelector="G"/></filter>
    <mask id="holeMask" maskUnits="userSpaceOnUse" x="0" y="0" width="{W}" height="{H}"><path d="{hole_path}" fill="#fff" filter="url(#rough)"/></mask>
    <linearGradient id="sheet" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#f1eaf7"/><stop offset=".55" stop-color="#e6dcef"/><stop offset="1" stop-color="#d6c9e4"/></linearGradient>
    <linearGradient id="rollg" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="#bfb1d0"/><stop offset=".10" stop-color="#e2d9ee"/><stop offset=".26" stop-color="#fcf9ff"/><stop offset=".48" stop-color="#ebe3f4"/>
      <stop offset=".74" stop-color="#cdc0df"/><stop offset=".92" stop-color="#a99bc0"/><stop offset="1" stop-color="#b8abcb"/></linearGradient>
    <linearGradient id="whitesurf" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ddd9e6"/><stop offset=".25" stop-color="#fbfaff"/><stop offset=".8" stop-color="#ffffff"/><stop offset="1" stop-color="#e7e4ee"/></linearGradient>
  </defs>

  <!-- 1. the sheet of paper -->
  <rect width="{W}" height="{H}" fill="url(#sheet)"/>

  <!-- 2. the opening: a white surface underneath, with the logo peeking through, shaded by the torn edges -->
  <g mask="url(#holeMask)">
    <rect x="0" y="380" width="{W}" height="760" fill="url(#whitesurf)"/>
    <image href="assets/logo-mark.png" x="-24" y="548" width="730" height="475" preserveAspectRatio="xMidYMid meet"/>
    <path d="{above_top}" fill="#1a1030" opacity=".7" filter="url(#blur14)" transform="translate(0,30)"/>
    <path d="{above_top}" fill="#120a24" opacity=".6" filter="url(#blur6)" transform="translate(0,9)"/>
    <path d="{below_bot}" fill="#1a1030" opacity=".28" filter="url(#blur14)" transform="translate(0,-12)"/>
    <path d="{roll_body}" fill="#120a24" opacity=".5" filter="url(#blur24)" transform="translate(-26,16)"/>
  </g>

  <!-- 3. the fibrous torn edges (lighter than the paper, with loose fibres) -->
  <path d="{rim_top}" fill="#fcf9ff" filter="url(#rough)"/>
  <path d="{rim_bot}" fill="#faf7fe" filter="url(#rough)"/>
  <path d="{fibres_top}" stroke="#fbf8fe" stroke-width="1.6" stroke-linecap="round" fill="none"/>
  <path d="{fibres_bot}" stroke="#f9f5fd" stroke-width="1.6" stroke-linecap="round" fill="none"/>
  <path d="{above_top}" fill="none"/>

  <!-- 4. the paper rolled back at the right -->
  <path d="{roll_body}" fill="#150b2a" opacity=".35" filter="url(#blur24)" transform="translate(14,34)"/>
  <path d="{roll_body}" fill="url(#rollg)"/>
  <path d="{roll_rim}" fill="#fdfbff" filter="url(#rough)"/>
  <path d="{roll_fibres}" stroke="#fcfaff" stroke-width="1.6" stroke-linecap="round" fill="none"/>
  <!-- layers of the roll seen at the open top -->
  <path d="M {RX0 + 40},{RT + 40} C {RX0 + 90},{RT + 4} {RX1 - 70},{RT + 4} {RX1 - 36},{RT + 44}" stroke="#cabcdc" stroke-width="3" fill="none" opacity=".8"/>
  <path d="M {RX0 + 70},{RT + 60} C {RX0 + 120},{RT + 30} {RX1 - 100},{RT + 30} {RX1 - 70},{RT + 62}" stroke="#d6cae6" stroke-width="2.4" fill="none" opacity=".8"/>
  <!-- soft light on the roll and a crease where it curls under -->
  <ellipse cx="{RX0 + 105}" cy="{(RT + RB) / 2}" rx="26" ry="300" fill="#ffffff" opacity=".35" filter="url(#blur14)"/>
  <path d="M {RX0 + 30},{RB} C {RX0 + 10},{RB - 90} {RX0 + 60},{RB - 150} {RX0 + 120},{RB - 168}" stroke="#a899bd" stroke-width="3" fill="none" opacity=".5"/>
  <!-- the layered end of the roll, seen from below -->
  <ellipse cx="{(RX0 + RX1) / 2 - 8}" cy="{RB - 6}" rx="150" ry="40" fill="#efe8f7"/>
  <ellipse cx="{(RX0 + RX1) / 2 - 8}" cy="{RB - 6}" rx="150" ry="40" fill="none" stroke="#bfb1d2" stroke-width="3"/>
  <ellipse cx="{(RX0 + RX1) / 2 - 2}" cy="{RB - 4}" rx="118" ry="30" fill="none" stroke="#c9bcda" stroke-width="2.6"/>
  <ellipse cx="{(RX0 + RX1) / 2 + 6}" cy="{RB - 2}" rx="84" ry="21" fill="none" stroke="#d3c7e2" stroke-width="2.4"/>
  <ellipse cx="{(RX0 + RX1) / 2 + 14}" cy="{RB}" rx="46" ry="11" fill="#d9cde7" stroke="#bfb1d2" stroke-width="2"/>

  <!-- 5. grain: multiplied over everything so the print and the paper feel like one surface -->
  <rect width="{W}" height="{H}" filter="url(#paper)" style="mix-blend-mode:multiply" opacity=".55"/>
  <!-- light falloff across the sheet -->
  <rect width="{W}" height="{H}" fill="url(#vig)" opacity="0"/>
</svg>

<!-- type, printed on the paper (above the grain so it stays crisp, then lightly multiplied) -->
<div class="abs" style="left:108px;top:200px;font-family:K;font-size:76px;line-height:1.14;letter-spacing:-.01em;color:#6b2ba6;white-space:nowrap">SOMETHING<br>NEW IS<br>STACKING UP…</div>
<div class="abs" style="left:108px;top:1058px;font-family:P;font-weight:500;font-size:46px;letter-spacing:.01em;color:#150b2a">STAY TUNED!</div>
<div class="abs" style="left:110px;top:1120px;font-family:P;font-weight:500;font-size:25px;letter-spacing:.14em;color:#150b2a">WWW.WYSTAK.COM</div>
<div class="abs" style="left:0;top:0;width:{W}px;height:{H}px;background:radial-gradient(120% 90% at 15% 8%,rgba(255,255,255,.35) 0%,transparent 55%),radial-gradient(110% 80% at 100% 100%,rgba(70,40,110,.22) 0%,transparent 60%);pointer-events:none"></div>
</body></html>"""


def render(out):
    chrome, is_shell = find_chrome()
    html = HERE / "_poster.html"; html.write_text(HTML)
    args = [chrome, f"--window-size={W},{H}"] if is_shell else [chrome, "--headless=new", f"--window-size={W},{H + 400}"]
    subprocess.run(args + ["--no-sandbox", "--disable-gpu", "--hide-scrollbars", "--force-device-scale-factor=1", "--allow-file-access-from-files",
                           "--virtual-time-budget=4000", f"--screenshot={out}", html.as_uri()], check=True, capture_output=True, timeout=180)
    img = Image.open(out).convert("RGB").crop((0, 0, W, H)); img.save(out); html.unlink()


if __name__ == "__main__":
    slides = HERE / "slides"; slides.mkdir(exist_ok=True)
    render(slides / "wystak-prelaunch.png")
    print("ok", slides / "wystak-prelaunch.png")
