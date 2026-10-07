# frame.md — WYSTAK loyalty reel

Concept: an editorial film made of fragments. Real footage and archival scraps cut on single words; isolated objects and clean phones on black; one huge word per section; noise that thins out into calm when the wallet appears.

## Canvas

- 1080×1920, 30fps, 44.02s (the edited voiceover drives everything).
- Safe zone for anything that must be read: x 90–850, y 230–1440. Nothing important in the right 230px (Instagram's action rail) or below y 1440 (caption and audio strip).

## Colour

| Token | Hex | Use |
|---|---|---|
| Void | `#0B0410` | Black frames, phone stages. Reads as black, tinted to the brand. |
| Paper | `#F7F5FA` | Type on dark; the off-white frames and the end card ground. |
| Aubergine | `#1A0B2E` | Type on Paper. |
| Muted on dark | `#9C8FB3` | Secondary UI text on dark. |
| Muted on light | `#6B5D82` | Secondary UI text on light. |
| Crane teal | `#06737C` | Paper Crane Coffee's pass colour (same as the launch reel). Pass artwork only. |
| Signal violet | `#7C3AED` | At most one UI action per view (the "Add to wallet" button). Never decoration. |

Footage grade: muted and slightly warm, controlled contrast, lifted blacks, fine grain (canonical `data-color-grading`, Film Memory as the seed). Crowds, trains and archival frames go black-and-white. No saturated colour anywhere except the pass artwork and the logo.

## Type (brand faces only, vendored in `assets/vendor/fonts/`)

| Role | Face | Spec |
|---|---|---|
| Isolated label words (PAY, VISIT, LOGIN…) | Archivo SemiBold | Uppercase, 0.16em tracking, 46px, Paper on dark / Aubergine on light |
| Hero word, one per section (EVERYWHERE, WALLET) | Archivo Black | Uppercase, −0.035em tracking, 190–240px |
| Spoken quote ("Sir, mobile number?") | Archivo Medium Italic | 64px, sentence case |
| Phone UI | Manrope | 500–800, never below 15px at phone scale |
| Point counts, SMS sender IDs | IBM Plex Mono | Tabular |
| End line | Archivo SemiBold | "THE NEXT PLACE FOR LOYALTY." uppercase, 0.16em tracking, Aubergine on Paper |

The reference reel mixes a grotesk with an italic serif; the brand has no serif, so emphasis comes from Archivo italic and scale instead.

## Layout rules

- One focal object per frame, centred or anchored to the lower third, with a lot of empty space (the reference's isolation).
- Phones are clean device renders on Void: generic iPhone-style and Android-style bodies, no logos, no real app UI.
- Label words sit at y≈1180–1260, centred; hero words sit across the optical centre.
- The logo is only ever the supplied PNG crops on Paper, with 0.3× mark-height clear space.

## Brand guards

- Fictional merchant: Paper Crane Coffee. Other businesses stay unnamed ("The Salon").
- Chats are plain bubbles with no WhatsApp green or logo. Apple Wallet and Google Wallet appear only as equal plain-text chips.
- The lock-screen push is a points change: "+18 points at Paper Crane Coffee" / "You're at 132 of 150. One more and the next one is on the house."
