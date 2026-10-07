"""Make the storyboard sheets for the loyalty reel.

Reads storyboard/shots.json, snapshots every shot at its poster time with the
HyperFrames CLI, and lays the stills out as labelled sheets (time range, the
line spoken, what we see, what moves), rendered with headless Chromium.

usage (from the project folder):  python3 storyboard/make_sheets.py
"""
import glob, json, os, pathlib, shutil, subprocess, sys

HERE = pathlib.Path(__file__).resolve().parent
PROJECT = HERE.parent
PER_SHEET = 15
COLS = 5


def find_chrome():
    if os.environ.get("CHROME"):
        return os.environ["CHROME"]
    shells = glob.glob("/opt/pw-browsers/chromium_headless_shell-*/*/headless_shell")
    if shells:
        return shells[0]
    for n in ("google-chrome", "chromium", "chromium-browser", "chrome"):
        if shutil.which(n):
            return shutil.which(n)
    raise SystemExit("Chrome not found; set CHROME=/path/to/chrome")


def tc(t):
    m, s = divmod(t, 60)
    return f"{int(m)}:{s:04.1f}"


def write_storyboard_md(shots):
    """Mirror shots.json into the project's STORYBOARD.md (HyperFrames storyboard format)."""
    lines = ["---", "format: 1080x1920", "duration: 44s",
             'message: "India already went digital on loyalty. Wystak gives it a place to live: the wallet."',
             "arc: Hook → Recognition → Data → WhatsApp → Everywhere → App fatigue → Silence → Wallet → Wystak",
             "audience: Indian café, restaurant, salon and shop owners", "mode: collaborative", "---", ""]
    for s in shots:
        lines += [f"## Frame {s['id']} — {tc(s['start'])}–{tc(s['end'])}", "",
                  f"- scene: {s['see']}", f"- duration: {s['end'] - s['start']:.2f}s", f"- poster: {s['poster']:.2f}",
                  "- transition_in: cut", "- status: built",
                  f"- voiceover: {s['vo'] or '(silence)'}", "", f"Moves: {s['moves']}", ""]
    (PROJECT / "STORYBOARD.md").write_text("\n".join(lines))


def main():
    shots = json.load(open(HERE / "shots.json"))
    write_storyboard_md(shots)
    frames = HERE / "frames"
    if frames.exists():
        shutil.rmtree(frames)
    at = ",".join(f"{s['poster']:.2f}" for s in shots)
    subprocess.run(["npx", "--yes", "hyperframes@0.8.139", "snapshot", "--at", at, "--no-end",
                    "--describe", "false", "--output", str(frames)], cwd=PROJECT, check=True)
    stills = sorted(frames.glob("frame-*.png"), key=lambda p: int(p.name.split("-")[1]))
    if len(stills) != len(shots):
        raise SystemExit(f"expected {len(shots)} stills, got {len(stills)}")
    fonts = (PROJECT / "assets/vendor/fonts").as_uri()
    css = f"""
@font-face{{font-family:A;src:url({fonts}/archivo-latin-600-normal.woff2);font-weight:600}}
@font-face{{font-family:A;src:url({fonts}/archivo-latin-500-italic.woff2);font-weight:500;font-style:italic}}
@font-face{{font-family:AB;src:url({fonts}/archivo-black-latin-400-normal.woff2)}}
@font-face{{font-family:M;src:url({fonts}/manrope-latin-500-normal.woff2);font-weight:500}}
@font-face{{font-family:M;src:url({fonts}/manrope-latin-700-normal.woff2);font-weight:700}}
@font-face{{font-family:P;src:url({fonts}/ibm-plex-mono-latin-500-normal.woff2)}}
*{{margin:0;padding:0;box-sizing:border-box}}
body{{background:#f7f5fa;color:#1a0b2e;font-family:M,sans-serif;width:1700px;padding:48px 40px 40px}}
h1{{font-family:AB;font-size:44px;letter-spacing:-.02em}}
.meta{{font-family:A;font-weight:600;font-size:17px;letter-spacing:.16em;text-transform:uppercase;color:#6b5d82;margin:10px 0 34px}}
.grid{{display:grid;grid-template-columns:repeat({COLS},1fr);gap:34px 26px}}
.cell img{{width:100%;aspect-ratio:9/16;display:block;border-radius:10px;background:#0b0410}}
.hd{{display:flex;justify-content:space-between;align-items:baseline;margin-top:12px}}
.no{{font-family:AB;font-size:22px}}
.t{{font-family:P;font-size:16px;color:#6b5d82}}
.vo{{font-family:A;font-style:italic;font-weight:500;font-size:19px;line-height:1.3;margin-top:8px;min-height:25px}}
.vo.silent{{color:#9c8fb3}}
.k{{font-family:A;font-weight:600;font-size:12px;letter-spacing:.16em;text-transform:uppercase;color:#6b5d82;margin-top:10px}}
.d{{font-size:15.5px;line-height:1.38;margin-top:3px;color:#2b1f3d}}
"""
    chrome = find_chrome()
    pages = [shots[i:i + PER_SHEET] for i in range(0, len(shots), PER_SHEET)]
    outs = []
    for pi, page in enumerate(pages, 1):
        cells = []
        for s in page:
            idx = shots.index(s)
            vo = s.get("vo") or "(no voice)"
            cells.append(f"""<div class="cell"><img src="{stills[idx].as_uri()}">
<div class="hd"><span class="no">{s['id']}</span><span class="t">{tc(s['start'])}–{tc(s['end'])}</span></div>
<div class="vo{' silent' if not s.get('vo') else ''}">{vo}</div>
<div class="k">On screen</div><div class="d">{s['see']}</div>
<div class="k">Moves</div><div class="d">{s['moves']}</div></div>""")
        html = f"""<!doctype html><html><head><meta charset="utf-8"><style>{css}</style></head><body>
<h1>The next place for loyalty · storyboard</h1>
<div class="meta">Wystak reel · 1080×1920 · 44.0s · sheet {pi} of {len(pages)} · shots {page[0]['id']}–{page[-1]['id']}</div>
<div class="grid">{''.join(cells)}</div></body></html>"""
        src = HERE / f"sheet-{pi}.html"
        src.write_text(html)
        png = HERE / f"storyboard-{pi}.png"
        rows = (len(page) + COLS - 1) // COLS
        height = 150 + rows * 860
        subprocess.run([chrome, "--headless=new", f"--window-size=1700,{height}", "--no-sandbox", "--disable-gpu",
                        "--hide-scrollbars", "--force-device-scale-factor=1", "--allow-file-access-from-files",
                        "--virtual-time-budget=4000", f"--screenshot={png}", src.as_uri()],
                       check=True, capture_output=True)
        from PIL import Image
        im = Image.open(png).convert("RGB")
        jpg = HERE / f"storyboard-{pi}.jpg"
        im.save(jpg, quality=88)
        png.unlink()
        src.unlink()
        outs.append(jpg)
    print("\n".join(str(o.relative_to(PROJECT)) for o in outs))


if __name__ == "__main__":
    sys.exit(main())
