# WYSTAK launch reel: voiceover scripts v2 (30s, 9:16)

Structure: **Hook → Reveal → Demo → Growth → CTA**, the same for both versions.
Message, from the pitch deck: *UPI made paying invisible. WYSTAK makes the shop visible again.* India digitised the payment, not the relationship. WYSTAK puts the shop's own brand on the customer's lock screen.

Decisions so far:
- Logo: the navy / purple / teal three-card mark (`wystak/brand/`).
- Tagline: ALL YOUR PASSES. ONE STACK.
- English only. Delivery: Apple keynote film narrator (calm, understated, real pauses).
- End card: logo plus tagline.

Pick ONE script. Section timings get re-cut to the reference video's beats.

---

## A. Merchant version (for shop and café owners)

| Section | Time | Voiceover | On screen |
|---|---|---|---|
| **Hook** | 0:00–0:05 | UPI made paying invisible. It made your shop invisible too. | A UPI history list. The café's name is one grey line among many and fades out |
| **Reveal** | 0:05–0:09 | Introducing Why-stack. Your brand, on every customer's phone. | Logo; the three cards fan out of the W into a phone's wallet |
| **Demo** | 0:09–0:19 | One scan adds your pass to their wallet. No app. Seconds after every visit, the points update. Right on their lock screen. | Counter QR → pass added (iPhone and Android) → lock screen shows "+18 points at Paper Crane Coffee" → pass reads 132 / 150 |
| **Growth** | 0:19–0:26 | No ad spend. No commission. Just a direct line to your own customers. | Three crossed-out chips ("Ads", "Commission", "Cost per message"), then the owner dashboard: who came back, and when |
| **CTA** | 0:26–0:30 | Why-stack. All your passes. One stack. | End card: logo plus tagline |

Text to paste into ElevenLabs (about 55 words):

```
UPI made paying invisible. It made your shop invisible too.
Introducing Why-stack. Your brand, on every customer's phone.
One scan adds your pass to their wallet. No app.
Seconds after every visit, the points update. Right on their lock screen.
No ad spend. No commission. Just a direct line to your own customers.
Why-stack. All your passes. One stack.
```

---

## B. Customer version (for the people carrying the pass)

| Section | Time | Voiceover | On screen |
|---|---|---|---|
| **Hook** | 0:00–0:05 | Your favourite café. Every week. And all you get back… is a UPI receipt. | A payment-success tick, then the receipt shrinks into a list of identical lines |
| **Reveal** | 0:05–0:09 | Meet Why-stack. Your favourite places, in your phone's wallet. | Logo; the cards fan out of the W into the wallet stack |
| **Demo** | 0:09–0:19 | Scan once. No app. The pass is in your wallet. Pay… and your points arrive before your coffee does. | QR scan → pass lands → "+18 points at Paper Crane Coffee" on the lock screen while the cup is still being made |
| **Growth** | 0:19–0:26 | Cafés. Salons. Fest tickets. iPhone or Android. | The stack grows: café pass, salon pass, fest ticket; Apple Wallet and Google Wallet side by side |
| **CTA** | 0:26–0:30 | Why-stack. All your passes. One stack. | End card: logo plus tagline |

Text to paste into ElevenLabs (about 50 words):

```
Your favourite café. Every week. And all you get back... is a UPI receipt.
Meet Why-stack. Your favourite places, in your phone's wallet.
Scan once. No app. The pass is in your wallet.
Pay... and your points arrive before your coffee does.
Cafés. Salons. Fest tickets. iPhone or Android.
Why-stack. All your passes. One stack.
```

---

## ElevenLabs settings

- **Pronunciation:** the script spells the name **"Why-stack"** so it is said "why-stak". On screen it is always WYSTAK.
- **Voice:** in the Voice Library, search *narration*, *calm*, *premium*, *documentary*. Pick a warm mid-to-low voice with a neutral accent and no "radio ad" energy. Audition "Why-stack. All your passes. One stack." first.
- **Model:** Eleven v3 (or Multilingual v2 if v3 sounds too acted).
- **Settings (Multilingual v2):** Stability 55–65 · Similarity 75 · Style 0–10 · Speaker boost on · Speed 0.92–0.95.
- **Voice only:** no music or effects. I add music and sound design to match the reference video.
- **Export:** WAV if your plan allows, otherwise MP3 at 44.1 kHz, 192 kbps or higher. Send 2–3 takes if you like.
- **Pauses:** "..." gives a short pause. Don't speed the voice up to fit 30s; I can adjust the silences on the timeline.

## Claims check

- Every claim comes from the pitch deck: no app, updates in seconds, lock-screen updates with no cost per message, no ad spend, no commission, Apple and Google Wallet, loyalty and event passes live at launch.
- No statistics or prices on screen.
- "Pass" means the wallet object; the only "card" left in either script is the logo's cards.
- Merchant shown: the fictional Paper Crane Coffee. Real apps (PhonePe, Google Pay) are never named or shown; the UPI list uses fictional names.
