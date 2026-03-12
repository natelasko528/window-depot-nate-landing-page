#!/usr/bin/env python3
"""
Window Depot USA Milwaukee — King Mode Social Post Generator
=============================================================
Two-phase pipeline:

  PHASE 1 — Gemini generates 12 photorealistic background photos
             (landscape 1376×768 + square 1024×1024 per service)

  PHASE 2 — Pillow composites:
             • Full-bleed photo background
             • Dark gradient left-side overlay (text stays readable)
             • Window Depot logo (top-left)
             • Pain Point headline (gold / white)
             • Solution body copy
             • Benefit lines (light blue)
             • Gold CTA button
             • Phone number + website
             • Nate cutout (bottom-right, never overlaps text)
             • Brand tagline strip (very bottom)

Output: /workspace/social-posts/  — 18 PNG files ready for review.
Nothing is sent to GHL until the user approves each image.

Run:
  python3 scripts/generate_social_posts.py
"""

import os
import io
import time
import base64
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

# ── API / model ────────────────────────────────────────────────────────────
from google import genai
from google.genai import types

API_KEY = os.environ.get("Gemini API Key")
MODEL   = "gemini-3.1-flash-image-preview"
client  = genai.Client(api_key=API_KEY)

# ── Paths ──────────────────────────────────────────────────────────────────
WORKSPACE = Path(__file__).parent.parent
LOGO      = WORKSPACE / "brand-assets/window-depot-logo.png"
NATE      = WORKSPACE / "brand-assets/nate_pointing_right_cutout.png"
BG_DIR    = WORKSPACE / "social-posts/backgrounds"
OUT_DIR   = WORKSPACE / "social-posts"
FONT      = "/usr/share/fonts/truetype/macos/Helvetica.ttc"

BG_DIR.mkdir(parents=True, exist_ok=True)
OUT_DIR.mkdir(exist_ok=True)

# ── Brand palette ──────────────────────────────────────────────────────────
NAVY      = (18,  32,  64)
NAVY_DARK = (8,   16,  36)
BLUE      = (30,  80, 160)
GOLD      = (212, 175,  55)
WHITE     = (255, 255, 255)
OFF_WHITE = (230, 235, 245)
LT_BLUE   = (100, 160, 220)

PHONE   = "(414) 312-5213"
WEBSITE = "windowdepotmilwaukee.com"
BOOKING = "wdusa-nate-landing.vercel.app/#booking"

# ── Platform sizes ─────────────────────────────────────────────────────────
PLATFORMS = {
    "facebook":  (1200, 628),
    "instagram": (1080, 1080),
    "linkedin":  (1200, 628),
}

# ══════════════════════════════════════════════════════════════════════════
#  PHASE 1 — IMAGE GENERATION PROMPTS  (King Mode: maximum specificity)
# ══════════════════════════════════════════════════════════════════════════
#
#  Prompt philosophy:
#  • Ultra-specific scene description — camera angle, lighting, time of day
#  • Wisconsin/Milwaukee regional authenticity
#  • Warm, aspirational, "after" state (problem already solved)
#  • Zero text, logos, watermarks, or UI elements in frame
#  • Professional photography keywords for quality signal
#  • Explicit negative constraints

NO_TEXT = (
    "No text overlays, no words, no logos, no watermarks, no signs with readable text, "
    "no UI elements, no borders, no frames."
)

