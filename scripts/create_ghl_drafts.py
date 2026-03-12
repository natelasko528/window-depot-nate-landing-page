#!/usr/bin/env python3
"""
GHL Social Planner — Create Draft Posts
========================================
Creates posts as DRAFTS in GoHighLevel Social Planner for the
RevolutionAi Marketing Group (Facebook, Instagram, LinkedIn).

Drafts are NEVER published automatically — they sit in the GHL
Social Planner queue for manual review before anything goes live.

Review & publish at:
  https://app.gohighlevel.com/location/Rkjt05VeS56IUr5caLBD/social-planner

Run:
  python3 scripts/create_ghl_drafts.py
"""

import os
import json
import sys
import requests
from pathlib import Path

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

GHL_API_TOKEN  = os.environ.get("GHL_API_TOKEN")
GHL_LOCATION_ID = os.environ.get("GHL_LOCATION_ID")
USER_ID        = "5x0U1s3UwojNVv9aK78P"  # Nate Lasko

BASE_URL = "https://services.leadconnectorhq.com"
HEADERS  = {
    "Authorization": f"Bearer {GHL_API_TOKEN}",
    "Version": "2021-07-28",
    "Content-Type": "application/json",
}

# RevolutionAi Marketing Group — individual account IDs
FACEBOOK_ACCOUNT  = "69338440ffbf8adc5de6ef3e_Rkjt05VeS56IUr5caLBD_999513493239724_page"
INSTAGRAM_ACCOUNT = "69338466e84b5e031adc0e6b_Rkjt05VeS56IUr5caLBD_17841428950943404"
LINKEDIN_ACCOUNT  = "69338480b97205c2da5810ab_Rkjt05VeS56IUr5caLBD_ppTjrCc6FX_profile"

WORKSPACE = Path(__file__).parent.parent


# ---------------------------------------------------------------------------
# Post content
# ---------------------------------------------------------------------------

def load_ad_copy() -> dict:
    with open(WORKSPACE / "ad-drafts/ad_copy.json") as f:
        return json.load(f)


# LinkedIn captions — professional brand voice, no hashtag overload (max 3)
LINKEDIN_POSTS = [
    {
        "service": "Windows",
        "image":   "social-media-images/by-service/03_windows_linkedin.png",
        "caption": (
            "Wisconsin winters don't care about your energy budget — but the right windows do.\n\n"
            "At Window Depot USA of Milwaukee, we install triple-pane replacement windows at dual-pane prices. "
            "Our ProVia Endure windows are backed by US Dept. of Energy data showing 12–40% energy bill reductions — "
            "not marketing estimates.\n\n"
            "FREE in-home estimate + $500 gift card. Your quote is price-locked for 12 full months — zero risk.\n\n"
            "Call Nate: (414) 312-5213\n\n"
            "#MilwaukeeHomeImprovement #WindowReplacement #EnergyEfficiency"
        ),
    },
    {
        "service": "Doors",
        "image":   "social-media-images/by-service/06_doors_linkedin.png",
        "caption": (
            "Your entry door makes a first impression every single day — on guests, on buyers, and on your energy bill.\n\n"
            "Window Depot USA of Milwaukee installs ProVia fiberglass and steel entry doors engineered for Wisconsin weather. "
            "Beautiful, durable, and sealed tight against the cold.\n\n"
            "FREE in-home estimate + $500 gift card just for meeting with Nate.\n\n"
            "Call (414) 312-5213 | windowdepotmilwaukee.com\n\n"
            "#EntryDoors #CurbAppeal #MilwaukeeHomes"
        ),
    },
    {
        "service": "Siding",
        "image":   "social-media-images/by-service/15_siding_linkedin.png",
        "caption": (
            "New siding does two things at once: transforms how your home looks and adds a serious protective barrier "
            "against Wisconsin's freeze-thaw cycles.\n\n"
            "We offer CraneBoard, Market Square, and ASCEND composite cladding — premium products backed by real warranties "
            "from a company with 4.9 stars and 1,000+ Google reviews.\n\n"
            "FREE in-home estimate. Price locked 12 months. No pressure, ever.\n\n"
            "Window Depot USA of Milwaukee | (414) 312-5213\n\n"
            "#SidingReplacement #HomeExterior #MilwaukeeContractor"
        ),
    },
    {
        "service": "Roofing",
        "image":   "social-media-images/by-service/12_roofing_linkedin.png",
        "caption": (
            "A leaking roof doesn't give you a warning. It just leaks.\n\n"
            "Window Depot USA of Milwaukee installs NorthGate asphalt shingles and ProVia metal roofing — products "
            "rated for our climate and backed by warranties that actually mean something.\n\n"
            "FREE estimate + $500 gift card. No obligation, no pressure.\n\n"
            "Call Nate at (414) 312-5213\n\n"
            "#Roofing #RoofReplacement #MilwaukeeContractor"
        ),
    },
    {
        "service": "Flooring",
        "image":   "social-media-images/by-service/09_flooring_linkedin.png",
        "caption": (
            "New floors change how your entire home feels — from the first step in the door.\n\n"
            "Window Depot USA of Milwaukee offers hardwood, LVP, laminate, and carpet to match any style and budget. "
            "Our team handles everything from measurement to installation with zero hassle.\n\n"
            "FREE consultation available now.\n\n"
            "(414) 312-5213 | windowdepotmilwaukee.com\n\n"
            "#Flooring #HomeRenovation #MilwaukeeHomes"
        ),
    },
    {
        "service": "Bathrooms",
        "image":   "social-media-images/by-service/18_bathroom_linkedin.png",
        "caption": (
            "A brand-new bathroom in ONE day. Yes, really.\n\n"
            "Our Bath Makeover acrylic remodels are custom-measured, professionally installed, and built to last — "
            "all completed in a single day with minimal disruption to your home.\n\n"
            "FREE estimate + $500 gift card.\n\n"
            "Window Depot USA of Milwaukee | (414) 312-5213\n\n"
            "#BathroomRemodel #MilwaukeeContractor #HomeImprovement"
        ),
    },
]


