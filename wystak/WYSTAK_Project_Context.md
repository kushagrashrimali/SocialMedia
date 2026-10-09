# WYSTAK — Project Context for the Marketing Video Phase

**Compiled:** 6 October 2026 · **For:** Claude Code, starting the marketing-video work
**Owner:** Kushagra (kushagra3161@gmail.com)

> **Where this came from.** Claude's chat memory is switched off for this account, so past chat
> transcripts could not be read directly. This file is compiled from everything those
> conversations produced and saved into the "startup" Project: `Brand_Identity_WYSTAK.md`,
> `Four_Suits_Product_Architecture.md`, `Team_WYSTAK_Guide.md`, `Playbook_Size_Corrections.md`,
> `CLAUDE.md`, `PHASE0_PLAN.md`, `Wallet_Native_India_Tech_Master_Plan.md`, the Legal &
> Compliance Handbook, `Wallet_Native_India_Full_Playbook.pdf`, and the installed `wystak-design`
> plugin (the `wystak-brand` skill). Anything said in chat but never written into those files is
> not here.

---

## 0. Read this first — the rules a video must not break

1. **Load the `wystak-brand` skill** before designing any frame. It wins on every colour, typeface
   and logo decision.
2. **Never redraw the logo by eye.** Use the supplied SVG / Figma vectors and scale the whole file.
3. **Never invent a statistic.** Any number not in section 6 goes on screen as a visible bracketed
   placeholder — `[N]`, `[PRICE]`, `[CITY]` — and gets flagged for a human to fill.
4. **Never put a real company's name or logo on a mockup.** The standing fictional sample
   merchant is **Bean Theory**.
5. **Never market WYSTAK as an Apple product.** About 19 in 20 Indian phones are Android. Show
   Google Wallet at least as prominently as Apple Wallet.
6. **Never recolour or modify the "Add to Apple Wallet" / "Add to Google Wallet" badges.** They
   are licensed artwork, used exactly as provided.
7. **Never show a lock-screen push that is marketing.** Pushes are genuine state changes only
   (`+18 points at Bean Theory`), never "New paneer tikka roll launched!".
8. **Never show or promise points expiry, rotating QR codes, velocity limits or geofencing as live
   features.** They are Phase 1, not built yet. Showing them is a false claim (and expiry copy is a
   consumer-protection dark-pattern risk).
9. **Never show money held by WYSTAK, cash-out, peer transfer of points, or points earned at one
   merchant spent at another.** WYSTAK is closed-loop by design (RBI). Each merchant's programme
   is separate.
10. **Never show pre-ticked consent boxes** in any enrolment screen.
11. Say **"pass"** for the wallet object. "Card" means the physical plastic thing WYSTAK replaces.
12. **Indian English spelling, prices in ₹.**

---

## 1. What WYSTAK is

WYSTAK issues **Apple Wallet and Google Wallet passes for Indian merchants** — cafés, bakeries,
salons, gyms, restaurants, college fests, clubs — and **updates the points on them within seconds
of a scan at the counter.** No app to install, no plastic to print.

- **Customer side:** scan a QR at the counter → phone number + first name → the pass is in their
  native wallet in under ten seconds. Double-tap the side button and it's there.
- **Merchant side:** a dashboard, a free Android scanner app (unlimited devices, works offline),
  and later POS integrations so points update without staff doing anything.
- **Internal/working name of the venture:** "Wallet-Native India" (appears on the playbook and
  engineering docs). The brand is **WYSTAK** — no C. The spelling "WYSTACK" is dead.

### The positioning (from the playbook)

- **Market it as "your card, in their phone"** — never as an Apple product.
- **The moat is not the pass, it is the update pipe.** Generating a pass is a weekend project; a
  dozen tools sell that. What's hard and defensible: (a) the balance changing on the lock screen
  within seconds of paying, (b) POS integrations, (c) a scanner that works on a ₹8,000 Android
  phone with patchy wifi in a basement, (d) the compliance wrapper (DPDP consent, closed-loop,
  GST-clean invoicing).
- **The gap:** big chains already have Google Wallet via Pine Labs, EasyRewardz, Twid. Nobody
  serves the long tail — a ₹1,500-a-month Indian café. **That gap is the entire business.**
