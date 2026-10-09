"""WYSTAK LinkedIn post: would you know if a best regular stopped coming? One image, 1080x1350.

Collage-style: a bold navy ground, a crumpled-paper panel holding the regulars list, a hand-drawn aqua ellipse
around one word and a small italic serif line. Type: Inter Black, DM Serif Display italic, Inter.
"""
import sys, pathlib
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent.parent / "instagram" / "carousels" / "_common"))
from common import RESET, render

CSS = RESET + """
@font-face{font-family:I;src:url(assets/inter-latin-500-normal.woff2);font-weight:500}
@font-face{font-family:I;src:url(assets/inter-latin-600-normal.woff2);font-weight:600}
@font-face{font-family:I;src:url(assets/inter-latin-900-normal.woff2);font-weight:900}
@font-face{font-family:DS;src:url(assets/dm-serif-display-latin-400-italic.woff2);font-style:italic}
:root{--ink:#0b1530;--aqua:#5fd4cf;--violet:#6b2ba6}
body{font-family:I,sans-serif;color:#fff}
.slide{background:radial-gradient(90% 65% at 30% 25%,#2250b4 0%,#12388a 45%,#0a2860 100%)}
.grain{opacity:.16;mix-blend-mode:soft-light}
.vig{box-shadow:inset 0 0 200px rgba(0,10,45,.5)}
.h{font-weight:900;letter-spacing:-.045em;word-spacing:.06em;line-height:1.1;white-space:nowrap;font-size:104px}
.it{font-family:DS,serif;font-style:italic}
"""

NAMES = [("Isha", "3 days ago", "14"), ("Dev", "5 days ago", "9"), ("Nisha", "8 days ago", "11"), ("Tara", "yesterday", "17")]
rows = ''.join(f'''<div style="display:flex;align-items:center;height:68px;border-bottom:2px solid rgba(11,21,48,.14);font-size:32px;font-weight:600">
  <div style="flex:1.2">{n}</div><div style="flex:1.2;font-weight:500;color:#4a5476">{d}</div><div style="flex:.4;text-align:right;font-weight:900">{v}</div></div>''' for n, d, v in NAMES)

slides = [f'''<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head><body>
<div class="slide">
  <svg width="0" height="0"><defs>
    <filter id="crumple" x="0" y="0" width="100%" height="100%"><feTurbulence type="fractalNoise" baseFrequency=".011 .016" numOctaves="4" seed="7" result="n"/>
      <feDiffuseLighting in="n" lighting-color="#fffdf6" surfaceScale="2.6" diffuseConstant="1.05"><feDistantLight azimuth="50" elevation="64"/></feDiffuseLighting></filter></defs></svg>

  <!-- headline -->
  <div class="abs" style="left:96px;top:96px">
    <div class="h">would you know</div>
    <div class="h">if your best</div>
    <div class="h">regular</div>
    <div class="h" style="position:relative;display:inline-block">stopped
      <svg class="abs" style="left:-30px;top:-12px;overflow:visible" width="520" height="150" preserveAspectRatio="none" viewBox="0 0 470 150" fill="none" stroke="#5fd4cf" stroke-width="8" stroke-linecap="round"><path d="M60 30 C130 -4 380 -2 440 56 C486 102 350 146 200 144 C70 142 -8 104 20 58 C34 34 80 20 130 16"/></svg></div>
    <div class="h" style="display:inline-block;margin-left:24px">coming?</div>
  </div>
  <div class="it abs" style="left:100px;top:600px;font-size:38px;line-height:1.3;color:rgba(255,255,255,.88);width:860px">the till shows the best-seller.<br>it does not show the regular who went quiet.</div>

  <!-- crumpled-paper panel -->
  <div class="abs" style="left:96px;top:742px;width:700px;height:440px;transform:rotate(-2.2deg);filter:drop-shadow(0 34px 34px rgba(0,10,45,.55))">
    <div style="position:absolute;inset:0;border-radius:6px;overflow:hidden;color:var(--ink)">
      <svg class="abs" style="left:0;top:0" width="700" height="440"><rect width="700" height="440" filter="url(#crumple)"/></svg>
      <div class="abs" style="left:40px;right:40px;top:26px">
        <div style="display:flex;justify-content:space-between;font-weight:600;font-size:19px;letter-spacing:.2em;color:#4a5476;padding-bottom:12px;border-bottom:3px solid var(--ink)"><span>BEAN THEORY · REGULARS</span><span>VISITS</span></div>
        {rows}
        <div style="display:flex;align-items:center;height:68px;font-size:32px;font-weight:600;opacity:.4"><div style="flex:1.2">Kabir</div><div style="flex:1.2;font-weight:500">26 days ago</div><div style="flex:.4;text-align:right;font-weight:900">6</div></div>
      </div></div></div>
  <div class="abs" style="left:620px;top:1150px;transform:rotate(-4deg);font-family:DS;font-style:italic;font-size:44px;color:var(--aqua);white-space:nowrap">quietly gone.</div>

  <!-- footer -->
  <div class="abs" style="left:96px;bottom:70px;height:62px;padding:0 30px;border-radius:31px;background:#fff;display:flex;align-items:center"><img src="assets/logo-wordmark.png" style="height:30px"></div>
  <div class="abs" style="right:96px;bottom:90px"><img src="assets/logo-tagline.png" style="height:17px;filter:brightness(0) invert(1);opacity:.85"></div>
  <div class="vig"></div><div class="grain"></div>
</div></body></html>''']

if __name__ == "__main__":
    render(slides, HERE, "wystak-linkedin-regulars", sys.argv[1:])
