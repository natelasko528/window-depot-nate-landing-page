#!/usr/bin/env python3
"""
Generate paired before/after images for index.html #before-after sliders.
For each project: (1) text-only prompt for BEFORE, (2) BEFORE image + prompt for AFTER
so framing matches for the clip slider.

Outputs to brand-assets/before-after/*.png (16:10, normalized size).
Requires env var: Gemini API Key
"""

import argparse
import os
import sys
import time
from io import BytesIO

from google import genai
from google.genai import types
from PIL import Image, ImageOps

WORKSPACE = "/workspace"
OUT_DIR = os.path.join(WORKSPACE, "brand-assets", "before-after")
MODEL = "gemini-3.1-flash-image-preview"
TARGET_SIZE = (1600, 1000)  # 16:10 for .ba-slider-wrap aspect-ratio

client = genai.Client(api_key=os.environ.get("Gemini API Key"))

COMMON = (
    "Photorealistic architectural photography, Wisconsin suburban residential setting, "
    "natural daylight, no people, no logos, no text of any kind, no words, no letters, "
    "no labels, no watermarks, no banners, no signage in the frame. "
    "Landscape 16:10 aspect ratio, professional real estate photo quality."
)

PROJECTS = [
    {
        "id": "windows",
        "before_prompt": (
            COMMON
            + " BEFORE renovation: Front three-quarter view of a two-story colonial-style home. "
            "Peeling white paint, dated aluminum-frame windows with storms, slightly neglected landscaping. "
            "Neutral overcast sky typical of Wisconsin. Same framing must allow an AFTER version "
            "with identical camera position."
        ),
        "after_prompt": (
            "Using the attached reference image as the BEFORE state: produce the AFTER renovation version. "
            "CRITICAL: Keep the identical camera angle, focal length, perspective, house position in frame, "
            "season, sky, and landscaping layout. ONLY change: install new white vinyl replacement windows "
            "with clean lines (suggestive of premium triple-pane style), fresh paint on trim, refreshed "
            "landscaping. The house should look well-maintained and energy-efficient. "
            + COMMON
        ),
    },
    {
        "id": "siding",
        "before_prompt": (
            COMMON
            + " BEFORE renovation: Front view of a single-family home with faded blue horizontal vinyl siding, "
            "some warping visible, white trim needing paint, concrete walk to front door. "
            "Overcast day. Camera position fixed for a matching AFTER composite."
        ),
        "after_prompt": (
            "Using the attached reference image as the BEFORE state: produce the AFTER renovation version. "
            "CRITICAL: Identical camera, perspective, and framing. ONLY change: new insulated siding in "
            "warm greige/tan tone (modern composite cladding style), subtle stone veneer wainscot at base, "
            "fresh trim, clean gutters. Same sky and yard layout. "
            + COMMON
        ),
    },
    {
        "id": "door",
        "before_prompt": (
            COMMON
            + " BEFORE renovation: Tight front-entrance photograph of a Midwest home: dated dark wood "
            "fiberglass-steel entry door, small sidelights, plain surround, slightly worn stoop. "
            "Straight-on or slight angle — must match for AFTER."
        ),
        "after_prompt": (
            "Using the attached reference image as the BEFORE state: produce the AFTER renovation version. "
            "CRITICAL: Same camera position and lens. ONLY change: new dark fiberglass-style entry door "
            "with decorative glass in sidelights, upgraded stone or trim surround, polished hardware, "
            "refreshed stoop. Elegant but not luxury-mansion. "
            + COMMON
        ),
    },
]


def extract_image_bytes(response) -> bytes | None:
    if not response.candidates:
        return None
    for part in response.candidates[0].content.parts:
        if part.inline_data is not None:
            return part.inline_data.data
    return None


def generate_text_image(prompt: str) -> bytes | None:
    response = client.models.generate_content(model=MODEL, contents=prompt)
    return extract_image_bytes(response)


def generate_from_reference_image(png_bytes: bytes, prompt: str) -> bytes | None:
    response = client.models.generate_content(
        model=MODEL,
        contents=[
            types.Part.from_bytes(data=png_bytes, mime_type="image/png"),
            prompt,
        ],
    )
    return extract_image_bytes(response)


def save_normalized(data: bytes, path: str) -> tuple[int, int]:
    im = Image.open(BytesIO(data)).convert("RGB")
    out = ImageOps.fit(im, TARGET_SIZE, method=Image.Resampling.LANCZOS, centering=(0.5, 0.5))
    out.save(path, "PNG", optimize=True)
    return out.size


def main():
    parser = argparse.ArgumentParser(description="Generate before/after slider assets")
    parser.add_argument(
        "--only",
        choices=[p["id"] for p in PROJECTS],
        help="Regenerate a single project only",
    )
    parser.add_argument(
        "--verify",
        action="store_true",
        help="Check that all PNGs exist and are %dx%d" % TARGET_SIZE,
    )
    args = parser.parse_args()

    if args.verify:
        n = verify_assets()
        print("verify:", "OK" if n == 0 else f"{n} issue(s)")
        sys.exit(1 if n else 0)

    if not os.environ.get("Gemini API Key"):
        print("ERROR: Set Gemini API Key in the environment.", file=sys.stderr)
        sys.exit(1)

    os.makedirs(OUT_DIR, exist_ok=True)
    print("=" * 60)
    print("Window Depot USA — Before/After gallery generator")
    print(f"Output: {OUT_DIR}")
    print("=" * 60)

    todo = [p for p in PROJECTS if not args.only or p["id"] == args.only]

    for proj in todo:
        pid = proj["id"]
        before_path = os.path.join(OUT_DIR, f"ba_{pid}_before.png")
        after_path = os.path.join(OUT_DIR, f"ba_{pid}_after.png")

        print(f"\n[{pid}] Generating BEFORE...")
        b_raw = generate_text_image(proj["before_prompt"])
        if not b_raw:
            print(f"  FAILED: no image for {pid} before")
            continue
        save_normalized(b_raw, before_path)
        print(f"  OK: {before_path}")
        time.sleep(2)

        with open(before_path, "rb") as f:
            b_bytes = f.read()

        print(f"[{pid}] Generating AFTER (from before reference)...")
        a_raw = generate_from_reference_image(b_bytes, proj["after_prompt"])
        if not a_raw:
            print(f"  FAILED: no image for {pid} after")
            continue
        save_normalized(a_raw, after_path)
        print(f"  OK: {after_path}")
        time.sleep(2)

    print("\nDone.")


def verify_assets() -> int:
    """Return error count; 0 means all pairs exist with matching target size."""
    errors = 0
    for proj in PROJECTS:
        pid = proj["id"]
        bp = os.path.join(OUT_DIR, f"ba_{pid}_before.png")
        ap = os.path.join(OUT_DIR, f"ba_{pid}_after.png")
        sizes = []
        for path in (bp, ap):
            if not os.path.isfile(path):
                print(f"MISSING: {path}")
                errors += 1
                sizes.append(None)
                continue
            im = Image.open(path)
            if im.size != TARGET_SIZE:
                print(f"BAD SIZE {im.size} (want {TARGET_SIZE}): {path}")
                errors += 1
            sizes.append(im.size)
        if sizes[0] and sizes[1] and sizes[0] != sizes[1]:
            print(f"MISMATCH: {pid} before {sizes[0]} vs after {sizes[1]}")
            errors += 1
    return errors


if __name__ == "__main__":
    main()
