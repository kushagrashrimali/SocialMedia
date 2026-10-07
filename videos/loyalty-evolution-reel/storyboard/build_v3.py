"""Build index.html for the loyalty reel, v3 (art-directed cut, 51.39s).

Type is art-directed (Inter Tight + Instrument Serif italic + JetBrains Mono), not subtitles.
Phones, notifications and Wallet screens are drawn here; the Cafe Aroma passes are rendered
separately (storyboard/card/render.sh -> assets/ui/pass-*.png).
usage (from the project folder): python3 storyboard/build_v3.py
then re-apply the voice carve on the bed (hyperframes-audio carve.mjs --bed bed --voice vo --strength 0.6).
"""
import json, pathlib

HERE = pathlib.Path(__file__).resolve().parent
P = HERE.parent
DUR = 51.39
ICONS = json.load(open(HERE / "icons.json"))

# ------------------------------------------------------------------ media (one place to swap shots)
V = {  # full-frame footage, cropped 9:16 and graded by storyboard/prep_v3.py
    "open": "assets/footage/v3-open.mp4",
    "pay": "assets/footage/v3-pay.mp4",
    "barista": "assets/footage/v3-barista.mp4",
    "walkin": "assets/footage/v3-walkin.mp4",
    "purchase": "assets/footage/v3-purchase.mp4",
    "pour": "assets/footage/v3-pour.mp4",
    "notice": "assets/footage/v3-notice.mp4",
    "scan": "assets/footage/scan-at-counter.mp4",
    "paid": "assets/footage/pay-at-counter.mp4",
}
S = {  # stills: bright grounds behind phones (pre-blurred) and the birthday photo
    "table": "assets/stills/bg-table.jpg",
    "counter": "assets/stills/bg-counter.jpg",
    "window": "assets/stills/bg-window.jpg",
    "cake": "assets/stills/birthday.jpg",
}

# ------------------------------------------------------------------ small drawing helpers
def glyph(name, fg, size):
    return f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="{fg}"><path d="{ICONS[name]}"/></svg>'


APP = {  # app icon: background, glyph colour  (social apps requested by the user)
    "whatsapp": ("#25D366", "#fff"), "instagram": ("linear-gradient(45deg,#f9b233 0%,#e4405f 45%,#c13584 70%,#5851db 100%)", "#fff"),
    "imessage": ("linear-gradient(180deg,#5cf777,#0abf30)", "#fff"), "facebook": ("#0866ff", "#fff"), "telegram": ("linear-gradient(180deg,#37aee2,#1e96c8)", "#fff"),
    "gmail": ("#ffffff", "#ea4335"), "youtube": ("#ffffff", "#ff0000"), "snapchat": ("#fffc00", "#fff"), "x": ("#000", "#fff"),
}


def app_icon(name, size, extra=""):
    bg, fg = APP[name]
    g = glyph(name, fg, int(size * 0.58))
    if name == "snapchat":
        g = f'<svg width="{int(size*.6)}" height="{int(size*.6)}" viewBox="0 0 24 24"><path d="{ICONS[name]}" fill="#fff" stroke="#111" stroke-width="0.9"/></svg>'
    return f'<div class="ai" style="width:{size}px;height:{size}px;border-radius:{size*0.225:.1f}px;background:{bg};{extra}">{g}</div>'


def custom_icon(size, bg, inner, extra=""):
    return f'<div class="ai" style="width:{size}px;height:{size}px;border-radius:{size*0.225:.1f}px;background:{bg};{extra}">{inner}</div>'


BEAN = lambda c, s: (f'<svg width="{s}" height="{s}" viewBox="0 0 30 30"><g transform="rotate(-32 15 15)"><ellipse cx="15" cy="15" rx="6.6" ry="9.4" fill="{c}"/>'
                     f'<path d="M15 5.8 C12 10 18 13.6 15 24.2" fill="none" stroke="#2a1a11" stroke-width="1.7" stroke-linecap="round"/></g></svg>')
