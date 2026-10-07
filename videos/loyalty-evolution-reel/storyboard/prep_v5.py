"""Prepare v5 footage: every category (club, salon, boutique, bar, barber, cinema, concert, café).
Trim, crop 9:16 (or a widescreen window for low-resolution sources), one shared warm editorial grade.

usage (from the project folder): python3 -I storyboard/prep_v5.py SRC_DIR [only-these-outputs ...]
SRC_DIR holds the Mixkit downloads named <id>.mp4 (URLs in assets/MANIFEST.md).
"""
import pathlib, subprocess, sys
from PIL import Image, ImageDraw

P = pathlib.Path(__file__).resolve().parent.parent
SRC = pathlib.Path(sys.argv[1])
GRADE = ("eq=saturation=0.9:contrast=1.04:gamma=1.02,colorbalance=rs=0.03:gs=0.0:bs=-0.035:rh=0.02:bh=-0.02,"
         "curves=all='0/0.03 0.5/0.51 1/0.98',vignette=PI/7")
# out name, source id, in point, duration, crop centre (fraction of width) or "window", extra filter
SHOTS = [
    ("v5-club-open", "343", 0.2, 1.4, 0.45, ""),            # a couple dancing in red club light
    ("v5-salon-open", "43235", 1.2, 1.3, 0.52, ""),         # blow-dry at the barber's chair
    ("v5-cafe-open", "222", 1.4, 1.4, 0.57, ""),            # a cup handed across the counter
    ("v5-boutique", "51217", 7.4, 1.85, 0.52, ""),          # an assistant shows a gown's fabric
    ("v5-bar", "4295", 0.5, 1.65, 0.48, ",unsharp=5:5:0.6"),  # a cocktail poured at the bar counter
    ("v5-barber", "40126", 7.0, 2.6, 0.5, ""),              # barber at work, client in the chair (vertical source)
    ("v5-cinema", "33312", 1.4, 1.55, "window", ""),        # cinema audience with popcorn (720p source: widescreen window)
    ("v5-boutique-browse", "51228", 2.2, 1.55, 0.5, ""),    # a customer flips through the rail (vertical source)
    ("v5-pour", "41859", 2.6, 1.9, 0.45, ""),               # a cappuccino served
    ("v5-birthday", "41860", 0.95, 3.75, 0.24, ""),         # café counter, cup from the machine
    ("v5-concert", "4188", 11.4, 1.35, 0.45, ",unsharp=5:5:0.5"),  # festival crowd, smoke cannons over the stage
    ("v5-club", "343", 4.55, 1.25, 0.45, ""),              # dancing in red club light, a second angle
]
MASK = P / "storyboard/frames/window-mask.png"


def window_mask(w, h, r):
    MASK.parent.mkdir(exist_ok=True)
    m = Image.new("L", (w, h), 0)
    ImageDraw.Draw(m).rounded_rectangle([0, 0, w - 1, h - 1], r, fill=255)
    m.save(MASK)


for out, sid, t0, dur, cx, extra in [x for x in SHOTS if len(sys.argv) < 3 or x[0] in sys.argv[2:]]:
    src = SRC / f"{sid}.mp4"
    w, h = map(int, subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height",
                                     "-of", "csv=p=0", str(src)], capture_output=True, text=True, check=True).stdout.split(",")[:2])
    dst = str(P / f"assets/footage/{out}.mp4")
    enc = ["-an", "-c:v", "libx264", "-preset", "slow", "-crf", "17", "-movflags", "+faststart", dst]
    if cx == "window":
        # the shot sits in a rounded widescreen window over a soft, dimmed enlargement of itself
        cw = int(h * 4 / 3) // 2 * 2; cx0 = (w - cw) // 2
        fw = 1000; fh = round(fw * 3 / 4 / 2) * 2; window_mask(fw, fh, 44)
        fc = (f"[0:v]fps=30,{GRADE}[g];[g]split[a][b];"
              f"[a]crop=iw:ih*0.32:0:0,scale=1080:1920,boxblur=70:3,eq=brightness=-0.06:saturation=1.35[bg];"
              f"[b]crop={cw}:{h}:{cx0}:0,scale={fw}:{fh}:flags=lanczos,unsharp=5:5:0.5,format=rgba[fg0];[1:v]format=gray[m];[fg0][m]alphamerge[fg];"
              f"[bg][fg]overlay=40:250,format=yuv420p[v]")
        cmd = ["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-ss", str(t0), "-t", str(dur), "-i", str(src), "-loop", "1", "-i", str(MASK),
               "-filter_complex", fc, "-map", "[v]", "-t", str(dur)] + enc
    else:
        cw = int(h * 9 / 16) // 2 * 2
        x = int(min(max(cx * w - cw / 2, 0), w - cw))
        vf = f"crop={cw}:{h}:{x}:0,scale=1080:1920:flags=lanczos,fps=30,{GRADE}{extra},format=yuv420p"
        cmd = ["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-ss", str(t0), "-t", str(dur), "-i", str(src), "-vf", vf] + enc
    subprocess.run(cmd, check=True)
    print(out, "<-", sid, f"{t0}s +{dur}s", cx)
