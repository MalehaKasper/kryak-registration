## ADDED Requirements

### Requirement: Password-protected access
The system SHALL require a shared admin credential (HTTP Basic Auth) before displaying any stored responses, for both the provid and lecturer response lists.

#### Scenario: Unauthenticated access blocked
- **WHEN** a visitor without the admin credential requests a responses page
- **THEN** the system does not display any response data and prompts for the credential

#### Scenario: Authenticated access allowed
- **WHEN** the organizer supplies the correct admin credential
- **THEN** the system displays the requested responses page

### Requirement: Tabular listing of all responses
The system SHALL display all stored responses for a form in a table, one row per submission, showing every captured field and the stored timestamp.

#### Scenario: All responses visible
- **WHEN** the organizer authenticates and opens the provid responses page
- **THEN** every stored provid submission appears as a row in the table, most recent first

### Requirement: Independent review per form
The provid and lecturer responses SHALL be viewable on separate admin pages, each showing only its own form's submissions.

#### Scenario: Separate admin pages
- **WHEN** the organizer opens the lecturer responses page
- **THEN** only lecturer submissions are shown, not provid submissions
