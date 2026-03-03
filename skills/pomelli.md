name: pomelli-skill
description: "Agent-automated skill for Google Labs Pomelli AI marketing tool — all browser interactions are executed by a computerUse subagent, not the user. Covers Business DNA setup, campaign generation, Photoshoot, Animate, AI Actor UGC, and multi-platform content strategy."
version: 2.0.0
---

# Pomelli AI Marketing Skill (Agent-Automated)

Google Labs Pomelli (built with Google DeepMind) is a free AI marketing tool for creating on-brand social media campaigns, product photography, animated video, and UGC-style ads at **https://labs.google.com/pomelli**.

**Availability**: Free public beta — US, Canada, Australia, New Zealand (English only).

**CRITICAL**: This skill is fully agent-automated. The active agent MUST spawn a `computerUse` subagent to perform all Pomelli browser interactions. Never ask the user to do manual steps — the agent does them.

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

## AUTHENTICATION PREREQUISITE

Before running any Pomelli workflow, the agent MUST verify Google account access:

1. Spawn a `computerUse` subagent to navigate to `https://labs.google.com/pomelli`.
2. If the page shows a Google sign-in screen, check if a session already exists (cookies from a prior login).
3. If sign-in is required and credentials are not available, the **active agent** (not the subagent) must request the user log in via the Desktop pane using an `<external_action>` block. Do NOT attempt to type credentials — let the user authenticate interactively.
4. Once authenticated, proceed with the requested workflow.

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

### Negative DNA

Define what the brand is NOT to prevent generic output:
- Banned phrases, words, and clichés
- Styles to avoid (e.g., no neon gradients, no clip-art aesthetics)
- Tone boundaries (e.g., never sarcastic, never overly formal)
- Visual anti-patterns (e.g., no stock-photo lifestyle shots)

---

## AGENT EXECUTION MODEL

All Pomelli workflows follow this pattern:

```
Active Agent
  │
  ├─ 1. Gather context (read codebase files, kb.js, brand info)
  ├─ 2. Build the computerUse subagent prompt (detailed, step-by-step)
  ├─ 3. Spawn computerUse subagent with the prompt
  ├─ 4. Review subagent results (screenshots, downloaded files)
  ├─ 5. If more steps needed, resume the computerUse subagent
  └─ 6. Save artifacts and report to user
```

**Rules for computerUse subagent prompts:**
- Be extremely explicit about every click, scroll, and text entry
- Include exact URLs, exact text to type, and exact button labels to click
- Tell the subagent to take screenshots at key decision points
- Tell the subagent to wait for page loads and animations to complete
- Tell the subagent to download/save generated assets to a specific local path
- If Pomelli shows multiple options, tell the subagent how to choose (or to screenshot all and let the active agent decide)

---

## FEATURE WORKFLOWS

### 1. Business DNA Setup

**When to run:** First time using Pomelli for a project, or when the user asks to set up / refresh their brand profile.

**Active agent preparation:**
1. Read the project's website URL, CSS variables, font families, and brand copy from the codebase
2. Read `kb.js` if it exists for business facts (services, locations, contact info)
3. Prepare a Negative DNA list based on the brand's style

**Spawn computerUse subagent with this prompt structure:**

```
TASK: Set up Pomelli Business DNA for [BUSINESS_NAME].

STEPS:
1. Open Chrome and navigate to https://labs.google.com/pomelli
2. If you see a sign-in page, STOP and report back that authentication is needed.
3. Once on the Pomelli dashboard, look for an option to create a new project or
   set up Business DNA. Click it.
4. When prompted for a website URL, enter: [WEBSITE_URL]
5. Wait for Pomelli to finish scanning the site (look for a loading indicator to
   complete or for brand elements to appear).
6. Take a screenshot of the extracted Business DNA — showing colors, fonts, tone,
   and visual identity.
7. Review the extracted brand elements:
   - Verify the color palette includes these hex codes: [LIST_HEX_CODES]
   - Verify the fonts include: [LIST_FONTS]
   - If any element is wrong or missing, click to edit and correct it.
8. Look for a section to add Negative DNA, exclusions, or "what to avoid."
   If found, enter the following exclusions:
   [LIST_NEGATIVE_DNA_ITEMS, one per line]
9. Save / confirm the Business DNA profile.
10. Take a final screenshot of the completed Business DNA profile.
11. Return all screenshot paths.
```

