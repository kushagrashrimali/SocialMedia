"""Sound for the WYSTAK launch intro: quiet, glassy, premium. Synthesised (deterministic), no music, no booms.

Every cue reads its time from src/timing.js, the same file that drives the picture:
  air        the cover pass lifts: soft moving air
  shimmer    light runs across the glass
  crystal    the logo comes fully into focus: one clear glass tone
  set        each glass pass sets down on the stack: a muted low touch and a tiny glass tick
  align      the fan closes into one stack: a soft low settle
  access     light runs down the deck
  resolve    the tagline: a quiet chord that opens and stays
usage (from the project folder): python3 -I sound/make_sound.py  -> assets/sfx.wav
"""
import json, pathlib, wave
import numpy as np
from scipy.signal import butter, sosfilt, fftconvolve

ROOT = pathlib.Path(__file__).resolve().parent.parent
T = json.loads((ROOT / "src/timing.js").read_text().split("window.WYSTAK_TIMING =", 1)[1].strip().rstrip(";"))
SR = 48000
DUR = T["duration"]
N = int(SR * DUR)
rng = np.random.default_rng(2026)


def t_(d):
    return np.arange(int(round(SR * d))) / SR


def filt(x, kind, fc, order=2):
    fc = np.atleast_1d(fc) / (SR / 2)
    return sosfilt(butter(order, fc if fc.size > 1 else fc[0], kind, output="sos"), x, axis=0)


def place(buf, sig, t0, gain=1.0, pan=0.0):
    if sig.ndim == 1:
        sig = np.stack([sig * np.cos((pan + 1) * np.pi / 4), sig * np.sin((pan + 1) * np.pi / 4)], 1) * np.sqrt(2)
    i0 = int(round(t0 * SR)); n = min(len(sig), len(buf) - i0)
    if n > 0:
        buf[i0:i0 + n] += sig[:n] * gain


def hz(m):
    return 440 * 2 ** ((m - 69) / 12)


def air(d):
    """moving air: noise through a band that slowly opens, panned left to centre"""
    t = t_(d); x = rng.standard_normal(len(t))
    lo = filt(x, "band", [300, 1400]); hi = filt(x, "band", [1400, 5200])
    m = (t / d) ** 1.4
    env = np.sin(np.pi * np.clip(t / d, 0, 1)) ** 1.6
    mono = (lo * (1 - m) * 0.7 + hi * m * 0.5) * env
    pan = -0.5 + 0.5 * (t / d)
    return np.stack([mono * np.cos((pan + 1) * np.pi / 4), mono * np.sin((pan + 1) * np.pi / 4)], 1) * np.sqrt(2)


def shimmer(d):
    """light on glass: a thin, high, breathing sheen with a few faint partials"""
    t = t_(d)
    x = filt(rng.standard_normal(len(t)), "band", [5500, 11000]) * 0.5
    for f in (hz(100), hz(103), hz(107)):
        x += np.sin(2 * np.pi * f * t + rng.uniform(0, 6.3)) * 0.05
    return x * np.sin(np.pi * t / d) ** 2


def glass_tone(note, d=3.2, bright=1.0):
    """one clear glass tone: a slightly inharmonic FM bell with a soft attack"""
    t = t_(d); f = hz(note)
    idx = (1.8 * np.exp(-t / 0.25) + 0.2) * bright
    mod = np.sin(2 * np.pi * f * 3.48 * t)
    s = np.sin(2 * np.pi * f * t + idx * mod) * 0.7 + np.sin(2 * np.pi * f * 2.002 * t) * 0.12 * np.exp(-t / 0.6)
    return s * (1 - np.exp(-t / 0.012)) * np.exp(-t / 1.15)


def set_down(weight=1.0):
    """a glass pass set onto the stack: a muted low touch, a tiny tick, a short ring"""
    t = t_(0.6)
    body = np.sin(2 * np.pi * np.cumsum(62 + 30 * np.exp(-t / 0.03)) / SR) * np.exp(-t / 0.09) * (1 - np.exp(-t / 0.004))
    tick = filt(rng.standard_normal(len(t)), "band", [2500, 7000]) * np.exp(-t / 0.006) * 0.35
    ring = np.sin(2 * np.pi * 2840 * t) * np.exp(-t / 0.09) * 0.05
    return (body * 0.9 * weight + tick + ring)


