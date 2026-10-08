// ClosetIQ front-end behaviour. Kept in an external file because the framework
// serves a strict CSP (default-src 'self') that blocks inline scripts, inline
// event handlers, and inline style attributes. The AJAX helpers live under the
// `frond` namespace (frond.min.js), not as globals.

// Register the service worker so ClosetIQ is installable as a PWA (the base for
// a Play Store TWA build) — but ONLY on a real host. On localhost a caching SW
// makes a restarted dev server show a sticky offline page, so we skip
// registration there; sw.js self-unregisters on localhost to clean up any that
// was registered earlier.
(function () {
    if (!("serviceWorker" in navigator)) return;
    var host = location.hostname;
    var isLocal =
        host === "localhost" || host === "127.0.0.1" || host === "[::1]" || host.endsWith(".localhost");
    if (isLocal) return;
    window.addEventListener("load", function () {
        navigator.serviceWorker.register("/sw.js").catch(function () { /* non-fatal */ });
    });
})();

document.addEventListener("DOMContentLoaded", function () {
    // Paint per-item swatch colours (inline style attrs are CSP-blocked, but the
    // CSSOM .style API from this same-origin script is allowed).
    document.querySelectorAll("[data-swatch]").forEach(function (el) {
        el.style.setProperty("--swatch", el.getAttribute("data-swatch"));
    });

    // Toggle the "add item" panel.
    document.querySelectorAll('[data-action="toggle-add"]').forEach(function (btn) {
        btn.addEventListener("click", function () {
            var panel = document.getElementById("addPanel");
            if (!panel) return;
            panel.hidden = !panel.hidden;
            if (!panel.hidden) panel.scrollIntoView({ behavior: "smooth" });
        });
    });

    // Save a new wardrobe item (frond.form.submit collects inputs, files & token).
    var saveBtn = document.querySelector('[data-action="save-item"]');
    if (saveBtn) {
        saveBtn.addEventListener("click", function () {
            var msg = document.getElementById("formMessage");
            frond.request("/api/wardrobe", {
                method: "POST",
                body: frond.form.collect("itemForm"),
                onSuccess: function () { window.location.reload(); },
                onError: function (status, xhr) {
                    var text = "Could not save item. Please try again.";
                    try {
                        var res = JSON.parse(xhr.response);
                        if (res && res.error) text = res.error;
                    } catch (e) {}
                    if (msg) msg.textContent = text;
                },
            });
        });
    }

    // Delete an item (each card is a small form carrying its id + token).
    document.querySelectorAll("form[data-delete-id]").forEach(function (form) {
        form.addEventListener("submit", function (event) {
            event.preventDefault();
            if (!confirm("Remove this item from your wardrobe?")) return;
            var id = form.getAttribute("data-delete-id");
            var body = new FormData(form);
            frond.request("/api/wardrobe/" + id + "/delete", {
                method: "POST",
                body: body,
                onSuccess: function () { window.location.reload(); },
            });
        });
    });

    // Auto-submit the outfit controls when occasion/weather changes.
    document.querySelectorAll("[data-autosubmit]").forEach(function (el) {
        el.addEventListener("change", function () {
            if (el.form) el.form.submit();
        });
    });

    // Live weather: detect location, look it up, and drive the outfit bucket.
    var outfitForm = document.querySelector("[data-outfit-form]");
    if (outfitForm) initWeather(outfitForm);
});

function initWeather(form) {
    var banner = document.getElementById("ciqWeatherBanner");
    var active = form.getAttribute("data-active-weather") || "mild";

    function setBanner(html, isWarn) {
        if (!banner) return;
        banner.innerHTML = html;
        banner.hidden = false;
        banner.classList.toggle("is-warn", !!isWarn);
    }

    function escapeHtml(s) {
        return String(s).replace(/[&<>"]/g, function (c) {
            return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c];
        });
    }

    function applyBucket(bucket) {
        var radio = form.querySelector('input[name="weather"][value="' + bucket + '"]');
        if (radio) {
            radio.checked = true;
            form.submit();
        }
    }

    function label(bucket) {
        return bucket.charAt(0).toUpperCase() + bucket.slice(1);
    }

    // Let the user re-apply a detected bucket that differs from the active one.
    if (banner) {
        banner.addEventListener("click", function (event) {
            var target = event.target.closest("[data-apply-weather]");
            if (target) applyBucket(target.getAttribute("data-apply-weather"));
        });
    }

    function render(res) {
        var html =
            '<span class="ciq-weather-live">📍 ' + res.temperature + "°C · " +
            escapeHtml(res.description) + " · Detected: <strong>" + label(res.bucket) + "</strong></span>";
        if (res.bucket !== active) {
            html += ' <button type="button" class="ciq-btn ciq-btn-sm ciq-btn-outline" data-apply-weather="' +
                res.bucket + '">Style for ' + label(res.bucket) + "</button>";
        }
        setBanner(html, false);
    }

    function markApplied() {
        try { sessionStorage.setItem("ciq_weather_applied", "1"); } catch (e) {}
    }

    function detect(autoApply) {
        if (!navigator.geolocation) {
            setBanner("Location is not available here — pick your weather below.", true);
            return;
        }
        setBanner("Detecting your local weather…", false);
        navigator.geolocation.getCurrentPosition(
            function (pos) {
                var url = "/api/weather?lat=" + pos.coords.latitude + "&lon=" + pos.coords.longitude;
                frond.request(url, {
                    onSuccess: function (res) {
                        if (!res || res.error) {
                            setBanner("Could not load weather — pick your weather below.", true);
                            return;
                        }
                        render(res);
                        if (autoApply && res.bucket !== active) {
                            markApplied();
                            applyBucket(res.bucket);
                        } else if (autoApply) {
                            markApplied();
                        }
                    },
                    onError: function () {
                        setBanner("Weather service unavailable — pick your weather below.", true);
                    },
                });
            },
            function () {
                setBanner("Location permission denied — pick your weather below.", true);
                markApplied();
            },
            { timeout: 8000, maximumAge: 600000 }
        );
    }

    document.querySelectorAll('[data-action="detect-weather"]').forEach(function (btn) {
        btn.addEventListener("click", function () { detect(false); });
    });

    // Auto-detect on load; only auto-apply the bucket once per browser session.
    var applied = false;
    try { applied = !!sessionStorage.getItem("ciq_weather_applied"); } catch (e) {}
    detect(!applied);
}
