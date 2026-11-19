#!/usr/bin/env python3
"""Draw one image summing up the world's news of Thursday 19 November 2026.

Pure Python standard library. Writes /output/entry.png (or the directory
named by MAKEFUN_OUTPUT_DIR). The drawing is fully deterministic: the same
bytes come out of every run.

Design: a dark "world in one day" board. A gold header names the day, six
story cards in a 2x3 grid carry the day's biggest stories from different
regions and fields, a gold ticker adds three more headlines, and a footer
line closes the day. Every glyph is drawn from a small 5x7 bitmap font
defined below, so the program needs no font files and no network.
"""

import math
import os
import struct
import zlib

W, H = 1024, 1024

BG = (13, 27, 46)        # deep navy
CARD = (22, 40, 63)      # card slate
BORDER = (42, 66, 88)    # card border
GOLD = (217, 164, 65)    # gold accent
WHITE = (242, 245, 248)  # headline white
MUTED = (168, 188, 208)  # summary grey-blue
FOOT = (143, 168, 191)   # footer grey-blue
INK = (13, 27, 46)       # dark text on the gold ticker

# ---------------------------------------------------------------- PNG output

def _chunk(kind, data):
    out = struct.pack(">I", len(data)) + kind + data
    out += struct.pack(">I", zlib.crc32(kind + data) & 0xFFFFFFFF)
    return out


def write_png(path, width, height, rgb):
    """Write RGB bytes (row-major, 3 bytes per pixel) as a PNG file."""
    raw = bytearray()
    stride = width * 3
    for y in range(height):
        raw.append(0)  # filter: none
        raw += rgb[y * stride:(y + 1) * stride]
    png = b"\x89PNG\r\n\x1a\n"
    png += _chunk(b"IHDR", struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0))
    png += _chunk(b"IDAT", zlib.compress(bytes(raw), 9))
    png += _chunk(b"IEND", b"")
    with open(path, "wb") as fh:
        fh.write(png)


# ---------------------------------------------------------------- 5x7 bitmap font

