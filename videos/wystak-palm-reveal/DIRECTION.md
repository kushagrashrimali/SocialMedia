# Wystak palm reveal: animation direction

One continuous, locked-off shot of the seaside garden. Four real palms, two crossing pairs that already read as a W, bend, uncross, turn navy from the roots up and settle into the Wystak W. Then the three passes fan out and the shot rests on the exact logo.

- **Storyboard:** `storyboard/frames/wystak-palm-reveal-storyboard.png` (3 × 2, 3156 × 2112).
- **Frames:** `storyboard/frames/frame-01 … frame-06*.png` (1020 × 1020 each).
- **Build:** `python3 storyboard/build_storyboard.py` (about 1 minute; `--plate <photo>` swaps in a sharper copy of the seaside photo).

## The idea in one line

The trees were always a W; nature just finishes the thought.

## Camera

- **Locked off.** Same position, lens and horizon for the whole piece. Use the plate's eye-level, slightly wide lens (about 28–35 mm full-frame equivalent).
- **Optional push-in.** A very slow digital push-in of 2–3 % across the whole shot is allowed for tension. It changes nothing in perspective. No cuts, no whip pans, no shake.
- **Light.** Hard Indian coastal daylight, high sun from the upper left, as in the photo. Nothing changes colour temperature.
- **Grade.** Natural and restrained. No glow, no particles, no light rays.

## Timing (about 10 seconds; 24 or 30 fps)

| Time | Frame | What happens | Motion notes |
|---|---|---|---|
| 0.0–1.6 s | 1 | **The familiar scene.** An ordinary afternoon: fountains run, the sea is calm, the visitors photograph the famous crossing palms. | Only natural motion: fountain water, frond flutter, a slight sway in the visitors. Hold long enough to register "real photo". |
| 1.6–3.2 s | 2 | **Something feels different.** A gust moves through the crowns. The outer trunks lean out a few degrees, the inner pair dips toward each other, and the curves deepen. | Physically believable flex: a slow ease-in-out, the tops lead and the roots stay rooted. Fronds react a beat late, like a real gust. |
| 3.2–5.4 s | 3 | **Nature begins forming the mark.** The crossing trunks slide along each other until the X climbs to the top and becomes the W's middle peak. The trunks straighten onto the W's four strokes and thicken. The bark rings tighten and smooth, and a deep navy finish climbs from the roots, ring by ring. The fronds start folding upward, like umbrellas closing. | The material change travels upward (it has a direction, so it reads as growth, not a dissolve). The palm rings stay visible in the navy for a moment before it smooths out. |
| 5.4–6.6 s | 4 | **The W takes shape.** The folded fronds retract into the stroke tips, which round off into the W's soft terminals. The trunks swell to full stroke width, and the fourth trunk flattens into a tall rounded slab: the W's last stroke. | Settle with a short, damped overshoot (one small give, no cartoon bounce). The W stands in the hedge: the hedge tops and the people stay in front of it. |
| 6.6–7.8 s | 5 | **The passes emerge.** The fourth stroke reveals itself as the first pass: its ticket presses up from the surface. The purple pass, then the teal pass, swing out from behind it around a pivot at the W's foot. | Purple starts 0.12 s before teal. Each pass decelerates into place (ease-out, about 0.6 s). A light rotational motion blur; each pass casts a soft shadow on the one behind it. |
| 7.8–10.0 s | 6 | **The Wystak logo.** The exact supplied logo, held still and clean, in the garden. The visitors keep filming. | No motion on the logo. Ambient motion only (water, fronds gone, people). Hold at least 2 s. |

## How to hand frames to a video model

- **Use the frames as keyframes.** Use the six frames as keyframes for image-to-video in first-and-last-frame mode, one segment per row of the table: 1→2, 2→3, 3→4, 4→5, 5→6. The prompt for each segment is in `VIDEO_PROMPT.md`.
- **Composite the logo in post.** Lay the supplied logo over the last 2.5 s in compositing (After Effects, Nuke or Resolve), using the frame-6 placement. Video models redraw logos. The W, the cards, their angles and icons must come from the file.
- **Motion from the file too.** Frames 5 and 6 can be animated entirely in post from the layered logo: the navy layer, then purple and teal rotating about the pivot at the W's foot. `build_storyboard.py` already splits these layers.

## Sound design (minimal, as in the Wystak films)

Only story moments make a sound. Low-pass the effects bus at about 8.5 kHz, keep effects around −37 LUFS, and master the mix to about −14 LUFS.

| Stage | Sound |
|---|---|
| 1 | Seaside ambience: gentle waves, the fountain, a light breeze, distant voices. No music yet, or the bed enters very low. |
| 2 | One soft gust through the fronds and a single low, woody creak as the trunks flex. |
| 3 | A slow stretching creak that turns into a smooth, rising tone as the navy climbs: wood becoming lacquer. Keep it subtle. |
| 4 | A soft, low settle (felt more than heard) as the W lands. |
| 5 | Three clean card-slide flicks, one per pass (tuned, short, no whoosh). |
| 6 | The Wystak brand chime on the hold. Ambience returns. |

**Music (optional).** Clean, mid-tempo electronic (100–120 BPM), no vocals, building under stages 2–4 with a low-pass opening up. The full entry lands on a downbeat with frame 6.

## Notes

- **The plate.** The supplied seaside photograph was not in the session. The plate is frame 1 of the reference sheet (about 510 px, shown at 2× = 1020 px). For a final film, drop the original photo in and rebuild (`--plate`). Tree and hedge positions are kept as fractions of the frame, so the same composition at a higher resolution works.
- **The logo.** Frames 4–6 use `logo-mark.png` from the brand assets. The teal pass carries the wallet icon, as in the file (the reference sheet showed a gift icon there).
- **No added text.** There is no tagline or other copy in any frame.
