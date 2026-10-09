# WYSTAK social media: Instagram reels and posts, LinkedIn posts

This repo holds WYSTAK's marketing reels: scripts and brand files in `wystak/`, HyperFrames video projects in `videos/`, and the installed video and Instagram skills in `.claude/skills/`.

## Reel process (follow for every new reel)

1. **Reference video.** The user sends a reference reel. Study its story, pacing, design, type, captions and sound (contact sheets from ffmpeg, cut timings).
2. **Script.** Write the voiceover script in the reference's storytelling style. Plain script only: no [PAUSE]/[BEAT]/[EMPHASIS] marks unless asked. Commit it.
3. **Audio.** The user records the script in ElevenLabs and sends the audio file.
4. **Storyboard, then stop.** Don't build the reel yet. Force-align the audio to word timings, then deliver a storyboard showing every frame/image of the reel: a still of each scene at its key moment, with its time range, the line spoken and what moves. The user marks what they don't like; revise the storyboard until they're happy.
5. **Build only after the user says "go".** Then build, check, render, master the audio to about -14 LUFS, verify frames from the delivered MP4, and commit.

## Post process (carousels and single-image posts)

1. **Brief and reference.** The user sends the topic or goal of the post, a reference (screenshots or a PDF of posts or accounts they like, for mindset and not to copy), and any assets or facts they're happy to show (photos, offers, real numbers).
2. **Copy, then stop.** Send the slide-by-slide copy (headline, line under it and visual idea per slide), the caption and the cover alt text. Score the cover hook with `ig-reel/hookscore.py`. The user edits or approves.
3. **Draft sheet, then stop.** Render all slides and send one contact sheet showing every slide side by side. The user marks what to change; revise until they're happy.
4. **Final after "go".** Export the final 1080×1350 PNGs (1080×1080 if a square post is asked for), save the copy file with the caption and alt text, commit, and send the files.

Posts reuse the system in `wystak/carousels/launch/` (`build.py`: HTML slides rendered by headless Chromium, alternating navy and light slides, logo badge top-left, one accent word per headline).

Commit and push without asking, but only what is worth keeping: reusable scripts, templates and the lessons below. Do not commit every reel render, draft, voice take or intermediate media; send those to the user as files instead.

## LinkedIn process (posts for Wystak's company page)

The LinkedIn audience is wider than Instagram's: merchants first, plus investors, POS and payment partners, hires and other founders. The tone is professional and founder-led, still human. Formats: text only, text plus one image (1200×1200 or 1080×1350), a document carousel (a PDF, 1080×1350 pages) or native video (reuse a reel). Only the first two or three lines show before "…see more", so the hook must fit there. Use 3 to 5 hashtags, and put links in the first comment, not the post.

1. **Brief.** The user sends the goal (launch, insight or opinion, product explainer, milestone, hiring, event), the format or "you pick", references (screenshots or a PDF of LinkedIn posts or pages they like) and any real facts they're happy to share.
2. **Post text, then stop.** Send 2 or 3 hook options (scored with `ig-reel/hookscore.py`), the full post text, the hashtags and a first comment. For visual posts, also send the slide or image plan. The user edits or approves.
3. **Visual draft, then stop.** For image, document or video posts, render drafts in the Wystak look (reuse `wystak/carousels/launch/build.py` and adapt the sizes) and send a preview sheet. Revise until the user is happy. Text-only posts skip this step.
4. **Final after "go".** Export the final file (PNG for an image, a PDF combining all pages for a document carousel, MP4 for video). Save `post.md` with the post text, hashtags, first comment, alt text and a short reshare line for each founder. Everything goes in `wystak/linkedin/<name>/`; commit and push.

## Inputs from the user

The user drops reference videos, ElevenLabs audio, reference screenshots/PDFs and photos into `inbox/<date-topic>/` (git-ignored) and points to them with `@inbox/...`. Watch videos by extracting frames and audio with ffmpeg. Put finished outputs in `wystak/` (posts, final MP4s, `wystak/linkedin/<name>/` for LinkedIn) and `videos/<name>/` (reel projects), and tell the user each file's path. For a new carousel, copy `wystak/carousels/launch/` to `wystak/carousels/<name>/` and edit its `build.py`. User-facing steps are in `SETUP.md`, Part B.

## Brand and content rules

