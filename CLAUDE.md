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
- No invented statistics, prices, customers or traction. The fictional sample merchant is **Paper Crane Coffee**. No real company logos; show Apple Wallet and Google Wallet with equal weight.
- Claims allowed (pitch deck): no app, scan at the counter to add the pass, points on the lock screen within seconds of a scan, and the owner sees who comes back and who stopped.
- Full context: `wystak/WYSTAK_Project_Context.md`, `wystak/WYSTAK_Pitch_Deck.pdf`.

## Build notes (this cloud environment)

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
- Music: calm, cinematic, no kick drum (Mixkit 543 "A New Life"); bed levelled to -21 LUFS, played at 0.5 and carved under the voice. Softened under the problem, quiet build under the question, full entry on the brand.
- Voice: when a take is longer than the slot, `storyboard/edit_vo.py` (loyalty reel) tightens pauses and speeds it up with Rubber Band (pitch and formants kept), then opens the story pauses by hand. Up to ~1.25x stays natural.
- Alignment: pocketsphinx `Decoder.set_align_text()`, decode, then read word timings from `dec.seg()` (`get_alignment()` returns None). Add "Why-stack" as `W AY S T AE K`; map "é" to "e".
- Re-cutting to a new voice: keep the old film's times and map them with one piecewise time table anchored on the words the scripts share (`tmap_v11.py`); a proxy timeline maps every GSAP position and scales durations. New scenes are written in real time on the raw timeline.
- Logos: never redraw. To animate the supplied logo, cut out only the white connected to the border, then split it into layers by colour (`storyboard/split_lockup_v11.py`); stacked unmoved the layers must equal the file.
- HyperFrames gotchas: never set `visibility` on a `.clip` element (lint error; end the clip with its data-duration instead); clips stretched by a time map must not run past their footage.
