#!/usr/bin/env python3
"""Render the round-2 poster for news-image-20261117.

Draws a 1024x1024 poster summing up the world news of Tuesday
17 November 2026, using only PIL. Unlike the round-1 newspaper wall of
text, this is a visual poster: one big lead illustration, colour-coded
story panels with icons, large type that stays legible at thumbnail
size, and a short "also today" strip.

Stories (all reported on 17 Nov 2026):
  LEAD   Ukraine destroys the Kerch Bridge road arch (Reuters/AP/Le Monde)
  IRAN   US strikes a missile site on Qeshm Island (Reuters)
  CHINA  Xi to host Trump & Putin in Shenzhen, Thu 19 Nov, at APEC
  HEALTH US loses measles elimination status after 26 years (PAHO/CDC)
  CLIMATE COP31 ministers fight over the fossil-fuel phase-out draft
  MARKETS AI stocks drag Wall Street down (NPR)
Run:  python3 render_poster.py [output_path]
"""

import math
import os
import sys

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
M = 28

BG = (13, 24, 40)
CREAM = (248, 246, 238)
PANEL = (255, 254, 248)
INK = (18, 22, 28)
GREY = (84, 88, 94)
RED = (196, 30, 36)
DARKRED = (150, 22, 28)
GOLD = (214, 144, 20)
TEAL = (6, 128, 140)
GREEN = (30, 128, 70)
BLUE = (35, 78, 160)
SKY = (196, 222, 240)
SEA = (38, 92, 138)
WHITE = (255, 255, 255)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


SANS_B = lambda s: font("DejaVuSans-Bold.ttf", s)
SANS = lambda s: font("DejaVuSans.ttf", s)
SERIF_B = lambda s: font("DejaVuSerif-Bold.ttf", s)


def wrap(draw, text, fnt, max_w):
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_wrapped(draw, x, y, text, fnt, max_w, fill=INK, leading=None):
    if leading is None:
        leading = int(fnt.size * 1.3)
    for line in wrap(draw, text, fnt, max_w):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def rrect(draw, box, radius, fill):
    draw.rounded_rectangle(box, radius=radius, fill=fill)


