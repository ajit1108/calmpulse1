(function() {
    const hostname = window.location.hostname;
    
    // Default local URL
    let url = "http://localhost:8080";
    
    // If accessed over the internet, point to your deployed Render backend service URL.
    // Replace 'calmpulse-backend.onrender.com' with your actual Render URL after deploying.
    if (hostname !== "localhost" && hostname !== "127.0.0.1" && hostname !== "") {
        url = "https://calmpulse.onrender.com";
    }

    window.CALMPULSE_CONFIG = Object.freeze({
        API_URL: url
    });

    window.getApiBaseUrl = function getApiBaseUrl() {
        return window.CALMPULSE_CONFIG.API_URL.replace(/\/+$/, "");
    };
})();
