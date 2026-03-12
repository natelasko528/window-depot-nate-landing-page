#!/usr/bin/env python3
"""
Window Depot USA Milwaukee — King Mode Social Post Generator v3
===============================================================

THREE PLATFORM-CUSTOM LAYOUTS (no Nate cutout):

  FACEBOOK  (1200×628) — "THE SPLIT"
  ┌─────────────────────┬─────────────────────┐
  │                     │  [WD Logo]          │
  │   HERO PHOTO        │                     │
  │   (left 50%)        │  PAIN POINT HEADLINE│
  │   crystal clear,    │  in gold bold       │
  │   no overlay        │  Solution copy      │
  │                     │  • Benefits         │
  │                     │  [CTA BUTTON]       │
  │                     │  (414) 312-5213     │
  │                     │  website            │
  └─────────────────────┴─────────────────────┘
  Rationale: Photo draws the eye, clean panel converts.
  Best for FB's audience: homeowners, 35-65, desktop+mobile.

  INSTAGRAM (1080×1080) — "THE STACK"
  ┌────────────────────────────────────────────┐
  │                                            │
  │   HERO PHOTO  (top 55% — full width)       │
  │   crystal clear, aspirational lifestyle    │
  │                                            │
  ├────────────────────────────────────────────┤
  │  [WD Logo]          [star rating]          │
  │  PAIN POINT HEADLINE — 2 lines max         │
  │  [GOLD CTA BUTTON]    (414) 312-5213        │
  └────────────────────────────────────────────┘
  Rationale: Photo-first stops scroll. Bold, minimal text
  drives tap. Caption carries the long copy + hashtags.

  LINKEDIN  (1200×628) — "THE PRO"
  ┌────────────────────────────────┬───────────┐
  │  [WD Logo]                     │           │
  │                                │  PHOTO    │
  │  PAIN POINT HEADLINE           │  right    │
  │  in bold                       │  38%      │
  │                                │  crisp    │
  │  Solution line 1               │  no       │
  │  Solution line 2               │  overlay  │
  │  • Benefit  • Benefit          │           │
  │  ⭐4.9  A+BBB  #3 National     │           │
  │  [CTA BUTTON]  (414) 312-5213  │           │
  └────────────────────────────────┴───────────┘
  Rationale: LinkedIn is text-tolerant + professional.
  Trust signals (stars, BBB, ranking) visible up-front.
  Photo accent right shows the product/result.

Run:
  python3 scripts/generate_social_posts.py
"""

import os, io, time
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

from google import genai
from google.genai import types

API_KEY = os.environ.get("Gemini API Key")
MODEL   = "gemini-3.1-flash-image-preview"
client  = genai.Client(api_key=API_KEY)

# ── Paths ──────────────────────────────────────────────────────────────────
W_DIR  = Path(__file__).parent.parent
LOGO   = W_DIR / "brand-assets/window-depot-logo.png"
BG_DIR = W_DIR / "social-posts/backgrounds"
OUT    = W_DIR / "social-posts"
FONT   = "/usr/share/fonts/truetype/macos/Helvetica.ttc"
BG_DIR.mkdir(parents=True, exist_ok=True)
OUT.mkdir(exist_ok=True)

# ── Palette ────────────────────────────────────────────────────────────────
NAVY      = (18,  32,  64)
NAVY_DARK = (8,   16,  36)
NAVY_MID  = (22,  40,  80)
GOLD      = (212, 175,  55)
WHITE     = (255, 255, 255)
OFF_WHITE = (225, 232, 245)
LT_BLUE   = (100, 160, 220)
GOLD_DIM  = (160, 130,  40)

PHONE   = "(414) 312-5213"
WEBSITE = "windowdepotmilwaukee.com"
STARS   = "4.9 Stars  |  1,000+ Reviews  |  A+ BBB  |  #3 National"

NO_TEXT = (
    "Absolutely no text, words, letters, logos, watermarks, signs with readable text, "
    "UI elements, frames, borders, or graphic overlays of any kind. Pure photography only."
)

# ══════════════════════════════════════════════════════════════════════════
#  PROMPTS — King Mode (ultra-specific, editorial quality)
# ══════════════════════════════════════════════════════════════════════════

