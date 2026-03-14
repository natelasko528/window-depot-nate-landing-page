# Owner Dashboard + Monitoring Automation — Deploy Runbook

This runbook documents safe deployment for the private owner dashboard routes and cron automation on Vercel.

## 1) Scope

- Preserve public static landing page behavior.
- Support private owner routes:
  - `/owner`
  - `/owner/dashboard`
- Keep API routes (`/api/*`) reachable without rewrite conflicts.
- Enable scheduled monitoring jobs:
  - `/api/cron/sync-performance` (hourly)
  - `/api/cron/evaluate-alerts` (every 30 minutes)

## 2) Required Vercel Environment Variables

Set these in **Project Settings → Environment Variables** for Production (and Preview where needed).

| Variable | Required | Purpose | Recommended rotation |
|---|---|---|---|
| `OWNER_DASHBOARD_PASSWORD` | Yes | Owner login credential gate for `/owner`. | Every 90 days or after personnel access change |
| `SESSION_SECRET` | Yes | Signs/encrypts owner session cookie. | Every 90 days |
| `GHL_API_TOKEN` | Yes | GoHighLevel API token for metrics sync. | Every 60–90 days (or provider policy) |
| `GHL_LOCATION_ID` | Yes | GoHighLevel location context for data pulls. | On location/account changes |
| `CURSOR_AGENT_WEBHOOK_URL` | Optional | Sends approved owner requests to external agent workflow. | Rotate on integration changes |
| `CRON_SHARED_SECRET` | Recommended | Optional shared secret check for cron endpoints if implemented in API handlers. | Every 90 days |

## 3) Deployment Steps

1. Confirm `vercel.json` includes:
   - ordered rewrites for `/api/*`, `/owner`, `/owner/dashboard`, then static fallback
   - cron definitions for the two monitoring endpoints
2. In Vercel, verify all required environment variables are set for Production.
3. Deploy from the target branch (or merge to `main` per release process).
4. After deployment, run smoke checks:
   - `GET /` loads landing page
   - `GET /owner` resolves to owner login page
   - `GET /owner/dashboard` resolves to private dashboard route (auth-protected by app logic)
   - `GET /api/cron/sync-performance` and `GET /api/cron/evaluate-alerts` return expected response/guard behavior
5. In Vercel Dashboard:
   - check **Functions** logs for cron executions
   - confirm each cron appears under project cron jobs with correct schedule

## 4) Security Checklist (Pre-Production)

- [ ] `OWNER_DASHBOARD_PASSWORD` is strong and unique (not reused).
- [ ] `SESSION_SECRET` is high-entropy (at least 32 random bytes).
- [ ] Owner session cookie is `HttpOnly`, `Secure`, and `SameSite=Lax` (or stricter) in production.
- [ ] Owner API endpoints enforce session auth on every request.
- [ ] Cron endpoints reject non-cron traffic unless explicitly intended.
- [ ] No secrets are hardcoded in repo, commit history, or client-side JS.
- [ ] Vercel project access is limited to authorized operators only.
- [ ] Deployment notifications/log access is restricted to approved team members.

## 5) Rotation Policy

Use this baseline unless company policy requires tighter windows:

- **90 days**: `OWNER_DASHBOARD_PASSWORD`, `SESSION_SECRET`, `CRON_SHARED_SECRET`
- **60–90 days**: `GHL_API_TOKEN`
- **Event-driven rotation**:
  - team member departure/access change
  - suspected key exposure
  - third-party integration compromise
  - migration of GHL account/location

After rotating:
1. Update values in Vercel env vars.
2. Trigger a redeploy.
3. Verify owner login + cron job execution in logs.

## 6) Troubleshooting

### Symptom: `/api/*` returns landing page HTML
- Cause: catch-all rewrite is matching before API routes.
- Fix: keep `/api/:path* -> /api/:path*` rewrite above fallback rewrite.

### Symptom: `/owner` or `/owner/dashboard` serves public page
- Cause: owner rewrites missing or placed below catch-all rewrite.
- Fix: keep owner rewrites above `/(.*) -> /index.html`.

### Symptom: Cron appears configured but never runs
- Cause: wrong cron path, cron disabled, or deployment mismatch.
- Fix:
  1. confirm cron `path` exactly matches deployed API endpoint
  2. verify schedule syntax and timezone assumptions (UTC)
  3. inspect Vercel function logs at expected run windows

### Symptom: Cron executes but fails auth/data fetch
- Cause: missing/expired `GHL_API_TOKEN`, invalid `GHL_LOCATION_ID`, or secret mismatch.
- Fix: re-check env vars, rotate token, redeploy, and run endpoint smoke checks.

## 7) Operational Notes

- Cron jobs should stay lightweight and idempotent.
- Keep alert evaluation more frequent than full sync only when endpoint logic supports stale-data handling.
- Prefer explicit owner route rewrites over implicit fallback behavior for private pages.
