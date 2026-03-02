name: pomelli-skill
description: "Comprehensive skill for leveraging Google Labs Pomelli AI marketing tool — covers Business DNA setup, campaign generation, Photoshoot, Animate, AI Actor UGC, prompt engineering, and multi-platform content strategy."
version: 1.0.0
---

# Pomelli AI Marketing Skill

Google Labs Pomelli (built with Google DeepMind) is a free AI marketing tool for creating on-brand social media campaigns, product photography, animated video, and UGC-style ads. Access it at **https://labs.google.com/pomelli** with any Google account.

**Availability**: Free public beta — US, Canada, Australia, New Zealand (English only).

---

## WHEN TO USE THIS SKILL

Use this skill when the user asks to:
- Create social media campaigns or marketing content
- Generate product photography or studio-quality images
- Animate static assets into Reels/TikTok/Shorts
- Build or refine a Brand DNA profile
- Produce AI Actor UGC-style video ads
- Optimize marketing prompts for Pomelli
- Plan multi-platform content calendars
- Generate email banners, Google Ads, or landing page visuals

---

## CORE CONCEPTS

### Business DNA

Business DNA is Pomelli's foundational intelligence layer — a brand profile auto-extracted from your website URL that captures:

| Element | What It Captures |
|---|---|
| **Brand Voice & Tone** | Formality level, humor appropriateness, messaging style |
| **Color Palette** | Hex codes, contrast ratios, safe tint ranges |
| **Typography** | Font pairings, weights, line-height, spacing |
| **Visual Identity** | Logo, image style, shadows, gradients, textures |
| **Messaging Priorities** | Taglines, CTAs, value propositions |

**Setup**: Enter your website URL at `https://labs.google.com/pomelli/onboarding` → Pomelli scans and extracts everything automatically.

### Negative DNA

Define what the brand is NOT to prevent generic output:
- Banned phrases, words, and clichés
- Styles to avoid (e.g., no neon gradients, no clip-art aesthetics)
- Tone boundaries (e.g., never sarcastic, never overly formal)
- Visual anti-patterns (e.g., no stock-photo lifestyle shots)

---

## FEATURES

### 1. Campaign Generator

Generates complete, ready-to-use social media campaigns tailored to your Business DNA.

**What it produces:**
- Social media posts with captions and visuals
- Platform-specific adaptations (dimensions, tone, hashtags)
- Multi-post coordinated series (3–5 posts per campaign)
- 10 post variations in ~60 seconds

**Supported platforms:**

| Platform | Content Types |
|---|---|
| **Instagram** | Feed posts, carousel posts, Stories, Reels covers |
| **Facebook** | Ads, promotional posts, event graphics |
| **LinkedIn** | Professional posts with adjusted tone |
| **X (Twitter)** | Character-limited posts |
| **TikTok** | Shot lists, on-screen text guides |
| **YouTube** | Thumbnails, channel assets |
| **Email** | Headers, templates, subject line sets |
| **Google Ads** | Display ad creatives |
| **Web** | Landing page banners, website banners |

**Workflow:**
1. Build Business DNA (one-time setup)
2. Choose campaign goal or enter a custom prompt
3. Browse generated campaign ideas
4. Select, edit, and customize assets
5. Download or export

### 2. Photoshoot

Transforms basic product photos into professional studio-quality images using Nano Banana image generation.

