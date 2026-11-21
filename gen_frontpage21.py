#!/usr/bin/env python3
"""Draws the 21 November 2026 front page for make.fun news-image-20261121.

One 1024x1024 image summing up Saturday 21 November 2026: a masthead
naming the day, a lead story on the missiles that fell on Poland, three
hero stories (Wall Street rout, Cyclone Akvan, Palisades verdict), a
numbered world map, 12 featured stories and 38 one-line briefs — 50
stories, 6 continents. All text drawn with PIL from the verified story
list in news-notes.md, so headlines are exactly as written. No downloaded
images, no AI image generation, no clock, no randomness, no network.

Usage: python3 gen_frontpage21.py [variant ...]  (no args = all variants)
Output: candidates/<variant>.png next to this script.
Deterministic: same inputs -> same bytes.
"""
import os
import sys
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "candidates")
os.makedirs(OUT, exist_ok=True)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

_cache = {}


def font(path, size):
    key = (path, size)
    if key not in _cache:
        _cache[key] = ImageFont.truetype(path, size)
    return _cache[key]


def wrap(text, fnt, max_w):
    lines, cur = [], ""
    for word in text.split(" "):
        trial = (cur + " " + word).strip()
        if fnt.getlength(trial) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def fit(text, fnt, max_w):
    """Shrink font size until text fits max_w; returns (font, text)."""
    size = fnt.size
    while size > 8 and fnt.getlength(text) > max_w:
        size -= 1
        fnt = ImageFont.truetype(fnt.path, size)
    return fnt


# ------------------------------------------------------------------ stories
# (n, place, beat, headline, deck, lon, lat)
FEATURED = [
    (1, "POLAND", "NATO",
     "Missiles fall on Poland; NATO calls it a grave violation",
     "Two Russian Kh-101 missiles and a drone came down in the east; Warsaw calls it deliberate provocation and seeks NATO backing.",
     19, 52),
    (2, "WALL STREET", "MARKETS",
     "Stocks plunge; S&P and Dow enter correction",
     "S&P -3.7%, Dow -950, Nasdaq -5.3%; Nasdaq wipes out its 2026 gains. Nvidia -14%; Anthropic -9% a day after its record IPO.",
     -74, 41),
    (3, "UKRAINE", "KYIV",
     "Kryvyi Rih strike kills 2, injures 42",
     "Russian strike hits the city; four children among the injured.",
     33, 48),
    (4, "LOS ANGELES", "JUSTICE",
     "Palisades arsonist convicted at retrial",
     "Jury finds Rinderknecht, 30, guilty on both arson counts; the Jan 2025 fire killed 12 and destroyed ~6,800 structures.",
     -118, 34),
    (5, "ODISHA", "WEATHER",
     "Akvan weakens; rains roll on after landfall",
     "370,000 evacuated, 423 rescue teams out; no major damage reported as heavy rain continues into Saturday.",
     85, 19),
    (6, "BRUSSELS", "EUROPE",
     "UK and EU sign food, carbon and youth deals",
     "PM Burnham signs three agreements with EU leaders at a Brussels summit.",
     4, 51),
    (7, "SHENZHEN", "SUMMIT",
     "Trump\u2013Xi\u2013Putin summit ends with few results",
     "First three-way meeting of the three leaders closes; Europe demands a seat at the table.",
     114, 23),
    (8, "BERLIN", "DIPLOMACY",
     "Europe presses for a place in peace talks",
     "Coalition of the Willing backs a four-party format; Kushner says Moscow agreed.",
     13, 53),
    (9, "WASHINGTON", "COURTS",
     "Second judge blocks Trump's triumphal arch",
     "Court calls the project a \u201crushed job\u201d.",
     -77, 39),
    (10, "WASHINGTON", "SANCTIONS",
     "US sanctions four Iranians over oil revenues",
     "Treasury adds four to the OFAC list for handling Iranian oil money.",
     -95, 38),
    (11, "THE HAGUE", "JUSTICE",
     "World backs ICJ genocide ruling on Myanmar",
     "Switzerland calls the verdict an important step for the Rohingya.",
     4, 52),
    (12, "CALIFORNIA", "TECH",
     "California subpoenas Nvidia over ex-CEO, China ties",
     "State AG probes the chipmaker as its shares plunge 14%.",
     -121, 37),
]

