---
workflow: motion-graphics
destination: instagram-reels, instagram-stories
aspect: 1080x1920 layout, rendered at 2160x3840
length: 10s
---

# WYSTAK launch intro

WYSTAK's first brand-introduction post: a quiet, premium 10-second logo film on off-white, built around the official
lockup and a stacking-passes metaphor. An introduction, not an explainer ("What is WYSTAK?").

## The film

| Time | What happens |
|---|---|
| 0.0 | **Story cover.** The official lockup sits in place behind a frosted glass pass, readable but soft. |
| 0.15-2.75 | The pass tips back and rises out of frame while its frost clears; one light sweep crosses it. The lockup settles ~1% into focus. A single glass tone lands at 2.2s. |
| 2.0-3.6 | Two thin glass sheets drift in behind with slow parallax; they only catch light at their edges. |
| 4.0-5.25 | **Stack.** Four glass passes (faint teal, plum and navy tints from the logo's own passes, then clear) deal in from depth and fan behind the mark, each with a muted set-down sound. |
| 5.75-6.7 | **Organise.** The fan closes into one stack, the back passes peeking above the front; a soft low settle. |
| 6.55-7.65 | **Access.** One light runs down the deck. |
| 7.3-8.6 | The tagline resolves word by word: ALL YOUR PASSES. ONE STACK. A quiet chord opens under it. |
| 9.0-10.0 | Hold. The camera has come fully to rest, so the last second matches the final still exactly. |

## Structure (every value easy to change)

- `src/timing.js`: every timing value, in one JSON object. The composition **and** `sound/make_sound.py` read it.
- `src/styles.css`: the look (ground, glass, deck, lockup, tagline). Layout at 1080x1920.
- Components, one per layer, each adds itself to the single timeline:
  `src/background.js` (ground, key light, parallax), `src/logo.js` (lockup settle), `src/glass.js` (cover pass,
  light sweep, thin sheets), `src/stack.js` (deal, fan, organise, access; positions in `WYSTAK.FAN` / `WYSTAK.STACK`),
  `src/tagline.js`, `src/camera.js` (push-in that stops at 9.0s).
- `index.html` assembles them. `sound/make_sound.py` synthesises the SFX from the same timing.

## Build

```
python3 -I sound/make_sound.py
npx --yes hyperframes@0.8.139 render --resolution portrait-4k -q delivery -o renders/wystak-launch-intro-4k.mp4
bash sound/master.sh renders/wystak-launch-intro-4k.mp4 ../../wystak/launch-intro
ffmpeg -i renders/wystak-launch-intro-4k.mp4 -frames:v 1 ../../wystak/launch-intro/wystak-launch-intro-cover.png
ffmpeg -sseof -0.05 -i renders/wystak-launch-intro-4k.mp4 -frames:v 1 ../../wystak/launch-intro/wystak-launch-intro-final-frame.png
```
(`tools/stills.mjs` exports the same stills straight from the page; it is very slow on the software renderer.)

## Notes

- Logo: the supplied files only (`wystak/brand/`, transparent crops in `assets/brand/`), scaled as a whole, never
  altered; displayed at ~1:1 with the source pixels at 2160x3840. The supplied logo is a raster; no vector master
  exists in the repo. The `wystak-brand` design-system skill describes a different, flat four-pass mark; the repo's
  supplied files were used, as the brief and the repo rules require.
- Type: Archivo SemiBold, 0.16em tracking (the brand's tagline face). Ink: Aubergine `#1A0B2E`, accent Crease `#4C1D95`.
- Sound: synthesised, no music; mastered to -14 LUFS (true peak -1.5 dBTP).
- Story-safe: lockup and tagline sit between y 520 and 1340 of 1920.
