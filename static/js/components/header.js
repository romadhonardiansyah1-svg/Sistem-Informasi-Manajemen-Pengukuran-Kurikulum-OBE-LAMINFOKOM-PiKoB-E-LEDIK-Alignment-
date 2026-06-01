/**
 * Header bar component.
 * Menampilkan dropdown periode kurikulum dan info user.
 */
var HeaderComponent = (function () {

    function init(user) {
        document.getElementById("header-user-name").textContent = user.nama;
        document.getElementById("header-user-role").textContent = user.role;

        document.getElementById("btn-logout").addEventListener("click", function () {
            Api.post("/api/auth/logout").then(function () {
                window.location.href = "/login";
            });
        });

        _loadPeriode();
    }

    function _loadPeriode() {
        Api.get("/api/periode").then(function (res) {
            var list = res.data || [];
            AppState.periodeList = list;

            var container = document.getElementById("header-periode");
            if (!container || list.length === 0) return;

            var html = '<select class="periode-select" id="periode-dropdown">';
            for (var i = 0; i < list.length; i++) {
                var p = list[i];
                var selected = p.status === "aktif" ? " selected" : "";
                html += '<option value="' + p.id + '"' + selected + '>';
                html += DomUtils.escape(p.nama);
                html += '</option>';
            }
            html += '</select>';
            container.innerHTML = html;

            var dropdown = document.getElementById("periode-dropdown");
            var activeItem = list.filter(function (p) { return p.status === "aktif"; })[0];
            AppState.currentPeriode = activeItem || list[0] || null;

            dropdown.addEventListener("change", function () {
                var selectedId = parseInt(this.value, 10);
                for (var j = 0; j < list.length; j++) {
                    if (list[j].id === selectedId) {
                        AppState.currentPeriode = list[j];
                        break;
                    }
                }
                EventBus.emit("periode:changed", AppState.currentPeriode);
            });
        });
    }

    return { init: init };

})();