PROMPTS = {

    "windows_landscape": (
        "DSLR architectural interior photograph. A sunlit Wisconsin craftsman living room at 7am. "
        "The hero element: a pair of massive, crystal-clear ProVia-style triple-pane picture windows "
        "spanning nearly floor to ceiling, their frames a crisp bright white. Outside the glass: a "
        "snowy Wisconsin yard — pine trees dusted with fresh snow, a split-rail fence, pale blue winter "
        "sky. Not a hint of condensation on the glass. Inside: warm amber recessed lighting, wide-plank "
        "white oak floors, a plush cream sectional, a lit gas fireplace with stone surround. "
        "The left half of frame is dominated by the beautiful windows; the right half shows more "
        "interior room for context. Shot on Canon EOS R5, 24mm tilt-shift, f/8, ISO 200, HDR composite. "
        "Warm golden interior light vs crisp blue exterior light — stunning contrast. "
        "8K detail, interior design magazine quality. " + NO_TEXT
    ),

    "windows_square": (
        "Close-up DSLR interior lifestyle photograph. A brand-new triple-pane window in a warm "
        "Wisconsin home. Shot from inside looking slightly up toward the window. The window frame is "
        "bright white vinyl, crystal-clear glass. Outside: bare oak trees backlit by golden-hour sun, "
        "a dusting of snow on the windowsill ledge outside. On the inside windowsill: a small white "
        "ceramic pot with a trailing pothos plant and a cup of black coffee in a navy mug. "
        "Shallow depth of field (f/1.8) — the coffee cup is tack-sharp, the window and outdoor scene "
        "fall into beautiful golden bokeh. Warm whites, soft shadows. Shot on Sony A7R IV, 50mm. "
        "Feels like a lifestyle magazine spread — cozy, aspirational, peaceful. " + NO_TEXT
    ),

    "doors_landscape": (
        "Wide exterior DSLR photograph of a beautiful Milwaukee-area 1920s brick bungalow with a "
        "brand-new ProVia fiberglass front door. The door: deep navy blue, raised-panel design, "
        "brushed nickel lever handle and knocker, two narrow frosted sidelights flanking it. "
        "Late afternoon October light falls at a dramatic 45-degree angle — long golden shadows "
        "stretch across the brick facade. The front steps are bluestone with a pumpkin and fall "
        "wreath on the door. Mature oak trees frame the scene, leaves in peak amber and orange. "
        "The composition centers on the door with the home extending symmetrically on both sides. "
        "Shot on Canon 5D Mark IV, 35mm tilt-shift, f/11, golden hour. "
        "Photorealistic architectural exterior, portfolio quality. " + NO_TEXT
    ),

    "doors_square": (
        "Beauty-shot close-up of a stunning new fiberglass front door on a Wisconsin home. "
        "The door is dark charcoal with a craftsman-style glass insert at the top — warm amber "
        "interior light glows through the frosted glass from inside the home. The door is framed "
        "by white trim and a brick surround. A simple fall wreath with dried eucalyptus and orange "
        "berries hangs at eye level. Shot at f/2.0 from slightly below eye level, catching the "
        "texture of the door panel in dramatic raking afternoon light. "
        "Deep shadows, rich colors, ultra-sharp hardware detail. Sony A7R IV, 85mm portrait lens. "
        "Commercial real estate photography quality. " + NO_TEXT
    ),

    "flooring_landscape": (
        "Wide interior DSLR photograph of a Wisconsin open-plan home featuring brand-new "
        "wide-plank white oak hardwood floors — 5-inch planks, natural matte finish, "
        "with subtle grain visible. The floor stretches from a bright kitchen in the background "
        "all the way to a living area in the foreground. Natural daylight floods in from "
        "floor-to-ceiling windows on the right side, creating long warm shadows across the planks. "
        "The room is staged with a modern navy sofa, a jute area rug partially covering the floor, "
        "and warm-toned art on white walls. The shot is taken from low-angle (knee height) with a "
        "wide lens — the floor texture dominates the foreground, creating dramatic leading lines "
        "into the depth of the room. Canon R5, 16mm, f/8, natural + fill light. "
        "Interior design magazine quality, ultra-realistic. " + NO_TEXT
    ),

    "flooring_square": (
        "Overhead flat-lay style DSLR shot of a Wisconsin home's new luxury vinyl plank floor. "
        "Warm honey-toned LVP planks fill 70% of the frame in ultra-sharp detail. "
        "At the edge of the floor: a cozy scene — a thick cream knit throw draped over a "
        "natural linen bench, a navy blue book lying open, and a small amber glass vase with "
        "dried pampas grass. Shot from directly above, slightly off-center for visual tension. "
        "f/4, soft diffused window light from the right, no harsh shadows. "
        "The wood grain texture is photographic-quality realistic — every scratch, knot, and "
        "groove visible in the foreground planks. Ultra warm, inviting, aspirational. " + NO_TEXT
    ),

    "roofing_landscape": (
        "Dramatic wide exterior DSLR photograph of a Wisconsin two-story craftsman home with a "
        "brand-new dimensional architectural asphalt shingle roof in slate charcoal. Shot from "
        "the street at a slight low angle, looking up at the roofline against a dynamic sky "
        "— dramatic cumulonimbus clouds parting to reveal shafts of brilliant sunlight from the "
        "upper right, backlighting the roofline in gold. The home has white hardie-plank siding, "
        "black shutters, a two-car garage with the same new roof. Perfectly manicured green lawn, "
        "mature maple trees flanking the property. The composition shows approximately 40% home "
        "and 60% dramatic sky with clouds. Shot on Nikon D850, 20mm ultra-wide, f/11, "
        "perfect exposure + HDR sky blend. Photorealistic, dramatic, portfolio-quality. " + NO_TEXT
    ),

    "roofing_square": (
        "Ultra-close architectural detail shot of a brand-new architectural asphalt roof "
        "on a Wisconsin home — charcoal dimensional shingles with visible depth and texture, "
        "freshly installed ridge cap along the peak. Shot from directly below at a sharp "
        "upward angle, the roofline cutting diagonally across the frame from lower-left to "
        "upper-right. Behind the roofline: a vivid deep blue sky with dramatic white clouds "
        "and a sunburst in the upper right corner. The shingles have that premium blue-gray "
        "slate look with micro-granule texture in sharp focus. "
        "Sony A7R V, 35mm, f/8, afternoon sun, polarizing filter — vivid, dramatic. " + NO_TEXT
    ),

    "siding_landscape": (
        "Stunning exterior DSLR photograph of a freshly sided large Wisconsin colonial home "
        "on a bright spring day. New CraneBoard-style lap siding in warm 'Aged Pewter' gray, "
        "with deep consistent shadow lines and crisp corners. White trim, black shutters, "
        "black gutters. Shot from a slight low angle to emphasize the home's presence. "
        "The front yard: a freshly edged green lawn, mature ornamental grasses, tulips in "
        "pink and white lining the walkway. The driveway is freshly sealed, a navy "
        "SUV parked at the edge. Brilliant blue spring sky, a few white cumulus clouds. "
        "The siding texture is razor-sharp — every plank line and texture groove visible. "
        "Canon EOS R5, 24mm tilt-shift, f/9, 10am morning light. Architecture photography, "
        "magazine quality. " + NO_TEXT
    ),

    "siding_square": (
        "Extreme close-up beauty shot of new composite lap siding installed on a Wisconsin home. "
        "Shot at a diagonal angle — the planks run from lower left to upper right. "
        "The siding is in warm 'Wheat' off-white, with deep crisp shadow lines casting dramatic "
        "contrast between each plank. Raking morning sunlight from the left illuminates the "
        "surface texture in extraordinary detail — you can see the subtle wood-grain embossing "
        "in the composite material. Sharp foreground planks transition to a beautifully blurred "
        "green lawn and blue sky in the background. "
        "Sony G Master 90mm macro lens, f/4, golden morning light. Commercial exterior "
        "photography, ultra-realistic detail. " + NO_TEXT
    ),

    "bathrooms_landscape": (
        "Wide interior DSLR photograph of a freshly remodeled Wisconsin master bathroom. "
        "The hero: a stunning walk-in shower with a seamless white acrylic surround — subtle "
        "marble-vein pattern — frameless glass door wide open. A chrome rain showerhead "
        "centered overhead, matching chrome trim throughout. To the left: a deep soaking tub "
        "in the same white acrylic, chrome faucet arching over. "
        "Walls: large-format 12x24 white ceramic tile in a stacked pattern. "
        "Floor: heated 12x12 white marble mosaic tile. A large frameless mirror spans the "
        "vanity on the far wall — white cabinet, quartz top, chrome fixtures, under-cabinet "
        "lighting. Warm recessed lighting + a frosted window on the right wall lets in "
        "diffused natural light. Everything is spotless, gleaming, spa-quality. "
        "Canon R5, 12mm ultra-wide, f/8, balanced lighting. Interior architecture photography. "
        + NO_TEXT
    ),

    "bathrooms_square": (
        "Detail DSLR shot inside a newly remodeled Wisconsin bathroom. "
        "The frame is filled with a pristine white acrylic bath/shower surround — the subtle "
        "Carrara marble vein pattern catches the light beautifully. A polished chrome rain "
        "showerhead is the centerpiece at the top of frame. The frameless clear glass door "
        "on the left reflects soft natural light from an unseen frosted window. "
        "On the tub ledge: a single white orchid in a small ceramic vase, a folded white "
        "Turkish cotton towel, and a small candle. The floor has herringbone marble mosaic "
        "tile in crisp focus. Shot at f/2.8, 35mm, soft window light from the left. "
        "Spa-like, aspirational, ultra-clean. Hotel and spa photography quality. " + NO_TEXT
    ),
}

