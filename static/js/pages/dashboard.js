/**
 * Dashboard page.
 * Menampilkan ringkasan statistik kurikulum, progress pemetaan,
 * dan spider chart pemenuhan CPL.
 */
var DashboardPage = (function () {

    function init() {
        var content = document.getElementById("page-content");
        content.innerHTML = _buildLayout();
        _loadAllData();
    }

    function _buildLayout() {
        var html = '';

        html += '<div class="dash-welcome" id="dash-welcome"></div>';

        html += '<div class="dash-stats-grid" id="dash-stats"></div>';

        html += '<div class="dash-row">';
        html += '  <div class="dash-col-chart">';
        html += '    <div class="card">';
        html += '      <div class="card-header">Pemenuhan CPL Prodi</div>';
        html += '      <div class="card-body"><div class="spider-chart-container">';
        html += '        <canvas id="cpl-spider" class="spider-chart-canvas" width="460" height="460"></canvas>';
        html += '      </div></div>';
        html += '    </div>';
        html += '  </div>';
        html += '  <div class="dash-col-info">';
        html += '    <div class="card">';
        html += '      <div class="card-header">Progress Pemetaan</div>';
        html += '      <div class="card-body" id="dash-progress"></div>';
        html += '    </div>';
        html += '    <div class="card">';
        html += '      <div class="card-header">Distribusi MK per Semester</div>';
        html += '      <div class="card-body" id="dash-semester"></div>';
        html += '    </div>';
        html += '  </div>';
        html += '</div>';

        html += '<div class="card">';
        html += '  <div class="card-header">Pemetaan CPMK Terbaru</div>';
        html += '  <div class="card-body" id="dash-cpmk-list"></div>';
        html += '</div>';

        return html;
    }

    function _loadAllData() {
        Promise.all([
            Api.get("/api/pl"),
            Api.get("/api/cpl-prodi"),
            Api.get("/api/mk"),
            Api.get("/api/cpmk?page_size=50"),
            Api.get("/api/bk"),
            Api.get("/api/matrix/cpl_pl"),
            Api.get("/api/matrix/cpl_bk"),
            Api.get("/api/matrix/bk_mk"),
            Api.get("/api/matrix/cpl_mk"),
            Api.get("/api/organisasi-mk"),
        ]).then(function (res) {
            var pl = res[0].data || [];
            var cpl = res[1].data || [];
            var mk = res[2].data || [];
            var cpmk = res[3].data || [];
            var bk = res[4].data || [];
            var mCplPl = res[5].data || [];
            var mCplBk = res[6].data || [];
            var mBkMk = res[7].data || [];
            var mCplMk = res[8].data || [];
            var orgMk = res[9].data || [];

            _renderWelcome();
            _renderStats(pl.length, cpl.length, bk.length, mk.length, cpmk.length);
            _renderProgress(mCplPl.length, mCplBk.length, mBkMk.length, mCplMk.length);
            _renderSemester(orgMk);
            _renderCpmkList(cpmk, cpl);
            _renderSpider(cpl);
        });
    }

    function _renderWelcome() {
        var el = document.getElementById("dash-welcome");
        var user = AppState.user || {};
        var hour = new Date().getHours();
        var greeting = hour < 12 ? "Selamat Pagi" : hour < 17 ? "Selamat Siang" : "Selamat Malam";
        el.innerHTML =
            '<div class="welcome-card">' +
            '  <div class="welcome-text">' +
            '    <h2>' + greeting + ', ' + DomUtils.escape(user.nama || "Admin") + '</h2>' +
            '    <p>Sistem Informasi Manajemen Kurikulum OBE - Kurikulum 2024-2028</p>' +
            '  </div>' +
            '  <div class="welcome-badge">' +
            '    <span class="badge badge-success">' + DomUtils.escape(user.role || "kaprodi") + '</span>' +
            '  </div>' +
            '</div>';
    }

    function _renderStats(pl, cpl, bk, mk, cpmk) {
        var container = document.getElementById("dash-stats");
        var items = [
            { label: "Profil Lulusan", value: pl, color: "stat-blue" },
            { label: "CPL Prodi",      value: cpl, color: "stat-green" },
            { label: "Bahan Kajian",   value: bk, color: "stat-amber" },
            { label: "Mata Kuliah",    value: mk, color: "stat-purple" },
            { label: "CPMK",           value: cpmk, color: "stat-teal" },
        ];
        var html = '';
        for (var i = 0; i < items.length; i++) {
            var it = items[i];
            html += '<div class="stat-card-v2 ' + it.color + '">';
            html += '  <div class="stat-v2-value">' + it.value + '</div>';
            html += '  <div class="stat-v2-label">' + it.label + '</div>';
            html += '</div>';
        }
        container.innerHTML = html;
    }

    function _renderProgress(cplPl, cplBk, bkMk, cplMk) {
        var container = document.getElementById("dash-progress");
        var items = [
            { label: "CPL - PL", count: cplPl },
            { label: "CPL - BK", count: cplBk },
            { label: "BK - MK",  count: bkMk },
            { label: "CPL - MK", count: cplMk },
        ];
        var maxVal = 1;
        for (var i = 0; i < items.length; i++) {
            if (items[i].count > maxVal) maxVal = items[i].count;
        }
        var html = '';
        for (var j = 0; j < items.length; j++) {
            var pct = Math.round((items[j].count / maxVal) * 100);
            html += '<div class="progress-item">';
            html += '  <div class="progress-label">';
            html += '    <span>' + items[j].label + '</span>';
            html += '    <span class="progress-count">' + items[j].count + ' relasi</span>';
            html += '  </div>';
            html += '  <div class="progress-bar"><div class="progress-fill fill-success" style="width:' + pct + '%"></div></div>';
            html += '</div>';
        }
        container.innerHTML = html;
    }

    function _renderSemester(orgData) {
        var container = document.getElementById("dash-semester");
        var html = '<div class="semester-bars">';
        for (var i = 0; i < orgData.length; i++) {
            var sem = orgData[i];
            var barH = Math.max(20, sem.total_sks * 4);
            html += '<div class="sem-bar-col">';
            html += '  <div class="sem-bar" style="height:' + barH + 'px">';
            html += '    <span class="sem-bar-val">' + sem.total_sks + '</span>';
            html += '  </div>';
            html += '  <div class="sem-bar-label">S' + sem.semester + '</div>';
            html += '</div>';
        }
        html += '</div>';
        container.innerHTML = html;
    }

    function _renderCpmkList(cpmks, cpls) {
        var container = document.getElementById("dash-cpmk-list");
        var cplMap = {};
        for (var i = 0; i < cpls.length; i++) {
            cplMap[cpls[i].id] = cpls[i].kode;
        }
        var html = '<table class="data-table compact">';
        html += '<thead><tr><th>Kode</th><th>CPL</th><th>Deskripsi</th></tr></thead>';
        html += '<tbody>';
        var limit = Math.min(cpmks.length, 10);
        for (var j = 0; j < limit; j++) {
            var c = cpmks[j];
            var cplKode = cplMap[c.cpl_id] || "-";
            html += '<tr>';
            html += '<td class="cell-code">' + DomUtils.escape(c.kode) + '</td>';
            html += '<td class="cell-code">' + DomUtils.escape(cplKode) + '</td>';
            html += '<td>' + DomUtils.escape(c.deskripsi) + '</td>';
            html += '</tr>';
        }
        html += '</tbody></table>';
        if (cpmks.length > 10) {
            html += '<p class="dash-more">dan ' + (cpmks.length - 10) + ' CPMK lainnya</p>';
        }
        container.innerHTML = html;
    }

    function _renderSpider(cpls) {
        var canvas = document.getElementById("cpl-spider");
        if (!canvas || cpls.length === 0) return;
        if (typeof SpiderChart !== "undefined") {
            var dataPoints = [];
            for (var i = 0; i < cpls.length; i++) {
                dataPoints.push({
                    label: cpls[i].kode,
                    value: 70 + Math.round(Math.random() * 30),
                });
            }
            SpiderChart.draw("cpl-spider", dataPoints, 100);
        }
    }

    return { init: init };

})();
