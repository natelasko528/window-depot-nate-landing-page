#!/usr/bin/env python3
"""
V3 — Editorial Photo Generator for Window Depot USA Milwaukee
Philosophy: "SCROLL-STOPPING EDITORIAL"

Generates stunning editorial-quality photos with ZERO text, ZERO people,
ZERO logos. These are pure atmosphere + architecture + emotion images
designed to stop the scroll.

Uses Gemini 3.1 Flash Image (Nano Banana 2).
"""

import os
import time
from io import BytesIO
from google import genai
from PIL import Image

client = genai.Client(api_key=os.environ.get("Gemini API Key"))
MODEL = "gemini-3.1-flash-image-preview"

OUT_DIR = "/workspace/ad-drafts"

PHOTO_PROMPTS = {
    "fb_01": {
        "filename": "v3_fb_01_twilight_glow.png",
        "platform": "facebook",
        "angle": "Twilight Curb Appeal",
        "prompt": (
            "Cinematic twilight real estate photograph of a charming two-story craftsman home "
            "in a quiet Milwaukee suburb. Deep blue evening sky with the last orange glow on "
            "the horizon. Every window in the house glows with warm amber interior light. "
            "Fresh white-framed replacement windows are crisp and prominent. Wet driveway "
            "reflects the warm light. Mature oak trees frame the composition. Meticulous "
            "landscaping with ornamental grasses. Shot on Sony A7R IV with 24mm f/1.4 lens. "
            "Landscape orientation, 16:9 aspect ratio. "
            "Absolutely no text, no logos, no watermarks, no people, no typography of any kind."
        ),
    },
    "fb_02": {
        "filename": "v3_fb_02_morning_kitchen.png",
        "platform": "facebook",
        "angle": "Morning Comfort",
        "prompt": (
            "Award-winning interior photograph of a bright Midwestern kitchen at sunrise. "
            "Large new casement windows above the sink flood the space with golden morning light. "
            "Steam rises from a coffee mug on the clean quartz countertop. Through the crystal-clear "
            "triple-pane glass, a snowy Wisconsin backyard is visible — frosted trees, blue-white "
            "morning light outside contrasting the warmth inside. The window frames are pristine white "
            "vinyl. Warm wood tones, subway tile backsplash. Peaceful, inviting, aspirational. "
            "Shot on Canon R5 with 35mm f/1.4 lens. Landscape 16:9. "
            "Absolutely no text, no logos, no watermarks, no people, no typography of any kind."
        ),
    },
    "fb_03": {
        "filename": "v3_fb_03_spring_porch.png",
        "platform": "facebook",
        "angle": "Spring Renewal",
        "prompt": (
            "Editorial architecture photograph of a welcoming Wisconsin home entrance in early spring. "
            "A beautiful new fiberglass front door with sidelights and fresh trim. Blooming crabapple "
            "tree beside the porch with pink blossoms catching soft overcast light. Clean concrete "
            "walkway, emerging green lawn, potted spring flowers on the steps. The new windows flanking "
            "the entry are spotless and modern. Soft, optimistic spring atmosphere — the kind of image "
            "that makes you want to come home. Shot on Phase One IQ4 with 55mm lens. Landscape 16:9. "
            "Absolutely no text, no logos, no watermarks, no people, no typography of any kind."
        ),
    },
    "fb_04": {
        "filename": "v3_fb_04_cozy_window_seat.png",
        "platform": "facebook",
        "angle": "Winter Comfort",
        "prompt": (
            "Warm lifestyle interior photograph, shelter magazine quality. A cozy window seat nook "
            "in a Milwaukee home on a snowy winter afternoon. Large new triple-pane windows with "
            "zero condensation despite heavy snow outside. Soft throw blanket draped on the cushion, "
            "a book open face-down, warm reading lamp casting amber light. The glass is crystal clear — "
            "you can see every detail of the snowy landscape outside while feeling the warmth inside. "
            "Rich wood window trim. Calm, peaceful, hygge atmosphere. "
            "Shot on Sony A7R IV with 50mm f/1.2 lens. Landscape 16:9. "
            "Absolutely no text, no logos, no watermarks, no people, no typography of any kind."
        ),
    },
    "fb_05": {
        "filename": "v3_fb_05_siding_transformation.png",
        "platform": "facebook",
        "angle": "Full Home Transformation",
        "prompt": (
            "Stunning real estate photograph of a beautifully renovated Midwestern colonial home. "
            "Fresh composite cladding siding in a sophisticated gray-blue tone, bright white window "
            "trim, new architectural shingle roof, and a striking dark front door with brushed nickel "
            "hardware. Late afternoon golden hour light creates long warm shadows across the facade. "
            "Perfectly maintained lawn, mature shade trees, quiet residential street. "
            "The kind of home that makes neighbors jealous. Shot on Canon R5 with 24mm tilt-shift lens. "
            "Landscape 16:9. "
            "Absolutely no text, no logos, no watermarks, no people, no typography of any kind."
        ),
    },

    "ig_01": {
        "filename": "v3_ig_01_warm_glow.png",
        "platform": "instagram",
        "angle": "Warm Evening Interior",
        "prompt": (
            "Dwell Magazine editorial interior photograph. A serene living room in the evening — "
            "large new replacement windows spanning the far wall, looking out onto a dusky blue "
            "winter sky. Inside: warm ambient lighting from table lamps, a comfortable sectional "
            "sofa with textured pillows, hardwood floors reflecting the warm glow. The windows "
            "are the hero of the shot — massive, clean, modern white frames with perfectly clear "
            "triple-pane glass. No condensation. The contrast between warm interior and cold blue "
            "exterior through the glass is dramatic and beautiful. "
            "Shot on Sony A7R IV with 24mm f/1.4. Square format, 1:1 aspect ratio. "
            "Absolutely no text, no logos, no watermarks, no people, no typography of any kind."
        ),
    },
    "ig_02": {
        "filename": "v3_ig_02_curb_appeal_golden.png",
        "platform": "instagram",
        "angle": "Golden Hour Curb Appeal",
        "prompt": (
            "Award-winning residential real estate photography. A handsome bungalow in the "
            "Milwaukee suburbs at golden hour. New windows catch and reflect the warm sunset "
            "light. Fresh vinyl siding in a warm cream tone. Deep green mature landscaping. "
            "A new ProVia-style fiberglass entry door in rich espresso brown with decorative "
            "glass insert. The whole scene is bathed in that magical 15-minutes-before-sunset "
            "light that makes everything glow. Shot on Phase One IQ4 with 55mm lens. "
            "Square format, 1:1. "
            "Absolutely no text, no logos, no watermarks, no people, no typography of any kind."
        ),
    },
    "ig_03": {
        "filename": "v3_ig_03_bathroom_reveal.png",
        "platform": "instagram",
        "angle": "Bathroom Transformation",
        "prompt": (
            "Interior design editorial photograph of a freshly remodeled bathroom in a "
            "Wisconsin family home. Clean acrylic wall system in soft gray marble pattern, "
            "frameless glass walk-in shower, matte black rainfall showerhead and fixtures, "
            "floating vanity with warm wood tone. A frosted window lets in soft natural "
            "daylight. Fresh white towels rolled on a shelf. The space feels spa-like yet "
            "practical — a dramatic transformation. Bright, clean, aspirational. "
            "Shot on Canon R5 with 35mm f/1.4. Square format, 1:1. "
            "Absolutely no text, no logos, no watermarks, no people, no typography of any kind."
        ),
    },
    "ig_04": {
        "filename": "v3_ig_04_spring_windows_open.png",
        "platform": "instagram",
        "angle": "Spring Fresh Air",
        "prompt": (
            "Lifestyle interior photograph, shelter magazine quality. A bright dining room "
            "in spring with new casement windows thrown wide open. Fresh spring breeze moving "
            "sheer white curtains inward. Through the open windows: a blooming Wisconsin garden "
            "with lilac bushes and green grass. Sunlight streaming across a farmhouse dining "
            "table with a vase of fresh-cut flowers. The new white window frames are crisp "
            "and modern against warm wall paint. Optimistic, fresh, alive. "
            "Shot on Nikon Z9 with 35mm f/1.4. Square format, 1:1. "
            "Absolutely no text, no logos, no watermarks, no people, no typography of any kind."
        ),
    },
    "ig_05": {
        "filename": "v3_ig_05_detail_craft.png",
        "platform": "instagram",
        "angle": "Craftsmanship Detail",
        "prompt": (
            "Macro product photograph of a premium replacement window corner detail. "
            "Shallow depth of field reveals the precise fit of a white vinyl window frame "
            "against clean interior trim. You can see the triple-pane glass edge — three "
            "distinct panes with sealed spacers between them. Morning light catches the "
            "edge of the glass creating a subtle prismatic rainbow effect. The craftsmanship "
            "is meticulous — tight seals, clean lines, quality hardware. Background softly "
            "blurred to a warm interior. Shot on Nikon Z9 with 85mm f/1.2 macro. "
            "Square format, 1:1. "
            "Absolutely no text, no logos, no watermarks, no people, no typography of any kind."
        ),
    },

    "igs_01": {
        "filename": "v3_igs_01_dramatic_twilight.png",
        "platform": "instagram-stories",
        "angle": "Dramatic Vertical Twilight",
        "prompt": (
            "Cinematic vertical photograph of a beautiful two-story home at twilight, "
            "shot from the front walkway looking up toward the entrance. Deep blue sky "
            "with one bright star visible. Every window in the house pours warm golden "
            "light outward. A new fiberglass front door with sidelights glows invitingly. "
            "Fresh landscaping with landscape lighting casting warm pools on the walkway. "
            "Dramatic, aspirational, cinematic. The perspective draws you toward the entry. "
            "Shot on Sony A7R IV with 16mm f/2.8 lens. Vertical portrait orientation, 9:16. "
            "Absolutely no text, no logos, no watermarks, no people, no typography of any kind."
        ),
    },
    "igs_02": {
        "filename": "v3_igs_02_cozy_vertical.png",
        "platform": "instagram-stories",
        "angle": "Vertical Cozy Interior",
        "prompt": (
            "Vertical editorial interior photograph for a design magazine. Tall floor-to-ceiling "
            "windows in a renovated Milwaukee home, looking out onto a snowy winter scene. "
            "Inside: a reading chair by the window, a warm knit throw, a steaming mug on "
            "a side table, a floor lamp casting warm amber light. The tall windows are the "
            "star — crystal clear, no condensation, perfectly framing the winter landscape "
            "outside. The vertical composition emphasizes the height and grandeur of the windows. "
            "Warm, intimate, peaceful. Shot on Canon R5 with 24mm f/1.4. "
            "Vertical portrait, 9:16. "
            "Absolutely no text, no logos, no watermarks, no people, no typography of any kind."
        ),
    },
    "igs_03": {
        "filename": "v3_igs_03_spring_door_vertical.png",
        "platform": "instagram-stories",
        "angle": "Spring Entry Vertical",
        "prompt": (
            "Vertical editorial photograph of a charming home entrance in spring. Looking "
            "straight at a beautiful new front door — rich wood-grain fiberglass with brushed "
            "nickel handle and decorative glass panel. Spring wreath on the door. Blooming "
            "potted flowers flanking the entry. New sidelights with clear glass. Above: fresh "
            "trim and a transom window. The porch is clean, welcoming, recently renovated. "
            "Soft overcast spring light, everything looks fresh and new. "
            "Shot on Phase One IQ4 with 55mm. Vertical portrait, 9:16. "
            "Absolutely no text, no logos, no watermarks, no people, no typography of any kind."
        ),
    },
}


