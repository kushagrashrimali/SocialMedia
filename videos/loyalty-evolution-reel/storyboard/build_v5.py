"""Build index.html for the loyalty reel, v5 (52.39s).

v5: every category (cinema, salon, retail, club, concert, café) in real footage, soft zoom-through and
focus-pull transitions with overlapping clips, light leaks, a longer Wystak introduction (+1.0s), category passes
in the Wallet stack, and a "now they notice" montage across categories.

v4: Indian Gen-Z photography, one caption family (Inter Tight) with per-word pops synced to the
voice, 3D phones and notifications on brand grounds, the question -> answer turn as one continuous
move (the scattered pieces collapse into the Wallet as the frame floods Wystak violet), Wallet
names with their icons under each phone, Add-to-Wallet badges inside the scanned page.
usage (from the project folder): python3 storyboard/build_v5.py
then re-apply the voice carve on the bed (hyperframes-audio carve.mjs --bed bed --voice vo --strength 0.6).
"""
import json, pathlib

HERE = pathlib.Path(__file__).resolve().parent
P = HERE.parent
DUR = 52.39
ICONS = json.load(open(HERE / "icons.json"))
W = json.load(open(P / "assets/words.json"))
W = W["words"] if isinstance(W, dict) else W
WT = [(w.get("text") or w.get("word"), w["start"], w["end"]) for w in W]

# ------------------------------------------------------------------ captions (exact words, short groups)
GROUPS = [  # (first word, last word, accent word indices)
    (0, 4, [3]), (5, 9, [9]), (10, 14, [14]), (15, 17, []), (18, 21, [21]),
    (22, 23, [23]), (24, 25, [25]), (26, 27, [27]), (28, 31, []), (32, 34, [34]),
    (35, 37, []), (38, 41, [41]), (42, 46, [46]), (47, 48, [48]), (49, 50, [50]),
    (51, 54, [54]), (55, 56, []), (57, 58, [58]), (59, 62, []), (63, 65, [64, 65]),
    (66, 69, [69]), (70, 74, [71]), (75, 79, []), (80, 81, [80, 81]), (82, 85, []),
    (86, 91, [90, 91]), (92, 94, [94]),
]
# caption theme by time: light grounds use navy + violet accent; footage / violet grounds use white + mint accent
LIGHT = [(2.72, 5.32), (14.88, 18.18), (21.42, 34.87)]
theme = lambda t: "light" if any(a <= t < b for a, b in LIGHT) else "dark"
cap_html, cap_js = [], []
ACC = {"light": "#6b2ba6", "dark": "#00e0a3"}
for gi, (a, b, acc) in enumerate(GROUPS):
    s0 = WT[a][1]
    nxt = WT[GROUPS[gi + 1][0]][1] if gi + 1 < len(GROUPS) else 46.55
    e = min(nxt - 0.04, WT[b][2] + 0.55)
    if WT[b][0] in ("cash.",):  # hand straight over to the next beat
        e = min(e, 9.05)
    if WT[b][0] == "login.":   # clear the frame on the lock click, before Wystak is introduced
        e = min(e, 29.62)
    # kinetic layout: the accent word(s) get their own big line; the rest sit small above / below
    lines, cur, cur_big = [], [], None
    for i in range(a, b + 1):
        big = i in acc
        if cur and big != cur_big:
            lines.append((cur_big, cur)); cur = []
        cur.append(i); cur_big = big
    lines.append((cur_big, cur))
    th = theme(s0)
    inner = "".join(f'<div class="cl{" big" if big else ""}">' + " ".join(f'<span class="cw{" acc" if i in acc else ""}" id="w{i}">{WT[i][0]}</span>' for i in ids) + "</div>" for big, ids in lines)
    pos = " top" if 38.0 <= s0 < 42.24 else ""  # over the hand-held phone, captions move up so the screen stays clear
    cap_html.append(f'<div class="cap {th}{pos}" id="cg{gi}"><div class="ci">{inner}</div></div>')
    cap_js.append([gi, round(s0, 3), round(e, 3), [[i, round(WT[i][1], 3), 1 if i in acc else 0] for i in range(a, b + 1)], ACC[th]])

# ------------------------------------------------------------------ drawing helpers
def glyph(name, fg, size):
    return f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="{fg}"><path d="{ICONS[name]}"/></svg>'


