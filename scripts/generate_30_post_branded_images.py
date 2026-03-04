#!/usr/bin/env python3
"""
Generate 30 branded social images (one per post) with:
- Clear pain point
- Clear solution
- CTA button
- Branded footer
"""

from __future__ import annotations

from pathlib import Path
from typing import Dict, List

from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance


ROOT = Path("/workspace")
SRC_DIR = ROOT / "ad-drafts" / "30-posts"
OUT_DIR = SRC_DIR / "branded"
CONTACT_SHEET_PATH = OUT_DIR / "30posts_branded_contact_sheet.png"

BRAND_NAVY = (18, 32, 64, 255)          # #122040
BRAND_BLUE = (30, 80, 160, 255)         # #1E50A0
BRAND_LIGHT = (100, 160, 220, 255)      # #64A0DC
BRAND_WHITE = (255, 255, 255, 255)
BRAND_GOLD = (212, 175, 55, 255)        # #D4AF37
BRAND_RED = (208, 44, 44, 255)
SHADOW = (0, 0, 0, 190)

PHONE = "(414) 312-5213"
WEBSITE = "windowdepotmilwaukee.com"
BRAND_LINE = "WINDOW DEPOT USA OF MILWAUKEE"
TAGLINE = "National Strength. Local Service."

BASE_IMAGES: Dict[str, Path] = {
    "windows": SRC_DIR / "30posts-windows-hero.png",
    "doors": SRC_DIR / "30posts-doors-hero.png",
    "siding": SRC_DIR / "30posts-siding-hero.png",
    "roofing": SRC_DIR / "30posts-roofing-hero.png",
    "bathroom": SRC_DIR / "30posts-bathroom-hero.png",
    # Use clean photo base for CTA variants to avoid embedded legacy text.
    "cta": SRC_DIR / "30posts-windows-hero.png",
}


def load_font(size: int, bold: bool = True) -> ImageFont.FreeTypeFont:
    # macOS Helvetica collection available in this cloud image
    helvetica_path = "/usr/share/fonts/truetype/macos/Helvetica.ttc"
    dejavu_bold = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
    dejavu = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
    try:
        return ImageFont.truetype(helvetica_path, size, index=1 if bold else 0)
    except Exception:
        try:
            return ImageFont.truetype(dejavu_bold if bold else dejavu, size)
        except Exception:
            return ImageFont.load_default()


def wrap_text(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.ImageFont, max_width: int) -> List[str]:
    words = text.split()
    lines: List[str] = []
    current: List[str] = []
    for word in words:
        test = " ".join(current + [word]).strip()
        w = draw.textbbox((0, 0), test, font=font)[2]
        if w <= max_width or not current:
            current.append(word)
        else:
            lines.append(" ".join(current))
            current = [word]
    if current:
        lines.append(" ".join(current))
    return lines


def fit_to_square(img: Image.Image, size: int = 1080) -> Image.Image:
    img = img.convert("RGBA")
    scale = max(size / img.width, size / img.height)
    nw, nh = int(img.width * scale), int(img.height * scale)
    resized = img.resize((nw, nh), Image.LANCZOS)
    x = (nw - size) // 2
    y = (nh - size) // 2
    return resized.crop((x, y, x + size, y + size))


def add_rect(draw: ImageDraw.ImageDraw, box, fill, radius: int = 18):
    draw.rounded_rectangle(box, radius=radius, fill=fill)


def draw_shadow_text(draw: ImageDraw.ImageDraw, xy, text: str, font, fill):
    x, y = xy
    draw.text((x + 2, y + 2), text, font=font, fill=SHADOW)
    draw.text((x, y), text, font=font, fill=fill)


def split_title(headline: str) -> tuple[str, str]:
    words = headline.split()
    if len(words) < 4:
        return headline, ""
    half = len(words) // 2
    return " ".join(words[:half]), " ".join(words[half:])


def compact_phrase(text: str, max_words: int = 7) -> str:
    words = text.replace("—", " ").split()
    clipped = words[:max_words]
    bad_endings = {"and", "or", "to", "with", "for", "of", "a", "an", "the", "no"}
    while clipped and clipped[-1].lower().strip(".,;:!?") in bad_endings:
        clipped.pop()
    snippet = " ".join(clipped).rstrip(".,;:!?")
    return snippet


