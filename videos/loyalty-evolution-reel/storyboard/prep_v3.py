"""Prepare v3 footage: trim, crop 9:16 from 4K Mixkit sources, one shared warm editorial grade.

usage (from the project folder): python3 -I storyboard/prep_v3.py SRC_DIR
SRC_DIR holds the Mixkit downloads named <id>.mp4 (URLs in assets/MANIFEST.md).
"""
import pathlib, subprocess, sys

P = pathlib.Path(__file__).resolve().parent.parent
SRC = pathlib.Path(sys.argv[1])
GRADE = ("eq=saturation=0.9:contrast=1.04:gamma=1.02,colorbalance=rs=0.03:gs=0.0:bs=-0.035:rh=0.02:bh=-0.02,"
         "curves=all='0/0.03 0.5/0.51 1/0.98',vignette=PI/7")
# out name, source id, in point, duration, crop centre (fraction of width)
SHOTS = [
    ("v3-open", "41220", 9.0, 2.75, 0.44),
    ("v3-pay", "41222", 1.0, 3.85, 0.40),
    ("v3-barista", "205", 1.0, 2.2, 0.70),
    ("v3-walkin", "39948", 2.6, 1.15, 0.55),
    ("v3-purchase", "41229", 1.6, 1.15, 0.42),
    ("v3-pour", "41859", 2.6, 1.45, 0.45),
    ("v3-notice", "43257", 4.6, 2.25, 0.66),
]
for out, sid, t0, dur, cx in SHOTS:
    src = SRC / f"{sid}.mp4"
    w, h = map(int, subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height",
                                     "-of", "csv=p=0", str(src)], capture_output=True, text=True, check=True).stdout.split(",")[:2])
    cw = int(h * 9 / 16) // 2 * 2
    x = int(min(max(cx * w - cw / 2, 0), w - cw))
    vf = f"crop={cw}:{h}:{x}:0,scale=1080:1920:flags=lanczos,fps=30,{GRADE},format=yuv420p"
    subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-ss", str(t0), "-t", str(dur), "-i", str(src), "-vf", vf,
                    "-an", "-c:v", "libx264", "-preset", "slow", "-crf", "17", "-movflags", "+faststart", str(P / f"assets/footage/{out}.mp4")], check=True)
    print(out, "<-", sid, f"{t0}s +{dur}s crop x={x}")
