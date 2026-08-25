## 1. Extract assets to static files

- [x] 1.1 Decode every embedded base64 image from the presentation Artifact source into `static/img/presentation/` (screenshots, cover art, comic sample panels); Крякобанк logo reused from the already-existing `static/duck_coin_logo.png`
- [x] 1.2 Decode every embedded base64 image from the comic viewer Artifact source into `static/img/comic/` (cover + 5 pages)
- [x] 1.3 Spot-check a handful of extracted files open correctly and match the originals

## 2. Presentation page

- [x] 2.1 Create `templates/presentation.html` by porting the Artifact's markup/CSS verbatim (dropped only the scroll-reveal fade-in JS/`.reveal` classes as a decorative, non-content simplification)
- [x] 2.2 Replace every inline `data:` image `src` with `{{ url_for('static', filename='img/presentation/...') }}`
- [x] 2.3 Replace the two CTA button hrefs with `{{ url_for('provid_form') }}` and `{{ url_for('lecturer_form') }}`
- [x] 2.4 Replace the "переглянути комікс" links with `{{ url_for('comic_viewer') }}`
- [x] 2.5 Add `GET /` route in `app.py` rendering `presentation.html`

## 3. Comic viewer page

- [x] 3.1 Create `templates/comic.html` by porting the Artifact's markup/CSS verbatim
- [x] 3.2 Replace every inline `data:` image `src` with `{{ url_for('static', filename='img/comic/...') }}`
- [x] 3.3 Replace the "back to presentation" links with `{{ url_for('presentation') }}`
- [x] 3.4 Add `GET /comic` route in `app.py` rendering `comic.html`

## 4. Local verification

- [x] 4.1 Run the app locally, load `/` and `/comic`, screenshot both
- [x] 4.2 Compare screenshots against the current live Artifact versions — confirmed no visual regressions
- [x] 4.3 Click every in-app link (presentation → comic → back, both CTA buttons → forms) and confirmed none leave the app's own domain (grepped for `claude.ai` — zero matches)

## 5. Deploy

- [ ] 5.1 Commit and push the new templates, routes, and static assets
- [ ] 5.2 Pull the changes in a PythonAnywhere Bash console
- [ ] 5.3 Reload the web app
- [ ] 5.4 Verify `https://malehakasper.pythonanywhere.com/` and `/comic` on the live deployment
- [ ] 5.5 Click through the live site end-to-end (same checks as 4.3, against the live URL)

## 6. Wrap-up

- [ ] 6.1 Confirm with the organizer that the new pages are the ones to share going forward
- [ ] 6.2 Note the still-open question from design.md (whether to eventually unpublish the old Claude Artifacts) somewhere it won't get lost
