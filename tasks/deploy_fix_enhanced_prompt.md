# Enhanced Prompt — Fix Vercel Deployment + Publish Owner Dashboard

Objective: make the current branch deploy successfully on Vercel and publish the private owner dashboard routes live without breaking public pages.

## Constraints
- Keep public landing page behavior unchanged.
- Keep owner auth/API/dashboard functionality unchanged.
- Fix deployment blocker with the smallest safe diff.
- Preserve cron API endpoints, but do not require paid-plan-only platform features in deployment config.

## Required execution steps
1. Identify deployment blocker from CI status/log links.
2. Remove or rework unsupported Vercel config causing deployment failure.
3. Keep routes functional:
   - `/owner`
   - `/owner/dashboard`
   - `/api/*`
4. Update docs/runbook to clarify:
   - cron endpoints still exist
   - scheduled invocation depends on Vercel plan capability
   - manual secure invocation fallback
5. Commit + push to active feature branch.
6. Verify live deploy success via commit status and URL checks.
7. Return final live URLs for:
   - Owner login
   - Owner dashboard

## Validation checklist
- `vercel.json` remains valid JSON.
- Branch commit shows successful Vercel deployment status.
- Live `/owner` and `/owner/dashboard` return owner portal HTML (not public homepage fallback).
- `/api/auth/session` returns JSON response contract.
