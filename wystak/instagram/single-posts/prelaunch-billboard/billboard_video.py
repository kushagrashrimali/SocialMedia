"""WYSTAK pre-launch: the poster on the green-screen billboard, a 7-second seamless loop (720x1280, 30 fps, no audio).

The camera is static, so the screen is a fixed quad. Per frame the green is keyed (G well above R and B), the poster
is laid in through the key, so the lamp post and the people in front of the screen stay in front of it. The poster
is warped once at 2x and shrunk (clean edges). A faint light sweep crosses the screen once per loop and starts and
ends off the poster, and the loop closes by cross-fading the last frames into the first ones.

  python3 billboard_video.py <green_screen.mp4> [poster.png] [out.mp4] [start_seconds]
"""
import sys, subprocess, pathlib
import numpy as np
from PIL import Image, ImageFilter

HERE = pathlib.Path(__file__).resolve().parent
VW, VH, FPS = 720, 1280, 30
LOOP = 7 * FPS            # frames in the loop
XFADE = 22                # frames of cross-fade that close the loop
SS = 2                    # supersampling for the warp

# the screen's corners in video pixels (fitted to the key edges of the median frame): TL, TR, BR, BL
QUAD = [(121.1, 39.4), (541.5, 77.1), (584.8, 848.8), (104.8, 838.2)]


def perspective_coeffs(dst, src):
    """Coefficients for Image.transform(PERSPECTIVE): maps each output point (dst) back to its input point (src)."""
    A, b = [], []
    for (x, y), (u, v) in zip(dst, src):
        A.append([x, y, 1, 0, 0, 0, -u * x, -u * y]); b.append(u)
        A.append([0, 0, 0, x, y, 1, -v * x, -v * y]); b.append(v)
    return np.linalg.solve(np.array(A, float), np.array(b, float)).tolist()


def grow(quad, k):
    c = np.mean(quad, axis=0)
    return [tuple(c + (np.array(p) - c) * k) for p in quad]


def warp_poster(poster):
    """The poster in screen position, at video size: float RGB and a coverage mask (slightly larger than the screen)."""
    q = grow(QUAD, 1.012)
    w, h = poster.size
    dst = [(x * SS, y * SS) for x, y in q]
    src = [(0, 0), (w, 0), (w, h), (0, h)]
    # shrink the poster so the warp samples near 1:1 (the screen is about 420 px wide at 2x = 840)
    pre = poster.resize((round(w * 0.8), round(h * 0.8)), Image.LANCZOS)
    k = pre.width / w
    src = [(x * k, y * k) for x, y in src]
    co = perspective_coeffs(dst, src)
    big = pre.transform((VW * SS, VH * SS), Image.PERSPECTIVE, co, Image.BICUBIC)
    mask = Image.new("L", pre.size, 255).transform((VW * SS, VH * SS), Image.PERSPECTIVE, co, Image.BILINEAR)
    rgb = np.asarray(big.resize((VW, VH), Image.LANCZOS), np.float32) / 255
    cov = np.asarray(mask.resize((VW, VH), Image.LANCZOS), np.float32) / 255
    return rgb, cov


def blur_arr(a, sigma):
    """Separable gaussian blur of an (H, W, C) float array."""
    r = int(sigma * 3) + 1
    k = np.exp(-0.5 * (np.arange(-r, r + 1) / sigma) ** 2); k /= k.sum()
    out = a.astype(np.float32)
    for ax in (0, 1):
        pad = [(0, 0)] * 3; pad[ax] = (r, r)
        p = np.pad(out, pad, mode="edge")
        acc = np.zeros_like(out)
        for i, kv in enumerate(k):
            acc += kv * (p[i:i + out.shape[0]] if ax == 0 else p[:, i:i + out.shape[1]])
        out = acc
    return out


