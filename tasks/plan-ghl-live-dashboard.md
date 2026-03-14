# Execution Plan: GHL Live Data → Owner Dashboard

> Status: **READY FOR APPROVAL**
> Based on: Official OpenAPI spec + verified live API calls (March 14, 2026)

---

## What We Know (verified)

| Fact | Detail |
|------|--------|
| GHL credentials | `GHL_API_TOKEN` and `GHL_LOCATION_ID` already configured as Cursor secrets |
| Connected accounts | 7 accounts: 4 Facebook pages, 1 Instagram, 1 LinkedIn, 1 YouTube |
| Total posts | 428 (334+ published, ~90 scheduled, 4 failed) |
| Platforms | facebook, instagram, linkedin, google, youtube |
| Env var mismatch | Code uses `GHL_API_KEY` but secret is named `GHL_API_TOKEN` |
| Post metrics limitation | GHL API does NOT return per-post engagement — only 7-day aggregate via `/statistics` |

---

## What Needs to Change

### 1. Fix `api/_lib/ghl.js` — the core integration layer

**Current problems:**
- Checks `GHL_API_KEY` env var — should be `GHL_API_TOKEN`
- Uses GET with query params for posts/list — should be POST with string body fields
- Doesn't call `/accounts` or `/statistics` at all
- Response parsing expects `data.posts` — actual path is `data.results.posts`
- Platform detection guesses — API returns `platform` directly on each post

**Changes:**
- `isGHLConfigured()` → check `GHL_API_TOKEN` and `GHL_LOCATION_ID`
- Add `fetchAccounts(locationId, token)` → `GET /social-media-posting/{locationId}/accounts`
- Rewrite `fetchGHLPosts()` → `POST /posts/list` with correct string body fields, pagination loop (100 per page)
- Add `fetchStatistics(locationId, token, profileIds)` → `POST /statistics?locationId=X` with profileIds in body
- Fix `normalizePost()` to use verified field names: `_id`, `platform`, `summary`, `media`, `status`, `scheduleDate`, `publishedAt`, `parentPostId`, `accountIds`
- Handle pagination: loop skip 0→100→200→... until posts < limit

### 2. Fix `api/performance/summary.js` — dashboard KPI endpoint

**Changes:**
- Call `fetchAccounts()` first to get profileIds
- Call `fetchStatistics()` with those profileIds for real aggregate metrics
- Map `breakdowns.posts/impressions/reach/engagement` to dashboard KPI cards
- Map `postPerformance` daily arrays to trend chart series
- Use `breakdowns.{metric}.totalChange` for the delta indicators (real data, not hardcoded)
- Map `platformTotals` to per-platform breakdown cards
- Build alerts from real data: post failures, engagement drops, etc.

### 3. Fix `api/performance/posts.js` — post table endpoint

**Changes:**
- Paginate through ALL posts from `fetchGHLPosts()`
- Since individual post metrics aren't available, calculate engagement per-post from aggregate data proportionally or show "N/A"
- Alternative: show post list with status/caption/media/dates and per-platform aggregate stats

### 4. Fix `api/cron/sync.js` — hourly cron job

**Changes:**
- Use the corrected `fetchGHLPosts()` and `fetchStatistics()` functions
- Log sync results with timestamps

### 5. Update `owner/dashboard.html` — frontend

**Changes:**
- KPI deltas: use real `totalChange` percentages from statistics API instead of hardcoded values
- Trend chart: use `postPerformance` daily arrays (7-value arrays for last week)
- Platform cards: use `breakdowns.*.platforms.*` for real per-platform metrics
- Post table: show post metadata (caption, platform, status, dates, media thumbnail) — note engagement column will show aggregate not per-post
- Add "google" and "youtube" to platform filters since Nate has those accounts
- Add demographics section (gender/age) from statistics API

### 6. Update `vercel.json` — env var references

**Changes:**
- Add `OWNER_PASSWORD` and `SESSION_SECRET` to required env vars documentation
- Cron config already correct

---

## Execution Order

| Step | Task | Files | Depends On |
|------|------|-------|-----------|
| 1 | Rewrite `api/_lib/ghl.js` with verified endpoints | `api/_lib/ghl.js` | — |
| 2 | Update `api/performance/summary.js` to use new GHL functions | `api/performance/summary.js` | Step 1 |
| 3 | Update `api/performance/posts.js` to use new GHL functions | `api/performance/posts.js` | Step 1 |
| 4 | Update `api/cron/sync.js` | `api/cron/sync.js` | Step 1 |
| 5 | Update dashboard UI for real data shapes | `owner/dashboard.html` | Steps 2-3 |
| 6 | Test with live API calls | — | Steps 1-5 |
| 7 | Commit, push, verify deploy | — | Step 6 |

---

## Constraints & Gotchas

1. **No per-post engagement**: GHL statistics endpoint returns 7-day aggregate per platform, not per individual post. Dashboard post table will show post metadata + status, but engagement column will show platform-level averages or "N/A".

2. **Statistics is 7-day only**: No 30-day or all-time aggregate from GHL. For 30d view, we'd need to cache 7-day snapshots over time via the cron job. For v1, show the 7-day data we have and note this limitation.

3. **Rate limits**: 100 req/10s. With 428 posts requiring ~5 paginated calls + 1 accounts call + 1 statistics call = ~7 calls total. Well within limits.

4. **90 scheduled "google" posts**: These are future-dated GBP posts. They'll appear in the table as "scheduled" status which is correct.

5. **parentPostId grouping**: The same content posted to FB + IG + LI has the same `parentPostId`. Dashboard could group these or show flat.

---

## Vercel Environment Variables Required

Set these in Vercel Dashboard → Settings → Environment Variables:

| Variable | Value | Required For |
|----------|-------|-------------|
| `OWNER_PASSWORD` | Your chosen password | Dashboard login |
| `SESSION_SECRET` | Random 32+ char string | JWT session signing |
| `GHL_API_TOKEN` | Already set as Cursor secret | Live data |
| `GHL_LOCATION_ID` | Already set as Cursor secret | Live data |
| `CRON_SECRET` | Random string | Cron job security |
