# PRD — Owner Page Psychology-Led Journey Overhaul

## 1) Overview

This PRD defines a conversion-focused overhaul of `https://wdusa-nate-landing.vercel.app/owner` using a structured, ethical decision journey:

1. Weight Audit  
2. Desire Stack  
3. Fear Reframe  
4. Quiet Close

The target is to make the page flow feel natural while improving estimate-booking conversion quality and velocity.

## 2) Baseline Findings

### What currently works on WDUSA owner page
- Strong hero with embedded booking widget (high intent path)
- Deep service authority content
- Existing energy-savings calculator
- Existing urgency and social-proof mechanics
- Persistent chat + call options

### What RevolutionAI does better (benchmark)
- Clear "How it works" process section
- More explicit objection handling via FAQ
- Cleaner step-to-step narrative from pain to action
- ROI framing tightly tied to CTA moments

### Core gap
WDUSA has rich content but a less explicit psychological progression from:
problem awareness -> quantified pain -> proof -> reduced risk -> decision.

## 3) Goals and Success Metrics

### Primary goals
- Increase booking conversion rate from owner page traffic
- Increase qualified booking rate (fit + intent)
- Reduce drop-off between hero and booking completion

### Secondary goals
- Increase interaction depth with high-intent tools
- Improve confidence signals before booking
- Improve post-booking show-up rate

### KPI targets (initial)
- +20% booking submit rate
- +15% booking completion after booking widget open
- +25% calculator-to-CTA click-through
- +10% increase in show-up rate (via post-booking expectation and follow-up clarity)

## 4) User Stories

### US-001: Quantify homeowner pain quickly
As a homeowner, I want to quickly see what waiting is costing me so I can decide if I should act now.

Acceptance criteria:
- [ ] New "Cost of Waiting" calculator is visible before deep content sections.
- [ ] Calculator has service-specific presets (windows, doors, siding, roofing, bath).
- [ ] Results include monthly and annual inaction cost with a clear explanation.
- [ ] CTA below calculator routes to booking widget anchor.

### US-002: Understand exact process before booking
As a homeowner, I want to know what happens after booking so I feel safe scheduling.

Acceptance criteria:
- [ ] New 4-step process section appears above first long-form deep-dive.
- [ ] Each step includes timeline expectations.
- [ ] Section has one low-friction CTA.

### US-003: Resolve objections without leaving page
As a skeptical buyer, I want answers to common concerns before I book.

Acceptance criteria:
- [ ] FAQ accordion includes top objections: pressure, pricing, timeline, financing, warranties.
- [ ] FAQ events are tracked by question ID.
- [ ] FAQ appears before major final CTA region.

### US-004: See proof from similar homeowners
As a local homeowner, I want to see outcomes from people like me.

Acceptance criteria:
- [ ] Story stack includes at least 3 transformation stories with concrete outcomes.
- [ ] Stories include location + service + measurable impact.
- [ ] Each story card includes contextual CTA.

### US-005: Book with confidence and low pressure
As a user near decision, I want a clear CTA and a no-pressure guarantee.

Acceptance criteria:
- [ ] "No-pressure guarantee" block appears immediately above final CTA.
- [ ] Guarantee language is owner-voice and plain language.
- [ ] Primary booking CTA remains prominent on desktop and mobile.

## 5) Functional Requirements

### FR-1 Journey restructuring
Reorder page sections to this conversion arc:
1. Hero + booking
2. Cost of Waiting (weight audit)
3. How It Works (risk reduction)
4. Outcomes + proof stories
5. Service deep dives (optional detail)
6. FAQ objections
7. No-pressure guarantee
8. Final CTA + booking anchor repeat

### FR-2 Tooling modules
- Add `cost_waiting_calculator`
- Keep and reposition enhanced `energy_savings_calculator`
- Add `home_value_impact_calculator` (phase 2+)

### FR-3 CTA system
- Every major section must end in one contextual CTA.
- CTA text must match section intent (analysis, book estimate, get questions answered).
- Sticky mobile CTA must remain available and not overlap chat widget.

### FR-4 Objection handling
- Add FAQ accordion with minimum 8 questions.
- Add expanded-state persistence for analytics session.