AROMA_ICON = lambda s: custom_icon(s, "linear-gradient(160deg,#3b2417,#1d110a)", BEAN("#f0d9b2", int(s * .7)))
BREW_ICON = lambda s: custom_icon(s, "linear-gradient(150deg,#ff8a3d,#e8452c)", f'<span style="font:800 {int(s*.5)}px/1 Inter Tight;color:#fff;letter-spacing:-.04em">bc</span>')
WALLET_ICON = lambda s: custom_icon(s, "#000", (
    f'<svg width="{int(s*.66)}" height="{int(s*.56)}" viewBox="0 0 40 34"><rect x="2" y="2" width="36" height="9" rx="3" fill="#2f80ed"/>'
    f'<rect x="2" y="8" width="36" height="9" rx="3" fill="#f2c94c"/><rect x="2" y="14" width="36" height="9" rx="3" fill="#eb5757"/>'
    f'<path d="M2 20 h11 a7 5 0 0 0 14 0 h11 v9 a3 3 0 0 1 -3 3 h-30 a3 3 0 0 1 -3 -3z" fill="#e8e8ed"/></svg>'))
SMS_ICON = lambda s: app_icon("imessage", s)
SYS = {  # plain system-style icons drawn here (no brands)
    "Camera": ("linear-gradient(180deg,#e9e9ee,#c9c9d1)", '<svg width="58%" height="58%" viewBox="0 0 24 24"><path d="M4 7h3l2-2h6l2 2h3v12H4z" fill="#3a3a3c"/><circle cx="12" cy="13" r="3.6" fill="#c9c9d1"/></svg>'),
    "Photos": ("#fff", '<svg width="70%" height="70%" viewBox="0 0 24 24">' + "".join(
        f'<ellipse cx="12" cy="6.6" rx="2.6" ry="5" fill="{c}" opacity=".85" transform="rotate({a} 12 12)"/>' for a, c in
        zip(range(0, 360, 45), ["#f6c143", "#f39a2e", "#ea4e3d", "#d43d8b", "#9b51e0", "#4b7bec", "#34b4c9", "#5fc35a"])) + '</svg>'),
    "Clock": ("#000", '<svg width="76%" height="76%" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10" fill="#fff"/><path d="M12 6v6l4 2" stroke="#000" stroke-width="1.6" fill="none" stroke-linecap="round"/></svg>'),
    "Settings": ("linear-gradient(180deg,#a7a7ae,#7d7d84)", '<svg width="66%" height="66%" viewBox="0 0 24 24"><circle cx="12" cy="12" r="7.4" fill="none" stroke="#3a3a3c" stroke-width="3" stroke-dasharray="2.6 1.6"/><circle cx="12" cy="12" r="3" fill="#3a3a3c"/></svg>'),
    "Calendar": ("#fff", '<div style="text-align:center;line-height:1"><div style="font:600 11px Inter Tight;color:#ff3b30">TUE</div><div style="font:400 34px Inter Tight;color:#111;margin-top:1px">7</div></div>'),
}


def status_bar(dark_text=False):
    c = "#111" if dark_text else "#fff"
    return (f'<div class="sb" style="color:{c}"><span>9:41</span><span class="sbi"><svg width="34" height="22" viewBox="0 0 34 22" fill="{c}">'
            '<rect x="0" y="14" width="5" height="7" rx="1.2"/><rect x="8" y="10" width="5" height="11" rx="1.2"/><rect x="16" y="6" width="5" height="15" rx="1.2"/><rect x="24" y="2" width="5" height="19" rx="1.2"/></svg>'
            f'<svg width="50" height="22" viewBox="0 0 50 22"><rect x="1" y="2" width="42" height="18" rx="5.5" fill="none" stroke="{c}" stroke-opacity=".45" stroke-width="2"/>'
            f'<rect x="4.5" y="5.5" width="31" height="11" rx="3" fill="{c}"/><rect x="45.5" y="8" width="3" height="6" rx="1.5" fill="{c}" fill-opacity=".45"/></svg></span></div>')


