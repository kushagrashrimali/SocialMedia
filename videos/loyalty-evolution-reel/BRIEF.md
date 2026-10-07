---
workflow: general-video
flow: automation
storyboard: yes
message: "India never stopped rewarding customers; loyalty just got scattered. Wystak puts it in the wallet: one scan, no app, points on the lock screen."
destination: instagram-reels
aspect: 1080x1920
language: en
audience: Indian café, restaurant, salon and shop owners (merchants)
length: 51s
---

## Intent

WYSTAK's second reel: a premium editorial film, not a startup ad. It follows the evolution of loyalty in India (payment → recognition → loyalty → data → WhatsApp → too many places → wallet → Wystak) and lands on "The next place for loyalty." The look comes from the reference reel (`Video-47672.mp4`, the CRED "money's glow-up" reel): real footage and archival fragments cut on single words, isolated objects on black, one huge word per section, muted warm grade with grain, black-and-white for crowds and motion. Sound goes from noise to calm: payment chime, pings, chaos, silence, one ding, calm bed, logo.

The full creative brief from the user is in the conversation that made `wystak/scripts/loyalty-evolution-reel.md`; the script there is final and recorded.

## Assets

- assets/voiceover.wav — ElevenLabs take (Kendra), sped up 5% with pitch kept and re-gapped for the brief's silences; 44.02s. It drives all timing.
- assets/words.json — word timings force-aligned (pocketsphinx) to the edited take.
- assets/brand/logo-mark.png, logo-wordmark.png — crops of the supplied three-card logo (`wystak/brand/`). Never redrawn or recoloured.
- assets/footage/, assets/stills/ — licensed stock and archival media; every file is listed in `assets/MANIFEST.md` with source, URL and licence.
- assets/music-bed.wav, assets/sfx.wav — synthesised locally (`sound/make_sound.py`); the bed is carved under the voice (hyperframes-audio carve, strength 0.6).

## Customizations (v2, user feedback on the first cut)

- New script and new ElevenLabs take (51.39s after regapping); timings in `assets/words.json`.
- Running captions, a phrase at a time, each word lighting gold as it is spoken (generated from the word timings).
- Slower opening: two held shots over the first five seconds, fading up from black.
- "Sir, mobile number?" is gone; "Every counter started collecting data" shows a drawn customer card over a POS counter.
- Premium, bright café photography (Unsplash) in place of the archival and chai stills; every phone sits on a bright ground.
- The fictional café is now **Cafe Aroma**, with a premium espresso-and-gold wallet pass.
- The social-media line shows WhatsApp, Instagram, Messages and other apps popping in as app icons with unread badges (requested by the user).
- "Add to Apple Wallet" and "Add to Google Wallet" badges, equal size, from "No app." (38.9s) through the payment, again on "Now they notice", and on the end card.
- A held end card (45.6–51.4s): logo mark, wordmark, then ALL YOUR PASSES. / ONE STACK. on their words.
- Build: `python3 storyboard/build_index.py`, then the carve (`carve.mjs --bed bed --voice vo --strength 0.6`), then render.

## Notes

- Brand rules from the repo's CLAUDE.md and the wystak-brand skill: fictional merchant Cafe Aroma (the user's choice for this reel); app logos only where the user asked for them; Apple Wallet and Google Wallet with equal weight as plain text; the lock-screen push is a real points change, never marketing; no invented statistics.
- Claims allowed: no app, one scan at the counter, points on the lock screen within seconds.
- Length follows the recorded voice: 51.39s.
