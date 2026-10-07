# Asset manifest: loyalty evolution reel

Every third-party file in this reel (v2, the Cafe Aroma cut), with its source and licence. All of them allow commercial use: Mixkit Stock Video Free License, Unsplash License or CC0. Stills are cropped to 9:16 by `storyboard/prep_media.py` (`storyboard/media.json`) and shown ungraded, bright and clean.

Licences:
- Mixkit Stock Video Free License: https://mixkit.co/license/#videoFree (commercial use, no attribution required)
- Unsplash License: https://unsplash.com/license (commercial use, no attribution required)
- CC0 1.0: https://creativecommons.org/publicdomain/zero/1.0/

## Video

| File | Time | Source | Licence | Notes |
|---|---|---|---|---|
| footage/scan-at-counter.mp4 | 37.05–39.55s | Composite: Mixkit 42636 "Chroma on a smartphone with a green screen background" (https://mixkit.co/free-stock-video/chroma-on-a-smartphone-with-a-green-screen-background-42636/) over `stills/cafe-interior.jpg`, lightly blurred | Mixkit Free + Unsplash | Screen replaced with `ui/screen-scan.png` (`storyboard/composite_phone.py`, --blur 5 --dim 1.0); source 0.3–2.8s |
| footage/pay-at-counter.mp4 | 39.55–41.15s | Composite: Mixkit 42636 over `stills/counter-kiosk.jpg` | Mixkit Free + Unsplash | Screen replaced with `ui/screen-pay.png`; source 2.2–3.8s |

## Stills (Unsplash License)

| File | Use | Page | Direct file | Licence |
|---|---|---|---|---|
| stills/cafe-interior.jpg | 0–2.7s; also the blurred ground of the scan composite | https://unsplash.com/photos/B2pVVV9Ee-o | https://images.unsplash.com/photo-1590741861173-85035e8af62c | Unsplash |
| stills/cappuccino-hand.jpg | 2.7–5.25s | https://unsplash.com/photos/TMkrYpWW7kc | https://images.unsplash.com/photo-1550731358-491ded4af838 | Unsplash |
| stills/pos-counter.jpg | 5.25–9.05s, behind the drawn customer card | https://unsplash.com/photos/aCkaR5G4Zd4 | https://images.unsplash.com/photo-1602665742701-389671bc40c0 | Unsplash |
| stills/boutique-desk.jpg | 9.05–11.2s (Ishan Sharma, Ajmer) | https://unsplash.com/photos/6gZMN5UZJXU | https://images.unsplash.com/photo-1788953324777-3d98984c0fa0 | Unsplash |
| stills/woman-counter.jpg | 11.2–12.4s | https://unsplash.com/photos/GMUbpaCjYSc | https://images.unsplash.com/photo-1790156591288-13a255334cd8 | Unsplash |
| stills/latte-pour.jpg | 12.4–13.55s; strip image on the Cafe Aroma pass | https://unsplash.com/photos/OFdqt1ECako | https://images.unsplash.com/photo-1670404161009-29548c027d06 | Unsplash |
| stills/flatwhite-pour.jpg | 13.55–14.8s | https://unsplash.com/photos/UBoH66BA48c | https://images.unsplash.com/photo-1670819916940-2db70584e3fc | Unsplash |
| stills/birthday-cake.jpg | 18.1–21.35s | https://unsplash.com/photos/B8bzPWEHUDQ | https://images.unsplash.com/photo-1784638865161-f2b825d815db | Unsplash |
| stills/counter-kiosk.jpg | blurred ground of the pay composite | https://unsplash.com/photos/5-39xoKn6ws | https://images.unsplash.com/photo-1790156591139-e460a7658661 | Unsplash |
| stills/barista-modern.jpg | spare, not on screen | https://unsplash.com/photos/TezASx9giqU | https://images.unsplash.com/photo-1745347455714-fdfc711ec593 | Unsplash |

## App and wallet marks

The user asked for WhatsApp, Instagram, Messages and other apps to appear as app icons, and for "Add to Apple Wallet" and "Add to Google Wallet" badges. The glyphs come from simple-icons (CC0, `storyboard/icons.json`); the badges and wallet glyphs are drawn in code at equal size.

## Made for this reel (no third-party rights)

- `ui/wallpaper.jpg`, `ui/screen-scan.png`, `ui/screen-pay.png`: drawn in code (`storyboard/screens/`).
- Every phone screen, chat, notification, the Cafe Aroma pass, captions and type card: HTML/CSS generated into `index.html` by `storyboard/build_index.py`.
- `brand/logo-mark.png`, `brand/logo-wordmark.png`: crops of WYSTAK's own logo files (`wystak/brand/`).
- Fonts: Archivo, Archivo Black, Manrope, IBM Plex Mono (SIL Open Font License, via @fontsource on npm). GSAP from npm.
- `voiceover.wav`: WYSTAK's ElevenLabs recording (Kendra), edited.
- `music-bed.wav`, `sfx.wav`: synthesised for this reel by `sound/make_sound.py` (tanpura drone, pads, kalimba, pulse, chimes, pings, ding). No samples.
