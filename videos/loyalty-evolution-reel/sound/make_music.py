"""Edit the licensed music bed for the reel (50.5s): Mixkit "Motivating Mornings" (track 33, Mixkit Stock Music Free License).

Why this track: product intro and launch films use clean, mid-tempo electronic with no vocals, a steady light pulse and a
gradual build (research notes in CLAUDE.md). This one is 120 BPM, soft intro, a light groove from 12s, lifts later: not a
club kick (Cat Walk was rejected as too dancy) and not cinematic swells (A New Life was rejected as too operatic).
Cut to the voice (times from assets/words.json), bars of 2.0s starting at 12.0s in the source:
  0 - "login."          the track as written: its soft intro under the hook, the groove from "Every visit"
  the question          the bars before the entry, low-passed and opening up: a filter build into the name
  "Introducing"         the entry (source 44.0, a downbeat) lands on the name and runs to the end
  the name              the bed eases down 3 dB to give the Wystak chime room, then comes back
  the last 1.5s         fade out under the logo
The bed is levelled to -21 LUFS integrated; index.html plays it at 0.5 and the voice carve ducks it further.
usage (from the project folder): python3 -I sound/make_music.py assets/music-src/mixkit-33-motivating-mornings.mp3
"""
import json, pathlib, re, subprocess, sys, wave
import numpy as np
from scipy.signal import butter, sosfilt

SR = 48000
ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "storyboard"))
from tmap_v11 import DUR, INTRO, V11

ENTRY = 44.0                     # a downbeat at the start of a 16-beat phrase (source time)
ENTRY_AT = V11[72]["start"]      # "Introducing Why-stack."
PROBLEM_END = V11[64]["end"] + 0.05   # "login."
PROBLEM_SRC = 0.0
TARGET_LUFS = -21.0
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


def lowpass_sweep(sig, f0, f1):
    """one-pole low-pass whose cutoff glides exponentially from f0 to f1"""
    n = len(sig); y = np.zeros_like(sig); fc = f0 * (f1 / f0) ** (np.arange(n) / n)
    a = np.exp(-2 * np.pi * fc / SR); s = np.zeros(2)
    for i in range(n):
        s = (1 - a[i]) * sig[i] + a[i] * s
        y[i] = s
    return y


# 1 · the problem: the track as written, easing out on "login."
put(0.0, PROBLEM_SRC, PROBLEM_END, fin=0.02, fout=0.45)
# 2 · the question: the bars just before the entry, filtered down and opening up, rising in level
pre = ENTRY_AT - PROBLEM_END + 0.25
seg = x[S(ENTRY - pre):S(ENTRY)].copy()
seg = lowpass_sweep(seg, 260.0, 7000.0) * (np.linspace(0, 1, len(seg)) ** 1.2 * 0.75 + 0.25)[:, None]
seg[:S(0.4)] *= np.linspace(0, 1, S(0.4))[:, None]
a0 = S(ENTRY_AT - pre); out[a0:a0 + len(seg)] += seg[: N - a0]
# 3 · the entry on "Introducing", running to the end
put(ENTRY_AT, ENTRY, DUR - ENTRY_AT, fin=0.004, fout=1.5)
# 4 · room for the chime: ease down 3 dB under the name
g = np.ones(N); a0, a1 = S(V11[73]["start"] - 0.5), S(INTRO[1] + 0.2); r = S(0.35)
g[a0:a1] = 10 ** (-3 / 20); g[a0:a0 + r] = np.linspace(1, 10 ** (-3 / 20), r); g[a1 - r:a1] = np.linspace(10 ** (-3 / 20), 1, r)
out *= g[:, None]


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
