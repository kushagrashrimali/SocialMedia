// Every time in the film, in seconds, on the music's grid: 120 BPM, one beat = 0.5 s, one bar = 2 s.
// The 3D scene, the HTML layers and the sound scripts all read this file (keep it plain JSON after the "=").
window.HYPE = {
  "beat": 0.5,
  "dur": 23.0,
  "edge":    [0.0, 2.0],
  "wake":    [2.0, 4.0],  "wakeOn": 2.2, "unlock": 2.85, "hint": 3.35,
  "type1":   [4.0, 6.0],  "words1": [4.0, 4.75, 5.25],
  "stack":   [6.0, 7.5],  "lands": [6.25, 6.625, 6.875, 7.0625, 7.1875], "whip": 7.25,
  "intro":   [7.5, 8.0],
  "reveal":  [8.0, 9.5],  "fan": 8.5, "pop": 9.0, "revealOut": 9.25,
  "pass":    [9.5, 11.5],
  "scan":    [11.5, 12.5], "scanRun": [11.6, 12.1], "scanWord": 11.75,
  "push":    [12.5, 13.5], "notif": 12.6,
  "spin":    [13.5, 16.0], "flashes": [15.0, 15.25, 15.5, 15.625, 15.75, 15.875],
  "type2":   [16.0, 17.0], "words2": [16.0, 16.5],
  "black":   [17.0, 17.5],
  "end":     [17.5, 23.0], "endPop": 18.0, "wordmark": 18.5, "tagline": 19.0, "wallets": 20.0
};