def build_subline(solution: str) -> str:
    # Solution-focused subheading, styled to stand out under headline.
    return f"{compact_phrase(solution, 9)}."


def prepare_middle_image(base: Image.Image, post_num: int, size: tuple[int, int]) -> Image.Image:
    """Create per-post image variations while preserving full-photo readability."""
    tw, th = size
    base = base.convert("RGBA")

    # Deterministic zoom/offset so each post has a unique visual variation.
    zoom = 1.04 + (post_num % 5) * 0.03
    w = int(base.width * zoom)
    h = int(base.height * zoom)
    base = base.resize((w, h), Image.LANCZOS)

    x_room = max(0, w - tw)
    y_room = max(0, h - th)
    x_off = int((post_num * 37) % (x_room + 1)) if x_room else 0
    y_off = int((post_num * 19) % (y_room + 1)) if y_room else 0
    cropped = base.crop((x_off, y_off, x_off + tw, y_off + th))

    # Subtle per-post tone shift.
    color = ImageEnhance.Color(cropped)
    contrast = ImageEnhance.Contrast(cropped)
    brightness = ImageEnhance.Brightness(cropped)
    c_factor = 1.00 + ((post_num % 4) - 1.5) * 0.03
    k_factor = 1.00 + ((post_num % 3) - 1) * 0.04
    b_factor = 1.00 + ((post_num % 5) - 2) * 0.015
    out = color.enhance(c_factor)
    out = contrast.enhance(k_factor)
    out = brightness.enhance(b_factor)

    # Mild sharpening for cleaner ad look.
    out = out.filter(ImageFilter.UnsharpMask(radius=1.2, percent=130, threshold=2))
    return out


