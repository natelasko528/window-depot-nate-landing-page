#!/usr/bin/env python3
"""
V3 — Modern Branded Overlay Generator for Window Depot USA Milwaukee
Philosophy: "SCROLL-STOPPING EDITORIAL"

Three tiers of branding:
  Tier 1 (Paid Ads):    Almost invisible — tiny frosted brand pill in corner
  Tier 2 (Organic):     Elegant bottom bar with Nate headshot badge + headline
  Tier 3 (Stories):     Text-forward with atmospheric photo backdrop

NO AI-generated people. Real Nate headshot only.
NO heavy navy overlays. Frosted glass + minimal opacity.
NO bullet point lists. One headline max.
"""

import os
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont, ImageFilter

BRAND_NAVY = (18, 32, 64)
BRAND_BLUE = (30, 80, 160)
BRAND_LIGHT_BLUE = (100, 160, 220)
BRAND_WHITE = (255, 255, 255)
BRAND_GOLD = (212, 175, 55)
PHONE = "(414) 312-5213"
BRAND_NAME = "Window Depot USA of Milwaukee"
BRAND_SHORT = "Window Depot USA"

FONT_PATH = "/usr/share/fonts/truetype/macos/Helvetica.ttc"
NATE_PHOTO = "/workspace/brand-assets/nate-profile.png"
OUT_DIR = "/workspace/ad-drafts"


def load_font(size, bold=True, condensed=False):
    try:
        if condensed:
            return ImageFont.truetype(FONT_PATH, size, index=10)
        elif bold:
            return ImageFont.truetype(FONT_PATH, size, index=1)
        else:
            return ImageFont.truetype(FONT_PATH, size, index=0)
    except Exception:
        try:
            return ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", size)
        except Exception:
            return ImageFont.load_default()


