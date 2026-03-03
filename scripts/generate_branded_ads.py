#!/usr/bin/env python3
"""
KING MODE — Window Depot USA Milwaukee Branded Ad Generator
Generates branded Facebook + Instagram ad images with:
  - Nate cutout composited in
  - Window Depot USA of Milwaukee branding
  - CTAs, phone number, headlines
  - Navy blue / white brand color scheme
"""

import os
import time
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from google import genai

client = genai.Client(api_key=os.environ.get("Gemini API Key"))
MODEL = "gemini-3.1-flash-image-preview"

BRAND_NAVY = (18, 32, 64)
BRAND_NAVY_RGB = (18, 32, 64)
BRAND_BLUE = (30, 80, 160)
BRAND_LIGHT_BLUE = (100, 160, 220)
BRAND_WHITE = (255, 255, 255)
BRAND_GOLD = (218, 165, 32)
BRAND_RED_CTA = (200, 35, 35)

PHONE = "(414) 312-5213"
BRAND_LINE = "Window Depot USA of Milwaukee"

FONT_BOLD_PATH = "/usr/share/fonts/truetype/macos/Helvetica.ttc"
FONT_COND_PATH = "/usr/share/fonts/truetype/macos/Helvetica.ttc"

OUT_DIR = "/workspace/ad-drafts"
NATE_DIR = "/workspace/brand-assets"


def load_font(size, bold=True, condensed=False):
    try:
        if condensed:
            return ImageFont.truetype(FONT_COND_PATH, size, index=10)
        elif bold:
            return ImageFont.truetype(FONT_BOLD_PATH, size, index=1)
        else:
            return ImageFont.truetype(FONT_BOLD_PATH, size, index=0)
    except Exception:
        try:
            return ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", size)
        except Exception:
            return ImageFont.load_default()


def generate_nate_cutouts():
    """Generate Nate cutout images using Nano Banana 2 with reference-style description."""
    nate_prompts = {
        "nate_pointing_right": (
            "Professional photograph of a confident, friendly Italian-American man in his mid-40s, "
            "short dark hair with some gray, light stubble beard, athletic build, big genuine smile showing teeth, "
            "wearing a navy blue collared polo shirt with a small white company logo on the chest. "
            "He is pointing with his right thumb to the right side, like presenting something. "
            "Standing pose, photographed from waist up. Clean white background for easy cutout. "
            "Professional headshot/marketing photo style, warm and approachable."
        ),
        "nate_arms_crossed": (
            "Professional photograph of a confident, friendly Italian-American man in his mid-40s, "
            "short dark hair with some gray, light stubble beard, athletic build, big genuine smile showing teeth, "
            "wearing a navy blue collared polo shirt with a small white company logo on the chest. "
            "Arms crossed confidently in front of chest. Standing pose, waist up. "
            "Clean white background. Professional marketing photo style, trustworthy and approachable."
        ),
        "nate_thumbs_up": (
            "Professional photograph of a confident, friendly Italian-American man in his mid-40s, "
            "short dark hair with some gray, light stubble beard, athletic build, big genuine smile showing teeth, "
            "wearing a navy blue collared polo shirt with a small white company logo on the chest. "
            "Giving a thumbs up with his right hand. Standing pose, waist up. "
            "Clean white background. Professional marketing photo, warm and genuine."
        ),
    }

    results = {}
    for key, prompt in nate_prompts.items():
        filepath = os.path.join(NATE_DIR, f"{key}.png")
        if os.path.exists(filepath):
            print(f"  [SKIP] {key} exists")
            results[key] = Image.open(filepath).convert("RGBA")
            continue

        for attempt in range(3):
            try:
                print(f"  [GEN] {key} (attempt {attempt+1})...")
                response = client.models.generate_content(model=MODEL, contents=prompt)
                for part in response.candidates[0].content.parts:
                    if part.inline_data is not None:
                        img = Image.open(BytesIO(part.inline_data.data)).convert("RGBA")
                        img.save(filepath, "PNG")
                        print(f"  [OK]  {key}: {img.size}")
                        results[key] = img
                        break
                if key in results:
                    break
            except Exception as e:
                print(f"  [ERR] {key}: {e}")
                time.sleep(3)
        time.sleep(2)

    return results


