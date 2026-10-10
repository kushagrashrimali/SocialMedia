"""Music and sound for the WYSTAK hype reel: one track, re-cut so the music speeds up when the film does.

The track is Mixkit 69 "Ramp It Up" (120 BPM, one bar = 2 s, downbeats at src 0.12 + 2k): a drumless pad (src 0-16),
a drum groove (16.12), the full groove (32.12), the last phrase (80.12) and an ending hit (96.12). The film's cuts sit on
the same grid (src/timing.js), so every section change lands on a downbeat:

  0.0-7.5   the pad alone, its filter opening; a soft heartbeat from the wake, kicks on the words, hits on every pass
            that lands in the stack (each one sooner than the last), a riser, then a hard stop
  7.5-8.0   near silence under "Introducing": a vacuum swell pulls into the drop
  8.0       the drop on the W: the drum groove, with a bass hit
  12.0      the scan lands, the music steps up to the full groove
  13.5-16   the spin: a sweep rises and a snare roll quickens into the flash cuts, a hit on every flash
  16-17     "All your passes. One stack.": the groove stutters 1/8 > 1/16 > 1/32 as a high-pass rises
  17.0-17.5 silence
  17.5      the end card hits on the track's last phrase; the Wystak chime on the mark; the track's own ending at 21.5

Sound effects stay few and soft (low-passed bus): Mixkit sound effects (Mixkit Sound Effects Free License) in
assets/sfx-src/, the rest synthesised. Sources are git-ignored; fetch them with the ids below.
  music  https://assets.mixkit.co/music/69/69.mp3                          -> assets/music-src/mixkit-69-ramp-it-up.mp3
  sfx    https://assets.mixkit.co/active_storage/sfx/<id>/<id>-preview.mp3 -> assets/sfx-src/mixkit-<id>.mp3
         2303 bass hit, 1465 vacuum swoosh, 168 air sweep, 1492 whoosh, 2634 sweep, 787 whoosh stutter, 2357 bubble pop

usage (from the project folder): python3 -I sound/make_sound.py  -> assets/audio/hype-mix.wav
"""
import json, pathlib, re, subprocess, wave
import numpy as np
from scipy.signal import butter, sosfilt, fftconvolve

ROOT = pathlib.Path(__file__).resolve().parent.parent
H = json.loads(re.search(r"=\s*(\{.*\})", (ROOT / "src/timing.js").read_text(), re.S).group(1))
SR = 48000
DUR = H["dur"]
N = int(round(SR * DUR))
PH = 0.12                                   # the track's first downbeat
rng = np.random.default_rng(69)


def T(d):
    return np.arange(int(round(SR * d))) / SR


def filt(x, kind, fc, order=2):
    fc = np.atleast_1d(fc) / (SR / 2)
    return sosfilt(butter(order, fc if fc.size > 1 else fc[0], kind, output="sos"), x, axis=0)


def load(path):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(path), "-ac", "2", "-ar", str(SR), "-f", "f32le", "-"],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.float32).reshape(-1, 2).astype(np.float64)


SONG = load(ROOT / "assets/music-src/mixkit-69-ramp-it-up.mp3")
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


# ------------------------------------------------------------------ the music edit
mus = np.zeros((N, 2))

# 0-7.5: the pad, its low-pass opening as the film wakes up, a little louder as it goes; a hard stop at 7.5
a0, a1 = 0.0, H["intro"][0]
pad = song(PH + a0, a1 - a0, fin=0.0, fout=0.012)
cuts = [600, 1200, 2500, 6000]
vers = [filt(pad, "low", c, 2) for c in cuts] + [pad]
k = np.clip(np.arange(len(pad)) / SR / 6.0, 0, 1) * (len(vers) - 1)      # fully open by 6.0
lo = np.floor(k).astype(int); fr = (k - lo)[:, None]; hi = np.minimum(lo + 1, len(vers) - 1)
V = np.stack(vers)
opened = V[lo, np.arange(len(pad))] * (1 - fr) + V[hi, np.arange(len(pad))] * fr
lvl = db(np.interp(np.arange(len(pad)) / SR, [0, 0.35, 4.0, 7.5], [-40, 7, 9, 11]))[:, None]
place(mus, opened * lvl, a0)

# the heartbeat from the wake, then kicks on the beat and stabs of the coming drop on the words
for t in (H["wake"][0], H["wake"][0] + 1.0, H["wake"][0] + 1.5):
    place(mus, filt(kick(soft=1.0), "low", 300), t, db(-9))
for t in np.arange(H["type1"][0], H["type1"][1], 0.5):
    place(mus, kick(), t, db(-6))
for t in H["words1"]:
    place(mus, filt(song(16.12, 0.24, fout=0.06), "low", 2200), t, db(-5))
for t in np.arange(H["type1"][0] + 0.25, H["stack"][0], 0.5):                  # off-beat hats, then 16ths
    place(mus, hat(), t, db(-14), pan=0.25)
for t in np.arange(H["type1"][0] + 1.0, H["stack"][0], 0.125):
    place(mus, hat(), t, db(-20), pan=-0.25)
# the stack: a hit on every landing (each sooner than the last), hats running to 32nds, a riser into the whip
for i, t in enumerate(H["lands"]):
    place(mus, kick(), t, db(-5 + i * 0.6))
    place(mus, filt(song(16.12, 0.2, fout=0.05), "low", 3000), t, db(-7 + i * 0.6))
