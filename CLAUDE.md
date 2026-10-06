# WYSTAK social media reels

This repo holds WYSTAK's marketing reels: scripts and brand files in `wystak/`, HyperFrames video projects in `videos/`, and the installed video and Instagram skills in `.claude/skills/`.

## Reel process (follow for every new reel)

1. **Reference video.** The user sends a reference reel. Study its story, pacing, design, type, captions and sound (contact sheets from ffmpeg, cut timings).
2. **Script.** Write the voiceover script in the reference's storytelling style. Plain script only: no [PAUSE]/[BEAT]/[EMPHASIS] marks unless asked. Commit it.
3. **Audio.** The user records the script in ElevenLabs and sends the audio file.
4. **Storyboard, then stop.** Don't build the reel yet. Force-align the audio to word timings, then deliver a storyboard showing every frame/image of the reel: a still of each scene at its key moment, with its time range, the line spoken and what moves. The user marks what they don't like; revise the storyboard until they're happy.
5. **Build only after the user says "go".** Then build, check, render, master the audio to about -14 LUFS, verify frames from the delivered MP4, and commit.

Commit and push work without asking.

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
