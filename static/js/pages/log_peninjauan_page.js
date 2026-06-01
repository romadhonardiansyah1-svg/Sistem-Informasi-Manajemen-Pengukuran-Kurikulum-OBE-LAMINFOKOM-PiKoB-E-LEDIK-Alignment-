/**
 * Halaman Log Peninjauan Kurikulum.
 * T-13.1b, T-13.2 Backlog Notion.
 * Drag-and-drop file uploader + list log rapat.
 */
var LogPeninjauanPage = (function () {

    var _selectedLogId = null;

    function init() {
        var content = document.getElementById("page-content");
        content.innerHTML =
            '<div class="page-header">' +
            '  <h2 class="page-title">Log Peninjauan Kurikulum</h2>' +
            '  <button class="btn btn-primary" id="btn-add-log">Tambah Log</button>' +
            '</div>' +
            '<div class="dash-row">' +
            '  <div class="dash-col-chart">' +
            '    <div class="card"><div class="card-header">Riwayat Peninjauan</div>' +
            '    <div class="card-body" id="log-list"></div></div>' +
            '  </div>' +
            '  <div class="dash-col-info">' +
            '    <div class="card"><div class="card-header">Detail dan Dokumen</div>' +
            '    <div class="card-body" id="log-detail">' +
            '      <div class="empty-state"><p>Pilih log untuk melihat detail</p></div>' +
            '    </div></div>' +
            '  </div>' +
            '</div>';

        document.getElementById("btn-add-log").addEventListener("click", _showCreateForm);
        _loadList();
    }

    function _loadList() {
        Api.get("/api/log-peninjauan").then(function (res) {
            var items = res.data || [];
            var container = document.getElementById("log-list");
            if (items.length === 0) {
                container.innerHTML = '<div class="empty-state"><p>Belum ada log peninjauan</p></div>';
                return;
            }
            var html = '';
            for (var i = 0; i < items.length; i++) {
                var item = items[i];
                var cls = _selectedLogId === item.id ? " active" : "";
                html += '<div class="sidebar-item log-item' + cls + '" data-id="' + item.id + '">';
                html += '<div><strong>' + DomUtils.escape(item.judul) + '</strong>';
                html += '<div class="log-meta"><span>' + DomUtils.escape(item.tanggal) + '</span>';
                html += '<span>' + item.dokumen_count + ' dokumen</span></div></div>';
                html += '</div>';
            }
            container.innerHTML = html;

            var logItems = container.querySelectorAll(".log-item");
            for (var j = 0; j < logItems.length; j++) {
                logItems[j].addEventListener("click", function () {
                    _selectedLogId = parseInt(this.dataset.id, 10);
                    _loadDetail(_selectedLogId);
                    _loadList();
                });
            }
        });
    }

    function _loadDetail(logId) {
        Api.get("/api/log-peninjauan/" + logId).then(function (res) {
            var item = res.data;
            var container = document.getElementById("log-detail");
            var html = '';
            html += '<h4>' + DomUtils.escape(item.judul) + '</h4>';
            html += '<div class="log-meta"><span>Tanggal: ' + DomUtils.escape(item.tanggal) + '</span>';
            html += '<span>Status: ' + DomUtils.escape(item.status) + '</span></div>';
            html += '<p style="margin-top:8px">' + DomUtils.escape(item.catatan || "Tidak ada catatan") + '</p>';
            html += '<p><strong>Peserta:</strong> ' + DomUtils.escape(item.peserta || "-") + '</p>';

            html += '<hr style="margin:16px 0">';
            html += '<h4>Dokumen Bukti Fisik</h4>';
            html += _buildDropZone(logId);

            var docs = item.dokumen || [];
            if (docs.length > 0) {
                html += '<div class="file-list">';
                for (var i = 0; i < docs.length; i++) {
                    html += '<div class="file-item">';
                    html += '<span class="file-item-name">' + DomUtils.escape(docs[i].filename) + '</span>';
                    html += '<button class="btn btn-sm btn-danger btn-del-doc" data-id="' + docs[i].id + '">Hapus</button>';
                    html += '</div>';
                }
                html += '</div>';
            }
            container.innerHTML = html;
            _initDropZone(logId);

            var delBtns = container.querySelectorAll(".btn-del-doc");
            for (var j = 0; j < delBtns.length; j++) {
                delBtns[j].addEventListener("click", function () {
                    var docId = this.dataset.id;
                    Api.del("/api/dokumen-bukti/" + docId).then(function () {
                        _loadDetail(logId);
                    });
                });
            }
        });
    }

    function _buildDropZone(logId) {
        return '<div class="drop-zone" id="drop-zone-' + logId + '">' +
            '<div class="drop-zone-text">Seret file PDF ke sini atau klik untuk memilih</div>' +
            '<div class="drop-zone-hint">Hanya file PDF yang diizinkan</div>' +
            '<input type="file" id="file-input-' + logId + '" multiple accept=".pdf" style="display:none" />' +
            '</div>';
    }

    function _initDropZone(logId) {
        var zone = document.getElementById("drop-zone-" + logId);
        var input = document.getElementById("file-input-" + logId);
        if (!zone || !input) return;

        zone.addEventListener("click", function () { input.click(); });

        zone.addEventListener("dragover", function (e) {
            e.preventDefault();
            zone.classList.add("drag-over");
        });

        zone.addEventListener("dragleave", function () {
            zone.classList.remove("drag-over");
        });

        zone.addEventListener("drop", function (e) {
            e.preventDefault();
            zone.classList.remove("drag-over");
            _uploadFiles(logId, e.dataTransfer.files);
        });

        input.addEventListener("change", function () {
            _uploadFiles(logId, this.files);
        });
    }

    function _uploadFiles(logId, fileList) {
        var formData = new FormData();
        for (var i = 0; i < fileList.length; i++) {
            formData.append("files", fileList[i]);
        }

        fetch("/api/log-peninjauan/" + logId + "/upload", {
            method: "POST",
            body: formData,
            credentials: "same-origin",
        })
        .then(function (r) { return r.json(); })
        .then(function (res) {
            if (res.status === "success") {
                ToastComponent.show(res.message, "success");
                _loadDetail(logId);
            }
        });
    }

    function _showCreateForm() {
        var footerHtml = '<button class="btn btn-primary" id="btn-save-log">Simpan</button>';
        ModalComponent.open("Tambah Log Peninjauan", _createFormHtml(), footerHtml);
        document.getElementById("btn-save-log").addEventListener("click", _saveLog);
    }

    function _createFormHtml() {
        return '<div class="form-group">' +
            '<label class="form-label">Judul</label>' +
            '<input class="form-input" id="log-judul" type="text" />' +
            '</div>' +
            '<div class="form-group">' +
            '<label class="form-label">Tanggal</label>' +
            '<input class="form-input" id="log-tanggal" type="date" />' +
            '</div>' +
            '<div class="form-group">' +
            '<label class="form-label">Peserta</label>' +
            '<textarea class="form-textarea" id="log-peserta" rows="2"></textarea>' +
            '</div>' +
            '<div class="form-group">' +
            '<label class="form-label">Catatan</label>' +
            '<textarea class="form-textarea" id="log-catatan" rows="3"></textarea>' +
            '</div>';
    }

    function _saveLog() {
        var payload = {
            judul: document.getElementById("log-judul").value,
            tanggal: document.getElementById("log-tanggal").value,
            peserta: document.getElementById("log-peserta").value,
            catatan: document.getElementById("log-catatan").value,
        };
        Api.post("/api/log-peninjauan", payload).then(function (res) {
            if (res.status === "success") {
                ModalComponent.close();
                ToastComponent.show("Log berhasil ditambahkan", "success");
                _loadList();
            }
        });
    }

    return { init: init };

})();
