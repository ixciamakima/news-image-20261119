#!/usr/bin/env python3
"""Render the front page for Thursday 19 November 2026.

Deterministic: no network, no randomness, no timestamps. Run with
``python3 render.py``; writes entry.png next to this file.
Only Pillow (plus the standard library) is required.
"""

import hashlib
import os
import sys

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "entry.png")

W, H = 1024, 1024
PAPER = (250, 248, 240)
INK = (16, 16, 16)
OCEAN = (198, 220, 232)
LAND = (232, 222, 198)
LAND_EDGE = (150, 140, 115)
GRID_LINE = (255, 255, 255)
YELLOW = (255, 210, 31)
RED = (178, 34, 34)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


F_SERIF_B = lambda s: font("DejaVuSerif-Bold.ttf", s)
F_SANS_B = lambda s: font("DejaVuSans-Bold.ttf", s)
F_SANS = lambda s: font("DejaVuSans.ttf", s)

# ---------------------------------------------------------------- stories
# n, headline, summary, lat, lon, dx, dy, region
# Regions: EUR Europe, MEA Middle East, ASI Asia, NAM North America,
# SAM South America, AFR Africa, OCE Oceania.
STORIES = [
    (1, "Summit of three powers", "Trump, Xi, Putin meet in Shenzhen", 22.55, 114.06, 0, 0, "ASI"),
    (2, "GTA VI is out", "Rockstar epic launches to 99 on Metacritic", 40.71, -74.00, -16, -14, "NAM"),
    (3, "Myanmar guilty of genocide", "ICJ rules on 2017 crackdown", 52.07, 4.30, 0, 0, "EUR"),
    (4, "Anthropic's record IPO", "$81bn raised, valued at $1.5tn", 40.71, -74.00, 16, -14, "NAM"),
    (5, "Wall Street sinks", "Dow -2.2%, S&P -2.0%, Nasdaq -2.3%", 40.71, -74.00, -16, 14, "NAM"),
    (6, "COP31 draft drops fossil fuels", "Deal text thins in Antalya", 36.90, 30.70, 12, -12, "EUR"),
    (7, "Missile hits Riyadh tower", "Houthi strike on PIF building, reports say", 24.71, 46.68, 0, 0, "MEA"),
    (8, "Israel pushes into Gaza", "Ground op goes beyond the Yellow Line", 31.50, 34.47, -10, 10, "MEA"),
    (9, "Europe open to Russia talks", "Leaders coordinate in Berlin", 52.52, 13.40, 0, 0, "EUR"),
    (10, "UK sends 1,000 drones", "Long-range kit pledged to Kyiv", 51.50, -0.13, -20, -12, "EUR"),
    (11, "Putin vows painful reply", "After new strikes on the Crimean Bridge", 55.76, 37.62, 0, 0, "EUR"),
    (12, "Crimean Bridge hit again", "Russia reports a fresh attack", 45.36, 36.47, 0, 0, "EUR"),
    (13, "Boat sinks off Senegal", "Dozens missing, about 100 aboard", 14.72, -17.47, 0, 0, "AFR"),
    (14, "Venezuela signs US deal", "Military pact months after Maduro's fall", 10.49, -66.88, 0, 0, "SAM"),
    (15, "Haiti army battles gangs", "Push to retake a key corridor", 18.54, -72.34, 0, 0, "SAM"),
    (16, "Kenya picks US miners", "Mrima Hill deal beats Chinese bid", -1.29, 36.82, -12, 6, "AFR"),
    (17, "Uganda landslide justice", "Survivors take their case to the UN", 0.35, 32.58, 12, -8, "AFR"),
    (18, "Cyclone Akvan nears India", "300,000 evacuated in Odisha", 20.30, 85.83, 0, 0, "ASI"),
    (19, "Takaichi meets Putin", "Japan PM talks at APEC sidelines", 35.68, 139.69, -10, -8, "ASI"),
    (20, "Kim stays home", "North Korea leader skips APEC summit", 39.04, 125.75, 0, 0, "ASI"),
    (21, "Two Americans raised", "Trump aide presses China on detainees", 38.90, -77.04, -10, -10, "NAM"),
    (22, "Pete Rose pardoned", "Trump clears baseball's banned hit king", 39.10, -84.51, -10, -8, "NAM"),
    (23, "Fiona the hippo dies", "Cincinnati Zoo star after swallowing hat", 39.10, -84.51, 10, 8, "NAM"),
    (24, "Voyager 1, a light-day out", "NASA probe phones home", 28.39, -80.61, 10, -8, "NAM"),
    (25, "Chase data leaked", "Thousands of emails in cyberattack", 40.71, -74.00, 16, 14, "NAM"),
    (26, "Iran war bill: $48bn", "Senate blocks bid to end the war", 38.90, -77.04, 10, 10, "NAM"),
    (27, "UK-EU summit", "London and Brussels try to patch ties", 51.50, -0.13, 20, -12, "EUR"),
    (28, "Covid inquiry reports", "UK findings on testing and tracing", 51.50, -0.13, -20, 12, "EUR"),
    (29, "Italy hit by hoaxes", "Hacking wave 'aims to destabilise'", 41.90, 12.50, -14, -10, "EUR"),
    (30, "California probes Nvidia", "Over AI chips reaching China", 38.58, -121.49, 10, -8, "NAM"),
    (31, "Alibaba cloud soars 53%", "But shares slip on earnings miss", 30.27, 120.15, 0, 0, "ASI"),
    (32, "China chip fears grow", "Tech firms dread US AI curbs", 39.90, 116.40, 0, 0, "ASI"),
    (33, "Bank of Japan hints hike", "Chief plays down soft spending", 35.68, 139.69, 10, 8, "ASI"),
    (34, "Train heist busted", "$22m cargo ring charged in LA", 34.05, -118.24, -10, 8, "NAM"),
    (35, "Shelton, Zverev advance", "ATP Finals semi-finalists set", 45.07, 7.69, 16, -12, "EUR"),
    (36, "Kangaroos reach final", "Australia beats Samoa 44-12 in Sydney", -33.87, 151.21, 0, 0, "OCE"),
    (37, "Iglesias faces court probe", "Inquiry over alleged offences", 40.42, -3.70, 0, 0, "EUR"),
    (38, "Ancient library reopens", "Rome treasure restored to public", 41.90, 12.50, 14, 10, "EUR"),
    (39, "Susan Smith denied parole", "32 years after her sons' deaths", 34.00, -81.03, 0, 0, "NAM"),
    (40, "Pastor guilty in Haiti plot", "Role in president's killing", 25.76, -80.19, -12, 8, "NAM"),
]

