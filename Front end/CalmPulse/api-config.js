window.CALMPULSE_CONFIG = Object.freeze({
    API_URL: "http://localhost:8080"
});

window.getApiBaseUrl = function getApiBaseUrl() {
    return window.CALMPULSE_CONFIG.API_URL.replace(/\/+$/, "");
};
