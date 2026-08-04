/**
 * CalmPulse Centralized Auth & User State Manager
 * Renders consistent Bootstrap 5 Navbar across all authenticated pages.
 * Handles profile fetching, caching, profile completion checks, and logout.
 */
(function () {
    const PUBLIC_PAGES = ["index.html", "signin.html", "signup.html", "aboutus.html", "faq.html", "working.html"];

    function isPublicPage() {
        const path = window.location.pathname.toLowerCase();
        const page = path.split("/").pop().toLowerCase();
        if (!page || page === "" || page === "index.html") return true;
        return PUBLIC_PAGES.some(p => p.toLowerCase() === page);
    }

    // Ping ML service warm-up asynchronously
    function pingMlService() {
        if (window.getMlBaseUrl) {
            fetch(`${window.getMlBaseUrl()}/health`, { mode: 'no-cors' })
                .then(() => console.log("ML service warm-up ping sent."))
                .catch(err => console.warn("ML warm-up ping deferred:", err));
        }
    }

    /**
     * Fetch current user profile from backend database
     * @param {boolean} forceRefresh If true, skips session cache
     */
    window.loadCurrentUser = async function loadCurrentUser(forceRefresh = false) {
        const userId = localStorage.getItem("user_id");
        if (!userId) {
            if (!isPublicPage()) {
                window.location.href = "signin.html";
            }
            return null;
        }

        const BASE_URL = window.getApiBaseUrl();
        const cachedStr = sessionStorage.getItem("cached_user_profile");

        if (!forceRefresh && cachedStr) {
            try {
                const cachedUser = JSON.parse(cachedStr);
                renderNavbar(cachedUser);
                return cachedUser;
            } catch (e) {
                sessionStorage.removeItem("cached_user_profile");
            }
        }

        try {
            const res = await fetch(`${BASE_URL}/profile/${userId}`);
            if (!res.ok) {
                if (res.status === 401 || res.status === 403) {
                    if (!isPublicPage()) window.logoutUser();
                    return null;
                }
                throw new Error(`Profile load failed: ${res.status}`);
            }

            const user = await res.json();

            // Cache profile in session storage
            sessionStorage.setItem("cached_user_profile", JSON.stringify(user));

            // Sync localStorage helpers
            localStorage.setItem("first_name", user.firstName || "");
            localStorage.setItem("last_name", user.lastName || "");
            localStorage.setItem("mode", user.role || "student");
            localStorage.setItem("is_new_user", String(user.isNewUser !== false));
            if (user.streak !== undefined) localStorage.setItem("streak", user.streak);
            if (user.badge !== undefined) localStorage.setItem("badge", user.badge);

            renderNavbar(user);
            return user;
        } catch (err) {
            console.error("Error in loadCurrentUser:", err);
            const fallbackUser = {
                id: userId,
                firstName: localStorage.getItem("first_name") || "User",
                lastName: localStorage.getItem("last_name") || "",
                role: localStorage.getItem("mode") || "student",
                isNewUser: localStorage.getItem("is_new_user") === "true"
            };
            renderNavbar(fallbackUser);
            return fallbackUser;
        }
    };

    /**
     * Render consistent Bootstrap 5 Top-Right Navbar
     */
    function renderNavbar(user) {
        const firstName = user.firstName || "User";
        const lastName = user.lastName || "";
        const fullName = `${firstName} ${lastName}`.trim() || "User";
        const initial = firstName.charAt(0).toUpperCase() || "U";
        const profilePic = user.profilePicture || null;

        // Update welcome message if present on page
        const welcomeEls = document.querySelectorAll(".welcome-name, #welcome-display-name, .nav-content h5");
        welcomeEls.forEach(el => {
            if (el.tagName === 'SPAN') {
                el.textContent = fullName;
            } else {
                el.textContent = `Welcome, ${fullName}!`;
            }
        });

        // Find or create Nav-Right container
        let navRight = document.querySelector(".nav-right");
        if (!navRight && !isPublicPage()) {
            const nav = document.querySelector(".nav");
            if (nav) {
                navRight = document.createElement("div");
                navRight.className = "nav-right";
                nav.appendChild(navRight);
            }
        }

        if (navRight && !isPublicPage()) {
            const avatarHtml = profilePic 
                ? `<img src="${profilePic}" alt="${fullName}" class="rounded-circle me-2" style="width:36px; height:36px; object-fit:cover;">`
                : `<div class="avatar-circle rounded-circle me-2 bg-success text-white d-inline-flex align-items-center justify-content-center fw-bold" style="width:36px; height:36px; font-size:16px;">${initial}</div>`;

            navRight.innerHTML = `
                <div class="dropdown user-profile-menu">
                    <button class="btn btn-link text-decoration-none dropdown-toggle d-flex align-items-center text-dark p-0 border-0 shadow-none" type="button" id="userDropdown" data-bs-toggle="dropdown" aria-expanded="false" style="color: inherit;">
                        ${avatarHtml}
                        <span class="user-name fw-semibold me-1">${fullName}</span>
                    </button>
                    <ul class="dropdown-menu dropdown-menu-end shadow-sm" aria-labelledby="userDropdown">
                        <li><a class="dropdown-item py-2 d-flex align-items-center" href="dashboard.html"><i class="fa-solid fa-house me-2 text-success"></i> Dashboard</a></li>
                        <li><a class="dropdown-item py-2 d-flex align-items-center" href="profile.html"><i class="fa-solid fa-user me-2 text-primary"></i> My Profile</a></li>
                        <li><a class="dropdown-item py-2 d-flex align-items-center" href="profile.html?edit=true"><i class="fa-solid fa-pen-to-square me-2 text-warning"></i> Edit Profile</a></li>
                        <li><hr class="dropdown-divider"></li>
                        <li><a class="dropdown-item py-2 d-flex align-items-center text-danger" href="#" id="dropdown-logout-btn"><i class="fa-solid fa-right-from-bracket me-2"></i> Logout</a></li>
                    </ul>
                </div>
            `;

            const logoutBtn = document.getElementById("dropdown-logout-btn");
            if (logoutBtn) {
                logoutBtn.addEventListener("click", (e) => {
                    e.preventDefault();
                    window.logoutUser();
                });
            }

            const pageSignoutBtn = document.getElementById("signout-btn");
            if (pageSignoutBtn) {
                pageSignoutBtn.addEventListener("click", (e) => {
                    e.preventDefault();
                    window.logoutUser();
                });
            }
        }
    }

    /**
     * Clear Session & Logout
     */
    window.logoutUser = function logoutUser() {
        localStorage.clear();
        sessionStorage.clear();
        window.location.href = "signin.html";
    };

    // Auto-run on DOM Ready
    document.addEventListener("DOMContentLoaded", () => {
        if (!isPublicPage()) {
            const userId = localStorage.getItem("user_id");
            if (!userId) {
                window.location.href = "signin.html";
                return;
            }
            window.loadCurrentUser();
            pingMlService();
        }
    });

})();
