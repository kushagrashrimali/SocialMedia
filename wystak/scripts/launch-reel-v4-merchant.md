# WYSTAK launch reel v4: merchant script in the style of the reference reel

## What the reference does (`Video-47672.mp4`, 45s, 4:3)

Read from contact sheets at one frame per second. The audio couldn't be transcribed in this environment, so the narration below is pieced together from the on-screen captions.

- **Story:** "Money has had the craziest journey in Indian history." Coins (actual metal) → notes → cards → everything bought on a card → a coin, a note, a card, then a **QR** → the turn on black: **"it was TRUST."** → "Somehow every hand now trusts a tiny screen with its entire financial life" → the brand's app on a phone.
- **Voice:** first person and conversational ("I recently saw a billboard…"), like a creator talking to camera, not an ad announcer.
- **Look:** a pale **sage paper ground**. One cut-out object at a time, centred (a coin, a note, a card, a QR), with a lot of empty space. Collage stretches of archival photos and object cut-outs; black-and-white crowd footage for the "everyone" beat; one real product shot (a phone paying at a terminal).
- **Type:** word-by-word captions in the lower third that mix a **grotesk sans with an italic serif** ("money has had the *craziest*"). A few words are promoted to huge display type: **"Ridiculous"** in yellow, **"TRUST"** in dark red on black.
- **Rhythm:** a new picture roughly every second, and the caption advances word by word. The single black frame with one red word is the turn of the film.
- **Ending:** the product appears only in the last few seconds, after the idea has landed.

## The Wystak story in the same shape

**Loyalty has had a wild ride in India.** It began with the shopkeeper who knew your name and kept your *khata*. Then came stamp cards, plastic and apps nobody kept. Credit cards learned to reward every swipe. Then UPI turned every shop into a QR code, and the relationship disappeared: the café became one line in someone else's app.

**The turn:** *India digitised the payment, not the* **RELATIONSHIP.** (From the pitch deck, slide 2.)
**The answer:** Wystak gives the shop back what the shopkeeper had: its regulars remember it, and it shows up on their lock screen after every visit.

## Script (Hook → Reveal → Demo → Growth → CTA)

| Section | Time | Voiceover | Picture (sage paper ground, one centred cut-out per beat) |
|---|---|---|---|
| **Hook** | 0:00–0:03 | Loyalty has had a *wild* ride in India. | A brass shop bell, then the caption builds word by word with "wild" in italic serif |
| | 0:03–0:06 | It began with a shopkeeper who knew your name. | A handwritten *khata* ledger page: "Sharma ji – 2 chai ✓" |
| | 0:06–0:09 | Then stamp cards. Plastic. Apps nobody kept. | Three cut-outs, one per second: paper stamp card → generic plastic card → app icon struck with ✕ |
| | 0:09–0:12 | Credit cards learned to reward every swipe. | Generic credit cards fan out and shed reward points (no real bank or brand) |
| | 0:12–0:13 | Then… UPI. | A single QR code cut-out, centred, as in the reference |
| **Reveal** | 0:13–0:16 | We digitised the payment… not the **relationship**. | Hard cut to black. **RELATIONSHIP** in huge purple display type, the reference's "TRUST" frame |
| | 0:16–0:19 | Your regulars? Just a line in someone else's app. | Black-and-white crowd paying by phone; a payment list where "Paper Crane Coffee ₹180" is one grey line among many |
| | 0:19–0:21 | So we built Why-stack. | Back on sage. The three logo cards fan out of the W |
| **Demo** | 0:21–0:26 | They pay. You scan their pass. Seconds later… points on their lock screen. | Real-looking product shot: phone at the counter → scanner on an Android phone → lock screen "+18 points at Paper Crane Coffee" |
| **Growth** | 0:26–0:27 | *(no voiceover, music only)* | Fast run: 132 → 150 → `FREE COFFEE READY`. Apple Wallet and Google Wallet side by side |
| **CTA** | 0:27–0:30 | Why-stack. All your passes. One stack. | End card on sage: logo plus tagline |

### Text to paste into ElevenLabs (about 70 words)

```
Loyalty has had a wild ride in India.
It began with a shopkeeper who knew your name.
Then stamp cards. Plastic. Apps nobody kept.
Credit cards learned to reward every swipe.
Then... UPI.
We digitised the payment... not the relationship.
Your regulars? Just a line in someone else's app.
So we built Why-stack.
They pay. You scan their pass. Seconds later... points on their lock screen.
Why-stack. All your passes. One stack.
```

If the take runs over 30s, cut "Credit cards learned to reward every swipe." first; the visual can carry it alone. Then cut "Then... UPI." (the QR picture says it).

### Voice for this version

The reference is a person talking, not a keynote announcer, so the delivery changes from the earlier scripts:
- Pick a **conversational, warm, slightly storytelling** voice (Voice Library: *conversational*, *storyteller*, *podcast*). An Indian-English accent fits this story well.
- Multilingual v2: Stability 45–55 (a little looser than before, for natural rhythm) · Similarity 75 · Style 10–20 · Speaker boost on · Speed 1.0.
- Let "relationship" land: a short pause before it and a slight drop in pitch.
- Voice only, no music. Export WAV, or MP3 at 192 kbps or higher.

## Design spec for the build

- **Ground:** sage paper `#E6EBDA` with a light paper grain, the reference's signature. Black (`#0B0B0F`) for the turn and the crowd beat.
- **Ink:** logo navy for captions; **purple** (from the logo) for the one promoted word, "RELATIONSHIP", in the reference's "TRUST" role; **teal** for point counts.
- **Type:** captions in a grotesk sans (Archivo / Inter Tight) with italic-serif emphasis words (Instrument Serif or Playfair Italic), as in the reference's "*craziest*" and "*History*". Display word in Archivo Black.
- **Objects:** one centred cut-out per beat with soft contact shadows and a slight drift in, never still. All are generic or drawn by us: ledger, stamp card, plastic card, app icon, credit card, QR code.
- **Footage:** one black-and-white crowd shot (free stock, e.g. Unsplash), and the phone and scanner product shots built in code.
- **Format:** **9:16, 1080×1920** for the reel. The reference is 4:3, so its centred-object layout carries over with more vertical space for the captions.
- **Sound:** soft piano or pulse bed like the reference, a small tick per word-advance on key beats, a paper stamp thud, a card snap, silence on the black "RELATIONSHIP" frame, then the music lifts into the reveal.

## Claims check

- Every product claim comes from the pitch deck: no app, points update seconds after a scan, Apple and Google Wallet.
- Rewards are the shop's own points on its own pass. Wystak never pays out rewards on UPI itself (closed loop).
- No real company names or logos on screen; the credit cards and payment list are generic. The merchant is the fictional Paper Crane Coffee.
- No statistics or prices.
