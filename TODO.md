# TODO

## P0 - Public launch without ads

- [x] Implement France public holidays endpoint (Nager.Date).
- [x] Keep and render France school holidays by zone (A/B/C).
- [x] Build mobile-first calendar experience (desktop + mobile rendering).
- [x] Generate JSON-LD Event data from displayed holidays.
- [x] Add AdSense-ready placeholder slots with CLS-safe reserved space.
- [x] Add and serve `ads.txt`.
- [ ] Verify available France public and school-holiday dates for zones A/B/C
  for the current and next calendar years against their sources; clearly
  indicate missing or partial coverage.
- [ ] Verify month view, year/zone selection, and loading, empty, and error
  states on mobile and desktop. Existing week, semester, and year views remain
  available but are not launch blockers.
- [ ] Verify key routes, basic SEO, legal/privacy links, and consistency between
  rendered holiday data and JSON-LD.
- [ ] Enable and verify an ad-free production deployment: current production
  startup requires ad/CMP settings and a non-placeholder `ads.txt`. Ensure ads
  and optional measurement do not initialize for this launch.

## P1 - Implemented follow-up work

- [x] Replace hardcoded AdSense placeholders with environment-driven publisher/slot IDs.
- [x] Add route/template-level revenue tracking (CTR/RPM by page type).
- [x] Expand France SEO landing pages (`/france/{year}/...`) with internal links.
- [x] Improve legal/privacy template metadata to match SEO checks.
- [x] Add legal footer links and dedicated legal routes/pages (`/mentions-legales`, `/privacy-policy`).
- [x] Add GDPR consent script placeholder in base homepage head.
- [x] Redesign the calendar in a Google Calendar style (week, month, semester and year grid views).

## P1.5 - Required before production ads (role-owned)

- [x] **PM:** document the consent policy in [CONSENT_POLICY.md](CONSENT_POLICY.md) (required vs optional processing, consent granularity, and auditability).
- [ ] **PM + legal review:** confirm applicable consent and deployment
  requirements before production ad activation.
- [ ] **SEO:** define index/canonical/meta policy for legal pages and verify internal linking weight.
- [ ] **UX/UI:** design and copy a mobile-first cookie consent banner/modal with clear accept/reject actions.
- [ ] **Full-Stack:** integrate real consent manager script and persist consent state for templates/scripts.
- [ ] **Ad Ops:** configure Consent Mode before ad initialization; block personalized ads without opt-in while allowing contextual ads as defined in [CONSENT_POLICY.md](CONSENT_POLICY.md).
- [ ] **Full-Stack + Ad Ops:** set and validate production AdSense values and
  `ads.txt`, and verify layout stability and failure behavior.
- [ ] **Full-Stack + Ad Ops:** verify ad and measurement behavior for both
  consented and non-consented states against the consent policy; optional
  analytics must remain disabled without its separate opt-in.

## P2 - Deferred until traffic baseline

- [ ] Add additional countries.
- [ ] Add moon phases only if PM confirms acquisition/revenue impact.
- [ ] Evaluate premium ad networks after eligibility thresholds.
- [ ] Evaluate paid data providers only after MVP revenue validation.

## Agent handoff workflow

1. PM defines scope and acceptance criteria.
2. SEO + UX provide requirements and constraints.
3. Full-Stack implements task slices.
4. Ad Ops validates monetization safety and performance impact.

## Auto-managed updates

<!-- AUTO-TODO-UPDATES:START -->
### Role-owned follow-ups from merged PRs
- [ ] **SEO:** review metadata/indexability implications from merged PR #4. <!-- AUTO-PR:4;ROLE:SEO -->
- [ ] **UX/UI:** review readability and interaction impact from merged PR #4. <!-- AUTO-PR:4;ROLE:UX/UI -->
- [ ] **Full-Stack:** validate implementation consistency from merged PR #4. <!-- AUTO-PR:4;ROLE:Full-Stack -->
- [ ] **Ad Ops:** review monetization/compliance implications from merged PR #4. <!-- AUTO-PR:4;ROLE:Ad Ops -->
<!-- AUTO-TODO-UPDATES:END -->