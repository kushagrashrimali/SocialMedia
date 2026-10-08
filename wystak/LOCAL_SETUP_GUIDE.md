# WYSTAK reels: how this project works and how to run it locally

Paste this file into a Claude chat to get step-by-step help setting up the project on your own PC.

## 1. What this is

A GitHub repo (`kushagrashrimali/SocialMedia`, branch `claude/modest-fermi-lv21nq`) that makes WYSTAK's marketing videos and posts with code:

- **Reels (video):** HTML + GSAP + Three.js, rendered to MP4 by HyperFrames (headless Chromium + ffmpeg).
- **Carousels and LinkedIn posts:** HTML slides rendered to PNG/PDF by headless Chromium (`wystak/carousels/launch/build.py`).
- **Sound:** Python scripts (numpy/scipy/ffmpeg) re-cut a licensed Mixkit music track and add soft effects.
- **Rules and lessons:** `CLAUDE.md` at the repo root. Claude Code reads it automatically; it holds the brand rules, the process for each format and every lesson learned so far.

Projects:

| Folder | What it is |
|---|---|
| `videos/loyalty-evolution-reel/` | 50 s voiceover reel (done, delivered) |
| `videos/wystak-hype-reel/` | 23 s launch/hype film, no voiceover, hand-modelled phone |
| `videos/wystak-iphone-reel/` | 30 s McDonald's-style reel using your iPhone 17 Pro FBX model |
| `wystak/` | finished outputs, brand files, scripts, carousels, LinkedIn posts |
| `.claude/skills/` | the installed skills (list in section 5) |

## 2. What happens when you run it locally

Short answer: **rendering costs no tokens; only the chat with Claude does.**

- **Renders, ffmpeg, Python sound scripts, Chromium:** these run on your PC's CPU/GPU. No tokens at all.
- **Claude Code on your PC:** every message you send and every file it reads or writes uses tokens.
- **Limits, which depend on how you log in (check your own plan to confirm):**
  - Logged in with a Claude subscription: Claude Code shares the plan's usage limits, so local use does *not* remove limits.
  - Logged in with an Anthropic API key (Console): you pay per token and there is no plan session limit, only API rate limits.
  So to use "only tokens", use an API key.
- **Time:** a cloud session renders on software WebGL (about 3-4 s per frame, 8-10 minutes per reel). A PC with a decent GPU can be much faster (HyperFrames auto-detects the GPU; `--browser-gpu` forces it).
- **Network:** the cloud environment blocks CDNs, so everything is vendored locally (GSAP, fonts, three.js). That also means the project works offline on your PC.
- **Things you must bring yourself locally** (git-ignored on purpose): your iPhone 17 Pro model files, the licensed music and sound-effect downloads, and any voiceover audio. Section 4 says how.

## 3. Setup on your PC (Windows, macOS or Linux)

Install:

1. **Git**
2. **Node.js 20 or newer** (for `npx hyperframes`)
3. **ffmpeg** (including `ffprobe`; also needed with the `rubberband` filter if you re-time a voiceover)
4. **Python 3.10+** with: `pip install numpy scipy pillow pocketsphinx`
5. **Claude Code** (`npm i -g @anthropic-ai/claude-code`), then log in or set `ANTHROPIC_API_KEY`
6. Chromium: HyperFrames installs or finds its own (`npx hyperframes browser` / `doctor` if it complains). Do **not** run `playwright install` in the cloud; locally it is fine.

Get the project:

```bash
git clone https://github.com/kushagrashrimali/SocialMedia.git
cd SocialMedia
git checkout claude/modest-fermi-lv21nq
claude          # starts Claude Code in the repo; it reads CLAUDE.md and the skills by itself
```

## 4. Run each project

All commands run from the project folder, e.g. `cd videos/wystak-iphone-reel`.

**Common HyperFrames commands** (version 0.8.139 was used):