def notif(id_, icon, title, time, body, cls=""):
    return (f'<div class="nt {cls}" id="{id_}">{icon}<div class="nb"><div class="nh"><b>{title}</b><span>{time}</span></div>'
            f'<div class="nx">{body}</div></div></div>')


def lock_screen(inner="", sleep_id=None):
    sl = f'<div class="sleep" id="{sleep_id}"></div>' if sleep_id else ""
    return (f'<div class="scr lock">{status_bar()}<div class="ldate">Tuesday 7 October</div><div class="ltime">9:41</div>'
            f'{inner}<div class="lbtn" style="left:44px"><svg width="26" height="26" viewBox="0 0 24 24" fill="#fff"><path d="M9 2h6v5l-2 3v12h-2V10L9 7z"/></svg></div>'
            f'<div class="lbtn" style="right:44px"><svg width="28" height="28" viewBox="0 0 24 24" fill="#fff"><path d="M4 7h3l2-2h6l2 2h3v12H4z"/><circle cx="12" cy="13" r="3.4" fill="#333"/></svg></div>'
            f'<div class="hbar"></div>{sl}</div>')


def phone(id_, screen, kind="ios", style=""):
    cls = "phone android" if kind == "android" else "phone"
    cut = '<div class="punch"></div>' if kind == "android" else '<div class="island"></div>'
    return f'<div class="{cls}" id="{id_}" style="{style}"><div class="glass">{screen}{cut}<div class="refl"></div></div></div>'


def type_block(id_, lines, top, theme="dark", align="left", extra=""):
    """lines: list of (kind, text, size) where kind in sans|serif|kick."""
    out = []
    for k, (kind, text, size) in enumerate(lines):
        if kind == "kick":
            out.append(f'<div class="kick" id="{id_}-k{k}" style="font-size:{size}px">{text}</div>')
        else:
            out.append(f'<div class="ln {kind}" id="{id_}-l{k}" style="font-size:{size}px"><span>{text}</span></div>')
    return f'<div class="t {theme}" id="{id_}" style="top:{top}px;text-align:{align};{extra}">{"".join(out)}</div>'


# ------------------------------------------------------------------ screens
NOTIF_B = [
    ("nB1", SMS_ICON(44), "AX-CAROMA", "2d ago", "Dear customer, you have earned reward points. T&amp;C apply."),
    ("nB2", BREW_ICON(44), "Brew Club", "1d ago", "Your points expire on Sunday. Log in to redeem."),
    ("nB3", app_icon("gmail", 44), "Gmail", "9:12", "Your monthly rewards statement is ready to view."),
]
NOTIF_H = [
    ("nH1", SMS_ICON(44), "AX-CAROMA", "now", "You've earned 40 reward points. Download our app to redeem."),
    ("nH2", app_icon("whatsapp", 44), "Cafe Aroma", "now", "Show this message at the counter for your points."),
    ("nH3", app_icon("gmail", 44), "Gmail", "now", "Your rewards statement for September is ready."),
    ("nH4", BREW_ICON(44), "Brew Club", "now", "Points expiring Sunday. Sign in to keep them."),
    ("nH5", app_icon("instagram", 44), "Instagram", "now", "cafearoma.bandra sent you a message."),
    ("nH6", app_icon("telegram", 44), "Aroma Club", "now", "New members' offer inside. Tap to view."),
    ("nH7", SMS_ICON(44), "VM-REWRDS", "now", "Your OTP for login is 4821. Do not share."),
]
lockB = lock_screen("".join(notif(*n) for n in NOTIF_B), sleep_id="sleepB")
lockH = lock_screen('<div class="nlist">' + "".join(notif(*n) for n in NOTIF_H) + "</div>")

