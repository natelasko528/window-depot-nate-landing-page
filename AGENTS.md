# AGENTS.md — Window Depot USA Milwaukee

> Master context file for AI agents working on this project.
> Read this FIRST before doing anything.

---

## Project Overview

**Business**: Window Depot USA of Milwaukee — home improvement company (windows, doors, siding, roofing, flooring, bathrooms) serving SE Wisconsin.

**Owner**: Nate Lasko. Phone: (414) 312-5213. Email: nlasko.wdusa.milwaukee@gmail.com

**Website**: windowdepotmilwaukee.com | **Live landing page**: https://wdusa-nate-landing.vercel.app

**Repo**: `natelasko528/window-depot-nate-landing-page`

This project contains:
1. Nate's personal landing page (HTML/CSS/JS, deployed on Vercel)
2. AI chatbot knowledge base (`kb.js`)
3. Voice AI agent prompt (`WDUSA_VOICE_AGENT_PROMPT_ULTRA.md`)
4. Marketing playbook & SkillBoss integration (`SKILLBOSS_GUIDE.md`)
5. Social media image library (`social-media-images/`)
6. Facebook & Instagram ad campaign drafts (`ad-drafts/`)
7. Reusable brand assets (`brand-assets/`)
8. Generation scripts for bulk ad creation (`scripts/`)

---

## Directory Structure

```
/workspace/
│
├── AGENTS.md                          ← YOU ARE HERE — read first
├── README.md                          ← Project overview & deployment info
├── SKILLBOSS_GUIDE.md                 ← SkillBoss AI platform marketing playbook
├── WDUSA_VOICE_AGENT_PROMPT_ULTRA.md  ← GoHighLevel voice AI agent prompt
│
├── index.html                         ← Main landing page (dark theme, all-in-one)
├── index_lightmode.html               ← Light theme variant
├── kb.js                              ← AI chatbot knowledge base (MASTER_KNOWLEDGE_BASE)
│
├── vercel.json                        ← Vercel deployment config
├── package.json                       ← Node deps (skillboss-mcp-server)
├── mcp.json.example                   ← MCP server config template
├── .gitignore
│
├── nate-profile.png                   ← Nate's headshot (referenced by index.html — DO NOT MOVE)
│
├── brand-assets/                      ← Reusable brand assets
│   ├── nate-profile.png               ← Copy of Nate's headshot (for ad scripts)
│   ├── nate_pointing_right.png        ← AI-generated Nate pose (raw)
│   ├── nate_pointing_right_cutout.png ← AI-generated Nate (background removed)
│   ├── nate_arms_crossed.png
│   ├── nate_arms_crossed_cutout.png
│   ├── nate_thumbs_up.png
│   └── nate_thumbs_up_cutout.png
│
├── ad-drafts/                         ← Current Facebook & Instagram ad campaign
│   ├── CAMPAIGN_OVERVIEW.md           ← Full campaign doc — all copy + images + status
│   ├── ad_copy.json                   ← Structured ad copy (machine-readable)
│   ├── facebook/                      ← 5 FB ads (landscape 1200x628)
│   │   ├── fb_01_energy_savings.png   ← Base image (no branding)
│   │   ├── fb_01_branded.png          ← Final branded version
│   │   └── ...
│   ├── instagram/                     ← 5 IG feed ads (square 1080x1080)
│   │   ├── ig_01_energy_savings.png
│   │   ├── ig_01_branded.png
│   │   └── ...
│   └── instagram-stories/             ← 3 IG stories (vertical 1080x1920)
│       ├── igs_01_cta.png
│       ├── igs_01_branded.png
│       └── ...
│
├── social-media-images/               ← Prior social media generation (from earlier session)
│   ├── by-service/                    ← 18 images: 6 services × 3 platforms
│   │   ├── 01_windows_facebook.png
│   │   ├── 02_windows_instagram.png
│   │   └── ... (through 18_bathroom_linkedin.png)
│   ├── templates/                     ← Social post template images
│   │   ├── social-facebook-post.png
│   │   ├── social-instagram-post.png
│   │   └── social-linkedin-post.png
│   └── WindowDepot_SocialMedia_Package.docx
│
├── scripts/                           ← Reusable generation scripts
│   ├── generate_ads.py                ← Base image generation (Nano Banana 2)
│   └── generate_branded_ads.py        ← Branded overlay compositing (Pillow + NB2)
│
└── tasks/                             ← PRDs, task tracking, campaign status
    └── ad-campaign-status.md          ← Current campaign status & next steps
```

---

## Brand Identity — CRITICAL CONTEXT

Every agent MUST use these values consistently. Never deviate.

