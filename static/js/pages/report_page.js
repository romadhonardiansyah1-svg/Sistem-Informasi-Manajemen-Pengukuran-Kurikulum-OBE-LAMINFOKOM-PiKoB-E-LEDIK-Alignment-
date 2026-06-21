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
            if (cpls.length === 0) {
                document.getElementById("cpl-summary").innerHTML =
                    '<div class="empty-state"><p>Belum ada data CPL Prodi.</p></div>';
                return;
            }

            var dataPoints = [];
            for (var i = 0; i < cpls.length; i++) {
                dataPoints.push({
                    label: cpls[i].kode,
                    value: 70 + Math.round(Math.random() * 30),
                });
            }
            SpiderChart.draw("report-spider", dataPoints, 100);

            var summary = document.getElementById("cpl-summary");
            var html = '<table class="data-table compact">';
            html += '<thead><tr><th>CPL</th><th>Deskripsi</th></tr></thead><tbody>';
            for (var j = 0; j < cpls.length; j++) {
                html += '<tr>';
                html += '<td class="cell-code">' + DomUtils.escape(cpls[j].kode) + '</td>';
                html += '<td>' + DomUtils.escape(cpls[j].deskripsi) + '</td>';
                html += '</tr>';
            }
            html += '</tbody></table>';
            html += '<p class="dash-more">Data nilai mahasiswa belum tersedia. Spider chart menampilkan data simulasi.</p>';
            summary.innerHTML = html;

            var cards = document.getElementById("cpl-cards");
            var cardsHtml = '';
            for (var k = 0; k < dataPoints.length; k++) {
                var dp = dataPoints[k];
                cardsHtml += '<div class="card cpl-report-card">';
                cardsHtml += '<div class="cpl-kode">' + dp.label + '</div>';
                cardsHtml += '<div class="cpl-score">' + Math.round(dp.value) + '</div>';
                cardsHtml += '<div class="cpl-grade">Simulasi</div>';
                cardsHtml += '<div class="progress-bar"><div class="progress-fill fill-' + _getColor(dp.value) + '" style="width:' + dp.value + '%"></div></div>';
                cardsHtml += '</div>';
            }
            cards.innerHTML = cardsHtml;
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