def remove_white_bg(img, threshold=230):
    """Remove white/near-white background from an image."""
    img = img.convert("RGBA")
    data = img.getdata()
    new_data = []
    for item in data:
        if item[0] > threshold and item[1] > threshold and item[2] > threshold:
            new_data.append((255, 255, 255, 0))
        else:
            new_data.append(item)
    img.putdata(new_data)
    return img


def try_rembg(img):
    """Try using rembg for professional background removal."""
    try:
        from rembg import remove
        img_bytes = BytesIO()
        img.convert("RGB").save(img_bytes, format="PNG")
        img_bytes.seek(0)
        result_bytes = remove(img_bytes.read())
        return Image.open(BytesIO(result_bytes)).convert("RGBA")
    except Exception as e:
        print(f"  [WARN] rembg failed: {e}, falling back to threshold removal")
        return remove_white_bg(img)


def draw_text_with_shadow(draw, pos, text, font, fill=BRAND_WHITE, shadow_color=(0, 0, 0, 160), offset=2):
    x, y = pos
    draw.text((x + offset, y + offset), text, font=font, fill=shadow_color)
    draw.text((x, y), text, font=font, fill=fill)


def draw_rounded_rect(draw, bbox, radius, fill):
    x0, y0, x1, y1 = bbox
    draw.rounded_rectangle(bbox, radius=radius, fill=fill)


def draw_gradient_rect(img, bbox, color_top, color_bottom):
    x0, y0, x1, y1 = bbox
    overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    height = y1 - y0
    for i in range(height):
        ratio = i / max(height - 1, 1)
        r = int(color_top[0] + (color_bottom[0] - color_top[0]) * ratio)
        g = int(color_top[1] + (color_bottom[1] - color_top[1]) * ratio)
        b = int(color_top[2] + (color_bottom[2] - color_top[2]) * ratio)
        a = int(color_top[3] + (color_bottom[3] - color_top[3]) * ratio)
        draw.line([(x0, y0 + i), (x1, y0 + i)], fill=(r, g, b, a))
    return Image.alpha_composite(img, overlay)


# ============================================================
# FACEBOOK AD TEMPLATES
# ============================================================

FB_ADS = [
    {
        "id": "fb_01",
        "bg": "ad-drafts/facebook/fb_01_energy_savings.png",
        "headline_1": "CUT YOUR ENERGY",
        "headline_2": "BILLS UP TO 40%",
        "bullets": [
            "Triple-Pane at Dual-Pane Prices",
            "FREE In-Home Estimate",
            "$500 Gift Card Included",
        ],
        "cta": "Book Your FREE 1-Year Estimate with Nate",
        "nate_key": "nate_pointing_right",
        "nate_position": "right",
    },
    {
        "id": "fb_02",
        "bg": "ad-drafts/facebook/fb_02_trust_reviews.png",
        "headline_1": "4.9 STARS",
        "headline_2": "1,000+ REVIEWS",
        "bullets": [
            "#3 National Remodeler",
            "A+ BBB Rating",
            "Milwaukee & Surrounding Areas",
        ],
        "cta": "Book Your FREE Estimate with Nate",
        "nate_key": "nate_arms_crossed",
        "nate_position": "right",
    },
    {
        "id": "fb_03",
        "bg": "ad-drafts/facebook/fb_03_spring_seasonal.png",
        "headline_1": "SPRING IS HERE",
        "headline_2": "UPGRADE YOUR WINDOWS",
        "bullets": [
            "Free In-Home Estimate",
            "Price Locked for a Full Year",
            "$500 Gift Card with Every Estimate",
        ],
        "cta": "Schedule Your FREE Estimate Today",
        "nate_key": "nate_thumbs_up",
        "nate_position": "right",
    },
    {
        "id": "fb_04",
        "bg": "ad-drafts/facebook/fb_04_comfort.png",
        "headline_1": "FEEL THE",
        "headline_2": "DIFFERENCE INSIDE",
        "bullets": [
            "No More Drafts or Cold Spots",
            "Custom-Made for Your Home",
            "Warmer Winters, Cooler Summers",
        ],
        "cta": "Book Your FREE 1-Year Estimate with Nate",
        "nate_key": "nate_pointing_right",
        "nate_position": "right",
    },
    {
        "id": "fb_05",
        "bg": "ad-drafts/facebook/fb_05_curb_appeal.png",
        "headline_1": "TRANSFORM YOUR",
        "headline_2": "HOME'S CURB APPEAL",
        "bullets": [
            "ProVia Products - #1 in Quality",
            "7 Showrooms Across SE Wisconsin",
            "Windows, Doors, Siding & More",
        ],
        "cta": "Book Your FREE Consultation with Nate",
        "nate_key": "nate_arms_crossed",
        "nate_position": "right",
    },
]

