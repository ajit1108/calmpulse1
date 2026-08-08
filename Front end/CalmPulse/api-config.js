(function() {
    const hostname = window.location.hostname;
    
    // Base Spring Boot backend URL: default to production, only use local for localhost dev servers
    let url = "https://calmpulsebackend.onrender.com";
    if (hostname === "localhost" || hostname === "127.0.0.1") {
        url = "http://localhost:8080";
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

    /**
     * Centralized Date/Time Formatter
     * @param {string|Date|number} dateInput 
     * @returns {string} formatted date string e.g. "04 Aug 2026, 07:45 PM"
     */
    window.formatDateTime = function formatDateTime(dateInput) {
        const d = new Date(dateInput);
        if (isNaN(d.getTime())) return "N/A";
        
        const day = String(d.getDate()).padStart(2, '0');
        const months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
        const month = months[d.getMonth()];
        const year = d.getFullYear();
        
        let hours = d.getHours();
        const minutes = String(d.getMinutes()).padStart(2, '0');
        const ampm = hours >= 12 ? 'PM' : 'AM';
        hours = hours % 12;
        hours = hours ? hours : 12; // the hour '0' should be '12'
        const formattedHours = String(hours).padStart(2, '0');
        
        return `${day} ${month} ${year}, ${formattedHours}:${minutes} ${ampm}`;
    };

    /**
     * Centralized Graph Date Formatter
     * @param {string|Date|number} dateInput 
     * @returns {string} formatted date string e.g. "28 Jul"
     */
    window.formatGraphDate = function formatGraphDate(dateInput) {
        const d = new Date(dateInput);
        if (isNaN(d.getTime())) return "Check-in";
        const day = String(d.getDate()).padStart(2, '0');
        const months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
        const month = months[d.getMonth()];
        return `${day} ${month}`;
    };
})();
