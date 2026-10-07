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
| footage/v4-open.mp4 | 0–2.72s | Mixkit 222 "Waiter pouring a cup of coffee (cup handed across the counter)", https://assets.mixkit.co/videos/222/222-2160.mp4 | Mixkit Free | 4K, cropped 9:16 + shared warm grade (`storyboard/prep_v3.py`); source 0.4s +2.75s |
| footage/v4-counter.mp4 | 5.32–9.12s | Mixkit 3574 "Serving coffee in a cup at a coffee shop (barista at the machine)", https://assets.mixkit.co/videos/3574/3574-2160.mp4 | Mixkit Free | 4K, cropped 9:16 + shared warm grade (`storyboard/prep_v3.py`); source 1.0s +3.85s |
| footage/v3-barista.mp4 | 9.12–11.28s | Mixkit 205 "A waiter serves coffee to a customer (French press)", https://assets.mixkit.co/videos/205/205-2160.mp4 | Mixkit Free | 4K, cropped 9:16 + shared warm grade (`storyboard/prep_v3.py`); source 1.0s +2.2s |
| footage/v4-visit.mp4 | 11.28–12.38s | Mixkit 219 "Waiter carries a cup of coffee to customer", https://assets.mixkit.co/videos/219/219-2160.mp4 | Mixkit Free | 4K, cropped 9:16 + shared warm grade (`storyboard/prep_v3.py`); source 1.7s +1.15s |
| footage/v4-purchase.mp4 | 12.38–13.48s | Mixkit 3582 "Barista putting the lid on an espresso", https://assets.mixkit.co/videos/3582/3582-2160.mp4 | Mixkit Free | 4K, cropped 9:16 + shared warm grade (`storyboard/prep_v3.py`); source 4.4s +1.15s |
| footage/v3-pour.mp4 | 13.48–14.88s | Mixkit 41859 "Serving a sparkling cappuccino in a cup", https://assets.mixkit.co/videos/41859/41859-2160.mp4 | Mixkit Free | 4K, cropped 9:16 + shared warm grade (`storyboard/prep_v3.py`); source 2.6s +1.45s |
| footage/v4-birthday.mp4 | 18.18–21.42s | Mixkit 41860 "Employee serving a cup of coffee from a machine", https://assets.mixkit.co/videos/41860/41860-2160.mp4 | Mixkit Free | 4K, cropped 9:16 + shared warm grade (`storyboard/prep_v3.py`); source 1.0s +3.3s |
| footage/v4-notice.mp4 | 43.42–45.62s | Mixkit 4919 "Person on social media while serving coffee (phone at the counter)", https://assets.mixkit.co/videos/4919/4919-2160.mp4 | Mixkit Free | 4K, cropped 9:16 + shared warm grade (`storyboard/prep_v3.py`); source 1.8s +2.25s |
| footage/scan-at-counter.mp4 | 37.12–39.62s | Composite: Mixkit 42636 "Chroma on a smartphone with a green screen background" (source 1.2–3.7s, whole phone in frame) over `stills/counter-long.jpg` | Mixkit Free + Unsplash | Screen `ui/screen-scan.png`: the Add-to-Wallet page with both badges |
| footage/pay-at-counter.mp4 | 39.62–41.24s | Composite: Mixkit 42636 (source 2.25–3.87s) over `stills/cafe-india.jpg` | Mixkit Free + Unsplash | Screen `ui/screen-pay.png` |

### Photography (Unsplash License)
| File | Scene | Page | Direct file | Photographer | Licence |
|---|---|---|---|---|---|
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