- Audience for reels and Instagram posts: **merchants** (café, restaurant and shop owners), not consumers.
- Logo: the navy, purple and teal three-card mark in `wystak/brand/`. Use the supplied files; never redraw it. Tagline: **ALL YOUR PASSES. ONE STACK.**
- The name is pronounced "WHYS-TAK". Spell it "Whys-tak" in ElevenLabs text.
- English only. The context is Indian (UPI, WhatsApp, kirana). India has no loyalty-card or stamp-card culture, so never build a story on lost loyalty cards.
- No invented statistics, prices, customers or traction. The fictional sample merchant is **Bean Theory** (a café). Never use Paper Crane Coffee again; it appears only in older reels. No real company logos; show Apple Wallet and Google Wallet with equal weight.
- Claims allowed (pitch deck): no app, scan at the counter to add the pass, points on the lock screen within seconds of a scan, and the owner sees who comes back and who stopped.
- Full context: `wystak/WYSTAK_Project_Context.md`, `wystak/WYSTAK_Pitch_Deck.pdf`.

## Build notes (this cloud environment)

- Skills: see `.claude/skills/SOURCES.md`. For 3D product shots, load the `threejs-*` skills (lighting, materials, textures, post-processing). For timelines and type motion, load `gsap-core` and `gsap-timeline`.
- Video engine: HyperFrames (`/hyperframes` skill). The first reel is `videos/wystak-launch-reel/`; reuse its structure, fonts (`assets/vendor/`) and its synthesised bed and SFX approach.
- CDN, Hugging Face and image hosts are blocked by the network policy, so:
  - vendor GSAP and fonts locally from npm;
  - force-align words with pocketsphinx (pip; the model is bundled) instead of Whisper;
  - draw objects in code.
- Storyboard stills: `npx hyperframes snapshot --at <times> --no-end --describe false` gives per-scene frames and a contact sheet.

## Lessons from the loyalty reel (keep applying these)

