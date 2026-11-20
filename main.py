#!/usr/bin/env python3
"""The World in One Day - v2.

Draws Thursday 19 November 2026 as a broadsheet front page: 50 verified
stories from 7 regions, led by the first Trump-Xi-Putin trilateral summit
in Shenzhen, the ICJ Rohingya genocide verdict, GTA VI's launch, Voyager 1
at one light-day, and Anthropic's record IPO.

Writes exactly one file, entry.png, 1024x1024, to the output directory:
first command-line argument, else MAKEFUN_OUTPUT_DIR, else /output.
No network, no randomness, no clock: two runs write identical bytes.
"""

import hashlib
import math
import os
import sys

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 243, 232)
INK = (17, 17, 17)
RED = (185, 28, 28)
NAVY = (30, 58, 95)
GOLD = (245, 197, 24)
OCEAN = (207, 227, 242)
LAND = (232, 220, 195)
GRID = (255, 255, 255)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    path = os.path.join(FONT_DIR, name)
    try:
        return ImageFont.truetype(path, size)
    except OSError:
        return ImageFont.load_default()


def serif_b(size):
    return font("DejaVuSerif-Bold.ttf", size)


def serif(size):
    return font("DejaVuSerif.ttf", size)


def sans(size):
    return font("DejaVuSans.ttf", size)


def sans_b(size):
    return font("DejaVuSans-Bold.ttf", size)


def text_w(draw, text, fnt):
    return draw.textlength(text, font=fnt)