REGION_COLORS = {
    "EUR": (31, 119, 180),
    "MEA": (230, 126, 34),
    "ASI": (201, 42, 42),
    "NAM": (44, 160, 44),
    "SAM": (148, 103, 189),
    "AFR": (140, 86, 75),
    "OCE": (23, 190, 207),
}
REGION_NAMES = {
    "EUR": "Europe",
    "MEA": "Middle East",
    "ASI": "Asia",
    "NAM": "N. America",
    "SAM": "S. America",
    "AFR": "Africa",
    "OCE": "Oceania",
}

# ------------------------------------------------------------- continents
# Rough lon/lat outlines, drawn on an equirectangular projection.
NORTH_AMERICA = [(-168, 66), (-165, 60), (-158, 58), (-152, 60), (-140, 60),
                 (-135, 58), (-130, 54), (-125, 49), (-124, 42), (-120, 34),
                 (-114, 29), (-110, 24), (-105, 20), (-97, 16), (-94, 17),
                 (-90, 14), (-86, 12), (-83, 9), (-79, 9), (-81, 13),
                 (-83, 15), (-87, 16), (-88, 18), (-90, 21), (-91, 19),
                 (-97, 26), (-93, 30), (-89, 30), (-84, 30), (-81, 26),
                 (-80, 32), (-76, 35), (-74, 40), (-70, 42), (-68, 45),
                 (-65, 44), (-60, 47), (-55, 52), (-60, 55), (-64, 58),
                 (-68, 58), (-72, 62), (-78, 62), (-85, 66), (-92, 66),
                 (-95, 69), (-110, 68), (-125, 70), (-140, 70), (-155, 71),
                 (-165, 68)]