- **Correction (October 2026):** Apple Pay *is* live in India. The earlier line saying it was not live was wrong. Never claim otherwise in any post, video or deck. Wallet passes work in both Apple Wallet and Google Wallet.

### The single most important moment — build videos around it

> "A merchant watching their own points balance change on their own lock screen ten seconds after
> a test transaction is the moment the sale happens." — Playbook §12

The hero beat of any product video is: **scan at the counter → lock-screen notification
`+18 points at [MERCHANT]` → pass shows the new number.** Real-time, no app.

---

## 2. Brand system (settled)

Editable vectors (Figma): https://www.figma.com/design/vTKjIxSGWRJZPAY33bNzsh

### 2.1 The mark

Three strokes of the W are solid; the fourth is a **deck of four passes fanning out of it**.
**Each card is a different merchant** — that's why they're different colours. The middle stroke is
a **crease**: a lighter facet, as if the letter were folded from card stock.

- **Every corner is cut, never rounded.** Butt caps, mitre joins clipped to a **1.5 mitre limit**
  (the bevelled peaks are the mark's character), square card corners.
- **Clear space:** `0.3×` the mark's height on all four sides. Nothing crosses it.
- **Small cut** (tiny sizes): deck drops from four cards to two (gold + violet), letter thickens.
- **One-colour version** is a different drawing: the letter plus one card with the seam masked
  through. No knockout box.
- Never re-weight strokes, re-space cards, or re-track the wordmark. Scale the whole SVG.
- **The wordmark is outlined to vector paths** — never retype "WYSTAK" in a live font and call it
  the logo.

Geometry (viewBox `0 0 100 100`, content in `translate(3 -1)`): vertices A(9,26) · B(26,78) ·
C(43,30) · D(60,78); letter path A→B→C→D, stroke 18; crease = B→C segment in `#4C1D95`; deck =
four 18×58 rects, `rx 0`, each `rotate(r, 60, 78)` at r = 2, 10, 18, 26. Rebuild scripts:
`build_stack.py` (logo variants), `make_stack_sheet.py`, `build_boards.py`, `render_stack.mjs`.
**Use the files, not these numbers, for anything on screen.**

> **Motion idea that comes straight from the mark:** the four cards fanning out of the W
> (pivot point 60,78, rotations 2→10→18→26°) is a natural logo animation. The order is
> load-bearing — see below.

### 2.2 Colour

**The deck, back → front (order is load-bearing — never reverse it):**

| Card | Hex | Suit / product |
|---|---|---|
| 1 · back | Mint `#00E0A3` | ♣ Clubs |
| 2 | Gold `#FFC300` | ♦ Offers |
| 3 | Rose `#FF3D71` | ♥ Rewards |
| 4 · front | Violet `#8B5CF6` | ♠ Tickets |

Violet sits in front so the brand colour reads first and the stack recedes into brighter hues. The
cards never change colour — not on light grounds, not on dark, not for a campaign.

**Inks:**

| Name | Hex | Role |
|---|---|---|
| Void | `#0B0410` | Ground. **The brand is dark-first** |
| Aubergine | `#1A0B2E` | The letter; the ink on light backgrounds |
| Crease | `#4C1D95` | The fold facet — the W's middle stroke |
| Signal violet | `#7C3AED` | UI actions only. **One per view.** Never decoration |
| Paper | `#F7F5FA` | Type on dark |

Surfaces: `#140724` raised · `#1A0B2E` raised-2 · `#2A1145` hairlines.
Muted text: `#9C8FB3` on dark, `#6B5D82` on light — **never swap them.**
Status colours (`#17C98B` ok · `#F5A524` offline · `#F04E6E` replay blocked) are **scanner UI only,
never marketing.**

Usage: on light backgrounds the ink is **aubergine, not violet** (violet on white vibrates). The
four card colours belong to the logo and pass artwork — don't scatter them through UI as accents.
Depth comes from the surface ladder plus hairlines — no drop shadows, no gradient washes.

### 2.3 Type

| Face | Use |
|---|---|
| **Archivo Black** | Wordmark (uppercase, 0.04em); headlines that must hit hard |
| **Archivo SemiBold (600)** | Tagline, eyebrows, small-caps labels — uppercase, **0.16em** tracking |
| **Manrope** | Interface and body. Never below 15px on screen |
| **IBM Plex Mono** | Serials, point counts, barcode digits. Tabular figures |

All free Google Fonts. Display type takes **negative** tracking (−3.5% at 76px); eyebrows take
**positive** (+0.16em). Build note from earlier work: Google Fonts wasn't reachable from the build
container, so boards embedded local `@fontsource/archivo-black` / `@fontsource/archivo` woff2 as
base64 — otherwise renders silently fall back to Arial. Check fonts in every render.

### 2.4 Layout rhythm

Adopted from Linear's design language, reconciled to the brand: 4px base unit, 96px section gap,
1280px max content width. The logo is the only zero-radius element.

### 2.5 Tagline(s)

- **"ALL YOUR PASSES. ONE STACK."** — the tagline in the brand identity doc (Archivo SemiBold,
  uppercase, 0.16em).
- **"All for one. One for all."** — the motto from the four-suits architecture doc: four suits
  into one deck for the customer; one deck across four products for the merchant.

> ⚠ Open question: which is the primary tagline for videos? (See section 9.)

---

## 3. The four suits — product architecture

The four cards in the W are four product lines, mapped to the four Apple pass styles WYSTAK uses.

| Suit | Colour | Product | Pass style | For |
|---|---|---|---|---|
| ♥ Hearts | Rose `#FF3D71` | **Rewards** | `storeCard` | Cafés, bakeries, restaurants, cinema F&B |
| ♠ Spades | Violet `#8B5CF6` | **Tickets** | `eventTicket` | Fests, gigs, nightlife, cinema, conferences |
| ♣ Clubs | Mint `#00E0A3` | **Clubs** | `storeCard` + expiry | Gyms, co-working, college societies, cinema membership |
| ♦ Diamonds | Gold `#FFC300` | **Offers** | `coupon` | Time-limited vouchers, festival campaigns, win-backs |

Why: Hearts = loyalty/affection (~70% of passes). Spades ranks highest and "cuts" — the ticket
decides whether you get in. Clubs: a gym *is* a club (the coincidence people repeat back). Diamonds
were historically the merchants' suit — coin and trade.

**The joker:** `boardingPass`, the fifth Apple style, is deliberately not played — transit in India
is already partnered. A named reason to say no keeps the roadmap from drifting.

**Build reality (important for what a video can claim today):** Phase 0/1 focus is **Rewards
(loyalty) for cafés**. Ticketing is a later phase (months 19–30). The Team guide tags product
features as Loyalty ("what we're building now"), Ticketing ("events, later") or Platform. Videos
can tell the four-suit story as vision, but must not claim ticketing, memberships with expiry
countdowns, or offers are live unless the team confirms.

Colour discipline: the logo's card order stays mint → gold → rose → violet. Suit colours are for
product surfaces (dashboards, docs, pass accents), not for re-ordering the logo.

---

## 4. Voice and copy

### 4.1 Notification voice (every on-screen push)

1. **The number leads.** `+18` opens the push, not a feeling.
2. **Ninety characters.** Title under 40, body under 90. iOS truncates.
3. **One scan, one push.** Never a digest, never a promo blast.
4. **The merchant is the name.** Customers know the café, not WYSTAK. WYSTAK sits second, small.

Reference push: **"+18 points at Bean Theory"** / *"You're at 132 of 150. One more and the
next one is on the house."*

Wallet pushes carry no payload — the phone fetches the new pass — so the substance lives on the
pass face, not in the notification.

### 4.2 Product copy

- Lead with **what changes for the merchant**, not technology.
- No invented stats; bracketed placeholders instead.
- Indian English, ₹.
- Niche one-liners from the playbook that work as video hooks:
  - Cafés: **"Buy 9, get the 10th free"** — stamp cards beat points here.
  - Gyms/salons: **"Kill the plastic card, and put an expiry countdown in every member's pocket."**
    *(vision line — expiry/renewal features are not built yet; see rule 8)*
  - QSR: **"₹150 off"** converts better than "1,500 points".
  - Merchant ROI line: one café's modelled net gain ≈ **11× the platform fee** — must be labelled
    *modelled*, not proven (see section 6).

### 4.3 Pass-face design rules (for any pass shown in a video)

- One number in the top-right header field — the only thing visible when the pass is collapsed
  in the wallet stack (e.g. `7 / 10` or `FREE COFFEE READY`).
- Brand colour fills the whole pass. Real product photography in the strip, not a stock cup.
- Member first name on the pass. Never more than four visible fields.
- QR first, Code 128 fallback, digits printed underneath.
- Strip image size: **375pt wide, up to 144pt tall** (corrected 5 Oct 2026; the old 375×98 is
  wrong).

---

## 5. The market and the merchant story

**Beachhead:** cafés and bakeries in **one neighbourhood of Bengaluru** (then Mumbai → Delhi NCR →
Pune, Hyderabad, Ahmedabad, Jaipur). Highest visit frequency (2–8×/month), one decision-maker, no
regulatory complexity.

**Niche ladder:**

| # | Niche | Pass | Role |
|---|---|---|---|
| 1 | Cafés & bakeries | storeCard | Beachhead |
| 2 | QSR & casual dining | storeCard + coupon | Revenue engine |
| 3 | Gyms, salons & wellness | storeCard + expiry | Underrated, short sale |
| 4 | College clubs & campus | eventTicket + generic | Distribution, not revenue |
| 5 | Nightclubs & events | eventTicket | Highest Apple share, hardest ops |
| 6 | Cinema | storeCard → eventTicket | Year three |

**Enrolment funnel:** a counter standee QR is the whole funnel. Phone number + first name only;
every extra field costs 15–20% of enrolments. DPDP notice inline. Pass issued in under ten seconds.

**Pricing (ex-GST, from the playbook — confirm before showing on screen):**

| Tier | Monthly | Setup | Includes |
|---|---|---|---|
| Starter | ₹1,499 | ₹2,500 | 1 outlet · loyalty pass · 2,000 active passes · scanner · both wallets |
| Growth | ₹3,999 | ₹7,500 | ≤3 outlets · loyalty + coupons · 10,000 passes · POS · campaigns |
| Chain | ₹12,999 | ₹25,000 | ≤15 outlets · all pass types · API · tiering |
| Enterprise | ₹60,000+ | ₹1,50,000 | Unlimited · SLA · own certificates · white-label |

Ticketing: ₹1.50/pass, guestlists free, campus fests free to the society (sponsor-funded).
Scanner app free, unlimited devices. Data export free — merchants can always leave with their list.
Annual prepay: 10 months for 12.

> The landing page treats price as a placeholder `[PRICE]` until confirmed — videos should do the
> same unless the team signs off.

---

## 6. Numbers that may appear on screen — and how

**Market sizing (sourced in the playbook; cite as such):**
India loyalty market $3.45B (2025) → $7.18B by 2030 · India online event ticketing ~$3.6B (2025) ·
500,000+ restaurants represented by NRAI · ~95% of Indian phones are Android · Apple ~7–9% of
shipments · Petpooja ~60 lakh bills/day across 100,000+ outlets · ~13.6M paid gym memberships.

**Modelled, not measured — must be labelled "modelled" or kept off screen:**
Café ROI ≈ ₹45,000/month net, ~11× the Growth fee (assumes 18% visit-frequency lift — the
playbook itself says replace this with real pilot data). 36-month ARR ~₹12.9 crore, ~3,100
merchants.

**Proof numbers from real pilots: none yet.** The landing page has three empty proof-number slots
waiting on the canary/pilot. Use `[N]` placeholders.

**Product promise you can state:** points update on the lock screen **in under 10 seconds** — this
is the Phase 0 engineering target (p95 < 10 s). Phrase as "within seconds" unless the team confirms
the measured figure.

---

## 7. Assets that already exist

- **Figma brand file:** https://www.figma.com/design/vTKjIxSGWRJZPAY33bNzsh (logo vectors, boards)
- **`wystak-design` plugin** (installed): `wystak-brand` (the system — always wins),
  `design-taste-frontend`, `image-to-code`, `web-design-guidelines`, `design-md-library`
  (74 DESIGN.md references incl. Linear). Declares Playwright and 21st.dev MCP servers (21st needs
  `TWENTY_FIRST_API_KEY`).
- **Landing page + wallet pass boards** rebuilt on the card-stack mark (placeholders still open —
  merchant logos, three proof numbers, price, contact email, entity name, city).
- **Four-suits board:** `suits.py` → `suits.html` → `wystak-four-suits.png` (1520px, 2×).
- **Demo passes in `wallet-demos/`:** two businesses — "Bounce Hair Salon" and "Sip Grove Juice
  Bar" (points and visits versions), plus iOS 27 poster-pass work (`posterGeneric`: `primaryLogo`
  30pt tall × 30–126pt wide; `artwork` 358×448pt). ⚠ Confirm these two are fictional before they
  appear in any video — the brand rule allows only fictional merchants.
