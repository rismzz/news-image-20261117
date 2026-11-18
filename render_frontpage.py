#!/usr/bin/env python3
"""Render the front page for news-image-20261117.

Draws a 1024x1024 newspaper front page summarising the world news of
Tuesday 17 November 2026, using only the Python standard library and PIL.
Run:  python3 render_frontpage.py [output_path]
Default output is entry.png next to this script.
"""

import os
import sys

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
MARGIN = 34
CONTENT_W = W - 2 * MARGIN

PAPER = (247, 243, 234)
INK = (20, 20, 20)
RED = (185, 28, 28)
NAVY = (30, 58, 95)
GREY = (90, 86, 78)
LIGHT_GREY = (210, 204, 190)
SKY = (214, 228, 238)
WATER = (120, 160, 190)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


SERIF_B = lambda s: font("DejaVuSerif-Bold.ttf", s)
SANS_B = lambda s: font("DejaVuSans-Bold.ttf", s)
SANS = lambda s: font("DejaVuSans.ttf", s)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns a list of lines that fit max_w."""
    lines = []
    for para in text.split("\n"):
        words = para.split()
        if not words:
            lines.append("")
            continue
        cur = words[0]
        for word in words[1:]:
            trial = cur + " " + word
            if draw.textlength(trial, font=fnt) <= max_w:
                cur = trial
            else:
                lines.append(cur)
                cur = word
        lines.append(cur)
    return lines


def draw_wrapped(draw, x, y, text, fnt, max_w, fill=INK, leading=None):
    """Draw wrapped text; returns the y just below the last line."""
    if leading is None:
        leading = int(fnt.size * 1.28)
    for line in wrap(draw, text, fnt, max_w):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def draw_bridge(draw, x, y, w, h):
    """Simple geometric illustration: a bridge with a collapsed span."""
    # sky
    draw.rectangle([x, y, x + w, y + h], fill=SKY, outline=NAVY, width=2)
    # water
    wy = y + h - 26
    draw.rectangle([x, wy, x + w, y + h], fill=WATER)
    for i in range(5):
        wx = x + 12 + i * (w // 5)
        draw.arc([wx, wy + 6, wx + 34, wy + 18], 0, 180, fill=NAVY, width=2)
    # deck (left span intact, middle collapsed, right span intact)
    deck_y = y + h - 62
    draw.line([x + 8, deck_y, x + w * 0.38, deck_y], fill=INK, width=6)
    draw.line([x + w * 0.62, deck_y, x + w - 8, deck_y], fill=INK, width=6)
    # broken stubs falling into the gap
    draw.line([x + w * 0.38, deck_y, x + w * 0.46, deck_y + 22],
              fill=INK, width=5)
    draw.line([x + w * 0.62, deck_y, x + w * 0.54, deck_y + 22],
              fill=INK, width=5)
    # towers
    for tx in (x + w * 0.20, x + w * 0.80):
        draw.line([tx, y + 22, tx, deck_y], fill=INK, width=5)
        draw.line([tx - 16, y + 22, tx + 16, y + 22], fill=INK, width=5)
        draw.line([tx - 16, y + 34, tx + 16, y + 34], fill=INK, width=3)
    # suspension cables
    draw.line([x + w * 0.20, y + 22, x + w * 0.38, deck_y],
              fill=GREY, width=2)
    draw.line([x + w * 0.80, y + 22, x + w * 0.62, deck_y],
              fill=GREY, width=2)
    # smoke over the gap
    cx, cy = x + w // 2, y + 26
    for dx, dy, r in ((-26, 10, 13), (0, 0, 17), (26, 12, 12), (-8, -12, 11)):
        draw.ellipse([cx + dx - r, cy + dy - r, cx + dx + r, cy + dy + r],
                      fill=(120, 118, 112))
    # explosion starburst at the break
    ex, ey = x + w // 2, deck_y - 4
    for ang in range(0, 360, 30):
        import math
        r1, r2 = 6, 20
        x1 = ex + r1 * math.cos(math.radians(ang))
        y1 = ey + r1 * math.sin(math.radians(ang))
        x2 = ex + r2 * math.cos(math.radians(ang))
        y2 = ey + r2 * math.sin(math.radians(ang))
        draw.line([x1, y1, x2, y2], fill=RED, width=3)
    draw.ellipse([ex - 7, ey - 7, ex + 7, ey + 7], fill=RED)
    # caption strip along the bottom edge, clear of the water arcs
    draw.rectangle([x, y + h - 20, x + w, y + h], fill=NAVY)
    draw.text((x + 8, y + h - 18), "THE KERCH BRIDGE, STRUCK",
              font=SANS_B(13), fill=(255, 255, 255))


def draw_globe(draw, x, y, w, h):
    """Small abstract globe for the sixth grid cell."""
    cx, cy = x + w // 2, y + h // 2 - 6
    r = min(w, h) // 2 - 14
    draw.ellipse([cx - r, cy - r, cx + r, cy + r],
                 outline=NAVY, width=3, fill=(226, 236, 244))
    draw.ellipse([cx - r * 0.45, cy - r, cx + r * 0.45, cy + r],
                 outline=NAVY, width=2)
    draw.line([cx - r, cy, cx + r, cy], fill=NAVY, width=2)
    draw.arc([cx - r, cy - r * 0.55, cx + r, cy + r * 0.55],
             200, 340, fill=NAVY, width=2)
    draw.arc([cx - r, cy - r * 0.55, cx + r, cy + r * 0.55],
             20, 160, fill=NAVY, width=2)


def render():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- masthead ------------------------------------------------------
    y = 26
    title = "THE WORLD \u2014 IN ONE IMAGE"
    tf = SERIF_B(54)
    tw = d.textlength(title, font=tf)
    d.text(((W - tw) / 2, y), title, font=tf, fill=INK)
    y += 72
    d.rectangle([MARGIN, y, W - MARGIN, y + 5], fill=RED)
    y += 14
    dateline = "TUESDAY  \u00b7  17 NOVEMBER 2026  \u00b7  THE DAY'S WORLD NEWS ON ONE PAGE"
    df = SANS_B(19)
    dw = d.textlength(dateline, font=df)
    d.text(((W - dw) / 2, y), dateline, font=df, fill=NAVY)
    y += 30
    d.line([MARGIN, y, W - MARGIN, y], fill=INK, width=2)
    y += 12

    # ---- lead story ----------------------------------------------------
    d.text((MARGIN, y), "LEAD  \u00b7  UKRAINE \u2014 RUSSIA",
           font=SANS_B(18), fill=RED)
    y += 26
    headline = ("Kerch Bridge struck for a second day \u2014 "
                "Kyiv's bridges hit in reply")
    y = draw_wrapped(d, MARGIN, y, headline, SERIF_B(40), CONTENT_W,
                     leading=48)
    y += 6

    # deck (left) + bridge illustration (right)
    ill_w, ill_h = 300, 160
    ill_x, ill_y = W - MARGIN - ill_w, y
    deck = ("Ukraine hit the Kerch Bridge for a second straight day, "
            "leaving part of the road bridge collapsed. Russia answered "
            "by striking Kyiv's bridges over the Dnipro, disrupting "
            "heating, water and power in the capital.")
    deck_w = CONTENT_W - ill_w - 24
    draw_wrapped(d, MARGIN, y, deck, SANS(21), deck_w, leading=27)
    draw_bridge(d, ill_x, ill_y, ill_w, ill_h)
    y = ill_y + ill_h + 14
    d.line([MARGIN, y, W - MARGIN, y], fill=INK, width=2)
    y += 12

    # ---- supporting stories, 2-column grid ----------------------------
    stories = [
        ("MIDDLE EAST",
         "Mine hits tanker near Hormuz; third US carrier arrives",
         "A tanker struck a mine near the Strait of Hormuz; a third US "
         "carrier, USS Theodore Roosevelt, arrived."),
        ("CHINA \u00b7 US \u00b7 RUSSIA",
         "First Xi\u2013Trump\u2013Putin meeting confirmed",
         "China confirms the first Xi\u2013Trump\u2013Putin meeting, "
         "Thursday in Shenzhen at the APEC summit."),
        ("BRITAIN \u00b7 ISRAEL",
         "UK sanctions eight settlement builders",
         "Britain sanctions eight Israeli settlement firms in the West "
         "Bank, plus a group blocking aid to Gaza."),
        ("JAPAN \u00b7 RUSSIA",
         "Japan scrambles jets over Russian planes",
         "Japan scrambled fighter jets after two Russian aircraft were "
         "suspected of violating its airspace."),
        ("EUROPE",
         "Five states plan joint Rwanda deportation hub",
         "Germany, Denmark, Austria, Greece and the Netherlands plan "
         "the joint hub in Rwanda."),
    ]
    col_w = (CONTENT_W - 28) // 2
    row_h = 130
    gx, gy = MARGIN, y
    for i, (kicker, head, body) in enumerate(stories):
        cx = gx + (i % 2) * (col_w + 28)
        cy = gy + (i // 2) * row_h
        d.text((cx, cy), kicker, font=SANS_B(15), fill=RED)
        cy = draw_wrapped(d, cx, cy + 20, head, SANS_B(21), col_w, leading=25)
        draw_wrapped(d, cx, cy + 2, body, SANS(17), col_w, leading=21)
        if i % 2 == 0:
            d.line([cx + col_w + 14, gy + (i // 2) * row_h,
                    cx + col_w + 14, gy + (i // 2 + 1) * row_h - 10],
                   fill=LIGHT_GREY, width=1)
    # sixth cell: globe + caption
    cx = gx + col_w + 28
    cy = gy + 2 * row_h
    draw_globe(d, cx, cy, 150, 104)
    cap = "Six regions, one day:\nEurope, the Middle East,\nAsia \u2014 and beyond."
    d.text((cx + 160, cy + 18), cap, font=SANS(17), fill=GREY)
    y = gy + 3 * row_h + 8
    d.line([MARGIN, y, W - MARGIN, y], fill=INK, width=2)
    y += 10

    # ---- ALSO TODAY footer strip ---------------------------------------
    d.text((MARGIN, y), "ALSO TODAY", font=SANS_B(18), fill=RED)
    y += 26
    items = [
        "Pentagon fails its financial audit for a 9th straight year \u2014 "
        "$4.8 trillion in assets unverified.",
        "G\u00e9rard Depardieu pleads guilty to sexual assault charges.",
        "Trump departs for Asia.",
        "Singapore seeks trusted access to advanced AI chips amid US curbs.",
    ]
    fcol_w = (CONTENT_W - 3 * 20) // 4
    for i, item in enumerate(items):
        fx = MARGIN + i * (fcol_w + 20)
        draw_wrapped(d, fx, y, item, SANS(16), fcol_w, leading=20)
    y += 86
    d.line([MARGIN, y, W - MARGIN, y], fill=LIGHT_GREY, width=1)
    y += 8
    credit = "Compiled from wire reports of 17 November 2026  \u00b7  THE WORLD \u2014 IN ONE IMAGE"
    cf = SANS(14)
    cw = d.textlength(credit, font=cf)
    d.text(((W - cw) / 2, y), credit, font=cf, fill=GREY)

    return img


def main():
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img = render()
    img.save(out, format="PNG", optimize=True)
    size = os.path.getsize(out)
    print("wrote", out, img.size, size, "bytes")
    if size > 1048576:
        print("WARNING: image exceeds the 1 MiB competition limit",
              file=sys.stderr)


if __name__ == "__main__":
    main()
