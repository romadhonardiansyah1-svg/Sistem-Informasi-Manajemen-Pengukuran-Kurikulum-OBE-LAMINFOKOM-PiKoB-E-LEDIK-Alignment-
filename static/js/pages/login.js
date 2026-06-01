/**
 * Login page handler.
 */
(function () {
    document.addEventListener("DOMContentLoaded", function () {
        var form = document.getElementById("login-form");
        if (!form) return;

        form.addEventListener("submit", function (e) {
            e.preventDefault();

            var username = document.getElementById("username").value;
            var password = document.getElementById("password").value;
            var errorEl = document.getElementById("login-error");

            Api.post("/api/auth/login", {
                username: username,
                password: password,
            }).then(function (res) {
                if (res.status === "success") {
                    window.location.href = "/";
                } else {
                    errorEl.textContent = res.message || "Login gagal";
                    errorEl.style.display = "block";
                }
            }).catch(function () {
                errorEl.textContent = "Koneksi gagal";
                errorEl.style.display = "block";
            });
        });
    });
})();
