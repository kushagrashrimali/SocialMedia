# Running this repo on your own computer

Part A sets up your laptop (do it once). Part B is the everyday guide: how to make a reel or a carousel with Claude Code, including how to hand it files.

# Part A: Setup (one-time)

These steps set up Claude Code on your own laptop, signed in with a Claude subscription, so you don't use Claude Code cloud credits. Everything else in the repo (HyperFrames, ffmpeg, Chrome, the Python helpers) is free software running locally.

If a command here doesn't match what you see, check the official docs: https://code.claude.com/docs

## 1. Claude plan

Sign up for a paid Claude plan (Pro or Max) at https://claude.ai/pricing. Claude Code usage is included in the plan.

## 2. Tools (one-time)

| Tool | Mac | Windows |
|---|---|---|
| Git | `brew install git` or https://git-scm.com | https://git-scm.com |
| Node.js (LTS) | https://nodejs.org | https://nodejs.org |
| Python 3 | `brew install python` | https://python.org (tick "Add to PATH") |
| ffmpeg | `brew install ffmpeg` | `winget install ffmpeg` |
| Google Chrome | https://google.com/chrome | https://google.com/chrome |

No Homebrew on the Mac yet? Install it from https://brew.sh.

## 3. Claude Code

- Mac or Linux: `curl -fsSL https://claude.ai/install.sh | bash`
- Windows (PowerShell): `irm https://claude.ai/install.ps1 | iex`
- Or, with Node installed: `npm install -g @anthropic-ai/claude-code`

The Claude desktop app's **Code** tab works too.

## 4. Get the project

```bash
git clone https://github.com/kushagrashrimali/SocialMedia.git
cd SocialMedia
```

If the work isn't merged into `main` yet, also run `git checkout claude/social-media-video-skills-tdpjs5`.

## 5. Python and Node helpers (one-time)

```bash
pip install pillow numpy pocketsphinx
cd videos/wystak-launch-reel && npm install && cd ../..
```

## 6. Start

```bash
claude
```

Choose to sign in with your Claude account (not an API key). Claude Code reads `CLAUDE.md` (the reel and post steps and the brand rules) and loads the skills in `.claude/skills/` automatically.

## Everyday commands (no AI needed)

| Task | Command |
|---|---|
| Rebuild the launch carousel | `python3 wystak/carousels/launch/build.py` |
| Preview a reel in the browser | `cd videos/wystak-launch-reel && npx hyperframes preview` |
| Check a reel | `npx hyperframes check` (inside the reel folder) |
| Render a reel | `npx hyperframes render -q delivery -o renders/out.mp4` |

If the carousel builder can't find Chrome, point it there: `CHROME="/path/to/chrome" python3 wystak/carousels/launch/build.py`.

## Differences from the cloud session

The cloud session's network blocked several sites, so it used workarounds. On your laptop:
- Instagram links, stock photos and Google Fonts all load.
- Whisper transcription works (`npx hyperframes transcribe`). The pocketsphinx aligner in `CLAUDE.md` still works as an offline fallback.
- You can watch reels live in the HyperFrames preview, or edit them in the free HyperFrames desktop app.

---

# Part B: Making content

## How you give Claude Code files

The Claude Code terminal has no upload button. It works with files that are **on your computer inside this project folder**, so "sending a file" means putting it in a folder and telling Claude where it is.

**1. Make a job folder for each piece of content.** Inside `inbox/`, create a folder per reel or post, named with the date and topic:

```
inbox/
  2026-10-20-diwali-reel/
    reference.mp4      <- the reel you want to copy the style of
    voiceover.mp3      <- your ElevenLabs audio (added later, at step 3)
    notes.txt          <- optional: anything you want to say about it
  2026-10-22-offline-scanner-carousel/
    ref-1.png          <- screenshots of posts you like
    ref-2.png
    reelo-profile.pdf  <- or a PDF of an account's grid
    photo-counter.jpg  <- any photo you want used in the post
```

Drag files into the folder in Finder or File Explorer, as with any folder. `inbox/` is ignored by git, so third-party reference videos and raw audio never get uploaded to GitHub. The finished reels and posts are saved under `wystak/` and `videos/`, and those are committed.

**2. Point Claude at the files in your message.** Use any of these:

| Way | How |
|---|---|
| `@` mention | Type `@` and start typing the path, e.g. `@inbox/2026-10-20-diwali-reel/reference.mp4`. It autocompletes. |
| Drag and drop | Drag the file from Finder or Explorer into the Claude Code window; its path is pasted in. |
| Just say it | "The reference video is in inbox/2026-10-20-diwali-reel." Claude can list the folder itself. |
| Paste a screenshot | Copy an image and paste it into Claude Code (try Ctrl+V; on some setups Cmd+V). Good for one quick reference. |

