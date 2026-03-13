#!/usr/bin/env python3
"""Resize V4 ads to exact platform dimensions for production."""

import os
from PIL import Image

SIZES = {
    "facebook": (1200, 628),
    "instagram": (1080, 1080),
    "instagram-stories": (1080, 1920),
}

V4_DIR = "/workspace/ad-drafts/v4"
FINAL_DIR = "/workspace/ad-drafts/v4-final"


def resize_all():
    for platform, (tw, th) in SIZES.items():
        src_dir = os.path.join(V4_DIR, platform)
        dst_dir = os.path.join(FINAL_DIR, platform)
        os.makedirs(dst_dir, exist_ok=True)

        if not os.path.isdir(src_dir):
            continue

        for fname in sorted(os.listdir(src_dir)):
            if not fname.endswith(".png"):
                continue

            src = os.path.join(src_dir, fname)
            dst = os.path.join(dst_dir, fname)

            img = Image.open(src).convert("RGB")
            sw, sh = img.size

            src_ratio = sw / sh
            tgt_ratio = tw / th

            if abs(src_ratio - tgt_ratio) < 0.05:
                resized = img.resize((tw, th), Image.LANCZOS)
            else:
                scale = max(tw / sw, th / sh)
                new_w, new_h = int(sw * scale), int(sh * scale)
                scaled = img.resize((new_w, new_h), Image.LANCZOS)
                left = (new_w - tw) // 2
                top = (new_h - th) // 2
                resized = scaled.crop((left, top, left + tw, top + th))

            resized.save(dst, "PNG", optimize=True)
            print(f"  {fname}: {sw}x{sh} → {tw}x{th}")

    print(f"\nAll resized to {FINAL_DIR}")


if __name__ == "__main__":
    resize_all()
