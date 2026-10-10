"""WYSTAK pre-launch post 2 (1080x1350): the chat goes on, and the answer is a photo.

Follows post 1 (../prelaunch-billboard-v4, "Soon. Very soon."): same raspberry ground, chat header and type. The reply is
a photo message: the Wystak mark standing in the seaside garden (frame 6 of videos/wystak-palm-reveal).
Run: python3 build.py
"""
import sys, pathlib, importlib.util
HERE = pathlib.Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("v4", HERE.parent / "prelaunch-billboard-v4" / "build.py")
v4 = importlib.util.module_from_spec(spec); spec.loader.exec_module(v4)
v2 = v4.v2

W, H = 1080, 1350
BG, IVORY, GOLD = "#C24366", v4.IVORY, v4.GOLD
sh = v4.shade


def html():
    return f'''<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{{font-family:I;src:url(assets/inter-latin-500-normal.woff2);font-weight:500}}
@font-face{{font-family:I;src:url(assets/inter-latin-700-normal.woff2);font-weight:700}}
@font-face{{font-family:I;src:url(assets/inter-latin-900-normal.woff2);font-weight:900}}
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:{W}px;height:{H}px;overflow:hidden}}
body{{font-family:I,sans-serif;color:{IVORY};
  background:radial-gradient(80% 40% at 10% 0%,rgba(255,255,255,.12) 0%,rgba(255,255,255,0) 100%),
             linear-gradient(180deg,{sh(BG,1.12)} 0%,{BG} 55%,{sh(BG,0.72)} 100%)}}
.abs{{position:absolute}}
.time{{left:0;right:0;top:30px;text-align:center;font-weight:500;font-size:26px;opacity:.75}}
.head{{left:64px;right:64px;top:70px;height:84px;display:flex;align-items:center;gap:26px}}
.av{{width:80px;height:80px;border-radius:50%;background:#fff;display:flex;align-items:center;justify-content:center;box-shadow:0 6px 18px rgba(0,0,0,.25)}}
.name{{font-weight:700;font-size:36px;line-height:1.1}} .on{{font-weight:500;font-size:24px;color:{v4.MINT}}}
.icons{{margin-left:auto;display:flex;gap:44px;align-items:center}}
.b{{position:absolute;border-radius:26px;font-weight:500;font-size:36px;line-height:1.2;box-shadow:0 14px 30px rgba(60,0,20,.30)}}
.b small{{display:flex;justify-content:flex-end;align-items:center;gap:8px;font-size:19px;margin-top:6px;opacity:.6}}
.in{{left:64px;top:186px;padding:20px 28px 18px;background:#fff;color:#141833;border-bottom-left-radius:8px}}
.ph{{right:64px;top:322px;padding:12px;background:#CDEFE3;color:#0D2A22;border-bottom-right-radius:8px}}
.ph img{{display:block;width:620px;height:620px;object-fit:cover;object-position:50% 40%;border-radius:18px}}
.ph small{{padding:8px 8px 2px}}
.hl{{left:64px;top:1050px;font-weight:900;font-size:108px;line-height:.98;letter-spacing:-.055em;white-space:nowrap}}
.hl .g{{color:{GOLD}}}
</style></head><body>
<div class="abs time">12:48 PM</div>
<div class="abs head">{v4.BACK}<div class="av"><img src="assets/logo-mark.png" style="width:58px"></div>
  <div><div class="name">Wystak</div><div class="on">online</div></div>
  <div class="icons">{v4.PHONE}{v4.VIDEO}{v4.DOTS}</div></div>
<div class="b in">How soon is soon?<small>12:48 PM</small></div>
<div class="b ph"><img src="assets/garden.jpg"><small>12:48 PM {v4.TICKS}</small></div>
<div class="abs hl">Closer than<br><span class="g">you think.</span></div>
</body></html>'''


if __name__ == "__main__":
    out = HERE / "slides"; out.mkdir(exist_ok=True)
    v2.HERE = HERE; v2.H = H
    v2.render(html(), out / "wystak-prelaunch-post-2.png")
    print("ok")
