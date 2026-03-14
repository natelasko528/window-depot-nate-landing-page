# Owner Dashboard + Monitoring Runbook

Concise operations guide for the private owner dashboard, cron monitoring, and owner chat handoff flow.

## 1) First-time setup checklist

- [ ] Confirm `vercel.json` includes owner rewrites (no catch-all override issues).
- [ ] Create Production env vars in Vercel (table below).
- [ ] Deploy and verify `/` (public), `/owner`, and `/owner/dashboard`.
- [ ] Smoke test cron endpoints locally and in deployed env.
- [ ] Confirm scheduled runs appear in Vercel function logs.
- [ ] Validate owner chat and export/handoff behavior.

## 2) Environment variables

| Variable | Required | Used for | Rotation baseline |
|---|---|---|---|
| `OWNER_DASHBOARD_PASSWORD` | Yes | Owner login gate | Every 90 days |
| `SESSION_SECRET` | Yes | Session signing/encryption | Every 90 days |
| `GHL_API_TOKEN` | Yes | GoHighLevel API access for sync/metrics | Every 60-90 days |
| `GHL_LOCATION_ID` | Yes | GoHighLevel location/account scope | On account/location change |
| `CURSOR_AGENT_WEBHOOK_URL` | Optional | Pushes approved owner requests to Cursor workflow | On integration changes |
| `CURSOR_AGENT_WEBHOOK_TOKEN` | Optional | Bearer auth for Cursor webhook dispatch | On integration changes |
| `CRON_SHARED_SECRET` or `CRON_SECRET` | Recommended | Verifies cron-origin requests (if enforced by handlers) | Every 90 days |

## 3) Rotating password / session secret / API token

1. Generate new values:
   - Password: long unique passphrase
   - Session secret: at least 32 random bytes (base64/hex safe)
   - API token: fresh token from GoHighLevel
2. Update env vars in Vercel Production.
3. Redeploy.
4. Verify:
   - owner login works with new password
   - prior sessions are invalidated after `SESSION_SECRET` rotation
   - sync endpoints can access GHL successfully

## 4) Verifying cron runs

### Scheduling model
- Cron endpoints remain available:
  - `/api/cron/sync-performance`
  - `/api/cron/evaluate-alerts`
- Use one of:
  1. Vercel scheduled jobs (if your plan supports it), or
  2. External scheduler (GitHub Actions, GoHighLevel workflow, or monitor service).

### Checks
1. Open Function logs and filter by each cron path.
2. Confirm execution timestamps match your configured scheduler windows.
3. Trigger manual smoke calls if needed:
   - `curl -i https://<deployment>/api/cron/sync-performance`
   - `curl -i https://<deployment>/api/cron/evaluate-alerts`

## 5) Troubleshooting common failures

### `/owner` or `/owner/dashboard` returns public page
- Cause: rewrite order issue.
- Fix: keep owner rewrites above catch-all `/(.*) -> /index.html`.

### `/api/*` returns HTML instead of JSON
- Cause: API rewrite not matched first.
- Fix: keep `/api/:path* -> /api/:path*` as top rewrite.

### Cron not firing
- Cause: no scheduler configured, plan limitation, path mismatch, or deployment mismatch.
- Fix: configure external scheduler (or supported Vercel cron), verify endpoint path and UTC expectation.

### Cron fires but data sync fails
- Cause: invalid/expired `GHL_API_TOKEN` or wrong `GHL_LOCATION_ID`.
- Fix: rotate token, confirm location ID, redeploy, re-check logs.

### Owner login keeps failing
- Cause: wrong `OWNER_DASHBOARD_PASSWORD` or stale deployment env.
- Fix: re-enter env var in Vercel, redeploy, retry in a fresh browser session.

## 6) Owner chat -> Cursor handoff flow

1. Owner submits request in dashboard chat (`/api/owner/chat`).
2. System returns:
   - conversational response for owner
   - structured change-request payload
3. Owner reviews/approves the request in dashboard.
4. Handoff step:
   - generate copy/paste task via `/api/owner/export-request`, or
   - auto-dispatch to `CURSOR_AGENT_WEBHOOK_URL` when configured.
5. Operator verifies webhook delivery/logs and tracks resulting Cursor task.

Operational note: keep the handoff payload specific (goal, files, acceptance criteria) so generated implementation tasks are reproducible.
