"""Sound effects for the loyalty reel, v11: minimal, in the way Apple and Meta films use sound.

Only the moments that matter make a sound, each one soft and rounded: the unread alerts, the flood of alerts, the screen
sleeping, the pass landing in the Wallet, the Wystak chime on its name, the payment, the push that matters, the logo.
No whooshes on cuts, no taps, no ticks. Everything is low-passed (no hard top end) and sits in a small room.
Cues are written in v9 time and mapped with M (storyboard/tmap_v11.py), except the introduction, which uses the v11 words.
Samples are Mixkit sound effects (Mixkit Sound Effects Free License) in assets/sfx-src/ (see assets/MANIFEST.md);
the Wystak chime and the glass settle are synthesised.

usage (from the project folder): python3 -I sound/make_sound.py  -> assets/sfx.wav
"""
import pathlib, subprocess, sys, wave
import numpy as np
from scipy.signal import butter, sosfilt, fftconvolve

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "storyboard"))
from tmap_v11 import M, DUR, V11, INTRO

SR = 48000
N = int(round(SR * DUR))
rng = np.random.default_rng(1007)


def T(d):
    return np.arange(int(round(SR * d))) / SR


def filt(x, kind, fc, order=2):
    fc = np.atleast_1d(fc) / (SR / 2)
    sos = butter(order, fc if fc.size > 1 else fc[0], kind, output="sos")
    return sosfilt(sos, x, axis=0)


_cache = {}


def smp(sid, start=0.0, dur=None, rate=1.0):
    """a Mixkit sample as stereo float, peak 1; optional trim and varispeed (rate > 1 is higher and shorter)"""
    if sid not in _cache:
        raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(ROOT / f"assets/sfx-src/mixkit-{sid}.mp3"), "-ac", "2", "-ar", str(SR),
                              "-f", "f32le", "-"], capture_output=True, check=True).stdout
        x = np.frombuffer(raw, np.float32).reshape(-1, 2).astype(np.float64)
        _cache[sid] = x / max(1e-9, np.abs(x).max())
    x = _cache[sid][int(start * SR):]
    if dur:
        x = x[:int(dur * SR)].copy()
        r = min(len(x), int(0.01 * SR))
        x[-r:] *= np.linspace(1, 0, r)[:, None]
    if rate != 1.0:
        idx = np.arange(0, len(x) - 1, rate)
        x = np.stack([np.interp(idx, np.arange(len(x)), x[:, c]) for c in range(2)], 1)
    return x


def place(buf, sig, t0, gain=1.0, pan=0.0):
    i0 = int(round(t0 * SR))
    if sig.ndim == 1:
        sig = np.stack([sig, sig], 1)
    lg, rg = np.cos((pan + 1) * np.pi / 4) * np.sqrt(2), np.sin((pan + 1) * np.pi / 4) * np.sqrt(2)
    sig = sig * np.array([lg, rg])
    n = min(len(sig), len(buf) - i0)
    if n > 0 and i0 >= 0:
        buf[i0:i0 + n] += sig[:n] * gain


def reverb(x, seconds=1.2, wet=0.16, seed=9):
    r = np.random.default_rng(seed)
    t = T(seconds)
    ir = np.stack([r.standard_normal(len(t)), r.standard_normal(len(t))], 1) * np.exp(-t / (seconds / 6.9))[:, None]
    ir = filt(ir, "low", 6000)
    ir /= np.sqrt((ir ** 2).sum(0))
    y = np.stack([fftconvolve(x[:, c], ir[:, c])[:len(x)] for c in range(2)], 1)
    return x * (1 - wet) + y * wet


