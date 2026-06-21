/**
 * Halaman master data (PL, CPL, BK, MK, CPMK).
 * Satu handler generic untuk semua entitas.
 */
var MasterDataPage = (function () {

    // Tiga kolom referutan sumber yang melekat di tiap data master (MODUL 1).
    var REF_COLUMNS = [
        { key: "ref_buku",        label: "Ref. Buku",   className: "cell-ref" },
        { key: "ref_spreadsheet", label: "Ref. Sheet",  className: "cell-ref" },
        { key: "ref_pikobe",      label: "Ref. PIKOBE", className: "cell-ref" },
    ];

    // Tiga input referensi sumber untuk form (dipakai semua entitas).
    var REF_FIELDS = [
        { key: "ref_buku",        label: "Referensi Buku Panduan (mis. Tabel 1, hal 15)", type: "text" },
        { key: "ref_spreadsheet", label: "Referensi Spreadsheet Rancangan (sheet)", type: "text" },
        { key: "ref_pikobe",      label: "Referensi PIKOBE (ledik/tabel no.)", type: "text" },
    ];

    function _withRefColumns(cols) {
        return cols.concat(REF_COLUMNS);
    }

    function _withRefFields(fields) {
        return fields.concat(REF_FIELDS);
    }

    var COLUMN_MAP = {
        "pl":   _withRefColumns([{ key: "kode", label: "Kode" }, { key: "deskripsi", label: "Deskripsi", className: "cell-desc" }, { key: "kategori", label: "Kategori" }]),
        "cpl":  _withRefColumns([{ key: "kode", label: "Kode" }, { key: "deskripsi", label: "Deskripsi", className: "cell-desc" }]),
        "bk":   _withRefColumns([{ key: "kode", label: "Kode" }, { key: "nama", label: "Nama" }, { key: "kompetensi", label: "Kompetensi" }]),
        "mk":   _withRefColumns([{ key: "kode", label: "Kode" }, { key: "nama", label: "Nama" }, { key: "sks", label: "SKS" }, { key: "semester", label: "Semester" }, { key: "jenis", label: "Jenis" }]),
        "cpmk": _withRefColumns([{ key: "kode", label: "Kode" }, { key: "deskripsi", label: "Deskripsi", className: "cell-desc" }]),
    };

    var FORM_FIELDS_MAP = {
        "pl":   _withRefFields([{ key: "kode", label: "Kode", type: "text" }, { key: "deskripsi", label: "Deskripsi", type: "textarea" }, { key: "kategori", label: "Kategori", type: "remote-select", endpoint: "/api/kategori-pl", valueKey: "nama" }]),
        "cpl":  _withRefFields([{ key: "kode", label: "Kode", type: "text" }, { key: "deskripsi", label: "Deskripsi", type: "textarea" }]),
        "bk":   _withRefFields([{ key: "kode", label: "Kode", type: "text" }, { key: "nama", label: "Nama", type: "text" }, { key: "kompetensi", label: "Kompetensi", type: "text" }]),
        "mk":   _withRefFields([{ key: "kode", label: "Kode", type: "text" }, { key: "nama", label: "Nama", type: "text" }, { key: "sks", label: "SKS", type: "number" }, { key: "semester", label: "Semester", type: "number" }, { key: "jenis", label: "Jenis", type: "remote-select", endpoint: "/api/jenis-mk", valueKey: "nama" }]),
        "cpmk": _withRefFields([{ key: "kode", label: "Kode", type: "text" }, { key: "deskripsi", label: "Deskripsi", type: "textarea" }]),
    };

    function init(entry) {
        var entity = entry.entity;
        var endpoint = entry.endpoint;
        var content = document.getElementById("page-content");

        content.innerHTML =
            '<div class="page-header">' +
            '  <h2 class="page-title">' + entry.title + '</h2>' +
            '  <button class="btn btn-primary" id="btn-add">Tambah</button>' +
            '</div>' +
            '<div id="table-container"></div>';

        _loadData(entity, endpoint);

        document.getElementById("btn-add").addEventListener("click", function () {
            _showForm(entity, endpoint, null);
        });
    }

    function _loadData(entity, endpoint) {
        // Filter sesuai periode aktif agar ganti periode benar-benar mengubah data.
        var pid = (AppState.currentPeriode && AppState.currentPeriode.id) || null;
        var url = endpoint + (pid ? ("?periode_id=" + pid) : "");
        Api.get(url).then(function (res) {
            var columns = COLUMN_MAP[entity] || [];
            var rows = res.data || [];

            var tableEl = TableComponent.render("table-container", columns, rows, [
                { label: "Edit",  btnClass: "btn-outline", handler: function (e) {
                    var id = e.target.dataset.id;
                    var row = rows.find(function (r) { return String(r.id) === id; });
                    _showForm(entity, endpoint, row);
                }},
                { label: "Hapus", btnClass: "btn-danger",  handler: function (e) {
                    var id = e.target.dataset.id;
                    _deleteRecord(entity, endpoint, id);
                }},
            ]);

            var container = document.getElementById("table-container");
            container.innerHTML = "";
            container.appendChild(tableEl);
        });
    }

    function _showForm(entity, endpoint, existing) {
        var fields = FORM_FIELDS_MAP[entity] || [];
        var form = FormBuilder.build(fields, existing);
        var isEdit = existing !== null && existing !== undefined;
        var title = isEdit ? "Edit " + entity.toUpperCase() : "Tambah " + entity.toUpperCase();

        var footer =
            '<button class="btn btn-outline" onclick="ModalComponent.close()">Batal</button>' +
            '<button class="btn btn-primary" id="btn-save-form">Simpan</button>';

        ModalComponent.open(title, "", footer);
        document.getElementById("modal-body").appendChild(form);

        document.getElementById("btn-save-form").addEventListener("click", function () {
            var data = FormBuilder.getValues(form);
            data.periode_id = (AppState.currentPeriode && AppState.currentPeriode.id) || 1;

            if (isEdit) {
                Api.put(endpoint + "/" + existing.id, data).then(function (res) {
                    ModalComponent.close();
                    ToastComponent.success("Data diperbarui");
                    _loadData(entity, endpoint);
                });
            } else {
                Api.post(endpoint, data).then(function (res) {
                    ModalComponent.close();
                    ToastComponent.success("Data ditambahkan");
                    _loadData(entity, endpoint);
                });
            }
        });
    }

    function _deleteRecord(entity, endpoint, id) {
        Api.del(endpoint + "/" + id).then(function () {
            ToastComponent.success("Data dihapus");
            _loadData(entity, endpoint);
        });
    }

    return { init: init };

})();
