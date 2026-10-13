# WYSTAK: Social Media Handbook

Everything another Claude account needs to create Wystak social media posts: what Wystak is, who it is for, brand, voice, hard rules, the step-by-step process for each format, the design lessons learned, and every post made so far (as examples to learn from, never to copy).

Sources: `CLAUDE.md`, `wystak/WYSTAK_Project_Context.md`, `wystak/WYSTAK_Pitch_Deck.pdf`, `SETUP.md`, and the copy files and scripts in `wystak/`. Repo: https://github.com/kushagrashrimali/SocialMedia

---

## 1. What Wystak is

- **Wystak** (pronounced "WHYS-TAK"; write "Whys-tak" in ElevenLabs text; the old spelling "WYSTACK" is dead) issues **Apple Wallet and Google Wallet loyalty passes for Indian merchants**: cafés, bakeries, grocery stores, salons, gyms, restaurants, college fests, clubs.
- **No app to install, no plastic card.** Customers **tap the counter stand (NFC) or scan the QR** to add the pass. Points update on the lock screen **within seconds** of a scan. The owner sees **who keeps coming back and who stopped**.
- **Tagline:** **ALL YOUR PASSES. ONE STACK.** (Uppercase. Secondary motto from the product doc: "All for one. One for all.")
- **Team:** Kushagra, Abhishek, Harsh, Parv (founders). Website placeholder: www.wystak.com.
- **Core insight (pitch deck):** *India digitised the payment, not the relationship.* UPI made the merchant a line in someone else's payment history. A pass puts the shop's own brand back on the lock screen.
- **The moat is the update pipe**, not the pass: balance changes on the lock screen seconds after paying, POS integrations, a scanner that works on a cheap Android phone with patchy wifi (works offline, syncs later), and compliance (DPDP consent in English and Hindi, closed-loop, we never hold customer money).
- **The gap:** big chains already have wallet loyalty through specialist providers. Nobody serves the long tail, a ₹1,500-a-month Indian café. That gap is the business.
- **Hero moment for any product story:** scan at the counter, lock-screen push "+18 points at Bean Theory", pass shows the new number. Real time, no app.

### How it works (the story you can tell)
1. Customer taps the stand or scans the counter QR. The pass is in their wallet in seconds. No app.
2. Staff scan the pass at checkout (free Android scanner app, works offline).
3. Points land on the customer's lock screen seconds later.
4. The owner learns who comes back and who stopped.

### Products (for context; only loyalty is live)
Four "suits" map to the four cards in the logo: Rewards (rose, cafés and restaurants), Tickets (violet, fests and events), Clubs (mint, gyms and societies), Offers (gold, vouchers and win-backs). **Phase 0/1 is Rewards for cafés.** Event passes are listed "live at launch" in the pitch deck, but ticketing is a later phase in the build plan. Do not claim tickets, memberships with expiry, or offers are live unless the team confirms. Vision is fine if framed as vision.

### Market and merchant context
- Beachhead: cafés and bakeries in one Bengaluru neighbourhood, then Mumbai, Delhi NCR, Pune, Hyderabad, Ahmedabad, Jaipur.
- Niche ladder: cafés and bakeries, QSR and casual dining, gyms, salons and wellness, college clubs, nightclubs and events, cinema.
- Posts so far target: cafés (launch), grocery stores, salons. Next candidates: bakeries, restaurants, gyms.
- Why now (pitch deck): Google Wallet came to India (May 2024); Apple Pay is live in India (launched October 2026 with Axis Bank); social feeds are crowded and pay-to-be-seen; DPDP privacy law enforcement begins around May 2027.
- Competitive framing: payment apps make the shop invisible; aggregators keep the relationship and charge 22 to 25% commission; Wystak gives visibility the shop owns, with no ad spend, no commission and no app to download.

