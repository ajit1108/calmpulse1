document.addEventListener("DOMContentLoaded", async () => {
    const userId = localStorage.getItem("user_id");
    if (!userId) {
        window.location.href = "signin.html";
        return;
    }

    const BASE_URL = window.getApiBaseUrl();

    // 1. Create or Find Nav-Right
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
        // Render initial UI using localStorage fallbacks
        const firstName = localStorage.getItem("first_name") || "User";
        const lastName = localStorage.getItem("last_name") || "";
        const fullName = (firstName + " " + lastName).trim();
        const initial = firstName.charAt(0).toUpperCase();

        renderDropdown(fullName, initial);

        // Fetch latest profile from DB to dynamically sync navbar and localStorage
        try {
            const res = await fetch(`${BASE_URL}/profile/${userId}`);
            if (res.ok) {
                const user = await res.json();
                const dbFullName = ((user.firstName || "") + " " + (user.lastName || "")).trim() || "User";
                const dbInitial = (user.firstName || "U").charAt(0).toUpperCase();

                // Update localStorage
                localStorage.setItem("first_name", user.firstName || "");
                localStorage.setItem("last_name", user.lastName || "");
                localStorage.setItem("mode", user.role || "student");
                localStorage.setItem("is_new_user", String(user.isNewUser));

                // Re-render with fresh database values
                renderDropdown(dbFullName, dbInitial);

                // Set welcome message if on dashboard
                const welcomeEl = document.querySelector(".nav-content h5");
                if (welcomeEl) welcomeEl.textContent = `Welcome, ${dbFullName}!`;
            }
        } catch (err) {
            console.error("Error syncing profile details:", err);
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
                window.location.href = "signin.html";
            });
        }
    }
});
