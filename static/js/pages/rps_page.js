/**
 * Halaman RPS (Rencana Pembelajaran Semester).
 * US-09: Menyusun RPS digital mengaitkan Sub-CPMK dan CPMK per minggu.
 * Menampilkan daftar MK, form buat RPS, dan detail mingguan.
 */
var RPSPage = (function () {

    var _mkList = [];
    var _rpsList = [];
    var _selectedRps = null;

    function init() {
        var content = document.getElementById("page-content");
        content.innerHTML =
            '<div class="page-header">' +
            '  <h2 class="page-title">Rencana Pembelajaran Semester</h2>' +
            '  <p class="page-desc">Penyusunan dokumen RPS per mata kuliah (16 minggu)</p>' +
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
            '      <div class="empty-state"><p>Pilih RPS dari daftar untuk melihat detail mingguan</p></div>' +
            '    </div></div>' +
            '  </div>' +
            '</div>';

        document.getElementById("btn-add-rps").addEventListener("click", _showCreateForm);
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
            _renderDetail();
        });
    }

    function _renderDetail() {
        var container = document.getElementById("rps-detail");
        var r = _selectedRps;
        if (!r) return;

        var html = '';
        html += '<div class="rps-header-info">';
        html += '<h4>' + DomUtils.escape(_getMkNama(r.mk_id)) + '</h4>';
        html += '<div class="log-meta">';
        html += '<span>Kode: ' + DomUtils.escape(r.kode_dokumen || "-") + '</span>';
        html += '<span>Dosen: ' + DomUtils.escape(r.dosen_pengampu || "-") + '</span>';
        html += '</div>';
        if (r.deskripsi_singkat) {
            html += '<p style="margin-top:8px">' + DomUtils.escape(r.deskripsi_singkat) + '</p>';
        }
        html += '</div>';

        html += '<hr style="margin:12px 0">';
        html += '<h4>Rincian Mingguan</h4>';

        var minggu = r.minggu || [];
        if (minggu.length === 0) {
            html += '<div class="empty-state"><p>Belum ada data mingguan. Gunakan tombol di bawah untuk generate 16 minggu.</p></div>';
            html += '<button class="btn btn-primary" id="btn-gen-minggu">Generate 16 Minggu</button>';
        } else {
            html += '<table class="data-table compact">';
            html += '<thead><tr><th>Mg</th><th>Materi</th><th>Bentuk</th><th>Bobot (%)</th></tr></thead>';
            html += '<tbody>';
            for (var i = 0; i < minggu.length; i++) {
                var m = minggu[i];
                var label = m.minggu_ke === 8 ? "UTS" : m.minggu_ke === 16 ? "UAS" : "";
                html += '<tr>';
                html += '<td class="cell-code">' + m.minggu_ke + (label ? " (" + label + ")" : "") + '</td>';
                html += '<td>' + DomUtils.escape(m.materi || "-") + '</td>';
                html += '<td>' + DomUtils.escape(m.bentuk_pembelajaran || "-") + '</td>';
                html += '<td>' + (m.bobot_penilaian_persen || 0) + '</td>';
                html += '</tr>';
            }
            html += '</tbody></table>';
            html += '<div style="margin-top:12px;text-align:right"><button class="btn btn-sm btn-outline" id="btn-print-rps">🖨️ Cetak / Print</button></div>';
        }

        container.innerHTML = html;

        var genBtn = document.getElementById("btn-gen-minggu");
        if (genBtn) {
            genBtn.addEventListener("click", function () {
                _generateMinggu(r.id);
            });
        }

        var printBtn = document.getElementById("btn-print-rps");
        if (printBtn) {
            printBtn.addEventListener("click", function () {
                window.print();
            });
        }
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
        Api.put("/api/rps/" + rpsId + "/minggu", { minggu: mingguData }).then(function () {
            ToastComponent.show("16 minggu berhasil di-generate", "success");
            _loadDetail(rpsId);
        });
    }

    function _showCreateForm() {
        var mkOptions = '';
        for (var i = 0; i < _mkList.length; i++) {
            mkOptions += '<option value="' + _mkList[i].id + '">';
            mkOptions += DomUtils.escape(_mkList[i].kode + " - " + _mkList[i].nama);
            mkOptions += '</option>';
        }

        var formHtml =
            '<div class="form-group">' +
            '<label class="form-label">Mata Kuliah</label>' +
            '<select class="form-input" id="rps-mk">' + mkOptions + '</select>' +
            '</div>' +
            '<div class="form-group">' +
            '<label class="form-label">Kode Dokumen</label>' +
            '<input class="form-input" id="rps-kode" type="text" placeholder="RPS-SI-001" />' +
            '</div>' +
            '<div class="form-group">' +
            '<label class="form-label">Dosen Pengampu</label>' +
            '<input class="form-input" id="rps-dosen" type="text" />' +
            '</div>' +
            '<div class="form-group">' +
            '<label class="form-label">Deskripsi Singkat</label>' +
            '<textarea class="form-textarea" id="rps-desc" rows="2"></textarea>' +
            '</div>';

        var footerHtml = '<button class="btn btn-primary" id="btn-save-rps">Simpan</button>';
        ModalComponent.open("Buat RPS Baru", formHtml, footerHtml);
        document.getElementById("btn-save-rps").addEventListener("click", _saveRps);
    }

    function _saveRps() {
        var periodeId = AppState.currentPeriode ? AppState.currentPeriode.id : 1;
        var payload = {
            mk_id: parseInt(document.getElementById("rps-mk").value, 10),
            periode_id: periodeId,
            kode_dokumen: document.getElementById("rps-kode").value,
            dosen_pengampu: document.getElementById("rps-dosen").value,
            deskripsi_singkat: document.getElementById("rps-desc").value,
        };
        Api.post("/api/rps", payload).then(function (res) {
            if (res.status === "success") {
                ModalComponent.close();
                ToastComponent.show("RPS berhasil dibuat", "success");
                _loadData();
            }
        });
    }

    return { init: init };

})();
