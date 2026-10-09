"""Shared helpers for the object-style Instagram posts: Chrome lookup, grain, QR, NFC, arrows and the slide renderer."""
import os, glob, shutil, subprocess, random, sys, pathlib


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


GRAIN = ("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='600' height='600'>"
         "<filter id='n'><feTurbulence type='fractalNoise' baseFrequency='.85' numOctaves='3' stitchTiles='stitch'/>"
         "<feColorMatrix type='saturate' values='0'/></filter><rect width='100%' height='100%' filter='url(%23n)'/></svg>")

RESET = """
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:1080px;height:1350px;overflow:hidden}
body{-webkit-font-smoothing:antialiased}
.slide{position:relative;width:1080px;height:1350px;overflow:hidden}
.abs{position:absolute}
.grain{position:absolute;inset:0;background:url("GRAIN");pointer-events:none;z-index:50}
.vig{position:absolute;inset:0;pointer-events:none;z-index:49}
""".replace("GRAIN", GRAIN)


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


def nfc(s, c):
    return (f'<svg width="{s}" height="{s}" viewBox="0 0 48 48" fill="none" stroke="{c}" stroke-width="4" stroke-linecap="round">'
            '<path d="M14 16 C18 20 18 28 14 32"/><path d="M21 11 C28 18 28 30 21 37"/><path d="M28 6 C38 16 38 32 28 42"/></svg>')


def arrow(w, h, d, color, sw=7, head=(0, 0, 0)):
    x, y, a = head
    return (f'<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}" fill="none" stroke="{color}" stroke-width="{sw}" '
            f'stroke-linecap="round" stroke-linejoin="round"><path d="{d}"/>'
            f'<g transform="translate({x} {y}) rotate({a})"><path d="M0 0 L-34 -16 M0 0 L-30 20"/></g></svg>')


def render(slides, here, prefix, argv):
    """Render each slide's HTML to slides/<prefix>-NN.png (1080x1350). argv: optional slide numbers."""
    here = pathlib.Path(here); out = here / "slides"; out.mkdir(exist_ok=True)
    chrome, is_shell = find_chrome()
    only = {int(a) for a in argv}
    for i, html in enumerate(slides, 1):
        if only and i not in only: continue
        p = here / f"_slide{i:02d}.html"; p.write_text(html)
        png = out / f"{prefix}-{i:02d}.png"
        args = [chrome, "--window-size=1080,1350"] if is_shell else [chrome, "--headless=new", "--window-size=1080,1700"]
        subprocess.run(args + ["--no-sandbox", "--disable-gpu", "--hide-scrollbars", "--force-device-scale-factor=1",
                        "--allow-file-access-from-files", "--virtual-time-budget=3000", f"--screenshot={png}", p.as_uri()],
                       check=True, capture_output=True, timeout=120)
        if not is_shell:
            from PIL import Image
            Image.open(png).crop((0, 0, 1080, 1350)).save(png)
        p.unlink()
        print("ok", png.name)
