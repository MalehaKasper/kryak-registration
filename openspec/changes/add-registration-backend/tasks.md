## 1. Project scaffold

- [x] 1.1 Create Flask app skeleton (`app.py`, `templates/`, `static/`, `requirements.txt`) in `/Users/admin/Documents/project/kryak-registration`
- [x] 1.2 Add `database.py` with SQLite connection helper and schema creation for `provid_responses` and `lecturer_responses` tables
- [x] 1.3 Initialize git repo, first commit

## 2. Provid registration form

- [x] 2.1 Port existing comic-styled `registration.html` markup/CSS into a Flask template, replacing the JS `mailto:` submit handler with a plain `<form method="POST" action="/provid/submit">`
- [x] 2.2 Implement `GET /provid` route rendering the form
- [x] 2.3 Implement `POST /provid/submit` route: validate name + at least one contact, store row (name, telegram, phone, tasks, idea, about, timestamp) in `provid_responses`, re-render the page with a visible "дякуємо" confirmation
- [x] 2.4 Handle validation failure by re-rendering the form with an inline error message (no data loss for what was typed)

## 3. Lecturer registration form

- [x] 3.1 Port existing comic-styled `registration_lecturer.html` markup/CSS the same way, posting to `/lecturer/submit`
- [x] 3.2 Implement `GET /lecturer` route rendering the form
- [x] 3.3 Implement `POST /lecturer/submit` route: validate name + at least one contact, store row (name, telegram, phone, talks, own_topic, experience, timestamp) in `lecturer_responses`, re-render with confirmation
- [x] 3.4 Handle validation failure the same way as 2.4

## 4. Admin review pages

- [x] 4.1 Add HTTP Basic Auth decorator reading the expected credential from an environment variable
- [x] 4.2 Implement `GET /provid/responses` (protected): table of all `provid_responses` rows, most recent first
- [x] 4.3 Implement `GET /lecturer/responses` (protected): table of all `lecturer_responses` rows, most recent first
- [x] 4.4 Verify unauthenticated requests to both admin routes are rejected with a credential prompt, not partial data

## 5. Local verification

- [x] 5.1 Run the app locally, submit a test provid entry, confirm it appears in `/provid/responses`
- [x] 5.2 Run the app locally, submit a test lecturer entry, confirm it appears in `/lecturer/responses`
- [x] 5.3 Confirm a restart of the local server does not lose previously stored rows
- [x] 5.4 Confirm submitting with no contact method is rejected with a clear message

## 6. PythonAnywhere deployment

- [x] 6.1 ~~Confirm PythonAnywhere's dormancy/deactivation policy~~ — checked official docs/pricing pages, no documented policy found either way; accepted as a residual known-unknown, not blocking
- [x] 6.2 Create the web app in the PythonAnywhere "Web" tab (manual configuration)
- [x] 6.3 Push code to the account (public GitHub repo `MalehaKasper/kryak-registration`, cloned via Bash console)
- [x] 6.4 Install dependencies (`pip install --user -r requirements.txt`)
- [x] 6.5 Point the WSGI config file at `app.py`
- [x] 6.6 Set the admin Basic Auth credential as environment variables inside the WSGI file
- [x] 6.7 Reload the web app; verified `/provid`, `/lecturer` (200) and `/provid/responses` (401 without auth) at `malehakasper.pythonanywhere.com`
- [x] 6.8 Submitted one real test entry per form on the live deployment; organizer confirmed both appear in the admin views

## 7. Wire up the presentation (outside this repo)

- [x] 7.1 Update the "Приєднатись до проводу" button on the presentation Artifact to point at the deployed `/provid` URL
- [x] 7.2 Update the "Зголоситись лектором" button on the presentation Artifact to point at the deployed `/lecturer` URL
- [x] 7.3 Republish the presentation Artifact; verified both live URLs return 200
