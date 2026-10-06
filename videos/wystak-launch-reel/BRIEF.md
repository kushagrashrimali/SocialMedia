---
workflow: general-video
flow: automation
storyboard: no
message: "Don't be a line in their payment history. Be in their wallet."
destination: instagram-reels
aspect: 1080x1920
language: en
audience: Indian café, restaurant and shop owners (merchants)
length: 33.6s
---

## Intent

The WYSTAK launch reel, built to win merchant clients. It follows the final merchant script (`wystak/scripts/launch-film-final-vo.md`) and takes its look from the reference reel (`Video-47672.mp4`): a sage paper ground, one centred cut-out object per beat, word-by-word captions mixing a grotesk sans with italic serif emphasis, and one black frame carrying a single huge word.

## Assets

- assets/voiceover.mp3: ElevenLabs voiceover (Kendra), 32.9s; it drives all timing.
- assets/words.json: word timestamps, force-aligned offline (pocketsphinx) to the known script.
- assets/logo-*.png: crops of the supplied three-card logo (`wystak/brand/logo-full-wordmark.webp`).
- assets/music-bed.mp3, assets/sfx.mp3: synthesised locally (ambient pad and pulse; soundbox beeps, swishes, chime, impacts).

## Customizations

- Burned-in word-by-word captions, with one emphasis word per line in purple italic serif.
- Black "WALLET." beat in place of the reference's "TRUST" frame.

## Notes

- Fictional merchant: Paper Crane Coffee. No real brand logos; "Apple Wallet" and "Google Wallet" appear as equal plain-text chips.
- The network blocks stock-photo hosts, so every object is drawn in code.
