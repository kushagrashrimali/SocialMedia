# Asset manifest: loyalty evolution reel

Every third-party file in this reel (v2, the Cafe Aroma cut), with its source and licence. All of them allow commercial use: Mixkit Stock Video Free License, Unsplash License or CC0. Stills are cropped to 9:16 by `storyboard/prep_media.py` (`storyboard/media.json`) and shown ungraded, bright and clean.

Licences:
- Mixkit Stock Video Free License: https://mixkit.co/license/#videoFree (commercial use, no attribution required)
- Unsplash License: https://unsplash.com/license (commercial use, no attribution required)
- CC0 1.0: https://creativecommons.org/publicdomain/zero/1.0/

## Video (v3)

| File | Time | Source | Licence | Notes |
|---|---|---|---|---|
| footage/v3-open.mp4 | 0–2.72s | https://mixkit.co/free-stock-video/ (Mixkit 41220, "Young woman drinking a cup of coffee in a cafe"), file https://assets.mixkit.co/videos/41220/41220-2160.mp4 | Mixkit Free | 4K source, cropped 9:16, warm grade baked (`storyboard/prep_v3.py`); source 9.0s +2.75s |
| footage/v3-pay.mp4 | 5.32–9.12s | https://mixkit.co/free-stock-video/ (Mixkit 41222, "Two girls chatting at the counter of a coffee shop"), file https://assets.mixkit.co/videos/41222/41222-2160.mp4 | Mixkit Free | 4K source, cropped 9:16, warm grade baked (`storyboard/prep_v3.py`); source 1.0s +3.85s |
| footage/v3-barista.mp4 | 9.12–11.28s | https://mixkit.co/free-stock-video/ (Mixkit 205, "A waiter serves coffee to a customer"), file https://assets.mixkit.co/videos/205/205-2160.mp4 | Mixkit Free | 4K source, cropped 9:16, warm grade baked (`storyboard/prep_v3.py`); source 1.0s +2.2s |
| footage/v3-walkin.mp4 | 11.28–12.38s | https://mixkit.co/free-stock-video/ (Mixkit 39948, "Couple walking into a romantic cafe on a date"), file https://assets.mixkit.co/videos/39948/39948-2160.mp4 | Mixkit Free | 4K source, cropped 9:16, warm grade baked (`storyboard/prep_v3.py`); source 2.6s +1.15s |
| footage/v3-purchase.mp4 | 12.38–13.48s | https://mixkit.co/free-stock-video/ (Mixkit 41229, "Two girls choosing at the counter in a coffee shop"), file https://assets.mixkit.co/videos/41229/41229-2160.mp4 | Mixkit Free | 4K source, cropped 9:16, warm grade baked (`storyboard/prep_v3.py`); source 1.6s +1.15s |
| footage/v3-pour.mp4 | 13.48–14.88s | https://mixkit.co/free-stock-video/ (Mixkit 41859, "Serving a sparkling cappuccino in a cup"), file https://assets.mixkit.co/videos/41859/41859-2160.mp4 | Mixkit Free | 4K source, cropped 9:16, warm grade baked (`storyboard/prep_v3.py`); source 2.6s +1.45s |
| footage/v3-notice.mp4 | 43.42–45.62s | https://mixkit.co/free-stock-video/ (Mixkit 43257, "Friends looking at social networks in the cafe"), file https://assets.mixkit.co/videos/43257/43257-2160.mp4 | Mixkit Free | 4K source, cropped 9:16, warm grade baked (`storyboard/prep_v3.py`); source 4.6s +2.25s |
| footage/scan-at-counter.mp4 | 37.12–39.62s | Composite: Mixkit 42636 "Chroma on a smartphone with a green screen background" over `stills/counter-long.jpg` | Mixkit Free + Unsplash | Screen replaced with `ui/screen-scan.png` (`storyboard/composite_phone.py`, --blur 6 --dim 1.0); source 0.3–2.8s |
| footage/pay-at-counter.mp4 | 39.62–41.24s | Composite: Mixkit 42636 over `stills/cafe-india.jpg` | Mixkit Free + Unsplash | Screen `ui/screen-pay.png`; source 2.2–3.82s |

## Stills (Unsplash License; bg-* are cropped 9:16 and lightly blurred as depth of field behind the phones)

| File | Scene | Page | Direct file | Author | Licence |
|---|---|---|---|---|---|
| bg-table | B, I | https://unsplash.com/photos/pezwxLK99zA | https://images.unsplash.com/photo-1636875485729-02ec3ec9091c | Valeriia Svitlini | Unsplash |
| bg-counter | F, N | https://unsplash.com/photos/tvdN_53_iK8 | https://images.unsplash.com/photo-1635847420403-d03e037078a0 | Marie G. | Unsplash |
| bg-window | H, K | https://unsplash.com/photos/2BI6mino4eY | https://images.unsplash.com/photo-1762304817469-1d6c808324ee | Bill Ringer | Unsplash |
| counter-long | scan composite ground | https://unsplash.com/photos/djqAK4rP-G8 | https://images.unsplash.com/photo-1780404197319-14f7b0d63697 | Haberdoedas | Unsplash |
| cafe-india | pay composite ground | https://unsplash.com/photos/81LMj3heZEs | https://images.unsplash.com/photo-1753541042293-5cbd98583db0 | Ashwin N | Unsplash |
| birthday | G | https://unsplash.com/photos/B8bzPWEHUDQ | https://images.unsplash.com/photo-1784638865161-f2b825d815db | see page | Unsplash |
| ui/aroma-strip, ui/aroma-hero | Cafe Aroma pass strip | https://unsplash.com/photos/LI8inyHnm_A | https://images.unsplash.com/photo-1611564494260-6f21b80af7ea | Robbie Down | Unsplash |

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