APP = {
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
WALLET_SVG = ('<svg width="66%" height="56%" viewBox="0 0 40 34"><rect x="2" y="2" width="36" height="9" rx="3" fill="#2f80ed"/>'
              '<rect x="2" y="8" width="36" height="9" rx="3" fill="#f2c94c"/><rect x="2" y="14" width="36" height="9" rx="3" fill="#eb5757"/>'
              '<path d="M2 20 h11 a7 5 0 0 0 14 0 h11 v9 a3 3 0 0 1 -3 3 h-30 a3 3 0 0 1 -3 -3z" fill="#e8e8ed"/></svg>')
GWALLET_SVG = ('<svg width="62%" height="52%" viewBox="0 0 46 38"><path d="M4 10 Q4 4 10 4 H36 Q42 4 42 10 V12 H4Z" fill="#4285f4"/>'
               '<path d="M4 12 H42 V18 H4Z" fill="#ea4335"/><path d="M4 18 H42 V24 H4Z" fill="#fbbc04"/>'
               '<path d="M4 24 H42 V28 Q42 34 36 34 H10 Q4 34 4 28Z" fill="#34a853"/></svg>')
WALLET_ICON = lambda s: custom_icon(s, "#000", WALLET_SVG)
GWALLET_ICON = lambda s: custom_icon(s, "#fff", GWALLET_SVG, "box-shadow:inset 0 0 0 1px #e3e3e3")
SMS_ICON = lambda s: app_icon("imessage", s)
SYS = {
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
    return (f'<div class="nt {cls}" id="{id_}"><i class="gs"></i>{icon}<div class="nb"><div class="nh"><b>{title}</b><span>{time}</span></div>'
            f'<div class="nx">{body}</div></div></div>')


def lock_screen(sleep_id=None):
    sl = f'<div class="sleep" id="{sleep_id}"></div>' if sleep_id else ""
    return (f'<div class="scr lock">{status_bar()}<div class="ldate">Tuesday 7 October</div><div class="ltime">9:41</div>'
            '<div class="lbtn" style="left:44px"><svg width="26" height="26" viewBox="0 0 24 24" fill="#fff"><path d="M9 2h6v5l-2 3v12h-2V10L9 7z"/></svg></div>'
            '<div class="lbtn" style="right:44px"><svg width="28" height="28" viewBox="0 0 24 24" fill="#fff"><path d="M4 7h3l2-2h6l2 2h3v12H4z"/><circle cx="12" cy="13" r="3.4" fill="#333"/></svg></div>'
            f'<div class="hbar"></div>{sl}</div>')


def phone3d(id_, screen, layer="", kind="ios", style=""):
    """A phone with real thickness (two edge planes) and a notification layer that lives in front of the glass."""
    cls = "phone android" if kind == "android" else "phone"
    cut = '<div class="punch"></div>' if kind == "android" else '<div class="island"></div>'
    return (f'<div class="pw" id="{id_}" style="{style}"><div class="{cls}"><div class="edge l"></div><div class="edge r"></div>'
            f'<div class="glass">{screen}{cut}<div class="refl"><i></i></div></div></div>'
            f'<div class="nl">{layer}</div></div>')


# ------------------------------------------------------------------ screens and notification layers
NB = [
    ("nB1", SMS_ICON(44), "AX-CAROMA", "2d ago", "Dear customer, you have earned reward points. T&amp;C apply."),
    ("nB2", BREW_ICON(44), "Brew Club", "1d ago", "Your points expire on Sunday. Log in to redeem."),
    ("nB3", app_icon("gmail", 44), "Gmail", "9:12", "Your monthly rewards statement is ready to view."),
]
NH = [
    ("nH1", SMS_ICON(44), "AX-CAROMA", "now", "You've earned 40 reward points. Download our app to redeem."),
    ("nH2", app_icon("whatsapp", 44), "Cafe Aroma", "now", "Show this message at the counter for your points."),
    ("nH3", app_icon("gmail", 44), "Gmail", "now", "Your rewards statement for September is ready."),
    ("nH4", BREW_ICON(44), "Brew Club", "now", "Points expiring Sunday. Sign in to keep them."),
    ("nH5", app_icon("instagram", 44), "Instagram", "now", "cafearoma.bandra sent you a message."),
    ("nH6", app_icon("telegram", 44), "Aroma Club", "now", "New members' offer inside. Tap to view."),
    ("nH7", SMS_ICON(44), "VM-REWRDS", "now", "Your OTP for login is 4821. Do not share."),
]
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
         '</div><div class="hbar"></div></div>')

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

# v5: every category lives in the same stack (generic category names: illustrations, not merchants)
PASSES = [("MOVIE CLUB", "Cinema", "linear-gradient(135deg,#7a1428,#3d0a16)"), ("SALON CLUB", "Salon", "linear-gradient(135deg,#b04a78,#6d2350)"),
          ("STYLE REWARDS", "Store", "linear-gradient(135deg,#0f7f7c,#0a4f57)"), ("LIVE PASS", "Events", "linear-gradient(135deg,#2b2a6b,#14133a)")]
walletJ = (f'<div class="scr light" id="jWallet" style="background:#f2f2f7">{status_bar(True)}<div class="w-h">Wallet<span>+</span></div>'
           + "".join(f'<div class="w-card" style="top:{150 + i * 48}px;background:{bg}"><b>{name}</b><em>{kind}</em></div>' for i, (name, kind, bg) in enumerate(PASSES)) +
           '<img class="w-pass" id="jPass" src="assets/ui/pass-apple.png" alt="" style="top:342px"><div class="hbar dk"></div></div>')
gwalletK = (f'<div class="scr light" style="background:#fff">{status_bar(True)}<div class="gw-h"><span>Wallet</span><i></i></div>'
            + "".join(f'<div class="g-card" style="top:{140 + i * 50}px;background:{bg}"><b>{name.title()}</b></div>' for i, (name, kind, bg) in enumerate(PASSES)) +
            '<img class="w-pass" id="kPassG" src="assets/ui/pass-google.png" alt="" style="top:340px"><div class="hbar dk"></div></div>')

FRAGS = [  # the scattered places loyalty lived, floating round the phone in the question beat
    ("fr1", notif("frn1", SMS_ICON(40), "AX-CAROMA", "", "You've earned 40 points. T&amp;C apply."), -280, -440, 160, -12),
    ("fr2", notif("frn2", app_icon("whatsapp", 40), "Cafe Aroma", "", "Show this at the counter."), 270, -290, 240, 10),
    ("fr3", BREW_ICON(118), -380, 40, 300, -10),
    ("fr4", notif("frn4", app_icon("gmail", 40), "Gmail", "", "Your rewards statement"), 280, 140, 120, 8),
    ("fr5", '<div class="otpcard"><span>OTP</span>4 8 2 1</div>', -290, 420, 220, 8),
    ("fr6", app_icon("instagram", 110), 360, 470, 280, -12),
]
frag_html = "".join(f'<div class="frag" id="{i}" data-x="{x}" data-y="{y}" data-z="{z}" data-r="{r}">{inner}</div>' for i, inner, x, y, z, r in FRAGS)
frag_js = json.dumps([[i, x, y, z, r] for i, _, x, y, z, r in FRAGS])

CHIPS = [("ch1", "Visit", "No. 12", 880), ("ch2", "Bought", "Silk gown", 1020), ("ch3", "Prefers", "Oat milk, extra hot", 1160)]
chips_html = "".join(f'<div class="chip3" id="{i}" style="top:{t}px"><span>{k}</span><b>{v}</b></div>' for i, k, v, t in CHIPS)

# ------------------------------------------------------------------ footage (v5: every category)
# (id, file, start, end, entry, exit): clips overlap the next one by OVL so every cut is a zoom-through dissolve.
# entry: "black" (from black), "zoom" (fades in on top of the outgoing clip), "under" (revealed as the scene above dissolves)
# exit: "zoom" (pushes in and defocuses under the next shot), "burn" (blows out to white into the end card), None
OVL = 0.4
SHOTS = [
    ("vX1", "v5-club-open", 0, 0.95, "black", "zoom"),          # club
    ("vX2", "v5-salon-open", 0.95, 1.8, "zoom", "zoom"),        # salon
    ("vA", "v5-cafe-open", 1.8, 2.72, "zoom", "zoom"),          # café, into the lock screen
    ("vC1", "v5-boutique", 5.12, 6.55, "under", "zoom"),        # "Every counter": a boutique,
    ("vC2", "v5-bar", 6.55, 7.75, "zoom", "zoom"),              # a bar,
    ("vC", "v4-counter", 7.75, 9.12, "zoom", "zoom"),           # a café
    ("vD", "v5-salon", 9.12, 11.28, "zoom", "zoom"),            # "Businesses learned to remember": the salon
    ("vE1", "v5-cinema", 11.28, 12.38, "zoom", "zoom"),         # "Every visit": the cinema
    ("vE2", "v5-boutique-browse", 12.38, 13.48, "zoom", "zoom"),  # "Every purchase": the boutique
    ("vE3", "v5-pour", 13.48, 14.88, "zoom", "zoom"),           # "Every preference": the café
    ("vG", "v5-birthday", 18.1, 21.42, "under", "zoom"),        # "Cafés remembered birthdays"
    ("vL", "scan-at-counter", 38.08, 40.62, "under", "zoom"),
    ("vM", "pay-at-counter", 40.62, 42.24, "zoom", "zoom"),
    ("vO1", "v5-concert", 44.3, 45.17, "under", "zoom"),        # "Now they notice": a concert,
    ("vO2", "v5-club", 45.17, 45.9, "zoom", "zoom"),            # a club,
    ("vO", "v4-notice", 45.9, 46.62, "zoom", "burn"),           # the café counter, blowing out into the logo
]
LEAKS = [9.12, 18.2, 44.36]
videos_html, foot_js = [], []
for k, (vid, f, t0, t1, cin, cout) in enumerate(SHOTS):
    end = t1 + (OVL if cout == "zoom" else 0)
    videos_html.append(f'      <video id="{vid}" class="clip media" src="assets/footage/{f}.mp4" data-start="{t0}" data-duration="{round(end - t0, 3)}" data-track-index="{k % 2 * 3}" muted playsinline></video>')
    foot_js.append([vid, t0, round(end, 3), cin, cout])
videos_html = "\n".join(videos_html)
# the ending's Wallet stack: every category's pass, the Cafe Aroma pass on top
WSTACK = ("".join(f'<div class="ws-card" style="top:{i * 54}px;background:{bg}"><b>{name}</b><em>{kind}</em></div>' for i, (name, kind, bg) in enumerate(PASSES))
          + f'<div id="wsPass" style="top:{len(PASSES) * 54}px"><img src="assets/ui/pass-apple.png" alt=""><i class="gs"></i></div>')

S = {}  # v4.1: the people beats are real footage now (see the <video> elements in v4_template.html)
TPL = (HERE / "v5_template.html").read_text()
rep = {
    "%%DUR%%": str(DUR), "%%DUR_END%%": str(round(DUR - 46.62, 2)),
    "%%PH_B%%": phone3d("pwB", lock_screen("sleepB"), "".join(notif(*n, "onlock") for n in NB)),
    "%%PH_F%%": phone3d("pwF", homeF, notif("nF", app_icon("whatsapp", 44), "Cafe Aroma", "now", "Your usual cold brew is waiting, Aarav. See you soon!", "banner")),
    "%%PH_H%%": phone3d("pwH", lock_screen(), "".join(notif(*n, "onlock") for n in NH)),
    "%%PH_I%%": phone3d("pwI", smsI + chatI + delI + storeI + loginI),
    "%%PH_J%%": phone3d("pwJ", lock_screen() + walletJ),
    "%%PH_K%%": phone3d("pwK", gwalletK, "", "android"),
    "%%PH_N%%": phone3d("pwN", lock_screen(), notif("nN", WALLET_ICON(48), "Wallet", "now", "<b>Cafe Aroma</b> · +18 points. 150 of 150: your free cappuccino is ready.", "hero onlock")),
    "%%NG1%%": notif("nG1", app_icon("whatsapp", 64), "Cafe Aroma", "9:00", "Happy birthday, Aarav! Your next coffee is on us today.", "float"),
    "%%NG2%%": notif("nG2", app_icon("whatsapp", 64), "Cousins", "6:45 pm", "Rohan: wait, whose birthday is it today?", "float"),
    "%%WSTACK%%": WSTACK,
    "%%VIDEOS%%": videos_html, "%%FOOT_JS%%": json.dumps(foot_js), "%%LEAKS%%": " ".join(f"leak({t});" for t in LEAKS),
    "%%FRAGS%%": frag_html, "%%FRAG_JS%%": frag_js, "%%CHIPS%%": chips_html,
    "%%WALLET_ICON%%": WALLET_ICON(64), "%%GWALLET_ICON%%": GWALLET_ICON(64),
    "%%CAPS%%": "\n".join(cap_html), "%%CAP_JS%%": json.dumps(cap_js),
}
html = TPL
for k, v in rep.items():
    html = html.replace(k, v)
for k, v in S.items():
    html = html.replace(f"%%S_{k}%%", v)
assert "%%" not in html, [l for l in html.splitlines() if "%%" in l][:3]
(P / "index.html").write_text(html)
print("index.html written:", len(GROUPS), "caption groups")