POST_SPECS = [
    {"post": 1, "theme": "windows", "headline": "WINDOW WARNING SIGNS", "pain": "Drafts, foggy glass, and rising bills mean your windows are costing you money.", "solution": "Upgrade to energy-efficient triple-pane windows with a free in-home estimate.", "cta": "Book Your Free Estimate"},
    {"post": 2, "theme": "cta", "headline": "BOOK DIRECTLY WITH NATE", "pain": "Homeowners are tired of call centers and unclear next steps.", "solution": "Get one local point of contact and a no-pressure consultation.", "cta": "Claim $1,000 OFF - Book Now"},
    {"post": 3, "theme": "doors", "headline": "ENTRY DOOR UPGRADE", "pain": "An outdated front door hurts curb appeal, comfort, and security.", "solution": "Install a ProVia door built for Wisconsin weather and daily use.", "cta": "Schedule Your Door Estimate"},
    {"post": 4, "theme": "windows", "headline": "TRUSTED BY MILWAUKEE", "pain": "Choosing the wrong contractor can lead to expensive rework.", "solution": "Work with a 4.9-star team backed by 1,000+ homeowner reviews.", "cta": "Talk With Nate Today"},
    {"post": 5, "theme": "siding", "headline": "PROTECT YOUR EXTERIOR", "pain": "Cracked or faded siding lets moisture in and value out.", "solution": "Replace siding with durable options made for freeze-thaw cycles.", "cta": "Get Siding Pricing"},
    {"post": 6, "theme": "windows", "headline": "SPRING HOME RESET", "pain": "Winter damage often stays hidden until spring storms arrive.", "solution": "Inspect windows, doors, and siding now before bigger issues grow.", "cta": "Book Spring Estimate"},
    {"post": 7, "theme": "roofing", "headline": "ROOF RED FLAGS", "pain": "Missing shingles and ceiling stains can quickly become major repairs.", "solution": "Get a professional roof inspection and clear replacement options.", "cta": "Request Free Roof Check"},
    {"post": 8, "theme": "cta", "headline": "FREE ESTIMATE CTA", "pain": "Most homeowners delay projects because the process feels overwhelming.", "solution": "Nate walks you through options in-home with zero pressure.", "cta": "Start With a Free Estimate"},
    {"post": 9, "theme": "bathroom", "headline": "BATHROOM IN A DAY", "pain": "Old tubs and stained grout make daily routines frustrating.", "solution": "Upgrade to a cleaner, safer shower system with fast installation.", "cta": "Book Bath Consultation"},
    {"post": 10, "theme": "windows", "headline": "ONE CREW. DONE RIGHT.", "pain": "Multiple subcontractors often cause delays and inconsistent quality.", "solution": "Use one accountable team from estimate through installation.", "cta": "Schedule Your Project Review"},
    {"post": 11, "theme": "windows", "headline": "TRIPLE PANE VALUE", "pain": "Dual-pane performance can still leave comfort and savings on the table.", "solution": "Get ProVia Endure triple-pane at dual-pane pricing.", "cta": "See Energy Savings"},
    {"post": 12, "theme": "doors", "headline": "PROVIA DOOR QUALITY", "pain": "Cheap doors warp, leak air, and age quickly in harsh weather.", "solution": "Choose fiberglass or steel doors built for durability and efficiency.", "cta": "Upgrade Your Entry Door"},
    {"post": 13, "theme": "cta", "headline": "FLOORING MADE SIMPLE", "pain": "Showroom shopping is time-consuming and hard to visualize at home.", "solution": "Bring samples to your home and choose flooring with confidence.", "cta": "Book In-Home Flooring Visit"},
    {"post": 14, "theme": "windows", "headline": "LOCAL SHOWROOM SUPPORT", "pain": "Remote-only brands often miss local design and climate needs.", "solution": "Get local expertise backed by seven SE Wisconsin showrooms.", "cta": "Connect With Local Team"},
    {"post": 15, "theme": "windows", "headline": "NO-PRESSURE CONSULTS", "pain": "High-pressure sales calls make homeowners postpone necessary upgrades.", "solution": "Receive straightforward recommendations and transparent pricing.", "cta": "Book Stress-Free Estimate"},
    {"post": 16, "theme": "roofing", "headline": "METAL ROOF LONGEVITY", "pain": "Frequent asphalt repairs add up over time.", "solution": "Consider long-life metal roofing for durability and peace of mind.", "cta": "Explore Roofing Options"},
    {"post": 17, "theme": "windows", "headline": "BUILT FOR WI WINTERS", "pain": "Freeze-thaw cycles expose weak materials and poor insulation.", "solution": "Install products selected specifically for Wisconsin conditions.", "cta": "Weatherproof Your Home"},
    {"post": 18, "theme": "windows", "headline": "LOCAL, NOT A CALL CENTER", "pain": "Generic support leaves homeowners without real accountability.", "solution": "Work with a local team that shows up and follows through.", "cta": "Call Nate Directly"},
    {"post": 19, "theme": "windows", "headline": "LOCK YOUR PRICE", "pain": "Unexpected add-ons and moving quotes break homeowner trust.", "solution": "Use price-lock style quoting for clear budgeting from day one.", "cta": "Get Transparent Quote"},
    {"post": 20, "theme": "windows", "headline": "TRUE BEFORE & AFTER", "pain": "Homes can feel dated, drafty, and uncomfortable year-round.", "solution": "Upgrade key exterior elements to transform comfort and curb appeal.", "cta": "Plan Your Transformation"},
    {"post": 21, "theme": "windows", "headline": "SUMMER BILL RELIEF", "pain": "Old windows force your AC to work harder and cost more.", "solution": "Improve efficiency with high-performance window systems.", "cta": "Lower Cooling Costs"},
    {"post": 22, "theme": "windows", "headline": "SELLABILITY BOOST", "pain": "Weak curb appeal can reduce buyer interest and offer strength.", "solution": "Modern windows, doors, and siding create standout first impressions.", "cta": "Improve Home Value"},
    {"post": 23, "theme": "windows", "headline": "BBB + REVIEW PROOF", "pain": "Homeowners need proof before trusting a major remodel decision.", "solution": "Choose a team with strong ratings, reviews, and local credibility.", "cta": "See Why Homeowners Choose Us"},
    {"post": 24, "theme": "doors", "headline": "WINDOW + DOOR COMBO", "pain": "Managing separate contractors increases cost and complexity.", "solution": "Bundle windows and doors with one timeline and one crew.", "cta": "Bundle & Save Time"},
    {"post": 25, "theme": "bathroom", "headline": "SAFER BATH ACCESS", "pain": "High step-in tubs and slippery surfaces increase fall risk.", "solution": "Switch to a safer walk-in shower built for daily comfort.", "cta": "Book Accessibility Consult"},
    {"post": 26, "theme": "siding", "headline": "SIDING COLOR REFRESH", "pain": "A worn exterior can make the whole home feel outdated.", "solution": "Select modern siding profiles and colors with long-term protection.", "cta": "Design Your Exterior"},
    {"post": 27, "theme": "roofing", "headline": "STORM DAMAGE SUPPORT", "pain": "Post-storm damage is stressful and insurance steps are confusing.", "solution": "Get expert repair guidance and full-scope roofing solutions.", "cta": "Start Storm Repair Plan"},
    {"post": 28, "theme": "windows", "headline": "MEET NATE", "pain": "Homeowners want one accountable expert, not a handoff chain.", "solution": "Get direct communication from estimate to project completion.", "cta": "Text Nate to Start"},
    {"post": 29, "theme": "windows", "headline": "FLEXIBLE SCHEDULING", "pain": "Busy families struggle to fit consultations into weekday hours.", "solution": "Choose appointment windows that match your real schedule.", "cta": "Pick Your Best Time"},
    {"post": 30, "theme": "cta", "headline": "YEAR-ROUND OFFER", "pain": "Delaying upgrades keeps energy loss and comfort issues in place.", "solution": "Use this season to lock in pricing and plan your project confidently.", "cta": "Book Now - Save $1,000"},
]


