/**
 * Halaman Identitas Program Studi.
 * Tabel A Buku Panduan APTIKOM -- Format Isian Identitas.
 */
var IdentitasPage = (function () {

    var FIELDS = [
        { key: "universitas_nama",   label: "Nama Perguruan Tinggi", group: "universitas", field: "nama" },
        { key: "universitas_alamat", label: "Alamat",                group: "universitas", field: "alamat" },
        { key: "fakultas_nama",      label: "Fakultas",              group: "fakultas",    field: "nama" },
        { key: "nama",               label: "Program Studi",         group: "prodi",       field: "nama" },
        { key: "akreditasi",         label: "Peringkat Akreditasi",  group: "prodi",       field: "akreditasi" },
        { key: "jenjang",            label: "Jenjang Pendidikan",    group: "prodi",       field: "jenjang" },
        { key: "gelar_lulusan",      label: "Gelar Lulusan",         group: "prodi",       field: "gelar_lulusan" },
        { key: "visi",               label: "Visi Keilmuan",         group: "prodi",       field: "visi",  multiline: true },
        { key: "misi",               label: "Misi Program Studi",    group: "prodi",       field: "misi",  multiline: true },
        { key: "website",            label: "Website",               group: "prodi",       field: "website" },
        { key: "email",              label: "Email",                 group: "prodi",       field: "email" },
    ];

    var _data = {};

    function init() {
        var content = document.getElementById("page-content");
        content.innerHTML =
            '<div class="page-header">' +
            '  <h2 class="page-title">Identitas Program Studi</h2>' +
            '  <p class="page-desc">Format Isian Identitas (Tabel A) sesuai Buku Panduan APTIKOM</p>' +
            '</div>' +
            '<div class="card" id="identitas-card">' +
            '  <div class="card-body"><div class="loading-text">Memuat data...</div></div>' +
            '</div>';

        Api.get("/api/identitas-prodi").then(function (res) {
            _data = res.data || {};
            _renderForm();
        });
    }

    function _getValue(fieldDef) {
        var group = fieldDef.group;
        var field = fieldDef.field;
        var src = _data[group] || _data.prodi || {};
        return src[field] || "";
    }

    function _renderForm() {
        var card = document.getElementById("identitas-card");
        var html = '<div class="card-body">';
        html += '<div class="identitas-form">';

        for (var i = 0; i < FIELDS.length; i++) {
            var f = FIELDS[i];
            var val = DomUtils.escape(_getValue(f));
            html += '<div class="form-group">';
            html += '<label class="form-label">' + f.label + '</label>';
            if (f.multiline) {
                html += '<textarea class="form-textarea" id="field-' + f.key + '" rows="3">' + val + '</textarea>';
            } else {
                html += '<input class="form-input" id="field-' + f.key + '" type="text" value="' + val + '" />';
            }
            html += '</div>';
        }

        html += '</div>';
        html += '</div>';
        html += '<div class="card-footer">';
        html += '  <button class="btn btn-primary" id="btn-save-identitas">Simpan Perubahan</button>';
        html += '</div>';

        card.innerHTML = html;

        document.getElementById("btn-save-identitas").addEventListener("click", _save);
    }

    function _save() {
        var payload = {};
        for (var i = 0; i < FIELDS.length; i++) {
            var f = FIELDS[i];
            var el = document.getElementById("field-" + f.key);
            if (el) payload[f.key] = el.value;
        }

        Api.put("/api/identitas-prodi", payload).then(function (res) {
            if (res.status === "success") {
                ToastComponent.show("Identitas prodi berhasil disimpan", "success");
            }
        });
    }

    return { init: init };

})();
