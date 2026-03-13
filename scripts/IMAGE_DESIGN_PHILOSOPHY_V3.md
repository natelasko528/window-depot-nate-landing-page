# Image Design Philosophy V3 — "SCROLL-STOPPING EDITORIAL"

> Window Depot USA of Milwaukee — Ad Image Generation System
> Supersedes all previous image generation approaches (V1 raw, V2 branded).

---

## What Went Wrong (V1 & V2 Post-Mortem)

### 7 Critical Failures

1. **AI-generated "Nate" looks nothing like real Nate** — The AI figure has straight gray hair & clean-shaven face. Real Nate has curly dark hair, blue eyes, stubble. Completely different person. Instantly destroys credibility.

2. **Wrong logos on polo shirt** — Every generation produces a different fake company logo ("ACC SOLUTIONS", "VALOR TECH", "ACME SOLUTIONS"). Looks unprofessional and embarrassing.

3. **Terrible compositing** — AI figures are composited over base photos with mismatched lighting, wrong scale, rough edges, and sometimes bizarre interactions (disembodied hands, people standing inside rooms through windows).

4. **Heavy-handed overlays destroy base images** — 60% navy blue opacity rectangle covering the left side of every FB image. Looks like a 2010 PowerPoint template, not a modern ad.

5. **Too much text crammed on images** — Headlines + bullet points + phone number + CTA button + brand name all on one image = visual clutter, amateur feel, and violates Facebook's image-text best practices.

6. **Zero layout variety** — Every FB ad has identical template (navy left, AI figure right, bullets middle). Every IG ad has identical template. No visual differentiation between ads.

7. **Generic "marketing advertisement" prompting** — Prompts use phrases like "Professional marketing advertisement photograph" which produces sterile, stock-photo-y results without emotional resonance.

---

## New Philosophy: "SCROLL-STOPPING EDITORIAL"

### Core Principle

**The image's ONLY job is to stop the scroll.** Everything else — copy, CTA, phone number, brand story — belongs in the ad platform fields (headline, description, primary text, CTA button). The image must be so visually arresting that someone stops scrolling and reads the copy.

### The Three Rules

1. **NO AI-generated people. Ever.** Use Nate's real headshot as a small circular badge where needed. Never composite a full-body AI figure.

2. **The photo IS the ad.** Don't overlay it with text blocks, bullets, or navy rectangles. Let the photo breathe. Add only the absolute minimum brand touch (a thin bar, a small badge, a subtle watermark).

3. **Shoot for emotion, not information.** The image should make someone FEEL something — warmth, security, aspiration, comfort — not try to TELL them about triple-pane specs.

---

## Image Tiers

### Tier 1: Paid Ad Creatives (Facebook/Instagram Ads)
- **Text on image**: ZERO or one short line (max 5 words)
- **Why**: Facebook/Instagram Ads Manager provides separate fields for headline, description, primary text, and CTA button. Putting text on the image is redundant AND penalized by the algorithm.
- **Goal**: Stunning, scroll-stopping photo that creates curiosity
- **Brand touch**: Optional small logo watermark in corner

### Tier 2: Organic Social Posts (Instagram Feed, Facebook Page)
- **Text on image**: One powerful headline (max 8 words)
- **Why**: Organic posts don't have separate headline/CTA fields — the image must carry some messaging
- **Design**: Modern "card" layout with frosted glass text container, Nate's real headshot badge, elegant typography
- **Brand touch**: Small Nate avatar + company name

### Tier 3: Story Cards (Instagram Stories, Facebook Stories)
- **Text on image**: Bold, impactful — text IS the hero
- **Why**: Stories are fast, swipeable, attention-grabbing
- **Design**: Full-bleed atmospheric photo with bold overlaid text, high contrast
- **Brand touch**: Nate avatar + swipe CTA

---

## Prompt Engineering — The New Approach

### What Changed

| Old Approach | New Approach |
|---|---|
| "Professional marketing advertisement photograph" | "Editorial architecture photograph, Architectural Digest style" |
| Long, compound prompts with 10+ descriptors | Tight, cinematic prompts focused on ONE hero moment |
| "No text overlays" buried at the end | Strong negative guidance throughout |
| Generic "beautiful home" descriptions | Specific Midwest architectural details, weather, lighting |
| Requests for people, families, split compositions | NO people. One subject. One mood. |
| No camera/lens reference | Specific camera + lens for realism cues |

### Prompt Template

```
[Photography style] of [specific subject], [one key detail], [lighting condition].
[Atmospheric context]. [One emotional descriptor].
Shot on [camera] with [lens]. [Aspect ratio]. 
Absolutely no text, no logos, no watermarks, no people, no typography of any kind.
```

### Photography Style References (rotate for variety)
- "Editorial architecture photograph, Architectural Digest quality"
- "Award-winning residential real estate photography"
- "Dwell Magazine editorial interior"
- "Cinematic twilight real estate photograph"
- "Warm lifestyle interior photograph, shelter magazine quality"

