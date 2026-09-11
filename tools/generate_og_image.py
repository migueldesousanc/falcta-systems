"""
Generates the social-preview image (og:image) for Falcta Systems, matching
the site's dark tactical/HUD visual theme (dark background, faint grid,
radar-ring motif, orange/green HUD accents). Produces both the English and
Portuguese variants.

Run: python3 generate_og_image.py
Requires: Pillow (pip install Pillow)
"""
from PIL import Image, ImageDraw, ImageFont

W, H = 1200, 630

BG = (7, 9, 10)
GRID = (30, 36, 32)
BORDER = (36, 43, 38)
TEXT_BRIGHT = (223, 231, 226)
TEXT_MAIN = (147, 163, 154)
ACCENT = (255, 153, 0)
ACCENT_SECONDARY = (75, 107, 70)
HUD_GREEN = (57, 255, 20)

FONT_DIR = "/System/Library/Fonts/Supplemental/"
mono_bold = lambda size: ImageFont.truetype(FONT_DIR + "Courier New Bold.ttf", size)
mono = lambda size: ImageFont.truetype(FONT_DIR + "Courier New.ttf", size)

VARIANTS = [
    {
        "out": "../og-image.png",
        "eyebrow": "// UAS & GEOSPATIAL INTELLIGENCE",
        "headline": ["BUILT FOR THE FIELD,", "NOT THE BROCHURE."],
    },
    {
        "out": "../pt/og-image.png",
        "eyebrow": "// UAS E INTELIGÊNCIA GEOESPACIAL",
        "headline": ["FEITO PARA O TERRENO,", "NÃO PARA O FOLHETO."],
    },
]


def render(out, eyebrow, headline):
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)

    # Faint background grid, matching the site's CSS grid pattern
    step = 46
    for x in range(0, W, step):
        draw.line([(x, 0), (x, H)], fill=GRID, width=1)
    for y in range(0, H, step):
        draw.line([(0, y), (W, y)], fill=GRID, width=1)

    # Radar-ring motif on the right, echoing the homepage hero visual
    cx, cy = 930, 315
    for r in (210, 158, 105, 53):
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=BORDER, width=1)
    draw.line([(cx, cy - 240), (cx, cy + 240)], fill=BORDER, width=1)
    draw.line([(cx - 240, cy), (cx + 240, cy)], fill=BORDER, width=1)
    draw.ellipse([cx - 210, cy - 210, cx + 210, cy + 210], outline=ACCENT_SECONDARY, width=2)

    # Blip
    br = 6
    bx, by = cx + 84, cy - 90
    draw.ellipse([bx - br, by - br, bx + br, by + br], fill=HUD_GREEN)

    # Drone glyph at center
    tri = [(cx, cy - 22), (cx + 16, cy + 16), (cx, cy + 6), (cx - 16, cy + 16)]
    draw.polygon(tri, fill=TEXT_BRIGHT, outline=ACCENT)

    # Wordmark: "[ FALCTA SYSTEMS ]"
    wm_font = mono_bold(46)
    x = 90
    y = 175
    draw.text((x, y), "[ ", font=wm_font, fill=ACCENT)
    bx1 = draw.textlength("[ ", font=wm_font)
    draw.text((x + bx1, y), "FALCTA SYSTEMS", font=wm_font, fill=TEXT_BRIGHT)
    bx2 = draw.textlength("FALCTA SYSTEMS", font=wm_font)
    draw.text((x + bx1 + bx2, y), " ]", font=wm_font, fill=ACCENT)

    # Eyebrow
    draw.text((x, y + 90), eyebrow, font=mono_bold(22), fill=ACCENT)

    # Headline
    headline_font = mono_bold(38)
    draw.text((x, y + 140), headline[0], font=headline_font, fill=TEXT_BRIGHT)
    draw.text((x, y + 190), headline[1], font=headline_font, fill=TEXT_BRIGHT)

    # Footer accent line + domain
    draw.line([(x, H - 70), (700, H - 70)], fill=ACCENT_SECONDARY, width=2)
    draw.text((x, H - 55), "falctasystems.com", font=mono(20), fill=TEXT_MAIN)

    img.save(out, optimize=True)
    print(f"wrote {out}")


for v in VARIANTS:
    render(v["out"], v["eyebrow"], v["headline"])
