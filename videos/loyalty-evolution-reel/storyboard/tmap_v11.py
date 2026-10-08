"""Time map: v9 time -> the current cut (the final script, 39.8s).

The film keeps v9's scenes in order and moves them onto the new voice. Anchors are the start of every word the two
scripts share (v9 words 10-65 are words 16-71 now, v9 70-100 are 82-112), plus:
  the hook ("Want to know something about your customers? They never stopped being rewarded.") plays over v9's opening
  montage; v9's phone of unread alerts lands on "They just stopped noticing.";
  v9's old introduction gap collapses; the phone rises on "What if loyalty didn't need another place?";
  the new introduction ("Introducing Why-stack.") is its own scene, written in current time (INTRO); v9 holds still
  under it, and the Wallet opens on "Bringing loyalty to where your customers already are." ("It already has one." is gone).
M(t) maps a v9 time to v11 time.
"""
import json, pathlib

HERE = pathlib.Path(__file__).resolve().parent
DUR = 39.8
V9 = json.loads((HERE.parent / "assets/words-v9.json").read_text())
V11 = json.loads((HERE.parent / "assets/words.json").read_text())

PAIRS = [(i, i + 6) for i in range(10, 66)] + [(i, i + 12) for i in range(70, 101)]
for a, b in PAIRS:
    assert V9[a]["text"].strip(".,?").lower() == V11[b]["text"].strip(".,?").lower(), (V9[a]["text"], V11[b]["text"])
KNOTS = [(0.0, 0.0), (2.72, V11[12]["start"] - 0.05)]                       # the unread phone lands on "They just stopped noticing."
KNOTS += [(V9[a]["start"], V11[b]["start"]) for a, b in PAIRS if a < 59]
KNOTS += [(V9[58]["end"], V11[64]["end"]), (29.62, V11[64]["end"] + 0.03), (31.84, V11[65]["start"] - 0.05)]
KNOTS += [(V9[a]["start"], V11[b]["start"]) for a, b in PAIRS if 59 <= a < 66]
# the introduction (its own scene, v11 time) sits between the question and "Bringing loyalty...": v9's timeline holds
# still under it (the pieces have just been pulled into the phone), then the Wallet opens on "Bringing loyalty"
INTRO = (V11[71]["end"] + 0.15, V11[74]["start"] - 0.45)
KNOTS += [(34.50, V11[71]["end"]), (34.51, INTRO[0] + 0.1), (34.53, INTRO[1] + 0.1),
          (34.60, V11[74]["start"]), (34.87, V11[75]["start"])]
KNOTS += [(V9[a]["start"], V11[b]["start"]) for a, b in PAIRS if a >= 70]
KNOTS += [(V9[100]["end"], V11[112]["end"]), (51.0, DUR)]
KNOTS.sort()
for (a, A), (b, B) in zip(KNOTS, KNOTS[1:]):
    assert b > a and B >= A, ((a, A), (b, B))


def M(t):
    for (a, A), (b, B) in zip(KNOTS, KNOTS[1:]):
        if t <= b:
            return A + (t - a) * (B - A) / (b - a)
    return DUR


def js():
    return json.dumps([[round(a, 4), round(A, 4)] for a, A in KNOTS])


if __name__ == "__main__":
    print("intro", [round(x, 2) for x in INTRO])
    for a, A in KNOTS:
        print(f"{a:7.2f} -> {A:7.2f}")
