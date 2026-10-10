# Wystak palm reveal: video-generation prompts

Use with an image-to-video model that accepts a first and a last frame (for example Runway, Kling, Luma or Veo). Give each segment its two storyboard frames from `storyboard/frames/`. Keep the aspect ratio square (1:1). For 9:16, extend the sky and garden first, never stretch the frames.

The logo must come from the supplied file. Use the model for segments 1 to 3 (the trees). Build segments 4 and 5 in compositing from the layered logo, or use the model there only for the motion and replace the logo with the file.

## Master prompt (one continuous shot, about 10 s)

> Photorealistic, locked-off eye-level shot of a sunny seaside garden on the Indian coast: blue sky, calm ocean horizon, flowering hedges, two white fountains, red benches, a few visitors photographing four tall palm trees whose crossing trunks form a W. Hard natural daylight from the upper left, restrained colour, real film texture. Camera does not move. Over ten seconds the palms perform one smooth, physically believable transformation:
>
> - a breeze bends them;
> - the crossing inner trunks slide apart until the crossing climbs to the top and becomes a peak;
> - the trunks straighten and thicken;
> - a deep navy lacquer climbs each trunk from the roots, ring by ring;
> - the fronds fold up and retract into rounded tips;
> - the trunks settle into a solid navy W, standing in the hedge with the visitors in front of it.
>
> Then three loyalty passes (navy, purple, teal) fan out from behind the W's right side and the shot holds still on the finished mark. No glow, no particles, no sparkles, no text, no extra objects. The people, fountains, hedges, horizon and light stay exactly the same throughout.

**Negative prompt.** Cartoon, plastic trees, morphing blobs, melting, glow, bloom, lens flare, particles, magic dust, neon outline, extra cards, extra letters, text, watermark, logo distortion, camera shake, cut, zoom, colour shift, oversaturation, duplicated people, people changing.

## Segment prompts (first frame → last frame)

**Segment 1 (frame 1 → frame 2), 1.6 s.**

> Locked-off shot. A light sea breeze passes through four palm crowns; the trunks flex slowly: the two outer palms lean slightly outward, the two inner crossing palms dip toward each other, and the curves deepen. The roots stay fixed. Fronds flutter naturally, a beat behind the trunks. Fountains keep running; visitors keep their positions with small natural movement. Photorealistic, no other change.

**Segment 2 (frame 2 → frame 3), 2.2 s.**

> Locked-off shot. The two crossing palm trunks slide along each other so the crossing point rises to the top and becomes a peak; all four trunks straighten into the four strokes of a W and grow thicker. The bark rings tighten and smooth while a deep navy lacquer climbs each trunk from the ground, ring by ring, as if the wood is turning into a polished material. The fronds begin folding upward like closing umbrellas. Smooth, continuous, physically convincing motion; no glow or particles; the garden, sea, fountains and people do not change.

**Segment 3 (frame 3 → frame 4), 1.2 s.**

> Locked-off shot. The folded fronds retract into the tips of the strokes, which round off into soft terminals; the strokes swell to full width and the right-hand trunk flattens into a tall rounded slab, completing a solid navy W with a smooth satin finish. It settles with one small damped give. The hedge tops and the visitors stay in front of its base. No glow, no text.

**Segment 4 (frame 4 → frame 5), 1.2 s (prefer compositing).**

> Locked-off shot. A ticket icon presses up from the surface of the tall right-hand stroke, revealing it as a navy pass. A purple pass, then a teal pass, swing out from behind it around a pivot at the W's foot and decelerate into a fan, each casting a soft shadow on the one behind. Clean premium product motion; no extra cards, no text.

**Segment 5 (frame 5 → frame 6), 2.2 s (compositing, exact logo).**

> Locked-off shot. The passes complete their fan into the exact final logo and everything holds still. Only the fountains, the sea and the visitors move slightly.

## Shot settings

- **Duration:** about 10 s; the hold on frame 6 is at least 2 s.
- **Frame rate:** 24 fps (film) or 30 fps (social).
- **Motion strength:** low to medium for segments 1–3. The look should stay photographic.
- **Seeds:** fix one seed per segment so retries stay comparable.
