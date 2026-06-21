/**
 * Header bar component.
 * Menampilkan dropdown periode kurikulum (+ durasi tahun), aksi VALIDASI/KUNCI
 * periode, dan info user.
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

    // Durasi periode (inklusif). 2024-2028 -> 5 tahun.
    function _durasi(p) {
        if (p && p.tahun_mulai && p.tahun_selesai) {
            return parseInt(p.tahun_selesai, 10) - parseInt(p.tahun_mulai, 10) + 1;
        }
        return null;
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
                var dur = _durasi(p);
                var labelDur = dur ? (" · " + dur + " tahun") : "";
                html += '<option value="' + p.id + '"' + selected + '>';
                html += DomUtils.escape(p.nama + labelDur);
                html += '</option>';
            }
            html += '</select>';
            html += '<span id="periode-lock-area" style="margin-left:10px;display:inline-flex;align-items:center;gap:6px"></span>';
            container.innerHTML = html;

            var dropdown = document.getElementById("periode-dropdown");
            var activeItem = list.filter(function (p) { return p.status === "aktif"; })[0];
            AppState.currentPeriode = activeItem || list[0] || null;
            _renderLock();

            dropdown.addEventListener("change", function () {
                var selectedId = parseInt(this.value, 10);
                for (var j = 0; j < list.length; j++) {
                    if (list[j].id === selectedId) {
                        AppState.currentPeriode = list[j];
                        break;
                    }
                }
                _renderLock();
                EventBus.emit("periode:changed", AppState.currentPeriode);
            });
        });
    }

    // Render badge status + tombol aksi validasi/kunci untuk periode terpilih.
    function _renderLock() {
        var area = document.getElementById("periode-lock-area");
        var p = AppState.currentPeriode;
        if (!area || !p) return;

        var badgeBase = "padding:2px 8px;border-radius:10px;font-size:0.7rem;font-weight:600;color:#fff;";
        if (p.locked) {
            area.innerHTML =
                '<span style="' + badgeBase + 'background:hsl(0,62%,46%)" title="Periode dikunci: data master/matriks tidak bisa diubah">🔒 Terkunci</span>' +
                '<button class="btn btn-sm btn-outline" id="btn-toggle-lock">Buka Kunci</button>';
        } else {
            area.innerHTML =
                '<span style="' + badgeBase + 'background:hsl(140,42%,38%)" title="Periode terbuka: data masih bisa diubah">🔓 Terbuka</span>' +
                '<button class="btn btn-sm btn-primary" id="btn-toggle-lock">Validasi &amp; Kunci</button>';
        }
        var btn = document.getElementById("btn-toggle-lock");
        if (btn) btn.addEventListener("click", _toggleLock);
    }

    function _toggleLock() {
        var p = AppState.currentPeriode;
        if (!p) return;
        var lock = !p.locked;
        var msg = lock
            ? 'Kunci periode "' + p.nama + '"?\n\nSetelah dikunci, seluruh data master & matriks tidak bisa diubah sampai dibuka kembali.'
            : 'Buka kunci periode "' + p.nama + '" agar data bisa diubah lagi?';
        if (!window.confirm(msg)) return;

        var url = "/api/periode/" + p.id + (lock ? "/lock" : "/unlock");
        Api.post(url).then(function (res) {
            var ok = res && res.status === "success";
            if (ok) {
                p.locked = lock;
                // Sinkronkan juga objek di periodeList agar konsisten saat ganti dropdown.
                var pl = AppState.periodeList || [];
                for (var i = 0; i < pl.length; i++) {
                    if (pl[i].id === p.id) { pl[i].locked = lock; break; }
                }
                _renderLock();
                EventBus.emit("periode:lockchanged", p);
            }
            if (typeof ToastComponent !== "undefined") {
                ToastComponent.show(
                    ok ? (lock ? "Periode dikunci — validasi aktif" : "Periode dibuka kuncinya")
                       : ((res && res.message) || "Gagal mengubah status kunci"),
                    ok ? "success" : "error"
                );
            }
        });
    }

    return { init: init };

})();
