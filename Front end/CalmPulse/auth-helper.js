document.addEventListener("DOMContentLoaded", () => {
    const userId = localStorage.getItem("user_id");
    if (!userId) {
        window.location.href = "signin.html";
        return;
    }

    const BASE_URL = window.getApiBaseUrl();

    // Warm up the Python ML microservice asynchronously in the background (prevents Render spin-down 502/Gateway Timeouts)
    fetch("https://calmpulse1.onrender.com/health", { mode: 'no-cors' })
        .then(() => console.log("ML service warm-up ping sent successfully."))
        .catch(err => console.warn("Warm-up ping deferred:", err));

    // 1. Find or create Nav-Right container
    let navRight = document.querySelector(".nav-right");
    if (!navRight) {
        const nav = document.querySelector(".nav");
        if (nav) {
            navRight = document.createElement("div");
            navRight.className = "nav-right";
            nav.appendChild(navRight);
        }
    }

    if (navRight) {
        // --- 1. INSTANT RENDER (Stale-While-Revalidate) ---
        // Render immediately using localStorage to make page transitions instant
        const firstName = localStorage.getItem("first_name") || "User";
        const lastName = localStorage.getItem("last_name") || "";
        const fullName = (firstName + " " + lastName).trim();
        const initial = firstName.charAt(0).toUpperCase();

        renderDropdown(fullName, initial);

        // Update welcome message instantly if it exists on the page
        const welcomeEl = document.querySelector(".nav-content h5");
        if (welcomeEl) welcomeEl.textContent = `Welcome, ${fullName}!`;

        // --- 2. BACKGROUND SYNC (Once per Session) ---
        // Only hit the backend if we haven't synced in this session yet
        if (sessionStorage.getItem("profile_synced") !== "true" || !localStorage.getItem("first_name")) {
            fetch(`${BASE_URL}/profile/${userId}`)
                .then(res => {
                    if (res.ok) return res.json();
                    throw new Error("Failed to fetch");
                })
                .then(user => {
                    const dbFullName = ((user.firstName || "") + " " + (user.lastName || "")).trim() || "User";
                    const dbInitial = (user.firstName || "U").charAt(0).toUpperCase();

                    // Sync storage
                    localStorage.setItem("first_name", user.firstName || "");
                    localStorage.setItem("last_name", user.lastName || "");
                    localStorage.setItem("mode", user.role || "student");
                    localStorage.setItem("is_new_user", String(user.isNewUser));
                    
                    // Mark session as synced
                    sessionStorage.setItem("profile_synced", "true");

                    // Re-render dropdown quietly with fresh DB values
                    renderDropdown(dbFullName, dbInitial);
                    if (welcomeEl) welcomeEl.textContent = `Welcome, ${dbFullName}!`;
                })
                .catch(err => console.warn("Background profile sync deferred:", err));
        }
    }

    function renderDropdown(name, initial) {
        navRight.innerHTML = `
            <div class="user-profile-menu">
                <div class="profile-trigger" id="profile-trigger">
                    <div class="avatar-circle" id="nav-avatar">${initial}</div>
                    <span class="user-name" id="nav-username">${name}</span>
                    <i class="fa-solid fa-chevron-down dropdown-arrow"></i>
                </div>
                <div class="dropdown-menu" id="profile-dropdown">
                    <a href="dashboard.html"><i class="fa-solid fa-house"></i> Dashboard</a>
                    <a href="profile.html"><i class="fa-solid fa-user"></i> My Profile</a>
                    <a href="profile.html?edit=true"><i class="fa-solid fa-pen-to-square"></i> Edit Profile</a>
                    <a href="#" id="dropdown-signout"><i class="fa-solid fa-right-from-bracket"></i> Logout</a>
                </div>
            </div>
        `;

        const trigger = document.getElementById("profile-trigger");
        const dropdown = document.getElementById("profile-dropdown");

        if (trigger && dropdown) {
            trigger.addEventListener("click", (e) => {
                e.stopPropagation();
                trigger.classList.toggle("active");
                dropdown.classList.toggle("show");
            });

            document.addEventListener("click", () => {
                trigger.classList.remove("active");
                dropdown.classList.remove("show");
            });
        }

        const signoutBtn = document.getElementById("dropdown-signout");
        if (signoutBtn) {
            signoutBtn.addEventListener("click", (e) => {
                e.preventDefault();
                localStorage.clear();
                sessionStorage.clear();
                window.location.href = "signin.html";
            });
        }
    }
});
