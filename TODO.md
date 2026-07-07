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
- [ ] Set production AdSense values in deployment environment variables.

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