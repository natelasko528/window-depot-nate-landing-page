# SkillBoss — Setup, General Usage & Marketing Playbook

> One platform. 100+ AI models. Pay once, use everywhere.
> **Website**: [skillboss.co](https://skillboss.co) | **Console**: [skillboss.co/console](https://skillboss.co/console) | **Docs**: [skillboss.co/docs](https://skillboss.co/docs)

---

## Table of Contents

1. [What Is SkillBoss?](#what-is-skillboss)
2. [Quick-Start Setup](#quick-start-setup)
3. [Available Tools & Models](#available-tools--models)
4. [General Usage](#general-usage)
5. [Marketing Yourself — Strategy & Playbook](#marketing-yourself--strategy--playbook)
6. [Mass Social Media Post Creation](#mass-social-media-post-creation)
7. [Ad Creation at Scale](#ad-creation-at-scale)
8. [Platform-Specific Guides](#platform-specific-guides)
9. [Prompt Templates & Recipes](#prompt-templates--recipes)
10. [Cost Optimization Tips](#cost-optimization-tips)
11. [Troubleshooting](#troubleshooting)

---

## What Is SkillBoss?

SkillBoss is a unified AI gateway that gives you access to **100+ AI models and services** through a single API key and credit balance. Instead of juggling separate accounts for ChatGPT, Claude, DALL-E, ElevenLabs, Flux, web scrapers, and email tools, you top up once on SkillBoss and use everything.

**Why it matters for marketing:**

- **Image Generation** — Create social media graphics, ads, and banners with DALL-E 3 or Flux
- **Copywriting** — Use Claude 4.5 Sonnet, GPT-5, or Gemini to write ad copy, captions, and blog posts
- **Web Scraping** — Pull competitor data, trending content, and audience insights from LinkedIn, Instagram, Facebook, X, and Yelp
- **Video Generation** — Create short promo clips with Google Veo or MiniMax
- **Text-to-Speech** — Generate voiceovers for ads and reels with ElevenLabs or OpenAI TTS
- **Email Campaigns** — Send bulk marketing emails via AWS SES integration
- **Document Generation** — Build pitch decks and eBooks with Gamma

SkillBoss is **100% open source** and works natively with **Cursor**, Claude Code, and Windsurf through its MCP (Model Context Protocol) server.

---

## Quick-Start Setup

### 1. Get Your API Key

1. Go to [skillboss.co/console](https://skillboss.co/console)
2. Sign up (free tier includes **20 credits** to start)
3. Copy your API key from the console dashboard

### 2. Install the MCP Server

The MCP server is already added to this project. To use it in Cursor:

**Option A — Project-level config (already done)**

Copy `mcp.json.example` from the project root to `.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "skillboss": {
      "command": "npx",
      "args": ["-y", "skillboss-mcp-server"],
      "env": {
        "SKILLBOSS_API_KEY": "YOUR_KEY_HERE"
      }
    }
  }
}
```

Replace `YOUR_KEY_HERE` with your actual API key from the SkillBoss console.

**Option B — Global config (all Cursor projects)**

Open Cursor → Settings → Features → MCP Servers → Add Server, and paste:

```json
{
  "skillboss": {
    "command": "npx",
    "args": ["-y", "skillboss-mcp-server"],
    "env": {
      "SKILLBOSS_API_KEY": "sk-your-key-here"
    }
  }
}
```

**Option C — Claude Code**

```bash
claude mcp add skillboss --command "npx" --args "-y,skillboss-mcp-server" --env "SKILLBOSS_API_KEY=sk-your-key-here"
claude mcp list   # verify
```

### 3. Top Up Credits

Go to [skillboss.co/pricing](https://skillboss.co/pricing) and add credits:

| Package       | Price  | Per-Credit Cost |
|---------------|--------|-----------------|
| 200 credits   | $15    | $0.075          |
| 500 credits   | $25    | $0.050          |
| 800 credits   | $40    | $0.050          |
| 1,200 credits | $56    | $0.047          |

### 4. Verify It Works

In Cursor's chat, type:

> "Use SkillBoss to check my balance"

or

> "Use SkillBoss to list available models"

If you see a response with models or balance info, you're live.

---

## Available Tools & Models

### MCP Server Tools

| Tool              | What It Does                                                    |
|-------------------|-----------------------------------------------------------------|
| `chat`            | Send messages to 50+ LLMs (Claude, GPT-5, Gemini, DeepSeek)    |
| `list_models`     | See all available models with pricing                           |
| `generate_image`  | Create images with DALL-E 3 or Flux                             |
| `text_to_speech`  | Convert text to audio with ElevenLabs or OpenAI TTS             |
| `get_balance`     | Check your current credit balance                               |
| `recommend_model` | Get the best model recommendation for your specific task        |

### Platform Services (via API)

Beyond the MCP tools, SkillBoss provides direct API access to:

| Category          | Services                                                        | Credits/Use      |
|-------------------|-----------------------------------------------------------------|------------------|
| Image Generation  | DALL-E 3, Flux Schnell, Flux Dev, Gemini, Wan Image             | 0.1–2.9/image    |
| Video Generation  | Google Veo 3.1, MiniMax, Wan Video                              | 3.6/sec (Veo)    |
| Chat / LLM        | Claude 4.6 Opus, GPT-5, Gemini 2.5 Flash, DeepSeek V3, Qwen   | Token-based      |
| Web Scraping      | LinkedIn, Instagram, X, Facebook, Yelp, Discord, Firecrawl      | 0.2–0.5/scrape   |
| Audio / TTS       | ElevenLabs Multilingual, OpenAI TTS                             | Per-character     |
| Email             | AWS SES (single + bulk)                                         | Per-send          |
| Documents         | Gamma (presentations, eBooks)                                   | Per-generation    |
| Storage           | Cloudflare R2 uploads                                           | Per-upload        |

### Top Chat Models for Marketing Copy

| Model                       | Best For                              | Cost (Input/Output per 1M tokens) |
|-----------------------------|---------------------------------------|-----------------------------------|
| `bedrock/claude-4-5-sonnet` | Complex reasoning, brand voice, long-form | $3.00 / $15.00                |
| `gpt-5`                     | Creative ad copy, trending language   | $15.00 / $15.00                   |
| `gemini-2.5-flash`          | Fast drafts, bulk generation          | $0.10 / $0.40                     |
| `deepseek/deepseek-v3`      | Budget batch processing               | $0.27 / $0.27                     |
| `gpt-4o-mini`               | High volume, low cost                 | $0.15 / $0.60                     |

---

## General Usage

### Talking to AI Models

Ask Cursor to use SkillBoss for any AI task:

```
"Use SkillBoss chat with Claude to write a professional bio for my LinkedIn"
```

```
"Use SkillBoss chat with GPT-5 to brainstorm 10 taglines for a home improvement company"
```

```
"Use SkillBoss to recommend the best model for writing marketing emails"
```

### Generating Images

```
"Use SkillBoss to generate an image: Professional home improvement company ad showing a modern kitchen with new windows, warm lighting, clean lines, hero banner style"
```

You can specify:
- **Model**: `dall-e-3` (high quality, follows prompts closely) or `flux` (fast, artistic)
- **Size**: `1024x1024` (square/Instagram), `1792x1024` (landscape/Facebook), `1024x1792` (portrait/Stories)

### Text-to-Speech

```
"Use SkillBoss text-to-speech to say: Get your free in-home estimate today. Call Nate at 414-312-5213."
```

Voices: `alloy`, `echo`, `fable`, `onyx`, `nova`, `shimmer`

### Checking Balance

```
"Use SkillBoss to check my balance"
```

Or visit [skillboss.co/console](https://skillboss.co/console) directly.

---

## Marketing Yourself — Strategy & Playbook

### Personal Brand Framework

Use SkillBoss to build and amplify your personal brand across all channels. Here's the framework:

#### Step 1 — Define Your Brand Voice

Ask Claude to help crystallize your brand:

```
Use SkillBoss chat with Claude:
"I'm Nate Lasko, owner of Window Depot USA of Milwaukee. I'm a family man,
community-focused, no-pressure sales approach. We're the #3 national remodeler
with 4.9 stars and 1000+ Google reviews. Help me define a brand voice guide
that covers: tone, vocabulary, key phrases to use/avoid, and personality traits.
Make it usable for social media, ads, and email."
```

#### Step 2 — Content Pillar Strategy

Generate a content strategy organized around pillars:

```
Use SkillBoss chat with Claude:
"Create a content pillar strategy for a home improvement company owner in Milwaukee.
Pillars should include: Educational (home tips), Behind-the-Scenes (team/family),
Social Proof (reviews/results), Community (local events), and Promotional (offers).
For each pillar, give me 10 specific post ideas with captions."
```

#### Step 3 — Competitor Research

Use SkillBoss scrapers to analyze what competitors are doing:

**LinkedIn Profile Analysis:**
```
Use the SkillBoss API to scrape LinkedIn profiles of top home improvement companies
in the Milwaukee area. Analyze their posting frequency, content types, and engagement.
```

**Yelp/Google Review Mining:**
```
Scrape competitor Yelp listings to identify common complaints and unmet needs
that I can address in my marketing.
```

#### Step 4 — Content Calendar

```
Use SkillBoss chat with Claude:
"Build me a 30-day social media content calendar for Window Depot USA Milwaukee.
Include posts for Facebook, Instagram, and LinkedIn. Mix educational tips,
customer testimonials, behind-the-scenes, community posts, and promotional offers.
Include the best posting times for each platform. Format as a table."
```

---

## Mass Social Media Post Creation

This is where SkillBoss really shines. You can batch-generate dozens of posts in minutes.

### The Batch Workflow

#### 1. Generate Bulk Copy

Use a fast, cheap model for initial drafts, then refine with a premium model:

```
Use SkillBoss chat with model gemini-2.5-flash:
"Generate 20 Facebook posts for Window Depot USA of Milwaukee.
Mix these types:
- 5 educational (home improvement tips for Wisconsin homeowners)
- 5 social proof (formats for sharing 5-star reviews)
- 5 promotional (free estimate offer, $500 gift card, price-lock guarantee)
- 5 seasonal (spring/summer home prep for Milwaukee weather)

Each post should be 2-3 short paragraphs, include a call-to-action,
and use emojis sparingly. Tone: warm, local, trustworthy, zero pressure.
Include hashtag suggestions for each."
```

#### 2. Adapt for Each Platform

Take those posts and reformat for every channel:

```
Use SkillBoss chat with Claude:
"Here are 20 Facebook posts [paste them]. Now adapt each one for:
1. Instagram (shorter, more visual language, 5-10 relevant hashtags)
2. LinkedIn (professional tone, industry insights, no hashtag spam)
3. X/Twitter (under 280 characters, punchy, with 1-2 hashtags)

Output as a spreadsheet-ready format: Platform | Post Text | Hashtags | CTA"
```

#### 3. Generate Matching Images

For each post, generate a custom image:

```
Use SkillBoss to generate an image:
"Professional photo-realistic image of a beautiful Milwaukee home with new energy-efficient triple-pane windows, warm interior lighting visible through windows, autumn leaves in the yard, golden hour lighting. Style: real estate photography, aspirational, clean."
```

**Batch image prompts by service category:**

| Category   | Image Prompt Focus                                                        |
|------------|---------------------------------------------------------------------------|
| Windows    | Modern homes with new windows, before/after, energy savings visualization |
| Doors      | Elegant entryways, curb appeal transformation, ProVia door closeups       |
| Siding     | Full exterior transformations, color options, weather protection           |
| Roofing    | Aerial views, storm damage vs. new roof, material closeups                |
| Flooring   | Room transformations, material textures, family-friendly scenes           |
| Bathroom   | Modern remodels, before/after, spa-like aesthetics                        |

#### 4. Generate Voiceovers for Video Posts

```
Use SkillBoss text-to-speech with voice nova:
"Hey Milwaukee! Did you know that upgrading to triple-pane windows can cut your
energy bills by up to 30 percent? At Window Depot USA, we offer triple-pane
at dual-pane prices. Call Nate at 414-312-5213 for your free estimate today."
```

### Automation Template: 30 Posts in 30 Minutes

Follow this sequence to produce a full month of content:

1. **Minutes 0–5**: Use `chat` with `gemini-2.5-flash` to generate 30 raw post concepts (one per day)
2. **Minutes 5–10**: Use `chat` with `bedrock/claude-4-5-sonnet` to refine the top posts and add brand voice
3. **Minutes 10–15**: Use `chat` to adapt all 30 posts for Facebook, Instagram, and LinkedIn (90 total)
4. **Minutes 15–25**: Use `generate_image` to create 10–15 key images (reuse across similar posts)
5. **Minutes 25–30**: Use `text_to_speech` to create 3–5 voiceovers for video/reel posts

**Result**: 90 platform-ready posts + images + voiceovers, ready to schedule.

---

## Ad Creation at Scale

### Facebook/Instagram Ads

#### Generate Ad Copy Variations

A/B testing requires multiple variants. Let SkillBoss generate them:

```
Use SkillBoss chat with Claude:
"Write 10 Facebook ad copy variations for Window Depot USA Milwaukee.

Offer: FREE in-home estimate + $500 gift card
Target: Homeowners in SE Wisconsin
USP: Triple-pane windows at dual-pane prices, 4.9 stars, 1000+ reviews

For each variation, provide:
- Headline (under 40 chars)
- Primary text (under 125 chars)
- Description (under 30 chars)
- CTA button text suggestion

Mix these angles: savings, comfort, energy efficiency, curb appeal, urgency (seasonal), trust/reviews."
```

#### Generate Ad Images

```
Use SkillBoss to generate an image with size 1792x1024:
"Professional marketing ad for a window replacement company. Split composition:
left side shows an old, drafty window with frost. Right side shows a modern
triple-pane window with warm, inviting interior. Text overlay area on the right.
Clean, high-contrast, professional advertisement style."
```

**Ad image sizes by platform:**

| Platform           | Recommended Size | SkillBoss Size  |
|--------------------|------------------|-----------------|
| Facebook Feed      | 1200×628         | `1792x1024`     |
| Instagram Feed     | 1080×1080        | `1024x1024`     |
| Instagram Stories  | 1080×1920        | `1024x1792`     |
| LinkedIn Feed      | 1200×627         | `1792x1024`     |

### Google Ads Copy

```
Use SkillBoss chat with GPT-5:
"Write 15 Google Search ad variations for Window Depot USA Milwaukee.

Keywords: window replacement milwaukee, new windows cost, triple pane windows, energy efficient windows

For each, provide:
- Headline 1 (30 chars max)
- Headline 2 (30 chars max)
- Headline 3 (30 chars max)
- Description 1 (90 chars max)
- Description 2 (90 chars max)

Strict character limits. Include price-lock guarantee and free estimate offer."
```

### Email Marketing Campaigns

```
Use SkillBoss chat with Claude:
"Write a 5-email drip campaign for Window Depot USA Milwaukee.

Audience: Homeowners who requested a free estimate but haven't booked yet.
Goal: Get them to schedule the appointment.

Email 1: Warm follow-up (sent day 1)
Email 2: Educational — energy savings data (sent day 3)
Email 3: Social proof — review highlights (sent day 5)
Email 4: Seasonal urgency (sent day 7)
Email 5: Final value stack — everything they get (sent day 10)

Each email: subject line, preview text, body (under 200 words), CTA button text."
```

---

## Platform-Specific Guides

### Facebook

**Post types that perform best:**
- Before/after project photos with storytelling captions
- Customer review screenshots with commentary
- Educational carousels (e.g., "5 Signs You Need New Windows")
- Local community involvement photos
- Video testimonials with TTS voiceover

**Prompt for batch Facebook content:**
```
Use SkillBoss chat with Claude:
"Write 10 Facebook posts for a home improvement company in Milwaukee.
Each post should be 50-100 words, include a soft CTA, feel personal and local,
and work well with a photo. Include emoji where natural. Mix educational,
promotional, and community content. End each with a question to drive comments."
```

### Instagram

**Post types that perform best:**
- High-quality project photos (use `generate_image`)
- Reels with voiceover (use `text_to_speech`)
- Carousel educational posts
- Stories with polls and questions
- Behind-the-scenes team content

**Prompt for batch Instagram content:**
```
Use SkillBoss chat with Claude:
"Write 10 Instagram captions for a home improvement company. Each should be
under 150 words, start with a hook (first line must stop the scroll), include
a mix of storytelling and value, and end with a CTA. Add 10-15 relevant
hashtags after each caption. Mix: transformation reveals, tips, testimonials,
and seasonal content for Wisconsin."
```

### LinkedIn

**Post types that perform best:**
- Industry insights and expertise
- Business growth stories
- Team and culture highlights
- Case studies with data
- Thought leadership on home improvement trends

**Prompt for batch LinkedIn content:**
```
Use SkillBoss chat with Claude:
"Write 10 LinkedIn posts from the perspective of a home improvement business
owner in Milwaukee. Professional but personable tone. Each should be 100-200
words, share a genuine insight or lesson, and position the author as a
trusted local expert. Topics: business growth, customer service philosophy,
industry trends, team building, community involvement. No hashtag spam —
max 3 relevant hashtags per post."
```

### X (Twitter)

**Prompt for batch tweets:**
```
Use SkillBoss chat with gemini-2.5-flash:
"Write 20 tweets for a home improvement company owner in Milwaukee.
Under 280 characters each. Mix: quick tips, fun facts about homes,
seasonal reminders, business wisdom, and soft promotions. Tone: casual,
knowledgeable, local. Include 1-2 hashtags max per tweet."
```

---

## Prompt Templates & Recipes

### Recipe 1: Weekly Content Kit

Run this once a week to generate all your content:

```
Use SkillBoss chat with Claude:
"Generate a complete weekly content kit for Window Depot USA Milwaukee.
Include:
- 3 Facebook posts (1 educational, 1 review-based, 1 promotional)
- 3 Instagram captions with hashtags
- 2 LinkedIn posts
- 5 tweets
- 1 email newsletter topic with subject line and outline
- 2 image generation prompts I can use to create matching visuals

This week's theme: [SPRING HOME PREP / ENERGY SAVINGS / etc.]
Make all content feel connected by theme but unique per platform."
```

### Recipe 2: Review-to-Content Converter

Turn a 5-star review into multi-platform content:

```
Use SkillBoss chat with Claude:
"Here's a real customer review: '[paste review]'

Turn this into:
1. A Facebook post celebrating this customer (anonymized)
2. An Instagram caption with the review as a quote graphic concept
3. A LinkedIn post about what this review means for our business
4. A tweet highlighting the key praise
5. An image prompt for a graphic featuring the quote"
```

### Recipe 3: Seasonal Campaign Generator

```
Use SkillBoss chat with Claude:
"Create a complete [SEASON] marketing campaign for Window Depot USA Milwaukee.

Include:
- Campaign theme and tagline
- 10 social media posts across all platforms
- 3 ad copy variations (Facebook/Instagram)
- 2 email subject lines and outlines
- 5 image generation prompts
- 1 video script (30 seconds) for a reel/short

Focus on [SEASON]-specific pain points for Wisconsin homeowners."
```

### Recipe 4: Competitor Differentiation Posts

```
Use SkillBoss chat with Claude:
"Write 5 social media posts that subtly differentiate Window Depot USA from
big-box retailers and national chains. Never name competitors directly.
Focus on: local ownership, triple-pane value, 1-year price lock, personal
service with Nate, real energy analysis (RESFEN), and 4.9 stars with 1000+ reviews.
Make each post feel like genuine advice, not a sales pitch."
```

### Recipe 5: Community Engagement Content

```
Use SkillBoss chat with Claude:
"Write 8 community-focused social media posts for a home improvement company
in Milwaukee, WI. Topics should reference real Milwaukee things: neighborhoods
(Bay View, Wauwatosa, Third Ward), events, weather, sports, food, local pride.
The goal is to feel genuinely local, not performatively local. Each post should
connect the local topic back to home improvement naturally."
```

---

## Cost Optimization Tips

### Model Selection Strategy

| Task                        | Best Model                  | Why                                |
|-----------------------------|-----------------------------|------------------------------------|
| Bulk draft generation       | `gemini-2.5-flash`          | 15× cheaper than Claude, very fast |
| Final copy polish           | `bedrock/claude-4-5-sonnet` | Best writing quality               |
| Quick social posts          | `gpt-4o-mini`               | Great quality at lowest cost       |
| Creative brainstorming      | `gpt-5`                     | Strongest creative capabilities    |
| Budget batch processing     | `deepseek/deepseek-v3`      | $0.27/1M tokens both ways          |

### Cost-Saving Workflow

1. **Draft with cheap models** — Use `gemini-2.5-flash` or `deepseek/deepseek-v3` for first drafts
2. **Refine with premium models** — Use `bedrock/claude-4-5-sonnet` only for final polish
3. **Reuse image prompts** — Generate one hero image per theme, crop/adapt for platforms
4. **Batch requests** — Send multiple posts in a single prompt instead of one at a time
5. **Use system prompts** — Set your brand voice once in the system prompt, reuse across all calls

### Credit Budget Example (Monthly Marketing)

| Activity                    | Credits/Month | Cost Estimate |
|-----------------------------|---------------|---------------|
| 60 social posts (copy)      | ~5 credits    | ~$0.38        |
| 15 images (DALL-E 3)        | ~30 credits   | ~$2.25        |
| 5 voiceovers (TTS)          | ~5 credits    | ~$0.38        |
| 4 email campaigns (copy)    | ~3 credits    | ~$0.23        |
| Ad copy variations          | ~3 credits    | ~$0.23        |
| **Total**                   | **~46 credits** | **~$3.50/mo** |

---

## Troubleshooting

### Common Issues

**"SKILLBOSS_API_KEY environment variable is required"**
- Make sure you've replaced `YOUR_KEY_HERE` in `.cursor/mcp.json` with your actual key
- Get your key at [skillboss.co/console](https://skillboss.co/console)

**MCP server not appearing in Cursor**
- Restart Cursor after editing `.cursor/mcp.json`
- Verify the JSON syntax is valid (no trailing commas)
- Check that Node.js 18+ is installed: `node --version`

**"Insufficient credits" error**
- Top up at [skillboss.co/pricing](https://skillboss.co/pricing)
- Use `get_balance` to check remaining credits

**Slow responses**
- Switch to a faster model like `gemini-2.5-flash`
- Reduce `max_tokens` for shorter outputs
- Break large requests into smaller batches

### Useful Links

| Resource          | URL                                                   |
|-------------------|-------------------------------------------------------|
| SkillBoss Console | [skillboss.co/console](https://skillboss.co/console)  |
| Pricing           | [skillboss.co/pricing](https://skillboss.co/pricing)  |
| All Models        | [skillboss.co/models](https://skillboss.co/models)    |
| Documentation     | [skillboss.co/docs](https://skillboss.co/docs)        |
| Discord Support   | [discord.gg/skillboss](https://discord.gg/skillboss)  |
| GitHub (MCP)      | [github.com/heeyo-life/skillboss-mcp](https://github.com/heeyo-life/skillboss-mcp) |

---

## Quick Reference Card

```
╔═══════════════════════════════════════════════════════════════╗
║  SKILLBOSS QUICK COMMANDS (use in Cursor chat)               ║
╠═══════════════════════════════════════════════════════════════╣
║                                                               ║
║  Check balance     → "Use SkillBoss to check my balance"     ║
║  List models       → "Use SkillBoss to list models"          ║
║  Chat with Claude  → "Use SkillBoss chat with Claude: ..."   ║
║  Chat with GPT-5   → "Use SkillBoss chat with GPT-5: ..."   ║
║  Generate image    → "Use SkillBoss to generate an image..." ║
║  Text to speech    → "Use SkillBoss TTS: ..."                ║
║  Get recommendation→ "Use SkillBoss to recommend a model..." ║
║                                                               ║
║  API Base URL: https://api.heybossai.com/v1                  ║
║  Console:      https://skillboss.co/console                  ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
```