def wystak_chime():
    """the sound of Wystak arriving: an airy shimmer rises into a glassy, slightly detuned FM bell chord
    (E major add9, arpeggiated upward), with a soft digital pitch settle and a ping-pong echo. Subtle, bright, future."""
    d = 3.4
    t = T(d)
    out = np.zeros((len(t), 2))
    # 1 · reverse shimmer swell into the hit (0.0-0.45s)
    sw = T(0.45)
    air = filt(rng.standard_normal(len(sw)), "band", [3500, 11000]) * (sw / sw[-1]) ** 2.6 * 0.35
    for c in range(2):
        out[:len(sw), c] += air
    hit = len(sw)
    # 2 · FM glass bells, arpeggiated upward, each settling in pitch from slightly sharp
    notes = [(76, 0.00, -0.35, 1.0), (83, 0.045, 0.3, 0.8), (88, 0.09, -0.15, 0.62), (90, 0.135, 0.4, 0.5), (95, 0.19, 0.0, 0.32)]
    for n, dt, pan, g in notes:
        tb = T(d - 0.45 - dt)
        f = 440 * 2 ** ((n - 69) / 12) * (1 + 0.012 * np.exp(-tb / 0.05))      # digital settle from +20 cents
        idx = 2.6 * np.exp(-tb / 0.18) + 0.25                                    # bright attack, glassy tail
        mod = np.sin(2 * np.pi * np.cumsum(f * 3.51) / SR)                     # inharmonic ratio: glass
        car = np.sin(2 * np.pi * np.cumsum(f) / SR + idx * mod)
        car2 = np.sin(2 * np.pi * np.cumsum(f * 1.003) / SR + idx * 0.8 * mod)  # slow beating shimmer
        env = (1 - np.exp(-tb / 0.004)) * np.exp(-tb / 1.1)
        b = (0.6 * car + 0.4 * car2) * env * g
        i0 = hit + int(dt * SR)
        lg, rg = np.cos((pan + 1) * np.pi / 4) * np.sqrt(2), np.sin((pan + 1) * np.pi / 4) * np.sqrt(2)
        out[i0:i0 + len(b), 0] += b * lg
        out[i0:i0 + len(b), 1] += b * rg
    # 3 · a soft sine an octave below for body
    tb = T(d - 0.45)
    out[hit:, :] += (np.sin(2 * np.pi * 329.63 * tb) * (1 - np.exp(-tb / 0.02)) * np.exp(-tb / 0.9) * 0.18)[:, None]
    out = filt(out, "high", 180)
    # 4 · ping-pong echo, darker each repeat
    wet = np.zeros_like(out)
    for k, (dl, g) in enumerate(((0.21, 0.32), (0.42, 0.2), (0.63, 0.12))):
        i = int(dl * SR)
        src = filt(out[:-i], "low", 7000 - 1500 * k)
        wet[i:, (k + 1) % 2] += src[:, k % 2] * g
    return out + wet


def set_down(weight=1.0):
    """a glass pass set onto the stack: a muted low touch, a tiny tick, a short ring (from the launch film)"""
    t = T(0.6)
    body = np.sin(2 * np.pi * np.cumsum(62 + 30 * np.exp(-t / 0.03)) / SR) * np.exp(-t / 0.09) * (1 - np.exp(-t / 0.004))
    tick = filt(rng.standard_normal(len(t)), "band", [2500, 7000]) * np.exp(-t / 0.006) * 0.35
    ring = np.sin(2 * np.pi * 2840 * t) * np.exp(-t / 0.09) * 0.05
    return body * 0.9 * weight + tick + ring


def settle():
    """the stack aligns: a soft, low settle with two gentle ticks"""
    t = T(1.2)
    out = np.sin(2 * np.pi * np.cumsum(50 + 16 * np.exp(-t / 0.08)) / SR) * np.exp(-t / 0.32) * (1 - np.exp(-t / 0.03)) * 0.9
    for dt in (0.0, 0.05):
        i = int(dt * SR); tk = filt(rng.standard_normal(1600), "band", [3000, 8000]) * np.exp(-np.arange(1600) / SR / 0.005) * 0.25
        out[i:i + len(tk)] += tk
    return out


