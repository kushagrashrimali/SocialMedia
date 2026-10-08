"""Sound effects for the loyalty reel, v5: real recorded sounds, placed subtly.

Every notification is one quick three-note ascending chime (the classic phone text-tone shape), the payment and the free reward are one clean
confirmation ding, the lock is a real switch click, and transitions are soft air whooshes. All samples are
Mixkit sound effects (Mixkit Sound Effects Free License), kept in assets/sfx-src/ (see assets/MANIFEST.md).
Synthesised: the Wystak chime (a soft rising shimmer into a glassy FM bell chord with a ping-pong echo)
and the low thump under the logo.

usage (from the project folder): python3 -I sound/make_sound.py  -> assets/sfx.wav
"""
import pathlib, subprocess, wave
import numpy as np
from scipy.signal import butter, sosfilt, fftconvolve

SR = 48000
DUR = 52.39
N = int(round(SR * DUR))
ROOT = pathlib.Path(__file__).resolve().parent.parent
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


def glints(n=7, seed=3):
    """sparkle: a few tiny, high, glassy pings scattered over ~0.4s (very quiet)"""
    r = np.random.default_rng(seed)
    out = np.zeros((int(0.9 * SR), 2))
    for i in range(n):
        f = r.choice([2637.0, 3135.96, 3520.0, 3951.07, 4698.63])         # E7 G7 A7 B7 D8: the E minor of the bed
        t = T(0.35)
        g = np.sin(2 * np.pi * f * t) * np.exp(-t / 0.07) * (1 - np.exp(-t / 0.002)) * (0.5 + 0.5 * r.random())
        i0 = int(r.random() * 0.45 * SR)
        pan = r.uniform(-0.7, 0.7)
        out[i0:i0 + len(t), 0] += g * np.cos((pan + 1) * np.pi / 4)
        out[i0:i0 + len(t), 1] += g * np.sin((pan + 1) * np.pi / 4)
    return out


def thump():
    t = T(1.2)
    f = 38 + 42 * np.exp(-t / 0.07)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / 0.38) * (1 - np.exp(-t / 0.004))


# the palette
NOTIF = lambda: smp(766, 0.0, 0.95) * 0.63      # quick three-note ascending chime (matched to the old alert level)
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

# opening montage: club -> salon -> café, each cut breathes
P(BREATH(), 0.0, 0.10)
P(ZOOM(), 0.86, 0.10, -0.3); P(ZOOM(), 1.71, 0.10, 0.3)
P(AIR(), 2.55, 0.14)                                               # into the lock screen
for t, g, p in ((3.05, 0.30, -0.25), (3.42, 0.26, 0.2), (3.78, 0.23, -0.1)):
    P(NOTIF(), t, g, p)                                            # unread, unnoticed
P(LOCK(), 4.5, 0.32)                                               # the screen sleeps
P(BREATH()[: int(1.0 * SR)], 5.05, 0.10)                           # out to the counters
P(SWEEP(), 5.56, 0.10, 0.2)                                        # the profile card swings in
for i in range(4):
    P(TICK(), 6.5 + i * 0.27, 0.10, 0.15)                          # rows fill in
P(ZOOM(), 6.46, 0.08, -0.3); P(ZOOM(), 7.66, 0.08, 0.3)
P(WIND(), 8.85, 0.12)                                              # light leak into the barber's
for t, p in ((11.19, -0.3), (12.29, 0.3), (13.39, -0.2)):
    P(ZOOM(), t, 0.09, p)
for t, p in ((11.6, -0.2), (12.6, 0.0), (13.78, 0.2)):
    P(TAP(), t, 0.13, p)                                           # chips land
P(AIR(), 14.7, 0.13)                                               # the home screen
for i in range(12):
    P(TICK(), 15.05 + i * 0.07, 0.035, ((i % 4) - 1.5) * 0.35)     # apps settle in, barely there
P(NOTIF(), 17.15, 0.34, 0.1)                                       # the café's message
P(TAP(), 17.78, 0.15)                                              # v8: the hand taps the banner
P(ZOOM(), 17.82, 0.13)                                             # and the camera pushes through it into the café
P(NOTIF(), 18.8, 0.36, -0.15)                                      # birthday
P(NOTIF(), 20.38, 0.22, 0.25)                                      # the cousins, late
P(AIR(), 21.25, 0.13)
for i, t in enumerate([21.72, 22.0, 22.25, 22.46, 22.64, 22.8, 22.94]):
    P(NOTIF(), t, 0.20 + 0.02 * i, ((i * 0.37) % 1.4) - 0.7)       # the flood: one real alert, again and again
