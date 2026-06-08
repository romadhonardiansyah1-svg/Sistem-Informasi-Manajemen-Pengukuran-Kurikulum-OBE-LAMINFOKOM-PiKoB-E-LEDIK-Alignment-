/**
 * Halaman "Manajemen Pengguna" (khusus Kaprodi/Admin).
 * Membuat & mengelola akun dosen, tim kurikulum, dan mahasiswa,
 * termasuk reset password.
 */
var UserManagementPage = (function () {

    var ROLE_LABELS = {
        "admin_universitas": "Admin Universitas",
        "dekan": "Dekan / Fakultas",
        "kaprodi": "Kaprodi",
        "tim_kurikulum": "Tim Kurikulum",
        "dosen": "Dosen / DPA",
        "mahasiswa": "Mahasiswa",
    };

    function init() {
        var content = document.getElementById("page-content");
        content.innerHTML =
            '<div class="page-header">' +
            '  <div><h2 class="page-title">Manajemen Pengguna</h2>' +
            '  <p class="page-desc">Kelola akun & hak akses dosen, tim kurikulum, dan mahasiswa</p></div>' +
            '  <button class="btn btn-primary btn-lg" id="btn-add-user">+ Tambah Pengguna</button>' +
            '</div>' +
            '<div class="card"><div class="card-body"><div id="user-list"></div></div></div>';

        document.getElementById("btn-add-user").addEventListener("click", function () {
            _openForm();
        });

        _loadUsers();
    }

    function _loadUsers() {
        Api.get("/api/users").then(function (res) {
            var items = res.data || [];
            var container = document.getElementById("user-list");
            if (items.length === 0) {
                container.innerHTML = '<div class="empty-state"><p>Belum ada pengguna.</p></div>';
                return;
            }
            var html = '<table class="data-table"><thead><tr>' +
                '<th>Username</th><th>Nama</th><th>Role</th><th>Email</th><th>Aksi</th>' +
                '</tr></thead><tbody>';
            for (var i = 0; i < items.length; i++) {
                var u = items[i];
                html += '<tr>';
                html += '<td class="cell-code">' + DomUtils.escape(u.username) + '</td>';
                html += '<td>' + DomUtils.escape(u.nama) + '</td>';
                html += '<td><span class="badge badge-success">' + DomUtils.escape(ROLE_LABELS[u.role] || u.role) + '</span></td>';
                html += '<td>' + DomUtils.escape(u.email || "-") + '</td>';
                html += '<td>' +
                    '<button class="btn btn-sm btn-outline" data-reset="' + u.id + '" data-uname="' + DomUtils.escape(u.username) + '">Reset Password</button> ' +
                    '<button class="btn btn-sm btn-outline" data-del="' + u.id + '">Hapus</button>' +
                    '</td>';
                html += '</tr>';
            }
            html += '</tbody></table>';
            container.innerHTML = html;

            _wireRowButtons(container);
        });
    }

    function _wireRowButtons(container) {
        var resetBtns = container.querySelectorAll("[data-reset]");
        for (var i = 0; i < resetBtns.length; i++) {
            resetBtns[i].addEventListener("click", function () {
                var id = this.getAttribute("data-reset");
                var uname = this.getAttribute("data-uname");
                var pwd = prompt("Password baru untuk " + uname + " (kosongkan = sama dengan username):", "");
                if (pwd === null) return;
                Api.post("/api/users/" + id + "/reset-password", { password: pwd }).then(function (res) {
                    if (res.status === "error") { ToastComponent.error(res.message); return; }
                    ToastComponent.success("Password direset.");
                });
            });
        }
        var delBtns = container.querySelectorAll("[data-del]");
        for (var j = 0; j < delBtns.length; j++) {
            delBtns[j].addEventListener("click", function () {
                var id = this.getAttribute("data-del");
                if (!confirm("Hapus pengguna ini?")) return;
                Api.del("/api/users/" + id).then(function (res) {
                    if (res.status === "error") { ToastComponent.error(res.message); return; }
                    ToastComponent.success("Pengguna dihapus.");
                    _loadUsers();
                });
            });
        }
    }

    function _openForm() {
        var roleOpts = '';
        Object.keys(ROLE_LABELS).forEach(function (k) {
            roleOpts += '<option value="' + k + '">' + ROLE_LABELS[k] + '</option>';
        });

        var body =
            '<div class="form-group"><label>Username / NIM</label>' +
            '  <input id="u-username" class="form-control"></div>' +
            '<div class="form-group"><label>Nama Lengkap</label>' +
            '  <input id="u-nama" class="form-control"></div>' +
            '<div class="form-group"><label>Role</label>' +
            '  <select id="u-role" class="periode-select" style="width:100%">' + roleOpts + '</select></div>' +
            '<div class="form-group" id="u-angkatan-group" style="display:none"><label>Angkatan</label>' +
            '  <input id="u-angkatan" type="number" class="form-control" placeholder="mis. 2024"></div>' +
            '<div class="form-group"><label>Email</label>' +
            '  <input id="u-email" class="form-control"></div>' +
            '<div class="form-group"><label>Password awal</label>' +
            '  <input id="u-password" class="form-control" placeholder="kosongkan = sama dengan username"></div>';

        var footer =
            '<button class="btn btn-outline" id="u-cancel">Batal</button>' +
            '<button class="btn btn-primary" id="u-save">Simpan</button>';

        ModalComponent.open("Tambah Pengguna", body, footer);

        var roleSel = document.getElementById("u-role");
        roleSel.addEventListener("change", function () {
            document.getElementById("u-angkatan-group").style.display =
                this.value === "mahasiswa" ? "" : "none";
        });

        document.getElementById("u-cancel").addEventListener("click", ModalComponent.close);
        document.getElementById("u-save").addEventListener("click", function () {
            var payload = {
                username: document.getElementById("u-username").value.trim(),
                nama: document.getElementById("u-nama").value.trim(),
                role: document.getElementById("u-role").value,
                email: document.getElementById("u-email").value.trim(),
                password: document.getElementById("u-password").value,
            };
            if (payload.role === "mahasiswa") {
                payload.angkatan = parseInt(document.getElementById("u-angkatan").value, 10) || 0;
            }
            if (!payload.username) { ToastComponent.error("Username wajib diisi."); return; }

            Api.post("/api/users", payload).then(function (res) {
                if (res.status === "error") { ToastComponent.error(res.message); return; }
                ToastComponent.success("Pengguna dibuat.");
                ModalComponent.close();
                _loadUsers();
            });
        });
    }

    return { init: init };

})();
