#!/usr/bin/env python3
"""THE WORLD IN ONE DAY - 21 NOVEMBER 2026.

A single 1600x1000 newsprint-style image summing up eight stories from
21 November 2026. Drawn purely with PIL shapes - no network, no randomness
without a fixed seed, no timestamps. Deterministic: running this script
twice produces byte-identical output.

Output location: $MAKEFUN_OUTPUT_DIR/entry.png when that variable is set
and non-empty (the make.fun grader mounts the repo read-only and provides
a writable output dir), otherwise entry.png next to this script.
"""

import os
import textwrap

from PIL import Image, ImageDraw, ImageFont

W, H = 1600, 1000

CREAM = (247, 241, 227)
INK = (26, 26, 26)
RED = (185, 28, 28)
DARK_RED = (140, 20, 20)
NIGHT = (11, 30, 58)
NIGHT2 = (18, 48, 88)
SKY_BLUE = (70, 110, 160)
GOLD = (232, 180, 60)
ORANGE = (240, 120, 40)
WHITE = (255, 255, 255)
GREY = (90, 90, 90)
LIGHT_GREY = (220, 214, 200)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def load_font(name, size):
    path = os.path.join(FONT_DIR, name)
    try:
        return ImageFont.truetype(path, size)
    except (OSError, IOError):
        return ImageFont.load_default()


SERIF_BOLD = lambda s: load_font("DejaVuSerif-Bold.ttf", s)
SANS_BOLD = lambda s: load_font("DejaVuSans-Bold.ttf", s)
SANS = lambda s: load_font("DejaVuSans.ttf", s)


def wrap_text(draw, text, font, max_width):
    """Greedy word wrap returning a list of lines fitting max_width."""
    lines = []
    for para in text.split("\n"):
        words = para.split()
        if not words:
            lines.append("")
            continue
        cur = words[0]
        for word in words[1:]:
            trial = cur + " " + word
            if draw.textlength(trial, font=font) <= max_width:
                cur = trial
            else:
                lines.append(cur)
                cur = word
        lines.append(cur)
    return lines


def draw_centered(draw, box, text, font, fill):
    x0, y0, x1, y1 = box
    w = draw.textlength(text, font=font)
    ascent, descent = font.getmetrics()
    draw.text(((x0 + x1 - w) / 2, y0 + (y1 - y0 - ascent - descent) / 2),
              text, font=font, fill=fill)


def starburst(draw, cx, cy, r_outer, r_inner, spikes, fill):
    import math
    pts = []
    for i in range(spikes * 2):
        r = r_outer if i % 2 == 0 else r_inner
        a = math.pi * i / spikes - math.pi / 2
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    draw.polygon(pts, fill=fill)


def draw_stars(draw, box):
    """Deterministic star field from fixed arithmetic, no randomness."""
    x0, y0, x1, y1 = box
    n = 46
    for i in range(n):
        x = x0 + ((i * 137 + 53) % (x1 - x0 - 8)) + 4
        y = y0 + ((i * 89 + 29) % (y1 - y0 - 8)) + 4
        r = 1 if i % 3 else 2
        c = (255, 255, 255) if i % 4 else (200, 210, 235)
        draw.ellipse([x - r, y - r, x + r, y + r], fill=c)


def draw_skyline(draw, x0, y_base, x1, color, seed=0):
    """Deterministic skyline silhouette along y_base."""
    widths = [46, 30, 58, 38, 66, 34, 52, 42, 60, 36, 48, 54, 40, 62, 44]
    heights = [70, 110, 84, 130, 96, 150, 78, 118, 92, 140, 104, 86, 124, 98, 112]
    x = x0
    i = 0
    while x < x1:
        w = widths[(i + seed) % len(widths)]
        h = heights[(i * 2 + seed) % len(heights)]
        draw.rectangle([x, y_base - h, min(x + w, x1), y_base], fill=color)
        # tiny lit windows
        for wy in range(y_base - h + 10, y_base - 8, 18):
            for wx in range(x + 8, min(x + w - 6, x1 - 4), 16):
                if (wx * 7 + wy * 13 + i) % 5 == 0:
                    draw.rectangle([wx, wy, wx + 4, wy + 6], fill=GOLD)
        x += w + 4
        i += 1