### Numbers (use with care)
- **Never invent statistics, prices, customers or traction.** Proof numbers from real pilots: none yet. Use bracketed placeholders (`[N]`, `[PRICE]`) and flag them for a human.
- Pricing (playbook, ex-GST, **confirm before showing**): Starter ₹1,499/month, Growth ₹3,999, Chain ₹12,999, Enterprise ₹60,000+. Scanner app free. Data export free. Treat price as `[PRICE]` in posts unless approved.
- Market sizing (sourced, cite if used): India loyalty market $3.45B (2025) to $7.18B by 2030; 500,000+ restaurants (NRAI); ~95% of Indian phones are Android; Petpooja ~60 lakh bills/day across 100,000+ outlets. Pitch deck cites 76.7% of Indian phone time goes to chat, social and video apps (Bobble AI).
- "Modelled, not measured" (e.g. café ROI ~11x the fee, ARR projections) must be labelled *modelled* or kept off.
- Illustration numbers inside objects ("26 days", "41 days ago", "40 times") are scenarios, not statistics, and each copy file notes this.

---

## 2. Hard rules (never break)

### Claims allowed
No app. Tap or scan at the counter to add the pass. Points on the lock screen within seconds of a scan. The owner sees who comes back and who stopped. Works in Apple Wallet and Google Wallet. No cost per message for lock-screen updates. Scanner works offline.

### Never
1. **Never invent** statistics, prices, customers, traction or testimonials.
2. **Fictional merchants only.** The standing sample café is **Bean Theory**. Others used: Marigold Lane Grocers (grocery), The Saffron Room (salon), Cafe Aroma (loyalty reel). **Never use Paper Crane Coffee again** (older reels only). Sip Grove Juice Bar and Bounce Hair Salon exist as demo passes; confirm they are fictional before use.
3. **No real company logos or names** on mockups (no PhonePe, Paytm, banks, Zomato, Swiggy, Starbucks, etc.). Generic soundbox, generic cards.
4. **Apple Wallet and Google Wallet get equal weight.** Never market Wystak as an Apple product. Do not recolour or modify the official "Add to Apple Wallet" / "Add to Google Wallet" badges.
5. **Apple Pay is live in India.** Never say or imply it is not, and never build a post on "Apple Wallet doesn't work in India". Check any market fact with the user first.
6. **No phone-number collection in posts.** Wystak identifies customers by phone number, so no post may joke about, complain about or imply that shops will not ask for numbers ("nobody wants to give their number" is out). Leave it out of captions, slide copy and alt text. Build on: the pass in the wallet, tap or scan, points on the lock screen, who comes back and who stopped.
7. **India has no loyalty-card or stamp-card culture.** Never build a story on lost loyalty cards or paper stamp cards. Use things every Indian owner has lived: UPI soundbox beeps, "Sir, mobile number?" at big stores, WhatsApp offers lost under good-morning forwards, the kirana wala who knew your name.
8. **Do not show as live:** points expiry, rotating QR codes, velocity limits, geofencing (Phase 1, not built). Do not show money held by Wystak, cash-out, transfer of points, or points earned at one merchant spent at another (closed-loop by design).
9. **No pre-ticked consent boxes** in any enrolment screen shown.
10. **No lock-screen push that is marketing.** Pushes are genuine state changes ("+18 points at Bean Theory"), never "New roll launched!".
11. **Never redraw the logo.** Use the supplied files in `wystak/brand/` (`logo-full-wordmark.webp`, `logo-horizontal-transparent.png`, `logo-mark.jpg`).
12. Say **"pass"** for the wallet object. "Card" means the physical plastic thing Wystak replaces.
13. **English only.** Indian English spelling, prices in ₹.
14. **No gendered pronouns** (he, she, his, her, him) anywhere: copy, captions, alt text, scripts, chat. Use roles ("the client", "the shopper", "the owner") or plural ("customers", "they").
15. **Headlines must be plain, easy sentences** that read on first look. No clipped or twisted grammar ("Not who.").
16. **Different posts open with different stories.** Never start two posts with the same idea (e.g. "a best customer quietly left").
17. **Never repeat a post's design pattern.** New objects, layouts, grounds and type pairings every time.
18. **Carousels: 4 to 5 slides.**
19. The launch post has **no logo badge** on slides; the brand appears in the reveal and end card. Ask before adding one.

