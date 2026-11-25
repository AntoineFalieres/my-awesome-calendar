# ROADMAP

## Step 1 - Public launch without ads

**Goal:** ship the smallest usable France calendar without production ads.

- France national public holidays and school zones A/B/C
- Current and next calendar years, subject to available source data
- Mobile-first month view, with existing additional views retained
- Stable data loading, error handling, and basic SEO
- Production deployment with ads and optional measurement disabled

**Done when:**
- Available dates are verified against their sources for each year and zone;
  missing or partial data is clearly indicated rather than presented as complete
- Year/zone selection and month view work on mobile and desktop, including
  loading, empty, and error states
- Key pages are crawlable and semantically structured; JSON-LD matches rendered
  holiday data, and legal/privacy pages are reachable
- An ad-free production configuration starts successfully and does not
  initialize ads or optional measurement

## Step 2 - Consent and monetization readiness

**Goal:** prepare production ads without compromising consent or layout.

- PM and legal review: confirm applicable requirements for the deployment and
  [consent policy](CONSENT_POLICY.md)
- SEO and UX/UI: verify legal-page metadata, links, and accessible consent controls
- Full-Stack and Ad Ops: implement consent state handling and validate ad and
  optional measurement behavior against the consent policy
- Configure production AdSense IDs and `ads.txt`; preserve reserved ad space
  and safe behavior on no-fill, blocking, or loading failure

**Done when:**
- Production ad configuration and `ads.txt` are valid
- Required consent behavior is verified before production ad initialization
  and optional measurement; non-consented behavior follows the policy
- Ads do not break the UI or cause layout shifts when loading fails or is blocked
- Legal/privacy pages, consent controls, and deployment requirements are reviewed

## Step 3 - Measure and expand

**Goal:** use observed traffic and indexing to prioritize improvements.

- Review search demand and indexing before expanding France landing pages or
  considering additional countries
- Optimize ad placements using permitted measurement after production ads launch

## Next

- Full-Stack: add an `ADS_ENABLED` setting (default off) to remove the ad/CMP
  configuration blocker for an ad-free production deployment and verify ads and
  optional measurement remain disabled
- Full-Stack: resolve PR #24 conflicts and add CI before launch merges
- PM + Full-Stack: verify current/next-year data coverage and public launch
  criteria; mark 2027 as partial until verified, and disable saint-name views
  for launch
- SEO: fix school-holiday JSON-LD labels, keep empty or partial pages out of
  the index, and test JSON-LD against rendered data
- UX/UI + Full-Stack + Ad Ops: complete and verify consent and production ad gates
- PM + SEO: evaluate landing-page expansion using observed traffic and indexing

## Auto-managed updates

<!-- AUTO-ROADMAP-UPDATES:START -->
### Next from merged PRs

- 2026-11-25 - PR #24 `Dev` - Roles: SEO, UX/UI, Full-Stack, Ad Ops (https://github.com/AntoineFalieres/my-awesome-calendar/pull/24) <!-- AUTO-PR:24 -->

- 2026-10-31 - PR #18 `feat(calendar): add daily date and saint-name views` - Roles: UX/UI, Full-Stack (https://github.com/AntoineFalieres/my-awesome-calendar/pull/18) <!-- AUTO-PR:18 -->
- 2026-10-31 - PR #16 `chore(agentic): add Anthropic frontend design skill` - Roles: PM, SEO, UX/UI (https://github.com/AntoineFalieres/my-awesome-calendar/pull/16) <!-- AUTO-PR:16 -->
- 2026-10-28 - PR #14 `docs(github): add caveman commit skill` - Roles: UX/UI (https://github.com/AntoineFalieres/my-awesome-calendar/pull/14) <!-- AUTO-PR:14 -->
- 2026-10-26 - PR #12 `feat(legal): add compliance reviewer and consent policy` - Roles: PM, UX/UI, Full-Stack, Ad Ops (https://github.com/AntoineFalieres/my-awesome-calendar/pull/12) <!-- AUTO-PR:12 -->
- 2026-10-26 - PR #9 `feat: add Code Quality Challenger engineer agent` - Roles: PM, SEO, UX/UI, Full-Stack, Ad Ops (https://github.com/AntoineFalieres/my-awesome-calendar/pull/9) <!-- AUTO-PR:9 -->

- 2026-07-07 - PR #7 `feat(agentic): automate roadmap/todo/changelog updates from merged PRs` - Roles: PM, SEO, UX/UI, Full-Stack, Ad Ops (https://github.com/AntoineFalieres/my-awesome-calendar/pull/7) <!-- AUTO-PR:7 -->

- 2026-06-25 - PR #4 `feat(ui): add legal footer links and GDPR script placeholder` - Roles: SEO, UX/UI, Full-Stack, Ad Ops (https://github.com/AntoineFalieres/my-awesome-calendar/pull/4) <!-- AUTO-PR:4 -->
<!-- AUTO-ROADMAP-UPDATES:END -->