**Workflow:**
1. Upload any product photo (doesn't need to be polished)
2. Choose a template: **Studio** or **Lifestyle** (or let Pomelli suggest)
3. Generate images — brand aesthetics auto-applied from Business DNA
4. Refine: change backgrounds, apply style references, manual edits
5. Download final assets

**Best for:** E-commerce product pages, social ads, catalog imagery, website hero shots.

**Tips:**
- Use clean product photos with neutral backgrounds for best extraction
- Upload a style reference image to match a specific visual aesthetic
- Generate multiple variations and A/B test in campaigns
- Pull product info from URL to auto-generate context-based visuals

### 3. Animate (Powered by Veo 3.1)

Converts static marketing assets into animated video content optimized for short-form platforms.

**Motion styles:**
- Camera movement (pan, zoom, dolly)
- Object motion (product rotation, element entrance)
- Text animation (kinetic typography, reveal effects)
- Scene transitions

**Output optimized for:**
- Instagram Reels
- TikTok
- YouTube Shorts
- LinkedIn video posts

**Workflow:**
1. Create or select a static visual in Pomelli
2. Click **Animate**
3. Choose motion style(s)
4. Generate — under 5 minutes per video
5. Preview, refine, export

**Performance:** Early users report 30–40% faster creative turnaround vs. traditional design workflows.

### 4. AI Actor UGC Videos

Creates creator-style ads with AI-generated spokespersons — realistic speech, expressions, and on-brand visuals.

**Workflow:**
1. Select an AI Actor persona
2. Write or paste your script
3. Pomelli generates natural speech and realistic facial expressions
4. Preview via **Storyboard Preview** — refine scenes, styles, shot flow
5. Export for TikTok, Instagram, and short-form paid ads

**Best for:** TikTok ads, product testimonials, UGC-style brand content, explainer videos.

---

## PROMPT ENGINEERING FOR POMELLI

### The RATACVDO Framework

Structure every Pomelli prompt with these 8 elements for near-ready-to-ship output:

| Element | Purpose | Example |
|---|---|---|
| **R**ole | Define the persona | "Senior product marketer for a home improvement brand" |
| **A**udience | Who you're targeting | "Milwaukee homeowners 35-65 planning renovations" |
| **T**ask | Specific deliverable | "Create a 5-post Instagram carousel campaign" |
| **A**dditional Context | Product details, proof points | "$1000 off promotion, ProVia Triple Pane windows, 4.9★ Google rating" |
| **C**onstraints | Length, format, channel rules | "Max 150 words per caption, include CTA, 1080×1080px" |
| **V**oice | 2–3 tone traits + banned phrases | "Warm and authoritative. No jargon. No exclamation marks." |
| **D**ata | Real facts to prevent fabrication | "Serving SE Wisconsin from 7 showrooms, Top 500 National #3" |
| **O**utput | Exact sections and structure | "For each post: headline, body, CTA, hashtag set, alt text" |

### Prompt Quality Tiers

| Input Quality | Output Quality | Edit Time |
|---|---|---|
| Vague one-liner | Generic, unusable | 40–60 min rework |
| Basic brief (3–4 elements) | Decent first draft | 15–20 min polish |
| Full RATACVDO prompt | 70–80% publishable | 5–10 min final touches |
| Full prompt + refined Business DNA | 90%+ ready to ship | Minimal tweaks |

### Platform-Specific Prompt Tips

**Instagram:**
- Request saveable tips and educational carousels
- Specify hashtag counts (8–15 optimal)
- Ask for Story-optimized vertical crops

**LinkedIn:**
- Request data-forward, value-focused language
- Specify no emoji overuse
- Ask for thought-leadership angle

**Facebook:**
- Request shareable copy with early link placement
- Specify community-building tone
- Ask for event or promo formatting

**TikTok:**
- Request shot lists and on-screen text scripts
- Specify hook in first 2 seconds
- Ask for trending sound/format suggestions

**Email:**
- Request subject line sets (5+ variations for A/B testing)
- Specify preview text and header hierarchy
- Ask for mobile-first formatting

---

## BUSINESS DNA OPTIMIZATION

### Initial Setup Checklist

- [ ] Enter website URL and let Pomelli scan
- [ ] Review extracted colors — verify hex codes match brand guidelines
- [ ] Review typography — confirm correct font pairings
- [ ] Review voice/tone — adjust formality scale (1-10)
- [ ] Add Negative DNA — specify what brand is NOT
- [ ] Test with a sample campaign — evaluate first-draft quality
- [ ] Refine based on output — iterate voice descriptors

### Advanced Optimization Parameters

**Voice Calibration:**
```
Formality: 7/10 (conversational-professional)
Humor: Light wit, never sarcastic
Sentence length: Mix short punchy + medium detail
CTA style: Direct, benefit-led ("Book your FREE estimate")
Banned phrases: "game-changer", "revolutionary", "cutting-edge"
```

**Visual Calibration:**
```
Primary palette: Navy #0A1628, Gold #D4AF37, Ivory #FAFAF6
Safe tints: Gold can lighten to #FDF8EC, Navy can darken to #050D18
Shadow style: Subtle drop shadows, no harsh outlines
Image style: Warm, residential, real photography preferred
Avoid: Neon colors, abstract patterns, clip-art
```

### 30-Day Refinement Framework

| Week | Focus | Action |
|---|---|---|
| 1 | Foundation | Build DNA, run 3 test campaigns, note gaps |
| 2 | Voice tuning | Adjust tone parameters based on Week 1 output |
| 3 | Visual tuning | Refine color usage, image style preferences |
| 4 | Negative DNA | Add exclusions based on any off-brand output |

---

## CAMPAIGN STRATEGY TEMPLATES

### Product Launch Campaign
```
Goal: Announce new product/service
Posts: 5-post series (teaser → reveal → features → social proof → CTA)
Platforms: Instagram carousel + Facebook ad + LinkedIn announcement
Assets: Product Photoshoot images + Animate teaser video
```

### Seasonal Promotion Campaign
```
Goal: Drive bookings during peak season
Posts: 3-post series (urgency → value → final CTA)
Platforms: Instagram Stories + Facebook promo + Email header
Assets: Branded promotional graphics + countdown animation
```

### Social Proof Campaign
```
Goal: Build trust with testimonials and ratings
Posts: 4-post series (stat highlight → customer quote → before/after → booking CTA)
Platforms: Instagram feed + LinkedIn + Google Ads
Assets: Review highlight graphics + Animated stat counters
```

### Educational Content Campaign
```
Goal: Position as industry expert
Posts: 5-post carousel series (problem → insight → solution → proof → CTA)
Platforms: Instagram carousel + LinkedIn article graphic + YouTube thumbnail
Assets: Infographic-style visuals + Animated explainer
```

---

## WORKFLOW: POMELLI FOR THIS PROJECT

This landing page (Window Depot USA Milwaukee) is a perfect Pomelli candidate. Here's the specific workflow:

### Step 1: Build Business DNA
1. Go to https://labs.google.com/pomelli
2. Enter the site URL: `https://wdusa-nate-landing.vercel.app`
3. Pomelli extracts: navy/gold palette, Cormorant Garant + Nunito Sans fonts, authoritative-yet-warm tone, home improvement imagery
4. Refine: Add Negative DNA (no generic stock photos, no "revolutionary" language, no neon colors)

### Step 2: Generate Campaigns
Target campaigns for this business:
- **Windows promo**: Triple pane energy savings + $1000 off CTA
- **Seasonal storm damage**: Roofing + siding before winter
- **Bathroom one-day makeover**: Quick-turnaround lifestyle content
- **Social proof**: 4.9★ Google rating, 1000+ reviews, A+ BBB

### Step 3: Product Photoshoot
Upload product/project photos and generate:
- Studio-quality window product shots
- Before/after renovation visuals
- Lifestyle-context home imagery

### Step 4: Animate for Reels/TikTok
Take top-performing static posts and:
- Add camera pan across renovation before/after
- Animate stat counters (energy savings calculator)
- Create kinetic text reveals for promotions

### Step 5: UGC-Style Ads
Create AI Actor testimonial-style ads:
- "I just got my windows replaced by Nate..." format
- Homeowner perspective script
- Authentic, conversational delivery

---

## CONTENT CALENDAR FRAMEWORK

### Weekly Cadence (Recommended)

| Day | Content Type | Platform Focus | Pomelli Feature |
|---|---|---|---|
| Monday | Educational tip | LinkedIn + Instagram | Campaign Generator |
| Tuesday | Product spotlight | Instagram + Facebook | Photoshoot + Campaign |
| Wednesday | Behind-the-scenes | Instagram Stories + TikTok | Animate |
| Thursday | Social proof/review | All platforms | Campaign Generator |
| Friday | Promotion/CTA | Facebook + Email + Instagram | Full suite |
| Saturday | Lifestyle/inspiration | Instagram + Pinterest | Photoshoot |

### Monthly Batching Strategy

Generate an entire month's content in one session:
1. Build 4 campaign themes (one per week)
2. Generate 6 posts per theme = 24 posts
3. Create 4 Photoshoot product sets
4. Animate 4 top posts into video
5. Create 2 UGC Actor ads
6. Total time: ~2-3 hours for a full month of content

---

## INTEGRATION WITH THIS CODEBASE

### Social Media Images
The repository already contains platform-specific social media images (`01_windows_facebook.png` through `18_bathroom_linkedin.png`). Pomelli can:
- Regenerate these with improved brand consistency
- Create animated versions via Animate
- Produce additional variations for A/B testing
- Generate Stories/Reels-optimized vertical versions

### Knowledge Base Sync
The `kb.js` file contains the AI chatbot knowledge base. Key data points from it (services, pricing, locations, warranties) should be fed into Pomelli prompts as the **Data** element to ensure factual accuracy in generated content.

### Landing Page Assets
Pomelli Photoshoot can generate hero images, service card visuals, and testimonial graphics that match the existing CSS variables:
```css
--navy: #0A1628
--gold: #B8900A
--gold2: #D4AF37
--ivory: #FAFAF6
```

---

## QUALITY CHECKLIST

Before publishing any Pomelli-generated content:

- [ ] Brand colors match palette (navy, gold, ivory)
- [ ] Fonts are consistent with brand (Cormorant Garant, Nunito Sans, Bebas Neue)
- [ ] Tone matches voice guidelines (warm, authoritative, zero-pressure)
- [ ] All facts are verified against `kb.js` knowledge base
- [ ] CTAs are actionable and specific (phone number, booking link)
- [ ] Platform dimensions are correct for target channel
- [ ] No Negative DNA violations (no banned phrases, no off-brand visuals)
- [ ] Hashtags are relevant and platform-appropriate
- [ ] Alt text is included for accessibility
- [ ] Legal compliance: accurate claims, proper disclaimers

---

## TROUBLESHOOTING

| Issue | Cause | Fix |
|---|---|---|
| Generic/bland output | Weak Business DNA | Add Negative DNA, refine voice parameters, use RATACVDO prompts |
| Wrong colors in visuals | DNA not calibrated | Manually verify hex codes in Business DNA settings |
| Off-brand tone | Vague voice descriptors | Use formality scale (1-10), add banned phrases, provide sample lines |
| Low-quality Photoshoot | Poor source image | Use clean product photo with neutral/white background |
| Animate looks choppy | Complex source image | Simplify the static design, reduce visual elements |
| Factual errors in copy | No data in prompt | Include real facts, pricing, and features in prompt's Data element |

---

## REFERENCE LINKS

- **Pomelli**: https://labs.google.com/pomelli
- **Onboarding**: https://labs.google.com/pomelli/onboarding
- **Google Blog (Launch)**: https://blog.google/technology/google-labs/pomelli/
- **Photoshoot Announcement**: https://blog.google/innovation-and-ai/models-and-research/google-labs/pomelli-photoshoot/
- **Business DNA Guide**: https://www.pomellihelp.com/pomelli-business-dna-optimization-guide
- **Campaign Examples (50+)**: https://pomelli.art/pomelli-examples
- **Video Tutorials**: https://pomelli.me/video
