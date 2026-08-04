(function() {
    const hostname = window.location.hostname;
    
    // Base Spring Boot backend URL
    let url = "http://localhost:8080";
    if (hostname !== "localhost" && hostname !== "127.0.0.1" && hostname !== "") {
        url = "https://calmpulsebackend.onrender.com";
    }

    // Base Python ML URL
    let mlUrl = "https://calmpulse1.onrender.com";

    window.CALMPULSE_CONFIG = Object.freeze({
        API_URL: url,
        ML_URL: mlUrl
    });

    window.getApiBaseUrl = function getApiBaseUrl() {
        return window.CALMPULSE_CONFIG.API_URL.replace(/\/+$/, "");
    };

    window.getMlBaseUrl = function getMlBaseUrl() {
        return window.CALMPULSE_CONFIG.ML_URL.replace(/\/+$/, "");
    };

    /**
     * Standard Prediction Mapper
     * @param {number|string} score Raw score or code
     * @param {string} role 'student' or 'employee'
     * @returns {object} { label: 'Low'|'Medium'|'High'|'Unknown', code: number|null, badgeClass: string, color: string }
     */
    window.mapPredictionScore = function mapPredictionScore(score, role) {
        const num = parseFloat(score);
        if (isNaN(num)) {
            return { label: 'Unknown', code: null, badgeClass: 'bg-secondary', color: '#6c757d' };
        }

        const isEmployee = (role && role.toLowerCase() === 'employee');

        if (isEmployee) {
            // Employee scale: 1 = Low, 2 = Medium, 3 = High
            if (num < 1.5 || num === 1) {
                return { label: 'Low', code: 1, badgeClass: 'bg-success', color: '#198754' };
            } else if (num < 2.5 || num === 2) {
                return { label: 'Medium', code: 2, badgeClass: 'bg-warning text-dark', color: '#ffc107' };
            } else {
                return { label: 'High', code: 3, badgeClass: 'bg-danger', color: '#dc3545' };
            }
        } else {
            // Student scale: 0 = Low, 1 = Medium, 2 = High
            if (num < 0.5 || num === 0) {
                return { label: 'Low', code: 0, badgeClass: 'bg-success', color: '#198754' };
            } else if (num < 1.5 || num === 1) {
                return { label: 'Medium', code: 1, badgeClass: 'bg-warning text-dark', color: '#ffc107' };
            } else {
                return { label: 'High', code: 2, badgeClass: 'bg-danger', color: '#dc3545' };
            }
        }
    };
})();
