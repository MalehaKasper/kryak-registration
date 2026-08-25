## ADDED Requirements

### Requirement: Public submission without authentication
The system SHALL allow any visitor to submit either the провід or лектор form without requiring a user account, login, or any prior access grant.

#### Scenario: Anonymous visitor submits provid form
- **WHEN** a visitor who is not logged into any account fills the required fields and submits the провід form
- **THEN** the system accepts and stores the submission without prompting for authentication

### Requirement: Required contact validation
The system SHALL require a name and at least one of Telegram or phone before accepting a submission, on both forms.

#### Scenario: Missing both contacts
- **WHEN** a visitor submits a form with the name filled in but both Telegram and phone left blank
- **THEN** the system rejects the submission and shows a message asking for at least one contact method

#### Scenario: Missing name
- **WHEN** a visitor submits a form with no name entered
- **THEN** the system rejects the submission and shows a message asking for a name

### Requirement: Task or talk selection captured as multiple values
The провід form SHALL allow selecting zero or more checkboxes from its fixed task list; the лектор form SHALL allow selecting zero or more checkboxes from its fixed talk list. Selecting none SHALL still allow submission.

#### Scenario: Multiple tasks selected
- **WHEN** a visitor checks three task checkboxes on the provid form and submits
- **THEN** all three selected values are stored together with that submission

#### Scenario: No task selected
- **WHEN** a visitor submits the provid form with no task checkbox selected
- **THEN** the submission is still accepted, with an empty task selection recorded

### Requirement: Visual identity preserved
The провід and лектор form pages SHALL keep the existing comic-book visual design (fonts, colors, panel styling, layout) already built for the Artifact-based versions of these forms.

#### Scenario: Page renders with existing styling
- **WHEN** the provid form page is loaded in a browser
- **THEN** it displays with the same comic-panel styling, color palette, and typography as the previous Artifact version

### Requirement: Confirmation after submission
The system SHALL show the visitor a clear on-page confirmation that their submission was received, without requiring any further action from them (no separate email step, no redirect to another service).

#### Scenario: Successful submission feedback
- **WHEN** a visitor successfully submits a form
- **THEN** the page displays a visible thank-you message confirming the application was received
