"""Synthesise the loyalty reel's music bed and sound effects (deterministic, no samples).

Arc (the brief's NOISE -> SIMPLICITY):
  0-17.7   memory: tanpura drone (Sa-Pa on D), warm D minor pad, sparse kalimba, soft heartbeat
  17.7-26.25 everywhere: pulse doubles, notification pings pile up, riser into the app fatigue
  26.25    lock click, then total silence; 26.55 one clean DING
  27-40    the wallet: D major pad, sparse kalimba, gentle heartbeat from the scan onwards
  40-40.74 recap hits, then a breath of silence; 40.74-44.02 resolution under the logo

usage (from the project folder): python3 sound/make_sound.py  -> assets/music-bed.wav, assets/sfx.wav
"""
import json, pathlib, wave
import numpy as np
from scipy.signal import butter, sosfilt, fftconvolve

SR = 48000
DUR = 51.39
N = int(round(SR * DUR))
BEAT = 60 / 96
ROOT = pathlib.Path(__file__).resolve().parent.parent
rng = np.random.default_rng(1007)


def T(d):
    return np.arange(int(round(SR * d))) / SR


def filt(x, kind, fc, order=2):
    fc = np.atleast_1d(fc) / (SR / 2)
    sos = butter(order, fc if fc.size > 1 else fc[0], kind, output="sos")
    return sosfilt(sos, x, axis=0)


def place(buf, sig, t0, gain=1.0, pan=0.0):
    i0 = int(round(t0 * SR))
    if sig.ndim == 1:
        lg, rg = np.cos((pan + 1) * np.pi / 4), np.sin((pan + 1) * np.pi / 4)
        sig = np.stack([sig * lg, sig * rg], 1) * np.sqrt(2)
    n = min(len(sig), len(buf) - i0)
    if n > 0 and i0 >= 0:
        buf[i0:i0 + n] += sig[:n] * gain


def reverb(x, seconds=2.4, wet=0.3, seed=3):
    r = np.random.default_rng(seed)
    t = T(seconds)
    ir = np.stack([r.standard_normal(len(t)), r.standard_normal(len(t))], 1) * np.exp(-t / (seconds / 6.9))[:, None]
    ir = filt(ir, "low", 6500)
    ir /= np.sqrt((ir ** 2).sum(0))
    y = np.stack([fftconvolve(x[:, c], ir[:, c])[:len(x)] for c in range(2)], 1)
    return x * (1 - wet) + y * wet


def fade(n, a, r):
    e = np.ones(n)
    a, r = int(a * SR), int(r * SR)
    if a:
        e[:a] = np.linspace(0, 1, a)
    if r:
        e[-r:] *= np.linspace(1, 0, r)
    return e


def hz(note):  # midi number -> Hz
    return 440 * 2 ** ((note - 69) / 12)


# ---------------------------------------------------------------- instruments
def tanpura(f0, dur=3.2):
    t = T(dur)
    s = np.zeros(len(t))
    for k in range(1, 26):
        fk = f0 * k * (1 + 0.0004 * k)
        swell = 1 + 1.8 * (k > 3) * np.exp(-((t - (0.25 + 0.05 * k)) / 0.5) ** 2)  # jawari shimmer
        e = (1 - np.exp(-t / 0.006)) * np.exp(-t / 1.9) * swell
        s += np.sin(2 * np.pi * fk * t + rng.uniform(0, 6.28)) * e / k ** 0.85
    return filt(s / np.abs(s).max(), "low", 4200)


def pad(notes, dur, a=1.2, r=1.2, cutoff=1400):
    t = T(dur)
    s = np.zeros(len(t))
    for n in notes:
        for cents in (-7, 0, 6):
            f = hz(n) * 2 ** (cents / 1200)
            ph = rng.uniform(0, 6.28)
            for k in range(1, 14):
                if f * k > 9000:
                    break
                s += np.sin(2 * np.pi * f * k * t + ph * k) / k
    s = filt(s, "low", cutoff) * fade(len(t), a, r)
    return s / np.abs(s).max()


