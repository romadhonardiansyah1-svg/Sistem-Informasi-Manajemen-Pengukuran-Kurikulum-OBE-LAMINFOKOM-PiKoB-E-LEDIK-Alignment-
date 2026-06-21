/**
 * Halaman RPS (Rencana Pembelajaran Semester).
 * Input disesuaikan dengan template "Rancangan RPS" pada spreadsheet & buku pedoman:
 * identitas MK, bobot T/P, dosen pengampu & koordinator, pustaka, MK prasyarat,
 * deskripsi singkat, lalu tabel mingguan (Sub-CPMK, indikator, kriteria & teknik,
 * bentuk pembelajaran, materi, bobot). Output cetak mengikuti bentuk template.
 */
var RPSPage = (function () {

    var _mkList = [];
    var _rpsList = [];
    var _selectedRps = null;
    var _subCpmkMap = {};
    var _subCpmkList = [];

    function init() {
        var content = document.getElementById("page-content");
        content.innerHTML =
            '<div class="page-header">' +
            '  <h2 class="page-title">Rencana Pembelajaran Semester</h2>' +
            '  <p class="page-desc">Penyusunan dokumen RPS per mata kuliah sesuai template pedoman (16 minggu)</p>' +
            '</div>' +
            '<div class="dash-row">' +
            '  <div class="dash-col-chart">' +
            '    <div class="card"><div class="card-header">' +
            '      Daftar RPS' +
            '      <button class="btn btn-sm btn-primary" id="btn-add-rps" style="float:right">Buat RPS</button>' +
            '    </div>' +
            '    <div class="card-body" id="rps-list"></div></div>' +
            '  </div>' +
            '  <div class="dash-col-info">' +
            '    <div class="card"><div class="card-header">Detail RPS</div>' +
            '    <div class="card-body" id="rps-detail">' +
            '      <div class="empty-state"><p>Pilih RPS dari daftar untuk melihat & mengedit detail</p></div>' +
            '    </div></div>' +
            '  </div>' +
            '</div>';

        document.getElementById("btn-add-rps").addEventListener("click", function () {
            _showForm(null);
        });
        _loadData();
    }

    function _loadData() {
        Promise.all([
            Api.get("/api/mk"),
            Api.get("/api/rps"),
        ]).then(function (res) {
            _mkList = res[0].data || [];
            _rpsList = res[1].data || [];
            _renderList();
        });
    }

    function _getMkNama(mkId) {
        for (var i = 0; i < _mkList.length; i++) {
            if (_mkList[i].id === mkId) return _mkList[i].kode + " - " + _mkList[i].nama;
        }
        return "MK #" + mkId;
    }

    function _getMkObj(mkId) {
        for (var i = 0; i < _mkList.length; i++) {
            if (_mkList[i].id === mkId) return _mkList[i];
        }
        return null;
    }

    function _renderList() {
        var container = document.getElementById("rps-list");
        if (_rpsList.length === 0) {
            container.innerHTML =
                '<div class="empty-state">' +
                '  <div class="empty-state-title">Belum ada RPS</div>' +
                '  <p>Klik "Buat RPS" untuk membuat dokumen RPS baru per mata kuliah.</p>' +
                '</div>';
            return;
        }
        var html = '<table class="data-table compact">';
        html += '<thead><tr><th>Mata Kuliah</th><th>Kode Dokumen</th><th>Dosen</th><th></th></tr></thead>';
        html += '<tbody>';
        for (var i = 0; i < _rpsList.length; i++) {
            var r = _rpsList[i];
            html += '<tr>';
            html += '<td>' + DomUtils.escape(_getMkNama(r.mk_id)) + '</td>';
            html += '<td class="cell-code">' + DomUtils.escape(r.kode_dokumen || "-") + '</td>';
            html += '<td>' + DomUtils.escape(r.dosen_pengampu || "-") + '</td>';
            html += '<td><button class="btn btn-sm btn-outline btn-view-rps" data-id="' + r.id + '">Detail</button></td>';
            html += '</tr>';
        }
        html += '</tbody></table>';
        container.innerHTML = html;

        var btns = container.querySelectorAll(".btn-view-rps");
        for (var j = 0; j < btns.length; j++) {
            btns[j].addEventListener("click", function () {
                _loadDetail(parseInt(this.dataset.id, 10));
            });
        }
    }

    function _loadDetail(rpsId) {
        Api.get("/api/rps/" + rpsId).then(function (res) {
            _selectedRps = res.data;
            var mkId = _selectedRps.mk_id;
            // Ambil Sub-CPMK MK ini untuk dropdown & pemetaan kode pada tabel mingguan.
            Api.get("/api/sub-cpmk?mk_id=" + mkId).then(function (sres) {
                _subCpmkList = sres.data || [];
                _subCpmkMap = {};
                for (var i = 0; i < _subCpmkList.length; i++) {
                    _subCpmkMap[_subCpmkList[i].id] = _subCpmkList[i].kode;
                }
                _renderDetail();
            }, function () {
                _subCpmkList = [];
                _subCpmkMap = {};
                _renderDetail();
            });
        });
    }

    function _renderDetail() {
        var container = document.getElementById("rps-detail");
        var r = _selectedRps;
        if (!r) return;
        var esc = DomUtils.escape;

        var html = '';
        html += '<div class="rps-header-info">';
        html += '<h4>' + esc(_getMkNama(r.mk_id)) + '</h4>';
        html += '<div class="log-meta">';
        html += '<span>Kode: ' + esc(r.kode_dokumen || "-") + '</span>';
        html += '<span>Dosen: ' + esc(r.dosen_pengampu || "-") + '</span>';
        html += '<span>Bobot: T' + (r.bobot_teori_sks || 0) + '/P' + (r.bobot_praktikum_sks || 0) + '</span>';
        html += '</div>';
        if (r.deskripsi_singkat) {
            html += '<p style="margin-top:8px">' + esc(r.deskripsi_singkat) + '</p>';
        }
        html += '<div style="margin-top:8px">' +
                '<button class="btn btn-sm btn-outline" id="btn-edit-rps">✎ Edit Header</button></div>';
        html += '</div>';

        html += '<hr style="margin:12px 0">';
        html += '<h4>Rincian Mingguan</h4>';

        var minggu = r.minggu || [];
        if (minggu.length === 0) {
            html += '<div class="empty-state"><p>Belum ada data mingguan.</p></div>';
            html += '<button class="btn btn-primary" id="btn-gen-minggu">Generate 16 Minggu</button>';
        } else {
            html += _buildWeeklyEditor(minggu);
            html += '<div style="margin-top:12px;display:flex;gap:8px;justify-content:flex-end">' +
                    '<button class="btn btn-sm btn-primary" id="btn-save-minggu">💾 Simpan Mingguan</button>' +
                    '<button class="btn btn-sm btn-outline" id="btn-print-rps">🖨️ Cetak / Print</button></div>';
        }

        container.innerHTML = html;

        var editBtn = document.getElementById("btn-edit-rps");
        if (editBtn) editBtn.addEventListener("click", function () { _showForm(r); });

        var genBtn = document.getElementById("btn-gen-minggu");
        if (genBtn) genBtn.addEventListener("click", function () { _generateMinggu(r.id); });

        var saveBtn = document.getElementById("btn-save-minggu");
        if (saveBtn) saveBtn.addEventListener("click", function () { _saveMinggu(r.id); });

        var printBtn = document.getElementById("btn-print-rps");
        if (printBtn) printBtn.addEventListener("click", function () { _buildPrintArea(); window.print(); });
    }

    // Tabel mingguan yang bisa diedit langsung (sesuai kolom template RPS).
    function _buildWeeklyEditor(minggu) {
        var esc = DomUtils.escape;
        var html = '<div class="rps-weekly-edit" style="overflow-x:auto">';
        html += '<table class="data-table compact"><thead><tr>' +
                '<th>Mg</th><th>Sub-CPMK</th><th>Materi</th><th>Bentuk &amp; Metode</th>' +
                '<th>Indikator</th><th>Kriteria &amp; Teknik</th><th>Bobot %</th>' +
                '</tr></thead><tbody>';
        for (var i = 0; i < minggu.length; i++) {
            var m = minggu[i];
            var label = m.minggu_ke === 8 ? " (UTS)" : m.minggu_ke === 16 ? " (UAS)" : "";
            html += '<tr data-minggu="' + m.minggu_ke + '">';
            html += '<td class="cell-code" style="white-space:nowrap">' + m.minggu_ke + label + '</td>';
            html += '<td><select class="form-input form-input-sm rps-w-sub">' + _subCpmkOptions(m.sub_cpmk_id) + '</select></td>';
            html += '<td><textarea class="form-textarea rps-w-materi" rows="2">' + esc(m.materi || "") + '</textarea></td>';
            html += '<td><textarea class="form-textarea rps-w-bentuk" rows="2">' + esc(m.bentuk_pembelajaran || "") + '</textarea></td>';
            html += '<td><textarea class="form-textarea rps-w-indikator" rows="2">' + esc(m.indikator || "") + '</textarea></td>';
            html += '<td><textarea class="form-textarea rps-w-kriteria" rows="2">' + esc(m.kriteria_teknik || "") + '</textarea></td>';
            html += '<td><input type="number" step="0.01" class="form-input form-input-sm rps-w-bobot" value="' + (m.bobot_penilaian_persen || 0) + '" style="width:64px"></td>';
            html += '</tr>';
        }
        html += '</tbody></table></div>';
        return html;
    }

    function _subCpmkOptions(selectedId) {
        var opt = '<option value="">—</option>';
        for (var i = 0; i < _subCpmkList.length; i++) {
            var s = _subCpmkList[i];
            var sel = (s.id === selectedId) ? " selected" : "";
            opt += '<option value="' + s.id + '"' + sel + '>' + DomUtils.escape(s.kode) + '</option>';
        }
        return opt;
    }

    function _saveMinggu(rpsId) {
        var rows = document.querySelectorAll(".rps-weekly-edit tbody tr");
        var mingguData = [];
        for (var i = 0; i < rows.length; i++) {
            var tr = rows[i];
            var subVal = tr.querySelector(".rps-w-sub").value;
            mingguData.push({
                minggu_ke: parseInt(tr.dataset.minggu, 10),
                sub_cpmk_id: subVal ? parseInt(subVal, 10) : null,
                materi: tr.querySelector(".rps-w-materi").value,
                bentuk_pembelajaran: tr.querySelector(".rps-w-bentuk").value,
                indikator: tr.querySelector(".rps-w-indikator").value,
                kriteria_teknik: tr.querySelector(".rps-w-kriteria").value,
                bobot_penilaian_persen: parseFloat(tr.querySelector(".rps-w-bobot").value) || 0,
            });
        }
        Api.put("/api/rps/" + rpsId + "/minggu", { minggu: mingguData }).then(function (res) {
            if (res && res.status === "success") {
                ToastComponent.show("Rincian mingguan tersimpan", "success");
                _loadDetail(rpsId);
            } else {
                ToastComponent.show((res && res.message) || "Gagal menyimpan (periode mungkin terkunci)", "error");
            }
        });
    }

    function _generateMinggu(rpsId) {
        var mingguData = [];
        for (var i = 1; i <= 16; i++) {
            var label = i === 8 ? "Ujian Tengah Semester" : i === 16 ? "Ujian Akhir Semester" : "Pertemuan " + i;
            mingguData.push({
                minggu_ke: i,
                materi: label,
                bentuk_pembelajaran: i === 8 || i === 16 ? "Ujian" : "Ceramah, Diskusi",
                bobot_penilaian_persen: i === 8 ? 30 : i === 16 ? 40 : 2.14,
            });
        }
        Api.put("/api/rps/" + rpsId + "/minggu", { minggu: mingguData }).then(function (res) {
            if (res && res.status === "success") {
                ToastComponent.show("16 minggu di-generate, silakan diedit", "success");
                _loadDetail(rpsId);
            } else {
                ToastComponent.show((res && res.message) || "Gagal (periode mungkin terkunci)", "error");
            }
        });
    }

    // Form input/edit header RPS — field mengikuti template Rancangan RPS.
    function _showForm(existing) {
        var isEdit = !!existing;
        var e = existing || {};

        var mkSelect;
        if (isEdit) {
            mkSelect = '<input class="form-input" value="' + DomUtils.escape(_getMkNama(e.mk_id)) + '" disabled />';
        } else {
            var mkOptions = '';
            for (var i = 0; i < _mkList.length; i++) {
                mkOptions += '<option value="' + _mkList[i].id + '">' +
                    DomUtils.escape(_mkList[i].kode + " - " + _mkList[i].nama) + '</option>';
            }
            mkSelect = '<select class="form-input" id="rps-mk">' + mkOptions + '</select>';
        }

        function field(label, id, type, val, ph) {
            var v = (val === undefined || val === null) ? "" : String(val);
            var input = (type === "textarea")
                ? '<textarea class="form-textarea" id="' + id + '" rows="2">' + DomUtils.escape(v) + '</textarea>'
                : '<input class="form-input" id="' + id + '" type="' + (type || "text") + '" value="' + DomUtils.escape(v) + '"' +
                  (ph ? ' placeholder="' + ph + '"' : '') + ' />';
            return '<div class="form-group"><label class="form-label">' + label + '</label>' + input + '</div>';
        }

        var formHtml = '';
        formHtml += '<div class="form-group"><label class="form-label">Mata Kuliah</label>' + mkSelect + '</div>';
        formHtml += '<div class="grid-2">';
        formHtml += field("Kode Dokumen", "rps-kode", "text", e.kode_dokumen, "RPS-SI-001");
        formHtml += field("Tanggal Penyusunan", "rps-tanggal", "text", e.tanggal_penyusunan, "DD-MM-YYYY");
        formHtml += field("Dosen Pengampu", "rps-dosen", "text", e.dosen_pengampu);
        formHtml += field("Koordinator / Pengembang", "rps-koor", "text", e.dosen_koordinator);
        formHtml += field("Bobot SKS Teori", "rps-teori", "number", e.bobot_teori_sks || 0);
        formHtml += field("Bobot SKS Praktikum", "rps-praktikum", "number", e.bobot_praktikum_sks || 0);
        formHtml += '</div>';
        formHtml += field("MK Prasyarat", "rps-prasyarat", "text", e.mk_prasyarat);
        formHtml += field("Deskripsi Singkat MK", "rps-desc", "textarea", e.deskripsi_singkat);
        formHtml += field("Pustaka Utama", "rps-pustaka-utama", "textarea", e.pustaka_utama);
        formHtml += field("Pustaka Pendukung", "rps-pustaka-pendukung", "textarea", e.pustaka_pendukung);

        var footerHtml = '<button class="btn btn-primary" id="btn-save-rps">Simpan</button>';
        ModalComponent.open(isEdit ? "Edit RPS" : "Buat RPS Baru", formHtml, footerHtml);
        document.getElementById("btn-save-rps").addEventListener("click", function () {
            _saveForm(existing);
        });
    }

    function _saveForm(existing) {
        function val(id) { var el = document.getElementById(id); return el ? el.value : ""; }
        var periodeId = AppState.currentPeriode ? AppState.currentPeriode.id : 1;

        var payload = {
            kode_dokumen: val("rps-kode"),
            tanggal_penyusunan: val("rps-tanggal"),
            dosen_pengampu: val("rps-dosen"),
            dosen_koordinator: val("rps-koor"),
            bobot_teori_sks: parseInt(val("rps-teori"), 10) || 0,
            bobot_praktikum_sks: parseInt(val("rps-praktikum"), 10) || 0,
            mk_prasyarat: val("rps-prasyarat"),
            deskripsi_singkat: val("rps-desc"),
            pustaka_utama: val("rps-pustaka-utama"),
            pustaka_pendukung: val("rps-pustaka-pendukung"),
        };

        var req;
        if (existing) {
            req = Api.put("/api/rps/" + existing.id, payload);
        } else {
            payload.mk_id = parseInt(val("rps-mk"), 10);
            payload.periode_id = periodeId;
            req = Api.post("/api/rps", payload);
        }

        req.then(function (res) {
            if (res && (res.status === "success" || res.status === "created")) {
                ModalComponent.close();
                ToastComponent.show(existing ? "RPS diperbarui" : "RPS berhasil dibuat", "success");
                _loadData();
                if (existing) _loadDetail(existing.id);
            } else {
                ToastComponent.show((res && res.message) || "Gagal menyimpan (periode mungkin terkunci)", "error");
            }
        });
    }

    function _buildPrintArea() {
        var r = _selectedRps;
        if (!r) return;
        var mk = _getMkObj(r.mk_id) || {};
        var esc = DomUtils.escape;

        var area = document.getElementById("rps-print-area");
        if (!area) {
            area = document.createElement("div");
            area.id = "rps-print-area";
            document.getElementById("page-content").appendChild(area);
        }

        var sksTotal = mk.sks || ((r.bobot_teori_sks || 0) + (r.bobot_praktikum_sks || 0));
        var html = '';
        html += '<div class="rps-doc-title">Rencana Pembelajaran Semester (RPS)</div>';
        html += '<div class="rps-doc-subtitle">Program Studi Sistem Informasi</div>';

        html += '<table class="rps-identitas">';
        html += '<tr><td class="lbl">Mata Kuliah</td><td>' + esc(mk.nama || "-") + '</td>' +
                '<td class="lbl">Kode MK</td><td>' + esc(mk.kode || "-") + '</td></tr>';
        html += '<tr><td class="lbl">Bobot SKS</td><td>' + sksTotal +
                ' (T:' + (r.bobot_teori_sks || 0) + ' / P:' + (r.bobot_praktikum_sks || 0) + ')</td>' +
                '<td class="lbl">Semester</td><td>' + esc(String(mk.semester || "-")) + '</td></tr>';
        html += '<tr><td class="lbl">Kode Dokumen</td><td>' + esc(r.kode_dokumen || "-") + '</td>' +
                '<td class="lbl">Tanggal Penyusunan</td><td>' + esc(r.tanggal_penyusunan || "-") + '</td></tr>';
        html += '<tr><td class="lbl">Dosen Pengampu</td><td>' + esc(r.dosen_pengampu || "-") + '</td>' +
                '<td class="lbl">Koordinator</td><td>' + esc(r.dosen_koordinator || "-") + '</td></tr>';
        html += '<tr><td class="lbl">MK Prasyarat</td><td colspan="3">' + esc(r.mk_prasyarat || mk.prasyarat || "-") + '</td></tr>';
        html += '</table>';

        html += '<div class="rps-section-title">Deskripsi Singkat Mata Kuliah</div>';
        html += '<div>' + esc(r.deskripsi_singkat || mk.deskripsi_singkat || "-") + '</div>';

        if (r.media_software || r.media_hardware) {
            html += '<div class="rps-section-title">Media Pembelajaran</div>';
            html += '<div>Perangkat lunak: ' + esc(r.media_software || "-") +
                    ' &nbsp;|&nbsp; Perangkat keras: ' + esc(r.media_hardware || "-") + '</div>';
        }

        html += '<div class="rps-section-title">Rencana Pembelajaran Mingguan</div>';
        var minggu = r.minggu || [];
        html += '<table class="rps-weekly">';
        html += '<thead><tr>' +
                '<th>Mg</th><th>Sub-CPMK</th><th>Materi / Bahan Kajian</th>' +
                '<th>Bentuk &amp; Metode Pembelajaran</th><th>Indikator</th><th>Kriteria &amp; Teknik</th><th>Bobot (%)</th>' +
                '</tr></thead><tbody>';
        for (var i = 0; i < minggu.length; i++) {
            var m = minggu[i];
            var label = m.minggu_ke === 8 ? " (UTS)" : m.minggu_ke === 16 ? " (UAS)" : "";
            var subKode = m.sub_cpmk_id ? (_subCpmkMap[m.sub_cpmk_id] || ("Sub-" + m.sub_cpmk_id)) : "-";
            var bentuk = m.bentuk_pembelajaran || "-";
            if (m.metode_luring) bentuk += " (Luring: " + m.metode_luring + ")";
            if (m.metode_daring) bentuk += " (Daring: " + m.metode_daring + ")";
            html += '<tr>';
            html += '<td class="c">' + m.minggu_ke + label + '</td>';
            html += '<td>' + esc(subKode) + '</td>';
            html += '<td>' + esc(m.materi || "-") + '</td>';
            html += '<td>' + esc(bentuk) + '</td>';
            html += '<td>' + esc(m.indikator || "-") + '</td>';
            html += '<td>' + esc(m.kriteria_teknik || "-") + '</td>';
            html += '<td class="c">' + (m.bobot_penilaian_persen || 0) + '</td>';
            html += '</tr>';
        }
        html += '</tbody></table>';

        html += '<div class="rps-pustaka">';
        html += '<div class="rps-section-title">Pustaka</div>';
        html += '<div><strong>Utama:</strong> ' + esc(r.pustaka_utama || "-") + '</div>';
        html += '<div><strong>Pendukung:</strong> ' + esc(r.pustaka_pendukung || "-") + '</div>';
        html += '</div>';

        area.innerHTML = html;
    }

    return { init: init };

})();