### Company
- **Name**: Window Depot USA of Milwaukee
- **Tagline**: "We Create Happy Customers" / "National Strength. Local Service."
- **Reputation**: 4.9 stars, 1,000+ Google reviews, #3 national remodeler, A+ BBB
- **USP**: Triple-pane windows at dual-pane prices. "America's Triple Pane Company."

### Nate Lasko (Owner / Sales Rep)
- **Phone**: (414) 312-5213 — this is the GoHighLevel AI appointment setter number
- **Email**: nlasko.wdusa.milwaukee@gmail.com
- **Real photo**: `brand-assets/nate-profile.png`
- **Personality**: Warm, no-pressure, family man, community-focused, expert

### Brand Colors
| Name         | Hex       | Usage                          |
|--------------|-----------|--------------------------------|
| Navy         | `#122040` | Primary — headers, overlays    |
| Brand Blue   | `#1E50A0` | CTA buttons, accents           |
| Light Blue   | `#64A0DC` | Phone number text, highlights  |
| White        | `#FFFFFF` | Headlines, body text on dark   |
| Gold         | `#D4AF37` | Accent, premium feel           |
| Dark Navy    | `#0A1628` | Landing page background        |
| Ivory        | `#FAFAF6` | Landing page light background  |

### Brand Voice
- Warm, expert, neighborly — like a knowledgeable friend
- Milwaukee/SE Wisconsin references are natural
- Confident but never arrogant
- NEVER pushy, NEVER high-pressure sales language
- ALWAYS end with a soft, natural call-to-action
- Use "Nate" naturally: "Nate can show you that in person"

### Current Promotions (update as needed)
- FREE in-home estimate
- $500 gift card with every estimate booked through Nate
- Price locked for 1 full year — zero risk
- Triple-pane at dual-pane prices

### Services (all 6)
1. **Windows** — ProVia Endure vinyl replacement windows (triple-pane specialty)
2. **Doors** — ProVia fiberglass/steel entry doors + patio doors
3. **Siding** — CraneBoard, Market Square, ASCEND composite cladding
4. **Roofing** — Asphalt shingles (NorthGate) + ProVia metal roofing
5. **Flooring** — Hardwood, LVP, laminate, carpet
6. **Bathrooms** — Bath Makeover acrylic remodels (installed in 1 day)

### Showrooms (7 locations)
St. Francis (HQ), Waukesha, Greenfield, Oak Creek, Wauwatosa, Mukwonago, Portage/Madison

---

## Key Files — What Each One Does

| File | Purpose | When to Read |
|------|---------|-------------|
| `kb.js` | Master knowledge base — every product spec, FAQ, objection handler, testimonial | When writing ANY content about Window Depot |
| `SKILLBOSS_GUIDE.md` | Marketing playbook with prompt templates for batch content | When generating social posts, ads, email campaigns |
| `WDUSA_VOICE_AGENT_PROMPT_ULTRA.md` | GoHighLevel voice AI agent prompt | When working on voice/phone AI features |
| `ad-drafts/CAMPAIGN_OVERVIEW.md` | Full ad campaign documentation with all copy + image pairings | When working on Facebook/Instagram ads |
| `ad-drafts/ad_copy.json` | Structured ad copy data (machine-readable) | When programmatically accessing ad copy |
| `tasks/ad-campaign-status.md` | Current campaign progress and next steps | When picking up ad campaign work |
| `tasks/ghl-api-reference.md` | Verified GHL Social Planner API endpoints, schemas, live data | When working on dashboard or GHL integration |
| `tasks/prd-owner-dashboard.md` | Owner dashboard PRD with screen mesh layout | When working on the dashboard |

---

## Image Generation — How It Works

### Technology Stack
- **Nano Banana 2** (Gemini 3.1 Flash Image) via `google-genai` Python SDK
- **Pillow** (PIL) for compositing, text overlays, branding
- **rembg** for background removal on cutout images

### API Access
- **Gemini API Key**: Set as Cursor Cloud Agent secret named `Gemini API Key`
- The key is accessed via `os.environ.get("Gemini API Key")` in Python scripts
- Model ID: `gemini-3.1-flash-image-preview`

### Generation Scripts

**`scripts/generate_ads.py`** — Generates base lifestyle/product images
- Outputs raw images (no branding) to `ad-drafts/{platform}/`
- Uses detailed prompts for each ad angle (energy, trust, seasonal, comfort, curb appeal)
- Handles retries and error recovery

**`scripts/generate_branded_ads.py`** — Adds branding, Nate, text overlays
- Reads raw images from `ad-drafts/{platform}/`
- Generates AI Nate cutouts (navy polo, various poses)
- Removes backgrounds with rembg
- Composites: navy overlay + headline + bullets + phone + CTA button + Nate + brand line
- Outputs `*_branded.png` files alongside raw originals

### To Re-Run Generation
```bash
cd /workspace
pip install google-genai Pillow rembg onnxruntime
python3 scripts/generate_ads.py           # Step 1: base images
python3 scripts/generate_branded_ads.py   # Step 2: branded overlays
```