def get_nate_avatar(size=64):
    """Load real Nate headshot and crop to circle with white border."""
    img = Image.open(NATE_PHOTO).convert("RGBA")

    min_dim = min(img.width, img.height)
    left = (img.width - min_dim) // 2
    top = (img.height - min_dim) // 2
    img = img.crop((left, top, left + min_dim, top + min_dim))
    img = img.resize((size, size), Image.LANCZOS)

    mask = Image.new("L", (size, size), 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse([0, 0, size - 1, size - 1], fill=255)

    circular = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    circular.paste(img, (0, 0), mask)

    border_size = size + 6
    bordered = Image.new("RGBA", (border_size, border_size), (0, 0, 0, 0))
    border_draw = ImageDraw.Draw(bordered)
    border_draw.ellipse([0, 0, border_size - 1, border_size - 1], fill=BRAND_WHITE)
    bordered.paste(circular, (3, 3), circular)

    return bordered


def frosted_glass_region(base_img, bbox, blur_radius=20, tint_color=(18, 32, 64), tint_alpha=140):
    """Create a frosted glass effect on a region of the image."""
    x0, y0, x1, y1 = bbox
    x0, y0 = max(0, x0), max(0, y0)
    x1, y1 = min(base_img.width, x1), min(base_img.height, y1)

    region = base_img.crop((x0, y0, x1, y1)).convert("RGBA")
    blurred = region.filter(ImageFilter.GaussianBlur(radius=blur_radius))

    tint = Image.new("RGBA", blurred.size, (*tint_color, tint_alpha))
    blurred = Image.alpha_composite(blurred, tint)

    result = base_img.copy()
    result.paste(blurred, (x0, y0))
    return result


def draw_rounded_rect_alpha(draw, bbox, radius, fill):
    """Draw a rounded rectangle with alpha support."""
    draw.rounded_rectangle(bbox, radius=radius, fill=fill)


def draw_text_shadow(draw, pos, text, font, fill=BRAND_WHITE, shadow_alpha=120, offset=2):
    """Draw text with a soft shadow."""
    x, y = pos
    shadow_color = (0, 0, 0, shadow_alpha)
    draw.text((x + offset, y + offset), text, font=font, fill=shadow_color)
    draw.text((x, y), text, font=font, fill=fill)


# ============================================================
# TIER 1: PAID AD CREATIVES — Minimal brand touch
# ============================================================

def build_tier1_fb(photo_path, output_path):
    """Paid Facebook ad — just a tiny frosted brand pill in corner."""
    img = Image.open(photo_path).convert("RGBA")
    W, H = 1200, 628
    img = img.resize((W, H), Image.LANCZOS)

    pill_text = BRAND_SHORT
    font = load_font(14, bold=True)
    text_bbox = font.getbbox(pill_text)
    tw = text_bbox[2] - text_bbox[0]
    th = text_bbox[3] - text_bbox[1]

    pill_w = tw + 24
    pill_h = th + 14
    pill_x = W - pill_w - 16
    pill_y = H - pill_h - 16

    img = frosted_glass_region(img, (pill_x, pill_y, pill_x + pill_w, pill_y + pill_h),
                                blur_radius=12, tint_alpha=120)

    draw = ImageDraw.Draw(img)
    draw_rounded_rect_alpha(draw, (pill_x, pill_y, pill_x + pill_w, pill_y + pill_h),
                            radius=pill_h // 2, fill=(18, 32, 64, 160))
    draw.text((pill_x + 12, pill_y + 6), pill_text, font=font, fill=(255, 255, 255, 220))

    img.convert("RGB").save(output_path, "PNG", quality=95)
    return img


def build_tier1_ig(photo_path, output_path):
    """Paid Instagram ad — tiny frosted brand pill in corner."""
    img = Image.open(photo_path).convert("RGBA")
    S = 1080
    img = img.resize((S, S), Image.LANCZOS)

    pill_text = BRAND_SHORT
    font = load_font(15, bold=True)
    text_bbox = font.getbbox(pill_text)
    tw = text_bbox[2] - text_bbox[0]
    th = text_bbox[3] - text_bbox[1]

    pill_w = tw + 24
    pill_h = th + 14
    pill_x = S - pill_w - 20
    pill_y = S - pill_h - 20

    img = frosted_glass_region(img, (pill_x, pill_y, pill_x + pill_w, pill_y + pill_h),
                                blur_radius=12, tint_alpha=120)

    draw = ImageDraw.Draw(img)
    draw_rounded_rect_alpha(draw, (pill_x, pill_y, pill_x + pill_w, pill_y + pill_h),
                            radius=pill_h // 2, fill=(18, 32, 64, 160))
    draw.text((pill_x + 12, pill_y + 6), pill_text, font=font, fill=(255, 255, 255, 220))

    img.convert("RGB").save(output_path, "PNG", quality=95)
    return img


# ============================================================
# TIER 2: ORGANIC POSTS — Elegant bottom bar + Nate badge
# ============================================================

def build_tier2_fb(photo_path, output_path, headline, sub_line=None):
    """Organic Facebook post — frosted bottom bar with headline + Nate."""
    img = Image.open(photo_path).convert("RGBA")
    W, H = 1200, 628
    img = img.resize((W, H), Image.LANCZOS)

    bar_h = int(H * 0.16)
    bar_y = H - bar_h

    img = frosted_glass_region(img, (0, bar_y, W, H), blur_radius=25, tint_alpha=170)

    draw = ImageDraw.Draw(img)
    draw.rectangle([(0, bar_y), (W, bar_y + 2)], fill=(*BRAND_GOLD, 180))

    nate = get_nate_avatar(size=int(bar_h * 0.70))
    nate_x = 20
    nate_y = bar_y + (bar_h - nate.height) // 2
    img.paste(nate, (nate_x, nate_y), nate)

    text_x = nate_x + nate.width + 16
    font_h = load_font(32, bold=True)
    font_sub = load_font(18, bold=False)
    font_phone = load_font(20, bold=True)

    hl_y = bar_y + 14
    draw_text_shadow(draw, (text_x, hl_y), headline, font_h, BRAND_WHITE, offset=1)

    if sub_line:
        draw_text_shadow(draw, (text_x, hl_y + 40), sub_line, font_sub,
                         (200, 220, 255, 255), shadow_alpha=80, offset=1)

    phone_text = f"Nate: {PHONE}"
    phone_bbox = font_phone.getbbox(phone_text)
    phone_w = phone_bbox[2] - phone_bbox[0]
    draw_text_shadow(draw, (W - phone_w - 20, bar_y + 16), phone_text,
                     font_phone, BRAND_LIGHT_BLUE, offset=1)

    brand_font = load_font(13, bold=True)
    draw.text((W - 220, bar_y + bar_h - 26), BRAND_NAME, font=brand_font,
              fill=(255, 255, 255, 160))

    img.convert("RGB").save(output_path, "PNG", quality=95)
    return img


def build_tier2_ig(photo_path, output_path, headline, sub_line=None):
    """Organic Instagram post — frosted bottom bar with headline + Nate."""
    img = Image.open(photo_path).convert("RGBA")
    S = 1080
    img = img.resize((S, S), Image.LANCZOS)

    bar_h = int(S * 0.17)
    bar_y = S - bar_h

    img = frosted_glass_region(img, (0, bar_y, S, S), blur_radius=25, tint_alpha=170)

    draw = ImageDraw.Draw(img)
    draw.rectangle([(0, bar_y), (S, bar_y + 2)], fill=(*BRAND_GOLD, 180))

    nate = get_nate_avatar(size=int(bar_h * 0.60))
    nate_x = 24
    nate_y = bar_y + 12
    img.paste(nate, (nate_x, nate_y), nate)

    text_x = nate_x + nate.width + 18
    font_h = load_font(34, bold=True)
    font_sub = load_font(20, bold=False)

    hl_y = bar_y + 14
    draw_text_shadow(draw, (text_x, hl_y), headline, font_h, BRAND_WHITE, offset=1)

    if sub_line:
        draw_text_shadow(draw, (text_x, hl_y + 42), sub_line, font_sub,
                         (200, 220, 255, 255), shadow_alpha=80, offset=1)

    font_cta = load_font(18, bold=True)
    cta_text = f"FREE Estimate  |  {PHONE}"
    cta_bbox = font_cta.getbbox(cta_text)
    cta_w = cta_bbox[2] - cta_bbox[0]
    draw.text(((S - cta_w) // 2, bar_y + bar_h - 38), cta_text,
              font=font_cta, fill=(*BRAND_LIGHT_BLUE, 230))

    img.convert("RGB").save(output_path, "PNG", quality=95)
    return img


# ============================================================
# TIER 3: STORIES — Text-forward with gradient overlay
# ============================================================

def build_tier3_story(photo_path, output_path, headline_1, headline_2, sub_line, cta_text):
    """Instagram/Facebook Story — gradient overlay, bold text, Nate badge, CTA."""
    img = Image.open(photo_path).convert("RGBA")
    W, H = 1080, 1920
    img = img.resize((W, H), Image.LANCZOS)

    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw_ov = ImageDraw.Draw(overlay)

    for i in range(H // 3):
        alpha = int(180 * (1 - i / (H // 3)))
        draw_ov.line([(0, i), (W, i)], fill=(18, 32, 64, alpha))

    for i in range(H // 2):
        y = H - 1 - i
        alpha = int(210 * (1 - i / (H // 2)))
        draw_ov.line([(0, y), (W, y)], fill=(18, 32, 64, alpha))

    img = Image.alpha_composite(img, overlay)

    draw = ImageDraw.Draw(img)

    font_h = load_font(68, bold=True, condensed=True)
    font_sub = load_font(30, bold=False)
    font_cta_f = load_font(24, bold=True)
    font_phone = load_font(32, bold=True)
    font_brand = load_font(20, bold=True)

    draw_text_shadow(draw, (50, 100), headline_1, font_h, BRAND_WHITE, offset=3)
    draw_text_shadow(draw, (50, 180), headline_2, font_h, BRAND_WHITE, offset=3)

    y_sub = 280
    for line in sub_line.split("\n"):
        draw_text_shadow(draw, (50, y_sub), line, font_sub,
                         (200, 220, 255, 255), shadow_alpha=100, offset=2)
        y_sub += 40

    cta_bbox = font_cta_f.getbbox(cta_text)
    cta_w = cta_bbox[2] - cta_bbox[0] + 50
    cta_h = 52
    cta_x = (W - cta_w) // 2
    cta_y = H - 380
    draw.rounded_rectangle(
        [(cta_x, cta_y), (cta_x + cta_w, cta_y + cta_h)],
        radius=cta_h // 2, fill=BRAND_BLUE
    )
    draw.text((cta_x + 25, cta_y + 13), cta_text, font=font_cta_f, fill=BRAND_WHITE)

    phone_text = f"Call/Text Nate: {PHONE}"
    phone_bbox = font_phone.getbbox(phone_text)
    px = (W - (phone_bbox[2] - phone_bbox[0])) // 2
    draw_text_shadow(draw, (px, H - 300), phone_text, font_phone, BRAND_LIGHT_BLUE, offset=2)

    nate = get_nate_avatar(size=56)
    brand_text = BRAND_NAME
    brand_font = load_font(18, bold=True)
    brand_bbox = brand_font.getbbox(brand_text)
    brand_w = brand_bbox[2] - brand_bbox[0]

    total_w = nate.width + 10 + brand_w
    start_x = (W - total_w) // 2
    nate_y = H - 220
    img.paste(nate, (start_x, nate_y), nate)
    draw.text((start_x + nate.width + 10, nate_y + 18), brand_text,
              font=brand_font, fill=(255, 255, 255, 200))

    img.convert("RGB").save(output_path, "PNG", quality=95)
    return img


# ============================================================
# AD DEFINITIONS
# ============================================================

FB_ADS = [
    {
        "photo": "v3_fb_01_twilight_glow.png",
        "headline": "Cut Energy Bills Up to 40%",
        "sub": "Triple-Pane Windows at Dual-Pane Prices",
    },
    {
        "photo": "v3_fb_02_morning_kitchen.png",
        "headline": "4.9 Stars  |  1,000+ Reviews",
        "sub": "#3 National Remodeler  •  A+ BBB",
    },
    {
        "photo": "v3_fb_03_spring_porch.png",
        "headline": "Spring Is the Perfect Time",
        "sub": "FREE Estimate + $500 Gift Card",
    },
    {
        "photo": "v3_fb_04_cozy_window_seat.png",
        "headline": "Feel the Difference Inside",
        "sub": "Warmer Winters. Cooler Summers. Zero Drafts.",
    },
    {
        "photo": "v3_fb_05_siding_transformation.png",
        "headline": "Transform Your Home's Look",
        "sub": "Windows  •  Doors  •  Siding  •  Roofing",
    },
]

IG_ADS = [
    {
        "photo": "v3_ig_01_warm_glow.png",
        "headline": "Save Up to 40% on Energy Bills",
        "sub": "Triple-Pane at Dual-Pane Prices",
    },
    {
        "photo": "v3_ig_02_curb_appeal_golden.png",
        "headline": "Your Neighbors Chose Us",
        "sub": "4.9 Stars  •  1,000+ Reviews",
    },
    {
        "photo": "v3_ig_03_bathroom_reveal.png",
        "headline": "One-Day Bathroom Remodels",
        "sub": "Spa-Quality. Installed in a Day.",
    },
    {
        "photo": "v3_ig_04_spring_windows_open.png",
        "headline": "Spring Cleaning Starts Here",
        "sub": "FREE Estimate + $500 Gift Card",
    },
    {
        "photo": "v3_ig_05_detail_craft.png",
        "headline": "America's Triple Pane Company",
        "sub": "52% Better Insulation Than Dual-Pane",
    },
]

IGS_ADS = [
    {
        "photo": "v3_igs_01_dramatic_twilight.png",
        "h1": "FREE ESTIMATE",
        "h2": "+ $500 GIFT CARD",
        "sub": "Triple-Pane Windows\nDual-Pane Prices",
        "cta": "Swipe Up or Call Nate",
    },
    {
        "photo": "v3_igs_02_cozy_vertical.png",
        "h1": "4.9 STARS",
        "h2": "1,000+ REVIEWS",
        "sub": "#3 National Remodeler\nMilwaukee's Most Trusted",
        "cta": "Book Your FREE Estimate",
    },
    {
        "photo": "v3_igs_03_spring_door_vertical.png",
        "h1": "SPRING =",
        "h2": "WINDOW SEASON",
        "sub": "Don't Waste Another Summer\nWith Drafty Windows",
        "cta": "Tap to Book Your FREE Estimate",
    },
]


def main():
    print("=" * 70)
    print("  V3 — MODERN BRANDED OVERLAY GENERATOR")
    print("  Window Depot USA of Milwaukee")
    print("  Philosophy: Minimal, elegant, NO AI people")
    print("=" * 70)

    count = 0
    total = len(FB_ADS) * 2 + len(IG_ADS) * 2 + len(IGS_ADS)

    # Facebook — Tier 1 (Paid) + Tier 2 (Organic)
    print("\n[FB] Building Facebook ads...")
    for i, ad in enumerate(FB_ADS, 1):
        photo_path = os.path.join(OUT_DIR, "facebook", ad["photo"])
        if not os.path.exists(photo_path):
            print(f"  [SKIP] Missing base photo: {photo_path}")
            continue

        paid_path = os.path.join(OUT_DIR, "facebook",
                                  ad["photo"].replace(".png", "_paid.png"))
        organic_path = os.path.join(OUT_DIR, "facebook",
                                     ad["photo"].replace(".png", "_organic.png"))

        print(f"  [{count+1}/{total}] FB Paid #{i}...")
        build_tier1_fb(photo_path, paid_path)
        count += 1

        print(f"  [{count+1}/{total}] FB Organic #{i}...")
        build_tier2_fb(photo_path, organic_path, ad["headline"], ad.get("sub"))
        count += 1

    # Instagram — Tier 1 (Paid) + Tier 2 (Organic)
    print("\n[IG] Building Instagram feed ads...")
    for i, ad in enumerate(IG_ADS, 1):
        photo_path = os.path.join(OUT_DIR, "instagram", ad["photo"])
        if not os.path.exists(photo_path):
            print(f"  [SKIP] Missing base photo: {photo_path}")
            continue

        paid_path = os.path.join(OUT_DIR, "instagram",
                                  ad["photo"].replace(".png", "_paid.png"))
        organic_path = os.path.join(OUT_DIR, "instagram",
                                     ad["photo"].replace(".png", "_organic.png"))

        print(f"  [{count+1}/{total}] IG Paid #{i}...")
        build_tier1_ig(photo_path, paid_path)
        count += 1

        print(f"  [{count+1}/{total}] IG Organic #{i}...")
        build_tier2_ig(photo_path, organic_path, ad["headline"], ad.get("sub"))
        count += 1

    # Instagram Stories — Tier 3 only
    print("\n[IGS] Building Instagram Stories...")
    for i, ad in enumerate(IGS_ADS, 1):
        photo_path = os.path.join(OUT_DIR, "instagram-stories", ad["photo"])
        if not os.path.exists(photo_path):
            print(f"  [SKIP] Missing base photo: {photo_path}")
            continue

        story_path = os.path.join(OUT_DIR, "instagram-stories",
                                   ad["photo"].replace(".png", "_branded.png"))

        print(f"  [{count+1}/{total}] Story #{i}...")
        build_tier3_story(photo_path, story_path, ad["h1"], ad["h2"], ad["sub"], ad["cta"])
        count += 1

    print(f"\n{'=' * 70}")
    print(f"  DONE! Generated {count} branded images")
    print(f"  Output: {OUT_DIR}/")
    print(f"{'=' * 70}")


if __name__ == "__main__":
    main()