**After subagent completes:** Review the screenshots. If corrections are needed, resume the subagent with specific edit instructions.

---

### 2. Campaign Generation

**When to run:** User asks to create social media posts, marketing campaigns, or content for specific platforms.

**Active agent preparation:**
1. Determine campaign goal, target platforms, and any specific messaging
2. Build a RATACVDO prompt (see Prompt Engineering section below)
3. Read `kb.js` for real business facts to include in the prompt

**Spawn computerUse subagent with this prompt structure:**

```
TASK: Generate a [CAMPAIGN_TYPE] campaign in Pomelli for [BUSINESS_NAME].

STEPS:
1. Open Chrome and navigate to https://labs.google.com/pomelli
2. If you see a sign-in page, STOP and report back.
3. On the Pomelli dashboard, look for a "Create Campaign" or "New Campaign"
   button. Click it.
4. If prompted to select a Business DNA / brand profile, select [BUSINESS_NAME].
5. In the campaign prompt / goal field, enter this text exactly:

   """
   [FULL_RATACVDO_PROMPT — paste the complete prompt here]
   """

6. If there are platform selection options, select: [LIST_PLATFORMS]
7. Click Generate / Create and wait for Pomelli to produce the campaign.
8. Take a screenshot of the generated campaign overview showing all variations.
9. For each generated post/asset:
   a. Click to view the full-size preview
   b. Take a screenshot
   c. Look for a Download button — click it and save the file
   d. If a download dialog appears, save to /workspace/pomelli-output/campaigns/
10. After reviewing all posts, take a final overview screenshot.
11. Return all screenshot paths and downloaded file paths.
```

**After subagent completes:** Review screenshots. If the output needs refinement, resume the subagent with instructions like "Edit post #2 — change the headline to [X]" or "Regenerate with a different tone."

---

### 3. Photoshoot

**When to run:** User asks for product photography, studio-quality images, or professional product visuals.

**Active agent preparation:**
1. Identify source product images in the codebase (or ask user to specify)
2. Determine style preference: Studio or Lifestyle
3. Prepare any style reference images if applicable

**Spawn computerUse subagent with this prompt structure:**

```
TASK: Use Pomelli Photoshoot to generate professional product images for
[BUSINESS_NAME].

STEPS:
1. Open Chrome and navigate to https://labs.google.com/pomelli
2. If you see a sign-in page, STOP and report back.
3. On the Pomelli dashboard, find and click the "Photoshoot" feature.
4. If prompted to select a Business DNA / brand profile, select [BUSINESS_NAME].
5. Upload the product image(s):
   - Click the upload area or "Upload Photo" button
   - Navigate to and select: [LOCAL_IMAGE_PATH]
   - Wait for the upload to complete
6. When template options appear, select: [STUDIO or LIFESTYLE]
   (If neither is clearly labeled, take a screenshot of available options
   and report back for the active agent to decide.)
7. Click Generate and wait for Pomelli to produce the images.
8. Take a screenshot of all generated image variations.
9. For each generated image:
   a. Click to view full-size
   b. Take a screenshot
   c. Download and save to /workspace/pomelli-output/photoshoot/
10. If there's an option to refine (change background, apply style reference):
    - [INCLUDE_SPECIFIC_REFINEMENT_INSTRUCTIONS_IF_NEEDED]
11. Return all screenshot paths and downloaded file paths.
```

**After subagent completes:** Review the generated images. If backgrounds need changing or style needs adjustment, resume with specific refinement instructions.

---

### 4. Animate

**When to run:** User asks for video content, Reels, TikTok videos, Shorts, or animated marketing assets.

**Active agent preparation:**
1. Identify the static asset to animate (either from a prior Pomelli session or from the codebase)
2. Determine desired motion style(s)
3. Determine target platform (Reels, TikTok, Shorts, LinkedIn)

**Spawn computerUse subagent with this prompt structure:**