### Image Sizes by Platform
| Platform          | Dimensions    | Script Size    |
|-------------------|---------------|----------------|
| Facebook Feed     | 1200×628      | `1376x768` raw → `1200x628` branded |
| Instagram Feed    | 1080×1080     | `1024x1024` raw → `1080x1080` branded |
| Instagram Stories | 1080×1920     | `768x1376` raw → `1080x1920` branded |

---

## Cursor Cloud Specific Instructions

### Environment Setup
- **Python 3.12** is available as `python3`
- pip packages install to `~/.local/` — may need `~/.local/bin` on PATH
- Fonts: Helvetica Neue (Bold, Condensed Bold, etc.) at `/usr/share/fonts/truetype/macos/Helvetica.ttc`
- System has `rg` (ripgrep) pre-installed

### Required Python Packages
```
google-genai
Pillow
rembg
onnxruntime
```

### Required Secrets (Cursor Dashboard > Cloud Agents > Secrets)
| Secret Name       | Purpose                                    |
|-------------------|--------------------------------------------|
| `Gemini API Key`  | Google Gemini API for Nano Banana 2 images  |
| `GHL_API_TOKEN`   | GoHighLevel Private Integration Token (PIT) |
| `GHL_LOCATION_ID` | GoHighLevel sub-account location ID         |

### MCP Servers (Optional — for local Cursor use, not Cloud Agents)
- **SkillBoss**: `skillboss-mcp-server` — requires `SKILLBOSS_API_KEY`
- Config template: `mcp.json.example`

### No Build Step Required
- The landing page is pure HTML/CSS/JS — no bundler, no framework
- Deployed on Vercel with `vercel.json` config (includes serverless functions in `api/`)
- Every push to `main` auto-deploys

### Testing the Landing Page
- The landing page uses Vercel Analytics and Facebook Meta Pixel (ID: 232929617735426)
- GHL booking widget iframe and chat widget are embedded in `index.html`
- To test locally: just open `index.html` in a browser

### Owner Dashboard
- Private performance dashboard at `/owner` (login) and `/owner/dashboard`
- Auth: password-protected via `OWNER_PASSWORD` env var, JWT sessions via `SESSION_SECRET`
- Data: fetches from GHL Social Planner API; falls back to demo data when GHL not configured
- Serverless functions in `api/` directory (Vercel auto-deploys)
- Full API reference: `tasks/ghl-api-reference.md`

---

## Current Project State (as of March 2026)

### Completed
- Landing page (dark + light themes) — DEPLOYED on Vercel
- AI chatbot knowledge base (`kb.js`) — COMPLETE
- Voice AI agent prompt — COMPLETE
- SkillBoss marketing playbook — COMPLETE
- Social media image library (18 images, 6 services × 3 platforms) — COMPLETE
- V4 ad campaign creatives — 13 complete-in-one ads (text baked in by Gemini)
- Private owner performance dashboard at `/owner` — auth, API, UI built
- GHL Social Planner API verified and documented (`tasks/ghl-api-reference.md`)

### In Progress
- Dashboard GHL live data integration (connecting `/accounts`, `/posts/list`, `/statistics`)
- Ad campaign awaiting Nate's final approval

### Known Issues / Next Steps
1. Dashboard currently shows demo data — needs GHL API wiring completed
2. GHL has 428 posts across FB/IG/LI/Google/YouTube; 334+ published
3. Statistics endpoint returns 7-day aggregate only — no per-post metrics via API
4. Vercel env vars needed for live dashboard: `OWNER_PASSWORD`, `SESSION_SECRET`, `GHL_API_TOKEN`, `GHL_LOCATION_ID`

---

## GoHighLevel Social Planner API — Quick Reference

> Full docs: `tasks/ghl-api-reference.md` (verified against official OpenAPI spec + live calls)

### Base URL & Auth
```
Base: https://services.leadconnectorhq.com
Auth: Authorization: Bearer {GHL_API_TOKEN}
Header: Version: 2021-07-28
Rate: 100 requests / 10 seconds
```

### Endpoints

| Method | Path | Purpose |
|--------|------|---------|
| GET | `/social-media-posting/{locationId}/accounts` | List connected accounts (returns `id`, `profileId`, `platform`, `name`) |
| POST | `/social-media-posting/{locationId}/posts/list` | List posts with pagination/filtering |
| GET | `/social-media-posting/{locationId}/posts/{id}` | Get single post |
| POST | `/social-media-posting/statistics?locationId={locationId}` | Aggregate analytics (7-day with delta) |