# ══════════════════════════════════════════════════════════════════════════
#  POST COPY — Pain Point → Solution → CTA
# ══════════════════════════════════════════════════════════════════════════

POSTS = {
    "windows": {
        "pain_fb":  "Drafty Windows Costing\nYou Hundreds Every Winter?",
        "pain_ig":  "Drafty Windows\nCosting You Hundreds?",
        "pain_li":  "Drafty Windows Costing\nYou Hundreds Every Winter?",
        "solution": "Triple-pane windows at dual-pane prices.\nSave up to 30% on energy bills.",
        "benefits": ["Energy Star Certified  |  Installed in 1 Day",
                     "Lifetime Warranty  |  4.9 Stars  |  A+ BBB"],
        "cta":      "FREE Estimate + $500 Gift Card",
        "accent":   LT_BLUE,
    },
    "doors": {
        "pain_fb":  "Old Door Letting In\nCold Air — Or Just Tired?",
        "pain_ig":  "Is Your Front Door\nLetting You Down?",
        "pain_li":  "Old Door Letting In\nCold Air — Or Just Tired?",
        "solution": "ProVia fiberglass & steel entry doors.\nBeautiful, weather-tight, lifetime warranty.",
        "benefits": ["Custom Colors & Hardware  |  Energy Efficient",
                     "A+ BBB  |  4.9 Stars  |  1,000+ Reviews"],
        "cta":      "Book Your FREE Door Consultation",
        "accent":   GOLD,
    },
    "flooring": {
        "pain_fb":  "Scratched, Dated Floors\nDragging Down Your Home?",
        "pain_ig":  "Scratched Floors\nDragging Down Your Home?",
        "pain_li":  "Scratched, Dated Floors\nDragging Down Your Home?",
        "solution": "Hardwood, LVP, laminate & carpet.\nFull installation — no subcontractors.",
        "benefits": ["Any Room, Any Budget  |  Expert Install Crew",
                     "Price Locked 12 Months  |  No Obligation"],
        "cta":      "FREE In-Home Measure & Quote",
        "accent":   LT_BLUE,
    },
    "roofing": {
        "pain_fb":  "An Aging Roof Is a\nDisaster Waiting to Happen.",
        "pain_ig":  "Your Roof Won't\nWarn You Before It Fails.",
        "pain_li":  "An Aging Roof Is a\nDisaster Waiting to Happen.",
        "solution": "NorthGate asphalt & ProVia metal roofing.\nRated for Wisconsin's extreme climate.",
        "benefits": ["Expert Local Crew  |  Strong Warranties",
                     "4.9 Stars  |  A+ BBB  |  #3 Nationally"],
        "cta":      "FREE Roof Inspection — Book Now",
        "accent":   GOLD,
    },
    "siding": {
        "pain_fb":  "Cracked, Faded Siding\nKilling Your Curb Appeal?",
        "pain_ig":  "Cracked Siding\nKilling Your Curb Appeal?",
        "pain_li":  "Cracked, Faded Siding\nKilling Your Curb Appeal?",
        "solution": "Premium composite siding built for Wisconsin.\nProtects your home. Transforms its look.",
        "benefits": ["CraneBoard & ASCEND Composite  |  Custom Colors",
                     "Price Locked 12 Months  |  No Pressure"],
        "cta":      "FREE Siding Estimate + $500 Gift Card",
        "accent":   LT_BLUE,
    },
    "bathrooms": {
        "pain_fb":  "Outdated Bathroom\nYou've Been Putting Off?",
        "pain_ig":  "Dreaming of a\nNew Bathroom?",
        "pain_li":  "Outdated Bathroom\nYou've Been Putting Off?",
        "solution": "Brand-new custom bath remodel\ninstalled in just ONE day.",
        "benefits": ["Custom Acrylic  |  Zero Grout Maintenance",
                     "Done in 1 Day, Guaranteed  |  Lifetime Warranty"],
        "cta":      "FREE Bath Estimate + $500 Gift Card",
        "accent":   GOLD,
    },
}

