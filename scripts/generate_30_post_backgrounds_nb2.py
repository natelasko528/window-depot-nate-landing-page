#!/usr/bin/env python3
"""
Generate 30 raw social post background images using Nano Banana 2.

Requirements implemented:
- Reads prompts from /workspace/ad-drafts/30-posts/prompt_pack_nb2.json
- Uses google-genai model gemini-3.1-flash-image-preview
- Uses API key from environment variable "Gemini API Key"
- Writes images to /workspace/ad-drafts/30-posts/raw/post_01_raw.png ... post_30_raw.png
- Retries each generation at least 3 times
- Supports resume behavior by skipping existing files
- Supports CLI flags: --start, --end, --force
"""

from __future__ import annotations

import argparse
import json
import os
import re
import time
from dataclasses import dataclass
from io import BytesIO
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from PIL import Image


MODEL_ID = "gemini-3.1-flash-image-preview"
ROOT_DIR = Path("/workspace")
PROMPT_PACK_PATH = ROOT_DIR / "ad-drafts" / "30-posts" / "prompt_pack_nb2.json"
RAW_OUTPUT_DIR = ROOT_DIR / "ad-drafts" / "30-posts" / "raw"
TOTAL_POSTS = 30
MAX_ATTEMPTS = 3

PROMPT_KEYS = (
    "prompt",
    "image_prompt",
    "background_prompt",
    "nb2_prompt",
    "raw_prompt",
    "text",
)

NEGATIVE_PROMPT_KEYS = (
    "negative_prompt",
    "negative",
    "negatives",
)

STYLE_NOTE_KEYS = (
    "style_notes",
    "style_note",
    "style",
)

ASPECT_RATIO_KEYS = (
    "aspect_ratio",
    "ratio",
)

INDEX_KEYS = (
    "post",
    "post_id",
    "post_number",
    "post_num",
    "index",
    "number",
    "id",
    "slug",
    "name",
)


@dataclass
class PostFailure:
    post_number: int
    reason: str


@dataclass
class PromptSpec:
    prompt: str
    negative_prompt: str = ""
    style_notes: str = ""
    theme: str = ""
    aspect_ratio: str = "1:1"


MASTER_PROMPT_V3 = (
    "Create a photorealistic, ad-grade background image for a Wisconsin home improvement campaign. "
    "This is a PHOTO-FIRST asset: no giant graphic treatment, no fake poster styling, no generic stock look. "
    "Scene must feel like real Southeastern Wisconsin neighborhoods, realistic architecture, weather, landscaping, "
    "materials, and natural light. Use documentary-real camera realism with believable lens perspective. "
    "Leave subtle visual breathing room near top and bottom edges for later branding overlays, but keep the image "
    "fully natural with no visible blocks or artificial blank zones."
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate 30 raw backgrounds with Gemini image model."
    )
    parser.add_argument(
        "--start",
        type=int,
        default=1,
        help="First post number to generate (1-30). Default: 1",
    )
    parser.add_argument(
        "--end",
        type=int,
        default=TOTAL_POSTS,
        help="Last post number to generate (1-30). Default: 30",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Regenerate images even if output files already exist.",
    )
    args = parser.parse_args()

    if args.start < 1 or args.start > TOTAL_POSTS:
        parser.error("--start must be between 1 and 30.")
    if args.end < 1 or args.end > TOTAL_POSTS:
        parser.error("--end must be between 1 and 30.")
    if args.start > args.end:
        parser.error("--start cannot be greater than --end.")

    return args


def parse_post_number(value: Any) -> Optional[int]:
    if isinstance(value, int):
        if 1 <= value <= TOTAL_POSTS:
            return value
        return None

    if isinstance(value, str):
        match = re.search(r"(\d+)", value)
        if not match:
            return None
        number = int(match.group(1))
        if 1 <= number <= TOTAL_POSTS:
            return number

    return None


def extract_prompt_text(value: Any) -> Optional[str]:
    if isinstance(value, str):
        text = value.strip()
        return text if text else None
    return None


def pick_first_string(value: Dict[str, Any], keys: Tuple[str, ...]) -> str:
    for key in keys:
        text = extract_prompt_text(value.get(key))
        if text:
            return text
    return ""


def extract_explicit_index(value: Dict[str, Any], key_hint: Optional[str]) -> Optional[int]:
    for index_key in INDEX_KEYS:
        if index_key in value:
            post_number = parse_post_number(value[index_key])
            if post_number is not None:
                return post_number

    if key_hint is not None:
        return parse_post_number(key_hint)

    return None