```
TASK: Use Pomelli Animate to create video content from a static asset for
[BUSINESS_NAME].

STEPS:
1. Open Chrome and navigate to https://labs.google.com/pomelli
2. If you see a sign-in page, STOP and report back.
3. On the Pomelli dashboard, find an existing asset to animate OR navigate to
   a previously generated campaign/photoshoot.
   [IF STARTING FROM SCRATCH: First create the static visual using the Campaign
   Generator following the campaign steps, then proceed to animate it.]
4. Find and click the "Animate" button on the selected asset.
5. When motion style options appear, select: [MOTION_STYLE]
   Options may include: camera movement, object motion, text animation,
   scene transitions. Choose: [SPECIFIC_CHOICES]
6. Click Generate and wait for the animation to render (may take up to 5 minutes).
7. When the preview is ready, play it through fully.
8. Take a screenshot of the video preview.
9. Download the animated video:
   - Click Download / Export
   - Save to /workspace/pomelli-output/animate/
10. If the result needs adjustment, look for a "Refine" or "Edit" option and
    apply: [SPECIFIC_ADJUSTMENTS]
11. Return all screenshot paths and downloaded file paths.
```

---

### 5. AI Actor UGC Videos

**When to run:** User asks for UGC-style ads, testimonial videos, spokesperson content, or creator-style TikTok ads.

**Active agent preparation:**
1. Write the script for the AI Actor to deliver
2. Determine the actor persona/style
3. Identify the target platform and tone

**Spawn computerUse subagent with this prompt structure:**

```
TASK: Create an AI Actor UGC video in Pomelli for [BUSINESS_NAME].

STEPS:
1. Open Chrome and navigate to https://labs.google.com/pomelli
2. If you see a sign-in page, STOP and report back.
3. On the Pomelli dashboard, find the AI Actor or UGC Video feature. Click it.
4. If prompted to select a Business DNA / brand profile, select [BUSINESS_NAME].
5. When actor selection appears, browse available AI Actor personas.
   Take a screenshot of the options.
   Select an actor that matches: [PERSONA_DESCRIPTION, e.g., "friendly homeowner
   in their 40s, casual but trustworthy"]
6. In the script / text field, enter this script exactly:

   """
   [FULL_SCRIPT_TEXT]
   """

7. If tone/style options are available, select: [TONE_PREFERENCE]
8. Click Generate and wait for the video to render.
9. When the Storyboard Preview appears, review each scene:
   a. Take a screenshot of the full storyboard
   b. If any scene needs adjustment, click to edit it
10. Once satisfied, click to produce the final video.
11. Download the video:
    - Save to /workspace/pomelli-output/ugc/
12. Return all screenshot paths and downloaded file paths.
```

---

## PROMPT ENGINEERING FOR POMELLI

### The RATACVDO Framework

The active agent MUST build RATACVDO prompts before passing them to the computerUse subagent. Never let the subagent improvise prompt text.

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

### Building the Prompt (Active Agent Steps)

1. Read project files to gather brand data (`kb.js`, `index.html` CSS variables, README)
2. Identify the user's campaign goal and target platforms
3. Assemble the RATACVDO elements into a single block of text
4. Pass the assembled prompt as a literal string inside the computerUse subagent instructions
5. The subagent pastes it verbatim into Pomelli's prompt field — it never writes its own marketing copy

### Platform-Specific Prompt Tips

**Instagram:** Request saveable tips, educational carousels, 8–15 hashtags, Story-optimized vertical crops.
**LinkedIn:** Data-forward, value-focused, no emoji overuse, thought-leadership angle.
**Facebook:** Shareable copy, early link placement, community-building tone, event/promo formatting.
**TikTok:** Shot lists, on-screen text scripts, hook in first 2 seconds, trending format suggestions.
**Email:** Subject line sets (5+ A/B variations), preview text, header hierarchy, mobile-first.

---

## BUSINESS DNA OPTIMIZATION

### Advanced Optimization Parameters

**Voice Calibration (for this project):**
```
Formality: 7/10 (conversational-professional)
Humor: Light wit, never sarcastic
Sentence length: Mix short punchy + medium detail
CTA style: Direct, benefit-led ("Book your FREE estimate")
Banned phrases: "game-changer", "revolutionary", "cutting-edge"
```

