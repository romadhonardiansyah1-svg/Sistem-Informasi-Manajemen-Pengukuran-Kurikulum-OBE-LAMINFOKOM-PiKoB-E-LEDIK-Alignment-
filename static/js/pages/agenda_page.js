/**
 * Halaman "Agenda & Dokumen Mutu".
 * Modul pengumpulan dokumen + notulensi untuk kegiatan penjaminan mutu:
 * Peninjauan Kurikulum, Reuni Alumni, FGD/Lokakarya, Rapat Mutu.
 * Mendukung filter per jenis & periode, serta unggah banyak PDF (drag-and-drop).
 */
var AgendaPage = (function () {

    var JENIS_LABELS = {
        "peninjauan_kurikulum": "Peninjauan Kurikulum",
        "reuni_alumni": "Reuni Alumni",
        "fgd_lokakarya": "FGD / Lokakarya",
        "rapat_mutu": "Rapat Mutu",
    };

    function _canManage() {
        var a = (AppState.user && AppState.user.allowed_actions) || [];
        return a.indexOf("manage_dokumen") !== -1;
    }

    function init() {
        var content = document.getElementById("page-content");

        var jenisOpts = '<option value="">Semua Jenis</option>';
        Object.keys(JENIS_LABELS).forEach(function (k) {
            jenisOpts += '<option value="' + k + '">' + JENIS_LABELS[k] + '</option>';
        });

        var addBtn = _canManage()
            ? '<button class="btn btn-primary btn-lg" id="btn-add-agenda">+ Tambah Agenda</button>'
            : '';

        content.innerHTML =
            '<div class="page-header">' +
            '  <div><h2 class="page-title">Agenda & Dokumen Mutu</h2>' +
            '  <p class="page-desc">Notulensi & bukti fisik kegiatan penjaminan mutu (termasuk reuni alumni)</p></div>' +
            '  ' + addBtn +
            '</div>' +
            '<div class="card"><div class="card-body">' +
            '  <div class="filter-bar" style="display:flex;gap:12px;flex-wrap:wrap;margin-bottom:12px">' +
            '    <select id="filter-jenis" class="periode-select">' + jenisOpts + '</select>' +
            '  </div>' +
            '  <div id="agenda-list"></div>' +
            '</div></div>';

        if (_canManage()) {
            document.getElementById("btn-add-agenda").addEventListener("click", function () {
                _openForm(null);
            });
        }
        document.getElementById("filter-jenis").addEventListener("change", _loadList);

        _loadList();
    }

    function _loadList() {
        var jenis = document.getElementById("filter-jenis").value;
        var url = "/api/log-peninjauan";
        if (jenis) url += "?jenis=" + encodeURIComponent(jenis);

        Api.get(url).then(function (res) {
            var items = res.data || [];
            var container = document.getElementById("agenda-list");
            if (items.length === 0) {
                container.innerHTML = '<div class="empty-state"><p>Belum ada agenda. ' +
                    (_canManage() ? 'Klik "Tambah Agenda" untuk membuat.' : '') + '</p></div>';
                return;
            }

            var html = '<table class="data-table"><thead><tr>' +
                '<th>Jenis</th><th>Judul</th><th>Tanggal</th><th>Lokasi</th><th>Dokumen</th><th>Aksi</th>' +
                '</tr></thead><tbody>';
            for (var i = 0; i < items.length; i++) {
                var it = items[i];
                html += '<tr>';
                html += '<td><span class="badge badge-success">' + DomUtils.escape(JENIS_LABELS[it.jenis] || it.jenis) + '</span></td>';
                html += '<td>' + DomUtils.escape(it.judul) + '</td>';
                html += '<td>' + DomUtils.escape(it.tanggal) + '</td>';
                html += '<td>' + DomUtils.escape(it.lokasi || "-") + '</td>';
                html += '<td>' + (it.dokumen_count || 0) + ' file</td>';
                html += '<td><button class="btn btn-sm btn-outline" data-detail="' + it.id + '">Buka</button></td>';
                html += '</tr>';
            }
            html += '</tbody></table>';
            container.innerHTML = html;

            var btns = container.querySelectorAll("[data-detail]");
            for (var b = 0; b < btns.length; b++) {
                btns[b].addEventListener("click", function () {
                    _openDetail(parseInt(this.getAttribute("data-detail"), 10));
                });
            }
        });
    }

    function _periodeOptions(selectedId) {
        var list = AppState.periodeList || [];
        var html = '<option value="">- Tidak terkait periode -</option>';
        for (var i = 0; i < list.length; i++) {
            var sel = (selectedId && list[i].id === selectedId) ? " selected" : "";
            html += '<option value="' + list[i].id + '"' + sel + '>' + DomUtils.escape(list[i].nama) + '</option>';
        }
        return html;
    }

    function _openForm(existing) {
        var ex = existing || {};
        var jenisOpts = '';
        Object.keys(JENIS_LABELS).forEach(function (k) {
            var sel = ex.jenis === k ? " selected" : "";
            jenisOpts += '<option value="' + k + '"' + sel + '>' + JENIS_LABELS[k] + '</option>';
        });

        var body =
            '<div class="form-group"><label>Jenis Kegiatan</label>' +
            '  <select id="ag-jenis" class="periode-select" style="width:100%">' + jenisOpts + '</select></div>' +
            '<div class="form-group"><label>Judul</label>' +
            '  <input id="ag-judul" class="form-control" value="' + DomUtils.escape(ex.judul || "") + '"></div>' +
            '<div class="form-group"><label>Tanggal</label>' +
            '  <input id="ag-tanggal" type="date" class="form-control" value="' + DomUtils.escape(ex.tanggal || "") + '"></div>' +
            '<div class="form-group"><label>Lokasi</label>' +
            '  <input id="ag-lokasi" class="form-control" value="' + DomUtils.escape(ex.lokasi || "") + '"></div>' +
            '<div class="form-group"><label>Periode Kurikulum</label>' +
            '  <select id="ag-periode" class="periode-select" style="width:100%">' + _periodeOptions(ex.periode_id) + '</select></div>' +
            '<div class="form-group"><label>Peserta</label>' +
            '  <textarea id="ag-peserta" class="form-control" rows="2">' + DomUtils.escape(ex.peserta || "") + '</textarea></div>' +
            '<div class="form-group"><label>Notulensi</label>' +
            '  <textarea id="ag-catatan" class="form-control" rows="5">' + DomUtils.escape(ex.catatan || "") + '</textarea></div>';

        var footer =
            '<button class="btn btn-outline" id="ag-cancel">Batal</button>' +
            '<button class="btn btn-primary" id="ag-save">Simpan</button>';

        ModalComponent.open(ex.id ? "Edit Agenda" : "Tambah Agenda", body, footer);

        document.getElementById("ag-cancel").addEventListener("click", ModalComponent.close);
        document.getElementById("ag-save").addEventListener("click", function () {
            var payload = {
                jenis: document.getElementById("ag-jenis").value,
                judul: document.getElementById("ag-judul").value.trim(),
                tanggal: document.getElementById("ag-tanggal").value,
                lokasi: document.getElementById("ag-lokasi").value.trim(),
                peserta: document.getElementById("ag-peserta").value.trim(),
                catatan: document.getElementById("ag-catatan").value.trim(),
            };
            var periodeVal = document.getElementById("ag-periode").value;
            if (periodeVal) payload.periode_id = parseInt(periodeVal, 10);

            if (!payload.judul || !payload.tanggal) {
                ToastComponent.error("Judul dan tanggal wajib diisi.");
                return;
            }

            var p = ex.id
                ? Api.put("/api/log-peninjauan/" + ex.id, payload)
                : Api.post("/api/log-peninjauan", payload);

            p.then(function (res) {
                if (res.status === "error") { ToastComponent.error(res.message); return; }
                ToastComponent.success("Agenda tersimpan.");
                ModalComponent.close();
                _loadList();
            });
        });
    }

    function _openDetail(id) {
        Api.get("/api/log-peninjauan/" + id).then(function (res) {
            var d = res.data;
            if (!d) { ToastComponent.error("Agenda tidak ditemukan."); return; }

            var manage = _canManage();
            var docs = d.dokumen || [];
            var docsHtml = '';
            if (docs.length === 0) {
                docsHtml = '<p class="dash-more">Belum ada dokumen.</p>';
            } else {
                docsHtml = '<ul class="doc-list">';
                for (var i = 0; i < docs.length; i++) {
                    var doc = docs[i];
                    docsHtml += '<li style="display:flex;justify-content:space-between;align-items:center;padding:6px 0;border-bottom:1px solid #eee">';
                    docsHtml += '<a href="/api/dokumen-bukti/' + doc.id + '/download" target="_blank">' + DomUtils.escape(doc.filename) + '</a>';
                    if (manage) {
                        docsHtml += '<button class="btn btn-sm btn-outline" data-deldoc="' + doc.id + '">Hapus</button>';
                    }
                    docsHtml += '</li>';
                }
                docsHtml += '</ul>';
            }

            var uploader = manage
                ? '<div id="dropzone" class="dropzone" style="border:2px dashed #b9c4d4;border-radius:8px;padding:18px;text-align:center;margin-top:10px;cursor:pointer">' +
                  '  Tarik & letakkan file PDF di sini, atau klik untuk memilih (boleh banyak).' +
                  '  <input id="file-input" type="file" accept="application/pdf" multiple style="display:none">' +
                  '</div>'
                : '';

            var body =
                '<div class="form-group"><strong>Jenis:</strong> ' + DomUtils.escape(JENIS_LABELS[d.jenis] || d.jenis) + '</div>' +
                '<div class="form-group"><strong>Tanggal:</strong> ' + DomUtils.escape(d.tanggal) +
                '  &nbsp; <strong>Lokasi:</strong> ' + DomUtils.escape(d.lokasi || "-") + '</div>' +
                '<div class="form-group"><strong>Peserta:</strong><br>' + DomUtils.escape(d.peserta || "-") + '</div>' +
                '<div class="form-group"><strong>Notulensi:</strong><br>' +
                '<div style="white-space:pre-wrap">' + DomUtils.escape(d.catatan || "-") + '</div></div>' +
                '<hr><div class="form-group"><strong>Dokumen (PDF):</strong>' + docsHtml + uploader + '</div>';

            var footer = '';
            if (manage) {
                footer += '<button class="btn btn-outline" id="ag-edit">Edit</button>';
                footer += '<button class="btn btn-danger" id="ag-delete">Hapus Agenda</button>';
            }
            footer += '<button class="btn btn-primary" id="ag-close">Tutup</button>';

            ModalComponent.open(d.judul, body, footer);

            document.getElementById("ag-close").addEventListener("click", ModalComponent.close);

            if (manage) {
                document.getElementById("ag-edit").addEventListener("click", function () {
                    ModalComponent.close();
                    _openForm(d);
                });
                document.getElementById("ag-delete").addEventListener("click", function () {
                    if (!confirm("Hapus agenda ini beserta seluruh dokumennya?")) return;
                    Api.del("/api/log-peninjauan/" + id).then(function () {
                        ToastComponent.success("Agenda dihapus.");
                        ModalComponent.close();
                        _loadList();
                    });
                });

                var delBtns = document.querySelectorAll("[data-deldoc]");
                for (var k = 0; k < delBtns.length; k++) {
                    delBtns[k].addEventListener("click", function () {
                        var docId = this.getAttribute("data-deldoc");
                        Api.del("/api/dokumen-bukti/" + docId).then(function () {
                            ToastComponent.success("Dokumen dihapus.");
                            _openDetail(id);
                        });
                    });
                }

                _wireUploader(id);
            }
        });
    }

    function _wireUploader(id) {
        var dz = document.getElementById("dropzone");
        var input = document.getElementById("file-input");
        if (!dz || !input) return;

        dz.addEventListener("click", function () { input.click(); });
        input.addEventListener("change", function () { _upload(id, input.files); });

        dz.addEventListener("dragover", function (e) { e.preventDefault(); dz.style.background = "#eef3fb"; });
        dz.addEventListener("dragleave", function () { dz.style.background = ""; });
        dz.addEventListener("drop", function (e) {
            e.preventDefault();
            dz.style.background = "";
            _upload(id, e.dataTransfer.files);
        });
    }

    function _upload(id, fileList) {
        if (!fileList || fileList.length === 0) return;
        var fd = new FormData();
        for (var i = 0; i < fileList.length; i++) {
            if (fileList[i].type === "application/pdf" || /\.pdf$/i.test(fileList[i].name)) {
                fd.append("files", fileList[i]);
            }
        }
        ToastComponent.success("Mengunggah...");
        fetch("/api/log-peninjauan/" + id + "/upload", {
            method: "POST",
            credentials: "same-origin",
            body: fd,
        }).then(function (r) { return r.json(); }).then(function (res) {
            if (res.status === "error") { ToastComponent.error(res.message); return; }
            var msg = (res.data && res.data.count ? res.data.count : 0) + " file terunggah.";
            if (res.data && res.data.skipped && res.data.skipped.length) {
                msg += " Dilewati: " + res.data.skipped.join(", ");
            }
            ToastComponent.success(msg);
            _openDetail(id);
        }).catch(function () {
            ToastComponent.error("Gagal mengunggah file.");
        });
    }

    return { init: init };

})();
