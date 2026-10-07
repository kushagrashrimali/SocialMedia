---
workflow: general-video
flow: automation
storyboard: yes
message: "India already went digital on loyalty. Wystak gives it a place to live: the wallet."
destination: instagram-reels
aspect: 1080x1920
language: en
audience: Indian café, restaurant, salon and shop owners (merchants)
length: 44s
---

## Intent

WYSTAK's second reel: a premium editorial film, not a startup ad. It follows the evolution of loyalty in India (payment → recognition → loyalty → data → WhatsApp → too many places → wallet → Wystak) and lands on "The next place for loyalty." The look comes from the reference reel (`Video-47672.mp4`, the CRED "money's glow-up" reel): real footage and archival fragments cut on single words, isolated objects on black, one huge word per section, muted warm grade with grain, black-and-white for crowds and motion. Sound goes from noise to calm: payment chime, pings, chaos, silence, one ding, calm bed, logo.

The full creative brief from the user is in the conversation that made `wystak/scripts/loyalty-evolution-reel.md`; the script there is final and recorded.

## Assets

- assets/voiceover.wav — ElevenLabs take (Kendra), sped up 5% with pitch kept and re-gapped for the brief's silences; 44.02s. It drives all timing.
- assets/words.json — word timings force-aligned (pocketsphinx) to the edited take.
- assets/brand/logo-mark.png, logo-wordmark.png, logo-full.png — crops of the supplied three-card logo (`wystak/brand/`). Never redrawn or recoloured.
- assets/footage/, assets/stills/ — licensed stock and archival media; every file is listed in `assets/MANIFEST.md` with source, URL and licence.

## Customizations

- Isolated words only, no running subtitles (the user's brief): PAY · PHONE · REWARD, VISIT · PURCHASE · PREFERENCE, MESSAGE, EVERYWHERE, APP · LOGIN, WALLET, PAYMENT → REWARD → MESSAGE → WALLET.
- Phone UI is drawn in code: lock screens, chats, SMS, app screens, the Paper Crane Coffee pass and its push.
- End card: the Wystak logo with "THE NEXT PLACE FOR LOYALTY." (the user's line, used in place of the standing tagline).

## Notes

- Brand rules from the repo's CLAUDE.md and the wystak-brand skill: fictional merchant Paper Crane Coffee only; no real company logos (chats are plain bubbles, no WhatsApp branding); Apple Wallet and Google Wallet with equal weight as plain text; the lock-screen push is a real points change, never marketing; no invented statistics.
- Claims allowed: no app, one scan at the counter, points on the lock screen within seconds.
- Hard limit 45s; target 42–44s.
