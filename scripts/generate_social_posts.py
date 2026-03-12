#!/usr/bin/env python3
"""
Window Depot USA Milwaukee — Social Post Image Generator (v2)
=============================================================
Layout: Two-column — TEXT LEFT (65%) | NATE RIGHT (35%)
Structure: Logo → Pain Point → Solution → Benefits → CTA Button → Phone

Run:
  python3 scripts/generate_social_posts.py
"""

import os
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

# ── Brand palette ──────────────────────────────────────────────────────────
NAVY        = (18,  32,  64)
NAVY_DARK   = (10,  22,  40)
NAVY_MID    = (24,  45,  90)
BLUE        = (30,  80, 160)
GOLD        = (212, 175,  55)
WHITE       = (255, 255, 255)
OFF_WHITE   = (230, 235, 245)
LIGHT_BLUE  = (100, 160, 220)

# ── Paths ──────────────────────────────────────────────────────────────────
WORKSPACE   = Path(__file__).parent.parent
LOGO_PATH   = WORKSPACE / "brand-assets/window-depot-logo.png"
NATE_PATH   = WORKSPACE / "brand-assets/nate_thumbs_up_cutout.png"
OUT_DIR     = WORKSPACE / "social-posts"
FONT_PATH   = "/usr/share/fonts/truetype/macos/Helvetica.ttc"

OUT_DIR.mkdir(exist_ok=True)

PHONE       = "(414) 312-5213"
WEBSITE     = "windowdepotmilwaukee.com"

# ── Platform sizes ─────────────────────────────────────────────────────────
SIZES = {
    "facebook":  (1200, 628),
    "instagram": (1080, 1080),
    "linkedin":  (1200, 628),
}

# ── Post content ──────────────────────────────────────────────────────────
# Clean Gemini-generated lifestyle photos (no baked-in text) for right column background
SERVICE_PHOTOS = {
    "windows":   "ad-drafts/facebook/fb_01_energy_savings.png",
    "doors":     "ad-drafts/facebook/fb_04_comfort.png",
    "flooring":  "ad-drafts/instagram/ig_02_transformation.png",
    "roofing":   "ad-drafts/facebook/fb_03_spring_seasonal.png",
    "siding":    "ad-drafts/facebook/fb_05_curb_appeal.png",
    "bathrooms": "ad-drafts/instagram/ig_04_spring.png",
}

POSTS = {
    "windows": {
        "pain":     "Drafty Windows\nCosting You Hundreds\nEvery Year?",
        "solution": "Triple-pane windows at dual-pane prices.\nSave up to 30% on energy bills.",
        "benefits": ["Energy Star Certified  |  Installed in 1 Day",
                     "Lifetime Warranty  |  4.9 Stars  |  A+ BBB"],
        "cta":      "FREE Estimate + $500 Gift Card",
        "accent":   LIGHT_BLUE,
    },
    "doors": {
        "pain":     "Old Door Letting In\nCold Air — Or Just\nLooking Tired?",
        "solution": "ProVia fiberglass & steel entry doors.\nBeautiful, weather-tight, lifetime warranty.",
        "benefits": ["Custom Colors & Hardware  |  Energy Efficient",
                     "A+ BBB  |  4.9 Stars Google  |  1,000+ Reviews"],
        "cta":      "Book FREE Door Consultation",
        "accent":   GOLD,
    },
    "flooring": {
        "pain":     "Scratched, Dated Floors\nDragging Down\nYour Home?",
        "solution": "Hardwood, LVP, laminate & carpet.\nFull installation — no subcontractors.",
        "benefits": ["Any Room, Any Budget  |  Expert Crew",
                     "Price Locked 12 Months  |  No Obligation"],
        "cta":      "FREE In-Home Measure & Quote",
        "accent":   LIGHT_BLUE,
    },
    "roofing": {
        "pain":     "An Aging Roof Is a\nDisaster Waiting\nto Happen.",
        "solution": "NorthGate asphalt & ProVia metal roofing.\nRated for Wisconsin's extreme climate.",
        "benefits": ["Expert Local Crew  |  Strong Warranties",
                     "4.9 Stars Google  |  A+ BBB  |  #3 Nationally"],
        "cta":      "FREE Roof Inspection - Schedule Now",
        "accent":   GOLD,
    },
    "siding": {
        "pain":     "Cracked, Faded Siding\nKilling Your\nCurb Appeal?",
        "solution": "Premium composite siding built for Wisconsin.\nProtects your home. Transforms its look.",
        "benefits": ["CraneBoard & ASCEND Composite  |  Custom Colors",
                     "Price Locked 12 Months  |  No Pressure"],
        "cta":      "FREE Siding Estimate + $500 Gift Card",
        "accent":   LIGHT_BLUE,
    },
    "bathrooms": {
        "pain":     "Outdated Bathroom\nYou've Been Putting\nOff For Years?",
        "solution": "Brand-new custom bath remodel\ninstalled in just ONE day.",
        "benefits": ["Custom Acrylic  |  Zero Grout Maintenance",
                     "Done in 1 Day, Guaranteed  |  Lifetime Warranty"],
        "cta":      "FREE Bath Estimate + $500 Gift Card",
        "accent":   GOLD,
    },
}

