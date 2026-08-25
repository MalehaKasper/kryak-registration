## ADDED Requirements

### Requirement: Presentation served from the app's own domain
The system SHALL serve the event presentation at the app's root path, with content and styling equivalent to the existing Claude Artifact version.

#### Scenario: Presentation loads at root
- **WHEN** a visitor requests `/` on the app's domain
- **THEN** the presentation page renders with the same sections, copy, and comic-book styling as the previous Artifact version

### Requirement: Comic viewer served from the app's own domain
The system SHALL serve the comic viewer at a dedicated path, with content and styling equivalent to the existing Claude Artifact version.

#### Scenario: Comic viewer loads
- **WHEN** a visitor requests `/comic` on the app's domain
- **THEN** the comic viewer renders the cover and all five pages in reading order, styled as in the previous Artifact version

### Requirement: Images served as static files
The system SHALL serve every image used by the presentation and comic viewer as a static file, not as an inline base64 data URI.

#### Scenario: Image requested independently
- **WHEN** the browser loads the presentation page
- **THEN** each image is fetched as a separate static-file request, not embedded in the page's HTML payload

### Requirement: In-app navigation without cross-domain links
The system SHALL link between the presentation, the comic viewer, and the two registration forms using relative in-app paths, without directing the visitor to any claude.ai Artifact URL.

#### Scenario: CTA buttons stay in-app
- **WHEN** a visitor on the presentation page clicks "Приєднатись до проводу" or "Зголоситись лектором"
- **THEN** they land on `/provid` or `/lecturer` on the same domain, never on a claude.ai link

#### Scenario: Comic link stays in-app
- **WHEN** a visitor clicks through to view the comic from the presentation, and then clicks back
- **THEN** both navigations stay on the app's own domain
