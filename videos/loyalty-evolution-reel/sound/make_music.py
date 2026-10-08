"""Edit the licensed music bed for the reel: Mixkit "Cat Walk" (track 371, Mixkit Stock Music Free License).

Structure, cut to the voice:
  0.00-29.62  the track's own intro and build (its drop sits at 29.66, so the build stops just short of it)
  29.62-31.20 silence under the Wystak introduction (the chime lands at 30.12)
  31.20-34.87 the bars before the drop, low-passed and opening up under the held lockup and the question
  34.87       the drop lands on "It already has one."
  46.37-51.00 the track's own ending, beat-aligned, under the logo, fading out over the last second
v5: the introduction holds 1.0s longer (voice re-gapped at 30.40), so everything after it moves by 1.0s.
usage (from the project folder): python3 -I sound/make_music.py /path/to/371.mp3
"""
import pathlib, subprocess, sys, wave
import numpy as np

SR = 48000
DUR = 51.0          # v9: ends one second after "One stack."
DROP_AT = 34.87     # "It already has one."
PRE_AT = 31.20      # filtered build starts under the held lockup
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
# 2 · silence under the introduction, then the bars before the drop, filter opening up
pre = DROP_AT - PRE_AT
seg = x[S(DROP - pre):S(DROP)].copy()
seg = lowpass_sweep(seg, 220.0, 9000.0) * (np.linspace(0.0, 1.0, len(seg)) ** 0.8 * 0.6 + 0.4)[:, None]
seg *= fade(len(seg), S(0.9), 0)
out[S(PRE_AT):S(PRE_AT) + len(seg)] += seg
# 3 · the drop on "It already has one", running to the switch point on a beat
sw = DROP_AT + 25 * BEAT                                 # 46.37
put(DROP_AT, DROP, sw - DROP_AT + 0.01, fin=0.002, fout=0.02)
# 4 · the track's ending, entered on a beat, under the logo
end_src = DROP + round((111.5 - DROP) / BEAT) * BEAT
put(sw, end_src, DUR - sw, fin=0.02, fout=1.1)

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