# Each glyph is 7 rows of 5 pixels, "#" on and "." off.
FONT = {
    "A": (".###.", "#...#", "#...#", "#####", "#...#", "#...#", "#...#"),
    "B": ("####.", "#...#", "#...#", "####.", "#...#", "#...#", "####."),
    "C": (".####", "#....", "#....", "#....", "#....", "#....", ".####"),
    "D": ("####.", "#...#", "#...#", "#...#", "#...#", "#...#", "####."),
    "E": ("#####", "#....", "#....", "####.", "#....", "#....", "#####"),
    "F": ("#####", "#....", "#....", "####.", "#....", "#....", "#...."),
    "G": (".####", "#....", "#....", "#.###", "#...#", "#...#", ".###."),
    "H": ("#...#", "#...#", "#...#", "#####", "#...#", "#...#", "#...#"),
    "I": ("#####", "..#..", "..#..", "..#..", "..#..", "..#..", "#####"),
    "J": ("..###", "...#.", "...#.", "...#.", "...#.", "#..#.", ".##.."),
    "K": ("#...#", "#..#.", "#.#..", "##...", "#.#..", "#..#.", "#...#"),
    "L": ("#....", "#....", "#....", "#....", "#....", "#....", "#####"),
    "M": ("#...#", "##.##", "#.#.#", "#.#.#", "#...#", "#...#", "#...#"),
    "N": ("#...#", "##..#", "##..#", "#.#.#", "#..##", "#..##", "#...#"),
    "O": (".###.", "#...#", "#...#", "#...#", "#...#", "#...#", ".###."),
    "P": ("####.", "#...#", "#...#", "####.", "#....", "#....", "#...."),
    "Q": (".###.", "#...#", "#...#", "#...#", "#.#.#", "#..#.", ".##.#"),
    "R": ("####.", "#...#", "#...#", "####.", "#.#..", "#..#.", "#...#"),
    "S": (".####", "#....", "#....", ".###.", "....#", "....#", "####."),
    "T": ("#####", "..#..", "..#..", "..#..", "..#..", "..#..", "..#.."),
    "U": ("#...#", "#...#", "#...#", "#...#", "#...#", "#...#", ".###."),
    "V": ("#...#", "#...#", "#...#", "#...#", "#...#", ".#.#.", "..#.."),
    "W": ("#...#", "#...#", "#...#", "#.#.#", "#.#.#", "##.##", "#...#"),
    "X": ("#...#", "#...#", ".#.#.", "..#..", ".#.#.", "#...#", "#...#"),
    "Y": ("#...#", "#...#", ".#.#.", "..#..", "..#..", "..#..", "..#.."),
    "Z": ("#####", "....#", "...#.", "..#..", ".#...", "#....", "#####"),
    "a": (".....", ".####", "....#", ".####", "#...#", ".####", "....."),
    "b": ("#....", "#....", "####.", "#...#", "#...#", "#...#", "####."),
    "c": (".....", ".....", ".####", "#....", "#....", "#....", ".####"),
    "d": ("....#", "....#", ".####", "#...#", "#...#", "#...#", ".####"),
    "e": (".....", ".....", ".###.", "#...#", "#####", "#....", ".###."),
    "f": ("..##.", ".#...", ".#...", "####.", ".#...", ".#...", ".#..."),
    "g": (".....", ".####", "#...#", "#...#", ".####", "....#", ".###."),
    "h": ("#....", "#....", "####.", "#...#", "#...#", "#...#", "#...#"),
    "i": (".....", "..#..", ".....", ".##..", "..#..", "..#..", ".###."),
    "j": (".....", "..#..", ".....", "..#..", "..#..", "#.#..", ".#..."),
    "k": ("#....", "#....", "#..#.", "#.#..", "##...", "#.#..", "#..#."),
    "l": (".##..", "..#..", "..#..", "..#..", "..#..", "..#..", ".###."),
    "m": (".....", ".....", "##.#.", "#.#.#", "#.#.#", "#.#.#", "#.#.#"),
    "n": (".....", ".....", "####.", "#...#", "#...#", "#...#", "#...#"),
    "o": (".....", ".....", ".###.", "#...#", "#...#", "#...#", ".###."),
    "p": (".....", ".....", "####.", "#...#", "####.", "#....", "#...."),
    "q": (".....", ".....", ".####", "#...#", ".####", "....#", "....#"),
    "r": (".....", ".....", "#.##.", "##..#", "#....", "#....", "#...."),
    "s": (".....", ".....", ".####", "#....", ".###.", "....#", "####."),
    "t": (".#...", ".#...", "####.", ".#...", ".#...", ".#...", "..##."),
    "u": (".....", ".....", "#...#", "#...#", "#...#", "#...#", ".###."),
    "v": (".....", ".....", "#...#", "#...#", "#...#", ".#.#.", "..#.."),
    "w": (".....", ".....", "#...#", "#.#.#", "#.#.#", "#.#.#", ".#.#."),
    "x": (".....", ".....", "#...#", ".#.#.", "..#..", ".#.#.", "#...#"),
    "y": (".....", ".....", "#...#", "#...#", ".#.#.", "..#..", "..#.."),
    "z": (".....", ".....", "#####", "...#.", "..#..", ".#...", "#####"),
    "0": (".###.", "#...#", "#..##", "#.#.#", "##..#", "#...#", ".###."),
    "1": ("..#..", ".##..", "..#..", "..#..", "..#..", "..#..", ".###."),
    "2": (".###.", "#...#", "....#", "...#.", "..#..", ".#...", "#####"),
    "3": ("####.", "....#", "....#", ".###.", "....#", "....#", "####."),
    "4": ("...#.", "..##.", ".#.#.", "#..#.", "#####", "...#.", "...#."),
    "5": ("#####", "#....", "####.", "....#", "....#", "#...#", ".###."),
    "6": (".###.", "#....", "#....", "####.", "#...#", "#...#", ".###."),
    "7": ("#####", "....#", "...#.", "..#..", "..#..", "..#..", "..#.."),
    "8": (".###.", "#...#", "#...#", ".###.", "#...#", "#...#", ".###."),
    "9": (".###.", "#...#", "#...#", ".####", "....#", "....#", ".###."),
    " ": (".....", ".....", ".....", ".....", ".....", ".....", "....."),
    ".": (".....", ".....", ".....", ".....", ".....", ".##..", ".##.."),
    ",": (".....", ".....", ".....", ".....", ".##..", ".##..", ".#..."),
    "-": (".....", ".....", ".....", ".###.", ".....", ".....", "....."),
    "$": ("..#..", ".####", "#.#..", ".###.", "..#.#", "####.", "..#.."),
    "%": ("##..#", "##.#.", "...#.", "..#..", ".#...", "#.##.", "#..##"),
    "!": ("..#..", "..#..", "..#..", "..#..", "..#..", ".....", "..#.."),
    "?": (".###.", "#...#", "....#", "...#.", "..#..", ".....", "..#.."),
    "'": ("..#..", "..#..", ".#...", ".....", ".....", ".....", "....."),
    ":": (".....", ".##..", ".##..", ".....", ".##..", ".##..", "....."),
    ";": (".....", ".##..", ".##..", ".....", ".##..", ".##..", ".#..."),
    "(": ("...##", "..#..", ".#...", ".#...", ".#...", "..#..", "...##"),
    ")": ("##...", "..#..", "...#.", "...#.", "...#.", "..#..", "##..."),
    "/": ("....#", "....#", "...#.", "..#..", ".#...", "#....", "#...."),
    "&": (".###.", "#...#", "#...#", ".#.#.", "#..#.", "#.#..", ".##.#"),
    "+": (".....", "..#..", "..#..", "#####", "..#..", "..#..", "....."),
    "=": (".....", ".....", "#####", ".....", "#####", ".....", "....."),
    "\u2022": (".....", ".....", ".###.", ".###.", ".###.", ".....", "....."),
}


