"""Music and sound for the WYSTAK iPhone reel (30 s): one track re-cut onto the film's grid, plus a few soft effects.

The track is Mixkit 33 "Motivating Mornings" (120 BPM, the light electronic bed already approved for the loyalty reel;
one bar = 2 s, downbeats at src 0.135 + 2k): a quiet intro (src 0-12), the drums (12.135), a build with rising hats
(26.135), the main section (44.135) and the ending hit (92.135). Every section change lands on a downbeat of the film:

  0-2     the intro, its low-pass opening as the phone wakes on the lilac set
  2       the drums come in on the first card ("Your regulars.")
  10      the build starts on "No app." and climbs through the passes and the reward ring
  15.75   a quarter-beat of air after the ring completes
  16      the main section drops on "See who comes back." and carries the macro shots and "Every visit counts."
  24      the track's last bars; its own ending hit lands on "ONE STACK." at 28.0 and rings out to 30

Effects (Mixkit Sound Effects Free License, in assets/sfx-src/, git-ignored; the rest synthesised) stay few and soft:
the pushes as they land, the scan, the mark, the drop, the passes filing into the Wallet, the Wystak chime on the end
card. Nothing on plain cuts, no taps or ticks; the effects bus is low-passed at 8.5 kHz.
  music  https://assets.mixkit.co/music/33/33.mp3                          -> assets/music-src/mixkit-33-motivating-mornings.mp3
  sfx    https://assets.mixkit.co/active_storage/sfx/<id>/<id>-preview.mp3 -> assets/sfx-src/mixkit-<id>.mp3  (2303, 168, 1492, 3114, 2357)

usage (from the project folder): python3 -I sound/make_sound.py  -> assets/audio/reel-mix.wav
"""
import json, pathlib, re, subprocess, wave
import numpy as np
from scipy.signal import butter, sosfilt, fftconvolve

ROOT = pathlib.Path(__file__).resolve().parent.parent
H = json.loads(re.search(r"=\s*(\{.*\})", (ROOT / "src/timing.js").read_text(), re.S).group(1))
SR = 48000
DUR = H["dur"]
N = int(round(SR * DUR))
PH = 0.135                                  # the track's first downbeat offset
rng = np.random.default_rng(33)


def T(d):
    return np.arange(int(round(SR * d))) / SR


def filt(x, kind, fc, order=2):
    fc = np.atleast_1d(fc) / (SR / 2)
    return sosfilt(butter(order, fc if fc.size > 1 else fc[0], kind, output="sos"), x, axis=0)


def load(path):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(path), "-ac", "2", "-ar", str(SR), "-f", "f32le", "-"],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.float32).reshape(-1, 2).astype(np.float64)


SONG = load(ROOT / "assets/music-src/mixkit-33-motivating-mornings.mp3")
_sfx = {}


def smp(sid, start=0.0, dur=None):
    if sid not in _sfx:
        x = load(ROOT / f"assets/sfx-src/mixkit-{sid}.mp3")
        _sfx[sid] = x / max(1e-9, np.abs(x).max())
    x = _sfx[sid][int(start * SR):].copy()
    if dur:
        x = x[:int(dur * SR)]
    r = min(len(x), int(0.008 * SR))
    x[:r] *= np.linspace(0, 1, r)[:, None]
    x[-r:] *= np.linspace(1, 0, r)[:, None]
    return x


def song(a, d, fin=0.004, fout=0.006):
    """a slice of the track, src seconds [a, a+d), with short de-click fades"""
    x = SONG[int(round(a * SR)):int(round((a + d) * SR))].copy()
    fi, fo = int(fin * SR), int(fout * SR)
    if fi: x[:fi] *= np.linspace(0, 1, fi)[:, None]
    if fo: x[-fo:] *= np.linspace(1, 0, fo)[:, None]
    return x


def place(buf, sig, t0, gain=1.0, pan=0.0):
    if sig.ndim == 1:
        sig = np.stack([sig, sig], 1)
    sig = sig * np.array([np.cos((pan + 1) * np.pi / 4), np.sin((pan + 1) * np.pi / 4)]) * np.sqrt(2)
    i0 = int(round(t0 * SR))
    s0 = max(0, -i0); i0 = max(0, i0)
    n = min(len(sig) - s0, len(buf) - i0)
    if n > 0:
        buf[i0:i0 + n] += sig[s0:s0 + n] * gain


