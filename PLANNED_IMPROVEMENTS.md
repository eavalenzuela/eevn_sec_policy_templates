# Planned Improvements & Features

Plan for this pass over `eevn_sec_policy_templates`. Improvements target existing
content/quality/robustness; features add new capability. Each item has a one-line
rationale.

## Improvements (10)

1. **Fix mangled cross-references in `operations/backup-policy.md.template`** — three
   occurrences of a mashed, nonexistent path (`resilience/business-continuity-and-../resilience/disaster-recovery-plan.md.template`)
   break navigation to the BCP and DRP.
2. **Fix nested HTML comments in 8 templates** — the opening guidance block contains a
   literal `<!-- TEMPLATE: ... -->`, whose inner `-->` closes the outer comment early and
   leaks instructions into the rendered document (`_TEMPLATE.md.template`, all of
   `people/`, all of `resilience/`, `vendor/third-party-risk-management-policy.md.template`).
3. **Convert bracketed pseudo-references to real relative links** — `` `[backup-policy]` ``
   (BCP, DRP x2, IRP), `` `[acceptable-use-policy]` `` (HR security), and
   `` `[media-disposal / data-classification]` `` (physical security) point at documents
   that exist in this repo and should be navigable.
4. **Add `tools/check_templates.py` structural linter** — validates every template's
   metadata header (9 required fields), Status line, required sections, H1 title, and
   well-formed unique Document IDs; a docs repo needs a correctness check.
5. **Cross-reference resolution in the linter** — resolve every backticked
   `*.md.template` path relative to its file; this class of check would have caught
   improvement #1 before it shipped.
6. **README coverage-index reconciliation in the linter** — verify every template on
   disk appears exactly once in the README index with a matching Document ID and
   directory, so the "navigable control library" claim stays true as the set grows.
7. **Add a `Makefile`** — canonical entry points (`make check`, `make render`) so the
   tooling is discoverable and CI/local runs stay identical.
8. **Add GitHub Actions workflow `.github/workflows/check.yml`** — run the linter on
   push/PR (stdlib Python only, no dependencies) so structural regressions are caught
   automatically.
9. **README: add a Tooling section and fix the build-order tree** — document the
   checker/renderer workflow, and fix the inconsistent indentation on the `access/` and
   `people/` lines in the verbatim directory tree.
10. **Repo hygiene: `CHANGELOG.md` + `.editorconfig`** — a policy-template set is itself
    a controlled document set (its own Document Control policy says so); track releases
    and normalize editor behavior.

## New Features (5)

1. **`tools/render.py` — template instantiation tool** — copies the set into a target
   directory, strips `.template` suffixes, substitutes `[PLACEHOLDER]` values from a
   simple config file, optionally strips `<!-- TEMPLATE: ... -->` guidance comments,
   rewrites cross-references to the rendered names, and reports remaining placeholders
   per file as a tailoring worklist.
2. **`governance/document-register.md.template` (REG-GOV-01)** — the master document
   register that POL-GOV-10 Document Control §10 mandates but which had no template;
   the schema is the control evidence.
3. **`vendor/vendor-register.md.template` (REG-VEN-01)** — the central vendor/BAA
   register POL-VEN-01 §3 requires; replaces the `[vendor & BAA tracker register]`
   placeholder with a real, linkable schema.
4. **`resilience/bcdr-test-exercise-log.md.template` (REG-RES-01)** — the BC/DR test &
   exercise log that BCP §9, DRP §8, and the Backup Policy's restore tests all say must
   exist; a documented test log is primary HITRUST 12.e evidence.
5. **`operations/ai-acceptable-use-policy.md.template` (POL-OPS-10)** — AI/LLM
   acceptable-use policy with PHI guardrails (approved-tools register, data rules by
   classification, BAA-before-PHI, human review); fills the most current gap for a
   healthcare SaaS ISMS and maps to the emerging HITRUST AI assessment.