---

## 3. Audience and voice

- **Instagram and reels:** merchants (café, restaurant, grocery and shop owners, salon owners), not consumers. Owner-to-owner, warm, concrete, a little wry.
- **LinkedIn:** wider: merchants first, plus investors, POS and payment partners, hires, other founders. Professional and founder-led, still human.
- **Lead with what changes for the merchant**, not technology.
- Few words per slide. Short sentences. The number or concrete detail leads.
- Recurring CTA: **DM us "STACK"** to bring Wystak to your counter / billing counter / front desk.
- Hashtags: Instagram 3 (e.g. `#cafeowners #restaurantbusiness #customerloyalty`); LinkedIn 3 to 5 (`#LoyaltyPrograms #SmallBusiness #DigitalWallet #IndiaStartups #CustomerRetention`).
- Closing line on carousels: "Built for India's cafés, restaurants and shops." (adapt to the niche).

### Notification voice (any on-screen push)
Number leads (`+18`). Title under 40 characters, body under 90. One scan, one push, never a digest. The merchant is the name; Wystak sits second, small. Reference: **"+18 points at Bean Theory"** / "You're at 132 of 150. One more and the next one is on the house."

### Pass-face rules (any pass shown)
One number in the top-right header field. Brand colour fills the pass. Member first name on the pass. Never more than four visible fields. QR first, Code 128 fallback. Strip image 375pt wide, up to 144pt tall. Demo pass: Bean Theory, 132 / 150 points.

---

## 4. Brand system

### The mark
Three solid strokes of a W, the fourth is a **deck of four passes fanning out** of it. Each card is a different merchant. Every corner is cut, never rounded (butt caps, clipped mitre joins, square card corners). Clear space = 0.3x the mark's height on all sides. Small cut (tiny sizes) drops to two cards. One-colour version is a different drawing. The wordmark is outlined paths; never retype it. Never re-weight, re-space or recolour. Scale the whole file.

### Colour
| Card (back to front, order is load-bearing) | Hex |
|---|---|
| 1 Mint | `#00E0A3` |
| 2 Gold | `#FFC300` |
| 3 Rose | `#FF3D71` |
| 4 Violet | `#8B5CF6` |

Inks: Void `#0B0410` (dark ground, brand is dark-first), Aubergine `#1A0B2E` (ink on light), Crease `#4C1D95`, Signal violet `#7C3AED` (UI actions only, one per view), Paper `#F7F5FA`. Muted text `#9C8FB3` on dark, `#6B5D82` on light. Status colours are scanner UI only, never marketing. On light grounds use aubergine, not violet, for text. The four card colours belong to the logo and pass artwork; do not scatter them as UI accents.

### Type
Brand system: Archivo Black (wordmark, hard headlines), Archivo SemiBold (tagline, eyebrows, uppercase, 0.16em tracking), Manrope (body), IBM Plex Mono (numbers). Display type takes negative tracking, eyebrows positive. **Check fonts in every render**; missing fonts silently fall back to Arial.

> **Where the brand system and the posts differ.** The brand file above is the identity. Instagram object-style posts deliberately use varied display pairings per post (see section 8), and reels use Poppins with Wystak violet `#6b2ba6` for key words. When making a new post, follow the post lessons below for typography, and keep the logo, tagline and colour usage from the brand system.

### Fictional-merchant visuals
Real product photography in pass strips, not stock cups. Paper, grain, real shadows, halftone cut-outs, highlighter tape, hand-drawn arrows and circles for object-style posts.

---

## 5. Repo layout (keep it)