# ══════════════════════════════════════════════════════════════════════════
#  UTILITIES
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
    return draw.textbbox((0, 0), text, font=fnt)[2]

def th(draw, text, fnt):
    bb = draw.textbbox((0, 0), text, font=fnt)
    return bb[3] - bb[1]

def shadow(draw, xy, text, fnt, fill, off=2):
    draw.text((xy[0]+off, xy[1]+off), text, font=fnt, fill=(0, 0, 0, 160))
    draw.text(xy, text, font=fnt, fill=fill)

def navy_panel(W, H):
    """Create a rich navy gradient panel."""
    img = Image.new("RGBA", (W, H))
    d   = ImageDraw.Draw(img)
    for y in range(H):
        t = y / H
        r = int(NAVY_DARK[0] + (NAVY_MID[0] - NAVY_DARK[0]) * (1 - abs(t - 0.5)*2))
        g = int(NAVY_DARK[1] + (NAVY_MID[1] - NAVY_DARK[1]) * (1 - abs(t - 0.5)*2))
        b = int(NAVY_DARK[2] + (NAVY_MID[2] - NAVY_DARK[2]) * (1 - abs(t - 0.5)*2))
        d.line([(0, y), (W, y)], fill=(r, g, b, 255))
    return img

def crop_to(img, W, H):
    """Resize + center-crop an image to exact W×H."""
    r  = img.width / img.height
    tr = W / H
    if r > tr:
        new_h, new_w = H, int(H * r)
    else:
        new_w, new_h = W, int(W / r)
    img = img.resize((new_w, new_h), Image.LANCZOS)
    ox, oy = (new_w - W)//2, (new_h - H)//2
    return img.crop((ox, oy, ox+W, oy+H))

def draw_logo(canvas, cx, cy, max_w):
    logo = Image.open(LOGO).convert("RGBA")
    lw   = min(max_w, int(max_w * 0.9))
    lh   = int(lw * logo.height / logo.width)
    logo = logo.resize((lw, lh), Image.LANCZOS)
    canvas.paste(logo, (cx, cy), mask=logo.split()[3])
    return lh

