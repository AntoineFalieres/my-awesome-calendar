(function () {
    "use strict";

    const body = document.body;
    const config = {
        pageType: body.dataset.pageType || "unknown",
        adsEnabled: body.dataset.adsEnabled === "1",
        adsClient: body.dataset.adsClient || "",
        cmpEnabled: body.dataset.cmpEnabled === "1"
    };

    // TCF purpose IDs that must all be consented to for each optional category.
    const REQUIRED_PURPOSES = {
        ads: [1],
        personalizedAds: [1, 3, 4],
        analytics: [7, 8]
    };
    const TCF_POLL_INTERVAL_MS = 250;
    const TCF_POLL_LIMIT = 40;

    // Nothing optional runs until the CMP reports an explicit choice.
    const consent = { ads: false, personalizedAds: false, analytics: false };
    let pageViewSent = false;
    let adScriptRequested = false;

    window.dataLayer = window.dataLayer || [];
    function gtag() {
        window.dataLayer.push(arguments);
    }
    gtag("consent", "default", {
        ad_storage: "denied",
        ad_user_data: "denied",
        ad_personalization: "denied",
        analytics_storage: "denied"
    });

    function hasPurposes(tcData, purposes) {
        const granted = (tcData && tcData.purpose && tcData.purpose.consents) || {};
        return purposes.every((purpose) => granted[purpose] === true);
    }

    function trackRevenueEvent(eventPayload) {
        if (!consent.analytics) {
            return;
        }
        const payloadBody = JSON.stringify({ pageType: config.pageType, ...eventPayload });
        if (navigator.sendBeacon) {
            const blob = new Blob([payloadBody], { type: "application/json" });
            navigator.sendBeacon("/api/metrics/revenue", blob);
            return;
        }
        fetch("/api/metrics/revenue", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: payloadBody,
            keepalive: true
        }).catch((error) => {
            console.warn("Revenue tracking failed", error);
        });
    }

    function trackPageViewOnce() {
        if (pageViewSent || !consent.analytics) {
            return;
        }
        pageViewSent = true;
        trackRevenueEvent({ eventType: "page_view", status: "viewed" });
    }

    function loadAdScript() {
        if (adScriptRequested) {
            return;
        }
        adScriptRequested = true;
        const script = document.createElement("script");
        script.async = true;
        script.crossOrigin = "anonymous";
        script.src = "https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=" +
            encodeURIComponent(config.adsClient);
        document.head.appendChild(script);
    }

    function initAds() {
        if (!config.adsEnabled || !consent.ads) {
            return;
        }
        loadAdScript();
        window.adsbygoogle = window.adsbygoogle || [];
        // Contextual ads only unless the visitor opted in to personalization.
        window.adsbygoogle.requestNonPersonalizedAds = consent.personalizedAds ? 0 : 1;

        document.querySelectorAll(".adsbygoogle").forEach((slot) => {
            if (slot.dataset.adsInitialized === "1") {
                return;
            }
            const container = slot.closest("[data-ad-container]");
            if (container) {
                container.hidden = false;
            }
            try {
                window.adsbygoogle.push({});
                slot.dataset.adsInitialized = "1";
                trackRevenueEvent({
                    eventType: "ad_init",
                    slot: slot.dataset.slotName || "unknown",
                    status: "success"
                });
            } catch (error) {
                if (container) {
                    container.hidden = true;
                }
                trackRevenueEvent({
                    eventType: "ad_init",
                    slot: slot.dataset.slotName || "unknown",
                    status: "failed"
                });
            }
        });
    }

    function applyConsent(tcData) {
        consent.ads = hasPurposes(tcData, REQUIRED_PURPOSES.ads);
        consent.personalizedAds = hasPurposes(tcData, REQUIRED_PURPOSES.personalizedAds);
        consent.analytics = hasPurposes(tcData, REQUIRED_PURPOSES.analytics);

        gtag("consent", "update", {
            ad_storage: consent.ads ? "granted" : "denied",
            ad_user_data: consent.personalizedAds ? "granted" : "denied",
            ad_personalization: consent.personalizedAds ? "granted" : "denied",
            analytics_storage: consent.analytics ? "granted" : "denied"
        });

        trackPageViewOnce();
        initAds();
    }

    function listenToCmp() {
        let attempts = 0;
        const timer = window.setInterval(() => {
            attempts += 1;
            if (typeof window.__tcfapi === "function") {
                window.clearInterval(timer);
                window.__tcfapi("addEventListener", 2, (tcData, success) => {
                    if (success && (tcData.eventStatus === "tcloaded" || tcData.eventStatus === "useractioncomplete")) {
                        applyConsent(tcData);
                    }
                });
            } else if (attempts >= TCF_POLL_LIMIT) {
                window.clearInterval(timer);
            }
        }, TCF_POLL_INTERVAL_MS);
    }

    function openConsentSettings() {
        if (typeof window.__tcfapi === "function") {
            window.__tcfapi("displayConsentUi", 2, () => {});
        }
        document.dispatchEvent(new CustomEvent("site:open-consent"));
    }

    document.addEventListener("click", (event) => {
        if (event.target.closest("[data-open-consent]")) {
            openConsentSettings();
        }
    });

    window.SiteConsent = { open: openConsentSettings, state: () => ({ ...consent }) };

    if (config.cmpEnabled) {
        listenToCmp();
    }
})();
