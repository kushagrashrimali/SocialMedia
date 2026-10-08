---
workflow: general-video
flow: automation
storyboard: yes
message: "India never stopped rewarding customers; loyalty just got scattered. Wystak puts it in the wallet: one scan, no app, points on the lock screen."
destination: instagram-reels
aspect: 1080x1920
language: en
audience: Indian merchants of every category (cafés, salons, stores, cinemas, clubs, events)
length: 52s
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

## Customizations (v7, current)

- The middle of the film is Indian and upmarket, shown as setups rather than faces (Pexels, warmer red grade to sit with the club/concert opening and ending): "Every counter" is a saree showroom counter, a gold jewellery counter, then the café; "Businesses learned to remember" is a pink modern salon; "Every visit" is a mall atrium; "Every purchase" is a saree being chosen; "Cafés remembered birthdays" is a family celebrating at a table. The opening and the ending are unchanged.

## Customizations (v6)

- "Businesses learned to remember" is now a wide salon setup (round mirror, stylist blow-drying, shelves) in the rounded window, instead of a face close-up.
- Notifications use a quick three-note ascending chime (Mixkit "Alert quick chime"); Apple's own iOS sounds are Apple's copyrighted assets and are not licensed for use in ads, so they are not used.
- The Wystak introduction has its own synthesised futuristic chime: an airy shimmer rising into a glassy, detuned FM bell chord with a soft pitch settle and a ping-pong echo (`wystak_chime()` in `sound/make_sound.py`).
- The ending ("Now they notice") shows no notifications: every category's pass deals into one floating Wallet stack with Apple Wallet and Google Wallet beneath it.

## Customizations (v5)

- Every category, in real footage: a club, a barber's blow-dry and a café in the opening montage; "Every counter" crosses a boutique, a bar and a café; a barber for "Businesses learned to remember" (v6: a wide salon); a cinema audience with popcorn ("Every visit"), a boutique rail ("Every purchase") and a café pour ("Every preference"); "Now they notice" runs concert, club, café, and the Wallet notifications pile into one stack across them (Live Pass, Club Night, Cafe Aroma).
- The Wallet stack holds every category (Movie Club, Salon Club, Style Rewards, Live Pass) under the Cafe Aroma pass, on both Apple Wallet and Google Wallet.
- Transitions: every footage cut is a zoom-through dissolve (clips overlap 0.4s; scale and focus hand over); brand-ground scenes focus-pull in and dissolve out over the footage; warm light leaks on the three topic changes; the last shot blows out to white into the logo. Slow bokeh drifts behind every phone.
- The Wystak introduction holds 1.0s longer (voice re-gapped at 30.40s, everything after it +1.0s): a light sweep runs across the mark and the wordmark, and the promise "All your passes. One stack." settles underneath before the lockup flies into the phone.
- Sound: real recorded effects (Mixkit) in place of the synthesised pops: one two-tone phone alert for every notification, a confirmation ding for paid and reward, a switch click for the lock, soft air whooshes for the cuts, one bell for Wystak. The effects sit about 6 dB lower than v4.
- Build: `python3 -I storyboard/prep_v5.py SRC_DIR`, `python3 -I sound/make_music.py assets/music-src/mixkit-371-cat-walk.mp3`, `python3 -I sound/make_sound.py`, `python3 storyboard/build_v5.py`, then the carve, then render.

## Customizations (v4)

- People are real action at the counter, on video: a cup handed across, a barista at the machine, coffee carried to a customer, a lid snapped on a takeaway cup, a phone at the counter (Mixkit 4K, framed on the action rather than faces).
- Kinetic captions, one family (Inter Tight), exact words in short groups: each word punches in on its spoken time (oversize, tipped back, out of focus, then snaps into place); the accent word gets its own big line, lands with a squash-and-stretch spring and floods into brand colour (violet #6b2ba6 on light, mint #00e0a3 on footage/violet); phrases lift away on time.
- 3D phones with edge thickness, glass reflection, glow and contact shadow. Notifications are Apple Liquid Glass (frosted backdrop blur, bright catching edge, inner highlights, a light sweep); on the lock screen they grow out of the Dynamic Island and spring open; floating cards materialise (blur and scale resolve together). The "everywhere" stack bursts into space around the phone.
- Brand grounds behind every showcased phone: light lilac for the problem, Wystak violet for the answer.
- The turn (29.7–34s): silence on a clean frame, then the ding introduces Wystak ("Introducing", the mark, the wordmark); the lockup flies down into the phone as it rises, and the scattered places loyalty lived float round it on the question, then get pulled into the phone as the Wallet and the Cafe Aroma pass land and the frame floods violet on the music drop ("It already has one").
- Apple Wallet and Google Wallet: an iPhone and an Android phone side by side, each with its own icon and name beneath it, equal size; the Add-to-Wallet badges sit inside the scanned page on the hand-held phone, so they move with it.
- Hand-held composites re-cut from the part of the source where the whole phone is in frame.
- Music: Mixkit "Cat Walk" edited to the voice (`sound/make_music.py`); SFX tuned to its E minor (`sound/make_sound.py`).
- End card: the Wystak logo and tagline only.
- Build: `python3 storyboard/build_v4.py`, then the carve, then render.

## Notes

- Brand rules from the repo's CLAUDE.md and the wystak-brand skill: fictional merchant Cafe Aroma (the user's choice for this reel); app logos only where the user asked for them; Apple Wallet and Google Wallet with equal weight as plain text; the lock-screen push is a real points change, never marketing; no invented statistics.
- Claims allowed: no app, one scan at the counter, points on the lock screen within seconds.
- Length follows the recorded voice: 52.39s (v5 added 1.0s of hold to the introduction).
