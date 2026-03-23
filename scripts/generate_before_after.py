#!/usr/bin/env python3
"""
Generate before/after photos for the Window Depot USA landing page.
Uses Nano Banana 2 (Gemini 3.1 Flash Image) to create matched pairs
of before (old/worn) and after (renovated) home improvement photos.
"""

import os
import time
from io import BytesIO
from google import genai
from PIL import Image

client = genai.Client(api_key=os.environ.get("Gemini API Key"))
MODEL = "gemini-3.1-flash-image-preview"

OUT_DIR = "/workspace/before-after"

PHOTO_PAIRS = [
    {
        "id": "01_windows",
        "before_prompt": (
            "Professional real estate photograph of the front exterior of a classic "
            "two-story colonial-style home in Waukesha, Wisconsin. The house has clearly "
            "old, worn, outdated single-pane windows with visible deterioration — peeling "
            "paint around window frames, foggy glass, some condensation between panes, "
            "and dated aluminum storm windows. The siding and roof look okay but the windows "
            "are the obvious weak point. Overcast day, slightly dreary feel. The home is "
            "a typical Midwest suburban house with a front lawn. Landscape orientation 16:10 "
            "aspect ratio. Realistic, documentary-style photography. No text overlays, no watermarks."
        ),
        "after_prompt": (
            "Professional real estate photograph of the front exterior of a classic "
            "two-story colonial-style home in Waukesha, Wisconsin, freshly renovated with "
            "brand new modern white vinyl replacement windows — crisp, clean triple-pane "
            "windows with beautiful grille patterns. The window frames are pristine white "
            "and perfectly installed. The same style of colonial home but now looking sharp "
            "and well-maintained. Beautiful sunny day, green lawn, blue sky. The new windows "
            "dramatically improve the curb appeal. Landscape orientation 16:10 aspect ratio. "
            "Professional real estate photography, warm and inviting. No text overlays, no watermarks."
        ),
    },
    {
        "id": "02_siding",
        "before_prompt": (
            "Professional real estate photograph of the front exterior of a ranch-style "
            "suburban home in New Berlin, Wisconsin. The house has old, faded, damaged vinyl "
            "siding — some pieces are cracked, warped, discolored, and showing their age. "
            "The color is an uneven, washed-out beige/tan. Some areas show dirt stains and "
            "algae growth. The overall look is tired and dated but the home structure is solid. "
            "Overcast lighting, autumn feel with some bare trees. A typical 1970s-1980s "
            "Midwest suburban ranch home needing siding replacement. Landscape orientation "
            "16:10 aspect ratio. Realistic photography. No text overlays, no watermarks."
        ),
        "after_prompt": (
            "Professional real estate photograph of the front exterior of a ranch-style "
            "suburban home in New Berlin, Wisconsin, with brand new CraneBoard solid core "
            "vinyl siding installed. The new siding is a beautiful rich gray/slate color, "
            "perfectly straight and uniform. The home looks completely transformed — clean, "
            "modern, and well-maintained. New trim and fascia complement the siding. Bright "
            "sunny day with blue sky and green lawn. Beautiful curb appeal. The same ranch "
            "style home but looking brand new. Landscape orientation 16:10 aspect ratio. "
            "Professional real estate photography, aspirational. No text overlays, no watermarks."
        ),
    },
    {
        "id": "03_door",
        "before_prompt": (
            "Professional real estate photograph focused on the front entry of a suburban "
            "home in Menomonee Falls, Wisconsin. The front door is old, weathered, and dated "
            "— a worn wooden door with peeling paint/finish, tarnished old hardware, a small "
            "single-pane window that looks foggy, and dated sidelights. The entry area shows "
            "its age with worn trim and a basic concrete step. The overall impression is tired "
            "and unwelcoming. Close-up view of the entry area. Landscape orientation 16:10 "
            "aspect ratio. Realistic documentary-style photography. No text overlays, no watermarks."
        ),
        "after_prompt": (
            "Professional real estate photograph focused on the front entry of a suburban "
            "home in Menomonee Falls, Wisconsin with a stunning new ProVia Signet fiberglass "
            "entry door installed. The new door is a rich dark wood-grain finish with elegant "
            "decorative glass sidelights and a transom window above. Beautiful new brushed "
            "nickel hardware. The entry area has fresh white trim and a welcoming feel. "
            "A potted plant on the step adds charm. Warm golden hour lighting makes the entry "
            "glow. The transformation is dramatic — from dated to elegant. Landscape orientation "
            "16:10 aspect ratio. Professional real estate photography. No text overlays, no watermarks."
        ),
    },
]


def generate_image(name, prompt, retries=3):
    filepath = os.path.join(OUT_DIR, f"{name}.png")
    if os.path.exists(filepath):
        print(f"  [SKIP] {filepath} already exists")
        return True

    for attempt in range(retries):
        try:
            print(f"  [GEN] {name} (attempt {attempt + 1}/{retries})...")
            response = client.models.generate_content(
                model=MODEL,
                contents=prompt,
            )

            for part in response.candidates[0].content.parts:
                if part.inline_data is not None:
                    image = Image.open(BytesIO(part.inline_data.data))
                    image.save(filepath, "PNG")
                    print(f"  [OK]  Saved: {filepath} ({image.size[0]}x{image.size[1]})")
                    return True

            print(f"  [WARN] No image data in response for {name}")
            if attempt < retries - 1:
                time.sleep(4)

        except Exception as e:
            print(f"  [ERR] {name}: {e}")
            if attempt < retries - 1:
                time.sleep(6)

    return False


def main():
    print("=" * 60)
    print("WINDOW DEPOT USA — BEFORE/AFTER PHOTO GENERATOR")
    print("Using Nano Banana 2 (Gemini 3.1 Flash Image)")
    print("=" * 60)

    os.makedirs(OUT_DIR, exist_ok=True)

    results = {"success": [], "failed": []}

    for pair in PHOTO_PAIRS:
        pair_id = pair["id"]
        print(f"\n--- Generating pair: {pair_id} ---")

        before_name = f"{pair_id}_before"
        ok = generate_image(before_name, pair["before_prompt"])
        if ok:
            results["success"].append(before_name)
        else:
            results["failed"].append(before_name)
        time.sleep(3)

        after_name = f"{pair_id}_after"
        ok = generate_image(after_name, pair["after_prompt"])
        if ok:
            results["success"].append(after_name)
        else:
            results["failed"].append(after_name)
        time.sleep(3)

    print("\n" + "=" * 60)
    print(f"RESULTS: {len(results['success'])} succeeded, {len(results['failed'])} failed")
    if results["failed"]:
        print(f"Failed: {', '.join(results['failed'])}")
    print("=" * 60)

    return results


if __name__ == "__main__":
    main()
