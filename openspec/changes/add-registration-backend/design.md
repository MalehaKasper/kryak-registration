## Context

Two comic-styled registration forms (провід, лектори) already exist and were fully designed as standalone Claude Artifacts. Three prior approaches to making them reliably persist responses were explored and ruled out:

- `mailto:`-only submission — depends on the visitor's device having a configured mail client; failed a live mobile test.
- Anthropic Artifact `artifact` capability — requires the submitter to hold edit access to the page, which requires a Claude account and an explicit share grant from the organizer; incompatible with an open, ~100-person, no-login audience. Also confirmed: an Artifact page cannot silently POST to any external host (own server or Google Forms) — its CSP blocks it. Verified by a direct `curl` POST to the test Google Form's `formResponse` endpoint, which succeeded, while the same submission attempted from inside the Artifact sandbox did not.
- Google Forms (real, visible redirect) — works reliably and solves storage/privacy, but its theming is limited to a header image and accent color; cannot fully carry the comic-book identity.

The organizer already has a free PythonAnywhere account (verified against the current free-tier quotas: 512 MB storage, 100 CPU-seconds/day, one always-on web app on a `pythonanywhere.com` subdomain), which comfortably covers an expected volume of "up to 100" submissions across both forms over the life of one event.

## Goals / Non-Goals

**Goals:**
- Anyone can open either form and submit it with no account and no login, from any device.
- Every submission is durably stored (survives app restarts/redeploys) and reviewable as a table.
- Only the organizer can view submitted responses.
- The existing comic-book visual design is carried over unchanged.
- Stay comfortably inside PythonAnywhere's free-tier quotas.

**Non-Goals:**
- Real-time notifications (e.g. push/email) when a new response arrives — the organizer will check the admin page manually.
- Editing or deleting responses through the UI — v1 is read-only review; corrections happen by contacting the applicant directly.
- Multi-admin roles or fine-grained permissions — one shared organizer credential is sufficient.
- Migrating storage off SQLite, or supporting materially more than ~200 total responses.
- Hardened production security beyond the basics appropriate to a low-value, low-traffic internal recruiting form (no WAF, no rate limiting beyond what Flask/PythonAnywhere give for free).
- Automating deployment (CI/CD) — updates are applied manually through PythonAnywhere's web console, matching the scale of the project.

## Decisions

- **Framework: Flask.** Matches the stack already used for `kryakobank`, is PythonAnywhere's best-supported quick-start option, and needs no extra services. Alternative considered: a Node app — rejected, no reuse of existing knowledge/tooling and PythonAnywhere's free tier is Python-first.
- **Storage: SQLite via the Python standard library, two tables (`provid_responses`, `lecturer_responses`).** The free tier has no free managed Postgres, and SQLite's persistent-file model fits PythonAnywhere's free disk quota (512 MB) with enormous headroom for ~100 rows. Alternative considered: keep exploring hosted Postgres (Supabase/Neon free tiers) — rejected as unnecessary complexity and an extra account/service to depend on for this volume.
- **Two separate forms/tables, not one branching form.** Matches the organizer's explicit decision earlier in the process ("окремі форми потрібно") — provid and lecturer applications are never merged.
- **Submission mechanism: plain HTML `<form method="POST">` to a Flask route, no client-side fetch/JS needed.** The existing Artifact pages' JS (built for the `mailto:`/`artifact`-capability attempts) is replaced by a normal form post; Flask re-renders the same page with a visible "дякуємо" confirmation. Simpler and more robust than a JS-driven submit, and there is no CSP to fight now that the page is served from our own origin.
- **Reuse existing HTML/CSS almost verbatim.** The comic-book styling already built for the two Artifact forms is carried over as-is; only the `<form>` `action`/`method` and the submit-handling script are replaced.
- **Admin auth: HTTP Basic Auth, one shared username/password held only by the organizer.** Proportionate to a single-admin, low-traffic internal tool. Alternative considered: a full login system with sessions — rejected as more code and more to maintain for no real benefit at this scale.
- **Deployment: PythonAnywhere "Beginner" free web app, manually configured**, code placed via a Bash console (`git clone`) or the Files web UI, no SSH (not available on the free tier). Manual "Reload" through the Web tab after any code change.

## Risks / Trade-offs

- **[Risk] Free-tier CPU/storage limits are exceeded** → Mitigation: expected load (~100 submissions total, occasional admin page views) is far below the 100 CPU-seconds/day and 512 MB quotas; re-check quotas if actual usage looks unusual.
- **[Risk] No SSH makes deployment/debugging more manual** → Mitigation: keep the app to a handful of files; use PythonAnywhere's web-based Bash console and file editor, which cover everything needed at this scale.
- **[Risk] The organizer is now operationally responsible for an always-on service** (unlike the zero-maintenance Artifact/Google Forms options) → Mitigation: this is the accepted trade-off for keeping the design; the app is kept intentionally minimal to reduce what can break.
- **[Risk] HTTP Basic Auth is unsophisticated** → Mitigation: acceptable for a single admin and low-value target; served over HTTPS by default on the `pythonanywhere.com` subdomain.
- **[Risk] No automated backup of the SQLite file** → Mitigation: document a manual "download the `.db` file occasionally" step for the organizer; out of scope to automate in v1.
- **[Risk] Possible free-tier account dormancy policy** (unconfirmed at proposal time) → Mitigation: organizer to verify PythonAnywhere's policy before relying on this long-term; tracked as an open question below.

## Migration Plan

No existing data to migrate (new application). Deployment steps:
1. Create a new Flask web app in the PythonAnywhere "Web" tab (manual configuration, matching Python version).
2. Place the code in the account via a Bash console (`git clone`) or the Files UI.
3. Point the WSGI config file at this app's entry point.
4. Let the app create its SQLite file and tables on first run (or run a small one-off init script).
5. Set the admin Basic Auth credential via a PythonAnywhere environment variable (not hardcoded in the repo).
6. Reload the web app from the Web tab; verify both form URLs and both admin URLs.
7. Update the two CTA buttons on the presentation Artifact to point at the new form URLs (done outside this repo).

Rollback: disable/stop the PythonAnywhere web app and point the presentation's CTA buttons back at the previous Artifact-based registration pages, which remain published and unaffected.

## Open Questions

- Does a fully free (never-upgraded) PythonAnywhere account have any dormancy/deactivation policy requiring periodic login? Needs confirmation from PythonAnywhere's own docs/FAQ before this is treated as a long-term solution.
- Where exactly should the admin Basic Auth credential be set (PythonAnywhere env var vs. a small local config file excluded from version control)? Leaning toward env var, to confirm during implementation.
- Is a CSV-export button on the admin pages worth adding now, or a later nice-to-have? Not required for v1.
