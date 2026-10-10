"""Prepare the user's iPhone 17 Pro model for the reel (assets/model/, git-ignored).

Input: the uploaded IPhone17Pro.fbx and the texture folder from "iphoneseries_Textures.rar"
("iphone series_Textures/texture"). Copies the FBX and the four PBR maps the scene uses, and paints the Apple logo
out of every map (brand rule: no real company logos). The display's own wallpaper stays in the maps; the reel draws
its own screen over it (src/phone.js).

usage (from the project folder):
  python3 -I tools/prep_model.py <IPhone17Pro.fbx> "<...>/iphone series_Textures/texture"
"""
import pathlib, shutil, sys
import numpy as np
from PIL import Image

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "assets/model"
LOGO = (815, 1000, 1335, 1545)          # x0, x1, y0, y1 of the logo on the back, in the 2048 maps (found by diffing Roughness)

fbx, tex = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])
OUT.mkdir(parents=True, exist_ok=True)
shutil.copy(fbx, OUT / "iphone17pro.fbx")
x0, x1, y0, y1 = LOGO
for m in ("BaseColor", "Metallic", "Roughness", "Normal"):
    img = Image.open(tex / f"Iphones17Series_Iphone17Pro1_{m}.png")
    a = np.asarray(img).copy()
    ring = np.concatenate([a[y0 - 40:y0, x0:x1].reshape(-1, *a.shape[2:]), a[y1:y1 + 40, x0:x1].reshape(-1, *a.shape[2:])])
    a[y0:y1, x0:x1] = np.median(ring, axis=0)          # fill with the panel's own surrounding value
    Image.fromarray(a, img.mode).save(OUT / f"pro_{m}.png")
    print("wrote", OUT / f"pro_{m}.png")