# ── Font loader ────────────────────────────────────────────────────────────
def load_font(size, bold=True):
    idx = 1 if bold else 0
    try:
        return ImageFont.truetype(FONT_PATH, size, index=idx)
    except Exception:
        fb = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold \
             else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
        try:
            return ImageFont.truetype(fb, size)
        except Exception:
            return ImageFont.load_default()

def txt_w(draw, text, fnt):
    return draw.textbbox((0, 0), text, font=fnt)[2]

def txt_h(draw, text, fnt):
    bb = draw.textbbox((0, 0), text, font=fnt)
    return bb[3] - bb[1]

def shadow_text(draw, xy, text, fnt, fill, shadow=(0, 0, 0, 160), offset=2):
    draw.text((xy[0] + offset, xy[1] + offset), text, font=fnt, fill=shadow)
    draw.text(xy, text, font=fnt, fill=fill)

# ── Background: navy gradient ──────────────────────────────────────────────
def make_background(W, H):
    img = Image.new("RGBA", (W, H))
    draw = ImageDraw.Draw(img)
    for y in range(H):
        t = y / H
        # gradient: dark navy at edges, slightly lighter in middle
        r = int(NAVY_DARK[0] + (NAVY_MID[0] - NAVY_DARK[0]) * (1 - abs(t - 0.5) * 2))
        g = int(NAVY_DARK[1] + (NAVY_MID[1] - NAVY_DARK[1]) * (1 - abs(t - 0.5) * 2))
        b = int(NAVY_DARK[2] + (NAVY_MID[2] - NAVY_DARK[2]) * (1 - abs(t - 0.5) * 2))
        draw.line([(0, y), (W, y)], fill=(r, g, b, 255))
    return img