def kalimba(note, dur=1.4):
    t = T(dur)
    f = hz(note)
    s = (np.sin(2 * np.pi * f * t) * np.exp(-t / 0.55)
         + 0.32 * np.sin(2 * np.pi * f * 2.76 * t) * np.exp(-t / 0.12)
         + 0.12 * np.sin(2 * np.pi * f * 5.4 * t) * np.exp(-t / 0.05))
    return s * (1 - np.exp(-t / 0.003))


def kick(gain=1.0):
    t = T(0.45)
    f = 46 + 70 * np.exp(-t / 0.03)
    s = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / 0.16)
    return s * gain


def tick(gain=1.0, bright=7000):
    t = T(0.05)
    s = filt(rng.standard_normal(len(t)), "high", bright) * np.exp(-t / 0.012)
    return s * gain


def noise(d):
    return rng.standard_normal(int(round(SR * d)))


# ---------------------------------------------------------------- sfx
def ping(f, d=0.6, bright=0.35):
    t = T(d)
    s = np.sin(2 * np.pi * f * t) * np.exp(-t / (d / 3.2)) + bright * np.sin(2 * np.pi * f * 2 * t) * np.exp(-t / (d / 6))
    return s * (1 - np.exp(-t / 0.002))


def chime_two(f1, f2, gap=0.11):  # payment soundbox, generic two-tone
    a = ping(f1, 0.45, 0.25)
    b = ping(f2, 0.7, 0.25)
    out = np.zeros(len(b) + int(gap * SR))
    out[:len(a)] += a
    out[int(gap * SR):] += b
    return out


def coin():
    t = T(1.1)
    s = sum(np.sin(2 * np.pi * f * t) * np.exp(-t / d) * g for f, d, g in
            ((3150, 0.35, 1.0), (4620, 0.22, 0.6), (6380, 0.14, 0.45), (7930, 0.09, 0.3), (2210, 0.5, 0.35)))
    click = filt(noise(0.012), "high", 3000) * np.exp(-T(0.012) / 0.003)
    s[:len(click)] += click * 0.6
    return s


def shutter():
    out = np.zeros(int(0.14 * SR))
    for t0, g in ((0.0, 1.0), (0.075, 0.7)):
        c = filt(noise(0.03), "band", [1800, 7000]) * np.exp(-T(0.03) / 0.006) * g
        place_mono(out, c, t0)
    return out


def place_mono(buf, sig, t0):
    i0 = int(t0 * SR)
    n = min(len(sig), len(buf) - i0)
    buf[i0:i0 + n] += sig[:n]


def whoosh(d=0.35, lo=600, hi=5000, rising=True):
    x = noise(d)
    a, b = filt(x, "band", [lo * 0.6, lo * 1.6]), filt(x, "band", [hi * 0.6, hi * 1.3])
    m = np.linspace(0, 1, len(x)) if rising else np.linspace(1, 0, len(x))
    env = np.sin(np.linspace(0, np.pi, len(x))) ** 1.5
    return (a * (1 - m) + b * m) * env


def pop(up=True):
    t = T(0.14)
    f = (380 + 560 * (1 - np.exp(-t / 0.03))) if up else (900 - 700 * (1 - np.exp(-t / 0.08)))
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / 0.05) * (1 - np.exp(-t / 0.002))


def keyclick():
    t = T(0.025)
    return filt(noise(0.025), "band", [1500, 6000]) * np.exp(-t / 0.004) + 0.3 * np.sin(2 * np.pi * 2300 * t) * np.exp(-t / 0.006)


def lock_click():
    out = np.zeros(int(0.08 * SR))
    for t0, g in ((0.0, 1.0), (0.018, 0.55)):
        place_mono(out, filt(noise(0.02), "band", [900, 5200]) * np.exp(-T(0.02) / 0.0035) * g, t0)
    return out


def ding():
    t = T(4.2)
    f = 1318.51  # E6: one clean bell
    s = (np.sin(2 * np.pi * f * t) * np.exp(-t / 1.6)
         + 0.18 * np.sin(2 * np.pi * f * 2.0 * t) * np.exp(-t / 0.7)
         + 0.07 * np.sin(2 * np.pi * f * 2.76 * t) * np.exp(-t / 0.35)
         + 0.25 * np.sin(2 * np.pi * f * 0.5 * t) * np.exp(-t / 2.2))
    return s * (1 - np.exp(-t / 0.0015))