def wrap(draw, text, fnt, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if text_w(draw, trial, fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_wrapped(draw, text, fnt, x, y, max_w, fill, leading=None):
    if leading is None:
        leading = fnt.size + 4
    lines = wrap(draw, text, fnt, max_w)
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += leading
    return y


def lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def vgrad(draw, box, top, bottom):
    x0, y0, x1, y1 = box
    for y in range(y0, y1):
        t = (y - y0) / max(1, y1 - y0 - 1)
        draw.line([(x0, y), (x1, y)], fill=lerp(top, bottom, t))


# ---------------------------------------------------------------- stories
# region, place, lon, lat (None = no map dot), headline, deck
STORIES = [
    ("Asia", "Shenzhen", 114.06, 22.55,
     "Summit of three powers",
     "Trump, Xi, Putin meet in Shenzhen"),
    ("N. America", "Miami", -80.19, 25.76,
     "GTA VI is out",
     "Rockstar epic launches to 99 on Metacritic"),
    ("Europe", "The Hague", 4.30, 52.07,
     "Myanmar guilty of genocide",
     "ICJ rules on 2017 Rohingya crackdown"),
    ("N. America", "San Francisco", -122.42, 37.77,
     "Anthropic's record IPO",
     "$81bn raised, shares jump 17% on debut"),
    ("N. America", "Pasadena", -118.14, 34.15,
     "Voyager 1: 1 light-day",
     "NASA probe phones home from deep space"),
    ("N. America", "New York", -74.01, 40.71,
     "Wall Street slides",
     "Stocks fall for a fifth straight day"),
    ("Europe", "Antalya", 30.71, 36.90,
     "COP31 draft thins out",
     "Deal text drops fossil-fuel phaseout"),
    ("Middle East", "Riyadh", 46.68, 24.71,
     "Missile hits Riyadh tower",
     "Houthi rocket debris damages PIF building"),
    ("Middle East", "Gaza", 34.47, 31.50,
     "Israel pushes into Gaza",
     "Ground op beyond the Yellow Line"),
    ("Middle East", "Qeshm", 56.27, 26.96,
     "US strikes Qeshm island",
     "Iran hits back at Kuwait and Bahrain"),
    ("Middle East", "Kuwait City", 47.98, 29.38,
     "Kuwait repels Iran attack",
     "First Iranian strike there in two months"),
    ("Middle East", "Hormuz", 56.50, 26.50,
     "Hormuz crisis grows",
     "IEA calls it the top energy threat"),
    ("Europe", "Brussels", 4.35, 50.85,
     "EU sends \u20ac45bn to Kyiv",
     "Commission proposes new Ukraine loan"),
    ("Europe", "Crimea", 34.00, 45.00,
     "Ukraine hits Crimea bridge",
     "Third strike in four days"),
    ("Europe", "Kyiv", 30.52, 50.45,
     "Russian strikes kill five",
     "Power cut across five Ukrainian regions"),
    ("N. America", "Washington", -77.04, 38.90,
     "Trump: no more Iran strikes",
     "No major strikes in 2026"),
    ("Asia", "Dhaka", 90.41, 23.81,
     "Bangladesh burns",
     "Four killed, Yunus home torched"),
    ("Asia", "Odisha coast", 85.80, 19.80,
     "Cyclone Akvan nears India",
     "300,000 evacuated from Odisha coast"),
    ("Europe", "Bulgarian coast", 28.00, 43.20,
     "Gas tanker sinks",
     "LPG carrier Gas Husky hit off Bulgaria"),
    ("Asia", "Yongbyon", 126.30, 39.80,
     "North Korea enriches more",
     "IAEA: enrichment expands"),
    ("N. America", "Ottawa", -75.70, 45.42,
     "Carney's China win",
     "Canada trade deal runs to 2028, $400m relief"),
    ("Europe", "Copenhagen", 12.57, 55.68,
     "Denmark backs Greenland deal",
     "Parliament approves 109-0"),
    ("Europe", "London", -0.13, 51.51,
     "Burnham's EU clause",
     "UK minister to sign 'Farage clause'"),
    ("Europe", "London", -0.13, 51.51,
     "Chelsea beat PSG 1-0",
     "Buurman late goal tops group"),
    ("Europe", "Turin", 7.69, 45.07,
     "Alcaraz rolls on",
     "Beats Medvedev for 11th straight win"),
    ("Oceania", "Hobart", 147.33, -42.88,
     "England take ODI series",
     "Beat Australia by 97 runs in Hobart"),
    ("Europe", "Budapest", 19.04, 47.50,
     "Firouzja wins Armageddon",
     "Faces Giri in Total Chess final"),
    ("Africa", "Johannesburg", 28.05, -26.20,
     "South Africa top Tests",
     "Harmer's 6/51 beats Bangladesh"),
    ("S. America", "Caracas", -66.87, 10.48,
     "Hegseth jogs in Caracas",
     "Surprise stop near Maduro arrest site"),
    ("S. America", "Caracas", -66.87, 10.48,
     "US-Venezuela pact signed",
     "Military cooperation deal agreed"),
    ("N. America", "Sinaloa", -107.40, 24.80,
     "Cartel bomb kills one",
     "Attack in Sinaloa, Mexico"),
    ("N. America", "Texas", -100.00, 31.00,
     "35 found in generator box",
     "Migrants locked near Texas border"),
    ("N. America", "Texas", -100.00, 31.00,
     "Ammo cache seized",
     "38,000 rounds, 17 guns at crossing"),
    ("N. America", "Washington", -77.04, 38.90,
     "Court blocks migrant shield",
     "Trump asks justices to end it"),
    ("N. America", "Alaska", -152.00, 64.00,
     "Begich keeps Alaska seat",
     "Wins ranked-choice House race"),
    ("N. America", "Cincinnati", -84.51, 39.10,
     "Pete Rose pardoned",
     "Trump clears baseball's hit king"),
    ("N. America", "Los Angeles", -118.24, 34.05,
     "Puka Nacua suspended",
     "Rams receiver banned three games"),
    ("N. America", "Miami", -80.19, 25.76,
     "Heat 137, Bucks 130",
     "Giannis posts 27-13-9 in Miami win"),
    ("N. America", "Salt Lake City", -111.89, 40.76,
     "Lakers' streak ends",
     "Jazz win 109-97 in Salt Lake City"),
    ("N. America", "San Francisco", -122.42, 37.77,
     "Valkyries reach Finals",
     "Sweep Aces 87-77 in overtime"),
    ("N. America", "Chicago", -87.63, 41.88,
     "Kipruto wins Chicago",
     "Marathon title; Feysa repeats"),
    ("N. America", "Caribbean", -70.00, 15.00,
     "Cruise ship outbreak",
     "About 150 passengers and crew fall ill"),
    ("Europe", "London", -0.13, 51.51,
     "Prince Harry: I'll re-enlist",
     "Ready to fight Russia in Ukraine"),
    ("World", None, None, None,
     "Muslims to pass Christians",
     "Study sees crossover by 2035"),
    ("World", None, None, None,
     "Bitcoin dips under $63k",
     "Then recovers as ETFs shed $158m"),
    ("Asia", "Bhopal", 77.41, 23.26,
     "India 4, Malaysia 1",
     "Women's hockey trophy defence opens"),
    ("Asia", "Rawalpindi", 73.06, 33.60,
     "Sri Lanka dig in",
     "309/9 leads Pakistan by 82"),
    ("N. America", "Las Vegas", -115.14, 36.17,
     "Houston stuns No. 1 Florida",
     "86-76 in Players Era semi-final"),
    ("Oceania", "Fiji", 178.44, -18.14,
     "Fiji's teens head to Qatar",
     "U-17 draw: Spain, China, Morocco"),
    ("N. America", "Miami", -80.19, 25.76,
     "Messi tops MLS pay list",
     "League publishes 2026 salaries"),
]

REGION_COLORS = {
    "Europe": (37, 99, 235),
    "Middle East": (234, 88, 12),
    "Asia": (220, 38, 38),
    "N. America": (22, 163, 74),
    "S. America": (147, 51, 234),
    "Africa": (146, 64, 14),
    "Oceania": (8, 145, 178),
    "World": (100, 100, 100),
}

REGION_ORDER = ["Europe", "Middle East", "Asia", "N. America",
                "S. America", "Africa", "Oceania"]


# ---------------------------------------------------------------- masthead
def draw_masthead(img, draw):
    draw.rectangle([0, 0, W, 52], fill=(10, 10, 10))
    f = serif_b(44)
    title = "THE WORLD IN ONE DAY"
    tw = text_w(draw, title, f)
    draw.text(((W - tw) / 2, 4), title, font=f, fill=(255, 255, 255))
    draw.rectangle([0, 52, W, 84], fill=GOLD)
    f2 = sans_b(23)
    draw.text((10, 58), "THURSDAY 19 NOVEMBER 2026", font=f2, fill=INK)
    f3 = sans_b(17)
    right = "50 STORIES  \u2022  7 REGIONS"
    tw3 = text_w(draw, right, f3)
    draw.text((W - 10 - tw3, 62), right, font=f3, fill=INK)
    draw.line([(0, 84), (W, 84)], fill=INK, width=2)


# ---------------------------------------------------------------- lead art
def draw_flag_us(draw, x, y, w, h):
    for i in range(7):
        draw.rectangle([x, y + i * h // 7, x + w, y + (i + 1) * h // 7],
                       fill=(255, 255, 255) if i % 2 else (178, 34, 52))
    draw.rectangle([x, y, x + w * 2 // 5, y + h * 4 // 7], fill=(60, 59, 110))
    for r in range(4):
        for c in range(5):
            draw.ellipse([x + 3 + c * 5, y + 3 + r * 5, x + 6 + c * 5,
                          y + 6 + r * 5], fill=(255, 255, 255))


def draw_flag_cn(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(222, 41, 16))
    cx, cy = x + w // 5, y + h // 4
    draw.regular_polygon((cx, cy, 6), 5, fill=(255, 222, 0))
    for sx, sy in [(x + w // 2, y + h // 6), (x + w * 3 // 5, y + h // 3),
                   (x + w * 3 // 5, y + h // 2), (x + w // 2, y + h * 2 // 3)]:
        draw.regular_polygon((sx, sy, 3), 5, fill=(255, 222, 0))


def draw_flag_ru(draw, x, y, w, h):
    for i, col in enumerate([(255, 255, 255), (0, 57, 166), (213, 0, 50)]):
        draw.rectangle([x, y + i * h // 3, x + w, y + (i + 1) * h // 3],
                       fill=col)


def draw_lead_art(img, draw, box):
    x0, y0, x1, y1 = box
    vgrad(draw, box, (254, 166, 80), (58, 48, 98))
    # sun
    draw.ellipse([x1 - 118, y0 + 14, x1 - 58, y0 + 74], fill=(255, 214, 90))
    # distant hills + Great Wall zigzag
    draw.polygon([(x0, y1 - 62), (x0 + 90, y1 - 96), (x0 + 190, y1 - 70),
                  (x0 + 300, y1 - 100), (x1, y1 - 66), (x1, y1 - 40),
                  (x0, y1 - 40)], fill=(46, 80, 52))
    draw.line([(x0 + 20, y1 - 84), (x0 + 120, y1 - 100), (x0 + 230, y1 - 82),
               (x0 + 330, y1 - 98), (x1 - 10, y1 - 80)],
              fill=(232, 220, 195), width=3)
    for wx in (70, 170, 270, 360):
        draw.rectangle([x0 + wx, y1 - 108, x0 + wx + 12, y1 - 84],
                       fill=(232, 220, 195))
    # Shenzhen skyline
    sky = [(0, 46), (28, 46), (28, 78), (52, 78), (52, 34), (66, 34),
           (66, 62), (92, 62), (92, 26), (104, 14), (116, 26), (116, 66),
           (150, 66), (150, 44), (176, 44), (176, 78), (210, 78),
           (210, 52), (238, 52), (238, 84), (268, 84), (268, 40),
           (284, 40), (284, 70), (316, 70), (316, 50), (344, 50),
           (344, 78), (380, 78), (380, 58), (410, 58), (410, 84)]
    pts = [(x0 + px, y1 - 84 + (84 - py)) for px, py in sky]
    pts += [(x1, y1), (x0, y1)]
    draw.polygon(pts, fill=(24, 28, 52))
    for wy in range(0, 60, 12):
        for wx in range(6, 400, 18):
            if (wx // 18 + wy // 12) % 3 == 0:
                draw.rectangle([x0 + wx, y1 - 78 + wy, x0 + wx + 4,
                                y1 - 74 + wy], fill=(255, 214, 90))
    # round table
    cx = (x0 + x1) // 2
    draw.ellipse([cx - 150, y1 - 46, cx + 150, y1 - 6], fill=(96, 58, 32))
    draw.ellipse([cx - 150, y1 - 52, cx + 150, y1 - 14], fill=(124, 78, 44))
    draw.ellipse([cx - 120, y1 - 48, cx + 120, y1 - 20], fill=(160, 110, 66))
    # three flag poles + flags
    for dx, fn in ((-118, draw_flag_us), (0, draw_flag_cn), (118, draw_flag_ru)):
        px = cx + dx
        draw.line([(px, y1 - 150), (px, y1 - 46)], fill=(220, 220, 220),
                  width=3)
        fw = 46 if fn is draw_flag_cn else 40
        fn(draw, px + 2, y1 - 150, fw, 28)
    # caption strip
    draw.rectangle([x0, y1 - 22, x1, y1], fill=(10, 10, 10))
    f = sans_b(12)
    cap = "Kylin Villa, Shenzhen \u2014 81 minutes that made history"
    draw.text((x0 + 10, y1 - 19), cap, font=f, fill=(255, 255, 255))


def draw_lead_text(draw, x, y, w):
    f_kick = sans_b(13)
    draw.text((x, y), "LEAD STORY  \u2014  SHENZHEN, CHINA",
              font=f_kick, fill=RED)
    y += 20
    f_head = serif_b(36)
    draw.text((x, y), "THREE LEADERS,", font=f_head, fill=INK)
    y += 40
    draw.text((x, y), "ONE TABLE", font=f_head, fill=INK)
    y += 44
    f_deck = sans(15)
    y = draw_wrapped(
        draw,
        "Donald Trump, Xi Jinping and Vladimir Putin meet for the first "
        "time as a trio and issue a joint declaration on nuclear risk.",
        f_deck, x, y, w, INK, leading=19)
    y += 4
    f_b = sans(13)
    bullets = [
        "81 minutes at Kylin Villa \u2014 Xi in the middle at a round table",
        "\u201cA nuclear war cannot be won and must never be fought\u201d",
        "No deal on Ukraine or Iran \u2014 and UN reform pledged too",
    ]
    for b in bullets:
        draw.rectangle([x, y + 4, x + 7, y + 11], fill=RED)
        y = draw_wrapped(draw, b, f_b, x + 14, y, w - 14, INK, leading=16)
    return y


# ---------------------------------------------------------------- panels
def draw_panel_gta(draw, box):
    x0, y0, x1, y1 = box
    vgrad(draw, box, (255, 120, 140), (255, 190, 120))
    draw.ellipse([x0 + 30, y0 + 6, x0 + 78, y0 + 54], fill=(255, 214, 90))
    for px, py, s in [(150, 10, 20), (180, 20, 16), (205, 8, 18)]:
        draw.line([(x0 + px, y0 + py + s), (x0 + px, y0 + py + s + 22)],
                  fill=(20, 60, 40), width=4)
        for a in (-40, -15, 10, 35):
            ang = math.radians(a - 90)
            ex = x0 + px + int(16 * math.cos(ang))
            ey = y0 + py + s + int(16 * math.sin(ang))
            draw.line([(x0 + px, y0 + py + s), (ex, ey)],
                      fill=(20, 60, 40), width=3)
    draw.rectangle([x0 + 14, y0 + 44, x0 + 92, y0 + 56], fill=(20, 20, 40))
    draw.rectangle([x0 + 20, y0 + 48, x0 + 86, y0 + 54], fill=(90, 180, 255))
    draw.text((x0 + 10, y0 + 4), "VI", font=serif_b(30), fill=(20, 20, 40))


def draw_panel_icj(draw, box):
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=(18, 28, 64))
    cx = (x0 + x1) // 2
    cy = y0 + 18
    draw.line([(cx, y0 + 6), (cx, y1 - 8)], fill=(255, 200, 60), width=4)
    draw.line([(cx - 62, cy), (cx + 62, cy)], fill=(255, 200, 60), width=4)
    draw.ellipse([cx - 6, y0 + 2, cx + 6, y0 + 12], fill=(255, 200, 60))
    for sx in (-62, 62):
        draw.line([(cx + sx, cy), (cx + sx - 16, cy + 22)],
                  fill=(255, 200, 60), width=2)
        draw.line([(cx + sx, cy), (cx + sx + 16, cy + 22)],
                  fill=(255, 200, 60), width=2)
        draw.arc([cx + sx - 17, cy + 14, cx + sx + 17, cy + 36],
                 0, 180, fill=(255, 200, 60), width=3)
    draw.line([(cx - 26, y1 - 8), (cx + 26, y1 - 8)],
              fill=(255, 200, 60), width=4)


def draw_panel_voyager(draw, box):
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=(5, 5, 18))
    for sx, sy, r in [(30, 16, 2), (70, 30, 1), (120, 12, 2), (170, 26, 1),
                      (210, 14, 2), (50, 52, 1), (150, 56, 2), (200, 48, 1),
                      (90, 44, 1), (20, 38, 1)]:
        draw.ellipse([x0 + sx - r, y0 + sy - r, x0 + sx + r, y0 + sy + r],
                     fill=(255, 255, 255))
    cx, cy = x0 + 120, y0 + 46
    draw.line([(cx, cy), (cx + 52, cy - 26)], fill=(200, 200, 210), width=3)
    draw.polygon([(cx + 52, cy - 34), (cx + 72, cy - 30), (cx + 58, cy - 8)],
                 fill=(220, 220, 230))
    draw.polygon([(cx - 26, cy - 12), (cx + 6, cy - 4), (cx - 4, cy + 12),
                  (cx - 30, cy + 8)], fill=(180, 180, 195))
    draw.line([(cx - 26, cy + 2), (cx - 58, cy + 12)],
              fill=(200, 200, 210), width=2)


def draw_panel_ipo(draw, box):
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=(8, 48, 32))
    for i, bh in enumerate([10, 14, 12, 20, 17, 27, 25, 35]):
        bx = x0 + 14 + i * 26
        draw.rectangle([bx, y1 - 10 - bh, bx + 18, y1 - 10],
                       fill=(46, 160, 90))
    pts = [(x0 + 14, y1 - 20), (x0 + 52, y1 - 32), (x0 + 92, y1 - 26),
           (x0 + 130, y1 - 40), (x0 + 168, y1 - 34), (x0 + 206, y1 - 52),
           (x0 + 228, y1 - 48)]
    draw.line(pts, fill=(120, 255, 170), width=4, joint="curve")
    draw.ellipse([x0 + 220, y1 - 56, x0 + 236, y1 - 40], fill=(120, 255, 170))


def draw_panels(draw, y, h):
    panels = [
        ("GTA VI IS OUT", "99 Metacritic \u00b7 $1.84bn day one",
         draw_panel_gta),
        ("MYANMAR GUILTY", "ICJ: genocide against the Rohingya",
         draw_panel_icj),
        ("VOYAGER 1", "One light-day out \u2014 26bn km",
         draw_panel_voyager),
        ("RECORD IPO", "$81bn raised \u00b7 shares +17%",
         draw_panel_ipo),
    ]
    pw = 248
    gap = 4
    x = 8
    for title, sub, fn in panels:
        fn(draw, (x, y, x + pw, y + h - 30))
        draw.rectangle([x, y + h - 30, x + pw, y + h], fill=(10, 10, 10))
        draw.text((x + 8, y + h - 28), title, font=sans_b(15),
                  fill=(255, 255, 255))
        draw.text((x + 8, y + h - 12), sub, font=sans(11),
                  fill=(200, 200, 200))
        x += pw + gap
    return y + h


# ---------------------------------------------------------------- map
# simplified continent outlines (lon, lat)
CONTINENTS = [
    [(-168, 66), (-165, 60), (-158, 58), (-152, 60), (-140, 60),
     (-135, 57), (-130, 54), (-125, 49), (-124, 42), (-120, 34),
     (-114, 29), (-110, 24), (-105, 20), (-97, 16), (-94, 17),
     (-90, 14), (-86, 12), (-83, 9), (-80, 8), (-79, 9), (-82, 15),
     (-87, 13), (-90, 14), (-92, 15), (-97, 16), (-97, 26), (-93, 30),
     (-89, 30), (-84, 30), (-81, 25), (-80, 32), (-76, 35), (-74, 40),
     (-70, 42), (-68, 45), (-65, 44), (-60, 47), (-55, 47), (-60, 52),
     (-65, 55), (-68, 58), (-72, 62), (-78, 62), (-85, 66), (-92, 66),
     (-95, 69), (-110, 68), (-125, 70), (-140, 70), (-155, 71),
     (-165, 68), (-168, 66)],
    [(-58, 64), (-52, 60), (-45, 60), (-40, 64), (-32, 68), (-25, 70),
     (-20, 74), (-25, 76), (-35, 78), (-50, 76), (-58, 72), (-58, 64)],
    [(-80, 9), (-77, 4), (-80, -3), (-81, -6), (-77, -12), (-72, -18),
     (-70, -23), (-70, -30), (-72, -37), (-73, -44), (-70, -50),
     (-68, -55), (-66, -55), (-65, -48), (-62, -41), (-57, -38),
     (-52, -33), (-48, -28), (-41, -23), (-39, -17), (-35, -9),
     (-35, -6), (-40, -3), (-44, -2), (-50, 0), (-53, 4), (-58, 6),
     (-62, 9), (-68, 11), (-72, 12), (-77, 8), (-80, 9)],
    [(-17, 15), (-17, 21), (-15, 27), (-10, 31), (-5, 35), (0, 36),
     (10, 37), (11, 34), (15, 32), (20, 32), (25, 31), (30, 31),
     (32, 31), (34, 28), (35, 24), (37, 20), (39, 15), (41, 11),
     (43, 11), (48, 11), (51, 12), (48, 5), (42, 0), (40, -5),
     (40, -10), (38, -15), (36, -20), (33, -26), (28, -33), (20, -35),
     (17, -32), (15, -27), (13, -20), (12, -15), (13, -10), (12, -5),
     (9, 0), (9, 4), (6, 4), (0, 6), (-8, 5), (-13, 8), (-17, 12),
     (-17, 15)],
    [(-10, 36), (-9, 38), (-9, 43), (-2, 44), (-1, 46), (-4, 48),
     (-2, 49), (0, 50), (3, 51), (5, 53), (8, 55), (8, 57), (10, 59),
     (5, 60), (5, 62), (10, 64), (13, 66), (18, 69), (25, 71),
     (30, 70), (32, 68), (35, 66), (40, 64), (45, 66), (50, 68),
     (55, 68), (60, 69), (68, 68), (60, 65), (55, 60), (50, 55),
     (45, 50), (40, 47), (35, 45), (30, 45), (28, 44), (25, 40),
     (23, 36), (22, 37), (20, 40), (18, 42), (15, 44), (12, 44),
     (8, 44), (3, 43), (0, 40), (-2, 37), (-6, 36), (-9, 37), (-10, 36)],
    [(30, 36), (35, 36), (36, 33), (40, 32), (43, 30), (48, 30),
     (50, 29), (54, 26), (57, 25), (60, 25), (62, 24), (66, 25),
     (70, 23), (72, 20), (76, 18), (80, 15), (80, 10), (77, 8),
     (80, 7), (82, 10), (85, 15), (88, 22), (91, 22), (94, 17),
     (97, 16), (100, 14), (103, 10), (105, 9), (108, 11), (109, 15),
     (106, 20), (108, 18), (110, 20), (114, 22), (118, 25), (121, 28),
     (122, 32), (120, 35), (122, 38), (124, 40), (127, 40), (130, 42),
     (132, 43), (135, 44), (138, 46), (140, 48), (142, 52), (142, 55),
     (140, 60), (138, 65), (140, 70), (145, 72), (150, 70), (155, 69),
     (158, 66), (160, 62), (162, 60), (163, 58), (160, 55), (156, 52),
     (152, 50), (148, 45), (142, 42), (140, 40), (135, 38), (130, 35),
     (127, 35), (126, 38), (122, 38), (120, 35), (115, 30), (110, 25),
     (105, 20), (100, 15), (98, 10), (95, 15), (92, 20), (90, 22),
     (88, 22), (85, 18), (82, 12), (80, 8), (77, 10), (74, 20),
     (70, 23), (66, 25), (62, 25), (58, 26), (55, 28), (52, 28),
     (50, 30), (48, 30), (44, 30), (40, 32), (36, 36), (33, 36),
     (30, 36)],
    [(113, -22), (114, -30), (115, -35), (118, -35), (124, -33),
     (129, -32), (132, -32), (135, -35), (137, -35), (140, -38),
     (145, -38), (150, -37), (153, -32), (153, -27), (150, -23),
     (146, -19), (142, -15), (142, -11), (140, -17), (136, -15),
     (135, -12), (132, -12), (130, -13), (126, -14), (122, -17),
     (118, -20), (113, -22)],
    [(109, 1), (113, 4), (117, 6), (119, 0), (117, -3), (113, -3),
     (110, -2), (109, 1)],
    [(95, 5), (98, 3), (100, 0), (103, -3), (105, -5), (104, -6),
     (101, -4), (98, 1), (95, 5)],
    [(105, -6), (108, -7), (111, -7), (114, -8), (114, -9), (111, -8),
     (107, -7), (105, -6)],
    [(131, -1), (136, -2), (141, -3), (146, -6), (150, -8), (147, -9),
     (143, -8), (138, -8), (134, -4), (131, -1)],
    [(167, -45), (170, -42), (173, -40), (176, -38), (178, -38),
     (175, -40), (172, -43), (168, -46), (167, -45)],
    [(-5, 50), (-3, 53), (-5, 56), (-3, 58), (-1, 57), (0, 53), (1, 51),
     (-3, 50), (-5, 50)],
    [(130, 31), (132, 33), (134, 34), (137, 35), (139, 35), (140, 38),
     (141, 41), (142, 44), (144, 44), (142, 40), (140, 37), (137, 34),
     (133, 33), (130, 31)],
    [(-22, 64), (-18, 63), (-15, 64), (-18, 66), (-22, 66), (-24, 65),
     (-22, 64)],
    [(44, -16), (47, -15), (50, -16), (49, -20), (47, -24), (44, -25),
     (43, -21), (44, -16)],
    [(80, 6), (81, 8), (80, 10), (79, 8), (80, 6)],
]

LAT_TOP, LAT_BOT = 75, -45


def draw_map(draw, box):
    x0, y0, x1, y1 = box
    mw, mh = x1 - x0, y1 - y0
    draw.rectangle(box, fill=OCEAN)

    def proj(lon, lat):
        return (x0 + (lon + 180) / 360 * mw,
                y0 + (LAT_TOP - lat) / (LAT_TOP - LAT_BOT) * mh)

    for lon in range(-150, 181, 30):
        px = x0 + (lon + 180) / 360 * mw
        draw.line([(px, y0), (px, y1)], fill=GRID, width=1)
    for lat in range(-30, 81, 30):
        py = y0 + (LAT_TOP - lat) / (LAT_TOP - LAT_BOT) * mh
        draw.line([(x0, py), (x1, py)], fill=GRID, width=1)
    for poly in CONTINENTS:
        pts = [proj(lon, lat) for lon, lat in poly]
        draw.polygon(pts, fill=LAND, outline=(120, 110, 90))
    f_ocean = sans_b(11)
    draw.text((x0 + 8, y1 - 18), "ATLANTIC", font=f_ocean,
              fill=(90, 120, 150))
    draw.text((x1 - 62, y0 + 6), "PACIFIC", font=f_ocean,
              fill=(90, 120, 150))
    draw.text((x0 + mw // 2 + 60, y1 - 18), "INDIAN", font=f_ocean,
              fill=(90, 120, 150))
    # dots with simple de-collision
    placed = []
    f_num = sans_b(8)
    for i, st in enumerate(STORIES, start=1):
        region, _place, lon, lat = st[0], st[1], st[2], st[3]
        if lon is None:
            continue
        tx, ty = proj(lon, lat)
        pos = (tx, ty)
        for dx, dy in [(0, 0), (17, -13), (-17, -13), (17, 13), (-17, 13),
                       (0, -18), (0, 18), (32, 0), (-32, 0), (32, -14),
                       (-32, -14), (32, 14), (-32, 14)]:
            cand = (tx + dx, ty + dy)
            if all((cand[0] - px) ** 2 + (cand[1] - py) ** 2 > 16 ** 2
                   for px, py in placed):
                pos = cand
                break
        if pos != (tx, ty):
            draw.line([(tx, ty), pos], fill=INK, width=1)
            draw.ellipse([tx - 2, ty - 2, tx + 2, ty + 2], fill=INK)
        placed.append(pos)
        r = 7
        draw.ellipse([pos[0] - r, pos[1] - r, pos[0] + r, pos[1] + r],
                     fill=REGION_COLORS[region], outline=(255, 255, 255))
        num = str(i)
        nw = text_w(draw, num, f_num)
        draw.text((pos[0] - nw / 2, pos[1] - 5), num, font=f_num,
                  fill=(255, 255, 255))
    return placed


def draw_map_side(draw, y, h):
    # left: region key
    x = 8
    draw.text((x, y), "WHERE IT HAPPENED", font=sans_b(14), fill=INK)
    yy = y + 22
    for region in REGION_ORDER:
        draw.rectangle([x, yy + 2, x + 12, yy + 14],
                       fill=REGION_COLORS[region])
        draw.text((x + 18, yy), region, font=sans(13), fill=INK)
        yy += 20
    # right: explainer
    x = 772
    draw.text((x, y), "THE MAP", font=sans_b(14), fill=INK)
    f = sans(12)
    txt = ("Every numbered dot marks where a story happened. Colour shows "
           "its region; a thin line links a shifted label to its true "
           "place.")
    draw_wrapped(draw, txt, f, x, y + 22, 244, INK, leading=16)


# ---------------------------------------------------------------- list
def draw_list(draw, y):
    draw.text((8, y), "THE DAY IN 50 STORIES", font=sans_b(15), fill=INK)
    f_note = sans(12)
    note = "headline, then what happened, in one line each"
    draw.text((250, y + 2), note, font=f_note, fill=(90, 90, 90))
    draw.line([(8, y + 20), (W - 8, y + 20)], fill=INK, width=1)
    y += 26
    f_head = sans_b(13)
    f_body = sans(13)
    f_num = sans_b(13)
    lead = 16
    cols = [(8, STORIES[:25]), (516, STORIES[25:])]
    for cx, items in cols:
        yy = y
        for i, st in enumerate(items, start=1):
            n = i if cx == 8 else i + 25
            region, _place, _lon, _lat, head, deck = st
            num = str(n) + "  "
            nw = text_w(draw, num, f_num)
            draw.text((cx, yy), num, font=f_num,
                      fill=REGION_COLORS[region])
            x = cx + nw
            hw = text_w(draw, head, f_head)
            draw.text((x, yy), head, font=f_head, fill=INK)
            x += hw
            sep = " \u2014 "
            sw = text_w(draw, sep, f_body)
            draw.text((x, yy), sep, font=f_body, fill=(90, 90, 90))
            x += sw
            max_w = 500 - (x - cx)
            d = deck
            while d and text_w(draw, d, f_body) > max_w:
                d = d[:-1]
            if d != deck:
                d = d.rstrip()
                if " " in d:
                    d = d[:d.rfind(" ")] + "\u2026"
                else:
                    d = d[:-1] + "\u2026"
            draw.text((x, yy), d, font=f_body, fill=(60, 60, 60))
            yy += lead
    return y + 25 * lead


# ---------------------------------------------------------------- build
def build(out_dir):
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)
    draw_masthead(img, draw)
    # lead row
    draw_lead_art(img, draw, (8, 88, 430, 283))
    draw_lead_text(draw, 446, 92, 570)
    draw.line([(8, 287), (W - 8, 287)], fill=INK, width=1)
    # panels row
    y = draw_panels(draw, 291, 88)
    draw.line([(8, y + 4), (W - 8, y + 4)], fill=INK, width=1)
    # map band
    my = y + 8
    draw_map_side(draw, my, 186)
    draw_map(draw, (260, my + 14, 764, my + 182))
    # list
    ly = my + 186
    end = draw_list(draw, ly)
    # markets strip
    draw.rectangle([0, 1000, W, H], fill=(10, 10, 10))
    f_m = sans_b(11)
    strip = ("MARKETS \u00b7 S&P 500 7,176 \u22122.02% \u00b7 FTSE 100 10,453 "
             "\u22120.93% \u00b7 NIKKEI \u22124.68% \u00b7 BRENT $89.72 +0.31% "
             "\u00b7 Sources: AP, Reuters, BBC, WSJ, CNN, Le Monde")
    draw.text((8, 1008), strip, font=f_m, fill=(255, 255, 255))
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.png")
    img.save(path, format="PNG")
    data = open(path, "rb").read()
    print("wrote", path, len(data), "bytes",
          hashlib.sha256(data).hexdigest()[:16], "list_end", end)
    return path


def main():
    if len(sys.argv) > 1:
        out_dir = sys.argv[1]
    else:
        out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    build(out_dir)


if __name__ == "__main__":
    main()
