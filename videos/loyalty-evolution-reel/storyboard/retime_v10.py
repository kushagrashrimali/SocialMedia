"""Retime the voiceover and its word timings from v9 to v10 (see tmap_v10.py): insert the introduction's extra 1.5s
of silence, remove the short slices of silence listed in CUTS, end at 51.0s. Reads the v9 files from git (commit 49fbf99),
so it can be re-run safely.
usage (from the project folder): python3 -I storyboard/retime_v10.py
"""
import io, json, pathlib, subprocess, sys, wave
import numpy as np
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from tmap_v10 import M, CUTS, DUR, INTRO_NEW, INTRO_OLD

P = pathlib.Path(__file__).resolve().parent.parent
V9 = "49fbf99"
git = lambda path: subprocess.run(["git", "show", f"{V9}:./{path}"], cwd=P, capture_output=True, check=True).stdout

w = wave.open(io.BytesIO(git("assets/voiceover.wav")))
sr, ch = w.getframerate(), w.getnchannels()
x = np.frombuffer(w.readframes(w.getnframes()), np.int16).reshape(-1, ch)
S = lambda t: int(round(t * sr))
gap = (INTRO_NEW[1] - INTRO_NEW[0]) - (INTRO_OLD[1] - INTRO_OLD[0]) + (INTRO_NEW[0] - INTRO_OLD[0])   # 1.5s
parts, pos = [x[:S(29.62)], np.zeros((S(gap), ch), np.int16)], 29.62        # the voice is silent from 29.56 to 32.01
for c, r in CUTS:
    parts.append(x[S(pos):S(c)]); pos = c + r
parts.append(x[S(pos):])
y = np.concatenate(parts)[:S(DUR)]
with wave.open(str(P / "assets/voiceover.wav"), "wb") as o:
    o.setnchannels(ch); o.setsampwidth(2); o.setframerate(sr); o.writeframes(y.tobytes())

words = json.loads(git("assets/words.json"))
lst = words["words"] if isinstance(words, dict) else words
for wd in lst:
    wd["start"], wd["end"] = round(M(wd["start"]), 3), round(M(wd["end"]), 3)
(P / "assets/words.json").write_text(json.dumps(words, indent=1))
print("voiceover", round(len(y) / sr, 2), "s; last word ends", lst[-1]["end"])
