# Project Plan (Agent-Driven)

## Scope

- Product: France-first holiday calendar website
- Model: PPC monetization
- Data: free/open APIs only for MVP
- Stack: Flask + template-rendered HTML/JS

## Reusable agent roles

- PM: `.github/agentic/agents/product/product.mvp-strategist.agent.md`
- SEO: `.github/agentic/agents/seo/seo.technical-strategist.agent.md`
- UX/UI: `.github/agentic/agents/ux/ux.conversion-designer.agent.md`
- Full-Stack: `.github/agentic/agents/engineering/engineering.fullstack-lead.agent.md`
- Code Quality Challenger: `.github/agentic/agents/engineering/engineering.code-quality-challenger.agent.md`
- Ad Ops: `.github/agentic/agents/ads/ads.monetization-optimizer.agent.md`

## Execution sequence

1. PM defines MVP scope and priorities.
2. SEO + UX define constraints and requirements.
3. Full-Stack implements feature slices.
4. Code Quality Challenger reviews Full-Stack implementation:
   - Challenges over-engineering and identifies simplifications.
   - Collaborates with Full-Stack to refine design and implementation.
   - Verifies code quality, correctness, and maintainability.
5. Ad Ops implements/optimizes monetization safely.
6. Final integration and deployment.

## MVP boundaries

- In: France public holidays, France school holidays (zones), mobile-first calendar UX, basic SEO, AdSense-ready slots.
- Out: multi-country support, user accounts, advanced personalization, premium paid APIs.

## Current implementation status

- France holiday API integration via Nager.Date added.
- School holidays (FR zones) preserved.
- Mobile-first calendar page and JSON-LD event output implemented.
- AdSense-safe slot structure and `ads.txt` setup implemented with placeholder IDs.

