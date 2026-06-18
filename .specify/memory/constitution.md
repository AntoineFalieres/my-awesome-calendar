<!--
SYNC IMPACT REPORT
==================
Version change: (none) → 1.0.0  (initial ratification)
Modified principles: N/A — all new
Added sections:
  - Core Principles (4 principles)
  - Quality Gates
  - Development Workflow
  - Governance
Removed sections: N/A
Templates requiring updates:
  - .specify/templates/plan-template.md  ✅ Constitution Check gates aligned
  - .specify/templates/spec-template.md  ✅ No structural changes required
  - .specify/templates/tasks-template.md ✅ Phase categories already aligned
Deferred TODOs: none
-->

# my-awesome-calendar Constitution

## Core Principles

### I. Code Quality (NON-NEGOTIABLE)

All code MUST be clean, consistent, and maintainable:

- Every module, function, and component MUST have a single, well-defined responsibility.
- Code MUST pass linting and static analysis checks (zero warnings tolerated in CI) before merge.
- Cyclomatic complexity per function MUST NOT exceed 10; refactor if exceeded.
- Dead code, commented-out blocks, and TODO stubs MUST NOT be merged; file a tracked issue instead.
- Dependencies MUST be pinned to explicit versions; indirect dependency drift MUST be reviewed on each release cycle.

**Rationale**: A calendar application accumulates feature complexity rapidly (recurrence rules,
timezone handling, locale formatting). Enforcing consistency from the start prevents compounding
technical debt and reduces the cognitive load of onboarding new contributors.

### II. Testing Standards (NON-NEGOTIABLE)

Test-first development is mandatory for all behavioral logic:

- Tests MUST be written and reviewed before implementation begins (TDD Red-Green-Refactor).
- Unit test coverage MUST be ≥ 80% for all business logic modules.
- Integration tests MUST cover every public API endpoint and every cross-module interaction.
- End-to-end tests MUST cover all P1 user stories defined in the feature spec.
- Flaky tests MUST be quarantined within 24 hours and fixed or deleted within one sprint.
- Test names MUST follow the pattern `test_<unit>_<scenario>_<expected_outcome>`.

**Rationale**: Calendar logic (recurrence, DST transitions, conflict detection) is high-risk and
complex. A strong test baseline is the only reliable safety net for refactors and platform updates.

### III. User Experience Consistency

All UI surfaces MUST follow a unified design language and interaction model:

- Visual tokens (colors, typography, spacing, iconography) MUST be sourced from a single shared
  design-token file; hardcoded values are PROHIBITED.
- Interactive elements (buttons, date pickers, event cards) MUST respond within 100 ms to user
  input at the interaction layer (optimistic UI is acceptable).
- Accessibility MUST meet WCAG 2.1 AA as a minimum; ARIA labels are REQUIRED on all
  interactive calendar controls.
- Error and empty states MUST display actionable copy — generic "Something went wrong" messages
  are PROHIBITED.
- Navigation patterns (keyboard shortcuts, swipe gestures, focus order) MUST be consistent across
  all calendar views (day, week, month, agenda).

**Rationale**: Inconsistent UI erodes user trust and increases support burden. A calendar is a
daily-driver tool; interaction patterns must feel predictable and effortless across all contexts.

### IV. Performance Requirements

The application MUST meet defined performance budgets at all times:

- Initial load (Time-to-Interactive) MUST be ≤ 3 s on a mid-range device over a 4G connection.
- Calendar view transitions (day ↔ week ↔ month) MUST complete in ≤ 200 ms.
- Event query responses (fetch events for a date range) MUST return within 300 ms at p95 for
  datasets up to 10,000 events.
- Bundle size (JS + CSS, gzipped) MUST NOT exceed 250 KB for the critical path.
- Performance budgets MUST be enforced in CI via automated Lighthouse / benchmark checks;
  regressions MUST block merge.

**Rationale**: A sluggish calendar feels broken. Users open it dozens of times per day; every
millisecond of latency compounds into lost trust. Budgets must be concrete and machine-enforced
to prevent gradual degradation.

## Quality Gates

All features MUST pass the following gates before being considered complete:

- **Lint gate**: Zero linting errors or warnings in changed files.
- **Test gate**: All unit, integration, and E2E tests pass; coverage ≥ 80% for new modules.
- **Performance gate**: Automated benchmark/Lighthouse scores do not regress below defined budgets.
- **Accessibility gate**: Automated a11y scan (e.g., axe-core) reports zero critical violations.
- **UX consistency gate**: Design-token audit confirms no hardcoded style values introduced.
- **Security gate**: Dependency audit (e.g., `npm audit` / `pip audit`) reports zero high-severity
  vulnerabilities in changed or added dependencies.

Any gate failure MUST block merge. Exceptions require written justification and a linked issue
with a remediation deadline.

## Development Workflow

- Features MUST originate from a spec (`.specify/specs/`) before implementation begins.
- Branches MUST follow the naming convention `###-short-description` tied to an issue number.
- Pull requests MUST reference the relevant spec and all linked quality gate results.
- Code reviews MUST verify constitution compliance explicitly — reviewers MUST check the
  Constitution Check section of the implementation plan before approving.
- Breaking changes to public APIs or shared data models MUST be flagged in the PR description
  and accompanied by a migration guide or compatibility shim.
- Releases follow semantic versioning (MAJOR.MINOR.PATCH); patch releases MUST NOT introduce
  new behavior.

## Governance

This constitution supersedes all other development practices and informal conventions.
Amendments MUST follow this procedure:

1. Open a GitHub issue describing the proposed change and its motivation.
2. Update `.specify/memory/constitution.md`, increment the version per semver rules, and update
   `LAST_AMENDED_DATE`.
3. Propagate any consequential changes to templates under `.specify/templates/`.
4. Obtain approval from at least one other contributor before merging.
5. Announce the amendment in the project changelog.

All pull requests and code reviews MUST verify compliance with the current constitution version.
Complexity deviations from stated principles MUST be justified in writing within the PR.

**Version**: 1.0.0 | **Ratified**: 2026-04-06 | **Last Amended**: 2026-04-06