# ── Main image builder ─────────────────────────────────────────────────────
def build_image(service, platform, content, W, H):

    canvas = make_background(W, H)
    draw   = ImageDraw.Draw(canvas)

    s = W / 1200  # scale factor

    # ── Column split ───────────────────────────────────────────────────
    text_col_w = int(W * 0.60)
    nate_col_x = text_col_w
    nate_col_w = W - text_col_w

    pad   = int(40 * s)
    bar   = max(6, int(8 * s))
    inner = text_col_w - pad - bar - int(8 * s) - int(16 * s)

    # ── Right column: service photo background (blurred, behind Nate) ──
    photo_path = WORKSPACE / SERVICE_PHOTOS[service]
    try:
        photo = Image.open(photo_path).convert("RGBA")
        # Crop photo to right-column dimensions
        ph_ratio = photo.width / photo.height
        tgt_ratio = nate_col_w / H
        if ph_ratio > tgt_ratio:
            new_h = H
            new_w = int(H * ph_ratio)
        else:
            new_w = nate_col_w
            new_h = int(nate_col_w / ph_ratio)
        photo = photo.resize((new_w, new_h), Image.LANCZOS)
        left = (new_w - nate_col_w) // 2
        top  = (new_h - H) // 2
        photo = photo.crop((left, top, left + nate_col_w, top + H))
        # Strong blur so text in photo doesn't clash
        photo = photo.filter(ImageFilter.GaussianBlur(radius=6))
        # Dark navy overlay over the photo (70% opacity)
        photo_overlay = Image.new("RGBA", (nate_col_w, H), (*NAVY, 175))
        photo = Image.alpha_composite(photo, photo_overlay)
        canvas.paste(photo.convert("RGBA"), (nate_col_x, 0), mask=photo.split()[3])
    except Exception as e:
        print(f"  (photo bg error: {e})")

    # Redraw draw after pasting photo
    draw = ImageDraw.Draw(canvas)

    # ── Left gold accent bar ───────────────────────────────────────────
    draw.rectangle([(0, 0), (bar, H)], fill=(*GOLD, 255))

    # ── Top-right corner accent ────────────────────────────────────────
    draw.polygon(
        [(W, 0), (W - int(160 * s), 0), (W, int(160 * s))],
        fill=(*content["accent"], 60)
    )

    # ── Vertical gold divider ─────────────────────────────────────────
    draw.rectangle(
        [(text_col_w - 1, int(H * 0.04)), (text_col_w, int(H * 0.96))],
        fill=(*GOLD, 80)
    )

    # ══ TEXT COLUMN ════════════════════════════════════════════════════

    cx   = bar + int(10 * s) + pad   # text x start (after gold bar + padding)
    cy   = int(24 * s)                # text y start
    # Bottom boundary: leave room for the bottom strip
    strip_h  = int(30 * s)
    max_cy   = H - strip_h - int(8 * s)

    # ── Logo ───────────────────────────────────────────────────────────
    logo      = Image.open(LOGO_PATH).convert("RGBA")
    logo_w    = min(int(inner * 0.88), int(320 * s))
    logo_h    = int(logo_w * logo.height / logo.width)
    logo      = logo.resize((logo_w, logo_h), Image.LANCZOS)
    canvas.paste(logo, (cx, cy), mask=logo.split()[3])
    cy += logo_h + int(10 * s)

    # Gold divider
    draw.rectangle([(cx, cy), (cx + inner, cy + 2)], fill=(*GOLD, 255))
    cy += int(12 * s)

    # ── Dynamic font sizes: shrink if content won't fit ────────────────
    pain_lines = content["pain"].splitlines()
    sol_lines  = content["solution"].splitlines()
    ben_lines  = content["benefits"]
    n_pain = len(pain_lines)
    n_sol  = len(sol_lines)
    n_ben  = len(ben_lines)

    # Estimated total height of all content below logo divider
    # Keep reducing until it fits in max_cy - cy
    available = max_cy - cy - int(10 * s)  # reserve some bottom margin

    for attempt in range(6):
        reduction = 1.0 - attempt * 0.06
        pain_sz  = int(46 * s * reduction)
        sol_sz   = int(25 * s * reduction)
        ben_sz   = int(21 * s * reduction)
        cta_sz   = int(24 * s * reduction)
        phone_sz = int(32 * s * reduction)
        web_sz   = int(16 * s * reduction)

        pain_lh = int(pain_sz * 1.2)
        sol_lh  = int(sol_sz  * 1.35)
        ben_lh  = int(ben_sz  * 1.5)
        btn_h   = cta_sz + int(14 * s) * 2
        ph_h    = int(phone_sz * 1.2)
        web_h   = int(web_sz  * 1.3)
        gaps    = int(14 * s) * 5   # 5 gaps between sections

        total = (n_pain * pain_lh + n_sol * sol_lh + n_ben * ben_lh
                 + btn_h + ph_h + web_h + gaps)
        if total <= available:
            break

    # ── Pain point ────────────────────────────────────────────────────
    pain_fnt = load_font(pain_sz, bold=True)
    for i, line in enumerate(pain_lines):
        color = GOLD if i == 0 else WHITE
        shadow_text(draw, (cx, cy + i * pain_lh), line, pain_fnt, color)
    cy += n_pain * pain_lh + int(14 * s)

    # ── Solution ──────────────────────────────────────────────────────
    sol_fnt = load_font(sol_sz, bold=False)
    for i, line in enumerate(sol_lines):
        shadow_text(draw, (cx, cy + i * sol_lh), line, sol_fnt, OFF_WHITE)
    cy += n_sol * sol_lh + int(14 * s)

    # ── Benefits ──────────────────────────────────────────────────────
    ben_fnt = load_font(ben_sz, bold=True)
    for i, line in enumerate(ben_lines):
        shadow_text(draw, (cx, cy + i * ben_lh), line, ben_fnt, LIGHT_BLUE)
    cy += n_ben * ben_lh + int(14 * s)

    # ── CTA button ────────────────────────────────────────────────────
    cta_fnt  = load_font(cta_sz, bold=True)
    btn_padx = int(18 * s)
    btn_pady = int(14 * s)
    btn_w    = min(txt_w(draw, content["cta"], cta_fnt) + btn_padx * 2, inner)
    btn_h    = cta_sz + btn_pady * 2

    draw.rounded_rectangle(
        [(cx, cy), (cx + btn_w, cy + btn_h)],
        radius=int(6 * s), fill=(*GOLD, 255)
    )
    draw.text((cx + btn_padx, cy + btn_pady), content["cta"], font=cta_fnt, fill=NAVY_DARK)
    cy += btn_h + int(12 * s)

    # ── Phone ─────────────────────────────────────────────────────────
    ph_fnt = load_font(phone_sz, bold=True)
    shadow_text(draw, (cx, cy), PHONE, ph_fnt, WHITE)
    cy += ph_h + int(4 * s)

    # ── Website ───────────────────────────────────────────────────────
    web_fnt = load_font(web_sz, bold=False)
    draw.text((cx, cy), WEBSITE, font=web_fnt, fill=(*LIGHT_BLUE, 210))

    # ══ NATE COLUMN ════════════════════════════════════════════════════
    try:
        nate_raw  = Image.open(NATE_PATH).convert("RGBA")
        # Fill the Nate column as much as possible, bottom-anchored
        margin    = int(6 * s)
        max_nate_w = nate_col_w - margin * 2
        max_nate_h = H - strip_h - margin
        ratio = nate_raw.width / nate_raw.height
        # Maximize height
        nate_h = max_nate_h
        nate_w = int(nate_h * ratio)
        if nate_w > max_nate_w:
            nate_w = max_nate_w
            nate_h = int(nate_w / ratio)
        nate = nate_raw.resize((nate_w, nate_h), Image.LANCZOS)
        nate_x = nate_col_x + (nate_col_w - nate_w) // 2
        nate_y = H - strip_h - nate_h
        canvas.paste(nate, (nate_x, nate_y), mask=nate.split()[3])
    except Exception as e:
        print(f"  (Nate: {e})")

    # ══ BOTTOM STRIP ═══════════════════════════════════════════════════
    strip_h = int(30 * s)
    draw.rectangle([(0, H - strip_h), (W, H)], fill=(*NAVY_DARK, 240))
    strip_fnt = load_font(int(14 * s), bold=True)
    strip_txt = "We Create Happy Customers™   |   National Strength. Local Service."
    draw.text((pad, H - strip_h + int(9 * s)), strip_txt, font=strip_fnt, fill=(*GOLD, 200))

    return canvas.convert("RGB")


# ── Main ───────────────────────────────────────────────────────────────────
def main():
    generated = []
    print("Generating branded social media images (v2)...\n")

    for service, content in POSTS.items():
        for platform, (W, H) in SIZES.items():
            label    = f"{service}_{platform}"
            out_path = OUT_DIR / f"{label}.png"
            print(f"  {label} ({W}×{H}) ... ", end="", flush=True)
            img = build_image(service, platform, content, W, H)
            img.save(out_path, "PNG", optimize=True)
            print("✓")
            generated.append(out_path)

    print(f"\n✅  {len(generated)} images saved to /workspace/social-posts/")
    return generated


if __name__ == "__main__":
    main()