- **Team WYSTAK workspace** (claude.ai page) — tasks, Sales pipeline, Ideas, Links & files.

---

## 8. Team and timeline

- **Team:** Kushagra, Abhishek, Harsh, Parv (the Team WYSTAK workspace; Kushagra owns sharing).
- **Working horizon:** tasks tracked to **31 December 2026**.
- **Engineering docs** refer to CF1 (backend), CF2 (marketing, copy, legal, credentials — writes
  every customer-facing string including push copy), CF3 (Android + front end). Map names to roles
  with the team, not by guessing.
- **Stack** (for any product footage): Python/FastAPI backend, Postgres on AWS Mumbai
  (`ap-south-1`), HTMX merchant dashboard, native Kotlin Android scanner. All customer data stays
  in India.
- **Where the product is:** Phase 0 build plan (46 tasks) → first pilot café → first paid GST
  invoice. Phase 0's headline demo is 10/10 transactions updating the lock screen in < 10 s on
  both platforms.

---

## 9. Open questions to settle before scripting

1. **Primary tagline:** "ALL YOUR PASSES. ONE STACK." or "All for one. One for all."?
2. **What's live vs. vision** at the time each video ships — which suits/features can be shown as
   real.
3. **Pricing on screen** — show the playbook tiers, or `[PRICE]`?
4. **Real proof numbers** from the pilot/canary, if any exist yet.
5. **Contact email, entity name, launch city/neighbourhood** for end cards.
6. **Bounce Hair Salon / Sip Grove Juice Bar** — confirmed fictional?
7. **Two small inconsistencies between brand sources** (the `wystak-brand` skill wins, but confirm):
   - Small-cut threshold: skill says below 32px; identity doc says 28px and below.
   - Corner radii: skill says 16–20px panels / 10–12px controls / 8px inputs; identity doc says
     16px panels / 12px cards / 8px controls.
