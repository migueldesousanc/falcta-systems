"""
Generates clearly-marked PLACEHOLDER images for the FMM-L concept renders,
in the site's dark tactical/HUD visual style, so the pages don't 404 or
show broken images before the real renders are dropped in.

Replace each file in assets/img/ with the real render using the exact same
filename (both the .jpg and the matching .webp) and these placeholders are
gone with no HTML/CSS changes needed.

Run: python3 generate_fmm_placeholders.py
Requires: Pillow (pip install Pillow)
"""
from PIL import Image, ImageDraw, ImageFont

BG = (7, 9, 10)
GRID = (26, 32, 29)
BORDER = (36, 43, 38)
TEXT_BRIGHT = (223, 231, 226)
TEXT_MAIN = (147, 163, 154)
ACCENT = (255, 153, 0)
ACCENT_SECONDARY = (75, 107, 70)
HUD_GREEN = (57, 255, 20)
DANGER = (255, 59, 59)

FONT_DIR = "fonts/"
SYS_FONT_DIR = "/System/Library/Fonts/Supplemental/"

heading = lambda size: ImageFont.truetype(FONT_DIR + "Archivo-ExtraBold.ttf", size)
heading_bold = lambda size: ImageFont.truetype(FONT_DIR + "Archivo-Bold.ttf", size)
body = lambda size: ImageFont.truetype(FONT_DIR + "Archivo-Regular.ttf", size)
mono = lambda size: ImageFont.truetype(SYS_FONT_DIR + "Courier New.ttf", size)
mono_bold = lambda size: ImageFont.truetype(SYS_FONT_DIR + "Courier New Bold.ttf", size)

IMAGES = [
    {"name": "fmm-hero", "w": 1600, "h": 900, "label": "FMM-L — HERO"},
    {"name": "fmm-views", "w": 1200, "h": 800, "label": "FMM-L — MULTIPLE VIEWS"},
    {"name": "fmm-exploded", "w": 1200, "h": 900, "label": "FMM-L — EXPLODED VIEW"},
    {"name": "fmm-ugv", "w": 1200, "h": 800, "label": "FMM-L — UGV MOUNT"},
    {"name": "fmm-blueprint", "w": 1200, "h": 900, "label": "FMM-L — BLUEPRINT"},
]


def draw_grid(draw, w, h, step=40):
    for x in range(0, w, step):
        draw.line([(x, 0), (x, h)], fill=GRID, width=1)
    for y in range(0, h, step):
        draw.line([(0, y), (w, y)], fill=GRID, width=1)


def draw_corner_brackets(draw, w, h, margin=28, size=34, color=ACCENT_SECONDARY, width=3):
    # top-left
    draw.line([(margin, margin), (margin + size, margin)], fill=color, width=width)
    draw.line([(margin, margin), (margin, margin + size)], fill=color, width=width)
    # top-right
    draw.line([(w - margin, margin), (w - margin - size, margin)], fill=color, width=width)
    draw.line([(w - margin, margin), (w - margin, margin + size)], fill=color, width=width)
    # bottom-left
    draw.line([(margin, h - margin), (margin + size, h - margin)], fill=color, width=width)
    draw.line([(margin, h - margin), (margin, h - margin - size)], fill=color, width=width)
    # bottom-right
    draw.line([(w - margin, h - margin), (w - margin - size, h - margin)], fill=color, width=width)
    draw.line([(w - margin, h - margin), (w - margin, h - margin - size)], fill=color, width=width)


def centered_text(draw, cx, cy, text, font, fill):
    bbox = draw.textbbox((0, 0), text, font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    draw.text((cx - tw / 2, cy - th / 2 - bbox[1]), text, font=font, fill=fill)


def make_placeholder(spec):
    w, h = spec["w"], spec["h"]
    img = Image.new("RGB", (w, h), BG)
    draw = ImageDraw.Draw(img)

    draw_grid(draw, w, h)

    # Diagonal dashed hazard border to make "placeholder" status unmistakable
    draw.rectangle([0, 0, w - 1, h - 1], outline=DANGER, width=2)
    draw_corner_brackets(draw, w, h, color=ACCENT_SECONDARY)

    # Radar-ring motif, faint, centered
    cx, cy = w // 2, h // 2
    for r in (min(w, h) * 0.32, min(w, h) * 0.22, min(w, h) * 0.12):
        bbox = [cx - r, cy - r, cx + r, cy + r]
        draw.ellipse(bbox, outline=BORDER, width=1)

    centered_text(draw, cx, cy - 46, "PLACEHOLDER", heading(46), ACCENT)
    centered_text(draw, cx, cy + 14, spec["label"], heading_bold(28), TEXT_BRIGHT)
    centered_text(draw, cx, cy + 56, "Concept render not yet supplied", body(20), TEXT_MAIN)
    centered_text(
        draw, cx, cy + 92,
        f"Drop in assets/img/{spec['name']}.jpg + .webp to replace",
        mono(16), HUD_GREEN,
    )

    draw.text((34, h - 34), f"// {w}x{h} · falcatasystems.site", font=mono(14), fill=TEXT_MAIN)

    return img


if __name__ == "__main__":
    import os
    out_dir = "../assets/img"
    os.makedirs(out_dir, exist_ok=True)
    for spec in IMAGES:
        img = make_placeholder(spec)
        jpg_path = os.path.join(out_dir, f"{spec['name']}.jpg")
        webp_path = os.path.join(out_dir, f"{spec['name']}.webp")
        img.save(jpg_path, "JPEG", quality=85)
        img.save(webp_path, "WEBP", quality=85)
        print(f"Wrote {jpg_path} and {webp_path} ({spec['w']}x{spec['h']})")
