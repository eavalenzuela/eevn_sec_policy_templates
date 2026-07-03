# Changelog

All notable changes to the template set. The set is itself a controlled document
library — per its own `governance/document-control.md.template`, changes are recorded.

Format follows [Keep a Changelog](https://keepachangelog.com/); versions are
template-set releases, independent of the per-document Version History tables.

## [Unreleased]

### Added
- `governance/document-register.md.template` (REG-GOV-01) — master document register
  required by POL-GOV-10 Document Control.
- `vendor/vendor-register.md.template` (REG-VEN-01) — central vendor & BAA register
  required by POL-VEN-01; replaces the former bracketed placeholder reference.
- `resilience/bcdr-test-exercise-log.md.template` (REG-RES-01) — BC/DR test & exercise
  log referenced by the BCP, DRP, and Backup Policy.
- `operations/ai-acceptable-use-policy.md.template` (POL-OPS-10) — AI/LLM acceptable
  use with PHI guardrails, approved-tools register, and SSDLC requirements for
  product AI features.
- `tools/check_templates.py` — structural linter (metadata, sections, Document IDs,
  cross-reference resolution, README-index reconciliation); wired into CI
  (`.github/workflows/check.yml`) and `make check`.
- `tools/render.py` + `tools/example.conf` — template instantiation tool
  (placeholder substitution, guidance-comment stripping, cross-reference rewriting,
  remaining-placeholder report); `make render`.
- `Makefile`, `.editorconfig`, this changelog.

### Fixed
- `operations/backup-policy.md.template`: three mangled cross-references to the BCP
  and DRP pointed at a nonexistent mashed path.
- Nested HTML comments in 8 templates (`_TEMPLATE.md.template`, all of `people/`,
  all of `resilience/`, `vendor/third-party-risk-management-policy.md.template`)
  leaked guidance text into rendered previews.
- Bracketed pseudo-references (`[backup-policy]`, `[acceptable-use-policy]`,
  `[media-disposal / data-classification]`) replaced with real relative links.
- README build-order tree indentation (`access/`, `people/`).

### Changed
- README: added Tooling section; coverage index extended with the four new documents.
- BCP/DRP/Backup Policy/Document Control/Third-Party Risk now link their registers.

## [0.1] - 2026-05-22

### Added
- Initial ISMS policy template set (49 documents across 10 domains) with the
  canonical `_TEMPLATE.md.template` skeleton and the HITRUST/HIPAA/SOC 2/ISO 27001
  coverage index in the README.
