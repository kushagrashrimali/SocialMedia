# Installed skills

Vendored copies of third-party Claude skills. Claude Code loads them automatically from `.claude/skills/`.
To update, re-clone the upstream repo and copy the skill folder over.

| Upstream repo | Commit | Skills |
|---|---|---|
| [heygen-com/hyperframes](https://github.com/heygen-com/hyperframes) | f80614c | hyperframes, hyperframes-core, hyperframes-animation, hyperframes-keyframes, hyperframes-creative, hyperframes-audio, hyperframes-cli, hyperframes-registry, media-use, motion-doctrine, product-launch-video, general-video, motion-graphics, cut-the-curve, seam-craft |
| [AbubakrChan/product-launch-motion](https://github.com/AbubakrChan/product-launch-motion) | 951d614 | product-launch-motion |
| [iart-ai/tiktok-video-skills](https://github.com/iart-ai/tiktok-video-skills) | 2a77533 | short-form-video, caption-animation |
| [Jakeschincariol/instagram-agent-skill](https://github.com/Jakeschincariol/instagram-agent-skill) | d03c56b | ig-reel, ig-story, ig-caption, ig-viral, ig-repurpose |
| [emilkowalski/skills](https://github.com/emilkowalski/skills) | e8a175d | animate, animation-vocabulary, apple-design, review-animations (motion-craft guidance for the reels' phone and notification animation) |
| [greensock/gsap-skills](https://github.com/greensock/gsap-skills) (official, MIT) | aed9cfd | gsap-core, gsap-timeline, gsap-plugins, gsap-utils, gsap-performance, gsap-react, gsap-frameworks, gsap-scrolltrigger |
| [remotion-dev/skills](https://github.com/remotion-dev/skills) (official) | 32b241b | remotion-best-practices, remotion-create, remotion-markup, remotion-render, remotion-studio, remotion-captions, remotion-multimedia, remotion-interactivity, remotion-maps, remotion-saas, remotion-docs, remotion-upgrade |
| [CloudAI-X/threejs-skills](https://github.com/CloudAI-X/threejs-skills) (MIT per README) | b1c6230 | threejs-fundamentals, threejs-geometry, threejs-materials, threejs-lighting, threejs-textures, threejs-loaders, threejs-shaders, threejs-postprocessing, threejs-animation, threejs-interaction |
| [Hmzbo/animation-skills](https://github.com/Hmzbo/animation-skills) (MIT) | 5874a4a | manim, motion-canvas, threejs, wgpu-shaders, remotion, gsap-motion (flattened from `skills/<licence>/<name>`; the shared ffmpeg recipe is copied into each skill that cites `shared/ffmpeg/README.md`) |
| [diffusionstudio/lottie](https://github.com/diffusionstudio/lottie) (MIT) | 3c72912 | text-to-lottie (without evals/). It verifies scenes in the repo's own Skia player app: `npx degit diffusionstudio/lottie <dir>` when needed |

Each skill keeps its upstream LICENSE terms. Engines with their own terms: Remotion is source-available and needs a paid company license above three people; GSAP and all its plugins are free, including commercial use.

The video engine for this repo's reels is still HyperFrames. The GSAP and Three.js skills feed directly into it (timelines, PBR materials, lighting, post-processing). Remotion, Manim, Motion Canvas, wgpu and Lottie are available when a piece calls for them.

## Removed (unused for reels and posts)

- From emilkowalski/skills: animate-expo, ask-sonner, break-ui, emil-design-eng, find-animation-opportunities, improve-animations, mobile-native, pick-ui-library, prototype, write-swift (web and app UI development, not video).
- From heygen-com/hyperframes: changelog-video, pr-to-video, talking-head-recut, embedded-captions, captions-overlay, faceless-explainer, slideshow, music-to-video, remotion-to-hyperframes, figma, hyperframes-studio (formats and tools this repo doesn't use), oversized-cursor (no cursors in Wystak reels).
- nolangz/pixel2motion (redraws logos as SVG; the brand rule is to use the supplied files) and echris6/motion-video-kit's business-motion-film (built on AI-generated footage).

They remain in git history if needed.

## Considered and left out

- **video-shotcraft**: built on Remotion, overlaps with the official Remotion skills.
- **onetake**: PolyForm Noncommercial license, so it can't be used for a commercial launch video.
- **OpenMontage**: a 92 MB standalone production system that overlaps with HyperFrames.
- **guizang-product-video-skill**: AGPL, written in Chinese, and overlaps with product-launch-video.
- **gooseworks-ai/gooseworks-ads-skills** (render-ios-lockscreen, notification-flood-ad): not reachable — the repo is private or no longer exists (anonymous clone refused). The public gooseworks-ai/gooseworks skills (goose-ads, goose-video and others) are front-ends to GooseWorks' paid, credit-billed cloud service, so they were not installed.
