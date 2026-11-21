#!/usr/bin/env python3
"""The World in One Day - 21 November 2026.

A newspaper front page summing up eight world-news stories of
21 November 2026 in a single 1600x1000 image. Pure PIL drawing:
no network, no randomness, fully deterministic.
"""

import math
from PIL import Image, ImageDraw, ImageFont

W, H = 1600, 1000

CREAM = (247, 242, 231)
INK = (26, 26, 26)
RED = (176, 32, 32)
RED_DARK = (140, 20, 20)
GREY = (90, 86, 78)
LIGHT_GREY = (210, 204, 190)
BLUE = (31, 68, 120)
GREEN = (34, 110, 70)
GOLD = (196, 148, 40)
SKY = (214, 228, 240)
SKY_DARK = (52, 68, 96)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def text_block(draw, x, y, lines, fnt, fill, align="left", max_w=0, leading=4):
    for line in lines:
        w = draw.textlength(line, font=fnt)
        lx = x + (max_w - w) // 2 if align == "center" else x
        draw.text((lx, y), line, font=fnt, fill=fill)
        y += fnt.size + leading
    return y


def rule(draw, x0, y, x1, color=INK, width=2):
    draw.line([(x0, y), (x1, y)], fill=color, width=width)


def kicker(draw, x, y, label, color=RED):
    f = font(SANS_B, 15)
    draw.text((x, y), label.upper(), font=f, fill=color)
    return y + 20


def panel(draw, x, y, w, h, border=INK, bw=2):
    draw.rectangle([x, y, x + w, y + h], outline=border, width=bw)


def headline(draw, x, y, text, size, max_w, color=INK, leading=2):
    f = font(SERIF_B, size)
    lines = wrap(draw, text, f, max_w)
    return text_block(draw, x, y, lines, f, color, leading=leading)