### posts/list — Required Body Fields (all strings)
```json
{ "skip": "0", "limit": "100", "fromDate": "2026-01-01T00:00:00.000Z", "toDate": "2026-12-31T23:59:59.000Z", "includeUsers": "false" }
```
Optional: `type` (published/scheduled/all), `accounts` (comma-separated IDs), `postType` (post/story/reel)

### statistics — Required Body
```json
{ "profileIds": ["profileId_from_accounts_endpoint"] }
```
Note: `locationId` goes as a **query parameter**, not in the body. `profileIds` come from the `profileId` field in `/accounts`, NOT the `id` field.

### Post Object Key Fields
`_id`, `platform` (facebook/instagram/linkedin/google/youtube), `status` (published/scheduled/failed), `summary` (caption), `media[]` ({url,type}), `accountIds[]`, `parentPostId` (groups multi-platform), `scheduleDate`, `publishedAt`

### Statistics Response Key Fields
`totals` (posts/likes/followers/impressions/comments), `breakdowns.{metric}.platforms.{platform}` ({value,change}), `breakdowns.engagement.{platform}` ({likes,comments,shares,change}), `postPerformance` (daily arrays), `platformTotals` (per-platform daily series), `demographics` (gender/age)

### Nate's Connected Accounts
| Platform | Name | profileId |
|----------|------|-----------|
| facebook | RevolutionAi | `6976d1f211a9c01a61bd6f42` |
| facebook | Happy Homes of Wisconsin | `697db4bb50434332a0a0c76b` |
| facebook | Lasko Health Solutions | `697db4eecd609119536316ea` |
| facebook | Daily Motivation and Inspiration | `6976d1cf287ff09169274459` |
| instagram | natelasko528 | `6933846d95529a7a63da72ad` |
| linkedin | Nate Lasko | `696efc1c4904d28f212f3a76` |
| youtube | Nate Lasko | `696efc35c715df2e5c3b5bd8` |

### Important Notes
- **posts/list does NOT return engagement metrics** — only post metadata
- **statistics gives 7-day aggregate only** — no per-post engagement breakdown via API
- **parentPostId** groups the same content across platforms (1 parent = N platform posts)
- Posts total: 428 (334+ published, ~90 scheduled, 4 failed)

---

## Agent Behavioral Guidelines

### When Working on Ads
1. ALWAYS read `ad-drafts/CAMPAIGN_OVERVIEW.md` first to see current state
2. ALWAYS read `tasks/ad-campaign-status.md` to see what needs doing next
3. Use `kb.js` as the source of truth for all product claims, stats, and company info
4. Never make up pricing, statistics, or claims not in the knowledge base
5. Follow the brand voice guidelines above strictly

### When Working on the Landing Page
1. Read `index.html` before making changes
2. Use the CSS variables defined at the top of `index.html`
3. Phone number is (414) 312-5213 — this links to GHL AI appointment setter
4. GHL booking widget and chat widget IDs are in the HTML — don't change without explicit instruction

### When Generating Images
1. Use Nano Banana 2 via the `google-genai` SDK (model: `gemini-3.1-flash-image-preview`)
2. Always save raw (unbranded) AND branded versions
3. Use the scripts in `scripts/` as templates — extend, don't rewrite from scratch
4. For Nate's figure: prefer using `brand-assets/nate-profile.png` with background removal

### When Writing Copy
1. Tone: warm, local, trustworthy, zero pressure
2. Always include a soft CTA — never "ACT NOW" or "LIMITED TIME!!!"
3. Always reference the $500 gift card, 12-month price lock, and free estimate
4. Milwaukee/SE Wisconsin specifics are encouraged
5. Hashtags: 10-15 per Instagram post, none on Facebook, max 3 on LinkedIn

### When Working on the Dashboard / GHL Integration
1. ALWAYS read `tasks/ghl-api-reference.md` first — it has verified endpoint schemas and live examples
2. Use `GHL_API_TOKEN` (not `GHL_API_KEY`) — this is the env var name for the Private Integration Token
3. The env var `GHL_LOCATION_ID` contains the location ID (`Rkjt05VeS56IUr5caLBD`)
4. posts/list body fields (skip, limit, fromDate, toDate, includeUsers) are ALL strings, not numbers
5. statistics endpoint takes `locationId` as a **query parameter** and `profileIds` in the body
6. `profileIds` come from the `profileId` field in `/accounts`, NOT the `id` field
7. Individual post engagement metrics are NOT available via the GHL API — only aggregate stats from `/statistics`
8. Auth system uses JWT via `api/_lib/auth.js` — no external dependencies
9. Dashboard files: `owner/index.html` (login), `owner/dashboard.html` (main dashboard)
10. API functions: `api/auth/`, `api/performance/`, `api/cron/`

### When the User Says "King Mode" or "ULTRATHINK"
- Go all-out. Maximum depth, maximum quality, maximum thoroughness.
- This is not a shortcut request — it means spare no effort.
