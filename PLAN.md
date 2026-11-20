# Project Plan (Agent-Driven)

## Scope

- Product: France-only holiday calendar website for the initial launch
- Model: launch without ads; enable PPC monetization after its separate readiness gate
- Data: free/open APIs only for MVP
- Stack: Flask + template-rendered HTML/JS

## Reusable agent roles

- PM: `.github/agents/product/product.mvp-strategist.agent.md`
- SEO: `.github/agents/seo/seo.technical-strategist.agent.md`
- UX/UI: `.github/agents/ux/ux.conversion-designer.agent.md`
- Full-Stack: `.github/agents/engineering/engineering.fullstack-lead.agent.md`
- Code Quality Challenger: `.github/agents/engineering/engineering.code-quality-challenger.agent.md`
- Ad Ops: `.github/agents/ads/ads.monetization-optimizer.agent.md`

## Execution sequence

1. PM defines MVP scope and priorities.
2. SEO + UX define constraints and requirements.
3. Full-Stack implements feature slices and validates holiday data coverage.
4. Code Quality Challenger reviews Full-Stack implementation:
   - Challenges over-engineering and identifies simplifications.
   - Collaborates with Full-Stack to refine design and implementation.
   - Verifies code quality, correctness, and maintainability.
5. Final integration verifies the public launch gate and deploys without ads.
6. UX/UI, Full-Stack, and Ad Ops complete consent and production checks before
   enabling ads; Ad Ops then optimizes monetization.

## MVP boundaries

- In: France national public holidays and school holidays for zones A/B/C,
  mobile-first month view, basic SEO, and clear loading, empty, and error states.
- Years: current and next calendar years, subject to source data availability.
  Identify unavailable or partial data rather than presenting it as complete.
- The existing week, semester, and year views remain available but are not
  launch blockers. Further views are deferred until their value is demonstrated.
- Out: additional countries, moon phases, user accounts, advanced
  personalization, and premium paid APIs.

## Launch gates

### Public launch without ads

- Verify available public and school-holiday dates for each zone against their
  sources for the current and next years; clearly indicate missing or partial
  coverage.
- Verify month-view usability on mobile and desktop, year/zone selection,
  loading and error behavior, key routes, basic SEO, and consistency between
  displayed holidays and JSON-LD.
- Make an ad-free production deployment possible and verify that ads and
  optional measurement do not initialize. Current production configuration
  requires ad and consent settings, so this remains a deployment blocker.

### Later ad enablement

- Set and validate production AdSense configuration and `ads.txt`; verify
  layout stability and failure behavior.
- Implement and verify consent and measurement behavior against
  [CONSENT_POLICY.md](CONSENT_POLICY.md), including the non-consented state,
  before enabling production ads or optional measurement.
- Confirm legal and privacy requirements for the actual deployment before
  activation; readiness is not a legal-compliance certification.

## Current implementation status

- France holiday API integration via Nager.Date added.
- School holidays (FR zones) preserved.
- Mobile-first calendar page and JSON-LD event output implemented.
- AdSense-safe slot structure, environment-driven IDs, and `ads.txt` are
  implemented; production values and consent-dependent activation remain
  outstanding. These do not establish production monetization readiness.