# ---------------------------------------------------------------- scenes
def scene_missiles(draw, x, y, w, h):
    """Night sky, missile trails arcing down, red explosions."""
    draw.rectangle([x, y, x + w, y + h], fill=SKY_DARK)
    # stars
    for sx, sy in [(0.08, 0.15), (0.2, 0.08), (0.35, 0.2), (0.5, 0.1),
                   (0.62, 0.18), (0.78, 0.08), (0.9, 0.2), (0.45, 0.28)]:
        px, py = x + int(w * sx), y + int(h * sy)
        draw.ellipse([px - 2, py - 2, px + 2, py + 2], fill=(240, 240, 220))
    # ground
    gy = y + int(h * 0.78)
    draw.rectangle([x, gy, x + w, y + h], fill=(38, 44, 40))
    draw.line([(x, gy), (x + w, gy)], fill=(120, 120, 110), width=2)
    # missile trails
    for fx, fy, tx in [(0.18, 0.06, 0.28), (0.55, 0.02, 0.62), (0.82, 0.08, 0.78)]:
        sx, sy = x + int(w * fx), y + int(h * fy)
        ex, ey = x + int(w * tx), gy - 6
        steps = 24
        pts = []
        for i in range(steps + 1):
            t = i / steps
            px = sx + (ex - sx) * t
            py = sy + (ey - sy) * t + 26 * math.sin(math.pi * t)
            pts.append((px, py))
        draw.line(pts, fill=(255, 210, 120), width=3)
        draw.ellipse([ex - 5, ey - 5, ex + 5, ey + 5], fill=(255, 190, 60))
    # explosions
    for cx, cy, r in [(0.28, 0.74, 34), (0.62, 0.76, 28), (0.78, 0.75, 22)]:
        ex, ey = x + int(w * cx), y + int(h * cy)
        for ang in range(0, 360, 30):
            a = math.radians(ang)
            r2 = r * (0.6 + 0.4 * ((ang // 30) % 2))
            draw.line([(ex, ey),
                       (ex + r2 * math.cos(a), ey + r2 * math.sin(a))],
                      fill=(255, 120, 40), width=5)
        draw.ellipse([ex - 12, ey - 12, ex + 12, ey + 12], fill=(255, 200, 60))


def scene_chart(draw, x, y, w, h):
    """Falling stock chart with red arrow."""
    draw.rectangle([x, y, x + w, y + h], fill=(255, 255, 255))
    draw.rectangle([x, y, x + w, y + h], outline=LIGHT_GREY, width=1)
    # grid
    for i in range(1, 4):
        gy = y + h * i // 4
        draw.line([(x, gy), (x + w, gy)], fill=(232, 228, 218), width=1)
    pts = []
    n = 9
    for i in range(n):
        px = x + 12 + i * (w - 24) // (n - 1)
        py = y + 14 + int((h - 40) * (i / (n - 1)) ** 1.4)
        pts.append((px, py))
    draw.line(pts, fill=RED, width=4)
    for px, py in pts:
        draw.ellipse([px - 4, py - 4, px + 4, py + 4], fill=RED_DARK)
    # arrow head at the end
    ex, ey = pts[-1]
    draw.polygon([(ex, ey + 16), (ex - 14, ey - 4), (ex + 2, ey - 2)],
                 fill=RED_DARK)
    draw.text((x + w - 62, y + 6), "-3.7%", font=font(SANS_B, 22), fill=RED)


def scene_handshake(draw, x, y, w, h):
    """Two flags (UK + EU) and a handshake arc."""
    draw.rectangle([x, y, x + w, y + h], fill=(238, 240, 246))
    # flag poles
    draw.line([(x + w * 0.30, y + 12), (x + w * 0.30, y + h - 12)],
              fill=INK, width=3)
    draw.line([(x + w * 0.70, y + 12), (x + w * 0.70, y + h - 12)],
              fill=INK, width=3)
    # UK flag (simplified cross)
    fx, fy, fw, fh = x + w * 0.08, y + 12, w * 0.20, 34
    draw.rectangle([fx, fy, fx + fw, fy + fh], fill=(30, 60, 140))
    draw.rectangle([fx + fw / 2 - 4, fy, fx + fw / 2 + 4, fy + fh],
                   fill=(255, 255, 255))
    draw.rectangle([fx, fy + fh / 2 - 4, fx + fw, fy + fh / 2 + 4],
                   fill=(255, 255, 255))
    draw.rectangle([fx + fw / 2 - 2, fy, fx + fw / 2 + 2, fy + fh],
                   fill=(200, 30, 40))
    draw.rectangle([fx, fy + fh / 2 - 2, fx + fw, fy + fh / 2 + 2],
                   fill=(200, 30, 40))
    # EU flag (circle of stars)
    ex, ey, ew, eh = x + w * 0.72, y + 12, w * 0.20, 34
    draw.rectangle([ex, ey, ex + ew, ey + eh], fill=(20, 50, 140))
    for i in range(8):
        a = math.radians(i * 45)
        sx = ex + ew / 2 + 11 * math.cos(a)
        sy = ey + eh / 2 + 8 * math.sin(a)
        draw.ellipse([sx - 2, sy - 2, sx + 2, sy + 2], fill=(255, 220, 60))
    # handshake: two clasped arcs
    cy = y + h - 26
    draw.arc([x + w * 0.28, cy - 22, x + w * 0.72, cy + 22],
             start=180, end=360, fill=INK, width=4)
    draw.arc([x + w * 0.36, cy - 12, x + w * 0.64, cy + 12],
             start=180, end=360, fill=INK, width=3)


def scene_drones(draw, x, y, w, h):
    """Drone swarm: many small quadcopters over a skyline."""
    draw.rectangle([x, y, x + w, y + h], fill=SKY)
    # skyline
    base = y + h - 18
    for bx, bw, bh in [(0.02, 0.16, 0.30), (0.20, 0.12, 0.45),
                       (0.34, 0.18, 0.28), (0.54, 0.14, 0.50),
                       (0.70, 0.13, 0.34), (0.85, 0.13, 0.42)]:
        draw.rectangle([x + w * bx, base - h * bh, x + w * (bx + bw), base],
                       fill=(70, 80, 95))
    draw.rectangle([x, base, x + w, y + h], fill=(50, 55, 60))
    # drones
    for dx, dy, s in [(0.15, 0.22, 9), (0.32, 0.12, 7), (0.48, 0.26, 10),
                      (0.62, 0.14, 7), (0.78, 0.24, 9), (0.88, 0.10, 6),
                      (0.24, 0.38, 6), (0.58, 0.36, 6), (0.86, 0.38, 5)]:
        cx, cy = x + w * dx, y + h * dy
        draw.ellipse([cx - s, cy - s // 2, cx + s, cy + s // 2],
                     fill=INK)
        draw.line([(cx - s - 4, cy - s // 2), (cx + s + 4, cy - s // 2)],
                  fill=INK, width=2)
        draw.line([(cx - s - 4, cy + s // 2), (cx + s + 4, cy + s // 2)],
                  fill=INK, width=2)
        draw.line([(cx, cy), (cx, cy + 10)], fill=RED, width=2)


def scene_cyclone(draw, x, y, w, h):
    """Spiral cyclone over a coastline."""
    draw.rectangle([x, y, x + w, y + h], fill=(226, 236, 244))
    cx, cy = x + w // 2, y + h // 2 - 6
    for k in range(3):
        pts = []
        for i in range(120):
            t = i / 119.0
            ang = t * math.pi * 4.2 + k * 2.1
            r = 4 + t * (min(w, h) // 2 - 6)
            pts.append((cx + r * math.cos(ang), cy + r * math.sin(ang)))
        draw.line(pts, fill=BLUE if k % 2 == 0 else (90, 140, 190), width=3)
    draw.ellipse([cx - 6, cy - 6, cx + 6, cy + 6], fill=BLUE)
    # coastline + rain
    draw.rectangle([x, y + h - 16, x + w, y + h], fill=(120, 150, 110))
    for rx in (0.15, 0.4, 0.65, 0.85):
        px = x + w * rx
        draw.line([(px, y + 8), (px - 6, y + 26)], fill=(70, 110, 160),
                  width=2)


def scene_shield(draw, x, y, w, h):
    """Shield with a padlock: banks under cyberattack."""
    draw.rectangle([x, y, x + w, y + h], fill=(240, 238, 232))
    cx, cy = x + w // 2, y + h // 2
    sw, sh = w // 3, h // 2 + 6
    pts = [(cx - sw // 2, cy - sh // 2), (cx + sw // 2, cy - sh // 2),
           (cx + sw // 2, cy + 4), (cx, cy + sh // 2),
           (cx - sw // 2, cy + 4)]
    draw.polygon(pts, fill=BLUE, outline=INK)
    # lock
    lx, ly = cx - 13, cy - 2
    draw.rectangle([lx, ly, lx + 26, ly + 22], fill=GOLD, outline=INK)
    draw.arc([lx + 4, ly - 12, lx + 22, ly + 6], start=180, end=360,
             fill=INK, width=3)
    draw.ellipse([cx - 3, cy + 6, cx + 3, cy + 12], fill=INK)
    # warning bolts
    for bx in (0.14, 0.86):
        px, py = x + w * bx, y + 14
        draw.polygon([(px, py), (px - 5, py + 14), (px + 1, py + 14),
                      (px - 2, py + 26), (px + 6, py + 12),
                      (px, py + 12)], fill=RED)


def scene_globe(draw, x, y, w, h):
    """Globe with a leaf: climate talks."""
    draw.rectangle([x, y, x + w, y + h], fill=(232, 240, 232))
    cx, cy = x + w // 2, y + h // 2
    r = min(w, h) // 2 - 8
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(150, 195, 230),
                 outline=BLUE, width=2)
    # land blobs
    draw.ellipse([cx - r + 6, cy - r // 2, cx - 2, cy + 4], fill=GREEN)
    draw.ellipse([cx + 2, cy + 2, cx + r - 6, cy + r // 2], fill=GREEN)
    draw.ellipse([cx - 6, cy - r + 4, cx + 10, cy - r // 3], fill=GREEN)
    # leaf
    lx, ly = cx + r - 14, cy - r + 2
    draw.ellipse([lx - 14, ly - 6, lx + 14, ly + 10], fill=(46, 139, 60))
    draw.line([(lx - 14, ly + 2), (lx + 14, ly + 2)], fill=(30, 90, 40),
              width=2)
    draw.text((x + 8, y + h - 22), "COP31", font=font(SANS_B, 15),
              fill=GREEN)


def scene_hospital(draw, x, y, w, h):
    """Hospital building with a red cross."""
    draw.rectangle([x, y, x + w, y + h], fill=(244, 240, 234))
    bx, by = x + w * 0.18, y + 18
    bw, bh = w * 0.64, h - 34
    draw.rectangle([bx, by, bx + bw, by + bh], fill=(255, 255, 255),
                   outline=INK, width=2)
    # windows
    for r in range(2):
        for c in range(3):
            wx = bx + 12 + c * (bw - 24) // 3
            wy = by + 14 + r * (bh - 28) // 2
            draw.rectangle([wx, wy, wx + 18, wy + 16], fill=SKY)
    # red cross sign
    cx, cy = x + w // 2, y + 12
    draw.rectangle([cx - 6, cy - 14, cx + 6, cy + 14], fill=RED)
    draw.rectangle([cx - 14, cy - 6, cx + 14, cy + 6], fill=RED)


# ---------------------------------------------------------------- page
def build():
    img = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(img)

    # outer frame
    d.rectangle([14, 14, W - 15, H - 15], outline=INK, width=3)

    # ---- masthead
    rule(d, 40, 128, W - 40, width=3)
    rule(d, 40, 134, W - 40, width=1)
    f_mast = font(SERIF_B, 64)
    title = "THE WORLD IN ONE DAY"
    tw = d.textlength(title, font=f_mast)
    d.text(((W - tw) / 2, 34), title, font=f_mast, fill=INK)
    f_sub = font(SANS, 22)
    sub = "21 NOVEMBER 2026  ·  EIGHT STORIES  ·  ONE PAGE"
    sw = d.textlength(sub, font=f_sub)
    d.text(((W - sw) / 2, 102), sub, font=f_sub, fill=GREY)

    # ---- lead panel: Poland missiles
    lx, ly, lw, lh = 40, 152, 900, 400
    panel(d, lx, ly, lw, lh, border=RED, bw=3)
    kicker(d, lx + 18, ly + 12, "Lead story — Europe", color=RED)
    headline(d, lx + 18, ly + 36, "MISSILES FALL ON POLAND",
             44, lw - 36, color=RED_DARK)
    cap = ("Two missiles and a suspected drone come down on Polish soil. "
           "Warsaw calls it a deliberate provocation; NATO calls it a "
           "grave violation of allied airspace.")
    f_cap = font(SANS, 19)
    text_block(d, lx + 18, ly + 96, wrap(d, cap, f_cap, lw - 36),
               f_cap, INK)
    scene_missiles(d, lx + 18, ly + 196, lw - 36, 186)

    # ---- right column: Wall Street + UK-EU
    rx, rw = 960, 600
    # Wall Street
    ry, rh = 152, 196
    panel(d, rx, ry, rw, rh)
    kicker(d, rx + 16, ry + 10, "Markets", color=RED)
    headline(d, rx + 16, ry + 32, "WALL STREET SLUMPS",
             30, rw - 32)
    f_small = font(SANS, 16)
    text_block(d, rx + 16, ry + 74,
               wrap(d, "US stocks fall ~3.7%; the S&P 500 and Dow enter "
                    "correction territory as AI shares sell off.",
                    f_small, rw - 32), f_small, INK)
    scene_chart(d, rx + 16, ry + 118, rw - 32, 62)
    # UK-EU
    ry2, rh2 = 356, 196
    panel(d, rx, ry2, rw, rh2)
    kicker(d, rx + 16, ry2 + 10, "Europe", color=BLUE)
    headline(d, rx + 16, ry2 + 32, "UK AND EU SIGN DEALS",
             30, rw - 32)
    text_block(d, rx + 16, ry2 + 74,
               wrap(d, "Food trade, carbon markets and youth mobility "
                    "agreed at a Brussels summit.",
                    f_small, rw - 32), f_small, INK)
    scene_handshake(d, rx + 16, ry2 + 118, rw - 32, 62)

    # ---- bottom row: five panels
    rule(d, 40, 568, W - 40, width=2)
    bx, by, bw, bh = 40, 584, 296, 372
    gap = 10
    bottom = [
        ("War in Ukraine", RED,
         "RUSSIA'S BIGGEST STRIKE ON UKRAINE",
         "400 drones and 110 missiles in one of the war's largest "
         "attacks. Kryvyi Rih: 2 dead, 42 injured, including 4 children.",
         scene_drones),
        ("Weather", BLUE,
         "CYCLONE AKVAN HITS INDIA",
         "The cyclone crosses the Odisha coast with strong winds and "
         "heavy rain, then weakens inland.",
         scene_cyclone),
        ("Banking", RED,
         "CYBERATTACK HITS BIG BANKS",
         "JPMorgan, Visa and Mastercard report incidents at "
         "third-party vendors. Core payment networks unaffected.",
         scene_shield),
        ("Climate", GREEN,
         "COP31 ENTERS FINAL STAGE",
         "The UN climate summit in Turkey reaches its crucial final "
         "days, with fossil fuels and climate finance at the centre.",
         scene_globe),
        ("Brazil", RED,
         "BOLSONARO HOSPITALISED",
         "Brazil's imprisoned ex-president is taken to hospital with "
         "severe abdominal pain.",
         scene_hospital),
    ]
    for i, (tag, color, head, cap_text, scene) in enumerate(bottom):
        x = bx + i * (bw + gap)
        panel(d, x, by, bw, bh)
        kicker(d, x + 14, by + 10, tag, color=color)
        y = headline(d, x + 14, by + 32, head, 24, bw - 28)
        y += 6
        f_b = font(SANS, 15)
        y = text_block(d, x + 14, y,
                       wrap(d, cap_text, f_b, bw - 28), f_b, INK)
        scene(d, x + 14, by + bh - 148, bw - 28, 132)

    # ---- footer
    f_foot = font(SANS, 15)
    foot = ("Sources: world news wires, 21 November 2026  ·  "
            "Illustrations drawn for this front page  ·  "
            "Made for make.fun — news-image-20261121")
    fw = d.textlength(foot, font=f_foot)
    d.text(((W - fw) / 2, H - 34), foot, font=f_foot, fill=GREY)

    img.save("entry.png", format="PNG")
    return img


if __name__ == "__main__":
    build()
    print("entry.png written: 1600x1000")
