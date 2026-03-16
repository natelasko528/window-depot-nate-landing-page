# Enhanced Execution Prompt — Psychology-Driven Owner Journey Overhaul

Use this prompt as-is for implementation execution.

---

You are a senior growth product engineer + CRO architect.  
Your job is to overhaul `https://wdusa-nate-landing.vercel.app/owner` by embedding a natural, ethical, psychology-driven decision journey inspired by:

1) The framework taught in **Adam Erhart's** video:  
   **"The DARK Psychology That Makes Clients BEG to PAY YOU"** (YouTube ID: `XsH6Cr8Kag0`)  
2) The conversion flow patterns on `https://revolutionai.pro`

Do **not** use manipulative, deceptive, or fake tactics.  
Apply the framework ethically for homeowner clarity and confidence.

## Core Decision Framework to Embed (in this order)

1. **Weight Audit** — surface and quantify homeowner pain (cost of inaction).  
2. **Desire Stack** — stack proof, outcomes, and future-state clarity.  
3. **Fear Reframe** — reduce fear of acting; increase fear of waiting.  
4. **Quiet Close** — clear CTA + low-pressure decision space.

## Business + Brand Constraints (non-negotiable)

- Company: **Window Depot USA of Milwaukee**
- Voice: warm, local, no-pressure, trustworthy
- Must keep promotion stack:
  - FREE in-home estimate
  - $500 gift card with estimate booked through Nate
  - 12-month price lock
  - Triple-pane at dual-pane prices
- Must keep contact:
  - Phone: `(414) 312-5213`
  - Owner: Nate
- Must preserve existing booking/chat widgets and improve flow around them.

## Required Deliverables

Produce all deliverables below in one execution pass:

### 1) Experience Architecture
- New owner-page section order (top to bottom)
- Intent of each section mapped to:
  - Awareness
  - Consideration
  - Commitment
  - Follow-up
- Explicit mapping of each section to the 4 framework steps above.

### 2) Component + Widget Overhaul
- Keep what works; redesign what does not.
- Add/upgrade these modules:
  - **How It Works (4 steps)**
  - **Cost of Waiting calculator** (loss-aversion framing)
  - **Outcome calculator** (savings + value impact)
  - **Objection FAQ accordion**
  - **Story stack carousel** (3 transformation stories with metrics)
  - **No-pressure guarantee block**
  - **Contextual CTA rails** by service section
  - **Post-booking expectation module** ("what happens next")

For each module provide:
- UX goal
- Inputs/outputs
- Trigger rules
- Placement
- Copy guardrails
- Mobile behavior

### 3) Event Tracking + Funnel Instrumentation
- Define full event taxonomy (`snake_case`) for:
  - Section view depth
  - Calculator interactions
  - CTA clicks by location
  - FAQ expands
  - Booking widget open/start/submit
  - Chat open/start/send
- Include `event_name`, properties, destination (`Meta Pixel`, `Vercel`, optional GHL webhook), and KPI purpose.

### 4) Technical Implementation Plan
- Incremental phases with effort estimate:
  - Phase 1: Structure + copy + CTA pathing
  - Phase 2: Calculators + FAQ + story stack
  - Phase 3: Instrumentation + A/B experiments
  - Phase 4: Follow-up automation and optimization
- For each phase include:
  - File-level change list
  - Acceptance criteria
  - Test plan (desktop/mobile)
  - Rollback strategy

### 5) CRO Experiment Plan (minimum 8 tests)
- Hypothesis
- Variant details
- Primary metric
- Guardrail metrics
- Sample size/decision rule

## UX/Copy Rules

- Lead with homeowner pain clarity, not hype.
- Every section ends with one soft CTA.
- Avoid fake scarcity language and aggressive pressure.
- No jargon. Plain homeowner language.
- Milwaukee/SE Wisconsin context should feel natural.

## Output Format

Return:
1. **Overhauled user journey blueprint** (visual text flow)
2. **Module spec table**
3. **Event instrumentation spec**
4. **Phased development plan**
5. **A/B test backlog**
6. **Execution checklist**

Use concrete, implementation-ready detail so an engineer can ship immediately.