def thump():
    t = T(1.2)
    f = 38 + 42 * np.exp(-t / 0.07)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / 0.38) * (1 - np.exp(-t / 0.004))


# the palette
NOTIF = lambda: smp(2357, 0.02, 0.19) * 0.8     # v10: a soft two-note bubble pop, the shape of a phone message alert
DING = lambda: smp(2870, 0.0, 1.1)              # clean confirmation ding (paid, reward unlocked)
LOCK = lambda: smp(2585, 0.0, 0.12)             # side-button click
TAP = lambda: smp(2568, 0.0, 0.12)              # soft UI tap
TICK = lambda: smp(2577, 0.0, 0.1)              # tiny tick (typing, rows, counting)
AIR = lambda: smp(1461, 0.0, 0.7)               # short air whoosh
ZOOM = lambda: smp(2608, 0.12, 0.7)             # air-zoom: the zoom-through cuts
SWEEP = lambda: smp(166, 0.0, 0.8)              # small fast sweep (cards, swipes)
WIND = lambda: smp(1471, 0.0, 1.45)             # soft cinematic wind (scene changes, leaks)
BREATH = lambda: smp(1489, 0.0, 2.3)            # long soft air
BELL = lambda: smp(3109, 0.0, 1.7)              # one gentle bell: Wystak
HUM = lambda: smp(2297, 0.4, 2.2)               # low room tone under the held introduction

sfx = np.zeros((N, 2))
P = lambda sig, t, g, pan=0.0: place(sfx, sig, t, g, pan)
W = {w["text"] + f"#{i}": w for i, w in enumerate(V11)}
word = lambda i: V11[i]["start"]

# the problem: alerts nobody reads
for t, g, p in ((3.05, 0.15, -0.25), (3.42, 0.13, 0.2), (3.78, 0.11, -0.1)):
    P(NOTIF(), M(t), g, p)
P(LOCK(), M(4.5), 0.10)                                            # the screen sleeps
P(NOTIF(), M(17.15), 0.15, 0.1)                                    # the café's message
P(NOTIF(), M(18.8), 0.15, -0.15)                                   # birthday
P(NOTIF(), M(20.38), 0.09, 0.25)                                   # the cousins, late
for i, t in enumerate([21.72, 22.0, 22.25, 22.46, 22.64, 22.8, 22.94]):
    P(NOTIF(), M(t), 0.07 + 0.008 * i, ((i * 0.37) % 1.4) - 0.7)   # everywhere: the same alert, again and again
# the question: the phone rises in near silence
P(AIR(), M(31.84), 0.035)
# the answer: the pass lands in the Wallet
P(set_down(0.8), M(34.6) + 0.25, 0.07)
# the introduction: light comes up, the name lands on one soft chime, the passes settle, we push through to the counter
P(BREATH()[: int(1.6 * SR)], INTRO[0] - 0.15, 0.04)
P(wystak_chime(), word(73) - 0.45, 0.06)                           # the chime's bell lands on "Why-stack."
P(settle(), word(73) + 0.15, 0.05)
P(AIR(), INTRO[1] + 0.1, 0.03)                                    # the push into the phone
# the payoff
P(DING(), M(40.95), 0.09)                                          # paid
P(NOTIF(), M(42.48), 0.17)                                         # the Wallet push: the one that matters
P(DING(), M(43.9), 0.06, 0.1)                                      # free cappuccino
P(BELL(), M(46.64), 0.10)                                          # the logo
sfx = filt(sfx, "low", 8500)                                       # no hard top end
sfx = reverb(sfx, 1.4, 0.2)


def write(path, x, peak_db=-3.0):
    x = x / max(1e-9, np.abs(x).max()) * 10 ** (peak_db / 20)
    with wave.open(str(path), "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((np.clip(x, -1, 1) * 32767).astype("<i2").tobytes())


write(ROOT / "assets/sfx.wav", sfx, -3.0)
print("wrote assets/sfx.wav", f"{N / SR:.2f}s")