```
wystak/
  brand/                  logo files (never redraw)
  instagram/
    carousels/<name>/     build.py, assets/, slides/ (final PNGs), copy.md
    carousels/_common/    shared render helpers (common.py)
    single-posts/<name>/  single-image posts
    reels/finals/         delivered reel MP4s
    reels/scripts/        reel voiceover scripts
  linkedin/<name>/        post.md plus the final image, PDF or MP4
  x/<name>/               X posts (none yet)
videos/<name>/            reel and film projects (HyperFrames)
inbox/<date-topic>/       user's reference videos, audio, screenshots (git-ignored)
```
Folder name = the topic. Finals go in git; drafts and raw media do not. Commit and push without asking, but only what is worth keeping (reusable scripts, templates, lessons, finals).

---

## 6. Process per format

### Instagram carousel or single-image post
1. **Brief and reference.** User sends topic or goal, reference screenshots or PDFs (for mindset, not to copy), and any real assets or facts.
2. **Copy, then stop.** Slide-by-slide copy (headline, line under it, visual idea), the caption, the cover alt text. Score the cover hook with `.claude/skills/ig-reel/hookscore.py` (strong is roughly 75+). User edits or approves.
3. **Draft sheet, then stop.** Render all slides and send one contact sheet of every slide side by side. Revise until approved.
4. **Final after "go".** Export final 1080x1350 PNGs (1080x1080 if square), save `copy.md` (copy, caption, alt text, truth check), commit, send the files.

Build: HTML slides rendered by headless Chromium through `_common/common.py`. For a new carousel copy `carousels/salon/` to `carousels/<name>/`, rename its type and objects (never reuse a design), edit `build.py`. Rebuild with `python3 wystak/instagram/carousels/<name>/build.py` (set `CHROME=/path/to/chrome` if needed).

Every `copy.md` ends with a **Truth check**: which claims are used, which names and numbers are fictional or illustrative.

### LinkedIn (company page)
Formats: text only; text plus one image (1200x1200 or 1080x1350); document carousel (PDF, 1080x1350 pages); native video (reuse a reel). Only the first 2 to 3 lines show before "...see more", so the hook must fit there. 3 to 5 hashtags. **Links go in the first comment, not the post.**
1. **Brief:** goal (launch, insight or opinion, product explainer, milestone, hiring, event), format or "you pick", references, real facts.
2. **Post text, then stop:** 2 or 3 hook options (scored with hookscore.py), full post text, hashtags, first comment; image or slide plan for visual posts.
3. **Visual draft, then stop** (skip for text-only): render in the Wystak look, send a preview.
4. **Final after "go":** export PNG / PDF / MP4. Save `post.md` with post text, hashtags, first comment, alt text and a short **reshare line for each founder** (Kushagra, Abhishek, Harsh, Parv, each in their own voice). Folder `wystak/linkedin/<name>/`.

LinkedIn post shape that worked: one-line hook, one or two sentences of context, "Wystak puts a loyalty pass in the customer's Apple Wallet or Google Wallet:" then four bullets (No app to install / Customers tap or scan at the counter to join / Points update on the lock screen within seconds of every visit / The owner sees who keeps coming back, and who stopped), then an audience line ("If you run one, or build tools for them (POS, billing, payments), we would like to talk. Link in the comments.") and hashtags.

### Instagram Reels (5 steps)
1. **Reference video.** User sends a reference reel (saved as MP4 in `inbox/`). Study story, pacing, design, type, captions and sound (ffmpeg contact sheets, cut timings).
2. **Script.** Voiceover in the reference's storytelling style. Plain script only: no [PAUSE]/[BEAT]/[EMPHASIS] marks unless asked. Commit it to `reels/scripts/`.
3. **Audio.** User records in ElevenLabs and sends the file.
4. **Storyboard, then stop.** Force-align audio to word timings (pocketsphinx if offline; Whisper works locally), deliver a storyboard of every frame with time range, spoken line, and what moves. Revise until approved.
5. **Build only after "go".** Build with HyperFrames, check, render, master audio to about -14 LUFS, verify frames from the delivered MP4, commit.

Also available: `ig-caption`, `ig-story`, `ig-viral`, `ig-repurpose`, `short-form-video`, `caption-animation` skills.

### X (Twitter)
Folder `wystak/x/<name>/` with `post.md`. None made yet. Follow the LinkedIn tone, shorter, no links in the first post if possible.

