# TODO

## P0 - Public launch without ads

- [x] Implement France public holidays endpoint (Nager.Date).
- [x] Keep and render France school holidays by zone (A/B/C).
- [x] Build mobile-first calendar experience (desktop + mobile rendering).
- [x] Generate JSON-LD Event data from displayed holidays.
- [x] Add AdSense-ready placeholder slots with CLS-safe reserved space.
- [x] Add and serve `ads.txt`.
- [ ] **Full-Stack (do first):** add an `ADS_ENABLED` setting (default false).
  When false, production startup skips the ad/CMP/`ads.txt` checks, and no
  ad, consent-manager or measurement scripts load and no `/api/metrics` calls
  are made. Placeholder values are still rejected when ads are enabled. Cover
  both cases with tests. This is the first step of the ad-free deployment item
  below.
- [ ] **Full-Stack:** resolve the PR #24 (`dev` to `main`) conflicts in
  `app.py` and `templates/index.html` after the `ADS_ENABLED` change, and add
  CI checks so launch changes are validated before merge.
- [ ] **Full-Stack + PM:** disable the saint-name views by default for launch
  behind a `NAME_DAYS_ENABLED` setting (default false); they are not a Step 1
  requirement.
- [ ] Verify available France public and school-holiday dates for zones A/B/C
  for the current and next calendar years against their sources; clearly
  indicate missing or partial coverage. Do not add unchecked dates: 2027 is
  currently missing Toussaint and Noël, so mark it partial in the UI and
  JSON-LD until verified against the official calendar.
- [ ] **SEO:** fix the school-holiday JSON-LD label (Christmas break starting
  2025-12-20 is shown as "Noël 2026"), keep empty or partial-year pages out of
  the sitemap or `noindex`, and add a test comparing rendered dates with
  JSON-LD for every sitemap URL.
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
- [ ] **PM:** review scope and roadmap impact from merged PR #7. <!-- AUTO-PR:7;ROLE:PM -->
- [ ] **SEO:** review metadata/indexability implications from merged PR #7. <!-- AUTO-PR:7;ROLE:SEO -->
- [ ] **UX/UI:** review readability and interaction impact from merged PR #7. <!-- AUTO-PR:7;ROLE:UX/UI -->
- [ ] **Full-Stack:** validate implementation consistency from merged PR #7. <!-- AUTO-PR:7;ROLE:Full-Stack -->
- [ ] **Ad Ops:** review monetization/compliance implications from merged PR #7. <!-- AUTO-PR:7;ROLE:Ad Ops -->
- [ ] **PM:** review scope and roadmap impact from merged PR #9. <!-- AUTO-PR:9;ROLE:PM -->
- [ ] **SEO:** review metadata/indexability implications from merged PR #9. <!-- AUTO-PR:9;ROLE:SEO -->
- [ ] **UX/UI:** review readability and interaction impact from merged PR #9. <!-- AUTO-PR:9;ROLE:UX/UI -->
- [ ] **Full-Stack:** validate implementation consistency from merged PR #9. <!-- AUTO-PR:9;ROLE:Full-Stack -->
- [ ] **Ad Ops:** review monetization/compliance implications from merged PR #9. <!-- AUTO-PR:9;ROLE:Ad Ops -->
- [ ] **PM:** review scope and roadmap impact from merged PR #12. <!-- AUTO-PR:12;ROLE:PM -->
- [ ] **UX/UI:** review readability and interaction impact from merged PR #12. <!-- AUTO-PR:12;ROLE:UX/UI -->
- [ ] **Full-Stack:** validate implementation consistency from merged PR #12. <!-- AUTO-PR:12;ROLE:Full-Stack -->
- [ ] **Ad Ops:** review monetization/compliance implications from merged PR #12. <!-- AUTO-PR:12;ROLE:Ad Ops -->
- [ ] **UX/UI:** review readability and interaction impact from merged PR #14. <!-- AUTO-PR:14;ROLE:UX/UI -->
- [ ] **PM:** review scope and roadmap impact from merged PR #16. <!-- AUTO-PR:16;ROLE:PM -->
- [ ] **SEO:** review metadata/indexability implications from merged PR #16. <!-- AUTO-PR:16;ROLE:SEO -->
- [ ] **UX/UI:** review readability and interaction impact from merged PR #16. <!-- AUTO-PR:16;ROLE:UX/UI -->
- [ ] **UX/UI:** review readability and interaction impact from merged PR #18. <!-- AUTO-PR:18;ROLE:UX/UI -->
- [ ] **Full-Stack:** validate implementation consistency from merged PR #18. <!-- AUTO-PR:18;ROLE:Full-Stack -->
- [ ] **SEO:** review metadata/indexability implications from merged PR #24. <!-- AUTO-PR:24;ROLE:SEO -->
- [ ] **UX/UI:** review readability and interaction impact from merged PR #24. <!-- AUTO-PR:24;ROLE:UX/UI -->
- [ ] **Full-Stack:** validate implementation consistency from merged PR #24. <!-- AUTO-PR:24;ROLE:Full-Stack -->
- [ ] **Ad Ops:** review monetization/compliance implications from merged PR #24. <!-- AUTO-PR:24;ROLE:Ad Ops -->
<!-- AUTO-TODO-UPDATES:END -->