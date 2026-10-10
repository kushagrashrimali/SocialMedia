"""Sound for the palm reveal (10 s): minimal, only the story makes a sound.

  0-10      the seaside: slow wave washes, the fountains' hiss, a breath of air
  1.6-3.4   a gust through the crowns: wind and palm-frond rustle, one low woody creak as the trunks flex
  3.4-5.4   a slow stretching creak that hands over to a smooth rising tone as the navy climbs (wood becoming lacquer)
  6.40      the W settles: a soft low touch, felt more than heard
  6.62-6.82 three clean flicks, one per pass (the ticket, the purple pass, the teal pass)
  7.60      the Wystak chime (synthesised, from the loyalty reel) as the fan completes, and the hold
Everything is synthesised except the pass flicks (Mixkit 166 "Fast small sweep transition", Mixkit Sound Effects Free
License, from videos/loyalty-evolution-reel/assets/sfx-src/). The effects bus is low-passed at 8.5 kHz.

usage: python3 -I sound/make_sound.py   (from videos/wystak-palm-reveal)  -> renders/sound.wav
"""
import pathlib, subprocess, wave
import numpy as np
from scipy.signal import butter, sosfilt, fftconvolve

ROOT = pathlib.Path(__file__).resolve().parent.parent
SFX = ROOT.parent / "loyalty-evolution-reel" / "assets" / "sfx-src"
SR = 48000
DUR = 10.0
N = int(SR * DUR)
rng = np.random.default_rng(2026)


def T(d):
    return np.arange(int(round(SR * d))) / SR


def filt(x, kind, fc, order=2):
    fc = np.atleast_1d(np.asarray(fc, float)) / (SR / 2)
    sos = butter(order, fc if fc.size > 1 else fc[0], kind, output="sos")
    return sosfilt(sos, x, axis=0)


def env(t, pts):
    """piecewise-linear envelope through (time, gain) points"""
    xs, ys = zip(*pts)
    return np.interp(t, xs, ys)


def place(buf, sig, t0, gain=1.0, pan=0.0):
    i0 = int(round(t0 * SR))
    if sig.ndim == 1:
        sig = np.stack([sig, sig], 1)
    lg, rg = np.cos((pan + 1) * np.pi / 4) * np.sqrt(2), np.sin((pan + 1) * np.pi / 4) * np.sqrt(2)
    sig = sig * np.array([lg, rg])
    n = min(len(sig), len(buf) - i0)
    if n > 0 and i0 >= 0:
        buf[i0:i0 + n] += sig[:n] * gain


def smp(sid, start=0.0, dur=None, rate=1.0):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(SFX / f"mixkit-{sid}.mp3"), "-ac", "2", "-ar", str(SR), "-f", "f32le", "-"],
                         capture_output=True, check=True).stdout
    x = np.frombuffer(raw, np.float32).reshape(-1, 2).astype(np.float64)
    x = x / max(1e-9, np.abs(x).max())
    x = x[int(start * SR):]
    if dur:
        x = x[:int(dur * SR)].copy()
        r = min(len(x), int(0.02 * SR)); x[-r:] *= np.linspace(1, 0, r)[:, None]
    if rate != 1.0:
        idx = np.arange(0, len(x) - 1, rate)
        x = np.stack([np.interp(idx, np.arange(len(x)), x[:, c]) for c in range(2)], 1)
    return x


# ------------------------------------------------------------------------------------------------ the seaside
def seaside():
    t = T(DUR)
    out = np.zeros((N, 2))
    # wave washes: low noise swelling every few seconds, with a brighter foam on each wash
    swell = 0.55 + 0.45 * np.clip(np.sin(2 * np.pi * t / 4.6 - 0.8), -0.3, 1) ** 2
    swell = np.convolve(swell, np.ones(2400) / 2400, "same")
    for c in range(2):
        body = filt(rng.standard_normal(N), "low", 520, 2) * 1.6
        foam = filt(rng.standard_normal(N), "band", [1800, 5200], 2) * np.clip(swell - 0.6, 0, None) * 1.4
        out[:, c] += (body * swell + foam) * 0.22
    # the fountains: a steady soft hiss, the near one a little left of centre
    for pan, g in ((-0.15, 0.11), (0.6, 0.06)):
        h = filt(rng.standard_normal(N), "band", [1500, 7000], 2) * (1 + 0.15 * filt(rng.standard_normal(N), "low", 6, 1))
        place(out, h, 0, g, pan)
    # air
    for c in range(2):
        out[:, c] += filt(rng.standard_normal(N), "low", 180, 2) * 0.10
    out *= env(t, [(0, 0.0), (0.35, 1.0), (9.5, 1.0), (10.0, 0.0)])[:, None]
    return out


