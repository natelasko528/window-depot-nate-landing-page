# PRD: Private Owner Performance Dashboard

> Status: **APPROVED — executing**
> Last updated: March 13, 2026

---

## 1. Introduction / Overview

A private, password-protected analytics dashboard deployed at `/owner` on the same Vercel project. Monitors real-time social media post performance across Facebook, Instagram, and LinkedIn. Accessible only by Nate via password authentication. Hidden from public users — no links, no sitemap entry.

---

## 2. Goals

- Real-time visibility into post performance by platform and by individual post
- Trend tracking (7d, 30d, delta vs prior period)
- Automated hourly data sync from GoHighLevel
- Anomaly detection: flag winners and underperformers
- Zero regression on the existing public landing page
- Deployable on the same Vercel project with no framework changes

---

## 3. Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Vercel Project                        │
│                                                         │
│  PUBLIC                  PRIVATE (auth-gated)            │
│  /  → index.html         /owner → login page            │
│                          /owner/dashboard → dashboard    │
│                                                         │
│  SERVERLESS FUNCTIONS (api/)                            │
│  /api/auth/login      POST   Password → JWT cookie      │
│  /api/auth/logout     POST   Clear cookie                │
│  /api/auth/session    GET    Verify session               │
│  /api/performance/summary  GET  KPI + platform data      │
│  /api/performance/posts    GET  Per-post metrics          │
│  /api/cron/sync       GET    Hourly GHL sync (cron)      │
│                                                         │
│  ENV VARS (Vercel Dashboard)                            │
│  OWNER_PASSWORD      Login password                      │
│  SESSION_SECRET      JWT signing key                     │
│  GHL_API_KEY         GoHighLevel API v2 token            │
│  GHL_LOCATION_ID     GHL location for social posts       │
│  CRON_SECRET         Vercel cron verification            │
└─────────────────────────────────────────────────────────┘
```

---

## 4. Screen Mesh Layout

### 4a. Login Page — `/owner`

```
╔══════════════════════════════════════════════╗
║                                              ║
║              ┌──────────────┐                ║
║              │   WD Shield  │                ║
║              │    (logo)    │                ║
║              └──────────────┘                ║
║                                              ║
║           Owner Dashboard Access             ║
║                                              ║
║         ┌────────────────────────┐           ║
║         │  🔒 Password           │           ║
║         │  [________________]    │           ║
║         │                        │           ║
║         │  [ ══ Sign In ══ ]     │           ║
║         │                        │           ║
║         │    ● Error message     │           ║
║         └────────────────────────┘           ║
║                                              ║
║        This page is not public.              ║
╚══════════════════════════════════════════════╝
```

**Design tokens:**
- Background: `--navy` (#0A1628)
- Card: `--navy2` (#1A2F50) with `--shadow-lg`
- CTA button: `--gold2` (#D4AF37) with dark text
- Input: transparent border-bottom, white text
- Border radius: `--radius` (16px)

---

### 4b. Dashboard — `/owner/dashboard`

```
╔══════════════════════════════════════════════════════════════╗
║  HEADER BAR (fixed top)                                      ║
║  ┌──────────────────────────────────────────────────────────┐║
║  │ ◆ WD     Owner Dashboard          [🔄 Sync] [Sign Out] │║
║  │          Last sync: 2 min ago  ●                        │║
║  └──────────────────────────────────────────────────────────┘║
║                                                              ║
║  DEMO MODE BANNER (shown when GHL not connected)             ║
║  ┌──────────────────────────────────────────────────────────┐║
║  │ ⚡ Demo Mode — Connect GHL API to see live data          │║
║  └──────────────────────────────────────────────────────────┘║
║                                                              ║
║  KPI STRIP (4-column grid, responsive → 2-col on mobile)     ║
║  ┌────────────┐ ┌────────────┐ ┌────────────┐ ┌───────────┐║
║  │ TOTAL      │ │ TOTAL      │ │ AVG        │ │ ACTIVE    │║
║  │ REACH      │ │ ENGAGEMENT │ │ CTR        │ │ POSTS     │║
║  │            │ │            │ │            │ │           │║
║  │  45,230    │ │  3,847     │ │  4.2%      │ │  72/90    │║
║  │  ▲ 12.3%   │ │  ▲ 8.1%    │ │  ▼ 0.3%    │ │           │║
║  │  vs 7d ago │ │  vs 7d ago │ │  vs 7d ago │ │           │║
║  └────────────┘ └────────────┘ └────────────┘ └───────────┘║
║                                                              ║
║  FILTERS ROW                                                 ║
║  ┌──────────────────────────────────────────────────────────┐║
║  │ Platform: [All ▾]   Period: [7 Days ▾]   🔍 Search...   │║
║  └──────────────────────────────────────────────────────────┘║
║                                                              ║
║  PLATFORM BREAKDOWN (3-column, responsive → stack)           ║
║  ┌─────────────────┐ ┌─────────────────┐ ┌────────────────┐║
║  │   FACEBOOK      │ │   INSTAGRAM     │ │   LINKEDIN     │║
║  │   ━━━━━━━━━━    │ │   ━━━━━━━━━━━━  │ │   ━━━━━━━━     │║
║  │                 │ │                 │ │                │║
║  │   30 posts      │ │   30 posts      │ │   30 posts     │║
║  │   15.2K reach   │ │   18.1K reach   │ │   12.0K reach  │║
║  │   1.2K engage   │ │   1.5K engage   │ │   1.1K engage  │║
║  │   3.8% CTR      │ │   4.7% CTR      │ │   3.1% CTR     │║
║  │                 │ │                 │ │                │║
║  │   ▓▓▓▓▓░░░░░   │ │   ▓▓▓▓▓▓░░░░   │ │   ▓▓▓▓░░░░░░  │║
║  │   reach bar     │ │   reach bar     │ │   reach bar    │║
║  └─────────────────┘ └─────────────────┘ └────────────────┘║
║                                                              ║
║  ENGAGEMENT TREND (full-width chart card)                    ║
║  ┌──────────────────────────────────────────────────────────┐║
║  │  Engagement Over Time                    [7d] [30d] [All]│║
║  │                                                          │║
║  │     ╱╲         ╱╲                                        │║
║  │    ╱  ╲  ╱╲  ╱  ╲    ╱╲                                 │║
║  │   ╱    ╲╱  ╲╱    ╲──╱  ╲───                             │║
║  │  ╱                       ╲                               │║
║  │  ── FB (gold)  ── IG (blue)  ── LI (gray)               │║
║  │                                                          │║
║  └──────────────────────────────────────────────────────────┘║
║                                                              ║
║  POST LEADERBOARD (sortable table, full-width)               ║
║  ┌──────────────────────────────────────────────────────────┐║
║  │  Post Performance                    Sort: [CTR ▾]       │║
║  │  ────────────────────────────────────────────────────── │║
║  │  #  │ Image │ Theme      │ Platform │ Reach │ Eng │ CTR │║
║  │  ── │ ───── │ ────────── │ ──────── │ ───── │ ─── │ ─── │║
║  │  1  │ [img] │ Windows    │ 📘 FB    │ 2.3K  │ 312 │5.1% │║
║  │  2  │ [img] │ Bathroom   │ 📸 IG    │ 1.9K  │ 287 │4.8% │║
║  │  3  │ [img] │ Roofing    │ 💼 LI    │ 1.4K  │ 201 │4.2% │║
║  │  4  │ [img] │ Doors      │ 📘 FB    │ 1.2K  │ 178 │3.9% │║
║  │  ...                                                     │║
║  │                                                          │║
║  │  ┌─ EXPANDED ROW (click to toggle) ───────────────────┐  │║
║  │  │ Post #1 — Windows — Facebook                       │  │║
║  │  │                                                     │  │║
║  │  │ [Thumbnail]  Caption: "Wisconsin winters hit..."    │  │║
║  │  │              Published: Mar 5, 2026                 │  │║
║  │  │                                                     │  │║
║  │  │ ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐ ┌──────┐ │  │║
║  │  │ │ 👍  │ │ 💬  │ │ 🔁  │ │ 📌  │ │ 🖱️  │ │ 📊   │ │  │║
║  │  │ │ 198 │ │  45 │ │  69 │ │  32 │ │ 112 │ │ 5.1% │ │  │║
║  │  │ │Like │ │Comm │ │Share│ │Save │ │Click│ │ CTR  │ │  │║
║  │  │ └─────┘ └─────┘ └─────┘ └─────┘ └─────┘ └──────┘ │  │║
║  │  └─────────────────────────────────────────────────────┘  │║
║  └──────────────────────────────────────────────────────────┘║
║                                                              ║
║  ALERTS PANEL                                                ║
║  ┌──────────────────────────────────────────────────────────┐║
║  │  Alerts & Insights                                       │║
║  │                                                          │║
║  │  ⚡ Post #7 (FB) is trending — 3× avg engagement         │║
║  │  ⚡ Post #15 (IG) hit 500+ engagements                   │║
║  │  ⚠️  Post #22 (LI) underperforming — 0.5% CTR           │║
║  │  ✅ All 30 Facebook posts published on schedule           │║
║  │  ✅ All 30 Instagram posts published on schedule          │║
║  └──────────────────────────────────────────────────────────┘║
║                                                              ║
║  FOOTER                                                      ║
║  ┌──────────────────────────────────────────────────────────┐║
║  │  Window Depot USA of Milwaukee · Owner Dashboard · v1.0  │║
║  └──────────────────────────────────────────────────────────┘║
╚══════════════════════════════════════════════════════════════╝
```

---

## 5. Component Specifications

### KPI Cards
- Gold top-border accent (3px)
- Large number with `font-size: 2rem; font-weight: 700`
- Delta indicator: green arrow ▲ for positive, red arrow ▼ for negative
- Comparison text: "vs 7d ago" in muted gray

### Platform Cards
- Platform icon + name as header
- Key metrics listed vertically
- Horizontal progress bar showing relative performance (reach ÷ max reach)
- Bar color: gold for FB, blue for IG, gray for LI

### Trend Chart
- Chart.js line chart with 3 series (FB, IG, LI)
- Toggle between 7d / 30d / All time
- Tooltip on hover showing exact values
- Grid lines: subtle white at 10% opacity

### Post Table
- Sortable by any column (click header)
- Platform icons: 📘 FB, 📸 IG, 💼 LI
- Click row to expand detailed view
- Expanded view shows: thumbnail, caption, publish date, 6 metric cards
- Pagination: 20 posts per page

### Alerts Panel
- Three alert types:
  - ⚡ Winner (gold left-border) — post exceeding 2× average engagement
  - ⚠️ Underperformer (red left-border) — post below 50% of average
  - ✅ Status (green left-border) — system health, scheduling confirmations

---

## 6. Functional Requirements

- FR-1: Owner can log in with a single password at `/owner`
- FR-2: Invalid password shows inline error, no page redirect
- FR-3: Session persists for 24 hours via HttpOnly secure cookie
- FR-4: Dashboard loads data via authenticated API calls
- FR-5: All API endpoints reject requests without valid session
- FR-6: Dashboard shows "Demo Mode" banner when GHL is not configured
- FR-7: Filters update dashboard data in real-time (client-side filtering)
- FR-8: Trend chart toggles between 7d / 30d / All time
- FR-9: Post table is sortable by any column
- FR-10: Clicking a post row expands detailed metrics
- FR-11: Cron job syncs data from GHL every hour
- FR-12: Alerts auto-generate based on performance thresholds

---

## 7. Non-Goals

- No multi-user auth system (single owner password)
- No editing posts from the dashboard
- No direct Facebook/Instagram API integration (all through GHL)
- No email/SMS alert notifications in v1 (dashboard alerts only)
- No A/B test management from the dashboard

---

## 8. Technical Considerations

- Vercel serverless functions for all API endpoints (Node.js runtime)
- JWT-based sessions using built-in `crypto` module (zero dependencies)
- Chart.js 4.x from CDN for trend charts
- GHL API v2 for data fetching (with demo data fallback)
- All API keys stored as Vercel environment variables
- Cron secured with CRON_SECRET header verification

---

## 9. Required Environment Variables

| Variable | Purpose | Required |
|----------|---------|----------|
| `OWNER_PASSWORD` | Dashboard login password | Yes |
| `SESSION_SECRET` | JWT signing secret (min 32 chars) | Yes |
| `GHL_API_KEY` | GoHighLevel API v2 bearer token | For live data |
| `GHL_LOCATION_ID` | GHL location ID for social posts | For live data |
| `CRON_SECRET` | Vercel cron job verification | For cron |

---

## 10. Success Criteria

- [ ] Owner can log in and see dashboard
- [ ] Dashboard displays KPI cards, platform breakdown, trend chart, post table, alerts
- [ ] All 90 posts (30 FB + 30 IG + 30 LI) visible in the table
- [ ] Filters work correctly (platform, date range)
- [ ] Chart toggles between time periods
- [ ] Post rows expand to show detailed metrics
- [ ] Public landing page is completely unaffected
- [ ] `/owner` is not discoverable from the public site
- [ ] Demo mode works fully when GHL is not connected