**Reference videos from Instagram:** Claude can't log in to Instagram, so a reel link alone usually won't work. Save the reel to your phone or laptop first (screen-record it, or use a reel downloader), put the MP4 in the job folder, then point to it. Claude "watches" a video by pulling out frames and the sound with ffmpeg, as it did for the first reel.

**Getting results back:** Claude saves outputs as files and tells you the path. Open them in Finder or Explorer: PNGs open in your image viewer and MP4s in your video player. Reels can also be watched live in the browser (see the reel steps below).

## Making a reel (5 steps)

Open a terminal in the project folder, run `claude`, then go step by step. Wait for each answer before moving on.

**Step 1: reference video.** Put the reference MP4 in a new job folder, then say:
> Let's make a new reel. Follow the reel process in CLAUDE.md. The reference video is @inbox/2026-10-20-diwali-reel/reference.mp4. The topic is: (one or two lines on what this reel should say).

Claude studies the reference (story, pacing, design, captions, sound) and tells you what it found.

**Step 2: script.** Claude writes the voiceover script in the reference's style and saves it in `wystak/scripts/`. Ask for changes until you like it ("make the hook shorter", "less salesy").

**Step 3: audio.** Paste the script into ElevenLabs, generate the voice, download the MP3, and save it as `voiceover.mp3` in the job folder. Then say:
> The audio is ready: @inbox/2026-10-20-diwali-reel/voiceover.mp3. Make the storyboard.

**Step 4: storyboard.** Claude matches every word to the audio, sets up a new project in `videos/<name>/` (copying the launch reel's style and fonts), and sends a storyboard: one still image per scene with its time and line. It saves the storyboard as an image (for example `videos/<name>/snapshots/contact-sheet.jpg`); open it to review. Reply with what to change, for example:
> Scene 3: replace the chat screen with a café counter. Scene 6: make the text bigger.

Repeat until you're happy. To see real motion before the final render, run `cd videos/<name> && npx hyperframes preview`; it opens the reel in your browser.

**Step 5: "go".** Say **go**. Claude builds the reel, checks it, renders it, sets the loudness for Instagram and saves the MP4 (for example `wystak/<name>.mp4`). It commits and pushes the work, and you upload the MP4 to Instagram.

## Making a carousel or single-image post (4 steps)

**The template.** Every post reuses the design system of the launch carousel: `wystak/carousels/launch/build.py`. That file holds the colours, fonts, phone and pass drawings, the logo badge and the slide layout. Claude copies it into a new folder (for example `wystak/carousels/offline-scanner/`) and changes the text and visuals, so all your posts look like one family. You don't need to edit it yourself. If you ever want a different look, say so and name a reference.

**Step 1: brief and reference.** Put screenshots or PDFs of posts you like (and any photos you want used) in a job folder, then say:
> Let's make a carousel. Follow the post process in CLAUDE.md. Topic: (what it's about and who it's for). References are in @inbox/2026-10-22-offline-scanner-carousel/. Use the launch carousel template.

Mention any real facts you're happy to show (an offer, a real number). Otherwise Claude uses no numbers.

**Step 2: copy.** Claude sends the slide-by-slide text, the caption and the cover alt text. Edit or approve.

**Step 3: draft sheet.** Claude renders all slides and saves one preview image of every slide side by side. Open it and reply with changes ("slide 4: swap the phone for the dashboard").

**Step 4: "go".** Say **go**. Claude exports the final PNGs to `wystak/carousels/<name>/slides/`, saves the caption in a copy file next to them, commits and pushes. Upload the PNGs to Instagram in order (01, 02, ...) and paste the caption.

## Small things that help

- **One job per Claude session.** Start a new `claude` session for each new reel or post; type `/clear` to start fresh in the same window.
- **Pick up later:** everything is saved in files, so if you close the session you can come back with "Continue the Diwali reel in videos/diwali-reel; we were at the storyboard step."
- **Change an old post:** "Change slide 6 of the launch carousel to say ... and re-render it." Claude edits that project and rebuilds it.
- **Rebuild without AI:** `python3 wystak/carousels/<name>/build.py` remakes a carousel; `npx hyperframes render` inside a reel folder remakes a reel.
- **Brand rules** (merchant audience, no invented numbers, Paper Crane Coffee, the logo files, "Whys-tak" in ElevenLabs) live in `CLAUDE.md`, and Claude follows them automatically. Edit that file to change a rule.