def bottom_strip(canvas, W, H, strip_h, pad):
    d = ImageDraw.Draw(canvas)
    d.rectangle([(0, H-strip_h), (W, H)], fill=(*NAVY_DARK, 240))
    fnt = load_font(max(12, int(13 * W/1200)), bold=True)
    txt = "We Create Happy Customers\u2122   |   National Strength. Local Service.   |   windowdepotmilwaukee.com"
    d.text((pad, H-strip_h+int(9*W/1200)), txt, font=fnt, fill=(*GOLD, 195))

def fit_text_block(draw, lines_groups, W, max_h, base_sizes, scale):
    """
    Auto-shrink font sizes so the combined block fits in max_h.
    lines_groups: list of (lines[], bold, color, line_height_mult)
    base_sizes: matching list of base font sizes
    Returns: final sizes list
    """
    for attempt in range(10):
        factor = 1.0 - attempt * 0.06
        sizes  = [max(10, int(bs * scale * factor)) for bs in base_sizes]
        total  = 0
        for (lines, bold, color, lh_mult), sz in zip(lines_groups, sizes):
            fnt   = load_font(sz, bold)
            lh    = int(sz * lh_mult)
            total += len(lines) * lh
        if total <= max_h:
            return sizes
    return [max(10, int(bs * scale * 0.45)) for bs in base_sizes]


# ══════════════════════════════════════════════════════════════════════════
#  LAYOUT A — FACEBOOK & LINKEDIN  "THE SPLIT"  (1200×628)
#  Left 50%: hero photo  |  Right 50%: navy text panel
# ══════════════════════════════════════════════════════════════════════════

def build_split(service, content, W, H, pain_key):
    s      = W / 1200
    strip  = int(28 * s)
    panel_w = W // 2
    pad     = int(40 * s)

    # ── Left: hero photo (no overlay, crystal clear) ──────────────────
    bg_path = BG_DIR / f"{service}_landscape.png"
    if bg_path.exists():
        photo = Image.open(bg_path).convert("RGB")
    else:
        photo = Image.new("RGB", (panel_w, H), NAVY_DARK)
    photo = crop_to(photo, panel_w, H)

    # Subtle left-edge vignette so photo bleeds cleanly into panel
    vign = Image.new("RGBA", (panel_w, H), (0,0,0,0))
    vd   = ImageDraw.Draw(vign)
    for x in range(min(30, panel_w)):
        alpha = int(60 * (1 - x/30))
        vd.line([(x,0),(x,H)], fill=(0,0,0,alpha))
    photo_rgba = photo.convert("RGBA")
    photo_rgba = Image.alpha_composite(photo_rgba, vign)
    photo = photo_rgba.convert("RGB")

    # ── Right: navy panel ─────────────────────────────────────────────
    panel = navy_panel(panel_w, H)

    # Thin vertical gold divider
    pd = ImageDraw.Draw(panel)
    pd.rectangle([(0, 0), (3, H)], fill=(*GOLD, 255))

    # Assemble canvas
    canvas = Image.new("RGB", (W, H))
    canvas.paste(photo, (0, 0))
    canvas.paste(panel.convert("RGB"), (panel_w, 0))

    draw = ImageDraw.Draw(canvas)

    # Gold left accent bar on far left
    draw.rectangle([(0, 0), (int(7*s), H)], fill=(*GOLD, 255))

    # ── Text layout in right panel ────────────────────────────────────
    cx   = panel_w + pad
    cy   = int(20 * s)
    inner = panel_w - pad * 2

    # Logo
    lh   = draw_logo(canvas, cx, cy, inner)
    cy  += lh + int(10 * s)

    # Gold rule
    draw.rectangle([(cx, cy), (cx+inner, cy+2)], fill=(*GOLD, 255))
    cy += int(14 * s)

    # Pain point + solution + benefits + cta + phone + website
    pain_lines = content[pain_key].splitlines()
    sol_lines  = content["solution"].splitlines()
    ben_lines  = content["benefits"]

    avail = H - strip - cy - int(10*s)

    groups   = [
        (pain_lines, True,  None,      1.2),
        (sol_lines,  False, None,      1.35),
        (ben_lines,  True,  None,      1.5),
        ([content["cta"]], True, None, 1.0),   # CTA button
        ([PHONE],    True,  None,      1.2),
        ([WEBSITE],  False, None,      1.3),
    ]
    base_sz = [44, 23, 19, 22, 28, 14]
    sizes   = fit_text_block(draw, groups, inner, avail, base_sz, s)

    pain_sz, sol_sz, ben_sz, cta_sz, ph_sz, web_sz = sizes

    # Paint text
    pain_fnt = load_font(pain_sz, True)
    pain_lh  = int(pain_sz * 1.2)
    for i, line in enumerate(pain_lines):
        col = GOLD if i == 0 else WHITE
        shadow(draw, (cx, cy + i*pain_lh), line, pain_fnt, col)
    cy += len(pain_lines)*pain_lh + int(12*s)

    sol_fnt = load_font(sol_sz, False)
    sol_lh  = int(sol_sz * 1.35)
    for i, line in enumerate(sol_lines):
        shadow(draw, (cx, cy + i*sol_lh), line, sol_fnt, OFF_WHITE)
    cy += len(sol_lines)*sol_lh + int(12*s)

    ben_fnt = load_font(ben_sz, True)
    ben_lh  = int(ben_sz * 1.5)
    for i, line in enumerate(ben_lines):
        shadow(draw, (cx, cy + i*ben_lh), line, ben_fnt, LT_BLUE)
    cy += len(ben_lines)*ben_lh + int(12*s)

    cta_fnt  = load_font(cta_sz, True)
    bp, bpy  = int(16*s), int(12*s)
    btn_w    = min(tw(draw, content["cta"], cta_fnt) + bp*2, inner)
    btn_h    = cta_sz + bpy*2
    draw.rounded_rectangle([(cx,cy),(cx+btn_w,cy+btn_h)], radius=int(5*s), fill=(*GOLD,255))
    draw.text((cx+bp, cy+bpy), content["cta"], font=cta_fnt, fill=NAVY_DARK)
    cy += btn_h + int(10*s)

    ph_fnt = load_font(ph_sz, True)
    shadow(draw, (cx, cy), PHONE, ph_fnt, WHITE)
    cy += int(ph_sz*1.2) + int(4*s)

    web_fnt = load_font(web_sz, False)
    draw.text((cx, cy), WEBSITE, font=web_fnt, fill=(*LT_BLUE, 205))

    bottom_strip(canvas, W, H, strip, pad)
    return canvas


