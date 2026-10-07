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

## Customizations (v4, current)

- People are young urban Indians (Unsplash photography by mostly India-based photographers), animated with slow camera moves; the strongest footage (French press, latte pour, the hand-held scan and pay) stays.
- One caption family: Inter Tight. Exact words of the voice in short groups, each word popping on its spoken time (the launch reel's language: scale, lift and a slight tilt, back-out ease). One accent word per group: violet (#6b2ba6) on light grounds, mint (#00e0a3) on footage and violet grounds.
- 3D phones with edge thickness, glass reflection, glow and contact shadow; notifications live in front of the glass and pop toward camera; the "everywhere" stack bursts into space around the phone.
- Brand grounds behind every showcased phone: light lilac for the problem, Wystak violet for the answer.
- The turn (29.7–34s): silence, the ding wakes the phone, the scattered places loyalty lived float round it on the question, then get pulled into the phone as the Wallet and the Cafe Aroma pass land and the frame floods violet on the music drop ("It already has one").
- Apple Wallet and Google Wallet: an iPhone and an Android phone side by side, each with its own icon and name beneath it, equal size; the Add-to-Wallet badges sit inside the scanned page on the hand-held phone, so they move with it.
- Hand-held composites re-cut from the part of the source where the whole phone is in frame.
- Music: Mixkit "Cat Walk" edited to the voice (`sound/make_music.py`); SFX tuned to its E minor (`sound/make_sound.py`).
- End card: the Wystak logo and tagline only.
- Build: `python3 storyboard/build_v4.py`, then the carve, then render.

## Notes

- Brand rules from the repo's CLAUDE.md and the wystak-brand skill: fictional merchant Cafe Aroma (the user's choice for this reel); app logos only where the user asked for them; Apple Wallet and Google Wallet with equal weight as plain text; the lock-screen push is a real points change, never marketing; no invented statistics.
- Claims allowed: no app, one scan at the counter, points on the lock screen within seconds.
- Length follows the recorded voice: 51.39s.
