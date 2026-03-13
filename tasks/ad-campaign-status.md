# Ad Campaign — Status & Task Tracker

> Last updated: March 13, 2026
> Branch: `cursor/new-image-design-philosophy-2bc8`

---

## Current Status: V4 — COMPLETE-IN-ONE (Current)

V4 takes a fundamentally different approach: Gemini generates the ENTIRE finished ad in a single call — text, layout, colors, photo all composed together. No more Pillow overlays, no more two-step process.

### Key Changes from V3 → V4
1. **Single-shot generation** — Gemini renders text + design + photo as one cohesive image
2. **No Pillow text overlays** — ALL text is AI-rendered, naturally integrated into the design
3. **Multiple visual styles** — Bold offer, photo+headline, seasonal, comfort lifestyle, transformation, stat hero, social proof
4. **Professional ad quality** — Looks like Canva/agency-designed ads, not stock-photo-plus-text
5. **Clean text rendering** — All text is perfectly legible and correctly spelled
6. **Platform-specific sizing** — Resized to exact dimensions (1200x628, 1080x1080, 1080x1920)

### V4 Ad Inventory (13 ads)

**Facebook (5):**
- `v4_fb_01_bold_offer` — "SAVE UP TO 40%" split layout with living room
- `v4_fb_02_photo_headline` — Twilight home + "4.9 Stars · 1,000+ Reviews"
- `v4_fb_03_seasonal_bold` — "SPRING WINDOW SALE" with cherry blossoms
- `v4_fb_04_comfort_lifestyle` — Cozy window seat + "FEEL THE DIFFERENCE INSIDE"
- `v4_fb_05_transformation_bold` — Colonial home + "TRANSFORM YOUR HOME"

**Instagram (5):**
- `v4_ig_01_stat_hero` — Bold navy "40%" stat card
- `v4_ig_02_photo_text` — Kitchen + "YOUR OLD WINDOWS ARE COSTING YOU"
- `v4_ig_03_bathroom_transformation` — Spa bathroom + "BATHROOM REMODEL"
- `v4_ig_04_social_proof` — Gold stars + "4.9 STARS / 1,000+ REVIEWS"
- `v4_ig_05_spring_offer` — Spring entrance + "SPRING SPECIAL"

**Instagram Stories (3):**
- `v4_igs_01_offer_vertical` — Twilight home + "FREE ESTIMATE + $500 GIFT CARD"
- `v4_igs_02_trust_vertical` — Navy + "4.9 STARS ON GOOGLE"
- `v4_igs_03_spring_vertical` — Spring home + "SPRING = WINDOW SEASON"

---

## Completed Tasks

| Task | Status | Notes |
|------|--------|-------|
| Draft ad copy (5 FB + 5 IG + 3 Stories) | ✅ Done | Energy, Trust, Spring, Comfort, Curb Appeal |
| V1: Generate raw base images | ✅ Done | Good stock photos but no branding |
| V2: Add branded overlays | ✅ Done | Heavy navy blocks + AI Nate = poor quality |
| Ad copy approved by Nate | ✅ Done | "Ad copy looks great" |
| V3: Editorial redesign | ✅ Done | Better photos, frosted glass overlays — still looked amateur |
| V4: Complete-in-one generation script | ✅ Done | `scripts/generate_v4_complete_ads.py` |
| V4: Generate 13 complete ads | ✅ Done | All text renders perfectly |
| V4: Resize to production dimensions | ✅ Done | `ad-drafts/v4-final/` — exact platform sizes |

## Pending Tasks

| Task | Status | Notes |
|------|--------|-------|
| Nate reviews V4 images | ⏳ Pending | Dramatic improvement — actual professional ad quality |
| Final approval from Nate | ⏳ Pending | |
| Upload to Facebook Ads Manager | ⏳ Pending | Use `ad-drafts/v4-final/facebook/` images |
| Upload to Instagram | ⏳ Pending | Use `ad-drafts/v4-final/instagram/` and `instagram-stories/` |
| Set targeting & budget | ⏳ Pending | SE Wisconsin homeowners |
| A/B test setup | ⏳ Pending | Run multiple angles simultaneously |

---

## Version History

### V1 — Raw Images (March 3, 2026)
- 13 photorealistic base images generated with Nano Banana 2
- No branding, no text overlays, no Nate, no CTA
- Nate feedback: "gorgeous images but they don't have any Window Depot of Milwaukee branding"

### V2 — Branded (March 3, 2026)
- Same base images + full branded overlay compositing via Pillow
- Added: Navy overlay, headlines, bullet points, phone number, CTA buttons, AI Nate cutout
- **Problems**: AI Nate wrong face, wrong logos, heavy overlays, too much text
- Nate feedback: "horrible"

### V3 — Editorial Redesign (March 13, 2026)
- New editorial photography prompts, frosted glass overlays, real Nate badge
- Still a two-step process (generate photo → overlay with Pillow)
- **Problems**: Pillow text rendering still looked amateur, frosted glass still looked cheap
- Nate feedback: "these look stupid as hell"

### V4 — Complete-in-One (March 13, 2026)
- **Breakthrough**: Gemini generates the ENTIRE finished ad in a single call
- All text is AI-rendered and naturally integrated into the design
- Multiple visual styles: bold offer, photo+headline, stat hero, social proof, seasonal
- Text rendering is clean, legible, and correctly spelled
- Resized to exact platform dimensions for production use
- **Quality**: Looks like professionally designed ads from a creative agency

---

## File Locations

| What | Where |
|------|-------|
| V4 raw generated ads | `ad-drafts/v4/{platform}/` |
| V4 production-ready (resized) | `ad-drafts/v4-final/{platform}/` |
| V4 generation script | `scripts/generate_v4_complete_ads.py` |
| V4 resize script | `scripts/resize_v4_final.py` |
| Previous versions (V1-V3) | `ad-drafts/facebook/`, `ad-drafts/instagram/`, `ad-drafts/instagram-stories/`, `ad-drafts/v3/` |

## How to Pick Up This Work

1. Read `AGENTS.md` first — full project context
2. Read this file — current status
3. V4 images are in `ad-drafts/v4-final/` (production-ready sizes)
4. To regenerate: `python3 scripts/generate_v4_complete_ads.py` then `python3 scripts/resize_v4_final.py`
5. To add new ads: extend the `ADS` list in `generate_v4_complete_ads.py`

### Key Technical Details
- Python 3.12 via `python3`
- Gemini API key is in env var `Gemini API Key`
- Model: `gemini-3.1-flash-image-preview` (Nano Banana 2)
- Install deps: `pip install google-genai Pillow`
