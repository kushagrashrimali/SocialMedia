"""Build index.html for the loyalty-evolution reel (v2 script, 51.39s).

Inputs: storyboard/base.css (fonts + phone UI), storyboard/icons.json (simple-icons paths, CC0),
assets/words.json (forced-aligned voice). Captions are generated from the word timings.
usage (from the project folder): python3 storyboard/build_index.py
then re-apply the voice carve on the bed (hyperframes-audio carve.mjs --bed bed --voice vo --strength 0.6).
"""
import json, pathlib

HERE = pathlib.Path(__file__).resolve().parent
P = HERE.parent
DUR = 51.39
END_T = 45.55  # end card starts; no running captions after this
BASE = (HERE / "base.css").read_text()
ICONS = json.load(open(HERE / "icons.json"))
W = json.load(open(P / "assets/words.json"))
W = W["words"] if isinstance(W, dict) else W

# ---------------------------------------------------------------- pieces
APPS = {  # name: (label, background, glyph colour)
    "whatsapp": ("WhatsApp", "#25D366", "#fff"),
    "instagram": ("Instagram", "linear-gradient(45deg,#f9b233 0%,#e4405f 45%,#c13584 70%,#5851db 100%)", "#fff"),
    "googlemessages": ("Messages", "#1a73e8", "#fff"),
    "facebook": ("Facebook", "#0866ff", "#fff"),
    "telegram": ("Telegram", "#26a5e4", "#fff"),
    "gmail": ("Gmail", "#ffffff", "#ea4335"),
    "youtube": ("YouTube", "#ff0000", "#fff"),
    "snapchat": ("Snapchat", "#fffc00", "#111"),
    "x": ("X", "#000000", "#fff"),
}


def icon(name, size, extra_style="", id_=""):
    label, bg, fg = APPS[name]
    g = int(size * 0.56)
    idattr = f' id="{id_}"' if id_ else ""
    return (f'<div class="app"{idattr} style="width:{size}px;height:{size}px;border-radius:{int(size*0.23)}px;background:{bg};{extra_style}">'
            f'<svg width="{g}" height="{g}" viewBox="0 0 24 24" fill="{fg}"><path d="{ICONS[name]}"/></svg></div>')


def lock(extra=""):
    return ('<div class="screen lock"><div class="island"></div><div class="date">Tuesday, 7 October</div>'
            f'<div class="time">9:42</div>{extra}<div class="bar"></div></div>')


def aroma(id_, qr_id, style=""):
    return f'''<div class="aroma" id="{id_}" style="{style}">
  <div class="ar-hd"><div class="ar-mono">a</div><div class="ar-nm">CAFE AROMA</div><div class="ar-pt"><span>POINTS</span>132</div></div>
  <div class="ar-strip"><img src="assets/stills/latte-pour.jpg" alt=""></div>
  <div class="ar-row"><div><span>MEMBER</span>Aarav M.</div><div><span>TIER</span>Gold</div><div><span>NEXT REWARD</span>at 150</div></div>
  <div class="ar-qr"><div id="{qr_id}"></div></div>
</div>'''


WALLET_GLYPH = ('<svg width="46" height="38" viewBox="0 0 46 38"><rect x="1" y="1" width="44" height="36" rx="7" fill="#fff"/>'
                '<rect x="5" y="6" width="36" height="8" rx="3" fill="#3d8bfd"/><rect x="5" y="11" width="36" height="8" rx="3" fill="#ffb300"/>'
                '<rect x="5" y="16" width="36" height="8" rx="3" fill="#ef4444"/><rect x="5" y="21" width="36" height="12" rx="3" fill="#22c55e"/></svg>')
GW_GLYPH = ('<svg width="46" height="38" viewBox="0 0 46 38"><path d="M4 10 Q4 4 10 4 H36 Q42 4 42 10 V12 H4Z" fill="#4285f4"/>'
            '<path d="M4 12 H42 V18 H4Z" fill="#ea4335"/><path d="M4 18 H42 V24 H4Z" fill="#fbbc04"/>'
            '<path d="M4 24 H42 V28 Q42 34 36 34 H10 Q4 34 4 28Z" fill="#34a853"/></svg>')


def badges(id_, top, scale=1.0, style=""):
    apple = (f'<div class="badge"><svg width="34" height="40" viewBox="0 0 24 24" fill="#fff"><path d="{ICONS["apple"]}"/></svg>{WALLET_GLYPH}'
             '<div class="bt"><span>Add to</span>Apple Wallet</div></div>')
    google = f'<div class="badge">{GW_GLYPH}<div class="bt"><span>Add to</span>Google Wallet</div></div>'
    return (f'<div class="badges" id="{id_}" style="top:{top}px;transform:scale({scale});{style}">{apple}{google}</div>')


def check():
    return '<svg width="30" height="30" viewBox="0 0 30 30"><circle cx="15" cy="15" r="15" fill="#06737c"/><path d="M8 15.5 L13 20.5 L22 10.5" fill="none" stroke="#fff" stroke-width="3.4" stroke-linecap="round" stroke-linejoin="round"/></svg>'


# ---------------------------------------------------------------- captions
def caption_groups():
    groups, cur = [], []
    for w in W:
        if w["start"] >= END_T:
            break
        cur.append(w)
        t = w["text"] if "text" in w else w["word"]
        if t[-1] in ".?," or len(cur) == 5:
            groups.append(cur); cur = []
    if cur:
        groups.append(cur)
    out = []
    for i, g in enumerate(groups):
        s = g[0]["start"] - 0.06
        nxt = groups[i + 1][0]["start"] - 0.06 if i + 1 < len(groups) else END_T
        e = min(nxt, g[-1]["end"] + 0.6)
        out.append((s, e, g))
    return out


