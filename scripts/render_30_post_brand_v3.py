#!/usr/bin/env python3
"""
Render V3 branded 30-post assets with a photo-first design system.

Inputs:
  /workspace/ad-drafts/30-posts/raw/post_XX_raw.png
  /workspace/ad-drafts/30-posts/prompt_pack_nb2.json
  /workspace/brand-assets/nate-profile.png

Outputs:
  /workspace/ad-drafts/30-posts/branded-v3/post_XX_branded_v3.png
  /workspace/ad-drafts/30-posts/branded-v3/30posts_branded_v3_contact_sheet.png
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Dict, List, Tuple

from PIL import Image, ImageDraw, ImageFont, ImageOps


ROOT = Path("/workspace")
RAW_DIR = ROOT / "ad-drafts" / "30-posts" / "raw"
PROMPT_PACK = ROOT / "ad-drafts" / "30-posts" / "prompt_pack_nb2.json"
OUT_DIR = ROOT / "ad-drafts" / "30-posts" / "branded-v3"
CONTACT_SHEET_PATH = OUT_DIR / "30posts_branded_v3_contact_sheet.png"
NATE_PHOTO = ROOT / "brand-assets" / "nate-profile.png"

SIZE = 1080
NAVY = (18, 32, 64, 255)
BLUE = (30, 80, 160, 255)
LIGHT_BLUE = (100, 160, 220, 255)
WHITE = (255, 255, 255, 255)
GOLD = (212, 175, 55, 255)
SHADOW = (0, 0, 0, 160)

PHONE = "(414) 312-5213"
BRAND_LINE = "Window Depot USA of Milwaukee"
TAGLINE = "National Strength. Local Service."

SERVICE_COPY: Dict[str, List[Tuple[str, str, str]]] = {
    "windows": [
        ("Triple-Pane Comfort", "Built for real Wisconsin winters and summers.", "Book Free Estimate"),
        ("Lower Bills, Better Comfort", "Energy-smart windows without sales pressure.", "See Window Options"),
        ("No Drafts. No Guesswork.", "Nate walks you through the right fit for your home.", "Talk With Nate"),
    ],
    "doors": [
        ("Entry Doors That Perform", "Security, curb appeal, and insulation in one upgrade.", "See Door Styles"),
        ("Built for Daily Use", "ProVia entry and patio doors made for Midwest weather.", "Book Door Estimate"),
        ("Welcome Home Better", "Upgrade first impressions without high-pressure sales.", "Plan Door Upgrade"),
    ],
    "siding": [
        ("Siding That Lasts", "Durable exterior protection through freeze-thaw cycles.", "Explore Siding"),
        ("Refresh Your Exterior", "Modern colors and profiles with long-term value.", "Get Siding Quote"),
        ("Curb Appeal + Protection", "A cleaner look and stronger weather defense.", "Book Exterior Review"),
    ],
    "roofing": [
        ("Roofing Done Right", "Clear recommendations and quality installation.", "Request Roof Review"),
        ("Storm-Ready Protection", "Durable roof systems for Wisconsin conditions.", "See Roofing Options"),
        ("Long-Term Roof Value", "Asphalt or metal options built for durability.", "Book Roof Estimate"),
    ],
    "bathroom": [
        ("Safer, Cleaner Showers", "Beautiful bath upgrades designed for daily comfort.", "Book Bath Consult"),
        ("One-Day Bath Options", "Fast transformation with practical, modern finishes.", "See Bath Upgrades"),
        ("Accessible by Design", "Low-threshold comfort with a polished look.", "Plan Bathroom Update"),
    ],
    "general": [
        ("Local Team. Real Support.", "Work directly with Nate from estimate to install.", "Start With Nate"),
        ("Upgrade With Confidence", "Free in-home estimate plus a clear one-year price lock.", "Book Free Estimate"),
        ("Milwaukee Home Experts", "Trusted by homeowners across SE Wisconsin.", "Call/Text Nate"),
    ],
}


def load_font(size: int, bold: bool = True) -> ImageFont.FreeTypeFont:
    candidates: List[Tuple[str, int]] = [
        ("/usr/share/fonts/truetype/macos/Helvetica.ttc", 1 if bold else 0),
        (
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
            if bold
            else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
            0,
        ),
    ]
    for path, idx in candidates:
        try:
            return ImageFont.truetype(path, size=size, index=idx)
        except Exception:
            continue
    return ImageFont.load_default()


def parse_post_number(value: object) -> int | None:
    if isinstance(value, int) and 1 <= value <= 30:
        return value
    if isinstance(value, str):
        m = re.search(r"(\d+)", value)
        if m:
            n = int(m.group(1))
            if 1 <= n <= 30:
                return n
    return None


def fit_cover(img: Image.Image, w: int, h: int) -> Image.Image:
    img = img.convert("RGBA")
    scale = max(w / img.width, h / img.height)
    nw = int(img.width * scale)
    nh = int(img.height * scale)
    resized = img.resize((nw, nh), Image.LANCZOS)
    x0 = (nw - w) // 2
    y0 = (nh - h) // 2
    return resized.crop((x0, y0, x0 + w, y0 + h))


def draw_vertical_gradient(canvas: Image.Image, top_alpha: int, bottom_alpha: int, start_y: int, end_y: int) -> None:
    overlay = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    h = max(1, end_y - start_y)
    for i in range(h):
        t = i / max(1, h - 1)
        a = int(top_alpha + (bottom_alpha - top_alpha) * t)
        y = start_y + i
        draw.line([(0, y), (SIZE, y)], fill=(NAVY[0], NAVY[1], NAVY[2], a))
    canvas.alpha_composite(overlay)


def text_width(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.ImageFont) -> int:
    box = draw.textbbox((0, 0), text, font=font)
    return box[2] - box[0]


def wrap_text(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.ImageFont, max_width: int, max_lines: int) -> List[str]:
    words = text.split()
    lines: List[str] = []
    cur: List[str] = []
    for w in words:
        candidate = " ".join(cur + [w])
        if cur and text_width(draw, candidate, font) > max_width:
            lines.append(" ".join(cur))
            cur = [w]
            if len(lines) >= max_lines:
                break
        else:
            cur.append(w)
    if cur and len(lines) < max_lines:
        lines.append(" ".join(cur))
    return lines


def infer_service(theme: str) -> str:
    t = theme.lower()
    if "window" in t:
        return "windows"
    if "door" in t:
        return "doors"
    if "siding" in t or "cladding" in t:
        return "siding"
    if "roof" in t:
        return "roofing"
    if "bath" in t:
        return "bathroom"
    return "general"


def build_nate_badge(size: int = 128) -> Image.Image:
    if not NATE_PHOTO.exists():
        return Image.new("RGBA", (size, size), (0, 0, 0, 0))
    src = Image.open(NATE_PHOTO).convert("RGB")
    head = ImageOps.fit(src, (size, size), method=Image.LANCZOS)
    mask = Image.new("L", (size, size), 0)
    mdraw = ImageDraw.Draw(mask)
    mdraw.ellipse((0, 0, size - 1, size - 1), fill=255)
    out = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    out.paste(head, (0, 0), mask)
    ring = ImageDraw.Draw(out)
    ring.ellipse((2, 2, size - 3, size - 3), outline=WHITE, width=4)
    return out


def pick_copy(service: str, post_num: int) -> Tuple[str, str, str]:
    variants = SERVICE_COPY.get(service, SERVICE_COPY["general"])
    return variants[(post_num - 1) % len(variants)]


def render_post(post_num: int, theme: str, nate_badge: Image.Image) -> Path:
    raw_path = RAW_DIR / f"post_{post_num:02d}_raw.png"
    if not raw_path.exists():
        raise FileNotFoundError(str(raw_path))

    bg = fit_cover(Image.open(raw_path), SIZE, SIZE)
    canvas = bg.copy()

    # Photo-first: subtle gradients only for readability.
    draw_vertical_gradient(canvas, top_alpha=175, bottom_alpha=0, start_y=0, end_y=430)
    draw_vertical_gradient(canvas, top_alpha=0, bottom_alpha=185, start_y=620, end_y=1080)
    draw = ImageDraw.Draw(canvas)

    service = infer_service(theme)
    headline, subline, cta = pick_copy(service, post_num)

    # Brand chip
    chip_x, chip_y, chip_w, chip_h = 36, 30, 540, 56
    draw.rounded_rectangle((chip_x, chip_y, chip_x + chip_w, chip_y + chip_h), radius=16, fill=(18, 32, 64, 210))
    draw.text((chip_x + 18, chip_y + 14), BRAND_LINE, font=load_font(30, bold=True), fill=WHITE)

    # Headline and subline
    head_font = load_font(86, bold=True)
    lines = wrap_text(draw, headline.upper(), head_font, 900, 2)
    while lines and max(text_width(draw, ln, head_font) for ln in lines) > 920 and head_font.size > 48:
        head_font = load_font(head_font.size - 2, bold=True)
        lines = wrap_text(draw, headline.upper(), head_font, 900, 2)

    y = 114
    for ln in lines:
        draw.text((42, y), ln, font=head_font, fill=WHITE, stroke_width=2, stroke_fill=SHADOW)
        y += head_font.size + 4

    sub_font = load_font(38, bold=True)
    sub_lines = wrap_text(draw, subline, sub_font, 850, 2)
    while sub_lines and max(text_width(draw, ln, sub_font) for ln in sub_lines) > 850 and sub_font.size > 26:
        sub_font = load_font(sub_font.size - 2, bold=True)
        sub_lines = wrap_text(draw, subline, sub_font, 850, 2)
    for ln in sub_lines:
        draw.text((44, y + 8), ln, font=sub_font, fill=GOLD, stroke_width=1, stroke_fill=SHADOW)
        y += sub_font.size + 2

    # Nate badge + trust copy
    canvas.paste(nate_badge, (38, 838), nate_badge)
    draw.text((184, 866), "Talk directly with Nate", font=load_font(34, bold=True), fill=WHITE, stroke_width=2, stroke_fill=SHADOW)
    draw.text((184, 908), PHONE, font=load_font(42, bold=True), fill=(130, 195, 255, 255), stroke_width=1, stroke_fill=SHADOW)
    draw.text((184, 956), TAGLINE, font=load_font(24, bold=False), fill=(220, 230, 255, 255))

    # Proof chips
    chips = ["4.9★ Google", "1,000+ Reviews", "Price Locked 1 Year"]
    cx = 42
    cy = 1004
    chip_font = load_font(22, bold=True)
    for label in chips:
        tw = text_width(draw, label, chip_font)
        cw = tw + 26
        draw.rounded_rectangle((cx, cy, cx + cw, cy + 38), radius=12, fill=(18, 32, 64, 215), outline=(76, 130, 198, 220), width=2)
        draw.text((cx + 13, cy + 9), label, font=chip_font, fill=WHITE)
        cx += cw + 10

    # CTA button
    btn_w = 320
    btn_h = 72
    bx = SIZE - btn_w - 36
    by = 968
    draw.rounded_rectangle((bx, by, bx + btn_w, by + btn_h), radius=20, fill=BLUE, outline=LIGHT_BLUE, width=2)
    cta_font = load_font(30, bold=True)
    cta_lines = wrap_text(draw, cta, cta_font, btn_w - 30, 2)
    while cta_lines and max(text_width(draw, ln, cta_font) for ln in cta_lines) > btn_w - 28 and cta_font.size > 18:
        cta_font = load_font(cta_font.size - 2, bold=True)
        cta_lines = wrap_text(draw, cta, cta_font, btn_w - 30, 2)
    lh = cta_font.size + 3
    ty = by + (btn_h - lh * len(cta_lines)) // 2
    for ln in cta_lines:
        tw = text_width(draw, ln, cta_font)
        tx = bx + (btn_w - tw) // 2
        draw.text((tx, ty), ln, font=cta_font, fill=WHITE, stroke_width=1, stroke_fill=SHADOW)
        ty += lh

    out_path = OUT_DIR / f"post_{post_num:02d}_branded_v3.png"
    canvas.convert("RGB").save(out_path, "PNG")
    return out_path


def build_contact_sheet(paths: List[Path]) -> None:
    cols = 6
    rows = (len(paths) + cols - 1) // cols
    thumb = 160
    label_h = 28
    pad = 20
    sheet_w = cols * thumb + (cols + 1) * pad
    sheet_h = rows * (thumb + label_h) + (rows + 1) * pad
    sheet = Image.new("RGB", (sheet_w, sheet_h), (10, 20, 40))
    draw = ImageDraw.Draw(sheet)
    label_font = load_font(20, bold=True)

    for i, path in enumerate(sorted(paths)):
        row = i // cols
        col = i % cols
        x = pad + col * (thumb + pad)
        y = pad + row * (thumb + label_h + pad)
        tile = Image.open(path).convert("RGB").resize((thumb, thumb), Image.LANCZOS)
        sheet.paste(tile, (x, y))
        label = path.stem.replace("_branded_v3", "").upper()
        draw.text((x, y + thumb + 4), label, font=label_font, fill=(225, 235, 255))

    sheet.save(CONTACT_SHEET_PATH, format="PNG")


def load_post_meta() -> Dict[int, str]:
    with PROMPT_PACK.open("r", encoding="utf-8") as handle:
        payload = json.load(handle)

    items: Dict[int, str] = {}
    for key, value in payload.items():
        if not isinstance(value, dict):
            continue
        post_num = parse_post_number(value.get("post")) or parse_post_number(key)
        if post_num is None:
            continue
        theme = str(value.get("theme", "")).strip()
        items[post_num] = theme
    return items


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    post_meta = load_post_meta()
    nate_badge = build_nate_badge(132)

    outputs: List[Path] = []
    missing: List[int] = []
    for post_num in range(1, 31):
        if post_num not in post_meta:
            missing.append(post_num)
            continue
        outputs.append(render_post(post_num, post_meta[post_num], nate_badge))

    if outputs:
        build_contact_sheet(outputs)

    print(f"Rendered V3 branded posts: {len(outputs)}")
    print(f"Output folder: {OUT_DIR}")
    print(f"Contact sheet: {CONTACT_SHEET_PATH}")
    if missing:
        print(f"Missing prompt metadata for posts: {missing}")


if __name__ == "__main__":
    main()
