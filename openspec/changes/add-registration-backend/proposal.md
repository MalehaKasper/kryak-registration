## Why

The event "Вишкіл з фінансової грамотності Макдака" needs two public application forms (провід і лектори) that (1) work for anyone who opens the link, regardless of whether they have any account, (2) reliably persist every submission so the organizer can review them as a list, and (3) keep the comic-book visual identity already built for the event's presentation.

Three approaches were tried and explored first and each fails at least one requirement:
- A pure `mailto:` link depends on the visitor's device having a mail client configured — this already failed a live test from a phone.
- Anthropic's Artifact `artifact` capability requires the submitter to have edit access to the page, which in practice requires a Claude account and an explicit share grant — incompatible with "anyone with the link, up to ~100 people."
- Google Forms solves reliability and storage, but its UI cannot be restyled to match the comic identity beyond a header banner and accent color — an aesthetic compromise the organizer wants to avoid if avoidable. It was also confirmed that a hidden/invisible submission from within an Artifact page to any external host (Google Forms or otherwise) is blocked by the Artifact sandbox's CSP — so keeping the current design without any hosting change is not possible.

The organizer already has a free PythonAnywhere account, which is sufficient (CPU, storage, and bandwidth quotas checked) to run a small always-on Flask app for this purpose at no cost.

## What Changes

- New standalone Flask application (separate small codebase, not part of `kryakobank`) hosted on PythonAnywhere's free tier at `MalehaKasper.pythonanywhere.com`.
- Two public HTML pages reusing the existing comic-book design already built for the two Artifact-based forms (провід registration, лектор registration) — same fields, same visual style, now served from this app instead of from a Claude Artifact.
- Each form POSTs to its own route on this app, which validates the input and writes a row to a local SQLite database.
- One password-protected admin page per form listing all submitted responses in a table (name, contact, chosen tasks/talks, free-text fields, timestamp) — visible only to the organizer.
- The "Приєднатись до проводу" / "Зголоситись лектором" buttons on the existing presentation Artifact will be updated to point at these new pages once deployed (tracked as a follow-up task here, executed against the existing Artifact, not this repo).

## Capabilities

### New Capabilities
- `registration-intake`: Public HTML forms (провід, лектори) and their submission endpoints — collects the same fields already designed (name, Telegram, phone, task/talk selection, free-text idea, free-text about) and validates that at least one contact method is provided.
- `response-storage`: Persistent storage of every submitted response (SQLite, one table per form) that survives app restarts and redeploys.
- `response-review`: Password-protected pages that list all stored responses for a form in a sortable/readable table, accessible only to the organizer.

### Modified Capabilities
- None — this is a new, standalone application. No existing spec is being changed.

## Impact

- New repository/codebase at `/Users/admin/Documents/project/kryak-registration` (Flask + SQLite), deployed to PythonAnywhere (free tier, account `MalehaKasper`).
- No changes to the `kryakobank` app or its database.
- The presentation Artifact (`Вишкіл з фінансової грамотності Макдака`) needs its two CTA button URLs updated once this app is deployed and reachable — a manual follow-up step, not a code change in this repo.
- Organizer takes on light operational ownership: this becomes a real always-on service they're responsible for (as opposed to the zero-maintenance Artifact/Google Forms options), in exchange for keeping full control of design, data, and access.