# ------------------------------------------------------------------------------------------------ the gust and the creaks
def gust():
    d = 2.2
    t = T(d)
    e = env(t, [(0, 0), (0.6, 0.6), (1.0, 1.0), (1.5, 0.7), (2.2, 0)])
    out = np.zeros((len(t), 2))
    for c in range(2):
        n = rng.standard_normal(len(t))
        # wind: a band that opens as the gust builds
        lo = filt(n, "band", [250, 1100], 2) * e
        # palm fronds: dry, fast rustle (sparse crackle, high band), riding the gust a little late
        crack = (rng.random(len(t)) < 0.004 + 0.02 * np.roll(e, int(0.12 * SR))) * rng.standard_normal(len(t))
        rust = filt(crack, "band", [2500, 7500], 2) * 3.0 + filt(rng.standard_normal(len(t)), "band", [3000, 7000], 2) * 0.25 * e
        out[:, c] = lo * 0.9 + rust * np.roll(e, int(0.12 * SR)) * 0.5
    return out


def creak(d, rate0, rate1, gain=1.0, res=(260, 610, 1150)):
    """stick-slip wood: an irregular pulse train through woody resonances"""
    t = T(d)
    rate = np.linspace(rate0, rate1, len(t)) * (1 + 0.25 * filt(rng.standard_normal(len(t)), "low", 8, 1) * 4)
    ph = np.cumsum(np.clip(rate, 5, None)) / SR
    pulses = np.diff(np.floor(ph), prepend=0) > 0
    x = pulses * (0.6 + 0.4 * rng.random(len(t)))
    y = np.zeros(len(t))
    for f, q in zip(res, (0.10, 0.07, 0.05)):
        y += filt(x, "band", [f * (1 - q), f * (1 + q)], 2)
    e = env(t, [(0, 0), (d * 0.2, 1), (d * 0.75, 0.8), (d, 0)])
    return filt(y * e, "low", 2500) * gain


def lacquer_tone(d):
    """a smooth tone rising under the navy as it climbs: soft, warm, no edges"""
    t = T(d)
    f = 98 * 2 ** (np.clip(t / d, 0, 1) * 1.0)
    ph = 2 * np.pi * np.cumsum(f) / SR
    x = np.sin(ph) + 0.35 * np.sin(2 * ph + 0.3) + 0.12 * np.sin(3 * ph)
    shimmer = filt(rng.standard_normal(len(t)), "band", [900, 2600], 2) * 0.05
    e = env(t, [(0, 0), (d * 0.35, 0.6), (d * 0.85, 1.0), (d, 0)])
    return (x * 0.5 + shimmer) * e


def settle():
    t = T(1.0)
    return np.sin(2 * np.pi * np.cumsum(58 + 22 * np.exp(-t / 0.05)) / SR) * np.exp(-t / 0.22) * (1 - np.exp(-t / 0.02))


