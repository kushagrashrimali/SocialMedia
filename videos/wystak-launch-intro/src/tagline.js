/* Tagline: word by word, each one resolving out of soft focus as it rises a few pixels. */
window.WYSTAK = window.WYSTAK || {};
WYSTAK.tagline = function (tl, T) {
  const G = T.tagline;
  tl.fromTo("#tagline .w", { opacity: 0, y: 14, filter: "blur(8px)" },
    { opacity: 1, y: 0, filter: "blur(0px)", duration: G.wordDur, ease: "power2.out", stagger: G.wordGap }, G.at);
};
