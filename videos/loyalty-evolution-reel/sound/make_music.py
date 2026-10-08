"""Edit the licensed music bed for the reel, v10: Mixkit "A New Life" (track 543, Mixkit Stock Music Free License).

v10 replaces the dance track ("Cat Walk") with a calm, cinematic one: sustained chords that swell, no kick drum.
Structure, cut to the voice (v10 time, see storyboard/tmap_v10.py):
  0.00-29.62  a later phrase of the track (from 39.64), softened (a gentle low-pass, -3 dB): the problem
  29.62-30.17 silence: the lock click and the pause
  30.17-36.29 the track's quiet build (18.52-24.64) rises under the introduction and the question
  36.29       its first full entry (24.64) lands on "It already has one."
  36.29-51.00 the track runs on from there, fading out over the last 1.4s
The bed is levelled to -21 LUFS integrated; index.html plays it at 0.5 and the voice carve ducks it further.
usage (from the project folder): python3 -I sound/make_music.py assets/music-src/mixkit-543-a-new-life.mp3
"""
import pathlib, re, subprocess, sys, wave
import numpy as np
from scipy.signal import butter, sosfilt

SR = 48000
DUR = 51.0
ENTRY = 24.64          # the track's first full entry (source time)
ENTRY_AT = 36.29       # "It already has one." (v10 time)
PAUSE = (29.62, 30.17)
PROBLEM_SRC = 39.64    # a phrase start, 7.5s phrases from the entry
TARGET_LUFS = -21.0
ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = sys.argv[1]

raw = subprocess.run(["ffmpeg", "-v", "error", "-i", SRC, "-ac", "2", "-ar", str(SR), "-f", "f32le", "-"], capture_output=True, check=True).stdout
x = np.frombuffer(raw, np.float32).reshape(-1, 2).astype(np.float64)
N = int(round(DUR * SR))
out = np.zeros((N, 2))
S = lambda t: int(round(t * SR))


def put(t_out, t_src, dur, fin=0.01, fout=0.01, gain=1.0, lowpass=None):
    seg = x[S(t_src):S(t_src) + S(dur)].copy()
    if lowpass:
        seg = sosfilt(butter(2, lowpass / (SR / 2), "low", output="sos"), seg, axis=0)
    e = np.ones(len(seg))
    if fin: e[:S(fin)] = np.linspace(0, 1, S(fin)) ** 2
    if fout: e[-S(fout):] *= np.linspace(1, 0, S(fout)) ** 1.5
    a = S(t_out)
    out[a:a + len(seg)] += (seg * e[:, None] * gain)[: N - a]


# 1 · the problem: a softened later phrase, eased in, gone by the lock click
put(0.0, PROBLEM_SRC, PAUSE[0], fin=0.35, fout=0.3, gain=10 ** (-3 / 20), lowpass=4200.0)
# 2 · the pause is silent; 3 · the quiet build rises under the introduction (lifted, it is very soft in the source)
pre = ENTRY_AT - PAUSE[1]
put(PAUSE[1], ENTRY - pre, pre + 0.01, fin=0.9, fout=0.0, gain=10 ** (8 / 20))
# 4 · the first full entry on "It already has one", running to the end
put(ENTRY_AT, ENTRY, DUR - ENTRY_AT, fin=0.004, fout=1.4)


def write(path, y):
    with wave.open(str(path), "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((np.clip(y, -1, 1) * 32767).astype("<i2").tobytes())


dst = ROOT / "assets/music-bed.wav"
write(dst, out)
log = subprocess.run(["ffmpeg", "-i", str(dst), "-af", "ebur128", "-f", "null", "-"], capture_output=True, text=True).stderr
lufs = float(re.findall(r"I:\s+(-?[\d.]+) LUFS", log)[-1])
g = 10 ** ((TARGET_LUFS - lufs) / 20)
g = min(g, 10 ** (-1.0 / 20) / np.abs(out).max())          # never above -1 dBFS peak
write(dst, out * g)
print("wrote assets/music-bed.wav", f"{N / SR:.2f}s", f"measured {lufs:.1f} LUFS, gain {20 * np.log10(g):+.1f} dB")