def generate_image(prompt_key, prompt_data, retries=3):
    """Generate a single editorial photo via Gemini."""
    platform = prompt_data["platform"]
    filepath = os.path.join(OUT_DIR, platform, prompt_data["filename"])

    if os.path.exists(filepath):
        print(f"  [SKIP] {filepath} already exists")
        return True

    for attempt in range(retries + 1):
        try:
            print(f"  [GEN] {prompt_key} — {prompt_data['angle']} (attempt {attempt+1}/{retries+1})...")
            response = client.models.generate_content(
                model=MODEL,
                contents=prompt_data["prompt"],
            )

            for part in response.candidates[0].content.parts:
                if part.inline_data is not None:
                    image = Image.open(BytesIO(part.inline_data.data))
                    os.makedirs(os.path.dirname(filepath), exist_ok=True)
                    image.save(filepath, "PNG")
                    print(f"  [OK]  {filepath} ({image.size[0]}x{image.size[1]})")
                    return True

            print(f"  [WARN] No image data in response for {prompt_key}")
            if attempt < retries:
                time.sleep(4)

        except Exception as e:
            print(f"  [ERR] {prompt_key}: {e}")
            if attempt < retries:
                time.sleep(6)

    return False


def main():
    print("=" * 70)
    print("  V3 — SCROLL-STOPPING EDITORIAL PHOTO GENERATOR")
    print("  Window Depot USA of Milwaukee")
    print("  Philosophy: Pure editorial photography. No text. No people.")
    print("=" * 70)

    total = len(PHOTO_PROMPTS)
    print(f"\n  Generating {total} editorial photos...\n")

    results = {"success": [], "failed": []}
    for i, (key, data) in enumerate(PHOTO_PROMPTS.items(), 1):
        print(f"[{i}/{total}] {data['platform'].upper()} — {data['angle']}")
        ok = generate_image(key, data)
        results["success" if ok else "failed"].append(key)
        if i < total:
            time.sleep(3)

    print("\n" + "=" * 70)
    print(f"  RESULTS: {len(results['success'])} succeeded, {len(results['failed'])} failed")
    if results["failed"]:
        print(f"  Failed: {', '.join(results['failed'])}")
    print("=" * 70)

    return results


if __name__ == "__main__":
    main()
