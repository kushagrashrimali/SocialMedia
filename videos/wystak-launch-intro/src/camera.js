/* Camera: one slow push-in that comes fully to rest at T.camera.end, so the last second is a true hold. */
window.WYSTAK = window.WYSTAK || {};
WYSTAK.camera = function (tl, T) {
  const C = T.camera;
  tl.fromTo("#world", { scale: C.from }, { scale: C.to, duration: C.end, ease: "power2.inOut" }, 0);
  tl.set({}, {}, T.duration);   // the timeline runs the full length
};