# ══════════════════════════════════════════════════════════════════════════
#  LAYOUT B — INSTAGRAM  "THE STACK"  (1080×1080)
#  Top 55%: full-width hero photo  |  Bottom 45%: navy text section
# ══════════════════════════════════════════════════════════════════════════

def build_stack(service, content, W, H):
    s         = W / 1080
    photo_h   = int(H * 0.55)
    text_h    = H - photo_h
    strip     = int(26 * s)
    pad       = int(36 * s)

    # ── Top: hero photo ───────────────────────────────────────────────
    bg_path = BG_DIR / f"{service}_square.png"
    if bg_path.exists():
        photo = Image.open(bg_path).convert("RGB")
    else:
        photo = Image.new("RGB", (W, photo_h), NAVY_DARK)
    photo = crop_to(photo, W, photo_h)

    # Subtle bottom-fade so photo blends into navy section
    fade = Image.new("RGBA", (W, photo_h), (0,0,0,0))
    fd   = ImageDraw.Draw(fade)
    for y in range(photo_h):
        t     = y / photo_h
        alpha = int(max(0, (t - 0.6) / 0.4 * 200)) if t > 0.6 else 0
        fd.line([(0,y),(W,y)], fill=(*NAVY_DARK, alpha))
    photo_rgba = photo.convert("RGBA")
    photo_rgba = Image.alpha_composite(photo_rgba, fade)
    photo      = photo_rgba.convert("RGB")

    # ── Bottom: navy text section ──────────────────────────────────────
    panel = navy_panel(W, text_h)

    # Gold horizontal divider at top of panel
    pd = ImageDraw.Draw(panel)
    pd.rectangle([(0,0),(W,3)], fill=(*GOLD,255))

    # Assemble canvas
    canvas = Image.new("RGB", (W, H))
    canvas.paste(photo, (0, 0))
    canvas.paste(panel.convert("RGB"), (0, photo_h))

    draw = ImageDraw.Draw(canvas)

    # Gold left accent bar
    draw.rectangle([(0,0),(int(7*s),H)], fill=(*GOLD,255))

    # ── Text in bottom section ────────────────────────────────────────
    cx    = int(14*s) + pad
    cy    = photo_h + int(18*s)
    inner = W - cx - pad

    # Logo + star rating on same row
    logo_img = Image.open(LOGO).convert("RGBA")
    lw       = int(inner * 0.48)
    lh_px    = int(lw * logo_img.height / logo_img.width)
    logo_img = logo_img.resize((lw, lh_px), Image.LANCZOS)
    canvas.paste(logo_img, (cx, cy), mask=logo_img.split()[3])

    # Stars on the right of logo row
    star_fnt = load_font(int(18*s), True)
    star_x   = cx + lw + int(16*s)
    star_y   = cy + (lh_px - int(18*s))//2
    draw.text((star_x, star_y), "4.9 \u2605  |  A+BBB  |  #3 National",
              font=star_fnt, fill=(*GOLD, 220))

    cy += lh_px + int(12*s)

    # Pain (2 lines max), solution (1 line), CTA button, phone — fit in remaining space
    pain_lines = content["pain_ig"].splitlines()[:2]
    sol_line   = content["solution"].splitlines()[0]
    avail      = H - strip - cy - int(10*s)

    base_sz = [40, 20, 22, 26]
    groups  = [(pain_lines, True, None, 1.2),
               ([sol_line], False, None, 1.3),
               ([content["cta"]], True, None, 1.0),
               ([PHONE], True, None, 1.2)]
    sizes   = fit_text_block(draw, groups, inner, avail, base_sz, s)
    p_sz, sol_sz, cta_sz, ph_sz = sizes

    pain_fnt = load_font(p_sz, True)
    pain_lh  = int(p_sz * 1.2)
    for i, line in enumerate(pain_lines):
        col = GOLD if i == 0 else WHITE
        shadow(draw, (cx, cy + i*pain_lh), line, pain_fnt, col)
    cy += len(pain_lines)*pain_lh + int(8*s)

    sol_fnt = load_font(sol_sz, False)
    shadow(draw, (cx, cy), sol_line, sol_fnt, OFF_WHITE)
    cy += int(sol_sz*1.3) + int(12*s)

    # CTA button (full width of text column)
    cta_fnt  = load_font(cta_sz, True)
    bp, bpy  = int(20*s), int(12*s)
    btn_w    = min(tw(draw, content["cta"], cta_fnt) + bp*2, inner)
    btn_h_px = cta_sz + bpy*2
    draw.rounded_rectangle([(cx,cy),(cx+btn_w,cy+btn_h_px)], radius=int(6*s), fill=(*GOLD,255))
    draw.text((cx+bp, cy+bpy), content["cta"], font=cta_fnt, fill=NAVY_DARK)
    cy += btn_h_px + int(8*s)

    # Phone
    ph_fnt = load_font(ph_sz, True)
    shadow(draw, (cx, cy), PHONE, ph_fnt, WHITE)

    bottom_strip(canvas, W, H, strip, int(pad*0.8))
    return canvas