home_apps = [("whatsapp", "WhatsApp"), ("instagram", "Instagram"), ("imessage", "Messages"), ("facebook", "Facebook"),
             ("telegram", "Telegram"), ("gmail", "Gmail"), ("youtube", "YouTube"), ("snapchat", "Snapchat"),
             ("x", "X"), ("Camera", "Camera"), ("Photos", "Photos"), ("Calendar", "Calendar")]
BADGES = {"whatsapp": "3", "instagram": "9+", "imessage": "12", "gmail": "24", "telegram": "2", "snapchat": "5"}


def home_cell(i, key, label):
    ic = app_icon(key, 86) if key in APP else custom_icon(86, SYS[key][0], SYS[key][1])
    b = f'<div class="hbadge">{BADGES[key]}</div>' if key in BADGES else ""
    return f'<div class="hc" id="hF{i}">{ic}{b}<div class="hl">{label}</div></div>'


homeF = (f'<div class="scr home">{status_bar()}<div class="hgrid">' + "".join(home_cell(i, k, l) for i, (k, l) in enumerate(home_apps)) +
         '</div><div class="dock">' + custom_icon(86, "linear-gradient(180deg,#5cf777,#0abf30)", '<svg width="54%" height="54%" viewBox="0 0 24 24" fill="#fff"><path d="M6.6 10.8a15.1 15.1 0 0 0 6.6 6.6l2.2-2.2c.3-.3.7-.4 1-.2 1.1.4 2.3.6 3.6.6.6 0 1 .4 1 1V20c0 .6-.4 1-1 1A17 17 0 0 1 3 4c0-.6.4-1 1-1h3.5c.6 0 1 .4 1 1 0 1.3.2 2.5.6 3.6.1.3 0 .7-.2 1z"/></svg>')
         + WALLET_ICON(86) + custom_icon(86, SYS["Settings"][0], SYS["Settings"][1]) + custom_icon(86, SYS["Clock"][0], SYS["Clock"][1]) +
         '</div>' + notif("nF", app_icon("whatsapp", 44), "Cafe Aroma", "now", "Your usual cold brew is waiting, Aarav. See you soon!", "banner") + '<div class="hbar"></div></div>')

# SMS / chat / delete / store / login screens (one phone, screens slide in)
smsI = (f'<div class="scr light" id="iS1">{status_bar(True)}<div class="navb"><span class="bk">&lsaquo;</span><div class="cav" style="background:#8e8e93">A</div>'
        '<div class="cn">AX-CAROMA</div></div><div class="day">Text Message · Today 9:38</div>'
        '<div class="bub in" style="top:250px">Dear Customer, you have earned 18 pts at Cafe Aroma. Download our app to redeem: aroma.app/r T&amp;C apply.</div>'
        '<div class="bub in" style="top:440px">Reply STOP to unsubscribe.</div><div class="hbar dk"></div></div>')
chatI = (f'<div class="scr light" id="iS2" style="background:#efe7de">{status_bar(True)}<div class="navb" style="background:#f6f6f6"><span class="bk">&lsaquo;</span>'
         '<div class="cav" style="background:linear-gradient(160deg,#3b2417,#1d110a)">' + BEAN("#f0d9b2", 30) + '</div><div><div class="cn">Cafe Aroma</div><div class="cs">Business account</div></div></div>'
         '<div class="day" style="color:#6d6d72">Yesterday</div><div class="bub in w" style="top:250px">Hi Aarav! You have 132 points with us. Reply POINTS to check your balance.<i>6:02 pm</i></div>'
         '<div class="bub in w" style="top:420px">New: double points on weekdays before 11 am.<i>6:02 pm</i></div>'
         '<div class="day" style="top:560px;color:#6d6d72">Today</div><div class="bub in w" style="top:610px">Rate your last visit: aroma.app/rate<i>9:30 am</i></div><div class="hbar dk"></div></div>')
