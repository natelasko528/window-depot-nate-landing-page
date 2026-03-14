# Enhanced Execution Prompt — Owner Analytics + Control Center

Build a private, production-ready **Owner Analytics & Control Center** for Window Depot USA of Milwaukee using the current project stack (pure HTML/CSS/JS + Vercel serverless functions).

## Non-negotiables
1. Keep all existing public pages and V3 social images unchanged.
2. Add hidden owner-only routes:
   - `/owner` (secure login)
   - `/owner/dashboard` (private analytics + controls)
3. Use real GoHighLevel data for performance metrics.
4. Add monitoring automation with Vercel cron endpoints.
5. Add owner chat interface to request campaign changes.
6. Include a **Cursor handoff bridge**:
   - convert approved chat requests into structured change prompts
   - optional webhook dispatch if environment variables are configured
7. Keep visual design consistent with existing brand style.

## Required features

### Security + access
- Owner password login using env var (`OWNER_DASHBOARD_PASSWORD`).
- Signed HttpOnly session cookie using `SESSION_SECRET`.
- All owner APIs require authenticated session.

### Data + monitoring
- GHL integration using `GHL_API_TOKEN` + `GHL_LOCATION_ID`.
- Pull and normalize:
  - scheduled/published post records
  - post-level metrics
  - platform rollups
- Vercel cron endpoints:
  - `/api/cron/sync-performance`
  - `/api/cron/evaluate-alerts`
- Alert rules for:
  - high performers
  - low performers
  - stale/no-activity posts

### Private dashboard UX
- KPI cards (impressions, reach, engagement rate, clicks)
- Platform breakdown (FB/IG/LinkedIn)
- Top/bottom post ranking
- Post table with filtering
- Last sync + API health status
- Owner Copilot chat panel

### Owner chat + Cursor bridge
- `/api/owner/chat` endpoint:
  - returns guidance and optimization suggestions from live metrics
  - generates structured change-request payloads
- `/api/owner/export-request` endpoint:
  - outputs copy/paste-ready Cursor task prompt
  - optional POST to `CURSOR_AGENT_WEBHOOK_URL` if configured

## Deployment + ops
- Keep static site behavior intact.
- Add required Vercel env variables in docs.
- Add `vercel.json` cron configuration and preserve public routing.

## Validation requirements
- Auth/session tests
- API response contract checks
- Live GHL smoke tests
- Cron endpoint smoke tests
- Manual owner dashboard walkthrough with video artifact
- Confirm no regressions on public landing page