def load_prompt_pack(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def build_prompt_map(payload: Any) -> Dict[int, PromptSpec]:
    prompt_map: Dict[int, PromptSpec] = {}

    if not isinstance(payload, dict):
        return prompt_map

    for key_hint, value in payload.items():
        if not isinstance(value, dict):
            continue

        post_number = extract_explicit_index(value, str(key_hint))
        if post_number is None:
            continue

        prompt = pick_first_string(value, PROMPT_KEYS)
        if not prompt:
            continue

        negative_prompt = pick_first_string(value, NEGATIVE_PROMPT_KEYS)
        style_notes = pick_first_string(value, STYLE_NOTE_KEYS)
        aspect_ratio = pick_first_string(value, ASPECT_RATIO_KEYS) or "1:1"
        theme = extract_prompt_text(value.get("theme")) or ""

        prompt_map[post_number] = PromptSpec(
            prompt=prompt,
            negative_prompt=negative_prompt,
            style_notes=style_notes,
            theme=theme,
            aspect_ratio=aspect_ratio,
        )

    return prompt_map


def build_generation_prompt(spec: PromptSpec) -> str:
    chunks = [
        MASTER_PROMPT_V3,
        f"Creative brief: {spec.prompt}",
    ]
    if spec.theme:
        chunks.append(f"Theme: {spec.theme}")
    if spec.style_notes:
        chunks.append(f"Style notes: {spec.style_notes}")
    chunks.append(f"Target aspect ratio: {spec.aspect_ratio}")
    if spec.negative_prompt:
        chunks.append(f"Avoid: {spec.negative_prompt}")
    chunks.append(
        "Hard constraints: no text, no letters, no numbers, no logos, no watermarks, no signs with readable words."
    )
    return "\n".join(chunks)


def extract_image_bytes(response: Any) -> Optional[bytes]:
    candidates = getattr(response, "candidates", None) or []
    for candidate in candidates:
        content = getattr(candidate, "content", None)
        parts = getattr(content, "parts", None) or []
        for part in parts:
            inline_data = getattr(part, "inline_data", None)
            if inline_data is None:
                continue
            data = getattr(inline_data, "data", None)
            if data:
                return data

    generated_images = getattr(response, "generated_images", None) or []
    for generated in generated_images:
        image = getattr(generated, "image", None)
        image_bytes = getattr(image, "image_bytes", None)
        if image_bytes:
            return image_bytes

    return None


def generate_one_image(client: Any, prompt_spec: PromptSpec, output_path: Path) -> Tuple[bool, str]:
    last_error = "Unknown error."
    final_prompt = build_generation_prompt(prompt_spec)

    for attempt in range(1, MAX_ATTEMPTS + 1):
        try:
            print(f"    Attempt {attempt}/{MAX_ATTEMPTS}")
            response = client.models.generate_content(
                model=MODEL_ID,
                contents=final_prompt,
            )

            image_bytes = extract_image_bytes(response)
            if not image_bytes:
                raise RuntimeError("No image data found in model response.")

            with Image.open(BytesIO(image_bytes)) as image:
                image.save(output_path, "PNG")

            return True, ""

        except Exception as exc:
            last_error = str(exc)
            print(f"    Error: {last_error}")
            if attempt < MAX_ATTEMPTS:
                backoff_seconds = min(2 * attempt, 8)
                print(f"    Retrying in {backoff_seconds}s...")
                time.sleep(backoff_seconds)

    return False, last_error


def main() -> int:
    args = parse_args()

    print("=" * 72)
    print("NB2 30-POST RAW BACKGROUND GENERATOR")
    print("=" * 72)
    print(f"Prompt pack: {PROMPT_PACK_PATH}")
    print(f"Output dir : {RAW_OUTPUT_DIR}")
    print(f"Range      : {args.start} to {args.end}")
    print(f"Force      : {args.force}")
    print("=" * 72)

    if not PROMPT_PACK_PATH.exists():
        print(f"ERROR: Prompt pack file not found: {PROMPT_PACK_PATH}")
        return 1

    api_key = os.environ.get("Gemini API Key")
    if not api_key:
        print('ERROR: Missing environment variable: "Gemini API Key"')
        return 1

    try:
        from google import genai
    except Exception as exc:
        print(f"ERROR: Failed to import google-genai: {exc}")
        return 1

    try:
        payload = load_prompt_pack(PROMPT_PACK_PATH)
    except Exception as exc:
        print(f"ERROR: Failed to read prompt pack JSON: {exc}")
        return 1

    prompt_map = build_prompt_map(payload)
    print(f"Discovered prompts for {len(prompt_map)} posts.")

    RAW_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    client = genai.Client(api_key=api_key)

    selected_posts = list(range(args.start, args.end + 1))
    generated: List[int] = []
    skipped: List[int] = []
    failures: List[PostFailure] = []

    for position, post_number in enumerate(selected_posts, start=1):
        filename = f"post_{post_number:02d}_raw.png"
        output_path = RAW_OUTPUT_DIR / filename
        print(f"\n[{position}/{len(selected_posts)}] Post {post_number:02d}: {filename}")

        if output_path.exists() and not args.force:
            print("  Skip: output already exists (resume mode).")
            skipped.append(post_number)
            continue

        prompt_spec = prompt_map.get(post_number)
        if not prompt_spec:
            reason = "No prompt found for this post number in prompt pack."
            print(f"  Fail: {reason}")
            failures.append(PostFailure(post_number=post_number, reason=reason))
            continue

        print("  Generating image...")
        ok, error_message = generate_one_image(client=client, prompt_spec=prompt_spec, output_path=output_path)
        if ok:
            print(f"  Success: wrote {output_path}")
            generated.append(post_number)
        else:
            print(f"  Fail: {error_message}")
            failures.append(PostFailure(post_number=post_number, reason=error_message))

    print("\n" + "=" * 72)
    print("FINAL SUMMARY")
    print("=" * 72)
    print(f"Requested range size : {len(selected_posts)}")
    print(f"Generated            : {len(generated)}")
    print(f"Skipped (existing)   : {len(skipped)}")
    print(f"Failed               : {len(failures)}")

    if generated:
        print(f"Generated posts      : {', '.join(f'{n:02d}' for n in generated)}")
    if skipped:
        print(f"Skipped posts        : {', '.join(f'{n:02d}' for n in skipped)}")
    if failures:
        print("Failure details:")
        for failure in failures:
            print(f"  - Post {failure.post_number:02d}: {failure.reason}")
        print("=" * 72)
        return 1

    print("=" * 72)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