8. **Aspect ratios and channels:** 9:16 reels (Instagram, YouTube Shorts) vs 16:9 explainer vs
   1:1 — and English, Hindi, or both? (The consent notice is EN + HI, so Hindi is in scope.)

---

## 10. Suggested video beats (starting point, not decided)

These follow the documents above; treat as a draft brief for the first session.

- **Launch / hero film (30–45s):** dark Void ground → the four cards fan out of the W → counter
  scan at Bean Theory → lock screen: `+18 points at Bean Theory` → pass face shows
  `132 / 150` → "No app. No plastic." → Apple **and** Google Wallet side by side → tagline → logo.
- **Merchant explainer (60–90s):** the problem (plastic cards lost, apps nobody installs, WhatsApp
  messages nobody scrolls back to) → standee QR enrolment in under ten seconds → scan on a cheap
  Android phone, works offline → balance updates within seconds → dashboard shows enrolments this
  week → `[PRICE]` / CTA.
- **Niche reels (15–20s each, 9:16):** café stamp card ("Buy 9, get the 10th free"), salon, gym —
  each ending on the pass in the wallet stack.
- **"Four suits" brand piece:** each card lands as its suit and product; "All for one. One for
  all." — clearly framed as the roadmap where features aren't live.

Every frame passes the brand skill's pre-ship check: right logo cut and clear space; exactly one
signal-violet action; every number real or bracketed; no real company names; contrast ≥ 4.5:1;
holds at phone width.