delI = (f'<div class="scr home" id="iS3">{status_bar()}<div class="dim"></div>'
        f'<div class="hc focus" id="delIcon">{AROMA_ICON(120)}<div class="hl" style="font-size:19px">Aroma</div></div>'
        '<div class="ctx" id="delMenu"><div>Share App</div><div>Edit Home Screen</div><div class="red">Remove App</div></div><div class="hbar"></div></div>')
storeI = (f'<div class="scr light" id="iS4">{status_bar(True)}<div class="st-top">{BREW_ICON(150)}<div><div class="st-n">Brew Club<br>Rewards</div>'
          '<div class="st-s">Collect points at Brew Club</div><div class="get" id="getBtn">GET</div></div></div>'
          '<div class="st-row"><div><b>4.1</b><span>2.3K RATINGS</span></div><div><b>12+</b><span>AGE</span></div><div><b>86 MB</b><span>SIZE</span></div></div>'
          '<div class="st-shot"></div><div class="hbar dk"></div></div>')
loginI = (f'<div class="scr light" id="iS5">{status_bar(True)}<div class="lg-h">Sign in to<br>Brew Club</div><div class="lg-s">Enter the 4-digit code we sent to +91 98•••• ••210</div>'
          '<div class="otp"><div><span class="dg">7</span></div><div><span class="dg">3</span></div><div><span class="dg">0</span></div><div><span class="dg">9</span></div></div>'
          '<div class="lg-b">Verify</div><div class="lg-x">Didn\'t get it? Resend in 0:28</div><div class="hbar dk"></div></div>')
screensI = smsI + chatI + delI + storeI + loginI

lockJ = lock_screen()
lockN = lock_screen('<div class="nlist" style="top:520px">' + notif("nN", WALLET_ICON(44), "Wallet", "now",
                     "<b>Cafe Aroma</b> · +18 points. 150 of 150: your free cappuccino is ready.", "hero") + "</div>")

walletK = (f'<div class="scr light" style="background:#f2f2f7">{status_bar(True)}<div class="w-h">Wallet<span>+</span></div>'
           '<div class="w-card" style="top:150px;background:#1f3b73"><b>METRO CARD</b></div><div class="w-card" style="top:206px;background:#5b2287"><b>BOARDING PASS</b></div>'
           '<img class="w-pass" id="kPassA" src="assets/ui/pass-apple.png" alt="" style="top:262px"><div class="hbar dk"></div></div>')
gwalletK = (f'<div class="scr light" style="background:#fff">{status_bar(True)}<div class="gw-h"><span>Wallet</span><i></i></div>'
            '<img class="w-pass" id="kPassG" src="assets/ui/pass-google.png" alt="" style="top:150px"><div class="hbar dk"></div></div>')

# ------------------------------------------------------------------ badges (drawn, equal size)
WG = ('<svg width="44" height="36" viewBox="0 0 46 38"><rect x="1" y="1" width="44" height="36" rx="7" fill="#fff"/>'
      '<rect x="5" y="6" width="36" height="8" rx="3" fill="#3d8bfd"/><rect x="5" y="11" width="36" height="8" rx="3" fill="#ffb300"/>'
      '<rect x="5" y="16" width="36" height="8" rx="3" fill="#ef4444"/><rect x="5" y="21" width="36" height="12" rx="3" fill="#22c55e"/></svg>')
GG = ('<svg width="44" height="36" viewBox="0 0 46 38"><path d="M4 10 Q4 4 10 4 H36 Q42 4 42 10 V12 H4Z" fill="#4285f4"/>'
      '<path d="M4 12 H42 V18 H4Z" fill="#ea4335"/><path d="M4 18 H42 V24 H4Z" fill="#fbbc04"/><path d="M4 24 H42 V28 Q42 34 36 34 H10 Q4 34 4 28Z" fill="#34a853"/></svg>')
BADGES_HTML = ('<div class="badges" id="bdL">'
               f'<div class="badge" id="bdA">{glyph("apple", "#fff", 36)}{WG}<div class="bt"><span>Add to</span>Apple Wallet</div></div>'
               f'<div class="badge" id="bdG">{GG}<div class="bt"><span>Add to</span>Google Wallet</div></div></div>')