BRIEFS = [
    "HIMARS strike wipes out 20 Russian commanders in Sumy region.",
    "EU Council gives \u20ac1bn in military aid to Ukraine.",
    "UK pledges 1,000+ drones for Ukraine in a \u00a3260m package.",
    "US sanctions Comancheros gang and Italy's 'Ndrangheta.",
    "Trump announces posthumous pardon for baseball star Pete Rose.",
    "US Senate rejects Iran war-powers resolution, 51\u201348.",
    "GTA VI sales pass $1.8bn in a day.",
    "Anthropic shares slide to near their $83 IPO price.",
    "Houthi missile debris falls on Riyadh; coalition strikes Hodeidah.",
    "Iraqi forces enter Jurf al-Sakhar after 12 years of militia rule.",
    "Germany and France agree a deal on ECB leadership.",
    "Modi calls for dialogue and trust at SCO conference in India.",
    "Brazil moves to protect Indigenous land in the Amazon.",
    "Berlin students march against rearmament and conscription.",
    "UN warns ISIS-K is gaining drones in Afghanistan.",
    "Tanker strike and fire reported in the Strait of Hormuz.",
    "ECB board race: Boone and Brunnermeier enter the running.",
    "Ethiopia and Eritrea mass forces on their shared border.",
    "Turkey's government takes over Sozcu TV.",
    "Pew: Islam on track to be the world's largest religion by 2035.",
    "Scientists may have found Earth's \u201cmissing\u201d billion years.",
    "Indonesia asks Google about 19,000 removed YouTube accounts.",
    "South Africa homicides run at 60 a day despite falling murder rate.",
    "Two Danes charged over a Russian plot to kill a Ukrainian rapper.",
    "US approves sale of ~900,000 AI chips to China in six months.",
    "US targets Italian crime syndicate in Canada and an Australian biker gang.",
    "Yemen: Houthis blamed for turning Hodeidah ports into arms routes.",
    "Morocco commits \u20ac366m to a defence manufacturing base by 2035.",
    "Egypt urged to build AI independence on data and computing.",
    "Bosnia presidency chair condemns meddling in the 1995 accord.",
    "Montenegro rejects land concessions in EU membership row.",
    "Ukraine disrupts Russian transport with strikes on the Crimean bridge.",
    "Russia's assault on Kyiv damages a WWII history exhibit.",
    "Kremlin opens its first war monument inside a kindergarten.",
    "US religious-freedom panel says India targets minorities in voter rolls.",
    "India jails man for 19+ years over a plot to kill a US-based Sikh leader.",
    "Fiji declares a national disaster as drought bites.",
    "South Korea's top court clears ex-PM Han Duck-soo.",
]

# Rough continent outlines (lon, lat) — drawn from memory, recognisable
# at map scale; pins are placed by the lon/lat in FEATURED.
CONTINENTS = [
    [(-168, 66), (-140, 70), (-125, 71), (-110, 68), (-95, 69), (-85, 66),
     (-80, 73), (-70, 62), (-55, 52), (-60, 46), (-70, 42), (-75, 35),
     (-80, 26), (-85, 29), (-90, 21), (-95, 19), (-105, 20), (-115, 28),
     (-125, 40), (-125, 49), (-140, 60), (-158, 58), (-168, 66)],
    [(-80, 10), (-70, 12), (-60, 8), (-50, 0), (-40, -5), (-35, -8),
     (-40, -20), (-48, -28), (-55, -35), (-65, -45), (-70, -54),
     (-73, -40), (-72, -20), (-78, -5), (-80, 10)],
    [(-17, 15), (-10, 30), (0, 36), (10, 37), (20, 32), (32, 31),
     (35, 28), (40, 15), (48, 11), (51, 10), (44, 0), (40, -10),
     (35, -20), (30, -30), (20, -35), (15, -30), (12, -18), (9, -1),
     (9, 4), (-8, 5), (-17, 15)],
    [(30, 62), (40, 68), (60, 70), (80, 73), (100, 77), (120, 73),
     (140, 72), (160, 70), (178, 66), (170, 60), (162, 55), (158, 50),
     (142, 45), (140, 38), (130, 35), (127, 40), (120, 30), (110, 20),
     (105, 10), (100, 8), (95, 15), (90, 22), (85, 20), (80, 8),
     (75, 10), (70, 22), (60, 25), (55, 26), (50, 29), (45, 30),
     (40, 32), (35, 36), (30, 36), (30, 42), (30, 50), (30, 62)],
    [(-10, 36), (-9, 43), (-2, 48), (0, 50), (5, 53), (8, 57), (10, 59),
     (18, 56), (21, 55), (24, 59), (28, 60), (30, 62), (25, 65), (20, 70),
     (15, 70), (10, 64), (5, 60), (-5, 58), (-10, 54), (-10, 43), (-10, 36)],
    [(113, -22), (114, -30), (115, -35), (124, -33), (130, -32), (137, -35),
     (140, -38), (147, -39), (150, -37), (153, -27), (150, -22), (146, -19),
     (142, -11), (136, -12), (132, -11), (126, -14), (122, -17), (113, -22)],
]