# ══════════════════════════════════════════════════════════════════════════
#  LAYOUT C — LINKEDIN  "THE PRO"  (1200×628)
#  Left 62%: navy text (more copy, trust signals)  |  Right 38%: photo
# ══════════════════════════════════════════════════════════════════════════

def build_pro(service, content, W, H):
    s       = W / 1200
    strip   = int(28 * s)
    text_w  = int(W * 0.62)
    photo_w = W - text_w
    pad     = int(40 * s)

    # ── Right: photo panel ─────────────────────────────────────────────
    bg_path = BG_DIR / f"{service}_landscape.png"
    if bg_path.exists():
        photo = Image.open(bg_path).convert("RGB")
    else:
        photo = Image.new("RGB", (photo_w, H), NAVY)
    photo = crop_to(photo, photo_w, H)

    # Left-edge fade on photo (blends into text panel)
    fade = Image.new("RGBA", (photo_w, H), (0,0,0,0))
    fd   = ImageDraw.Draw(fade)
    for x in range(min(50, photo_w)):
        alpha = int(180 * (1 - x/50))
        fd.line([(x,0),(x,H)], fill=(*NAVY_DARK, alpha))
    photo_rgba = photo.convert("RGBA")
    photo_rgba = Image.alpha_composite(photo_rgba, fade)
    photo      = photo_rgba.convert("RGB")

    # ── Left: navy text panel ──────────────────────────────────────────
    panel  = navy_panel(text_w, H)

    # Gold right-edge strip on panel
    pd = ImageDraw.Draw(panel)
    pd.rectangle([(text_w-3, 0),(text_w, H)], fill=(*GOLD, 200))

    canvas = Image.new("RGB", (W, H))
    canvas.paste(panel.convert("RGB"), (0, 0))
    canvas.paste(photo, (text_w, 0))
    draw = ImageDraw.Draw(canvas)

    # Gold left bar
    draw.rectangle([(0,0),(int(7*s),H)], fill=(*GOLD,255))

    # Accent triangle top-right of photo
    draw.polygon(
        [(W,0),(W-int(100*s),0),(W,int(100*s))],
        fill=(*content["accent"],50)
    )

    # ── Text column ───────────────────────────────────────────────────
    cx    = int(7*s) + int(12*s) + pad
    cy    = int(18*s)
    inner = text_w - cx - int(20*s)

    # Logo
    lh = draw_logo(canvas, cx, cy, inner)
    cy += lh + int(10*s)

    # Gold rule
    draw.rectangle([(cx, cy),(cx+inner, cy+2)], fill=(*GOLD,255))
    cy += int(12*s)

    pain_lines = content["pain_li"].splitlines()
    sol_lines  = content["solution"].splitlines()
    ben_lines  = content["benefits"]

    avail = H - strip - cy - int(10*s)

    base_sz = [40, 22, 18, 21, 26, 18, 14]
    groups  = [
        (pain_lines,        True,  None, 1.2),
        (sol_lines,         False, None, 1.35),
        (ben_lines,         True,  None, 1.5),
        ([STARS],           True,  None, 1.2),
        ([content["cta"]], True,  None, 1.0),
        ([PHONE],           True,  None, 1.2),
        ([WEBSITE],         False, None, 1.3),
    ]
    sizes = fit_text_block(draw, groups, inner, avail, base_sz, s)
    p_sz, sol_sz, ben_sz, star_sz, cta_sz, ph_sz, web_sz = sizes

    pain_fnt = load_font(p_sz, True)
    pain_lh  = int(p_sz * 1.2)
    for i, line in enumerate(pain_lines):
        col = GOLD if i == 0 else WHITE
        shadow(draw, (cx, cy + i*pain_lh), line, pain_fnt, col)
    cy += len(pain_lines)*pain_lh + int(10*s)

    sol_fnt = load_font(sol_sz, False)
    sol_lh  = int(sol_sz * 1.35)
    for i, line in enumerate(sol_lines):
        shadow(draw, (cx, cy + i*sol_lh), line, sol_fnt, OFF_WHITE)
    cy += len(sol_lines)*sol_lh + int(10*s)

    ben_fnt = load_font(ben_sz, True)
    ben_lh  = int(ben_sz * 1.5)
    for i, line in enumerate(ben_lines):
        shadow(draw, (cx, cy + i*ben_lh), line, ben_fnt, LT_BLUE)
    cy += len(ben_lines)*ben_lh + int(10*s)

    star_fnt = load_font(star_sz, True)
    draw.text((cx, cy), STARS, font=star_fnt, fill=(*GOLD, 220))
    cy += int(star_sz*1.2) + int(10*s)

    cta_fnt  = load_font(cta_sz, True)
    bp, bpy  = int(16*s), int(11*s)
    btn_w    = min(tw(draw, content["cta"], cta_fnt) + bp*2, inner)
    btn_h_px = cta_sz + bpy*2
    draw.rounded_rectangle([(cx,cy),(cx+btn_w,cy+btn_h_px)], radius=int(5*s), fill=(*GOLD,255))
    draw.text((cx+bp, cy+bpy), content["cta"], font=cta_fnt, fill=NAVY_DARK)
    cy += btn_h_px + int(8*s)

    ph_fnt = load_font(ph_sz, True)
    shadow(draw, (cx, cy), PHONE, ph_fnt, WHITE)
    cy += int(ph_sz*1.2) + int(4*s)

    web_fnt = load_font(web_sz, False)
    draw.text((cx, cy), WEBSITE, font=web_fnt, fill=(*LT_BLUE, 205))

    bottom_strip(canvas, W, H, strip, pad)
    return canvas