# ---------------------------------------------------------------- canvas

class Canvas:
    def __init__(self, width, height, color):
        self.w = width
        self.h = height
        self.px = bytearray(color * (width * height))

    def set(self, x, y, color):
        if 0 <= x < self.w and 0 <= y < self.h:
            i = (y * self.w + x) * 3
            self.px[i:i + 3] = bytes(color)

    def fill_rect(self, x, y, w, h, color):
        x0, y0 = max(0, x), max(0, y)
        x1, y1 = min(self.w, x + w), min(self.h, y + h)
        row = bytes(color) * (x1 - x0)
        for yy in range(y0, y1):
            i = (yy * self.w + x0) * 3
            self.px[i:i + len(row)] = row

    def rect_outline(self, x, y, w, h, color):
        self.fill_rect(x, y, w, 1, color)
        self.fill_rect(x, y + h - 1, w, 1, color)
        self.fill_rect(x, y, 1, h, color)
        self.fill_rect(x + w - 1, y, 1, h, color)

    def line(self, x0, y0, x1, y1, color):
        dx, dy = abs(x1 - x0), abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx - dy
        while True:
            self.set(x0, y0, color)
            if x0 == x1 and y0 == y1:
                return
            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x0 += sx
            if e2 < dx:
                err += dx
                y0 += sy

    def fill_circle(self, cx, cy, r, color):
        for dy in range(-r, r + 1):
            dx = int(math.sqrt(max(0, r * r - dy * dy)))
            self.fill_rect(cx - dx, cy + dy, 2 * dx + 1, 1, color)

    def circle_outline(self, cx, cy, r, color):
        for deg in range(0, 360, 2):
            a = math.radians(deg)
            self.set(cx + int(r * math.cos(a)), cy + int(r * math.sin(a)), color)

    def fill_ellipse(self, cx, cy, rx, ry, color):
        for dy in range(-ry, ry + 1):
            t = 1.0 - (dy * dy) / float(ry * ry)
            dx = int(rx * math.sqrt(max(0.0, t)))
            self.fill_rect(cx - dx, cy + dy, 2 * dx + 1, 1, color)

    def ellipse_outline(self, cx, cy, rx, ry, color):
        for deg in range(0, 360, 2):
            a = math.radians(deg)
            self.set(cx + int(rx * math.cos(a)), cy + int(ry * math.sin(a)), color)


# ---------------------------------------------------------------- text

def text_width(text, scale):
    return len(text) * 6 * scale


def draw_text(cv, x, y, text, scale, color):
    """Draw text with the 5x7 font; unknown glyphs fall back to '?''."""
    cx = x
    for ch in text:
        glyph = FONT.get(ch, FONT["?"])
        for row in range(7):
            bits = glyph[row]
            for col in range(5):
                if bits[col] == "#":
                    cv.fill_rect(cx + col * scale, y + row * scale,
                                 scale, scale, color)
        cx += 6 * scale
    return cx


def wrap_text(text, max_chars):
    """Greedy word wrap into lines of at most max_chars characters."""
    lines, cur = [], ""
    for word in text.split(" "):
        if cur and len(cur) + 1 + len(word) > max_chars:
            lines.append(cur)
            cur = word
        else:
            cur = word if not cur else cur + " " + word
    if cur:
        lines.append(cur)
    return lines


# ---------------------------------------------------------------- icons