- Type: one family (Poppins) for everything laid over the film, one weight in captions; the key word is set apart by colour (Wystak violet #6b2ba6, a light tint on dark grounds) and size, never by a second font. Phone screens keep their iOS-like UI type.
- Motion: no hand cursor and no sparkle bursts. Glass, focus pulls and zoom-through seams; the scale direction must match across a cut (motion-doctrine skill).
- Sound: minimal, Apple-style. Only story moments make a sound (alerts, the pass landing, the brand chime, payment, the logo); nothing on cuts, no taps or ticks; low-pass the SFX bus (~8.5 kHz), effects ~-37 LUFS against the voice. Notifications: a soft two-note bubble pop (Mixkit 2357). Real Apple sounds are copyrighted.
- Music: product intro / launch films use clean, mid-tempo electronic (about 100-120 BPM), no vocals, a steady light pulse and a gradual build. Both extremes were rejected: a club kick ("Cat Walk", too dancy) and cinematic swells ("A New Life", too operatic). The loyalty reel uses Mixkit 33 "Motivating Mornings" (120 BPM). Judge candidates by measured kick share and pulse strength when you can't listen (`sound/make_music.py` notes). Bed levelled to -21 LUFS, played at 0.5, carved under the voice; the track as written under the problem, a low-pass filter build under the question, the full entry on a downbeat at the brand.
- Layout: keep captions low (top ~1420 of 1920) with the phones and cards moved down to meet them; a caption band at 1300 left the lower third empty. Over hand-held footage, captions sit just above the phone (~470).
- Pace: viewers need time to read. A ~50-word-per-20s script squeezed to 40s (1.22x) felt too fast; the same script at near-natural speed (~1.05x) with ~0.3s between lines and ~0.8s before the brand reads well at ~50s. Prefer a longer reel over a faster voice.
- Voice: `storyboard/edit_vo.py` (loyalty reel) fits a take to a target length: it caps each pause, applies one Rubber Band tempo (pitch and formants kept), then opens the story pauses by hand (before the brand, after the name, before the end card).
- Alignment: pocketsphinx `Decoder.set_align_text()`, decode, then read word timings from `dec.seg()` (`get_alignment()` returns None). Add "Why-stack" as `W AY S T AE K`; map "é" to "e".
- Re-cutting to a new voice: keep the old film's times and map them with one piecewise time table anchored on the words the scripts share (`tmap_v11.py`); a proxy timeline maps every GSAP position and scales durations. New scenes are written in real time on the raw timeline.
- Brand reveal that worked: no glass card. Every kind of loyalty pass flies in from the frame edges and fans out, snaps into one stack, then shrinks and turns into the passes of the mark; the W rises to catch it with a soft light bloom, the purple and teal passes flick out, the wordmark cascades in on the name with the chime (`v11_template.html`, scene X).
- Logos: never redraw. To animate the supplied logo, cut out only the white connected to the border, then split it into layers by colour (`storyboard/split_lockup_v11.py`); stacked unmoved the layers must equal the file.
- HyperFrames gotchas: never set `visibility` on a `.clip` element (lint error; end the clip with its data-duration instead); clips stretched by a time map must not run past their footage.

## Lessons from the hype reel (launch film, no voiceover)

- Project: `videos/wystak-hype-reel/`. The phone and passes are modelled in Three.js (vendored, no CDN) in `src/phone.js` and `src/passes.js`. Screens are canvas textures in `src/screens.js`. `renderAt(t)` is a pure function of time driven by `hf-seek`; register it in `window.__hf.buildReady`. Software WebGL renders at about 3-4 s per frame, so snapshot a few times before a full render.
- Never put the phone on a dark ground. Product shots sit on a bright lilac set:
  - backdrop: a gradient from #d8ccf8 to #b9a5ee with a white light pool behind the product;
  - reflections: the environment matches the set (a lilac room at low intensity with white strip lights), so the titanium and glass pick up the set's colour;
  - shadow: a soft violet `drop-shadow` on the WebGL canvas;
  - fill light: keep it low (hemisphere 0.3 or less) and keep the pass faces' clearcoat soft, or dark passes look milky.
- Type cards stay paper (#f3f1f6), so they stand apart from the lilac set.
- When passes stack, space them apart (z of 0.3 or more) and square each one to the stack before it lands, so they never cut through each other.
- Music for a film with no voiceover: re-cut one track on its own grid (`sound/make_sound.py`), with every scene change on a downbeat. The build should match the picture:
  - the filter opens and hits get closer together as the cuts speed up;
  - stop the music before the reveal;
  - the drop lands on the mark;
  - step up to a fuller section on the key action;
  - a snare roll or stutter leads into the climax;
  - the end card sits on the start of the track's last phrase and finishes on the track's own ending.

## Lessons from the iPhone reel (McDonald's-style, user's 3D model)

- Project: `videos/wystak-iphone-reel/` (30 s, no voiceover). It follows the McDonald's app reel's rhythm:
  - a new beat every 1.5-2.5 s;
  - white UI cards on a bold brand ground (violet), alternating with paper;
  - two-size Poppins captions ("Your / regulars.");
  - the mark alone mid-film, the end card on paper;
  - product shots of the phone in between.
- The user's iPhone 17 Pro model (FBX plus PBR maps) is git-ignored in `assets/model/`. Rebuild it from the two uploads with `tools/prep_model.py`, which paints the Apple logo out of every map.
- In three.js:
  - load the model with the vendored `FBXLoader` (it needs `fflate` and `NURBSCurve` next to it);
  - assign one `MeshPhysicalMaterial` with the maps;
  - lay our own screen over the display: measure its rectangle in the BaseColor atlas, then least-squares-fit atlas UV to model position on the front face (`src/phone.js`).
- The model's lenses render as flat grey. Lay a coated glass disc with a drawn lens texture over each one; don't split the mesh.
- GSAP: a `fromTo` placed later on an element that already has tweens needs `immediateRender: false`, or its start state shows early.
- GSAP: don't put a degenerate CSS transform such as `scaleX(0) rotate()` inline; set it with `gsap.set`.
- Card flips read better flat (`scaleX`) than with a strong `rotationY` perspective.
- Pushes that stack, iOS-style: each new one lands in the bottom slot and lifts the earlier ones. Don't let rising cards cross each other.

## Lessons from the object-style launch post (Instagram design direction)

- Project: `wystak/carousels/launch-objects/` (`build.py`). The user's references were agency posts from Pinterest. This is the design thinking to keep for every Instagram post:
  - one real-world object carries each slide's idea (a delete dialog, a newspaper, a counter stand, an order pad, an envelope), drawn in code;
  - huge condensed capitals with one handwritten accent word, plus a small sans for the line under it;
  - one bold ground per slide, warm paper in between, with grain, real shadows, halftone cut-outs, highlighter tape and hand-drawn arrows or circles;
  - very few words per slide.
- Never repeat a post's design pattern. Each new post needs new objects, layouts, grounds and type pairings, with the same level of thinking and craft. The launch post used Anton + Caveat + Poppins on violet, navy and paper; pick a different combination next time.
- The launch post has no logo badge on the slides (the brand appears in the reveal and the end card). Ask before adding one.
- Carousels: keep them to 4-5 slides.
- Wystak also offers NFC: a customer taps the counter stand to become a member (as well as scanning the QR).