GREENLAND = [(-58, 64), (-52, 60), (-44, 60), (-40, 64), (-32, 68),
             (-22, 70), (-20, 74), (-25, 76), (-35, 78), (-50, 76),
             (-58, 74), (-60, 70)]
SOUTH_AMERICA = [(-79, 9), (-77, 4), (-80, -3), (-81, -6), (-77, -12),
                 (-72, -18), (-70, -23), (-70, -30), (-72, -37), (-73, -44),
                 (-74, -50), (-70, -54), (-66, -55), (-68, -50), (-65, -45),
                 (-62, -41), (-58, -38), (-52, -33), (-48, -28), (-41, -23),
                 (-39, -17), (-35, -9), (-35, -6), (-40, -3), (-44, -2),
                 (-50, 0), (-53, 4), (-58, 6), (-62, 9), (-68, 11),
                 (-72, 12), (-77, 8)]
AFRICA = [(-17, 15), (-16, 20), (-15, 27), (-10, 31), (-6, 34), (0, 36),
          (10, 37), (11, 34), (19, 33), (25, 32), (32, 31), (34, 28),
          (35, 24), (37, 20), (39, 18), (43, 12), (48, 11), (51, 12),
          (46, 5), (42, 0), (40, -5), (40, -12), (36, -18), (33, -26),
          (28, -33), (20, -35), (17, -32), (15, -27), (13, -18), (12, -10),
          (13, -5), (9, 4), (4, 6), (-8, 5), (-13, 8), (-17, 12)]
EUROPE = [(-10, 36), (-9, 38), (-9, 43), (-2, 44), (-1, 46), (-4, 48),
          (-2, 50), (0, 51), (3, 53), (8, 55), (8, 57), (10, 59), (6, 62),
          (12, 65), (18, 69), (25, 71), (30, 70), (32, 68), (40, 68),
          (44, 66), (48, 68), (52, 68), (55, 68), (58, 69), (60, 69),
          (65, 69), (68, 68), (60, 66), (55, 64), (50, 60), (45, 58),
          (40, 55), (38, 52), (35, 50), (30, 50), (28, 48), (25, 46),
          (23, 44), (20, 42), (19, 40), (22, 38), (26, 38), (28, 36),
          (23, 36), (20, 38), (16, 38), (14, 38), (12, 40), (10, 42),
          (8, 44), (5, 43), (3, 42), (0, 40), (-2, 37), (-6, 36)]
ASIA = [(30, 36), (28, 40), (30, 45), (32, 50), (35, 55), (40, 60),
        (45, 65), (50, 68), (55, 68), (60, 69), (65, 69), (70, 72),
        (75, 73), (80, 73), (85, 75), (90, 75), (95, 76), (100, 77),
        (105, 77), (110, 74), (115, 73), (120, 73), (125, 72), (130, 72),
        (135, 72), (140, 72), (145, 72), (150, 70), (155, 70), (160, 69),
        (162, 66), (160, 62), (158, 58), (156, 52), (150, 60), (142, 55),
        (140, 50), (138, 46), (135, 43), (132, 43), (130, 42), (127, 40),
        (126, 38), (124, 38), (122, 38), (120, 35), (119, 32), (121, 28),
        (118, 25), (115, 22), (110, 20), (108, 18), (105, 10), (103, 8),
        (100, 7), (98, 10), (97, 15), (94, 17), (92, 21), (89, 22),
        (86, 20), (83, 18), (80, 13), (80, 7), (77, 8), (76, 10),
        (73, 16), (72, 20), (70, 23), (67, 24), (66, 25), (62, 22),
        (61, 25), (58, 25), (57, 26), (54, 27), (52, 28), (50, 29),
        (48, 30), (44, 30), (40, 32), (36, 33), (36, 36)]