def db(v):
    return 10 ** (v / 20)


def reverb(x, seconds=1.4, wet=0.2, seed=3):
    r = np.random.default_rng(seed)
    t = T(seconds)
    ir = np.stack([r.standard_normal(len(t)), r.standard_normal(len(t))], 1) * np.exp(-t / (seconds / 6.9))[:, None]
    ir = filt(ir, "low", 5000); ir /= np.sqrt((ir ** 2).sum(0))
    y = np.stack([fftconvolve(x[:, c], ir[:, c])[:len(x)] for c in range(2)], 1)
    return x * (1 - wet) + y * wet


# ------------------------------------------------------------------ synthesised voices
def kick(soft=0.0):
    t = T(0.45)
    f = 46 + 110 * np.exp(-t / 0.035)
    body = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / (0.16 + 0.1 * soft)) * (1 - np.exp(-t / 0.002))
    click = filt(rng.standard_normal(len(t)), "band", [1800, 5000]) * np.exp(-t / 0.004) * 0.25 * (1 - soft)
    return np.tanh(1.6 * body) * 0.9 + click


def hat(open_=False):
    t = T(0.25 if open_ else 0.06)
    return filt(rng.standard_normal(len(t)), "high", 7000, 4) * np.exp(-t / (0.06 if open_ else 0.012)) * 0.5


def snare():
    t = T(0.22)
    tone = np.sin(2 * np.pi * np.cumsum(185 + 60 * np.exp(-t / 0.02)) / SR) * np.exp(-t / 0.05) * 0.5
    noise = filt(rng.standard_normal(len(t)), "band", [1200, 7000]) * np.exp(-t / 0.07) * 0.6
    return tone + noise


def sub_drop(d=1.6):
    t = T(d)
    return np.sin(2 * np.pi * np.cumsum(30 + 34 * np.exp(-t / 0.25)) / SR) * np.exp(-t / 0.55) * (1 - np.exp(-t / 0.006))


def riser(d, f0=300, f1=7000):
    """noise rising through a band-pass, louder as it climbs, with a sine glide underneath"""
    t = T(d); k = t / d
    nz = rng.standard_normal(len(t))
    out = np.zeros(len(t)); seg = int(0.02 * SR)
    for i in range(0, len(t), seg):
        fc = f0 * (f1 / f0) ** k[i]
        lo, hi = fc / 1.6, min(fc * 1.6, SR / 2 - 100)
        out[i:i + seg] = sosfilt(butter(2, [lo / (SR / 2), hi / (SR / 2)], "band", output="sos"), nz[max(0, i - 2000):i + seg])[-len(out[i:i + seg]):]
    glide = np.sin(2 * np.pi * np.cumsum(110 * 2 ** (2.5 * k)) / SR) * 0.25
    return (out * 0.8 + glide) * k ** 2.2


def ping():
    """the scan reads: one soft glass ping, a fifth above, gone in half a second"""
    t = T(0.6)
    a = np.sin(2 * np.pi * 1318.5 * t) * np.exp(-t / 0.16)
    b = np.sin(2 * np.pi * 1975.5 * t) * np.exp(-t / 0.12) * 0.5
    return (a + b) * (1 - np.exp(-t / 0.002)) * 0.6