def make_post_image(spec: dict) -> Path:
    base_path = BASE_IMAGES[spec["theme"]]
    if not base_path.exists():
        raise FileNotFoundError(f"Missing base image: {base_path}")

    # Reference template geometry:
    # top banner (0-300), image zone (300-900), footer (900-1080)
    canvas = Image.new("RGBA", (1080, 1080), BRAND_NAVY)
    draw = ImageDraw.Draw(canvas, "RGBA")

    top_h = 300
    mid_y0, mid_y1 = 300, 900
    foot_y0 = 900

    # Middle imagery should shine through with no opaque text blocks.
    mid_img = prepare_middle_image(Image.open(base_path), spec["post"], (1080, mid_y1 - mid_y0))
    canvas.paste(mid_img, (0, mid_y0), mid_img)

    # Top dark branded banner
    draw.rectangle((0, 0, 1080, top_h), fill=BRAND_NAVY)
    draw.rectangle((0, top_h - 2, 1080, top_h), fill=(75, 125, 190, 255))

    # Footer band + top border
    draw.rectangle((0, foot_y0, 1080, 1080), fill=BRAND_NAVY)
    draw.rectangle((0, foot_y0, 1080, foot_y0 + 2), fill=(75, 125, 190, 255))

    # Headline (two lines) + subline
    title_a, title_b = split_title(spec["headline"])
    h1_font = load_font(80, bold=True)
    h2_font = load_font(80, bold=True)

    # Fit title sizes for long headlines
    max_w = 1020
    while draw.textbbox((0, 0), title_a, font=h1_font)[2] > max_w and h1_font.size > 50:
        h1_font = load_font(h1_font.size - 2, bold=True)
    while title_b and draw.textbbox((0, 0), title_b, font=h2_font)[2] > max_w and h2_font.size > 50:
        h2_font = load_font(h2_font.size - 2, bold=True)

    y = 26
    if title_a:
        w = draw.textbbox((0, 0), title_a, font=h1_font)[2]
        draw_shadow_text(draw, ((1080 - w) // 2, y), title_a, h1_font, BRAND_WHITE)
        y += h1_font.size + 10
    if title_b:
        w = draw.textbbox((0, 0), title_b, font=h2_font)[2]
        draw_shadow_text(draw, ((1080 - w) // 2, y), title_b, h2_font, BRAND_WHITE)
        y += h2_font.size + 10

    # Bigger yellow solution subheading per request.
    subline = build_subline(spec["solution"])
    subline_font = load_font(44, bold=True)
    available_h = max(24, top_h - y - 14)
    sub_lines = wrap_text(draw, subline, subline_font, 960)[:2]
    while subline_font.size > 26 and (len(sub_lines) * (subline_font.size + 4) > available_h):
        subline_font = load_font(subline_font.size - 2, bold=True)
        sub_lines = wrap_text(draw, subline, subline_font, 960)[:2]

    for line in sub_lines:
        w = draw.textbbox((0, 0), line, font=subline_font)[2]
        draw_shadow_text(draw, ((1080 - w) // 2, y + 6), line, subline_font, BRAND_GOLD)
        y += subline_font.size + 4

    # Optional before/after labels for transformation-heavy posts.
    if spec["post"] in {20, 22}:
        lbl_font = load_font(52, bold=True)
        draw_shadow_text(draw, (40, 834), "BEFORE", lbl_font, BRAND_WHITE)
        w = draw.textbbox((0, 0), "AFTER", font=lbl_font)[2]
        draw_shadow_text(draw, (1080 - 40 - w, 834), "AFTER", lbl_font, BRAND_WHITE)

    # Footer left "logo-like" wordmark to mirror reference style.
    logo_main_font = load_font(78, bold=True)
    logo_sub_font = load_font(44, bold=True)
    logo_x = 24
    logo_y = 936

    # Stroke-style effect for stronger brand lockup.
    draw.text((logo_x, logo_y), "WNDWDEPOT", font=logo_main_font, fill=BRAND_WHITE, stroke_width=3, stroke_fill=(18, 52, 120, 255))
    draw.text((logo_x + 118, logo_y + 64), "of MILWAUKEE", font=logo_sub_font, fill=BRAND_RED)

    # CTA button on footer right, two-line support if needed.
    cta_text = spec["cta"]
    cta_font = load_font(46, bold=True)
    btn_w, btn_h = 500, 138
    btn_x = 1080 - btn_w - 24
    btn_y = 930
    add_rect(draw, (btn_x, btn_y, btn_x + btn_w, btn_y + btn_h), BRAND_BLUE, radius=26)

    cta_lines = wrap_text(draw, cta_text, cta_font, btn_w - 60)
    if len(cta_lines) > 2:
        cta_lines = cta_lines[:2]
    while any(draw.textbbox((0, 0), ln, font=cta_font)[2] > btn_w - 60 for ln in cta_lines) and cta_font.size > 28:
        cta_font = load_font(cta_font.size - 2, bold=True)
        cta_lines = wrap_text(draw, cta_text, cta_font, btn_w - 60)[:2]

    line_h = cta_font.size + 6
    total_h = len(cta_lines) * line_h
    ty = btn_y + (btn_h - total_h) // 2 - 2
    for ln in cta_lines:
        tw = draw.textbbox((0, 0), ln, font=cta_font)[2]
        draw_shadow_text(draw, (btn_x + (btn_w - tw) // 2, ty), ln, cta_font, BRAND_WHITE)
        ty += line_h

    out_path = OUT_DIR / f"post_{spec['post']:02d}_branded.png"
    canvas.convert("RGB").save(out_path, "PNG")
    return out_path


def build_contact_sheet(images: List[Path], cols: int = 5, thumb_w: int = 300, thumb_h: int = 300, pad: int = 20):
    rows = (len(images) + cols - 1) // cols
    width = cols * thumb_w + (cols + 1) * pad
    height = rows * (thumb_h + 44) + (rows + 1) * pad
    sheet = Image.new("RGB", (width, height), (12, 20, 40))
    draw = ImageDraw.Draw(sheet)
    label_font = load_font(24, bold=True)

    for i, path in enumerate(images):
        row, col = divmod(i, cols)
        x = pad + col * (thumb_w + pad)
        y = pad + row * (thumb_h + 44 + pad)
        thumb = Image.open(path).convert("RGB").resize((thumb_w, thumb_h), Image.LANCZOS)
        sheet.paste(thumb, (x, y))
        label = path.stem.replace("_branded", "").upper()
        draw.text((x, y + thumb_h + 10), label, fill=(235, 240, 255), font=label_font)

    sheet.save(CONTACT_SHEET_PATH, "PNG")


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    outputs: List[Path] = []
    for spec in POST_SPECS:
        outputs.append(make_post_image(spec))

    build_contact_sheet(outputs)

    print("=" * 60)
    print("Generated branded images:", len(outputs))
    print("Output folder:", OUT_DIR)
    print("Contact sheet:", CONTACT_SHEET_PATH)
    print("=" * 60)


if __name__ == "__main__":
    main()
