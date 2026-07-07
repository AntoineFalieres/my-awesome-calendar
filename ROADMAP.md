# ROADMAP

## Step 1 - Core launch (France utility)

**Goal:** ship the smallest usable France calendar.

- France-only calendar flow
- Public holidays + school zones
- Stable API and caching behavior
- Baseline mobile-first UI

**Done when:**
- Year/zone selection reliably displays accurate events
- Main calendar experience works on mobile and desktop

## Step 2 - SEO and UX requirements

**Goal:** make pages indexable, readable, and structured.

- SEO URL strategy for France/year/holiday pages
- Metadata and heading conventions
- JSON-LD Event structure
- Mobile-first layout with ad-safe placeholders
- Legal footer links and dedicated legal/privacy pages
- GDPR consent script placeholder wired in `<head>` for future consent manager integration

**Done when:**
- Pages are crawlable and semantically structured
- JSON-LD is present and consistent with rendered holiday data
- Legal and privacy pages are reachable from core pages and aligned with SEO/legal baseline

## Step 3 - Full-stack delivery

**Goal:** implement prioritized PM+SEO+UX requirements.

- France endpoint backed by Nager.Date
- Calendar rendering + school holiday merge
- JSON-LD generation
- CLS-safe placeholders

**Done when:**
- Core routes and APIs are stable
- UX remains readable with resilient loading/error states

## Step 4 - Monetization readiness

**Goal:** integrate ad stack safely.

- Async AdSense loader
- Guarded per-slot initialization
- Layout-stable fallback behavior on no-fill/block
- `ads.txt` served at `/ads.txt`

**Done when:**
- Ad loading failures do not break UI or shift layout
- `ads.txt` is reachable and validly formatted

## Step 5 - Compliance and consent hardening

**Goal:** make monetization legally compliant while preserving UX and performance.

- PM: define consent scope (analytics, ads personalization, required cookies) and acceptance criteria
- SEO: enforce metadata/canonical/indexing policy for legal pages
- UX/UI: design mobile-first cookie consent UX with readable copy and low friction
- Full-Stack: integrate consent manager script and consent state handling
- Ad Ops: enforce Consent Mode and block ad initialization before valid consent signal

**Done when:**
- Consent state is captured before ad/measurement activation
- Legal/privacy pages, footer links, and consent UX are consistent and production-ready
- Revenue tracking remains available in compliant mode

## Next

- PM: approve consent model and production rollout criteria
- Full-Stack + Ad Ops: set production AdSense IDs and consent-gated ad initialization
- SEO + UX/UI: refine legal/privacy page structure, metadata, and footer discoverability
- Ad Ops: iterate ad placement by RPM/CTR data
- PM + SEO: expand SEO landing pages before country expansion

## Auto-managed updates

<!-- AUTO-ROADMAP-UPDATES:START -->
### Next from merged PRs

- 2026-06-25 - PR #4 `feat(ui): add legal footer links and GDPR script placeholder` - Roles: SEO, UX/UI, Full-Stack, Ad Ops (https://github.com/AntoineFalieres/my-awesome-calendar/pull/4) <!-- AUTO-PR:4 -->
<!-- AUTO-ROADMAP-UPDATES:END -->