def riser(d):
    t = T(d)
    sweep = np.sin(2 * np.pi * np.cumsum(180 * 2 ** (2.6 * t / d)) / SR)
    n = filt(noise(d), "band", [800, 6000])
    env = (t / d) ** 2.2
    return (0.55 * sweep + 0.45 * n) * env


def impact():
    t = T(1.4)
    f = 34 + 50 * np.exp(-t / 0.08)
    boom = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / 0.45)
    burst = filt(noise(1.4), "low", 2400) * np.exp(-t / 0.09)
    return boom + 0.5 * burst


def train_rush(d=1.2):
    x = filt(noise(d), "band", [180, 2600])
    env = np.exp(-((np.linspace(-1, 1, len(x))) / 0.45) ** 2)
    return x * env


def card_slide():
    t = T(0.22)
    s = filt(noise(0.22), "band", [1200, 5000]) * np.sin(np.linspace(0, np.pi, len(t))) ** 2 * 0.6
    th = np.sin(2 * np.pi * 140 * t) * np.exp(-((t - 0.16) / 0.02) ** 2) * 0.5
    return s + th


def swell(d=0.7):
    x = filt(noise(d), "high", 2500)
    return x * np.linspace(0, 1, len(x)) ** 3


def crackle(d, density=14):
    out = np.zeros(int(d * SR))
    for t0 in np.sort(rng.uniform(0, d - 0.01, int(d * density))):
        c = filt(noise(0.004), "high", 1500) * rng.uniform(0.2, 1.0)
        place_mono(out, c, t0)
    hiss = filt(noise(d), "band", [2000, 8000]) * 0.04
    return out + hiss


# ================================================================== BED
bed = np.zeros((N, 2))

# tanpura cycle (Pa, Sa, Sa, low Sa) through the memory section, and again under the logo
def tanpura_cycle(t0, t1, gain):
    seq = [hz(57), hz(62), hz(62), hz(50)]  # A2 D3 D3 D2
    t, i = t0, 0
    while t < t1:
        place(bed, tanpura(seq[i % 4]), t, gain * (0.9 if i % 4 else 1.0), pan=(-0.25, 0.2, 0.25, -0.1)[i % 4])
        t += 0.94
        i += 1
tanpura_cycle(0.0, 21.4, 0.16)
tanpura_cycle(45.6, 50.8, 0.12)

# pads: D minor add9 (memory), darker tension cluster (everywhere), D major 9 (wallet), open Dmaj9 (logo)
place(bed, pad([50, 57, 62, 65, 69, 76], 21.8, a=0.35, r=1.0, cutoff=1300), 0.0, 0.20)
place(bed, pad([50, 57, 62, 63, 65, 69], 8.4, a=0.6, r=0.05, cutoff=1700), 21.3, 0.20)
place(bed, pad([50, 57, 62, 66, 69, 73, 76], 15.4, a=1.6, r=0.25, cutoff=1500), 30.3, 0.20)
place(bed, pad([38, 50, 57, 64, 66, 69, 73], 5.77, a=0.25, r=2.2, cutoff=1600), 45.62, 0.25)