**Visual Calibration (for this project):**
```
Primary palette: Navy #0A1628, Gold #D4AF37, Ivory #FAFAF6
Safe tints: Gold can lighten to #FDF8EC, Navy can darken to #050D18
Shadow style: Subtle drop shadows, no harsh outlines
Image style: Warm, residential, real photography preferred
Avoid: Neon colors, abstract patterns, clip-art
```

### Refining Business DNA via Subagent

If campaign output quality is below 80% publishable, the active agent should spawn a computerUse subagent to refine the DNA:

```
TASK: Refine the Pomelli Business DNA for [BUSINESS_NAME].

STEPS:
1. Navigate to https://labs.google.com/pomelli
2. Open the Business DNA / Brand Profile settings for [BUSINESS_NAME].
3. Take a screenshot of the current DNA settings.
4. Update the following fields:
   - Voice/Tone: Change to "[NEW_VOICE_PARAMETERS]"
   - Add these Negative DNA exclusions: [LIST]
   - Adjust color palette: [SPECIFIC_CHANGES]
5. Save changes.
6. Take a screenshot of the updated DNA.
7. Return screenshot paths.
```

---

## CAMPAIGN STRATEGY TEMPLATES

Use these as starting points for the RATACVDO prompt's Task + Additional Context elements.

### Product Launch Campaign
```
Task: 5-post series (teaser → reveal → features → social proof → CTA)
Platforms: Instagram carousel + Facebook ad + LinkedIn announcement
Assets needed: Product Photoshoot images + Animate teaser video
```

### Seasonal Promotion Campaign
```
Task: 3-post series (urgency → value → final CTA)
Platforms: Instagram Stories + Facebook promo + Email header
Assets needed: Branded promotional graphics + countdown animation
```

### Social Proof Campaign
```
Task: 4-post series (stat highlight → customer quote → before/after → booking CTA)
Platforms: Instagram feed + LinkedIn + Google Ads
Assets needed: Review highlight graphics + Animated stat counters
```

### Educational Content Campaign
```
Task: 5-post carousel (problem → insight → solution → proof → CTA)
Platforms: Instagram carousel + LinkedIn article graphic + YouTube thumbnail
Assets needed: Infographic-style visuals + Animated explainer
```

---

## WORKFLOW: POMELLI FOR THIS PROJECT

This landing page (Window Depot USA Milwaukee) is a perfect Pomelli candidate. The active agent should execute these steps in order, spawning a computerUse subagent for each browser-based phase.

### Phase 1: Build Business DNA

**Active agent reads:** `index.html` (CSS variables, brand copy), `kb.js` (services, locations, facts), `README.md` (brand context).

**Active agent spawns computerUse subagent:**
- Navigate to `https://labs.google.com/pomelli`
- Create Business DNA using URL `https://wdusa-nate-landing.vercel.app`
- Verify extracted palette: navy `#0A1628`, gold `#D4AF37`, ivory `#FAFAF6`
- Verify fonts: Cormorant Garant, Nunito Sans, Bebas Neue
- Add Negative DNA: no generic stock photos, no "revolutionary" language, no neon colors, no clip-art, no sarcasm
- Screenshot the final DNA profile

### Phase 2: Generate Campaigns

**Active agent builds RATACVDO prompts** using data from `kb.js`:
- **Windows promo**: Triple pane energy savings + $1000 off CTA
- **Seasonal storm damage**: Roofing + siding before winter
- **Bathroom one-day makeover**: Quick-turnaround lifestyle content
- **Social proof**: 4.9★ Google rating, 1000+ reviews, A+ BBB

**Active agent spawns computerUse subagent** for each campaign (or batches if Pomelli supports it):
- Enter the RATACVDO prompt verbatim
- Select target platforms
- Generate and download all assets to `/workspace/pomelli-output/campaigns/`

### Phase 3: Product Photoshoot

**Active agent identifies source images** from the repo (`nate-profile.png`, social post images, etc.).

**Active agent spawns computerUse subagent:**
- Upload images to Pomelli Photoshoot
- Select Studio template for product shots, Lifestyle for contextual shots
- Generate and download to `/workspace/pomelli-output/photoshoot/`

### Phase 4: Animate for Reels/TikTok

**Active agent selects top campaign assets** from Phase 2 output.