AUSTRALIA = [(113, -22), (114, -30), (115, -33), (118, -35), (124, -33),
             (129, -32), (132, -32), (135, -35), (137, -35), (140, -38),
             (145, -38), (150, -37), (153, -32), (153, -27), (150, -22),
             (146, -19), (142, -15), (142, -11), (137, -12), (135, -15),
             (132, -12), (130, -13), (126, -14), (122, -17), (118, -20)]
JAPAN = [(130, 31), (133, 34), (137, 35), (140, 36), (141, 39), (141, 42),
         (143, 44), (145, 44), (142, 42), (141, 38), (139, 35), (136, 33),
         (132, 33)]
BRITAIN = [(-5, 50), (-3, 53), (-5, 56), (-3, 58), (-1, 57), (0, 53),
           (1, 51), (-2, 50)]
NEW_ZEALAND = [(167, -45), (170, -43), (174, -41), (176, -38), (178, -37),
               (175, -40), (172, -43), (168, -46)]
MADAGASCAR = [(44, -16), (47, -15), (50, -16), (49, -20), (47, -25),
              (45, -25), (43, -21), (43, -17)]
INDONESIA = [(95, 5), (100, 0), (105, -6), (110, -7), (114, -8), (119, -9),
             (120, -10), (124, -10), (128, -8), (131, -4), (136, -2),
             (140, -3), (141, -1), (138, 0), (132, 0), (128, 2), (124, 1),
             (120, 1), (116, 0), (112, -1), (108, -3), (104, -1), (100, 2),
             (97, 4)]
CONTINENTS = [NORTH_AMERICA, GREENLAND, SOUTH_AMERICA, AFRICA, EUROPE,
              ASIA, AUSTRALIA, JAPAN, BRITAIN, NEW_ZEALAND, MADAGASCAR,
              INDONESIA]


def wrap(text, fnt, width):
    """Greedy word wrap; returns a list of lines that fit `width`."""
    lines, cur = [], ""
    for word in text.split():
        trial = word if not cur else cur + " " + word
        if fnt.getlength(trial) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines

# ------------------------------------------------------------- map geometry
MAP_X0, MAP_Y0, MAP_W, MAP_H = 132, 316, 760, 300
LAT_TOP, LAT_BOT = 84.0, -58.0


def project(lon, lat):
    x = MAP_X0 + (lon + 180.0) / 360.0 * MAP_W
    y = MAP_Y0 + (LAT_TOP - lat) / (LAT_TOP - LAT_BOT) * MAP_H
    return x, y


