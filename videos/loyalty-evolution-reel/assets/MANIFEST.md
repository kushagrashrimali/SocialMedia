# Asset manifest: loyalty evolution reel

Every third-party file in this reel (v4), with its source and licence. All allow commercial use: Mixkit Stock Video / Music Free License, Unsplash License or CC0.

Licences:
- Mixkit Stock Video Free License: https://mixkit.co/license/#videoFree (commercial use, no attribution required)
- Unsplash License: https://unsplash.com/license (commercial use, no attribution required)
- CC0 1.0: https://creativecommons.org/publicdomain/zero/1.0/

## v4 media

### Music
| File | Source | Licence | Notes |
|---|---|---|---|
| music-src/mixkit-371-cat-walk.mp3 | Mixkit "Cat Walk" (track 371), https://mixkit.co/free-stock-music/ , file https://assets.mixkit.co/music/371/371.mp3 | Mixkit Stock Music Free License (https://mixkit.co/license/#musicFree) | Edited to the voice by `sound/make_music.py` into `music-bed.wav` (build, silence, filtered pre-drop, drop on "It already has one", ending under the logo) |

### Video
| File | Time | Source | Licence | Notes |
|---|---|---|---|---|
| footage/v3-barista.mp4 | 9.12–11.28s | Mixkit 205 "A waiter serves coffee to a customer" (hands only), https://assets.mixkit.co/videos/205/205-2160.mp4 | Mixkit Free | `storyboard/prep_v3.py` |
| footage/v3-pour.mp4 | 13.48–14.88s | Mixkit 41859 "Serving a sparkling cappuccino in a cup", https://assets.mixkit.co/videos/41859/41859-2160.mp4 | Mixkit Free | `storyboard/prep_v3.py` |
| footage/scan-at-counter.mp4 | 37.12–39.62s | Composite: Mixkit 42636 "Chroma on a smartphone with a green screen background" (source 1.2–3.7s, the window where the whole phone is in frame) over `stills/counter-long.jpg` | Mixkit Free + Unsplash | Screen `ui/screen-scan.png`: the Add-to-Wallet page with both badges |
| footage/pay-at-counter.mp4 | 39.62–41.24s | Composite: Mixkit 42636 (source 2.25–3.87s) over `stills/cafe-india.jpg` | Mixkit Free + Unsplash | Screen `ui/screen-pay.png` |

### Photography (Unsplash License; cropped 9:16 with the shared warm grade)
| File | Scene | Page | Direct file | Photographer | Licence |
|---|---|---|---|---|---|
| stills/in-open.jpg | A · 0–2.72s | https://unsplash.com/photos/QvVFwx6LBbo | https://images.unsplash.com/photo-1634749724102-f89da39ec545 | Dollar Gill (Sydney, Australia) | Unsplash |
| stills/in-counter.jpg | C · 5.32–9.12s | https://unsplash.com/photos/CrhjMkeHU5k | https://images.unsplash.com/photo-1628633964338-3a362d5fbab0 | Dollar Gill (Sydney, Australia) | Unsplash |
| stills/in-visit.jpg | E1 · 11.28–12.38s (shop sign softened) | https://unsplash.com/photos/bClDppHtoJ4 | https://images.unsplash.com/photo-1570471946274-eecd5ae2c41e | ASHWATH PC (Bangalore, India) | Unsplash |
| stills/in-purchase.jpg | E2 · 12.38–13.48s (cup logo softened) | https://unsplash.com/photos/KZLjiZT5ZdA | https://images.unsplash.com/photo-1665808771375-b58b83548757 | Bipin Kumar Pal (India) | Unsplash |
| stills/in-friends.jpg | G · 18.18–21.42s | https://unsplash.com/photos/Y4zNMW3pQAs | https://images.unsplash.com/photo-1625463006115-09f08489f591 | Karthik Balakrishnan (Bangalore, India) | Unsplash |
| stills/in-notice.jpg | O · 43.42–45.62s | https://unsplash.com/photos/nrcrU20C9Fo | https://images.unsplash.com/photo-1671823469756-1e64ab077acb | Rupinder Singh (India) | Unsplash |
| stills/counter-long.jpg | scan composite ground | https://unsplash.com/photos/djqAK4rP-G8 | https://images.unsplash.com/photo-1780404197319-14f7b0d63697 | Haberdoedas | Unsplash |
| stills/cafe-india.jpg | pay composite ground | https://unsplash.com/photos/81LMj3heZEs | https://images.unsplash.com/photo-1753541042293-5cbd98583db0 | Ashwin N | Unsplash |
| ui/aroma-strip.jpg, ui/aroma-hero.jpg | Cafe Aroma pass strip | https://unsplash.com/photos/LI8inyHnm_A | https://images.unsplash.com/photo-1611564494260-6f21b80af7ea | Robbie Down | Unsplash |

## Drawn for this reel

- `ui/pass-apple.png`, `ui/pass-google.png`: the Cafe Aroma Wallet passes (`storyboard/card/cards.html`, `render.sh`).
- `ui/wallpaper-brand.jpg`: phone wallpaper in Wystak's navy, plum and teal (generated).
- App glyphs from simple-icons (CC0, `storyboard/icons.json`): WhatsApp, Instagram, Messages, Facebook, Telegram, Gmail, YouTube, Snapchat, X, as the user asked; the wallet badges are drawn at equal size.

## Made for this reel (no third-party rights)

- `ui/wallpaper.jpg`, `ui/screen-scan.png`, `ui/screen-pay.png`: drawn in code (`storyboard/screens/`).
- Every phone screen, chat, notification, the Cafe Aroma pass, captions and type card: HTML/CSS generated into `index.html` by `storyboard/build_index.py`.
- `brand/logo-mark.png`, `brand/logo-wordmark.png`: crops of WYSTAK's own logo files (`wystak/brand/`).
- Fonts: Archivo, Archivo Black, Manrope, IBM Plex Mono (SIL Open Font License, via @fontsource on npm). GSAP from npm.
- `voiceover.wav`: WYSTAK's ElevenLabs recording (Kendra), edited.
- `music-bed.wav`, `sfx.wav`: synthesised for this reel by `sound/make_sound.py` (tanpura drone, pads, kalimba, pulse, chimes, pings, ding). No samples.
