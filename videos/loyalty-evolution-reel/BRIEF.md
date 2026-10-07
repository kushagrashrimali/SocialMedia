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

## Customizations (v3, art-directed cut)

- Type is art direction, not subtitles: Inter Tight (statements), Instrument Serif italic (the accent word), JetBrains Mono (data labels), cream/mint on footage and navy/plum/teal on bright grounds, lines rising out of masks. Short phrases, not the voiceover word for word. No boxes.
- Real 4K café footage (Mixkit) cropped 9:16 with one shared warm grade; bright, softly blurred café photographs behind every phone.
- Phone choreography after the first cut: notifications stacking iOS-style, a 13-ping cascade on "everywhere", one phone moving through SMS, chat, a deleted app, an App Store page and an OTP login, a clean lock screen in the silence, the Wallet push with the camera leaning in.
- Cafe Aroma passes redesigned as real Apple Wallet store card and Google Wallet loyalty card (`storyboard/card/`); they land in an iPhone and an Android phone side by side (equal weight).
- Add to Apple Wallet / Google Wallet badges on "No app." through the payment (38.9–41.2s).
- End card: the Wystak logo and tagline only.
- Sound at the first cut's density: tanpura, pads, kalimba and pulse; pings, shutters, card slides, the cascade and impact, riser, lock click, silence, one ding, the Wallet chime, logo bells.
- Build: `python3 storyboard/build_v3.py`, then the carve (`carve.mjs --bed bed --voice vo --strength 0.6`), then render.

## Notes

- Brand rules from the repo's CLAUDE.md and the wystak-brand skill: fictional merchant Cafe Aroma (the user's choice for this reel); app logos only where the user asked for them; Apple Wallet and Google Wallet with equal weight as plain text; the lock-screen push is a real points change, never marketing; no invented statistics.
- Claims allowed: no app, one scan at the counter, points on the lock screen within seconds.
- Length follows the recorded voice: 51.39s.