# ------------------------------------------------------------------ variants
# palette: paper, ink, accent, lead_bg, lead_ink, hero_bg, map_land, pin
PALETTES = {
    "navy": dict(paper="#fdf8ee", ink="#16233f", accent="#b3261e",
                 lead_bg="#16233f", lead_ink="#fdf8ee", hero_bg="#ffffff",
                 map_land="#d8c9a3", pin="#b3261e", rule="#16233f",
                 sub="#5a6478"),
    "crimson": dict(paper="#fdf8ee", ink="#1f1a17", accent="#8c1d18",
                    lead_bg="#8c1d18", lead_ink="#fdf8ee", hero_bg="#ffffff",
                    map_land="#d8c9a3", pin="#8c1d18", rule="#1f1a17",
                    sub="#6b5d52"),
    "teal": dict(paper="#f7f5ef", ink="#0f2a2e", accent="#0e7490",
                 lead_bg="#0f2a2e", lead_ink="#f7f5ef", hero_bg="#ffffff",
                 map_land="#c3d4c9", pin="#b3261e", rule="#0f2a2e",
                 sub="#55696b"),
    "cream": dict(paper="#f6ead2", ink="#2b2118", accent="#9c2b1e",
                  lead_bg="#2b2118", lead_ink="#f6ead2", hero_bg="#fffaf0",
                  map_land="#d9bd8a", pin="#9c2b1e", rule="#2b2118",
                  sub="#6d5b45"),
}

VARIANTS = {
    # name: (palette, lead_story_n, layout, hero_big)
    "v1-navy-poland": ("navy", 1, "standard", False),
    "v2-crimson-poland": ("crimson", 1, "standard", False),
    "v3-teal-poland": ("teal", 1, "standard", False),
    "v4-navy-markets": ("navy", 2, "standard", False),
    "v5-navy-nomap": ("navy", 1, "nomap", False),
    "v6-navy-maptop": ("navy", 1, "maptop", False),
    "v7-cream-poland": ("cream", 1, "standard", False),
    "v8-navy-bigart": ("navy", 1, "standard", True),
}

W, H = 1024, 1024


# ------------------------------------------------------------------ icons
def starburst(d, cx, cy, r, colour, spikes=12):
    pts = []
    import math
    for i in range(spikes * 2):
        ang = math.pi * i / spikes - math.pi / 2
        rr = r if i % 2 == 0 else r * 0.45
        pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
    d.polygon(pts, fill=colour)


def icon_missile(d, x, y, s, ink, accent):
    # diagonal missile with smoke trail
    d.line([(x, y + s * 0.7), (x + s * 0.45, y + s * 0.45)], fill=ink, width=3)
    for i, r in enumerate((3, 5, 7)):
        d.ellipse([x + i * 9 - r, y + s * 0.7 + i * 9 - r,
                   x + i * 9 + r, y + s * 0.7 + i * 9 + r],
                  outline="#9aa3b2", width=2)
    d.polygon([(x + s * 0.55, y + s * 0.1), (x + s * 0.95, y + s * 0.5),
               (x + s * 0.62, y + s * 0.62), (x + s * 0.42, y + s * 0.42)],
              fill=ink)
    d.polygon([(x + s * 0.62, y + s * 0.62), (x + s * 0.78, y + s * 0.78),
               (x + s * 0.62, y + s * 0.82)], fill=accent)
    starburst(d, x + s * 0.85, y + s * 0.15, s * 0.22, accent, 8)


