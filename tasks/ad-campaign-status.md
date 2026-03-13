# Ad Campaign — Status & Task Tracker

> Last updated: March 13, 2026
> Branch: `cursor/new-image-design-philosophy-2bc8`

---

## Current Status: V3 — NEW EDITORIAL DESIGN SYSTEM

V3 completely redesigns the image generation approach using "Scroll-Stopping Editorial" philosophy. See `scripts/IMAGE_DESIGN_PHILOSOPHY_V3.md` for full details.

### Key Changes from V2 → V3
1. **No more AI-generated Nate** — Uses real Nate headshot as circular badge only
2. **Editorial photography prompts** — Architectural Digest / Dwell Magazine quality
3. **Three-tier branding**: Paid (minimal pill), Organic (frosted bar + badge), Stories (text-forward)
4. **No heavy navy overlays** — Frosted glass effect instead
5. **Camera/lens references** in prompts for photographic realism
6. **No text on paid ad images** — Platform handles headline/CTA

---

## Completed Tasks

| Task | Status | Notes |
|------|--------|-------|
| Draft ad copy (5 FB + 5 IG + 3 Stories) | ✅ Done | Energy, Trust, Spring, Comfort, Curb Appeal |
| V1: Generate raw base images | ✅ Done | Good stock photos but no branding |
| V2: Add branded overlays | ✅ Done | Heavy navy blocks + AI Nate = poor quality |
| Ad copy approved by Nate | ✅ Done | "Ad copy looks great" |
| V3: New design philosophy doc | ✅ Done | `scripts/IMAGE_DESIGN_PHILOSOPHY_V3.md` |
| V3: New photo generation script | ✅ Done | `scripts/generate_v3_photos.py` |
| V3: New branded overlay script | ✅ Done | `scripts/generate_v3_branded.py` |
| V3: Generate 13 editorial base photos | ✅ Done | 5 FB + 5 IG + 3 Stories |
| V3: Generate 23 branded variants | ✅ Done | 10 paid + 10 organic + 3 stories |

## Pending Tasks

| Task | Status | Notes |
|------|--------|-------|
| Nate reviews V3 images | ⏳ Pending | Massive improvement over V2 |
| Final approval from Nate | ⏳ Pending | V3 should be close to production-ready |
| Upload to Facebook Ads Manager | ⏳ Pending | Use *_paid.png versions for ads |
| Set targeting & budget | ⏳ Pending | SE Wisconsin homeowners |
| A/B test setup | ⏳ Pending | Run multiple angles simultaneously |

---

## Version History

### V1 — Raw Images (March 3, 2026)
- 13 photorealistic base images generated with Nano Banana 2
- No branding, no text overlays, no Nate, no CTA
- Nate feedback: "gorgeous images but they don't have any Window Depot of Milwaukee branding"

### V2 — Branded (March 3, 2026)
- Same base images + full branded overlay compositing
- Added: Navy overlay, headlines, bullet points, phone number, CTA buttons, AI Nate cutout
- **Problems identified**: AI Nate doesn't look like real Nate, wrong logos on polo, heavy overlays, too much text, no visual variety
- Nate feedback: "horrible" — needs complete redesign

### V3 — Editorial Redesign (March 13, 2026)
- Completely new "Scroll-Stopping Editorial" philosophy
- 13 new editorial-quality base photos (NO people, NO text)
- Three-tier branding: Paid (tiny pill), Organic (frosted bar + real Nate badge), Stories (gradient + bold text)
- Uses real Nate headshot only — no more AI-generated figures
- Frosted glass effects instead of heavy navy overlays
- Camera/lens prompting for photographic realism
- 23 branded variants generated (10 paid + 10 organic + 3 stories)

---

## How to Pick Up This Work

If you're a new agent continuing this project:

1. Read `AGENTS.md` first — full project context
2. Read this file (`tasks/ad-campaign-status.md`) — current status
3. Read `ad-drafts/CAMPAIGN_OVERVIEW.md` — all ad copy + image pairings
4. Check the latest user messages for any new feedback or corrections
5. If Nate has corrections → modify `scripts/generate_branded_ads.py` and re-run
6. If new ads needed → extend the data structures in the scripts
7. If real Nate photo needed → use `brand-assets/nate-profile.png`, remove background with rembg, composite into ads

### Key Technical Details
- Python 3.12 via `python3`
- Gemini API key is in env var `Gemini API Key`
- Model: `gemini-3.1-flash-image-preview` (Nano Banana 2)
- Scripts: `scripts/generate_ads.py` (base images), `scripts/generate_branded_ads.py` (branded)
- Fonts: Helvetica Neue Bold at `/usr/share/fonts/truetype/macos/Helvetica.ttc`
- Install deps: `pip install google-genai Pillow rembg onnxruntime`
