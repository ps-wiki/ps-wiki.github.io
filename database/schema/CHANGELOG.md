# PS-Wiki Schema Changelog

All notable changes to the **term schema** are documented here.  
This file is published at <https://ps-wiki.github.io/schema/CHANGELOG.md>.

The schema follows **Semantic Versioning**:

- **MAJOR** – incompatible (breaking) changes to the JSON structure or required fields
- **MINOR** – backward-compatible additions or relaxed rules
- **PATCH** – corrections or clarifications that don’t change validation behavior

---

## [1.0.0] – 2025-11-02

### Added

- Initial release of `term.schema.json` (v1).
- Fields defined:
  - Top-level: `id`, `title`, `description`, `language`, `tags`, `related`, `aliases`,
    `version`, `breaking`, `status`, `license`, `dates`, `authors`, `content`.
  - Nested: `content.sections[].order`, `id`, `title`, `type`, `source_keys`, `page`, `body_md`, `figures`.
- Draft 2020-12 JSON Schema.
- Supports optional `license` (defaults to repository license CC-BY-NC-4.0).
- Allows `language` tags such as `"en"`, `"en-GB"`, `"en-US"`.
- Permits `null` values for optional fields (`page`, figure properties, etc.).
- Introduced schema metadata:
  - `"x-schema-version": "1.0.0"`
  - `"x-changelog-url": "https://ps-wiki.github.io/schema/CHANGELOG.md"`

### Notes

- This version corresponds to **API v1** of the planned REST interface.
- Term JSON examples validated: `stability`, `30-minute-reserve-service`.
- No deprecated fields at this stage.

---

## [Unreleased]

### Planned

- Add schema for reference list entries (`reference.schema.json`).
- Add schema for glossary categories / index pages.
