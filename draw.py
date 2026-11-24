#!/usr/bin/env python3
"""Draw the news-image-20261124 front page with Pillow.

One-page newspaper front page for Tuesday 24 November 2026, built from
that morning's reporting. Three layout variants; the caller picks one
with --variant 1|2|3. Variant 1 is the hero-lead layout.
Usage: python3 draw.py [--variant N] [--out path]
"""
import argparse
import sys

from PIL import Image, ImageDraw, ImageFont

W = 1024
H = 1024
PAPER = (247, 242, 231)
INK = (17, 17, 17)
RED = (178, 32, 44)
BLUE = (29, 78, 137)
TEAL = (14, 106, 102)
GOLD = (176, 124, 22)
GREY = (90, 86, 78)
LIGHT = (232, 226, 212)
DARKBAND = (24, 24, 24)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(d, text, fnt, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if d.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def para(d, x, y, text, fnt, max_w, leading, fill=INK):
    for line in wrap(d, text, fnt, max_w):
        d.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def headline_block(d, x, y, max_w, lines, fnt, leading, fill=INK):
    for line in lines:
        d.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def masthead(d):
    d.rectangle([0, 0, W, 8], fill=INK)
    d.text((W // 2, 26), "THE WORLD", font=font(SERIF_B, 84),
           fill=INK, anchor="ma")
    d.text((W // 2, 116), "THE DAY'S NEWS  •  IN ONE PAGE",
           font=font(SANS_B, 15), fill=GREY, anchor="ma")
    d.line([28, 142, W - 28, 142], fill=INK, width=2)
    # Dateline band
    d.rectangle([28, 152, W - 28, 192], fill=DARKBAND)
    d.text((W // 2, 158), "TUESDAY  •  24 NOVEMBER 2026",
           font=font(SANS_B, 26), fill=(255, 255, 255), anchor="ma")


def ticker(d, y=960):
    d.rectangle([28, y, W - 28, y + 56], fill=DARKBAND)
    txt = ("ALSO TODAY  —  NATO vows space defence after satellite report  "
           "•  Denmark court backs 'ghetto law'  •  US court gives Trump "
           "path to erase hush-money conviction  •  Thousands flee "
           "Manchester concert after unknown substance released  •  Modi "
           "opens AI centre at IIT Patna  •  Chess: Gukesh defends world "
           "title vs Sindarov in Geneva")
    para(d, 44, y + 4, txt, font(SANS, 15), W - 88, 17,
         fill=(240, 238, 230))


# ---- small illustrations (simple flat vector scenes) ----

def draw_ship(d, x0, y0, x1, y1):
    """Warship at sea, on fire, at Benghazi port. Scales to its box."""
    bw, bh = x1 - x0, y1 - y0
    sx, sy = bw / 400.0, bh / 150.0

    def X(v):
        return x0 + v * sx

    def Y(v):
        return y0 + v * sy

    d.rectangle([x0, y0, x1, y1], fill=(178, 214, 228))
    d.rectangle([x0, Y(108), x1, y1], fill=(38, 92, 128))
    for yy in range(118, 148, 16):
        d.line([x0 + 8, Y(yy), x1 - 8, Y(yy)], fill=(120, 170, 200), width=2)
    # distant port cranes
    d.line([X(30), Y(108), X(30), Y(58)], fill=(70, 70, 70), width=4)
    d.line([X(30), Y(58), X(74), Y(72)], fill=(70, 70, 70), width=4)
    d.line([X(330), Y(108), X(330), Y(66)], fill=(70, 70, 70), width=4)
    d.line([X(330), Y(66), X(292), Y(80)], fill=(70, 70, 70), width=4)
    # hull
    hull = [(X(40), Y(92)), (X(330), Y(92)), (X(310), Y(118)),
            (X(62), Y(118))]
    d.polygon(hull, fill=(52, 58, 64))
    d.rectangle([X(90), Y(62), X(210), Y(92)], fill=(72, 80, 88))
    d.rectangle([X(150), Y(40), X(168), Y(62)], fill=(72, 80, 88))
    d.line([X(159), Y(40), X(159), Y(22)], fill=INK, width=3)
    d.polygon([(X(159), Y(22)), (X(185), Y(30)), (X(159), Y(38))],
              fill=RED)
    # fire + smoke over the stern
    for cx, cy, r, col in [(250, 46, 26, (255, 122, 26)),
                           (272, 30, 20, (255, 196, 0)),
                           (232, 28, 16, (255, 196, 0))]:
        d.ellipse([X(cx) - r * sx, Y(cy) - r * sy, X(cx) + r * sx,
                   Y(cy) + r * sy], fill=col)
    for cx, cy, r in [(300, 8, 18), (322, -2, 14), (282, -6, 12)]:
        d.ellipse([X(cx) - r * sx, Y(cy) - r * sy, X(cx) + r * sx,
                   Y(cy) + r * sy], fill=(120, 118, 112))
    d.text((x0 + 12, y1 - 26), "BENGHAZI PORT, LIBYA",
           font=font(SANS_B, 13), fill=(255, 255, 255))


def draw_chart(d, x0, y0, x1, y1):
    d.rectangle([x0, y0, x1, y1], fill=(222, 236, 222))
    d.rectangle([x0, y0, x1, y0 + 26], fill=TEAL)
    d.text((x0 + 8, y0 + 4), "STOCKS SOAR", font=font(SANS_B, 13),
           fill=(255, 255, 255))
    pts = [(x0 + 16, y1 - 30), (x0 + 70, y1 - 52), (x0 + 120, y1 - 44),
           (x0 + 175, y1 - 78), (x0 + 225, y1 - 66), (x0 + 275, y1 - 108)]
    d.line(pts, fill=TEAL, width=5, joint="curve")
    d.polygon([(pts[-1][0], pts[-1][1]), (pts[-1][0] + 16, pts[-1][1] + 4),
               (pts[-1][0] + 2, pts[-1][1] + 16)], fill=TEAL)
    for gx in range(x0 + 16, x1 - 10, 44):
        d.line([gx, y1 - 22, gx, y1 - 12], fill=GREY, width=2)


def draw_climate(d, x0, y0, x1, y1):
    d.rectangle([x0, y0, x1, y1], fill=(232, 222, 196))
    # sun half-hidden by cloud, cracked earth below
    d.ellipse([x0 + 100, y0 + 6, x0 + 176, y0 + 82], fill=(232, 148, 32))
    for cx, cy, r in [(140, 62, 26), (180, 68, 22), (104, 68, 20)]:
        d.ellipse([x0 + cx - r, y0 + cy - r // 2, x0 + cx + r,
                   y0 + cy + r // 2], fill=(150, 146, 138))
    d.rectangle([x0, y0 + 84, x1, y1], fill=(196, 160, 110))
    d.line([(x0 + 30, y0 + 94), (x0 + 110, y0 + 106), (x0 + 180, y0 + 96),
            (x0 + 250, y0 + 108)], fill=(120, 86, 50), width=4)


def draw_factory(d, x0, y0, x1, y1):
    d.rectangle([x0, y0, x1, y1], fill=(244, 214, 200))
    d.rectangle([x0 + 30, y0 + 70, x0 + 250, y1 - 14], fill=(120, 66, 60))
    d.rectangle([x0 + 30, y0 + 70, x0 + 250, y0 + 86], fill=(90, 48, 44))
    d.rectangle([x0 + 200, y0 + 20, x0 + 224, y0 + 72], fill=(90, 48, 44))
    for wx in (60, 110, 160):
        d.rectangle([x0 + wx, y0 + 100, x0 + wx + 28, y0 + 128],
                    fill=(255, 196, 0))
    for cx, cy, r, col in [(212, 8, 22, (255, 122, 26)),
                           (232, -6, 16, (255, 196, 0))]:
        d.ellipse([x0 + cx - r, y0 + cy - r, x0 + cx + r, y0 + cy + r],
                  fill=col)
    for cx, cy, r in [(250, -14, 14), (268, -4, 11)]:
        d.ellipse([x0 + cx - r, y0 + cy - r, x0 + cx + r, y0 + cy + r],
                  fill=(110, 108, 102))


def draw_city(d, x0, y0, x1, y1):
    d.rectangle([x0, y0, x1, y1], fill=(36, 44, 66))
    for bx, bw, bh in [(20, 52, 72), (86, 44, 96), (144, 58, 62),
                       (216, 46, 88)]:
        d.rectangle([x0 + bx, y1 - bh, x0 + bx + bw, y1 - 10],
                    fill=(70, 78, 100))
        for wy in range(y1 - bh + 12, y1 - 18, 20):
            for wx in range(x0 + bx + 8, x0 + bx + bw - 8, 16):
                d.rectangle([wx, wy, wx + 7, wy + 9], fill=(255, 196, 0))
    # drone + blast
    d.ellipse([x0 + 150, y0 + 22, x0 + 178, y0 + 36], fill=(200, 200, 200))
    d.line([x0 + 138, y0 + 29, x0 + 190, y0 + 29], fill=(200, 200, 200),
           width=3)
    for cx, cy, r, col in [(60, 40, 16, (255, 122, 26)),
                           (76, 28, 11, (255, 196, 0))]:
        d.ellipse([x0 + cx - r, y0 + cy - r, x0 + cx + r, y0 + cy + r],
                  fill=col)


def draw_trophy(d, x0, y0, x1, y1):
    d.rectangle([x0, y0, x1, y1], fill=(238, 226, 190))
    # court lines
    d.line([x0, y1 - 34, x1, y1 - 34], fill=(255, 255, 255), width=3)
    d.line([x0 + 150, y0 + 10, x0 + 150, y1 - 34], fill=(255, 255, 255),
           width=2)
    # trophy
    cx = x0 + 150
    d.polygon([(cx - 52, y0 + 22), (cx + 52, y0 + 22), (cx + 38, y0 + 78),
               (cx - 38, y0 + 78)], fill=GOLD)
    d.arc([cx - 74, y0 + 22, cx - 30, y0 + 66], 90, 270, fill=GOLD, width=8)
    d.arc([cx + 30, y0 + 22, cx + 74, y0 + 66], -90, 90, fill=GOLD, width=8)
    d.rectangle([cx - 14, y0 + 78, cx + 14, y0 + 96], fill=GOLD)
    d.rectangle([cx - 34, y0 + 96, cx + 34, y0 + 108], fill=GOLD)
    # tennis ball
    d.ellipse([x0 + 238, y0 + 96, x0 + 272, y0 + 130], fill=(190, 220, 60))
    d.arc([x0 + 238, y0 + 96, x0 + 272, y0 + 130], 200, 340, fill=(255, 255, 255),
          width=3)


def draw_scales(d, x0, y0, x1, y1):
    d.rectangle([x0, y0, x1, y1], fill=(224, 230, 238))
    cx = x0 + 150
    d.line([cx, y0 + 18, cx, y1 - 26], fill=INK, width=5)
    d.line([cx - 96, y0 + 34, cx + 96, y0 + 34], fill=INK, width=5)
    d.polygon([(cx - 8, y0 + 12), (cx + 8, y0 + 12), (cx, y0 + 26)],
              fill=INK)
    for sx in (cx - 96, cx + 96):
        d.line([sx, y0 + 34, sx, y0 + 62], fill=INK, width=3)
        d.polygon([(sx - 34, y0 + 62), (sx + 34, y0 + 62), (sx, y0 + 96)],
                  fill=BLUE)
    d.rectangle([cx - 46, y1 - 26, cx + 46, y1 - 14], fill=INK)


def panel(img, x0, x1, y0, y1, kicker, head, body, ill, accent,
          head_size=24, ill_h=80):
    d = ImageDraw.Draw(img)
    d.rectangle([x0, y0, x1, y1], outline=INK, width=2, fill=(255, 255, 255))
    d.rectangle([x0, y0, x1, y0 + 30], fill=accent)
    d.text((x0 + 10, y0 + 5), kicker, font=font(SANS_B, 14),
           fill=(255, 255, 255))
    # Draw the illustration at its design size, then scale it into the box
    # so no panel illustration can ever overflow its frame.
    tmp = Image.new("RGB", (320, 118), (255, 255, 255))
    td = ImageDraw.Draw(tmp)
    ill(td, 0, 0, 320, 118)
    tmp = tmp.resize((x1 - x0 - 16, ill_h), Image.LANCZOS)
    img.paste(tmp, (x0 + 8, y0 + 36))
    hy = y0 + 36 + ill_h + 8
    hy = headline_block(d, x0 + 10, hy, x1 - x0 - 20,
                         wrap(d, head, font(SERIF_B, head_size),
                              x1 - x0 - 20),
                         font(SERIF_B, head_size), head_size + 4)
    para(d, x0 + 10, hy + 4, body, font(SANS, 14), x1 - x0 - 20, 16)


def lead_hero(d, x0, y0, x1, y1):
    d.rectangle([x0, y0, x1, y1], outline=INK, width=2, fill=(255, 255, 255))
    d.rectangle([x0, y0, x1, y0 + 30], fill=RED)
    d.text((x0 + 12, y0 + 5), "LEAD  •  BLACK SEA WAR", font=font(SANS_B, 14),
           fill=(255, 255, 255))
    tx = x0 + 14
    ty = y0 + 44
    # Fit the headline inside the text column (never under the picture).
    size = 52
    while (size > 36 and
           d.textlength("RUSSIAN WARSHIP", font=font(SERIF_B, size)) > 520):
        size -= 2
    ty = headline_block(d, tx, ty, 520,
                        ["UKRAINE SINKS", "RUSSIAN WARSHIP"],
                        font(SERIF_B, size), size + 4)
    ty = para(d, tx, ty + 8,
              "A Russian Navy missile corvette, believed to be the "
              "Merkury, is hit by an explosion and fire at Benghazi port "
              "in Libya. Ukraine claims the strike.",
              font(SANS, 16), 520, 20)
    para(d, tx, ty + 6,
         "Cargo ship Sparta II also caught fire after a drone strike in "
         "the Gulf of Finland.",
         font(SANS, 16), 520, 20)
    draw_ship(d, x0 + 556, y0 + 44, x1 - 14, y1 - 16)


def build_v1():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    masthead(d)
    lead_hero(d, 28, 204, W - 28, 460)
    y0, y1 = 472, 704
    xs = [(28, 348), (360, 680), (692, 996)]
    panel(img, *xs[0], y0, y1, "MARKETS", "NVIDIA GAINS ALMOST $1TN",
          "Jensen Huang is reinstated as chief executive after President "
          "Trump intervenes. Tech stocks rally.",
          draw_chart, TEAL)
    panel(img, *xs[1], y0, y1, "CLIMATE", "COP31 ENDS WITH NO DEAL",
          "The climate summit closes without a final agreement after days "
          "of deadlock.", draw_climate, GOLD)
    panel(img, *xs[2], y0, y1, "ASIA", "24 KILLED IN FACTORY FIRE",
          "A blaze at a candy factory in Indonesia kills at least 24; 34 "
          "people are missing as investigators probe the cause.",
          draw_factory, RED)
    y0, y1 = 716, 948
    panel(img, *xs[0], y0, y1, "WAR", "14 KILLED IN KYIV REGION",
          "Russian drone and missile attacks kill 14 people and damage "
          "homes in Kyiv Oblast.", draw_city, BLUE)
    panel(img, *xs[1], y0, y1, "SPORT", "ALCARAZ WINS ATP FINALS",
          "Beats Alexander Zverev in Turin for a maiden title. UK "
          "confirmed as host of the 2035 Women's World Cup.",
          draw_trophy, TEAL)
    panel(img, *xs[2], y0, y1, "LAW", "MYANMAR GUILTY OF GENOCIDE",
          "The court rules Myanmar committed genocide against the "
          "Rohingya.", draw_scales, BLUE)
    ticker(d)
    return img


def build_v2():
    """Split hero: lead left, markets right on top; 3+3 below."""
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    masthead(d)
    # lead, narrower, left 60%
    d.rectangle([28, 204, 620, 460], outline=INK, width=2,
                fill=(255, 255, 255))
    d.rectangle([28, 204, 620, 234], fill=RED)
    d.text((40, 209), "LEAD  •  BLACK SEA WAR", font=font(SANS_B, 14),
           fill=(255, 255, 255))
    ty = headline_block(d, 40, 246, 560, ["UKRAINE SINKS", "RUSSIAN WARSHIP"],
                        font(SERIF_B, 40), 44)
    draw_ship(d, 40, 348, 606, 450)
    panel(img, 632, 996, 204, 460, "MARKETS",
          "NVIDIA GAINS ALMOST $1TN",
          "Jensen Huang reinstated as chief executive after President "
          "Trump intervenes. Tech stocks rally.",
          draw_chart, TEAL, head_size=25)
    y0, y1 = 472, 704
    xs = [(28, 348), (360, 680), (692, 996)]
    panel(img, *xs[0], y0, y1, "CLIMATE", "COP31 ENDS WITH NO DEAL",
          "The climate summit closes without a final agreement after days "
          "of deadlock.", draw_climate, GOLD)
    panel(img, *xs[1], y0, y1, "ASIA", "24 KILLED IN FACTORY FIRE",
          "A blaze at a candy factory in Indonesia kills at least 24; 34 "
          "people are missing as investigators probe the cause.",
          draw_factory, RED)
    panel(img, *xs[2], y0, y1, "WAR", "14 KILLED IN KYIV REGION",
          "Russian drone and missile attacks kill 14 people and damage "
          "homes in Kyiv Oblast.", draw_city, BLUE)
    y0, y1 = 716, 948
    panel(img, *xs[0], y0, y1, "SPORT", "ALCARAZ WINS ATP FINALS",
          "Beats Alexander Zverev in Turin for a maiden title. UK "
          "confirmed as host of the 2035 Women's World Cup.",
          draw_trophy, TEAL)
    panel(img, *xs[1], y0, y1, "LAW", "MYANMAR GUILTY OF GENOCIDE",
          "The court rules Myanmar committed genocide against the "
          "Rohingya.", draw_scales, BLUE)
    panel(img, *xs[2], y0, y1, "WORLD", "NATO VOWS SPACE DEFENCE",
          "Alliance pledges to defend space after a report of a Russian "
          "nuclear satellite.", draw_city, BLUE)
    ticker(d)
    return img


def build_v3():
    """Six equal panels, no hero image."""
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    masthead(d)
    xs = [(28, 348), (360, 680), (692, 996)]
    rows = [
        (204, 436, [
            ("BLACK SEA WAR", "UKRAINE SINKS RUSSIAN WARSHIP",
             "Corvette believed to be the Merkury hit by explosion and "
             "fire at Benghazi port, Libya. Ukraine claims the strike.", draw_ship, RED),
            ("MARKETS", "NVIDIA GAINS ALMOST $1TN",
             "Jensen Huang reinstated as chief executive after President "
             "Trump intervenes. Tech stocks rally.", draw_chart, TEAL),
            ("CLIMATE", "COP31 ENDS WITH NO DEAL",
             "The climate summit closes without a final agreement after "
             "days of deadlock.", draw_climate, GOLD),
        ]),
        (448, 680, [
            ("ASIA", "24 KILLED IN FACTORY FIRE",
             "A blaze at a candy factory in Indonesia kills at least 24; "
             "34 people are missing as investigators probe the cause.",
             draw_factory, RED),
            ("WAR", "14 KILLED IN KYIV REGION",
             "Russian drone and missile attacks kill 14 people and damage "
             "homes in Kyiv Oblast.", draw_city, BLUE),
            ("SPORT", "ALCARAZ WINS ATP FINALS",
             "Beats Alexander Zverev in Turin for a maiden title. UK "
             "confirmed as host of the 2035 Women's World Cup.",
             draw_trophy, TEAL),
        ]),
    ]
    for y0, y1, items in rows:
        for (x0, x1), (kick, head, body, ill, accent) in zip(xs, items):
            panel(img, x0, x1, y0, y1, kick, head, body, ill, accent,
                  head_size=24)
    # The day in numbers strip.
    d.rectangle([28, 692, W - 28, 940], outline=INK, width=2,
                fill=(255, 255, 255))
    d.rectangle([28, 692, W - 28, 722], fill=DARKBAND)
    d.text((W // 2, 697), "THE DAY IN NUMBERS", font=font(SANS_B, 15),
           fill=(255, 255, 255), anchor="ma")
    stats = [("$1tn", "Nvidia's gain in a day"),
             ("24", "killed in the Indonesia factory fire"),
             ("14", "killed in Kyiv region strikes"),
             ("2035", "Women's World Cup goes to the UK")]
    for i, (num, label) in enumerate(stats):
        cx = 28 + i * 242 + 121
        d.text((cx, 742), num, font=font(SERIF_B, 52), fill=RED,
               anchor="ma")
        para(d, 28 + i * 242 + 16, 812, label, font(SANS, 15), 210, 19)
    ticker(d)
    return img


BUILDERS = {1: build_v1, 2: build_v2, 3: build_v3}


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--variant", type=int, default=1, choices=[1, 2, 3])
    ap.add_argument("--out", default="entry.png")
    args = ap.parse_args(argv)
    img = BUILDERS[args.variant]()
    img.save(args.out, format="PNG", optimize=True)
    print(f"wrote {args.out} variant={args.variant} "
          f"{img.size[0]}x{img.size[1]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
