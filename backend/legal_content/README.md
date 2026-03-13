# Legal HTML Content

This folder is used to load legal text content at runtime.

The real HTML files are intentionally excluded from git via [.gitignore](../../.gitignore) and should be provided per deployment environment.

Expected files (language-specific):

- imprint.en.html
- imprint.de.html
- data-protection.en.html
- data-protection.de.html
- terms-of-service.en.html
- terms-of-service.de.html

Backend endpoint:

- GET /api/v1/config/legal/imprint?lang=en|de
- GET /api/v1/config/legal/data-protection?lang=en|de
- GET /api/v1/config/legal/terms-of-service?lang=en|de

Configuration via environment variables:

- LEGAL_CONTENT_DIRECTORY
- LEGAL_IMPRINT_FILENAME_TEMPLATE
- LEGAL_DATA_PROTECTION_FILENAME_TEMPLATE
- LEGAL_TERMS_OF_SERVICE_FILENAME_TEMPLATE

Placeholder files in this directory document the expected file names.