# ---------------------------------------------------------------- icons
def draw_bridge_scene(draw, x, y, w, h):
    """Wide scene: the Kerch Bridge with its road arch collapsed."""
    draw.rectangle([x, y, x + w, y + h], fill=SKY)
    sea_y = y + int(h * 0.68)
    draw.rectangle([x, sea_y, x + w, y + h], fill=SEA)
    for i in range(9):
        wx = x + 18 + i * (w // 9)
        draw.arc([wx, sea_y + 10, wx + 44, sea_y + 24], 0, 180,
                 fill=(120, 180, 220), width=3)
    deck_y = y + int(h * 0.52)
    # towers
    for tx in (x + int(w * 0.16), x + int(w * 0.84)):
        draw.line([tx, y + 16, tx, deck_y], fill=INK, width=7)
        draw.line([tx - 22, y + 16, tx + 22, y + 16], fill=INK, width=7)
    # intact decks
    draw.line([x + 8, deck_y, x + int(w * 0.40), deck_y], fill=INK, width=9)
    draw.line([x + int(w * 0.60), deck_y, x + w - 8, deck_y], fill=INK, width=9)
    # the great arch, broken: two stubs curving down into the gap
    draw.arc([x + int(w * 0.30), y + 8, x + int(w * 0.52), deck_y + 26],
             300, 360, fill=INK, width=7)
    draw.arc([x + int(w * 0.48), y + 8, x + int(w * 0.70), deck_y + 26],
             180, 240, fill=INK, width=7)
    # fallen arch segment in the sea, tilted
    fx, fy = x + int(w * 0.50), sea_y + 16
    draw.line([fx - 64, fy + 20, fx + 58, fy - 8], fill=(90, 96, 104), width=10)
    draw.line([fx - 64, fy + 34, fx + 58, fy + 6], fill=(90, 96, 104), width=6)
    # splash
    for dx in (-46, -18, 12, 40):
        draw.line([fx + dx, fy + 26, fx + dx - 6, fy + 6],
                  fill=(190, 225, 245), width=4)
    # explosion at the break
    ex, ey = x + int(w * 0.50), deck_y - 6
    for ang in range(0, 360, 30):
        r1, r2 = 8, 30
        draw.line([ex + r1 * math.cos(math.radians(ang)),
                   ey + r1 * math.sin(math.radians(ang)),
                   ex + r2 * math.cos(math.radians(ang)),
                   ey + r2 * math.sin(math.radians(ang))], fill=RED, width=5)
    draw.ellipse([ex - 10, ey - 10, ex + 10, ey + 10], fill=RED)
    # smoke
    for dx, dy, r in ((-96, -34, 20), (-58, -48, 26), (-16, -38, 21)):
        draw.ellipse([ex + dx - r, ey + dy - r, ex + dx + r, ey + dy + r],
                     fill=(110, 108, 102))
    # drone silhouette, top left
    dx, dy = x + 64, y + 26
    draw.line([dx - 26, dy, dx + 26, dy], fill=INK, width=5)
    draw.line([dx, dy - 10, dx, dy + 10], fill=INK, width=5)
    for px, py in ((-26, 0), (26, 0), (0, -10), (0, 10)):
        draw.ellipse([dx + px - 6, dy + py - 6, dx + px + 6, dy + py + 6],
                     outline=INK, width=3)
    draw.ellipse([dx - 7, dy - 7, dx + 7, dy + 7], fill=INK)


def draw_flame_ship(draw, cx, cy, s, color):
    # tanker hull
    draw.polygon([(cx - s, cy + int(s * 0.55)), (cx + s, cy + int(s * 0.55)),
                  (cx + int(s * 0.72), cy + int(s * 0.95)),
                  (cx - int(s * 0.72), cy + int(s * 0.95))], fill=INK)
    draw.rectangle([cx - int(s * 0.55), cy + int(s * 0.28),
                    cx + int(s * 0.1), cy + int(s * 0.55)], fill=INK)
    # flame above the stern
    fx, fy = cx + int(s * 0.42), cy + int(s * 0.30)
    draw.polygon([(fx, fy - int(s * 0.85)), (fx + int(s * 0.30), fy),
                  (fx - int(s * 0.30), fy)], fill=color)
    draw.polygon([(fx, fy - int(s * 0.42)), (fx + int(s * 0.16), fy),
                  (fx - int(s * 0.16), fy)], fill=GOLD)


def draw_three_leaders(draw, cx, cy, s):
    # three heads around a table: the first trilateral
    for dx, dy, col in ((-s * 0.62, -s * 0.30, RED),
                        (s * 0.62, -s * 0.30, BLUE),
                        (0, -s * 0.78, GOLD)):
        draw.ellipse([cx + dx - s * 0.30, cy + dy - s * 0.30,
                      cx + dx + s * 0.30, cy + dy + s * 0.30], fill=col)
    draw.ellipse([cx - s, cy + s * 0.28, cx + s, cy + s * 0.78],
                 outline=INK, width=5)


def draw_virus(draw, cx, cy, s, color):
    for ang in range(0, 360, 45):
        x2 = cx + (s + 10) * math.cos(math.radians(ang))
        y2 = cy + (s + 10) * math.sin(math.radians(ang))
        draw.line([cx, cy, x2, y2], fill=color, width=5)
        draw.ellipse([x2 - 7, y2 - 7, x2 + 7, y2 + 7], fill=color)
    draw.ellipse([cx - s, cy - s, cx + s, cy + s], fill=color)
    for dx, dy in ((-14, -8), (12, 4), (-2, 16)):
        draw.ellipse([cx + dx - 6, cy + dy - 6, cx + dx + 6, cy + dy + 6],
                     fill=WHITE)


def draw_leaf(draw, cx, cy, s, color):
    draw.ellipse([cx - s, cy - int(s * 0.62), cx + s, cy + int(s * 0.62)],
                 fill=color)
    draw.line([cx - s + 8, cy + int(s * 0.5), cx + s - 8, cy - int(s * 0.5)],
              fill=WHITE, width=4)


def draw_chart_down(draw, cx, cy, s, color):
    draw.line([cx - s, cy - s, cx - s, cy + s], fill=INK, width=5)
    draw.line([cx - s, cy + s, cx + s, cy + s], fill=INK, width=5)
    pts = [(cx - int(s * 0.8), cy - int(s * 0.55)),
           (cx - int(s * 0.3), cy - int(s * 0.1)),
           (cx + int(s * 0.15), cy - int(s * 0.35)),
           (cx + int(s * 0.72), cy + int(s * 0.62))]
    draw.line(pts, fill=color, width=7)
    ex, ey = pts[-1]
    draw.polygon([(ex + 16, ey + 2), (ex - 8, ey - 4), (ex + 2, ey + 18)],
                 fill=color)


# ---------------------------------------------------------------- layout
def panel_header(draw, x, y, w, text, color):
    draw.rectangle([x, y, x + w, y + 34], fill=color)
    draw.text((x + 14, y + 6), text, font=SANS_B(19), fill=WHITE)


def render():
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)

    # ---- masthead ------------------------------------------------------
    y = 20
    kick = "TUESDAY  ·  THE WORLD IN ONE IMAGE"
    kf = SANS_B(20)
    d.text(((W - d.textlength(kick, font=kf)) / 2, y), kick, font=kf,
           fill=(240, 190, 80))
    y += 34
    date = "17 NOVEMBER 2026"
    df = SANS_B(66)
    d.text(((W - d.textlength(date, font=df)) / 2, y), date, font=df,
           fill=WHITE)
    y += 88
    d.rectangle([M, y, W - M, y + 4], fill=RED)
    y += 16

    # ---- lead panel ----------------------------------------------------
    lead_y = y
    lead_h = 372
    rrect(d, [M, lead_y, W - M, lead_y + lead_h], 14, CREAM)
    panel_header(d, M, lead_y, W - 2 * M,
                 "LEAD  ·  UKRAINE — RUSSIA", RED)
    hy = lead_y + 46
    headline = "UKRAINE BLOWS THE KERCH BRIDGE APART"
    hy = draw_wrapped(d, M + 22, hy, headline, SERIF_B(43), W - 2 * M - 44,
                      leading=50)
    ill_y = hy + 4
    draw_bridge_scene(d, M + 22, ill_y, W - 2 * M - 44, 128)
    dy = ill_y + 136
    deck = ("Kyiv's seven-stage strike drops the road arch of Putin's "
            "19-km Crimea bridge into the strait — two days before the "
            "Shenzhen summit. Russia answers on Kyiv's Dnipro bridges.")
    dy = draw_wrapped(d, M + 22, dy, deck, SANS(19), W - 2 * M - 44,
                      leading=25)
    # stat chips
    chips = ["ROAD LINK CUT", "RAIL ON ONE TRACK",
             "1,441 DRONES IN ONE NIGHT — MOSCOW'S COUNT"]
    cx = M + 22
    cy = lead_y + lead_h - 38
    for chip in chips:
        cf = SANS_B(15)
        cw = d.textlength(chip, font=cf) + 22
        rrect(d, [cx, cy, cx + cw, cy + 28], 8, (24, 40, 64))
        d.text((cx + 11, cy + 5), chip, font=cf, fill=WHITE)
        cx += cw + 12
    y = lead_y + lead_h + 12

    # ---- middle row: two panels ---------------------------------------
    mid_h = 184
    half = (W - 2 * M - 16) // 2
    # Iran
    x0 = M
    rrect(d, [x0, y, x0 + half, y + mid_h], 12, PANEL)
    panel_header(d, x0, y, half, "IRAN  ·  STRAIT OF HORMUZ", DARKRED)
    draw_flame_ship(d, x0 + 52, y + 88, 34, RED)
    hy = draw_wrapped(d, x0 + 104, y + 46, "U.S. STRIKES IRAN'S QESHM ISLAND",
                      SANS_B(24), half - 122, leading=29)
    draw_wrapped(d, x0 + 104, hy + 4,
                 "Jets hit a missile launch site after attacks on U.S. "
                 "forces. Tehran claims another tanker hit a mine in "
                 "the strait.", SANS(17), half - 122, leading=22)
    # Shenzhen
    x1 = M + half + 16
    rrect(d, [x1, y, x1 + half, y + mid_h], 12, PANEL)
    panel_header(d, x1, y, half, "CHINA  ·  APEC — SHENZHEN", GOLD)
    draw_three_leaders(d, x1 + 52, y + 96, 34)
    hy = draw_wrapped(d, x1 + 104, y + 46,
                      "FIRST-EVER XI–TRUMP–PUTIN MEETING",
                      SANS_B(22), half - 122, leading=27)
    draw_wrapped(d, x1 + 104, hy + 4,
                 "Xi hosts both presidents on Thursday at APEC — the "
                 "first-ever trilateral of the U.S., China and Russia.",
                 SANS(17), half - 122, leading=22)
    y += mid_h + 12

    # ---- bottom row: three panels --------------------------------------
    bot_h = 176
    third = (W - 2 * M - 2 * 16) // 3
    cells = [
        ("HEALTH  ·  AMERICAS", TEAL, "virus",
         "U.S. LOSES MEASLES-FREE STATUS",
         "After 26 years: 5,412 cases in 2026, a 35-year high. Mexico "
         "and Bolivia also lose status."),
        ("CLIMATE  ·  COP31 ANTALYA", GREEN, "leaf",
         "MINISTERS FIGHT OVER ENDING OIL & GAS",
         "Draft deal: phase out fossil fuels, triple adaptation aid "
         "to $120bn a year by 2035."),
        ("MARKETS  ·  WALL STREET", BLUE, "chart",
         "AI STOCKS DRAG WALL ST. DOWN",
         "A tech-led sell-off on Tuesday, as investors turn on the "
         "AI boom's biggest winners."),
    ]
    for i, (kick2, col, icon, head, body) in enumerate(cells):
        x0 = M + i * (third + 16)
        rrect(d, [x0, y, x0 + third, y + bot_h], 12, PANEL)
        panel_header(d, x0, y, third, kick2, col)
        hy = draw_wrapped(d, x0 + 14, y + 44, head, SANS_B(20),
                          third - 28, leading=24)
        draw_wrapped(d, x0 + 14, hy + 6, body, SANS(16),
                     third - 28, leading=21)
    y += bot_h + 12

    # ---- also today strip ----------------------------------------------
    d.text((M, y), "ALSO TODAY", font=SANS_B(19), fill=(240, 190, 80))
    y += 26
    also = ("UK sanctions 8 Israeli settlement firms  ·  Japan scrambles "
            "jets over Russian aircraft  ·  Houthis advance as Yemen's "
            "army falls back on Aden  ·  Depardieu pleads guilty in Paris"
            "  ·  Pentagon fails its audit for a 9th straight year")
    y = draw_wrapped(d, M, y, also, SANS(17), W - 2 * M, fill=(226, 230, 236),
                     leading=22)
    y += 6
    credit = "Sources: Reuters · AP · PAHO · CDC · Le Monde · NPR — reports of 17 November 2026"
    cf = SANS(13)
    d.text(((W - d.textlength(credit, font=cf)) / 2, y), credit, font=cf,
           fill=(150, 160, 175))
    return img


def main():
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img = render()
    img.save(out, format="PNG", optimize=True)
    size = os.path.getsize(out)
    print("wrote", out, img.size, size, "bytes")
    if size > 1048576:
        print("WARNING: exceeds 1 MiB limit", file=sys.stderr)


if __name__ == "__main__":
    main()