CAPS = caption_groups()
cap_html = "\n".join(
    f'<div class="cap" id="cap{i}"><div class="cap-in">' + " ".join(
        f'<span class="cw" id="cw{i}_{j}">{(w.get("text") or w.get("word"))}</span>' for j, w in enumerate(g)) + "</div></div>"
    for i, (s, e, g) in enumerate(CAPS))
cap_js = json.dumps([[round(s, 3), round(e, 3), [[round(w["start"], 3), round(w["end"], 3)] for w in g]] for s, e, g in CAPS])

# ---------------------------------------------------------------- scenes
grid = "".join(
    f'<div class="cell" id="g{i}">{icon(n, 190)}<div class="badge-n">{b}</div><div class="nm">{APPS[n][0]}</div></div>' if b else
    f'<div class="cell" id="g{i}">{icon(n, 190)}<div class="nm">{APPS[n][0]}</div></div>'
    for i, (n, b) in enumerate([("whatsapp", "3"), ("instagram", "9+"), ("googlemessages", "12"), ("facebook", ""), ("telegram", "2"),
                                ("gmail", "24"), ("youtube", ""), ("snapchat", "5"), ("x", "")]))

chats = [("Family", "Mummy: Call me when free", "#f59e0b", "F", "4"), ("Office team", "Ravi: Deck is shared", "#0ea5e9", "O", "18"),
         ("Delivery updates", "Your order is on the way", "#22c55e", "D", "2"), ("Cafe Aroma", "You have points waiting for you", "#2a170d", "a", "1"),
         ("Bank alerts", "A/c XX21 debited", "#64748b", "B", "6"), ("Gym buddies", "Neha: 6 am tomorrow?", "#a855f7", "G", "31"),
         ("Society group", "Water supply notice", "#ef4444", "S", "57")]
chat_rows = "".join(
    f'<div class="crow{" hot" if n == "Cafe Aroma" else ""}"><div class="cav" style="background:{c}">{l}</div><div class="cb"><div class="cn">{n}</div>'
    f'<div class="cm">{m}</div></div><div class="cu">{u}</div></div>' for n, m, c, l, u in chats)

lock_icons = "".join(icon(n, 120, f"position:absolute;left:{x}px;top:{y}px", f"li{i}") for i, (n, x, y) in enumerate(
    [("whatsapp", 110, 380), ("instagram", 860, 300), ("googlemessages", 70, 900), ("gmail", 880, 820), ("telegram", 150, 1250), ("snapchat", 830, 1300)]))

