/**
 * Halaman Laporan CPL dengan spider chart.
 * US 11: spider chart interaktif ketercapaian CPL.
 */
var ReportPage = (function () {

    function init() {
        var content = document.getElementById("page-content");
        content.innerHTML =
            '<div class="page-header">' +
            '  <div><h2 class="page-title">Laporan Pemenuhan CPL</h2>' +
            '  <p class="page-desc">Visualisasi ketercapaian Capaian Pembelajaran Lulusan</p></div>' +
            '  <div class="page-header-actions">' +
            '    <select class="periode-select" id="report-mhs" style="min-width:220px"></select>' +
            '    <button class="btn btn-primary" id="btn-export-pdf">Unduh PDF</button>' +
            '  </div>' +
            '</div>' +
            '<div class="dash-row">' +
            '  <div class="dash-col-chart">' +
            '    <div class="card">' +
            '      <div class="card-header">Spider Chart CPL Prodi</div>' +
            '      <div class="card-body"><div class="spider-chart-container">' +
            '        <canvas id="report-spider" class="spider-chart-canvas" width="500" height="500"></canvas>' +
            '      </div></div>' +
            '    </div>' +
            '  </div>' +
            '  <div class="dash-col-info">' +
            '    <div class="card">' +
            '      <div class="card-header">Ringkasan CPL</div>' +
            '      <div class="card-body" id="cpl-summary"></div>' +
            '    </div>' +
            '  </div>' +
            '</div>' +
            '<div class="cpl-report-grid" id="cpl-cards"></div>';

        _loadMahasiswaThenReport();

        document.getElementById("btn-export-pdf").addEventListener("click", function () {
            window.print();
        });
    }

    function _loadMahasiswaThenReport() {
        var sel = document.getElementById("report-mhs");
        Api.get("/api/mahasiswa").then(function (res) {
            var list = (res && res.data) || [];
            if (list.length === 0) {
                sel.style.display = "none";
                _renderFallback();
                return;
            }
            var opts = "";
            for (var i = 0; i < list.length; i++) {
                opts += '<option value="' + list[i].id + '">' +
                        DomUtils.escape(list[i].nim + " - " + list[i].nama) + '</option>';
            }
            sel.innerHTML = opts;
            sel.addEventListener("change", function () {
                _loadReport(parseInt(this.value, 10));
            });
            _loadReport(parseInt(sel.value, 10));
        }, function () {
            sel.style.display = "none";
            _renderFallback();
        });
    }

    function _loadReport(mahasiswaId) {
        // Bersihkan kartu sebelum render ulang agar tidak menumpuk saat ganti mahasiswa.
        var cards = document.getElementById("cpl-cards");
        if (cards) cards.innerHTML = "";

        Api.get("/api/report/cpl/mahasiswa?mahasiswa_id=" + mahasiswaId).then(function (res) {
            if (res.data && res.data.spider_chart && res.data.spider_chart.length > 0) {
                _renderWithData(res.data);
                return;
            }
            _renderFallback();
        });
    }

    function _renderWithData(data) {
        SpiderChart.draw("report-spider", data.spider_chart, 100);

        var cards = document.getElementById("cpl-cards");
        var items = data.spider_chart;
        for (var i = 0; i < items.length; i++) {
            var item = items[i];
            var card = document.createElement("div");
            card.className = "card cpl-report-card";
            card.innerHTML =
                '<div class="cpl-kode">' + item.label + '</div>' +
                '<div class="cpl-score">' + Math.round(item.value) + '</div>' +
                '<div class="cpl-grade">' + item.grade + '</div>' +
                '<div class="progress-bar">' +
                '  <div class="progress-fill fill-' + _getColor(item.value) + '" style="width: ' + item.value + '%"></div>' +
                '</div>';
            cards.appendChild(card);
        }
    }

    function _renderFallback() {
        Api.get("/api/cpl-prodi").then(function (res) {
            var cpls = res.data || [];
            var summary = document.getElementById("cpl-summary");
            if (cpls.length === 0) {
                summary.innerHTML =
                    '<div class="empty-state"><p>Belum ada data CPL Prodi pada periode ini.</p></div>';
                return;
            }

            // Jangan membuat angka palsu. Tampilkan daftar CPL + status kosong.
            var html = '<div class="empty-state" style="padding:16px 8px">' +
                '<div class="empty-state-title">Nilai mahasiswa belum tersedia</div>' +
                '<p>Ketercapaian CPL akan muncul otomatis setelah dosen menginput nilai mahasiswa. ' +
                'Angka tidak ditampilkan agar laporan tidak menyesatkan.</p></div>';
            html += '<table class="data-table compact" style="margin-top:12px">';
            html += '<thead><tr><th>CPL</th><th>Deskripsi</th><th>Status</th></tr></thead><tbody>';
            for (var j = 0; j < cpls.length; j++) {
                html += '<tr>';
                html += '<td class="cell-code">' + DomUtils.escape(cpls[j].kode) + '</td>';
                html += '<td>' + DomUtils.escape(cpls[j].deskripsi) + '</td>';
                html += '<td><span class="badge badge-warning">Belum dinilai</span></td>';
                html += '</tr>';
            }
            html += '</tbody></table>';
            summary.innerHTML = html;

            // Kosongkan area chart & kartu (tidak menggambar data simulasi).
            var cards = document.getElementById("cpl-cards");
            if (cards) cards.innerHTML = "";
            var canvas = document.getElementById("report-spider");
            if (canvas) {
                var ctx = canvas.getContext("2d");
                ctx.clearRect(0, 0, canvas.width, canvas.height);
                ctx.save();
                ctx.fillStyle = "#94a3b8";
                ctx.font = "14px Inter, sans-serif";
                ctx.textAlign = "center";
                ctx.fillText("Belum ada nilai", canvas.width / 2, canvas.height / 2);
                ctx.restore();
            }
        });
    }

    function _getColor(value) {
        var COLOR_THRESHOLDS = [
            { max: 40, cls: "danger" },
            { max: 70, cls: "warning" },
            { max: 101, cls: "success" },
        ];
        for (var i = 0; i < COLOR_THRESHOLDS.length; i++) {
            if (value < COLOR_THRESHOLDS[i].max) return COLOR_THRESHOLDS[i].cls;
        }
        return "success";
    }

    return { init: init };

})();