**Active agent spawns computerUse subagent:**
- Open selected assets in Pomelli
- Click Animate
- Choose motion styles: camera pan for before/after, kinetic text for promotions
- Download videos to `/workspace/pomelli-output/animate/`

### Phase 5: UGC-Style Ads

**Active agent writes scripts** based on `kb.js` content:
- "I just got my windows replaced by Nate..." homeowner testimonial format
- Authentic, conversational delivery

**Active agent spawns computerUse subagent:**
- Navigate to AI Actor feature
- Select appropriate persona
- Enter script verbatim
- Preview storyboard, generate, download to `/workspace/pomelli-output/ugc/`

---

## OUTPUT MANAGEMENT

### File Organization

The active agent should create this directory structure before spawning subagents:

```
/workspace/pomelli-output/
├── campaigns/        # Generated campaign post images and captions
├── photoshoot/       # AI product photography
├── animate/          # Animated video files
├── ugc/              # AI Actor UGC videos
└── screenshots/      # Subagent screenshots for review
```

**Shell command to run before any Pomelli workflow:**
```bash
mkdir -p /workspace/pomelli-output/{campaigns,photoshoot,animate,ugc,screenshots}
```

### After Subagent Downloads

1. Review all downloaded assets by examining the screenshot evidence
2. Copy final approved assets to `/opt/cursor/artifacts/` for user visibility
3. If assets will be used in the codebase, move them to the appropriate repo location
4. Record a demo video (`RecordScreen`) showing the best generated content if it's visually significant

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

### Monthly Batching via Agent

The active agent can batch an entire month's content in one session:
1. Build 4 RATACVDO prompts (one campaign theme per week)
2. Spawn 4 sequential computerUse subagents (one per campaign)
3. Spawn 1 subagent for Photoshoot batch (4 product sets)
4. Spawn 1 subagent to Animate top 4 static posts
5. Spawn 1 subagent for 2 UGC Actor ads
6. Total: ~7 subagent invocations for a full month of content

---

## INTEGRATION WITH THIS CODEBASE

### Social Media Images
The repo contains platform-specific images (`01_windows_facebook.png` through `18_bathroom_linkedin.png`). The agent can:
- Upload these to Pomelli Photoshoot for brand-consistent regeneration
- Create animated versions via the Animate workflow
- Generate A/B test variations

### Knowledge Base Sync
`kb.js` contains the AI chatbot knowledge base. The active agent MUST read this file and extract key facts (services, pricing, locations, warranties) before building any RATACVDO prompt. These facts go into the **Data** element to ensure generated content is factually accurate.

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

The active agent reviews all subagent output against this list before presenting to user:

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

| Issue | Cause | Agent Action |
|---|---|---|
| Sign-in page appears | No Google session | Request user login via `<external_action>` Desktop pane |
| Generic/bland output | Weak Business DNA | Spawn subagent to refine DNA (add Negative DNA, adjust voice) |
| Wrong colors in visuals | DNA not calibrated | Spawn subagent to manually verify and correct hex codes |
| Off-brand tone | Vague voice descriptors | Rebuild RATACVDO prompt with stricter Voice element |
| Low-quality Photoshoot | Poor source image | Try a different source image with neutral background |
| Animate looks choppy | Complex source | Spawn subagent to simplify the static design first |
| Factual errors in copy | Missing Data element | Re-read `kb.js`, add real facts to prompt, regenerate |
| Pomelli is unavailable | Beta region restriction | Report to user; suggest VPN or wait for global launch |
| Download fails | Browser dialog issue | Instruct subagent to right-click → Save As instead |

---

## REFERENCE LINKS

- **Pomelli**: https://labs.google.com/pomelli
- **Onboarding**: https://labs.google.com/pomelli/onboarding
- **Google Blog (Launch)**: https://blog.google/technology/google-labs/pomelli/
- **Photoshoot Announcement**: https://blog.google/innovation-and-ai/models-and-research/google-labs/pomelli-photoshoot/
- **Business DNA Guide**: https://www.pomellihelp.com/pomelli-business-dna-optimization-guide
- **Campaign Examples (50+)**: https://pomelli.art/pomelli-examples
- **Video Tutorials**: https://pomelli.me/video
