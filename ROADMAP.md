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

**Done when:**
- Pages are crawlable and semantically structured
- JSON-LD is present and consistent with rendered holiday data

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

## Next

- Validate real AdSense IDs
- Iterate ad placement by RPM/CTR data
- Expand SEO landing pages before country expansion

