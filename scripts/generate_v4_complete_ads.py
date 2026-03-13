#!/usr/bin/env python3
"""
V4 — COMPLETE-IN-ONE Ad Generator for Window Depot USA Milwaukee

The breakthrough: Stop generating stock photos and overlaying text.
Instead, have Gemini generate the ENTIRE finished ad in one shot —
text, layout, colors, photo elements all composed together by the AI.

Multiple visual styles tested per platform to find what actually works.
"""

import os
import time
from io import BytesIO
from google import genai
from PIL import Image

client = genai.Client(api_key=os.environ.get("Gemini API Key"))
MODEL = "gemini-3.1-flash-image-preview"

OUT_DIR = "/workspace/ad-drafts/v4"

BRAND_CONTEXT = (
    "Brand: Window Depot USA of Milwaukee. "
    "Colors: deep navy blue (#122040) and white, with gold (#D4AF37) accents. "
    "Font style: bold, clean, modern sans-serif. "
    "Tone: warm, trustworthy, premium but approachable. "
)

ADS = [
    # ===== FACEBOOK (1200x628, landscape 16:9) =====
    {
        "id": "v4_fb_01",
        "platform": "facebook",
        "style": "bold_offer",
        "prompt": (
            "Create a high-end social media advertisement image in landscape 16:9 format. "
            "Design a premium home improvement ad with a split layout: "
            "The left 55% has a deep navy blue (#122040) solid background. "
            "On the navy side, display this text in large bold white sans-serif letters: "
            "'SAVE UP TO 40%' as the main headline, and below it in smaller gold (#D4AF37) text: "
            "'on your energy bills'. Below that, in clean white text: "
            "'Triple-Pane Windows at Dual-Pane Prices'. "
            "At the bottom of the navy section, a gold line separator and "
            "'FREE Estimate + $500 Gift Card' in white. "
            "The right 45% shows a beautiful, photorealistic image of a cozy living room "
            "with large modern replacement windows looking out onto a snowy Wisconsin landscape, "
            "warm interior lighting, inviting atmosphere. "
            "The overall design should look like a professionally designed Facebook ad — "
            "clean, modern, premium. No clutter. Strong visual hierarchy. "
            "Absolutely no logos, no company name text, no website URLs."
        ),
    },
    {
        "id": "v4_fb_02",
        "platform": "facebook",
        "style": "photo_headline",
        "prompt": (
            "Create a stunning social media advertisement image in landscape 16:9 format. "
            "A beautiful photorealistic twilight exterior shot of a charming craftsman home "
            "with warm light glowing through every window, wet driveway reflecting the warm light. "
            "Overlaid at the bottom of the image is a semi-transparent dark navy gradient bar "
            "that fades from transparent at top to solid navy at bottom, covering the bottom 30%. "
            "On this gradient bar, large bold white text reads: '4.9 Stars · 1,000+ Reviews' "
            "as the headline. Below in slightly smaller text: "
            "'Milwaukee\\'s Most Trusted Home Remodeler'. "
            "The text should be clean, modern, perfectly legible, and professionally laid out. "
            "The photo is the hero — dramatic, cinematic, scroll-stopping. "
            "The text overlay is subtle but impactful. "
            "No logos, no phone numbers, no URLs, no company name."
        ),
    },
    {
        "id": "v4_fb_03",
        "platform": "facebook",
        "style": "seasonal_bold",
        "prompt": (
            "Create a vibrant social media advertisement image in landscape 16:9 format. "
            "Spring-themed home improvement ad. The background is a beautiful spring scene: "
            "a charming Midwest home with blooming cherry trees, green lawn, blue sky. "
            "Over the image, large bold text in white with dark shadow reads: "
            "'SPRING WINDOW SALE' as the dominant headline — these words should be HUGE "
            "and take up the central portion of the image. "
            "Below the headline in smaller clean white text: "
            "'Free Estimate · $500 Gift Card · Price Locked 12 Months'. "
            "The overall feel is fresh, optimistic, and energetic. "
            "The text should be clean and modern — think Nike or Apple ad quality. "
            "No logos, no phone numbers, no URLs."
        ),
    },
    {
        "id": "v4_fb_04",
        "platform": "facebook",
        "style": "comfort_lifestyle",
        "prompt": (
            "Create a warm, inviting social media advertisement image in landscape 16:9 format. "
            "A photorealistic cozy winter interior scene: beautiful window seat with a thick "
            "throw blanket, a mug of hot coffee, and large crystal-clear triple-pane windows "
            "showing a snowy Wisconsin neighborhood outside. Warm golden interior light. "
            "In the upper left area of the image, text overlaid in large bold white letters "
            "with subtle shadow: 'FEEL THE DIFFERENCE' on one line, and 'INSIDE' on the next. "
            "Below in smaller text: 'Zero drafts. Zero condensation. Total comfort.' "
            "The text should feel organic and integrated with the image, not pasted on. "
            "Premium, editorial quality. Think Dwell Magazine meets Nike advertising. "
            "No logos, no phone numbers, no URLs."
        ),
    },
    {
        "id": "v4_fb_05",
        "platform": "facebook",
        "style": "transformation_bold",
        "prompt": (
            "Create a striking social media advertisement image in landscape 16:9 format. "
            "A dramatic before-and-after concept: the image shows a beautiful renovated "
            "Midwestern colonial home with new windows, fresh siding, and a stunning front door — "
            "all looking pristine at golden hour. "
            "Large bold text overlaid across the top reads: 'TRANSFORM YOUR HOME' "
            "in huge white bold sans-serif letters with a subtle dark shadow for contrast. "
            "Below in smaller gold (#D4AF37) text: 'Windows · Doors · Siding · Roofing'. "
            "The overall design is bold, confident, aspirational. "
            "Think luxury car advertisement applied to home improvement. "
            "No logos, no phone numbers, no URLs, no fine print."
        ),
    },

    # ===== INSTAGRAM (1080x1080, square 1:1) =====
    {
        "id": "v4_ig_01",
        "platform": "instagram",
        "style": "stat_hero",
        "prompt": (
            "Create a bold social media advertisement image in square 1:1 format. "
            "Design a premium, modern ad with a deep navy blue (#122040) background. "
            "In the center, MASSIVE bold white text reads: '40%' — this should be "
            "absolutely enormous, taking up most of the vertical space. "
            "Above the big number in smaller gold (#D4AF37) text: 'SAVE UP TO'. "
            "Below the big number in clean white text: 'On Your Energy Bills'. "
            "At the very bottom, separated by a thin gold line: "
            "'Triple-Pane Windows · Dual-Pane Prices' in small white text. "
            "The design is ultra-clean, minimal, high-impact. Like a Bloomberg "
            "or financial infographic meets luxury brand ad. Just text on solid navy. "
            "No photos, no images, no logos, no illustrations."
        ),
    },
    {
        "id": "v4_ig_02",
        "platform": "instagram",
        "style": "photo_text",
        "prompt": (
            "Create a stunning social media advertisement image in square 1:1 format. "
            "A gorgeous photorealistic interior shot of a bright modern kitchen with "
            "large new casement windows flooding the space with golden morning light. "
            "Through the windows, a beautiful snowy winter scene is visible. "
            "A coffee mug sits on the clean quartz countertop. Warm, inviting. "
            "Across the bottom third of the image, large bold white text with shadow "
            "reads: 'YOUR OLD WINDOWS' on one line, 'ARE COSTING YOU' on the next. "
            "The text is big, bold, and perfectly integrated into the image. "
            "Clean modern sans-serif typography. Professional ad quality. "
            "No logos, no phone numbers, no URLs."
        ),
    },
    {
        "id": "v4_ig_03",
        "platform": "instagram",
        "style": "bathroom_transformation",
        "prompt": (
            "Create a beautiful social media advertisement image in square 1:1 format. "
            "A stunning photorealistic spa-like bathroom remodel: frameless glass walk-in "
            "shower, marble tile walls, matte black rainfall showerhead, floating wood vanity, "
            "and a frosted window letting in soft natural light. Fresh white towels. "
            "In the top portion, overlaid text in bold white letters with subtle shadow: "
            "'BATHROOM REMODEL' as main text, and below in gold (#D4AF37): "
            "'Installed in Just 1 Day'. "
            "The design is clean, premium, aspirational. Spa luxury feel. "
            "No logos, no phone numbers, no URLs."
        ),
    },
    {
        "id": "v4_ig_04",
        "platform": "instagram",
        "style": "social_proof",
        "prompt": (
            "Create a professional social media advertisement image in square 1:1 format. "
            "Clean design on a dark navy (#122040) background. "
            "Five large gold star icons in a row near the top. "
            "Below the stars, large bold white text: '4.9 STARS' on one line. "
            "Below that: '1,000+ REVIEWS' in the same size. "
            "Below that, separated by a thin gold line, in smaller white text: "
            "'#3 Nationally Ranked Remodeler' on one line, and "
            "'A+ BBB Rating' on the next. "
            "At the bottom in gold text: 'Milwaukee\\'s Most Trusted'. "
            "The overall design is minimal, authoritative, and trust-building. "
            "Like an awards ceremony graphic. Clean typography, generous spacing. "
            "No photos, no logos, no illustrations."
        ),
    },
    {
        "id": "v4_ig_05",
        "platform": "instagram",
        "style": "spring_offer",
        "prompt": (
            "Create a fresh, vibrant social media advertisement image in square 1:1 format. "
            "A beautiful photorealistic spring scene: a charming home entrance with blooming "
            "flowers, new fiberglass front door with sidelights, fresh landscaping. "
            "Pink cherry blossoms, green grass, soft spring light. "
            "Overlaid across the center in large bold white text with dark shadow: "
            "'SPRING SPECIAL' as the dominant headline. "
            "Below in clean white text: 'FREE Estimate + $500 Gift Card'. "
            "The design feels fresh, optimistic, and premium. "
            "Not cluttered — just the photo, the headline, and the offer. "
            "No logos, no phone numbers, no URLs."
        ),
    },

    # ===== INSTAGRAM STORIES (1080x1920, vertical 9:16) =====
    {
        "id": "v4_igs_01",
        "platform": "instagram-stories",
        "style": "offer_vertical",
        "prompt": (
            "Create a striking vertical social media story advertisement in 9:16 portrait format. "
            "A dramatic twilight photo of a beautiful home with warm light glowing through "
            "every window as the background — cinematic and atmospheric. "
            "Over the image, large bold text fills the top third: "
            "'FREE ESTIMATE' in huge white bold letters, and below it "
            "'+ $500 GIFT CARD' in gold (#D4AF37) letters. "
            "In the middle of the image, smaller white text: "
            "'Triple-Pane Windows at Dual-Pane Prices'. "
            "Near the bottom, a rounded blue (#1E50A0) button with white text: "
            "'TAP TO BOOK NOW'. "
            "The overall feel is dramatic, premium, and urgent without being pushy. "
            "Cinematic photography with bold modern typography. "
            "No logos, no phone numbers, no URLs."
        ),
    },
    {
        "id": "v4_igs_02",
        "platform": "instagram-stories",
        "style": "trust_vertical",
        "prompt": (
            "Create a professional vertical social media story advertisement in 9:16 portrait format. "
            "Deep navy blue (#122040) solid background — no photo. "
            "Five large gold star icons centered near the top. "
            "Below the stars: '4.9' in MASSIVE white bold text — this number should be "
            "extremely large and impactful. "
            "Below: 'STARS ON GOOGLE' in medium white text. "
            "Below: '1,000+ Happy Customers' in smaller gold text. "
            "A thin gold divider line. "
            "Below: '#3 National Remodeler' and 'A+ BBB Rating' in small white text. "
            "Near the bottom: a rounded blue (#1E50A0) button with 'BOOK FREE ESTIMATE'. "
            "Ultra-clean, minimal, authoritative design. Premium feel. "
            "No photos, no logos, no illustrations."
        ),
    },
    {
        "id": "v4_igs_03",
        "platform": "instagram-stories",
        "style": "spring_vertical",
        "prompt": (
            "Create a beautiful vertical social media story advertisement in 9:16 portrait format. "
            "A gorgeous spring photo of a charming home entrance with blooming flowers, "
            "beautiful new front door, fresh landscaping — shot from the walkway looking "
            "toward the door. Bright, fresh, optimistic spring atmosphere. "
            "In the top portion, large bold white text with shadow: "
            "'SPRING' on one line, '= WINDOW' on the next, 'SEASON' on the next. "
            "The text is big and bold. In the lower portion, smaller white text: "
            "'Don\\'t waste another summer with drafty windows'. "
            "Near the bottom, a rounded gold (#D4AF37) button with dark text: "
            "'GET YOUR FREE ESTIMATE'. "
            "Fresh, bright, energetic design. "
            "No logos, no phone numbers, no URLs."
        ),
    },
]