IG_ADS = [
    {
        "id": "ig_01",
        "bg": "ad-drafts/instagram/ig_01_energy_savings.png",
        "headline_1": "SAVE UP TO 40%",
        "headline_2": "ON ENERGY BILLS",
        "sub": "Triple-Pane Windows\nat Dual-Pane Prices",
        "cta": "FREE Estimate + $500 Gift Card",
        "nate_key": "nate_pointing_right",
    },
    {
        "id": "ig_02",
        "bg": "ad-drafts/instagram/ig_02_transformation.png",
        "headline_1": "THE TRANSFORMATION",
        "headline_2": "IS REAL",
        "sub": "New Windows. New Siding.\nNew Home.",
        "cta": "Book Your FREE Estimate Today",
        "nate_key": None,
    },
    {
        "id": "ig_03",
        "bg": "ad-drafts/instagram/ig_03_family_trust.png",
        "headline_1": "YOUR NEIGHBOR,",
        "headline_2": "NOT A CORPORATION",
        "sub": "Family-Owned. Local Service.\n4.9 Stars. 1,000+ Reviews.",
        "cta": "Call or Text Nate: (414) 312-5213",
        "nate_key": None,
    },
    {
        "id": "ig_04",
        "bg": "ad-drafts/instagram/ig_04_spring.png",
        "headline_1": "SPRING CLEANING?",
        "headline_2": "START WITH YOUR WINDOWS",
        "sub": "Free Estimate\nPrice Locked 12 Months",
        "cta": "FREE Estimate + $500 Gift Card",
        "nate_key": "nate_thumbs_up",
    },
    {
        "id": "ig_05",
        "bg": "ad-drafts/instagram/ig_05_product_showcase.png",
        "headline_1": "AMERICA'S TRIPLE",
        "headline_2": "PANE COMPANY",
        "sub": "52% Better Insulation\nSuperior Sound Reduction",
        "cta": "Book Your FREE Estimate with Nate",
        "nate_key": None,
    },
]

IGS_ADS = [
    {
        "id": "igs_01",
        "bg": "ad-drafts/instagram-stories/igs_01_cta.png",
        "headline_1": "FREE ESTIMATE",
        "headline_2": "+ $500 GIFT CARD",
        "sub": "Triple-Pane Windows\nDual-Pane Prices",
        "cta": "Swipe Up or Call Nate",
        "phone": True,
        "nate_key": "nate_pointing_right",
    },
    {
        "id": "igs_02",
        "bg": "ad-drafts/instagram-stories/igs_02_reviews.png",
        "headline_1": "4.9 STARS",
        "headline_2": "1,000+ REVIEWS",
        "sub": "#3 National Remodeler\nMilwaukee's Most Trusted",
        "cta": "Book Your FREE Estimate",
        "phone": True,
        "nate_key": "nate_arms_crossed",
    },
    {
        "id": "igs_03",
        "bg": "ad-drafts/instagram-stories/igs_03_seasonal.png",
        "headline_1": "SPRING =",
        "headline_2": "WINDOW SEASON",
        "sub": "Don't Waste Another Summer\nwith Drafty Windows",
        "cta": "FREE Estimate - Price Locked 12 Months",
        "phone": True,
        "nate_key": "nate_thumbs_up",
    },
]


