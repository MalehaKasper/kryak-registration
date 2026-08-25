## Context

The presentation and comic viewer already exist as finished, working HTML/CSS/JS built for Claude Artifacts (one self-contained file each, all images inlined as base64 because Artifacts require a single file). The registration app (`kryak-registration`) already runs on PythonAnywhere with a working Flask + Jinja template setup, a `static/` folder, and an established visual language (the same `:root` CSS variables, fonts, and comic-panel styling are already duplicated across `base.html`, `provid_form.html`, `lecturer_form.html`).

## Goals / Non-Goals

**Goals:**
- Presentation and comic viewer reachable at `malehakasper.pythonanywhere.com` (e.g. `/` and `/comic`), fully replacing the claude.ai Artifact links for outward-facing sharing.
- All images served as real static files, not inline base64 — smaller page weight, browser-cacheable.
- Visual output is unchanged from the current Artifact versions (same layout, same content, same styling) — this is a hosting migration, not a redesign.
- Internal navigation (presentation ↔ comic ↔ provid/lecturer forms) uses relative in-app links, no more cross-domain jumps.

**Non-Goals:**
- No redesign of the presentation or comic content — copy is carried over as-is.
- No change to the registration forms, database, or admin views.
- Not unpublishing the existing Claude Artifacts in this change — they can simply go unused; removing them is a separate, later decision if wanted.
- Not building a CMS or making the presentation content editable through an admin UI — it stays a static Jinja template like the forms.

## Decisions

- **Serve as two new Flask routes (`GET /` for the presentation, `GET /comic` for the comic viewer), rendered from Jinja templates**, consistent with how the forms are already built. Alternative considered: serve as plain static HTML files — rejected, because Jinja templates keep the current pattern (shared head/style conventions) consistent with the rest of the app and cost nothing extra.
- **Extract every embedded image to `static/img/...` and reference via `url_for('static', ...)`.** This is the core motivation (page weight, caching) and is mechanical: decode each existing base64 payload back to a file once, commit the files, replace the `src`/`href` with a `static` URL.
- **Root path `/` becomes the presentation.** It's the natural entry point for anyone sharing the single domain; the forms keep their existing `/provid` and `/lecturer` paths unchanged.
- **CTA buttons and cross-links become relative paths** (`/provid`, `/lecturer`, `/comic`, `/`) instead of full claude.ai URLs — removes the cross-domain hop entirely.
- **Leave the two Claude Artifacts published, untouched.** No reason to spend effort unpublishing them now; they simply stop being the shared links. Revisit later if the organizer wants them gone.

## Risks / Trade-offs

- **[Risk] Visual regressions while porting markup/CSS by hand from the Artifact source to Jinja templates** → Mitigation: port content verbatim first, diff visually (screenshot before/after) before treating the task as done, the same approach used for the registration forms port.
- **[Risk] Broken relative links if paths are typo'd** → Mitigation: click through every link (presentation → comic → back, presentation → provid/lecturer) after deployment as an explicit verification task.
- **[Risk] Repo/static folder grows notably (screenshots + comic art, several MB)** → Mitigation: still far under the 512 MB free-tier quota; no action needed, just noted.
- **[Risk] Two now-orphaned Claude Artifacts could confuse someone who still has the old link bookmarked** → Mitigation: acceptable for v1; could add a small "moved to <new URL>" notice on the old Artifacts later if this turns out to matter in practice.

## Migration Plan

1. Extract all embedded images from the two Artifact source files into `static/img/` (comic panels + cover, app screenshots, Крякобанк logo already present).
2. Build `templates/presentation.html` and `templates/comic.html` from the existing Artifact markup, swapping inline `data:` URIs for `static` file references and claude.ai links for relative paths.
3. Add the two routes to `app.py`.
4. Verify locally (screenshot comparison against the current Artifact rendering).
5. `git push`, `git pull` on PythonAnywhere, Reload.
6. Click through the live site end-to-end (presentation → comic → back, both CTA buttons → forms).

Rollback: the routes are additive; if something looks wrong, the previous Artifact URLs still work unchanged and can be shared again while the new pages are fixed.

## Open Questions

- Should the two Claude Artifacts eventually be unpublished/redirected once the new pages are confirmed working, or kept indefinitely as a passive backup? Not needed for this change; revisit later.
