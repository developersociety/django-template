/* global Sentry */

window.sentryOnLoad = () => {
    let sentryConfig = {};
    const sentryConfigElement = document.getElementById('sentry-config');
    if (sentryConfigElement) {
        sentryConfig = JSON.parse(sentryConfigElement.textContent);
    }

    Sentry.init({
        ...sentryConfig,
        ignoreErrors: [
            // Excessive network issues
            'TypeError: Failed to fetch',
        ],
    });
};