def wystak_chime():
    """the Wystak chime (as in the loyalty reel): an airy shimmer into a glassy, slightly detuned FM bell chord
    (E major add9, arpeggiated upward), a soft pitch settle and a ping-pong echo. The hit lands 0.45 s in."""
    d = 3.4
    t = T(d)
    out = np.zeros((len(t), 2))
    sw = T(0.45)
    air = filt(rng.standard_normal(len(sw)), "band", [3500, 11000]) * (sw / sw[-1]) ** 2.6 * 0.35
    out[:len(sw)] += air[:, None]
    hit = len(sw)
    notes = [(76, 0.00, -0.35, 1.0), (83, 0.045, 0.3, 0.8), (88, 0.09, -0.15, 0.62), (90, 0.135, 0.4, 0.5), (95, 0.19, 0.0, 0.32)]
    for n, dt, pan, g in notes:
        tb = T(d - 0.45 - dt)
        f = 440 * 2 ** ((n - 69) / 12) * (1 + 0.012 * np.exp(-tb / 0.05))
        idx = 2.6 * np.exp(-tb / 0.18) + 0.25
        mod = np.sin(2 * np.pi * np.cumsum(f * 3.51) / SR)
        car = np.sin(2 * np.pi * np.cumsum(f) / SR + idx * mod)
        car2 = np.sin(2 * np.pi * np.cumsum(f * 1.003) / SR + idx * 0.8 * mod)
        e = (1 - np.exp(-tb / 0.004)) * np.exp(-tb / 1.1)
        b = (0.6 * car + 0.4 * car2) * e * g
        i0 = hit + int(dt * SR)
        lg, rg = np.cos((pan + 1) * np.pi / 4) * np.sqrt(2), np.sin((pan + 1) * np.pi / 4) * np.sqrt(2)
        out[i0:i0 + len(b), 0] += b * lg
        out[i0:i0 + len(b), 1] += b * rg
    tb = T(d - 0.45)
    out[hit:, :] += (np.sin(2 * np.pi * 329.63 * tb) * (1 - np.exp(-tb / 0.02)) * np.exp(-tb / 0.9) * 0.18)[:, None]
    out = filt(out, "high", 180)
    wet = np.zeros_like(out)
    for k, (dl, g) in enumerate(((0.21, 0.32), (0.42, 0.2), (0.63, 0.12))):
        i = int(dl * SR)
        src = filt(out[:-i], "low", 7000 - 1500 * k)
        wet[i:, (k + 1) % 2] += src[:, k % 2] * g
    return out + wet


def air_space(x, seconds=0.6, wet=0.10):
    """an open-air tail: short, dark, mostly early reflections"""
    t = T(seconds)
    r = np.random.default_rng(4)
    ir = np.stack([r.standard_normal(len(t)), r.standard_normal(len(t))], 1) * np.exp(-t / (seconds / 6.9))[:, None]
    ir = filt(ir, "low", 4500); ir /= np.sqrt((ir ** 2).sum(0))
    y = np.stack([fftconvolve(x[:, c], ir[:, c])[:len(x)] for c in range(2)], 1)
    return x * (1 - wet) + y * wet


def main():
    amb = seaside()
    fx = np.zeros((N, 2))
    place(fx, gust(), 1.45, 0.55, -0.1)
    place(fx, creak(0.9, 18, 34, 0.9), 2.05, 1.0, -0.25)
    place(fx, creak(1.9, 14, 60, 0.7), 3.35, 1.0, 0.1)
    place(fx, lacquer_tone(1.9), 3.95, 0.16, 0.0)
    place(fx, settle(), 6.38, 0.30, 0.0)
    for t0, rate, pan, g in ((6.62, 1.00, 0.15, 0.30), (6.70, 1.06, 0.3, 0.34), (6.82, 1.12, 0.45, 0.34)):
        place(fx, filt(smp(166, 0.0, 0.32, rate), "high", 600), t0, g, pan)
    place(fx, wystak_chime(), 7.60 - 0.45, 0.62, 0.0)
    fx = filt(fx, "low", 8500)
    fx = air_space(fx)
    # the seaside steps back a little while the chime rings
    duck = env(np.arange(N) / SR, [(0, 1), (7.4, 1), (7.7, 0.7), (9.3, 0.8), (10, 0.8)])[:, None]
    mix = amb * duck + fx
    mix *= 0.5 / np.abs(mix).max()
    out = ROOT / "renders" / "sound.wav"
    out.parent.mkdir(exist_ok=True)
    pcm = (np.clip(mix, -1, 1) * 32767).astype("<i2")
    with wave.open(str(out), "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())
    print(out)


if __name__ == "__main__":
    main()
