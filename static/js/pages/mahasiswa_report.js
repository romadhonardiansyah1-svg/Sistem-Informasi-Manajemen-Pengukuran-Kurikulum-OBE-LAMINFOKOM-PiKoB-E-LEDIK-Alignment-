/**
 * Halaman "Laporan Capaian Saya" untuk role mahasiswa.
 * Menampilkan ketercapaian CPL pribadi (radar + tabel) dan tombol unduh PDF.
 * Data di-scope otomatis ke mahasiswa yang login (endpoint /api/report/cpl/saya).
 */
var MahasiswaReportPage = (function () {

    function init() {
        var content = document.getElementById("page-content");
        content.innerHTML =
            '<div class="page-header">' +
            '  <div><h2 class="page-title">Laporan Capaian Pembelajaran Saya</h2>' +
            '  <p class="page-desc" id="mhs-identitas">Memuat data...</p></div>' +
            '  <button class="btn btn-primary btn-lg" id="btn-export-pdf">Unduh PDF</button>' +
            '</div>' +
            '<div id="mhs-report-body"></div>';

        document.getElementById("btn-export-pdf").addEventListener("click", function () {
            window.print();
        });

        _loadReport();
    }

    function _loadReport() {
        Api.get("/api/report/cpl/saya").then(function (res) {
            if (res.status !== "success" || !res.data) {
                _renderEmpty(res.message || "Data tidak tersedia.");
                return;
            }
            _render(res.data);
        }).catch(function () {
            _renderEmpty("Gagal memuat laporan.");
        });
    }

    function _render(data) {
        var mhs = data.mahasiswa || {};
        document.getElementById("mhs-identitas").textContent =
            (mhs.nama || "-") + "  •  NIM " + (mhs.nim || "-") + "  •  Angkatan " + (mhs.angkatan || "-");

        var items = data.spider_chart || [];
        var ringkasan = data.ringkasan || {};

        if (items.length === 0) {
            _renderEmpty("Belum ada CPL yang terdaftar untuk periode ini.");
            return;
        }

        var hasNilai = items.some(function (it) { return it.value > 0; });

        var body = document.getElementById("mhs-report-body");
        body.innerHTML =
            '<div class="dash-stats-grid" id="mhs-summary"></div>' +
            '<div class="dash-row">' +
            '  <div class="dash-col-chart">' +
            '    <div class="card">' +
            '      <div class="card-header">Diagram Radar Ketercapaian CPL</div>' +
            '      <div class="card-body"><div class="spider-chart-container">' +
            '        <canvas id="mhs-spider" class="spider-chart-canvas" width="500" height="500"></canvas>' +
            '      </div></div>' +
            '    </div>' +
            '  </div>' +
            '  <div class="dash-col-info">' +
            '    <div class="card">' +
            '      <div class="card-header">Rincian Ketercapaian per CPL</div>' +
            '      <div class="card-body" id="mhs-cpl-table"></div>' +
            '    </div>' +
            '  </div>' +
            '</div>';

        _renderSummary(ringkasan);
        SpiderChart.draw("mhs-spider", items, 100);
        _renderTable(items);

        if (!hasNilai) {
            var note = document.createElement("p");
            note.className = "dash-more";
            note.textContent = "Catatan: nilai aktivitas kelas Anda belum diinput dosen, sehingga capaian masih 0.";
            body.appendChild(note);
        }
    }

    function _renderSummary(r) {
        var container = document.getElementById("mhs-summary");
        var items = [
            { label: "Rata-rata Capaian", value: (r.rata_rata != null ? r.rata_rata : 0), color: "stat-blue" },
            { label: "CPL Tercapai", value: (r.jumlah_lulus || 0) + " / " + (r.jumlah_cpl || 0), color: "stat-green" },
            { label: "Persentase Tercapai", value: (r.persen_lulus != null ? r.persen_lulus : 0) + "%", color: "stat-teal" },
            { label: "Batas Lulus (KKM)", value: (r.threshold != null ? r.threshold : 70), color: "stat-amber" },
        ];
        var html = '';
        for (var i = 0; i < items.length; i++) {
            html += '<div class="stat-card-v2 ' + items[i].color + '">';
            html += '  <div class="stat-v2-value">' + items[i].value + '</div>';
            html += '  <div class="stat-v2-label">' + items[i].label + '</div>';
            html += '</div>';
        }
        container.innerHTML = html;
    }

    function _renderTable(items) {
        var html = '<table class="data-table compact">';
        html += '<thead><tr><th>CPL</th><th>Deskripsi</th><th>Skor</th><th>Grade</th><th>Status</th></tr></thead><tbody>';
        for (var i = 0; i < items.length; i++) {
            var it = items[i];
            var badge = it.lulus
                ? '<span class="badge badge-success">Tercapai</span>'
                : '<span class="badge badge-danger">Belum</span>';
            html += '<tr>';
            html += '<td class="cell-code">' + DomUtils.escape(it.label) + '</td>';
            html += '<td>' + DomUtils.escape(_truncate(it.deskripsi, 90)) + '</td>';
            html += '<td><strong>' + Math.round(it.value) + '</strong></td>';
            html += '<td>' + DomUtils.escape(it.grade) + '</td>';
            html += '<td>' + badge + '</td>';
            html += '</tr>';
        }
        html += '</tbody></table>';
        document.getElementById("mhs-cpl-table").innerHTML = html;
    }

    function _truncate(s, n) {
        s = s || "";
        return s.length > n ? s.substring(0, n) + "..." : s;
    }

    function _renderEmpty(msg) {
        document.getElementById("mhs-report-body").innerHTML =
            '<div class="card"><div class="card-body">' +
            '<div class="empty-state"><p>' + DomUtils.escape(msg) + '</p></div>' +
            '</div></div>';
    }

    return { init: init };

})();
