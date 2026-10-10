/* Background: off-white ground, one soft key light that drifts, a faint brand tint that warms in. */
window.WYSTAK = window.WYSTAK || {};
WYSTAK.background = function (tl, T) {
  tl.fromTo(".bg-key", { x: -70, y: 30 }, { x: 70, y: -30, duration: T.duration, ease: "none" }, 0);
  tl.fromTo(".bg-tint", { opacity: 0.35 }, { opacity: 1, duration: 3.0, ease: "sine.inOut" }, 0.4);
  // parallax: the ground moves a fraction of the camera
  tl.fromTo("#bgwrap", { scale: 1.0 }, { scale: 1.012, duration: T.camera.end, ease: "power2.inOut", transformOrigin: "50% 44%" }, 0);
};