def icon_chart(d, x, y, w, h, accent, ink):
    # falling market chart
    d.line([(x, y + h), (x + w, y + h)], fill=ink, width=2)
    d.line([(x, y), (x, y + h)], fill=ink, width=2)
    pts = [(x + 4, y + 8), (x + w * 0.3, y + h * 0.25),
           (x + w * 0.5, y + h * 0.2), (x + w * 0.7, y + h * 0.55),
           (x + w - 4, y + h - 6)]
    d.line(pts, fill=accent, width=4)
    d.polygon([(x + w - 4, y + h - 6), (x + w - 16, y + h - 6),
               (x + w - 4, y + h - 18)], fill=accent)
    for px, py in pts:
        d.ellipse([px - 3, py - 3, px + 3, py + 3], fill=accent)


def icon_cyclone(d, cx, cy, r, ink, accent):
    import math
    for k in range(3):
        pts = []
        a0 = k * 2.1
        for i in range(28):
            t = i / 27.0
            ang = a0 + t * 4.6
            rr = r * (0.25 + 0.75 * t)
            pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
        d.line(pts, fill=accent if k == 0 else ink, width=3)
    d.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=ink)
    # (no rain drops: they hung below the icon into the hero headline)


def icon_flame(d, cx, cy, s, accent):
    d.polygon([(cx, cy - s), (cx + s * 0.55, cy - s * 0.1),
               (cx + s * 0.7, cy + s * 0.5), (cx + s * 0.2, cy + s * 0.85),
               (cx - s * 0.3, cy + s * 0.85), (cx - s * 0.7, cy + s * 0.45),
               (cx - s * 0.5, cy - s * 0.05)], fill=accent)
    d.polygon([(cx, cy + s * 0.1), (cx + s * 0.3, cy + s * 0.45),
               (cx, cy + s * 0.7), (cx - s * 0.3, cy + s * 0.45)],
              fill="#f5b942")