# ---------------------------------------------------------------------------
# API helpers
# ---------------------------------------------------------------------------

def upload_image(image_path: Path) -> dict:
    """Upload an image to GHL Media Library. Returns {url, type} dict."""
    mime = "image/jpeg" if image_path.suffix.lower() in (".jpg", ".jpeg") else "image/png"
    print(f"    Uploading {image_path.name} ... ", end="", flush=True)

    with open(image_path, "rb") as f:
        resp = requests.post(
            f"{BASE_URL}/medias/upload-file",
            headers={
                "Authorization": f"Bearer {GHL_API_TOKEN}",
                "Version": "2021-07-28",
            },
            files={"file": (image_path.name, f, mime)},
            data={"fileAltText": image_path.stem, "locationId": GHL_LOCATION_ID},
        )

    data = resp.json()
    if "url" not in data:
        raise RuntimeError(f"Upload failed: {data}")

    print(f"✓")
    return {"url": data["url"], "type": mime}


def create_draft(account_ids: list, summary: str, media: list, label: str = "") -> dict:
    """
    Create a DRAFT post — status:'draft' means it will NEVER auto-publish.
    Nate must manually approve and publish from the GHL Social Planner UI.
    """
    payload = {
        "accountIds": account_ids,
        "summary":    summary,
        "type":       "post",       # content type: post / story / reel
        "status":     "draft",      # CRITICAL — prevents any publishing
        "media":      media,
        "userId":     USER_ID,
    }

    resp = requests.post(
        f"{BASE_URL}/social-media-posting/{GHL_LOCATION_ID}/posts",
        headers=HEADERS,
        json=payload,
    )
    data = resp.json()

    if not data.get("success"):
        raise RuntimeError(f"Draft creation failed for '{label}': {data}")

    return data


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    if not GHL_API_TOKEN or not GHL_LOCATION_ID:
        print("ERROR: GHL_API_TOKEN and GHL_LOCATION_ID must be set as environment variables.")
        sys.exit(1)

    ad_copy = load_ad_copy()
    created = {"facebook": 0, "instagram": 0, "linkedin": 0}

    # ------------------------------------------------------------------
    # FACEBOOK — 5 posts (branded ad images + ad copy headlines)
    # ------------------------------------------------------------------
    print("\n📘 Facebook drafts (5 posts)")
    print("-" * 40)
    for post in ad_copy["facebook"]:
        num     = post["id"].split("-")[1]          # "FB-01" → "01"
        img     = WORKSPACE / f"ad-drafts/facebook/fb_{num}_branded.png"
        label   = f"{post['id']} — {post['headline']}"

        if not img.exists():
            print(f"  ⚠  Image not found, skipping: {img}")
            continue

        print(f"  {label}")
        media   = [upload_image(img)]
        summary = (
            f"{post['headline']}\n\n"
            f"{post['primary_text']}\n\n"
            f"{post['description']}"
        )
        create_draft([FACEBOOK_ACCOUNT], summary, media, label)
        created["facebook"] += 1
        print(f"    ✓ Draft saved")

    # ------------------------------------------------------------------
    # INSTAGRAM — 5 posts (branded ad images + captions + hashtags)
    # ------------------------------------------------------------------
    print("\n📸 Instagram drafts (5 posts)")
    print("-" * 40)
    for post in ad_copy["instagram"]:
        num   = post["id"].split("-")[1]            # "IG-01" → "01"
        img   = WORKSPACE / f"ad-drafts/instagram/ig_{num}_branded.png"
        label = f"{post['id']} — {post['angle']}"

        if not img.exists():
            print(f"  ⚠  Image not found, skipping: {img}")
            continue

        print(f"  {label}")
        media   = [upload_image(img)]
        summary = f"{post['caption']}\n\n{post['hashtags']}"
        create_draft([INSTAGRAM_ACCOUNT], summary, media, label)
        created["instagram"] += 1
        print(f"    ✓ Draft saved")

    # ------------------------------------------------------------------
    # LINKEDIN — 6 service posts (service images + professional captions)
    # ------------------------------------------------------------------
    print("\n💼 LinkedIn drafts (6 posts)")
    print("-" * 40)
    for post in LINKEDIN_POSTS:
        img   = WORKSPACE / post["image"]
        label = f"LinkedIn — {post['service']}"

        if not img.exists():
            print(f"  ⚠  Image not found, skipping: {img}")
            continue

        print(f"  {post['service']}")
        media = [upload_image(img)]
        create_draft([LINKEDIN_ACCOUNT], post["caption"], media, label)
        created["linkedin"] += 1
        print(f"    ✓ Draft saved")

    # ------------------------------------------------------------------
    # Summary
    # ------------------------------------------------------------------
    total = sum(created.values())
    print("\n" + "=" * 50)
    print(f"✅  Done! {total} draft posts created.")
    print(f"   Facebook  : {created['facebook']} drafts")
    print(f"   Instagram : {created['instagram']} drafts")
    print(f"   LinkedIn  : {created['linkedin']} drafts")
    print()
    print("All posts are DRAFTS — nothing is live.")
    print("Review and publish at:")
    print(f"  https://app.gohighlevel.com/location/{GHL_LOCATION_ID}/social-planner")


if __name__ == "__main__":
    main()
