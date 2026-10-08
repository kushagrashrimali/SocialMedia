"""Voiceover: the final script (ElevenLabs, Kendra), cut to 39.8s.

The take has 44.9s of speech, so it is sped up (Rubber Band, pitch and formants kept) and its pauses are tightened.
Pauses that carry the story are set after the speed-up, by hand:
  after "...another place?"   the breath before "Introducing Why-stack." (the turn from the problem to the answer)
  after the name             the logo finishes building
  before the end card's "Why-stack.", and the end hold.
Inputs: assets/voiceover-src.mp3 and its word alignment assets/words-src.json (pocketsphinx, see BRIEF.md).
Outputs: assets/voiceover.wav, assets/words.json.
usage (from the project folder): python3 -I storyboard/edit_vo_v11.py
"""
import json, pathlib, re, subprocess, wave
import numpy as np

P = pathlib.Path(__file__).resolve().parent.parent
DUR = 39.8
SR = 48000
GAP = {"comma": 0.09, "list": 0.10, "sentence": 0.13}          # before the speed-up
SPECIAL = {"place?": 0.55, "Why-stack.#1": 0.42, "notice.": 0.26}   # after the speed-up (seconds of silence)
END_HOLD = 0.40

raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(P / "assets/voiceover-src.mp3"), "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"],
                     capture_output=True, check=True).stdout
x = np.frombuffer(raw, np.float32).astype(np.float64)
W = json.loads((P / "assets/words-src.json").read_text())
END = len(x) / SR

# every pause in the take (below -40 dBFS for 0.1s or more), from ffmpeg silencedetect
log = subprocess.run(["ffmpeg", "-i", str(P / "assets/voiceover-src.mp3"), "-af", "silencedetect=noise=-40dB:d=0.1", "-f", "null", "-"],
                     capture_output=True, text=True).stderr
st = [float(v) for v in re.findall(r"silence_start: ([\d.]+)", log)]
en = [float(v) for v in re.findall(r"silence_end: ([\d.]+)", log)]
SIL = [(a, b) for a, b in zip(st, en) if a > 0.05 and b < END - 0.05]

# what each pause follows: the last word starting before it
seen, plan = {}, []                                     # (start, end, pre-speed length, post-speed pause)
for a, b in SIL:
    i = max(k for k, w in enumerate(W) if w["start"] < a)
    txt = W[i]["text"]
    nxt = W[i + 1]["text"] if i + 1 < len(W) else ""
    if not (txt[-1] in ".?," and W[i + 1]["start"] >= a - 0.05 if i + 1 < len(W) else True):
        plan.append((a, b, min(b - a, 0.08), 0.0)); continue  # a pause inside a phrase: keep it short
    seen[txt] = seen.get(txt, 0) + 1
    key = f"{txt}#{seen[txt]}" if f"{txt}#{seen[txt]}" in SPECIAL else txt
    if key in SPECIAL:
        plan.append((a, b, 0.06, SPECIAL[key]))
    elif txt.endswith(","):
        plan.append((a, b, min(b - a, GAP["comma"]), 0.0))
    elif txt in ("visit.", "purchase.", "SMS.", "chat.") or nxt in ("Every", "Another"):
        plan.append((a, b, min(b - a, GAP["list"]), 0.0))
    else:
        plan.append((a, b, min(b - a, GAP["sentence"]), 0.0))

# pre-speed edit: each pause shortened to its length, keeping its own edges (natural decay and breath-in)
parts, knots, t, pos = [], [(0.0, 0.0)], 0.0, 0.0
marks = []                                              # pre-speed times where a post-speed pause opens
for a, b, g, p in plan:
    parts.append(x[int(pos * SR):int(a * SR)]); t += a - pos
    knots.append((a, t))
    h = g / 2
    parts.append(x[int(a * SR):int((a + h) * SR)]); parts.append(x[int((b - h) * SR):int(b * SR)])
    if p: marks.append((t + h, p))
    t += 2 * h; knots.append((b, t)); pos = b
parts.append(x[int(pos * SR):]); t += END - pos; knots.append((END, t))
y = np.concatenate(parts)
speech = END - sum(b - a for a, b, _, _ in plan)
post = sum(p for *_, p in plan) + END_HOLD
R = (len(y) / SR) / (DUR - post)
print(f"{len(plan)} pauses, speech {speech:.2f}s, edit {len(y) / SR:.2f}s, tempo {R:.3f}")

proc = subprocess.run(["ffmpeg", "-v", "error", "-f", "f64le", "-ar", str(SR), "-ac", "1", "-i", "-", "-af",
                       f"rubberband=tempo={R:.5f}:pitchq=quality:formant=preserved:window=standard", "-f", "f64le", "-"],
                      input=y.tobytes(), capture_output=True, check=True).stdout
z = np.frombuffer(proc, np.float64)
ka, kb = np.array([k[0] for k in knots]), np.array([k[1] for k in knots])

def T(src):
    """source time -> final time"""
    u = float(np.interp(src, ka, kb)) / R
    return u + sum(p for m, p in marks if m / R <= u + 1e-6)

out, pos = [], 0
for m, p in marks:
    cut = int(round(m / R * SR)); out += [z[pos:cut], np.zeros(int(round(p * SR)))]; pos = cut
out.append(z[pos:])
v = np.concatenate(out)
n = int(DUR * SR)
v = np.concatenate([v, np.zeros(max(0, n - len(v)))])[:n]
fade = int(0.02 * SR); v[-fade:] *= np.linspace(1, 0, fade)
v = v / np.abs(v).max() * 10 ** (-2.0 / 20)
with wave.open(str(P / "assets/voiceover.wav"), "wb") as o:
    o.setnchannels(1); o.setsampwidth(2); o.setframerate(SR)
    o.writeframes((v * 32767).astype("<i2").tobytes())
words = [{"text": w["text"], "start": round(T(w["start"]), 3), "end": round(T(min(w["end"], END)), 3)} for w in W]
(P / "assets/words.json").write_text(json.dumps(words, indent=1))
print("wrote voiceover.wav", len(v) / SR, "s; last word ends", words[-1]["end"])