def icon_gavel(d, x, y, s, ink):
    d.polygon([(x, y + s * 0.15), (x + s * 0.55, y),
               (x + s * 0.7, y + s * 0.18), (x + s * 0.15, y + s * 0.33)],
              fill=ink)
    d.line([(x + s * 0.4, y + s * 0.25), (x + s * 0.85, y + s * 0.7)],
           fill=ink, width=max(3, s // 12))
    d.line([(x + s * 0.05, y + s * 0.85), (x + s * 0.95, y + s * 0.85)],
           fill=ink, width=3)


def icon_globe(d, cx, cy, r, ink, accent):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=ink, width=3)
    d.ellipse([cx - r * 0.45, cy - r, cx + r * 0.45, cy + r],
              outline=ink, width=2)
    d.line([(cx - r, cy), (cx + r, cy)], fill=ink, width=2)
    d.arc([cx - r, cy - r * 0.55, cx + r, cy + r * 0.55], 0, 360,
          fill=ink, width=2)
    d.ellipse([cx + r * 0.35, cy - r * 0.6, cx + r * 0.75, cy - r * 0.2],
              fill=accent)


# ------------------------------------------------------------------ map
def draw_map(d, box, pal, big_pins=False):
    x0, y0, x1, y1 = box
    d.rectangle(box, fill="#eef2f4")
    d.rectangle(box, outline=pal["rule"], width=2)
    mw, mh = x1 - x0, y1 - y0

    def proj(lon, lat):
        return (x0 + (lon + 180.0) / 360.0 * mw,
                y0 + (85.0 - lat) / 145.0 * mh)

    for poly in CONTINENTS:
        d.polygon([proj(lon, lat) for lon, lat in poly], fill=pal["map_land"])
    # UK + Japan dots
    for lon, lat in ((-2, 54), (138, 37), (127, 37)):
        px, py = proj(lon, lat)
        d.ellipse([px - 3, py - 3, px + 3, py + 3], fill=pal["map_land"])
    r = 11 if big_pins else 9
    for n, place, beat, head, deck, lon, lat in FEATURED:
        px, py = proj(lon, lat)
        d.ellipse([px - r, py - r, px + r, py + r], fill=pal["pin"],
                  outline="#ffffff", width=2)
        tf = font(SANS_B, 11 if big_pins else 10)
        tw = tf.getlength(str(n))
        d.text((px - tw / 2, py - 7), str(n), font=tf, fill="#ffffff")
    lab = font(SANS_B, 11)
    d.text((x0 + 8, y0 + 6), "WHERE IT HAPPENED \u2014 12 STORIES, 6 CONTINENTS",
           font=lab, fill=pal["ink"])


# ------------------------------------------------------------------ draw
def draw(variant):
    pal_name, lead_n, layout, big_art = VARIANTS[variant]
    pal = PALETTES[pal_name]
    img = Image.new("RGB", (W, H), pal["paper"])
    d = ImageDraw.Draw(img)
    ink, accent, sub = pal["ink"], pal["accent"], pal["sub"]

    # ---- masthead
    d.rectangle([0, 0, W, 118], fill=pal["paper"])
    d.line([(24, 14), (W - 24, 14)], fill=ink, width=3)
    name_f = font(SERIF_B, 26)
    d.text((24, 22), "THE WORLD IN ONE DAY", font=name_f, fill=ink)
    tag_f = font(SANS_B, 12)
    tag = "50 STORIES  \u00b7  6 CONTINENTS  \u00b7  ONE FRONT PAGE"
    d.text((W - 24 - tag_f.getlength(tag), 32), tag, font=tag_f, fill=accent)
    date_f = font(SERIF_B, 46)
    date_txt = "SATURDAY 21 NOVEMBER 2026"
    d.text((24, 56), date_txt, font=date_f, fill=accent)
    d.line([(24, 112), (W - 24, 112)], fill=ink, width=2)
    d.line([(24, 116), (W - 24, 116)], fill=ink, width=1)

    lead = FEATURED[lead_n - 1]
    heroes = [s for s in FEATURED if s[0] in (2, 4, 5) and s[0] != lead_n]
    if lead_n in (2, 4, 5):
        heroes = [s for s in FEATURED if s[0] in (1, 2, 4, 5)
                  and s[0] != lead_n][:3]
    else:
        heroes = [s for s in FEATURED if s[0] in (2, 4, 5)]

    y = 126
    map_h = 0 if layout == "nomap" else 150
    if layout == "maptop":
        draw_map(d, (24, y, W - 24, y + map_h), pal, big_art)
        y += map_h + 10

    # ---- lead banner
    lead_h = 168
    d.rectangle([24, y, W - 24, y + lead_h], fill=pal["lead_bg"])
    d.rectangle([24, y, W - 24, y + lead_h], outline=ink, width=2)
    lx = 44
    kick = font(SANS_B, 14)
    d.text((lx, y + 14), "%s  \u00b7  %s  \u00b7  LEAD STORY" % (lead[1], lead[2]),
           font=kick, fill="#f5b942")
    hf = font(SERIF_B, 38)
    lines = wrap(lead[3], hf, 620)
    # shrink the headline until it fits two lines (the lead block has no
    # room for a third line); deterministic, same input -> same size.
    _sz = 38
    while len(lines) > 2 and _sz > 28:
        _sz -= 1
        hf = font(SERIF_B, _sz)
        lines = wrap(lead[3], hf, 620)
    yy = y + 40
    for ln in lines[:2]:
        d.text((lx, yy), ln, font=hf, fill=pal["lead_ink"])
        yy += 44
    df = font(SANS, 16)
    dlines = wrap(lead[4], df, 620)
    yy += 4
    for ln in dlines[:2]:
        d.text((lx, yy), ln, font=df, fill="#d7dce6")
        yy += 22
    # lead art: missile + burst on the right
    ax = 700
    icon_missile(d, ax, y + 30, 110, "#d7dce6", "#f5b942")
    starburst(d, ax + 210, y + 52, 26, "#f5b942", 10)
    _cap = "NOWY LIPOWIEC \u00b7 POLAND"
    _cf = font(SANS_B, 12)
    d.text((W - 24 - _cf.getlength(_cap), y + 118), _cap,
           font=_cf, fill="#9aa3b2")
    y += lead_h + 10

    # ---- hero trio
    hero_h = 172
    cw = (W - 48 - 20) // 3
    arts = {2: "chart", 4: "flame", 5: "cyclone", 1: "missile"}
    for i, s in enumerate(heroes):
        x0 = 24 + i * (cw + 10)
        d.rectangle([x0, y, x0 + cw, y + hero_h], fill=pal["hero_bg"],
                    outline=ink, width=2)
        d.rectangle([x0, y, x0 + cw, y + 26], fill=accent)
        d.text((x0 + 10, y + 5), "%s  \u00b7  %s" % (s[1], s[2]),
               font=font(SANS_B, 12), fill="#ffffff")
        art = arts.get(s[0], "globe")
        ah = 62 if big_art else 48
        if art == "chart":
            icon_chart(d, x0 + 12, y + 34, 96, ah, accent, ink)
        elif art == "cyclone":
            icon_cyclone(d, x0 + 60, y + 58, 26, ink, accent)
        elif art == "flame":
            icon_flame(d, x0 + 60, y + 62, 26, accent)
            # gavel small and high, clear of the hero headline below
            icon_gavel(d, x0 + 232, y + 38, 40, ink)
        else:
            icon_globe(d, x0 + 60, y + 60, 26, ink, accent)
        hf2 = font(SERIF_B, 17)
        hl = wrap(s[3], hf2, cw - 20)
        yy = y + 34 + ah + 6
        for ln in hl[:2]:
            d.text((x0 + 10, yy), ln, font=hf2, fill=ink)
            yy += 21
        df2 = font(SANS, 11)
        dl = wrap(s[4], df2, cw - 20)
        for ln in dl[:2]:
            if yy + 13 > y + hero_h - 4:
                break
            d.text((x0 + 10, yy), ln, font=df2, fill=sub)
            yy += 14
    y += hero_h + 10

    # ---- map (standard layout)
    if layout == "standard":
        draw_map(d, (24, y, W - 24, y + map_h), pal, big_art)
        y += map_h + 10

    # ---- featured grid: 12 stories, 2 columns
    grid_top = y
    grid_h = 864 - grid_top if layout != "nomap" else 864 - grid_top
    col_w = (W - 48 - 16) // 2
    row_h = grid_h // 6
    for idx, s in enumerate(FEATURED):
        col = idx % 2
        row = idx // 2
        x0 = 24 + col * (col_w + 16)
        yy = grid_top + row * row_h
        d.rectangle([x0, yy, x0 + 26, yy + 26], fill=accent)
        tf = font(SANS_B, 14)
        d.text((x0 + 8, yy + 4), str(s[0]), font=tf, fill="#ffffff")
        kf = font(SANS_B, 11)
        d.text((x0 + 34, yy + 1), "%s \u00b7 %s" % (s[1], s[2]),
               font=kf, fill=accent)
        hf3 = font(SERIF_B, 15)
        hl = wrap(s[3], hf3, col_w - 34)
        ty = yy + 18
        for ln in hl[:2]:
            d.text((x0 + 34, ty), ln, font=hf3, fill=ink)
            ty += 18
        df3 = font(SANS, 11)
        dl = wrap(s[4], df3, col_w - 34)
        for ln in dl[:2]:
            if ty + 13 > yy + row_h - 2:
                break
            d.text((x0 + 34, ty), ln, font=df3, fill=sub)
            ty += 14
        if row < 5:
            d.line([(x0, yy + row_h - 5), (x0 + col_w, yy + row_h - 5)],
                   fill="#c9bfa5", width=1)
    y = 864

    # ---- briefs
    d.line([(24, y), (W - 24, y)], fill=ink, width=2)
    bf = font(SANS_B, 12)
    d.text((24, y + 6), "ALSO TODAY \u2014 38 MORE STORIES",
           font=bf, fill=ink)
    d.text((W - 24 - bf.getlength("13\u201350"), y + 6), "13\u201350",
           font=bf, fill=accent)
    bcol_w = (W - 48 - 24) // 3
    bf2 = font(SANS, 10)
    per_col = 13
    for ci in range(3):
        x0 = 24 + ci * (bcol_w + 12)
        yy = y + 26
        for j in range(per_col):
            k = ci * per_col + j
            if k >= len(BRIEFS):
                break
            txt = "%d. %s" % (13 + k, BRIEFS[k])
            for ln in wrap(txt, bf2, bcol_w):
                d.text((x0, yy), ln, font=bf2, fill=ink)
                yy += 12
            yy += 1
    # ---- footer
    d.line([(24, 996), (W - 24, 996)], fill=ink, width=2)
    ff = font(SANS, 10)
    d.text((24, 1002),
           "Sources: Reuters, CNN, WSJ, MarketWatch, AP, The Hindu, IMD \u2014 "
           "verified reports of 21 Nov 2026.",
           font=ff, fill=sub)
    d.text((W - 24 - ff.getlength("THE WORLD IN ONE DAY"),
            1002), "THE WORLD IN ONE DAY", font=font(SANS_B, 10), fill=ink)
    return img


def main():
    names = sys.argv[1:] or list(VARIANTS)
    for name in names:
        img = draw(name)
        path = os.path.join(OUT, name + ".png")
        img.save(path, optimize=True)
        size = os.path.getsize(path)
        print(name, img.size, size, "bytes",
              "OK" if size <= 1048576 else "TOO BIG")


if __name__ == "__main__":
    main()
