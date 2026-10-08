"""v10 time map: v9 time -> v10 time, total length kept at 51.0s.

v10 gives the Wystak introduction room to breathe:
  * a pause: after the lock click the screen stays black and silent for ~0.5s (v9 29.62-29.66 -> v10 29.62-30.17)
  * the introduction itself plays ~1.45x slower (v9 29.66-31.84 -> v10 30.17-33.34)
The 1.5s this adds is taken back from the voice's own silences after the introduction (CUTS: start, length in v9 time,
each cut sits inside a pause between words) and from the end hold (1.01s -> 0.60s), so the reel still ends at 51.0s.

M(t) maps any v9 time to v10 time. A time inside a cut lands on the cut point.
"""
import json

DUR = 51.0
INTRO_OLD = (29.66, 31.84)
INTRO_NEW = (30.17, 33.34)
K_INTRO = (INTRO_NEW[1] - INTRO_NEW[0]) / (INTRO_OLD[1] - INTRO_OLD[0])
CUTS = [(34.68, 0.08), (36.09, 0.09), (37.87, 0.16), (40.65, 0.11), (44.28, 0.12), (46.0, 0.45), (47.61, 0.08)]

KNOTS = [(0.0, 0.0), (29.62, 29.62), (INTRO_OLD[0], INTRO_NEW[0]), (INTRO_OLD[1], INTRO_NEW[1])]
_s = INTRO_NEW[1] - INTRO_OLD[1]
for c, r in CUTS:
    KNOTS += [(c, c + _s), (c + r, c + _s)]
    _s -= r
KNOTS.append((60.0, 60.0 + _s))
END_SHIFT = _s           # +0.41: v9 "stack." (49.99) lands at 50.40, held 0.60s to 51.0


def M(t):
    for (a, A), (b, B) in zip(KNOTS, KNOTS[1:]):
        if t <= b:
            return A if b == a else A + (t - a) * (B - A) / (b - a)
    return t + END_SHIFT


def js():
    return json.dumps([[round(a, 4), round(A, 4)] for a, A in KNOTS])


if __name__ == "__main__":
    print("K_INTRO", round(K_INTRO, 4), "end shift", round(END_SHIFT, 3))
    for a, A in KNOTS:
        print(f"{a:7.2f} -> {A:7.2f}")