```bash
npx hyperframes@0.8.139 lint                       # check the composition
npx hyperframes@0.8.139 snapshot --at 0.5,3,7 --no-end --describe false -o snaps   # still frames + contact sheet
npx hyperframes@0.8.139 preview                    # live preview in the browser
npx hyperframes@0.8.139 render -q delivery -f 30 -w 4 -o renders/out.mp4            # final render
bash sound/master.sh renders/out.mp4 ../../wystak/out.mp4   # master to -14 LUFS, H.264/AAC
bash sound/verify.sh ../../wystak/out.mp4 some-folder       # contact sheet from the delivered MP4
```

### wystak-iphone-reel (30 s, uses your 3D model)

1. Put the two uploads somewhere, unpack the `.rar`, then:
   ```bash
   python3 tools/prep_model.py /path/IPhone17Pro.fbx "/path/iphone series_Textures/texture"
   ```
   This copies the FBX + four PBR maps into `assets/model/` and paints the Apple logo out of them (no real company logos).
2. Music and effects (free Mixkit licence; download once):
   - `https://assets.mixkit.co/music/33/33.mp3` -> `assets/music-src/mixkit-33-motivating-mornings.mp3`
   - `https://assets.mixkit.co/active_storage/sfx/<id>/<id>-preview.mp3` -> `assets/sfx-src/mixkit-<id>.mp3` for ids 2303, 168, 1492, 3114, 2357
3. Build the sound: `python3 -I sound/make_sound.py` (writes `assets/audio/reel-mix.wav`).
4. `lint`, `snapshot` to check, then `render`, `master.sh`, `verify.sh`.

Timing of every scene lives in `src/timing.js`. The scenes are in `index.html`; the 3D shots in `src/scene.js`; the phone and its screen in `src/phone.js` and `src/screens.js`.

### wystak-hype-reel (23 s, procedural phone)

Same steps; the music is Mixkit 69 "Ramp It Up" (`https://assets.mixkit.co/music/69/69.mp3` -> `assets/music-src/mixkit-69-ramp-it-up.mp3`) and effects ids 2303, 1465, 168, 1492, 2634, 787, 3114, 2357. `python3 -I sound/make_sound.py` writes `assets/audio/hype-mix.wav`.

### loyalty-evolution-reel (50 s, voiceover)

Needs the ElevenLabs voiceover in `assets/`. See `videos/loyalty-evolution-reel/storyboard/` (voice fitting, word alignment, retiming) and `sound/`.

### Carousels and LinkedIn

Copy `wystak/carousels/launch/` to `wystak/carousels/<name>/`, edit `build.py`, run it. Outputs go in `wystak/` or `wystak/linkedin/<name>/`.

## 5. Skills used (all live in `.claude/skills/`; Claude Code loads them automatically)

Sources and licences are in `.claude/skills/SOURCES.md`. "Used" means used in building these reels; "available" means installed for the same kind of work.

**Video engine and motion law (used on every reel)**
- `hyperframes`: entry point for any video request; routes to the others
- `hyperframes-core`: the composition contract (data-* timing, clips, tracks, deterministic rendering)
- `hyperframes-animation`: animation rules, scene blueprints, transitions, runtime adapters (GSAP, Three.js, Lottie)
- `hyperframes-keyframes`: zooms, camera moves, handoffs
- `hyperframes-creative`: palettes, type, beat planning
- `hyperframes-audio`: mixing, ducking, music carve under voice
- `hyperframes-cli`: lint / snapshot / render / doctor commands
- `hyperframes-registry`: ready-made blocks and effects
- `media-use`: music, SFX, voice, transcription helpers
- `motion-doctrine`: the seam rules (direction, matched speed, no idle wobble, stillness before climax)
- `cut-the-curve`: the transition catalog (zoom-through, waterfall, rack-focus)
- `seam-craft`: how seams composite correctly on the master timeline
- `general-video`, `motion-graphics`, `product-launch-video`, `product-launch-motion`: workflows for longer films, short motion units and launch/promo films

**Short-form and Instagram**
- `short-form-video`, `caption-animation`: vertical-video grammar, animated captions
- `ig-reel`, `ig-caption`, `ig-story`, `ig-viral`, `ig-repurpose`: scripts, captions, stories, swipe files; `ig-reel/hookscore.py` scores hooks for posts