def build_fb_ad(ad_data, nate_images):
    """Build a branded Facebook ad image."""
    bg = Image.open(os.path.join("/workspace", ad_data["bg"])).convert("RGBA")
    W, H = 1200, 628
    bg = bg.resize((W, H), Image.LANCZOS)

    canvas = bg.copy()

    # Dark overlay on the left 60% for text readability
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw_ov = ImageDraw.Draw(overlay)
    draw_ov.rectangle([(0, 0), (W * 6 // 10, H)], fill=(18, 32, 64, 190))
    canvas = Image.alpha_composite(canvas, overlay)

    # Top gradient bar
    canvas = draw_gradient_rect(canvas, (0, 0, W, 70),
                                (30, 80, 160, 240), (18, 32, 64, 240))

    # Bottom bar
    bottom_bar = Image.new("RGBA", (W, 80), (0, 0, 0, 0))
    draw_bb = ImageDraw.Draw(bottom_bar)
    draw_bb.rectangle([(0, 0), (W, 80)], fill=(18, 32, 64, 245))
    canvas.paste(Image.alpha_composite(
        Image.new("RGBA", (W, 80), (0, 0, 0, 0)), bottom_bar
    ), (0, H - 80), bottom_bar)

    draw = ImageDraw.Draw(canvas)

    # Headline
    font_h1 = load_font(52, bold=True)
    font_h2 = load_font(52, bold=True)
    font_bullet = load_font(22, bold=False)
    font_brand = load_font(18, bold=True)
    font_cta = load_font(20, bold=True)
    font_phone = load_font(24, bold=True)

    y = 85
    draw_text_with_shadow(draw, (35, y), ad_data["headline_1"], font_h1, BRAND_WHITE)
    y += 58
    draw_text_with_shadow(draw, (35, y), ad_data["headline_2"], font_h2, BRAND_WHITE)
    y += 75

    # Bullets
    for bullet in ad_data["bullets"]:
        draw_text_with_shadow(draw, (45, y), f"\u2022  {bullet}", font_bullet, BRAND_WHITE, offset=1)
        y += 34

    # Phone number
    y += 15
    draw_text_with_shadow(draw, (35, y), f"Call/Text Nate: {PHONE}", font_phone, (100, 200, 255, 255), offset=1)

    # Bottom bar content
    draw.text((25, H - 60), BRAND_LINE, font=load_font(20, bold=True), fill=BRAND_WHITE)

    # CTA button
    cta_font = load_font(16, bold=True)
    cta_text = ad_data["cta"]
    cta_bbox = draw.textbbox((0, 0), cta_text, font=cta_font)
    cta_w = cta_bbox[2] - cta_bbox[0] + 30
    cta_h = 36
    cta_x = W - cta_w - 20
    cta_y = H - 58
    draw.rounded_rectangle([(cta_x, cta_y), (cta_x + cta_w, cta_y + cta_h)],
                           radius=4, fill=(30, 80, 160))
    draw.text((cta_x + 15, cta_y + 8), cta_text, font=cta_font, fill=BRAND_WHITE)

    # Nate cutout on the right
    nate_key = ad_data.get("nate_key")
    if nate_key and nate_key in nate_images:
        nate = nate_images[nate_key].copy()
        nate_h = int(H * 0.82)
        nate_w = int(nate.width * (nate_h / nate.height))
        nate = nate.resize((nate_w, nate_h), Image.LANCZOS)
        nate_x = W - nate_w + nate_w // 8
        nate_y = H - 80 - nate_h
        canvas.paste(nate, (nate_x, nate_y), nate)

    return canvas.convert("RGB")


def build_ig_ad(ad_data, nate_images):
    """Build a branded Instagram feed ad image."""
    bg = Image.open(os.path.join("/workspace", ad_data["bg"])).convert("RGBA")
    S = 1080
    bg = bg.resize((S, S), Image.LANCZOS)
    canvas = bg.copy()

    # Top overlay for headline
    canvas = draw_gradient_rect(canvas, (0, 0, S, 260),
                                (18, 32, 64, 230), (18, 32, 64, 50))

    # Bottom overlay for CTA + branding
    canvas = draw_gradient_rect(canvas, (0, S - 200, S, S),
                                (18, 32, 64, 50), (18, 32, 64, 235))

    draw = ImageDraw.Draw(canvas)

    font_h = load_font(50, bold=True)
    font_sub = load_font(24, bold=False)
    font_cta = load_font(22, bold=True)
    font_brand = load_font(18, bold=True)
    font_phone = load_font(20, bold=True)

    # Headline
    draw_text_with_shadow(draw, (30, 30), ad_data["headline_1"], font_h, BRAND_WHITE, offset=2)
    draw_text_with_shadow(draw, (30, 85), ad_data["headline_2"], font_h, BRAND_WHITE, offset=2)

    # Subtitle
    if ad_data.get("sub"):
        y = 150
        for line in ad_data["sub"].split("\n"):
            draw_text_with_shadow(draw, (30, y), line, font_sub, (200, 220, 255, 255), offset=1)
            y += 30

    # Bottom area
    # CTA button
    cta_text = ad_data["cta"]
    cta_bbox = draw.textbbox((0, 0), cta_text, font=font_cta)
    cta_w = cta_bbox[2] - cta_bbox[0] + 40
    cta_h = 42
    cta_x = (S - cta_w) // 2
    cta_y = S - 140
    draw.rounded_rectangle([(cta_x, cta_y), (cta_x + cta_w, cta_y + cta_h)],
                           radius=6, fill=(30, 80, 160))
    draw.text((cta_x + 20, cta_y + 10), cta_text, font=font_cta, fill=BRAND_WHITE)

    # Brand line + phone
    draw.text((30, S - 82), BRAND_LINE, font=font_brand, fill=BRAND_WHITE)
    phone_bbox = draw.textbbox((0, 0), PHONE, font=font_phone)
    draw.text((S - (phone_bbox[2] - phone_bbox[0]) - 30, S - 80), PHONE,
              font=font_phone, fill=(100, 200, 255, 255))

    # Nate (smaller, bottom-right area, only on select posts)
    nate_key = ad_data.get("nate_key")
    if nate_key and nate_key in nate_images:
        nate = nate_images[nate_key].copy()
        nate_h = int(S * 0.45)
        nate_w = int(nate.width * (nate_h / nate.height))
        nate = nate.resize((nate_w, nate_h), Image.LANCZOS)
        nate_x = S - nate_w + nate_w // 8
        nate_y = S - 200 - nate_h + 40
        canvas.paste(nate, (nate_x, nate_y), nate)

    return canvas.convert("RGB")


def build_igs_ad(ad_data, nate_images):
    """Build a branded Instagram Stories ad image."""
    bg = Image.open(os.path.join("/workspace", ad_data["bg"])).convert("RGBA")
    W, H = 1080, 1920
    bg = bg.resize((W, H), Image.LANCZOS)
    canvas = bg.copy()

    # Top overlay
    canvas = draw_gradient_rect(canvas, (0, 0, W, 480),
                                (18, 32, 64, 230), (18, 32, 64, 20))

    # Bottom overlay
    canvas = draw_gradient_rect(canvas, (0, H - 550, W, H),
                                (18, 32, 64, 20), (18, 32, 64, 240))

    draw = ImageDraw.Draw(canvas)

    font_h = load_font(64, bold=True)
    font_sub = load_font(30, bold=False)
    font_cta = load_font(26, bold=True)
    font_brand = load_font(22, bold=True)
    font_phone = load_font(34, bold=True)

    # Headline
    draw_text_with_shadow(draw, (40, 80), ad_data["headline_1"], font_h, BRAND_WHITE, offset=3)
    draw_text_with_shadow(draw, (40, 155), ad_data["headline_2"], font_h, BRAND_WHITE, offset=3)

    # Subtitle
    if ad_data.get("sub"):
        y = 260
        for line in ad_data["sub"].split("\n"):
            draw_text_with_shadow(draw, (40, y), line, font_sub, (200, 220, 255, 255), offset=2)
            y += 40

    # Bottom area
    # CTA button
    cta_text = ad_data["cta"]
    cta_bbox = draw.textbbox((0, 0), cta_text, font=font_cta)
    cta_w = min(cta_bbox[2] - cta_bbox[0] + 60, W - 80)
    cta_h = 54
    cta_x = (W - cta_w) // 2
    cta_y = H - 350
    draw.rounded_rectangle([(cta_x, cta_y), (cta_x + cta_w, cta_y + cta_h)],
                           radius=8, fill=(30, 80, 160))
    draw.text((cta_x + 30, cta_y + 13), cta_text, font=font_cta, fill=BRAND_WHITE)

    # Phone
    if ad_data.get("phone"):
        phone_text = f"Call/Text Nate: {PHONE}"
        phone_bbox = draw.textbbox((0, 0), phone_text, font=font_phone)
        px = (W - (phone_bbox[2] - phone_bbox[0])) // 2
        draw_text_with_shadow(draw, (px, H - 270), phone_text, font_phone,
                              (100, 200, 255, 255), offset=2)

    # Brand
    brand_bbox = draw.textbbox((0, 0), BRAND_LINE, font=font_brand)
    bx = (W - (brand_bbox[2] - brand_bbox[0])) // 2
    draw.text((bx, H - 200), BRAND_LINE, font=font_brand, fill=BRAND_WHITE)

    # Nate
    nate_key = ad_data.get("nate_key")
    if nate_key and nate_key in nate_images:
        nate = nate_images[nate_key].copy()
        nate_h = int(H * 0.35)
        nate_w = int(nate.width * (nate_h / nate.height))
        nate = nate.resize((nate_w, nate_h), Image.LANCZOS)
        nate_x = W - nate_w + nate_w // 6
        nate_y = H // 2 - nate_h // 4
        canvas.paste(nate, (nate_x, nate_y), nate)

    return canvas.convert("RGB")


def main():
    print("=" * 60)
    print("KING MODE — BRANDED AD GENERATOR")
    print("Window Depot USA of Milwaukee")
    print("=" * 60)

    # Step 1: Generate Nate cutouts
    print("\n[1/4] Generating Nate cutout images...")
    nate_raw = generate_nate_cutouts()

    # Step 2: Remove backgrounds
    print("\n[2/4] Removing backgrounds from Nate images...")
    nate_images = {}
    for key, img in nate_raw.items():
        print(f"  Processing {key}...")
        nate_images[key] = try_rembg(img)
        cutout_path = os.path.join(NATE_DIR, f"{key}_cutout.png")
        nate_images[key].save(cutout_path, "PNG")
        print(f"  [OK] Saved cutout: {cutout_path}")

    # Step 3: Build all branded ads
    print("\n[3/4] Building branded Facebook ads...")
    for ad in FB_ADS:
        print(f"  Building {ad['id']}...")
        img = build_fb_ad(ad, nate_images)
        path = os.path.join(OUT_DIR, "facebook", f"{ad['id']}_branded.png")
        img.save(path, "PNG", quality=95)
        print(f"  [OK] {path}")

    print("\n[3/4] Building branded Instagram feed ads...")
    for ad in IG_ADS:
        print(f"  Building {ad['id']}...")
        img = build_ig_ad(ad, nate_images)
        path = os.path.join(OUT_DIR, "instagram", f"{ad['id']}_branded.png")
        img.save(path, "PNG", quality=95)
        print(f"  [OK] {path}")

    print("\n[3/4] Building branded Instagram Stories ads...")
    for ad in IGS_ADS:
        print(f"  Building {ad['id']}...")
        img = build_igs_ad(ad, nate_images)
        path = os.path.join(OUT_DIR, "instagram-stories", f"{ad['id']}_branded.png")
        img.save(path, "PNG", quality=95)
        print(f"  [OK] {path}")

    print("\n[4/4] DONE!")
    print("=" * 60)
    print(f"Generated: 5 FB + 5 IG + 3 Stories = 13 branded ads")
    print(f"Output: {OUT_DIR}/")
    print("=" * 60)


if __name__ == "__main__":
    main()