def green_plate(sample):
    """The empty screen as the camera sees it: the median over time keeps the screen and drops the people; holes
    where something static is in front (the lamp post) are filled from the green around them."""
    med = np.median(sample, axis=0).astype(np.float32) / 255
    spill = med[..., 1] - np.maximum(med[..., 0], med[..., 2])
    m = (spill > 0.45).astype(np.float32)
    m = np.asarray(Image.fromarray((m * 255).astype(np.uint8)).filter(ImageFilter.MinFilter(5)), np.float32) / 255  # erode
    num = med * m[..., None]
    plate = np.zeros_like(med)
    weight = np.zeros(m.shape, np.float32)
    for sig in (2.0, 7.0, 25.0):
        w = blur_arr(m[..., None], sig)[..., 0]
        p = blur_arr(num, sig) / np.maximum(w[..., None], 1e-4)
        take = (weight < 0.5) & (w > 0.02)
        plate[take] = p[take]; weight[take] = 1
    plate_spill = np.clip(plate[..., 1] - np.maximum(plate[..., 0], plate[..., 2]), 0.2, 1)
    return plate, plate_spill


def main():
    src = sys.argv[1]
    poster_path = sys.argv[2] if len(sys.argv) > 2 else str(HERE / "slides" / "wystak-billboard-cinematic.png")
    out = sys.argv[3] if len(sys.argv) > 3 else str(HERE / "slides" / "wystak-billboard-loop.mp4")
    start = float(sys.argv[4]) if len(sys.argv) > 4 else 1.0

    poster = Image.open(poster_path).convert("RGB")
    prgb, cov = warp_poster(poster)
    prgb = np.asarray(Image.fromarray((prgb * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(0.55)), np.float32) / 255
    # a billboard is lit from inside: lift the exposure a little
    prgb = np.clip(prgb * 1.18 + 0.012, 0, 1)

    yy, xx = np.mgrid[0:VH, 0:VW].astype(np.float32)
    diag = (xx * 0.55 + yy * 0.85)
    diag = (diag - diag.min()) / (diag.max() - diag.min())

    n_in = LOOP + XFADE
    rd = subprocess.run(["ffmpeg", "-v", "error", "-ss", str(start), "-i", src, "-an", "-frames:v", str(n_in),
                         "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True, check=True).stdout
    frames = np.frombuffer(rd, np.uint8).reshape(-1, VH, VW, 3)
    assert len(frames) >= n_in, f"only {len(frames)} frames after {start}s"

    enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{VW}x{VH}", "-r", str(FPS), "-i", "-",
                            "-c:v", "libx264", "-crf", "15", "-preset", "slow", "-pix_fmt", "yuv420p", "-movflags", "+faststart", out], stdin=subprocess.PIPE)
    rng = np.random.default_rng(3)
    plate, plate_spill = green_plate(frames[::10])
    # a few pixels around the screen, where the video's chroma bleeds the green outward
    rim_zone = np.asarray(Image.fromarray((cov > 0.02).astype(np.uint8) * 255).filter(ImageFilter.MaxFilter(9))) > 0
    for k in range(LOOP):
        if k < XFADE:   # the loop closes here: blend from the tail of the clip into its head
            wgt = (k / XFADE) ** 1.0
            f = (frames[LOOP + k].astype(np.float32) * (1 - wgt) + frames[k].astype(np.float32) * wgt) / 255
        else:
            f = frames[k].astype(np.float32) / 255
        r, g, b = f[..., 0], f[..., 1], f[..., 2]
        spill = g - np.maximum(r, b)
        # linear unmix against the local screen colour: pixel = a * screen + (1 - a) * foreground
        a = np.clip((spill / plate_spill - 0.04) / 0.92, 0, 1) * np.clip(cov * 1.5, 0, 1)
        # foreground over the screen = the frame with the screen colour taken out; the poster goes in where a is
        f = f - a[..., None] * plate
        f = np.clip(f, 0, 1)
        # clear any green left on the screen's rim
        rim = rim_zone[..., None]
        f = np.where(rim, np.stack([f[..., 0], np.minimum(f[..., 1], np.maximum(f[..., 0], f[..., 2]) + 0.02), f[..., 2]], -1), f)

        ph = k / LOOP
        band = np.exp(-(((diag - (ph * 1.9 - 0.45)) / 0.07) ** 2)) * 0.10
        p = prgb + band[..., None] * np.array([1.0, 0.97, 0.9], np.float32)
        p = p + rng.normal(0, 0.012, (VH, VW, 1)).astype(np.float32)
        comp = f + np.clip(p, 0, 1) * a[..., None]
        enc.stdin.write((np.clip(comp, 0, 1) * 255 + 0.5).astype(np.uint8).tobytes())
    enc.stdin.close(); enc.wait()
    print("wrote", out)


if __name__ == "__main__":
    main()