**Animation craft**
- `animate`, `animation-vocabulary`, `apple-design`, `review-animations`: how to make motion feel right, name effects, Apple-style physical motion

**GSAP (official, free)**
- `gsap-core`, `gsap-timeline`, `gsap-plugins`, `gsap-utils`, `gsap-performance`, `gsap-react`, `gsap-frameworks`, `gsap-scrolltrigger`
- `gsap-motion`: GSAP video workflow (proprietary gratis licence, check terms before commercial use)

**Three.js (3D phone, lighting, materials)**
- `threejs-fundamentals`, `threejs-loaders` (used for the FBX), `threejs-materials`, `threejs-lighting`, `threejs-textures`, `threejs-postprocessing`, `threejs-shaders`, `threejs-geometry`, `threejs-animation`, `threejs-interaction`
- `threejs`: a full Three.js video workflow

**Available for other kinds of video (not used on these reels)**
- `remotion` plus the 12 official `remotion-*` skills (Remotion needs a paid company licence above three people)
- `manim`, `motion-canvas`, `wgpu-shaders`, `text-to-lottie`

**Brand**
- `wystak-design:wystak-brand` (plugin skill): logo geometry, colours, type, notification voice, "Paper Crane Coffee" sample merchant. The reels also follow `CLAUDE.md` brand rules: use the supplied logo files only, never redraw; tagline ALL YOUR PASSES. ONE STACK.; merchants as audience; Apple Wallet and Google Wallet with equal weight; no invented stats; no real company logos.

Skills removed as unused: animate-expo, ask-sonner, break-ui, emil-design-eng, find-animation-opportunities, improve-animations, mobile-native, pick-ui-library, prototype, write-swift, changelog-video, pr-to-video, talking-head-recut, embedded-captions, captions-overlay, faceless-explainer, slideshow, music-to-video, remotion-to-hyperframes, figma, hyperframes-studio, oversized-cursor, pixel2motion, business-motion-film.

## 6. The working process (what Claude follows from `CLAUDE.md`)

**Reels with a voiceover:** reference video -> script -> you record it in ElevenLabs -> storyboard of stills, stop -> build only after you say "go" -> render, master to about -14 LUFS, verify frames from the delivered MP4 -> commit.

**Reels without a voiceover (hype and iPhone reels):** study the reference reel (cut timings, type, pace, sound) -> plan scenes on a music grid (`src/timing.js`) -> build -> snapshot key frames and fix -> render -> master -> verify.

**Posts:** brief -> copy, stop -> draft sheet, stop -> final PNGs after "go".

**Commit rule:** only reusable scripts, templates and lessons go to git. Renders, drafts, voice takes, the 3D model and downloaded music/SFX stay out (they are in `.gitignore` or `.git/info/exclude`).

## 7. Lessons that matter most (full list in `CLAUDE.md`)

- One font family (Poppins) on the film; the key word stands out by colour and size only.
- No hand cursor, no sparkle bursts. Cuts go left and keep motion across the seam.
- Music: clean 100-120 BPM electronic, no vocals; re-cut one track so each section change lands on a downbeat; effects are few and soft (low-passed, only on story moments).
- Never put the phone on a dark ground: bright lilac set, matching reflections, soft violet shadow.
- Pace so people can read: prefer a longer reel over a faster one.
- The user's 3D phone lenses render flat: add a coated-glass disc over each.
- GSAP: use `immediateRender: false` on a later `fromTo` of an element with earlier tweens; set degenerate transforms with `gsap.set`, not inline CSS.

## 8. Good first prompts to give Claude Code locally

- "Read CLAUDE.md and .claude/skills/SOURCES.md, then run lint and a snapshot of videos/wystak-iphone-reel and tell me what is broken."
- "Re-render the iPhone reel at delivery quality and master it to -14 LUFS."
- "In the iPhone reel, change scene 6 to ... (describe), keep every cut on the music grid in src/timing.js."
- Tip: ask for snapshots of only the frames you changed instead of re-rendering the whole film while iterating.
