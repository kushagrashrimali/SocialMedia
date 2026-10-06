# WYSTAK social media reels and posts

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

Commit and push work without asking.

## Inputs from the user

The user drops reference videos, ElevenLabs audio, reference screenshots/PDFs and photos into `inbox/<date-topic>/` (git-ignored) and points to them with `@inbox/...`. Watch videos by extracting frames and audio with ffmpeg. Put finished outputs in `wystak/` (posts, final MP4s) and `videos/<name>/` (reel projects), and tell the user each file's path. For a new carousel, copy `wystak/carousels/launch/` to `wystak/carousels/<name>/` and edit its `build.py`. User-facing steps are in `SETUP.md`, Part B.

## Brand and content rules

- Audience for reels: **merchants** (café, restaurant and shop owners), not consumers.
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