def wystak_chime():
    """the Wystak chime (from the loyalty reel): an airy shimmer rises into a glassy FM bell chord, E major add9"""
    d = 3.4; t = T(d); out = np.zeros((len(t), 2))
    sw = T(0.45)
    air = filt(rng.standard_normal(len(sw)), "band", [3500, 11000]) * (sw / sw[-1]) ** 2.6 * 0.35
    out[:len(sw)] += air[:, None]
    hit = len(sw)
    for n, dt, pan, g in [(76, 0.00, -0.35, 1.0), (83, 0.045, 0.3, 0.8), (88, 0.09, -0.15, 0.62), (90, 0.135, 0.4, 0.5), (95, 0.19, 0.0, 0.32)]:
        tb = T(d - 0.45 - dt)
        f = 440 * 2 ** ((n - 69) / 12) * (1 + 0.012 * np.exp(-tb / 0.05))
        idx = 2.6 * np.exp(-tb / 0.18) + 0.25
        mod = np.sin(2 * np.pi * np.cumsum(f * 3.51) / SR)
        car = 0.6 * np.sin(2 * np.pi * np.cumsum(f) / SR + idx * mod) + 0.4 * np.sin(2 * np.pi * np.cumsum(f * 1.003) / SR + idx * 0.8 * mod)
        b = car * (1 - np.exp(-tb / 0.004)) * np.exp(-tb / 1.1) * g
        i0 = hit + int(dt * SR)
        out[i0:i0 + len(b), 0] += b * np.cos((pan + 1) * np.pi / 4) * np.sqrt(2)
        out[i0:i0 + len(b), 1] += b * np.sin((pan + 1) * np.pi / 4) * np.sqrt(2)
    tb = T(d - 0.45)
    out[hit:] += (np.sin(2 * np.pi * 329.63 * tb) * (1 - np.exp(-tb / 0.02)) * np.exp(-tb / 0.9) * 0.18)[:, None]
    out = filt(out, "high", 180)
    wet = np.zeros_like(out)
    for k, (dl, g) in enumerate(((0.21, 0.32), (0.42, 0.2), (0.63, 0.12))):
        i = int(dl * SR)
        wet[i:, (k + 1) % 2] += filt(out[:-i], "low", 7000 - 1500 * k)[:, k % 2] * g
    return out + wet, 0.45                     # (signal, offset of the hit)



def card_flick():
    """a pass filing into the stack: a short soft brush of air and a low touch"""
    t = T(0.18)
    air = filt(rng.standard_normal(len(t)), "band", [1500, 6000]) * np.exp(-t / 0.03) * 0.4
    touch = np.sin(2 * np.pi * np.cumsum(140 + 80 * np.exp(-t / 0.02)) / SR) * np.exp(-t / 0.05) * 0.6
    return air + touch


def two_note():
    """the reward unlocks: two soft glass notes, a fourth apart"""
    out = np.zeros(int(SR * 0.9))
    for dt, f in ((0.0, 987.8), (0.11, 1318.5)):
        t = T(0.9 - dt); i = int(dt * SR)
        out[i:] += np.sin(2 * np.pi * f * t) * np.exp(-t / 0.22) * (1 - np.exp(-t / 0.003)) * 0.5
    return out


def opened(x, cuts, t_open):
    """a section whose low-pass opens over t_open seconds (crossfading pre-filtered versions)"""
    vers = [filt(x, "low", c, 2) for c in cuts] + [x]
    k = np.clip(np.arange(len(x)) / SR / t_open, 0, 1) * (len(vers) - 1)
    lo = np.floor(k).astype(int); fr = (k - lo)[:, None]; hi = np.minimum(lo + 1, len(vers) - 1)
    V = np.stack(vers); idx = np.arange(len(x))
    return V[lo, idx] * (1 - fr) + V[hi, idx] * fr


# ------------------------------------------------------------------ the music edit
mus = np.zeros((N, 2))
intro = song(PH + 4.0, 2.0, fin=0.0, fout=0.004)
intro = opened(intro, [500, 1100, 2400], 1.9) * db(np.interp(np.arange(len(intro)) / SR, [0, 0.25, 2.0], [-40, 3, 5]))[:, None]
place(mus, intro, 0.0)
place(mus, song(PH + 12.0, 8.0, fin=0.0, fout=0.004), 2.0)                      # the drums, 2-10
build = song(PH + 26.0, 5.75, fin=0.004, fout=0.03)                             # the build, 10-15.75
place(mus, build * db(np.interp(np.arange(len(build)) / SR, [0, 5.75], [-1.5, 1.0]))[:, None], 10.0)
r = riser(1.2, 400, 8000); r[-int(0.02 * SR):] *= np.linspace(1, 0, int(0.02 * SR))
place(mus, r, 15.75 - 1.2, db(-15))
place(mus, song(PH + 44.0, 8.0, fin=0.0, fout=0.004), 16.0)                    # the drop, 16-24
end = song(PH + 88.0, DUR - 24.0, fin=0.004, fout=0.0)                          # the last bars and the ending hit (28.0)
fade = np.ones(len(end)); fl = int(0.6 * SR); fade[-fl:] = np.linspace(1, 0, fl) ** 1.5
place(mus, end * fade[:, None], 24.0)