### FR-5 Social proof quality
- Replace generic notification-only proof with mixed proof:
  - review metrics
  - narrative outcomes
  - service-specific results

### FR-6 Instrumentation
Track:
- `section_view`
- `calculator_interaction`
- `calculator_result_view`
- `cta_click`
- `faq_expand`
- `booking_widget_open`
- `booking_start`
- `booking_submit`
- `chat_open`
- `chat_message_sent`

### FR-7 Follow-up handoff
After booking submit, show "What happens next" confirmation copy and ensure GHL flow tags source as `owner_page_overhaul_v1`.

## 6) Non-Goals

- Full site redesign of non-owner routes
- Backend platform migration
- Replacing existing booking/chat providers
- New CRM implementation

## 7) UX and Content Guidelines

- Tone: trusted advisor, local, no pressure
- Keep homeowner language concrete and simple
- Use loss framing ethically (cost of waiting) with transparent assumptions
- Keep claims aligned with existing KB and approved offers

## 8) Technical Plan

### Phase 1 — Structural conversion pass (high impact, low risk)
Scope:
- Section reorder in `index.html` owner route content
- Add How It Works section
- Add FAQ accordion
- Add no-pressure guarantee block
- Harmonize CTA language by section context

Estimate: 1-2 days

### Phase 2 — Interactive persuasion tools
Scope:
- Add Cost of Waiting calculator
- Upgrade current calculator outputs and assumptions label
- Add story stack carousel/cards with structured data source

Estimate: 2-3 days

### Phase 3 — Analytics and experimentation foundation
Scope:
- Add analytics event layer wrappers in inline JS
- Route events to Meta Pixel + Vercel Analytics + optional webhook
- Validate event payloads in browser devtools and logs

Estimate: 1-2 days

### Phase 4 — Follow-up optimization
Scope:
- Post-booking "what to expect" module
- GHL tag routing and segmentation
- 90-day nurture skeleton (outside page code; in GHL automations)

Estimate: 2-3 days

## 9) Event Taxonomy (v1)

- `section_view`  
  props: `section_id`, `scroll_depth_pct`, `session_id`

- `calculator_interaction`  
  props: `calculator_id`, `field`, `value`, `service_context`

- `calculator_result_view`  
  props: `calculator_id`, `monthly_impact`, `annual_impact`, `confidence_band`

- `cta_click`  
  props: `cta_id`, `section_id`, `cta_variant`, `destination_anchor`

- `faq_expand`  
  props: `question_id`, `section_id`, `expanded_state`

- `booking_widget_open` / `booking_start` / `booking_submit`  
  props: `entry_section`, `service_context`, `device_type`

- `chat_open` / `chat_message_sent`  
  props: `entry_section`, `time_on_page_sec`, `device_type`

## 10) Experiment Backlog (initial 8)

1. Hero headline: authority-led vs pain-led  
2. CTA copy: "Book FREE Estimate" vs "See What Waiting Costs"  
3. Calculator placement: above vs below service grid  
4. FAQ placement: mid-page vs pre-final CTA  
5. Story format: carousel vs static 3-card grid  
6. No-pressure guarantee: short vs long owner message  
7. Offer framing: $500 gift card first vs 12-month lock first  
8. Final CTA layout: single primary vs primary+secondary split

For each test:
- Primary metric: booking submit rate
- Guardrails: bounce rate, time to first interaction, chat deflection, rage-clicks

## 11) Risks and Mitigations

- Risk: Overloading users with too many widgets  
  Mitigation: progressive disclosure; one primary action per section.

- Risk: Aggressive urgency harms trust  
  Mitigation: remove hype language; keep transparent assumptions and dates.

- Risk: Event noise and inconsistent naming  
  Mitigation: lock event schema before launch; validate with preflight checklist.

- Risk: Mobile clutter from sticky CTA + chat  
  Mitigation: enforce collision offsets and z-index audits on common breakpoints.

## 12) Acceptance Checklist

- [ ] Journey order reflects 4-step framework
- [ ] New modules are responsive and accessible
- [ ] All CTAs route correctly to booking or relevant action
- [ ] Event tracking fires with expected payloads
- [ ] Booking + chat widgets remain functional
- [ ] Copy remains on-brand and no-pressure
- [ ] Lighthouse performance does not regress materially