# ------------------------------------------------------------------ page
TPL = (HERE / "v3_template.html").read_text()
html = (TPL.replace("%%DUR%%", str(DUR))
        .replace("%%LOCK_B%%", phone("phB", lockB))
        .replace("%%HOME_F%%", phone("phF", homeF))
        .replace("%%LOCK_H%%", phone("phH", lockH))
        .replace("%%SCREENS_I%%", phone("phI", screensI))
        .replace("%%LOCK_J%%", phone("phJ", lockJ))
        .replace("%%WALLET_K%%", phone("phKa", walletK))
        .replace("%%GWALLET_K%%", phone("phKg", gwalletK, "android"))
        .replace("%%LOCK_N%%", phone("phN", lockN))
        .replace("%%BADGES%%", BADGES_HTML)
        .replace("%%AROMA_NOTIF_G1%%", notif("nG1", app_icon("whatsapp", 64), "Cafe Aroma", "9:00", "Happy birthday, Aarav! Your next coffee is on us today.", "float"))
        .replace("%%AROMA_NOTIF_G2%%", notif("nG2", app_icon("whatsapp", 64), "Cousins", "6:45 pm", "Rohan: wait, whose birthday is it today?", "float"))
        )
for k, v in V.items():
    html = html.replace(f"%%V_{k}%%", v)
for k, v in S.items():
    html = html.replace(f"%%S_{k}%%", v)
# type blocks
T = {
    "tA": type_block("tA", [("sans", "India never stopped", 82), ("serif", "rewarding.", 196)], 1150),
    "tB": type_block("tB", [("sans", "Customers stopped", 80), ("serif", "noticing.", 184)], 210, "light"),
    "tC": type_block("tC", [("sans", "Every counter started", 76), ("serif", "collecting data.", 150), ("kick", "+ not just cash", 32)], 1150),
    "tD": type_block("tD", [("sans", "Businesses learned", 80), ("serif", "to remember.", 180)], 1170),
    "tF": type_block("tF", [("sans", "Staying connected", 80), ("serif", "got effortless.", 156)], 210, "light"),
    "tG": type_block("tG", [("kick", "Cafés remembered birthdays", 30), ("serif", "better than", 150), ("serif", "your cousins.", 150)], 1110),
    "tI": type_block("tI", [("kick", "Loyalty lived in", 30)], 230, "light"),
    "tJ": type_block("tJ", [("sans", "What if loyalty didn't need", 62), ("serif", "another place?", 168)], 210, "light"),
    "tK": type_block("tK", [("sans", "It already has a home.", 76), ("serif", "Their wallet.", 176)], 200, "light"),
    "tK2": type_block("tK2", [("kick", "Apple Wallet &nbsp;·&nbsp; Google Wallet", 32)], 1390, "light", "center"),
    "tL": type_block("tL", [("sans", "One scan.", 92), ("serif", "No app.", 210)], 230),
    "tM": type_block("tM", [("serif", "Seconds", 210), ("sans", "after they pay.", 84)], 230),
    "tO": type_block("tO", [("sans", "Now they", 92), ("serif", "notice.", 240)], 1120),
}
for k, v in T.items():
    html = html.replace(f"%%{k}%%", v)
# swapping words for the SMS / chat / app / login run
SW = [("an SMS.", 24.15), ("a chat.", 25.24), ("an app they deleted.", 26.08), ("another app.", 27.46), ("another login.", 28.42)]
html = html.replace("%%SWAP%%", "".join(f'<div class="ln serif sw" id="sw{i}" style="font-size:{140 if len(w) < 16 else 112}px"><span>{w}</span></div>' for i, (w, _) in enumerate(SW)))
html = html.replace("%%SWAP_JS%%", json.dumps(SW))
assert "%%" not in html, [l for l in html.splitlines() if "%%" in l][:3]
(P / "index.html").write_text(html)
print("index.html written")