# ------------------------------------------------------------------ effects (soft; low-passed bus)
fx = np.zeros((N, 2))
pop = lambda: smp(2357, 0.02, 0.19)
for i, t in enumerate(H["notifs"]):
    place(fx, pop(), t + 0.06, db(-17 + i), pan=(-0.3, 0.1, 0.3)[i])          # the pushes rise out of the phone
place(fx, smp(168), H["s1_open"][1] - 0.3, db(-17))                             # zoom-through into the first card
place(fx, smp(3114), H["scanRun"][0] - 0.05, db(-24))                           # the scanner's light
place(fx, ping(), H["scanRun"][1], db(-13))                                     # the code reads
place(fx, pop(), H["plus"] + 0.03, db(-15))                                     # +18
place(fx, smp(2303), H["markHit"] - 0.06, db(-11))                              # the mark lands
place(fx, sub_drop(1.2), H["markHit"], db(-12))
place(fx, smp(168), H["press"] - 0.05, db(-17))                                 # the pass presses into the phone
place(fx, pop(), H["notif"] + 0.05, db(-10))                                    # +18 points on the lock screen
for i, t in enumerate(H["cycle"]):
    place(fx, card_flick(), t + 0.02, db(-22 + i), pan=-0.3)                    # passes cycle
place(fx, two_note(), H["unlock"], db(-12))                                     # reward unlocked
place(fx, smp(2303), H["s9_owner"][0] - 0.06, db(-10))                          # the drop
place(fx, sub_drop(), H["s9_owner"][0], db(-11))
place(fx, pop(), H["send"] + 0.02, db(-15))                                     # offer sent
place(fx, smp(1492), H["s10_macro"][0] - 1.05, db(-18))                         # zoom-through into the macro shots
place(fx, smp(2303), H["countsWord"] - 0.06, db(-13))                           # Every visit counts.
for i, t in enumerate(H["stackIn"]):
    place(fx, card_flick(), t + 0.32, db(-20 + i * 0.6), pan=0.2)              # each pass files into the Wallet
place(fx, smp(168), H["s12_stack"][1] - 0.3, db(-18))                           # rise into the end card
ch, off = wystak_chime()
place(fx, ch, H["fan"] - off, db(-10))                                          # the mark fans out: the Wystak chime
fx = filt(fx, "low", 8500, 2)

mix = mus + fx
# a gentle peak limiter (5 ms hold, 1 ms attack, 120 ms release) so the hits don't set the level of the whole film
thr = np.percentile(np.abs(mix), 99.7) * 1.6
env = np.abs(mix).max(1)
hold = int(0.005 * SR)
env = np.maximum.reduce([np.roll(env, -k) for k in range(0, hold, 8)])
g = np.minimum(1.0, thr / np.maximum(env, 1e-9))
rel = np.exp(-1 / (0.12 * SR)); att = np.exp(-1 / (0.001 * SR))
gs = np.empty_like(g); c = 1.0
for i, v in enumerate(g):
    c = v + (c - v) * (att if v < c else rel); gs[i] = c
mix = mix * gs[:, None]
pk = np.abs(mix).max()
mix = mix / pk * db(-1.0)
out = ROOT / "assets/audio/reel-mix.wav"
out.parent.mkdir(parents=True, exist_ok=True)
with wave.open(str(out), "wb") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((np.clip(mix, -1, 1) * 32767).astype("<i2").tobytes())
print(f"{out}  {DUR:.2f}s  peak-normalised from {20 * np.log10(pk):+.1f} dBFS")
