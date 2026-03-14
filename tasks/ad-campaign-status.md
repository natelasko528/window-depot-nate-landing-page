# Ad Campaign — Status & Task Tracker

> Last updated: March 3, 2026
> Branch: `cursor/ad-copy-and-image-drafts-f377`

---

## Current Status: DRAFT V2 — AWAITING APPROVAL

The second draft (V2) of the Facebook & Instagram ad campaign is complete. V1 had beautiful base images but lacked branding. V2 adds full Window Depot branding, Nate figure, CTAs, and phone number.

---

## Completed Tasks

| Task | Status | Notes |
|------|--------|-------|
| Draft Facebook ad copy (5 variations) | ✅ Done | Energy, Trust, Spring, Comfort, Curb Appeal angles |
| Draft Instagram feed copy (5 variations) | ✅ Done | With hashtags, CTAs, emojis |
| Draft Instagram Stories copy (3 variations) | ✅ Done | CTA, Social Proof, Seasonal |
| Generate base images with Nano Banana 2 | ✅ Done | 13 raw images (5 FB + 5 IG + 3 Stories) |
| Generate AI Nate cutouts (3 poses) | ✅ Done | Pointing, arms crossed, thumbs up |
| Background removal on Nate cutouts | ✅ Done | Using rembg |
| Build branded Facebook ads (5) | ✅ Done | Navy overlay + headline + bullets + phone + CTA + Nate |
| Build branded Instagram feed ads (5) | ✅ Done | Top/bottom gradient + branding |
| Build branded Instagram Stories (3) | ✅ Done | Full vertical layout with branding |
| Ad copy approved by Nate | ✅ Done | "Ad copy looks great" — approved in session |
| Organize project directory structure | ✅ Done | See AGENTS.md for full structure |
| Create AGENTS.md for future sessions | ✅ Done | Comprehensive agent context file |
| Update CAMPAIGN_OVERVIEW.md | ✅ Done | Full copy + image pairings |
| Build V3 platform post copy pack | ✅ Done | Facebook + Instagram + LinkedIn conversion-focused copy for all 30 creatives |
| Build staggered GHL posting schedule | ✅ Done | 90 scheduled slots (30 posts × 3 platforms), CT timezone |
| Schedule V3 posts in GoHighLevel | ✅ Done | Queued via Social Planner API for RevolutionAi location |

## Pending Tasks

| Task | Status | Notes |
|------|--------|-------|
| Nate reviews branded images | ⏳ Pending | V2 images shown in chat, awaiting feedback |
| Replace AI Nate with real photo | ⏳ Pending | AI figure has generic polo logos; need real cutout |
| Final approval from Nate | ⏳ Pending | May need V3 with corrections |
| Upload to Facebook Ads Manager | ⏳ Pending | After approval |
| Set targeting & budget | ⏳ Pending | SE Wisconsin homeowners |
| A/B test setup | ⏳ Pending | Run multiple angles simultaneously |
| Monitor first 72 hours of scheduled rollout | ⏳ Pending | Review CTR, saves, comments, and outbound clicks by platform |

---

## Version History

### V1 — Raw Images (March 3, 2026)
- 13 beautiful photorealistic base images generated with Nano Banana 2
- No branding, no text overlays, no Nate, no CTA
- Nate feedback: "gorgeous images but they don't have any Window Depot of Milwaukee branding"

### V2 — Branded (March 3, 2026)
- Same base images + full branded overlay compositing
- Added: Navy overlay, headlines, bullet points, phone number, CTA buttons, Nate cutout, brand line
- Used Pillow for compositing, rembg for background removal
- Nate feedback: Pending

### V3 — Photo-First Reset (March 13, 2026)
- New creative direction focused on photo-first composition and reduced template feel
- Added enhanced prompt architecture in `scripts/generate_30_post_backgrounds_nb2.py`
- Added new renderer `scripts/render_30_post_brand_v3.py` using real Nate headshot badge (`brand-assets/nate-profile.png`)
- Generated fresh preview set in `ad-drafts/30-posts/branded-v3/` with contact sheet
- Added platform-ready copy + schedule artifacts for GoHighLevel:
  - `ad-drafts/30-posts/v3_platform_post_copy.json`
  - `ad-drafts/30-posts/v3_ghl_staggered_schedule.csv`
  - `ad-drafts/30-posts/V3_GHL_POSTING_PLAN.md`
  - `ad-drafts/30-posts/PROMPT_GHL_EXECUTION_V3.md`
- Re-ran GHL scheduling reset to guarantee 30 Facebook + 30 Instagram + 30 LinkedIn scheduled entries with platform-tailored copy, and recorded refreshed confirmation artifacts
- Status: Ready for Nate review and refinement feedback

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
