/* Glass and refraction: the cover pass lifts away and clears; a light sweep travels across it;
   two thin sheets drift in behind the lockup with slow parallax. */
window.WYSTAK = window.WYSTAK || {};
WYSTAK.glass = function (tl, T) {
  const P = T.pane;
  // the cover pass tips back and rises out of the way while its frost clears
  tl.fromTo("#pane", { y: 0, z: 0, rotationX: 0, rotationY: 0 },
    { y: -190, z: -320, rotationX: 18, rotationY: -7, duration: P.liftDur, ease: "power2.inOut" }, P.lift);
  tl.fromTo("#pane", { "--frost": T.cover.frost + "px" }, { "--frost": "0px", duration: P.frostOut, ease: "power1.inOut" }, P.lift);
  tl.fromTo("#pane", { opacity: 1 }, { opacity: 0, duration: P.fadeDur, ease: "power1.in" }, P.fadeAt);
  tl.fromTo("#pane .sw", { xPercent: -180 }, { xPercent: 460, duration: T.sweep1.dur, ease: "power2.inOut" }, T.sweep1.at);

  // thin sheets: barely there, they only catch the light at their edges
  const S = T.sheets;
  tl.fromTo("#sheetA", { opacity: 0, y: 60, rotation: -9 }, { opacity: 0.75, y: 0, rotation: -7, duration: S.dur, ease: "power2.out" }, S.at);
  tl.fromTo("#sheetB", { opacity: 0, y: 90, rotation: 7 }, { opacity: 0.75, y: 0, rotation: 5, duration: S.dur, ease: "power2.out" }, S.at + 0.25);
  tl.to("#sheetA", { y: -26, rotation: -5.5, duration: S.drift, ease: "sine.inOut" }, S.at + S.dur);
  tl.to("#sheetB", { y: -14, rotation: 4, duration: S.drift, ease: "sine.inOut" }, S.at + S.dur + 0.25);
};
