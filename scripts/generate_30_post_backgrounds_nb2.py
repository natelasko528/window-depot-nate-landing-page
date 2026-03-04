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

    if isinstance(value, dict):
        for key in PROMPT_KEYS:
            if key in value and isinstance(value[key], str):
                text = value[key].strip()
                if text:
                    return text

    return None


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


def build_prompt_map(payload: Any) -> Dict[int, str]:
    scored_prompts: Dict[int, Tuple[int, str]] = {}

    def set_prompt(post_number: Optional[int], prompt: Optional[str], explicit: bool) -> None:
        if post_number is None or prompt is None:
            return
        if not (1 <= post_number <= TOTAL_POSTS):
            return

        new_score = 2 if explicit else 1
        current = scored_prompts.get(post_number)
        if current is None or new_score >= current[0]:
            scored_prompts[post_number] = (new_score, prompt)

    def walk(node: Any, fallback_index: Optional[int] = None, key_hint: Optional[str] = None) -> None:
        if isinstance(node, str):
            set_prompt(fallback_index, extract_prompt_text(node), explicit=False)
            return

        if isinstance(node, list):
            for index, item in enumerate(node, start=1):
                walk(item, fallback_index=index, key_hint=None)
            return

        if not isinstance(node, dict):
            return

        dict_prompt = extract_prompt_text(node)
        dict_index = extract_explicit_index(node, key_hint)
        if dict_prompt is not None:
            if dict_index is not None:
                set_prompt(dict_index, dict_prompt, explicit=True)
            else:
                set_prompt(fallback_index, dict_prompt, explicit=False)

        for child_key, child_value in node.items():
            if isinstance(child_value, (dict, list, str)):
                child_fallback = None
                if isinstance(child_value, (dict, str)):
                    child_fallback = fallback_index
                walk(child_value, fallback_index=child_fallback, key_hint=str(child_key))

    walk(payload)
    return {post_number: value[1] for post_number, value in scored_prompts.items()}


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


def generate_one_image(client: Any, prompt: str, output_path: Path) -> Tuple[bool, str]:
    last_error = "Unknown error."

    for attempt in range(1, MAX_ATTEMPTS + 1):
        try:
            print(f"    Attempt {attempt}/{MAX_ATTEMPTS}")
            response = client.models.generate_content(
                model=MODEL_ID,
                contents=prompt,
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

        prompt = prompt_map.get(post_number)
        if not prompt:
            reason = "No prompt found for this post number in prompt pack."
            print(f"  Fail: {reason}")
            failures.append(PostFailure(post_number=post_number, reason=reason))
            continue

        print("  Generating image...")
        ok, error_message = generate_one_image(client=client, prompt=prompt, output_path=output_path)
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
