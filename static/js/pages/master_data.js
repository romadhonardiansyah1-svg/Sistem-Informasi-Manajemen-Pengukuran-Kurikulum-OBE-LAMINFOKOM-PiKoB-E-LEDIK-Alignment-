/**
 * Halaman master data (PL, CPL, BK, MK, CPMK).
 * Satu handler generic untuk semua entitas.
 */
var MasterDataPage = (function () {

    var COLUMN_MAP = {
        "pl":   [{ key: "kode", label: "Kode" }, { key: "deskripsi", label: "Deskripsi" }, { key: "kategori", label: "Kategori" }],
        "cpl":  [{ key: "kode", label: "Kode" }, { key: "deskripsi", label: "Deskripsi" }],
        "bk":   [{ key: "kode", label: "Kode" }, { key: "nama", label: "Nama" }, { key: "kompetensi", label: "Kompetensi" }],
        "mk":   [{ key: "kode", label: "Kode" }, { key: "nama", label: "Nama" }, { key: "sks", label: "SKS" }, { key: "semester", label: "Semester" }, { key: "jenis", label: "Jenis" }],
        "cpmk": [{ key: "kode", label: "Kode" }, { key: "deskripsi", label: "Deskripsi" }],
    };

    var FORM_FIELDS_MAP = {
        "pl":   [{ key: "kode", label: "Kode", type: "text" }, { key: "deskripsi", label: "Deskripsi", type: "textarea" }, { key: "kategori", label: "Kategori", type: "text" }],
        "cpl":  [{ key: "kode", label: "Kode", type: "text" }, { key: "deskripsi", label: "Deskripsi", type: "textarea" }],
        "bk":   [{ key: "kode", label: "Kode", type: "text" }, { key: "nama", label: "Nama", type: "text" }, { key: "kompetensi", label: "Kompetensi", type: "text" }],
        "mk":   [{ key: "kode", label: "Kode", type: "text" }, { key: "nama", label: "Nama", type: "text" }, { key: "sks", label: "SKS", type: "number" }, { key: "semester", label: "Semester", type: "number" }, { key: "jenis", label: "Jenis", type: "text" }],
        "cpmk": [{ key: "kode", label: "Kode", type: "text" }, { key: "deskripsi", label: "Deskripsi", type: "textarea" }],
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
        Api.get(endpoint).then(function (res) {
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
            data.periode_id = 1;

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
