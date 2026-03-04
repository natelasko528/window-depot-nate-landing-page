#!/usr/bin/env python3
"""
Render branded 30-post assets from raw square images.

Inputs:
  /workspace/ad-drafts/30-posts/raw/post_XX_raw.png

Outputs:
  /workspace/ad-drafts/30-posts/branded/post_XX_branded.png
  /workspace/ad-drafts/30-posts/branded/30posts_branded_contact_sheet.png
"""

from __future__ import annotations

from pathlib import Path
from typing import Dict, List

from PIL import Image, ImageDraw, ImageFont


ROOT = Path("/workspace")
RAW_DIR = ROOT / "ad-drafts" / "30-posts" / "raw"
BRANDED_DIR = ROOT / "ad-drafts" / "30-posts" / "branded"
CONTACT_SHEET_PATH = BRANDED_DIR / "30posts_branded_contact_sheet.png"

SIZE = 1080
TOP_BANNER_H = 270
FOOTER_H = 210
MIDDLE_Y0 = TOP_BANNER_H
MIDDLE_Y1 = SIZE - FOOTER_H

NAVY = (18, 32, 64, 255)       # #122040
BLUE = (30, 80, 160, 255)      # #1E50A0
LIGHT_BLUE = (100, 160, 220, 255)
WHITE = (255, 255, 255, 255)
GOLD = (255, 210, 85, 255)
SHADOW = (0, 0, 0, 170)


# In-script content source, required fields only.
POST_SPECS: List[Dict[str, str]] = [
    {"post": 1, "headline": "WINDOW WARNING SIGNS", "solution": "Upgrade to energy-efficient triple-pane windows with a free in-home estimate.", "cta": "Book Your Free Estimate"},
    {"post": 2, "headline": "BOOK DIRECTLY WITH NATE", "solution": "Get one local point of contact and a no-pressure consultation.", "cta": "Claim $1,000 OFF - Book Now"},
    {"post": 3, "headline": "ENTRY DOOR UPGRADE", "solution": "Install a ProVia door built for Wisconsin weather and daily use.", "cta": "Schedule Your Door Estimate"},
    {"post": 4, "headline": "TRUSTED BY MILWAUKEE", "solution": "Work with a 4.9-star team backed by 1,000+ homeowner reviews.", "cta": "Talk With Nate Today"},
    {"post": 5, "headline": "PROTECT YOUR EXTERIOR", "solution": "Replace siding with durable options made for freeze-thaw cycles.", "cta": "Get Siding Pricing"},
    {"post": 6, "headline": "SPRING HOME RESET", "solution": "Inspect windows, doors, and siding now before bigger issues grow.", "cta": "Book Spring Estimate"},
    {"post": 7, "headline": "ROOF RED FLAGS", "solution": "Get a professional roof inspection and clear replacement options.", "cta": "Request Free Roof Check"},
    {"post": 8, "headline": "FREE ESTIMATE CTA", "solution": "Nate walks you through options in-home with zero pressure.", "cta": "Start With a Free Estimate"},
    {"post": 9, "headline": "BATHROOM IN A DAY", "solution": "Upgrade to a cleaner, safer shower system with fast installation.", "cta": "Book Bath Consultation"},
    {"post": 10, "headline": "ONE CREW. DONE RIGHT.", "solution": "Use one accountable team from estimate through installation.", "cta": "Schedule Your Project Review"},
    {"post": 11, "headline": "TRIPLE PANE VALUE", "solution": "Get ProVia Endure triple-pane at dual-pane pricing.", "cta": "See Energy Savings"},
    {"post": 12, "headline": "PROVIA DOOR QUALITY", "solution": "Choose fiberglass or steel doors built for durability and efficiency.", "cta": "Upgrade Your Entry Door"},
    {"post": 13, "headline": "FLOORING MADE SIMPLE", "solution": "Bring samples to your home and choose flooring with confidence.", "cta": "Book In-Home Flooring Visit"},
    {"post": 14, "headline": "LOCAL SHOWROOM SUPPORT", "solution": "Get local expertise backed by seven SE Wisconsin showrooms.", "cta": "Connect With Local Team"},
    {"post": 15, "headline": "NO-PRESSURE CONSULTS", "solution": "Receive straightforward recommendations and transparent pricing.", "cta": "Book Stress-Free Estimate"},
    {"post": 16, "headline": "METAL ROOF LONGEVITY", "solution": "Consider long-life metal roofing for durability and peace of mind.", "cta": "Explore Roofing Options"},
    {"post": 17, "headline": "BUILT FOR WI WINTERS", "solution": "Install products selected specifically for Wisconsin conditions.", "cta": "Weatherproof Your Home"},
    {"post": 18, "headline": "LOCAL, NOT A CALL CENTER", "solution": "Work with a local team that shows up and follows through.", "cta": "Call Nate Directly"},
    {"post": 19, "headline": "LOCK YOUR PRICE", "solution": "Use price-lock style quoting for clear budgeting from day one.", "cta": "Get Transparent Quote"},
    {"post": 20, "headline": "TRUE BEFORE & AFTER", "solution": "Upgrade key exterior elements to transform comfort and curb appeal.", "cta": "Plan Your Transformation"},
    {"post": 21, "headline": "SUMMER BILL RELIEF", "solution": "Improve efficiency with high-performance window systems.", "cta": "Lower Cooling Costs"},
    {"post": 22, "headline": "SELLABILITY BOOST", "solution": "Modern windows, doors, and siding create standout first impressions.", "cta": "Improve Home Value"},
    {"post": 23, "headline": "BBB + REVIEW PROOF", "solution": "Choose a team with strong ratings, reviews, and local credibility.", "cta": "See Why Homeowners Choose Us"},
    {"post": 24, "headline": "WINDOW + DOOR COMBO", "solution": "Bundle windows and doors with one timeline and one crew.", "cta": "Bundle & Save Time"},
    {"post": 25, "headline": "SAFER BATH ACCESS", "solution": "Switch to a safer walk-in shower built for daily comfort.", "cta": "Book Accessibility Consult"},
    {"post": 26, "headline": "SIDING COLOR REFRESH", "solution": "Select modern siding profiles and colors with long-term protection.", "cta": "Design Your Exterior"},
    {"post": 27, "headline": "STORM DAMAGE SUPPORT", "solution": "Get expert repair guidance and full-scope roofing solutions.", "cta": "Start Storm Repair Plan"},
    {"post": 28, "headline": "MEET NATE", "solution": "Get direct communication from estimate to project completion.", "cta": "Text Nate to Start"},
    {"post": 29, "headline": "FLEXIBLE SCHEDULING", "solution": "Choose appointment windows that match your real schedule.", "cta": "Pick Your Best Time"},
    {"post": 30, "headline": "YEAR-ROUND OFFER", "solution": "Use this season to lock in pricing and plan your project confidently.", "cta": "Book Now - Save $1,000"},
]


