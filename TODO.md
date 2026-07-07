# TODO

## P0 - Required for MVP launch

- [x] Implement France public holidays endpoint (Nager.Date).
- [x] Keep and render France school holidays by zone (A/B/C).
- [x] Build mobile-first calendar experience (desktop + mobile rendering).
- [x] Generate JSON-LD Event data from displayed holidays.
- [x] Add AdSense-ready placeholder slots with CLS-safe reserved space.
- [x] Add and serve `ads.txt`.

## P1 - Immediately after launch

- [x] Replace hardcoded AdSense placeholders with environment-driven publisher/slot IDs.
- [x] Add route/template-level revenue tracking (CTR/RPM by page type).
- [x] Expand France SEO landing pages (`/france/{year}/...`) with internal links.
- [x] Improve legal/privacy template metadata to match SEO checks.
- [x] Add legal footer links and dedicated legal routes/pages (`/mentions-legales`, `/privacy-policy`).
- [x] Add GDPR consent script placeholder in base homepage head.
- [ ] Set production AdSense values in deployment environment variables.

## P2 - Deferred until traffic baseline

- [ ] Add additional countries.
- [ ] Add moon phases only if PM confirms acquisition/revenue impact.
- [ ] Evaluate premium ad networks after eligibility thresholds.
- [ ] Evaluate paid data providers only after MVP revenue validation.

## P1.5 - Compliance hardening (role-owned)

- [ ] **PM:** lock final consent policy (required vs optional cookies, consent granularity, auditability).
- [ ] **SEO:** define index/canonical/meta policy for legal pages and verify internal linking weight.
- [ ] **UX/UI:** design and copy a mobile-first cookie consent banner/modal with clear accept/reject actions.
- [ ] **Full-Stack:** integrate real consent manager script and persist consent state for templates/scripts.
- [ ] **Ad Ops:** enforce consent-gated ad loading + Consent Mode signal wiring before ad initialization.
- [ ] **Full-Stack + Ad Ops:** ensure revenue tracking works in consented and non-consented states.

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
- [ ] **PM:** review scope and roadmap impact from merged PR #7. <!-- AUTO-PR:7;ROLE:PM -->
- [ ] **SEO:** review metadata/indexability implications from merged PR #7. <!-- AUTO-PR:7;ROLE:SEO -->
- [ ] **UX/UI:** review readability and interaction impact from merged PR #7. <!-- AUTO-PR:7;ROLE:UX/UI -->
- [ ] **Full-Stack:** validate implementation consistency from merged PR #7. <!-- AUTO-PR:7;ROLE:Full-Stack -->
- [ ] **Ad Ops:** review monetization/compliance implications from merged PR #7. <!-- AUTO-PR:7;ROLE:Ad Ops -->
<!-- AUTO-TODO-UPDATES:END -->