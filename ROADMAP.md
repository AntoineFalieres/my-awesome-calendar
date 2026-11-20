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

- Full-Stack: remove the ad/CMP configuration blocker for an ad-free production
  deployment and verify ads and optional measurement remain disabled
- PM + Full-Stack: verify current/next-year data coverage and public launch criteria
- UX/UI + Full-Stack + Ad Ops: complete and verify consent and production ad gates
- PM + SEO: evaluate landing-page expansion using observed traffic and indexing

## Auto-managed updates

<!-- AUTO-ROADMAP-UPDATES:START -->
### Next from merged PRs

- 2026-06-25 - PR #4 `feat(ui): add legal footer links and GDPR script placeholder` - Roles: SEO, UX/UI, Full-Stack, Ad Ops (https://github.com/AntoineFalieres/my-awesome-calendar/pull/4) <!-- AUTO-PR:4 -->
<!-- AUTO-ROADMAP-UPDATES:END -->