def draw_missile_trail(draw, x0, y0, x1, y1):
    """Bright streak with a soft glow, faked with layered lines."""
    for width, color in ((9, (60, 90, 150)), (5, (150, 180, 230)),
                         (2, (255, 255, 255))):
        draw.line([x0, y0, x1, y1], fill=color, width=width)
    # warhead glow at the head
    draw.ellipse([x1 - 7, y1 - 7, x1 + 7, y1 + 7], fill=(255, 240, 180))
    draw.ellipse([x1 - 4, y1 - 4, x1 + 4, y1 + 4], fill=WHITE)


def draw_lead_panel(draw, x0, y0, x1, y1):
    draw.rectangle([x0, y0, x1, y1], outline=INK, width=3)
    # Headline band
    hb = 96
    draw.rectangle([x0, y0, x1, y0 + hb], fill=RED)
    draw.text((x0 + 24, y0 + 12), "MISSILES FALL", font=SERIF_BOLD(52),
              fill=WHITE)
    draw.text((x0 + 24, y0 + 12 + 0), "", font=SERIF_BOLD(52), fill=WHITE)
    # second line of headline, right-aligned under the first
    f2 = SERIF_BOLD(52)
    draw.text((x0 + 24, y0 + 12 + 0), "", font=f2, fill=WHITE)
    # (headline is two lines: draw ON POLAND below MISSILES FALL)
    # -- redraw cleanly: clear band and write both lines
    draw.rectangle([x0, y0, x1, y0 + hb], fill=RED)
    draw.text((x0 + 24, y0 + 6), "MISSILES FALL", font=SERIF_BOLD(44),
              fill=WHITE)
    draw.text((x0 + 24, y0 + 52), "ON POLAND", font=SERIF_BOLD(44),
              fill=WHITE)
    draw.text((x1 - 150, y0 + 58), "LEAD STORY", font=SANS_BOLD(20),
              fill=(255, 220, 200))

    # Night sky scene
    sy0, sy1 = y0 + hb, y1 - 128
    draw.rectangle([x0, sy0, x1, sy1], fill=NIGHT)
    # horizon glow
    for i in range(40):
        c = (11 + i, 30 + i // 2, 58 + i)
        draw.line([x0, sy1 - 40 + i, x1, sy1 - 40 + i], fill=c)
    draw_stars(draw, (x0, sy0, x1, sy1 - 60))
    # missile trails arcing down
    draw_missile_trail(draw, x0 + 90, sy0 + 30, x0 + 330, sy0 + 260)
    draw_missile_trail(draw, x0 + 700, sy0 + 20, x0 + 520, sy0 + 210)
    draw_missile_trail(draw, x0 + 560, sy0 + 90, x0 + 430, sy0 + 300)
    # explosion burst
    ex, ey = x0 + 420, sy0 + 300
    starburst(draw, ex, ey, 74, 30, 12, ORANGE)
    starburst(draw, ex, ey, 48, 20, 10, GOLD)
    draw.ellipse([ex - 26, ey - 26, ex + 26, ey + 26], fill=(255, 220, 120))
    draw.ellipse([ex - 12, ey - 12, ex + 12, ey + 12], fill=WHITE)
    # smoke puffs
    for dx, dy, r in ((-90, -30, 22), (-60, -48, 16), (80, -40, 20),
                      (110, -18, 14)):
        draw.ellipse([ex + dx - r, ey + dy - r, ex + dx + r, ey + dy + r],
                     fill=(70, 70, 80))
    # skyline silhouette at the bottom of the sky
    draw_skyline(draw, x0, sy1, x1, (5, 12, 26))

    # Caption
    cap = ("Two missiles and a suspected drone came down in Poland; "
           "NATO calls it a grave violation of its airspace.")
    fcap = SANS(21)
    lines = wrap_text(draw, cap, fcap, x1 - x0 - 48)
    cy = sy1 + 16
    for line in lines:
        draw.text((x0 + 24, cy), line, font=fcap, fill=INK)
        cy += 28


def draw_panel(draw, x0, y0, x1, y1, headline, caption, scene):
    draw.rectangle([x0, y0, x1, y1], outline=INK, width=2)
    draw.rectangle([x0, y0, x1, y0 + 4], fill=RED)
    fh = SANS_BOLD(20)
    draw.text((x0 + 12, y0 + 12), headline, font=fh, fill=INK)
    scene(draw, x0 + 12, y0 + 44, x1 - 12, y1 - 52)
    fcap = SANS(14)
    lines = wrap_text(draw, caption, fcap, x1 - x0 - 24)
    cy = y1 - 50
    for line in lines[:2]:
        draw.text((x0 + 12, cy), line, font=fcap, fill=GREY)
        cy += 18


# ---- small scenes (each takes the scene box x0,y0,x1,y1) ----

def scene_wall_street(draw, x0, y0, x1, y1):
    draw.rectangle([x0, y0, x1, y1], fill=WHITE, outline=LIGHT_GREY)
    # grid
    for gy in range(y0 + 12, y1 - 4, 16):
        draw.line([x0, gy, x1, gy], fill=(235, 232, 222))
    pts = [(x0 + 8, y0 + 12), (x0 + 45, y0 + 26), (x0 + 80, y0 + 20),
           (x0 + 120, y0 + 44), (x0 + 160, y0 + 38), (x0 + 200, y0 + 62),
           (x0 + 240, y0 + 58), (x0 + 285, y0 + 82)]
    draw.line(pts, fill=RED, width=4, joint="curve")
    draw.ellipse([pts[-1][0] - 5, pts[-1][1] - 5, pts[-1][0] + 5,
                  pts[-1][1] + 5], fill=RED)
    draw.text((x0 + 10, y0 + 6), "-3.7%", font=SANS_BOLD(26), fill=RED)


def scene_uk_eu(draw, x0, y0, x1, y1):
    draw.rectangle([x0, y0, x1, y1], fill=WHITE, outline=LIGHT_GREY)
    # Union Jack-ish flag
    fx, fy, fw, fh = x0 + 14, y0 + 12, 96, 54
    draw.rectangle([fx, fy, fx + fw, fy + fh], fill=(30, 60, 140))
    draw.line([fx, fy, fx + fw, fy + fh], fill=WHITE, width=10)
    draw.line([fx + fw, fy, fx, fy + fh], fill=WHITE, width=10)
    draw.line([fx, fy, fx + fw, fy + fh], fill=RED, width=4)
    draw.line([fx + fw, fy, fx, fy + fh], fill=RED, width=4)
    draw.line([fx + fw // 2, fy, fx + fw // 2, fy + fh], fill=WHITE, width=16)
    draw.line([fx, fy + fh // 2, fx + fw, fy + fh // 2], fill=WHITE, width=16)
    draw.line([fx + fw // 2, fy, fx + fw // 2, fy + fh], fill=RED, width=8)
    draw.line([fx, fy + fh // 2, fx + fw, fy + fh // 2], fill=RED, width=8)
    # EU flag
    ex, ey = x0 + 130, y0 + 12
    draw.rectangle([ex, ey, ex + 96, ey + 54], fill=(20, 50, 130))
    import math
    for i in range(12):
        a = 2 * math.pi * i / 12 - math.pi / 2
        sx = ex + 48 + 20 * math.cos(a)
        sy = ey + 27 + 16 * math.sin(a)
        draw.ellipse([sx - 3, sy - 3, sx + 3, sy + 3], fill=GOLD)
    # handshake-ish motif: two clasped arcs
    hy = y1 - 18
    draw.arc([x0 + 90, hy - 14, x0 + 150, hy + 14], 180, 360, fill=INK,
             width=4)
    draw.arc([x0 + 150, hy - 14, x0 + 210, hy + 14], 180, 360, fill=RED,
             width=4)
    draw.line([x0 + 120, hy, x0 + 180, hy], fill=INK, width=3)


def scene_russia_strike(draw, x0, y0, x1, y1):
    # dusk gradient bands
    bands = [(250, 170, 90), (230, 120, 80), (150, 80, 110), (70, 50, 100)]
    bh = (y1 - y0) // len(bands)
    for i, c in enumerate(bands):
        draw.rectangle([x0, y0 + i * bh, x1, y0 + (i + 1) * bh], fill=c)
    draw.rectangle([x0, y0 + 3 * bh, x1, y1], fill=(50, 38, 80))
    # drone swarm: small quadcopters
    for dx, dy, s in ((40, 14, 1.0), (110, 26, 0.8), (180, 10, 1.1),
                      (240, 30, 0.7), (70, 44, 0.7), (200, 48, 0.8)):
        cx, cy = x0 + dx, y0 + dy
        r = int(9 * s)
        draw.line([cx - r, cy - r, cx + r, cy + r], fill=INK, width=2)
        draw.line([cx - r, cy + r, cx + r, cy - r], fill=INK, width=2)
        for px, py in ((-r, -r), (r, -r), (-r, r), (r, r)):
            draw.ellipse([cx + px - 3, cy + py - 3, cx + px + 3,
                          cy + py + 3], fill=INK)
        draw.ellipse([cx - 4, cy - 3, cx + 4, cy + 3], fill=(40, 40, 40))
    draw_skyline(draw, x0, y1, x1, (20, 16, 34), seed=3)


def scene_cyclone(draw, x0, y0, x1, y1):
    draw.rectangle([x0, y0, x1, y1], fill=(190, 215, 230))
    # coastline: sand diagonal bottom-right
    draw.polygon([(x0 + 150, y1), (x1, y1), (x1, y0 + 55),
                  (x0 + 210, y0 + 90)], fill=(232, 210, 160))
    draw.line([x0 + 150, y1, x1, y0 + 55], fill=(120, 140, 150), width=3)
    # white spiral
    cx, cy = x0 + 105, y0 + 46
    for r, a0, a1 in ((34, 0, 300), (25, 40, 330), (16, 80, 350),
                     (8, 120, 360)):
        draw.arc([cx - r, cy - r, cx + r, cy + r], a0, a1, fill=WHITE,
                 width=5)
    draw.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=WHITE)
    # rain streaks
    for i in range(10):
        rx = x0 + 20 + i * 28
        ry = y0 + 8 + (i % 3) * 10
        draw.line([rx, ry, rx - 6, ry + 16], fill=(90, 120, 150), width=2)


def scene_bank(draw, x0, y0, x1, y1):
    draw.rectangle([x0, y0, x1, y1], fill=WHITE, outline=LIGHT_GREY)
    cx = (x0 + x1) // 2
    cy = (y0 + y1) // 2 - 4
    # shield
    draw.polygon([(cx - 42, cy - 34), (cx + 42, cy - 34), (cx + 42, cy + 6),
                  (cx, cy + 42), (cx - 42, cy + 6)], fill=(25, 60, 110),
                 outline=INK)
    # padlock
    draw.arc([cx - 13, cy - 16, cx + 13, cy + 4], 180, 360, fill=GOLD,
             width=5)
    draw.rectangle([cx - 16, cy - 2, cx + 16, cy + 22], fill=GOLD)
    draw.ellipse([cx - 3, cy + 5, cx + 3, cy + 11], fill=(25, 60, 110))
    draw.line([cx, cy + 10, cx, cy + 16], fill=(25, 60, 110), width=3)
    # warning ticks
    draw.text((x0 + 12, y1 - 20), "!", font=SANS_BOLD(18), fill=RED)
    draw.text((x1 - 24, y1 - 20), "!", font=SANS_BOLD(18), fill=RED)


def scene_cop31(draw, x0, y0, x1, y1):
    draw.rectangle([x0, y0, x1, y1], fill=(225, 240, 225))
    cx, cy = x0 + 78, y0 + 46
    draw.ellipse([cx - 40, cy - 40, cx + 40, cy + 40], fill=(60, 130, 200),
                 outline=INK, width=2)
    # land blobs
    draw.ellipse([cx - 28, cy - 26, cx - 2, cy - 2], fill=(80, 170, 90))
    draw.ellipse([cx + 2, cy + 4, cx + 30, cy + 28], fill=(80, 170, 90))
    draw.ellipse([cx + 6, cy - 30, cx + 26, cy - 12], fill=(100, 190, 100))
    # green leaf
    lx, ly = x0 + 205, y0 + 30
    draw.pieslice([lx, ly, lx + 66, ly + 40], 200, 20, fill=(40, 160, 70))
    draw.line([lx + 4, ly + 36, lx + 62, ly + 6], fill=(20, 110, 40),
              width=3)
    draw.text((x0 + 176, y1 - 22), "COP31", font=SANS_BOLD(20),
              fill=(20, 110, 40))


def scene_bolsonaro(draw, x0, y0, x1, y1):
    draw.rectangle([x0, y0, x1, y1], fill=(225, 235, 245))
    bx0, by1 = x0 + 60, y1 - 6
    bw, bh = 190, 66
    draw.rectangle([bx0, by1 - bh, bx0 + bw, by1], fill=WHITE, outline=INK,
                   width=2)
    # windows
    for r in range(2):
        for c in range(5):
            wx = bx0 + 14 + c * 34
            wy = by1 - bh + 12 + r * 24
            draw.rectangle([wx, wy, wx + 18, wy + 14], fill=(120, 180, 220),
                           outline=INK)
    # red cross sign on the roof
    cx = bx0 + bw // 2
    cy = by1 - bh - 12
    draw.rectangle([cx - 5, cy - 14, cx + 5, cy + 14], fill=RED)
    draw.rectangle([cx - 14, cy - 5, cx + 14, cy + 5], fill=RED)
    # ground line
    draw.line([x0 + 10, by1, x1 - 10, by1], fill=INK, width=2)


def main():
    img = Image.new("RGB", (W, H), CREAM)
    draw = ImageDraw.Draw(img)

    # ---- Masthead ----
    title = "THE WORLD IN ONE DAY \u2014 21 NOVEMBER 2026"
    ftitle = SERIF_BOLD(50)
    tw = draw.textlength(title, font=ftitle)
    draw.text(((W - tw) / 2, 26), title, font=ftitle, fill=INK)
    draw.line([40, 108, W - 40, 108], fill=INK, width=3)
    draw.line([40, 114, W - 40, 114], fill=RED, width=2)

    # ---- Lead panel (left) ----
    draw_lead_panel(draw, 40, 130, 830, 930)

    # ---- Seven smaller panels (right grid) ----
    gx0, gy0, gx1 = 850, 130, 1560
    gap = 16
    cell_w = (gx1 - gx0 - gap) // 2
    cell_h = (930 - gy0 - 3 * gap) // 4
    panels = [
        ("WALL STREET SLUMPS",
         "S&P 500 and Dow enter correction as AI shares sell off.",
         scene_wall_street),
        ("UK\u2013EU DEALS",
         "Deals signed on food trade, carbon markets and youth mobility.",
         scene_uk_eu),
        ("RUSSIA'S BIGGEST STRIKE",
         "400 drones and 110 missiles; 2 dead, 42 injured in Kryvyi Rih.",
         scene_russia_strike),
        ("CYCLONE AKVAN",
         "Cyclone crosses the Odisha coast, then weakens.",
         scene_cyclone),
        ("BANK CYBERATTACK",
         "JPMorgan, Visa and Mastercard hit via third-party vendors.",
         scene_bank),
        ("COP31",
         "Climate talks in Turkey enter their crucial final stage.",
         scene_cop31),
        ("BOLSONARO HOSPITALISED",
         "Brazil's ex-president taken to hospital with severe abdominal pain.",
         scene_bolsonaro),
    ]
    for i, (headline, caption, scene) in enumerate(panels):
        row, col = divmod(i, 2)
        if i == 6:
            # last panel spans both columns
            x0 = gx0
            x1 = gx1
        else:
            x0 = gx0 + col * (cell_w + gap)
            x1 = x0 + cell_w
        y0 = gy0 + row * (cell_h + gap)
        y1 = y0 + cell_h
        # wide last panel: scene function gets the full box; wrap scene
        # call in a lambda-free way by passing the function directly.
        draw_panel(draw, x0, y0, x1, y1, headline, caption, scene)

    # ---- Footer ----
    footer = ("21 November 2026 \u00b7 Eight stories, one image \u00b7 "
              "Built by an AI agent for make.fun")
    ffoot = SANS(17)
    fw = draw.textlength(footer, font=ffoot)
    draw.line([40, 946, W - 40, 946], fill=INK, width=2)
    draw.text(((W - fw) / 2, 956), footer, font=ffoot, fill=INK)

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or os.path.dirname(
        os.path.abspath(__file__))
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "entry.png")
    img.save(out_path, format="PNG")
    print("Wrote", out_path)


if __name__ == "__main__":
    main()
