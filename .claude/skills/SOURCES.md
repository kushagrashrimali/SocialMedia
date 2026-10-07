# Installed skills

Vendored copies of third-party Claude skills. Claude Code loads them automatically from `.claude/skills/`.
To update, re-clone the upstream repo and copy the skill folder over.

| Upstream repo | Commit | Skills |
|---|---|---|
| [heygen-com/hyperframes](https://github.com/heygen-com/hyperframes) | f80614c | hyperframes, hyperframes-core, hyperframes-animation, hyperframes-keyframes, hyperframes-creative, hyperframes-audio, hyperframes-cli, hyperframes-registry, hyperframes-studio, media-use, motion-doctrine, product-launch-video, general-video, motion-graphics, embedded-captions, faceless-explainer, pr-to-video, slideshow, music-to-video, talking-head-recut, remotion-to-hyperframes, figma, cut-the-curve, seam-craft, oversized-cursor, captions-overlay, changelog-video |
| [AbubakrChan/product-launch-motion](https://github.com/AbubakrChan/product-launch-motion) | 951d614 | product-launch-motion |
| [iart-ai/tiktok-video-skills](https://github.com/iart-ai/tiktok-video-skills) | 2a77533 | short-form-video, caption-animation |
| [echris6/motion-video-kit](https://github.com/echris6/motion-video-kit) (MIT) | 255562b | business-motion-film |
| [nolangz/pixel2motion](https://github.com/nolangz/pixel2motion) (MIT) | e9faedb | pixel2motion (without docs/ gallery) |
| [Jakeschincariol/instagram-agent-skill](https://github.com/Jakeschincariol/instagram-agent-skill) | d03c56b | ig-reel, ig-story, ig-caption, ig-viral, ig-repurpose |
| [emilkowalski/skills](https://github.com/emilkowalski/skills) | e8a175d | animate, animate-expo, animation-vocabulary, apple-design, ask-sonner, break-ui, emil-design-eng, find-animation-opportunities, improve-animations, mobile-native, pick-ui-library, prototype, review-animations, write-swift (installed with `npx skills add`; motion and UI-polish guidance used for the reels' phone and notification animation) |

Each skill keeps its upstream LICENSE terms.

## Considered and left out

- **video-shotcraft, remotion-dev/skills**: built on Remotion. This repo uses HyperFrames as its one video engine, and two engines would compete for the same requests. Remotion also needs a paid company license for larger teams.
- **onetake**: PolyForm Noncommercial license, so it can't be used for a commercial launch video.
- **OpenMontage**: a 92 MB standalone production system that overlaps with HyperFrames.
- **guizang-product-video-skill**: AGPL, written in Chinese, and overlaps with product-launch-video.
- **diffusionstudio/lottie**: needs its own Skia player. HyperFrames already has a Lottie adapter.
- **gooseworks-ai/gooseworks-ads-skills** (render-ios-lockscreen, notification-flood-ad): not reachable — the repo is private or no longer exists (anonymous clone refused). The public gooseworks-ai/gooseworks skills (goose-ads, goose-video and others) are front-ends to GooseWorks' paid, credit-billed cloud service, so they were not installed.