def load_font(size: int, bold: bool = True) -> ImageFont.FreeTypeFont:
    candidates: List[tuple[str, int]] = [
        ("/usr/share/fonts/truetype/macos/Helvetica.ttc", 1 if bold else 0),
        ("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 0),
        ("/usr/share/fonts/truetype/liberation2/LiberationSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf", 0),
    ]
    for path, idx in candidates:
        try:
            return ImageFont.truetype(path, size=size, index=idx)
        except Exception:
            continue
    return ImageFont.load_default()


def fit_and_crop(img: Image.Image, target_w: int, target_h: int) -> Image.Image:
    img = img.convert("RGBA")
    scale = max(target_w / img.width, target_h / img.height)
    nw = int(img.width * scale)
    nh = int(img.height * scale)
    resized = img.resize((nw, nh), Image.LANCZOS)
    x0 = (nw - target_w) // 2
    y0 = (nh - target_h) // 2
    return resized.crop((x0, y0, x0 + target_w, y0 + target_h))


def text_width(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.ImageFont) -> int:
    box = draw.textbbox((0, 0), text, font=font)
    return box[2] - box[0]


def trim_dangling(words: List[str]) -> List[str]:
    bad_endings = {
        "and",
        "or",
        "to",
        "with",
        "for",
        "of",
        "a",
        "an",
        "the",
        "no",
        "in",
        "on",
        "at",
        "by",
    }
    while words:
        last = words[-1].lower().strip(".,;:!?")
        if last not in bad_endings:
            break
        words.pop()
    return words


def compact_sentence(text: str, max_words: int) -> str:
    cleaned = text.replace(" - ", " ").replace("-", " ").replace("  ", " ").strip()
    words = cleaned.split()
    if len(words) <= max_words:
        return cleaned.rstrip(".,;:!?")
    clipped = trim_dangling(words[:max_words])
    if not clipped:
        clipped = words[: max(1, min(3, len(words)))]
    return " ".join(clipped).rstrip(".,;:!?")


def wrap_text(
    draw: ImageDraw.ImageDraw,
    text: str,
    font: ImageFont.ImageFont,
    max_width: int,
    max_lines: int | None = None,
) -> List[str]:
    words = text.split()
    if not words:
        return []

    lines: List[str] = []
    current: List[str] = []
    idx = 0
    truncated = False

    while idx < len(words):
        word = words[idx]
        trial = " ".join(current + [word]).strip()
        if current and text_width(draw, trial, font) > max_width:
            lines.append(" ".join(current))
            current = []
            if max_lines and len(lines) >= max_lines:
                truncated = True
                break
        else:
            current.append(word)
            idx += 1

    if current and (not max_lines or len(lines) < max_lines):
        lines.append(" ".join(current))

    if max_lines and len(lines) > max_lines:
        lines = lines[:max_lines]
        truncated = True

    if max_lines and (truncated or idx < len(words)):
        max_words = max(2, max_width // max(14, int(getattr(font, "size", 32) * 0.55)))
        compacted = compact_sentence(text, max_words)
        lines = wrap_text(draw, compacted, font, max_width, None)
        if max_lines and len(lines) > max_lines:
            lines = lines[:max_lines]
            lines[-1] = " ".join(trim_dangling(lines[-1].split()))

    sanitized: List[str] = []
    for line in lines:
        parts = trim_dangling(line.split())
        if parts:
            sanitized.append(" ".join(parts))
    return sanitized


def draw_centered_lines(
    draw: ImageDraw.ImageDraw,
    lines: List[str],
    font: ImageFont.ImageFont,
    y_start: int,
    fill: tuple[int, int, int, int],
    line_gap: int,
    stroke_fill: tuple[int, int, int, int] = SHADOW,
    stroke_width: int = 2,
) -> int:
    y = y_start
    for line in lines:
        w = text_width(draw, line, font)
        x = (SIZE - w) // 2
        draw.text((x, y), line, font=font, fill=fill, stroke_width=stroke_width, stroke_fill=stroke_fill)
        y += font.size + line_gap
    return y


def draw_top_banner(draw: ImageDraw.ImageDraw, spec: Dict[str, str]) -> None:
    draw.rectangle((0, 0, SIZE, TOP_BANNER_H), fill=NAVY)
    draw.rectangle((0, TOP_BANNER_H - 3, SIZE, TOP_BANNER_H), fill=LIGHT_BLUE)

    headline_font = load_font(82, bold=True)
    headline_lines = wrap_text(draw, spec["headline"].upper(), headline_font, 1000, max_lines=2)
    while (
        (not headline_lines or len(headline_lines) > 2)
        or (headline_lines and max(text_width(draw, ln, headline_font) for ln in headline_lines) > 1000)
        or (len(headline_lines) * (headline_font.size + 6) > 150)
    ) and headline_font.size > 46:
        headline_font = load_font(headline_font.size - 2, bold=True)
        headline_lines = wrap_text(draw, spec["headline"].upper(), headline_font, 1000, max_lines=2)

    y = 24
    y = draw_centered_lines(draw, headline_lines, headline_font, y, WHITE, line_gap=6, stroke_width=3)

    solution_text = compact_sentence(spec["solution"], max_words=14)
    solution_font = load_font(56, bold=True)
    sub_lines = wrap_text(draw, solution_text, solution_font, 980, max_lines=2)
    max_sub_h = TOP_BANNER_H - y - 14
    while (
        (not sub_lines or len(sub_lines) > 2)
        or (sub_lines and max(text_width(draw, ln, solution_font) for ln in sub_lines) > 980)
        or (len(sub_lines) * (solution_font.size + 5) > max_sub_h)
    ) and solution_font.size > 30:
        solution_font = load_font(solution_font.size - 2, bold=True)
        sub_lines = wrap_text(draw, solution_text, solution_font, 980, max_lines=2)

    draw_centered_lines(draw, sub_lines, solution_font, y + 2, GOLD, line_gap=5, stroke_width=2)


def draw_footer(draw: ImageDraw.ImageDraw, spec: Dict[str, str]) -> None:
    y0 = SIZE - FOOTER_H
    draw.rectangle((0, y0, SIZE, SIZE), fill=NAVY)
    draw.rectangle((0, y0, SIZE, y0 + 3), fill=LIGHT_BLUE)

    logo_main = load_font(84, bold=True)
    logo_sub = load_font(48, bold=True)
    logo_x = 32
    logo_y = y0 + 26

    # Exact spelling required by spec.
    draw.text((logo_x, logo_y), "WINDOW DEPOT", font=logo_main, fill=WHITE, stroke_width=3, stroke_fill=SHADOW)
    draw.text((logo_x + 6, logo_y + 92), "of MILWAUKEE", font=logo_sub, fill=GOLD, stroke_width=2, stroke_fill=SHADOW)

    btn_w = 420
    btn_h = 126
    btn_x = SIZE - btn_w - 32
    btn_y = y0 + 42
    draw.rounded_rectangle((btn_x, btn_y, btn_x + btn_w, btn_y + btn_h), radius=24, fill=BLUE)
    draw.rounded_rectangle((btn_x, btn_y, btn_x + btn_w, btn_y + btn_h), radius=24, outline=LIGHT_BLUE, width=3)

    cta_font = load_font(44, bold=True)
    cta_lines = wrap_text(draw, spec["cta"], cta_font, btn_w - 48, max_lines=2)
    while (
        (not cta_lines or len(cta_lines) > 2)
        or (cta_lines and max(text_width(draw, ln, cta_font) for ln in cta_lines) > btn_w - 48)
        or (len(cta_lines) * (cta_font.size + 5) > btn_h - 24)
    ) and cta_font.size > 24:
        cta_font = load_font(cta_font.size - 2, bold=True)
        cta_lines = wrap_text(draw, spec["cta"], cta_font, btn_w - 48, max_lines=2)

    line_h = cta_font.size + 5
    total_h = len(cta_lines) * line_h
    ty = btn_y + (btn_h - total_h) // 2
    for line in cta_lines:
        w = text_width(draw, line, cta_font)
        tx = btn_x + (btn_w - w) // 2
        draw.text((tx, ty), line, font=cta_font, fill=WHITE, stroke_width=2, stroke_fill=SHADOW)
        ty += line_h


def render_post(spec: Dict[str, str]) -> Path:
    post_num = int(spec["post"])
    raw_path = RAW_DIR / f"post_{post_num:02d}_raw.png"
    if not raw_path.exists():
        raise FileNotFoundError(str(raw_path))

    canvas = Image.new("RGBA", (SIZE, SIZE), NAVY)
    draw = ImageDraw.Draw(canvas, "RGBA")

    middle_img = fit_and_crop(Image.open(raw_path), SIZE, MIDDLE_Y1 - MIDDLE_Y0)
    canvas.paste(middle_img, (0, MIDDLE_Y0), middle_img)

    # No opaque blocks in the middle image section, only top and footer branding.
    draw_top_banner(draw, spec)
    draw_footer(draw, spec)

    out_path = BRANDED_DIR / f"post_{post_num:02d}_branded.png"
    canvas.convert("RGB").save(out_path, format="PNG")
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
    label_font = load_font(22, bold=True)

    for i, path in enumerate(sorted(paths)):
        row = i // cols
        col = i % cols
        x = pad + col * (thumb + pad)
        y = pad + row * (thumb + label_h + pad)
        tile = Image.open(path).convert("RGB").resize((thumb, thumb), Image.LANCZOS)
        sheet.paste(tile, (x, y))
        label = path.stem.replace("_branded", "").upper()
        draw.text((x, y + thumb + 4), label, font=label_font, fill=(225, 235, 255))

    sheet.save(CONTACT_SHEET_PATH, format="PNG")


def validate_specs() -> None:
    required = {"post", "headline", "solution", "cta"}
    seen: set[int] = set()
    for spec in POST_SPECS:
        if set(spec.keys()) != required:
            raise ValueError(f"Spec keys must be exactly {required}: {spec}")
        post_num = int(spec["post"])
        if post_num in seen:
            raise ValueError(f"Duplicate post number: {post_num}")
        seen.add(post_num)
    if seen != set(range(1, 31)):
        raise ValueError("POST_SPECS must include posts 1 through 30.")


def main() -> None:
    validate_specs()
    BRANDED_DIR.mkdir(parents=True, exist_ok=True)

    outputs: List[Path] = []
    missing: List[Path] = []

    for spec in sorted(POST_SPECS, key=lambda s: int(s["post"])):
        try:
            outputs.append(render_post(spec))
        except FileNotFoundError:
            missing.append(RAW_DIR / f"post_{int(spec['post']):02d}_raw.png")

    if outputs:
        build_contact_sheet(outputs)

    print(f"Rendered branded posts: {len(outputs)}")
    print(f"Branded output folder: {BRANDED_DIR}")
    print(f"Contact sheet: {CONTACT_SHEET_PATH}")

    if missing:
        print("Missing raw input files:")
        for path in missing:
            print(f" - {path}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