# ══════════════════════════════════════════════════════════════════════════
#  PHASE 1 — Generate backgrounds
# ══════════════════════════════════════════════════════════════════════════

def gen_bg(name, prompt):
    out = BG_DIR / f"{name}.png"
    if out.exists():
        print(f"    (cached) {name}")
        return True
    shape = "landscape 16:9" if "landscape" in name else "square 1:1"
    full  = f"{prompt} Image format: {shape}."
    for attempt in range(3):
        try:
            resp = client.models.generate_content(
                model=MODEL,
                contents=full,
                config=types.GenerateContentConfig(response_modalities=["IMAGE","TEXT"])
            )
            for part in resp.candidates[0].content.parts:
                if part.inline_data and "image" in part.inline_data.mime_type:
                    img = Image.open(io.BytesIO(part.inline_data.data))
                    img.save(out)
                    print(f"    {name}  {img.size}")
                    return True
        except Exception as e:
            print(f"    error ({attempt+1}): {e}")
            if attempt < 2: time.sleep(4)
    return False


def phase1():
    print("\n" + "="*62)
    print("PHASE 1 — Gemini photorealistic background generation")
    print("="*62)
    ok = 0
    for name, prompt in PROMPTS.items():
        service = name.replace("_landscape","").replace("_square","")
        print(f"\n  {name}")
        if gen_bg(name, prompt): ok += 1
        time.sleep(1.5)
    print(f"\n  {ok}/{len(PROMPTS)} backgrounds ready.")


# ══════════════════════════════════════════════════════════════════════════
#  PHASE 2 — Composite all 18 images
# ══════════════════════════════════════════════════════════════════════════

def phase2():
    print("\n" + "="*62)
    print("PHASE 2 — Platform-custom compositing")
    print("="*62)
    count = 0
    for service, content in POSTS.items():
        print(f"\n  {service.upper()}")
        for platform in ["facebook", "instagram", "linkedin"]:
            W, H   = (1200,628) if platform != "instagram" else (1080,1080)
            out    = OUT / f"{service}_{platform}.png"
            print(f"    {platform} ({W}x{H}) ... ", end="", flush=True)

            if platform == "facebook":
                img = build_split(service, content, W, H, "pain_fb")
            elif platform == "instagram":
                img = build_stack(service, content, W, H)
            else:
                img = build_pro(service, content, W, H)

            img.save(out, "PNG", optimize=True)
            print("saved")
            count += 1
    return count


# ══════════════════════════════════════════════════════════════════════════
#  MAIN
# ══════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("\n" + "█"*62)
    print("  KING MODE v3 — Window Depot Social Post Generator")
    print("  No Nate cutout | 3 platform-custom layouts")
    print("█"*62)
    phase1()
    n = phase2()
    print(f"\n{'='*62}")
    print(f"  {n}/18 images saved to social-posts/")
    print(f"  *** AWAITING USER APPROVAL — nothing sent to GHL ***")
    print("="*62)
