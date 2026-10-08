"""v11 time map: v9 time -> v11 time (the final script, 40.0s).

The v11 film keeps v9's scenes in order and moves them to the new voice. Anchors are the start of every word the two
scripts share (v9 words 10-58 are v11 words 16-64, v9 59-74 are v11 77-92, v9 75-100 are v11 95-120), plus:
  the new hook ("Want to know something about your customers? They never stopped being rewarded.") plays over v9's
  opening montage, and v9's phone of unread notifications lands on "They just stopped noticing.";
  v9's introduction gap (29.62-31.84) collapses; the phone rising out of it is slowed across the new first question
  ("What if you met them where they already look, every single day?");
  after "The wallet on their phone." the Wallet scene holds under the new introduction (its own scene, written in
  v11 time) and the scan footage starts as the introduction leaves.
M(t) maps a v9 time to v11 time.
"""
import json, pathlib

HERE = pathlib.Path(__file__).resolve().parent
DUR = 40.0
V9 = json.loads((HERE.parent / "assets/words-v9.json").read_text())
V11 = json.loads((HERE.parent / "assets/words.json").read_text())

PAIRS = [(i, i + 6) for i in range(10, 59)] + [(i, i + 18) for i in range(59, 75)] + [(i, i + 20) for i in range(75, 101)]
for a, b in PAIRS:
    assert V9[a]["text"].strip(".,?").lower() == V11[b]["text"].strip(".,?").lower(), (V9[a]["text"], V11[b]["text"])
KNOTS = [(0.0, 0.0), (2.72, V11[12]["start"] - 0.05)]                       # the unread phone lands on "They just stopped noticing."
KNOTS += [(V9[a]["start"], V11[b]["start"]) for a, b in PAIRS if a < 59]
KNOTS += [(V9[58]["end"], V11[64]["end"]), (29.62, V11[64]["end"] + 0.03), (31.84, V11[65]["start"])]
KNOTS += [(V9[a]["start"], V11[b]["start"]) for a, b in PAIRS if 59 <= a < 75]
INTRO = (V11[92]["end"] + 0.05, V11[95]["start"] - 0.28)                    # the introduction overlay, v11 time
KNOTS += [(V9[74]["end"], V11[92]["end"]), (37.80, INTRO[0]), (38.03, INTRO[1])]
KNOTS += [(V9[a]["start"], V11[b]["start"]) for a, b in PAIRS if a >= 75]
KNOTS += [(V9[100]["end"], V11[120]["end"]), (51.0, DUR)]
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
