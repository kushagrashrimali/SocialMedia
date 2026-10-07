"""Edit the licensed music bed for the reel: Mixkit "Cat Walk" (track 371, Mixkit Stock Music Free License).

Structure, cut to the voice:
  0.00-29.62  the track's own intro and build (its drop sits at 29.66, so the build stops just short of it)
  29.62-30.95 silence (the ding lands at 30.12)
  30.95-33.87 the bar before the drop, low-passed and opening up ("What if loyalty didn't need another place?")
  33.87       the drop lands on "It already has one."
  45.37-51.39 the track's own ending, beat-aligned, under the logo
usage (from the project folder): python3 -I sound/make_music.py /path/to/371.mp3
"""
import pathlib, subprocess, sys, wave
import numpy as np

SR = 48000
DUR = 51.39
ROOT = pathlib.Path(__file__).resolve().parent.parent
DROP = 29.66          # first kick of the drop in the source
BEAT = 0.46           # ~130 BPM
SRC = sys.argv[1]

raw = subprocess.run(["ffmpeg", "-v", "error", "-i", SRC, "-ac", "2", "-ar", str(SR), "-f", "f32le", "-"], capture_output=True, check=True).stdout
x = np.frombuffer(raw, np.float32).reshape(-1, 2).astype(np.float64)
N = int(round(DUR * SR))
out = np.zeros((N, 2))
S = lambda t: int(round(t * SR))


def fade(n, a, r):
    e = np.ones(n)
    if a: e[:a] = np.linspace(0, 1, a)
    if r: e[-r:] *= np.linspace(1, 0, r)
    return e[:, None]


def put(t_out, t_src, dur, fin=0.004, fout=0.004, gain=1.0):
    seg = x[S(t_src):S(t_src) + S(dur)].copy()
    seg *= fade(len(seg), S(fin), S(fout)) * gain
    a = S(t_out)
    out[a:a + len(seg)] += seg[: N - a]


def lowpass_sweep(sig, f0, f1):
    """one-pole low-pass whose cutoff glides exponentially from f0 to f1 over the segment"""
    n = len(sig); y = np.zeros_like(sig); fc = f0 * (f1 / f0) ** (np.arange(n) / n)
    a = np.exp(-2 * np.pi * fc / SR); s = np.zeros(2)
    for i in range(n):
        s = (1 - a[i]) * sig[i] + a[i] * s
        y[i] = s
    return y


# 1 · intro and build, stopping a hair before the drop
put(0.0, 0.0, 29.62, fin=0.02, fout=0.03)
# 2 · silence 29.62-30.95, then the bar before the drop under the question, filter opening up
pre = 33.87 - 30.95
seg = x[S(DROP - pre):S(DROP)].copy()
seg = lowpass_sweep(seg, 260.0, 9000.0) * np.linspace(0.55, 1.0, len(seg))[:, None]
seg *= fade(len(seg), S(0.35), 0)
out[S(30.95):S(30.95) + len(seg)] += seg
# 3 · the drop on "It already has one", running to the switch point on a beat
sw = 33.87 + 25 * BEAT                                   # 45.37
put(33.87, DROP, sw - 33.87 + 0.01, fin=0.002, fout=0.02)
# 4 · the track's ending, entered on a beat, under the logo
end_src = DROP + round((111.5 - DROP) / BEAT) * BEAT
put(sw, end_src, DUR - sw, fin=0.02, fout=0.6)

# lift the quiet intro so the film starts with energy, easing back to unity as the track builds
g = np.ones(N); g[:S(13.0)] = 2.0; g[S(13.0):S(16.0)] = np.linspace(2.0, 1.0, S(16.0) - S(13.0))
out *= g[:, None]
out *= fade(N, 0, S(0.4))
pk = np.abs(out).max()
out = out / pk * 10 ** (-1.0 / 20)
with wave.open(str(ROOT / "assets/music-bed.wav"), "wb") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((np.clip(out, -1, 1) * 32767).astype("<i2").tobytes())
print("wrote assets/music-bed.wav", f"{N / SR:.2f}s", "switch", round(sw, 2), "ending from", round(end_src, 2))