HTML = f'''<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=1080, height=1920">
    <script src="assets/vendor/gsap.min.js"></script>
    <style>
{BASE}
      /* ---------- v2 ---------- */
      .ground-bright {{ background: linear-gradient(165deg, #fffaf3 0%, #f6eee6 45%, #ece6f7 100%); }}
      .ground-bright::after {{ content: ""; position: absolute; left: 190px; right: 190px; top: 1180px; height: 120px; border-radius: 50%; background: rgba(60, 40, 30, 0.16); filter: blur(30px); }}
      .ground-bright .phone {{ box-shadow: 0 0 0 2px #2c2833, 0 60px 110px -40px rgba(60, 35, 20, 0.55); }}
      .media.still {{ transform-origin: 50% 50%; }}
      .app {{ position: relative; display: flex; align-items: center; justify-content: center; box-shadow: 0 18px 40px -18px rgba(30, 20, 40, 0.45); }}
      .shade-b {{ position: absolute; left: 0; right: 0; bottom: 0; height: 760px; background: linear-gradient(to bottom, rgba(11, 4, 16, 0), rgba(11, 4, 16, 0.55)); }}

      /* captions */
      .cap {{ position: absolute; left: 60px; right: 60px; top: 1400px; display: flex; justify-content: center; opacity: 0; z-index: 60; }}
      .cap-in {{ max-width: 960px; padding: 16px 34px 20px; border-radius: 26px; background: rgba(16, 8, 24, 0.8); text-align: center; font-family: "Manrope", sans-serif; font-weight: 800; font-size: 60px; line-height: 1.18; letter-spacing: -0.01em; color: #fff; }}
      .cw {{ display: inline-block; opacity: 0.45; }}

      /* premium Cafe Aroma pass */
      .aroma {{ position: absolute; left: 18px; right: 18px; height: 560px; border-radius: 26px; overflow: hidden; color: #f3e3c0;
        background: linear-gradient(155deg, #4a2c1b 0%, #2a170d 46%, #160b06 100%);
        box-shadow: inset 0 0 0 1.5px rgba(227, 194, 126, 0.55), 0 24px 50px -20px rgba(30, 12, 4, 0.7); }}
      .ar-hd {{ position: absolute; left: 22px; right: 22px; top: 20px; height: 62px; display: flex; align-items: center; gap: 12px; }}
      .ar-mono {{ width: 54px; height: 54px; border-radius: 50%; border: 2px solid #e3c27e; display: flex; align-items: center; justify-content: center; font-family: "Archivo", sans-serif; font-style: italic; font-weight: 600; font-size: 34px; color: #e3c27e; padding-bottom: 6px; }}
      .ar-nm {{ flex: 1; font-family: "Archivo", sans-serif; font-weight: 600; font-size: 20px; letter-spacing: 0.24em; color: #f0d79f; }}
      .ar-pt {{ text-align: right; font-family: "IBM Plex Mono", monospace; font-weight: 600; font-size: 40px; line-height: 1; color: #fff3d6; }}
      .ar-pt span, .ar-row span {{ display: block; font-family: "Manrope", sans-serif; font-weight: 700; font-size: 12px; letter-spacing: 0.2em; color: #c9a467; margin-bottom: 4px; }}
      .ar-strip {{ position: absolute; left: 0; right: 0; top: 96px; height: 150px; overflow: hidden; border-top: 1px solid rgba(227, 194, 126, 0.4); border-bottom: 1px solid rgba(227, 194, 126, 0.4); }}
      .ar-strip img {{ width: 100%; height: 100%; object-fit: cover; object-position: 50% 58%; display: block; }}
      .ar-row {{ position: absolute; left: 22px; right: 22px; top: 266px; display: flex; justify-content: space-between; font-weight: 700; font-size: 21px; color: #fff3d6; }}
      .ar-qr {{ position: absolute; left: 50%; bottom: 26px; width: 166px; height: 166px; margin-left: -83px; border-radius: 16px; background: #fffaf0; padding: 12px; }}

      /* wallet badges (drawn) */
      .badges {{ position: absolute; left: 0; right: 0; display: flex; justify-content: center; gap: 34px; transform-origin: 50% 50%; z-index: 40; }}
      .badge {{ width: 400px; height: 112px; border-radius: 22px; background: #000; border: 2px solid #a6a6a6; display: flex; align-items: center; gap: 14px; padding: 0 22px; color: #fff; box-shadow: 0 20px 40px -20px rgba(0, 0, 0, 0.6); }}
      .badge .bt {{ font-family: "Manrope", sans-serif; font-weight: 700; font-size: 33px; line-height: 1.05; letter-spacing: -0.01em; white-space: nowrap; }}
      .badge .bt span {{ display: block; font-weight: 600; font-size: 19px; letter-spacing: 0.02em; opacity: 0.9; }}

      /* data card */
      .crm {{ position: absolute; left: 130px; right: 130px; top: 330px; border-radius: 36px; background: rgba(255, 255, 255, 0.95); color: var(--aub); padding: 34px 40px 18px; box-shadow: 0 40px 80px -30px rgba(0, 0, 0, 0.6); }}
      .crm .who {{ display: flex; align-items: center; gap: 20px; padding-bottom: 22px; border-bottom: 2px solid #ece8f1; }}
      .crm .av {{ width: 84px; height: 84px; border-radius: 50%; background: linear-gradient(140deg, #7c3aed, #06737c); color: #fff; font-weight: 800; font-size: 38px; display: flex; align-items: center; justify-content: center; }}
      .crm .nm {{ font-weight: 800; font-size: 38px; }}
      .crm .sb {{ font-weight: 600; font-size: 22px; color: var(--muted-l); letter-spacing: 0.08em; text-transform: uppercase; margin-top: 2px; }}
      .crm .row {{ display: flex; justify-content: space-between; padding: 20px 0; border-bottom: 1px solid #ece8f1; font-size: 30px; }}
      .crm .row:last-child {{ border-bottom: none; }}
      .crm .row span {{ color: var(--muted-l); font-weight: 600; }}
      .crm .row b {{ font-weight: 800; }}
      .tag {{ position: absolute; left: 70px; top: 1190px; display: flex; align-items: center; gap: 16px; padding: 18px 30px 18px 20px; border-radius: 40px; background: rgba(255, 255, 255, 0.95); color: var(--aub); font-weight: 800; font-size: 34px; box-shadow: 0 20px 40px -20px rgba(0, 0, 0, 0.6); }}

      /* app grid */
      .grid {{ position: absolute; left: 90px; right: 90px; top: 250px; display: grid; grid-template-columns: repeat(3, 1fr); row-gap: 70px; justify-items: center; }}
      .cell {{ position: relative; display: flex; flex-direction: column; align-items: center; gap: 16px; }}
      .cell .nm {{ font-weight: 700; font-size: 30px; color: var(--aub); }}
      .badge-n {{ position: absolute; right: -18px; top: -18px; min-width: 62px; height: 62px; padding: 0 14px; border-radius: 31px; background: #ff3b30; color: #fff; font-weight: 800; font-size: 30px; display: flex; align-items: center; justify-content: center; border: 4px solid #fbf6ef; }}

      /* chat list */
      .crow {{ display: flex; align-items: center; gap: 16px; padding: 16px 22px; border-bottom: 1px solid #e7e3ec; background: #fff; }}
      .crow.hot {{ background: #fff7e8; }}
      .cav {{ width: 62px; height: 62px; border-radius: 50%; flex: none; color: #fff; font-weight: 800; font-size: 28px; display: flex; align-items: center; justify-content: center; }}
      .cb {{ flex: 1; min-width: 0; }}
      .cn {{ font-weight: 800; font-size: 22px; color: var(--aub); }}
      .cm {{ font-weight: 500; font-size: 18px; color: var(--muted-l); white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }}
      .cu {{ min-width: 34px; height: 34px; padding: 0 8px; border-radius: 17px; background: #15803d; color: #fff; font-weight: 800; font-size: 17px; display: flex; align-items: center; justify-content: center; }}

      /* floating fragments ("everywhere") */
      .frag {{ position: absolute; border-radius: 28px; background: #fff; color: var(--aub); padding: 22px 26px; font-weight: 600; font-size: 28px; line-height: 1.3; box-shadow: 0 26px 50px -24px rgba(40, 20, 50, 0.45); }}
      .frag small {{ display: block; font-weight: 800; font-size: 19px; letter-spacing: 0.12em; color: var(--muted-l); margin-bottom: 6px; }}

      /* end card */
      .end-tag {{ position: absolute; left: 0; right: 0; text-align: center; font-family: "Archivo Black", sans-serif; font-size: 76px; letter-spacing: 0.01em; color: var(--aub); line-height: 1; }}
      .end-tag.acc {{ color: var(--violet); }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{DUR}" data-width="1080" data-height="1920">

      <!-- ===== "India didn't stop rewarding customers." ===== -->
      <div id="s01" class="scene clip ground-void" data-start="0" data-duration="2.7" data-track-index="1">
        <img id="m-interior" class="media still" src="assets/stills/cafe-interior.jpg" alt="">
        <div id="s01-fade" style="position:absolute;inset:0;background:#0b0410"></div>
      </div>
      <!-- ===== "Your customers just stopped noticing." ===== -->
      <div id="s02" class="scene clip ground-void" data-start="2.7" data-duration="2.55" data-track-index="1">
        <img id="m-cup" class="media still" src="assets/stills/cappuccino-hand.jpg" alt="">
        <div id="s02-n" class="notif" style="left:110px;right:110px;top:420px;padding:22px 26px">
          <div class="ic" style="background:#64748b">S</div>
          <div class="nb"><div class="t1">Messages <span>2d ago</span></div><div class="t2">Dear customer, you have earned reward points. T&amp;C apply.</div></div>
        </div>
      </div>
      <!-- ===== "Every counter started collecting data, not just cash." ===== -->
      <div id="s03" class="scene clip ground-void" data-start="5.25" data-duration="3.8" data-track-index="1">
        <img id="m-pos" class="media still" src="assets/stills/pos-counter.jpg" alt="">
        <div class="crm" id="s03-card">
          <div class="who"><div class="av">A</div><div><div class="nm">Aarav Mehta</div><div class="sb">Regular customer</div></div></div>
          <div class="row" id="r1"><span>Visits</span><b>12</b></div>
          <div class="row" id="r2"><span>Usual order</span><b>Cold brew, no sugar</b></div>
          <div class="row" id="r3"><span>Birthday</span><b>14 October</b></div>
          <div class="row" id="r4"><span>Last visit</span><b>Tuesday</b></div>
        </div>
      </div>
      <!-- ===== "Businesses learned to remember." ===== -->
      <div id="s04" class="scene clip ground-void" data-start="9.05" data-duration="2.15" data-track-index="1">
        <img id="m-desk" class="media still" src="assets/stills/boutique-desk.jpg" alt="">
      </div>
      <!-- ===== "Every visit. Every purchase. Every preference." ===== -->
      <div id="s05a" class="scene clip ground-void" data-start="11.2" data-duration="1.2" data-track-index="1">
        <img id="m-wcounter" class="media still" src="assets/stills/woman-counter.jpg" alt="">
        <div class="tag">{check()}Visit logged</div>
      </div>
      <div id="s05b" class="scene clip ground-void" data-start="12.4" data-duration="1.15" data-track-index="1">
        <img id="m-pour" class="media still" src="assets/stills/latte-pour.jpg" alt="">
        <div class="tag">{check()}Order: Flat white</div>
      </div>
      <div id="s05c" class="scene clip ground-void" data-start="13.55" data-duration="1.25" data-track-index="1">
        <img id="m-pour2" class="media still" src="assets/stills/flatwhite-pour.jpg" alt="">
        <div class="tag">{check()}Prefers oat milk</div>
      </div>
      <!-- ===== "And social media made staying connected effortless." ===== -->
      <div id="s06" class="scene clip ground-bright" data-start="14.8" data-duration="3.3" data-track-index="1">
        <div class="grid" id="s06-grid">{grid}</div>
      </div>
      <!-- ===== "Cafés remembered birthdays better than your cousins." ===== -->
      <div id="s07" class="scene clip ground-void" data-start="18.1" data-duration="3.25" data-track-index="1">
        <img id="m-cake" class="media still" src="assets/stills/birthday-cake.jpg" alt="">
        <div id="s07-n1" class="notif hero-push" style="left:90px;right:90px;top:300px;padding:26px 28px">
          <div class="ic" style="background:linear-gradient(140deg,#4a2c1b,#160b06);color:#e3c27e;font-style:italic;width:64px;height:64px;border-radius:50%;border:2px solid #e3c27e">a</div>
          <div class="nb"><div class="t1">Cafe Aroma <span>9:00 am</span></div><div class="tt">Happy birthday, Aarav!</div><div class="t2">Your coffee is on us today.</div></div>
        </div>
        <div id="s07-n2" class="notif" style="left:150px;right:150px;top:560px;padding:20px 24px;opacity:0.0">
          <div class="ic" style="background:#f59e0b">C</div>
          <div class="nb"><div class="t1">Cousins group <span>3 weeks ago</span></div><div class="t2">No new messages</div></div>
        </div>
      </div>
      <!-- ===== "But loyalty started living everywhere." ===== -->
      <div id="s08" class="scene clip ground-bright" data-start="21.35" data-duration="2.75" data-track-index="1">
        <div class="frag" id="f1" style="left:80px;top:250px;width:520px"><small>SMS</small>You've earned 40 reward points.</div>
        <div class="frag" id="f2" style="left:560px;top:520px;width:440px"><small>CHAT</small>Show this message at the counter.</div>
        <div id="f3" style="position:absolute;left:150px;top:640px">{icon("whatsapp", 150)}</div>
        <div class="frag" id="f4" style="left:120px;top:900px;width:470px"><small>EMAIL</small>Your rewards statement</div>
        <div class="frag" id="f5" style="left:640px;top:1000px;width:340px;text-align:center"><small>OTP</small><span class="mono" style="font-size:48px">4 8 2 1</span></div>
        <div id="f6" style="position:absolute;left:760px;top:240px">{icon("instagram", 150)}</div>
        <div class="frag" id="f7" style="left:300px;top:1180px;width:480px"><small>APP</small>Log in to see your points</div>
      </div>
      <!-- ===== "An SMS." ===== -->
      <div id="s09" class="scene clip ground-bright" data-start="24.1" data-duration="1.1" data-track-index="1">
        <div class="phone" id="s09-ph"><div class="screen chat"><div class="island"></div>
          <div class="hd"><div class="back">&lsaquo;</div><div class="av" style="background:#64748b">A</div><div><div class="nm">AX-AROMA</div><div class="sb">Text message</div></div></div>
          <div class="chip-date" style="top:190px">Today 9:41 am</div>
          <div class="bubble" id="s09-b" style="top:250px;max-width:380px">Dear customer, you have earned reward points at Cafe Aroma. Download our app to redeem. T&amp;C apply.<div class="tm">9:41</div></div>
        </div></div>
      </div>
      <!-- ===== "A chat." ===== -->
      <div id="s10" class="scene clip ground-bright" data-start="25.2" data-duration="0.85" data-track-index="1">
        <div class="phone" id="s10-ph"><div class="screen light"><div class="island"></div>
          <div style="position:absolute;left:26px;top:80px;font-weight:800;font-size:40px;color:var(--aub)">Chats</div>
          <div style="position:absolute;left:0;right:0;top:150px">{chat_rows}</div>
        </div></div>
      </div>
      <!-- ===== "An app they deleted." ===== -->
      <div id="s11" class="scene clip ground-bright" data-start="26.05" data-duration="1.35" data-track-index="1">
        <div id="s11-icon" class="appicon" style="left:425px;top:420px;width:230px;height:230px;background:linear-gradient(155deg,#4a2c1b,#160b06);box-shadow:inset 0 0 0 3px rgba(227,194,126,.6),0 30px 60px -24px rgba(30,12,4,.6)">
          <div style="font-family:'Archivo',sans-serif;font-style:italic;font-weight:600;font-size:120px;color:#e3c27e;margin-top:-16px">a</div></div>
        <div id="s11-name" style="position:absolute;left:0;right:0;top:672px;text-align:center;font-weight:700;font-size:32px;color:var(--aub)">Aroma Rewards</div>
        <div class="menu" id="s11-menu" style="left:305px;top:750px;box-shadow:0 30px 60px -24px rgba(30,20,40,.4)"><div>Share App</div><div>Edit Home Screen</div><div class="del">Delete App</div></div>
      </div>
      <!-- ===== "Another app." ===== -->
      <div id="s12" class="scene clip ground-bright" data-start="27.4" data-duration="1.0" data-track-index="1">
        <div class="phone" id="s12-ph"><div class="screen light"><div class="island"></div>
          <div style="position:absolute;left:30px;top:110px;width:150px;height:150px;border-radius:36px;background:linear-gradient(150deg,#0ea5e9,#6366f1);display:flex;align-items:center;justify-content:center;font-weight:800;font-size:64px;color:#fff">B</div>
          <div style="position:absolute;left:200px;top:120px;font-weight:800;font-size:32px;color:var(--aub);line-height:1.15">Brew Club<br>Rewards</div>
          <div style="position:absolute;left:200px;top:204px;font-weight:600;font-size:19px;color:var(--muted-l)">Collect points. Sign up to start.</div>
          <div class="btn-dark" id="s12-btn" style="top:300px;background:#2563eb">Install</div>
          <div class="sub" style="top:410px">Another app to download, another account to make.</div>
        </div></div>
      </div>
      <!-- ===== "Another login." ===== -->
      <div id="s13" class="scene clip ground-bright" data-start="28.4" data-duration="1.3" data-track-index="1">
        <div class="phone" id="s13-ph"><div class="screen light"><div class="island"></div>
          <div class="top">Log in to<br>Brew Club</div>
          <div class="sub" style="top:200px">Enter the 4-digit code sent to +91 98&bull;&bull;&bull;&bull;&bull;&bull;210</div>
          <div class="otp" style="top:290px"><div id="o1"><span class="dg">7</span></div><div id="o2"><span class="dg">3</span></div><div id="o3"><span class="dg">0</span></div><div id="o4"><span class="dg">9</span></div></div>
          <div class="btn-dark" style="top:420px">Verify</div>
        </div></div>
      </div>
      <!-- ===== silence · "What if loyalty didn't need another place?" ===== -->
      <div id="s14" class="scene clip ground-bright" data-start="29.7" data-duration="4.05" data-track-index="1">
        {lock_icons}
        <div class="phone" id="s14-ph">{lock()}</div>
      </div>
      <!-- ===== "It already has one. The wallet on their phone." ===== -->
      <div id="s15" class="scene clip ground-bright" data-start="33.75" data-duration="3.3" data-track-index="1">
        <div class="phone" id="s15-ph"><div class="screen wallet"><div class="island"></div>
          <div class="wt">Wallet</div>
          <div class="gw-card" style="top:780px;background:#0f766e"><div class="phd">METRO CARD</div></div>
          <div class="gw-card" style="top:720px;background:#4338ca"><div class="phd">LIBRARY PASS</div></div>
          {aroma("s15-pass", "qr-a", "top:150px")}
        </div></div>
      </div>
      <!-- ===== "Now they notice." · iPhone + Android, same pass ===== -->
      <div id="s19" class="scene clip ground-bright" data-start="43.3" data-duration="2.25" data-track-index="1">
        <div class="phone small" id="s19-l" style="left:150px;top:300px"><div class="screen wallet"><div class="island"></div>
          <div class="wt" style="font-size:34px;top:70px;left:24px">Wallet</div>
          <div style="position:absolute;left:0;top:130px;width:388px;transform:scale(0.825);transform-origin:0 0">{aroma("s19-pa", "qr-b", "left:0;right:0")}</div>
        </div></div>
        <div class="phone small android" id="s19-r" style="left:590px;top:300px"><div class="screen wallet" style="background:#f8f9fb"><div class="island"></div>
          <div class="wt" style="font-size:30px;top:70px;left:24px;font-weight:700">Google Wallet</div>
          <div style="position:absolute;left:0;top:130px;width:388px;transform:scale(0.825);transform-origin:0 0">{aroma("s19-pb", "qr-c", "left:0;right:0")}</div>
        </div></div>
        {badges("s19-bd", 1090, 0.98)}
      </div>
      <!-- ===== end card · "Why-stack. All your passes. One stack." ===== -->
      <div id="s20" class="scene clip ground-paper" data-start="{END_T}" data-duration="{round(DUR - END_T, 2)}" data-track-index="1">
        <div id="e-cam" style="position:absolute;inset:0">
          <div id="e-mark" class="end-mark" style="top:470px"><img src="assets/brand/logo-mark.png" alt="" style="width:640px;height:416px;display:block"></div>
          <div id="e-word" class="end-word" style="top:950px"><img src="assets/brand/logo-wordmark.png" alt="WYSTAK" style="width:700px;height:84px;display:block"></div>
          <div id="e-l1" class="end-tag" style="top:1130px">ALL YOUR PASSES.</div>
          <div id="e-l2" class="end-tag acc" style="top:1225px">ONE STACK.</div>
          {badges("e-bd", 1420, 0.8)}
        </div>
      </div>

      <!-- full-frame media on track 0 (videos must not sit inside a timed wrapper) -->
      <video id="m-scan" class="clip media" src="assets/footage/scan-at-counter.mp4" data-start="37.05" data-duration="2.5" data-track-index="0" muted playsinline></video>
      <video id="m-pay" class="clip media" src="assets/footage/pay-at-counter.mp4" data-start="39.55" data-duration="1.6" data-track-index="0" muted playsinline></video>
      <div id="s16" class="scene clip" data-start="37.05" data-duration="4.1" data-track-index="2">
        {badges("s16-bd", 1190, 0.9)}
      </div>
      <!-- ===== "...points land on their lock screen." ===== -->
      <div id="s18" class="scene clip ground-bright" data-start="41.15" data-duration="2.15" data-track-index="1">
        <div class="phone" id="s18-ph">{lock('''<div class="notif hero-push" id="s18-push" style="top:330px;padding:20px 20px">
            <div class="ic" style="background:linear-gradient(140deg,#4a2c1b,#160b06);color:#e3c27e;font-style:italic;border:2px solid #e3c27e;border-radius:50%">a</div>
            <div class="nb"><div class="t1">Wallet <span>now</span></div><div class="tt">+18 points at Cafe Aroma</div><div class="t2">132 points. Free cappuccino at 150.</div></div></div>''')}</div>
      </div>

      <div id="caps" style="position:absolute;inset:0;pointer-events:none;z-index:60">
{cap_html}
      </div>

      <audio id="vo" src="assets/voiceover.wav" data-start="0" data-duration="{DUR}" data-track-index="20" data-volume="1"></audio>
      <audio id="bed" src="assets/music-bed.wav" data-start="0" data-duration="{DUR}" data-track-index="21" data-volume="0.9"></audio>
      <audio id="sfx" src="assets/sfx.wav" data-start="0" data-duration="{DUR}" data-track-index="22" data-volume="0.55"></audio>

      <div id="grain-overlay" style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; pointer-events: none; z-index: 100; overflow: hidden">
        <div class="grain-texture"></div>
      </div>
      <style>
        @keyframes hf-grain-noise {{
          0%, 100% {{ transform: translate(0, 0); }} 10% {{ transform: translate(-5%, -5%); }} 20% {{ transform: translate(-10%, 5%); }}
          30% {{ transform: translate(5%, -10%); }} 40% {{ transform: translate(-5%, 15%); }} 50% {{ transform: translate(-10%, 5%); }}
          60% {{ transform: translate(15%, 0); }} 70% {{ transform: translate(0, 10%); }} 80% {{ transform: translate(-15%, 0); }} 90% {{ transform: translate(10%, 5%); }}
        }}
        #grain-overlay .grain-texture {{
          position: absolute; top: -50%; left: -50%; width: 200%; height: 200%;
          background: url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.65' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)'/%3E%3C/svg%3E");
          opacity: 0.05;
          animation: hf-grain-noise 0.5s steps(1) infinite;
        }}
      </style>
    </div>

    <script>
      (function () {{
        function rng(seed) {{ return function () {{ seed = (seed * 1664525 + 1013904223) >>> 0; return seed / 4294967296; }}; }}
        function qrSVG(size, seed, color) {{
          const N = 25, m = size / N, r = rng(seed); let rects = "";
          const finder = (x, y) => x >= 0 && x < 8 && y >= 0 && y < 8;
          for (let y = 0; y < N; y++) for (let x = 0; x < N; x++) {{
            if (finder(x, y) || finder(x - (N - 8), y) || finder(x, y - (N - 8))) continue;
            if (r() > 0.52) rects += `<rect x="${{x * m}}" y="${{y * m}}" width="${{m + 0.4}}" height="${{m + 0.4}}"/>`;
          }}
          const fp = (x, y) => `<rect x="${{x * m}}" y="${{y * m}}" width="${{7 * m}}" height="${{7 * m}}"/><rect x="${{(x + 1) * m}}" y="${{(y + 1) * m}}" width="${{5 * m}}" height="${{5 * m}}" fill="#fffaf0"/><rect x="${{(x + 2) * m}}" y="${{(y + 2) * m}}" width="${{3 * m}}" height="${{3 * m}}"/>`;
          return `<svg width="${{size}}" height="${{size}}" viewBox="0 0 ${{size}} ${{size}}" fill="${{color}}" style="display:block">${{rects}}${{fp(0, 0)}}${{fp(N - 7, 0)}}${{fp(0, N - 7)}}</svg>`;
        }}
        ["qr-a", "qr-b", "qr-c"].forEach((id) => (document.getElementById(id).innerHTML = qrSVG(142, 17, "#2a170d")));

        const tl = gsap.timeline({{ paused: true }});
        function push(target, t0, dur, from, to, origin) {{
          tl.fromTo(target, {{ scale: from }}, {{ scale: to, duration: dur, ease: "none", transformOrigin: origin || "50% 50%" }}, t0);
        }}
        const rise = (target, t, dy, d) => tl.fromTo(target, {{ opacity: 0, y: dy || 40 }}, {{ opacity: 1, y: 0, duration: d || 0.5, ease: "power3.out" }}, t);
        const pop = (target, t, from) => tl.fromTo(target, {{ opacity: 0, scale: from || 0.6 }}, {{ opacity: 1, scale: 1, duration: 0.42, ease: "back.out(1.7)" }}, t);

        // ---------- opening: two slow shots, fade up from black ----------
        tl.fromTo("#s01-fade", {{ opacity: 1 }}, {{ opacity: 0, duration: 0.9, ease: "power1.inOut" }}, 0);
        push("#m-interior", 0, 2.7, 1.0, 1.09, "50% 45%");
        push("#m-cup", 2.7, 2.55, 1.04, 1.12, "50% 45%");
        rise("#s02-n", 3.05, -50, 0.6);
        tl.to("#s02-n", {{ opacity: 0.25, y: -20, filter: "blur(2px)", duration: 0.7, ease: "power2.in" }}, 4.25);

        // ---------- data ----------
        push("#m-pos", 5.25, 3.8, 1.03, 1.11, "60% 55%");
        rise("#s03-card", 5.55, 60, 0.6);
        ["#r1", "#r2", "#r3", "#r4"].forEach((r, i) => rise(r, 6.5 + i * 0.32, 16, 0.3));
        push("#m-desk", 9.05, 2.15, 1.02, 1.09, "50% 50%");
        push("#m-wcounter", 11.2, 1.2, 1.05, 1.1, "50% 50%");
        push("#m-pour", 12.4, 1.15, 1.04, 1.1, "45% 50%");
        push("#m-pour2", 13.55, 1.25, 1.04, 1.1, "45% 50%");
        rise("#s05a .tag", 11.45, 24, 0.35);
        rise("#s05b .tag", 12.6, 24, 0.35);
        rise("#s05c .tag", 13.8, 24, 0.35);

        // ---------- social media: apps pop in, then the badges ----------
        for (let i = 0; i < 9; i++) pop(`#g${{i}} .app`, 14.95 + i * 0.11, 0.4);
        for (let i = 0; i < 9; i++) tl.fromTo(`#g${{i}} .nm`, {{ opacity: 0 }}, {{ opacity: 1, duration: 0.3 }}, 15.1 + i * 0.11);
        tl.fromTo("#s06 .badge-n", {{ scale: 0, opacity: 0 }}, {{ scale: 1, opacity: 1, duration: 0.3, ease: "back.out(2.5)", stagger: 0.12 }}, 16.45);
        push("#s06-grid", 14.8, 3.3, 1.0, 1.05, "50% 40%");

        // ---------- birthdays ----------
        push("#m-cake", 18.1, 3.25, 1.03, 1.1, "50% 50%");
        rise("#s07-n1", 18.85, -60, 0.6);
        tl.fromTo("#s07-n2", {{ opacity: 0, y: -30 }}, {{ opacity: 0.8, y: 0, duration: 0.5, ease: "power3.out" }}, 20.35);

        // ---------- everywhere: fragments drift out from the centre ----------
        const frags = ["#f1", "#f2", "#f3", "#f4", "#f5", "#f6", "#f7"];
        frags.forEach((f, i) => {{
          tl.fromTo(f, {{ opacity: 0, scale: 0.7, x: (i % 2 ? -1 : 1) * 120, y: (i < 3 ? 1 : -1) * 120 }},
            {{ opacity: 1, scale: 1, x: 0, y: 0, duration: 0.9, ease: "power3.out" }}, 21.45 + i * 0.22);
          tl.to(f, {{ x: (i % 2 ? 1 : -1) * 30, y: (i < 3 ? -1 : 1) * 24, duration: 1.4, ease: "none" }}, 22.7);
        }});

        // ---------- SMS / chat / deleted / another app / login ----------
        push("#s09-ph", 24.1, 1.1, 1.0, 1.04);
        rise("#s09-b", 24.25, 30, 0.4);
        push("#s10-ph", 25.2, 0.85, 1.0, 1.04);
        tl.fromTo("#s10 .crow.hot", {{ backgroundColor: "#ffffff" }}, {{ backgroundColor: "#ffe8b8", duration: 0.3 }}, 25.45);
        tl.fromTo("#s11-icon", {{ rotation: -3 }}, {{ rotation: 3, duration: 0.12, repeat: 5, yoyo: true, ease: "sine.inOut" }}, 26.1);
        rise("#s11-menu", 26.15, -20, 0.3);
        tl.to("#s11-menu .del", {{ backgroundColor: "#fde2e6", duration: 0.12 }}, 26.6);
        tl.to("#s11-icon, #s11-name", {{ scale: 0, opacity: 0, duration: 0.35, ease: "back.in(1.6)" }}, 26.75);
        tl.to("#s11-menu", {{ opacity: 0, duration: 0.25 }}, 26.72);
        push("#s12-ph", 27.4, 1.0, 1.0, 1.04);
        tl.to("#s12-btn", {{ scale: 0.94, duration: 0.1, yoyo: true, repeat: 1 }}, 27.95);
        push("#s13-ph", 28.4, 1.3, 1.0, 1.04);
        tl.fromTo("#s13 .dg", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.05, stagger: 0.14 }}, 28.95);

        // ---------- silence, then "another place?": the apps fall away ----------
        push("#s14-ph", 29.7, 4.05, 0.98, 1.04);
        tl.fromTo("#s14 .app", {{ opacity: 0 }}, {{ opacity: 0.9, duration: 0.6, stagger: 0.05 }}, 31.0);
        tl.to("#s14 .app", {{ y: 260, opacity: 0, rotation: 12, duration: 0.6, ease: "power2.in", stagger: 0.06 }}, 32.75);

        // ---------- wallet: the Cafe Aroma pass ----------
        push("#s15-ph", 33.75, 3.3, 1.0, 1.05);
        tl.fromTo("#s15-pass", {{ y: 700 }}, {{ y: 0, duration: 0.7, ease: "power3.out" }}, 34.0);
        tl.fromTo("#s15 .gw-card", {{ opacity: 0.0 }}, {{ opacity: 1, duration: 0.4 }}, 35.35);

        // ---------- scan, pay: Add to Apple Wallet / Google Wallet ----------
        pop("#s16-bd .badge", 38.85, 0.7);
        tl.to("#s16-bd", {{ opacity: 0, duration: 0.2 }}, 40.9);

        // ---------- lock-screen push ----------
        push("#s18-ph", 41.15, 2.15, 1.0, 1.05);
        tl.fromTo("#s18-push", {{ y: -140, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.45, ease: "back.out(1.4)" }}, 41.45);

        // ---------- now they notice ----------
        tl.fromTo("#s19-l", {{ x: -60, opacity: 0 }}, {{ x: 0, opacity: 1, duration: 0.45, ease: "power3.out" }}, 43.3);
        tl.fromTo("#s19-r", {{ x: 60, opacity: 0 }}, {{ x: 0, opacity: 1, duration: 0.45, ease: "power3.out" }}, 43.42);
        push("#s19-l, #s19-r", 43.3, 2.25, 1.0, 1.04);
        pop("#s19-bd .badge", 43.7, 0.7);

        // ---------- end card: slow, held ----------
        tl.fromTo("#e-mark", {{ opacity: 0, scale: 1.18, filter: "blur(18px)" }}, {{ opacity: 1, scale: 1, filter: "blur(0px)", duration: 1.0, ease: "power3.out" }}, 45.6);
        tl.fromTo("#e-word", {{ clipPath: "inset(0 100% 0 0)" }}, {{ clipPath: "inset(0 0% 0 0)", duration: 0.8, ease: "power3.inOut" }}, 46.05);
        rise("#e-l1", 46.8, 30, 0.6);
        tl.fromTo("#e-l2", {{ opacity: 0, scale: 1.25 }}, {{ opacity: 1, scale: 1, duration: 0.6, ease: "back.out(1.6)" }}, 47.98);
        tl.fromTo("#e-bd", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.7 }}, 49.1);
        push("#e-cam", 45.55, {round(DUR - END_T, 2)}, 1.0, 1.05, "50% 45%");

        // ---------- captions: phrase on, each word lights as it is spoken ----------
        const CAPS = {cap_js};
        CAPS.forEach(([s, e, ws], i) => {{
          tl.fromTo(`#cap${{i}}`, {{ opacity: 0, y: 14 }}, {{ opacity: 1, y: 0, duration: 0.14, ease: "power2.out" }}, s);
          tl.to(`#cap${{i}}`, {{ opacity: 0, duration: 0.08 }}, e - 0.08);
          ws.forEach(([a, b], j) => {{
            tl.fromTo(`#cw${{i}}_${{j}}`, {{ opacity: 0.45, color: "#ffffff" }}, {{ opacity: 1, color: "#ffd479", duration: 0.08 }}, a);
            tl.to(`#cw${{i}}_${{j}}`, {{ color: "#ffffff", duration: 0.12 }}, Math.max(b, a + 0.1));
          }});
        }});

        window.__timelines = window.__timelines || {{}};
        window.__timelines["main"] = tl;
      }})();
    </script>
  </body>
</html>
'''
(P / "index.html").write_text(HTML)
print("index.html written:", len(CAPS), "caption groups")
