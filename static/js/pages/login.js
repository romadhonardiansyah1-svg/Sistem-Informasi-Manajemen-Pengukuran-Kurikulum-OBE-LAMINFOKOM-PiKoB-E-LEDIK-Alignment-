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
            var btn = form.querySelector("button[type=submit]");
            btn.disabled = true;
            btn.textContent = "Menghubungkan...";

            fetch("/api/auth/login", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                credentials: "same-origin",
                body: JSON.stringify({ username: username, password: password }),
            })
            .then(function (response) {
                return response.text().then(function (text) {
                    return { status: response.status, body: text };
                });
            })
            .then(function (result) {
                btn.disabled = false;
                btn.textContent = "Masuk";

                var data;
                try {
                    data = JSON.parse(result.body);
                } catch (parseErr) {
                    errorEl.textContent = "HTTP " + result.status + ": Server mengembalikan respon bukan JSON. Detail: " + result.body.substring(0, 300);
                    errorEl.style.display = "block";
                    return;
                }

                if (data.status === "success") {
                    window.location.href = "/";
                } else {
                    var msg = data.message || ("HTTP " + result.status + ": Login gagal");
                    if (data.traceback) {
                        msg += "\n\nTraceback:\n" + data.traceback;
                    }
                    errorEl.style.whiteSpace = "pre-wrap";
                    errorEl.textContent = msg;
                    errorEl.style.display = "block";
                }
            })
            .catch(function (err) {
                btn.disabled = false;
                btn.textContent = "Masuk";
                errorEl.textContent = "Network error: " + (err.message || err);
                errorEl.style.display = "block";
            });
        });
    });
})();