---

## 7. Reel design and sound lessons

- **Type:** one family (Poppins) over the film, one weight in captions; key word set apart by colour (Wystak violet `#6b2ba6`, lighter tint on dark) and size, never a second font. Phone screens keep iOS-like UI type.
- **Motion:** no hand cursor, no sparkle bursts. Glass, focus pulls, zoom-through seams; scale direction must match across a cut (motion-doctrine skill).
- **Sound:** minimal, Apple-style. Only story moments make a sound (alerts, the pass landing, brand chime, payment, logo). Nothing on cuts, no taps or ticks. Low-pass the SFX bus (~8.5 kHz), effects about -37 LUFS against the voice. Notification sound: soft two-note bubble pop (Mixkit 2357). Real Apple sounds are copyrighted.
- **Music:** clean mid-tempo electronic (100 to 120 BPM), no vocals, steady light pulse, gradual build. Rejected extremes: club kick ("Cat Walk"), cinematic swells ("A New Life"). The loyalty reel uses Mixkit 33 "Motivating Mornings" (120 BPM). Bed levelled to -21 LUFS, played at 0.5, carved under the voice.
- **Layout:** captions low (top ~1420 of 1920), phones and cards moved down to meet them. Over hand-held footage, captions sit just above the phone (~470).
- **Pace:** viewers need time to read. Near-natural speed (~1.05x) with ~0.3s between lines and ~0.8s before the brand reads well at ~50s. Prefer a longer reel over a faster voice.
- **Brand reveal that worked:** no glass card. Every kind of loyalty pass flies in from the edges and fans out, snaps into one stack, shrinks and turns into the passes of the mark; the W rises to catch it with a soft light bloom, the purple and teal passes flick out, the wordmark cascades in on the name with the chime.
- **Logos:** to animate the supplied logo, cut out only the white connected to the border, split into layers by colour. Stacked unmoved, the layers must equal the file.
- **Product shots** sit on a bright lilac set (gradient `#d8ccf8` to `#b9a5ee`, white light pool), never a dark ground. Type cards stay paper `#f3f1f6`. Soft violet drop-shadow. When passes stack, space them apart and square each one before it lands.
- **Hype film (no voiceover):** re-cut one music track on its own grid, every scene change on a downbeat; stop the music before the reveal; the drop lands on the mark.
- **iPhone reel (McDonald's-style):** new beat every 1.5 to 2.5 s; white UI cards on a bold violet ground alternating with paper; two-size Poppins captions; the mark alone mid-film; end card on paper.
- **Engine:** HyperFrames (`/hyperframes` skill). GSAP for timelines and type motion; Three.js for 3D product shots. Vendor GSAP and fonts locally from npm if the network blocks CDNs.

### Reel projects and finals so far
`videos/wystak-launch-reel`, `wystak-launch-intro`, `wystak-hype-reel`, `wystak-iphone-reel`, `loyalty-evolution-reel`. Finals in `wystak/instagram/reels/finals/`: `wystak-launch-reel.mp4`, `loyalty-evolution-reel.mp4`, `launch-intro/`.

---

## 8. Instagram post design direction (object style)

Keep this thinking for every post:
- **One real-world object carries each slide's idea**, drawn in code (a delete dialog, a newspaper, a counter stand, an order pad, an envelope, a fridge list, a price tag, a khata ledger, a desk bell, an appointment card).
- **Huge condensed capitals with one handwritten accent word**, plus a small sans for the line under it.
- **One bold ground per slide**, warm paper in between, with grain, real shadows, halftone cut-outs, highlighter tape and hand-drawn arrows or circles.
- **Very few words per slide.**
- **Structure that works across posts:** (1) provocative object hook on the cover, (2) the insight or problem, (3) tap or scan, no app, (4) "see who came back and who stopped" with one name circled or stamped, (5) CTA object with the Wystak card and "DM us STACK".
- **Pick a new type pairing and ground each time.** Used so far:
  - Launch: Anton + Caveat + Poppins on violet, navy, paper.
  - Grocery: Archivo Black + Permanent Marker + Poppins on navy and cream.
  - Salon: DM Serif Display + Allura + Poppins on teal and blush.
- Cover hook is scored with `hookscore.py`; aim for STRONG.

---

## 9. Everything posted so far (examples; never copy a story)

### Instagram carousels

**Launch, cafés (5 slides, violet/navy/paper)** `carousels/launch/`
1. "Nobody is downloading your café's *app.* Not one regular." Object: "Delete Bean Theory?" dialog with a halftone thumb on Delete.
2. "Cafés move into the wallet" (extra: loyalty, without the app). Object: *The Counter Times* front page with Wystak as the photo.
3. "Tap. Or scan. No *app.*" Object: counter stand with QR and NFC tap zone.
4. "Know who came back. And who *stopped.*" Object: order pad of regulars, one name circled.
5. "Open this. *Your* counter is invited." Object: wax-sealed envelope with the Wystak card. DM us "STACK".

Caption: "Nobody is downloading your café's app. Not one regular. / They don't need to. Wystak puts your loyalty pass in Apple Wallet and Google Wallet. Customers tap the stand or scan the QR at your counter and they're a member, no app. Points land on their lock screen seconds after they pay, and you see who keeps coming back and who quietly stopped. / Built for India's cafés, restaurants and shops. / DM us "STACK" to bring Wystak to your counter. / #cafeowners #restaurantbusiness #customerloyalty"

**Grocery stores (5 slides, navy/cream)** `carousels/grocery/` (fictional Marigold Lane Grocers; cover scored 77.8)
1. "YOUR STORE IS NOT ON THEIR *list.*" Shopping list on a fridge, "Marigold Lane ???" unticked in red.
2. "YOU KNOW WHAT SOLD. WHO BOUGHT IT? *no idea.*" Hanging price tag with blank "Sold to: ???".
3. "TAP AT BILLING. *done.*" Card machine showing "Tap to join".
4. "SEE WHO *stopped* COMING." Khata ledger with a red "GONE QUIET" stamp.
5. "PUT US IN THE *bag.*" Kraft grocery bag with the Wystak card. DM us "STACK".

**Salon (5 slides, teal/blush)** `carousels/salon/` (fictional The Saffron Room; cover scored 77.8)
1. "WHEN DID YOUR CLIENTS LAST *visit?*" Appointment card, "Last visit: ???", scissors.
2. "EVERY CLIENT HAS A *shade.*" Hair-colour swatch fan; the last swatch is the salon's pass.
3. "TAP THE *bell.*" Desk bell with tap waves and QR card.
4. "SEE WHO'S *drifting.*" Mirror with polaroids, one faded "41 days ago" circled.
5. "THE FINISHING *touch.*" Flat lay: Wystak card with hand mirror, comb, scissors. DM us "STACK".

**Launch v1 (older phone-mockup, 8 slides)** `carousels/launch-v1/`. Apple-style: dark navy and light grey slides alternate, one accent word per headline. Opens "Is your café on their *phone?*". Uses Paper Crane Coffee (retired).

### LinkedIn
1. **Introducing Wystak** (single image): "Every phone already has a wallet. Your business is not in it." Image: stack of wallet passes with a teal Bean Theory pass on top, headline "every phone already has a WALLET. is your business in it?"
2. **One pass, both wallets** (single image): "Two phones in one queue. One loyalty pass for both." Image: field of dark passes with one glowing white and teal Wystak pass.
3. **Regulars without an app** (two images): ""You can't track your regulars without an app." That is a myth." Image 1 lavender myth card; image 2 navy collage "a wallet pass shows you who stopped coming."

Each has a `post.md` with first comment ("See how Wystak works or talk to the team: www.wystak.com"), alt text, four founder reshare lines and a truth check.

### Reel scripts (`reels/scripts/`)
- **launch-film-final-vo** (~33s): "Your regular paid you 40 times this year. You still don't know their name." UPI made paying easy, made you a line in their payment history; WhatsApp offers lost under good-morning forwards; then Wystak: one scan, no app, points on lock screen, see who stopped. Close: "Don't be a line in their payment history. Be in their wallet. Wystak. All your passes. One stack."
- **launch-reel-v5-merchant** (30s): "40 soundbox beeps" motif; kirana wala who knew your name; "Sir, mobile number?" (note: the v5 script predates the no-phone-number rule, do not reuse that line in new posts); credit-card points; "India digitised the payment. Not the relationship." Demo with scanner, lock screen "+18 points", Apple and Google Wallet side by side.
- **loyalty-evolution-reel** (~51s): "India didn't stop rewarding customers. Your customers just stopped noticing." Loyalty scattered across SMS, chat, deleted apps; "What if loyalty didn't need another place? It already has one. The wallet on their phone." Close: "Why-stack. All your passes. One stack."
- **loyalty-merchant-advice-reel**: same story told owner-to-owner ("Can I tell you something about your customers?"), ends "Trust me, get Why-stack for your counter."

Reel script format: Hook, Reveal, Demo, Growth, CTA; table of time, voiceover, on-screen; the ElevenLabs paste block; on-screen cards of six words or fewer inside the 1080x1920 safe zone; word-by-word captions burned in; a claims check.

---

## 10. Story angles that are on-brand (new posts must open differently from existing ones)

Used already: delete-the-app, wallet-not-feed, tap or scan, regulars who stopped, shopping list, unknown buyer, last visit, shade swatches, payment-history line, soundbox beeps, SMS/chat/app scatter, myth about tracking, one pass for both phones.

Fresh directions (check each with the user): bakery or restaurant counter; gym (only as vision, no expiry features); the pass lives where boarding passes live; "your shop on the lock screen every day"; the end of the WhatsApp offer lost under forwards; owner sees the quiet week; Hindi-and-English consent ("DPDP built in", no phone-number framing); works offline in a basement; no commission vs aggregators (without naming real brands); festival or Diwali week; the counter stand (NFC) as the hero object; staff scan in two seconds on a cheap Android phone.

---

## 11. Pre-publish checklist

- [ ] Opens with a story no other post used; headline is a plain, easy sentence.
- [ ] 4 to 5 slides (carousel); very few words per slide.
- [ ] New objects, grounds and type pairing; no reused design.
- [ ] Only allowed claims; no invented numbers; illustrations flagged in the truth check.
- [ ] Fictional merchant only (Bean Theory etc.); no real company names or logos; no Paper Crane Coffee.
- [ ] Apple Wallet and Google Wallet shown with equal weight; no "Apple Pay not in India".
- [ ] No phone-number collection mentioned; no loyalty-card or stamp-card story.
- [ ] No gendered pronouns anywhere (copy, caption, alt text).
- [ ] Logo from supplied files, never redrawn; clear space respected.
- [ ] Caption: hook line, 2 to 4 short lines, audience line, CTA ("DM us STACK"), 3 hashtags (Instagram) or 3 to 5 (LinkedIn); LinkedIn link in first comment.
- [ ] Cover alt text written; cover hook scored.
- [ ] Exported at 1080x1350 (or 1080x1080 for square); fonts verified in the render.
- [ ] Copy file saved with truth check; committed and pushed; file paths reported to the user.

---

## 12. Open questions (ask the user, do not guess)

1. Primary tagline for new work: "ALL YOUR PASSES. ONE STACK." (current default) or "All for one. One for all."
2. What is live versus vision at the time of posting (tickets, offers, memberships).
3. Pricing on screen: show playbook tiers or `[PRICE]`?
4. Real proof numbers from pilots (none yet; use `[N]`).
5. Contact email, entity name, launch neighbourhood for end cards; final website link (www.wystak.com is a placeholder).
6. Whether Sip Grove Juice Bar and Bounce Hair Salon are confirmed fictional.
7. Brand-doc inconsistencies (small-cut threshold 32px vs 28px; corner radii) to settle; the `wystak-brand` skill wins.
