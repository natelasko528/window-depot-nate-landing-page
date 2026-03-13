# Window Depot USA — Image Design Philosophy V3 (Photo-First Reset)

## Why the last rounds felt off

After auditing the latest `30posts_branded_contact_sheet.png`, the recurring issues are clear:

1. **Template fatigue**: every post uses the same heavy top/bottom bars, so the feed looks repetitive.
2. **Graphic-first instead of photo-first**: text containers dominate and hide the strongest asset (the image).
3. **Generic ad energy**: copy style reads like broad lead-gen templates, not local Milwaukee trust marketing.
4. **Weak human anchor**: little or no real Nate presence; AI-human look introduces trust risk.
5. **Low hierarchy clarity**: too many lines, all loud, so no single message lands quickly.

## New philosophy: "Local Editorial Realism"

Design principle: **Use premium, believable photography as hero; keep branding precise and restrained.**

### Core rules

1. **One message per creative**
   - One headline, one support line, one CTA.
   - No paragraph blocks in-image.

2. **Photo carries the persuasion**
   - Overlays are minimal and legible.
   - Preserve architecture, textures, weather, and lighting detail.

3. **Trust over hype**
   - Use natural language and local proof.
   - Avoid shouty promo phrasing and gimmick CTAs.

4. **Real Nate, not synthetic Nate**
   - Use `brand-assets/nate-profile.png` as the human trust marker.
   - No AI-generated mascot variants for production.

5. **Platform consistency with creative variation**
   - Shared brand DNA, varied composition and framing.
   - No “same template x 30” effect.

## Prompt system V3 (enhanced master prompt)

Use this as the **prefix** for every raw image generation prompt:

Create a photorealistic, ad-grade background image for a Wisconsin home improvement campaign. This is a PHOTO-FIRST asset: no giant graphic treatment, no fake poster styling, no generic stock look. Scene must feel like real Southeastern Wisconsin neighborhoods, realistic architecture, weather, landscaping, materials, and natural light. Use documentary-real camera realism with believable lens perspective. Leave subtle visual breathing room near top and bottom edges for later branding overlays, but keep the image fully natural with no visible blocks or artificial blank zones.

Then append:

- `Creative brief:` (service-specific prompt)
- `Theme:` (post theme)
- `Style notes:` (quality direction)
- `Target aspect ratio:`
- `Avoid:` (negative prompt)
- `Hard constraints: no text, no letters, no numbers, no logos, no watermarks, no signs with readable words.`

## Visual composition approach (V3 branded layer)

1. **Subtle gradients only** (top + bottom) for readability.
2. **Small brand chip** at top-left instead of full-width bars.
3. **Large, concise headline** (max 2 lines) in one focal area.
4. **Single support line** under headline.
5. **Nate trust badge** (real headshot, circular) near CTA zone.
6. **Compact proof chips** (4.9 stars, 1,000+ reviews, 1-year lock).
7. **Single CTA button** with phone nearby.

## Quality gate (reject if any fail)

- Image looks templated or repetitive at 6-up feed view.
- Headline competes with too many secondary elements.
- Overlay covers important product details (window/door/siding/roof/bath).
- Human looks synthetic or uncanny.
- Any accidental text/artifacts appear in the raw image.
- Creative could belong to any contractor outside SE Wisconsin.

## Operational changes implemented

- `scripts/generate_30_post_backgrounds_nb2.py`
  - Now assembles an enhanced V3 prompt per post using prompt + negative prompt + style notes + hard constraints.
- `scripts/render_30_post_brand_v3.py`
  - New photo-first renderer with minimal overlays and real Nate trust badge.