for t in np.arange(H["stack"][0], H["whip"], 0.125):
    place(mus, hat(), t, db(-18), pan=0.2)
for t in np.arange(H["whip"] - 0.25, H["intro"][0], 0.0625):
    place(mus, hat(), t, db(-17), pan=-0.2)
r = riser(1.5)
r[-int(0.012 * SR):] *= np.linspace(1, 0, int(0.012 * SR))
place(mus, r, H["stack"][0], db(-13))

# 8.0: the drop on the W (the drum groove), 12.0: the full groove as the scan lands
gA = song(16.12, 4.0, fin=0.0, fout=0.004)
place(mus, gA, H["reveal"][0])
gB = song(32.12, 4.0, fin=0.004, fout=0.0)
place(mus, gB, 12.0, db(-1.5))
# the spin: a snare roll quickens into the flash cuts; a hit on every flash
s0 = 14.0
roll = [s0 + 0.25 * i for i in range(2)] + [14.5 + 0.125 * i for i in range(2)] + [14.75 + 0.0625 * i for i in range(4)]
for i, t in enumerate(roll):
    place(mus, snare(), t, db(-17 + i * 1.3), pan=0.1 * (-1) ** i)
for i, t in enumerate(H["flashes"]):
    place(mus, kick(), t, db(-4 if i == 0 else -7))
    place(mus, snare(), t, db(-12 + i * 0.6), pan=0.15 * (-1) ** i)
# 16-17: the groove stutters 1/8 > 1/16 > 1/32 under the promise, a high-pass rising through it; then stop
st = np.zeros((int(SR * 1.0) + 1, 2))
t, i = 0.0, 0
for seg, n in ((0.25, 2), (0.125, 2), (0.0625, 4)):
    for _ in range(n):
        place(st, song(36.12, seg, fin=0.002, fout=0.004), t)
        t += seg
cut = [150, 400, 900, 1600]
sv = [filt(st, "high", c, 2) for c in cut]
kk = np.clip(np.arange(len(st)) / len(st), 0, 1) * (len(sv) - 1)
lo = np.floor(kk).astype(int); fr = (kk - lo)[:, None]; hi = np.minimum(lo + 1, len(sv) - 1)
SV = np.stack(sv)
st = SV[lo, np.arange(len(st))] * (1 - fr) + SV[hi, np.arange(len(st))] * fr
st = reverb(st, 1.2, 0.18)
place(mus, st[:int(SR * 1.0)], H["type2"][0], db(3))
tail = reverb(np.concatenate([st[int(SR * 0.94):int(SR * 1.0)], np.zeros((int(SR * 0.5), 2))]), 1.2, 0.9)
place(mus, tail * np.linspace(1, 0, len(tail))[:, None] ** 2, H["type2"][1] - 0.06, db(-8))
r = riser(1.0, 500, 9000)
r[-int(0.01 * SR):] *= np.linspace(1, 0, int(0.01 * SR))
place(mus, r, H["type2"][0], db(-11))

# 17.5: the end card hits on the start of the track's last phrase; at 21.5 the track's own ending hit and its tail
e0 = H["end"][0]
place(mus, song(80.12, 4.0, fin=0.0, fout=0.01), e0, db(-3))
end = song(96.12, DUR - (e0 + 4.0), fin=0.0, fout=0.0)
fade = np.ones(len(end)); fl = int(0.45 * SR); fade[-fl:] = np.linspace(1, 0, fl) ** 1.5
place(mus, end * fade[:, None], e0 + 4.0, db(-3))

# ------------------------------------------------------------------ sound effects (soft, low-passed bus)
fx = np.zeros((N, 2))
place(fx, smp(1492), H["intro"][0] - 1.08, db(-12))                      # the rush into the stop (peaks just before 7.5)
place(fx, smp(168), H["whip"] - 0.28, db(-14), pan=-0.4)                   # the stack whips away
v = smp(1465, 1.05, 0.75)                                                   # "Introducing": a vacuum swell into the drop
place(fx, v, H["reveal"][0] - 0.5, db(-9))
place(fx, smp(2303), H["reveal"][0] - 0.06, db(-6))                         # the W lands: bass hit + sub
place(fx, sub_drop(), H["reveal"][0], db(-6))
place(fx, smp(168), H["revealOut"] - 0.22, db(-15), pan=0.3)                # the mark rushes into the next shot
place(fx, ping(), H["scanRun"][1], db(-12))                                 # the scan reads
place(fx, smp(2357, 0.02, 0.19), H["notif"] + 0.05, db(-9))                 # +18 points
place(fx, smp(2634), H["flashes"][0] - 1.72, db(-13))                       # the spin: a sweep rising into the flashes
place(fx, sub_drop(1.0), H["flashes"][0], db(-9))
place(fx, smp(787), H["type2"][1] - 2.0, db(-18))                           # a stuttering whoosh under the roll
place(fx, smp(2303), e0 - 0.06, db(-5))                                     # the end card
place(fx, sub_drop(), e0, db(-5))
ch, off = wystak_chime()
place(fx, ch, H["endPop"] - off, db(-11))                                   # the mark fans out: the Wystak chime
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
out = ROOT / "assets/audio/hype-mix.wav"
out.parent.mkdir(parents=True, exist_ok=True)
with wave.open(str(out), "wb") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((np.clip(mix, -1, 1) * 32767).astype("<i2").tobytes())
print(f"{out}  {DUR:.2f}s  peak-normalised from {20 * np.log10(pk):+.1f} dBFS")