def generate_ad(ad_data, retries=3):
    """Generate a complete ad in one Gemini call."""
    platform = ad_data["platform"]
    out_dir = os.path.join(OUT_DIR, platform)
    os.makedirs(out_dir, exist_ok=True)
    filepath = os.path.join(out_dir, f"{ad_data['id']}_{ad_data['style']}.png")

    if os.path.exists(filepath):
        print(f"  [SKIP] {filepath}")
        return True

    full_prompt = BRAND_CONTEXT + ad_data["prompt"]

    for attempt in range(retries + 1):
        try:
            print(f"  [GEN] {ad_data['id']} — {ad_data['style']} (attempt {attempt+1})...")
            response = client.models.generate_content(
                model=MODEL,
                contents=full_prompt,
            )

            for part in response.candidates[0].content.parts:
                if part.inline_data is not None:
                    image = Image.open(BytesIO(part.inline_data.data))
                    image.save(filepath, "PNG")
                    print(f"  [OK]  {filepath} ({image.size[0]}x{image.size[1]})")
                    return True

            print(f"  [WARN] No image in response")
            if attempt < retries:
                time.sleep(4)

        except Exception as e:
            print(f"  [ERR] {e}")
            if attempt < retries:
                time.sleep(6)

    return False


def main():
    print("=" * 70)
    print("  V4 — COMPLETE-IN-ONE AD GENERATOR")
    print("  Window Depot USA of Milwaukee")
    print("  Gemini generates the ENTIRE finished ad — text + design + photo")
    print("=" * 70)

    total = len(ADS)
    print(f"\n  Generating {total} complete ads...\n")

    results = {"success": [], "failed": []}
    for i, ad in enumerate(ADS, 1):
        print(f"[{i}/{total}] {ad['platform'].upper()} — {ad['style']}")
        ok = generate_ad(ad)
        results["success" if ok else "failed"].append(ad["id"])
        if i < total:
            time.sleep(3)

    print(f"\n{'=' * 70}")
    print(f"  RESULTS: {len(results['success'])} succeeded, {len(results['failed'])} failed")
    if results["failed"]:
        print(f"  Failed: {', '.join(results['failed'])}")
    print(f"{'=' * 70}")


if __name__ == "__main__":
    main()
