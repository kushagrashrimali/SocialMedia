// Every time in the film, in seconds, on the music's grid (120 BPM: beat 0.5 s, bar 2 s).
// The 3D stage, the HTML scenes and sound/make_sound.py all read this file (keep it plain JSON after the "=").
// Scenes follow the McDonald's app reel's rhythm: a new beat every 1.5-2.5 s, white UI cards on a bold brand ground,
// big two-size words, product hero shots of the phone in between, the mark on white, the end card on the brand.
window.REEL = {
  "dur": 30.0,
  "s1_open":    [0.0, 2.0],   "wake": 0.35, "notifs": [0.85, 1.1, 1.35],
  "s2_regular": [2.0, 3.75],
  "s3_scan":    [3.75, 5.5],  "scanRun": [4.0, 4.4], "plus": 4.5, "count": [4.55, 5.05],
  "s4_mark":    [5.5, 7.0],   "markHit": 6.0, "press": 6.75,
  "s5_lock":    [7.0, 10.0],  "notif": 8.0,
  "s6_noapp":   [10.0, 12.0], "wallet": 11.0,
  "s7_passes":  [12.0, 14.0], "cycle": [13.0, 13.4, 13.7],
  "s8_ring":    [14.0, 16.0], "ring": [14.25, 15.25], "unlock": 15.3,
  "s9_owner":   [16.0, 18.5], "rows": [16.3, 16.45, 16.6], "send": 17.55,
  "s10_macro":  [18.5, 21.0], "cuts": [18.5, 19.25, 19.75, 20.25, 20.5, 20.75],
  "s11_counts": [21.0, 23.0], "countsWord": 22.0,
  "s12_stack":  [23.0, 26.0], "stackIn": [23.4, 23.8, 24.15, 24.45, 24.7],
  "s13_end":    [26.0, 30.0], "fan": 26.4, "wordmark": 26.8, "tagline": 27.2, "button": 28.0, "wallets": 28.4
};