# ------------------------------------------------------------- scene panels
def draw_gta(d, x, y, w, h):
    for i in range(h):
        t = i / max(1, h - 1)
        r = int(255 - 60 * t)
        g = int(120 + 60 * t)
        b = int(140 + 40 * t)
        d.line([(x, y + i), (x + w, y + i)], fill=(r, g, b))
    d.ellipse([x + w // 2 - 26, y + 8, x + w // 2 + 26, y + 60],
              fill=(255, 214, 90))
    d.rectangle([x, y + h - 26, x + w, y + h], fill=(30, 30, 46))
    d.rectangle([x + 18, y + h - 44, x + 78, y + h - 26], fill=(20, 20, 34))
    d.rectangle([x + 26, y + h - 40, x + 44, y + h - 32], fill=(150, 220, 255))
    d.rectangle([x + 50, y + h - 40, x + 70, y + h - 32], fill=(150, 220, 255))
    d.ellipse([x + 28, y + h - 24, x + 40, y + h - 12], fill=(10, 10, 10))
    d.ellipse([x + 58, y + h - 24, x + 70, y + h - 12], fill=(10, 10, 10))
    for px, py, s in [(x + w - 42, y + 14, 16), (x + w - 26, y + 26, 12)]:
        d.line([(px, py + s), (px, py)], fill=(20, 60, 30), width=3)
        for a in range(5):
            ang = 3.14159 * (0.15 + 0.175 * a)
            ex = px + int(13 * __import__("math").cos(ang))
            ey = py - int(11 * __import__("math").sin(ang))
            d.line([(px, py), (ex, ey)], fill=(20, 60, 30), width=3)
    d.text((x + 10, y + 6), "GTA VI", font=F_SANS_B(24), fill=(255, 255, 255),
           stroke_width=2, stroke_fill=(0, 0, 0))
    d.rectangle([x, y + h - 18, x + w, y + h], fill=(0, 0, 0))
    d.text((x + 8, y + h - 17), "OUT NOW  -  99/100",
           font=F_SANS_B(13), fill=(255, 255, 255))


def draw_icj(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(38, 48, 84))
    d.rectangle([x, y + h - 18, x + w, y + h], fill=(0, 0, 0))
    cx, cy = x + w // 2, y + 16
    d.line([(cx, cy), (cx, y + h - 26)], fill=(212, 175, 55), width=4)
    d.line([(cx - 52, cy + 6), (cx + 52, cy + 6)], fill=(212, 175, 55), width=4)
    for sx in (cx - 52, cx + 52):
        d.line([(sx, cy + 6), (sx, cy + 26)], fill=(212, 175, 55), width=2)
        d.arc([sx - 20, cy + 16, sx + 20, cy + 44], 0, 180,
              fill=(212, 175, 55), width=3)
    d.ellipse([cx - 7, cy - 7, cx + 7, cy + 7], fill=(212, 175, 55))
    d.text((x + 8, y + h - 17), "ICJ: GENOCIDE VERDICT",
           font=F_SANS_B(13), fill=(255, 255, 255))


def draw_voyager(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(8, 10, 26))
    import random as _r
    rng = _r.Random(19)
    for _ in range(46):
        sx = x + rng.randint(2, w - 3)
        sy = y + rng.randint(2, h - 24)
        d.point((sx, sy), fill=(255, 255, 255))
    d.line([(x + 52, y + 44), (x + 128, y + 30)], fill=(200, 200, 200), width=3)
    d.polygon([(x + 118, y + 18), (x + 150, y + 26), (x + 128, y + 44),
               (x + 104, y + 34)], fill=(180, 180, 190))
    d.rectangle([x + 44, y + 40, x + 62, y + 50], fill=(220, 220, 220))
    d.line([(x + 52, y + 50), (x + 40, y + 62)], fill=(200, 200, 200), width=2)
    d.line([(x + 52, y + 50), (x + 66, y + 62)], fill=(200, 200, 200), width=2)
    d.rectangle([x, y + h - 18, x + w, y + h], fill=(0, 0, 0))
    d.text((x + 8, y + h - 17), "VOYAGER 1: 1 LIGHT-DAY",
           font=F_SANS_B(13), fill=(255, 255, 255))


def draw_cyclone(d, x, y, w, h):
    for i in range(h):
        t = i / max(1, h - 1)
        d.line([(x, y + i), (x + w, y + i)],
               fill=(int(90 + 60 * t), int(110 + 60 * t), int(130 + 60 * t)))
    for rx in range(x + 12, x + w - 8, 22):
        d.line([(rx, y + 10), (rx - 6, y + 30)], fill=(220, 230, 255), width=2)
        d.line([(rx + 8, y + 34), (rx + 2, y + 54)], fill=(220, 230, 255), width=2)
    d.polygon([(x + 60, y + 44), (x + 110, y + 44), (x + 100, y + 58),
               (x + 70, y + 58)], fill=(120, 60, 40))
    d.rectangle([x + 68, y + 58, x + 102, y + h - 18], fill=(150, 90, 60))
    d.rectangle([x, y + h - 18, x + w, y + h], fill=(0, 0, 0))
    d.text((x + 8, y + h - 17), "AKVAN: 300K EVACUATED",
           font=F_SANS_B(13), fill=(255, 255, 255))


# ------------------------------------------------------------- page sections
def draw_masthead(d):
    d.rectangle([0, 0, W, 54], fill=INK)
    d.text((W // 2, 8), "THE WORLD IN ONE DAY", font=F_SERIF_B(38),
           fill=(255, 255, 255), anchor="ma")
    d.rectangle([0, 54, W, 92], fill=YELLOW)
    d.text((16, 61), "THURSDAY 19 NOVEMBER 2026", font=F_SANS_B(30),
           fill=INK)
    d.text((W - 16, 66), "40 STORIES  •  7 REGIONS", font=F_SANS_B(16),
           fill=INK, anchor="ra")


def draw_lead(d):
    d.text((16, 100), "LEAD STORY  —  SHENZHEN, CHINA", font=F_SANS_B(13),
           fill=RED)
    d.text((16, 116), "THREE LEADERS,", font=F_SERIF_B(38), fill=INK)
    d.text((16, 154), "ONE TABLE", font=F_SERIF_B(38), fill=INK)
    dek = ("Donald Trump, Xi Jinping and Vladimir Putin meet for the "
           "first time as a trio and issue a joint \u201cpeace "
           "declaration\u201d on nuclear risk and UN reform.")
    yy = 196
    for line in wrap(dek, F_SANS(15), 580):
        d.text((16, yy), line, font=F_SANS(15), fill=(40, 40, 40))
        yy += 19
    yy += 4
    bullets = [
        "GTA VI launches worldwide after 13 years \u2014 $1.84bn day one, SensorTower says.",
        "World court: Myanmar committed genocide against the Rohingya in 2017.",
        "Anthropic's $81bn IPO is the biggest ever, yet Wall Street sinks 2%.",
    ]
    for b in bullets:
        d.text((16, yy), "\u2022", font=F_SANS_B(13), fill=RED)
        d.text((34, yy), b, font=F_SANS(13), fill=(40, 40, 40))
        yy += 16
    px, py = 612, 100
    pw, ph = 192, 84
    draw_gta(d, px, py, pw, ph)
    draw_icj(d, px + pw + 12, py, pw, ph)
    draw_voyager(d, px, py + ph + 8, pw, ph)
    draw_cyclone(d, px + pw + 12, py + ph + 8, pw, ph)


def draw_map(d):
    d.text((16, 296), "WHERE IT HAPPENED", font=F_SANS_B(16), fill=INK)
    d.text((212, 298), "— 40 stories numbered on the map  •  equirectangular, lat -58\u00b0 to 84\u00b0",
           font=F_SANS(13), fill=(80, 80, 80))
    d.rectangle([MAP_X0, MAP_Y0, MAP_X0 + MAP_W, MAP_Y0 + MAP_H], fill=OCEAN,
                outline=INK, width=2)
    for lon in range(-180, 181, 30):
        gx, _ = project(lon, 84)
        d.line([(gx, MAP_Y0), (gx, MAP_Y0 + MAP_H)], fill=(255, 255, 255), width=1)
    for lat in range(-60, 91, 30):
        _, gy = project(0, lat)
        d.line([(MAP_X0, gy), (MAP_X0 + MAP_W, gy)], fill=(255, 255, 255), width=1)
    for poly in CONTINENTS:
        pts = [project(lon, lat) for lon, lat in poly]
        d.polygon(pts, fill=LAND, outline=LAND_EDGE)
    d.text((MAP_X0 + 8, MAP_Y0 + MAP_H - 22), "ATLANTIC",
           font=F_SANS_B(13), fill=(90, 110, 130))
    d.text((MAP_X0 + MAP_W - 72, MAP_Y0 + 8), "PACIFIC",
           font=F_SANS_B(13), fill=(90, 110, 130))
    for n, head, summ, lat, lon, dx, dy, region in STORIES:
        ax, ay = project(lon, lat)
        cx, cy = ax + dx, ay + dy
        if dx or dy:
            d.line([(ax, ay), (cx, cy)], fill=(90, 90, 90), width=1)
        d.ellipse([cx - 9, cy - 9, cx + 9, cy + 9],
                  fill=REGION_COLORS[region], outline=INK, width=1)
        d.text((cx, cy - 1), str(n), font=F_SANS_B(10), fill=(255, 255, 255),
               anchor="mm")
    # left legend
    d.text((16, 320), "REGIONS", font=F_SANS_B(13), fill=INK)
    ly = 342
    for key in ("EUR", "MEA", "ASI", "NAM", "SAM", "AFR", "OCE"):
        d.rectangle([16, ly, 28, ly + 12], fill=REGION_COLORS[key],
                    outline=INK)
        d.text((33, ly - 1), REGION_NAMES[key], font=F_SANS(13), fill=INK)
        ly += 20
    # right notes
    d.text((910, 320), "THE MAP", font=F_SANS_B(13), fill=INK)
    note = ("Every numbered dot marks where a story happened. "
            "Colour shows its region; a thin line links a shifted "
            "label to its true place.")
    yy = 342
    for line in wrap(note, F_SANS(13), 98):
        d.text((930, yy), line, font=F_SANS(13), fill=(60, 60, 60))
        yy += 16


def draw_grid(d):
    d.text((16, 622), "THE DAY IN 40 STORIES", font=F_SANS_B(16), fill=INK)
    d.text((270, 624), "— headline, then what happened, in one line each",
           font=F_SANS(13), fill=(80, 80, 80))
    d.line([(16, 642), (W - 16, 642)], fill=INK, width=2)
    col_w = 484
    row_h = 16
    y0 = 646
    problems = []
    for i, (n, head, summ, lat, lon, dx, dy, region) in enumerate(STORIES):
        col = 0 if i < 20 else 1
        row = i if i < 20 else i - 20
        x = 16 if col == 0 else 524
        y = y0 + row * row_h
        num = "%2d" % n
        d.text((x, y), num, font=F_SANS_B(13), fill=REGION_COLORS[region])
        tx = x + 26
        d.text((tx, y), head, font=F_SANS_B(13), fill=INK)
        hx = tx + F_SANS_B(13).getlength(head)
        rest = "  \u2014  " + summ
        if F_SANS(13).getlength(rest) > col_w - (hx - tx) - 4:
            problems.append(n)
        d.text((hx, y), rest, font=F_SANS(13), fill=(40, 40, 40))
    return problems


def draw_markets(d):
    d.rectangle([0, 970, W, H], fill=INK)
    d.text((16, 976), "MARKETS   DOW 49,097 -2.19%   S&P 7,176 -2.02%   "
           "NASDAQ 23,879 -2.25%   GOLD $3,686 -1.5%   BRENT $91.98 +0.0%",
           font=F_SANS_B(13), fill=(255, 255, 255))
    d.text((16, 997), "BITCOIN $61,590 -1.5%   VIX 28.44 +15.8%      "
           "Sources: Reuters, BBC, AP, ATP Tour, Investopedia",
           font=F_SANS(13), fill=(200, 200, 200))


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    draw_masthead(d)
    draw_lead(d)
    draw_map(d)
    problems = draw_grid(d)
    draw_markets(d)
    img.save(OUT, optimize=True)
    size = os.path.getsize(OUT)
    digest = hashlib.sha256(open(OUT, "rb").read()).hexdigest()
    print("saved entry.png bytes=%d sha256=%s" % (size, digest))
    if problems:
        print("LONG LINES (story numbers over column width): %s" % problems)
    else:
        print("all grid lines fit")
    return 0


if __name__ == "__main__":
    sys.exit(main())
