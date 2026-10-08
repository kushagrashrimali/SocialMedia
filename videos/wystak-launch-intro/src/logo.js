/* Logo reveal: the official mark and wordmark are never altered: only the whole lockup moves (a settle of
   ~1%) and the glass in front of it clears. At t=0 it already sits in place, softly seen through the cover pass. */
window.WYSTAK = window.WYSTAK || {};
WYSTAK.logo = function (tl, T) {
  tl.fromTo("#lockup", { scale: 1.014, y: 6 }, { scale: 1, y: 0, duration: T.logo.settleDur, ease: "power2.out", transformOrigin: "50% 46%" }, T.logo.settleAt);
  tl.fromTo(".mark-shadow", { opacity: 0.35, scaleX: 0.9 }, { opacity: 1, scaleX: 1, duration: T.logo.settleDur, ease: "power2.out" }, T.logo.settleAt);
};
