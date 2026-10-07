"""Composite a real green-screen hand + phone (Mixkit 42636) over a still background, with a
tracked screen replacement. Writes a 1080x1920 30fps H.264 clip.

usage: python3 -I composite_phone.py SRC.mp4 T0 DUR BG.jpg SCREEN.png OUT.mp4
         [--bg-cx 0.5] [--bg-cy 0.5] [--bg-zoom 1.0] [--blur 9] [--scale 0.6] [--push 0.04] [--dim 0.82]
"""
import argparse, subprocess
import cv2
import numpy as np

W, H = 1080, 1920

ap = argparse.ArgumentParser()
ap.add_argument("src"); ap.add_argument("t0", type=float); ap.add_argument("dur", type=float)
ap.add_argument("bg"); ap.add_argument("screen"); ap.add_argument("out")
ap.add_argument("--bg-cx", type=float, default=0.5); ap.add_argument("--bg-cy", type=float, default=0.5)
ap.add_argument("--bg-zoom", type=float, default=1.0); ap.add_argument("--blur", type=float, default=9)
ap.add_argument("--scale", type=float, default=0.6); ap.add_argument("--push", type=float, default=0.04)
ap.add_argument("--dim", type=float, default=0.82)
a = ap.parse_args()


def cover_crop(img, cx, cy, zoom, w, h):
    ih, iw = img.shape[:2]
    tw = min(iw, ih * w / h) / zoom
    th = tw * h / w
    x = int(min(max(cx * iw - tw / 2, 0), iw - tw)); y = int(min(max(cy * ih - th / 2, 0), ih - th))
    return cv2.resize(img[y:y + int(th), x:x + int(tw)], (w, h), interpolation=cv2.INTER_AREA)


# background: 9:16 cover crop, shallow depth of field, a little darker than the hand
bg0 = cover_crop(cv2.imread(a.bg), a.bg_cx, a.bg_cy, a.bg_zoom, int(W * 1.1), int(H * 1.1))
bg0 = cv2.GaussianBlur(bg0, (0, 0), a.blur)
bg0 = np.clip(bg0.astype(np.float32) * a.dim, 0, 255)

ui = cv2.imread(a.screen).astype(np.float32) * 0.94
uh, uw = ui.shape[:2]

cap = cv2.VideoCapture(a.src)
fps = cap.get(cv2.CAP_PROP_FPS)
cap.set(cv2.CAP_PROP_POS_MSEC, a.t0 * 1000)
n = int(round(a.dur * fps))
sw = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH) * a.scale); sh = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT) * a.scale)

enc = subprocess.Popen(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24",
                        "-s", f"{W}x{H}", "-framerate", f"{fps}", "-i", "-", "-vf", "fps=30,format=yuv420p",
                        "-c:v", "libx264", "-preset", "slow", "-crf", "17", "-movflags", "+faststart", a.out],
                       stdin=subprocess.PIPE)
xoff = None
for i in range(n):
    ok, fr = cap.read()
    if not ok:
        break
    fr = cv2.resize(fr, (sw, sh), interpolation=cv2.INTER_AREA)
    hsv = cv2.cvtColor(fr, cv2.COLOR_BGR2HSV)
    hch, sch, vch = hsv[..., 0], hsv[..., 1], hsv[..., 2]
    green = ((hch > 35) & (hch < 88) & (sch > 70) & (vch > 50)).astype(np.uint8)
    blue = ((hch > 98) & (hch < 132) & (sch > 110) & (vch > 50)).astype(np.uint8)
    if xoff is None:  # centre the phone horizontally, hand anchored to the bottom edge
        ys, xs = np.nonzero(blue)
        xoff = int(W / 2 - xs.mean())
    yoff = H - sh
    # place the scaled source on the canvas
    canvas_fg = np.zeros((H, W, 3), np.float32); g = np.ones((H, W), np.float32); b = np.zeros((H, W), np.float32)
    x0, x1 = max(0, xoff), min(W, xoff + sw); sx0 = x0 - xoff; sx1 = sx0 + (x1 - x0)
    canvas_fg[yoff:, x0:x1] = fr[:, sx0:sx1]
    g[yoff:, x0:x1] = green[:, sx0:sx1]; b[yoff:, x0:x1] = blue[:, sx0:sx1]
    # soft mattes
    g = cv2.GaussianBlur(g, (0, 0), 1.6)
    # grow the screen matte a little so the UI covers the blue fringe at the bezel
    b = cv2.GaussianBlur(cv2.dilate(b, np.ones((5, 5), np.uint8)), (0, 0), 1.0)
    a_fg = np.clip(1.0 - g - b, 0, 1)
    # despill: pull green down to max(red, blue) and blue down to max(red, green) on the edges
    fgc = canvas_fg.copy(); mx = np.maximum(fgc[..., 0], fgc[..., 2]); fgc[..., 1] = np.minimum(fgc[..., 1], mx * 1.02)
    mb = np.maximum(fgc[..., 1], fgc[..., 2]); fgc[..., 0] = np.minimum(fgc[..., 0], mb * 1.05)
    fgc *= np.array([0.95, 1.0, 1.05], np.float32)  # warm it toward the café light (BGR)
    # screen: fit the blue region's rotated rectangle and warp the UI into it
    cnts, _ = cv2.findContours((b > 0.5).astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    screen = np.zeros_like(canvas_fg)
    if cnts:
        c = max(cnts, key=cv2.contourArea)
        box = cv2.boxPoints(cv2.minAreaRect(c))
        s = box.sum(1); d = np.diff(box, axis=1).ravel()
        tl, br = box[np.argmin(s)], box[np.argmax(s)]; tr, bl = box[np.argmin(d)], box[np.argmax(d)]
        M = cv2.getPerspectiveTransform(np.float32([[0, 0], [uw, 0], [uw, uh], [0, uh]]), np.float32([tl, tr, br, bl]))
        screen = cv2.warpPerspective(ui, M, (W, H), flags=cv2.INTER_LINEAR)
    # background with a slow push
    k = 1.0 + a.push * i / max(1, n - 1)
    bw, bh = int(W * k), int(H * k)
    bgk = cv2.resize(bg0, (bw, bh), interpolation=cv2.INTER_LINEAR) if (bw, bh) != bg0.shape[1::-1] else bg0
    cy0 = (bgk.shape[0] - H) // 2; cx0 = (bgk.shape[1] - W) // 2
    out = bgk[cy0:cy0 + H, cx0:cx0 + W].copy()
    out = out * (1 - b[..., None]) + screen * b[..., None]
    out = out * (1 - a_fg[..., None]) + fgc * a_fg[..., None]
    enc.stdin.write(np.clip(out, 0, 255).astype(np.uint8).tobytes())
enc.stdin.close(); enc.wait(); cap.release()
print("wrote", a.out, n, "frames @", fps)
