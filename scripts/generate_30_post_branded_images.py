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

from PIL import Image, ImageDraw, ImageFont, ImageFilter


ROOT = Path("/workspace")
SRC_DIR = ROOT / "ad-drafts" / "30-posts"
OUT_DIR = SRC_DIR / "branded"
CONTACT_SHEET_PATH = OUT_DIR / "30posts_branded_contact_sheet.png"

BRAND_NAVY = (18, 32, 64, 255)          # #122040
BRAND_BLUE = (30, 80, 160, 255)         # #1E50A0
BRAND_LIGHT = (100, 160, 220, 255)      # #64A0DC
BRAND_WHITE = (255, 255, 255, 255)
BRAND_GOLD = (212, 175, 55, 255)        # #D4AF37
SHADOW = (0, 0, 0, 180)

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
    "cta": SRC_DIR / "30posts-cta-estimate.png",
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


def add_rect(draw: ImageDraw.ImageDraw, box, fill):
    draw.rounded_rectangle(box, radius=18, fill=fill)


def draw_shadow_text(draw: ImageDraw.ImageDraw, xy, text: str, font, fill):
    x, y = xy
    draw.text((x + 2, y + 2), text, font=font, fill=SHADOW)
    draw.text((x, y), text, font=font, fill=fill)


def apply_soft_gradient(
    base: Image.Image,
    box: tuple[int, int, int, int],
    color: tuple[int, int, int] = (12, 24, 48),
    alpha_start: int = 140,
    alpha_end: int = 25,
) -> None:
    """Apply a transparent gradient so imagery still shines through."""
    x0, y0, x1, y1 = box
    overlay = Image.new("RGBA", base.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay, "RGBA")
    height = max(1, y1 - y0)
    for i in range(height):
        t = i / max(1, height - 1)
        a = int(alpha_start + (alpha_end - alpha_start) * t)
        draw.line([(x0, y0 + i), (x1, y0 + i)], fill=(color[0], color[1], color[2], a))
    base.alpha_composite(overlay)


def apply_frosted_panel(
    base: Image.Image,
    box: tuple[int, int, int, int],
    radius: int = 28,
    blur_radius: int = 8,
    tint: tuple[int, int, int, int] = (8, 24, 46, 108),
    border: tuple[int, int, int, int] = (130, 180, 245, 150),
) -> None:
    """Glass-morphism style text panel with blur + low opacity tint."""
    x0, y0, x1, y1 = box
    region = base.crop((x0, y0, x1, y1)).filter(ImageFilter.GaussianBlur(blur_radius))
    region = Image.alpha_composite(region, Image.new("RGBA", region.size, tint))

    mask = Image.new("L", region.size, 0)
    mdraw = ImageDraw.Draw(mask)
    mdraw.rounded_rectangle((0, 0, region.size[0] - 1, region.size[1] - 1), radius=radius, fill=255)
    base.paste(region, (x0, y0), mask)

    border_layer = Image.new("RGBA", base.size, (0, 0, 0, 0))
    bdraw = ImageDraw.Draw(border_layer, "RGBA")
    bdraw.rounded_rectangle((x0, y0, x1, y1), radius=radius, outline=border, width=2)
    base.alpha_composite(border_layer)


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

    canvas = fit_to_square(Image.open(base_path), 1080)
    draw = ImageDraw.Draw(canvas, "RGBA")

    # KING MODE transparent overlays: keep imagery visible.
    apply_soft_gradient(canvas, (0, 0, 1080, 260), color=(10, 22, 44), alpha_start=150, alpha_end=35)
    apply_soft_gradient(canvas, (0, 850, 1080, 1080), color=(10, 22, 44), alpha_start=20, alpha_end=165)
    apply_frosted_panel(canvas, (40, 280, 1040, 760), tint=(8, 24, 46, 94), blur_radius=9)
    apply_frosted_panel(canvas, (20, 885, 1060, 1060), tint=(8, 22, 46, 122), blur_radius=7, border=(120, 170, 240, 120))
    apply_frosted_panel(canvas, (20, 18, 1060, 252), tint=(8, 22, 46, 82), blur_radius=6, border=(120, 170, 240, 105))

    draw = ImageDraw.Draw(canvas, "RGBA")

    h_font = load_font(68, bold=True)
    h_lines = wrap_text(draw, spec["headline"], h_font, 1000)
    h_lines = h_lines[:2]
    h_y = 30
    for line in h_lines:
        line_w = draw.textbbox((0, 0), line, font=h_font)[2]
        draw_shadow_text(draw, ((1080 - line_w) // 2, h_y), line, h_font, BRAND_WHITE)
        h_y += 75

    # Post badge
    badge_text = f"POST {spec['post']:02d}"
    badge_font = load_font(26, bold=True)
    add_rect(draw, (40, 205, 220, 255), (30, 80, 160, 220))
    draw_shadow_text(draw, (60, 218), badge_text, badge_font, BRAND_WHITE)

    label_font = load_font(34, bold=True)
    body_font = load_font(40, bold=False)

    # Pain section
    draw_shadow_text(draw, (75, 325), "PAIN POINT", label_font, BRAND_GOLD)
    pain_lines = wrap_text(draw, spec["pain"], body_font, 930)[:3]
    py = 370
    for line in pain_lines:
        draw_shadow_text(draw, (75, py), line, body_font, BRAND_WHITE)
        py += 48

    # Divider
    draw.rectangle([(75, py + 10), (1005, py + 14)], fill=(100, 160, 220, 210))

    # Solution section
    sy = py + 28
    draw_shadow_text(draw, (75, sy), "SOLUTION", label_font, BRAND_LIGHT)
    solution_lines = wrap_text(draw, spec["solution"], body_font, 930)[:3]
    sy += 45
    for line in solution_lines:
        draw_shadow_text(draw, (75, sy), line, body_font, BRAND_WHITE)
        sy += 48

    # CTA button
    cta_font = load_font(40, bold=True)
    cta_text = spec["cta"]
    cta_w = draw.textbbox((0, 0), cta_text, font=cta_font)[2] + 80
    cta_w = min(cta_w, 920)
    cta_x = (1080 - cta_w) // 2
    cta_y = 795
    add_rect(draw, (cta_x, cta_y, cta_x + cta_w, cta_y + 72), (30, 80, 160, 222))
    tw = draw.textbbox((0, 0), cta_text, font=cta_font)[2]
    draw_shadow_text(draw, (cta_x + (cta_w - tw) // 2, cta_y + 15), cta_text, cta_font, BRAND_WHITE)

    # Footer
    footer_brand_font = load_font(38, bold=True)
    footer_meta_font = load_font(30, bold=True)
    footer_tag_font = load_font(26, bold=False)

    bw = draw.textbbox((0, 0), BRAND_LINE, font=footer_brand_font)[2]
    draw_shadow_text(draw, ((1080 - bw) // 2, 915), BRAND_LINE, footer_brand_font, BRAND_WHITE)

    info = f"{PHONE}  |  {WEBSITE}"
    iw = draw.textbbox((0, 0), info, font=footer_meta_font)[2]
    draw_shadow_text(draw, ((1080 - iw) // 2, 960), info, footer_meta_font, BRAND_LIGHT)

    tw2 = draw.textbbox((0, 0), TAGLINE, font=footer_tag_font)[2]
    draw_shadow_text(draw, ((1080 - tw2) // 2, 1002), TAGLINE, footer_tag_font, BRAND_GOLD)

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