def settle():
    """the stack aligns: a soft, low settle with two gentle ticks"""
    t = t_(1.2)
    low = np.sin(2 * np.pi * np.cumsum(50 + 16 * np.exp(-t / 0.08)) / SR) * np.exp(-t / 0.32) * (1 - np.exp(-t / 0.03))
    out = low * 0.9
    for dt in (0.0, 0.05):
        i = int(dt * SR); tk = filt(rng.standard_normal(1600), "band", [3000, 8000]) * np.exp(-np.arange(1600) / SR / 0.005) * 0.25
        out[i:i + len(tk)] += tk
    return out


def resolve(d):
    """a quiet chord that opens under the tagline and stays: E major add9, soft and wide"""
    t = t_(d); s = np.zeros((len(t), 2))
    for k, (n, g) in enumerate(((52, 0.5), (59, 0.42), (64, 0.36), (68, 0.26), (71, 0.2), (78, 0.12))):
        for cents, side in ((-5, 0), (5, 1)):
            f = hz(n) * 2 ** (cents / 1200)
            ph = rng.uniform(0, 6.3)
            tone = np.sin(2 * np.pi * f * t + ph) + 0.18 * np.sin(2 * np.pi * 2 * f * t + ph) + 0.05 * np.sin(2 * np.pi * 3 * f * t)
            s[:, side] += tone * g
    att, rel = 1.1, 1.3
    env = np.minimum(1, t / att) ** 2 * np.clip((d - t) / rel, 0, 1)
    s = filt(s, "low", 2600) * env[:, None]
    return s


def reverb(x, seconds=2.6, wet=0.32, seed=4):
    r = np.random.default_rng(seed); t = t_(seconds)
    ir = np.stack([r.standard_normal(len(t)), r.standard_normal(len(t))], 1) * np.exp(-t / (seconds / 6.9))[:, None]
    ir = filt(ir, "low", 7000); ir /= np.sqrt((ir ** 2).sum(0))
    y = np.stack([fftconvolve(x[:, c], ir[:, c])[:len(x)] for c in range(2)], 1)
    return x * (1 - wet) + y * wet


sfx = np.zeros((N, 2))
P = T["pane"]; K = T["stack"]; G = T["tagline"]
place(sfx, air(P["liftDur"] + 0.6), max(0.0, P["lift"] - 0.2), 0.10)
place(sfx, shimmer(T["sweep1"]["dur"]), T["sweep1"]["at"], 0.06, -0.2)
place(sfx, glass_tone(88, 3.6), T["logo"]["sharpAt"], 0.16, -0.1)                 # E6, the logo arrives
place(sfx, glass_tone(95, 3.0, 0.7), T["logo"]["sharpAt"] + 0.09, 0.07, 0.25)     # B6, its octave-fifth
place(sfx, air(T["sheets"]["dur"] + 0.8), T["sheets"]["at"], 0.035, 0.3)
for i in range(4):                                                                # each pass sets down
    place(sfx, set_down(0.8 + 0.07 * i), K["inAt"] + i * K["gap"] + 0.28, 0.18, (-0.45, -0.15, 0.15, 0.45)[i])
place(sfx, settle(), K["organiseAt"] + K["organiseDur"] - 0.12, 0.2)            # the stack aligns
place(sfx, shimmer(K["accessDur"] + 0.3), K["accessAt"], 0.05, 0.15)
place(sfx, resolve(DUR - G["at"] + 0.2), G["at"] - 0.25, 0.085)
place(sfx, glass_tone(83, 2.6, 0.6), G["at"] + 0.05, 0.06, 0.0)                   # B5, a last soft glint
sfx = reverb(sfx)
sfx *= np.clip((DUR - t_(DUR)) / 0.25, 0, 1)[:, None]                               # clean tail at the very end
sfx = sfx / max(1e-9, np.abs(sfx).max()) * 10 ** (-3 / 20)
with wave.open(str(ROOT / "assets/sfx.wav"), "wb") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((np.clip(sfx, -1, 1) * 32767).astype("<i2").tobytes())
print("wrote assets/sfx.wav", DUR, "s")
