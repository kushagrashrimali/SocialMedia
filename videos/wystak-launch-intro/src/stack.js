/* Stacking: four glass passes deal in from depth and fan behind the mark (stack), gather into one neat
   stack (organise), then a single light runs down the deck (access). Smooth and physical; no bounce. */
window.WYSTAK = window.WYSTAK || {};
WYSTAK.FAN = [   // back to front: where each pass lands as it deals in
  { x: -150, y: 40, r: -12 }, { x: -52, y: 10, r: -4 }, { x: 52, y: 10, r: 4 }, { x: 150, y: 40, r: 12 }];
WYSTAK.STACK = [ // where they settle: one stack, the back passes peeking above the front
  { x: 0, y: -72, r: 0, s: 0.91 }, { x: 0, y: -48, r: 0, s: 0.94 }, { x: 0, y: -24, r: 0, s: 0.97 }, { x: 0, y: 0, r: 0, s: 1 }];
WYSTAK.stack = function (tl, T) {
  const K = T.stack, cards = document.querySelectorAll("#deck .glass");
  cards.forEach((c, i) => {
    const f = WYSTAK.FAN[i], s = WYSTAK.STACK[i], t = K.inAt + i * K.gap;
    tl.fromTo(c, { opacity: 0, x: f.x + (i < 2 ? -320 : 320), y: f.y + 420, z: -520, rotation: f.r * 2.4, rotationX: 28, scale: 1 },
      { opacity: 1, x: f.x, y: f.y, z: 0, rotation: f.r, rotationX: 0, duration: K.inDur, ease: "expo.out" }, t);
    // organise: the fan closes into a single stack, the front pass first
    tl.to(c, { x: s.x, y: s.y, rotation: s.r, scale: s.s, z: -(3 - i) * 18, duration: K.organiseDur, ease: "power3.inOut" }, K.organiseAt + (3 - i) * 0.05);
    // access: one light travels down the deck, back to front
    tl.fromTo(c.querySelector(".sw"), { xPercent: -180 }, { xPercent: 460, duration: K.accessDur, ease: "power2.inOut" }, K.accessAt + i * 0.07);
  });
  tl.fromTo("#deck", { y: 10 }, { y: 0, duration: K.organiseDur + 1.2, ease: "power2.out" }, K.organiseAt);
};