### Camera + Lens References (for realism cues)
- "Shot on Sony A7R IV with 24mm f/1.4" (wide interiors/exteriors)
- "Shot on Canon R5 with 35mm f/1.4" (medium interiors)
- "Shot on Nikon Z9 with 85mm f/1.2" (detail/product shots)
- "Shot on Phase One IQ4 with 55mm" (ultra-sharp editorial)

### Subject Categories

1. **Twilight Exterior** — Home at blue hour with warm interior glow through windows
2. **Cozy Interior** — Living room/kitchen with natural light through crystal-clear windows
3. **Seasonal Exterior** — Spring blooms, fall colors, winter snow with beautiful home
4. **Detail/Craft** — Close-up of window hardware, frame quality, glass clarity
5. **Atmospheric Interior** — Morning light, coffee on windowsill, peaceful mood
6. **Curb Appeal** — Front approach, new door, landscaping, inviting entry

### What to NEVER Include in Prompts
- People, families, hands, faces, bodies
- Text, labels, signs, house numbers
- Split compositions or before/after layouts
- "Marketing" or "advertisement" framing
- Brand names or logos
- Product cross-sections or technical diagrams

---

## Branding Overlay — The New Design System

### For Paid Ads (Tier 1)
- **Approach**: Minimal. Small frosted-glass pill in bottom corner with "Window Depot USA" text
- **Nate**: Not on paid ad images (the ad copy mentions him)
- **Text**: Zero text on image, or one emotional stat ("40% Lower Energy Bills")
- **Layout**: Full-bleed photo with 2-4px brand-color border (optional)

### For Organic Posts (Tier 2)
- **Approach**: Modern card design
- **Layout options**:
  - **Bottom Bar**: Thin frosted-glass bar at bottom (8-12% of image height) with headline + Nate badge
  - **Corner Card**: Frosted-glass rounded rectangle in bottom-left corner with headline
  - **Clean Strip**: Full-width thin gradient strip at bottom with brand name + phone
- **Nate**: Real headshot in small (60-80px) circle with white border
- **Typography**: Clean, properly kerned, generous letter-spacing
- **Colors**: Semi-transparent navy (#122040 at 70-80% opacity) with white text

### For Stories (Tier 3)
- **Approach**: Text-forward, photo as atmosphere
- **Layout**: Full-bleed photo, top-to-bottom gradient overlay (transparent → 60% navy)
- **Text**: Large, bold headline centered. Subtext below. CTA button at bottom.
- **Nate**: Small circular badge near CTA
- **Typography**: Bold condensed for headline, regular for subtext

### Design Tokens

```python
COLORS = {
    "navy": (18, 32, 64),          # Primary overlay
    "brand_blue": (30, 80, 160),   # CTA buttons
    "light_blue": (100, 160, 220), # Accents, phone number
    "white": (255, 255, 255),      # Text
    "gold": (212, 175, 55),        # Premium accent
    "frost": (18, 32, 64, 160),    # Frosted glass base
}

TYPOGRAPHY = {
    "headline": {"size": 48, "weight": "bold", "tracking": 2},
    "subhead": {"size": 28, "weight": "regular", "tracking": 1},
    "body": {"size": 20, "weight": "regular", "tracking": 0},
    "badge": {"size": 16, "weight": "bold", "tracking": 1},
}

SPACING = {
    "bar_height_ratio": 0.10,      # Bottom bar = 10% of image height
    "padding": 24,                  # Internal padding
    "avatar_size": 64,              # Nate headshot circle diameter
    "border_radius": 12,            # Rounded corners
    "border_width": 3,              # Avatar border
}
```

---

## Technical Implementation

### Script Architecture
- `scripts/generate_v3_photos.py` — Generates base editorial photos via Gemini
- `scripts/generate_v3_branded.py` — Applies minimal brand overlays via Pillow

### Key Technical Improvements
1. **Gaussian blur backing** for text readability (frosted glass effect)
2. **Anti-aliased circular crop** for Nate's real headshot
3. **Proper alpha compositing** with correct blend modes
4. **Multiple layout variants** — each ad gets a DIFFERENT visual treatment
5. **Real Nate headshot only** — from `brand-assets/nate-profile.png`
6. **No AI-generated people** in any step of the pipeline

### File Naming Convention
```
v3_{platform}_{number}_{angle}.png          # Base photo
v3_{platform}_{number}_{angle}_branded.png  # With brand overlay
```

### Output Sizes
| Platform | Dimensions | Notes |
|---|---|---|
| Facebook Feed | 1200×628 | 1.91:1 landscape |
| Instagram Feed | 1080×1080 | 1:1 square |
| Instagram Stories | 1080×1920 | 9:16 vertical |

---

## Measurement of Success

A good V3 image should:
1. Look indistinguishable from a professional real estate photo
2. Stop someone mid-scroll on their phone
3. NOT look like it has an AI-generated person pasted on it
4. NOT look like a PowerPoint slide
5. Feel warm, aspirational, and distinctly Midwestern
6. Have branding so subtle you almost miss it on paid ads
7. Have branding clean and elegant (not cluttered) on organic posts
