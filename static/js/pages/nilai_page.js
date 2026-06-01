/**
 * Halaman Input Nilai Mahasiswa.
 * US-10: Menginput nilai mentah aktivitas kelas berdasarkan NIM.
 * Pilih MK terlebih dahulu, lalu input nilai per mahasiswa per CPMK.
 */
var NilaiPage = (function () {

    var _mkList = [];
    var _cpmkList = [];
    var _nilaiList = [];
    var _selectedMkId = null;

    function init() {
        var content = document.getElementById("page-content");
        content.innerHTML =
            '<div class="page-header">' +
            '  <div><h2 class="page-title">Input Nilai Mahasiswa</h2>' +
            '  <p class="page-desc">Evaluasi capaian pembelajaran per komponen penilaian</p></div>' +
            '</div>' +
            '<div class="card">' +
            '  <div class="card-body">' +
            '    <div class="form-group" style="max-width:400px">' +
            '      <label class="form-label">Pilih Mata Kuliah</label>' +
            '      <select class="form-input" id="nilai-mk-select">' +
            '        <option value="">-- Pilih MK --</option>' +
            '      </select>' +
            '    </div>' +
            '  </div>' +
            '</div>' +
            '<div id="nilai-container"></div>';

        _loadMk();
    }

    function _loadMk() {
        Promise.all([
            Api.get("/api/mk"),
            Api.get("/api/cpmk"),
        ]).then(function (res) {
            _mkList = res[0].data || [];
            _cpmkList = res[1].data || [];

            var select = document.getElementById("nilai-mk-select");
            for (var i = 0; i < _mkList.length; i++) {
                var opt = document.createElement("option");
                opt.value = _mkList[i].id;
                opt.textContent = _mkList[i].kode + " - " + _mkList[i].nama;
                select.appendChild(opt);
            }

            select.addEventListener("change", function () {
                _selectedMkId = this.value ? parseInt(this.value, 10) : null;
                if (_selectedMkId) {
                    _loadNilai(_selectedMkId);
                } else {
                    document.getElementById("nilai-container").innerHTML = "";
                }
            });
        });
    }

    function _loadNilai(mkId) {
        Api.get("/api/nilai?mk_id=" + mkId).then(function (res) {
            _nilaiList = res.data || [];
            _renderNilaiSection(mkId);
        });
    }

    function _getMkNama(mkId) {
        for (var i = 0; i < _mkList.length; i++) {
            if (_mkList[i].id === mkId) return _mkList[i].kode + " - " + _mkList[i].nama;
        }
        return "MK #" + mkId;
    }

    function _getCpmkForMk(mkId) {
        var result = [];
        for (var i = 0; i < _cpmkList.length; i++) {
            result.push(_cpmkList[i]);
        }
        return result;
    }

    function _renderNilaiSection(mkId) {
        var container = document.getElementById("nilai-container");
        var html = '';

        html += '<div class="card" style="margin-top:16px">';
        html += '<div class="card-header">';
        html += 'Nilai: ' + DomUtils.escape(_getMkNama(mkId));
        html += '<button class="btn btn-sm btn-primary" id="btn-add-nilai" style="float:right">Tambah Nilai</button>';
        html += '</div>';
        html += '<div class="card-body">';

        if (_nilaiList.length === 0) {
            html += '<div class="empty-state">';
            html += '<div class="empty-state-title">Belum ada data nilai untuk MK ini</div>';
            html += '<p>Klik "Tambah Nilai" untuk menginput nilai mahasiswa.</p>';
            html += '</div>';
        } else {
            html += '<table class="data-table">';
            html += '<thead><tr>';
            html += '<th>Mahasiswa ID</th><th>CPMK ID</th>';
            html += '<th>Partisipasi</th><th>Observasi</th><th>Unjuk Kerja</th>';
            html += '<th>UTS</th><th>UAS</th><th>Tes Lisan</th><th>Total</th>';
            html += '</tr></thead><tbody>';
            for (var i = 0; i < _nilaiList.length; i++) {
                var n = _nilaiList[i];
                html += '<tr>';
                html += '<td>' + n.mahasiswa_id + '</td>';
                html += '<td>' + n.cpmk_id + '</td>';
                html += '<td>' + (n.skor_partisipasi || 0) + '</td>';
                html += '<td>' + (n.skor_observasi || 0) + '</td>';
                html += '<td>' + (n.skor_unjuk_kerja || 0) + '</td>';
                html += '<td>' + (n.skor_uts || 0) + '</td>';
                html += '<td>' + (n.skor_uas || 0) + '</td>';
                html += '<td>' + (n.skor_tes_lisan || 0) + '</td>';
                html += '<td class="cell-code">' + (n.skor_total || 0) + '</td>';
                html += '</tr>';
            }
            html += '</tbody></table>';
        }

        html += '</div></div>';
        container.innerHTML = html;

        document.getElementById("btn-add-nilai").addEventListener("click", function () {
            _showInputForm(mkId);
        });
    }

    function _showInputForm(mkId) {
        var cpmkOptions = '';
        var cpmks = _getCpmkForMk(mkId);
        for (var i = 0; i < cpmks.length; i++) {
            cpmkOptions += '<option value="' + cpmks[i].id + '">';
            cpmkOptions += DomUtils.escape(cpmks[i].kode + " - " + (cpmks[i].deskripsi || "").substring(0, 50));
            cpmkOptions += '</option>';
        }

        var formHtml =
            '<div class="form-group">' +
            '<label class="form-label">Mahasiswa ID (NIM)</label>' +
            '<input class="form-input" id="inp-mhs-id" type="number" placeholder="1" />' +
            '</div>' +
            '<div class="form-group">' +
            '<label class="form-label">CPMK</label>' +
            '<select class="form-input" id="inp-cpmk">' + cpmkOptions + '</select>' +
            '</div>' +
            '<div class="identitas-form">' +
            '<div class="form-group">' +
            '<label class="form-label">Partisipasi</label>' +
            '<input class="form-input" id="inp-partisipasi" type="number" value="0" />' +
            '</div>' +
            '<div class="form-group">' +
            '<label class="form-label">Observasi</label>' +
            '<input class="form-input" id="inp-observasi" type="number" value="0" />' +
            '</div>' +
            '<div class="form-group">' +
            '<label class="form-label">Unjuk Kerja</label>' +
            '<input class="form-input" id="inp-unjuk" type="number" value="0" />' +
            '</div>' +
            '<div class="form-group">' +
            '<label class="form-label">UTS</label>' +
            '<input class="form-input" id="inp-uts" type="number" value="0" />' +
            '</div>' +
            '<div class="form-group">' +
            '<label class="form-label">UAS</label>' +
            '<input class="form-input" id="inp-uas" type="number" value="0" />' +
            '</div>' +
            '<div class="form-group">' +
            '<label class="form-label">Tes Lisan</label>' +
            '<input class="form-input" id="inp-lisan" type="number" value="0" />' +
            '</div>' +
            '</div>';

        var footerHtml = '<button class="btn btn-primary" id="btn-save-nilai">Simpan Nilai</button>';
        ModalComponent.open("Input Nilai Mahasiswa", formHtml, footerHtml);
        document.getElementById("btn-save-nilai").addEventListener("click", function () {
            _saveNilai(mkId);
        });
    }

    function _saveNilai(mkId) {
        var p = parseFloat(document.getElementById("inp-partisipasi").value) || 0;
        var o = parseFloat(document.getElementById("inp-observasi").value) || 0;
        var u = parseFloat(document.getElementById("inp-unjuk").value) || 0;
        var uts = parseFloat(document.getElementById("inp-uts").value) || 0;
        var uas = parseFloat(document.getElementById("inp-uas").value) || 0;
        var l = parseFloat(document.getElementById("inp-lisan").value) || 0;
        var total = p + o + u + uts + uas + l;

        var payload = {
            records: [{
                mahasiswa_id: parseInt(document.getElementById("inp-mhs-id").value, 10),
                mk_id: mkId,
                cpmk_id: parseInt(document.getElementById("inp-cpmk").value, 10),
                skor_partisipasi: p,
                skor_observasi: o,
                skor_unjuk_kerja: u,
                skor_uts: uts,
                skor_uas: uas,
                skor_tes_lisan: l,
                skor_total: total,
            }],
        };
        Api.post("/api/nilai", payload).then(function (res) {
            if (res.status === "success") {
                ModalComponent.close();
                ToastComponent.show("Nilai berhasil disimpan", "success");
                _loadNilai(mkId);
            }
        });
    }

    return { init: init };

})();