P(WIND(), 22.95, 0.16); P(thump(), 23.1, 0.12)                     # "everywhere": the stack bursts
P(SWEEP(), 23.95, 0.10, -0.3)                                      # the cloud slides away
P(TAP(), 24.3, 0.10)                                               # SMS opens
P(SWEEP(), 25.12, 0.08, 0.3)                                       # chat
P(TICK(), 26.12, 0.10); P(TAP(), 26.58, 0.13)                      # long-press, Remove App
P(AIR()[: int(0.4 * SR)], 26.72, 0.08)                             # the app goes
P(SWEEP(), 27.34, 0.08, 0.3)                                       # store
P(TAP(), 27.92, 0.15)                                              # GET
P(SWEEP(), 28.32, 0.08, -0.3)                                      # login
for i in range(4):
    P(TICK(), 28.95 + i * 0.14, 0.14)                              # OTP
P(TAP(), 29.36, 0.13)                                              # v8: Verify
P(LOCK(), 29.58, 0.5)                                              # click. silence.
# the introduction: one bell, low room tone, the light across the mark
P(wystak_chime(), 30.12 - 0.45, 0.10)                              # the Wystak chime lands with the mark
P(HUM(), 30.15, 0.08)
P(SWEEP(), 30.3, 0.05)                                             # the wordmark wipes on
P(BREATH()[: int(1.4 * SR)], 31.78, 0.12)                          # the lockup flies into the rising phone
for i in range(6):
    P(AIR(), 32.3 + i * 0.11, 0.04, (-0.6, 0.6)[i % 2])            # the scattered places drift in
P(ZOOM(), 34.08, 0.14)                                             # pulled into the phone
P(SWEEP(), 34.52, 0.09, -0.2); P(TAP(), 34.66, 0.12)               # the stack fills, the pass lands
P(BREATH()[: int(1.2 * SR)], 35.85, 0.10)                          # camera pulls back
P(SWEEP(), 36.0, 0.09, 0.4)                                        # the Android phone arrives
P(TAP(), 36.55, 0.09, -0.3); P(TAP(), 36.63, 0.09, 0.3)
P(WIND(), 37.85, 0.10)                                             # out to the counter
P(TAP(), 38.55, 0.12)                                              # scan
P(ZOOM(), 40.53, 0.09)
P(DING(), 40.95, 0.30)                                             # paid
P(AIR(), 42.07, 0.12)
P(NOTIF(), 42.48, 0.42)                                            # the Wallet push: the one that matters
P(TAP(), 42.96, 0.14)                                              # v8: the hand taps the Wallet push
P(SWEEP(), 43.0, 0.08, 0.3)                                        # and it opens into the points ring
for i in range(9):
    P(TICK(), 43.1 + i * 0.09, 0.05 + 0.006 * i)                    # points counting up
P(DING(), 43.9, 0.2)                                               # free cappuccino
P(WIND(), 44.1, 0.11)                                              # leak into the montage
P(SWEEP(), 44.46, 0.09, -0.2)                                      # every category's pass deals into one stack
for i in range(5):
    P(TICK(), 44.62 + i * 0.08, 0.06, (i - 2) * 0.2)
P(TAP(), 44.98, 0.12)                                              # the Cafe Aroma pass settles on top
P(ZOOM(), 45.08, 0.08, 0.3); P(ZOOM(), 45.81, 0.08, -0.3)
P(BREATH()[: int(0.9 * SR)], 45.9, 0.10)                           # the frame blows out to white
P(BELL(), 46.64, 0.30); P(thump(), 46.64, 0.16)                    # the logo
P(SWEEP(), 47.02, 0.05)
P(TAP(), 47.78, 0.10, -0.2); P(TAP(), 48.96, 0.10, 0.2)            # the tagline, word by word
for k, (t, g) in enumerate(((1.3, 0.05), (34.86, 0.06), (43.9, 0.06), (46.72, 0.06), (49.02, 0.05))):
    P(glints(seed=11 + k), t, g)                                   # v8: sparkle bursts
sfx = reverb(sfx, 1.2, 0.16)
sfx[int(29.72 * SR):int(30.08 * SR)] *= 0.0                        # true silence after the click


def write(path, x, peak_db=-3.0):
    x = x / max(1e-9, np.abs(x).max()) * 10 ** (peak_db / 20)
    with wave.open(str(path), "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((np.clip(x, -1, 1) * 32767).astype("<i2").tobytes())


write(ROOT / "assets/sfx.wav", sfx, -3.0)
print("wrote assets/sfx.wav", f"{N / SR:.2f}s")