def draw_icon(cv, kind, cx, cy, color):
    """Small geometric icon for a story card, centred on (cx, cy)."""
    if kind == "network":  # three leaders, linked
        pts = [(cx - 20, cy + 8), (cx, cy - 12), (cx + 20, cy + 8)]
        for i in range(3):
            for j in range(i + 1, 3):
                cv.line(pts[i][0], pts[i][1], pts[j][0], pts[j][1], color)
        for px, py in pts:
            cv.fill_circle(px, py, 7, color)
    elif kind == "burst":  # strikes, blasts outward
        for k in range(8):
            a = math.radians(k * 45)
            cv.line(cx, cy, cx + int(24 * math.cos(a)),
                    cy + int(24 * math.sin(a)), color)
        cv.fill_circle(cx, cy, 6, color)
    elif kind == "sprout":  # climate: a shoot with two leaves
        cv.line(cx, cy + 20, cx, cy - 4, color)
        cv.fill_ellipse(cx - 11, cy - 6, 11, 6, color)
        cv.fill_ellipse(cx + 11, cy - 6, 11, 6, color)
        cv.fill_circle(cx, cy - 12, 4, color)
    elif kind == "chip":  # tech: a processor
        cv.rect_outline(cx - 15, cy - 15, 30, 30, color)
        cv.rect_outline(cx - 6, cy - 6, 12, 12, color)
        for off in (-9, 0, 9):
            cv.line(cx + off, cy - 15, cx + off, cy - 21, color)
            cv.line(cx + off, cy + 15, cx + off, cy + 21, color)
            cv.line(cx - 15, cy + off, cx - 21, cy + off, color)
            cv.line(cx + 15, cy + off, cx + 21, cy + off, color)
    elif kind == "planet":  # space: a ringed world
        cv.fill_circle(cx, cy, 12, color)
        cv.ellipse_outline(cx, cy, 24, 8, color)
    elif kind == "pad":  # culture: a game controller
        cv.rect_outline(cx - 21, cy - 13, 42, 26, color)
        cv.line(cx - 13, cy - 4, cx - 13, cy + 4, color)
        cv.line(cx - 17, cy, cx - 9, cy, color)
        cv.fill_circle(cx + 10, cy - 3, 3, color)
        cv.fill_circle(cx + 15, cy + 3, 3, color)


# ---------------------------------------------------------------- the day's stories

# Six stories, one per region/field, each reported on 19 November 2026:
# 1. Diplomacy - Trump, Xi and Putin hold trilateral talks in Shenzhen
#    at the APEC summit (New York Times, 19 Nov).
# 2. Middle East - the US-Iran exchange widens: US strikes on Qeshm
#    Island, Iran hits US bases in Bahrain and Kuwait (Khaleej Times
#    front page and wire reports, 19 Nov).
# 3. Climate - COP30 day 10 in Belem puts farming, land and women at
#    the centre; the RAIZ land-restoration initiative launches
#    (COP30 official morning brief, 19 Nov).
# 4. Tech - Anthropic raises $81.3bn in the biggest IPO of all time
#    (Al Jazeera, 19 Nov).
# 5. Space - Voyager 1 reaches one light-day from Earth, 50 years
#    after launch (Al Jazeera, 19 Nov).
# 6. Culture - Grand Theft Auto VI begins its global rollout, gamers
#    return to Vice City after a 13-year wait (19 Nov).
CARDS = [
    {
        "tag": "SUMMIT",
        "accent": (232, 179, 75),
        "icon": "network",
        "headline": ["TRUMP, XI AND PUTIN", "MEET IN SHENZHEN"],
        "summary": "The three leaders hold trilateral talks at the "
                   "APEC summit in Shenzhen.",
        "stat": "APEC SUMMIT IN SHENZHEN, CHINA",
    },
    {
        "tag": "CONFLICT",
        "accent": (228, 87, 46),
        "icon": "burst",
        "headline": ["US AND IRAN TRADE", "BLOWS ACROSS THE GULF"],
        "summary": "Washington hits a missile site on Qeshm Island; "
                   "Tehran strikes US bases in Bahrain and Kuwait.",
        "stat": "QESHM ISLAND \u2022 BAHRAIN \u2022 KUWAIT",
    },
    {
        "tag": "CLIMATE",
        "accent": (76, 175, 125),
        "icon": "sprout",
        "headline": ["COP30 TURNS TO FOOD", "AND FARMS"],
        "summary": "In Belem, day 10 puts farming, land and women at "
                   "the centre of the climate talks.",
        "stat": "BELEM, BRAZIL \u2022 DAY 10 OF 12",
    },
    {
        "tag": "TECH",
        "accent": (108, 140, 255),
        "icon": "chip",
        "headline": ["ANTHROPIC RAISES", "$81BN IN BIGGEST IPO EVER"],
        "summary": "The Claude maker's record listing tops every "
                   "IPO before it.",
        "stat": "A $1.4 TRILLION MARKET DEBUT",
    },
    {
        "tag": "SPACE",
        "accent": (179, 136, 255),
        "icon": "planet",
        "headline": ["VOYAGER 1 REACHES", "ONE LIGHT-DAY"],
        "summary": "Fifty years after launch, the probe is the "
                   "farthest human object ever.",
        "stat": "ONE LIGHT-DAY: 25.9 BILLION KM",
    },
    {
        "tag": "CULTURE",
        "accent": (255, 107, 157),
        "icon": "pad",
        "headline": ["GTA VI ROLLS OUT", "WORLDWIDE"],
        "summary": "After a 13-year wait, gamers return to Vice City "
                   "as the game launches globally.",
        "stat": "VICE CITY \u2022 13 YEARS AFTER GTA V",
    },
]