SERVICES = {
    "windows": {
        "landscape_prompt": (
            "Stunning interior architectural photograph of a beautiful Wisconsin craftsman-style living room "
            "bathed in warm golden morning light streaming through a brand-new set of large triple-pane "
            "picture windows. The windows are crystal-clear with no condensation or frost. Outside, a snowy "
            "Wisconsin yard is visible through the spotless glass — emphasizing the warmth inside. "
            "The room features warm hardwood floors, neutral contemporary furniture in navy and cream tones, "
            "a stone fireplace, and lush indoor plants. The composition uses a wide-angle lens with the "
            "windows as the hero element, taking up roughly two-thirds of the frame. Soft bokeh on foreground "
            "furniture. Color grade: warm golden tones, deep navy accents, cinematic quality. "
            "Shot on Sony A7R IV with 24mm f/2.8 lens, natural morning light, ISO 400. "
            "Photorealistic, 8K detail, professional real estate photography. " + NO_TEXT
        ),
        "square_prompt": (
            "Close-up architectural detail photograph: a stunning triple-pane window with a polished white "
            "vinyl frame in a cozy Wisconsin home. The glass is perfectly clear — outside the window, soft "
            "golden-hour light illuminates a manicured suburban backyard with mature trees turning autumn "
            "orange and red. Inside, a warm cup of coffee sits on the windowsill, slightly out of focus in "
            "the foreground. The image evokes comfort, warmth, and energy efficiency. "
            "Macro-to-wide hybrid lens, f/2.0, natural golden-hour light, shallow depth of field. "
            "Warm film-like color grade with deep shadows. Ultra-photorealistic, magazine-quality. " + NO_TEXT
        ),
    },
    "doors": {
        "landscape_prompt": (
            "Wide-angle exterior photograph of a stunning Milwaukee-area brick craftsman home taken at golden "
            "hour. The hero element is a gorgeous brand-new ProVia-style fiberglass front door in deep navy "
            "blue with brushed nickel hardware, sidelights, and a transom window above. The door is perfectly "
            "centered in the frame. Warm sunset light casts long shadows across immaculate stone front steps "
            "flanked by symmetrical potted mums. Mature oak trees with autumn leaves frame the scene. "
            "The home exterior is brick with white trim — the navy door pops dramatically. "
            "Shot with a 35mm tilt-shift lens, f/8, golden-hour light, HDR tone mapping. "
            "Photorealistic, architectural photography, magazine-quality detail. " + NO_TEXT
        ),
        "square_prompt": (
            "Tight beauty shot of an elegant new fiberglass front door — deep navy blue with a "
            "raised-panel design, brushed nickel lever handle, and a half-moon frosted glass insert at the "
            "top. The door is slightly ajar, revealing warm golden interior light spilling out onto a stone "
            "porch. A fall wreath with orange and burgundy tones hangs on the door. "
            "Shallow depth of field, f/2.8, creamy bokeh on the background showing a blurred Wisconsin "
            "neighborhood. Warm color grade, rich shadows. Photorealistic, commercial photography quality. "
            + NO_TEXT
        ),
    },
    "flooring": {
        "landscape_prompt": (
            "Wide interior photograph of a beautifully renovated Wisconsin home living room featuring "
            "brand-new wide-plank natural oak hardwood floors. The floors gleam under warm recessed lighting "
            "and natural daylight from large windows at the far end of the room. The room is tastefully "
            "furnished with a modern navy sofa, cream area rug, and warm-toned decor. "
            "A doorway in the middle distance shows the flooring extending seamlessly into a dining room. "
            "Shot with a 16-35mm lens at 24mm, f/5.6, golden midday light, HDR processing. "
            "The wood grain texture is crisp and detailed. Warm, inviting mood. "
            "Professional interior design photography, 8K resolution quality. " + NO_TEXT
        ),
        "square_prompt": (
            "Stunning close-up detail shot of brand-new wide-plank luxury vinyl plank (LVP) flooring "
            "in a warm honey oak color, with a slightly elevated angle showing the floor extending to a "
            "cozy Wisconsin living room in the background. A soft golden light from a nearby window "
            "rakes across the surface, highlighting the realistic wood grain texture. "
            "A pair of white socked feet are visible at the far edge, suggesting comfort. "
            "Shot at f/1.8, extremely shallow DOF, warm golden light, ultra-realistic detail. " + NO_TEXT
        ),
    },
    "roofing": {
        "landscape_prompt": (
            "Dramatic wide-angle exterior photograph of a gorgeous Wisconsin two-story craftsman home "
            "with a brand-new architectural asphalt shingle roof in charcoal gray. The sky behind the home "
            "is dramatic — storm clouds clearing on the right, brilliant blue sky and sunlight breaking "
            "through on the left, creating a powerful god-ray effect that illuminates the roof. "
            "The home sits on a large lot with mature trees, an attached garage, and manicured landscaping. "
            "A wide-angle lens captures the full scope of the home and sky. "
            "The new shingles have rich, dimensional texture with a slight gloss. "
            "Shot with a 16mm lens, f/8, dramatic natural light, HDR processing. "
            "Photorealistic, architectural photography, high drama. " + NO_TEXT
        ),
        "square_prompt": (
            "Up-close detail photograph of brand-new architectural asphalt roof shingles on a "
            "Wisconsin home — charcoal gray with subtle dimensional texture and a slight gleam. "
            "The shot is slightly low-angle looking up at the roofline against a vivid deep blue sky "
            "with dramatic white clouds. The ridge cap is freshly installed. "
            "Warm afternoon sunlight rakes across the shingles, revealing every ridge and shadow. "
            "Shot at f/5.6, 35mm lens, perfect exposure, vivid colors. "
            "Ultra-realistic, commercial photography quality. " + NO_TEXT
        ),
    },
    "siding": {
        "landscape_prompt": (
            "Stunning exterior photograph of a freshly re-sided Milwaukee-area two-story colonial home "
            "with beautiful new CraneBoard-style fiber cement lap siding in warm Navajo White. "
            "The photo is taken from a slight low-angle perspective on a bright spring morning, "
            "showcasing the clean lines, consistent shadow lines, and premium texture of the new siding. "
            "The home has white trim, black shutters, and a well-manicured front lawn with fresh mulch beds "
            "and blooming tulips in red and yellow. A bright blue sky with soft white clouds frames the home. "
            "Shot with a 24mm tilt-shift lens, f/8, bright morning light, perfect exposure. "
            "Photorealistic, architectural exterior photography, magazine quality. " + NO_TEXT
        ),
        "square_prompt": (
            "Close beauty shot of new composite lap siding installed on a Wisconsin home — "
            "warm Navajo White color with deep shadow lines between each plank. "
            "The side of the home is shown at a diagonal angle with a beautiful blurred background "
            "showing a green lawn and blue sky. Morning light rakes across the siding surface, "
            "showing every texture detail and the crisp factory-fresh installation quality. "
            "Shot at f/3.5, 50mm lens, shallow depth of field, warm morning light. "
            "Ultra-realistic, commercial real estate photography. " + NO_TEXT
        ),
    },
    "bathrooms": {
        "landscape_prompt": (
            "Wide interior photograph of a stunning newly remodeled Wisconsin bathroom — "
            "a pristine white acrylic bath and shower surround with subtle marble-pattern texture, "
            "gleaming chrome fixtures, a frameless glass shower door, and coordinated white subway tile "
            "above the tub deck. The bathroom has warm recessed lighting and a large window with frosted "
            "glass letting in soft natural light. A fluffy white towel is draped over a chrome towel bar. "
            "The grout lines are perfectly clean. The space feels spa-like, bright, and fresh. "
            "Shot with a 12mm ultra-wide lens, f/8, balanced ambient and natural light, HDR. "
            "Professional interior/architectural photography, magazine quality, 8K detail. " + NO_TEXT
        ),
        "square_prompt": (
            "Beautiful detail shot of a brand-new acrylic bath/shower remodel — "
            "a pristine white surround with a subtle marble vein texture catches the light from a "
            "frosted window to the left. A chrome rain showerhead gleams above. "
            "Fresh white towels and a small succulent plant sit on the ledge in the background. "
            "The image radiates cleanliness, quality, and spa-like luxury. "
            "Shot at f/2.8, 35mm lens, soft window light, warm color grade. "
            "Ultra-realistic, professional interior photography. " + NO_TEXT
        ),
    },
}

