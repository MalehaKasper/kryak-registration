## Why

The event presentation ("Вишкіл з фінансової грамотності Макдака") and its comic viewer currently live as two separate Claude Artifacts on claude.ai, while the two registration forms they link out to now live on `malehakasper.pythonanywhere.com`. This split means visitors jump between two unrelated domains mid-flow, the organizer manages two different publishing mechanisms for one coherent site, and the Artifacts carry every image as an inline base64 data URI (no real static-file serving), which the organizer specifically flagged as unnecessarily heavy — 1.86 MB for the presentation and 6.22 MB for the comic viewer. Moving both pages onto the same PythonAnywhere app the forms already run on gives one domain, one place to maintain everything, real static-file serving (smaller pages, browser caching), and more room to extend the site later without juggling two hosting mechanisms.

## What Changes

- Add two new pages to the existing `kryak-registration` Flask app: the presentation page (currently the Artifact at `.../artifact/c5ec031d-...`) and the comic viewer page (currently `.../artifact/200f6c6f-...`).
- Convert every embedded base64 image in both pages (screenshots, comic panels, cover art, the Крякобанк logo) into real files under `static/`, referenced by normal `<img src>` / `url_for('static', ...)` instead of inline data URIs.
- Update the two CTA buttons on the presentation ("Приєднатись до проводу", "Зголоситись лектором") and the comic link to use relative in-app paths instead of full claude.ai Artifact URLs.
- Update the presentation's link to the comic viewer, and the comic viewer's "back to presentation" link, to relative in-app paths.
- The two existing Claude Artifacts (presentation, comic) are left published as-is (harmless, no cost) but are no longer the canonical/shared links going forward — the PythonAnywhere URLs become canonical.

## Capabilities

### New Capabilities
- `presentation-hosting`: Serves the event presentation and comic viewer as pages of the same Flask app that hosts the registration forms, with images served as static files rather than embedded base64.

### Modified Capabilities
- None — `registration-intake`, `response-storage`, and `response-review` are unaffected; this change only adds new, unrelated pages to the same app.

## Impact

- New routes and templates in the existing `kryak-registration` repo; no changes to `app.py`'s existing form/admin routes or to `database.py`.
- New static assets added to `static/` (screenshots, comic art, logo) — increases repo size, still comfortably within PythonAnywhere's free 512 MB quota.
- No changes to `kryakobank` or its database.
- The two Claude Artifacts remain published (organizer may keep or unpublish them later) but stop being the links shared with the provid/lecturer audience — all outward-facing links switch to `malehakasper.pythonanywhere.com`.
