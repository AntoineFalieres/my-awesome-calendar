# Consent policy

This document records the product and technical consent decisions for the
calendar service. It is an implementation brief, not legal advice or final
privacy-policy copy.

**Policy version:** 1

Increment the policy version when a change affects consent categories, defaults,
or how optional processing works. A record from an earlier version grants no
optional consent.

## Defaults and categories

Required processing is always enabled and limited to what is needed to provide,
secure, and operate the service, including remembering the visitor's consent
choices. Optional processing is off until a visitor actively opts in.

| Category | Default | Policy |
| --- | --- | --- |
| Required service operations | On | May run without consent. Do not use this category to justify optional analytics or advertising personalization. |
| Analytics | Off | Collect page or ad-performance metrics only after a separate analytics opt-in. If declined, do not send optional events to the site's metrics endpoint. |
| Personalized advertising | Off | Do not enable personalized ads or related optional advertising storage unless the visitor opts in to this category. |

Visitors must be able to accept or reject optional categories, including a
single reject-all action. Optional categories must not be preselected.

## Contextual advertising

Contextual, non-personalized ads may be shown without personalized-ad consent.
The ad integration must use a contextual/non-personalized configuration and
must not enable personalized advertising or its optional storage in that state.
If the integration cannot honor this distinction, ads must remain disabled until
it can.

Consent to analytics is independent of ad delivery. Ad initialization or page
activity must not be sent to the site's optional metrics endpoint unless
analytics is enabled.

## Consent state and controls

Keep only the visitor's category choices, the policy version, and the time of
the last choice in browser storage. Do not send this consent record to the
server or create a server-side consent log. The visitor's choices remain in
that browser until changed, cleared, or invalidated by a policy-version change.

Provide a persistent, accessible way to reopen consent settings from the site's
pages. A visitor can change or withdraw optional consent there; apply the new
choice immediately to subsequent analytics collection and ad requests. A
missing, unreadable, or outdated consent record must be treated as no optional
consent, and the visitor should be offered the current settings.

## Acceptance criteria for follow-on work

- The initial state enables required operations only; analytics and personalized
  advertising are independently opt-in.
- Visitors can reject all optional categories without accepting another
  category, and neither optional category is preselected.
- Contextual ads can load when personalized advertising is declined, without
  enabling personalized advertising or its optional storage.
- Personalized ads and optional analytics remain disabled until their
  respective choices are granted.
- Changing or withdrawing a choice takes effect immediately, and settings can
  be reopened on every relevant page.
- The browser record contains only category choices, policy version, and choice
  timestamp; no server-side consent record is created.
- Missing, invalid, or outdated state never grants optional consent.