TICKER_TOP = "ALSO TODAY: VAN GOGH SELLS FOR A RECORD $190.4M"
TICKER_BOTTOM = ("CYCLONE AKVAN NEARS INDIA'S COAST \u2022 MYANMAR FACES "
                 "UN GENOCIDE VERDICT")
FOOTER = "SIX STORIES, ONE DAY - THE WORLD ON 19 NOVEMBER 2026"


# ---------------------------------------------------------------- drawing

def draw_card(cv, x, y, card):
    w, h = 480, 240
    accent = card["accent"]
    cv.fill_rect(x, y, w, h, CARD)
    cv.rect_outline(x, y, w, h, BORDER)
    cv.fill_rect(x, y, w, 6, accent)
    draw_text(cv, x + 20, y + 20, card["tag"], 2, accent)
    draw_icon(cv, card["icon"], x + 428, y + 48, accent)
    hy = y + 52
    for line in card["headline"]:
        draw_text(cv, x + 20, hy, line, 3, WHITE)
        hy += 29
    sy = y + 122
    for line in wrap_text(card["summary"], 36):
        draw_text(cv, x + 20, sy, line, 2, MUTED)
        sy += 19
    cv.fill_rect(x + 20, y + 196, w - 40, 2, BORDER)
    draw_text(cv, x + 20, y + 206, card["stat"], 2, accent)


def draw_globe(cv, cx, cy, r, color):
    cv.circle_outline(cx, cy, r, color)
    cv.ellipse_outline(cx, cy, 18, r, color)
    cv.ellipse_outline(cx, cy, 34, r, color)
    cv.line(cx - r, cy, cx + r, cy, color)
    half = int(math.sqrt(max(0, r * r - 23 * 23)))
    cv.line(cx - half, cy - 23, cx + half, cy - 23, color)
    cv.line(cx - half, cy + 23, cx + half, cy + 23, color)


def draw_image():
    cv = Canvas(W, H, BG)
    # Header: title, date, globe, gold rule.
    draw_text(cv, 40, 26, "THE WORLD IN ONE DAY", 6, WHITE)
    draw_text(cv, 42, 84, "THURSDAY, 19 NOVEMBER 2026", 3, GOLD)
    draw_globe(cv, 918, 76, 46, GOLD)
    cv.fill_rect(40, 140, 944, 4, GOLD)
    # Six story cards, 2 columns by 3 rows.
    for i, card in enumerate(CARDS):
        x = 24 + (i % 2) * 496
        y = 166 + (i // 2) * 256
        draw_card(cv, x, y, card)
    # Gold ticker with three more headlines of the day.
    cv.fill_rect(24, 934, 976, 56, GOLD)
    draw_text(cv, 40, 942, TICKER_TOP, 2, INK)
    draw_text(cv, 40, 964, TICKER_BOTTOM, 2, INK)
    # Footer line.
    fx = (W - text_width(FOOTER, 2)) // 2
    draw_text(cv, fx, 1002, FOOTER, 2, FOOT)
    return cv


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    cv = draw_image()
    write_png(os.path.join(out_dir, "entry.png"), W, H, bytes(cv.px))


if __name__ == "__main__":
    main()
