"""Prepare licensed source media for the reel: trim, crop to 9:16, scale to 1080x1920, encode.

Reads storyboard/media.json:
  [{"out": "assets/footage/02-scan.mp4", "src": "/path/to/source.mp4", "in": 3.2, "dur": 2.4,
    "cx": 0.5, "zoom": 1.0}, ...]
  - in/dur: source seconds to keep (video only); omit for stills
  - cx, cy: crop centre as a fraction of the source frame (default 0.5)
  - zoom: extra punch-in on top of the 9:16 cover crop (default 1.0)
Stills (.jpg/.png sources) are written as 2160px-tall JPGs cropped to 9:16.
usage (from the project folder):  python3 storyboard/prep_media.py [only-this-out ...]
"""
import json, pathlib, subprocess, sys

HERE = pathlib.Path(__file__).resolve().parent
PROJECT = HERE.parent


def probe(src):
    out = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
                          "stream=width,height", "-of", "csv=p=0", src], capture_output=True, text=True, check=True)
    w, h = out.stdout.strip().split(",")[:2]
    return int(w), int(h)


def crop_box(w, h, cx, cy, zoom):
    tw = min(w, h * 9 / 16) / zoom
    th = tw * 16 / 9
    if th > h:
        th = h / zoom
        tw = th * 9 / 16
    x = min(max(cx * w - tw / 2, 0), w - tw)
    y = min(max(cy * h - th / 2, 0), h - th)
    return int(tw) // 2 * 2, int(th) // 2 * 2, int(x), int(y)


def main(only):
    items = json.load(open(HERE / "media.json"))
    for it in items:
        if only and it["out"] not in only:
            continue
        src, out = it["src"], PROJECT / it["out"]
        out.parent.mkdir(parents=True, exist_ok=True)
        w, h = probe(src)
        cw, ch, x, y = crop_box(w, h, it.get("cx", 0.5), it.get("cy", 0.5), it.get("zoom", 1.0))
        is_still = src.lower().endswith((".jpg", ".jpeg", ".png", ".webp", ".tif", ".tiff"))
        if is_still:
            vf = f"crop={cw}:{ch}:{x}:{y},scale=-2:{min(2160, ch)}:flags=lanczos"
            cmd = ["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", src, "-vf", vf, "-q:v", "2", str(out)]
        else:
            vf = f"crop={cw}:{ch}:{x}:{y},scale=1080:1920:flags=lanczos,fps=30,format=yuv420p"
            cmd = ["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-ss", str(it.get("in", 0)), "-t", str(it["dur"]),
                   "-i", src, "-vf", vf, "-an", "-c:v", "libx264", "-preset", "slow", "-crf", "17",
                   "-movflags", "+faststart", str(out)]
        subprocess.run(cmd, check=True)
        print(f"{it['out']}  <-  {pathlib.Path(src).name}  crop {cw}x{ch}+{x}+{y}")


if __name__ == "__main__":
    main(set(sys.argv[1:]))