# kalimba lines (D minor pentatonic in the memory section, D major in the wallet section)
mem = [74, 77, 81, 79, 76, 74, 72, 69]
for i, b in enumerate(range(0, 40)):
    t = b * BEAT
    if 2.4 < t < 21.2 and i % 2 == 0:
        place(bed, kalimba(mem[(i // 2) % len(mem)]), t, 0.11, pan=0.35 if i % 4 else -0.35)
for i, b in enumerate(range(34, 48)):  # busier in "everywhere"
    for h in (0, 0.5):
        t = (b + h) * BEAT
        if 21.4 < t < 29.5:
            place(bed, kalimba(mem[(i * 2 + int(h * 2)) % len(mem)] + 12 * (i % 3 == 2)), t, 0.08, pan=0.5 if h else -0.5)
wal = [78, 81, 85, 83, 81, 78, 76, 74]
for i, b in enumerate(range(49, 74)):
    t = b * BEAT
    if 31.0 < t < 45.4 and i % 2 == 0:
        place(bed, kalimba(wal[(i // 2) % len(wal)]), t, 0.10, pan=0.3 if i % 4 else -0.3)

# pulse: half-time from the first cut, full with ticks in "everywhere", half again once the wallet arrives
for b in range(0, 84):
    t = b * BEAT
    if 4.6 < t < 21.3 and b % 2 == 0:
        place(bed, kick(), t, 0.28)
    if 21.3 <= t < 29.6:
        place(bed, kick(), t, 0.34)
    if 34.9 < t < 45.4 and b % 2 == 0:
        place(bed, kick(), t, 0.24)
    for h in (0.5,) if t < 21.3 else (0.25, 0.5, 0.75):
        tt = t + h * BEAT
        if 8.15 < tt < 21.3 and h == 0.5:
            place(bed, tick(), tt, 0.05, pan=0.3)
        if 21.3 <= tt < 29.6:
            place(bed, tick(bright=8000), tt, 0.045 if h != 0.5 else 0.07, pan=-0.3 if h == 0.25 else 0.3)

# riser into the lock click, then nothing
place(bed, riser(2.7), 26.95, 0.15)
bed[int(29.66 * SR):int(30.1 * SR)] = 0.0
bed = reverb(bed, 2.6, 0.32)
bed[int(29.66 * SR):int(30.12 * SR)] *= 0.0  # keep the silence clean after the reverb tail
bed *= fade(N, 0.02, 1.6)[:, None]

# ================================================================== SFX
sfx = np.zeros((N, 2))
place(sfx, swell(1.0), 0.0, 0.14)
place(sfx, ping(hz(74), 2.0, 0.2), 0.35, 0.14)
place(sfx, chime_two(hz(83), hz(88)), 1.15, 0.22)                 # "rewarding"
place(sfx, whoosh(0.3, 500, 3000), 2.66, 0.2)                     # phone rises
for t, n, p in ((3.05, 84, -0.3), (3.42, 81, 0.25), (3.78, 86, -0.1)):
    place(sfx, ping(hz(n)), t, 0.28, p)                           # unread notifications
place(sfx, lock_click(), 4.5, 0.5)                                # the screen sleeps
place(sfx, shutter(), 5.3, 0.42, 0.2)
place(sfx, card_slide(), 5.7, 0.35, -0.2)                         # data card
for i in range(4):
    place(sfx, keyclick(), 6.45 + i * 0.27, 0.32, 0.15)
place(sfx, coin()[: int(0.45 * SR)], 7.8, 0.3)                    # "not just cash"
place(sfx, whoosh(0.3, 500, 2600), 9.08, 0.16)
place(sfx, ping(hz(79), 0.6), 10.12, 0.16)
for t in (11.28, 12.38, 13.48):
    place(sfx, shutter(), t, 0.36, 0.2)
for t in (11.38, 12.45, 13.6):
    place(sfx, pop(), t, 0.28)                                    # visit / purchase / preference logged
place(sfx, whoosh(0.3, 500, 3000), 14.84, 0.2)
for i in range(12):
    place(sfx, pop(), 15.02 + i * 0.075, 0.18, ((i % 4) - 1.5) * 0.4)   # apps pop in
notes = [84, 79, 86, 81, 88, 83]
for i in range(6):
    place(sfx, ping(hz(notes[i]), 0.5), 16.3 + i * 0.11, 0.2, ((i * 0.37) % 1.4) - 0.7)
place(sfx, chime_two(hz(86), hz(93), 0.09), 17.15, 0.3)           # message from the café
place(sfx, shutter(), 18.18, 0.32)
place(sfx, chime_two(hz(86), hz(93), 0.09), 18.8, 0.32)           # birthday
place(sfx, ping(hz(74), 0.4, 0.1), 20.4, 0.2)                     # the cousins, late
place(sfx, whoosh(0.3, 500, 3000), 21.38, 0.2)
casc = [21.72, 21.95, 22.08, 22.26, 22.38, 22.52, 22.63, 22.74, 22.84, 22.94, 23.02, 23.1, 23.18]
cn = [84, 79, 86, 81, 88, 83, 76, 91, 85, 80, 87, 82, 89]
for i, (t, n) in enumerate(zip(casc, cn)):
    place(sfx, ping(hz(n), 0.5), t, 0.2 + 0.013 * i, pan=((i * 0.37) % 1.4) - 0.7)
place(sfx, impact(), 23.1, 0.58)                                  # "everywhere"
place(sfx, impact(), 23.42, 0.4)
place(sfx, train_rush(1.0), 23.0, 0.22)
place(sfx, ping(hz(84)), 24.22, 0.3)                              # SMS
place(sfx, whoosh(0.28, 700, 3600), 25.16, 0.18)
place(sfx, ping(hz(88), 0.5), 25.32, 0.28, 0.3)                   # chat
for t in (26.12, 26.32, 26.52):
    place(sfx, tick(bright=4000), t, 0.16)                        # jiggle
place(sfx, pop(), 26.2, 0.26)
place(sfx, pop(up=False), 26.74, 0.42)                            # app removed
place(sfx, whoosh(0.28, 700, 3600), 27.38, 0.18)
place(sfx, tick(bright=3000), 27.92, 0.3)                         # GET
place(sfx, whoosh(0.28, 700, 3600), 28.36, 0.18)
for i in range(4):
    place(sfx, keyclick(), 28.95 + i * 0.14, 0.34)                # OTP
place(sfx, lock_click(), 29.62, 0.9)
place(sfx, ding(), 30.12, 0.5)
place(sfx, ping(hz(81), 1.2, 0.15), 32.56, 0.12)
place(sfx, whoosh(0.35, 400, 2600), 33.82, 0.22)
place(sfx, card_slide(), 33.88, 0.42, -0.2)                       # the passes rise
place(sfx, card_slide(), 34.04, 0.36, 0.2)
place(sfx, whoosh(0.3, 500, 3000), 35.3, 0.2)                     # phones rise
place(sfx, card_slide(), 35.48, 0.4, -0.2)                        # passes drop into the wallets
place(sfx, card_slide(), 35.56, 0.36, 0.2)
place(sfx, chime_two(hz(83), hz(88)), 36.05, 0.26)
place(sfx, shutter(), 37.12, 0.32)
place(sfx, ping(hz(86), 0.5), 37.48, 0.18, -0.4)                  # scan
place(sfx, ping(hz(90), 0.5), 37.6, 0.18, 0.4)
place(sfx, pop(), 38.9, 0.28, -0.3)                               # wallet badges
place(sfx, pop(), 38.98, 0.28, 0.3)
place(sfx, shutter(), 39.62, 0.3)
place(sfx, chime_two(hz(83), hz(88)), 39.95, 0.34)                # paid
place(sfx, whoosh(0.3, 500, 2600), 41.22, 0.16)
place(sfx, chime_two(hz(86), hz(93), 0.09), 41.5, 0.42)           # the Wallet push: a warm rising two-note
place(sfx, swell(0.9), 41.7, 0.12)
place(sfx, shutter(), 43.42, 0.26)
place(sfx, ping(hz(88), 0.6), 44.12, 0.16)
place(sfx, impact(), 45.64, 0.34)                                 # logo
place(sfx, ping(hz(74), 3.0, 0.2), 45.66, 0.22)
place(sfx, ping(hz(81), 3.0, 0.2), 45.68, 0.14)
place(sfx, whoosh(0.5, 400, 2400), 46.06, 0.1)
place(sfx, ping(hz(86), 1.2, 0.2), 46.8, 0.14)
place(sfx, ping(hz(90), 1.6, 0.2), 47.98, 0.18)
sfx = reverb(sfx, 1.3, 0.22, seed=9)
sfx[int(29.72 * SR):int(30.1 * SR)] *= 0.0   # true silence before the ding

def write(path, x, peak_db=-3.0):
    x = x / max(1e-9, np.abs(x).max()) * 10 ** (peak_db / 20)
    with wave.open(str(path), "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((np.clip(x, -1, 1) * 32767).astype("<i2").tobytes())


write(ROOT / "assets/music-bed.wav", bed, -4.0)
write(ROOT / "assets/sfx.wav", sfx, -3.0)
print("wrote assets/music-bed.wav, assets/sfx.wav", f"{N / SR:.2f}s")
