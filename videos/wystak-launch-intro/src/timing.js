/* WYSTAK launch intro: every timing value in one place (seconds).
   The composition (index.html) and the sound script (sound/make_sound.py) both read this file,
   so picture and sound move together when a number changes here. Keep it plain JSON after the "=". */
window.WYSTAK_TIMING = {
  "duration": 10.0,

  "cover": { "frost": 9, "comment": "t=0 is the Story cover: the lockup softly behind a frosted glass pass" },

  "pane": { "lift": 0.15, "liftDur": 2.6, "frostOut": 2.3, "fadeAt": 1.7, "fadeDur": 0.9 },
  "sweep1": { "at": 0.45, "dur": 1.6 },
  "logo": { "settleAt": 0.0, "settleDur": 2.8, "sharpAt": 2.2 },

  "sheets": { "at": 2.0, "dur": 1.6, "drift": 8.0 },

  "stack": {
    "inAt": 4.0, "gap": 0.32, "inDur": 1.25,
    "organiseAt": 5.75, "organiseDur": 0.95,
    "accessAt": 6.55, "accessDur": 1.1
  },

  "tagline": { "at": 7.3, "wordGap": 0.085, "wordDur": 0.9 },

  "camera": { "from": 1.0, "to": 1.035, "end": 9.0 },
  "hold": 9.0
};
