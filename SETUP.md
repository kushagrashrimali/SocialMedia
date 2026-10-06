# Running this repo on your own computer

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
