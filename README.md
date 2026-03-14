# Window Depot USA Milwaukee — Nate's Landing Page & Marketing Hub

## About
Official landing page and marketing asset hub for Nate Lasko at Window Depot USA of Milwaukee. The landing page is pure HTML/CSS/JS (no frameworks, no build step). Marketing content is generated with AI (Nano Banana 2, SkillBoss).

**Live Site**: https://wdusa-nate-landing.vercel.app

---

## Project Structure

```
├── AGENTS.md                          ← AI agent context (read this first in new sessions)
├── README.md                          ← This file
├── SKILLBOSS_GUIDE.md                 ← SkillBoss AI marketing playbook
├── WDUSA_VOICE_AGENT_PROMPT_ULTRA.md  ← Voice AI agent prompt (GoHighLevel)
│
├── index.html                         ← Main landing page (dark theme)
├── index_lightmode.html               ← Light theme variant
├── kb.js                              ← AI chatbot knowledge base
│
├── vercel.json                        ← Vercel deployment config
├── package.json                       ← Node deps (skillboss-mcp-server)
├── mcp.json.example                   ← MCP config template for SkillBoss
│
├── nate-profile.png                   ← Nate's headshot (used by index.html — DO NOT MOVE)
│
├── brand-assets/                      ← Brand photos & cutouts
│   ├── nate-profile.png               ← Copy of headshot (for ad scripts)
│   └── nate_*_cutout.png              ← AI-generated cutouts (3 poses)
│
├── ad-drafts/                         ← Facebook & Instagram ad campaign
│   ├── CAMPAIGN_OVERVIEW.md           ← Full campaign doc (copy + images)
│   ├── ad_copy.json                   ← Machine-readable ad copy
│   ├── facebook/                      ← 5 landscape ads (raw + branded)
│   ├── instagram/                     ← 5 square ads (raw + branded)
│   └── instagram-stories/             ← 3 vertical ads (raw + branded)
│
├── social-media-images/               ← Social media image library
│   ├── by-service/                    ← 18 images (6 services × 3 platforms)
│   ├── templates/                     ← Post templates
│   └── WindowDepot_SocialMedia_Package.docx
│
├── scripts/                           ← AI generation scripts
│   ├── generate_ads.py                ← Base image gen (Nano Banana 2)
│   └── generate_branded_ads.py        ← Branded overlay compositing
│
└── tasks/                             ← Campaign status & task tracking
    └── ad-campaign-status.md
```

---

## SkillBoss Integration

This project includes [SkillBoss](https://skillboss.co) — a unified AI platform (100+ models) for generating social media posts, ad copy, images, voiceovers, and more through Cursor's MCP protocol.

**Quick setup:**
1. Get your API key at [skillboss.co/console](https://skillboss.co/console)
2. Copy `mcp.json.example` to `.cursor/mcp.json`
3. Replace `YOUR_KEY_HERE` with your key
4. Restart Cursor

See **[SKILLBOSS_GUIDE.md](SKILLBOSS_GUIDE.md)** for the full marketing playbook.

---

## Ad Generation (Nano Banana 2)

The ad campaign uses Google's Nano Banana 2 (Gemini 3.1 Flash Image) for image generation and Pillow for branded compositing.

**Prerequisites:**
```bash
pip install google-genai Pillow rembg onnxruntime
```

**Requires**: `Gemini API Key` environment variable (set in Cursor Cloud Agent secrets)

**Run:**
```bash
python3 scripts/generate_ads.py           # Generate base images
python3 scripts/generate_branded_ads.py   # Add branding + Nate + CTAs
```

---

## Deploying to Vercel
1. Connect this GitHub repo to Vercel at vercel.com/new
2. Vercel auto-detects the config — zero setup needed
3. Every push to `main` auto-deploys

---

## Owner Dashboard + Monitoring (Deployment/Ops)

### Owner routes
- `/owner` → owner login route
- `/owner/dashboard` → private dashboard route

### Required environment variables
- `OWNER_DASHBOARD_PASSWORD` (owner login password)
- `SESSION_SECRET` (signs/encrypts owner session cookie)
- `GHL_API_TOKEN` (GoHighLevel API access)
- `GHL_LOCATION_ID` (GoHighLevel location context)
- Optional: `CURSOR_AGENT_WEBHOOK_URL` (owner chat handoff webhook), `CRON_SHARED_SECRET` (cron request guard)

### Cron behavior
- `/api/cron/sync-performance` runs hourly (`0 * * * *`)
- `/api/cron/evaluate-alerts` runs every 30 minutes (`*/30 * * * *`)
- Cron schedules are evaluated in UTC by Vercel.

### Local testing commands
```bash
# start local Vercel runtime
vercel dev

# quick route checks
curl -i http://localhost:3000/owner
curl -i http://localhost:3000/owner/dashboard

# cron endpoint checks
curl -i http://localhost:3000/api/cron/sync-performance
curl -i http://localhost:3000/api/cron/evaluate-alerts
```

### Security notes
- Keep owner routes private; do not expose credentials client-side.
- Use a strong unique `OWNER_DASHBOARD_PASSWORD` and high-entropy `SESSION_SECRET`.
- Rotate password, session secret, and API token regularly and after access changes.
- Restrict Vercel project access to authorized operators only.

Runbook: `tasks/owner-dashboard-runbook.md`.

---

## Contact Info
- **Nate Lasko**: (414) 312-5213 | nlasko.wdusa.milwaukee@gmail.com
- **Website**: windowdepotmilwaukee.com
- **Company**: Window Depot USA of Milwaukee

## Key CSS Variables (landing page)
```css
--navy: #0A1628      /* dark navy */
--gold: #B8900A      /* dark gold */
--gold2: #D4AF37     /* bright gold */
--ivory: #FAFAF6     /* page background */
```