# ══════════════════════════════════════════════════════════════════════════
#  POST CONTENT — Pain Point → Solution → CTA
# ══════════════════════════════════════════════════════════════════════════

POSTS = {
    "windows": {
        "pain":     "Drafty Windows\nCosting You Hundreds\nEvery Winter?",
        "solution": "Triple-pane windows at dual-pane prices.\nSave up to 30% on energy bills.",
        "benefits": ["Energy Star Certified  |  Installed in 1 Day",
                     "Lifetime Warranty  |  4.9 Stars  |  A+ BBB"],
        "cta":      "FREE Estimate + $500 Gift Card",
        "accent":   LT_BLUE,
    },
    "doors": {
        "pain":     "Old Door Letting In\nCold Air — Or Just\nLooking Tired?",
        "solution": "ProVia fiberglass & steel entry doors.\nBeautiful, weather-tight, lifetime warranty.",
        "benefits": ["Custom Colors & Hardware  |  Energy Efficient",
                     "A+ BBB  |  4.9 Stars  |  1,000+ Reviews"],
        "cta":      "Book Your FREE Door Consultation",
        "accent":   GOLD,
    },
    "flooring": {
        "pain":     "Scratched, Dated\nFloors Dragging Down\nYour Entire Home?",
        "solution": "Hardwood, LVP, laminate & carpet.\nFull installation — no subcontractors.",
        "benefits": ["Any Room, Any Budget  |  Expert Crew",
                     "Price Locked 12 Months  |  No Obligation"],
        "cta":      "FREE In-Home Measure & Quote",
        "accent":   LT_BLUE,
    },
    "roofing": {
        "pain":     "An Aging Roof Is a\nDisaster Waiting\nto Happen.",
        "solution": "NorthGate asphalt & ProVia metal roofing.\nRated for Wisconsin's extreme climate.",
        "benefits": ["Expert Local Crew  |  Strong Warranties",
                     "4.9 Stars  |  A+ BBB  |  #3 Nationally"],
        "cta":      "FREE Roof Inspection — Schedule Now",
        "accent":   GOLD,
    },
    "siding": {
        "pain":     "Cracked, Faded Siding\nKilling Your\nCurb Appeal?",
        "solution": "Premium composite siding built for Wisconsin.\nProtects your home. Transforms its look.",
        "benefits": ["CraneBoard & ASCEND Composite  |  Custom Colors",
                     "Price Locked 12 Months  |  No Pressure"],
        "cta":      "FREE Siding Estimate + $500 Gift Card",
        "accent":   LT_BLUE,
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

# ══════════════════════════════════════════════════════════════════════════
#  PHASE 1 — Gemini image generation
# ══════════════════════════════════════════════════════════════════════════

def generate_bg(service, shape, prompt, out_path):
    """Generate one background image via Gemini. shape='landscape'|'square'"""
    if out_path.exists():
        print(f"    (cached) {out_path.name}")
        return True

    aspect = "landscape orientation, 16:9 aspect ratio" if shape == "landscape" \
             else "square format, 1:1 aspect ratio"
    full_prompt = f"{prompt} {aspect}."

    for attempt in range(3):
        try:
            resp = client.models.generate_content(
                model=MODEL,
                contents=full_prompt,
                config=types.GenerateContentConfig(
                    response_modalities=["IMAGE", "TEXT"]
                ),
            )
            for part in resp.candidates[0].content.parts:
                if part.inline_data and "image" in part.inline_data.mime_type:
                    img = Image.open(io.BytesIO(part.inline_data.data))
                    img.save(out_path)
                    print(f"    Generated {out_path.name}  ({img.size})")
                    return True
            print(f"    No image in response (attempt {attempt+1})")
        except Exception as e:
            print(f"    Error attempt {attempt+1}: {e}")
            if attempt < 2:
                time.sleep(4)

    print(f"    FAILED after 3 attempts: {service}/{shape}")
    return False


def run_phase1():
    print("\n" + "="*60)
    print("PHASE 1 — Generating photorealistic backgrounds with Gemini")
    print("="*60)
    successes = 0
    for service, data in SERVICES.items():
        print(f"\n  {service.upper()}")
        for shape, prompt_key in [("landscape", "landscape_prompt"),
                                   ("square",    "square_prompt")]:
            out = BG_DIR / f"{service}_{shape}.png"
            ok = generate_bg(service, shape, data[prompt_key], out)
            if ok:
                successes += 1
            time.sleep(1.5)
    print(f"\nPhase 1 complete: {successes}/12 backgrounds generated.")
    return successes


# ══════════════════════════════════════════════════════════════════════════
#  PHASE 2 — Pillow compositing
# ══════════════════════════════════════════════════════════════════════════

def load_font(size, bold=True):
    idx = 1 if bold else 0
    for path in [FONT,
                 "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
                 "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"]:
        try:
            return ImageFont.truetype(path, size, index=idx)
        except Exception:
            continue
    return ImageFont.load_default()

def tw(draw, text, fnt):
    return draw.textbbox((0,0), text, font=fnt)[2]

def shadow(draw, xy, text, fnt, fill, off=2, sc=(0,0,0,170)):
    draw.text((xy[0]+off, xy[1]+off), text, font=fnt, fill=sc)
    draw.text(xy, text, font=fnt, fill=fill)


def composite(service, platform, content, W, H):
    s = W / 1200  # scale factor

    # ── 1. Background photo ────────────────────────────────────────────
    shape  = "square" if platform == "instagram" else "landscape"
    bg_path = BG_DIR / f"{service}_{shape}.png"

    if bg_path.exists():
        bg = Image.open(bg_path).convert("RGBA")
    else:
        bg = Image.new("RGBA", (W, H), (*NAVY, 255))

    # Resize / center-crop to canvas
    br = bg.width / bg.height
    tr = W / H
    if br > tr:
        new_h, new_w = H, int(H * br)
    else:
        new_w, new_h = W, int(W / br)
    bg = bg.resize((new_w, new_h), Image.LANCZOS)
    ox, oy = (new_w - W)//2, (new_h - H)//2
    bg = bg.crop((ox, oy, ox+W, oy+H))

    # Light blur on bg for depth
    bg = bg.filter(ImageFilter.GaussianBlur(radius=1.2))

    # ── 2. Gradient overlay (dark left → transparent right) ────────────
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    text_zone = int(W * 0.64)   # gradient covers 64% of width fully, fades to 80%

    for x in range(W):
        if x <= text_zone:
            t = x / text_zone
            # Strong at far left, eases to medium at text_zone edge
            alpha = int(215 - t * 70)
        else:
            t = (x - text_zone) / (W - text_zone)
            alpha = int(145 - t * 100)
        alpha = max(0, min(240, alpha))
        od.rectangle([(x, 0), (x+1, H)], fill=(*NAVY_DARK, alpha))

    canvas = Image.alpha_composite(bg, overlay)
    draw   = ImageDraw.Draw(canvas)

    # ── 3. Accent bar (left edge, gold) ───────────────────────────────
    bar = max(6, int(8 * s))
    draw.rectangle([(0, 0), (bar, H)], fill=(*GOLD, 255))

    # ── 4. Top-right accent triangle ──────────────────────────────────
    draw.polygon(
        [(W, 0), (W - int(180*s), 0), (W, int(180*s))],
        fill=(*content["accent"], 45)
    )

    # ── 5. Layout constants ────────────────────────────────────────────
    pad      = int(46 * s)
    cx       = bar + int(12 * s) + pad        # text left edge
    text_max_w = int(W * 0.62) - cx - int(10*s)  # max text width
    strip_h  = int(30 * s)
    max_cy   = H - strip_h - int(10 * s)

    # Starting y
    cy = int(22 * s)

    # ── 6. Window Depot Logo ───────────────────────────────────────────
    logo_img = Image.open(LOGO).convert("RGBA")
    logo_w   = min(int(text_max_w * 0.82), int(300 * s))
    logo_h   = int(logo_w * logo_img.height / logo_img.width)
    logo_img = logo_img.resize((logo_w, logo_h), Image.LANCZOS)
    canvas.paste(logo_img, (cx, cy), mask=logo_img.split()[3])
    cy += logo_h + int(10 * s)

    # Gold rule
    draw.rectangle([(cx, cy), (cx + text_max_w, cy + 2)], fill=(*GOLD, 255))
    cy += int(14 * s)

    # ── 7. Dynamic font sizing (shrink to fit) ─────────────────────────
    pain_lines = content["pain"].splitlines()
    sol_lines  = content["solution"].splitlines()
    ben_lines  = content["benefits"]

    available = max_cy - cy - int(12 * s)

    for step in range(8):
        r       = 1.0 - step * 0.055
        pain_sz = int(44 * s * r)
        sol_sz  = int(24 * s * r)
        ben_sz  = int(20 * s * r)
        cta_sz  = int(23 * s * r)
        ph_sz   = int(30 * s * r)
        web_sz  = int(15 * s * r)

        pain_lh = int(pain_sz * 1.2)
        sol_lh  = int(sol_sz  * 1.35)
        ben_lh  = int(ben_sz  * 1.55)
        btn_h   = cta_sz + int(13*s)*2
        ph_h    = int(ph_sz   * 1.2)
        web_h   = int(web_sz  * 1.3)
        gaps    = int(12*s) * 5

        total = (len(pain_lines) * pain_lh + len(sol_lines) * sol_lh
                 + len(ben_lines) * ben_lh + btn_h + ph_h + web_h + gaps)
        if total <= available:
            break

    # ── 8. Pain point headline ─────────────────────────────────────────
    pain_fnt = load_font(pain_sz, bold=True)
    for i, line in enumerate(pain_lines):
        color = GOLD if i == 0 else WHITE
        shadow(draw, (cx, cy + i * pain_lh), line, pain_fnt, color)
    cy += len(pain_lines) * pain_lh + int(12 * s)

    # ── 9. Solution ───────────────────────────────────────────────────
    sol_fnt = load_font(sol_sz, bold=False)
    for i, line in enumerate(sol_lines):
        shadow(draw, (cx, cy + i * sol_lh), line, sol_fnt, OFF_WHITE)
    cy += len(sol_lines) * sol_lh + int(12 * s)

    # ── 10. Benefits ──────────────────────────────────────────────────
    ben_fnt = load_font(ben_sz, bold=True)
    for i, line in enumerate(ben_lines):
        shadow(draw, (cx, cy + i * ben_lh), line, ben_fnt, LT_BLUE)
    cy += len(ben_lines) * ben_lh + int(12 * s)

    # ── 11. CTA button ────────────────────────────────────────────────
    cta_fnt  = load_font(cta_sz, bold=True)
    btn_padx = int(18 * s)
    btn_pady = int(13 * s)
    btn_w    = min(tw(draw, content["cta"], cta_fnt) + btn_padx*2, text_max_w)
    btn_h_px = cta_sz + btn_pady * 2
    draw.rounded_rectangle([(cx, cy), (cx+btn_w, cy+btn_h_px)],
                            radius=int(6*s), fill=(*GOLD, 255))
    draw.text((cx+btn_padx, cy+btn_pady), content["cta"], font=cta_fnt, fill=NAVY_DARK)
    cy += btn_h_px + int(10 * s)

    # ── 12. Phone ─────────────────────────────────────────────────────
    ph_fnt = load_font(ph_sz, bold=True)
    shadow(draw, (cx, cy), PHONE, ph_fnt, WHITE)
    cy += ph_h + int(4 * s)

    # ── 13. Website ───────────────────────────────────────────────────
    web_fnt = load_font(web_sz, bold=False)
    draw.text((cx, cy), WEBSITE, font=web_fnt, fill=(*LT_BLUE, 210))

    # ── 14. Nate cutout (right side, bottom-anchored) ─────────────────
    try:
        nate_raw = Image.open(NATE).convert("RGBA")
        # Right zone: 36% of width
        nate_zone_x = int(W * 0.64)
        nate_zone_w = W - nate_zone_x - int(4 * s)
        nate_zone_h = H - strip_h - int(4 * s)

        ratio  = nate_raw.width / nate_raw.height
        nate_h = nate_zone_h
        nate_w = int(nate_h * ratio)
        if nate_w > nate_zone_w:
            nate_w = nate_zone_w
            nate_h = int(nate_w / ratio)

        nate_img = nate_raw.resize((nate_w, nate_h), Image.LANCZOS)
        nate_x   = nate_zone_x + (nate_zone_w - nate_w) // 2
        nate_y   = H - strip_h - nate_h
        canvas.paste(nate_img, (nate_x, nate_y), mask=nate_img.split()[3])
    except Exception as e:
        print(f"  Nate error: {e}")

    # ── 15. Bottom brand strip ────────────────────────────────────────
    draw = ImageDraw.Draw(canvas)
    draw.rectangle([(0, H-strip_h), (W, H)], fill=(*NAVY_DARK, 235))
    strip_fnt = load_font(int(13*s), bold=True)
    strip_txt = "We Create Happy Customers\u2122   |   National Strength. Local Service.   |   windowdepotmilwaukee.com"
    draw.text((pad, H-strip_h+int(9*s)), strip_txt, font=strip_fnt, fill=(*GOLD, 200))

    return canvas.convert("RGB")


def run_phase2():
    print("\n" + "="*60)
    print("PHASE 2 — Compositing branded social post images")
    print("="*60)
    generated = []
    for service, content in POSTS.items():
        print(f"\n  {service.upper()}")
        for platform, (W, H) in PLATFORMS.items():
            out = OUT_DIR / f"{service}_{platform}.png"
            print(f"    {platform} ({W}x{H}) ... ", end="", flush=True)
            img = composite(service, platform, content, W, H)
            img.save(out, "PNG", optimize=True)
            print("saved")
            generated.append(out)
    return generated


# ══════════════════════════════════════════════════════════════════════════
#  MAIN
# ══════════════════════════════════════════════════════════════════════════

def main():
    print("\n" + "█"*60)
    print("  KING MODE — Window Depot Social Post Generator")
    print("█"*60)

    phase1_ok = run_phase1()
    generated = run_phase2()

    print(f"\n{'='*60}")
    print(f"DONE.")
    print(f"  Backgrounds generated : {phase1_ok}/12")
    print(f"  Final posts composited: {len(generated)}/18")
    print(f"\n  Output: /workspace/social-posts/")
    print(f"\n  *** WAITING FOR USER APPROVAL ***")
    print(f"  Nothing has been sent to GHL.")
    print(f"  Review the images, then run the GHL upload script separately.")
    print("="*60)


if __name__ == "__main__":
    main()
