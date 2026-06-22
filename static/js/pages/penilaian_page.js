/**
 * Halaman Penilaian dan Bobot.
 * Tabel 16, 17, 18 Buku Panduan APTIKOM.
 * Menampilkan 3 tab: Teknik Penilaian, Tahap Penilaian, Bobot Penilaian.
 */
var PenilaianPage = (function () {

    var TABS = [
        { key: "teknik", label: "Teknik Penilaian (Tabel 16)", endpoint: "/api/penilaian/teknik" },
        { key: "tahap",  label: "Tahap Penilaian (Tabel 17)",  endpoint: "/api/penilaian/tahap" },
        { key: "bobot",  label: "Bobot Penilaian (Tabel 18)",  endpoint: "/api/penilaian/bobot" },
    ];

    var COLUMNS = {
        teknik: [
            { key: "cpl_kode", label: "CPL" },
            { key: "mk_kode", label: "MK" },
            { key: "cpmk_kode", label: "CPMK" },
            { key: "partisipasi", label: "Partisipasi" },
            { key: "observasi", label: "Observasi" },
            { key: "unjuk_kerja", label: "Unjuk Kerja" },
            { key: "tes_tulis_uts", label: "UTS" },
            { key: "tes_tulis_uas", label: "UAS" },
            { key: "tes_lisan", label: "Tes Lisan" },
        ],
        tahap: [
            { key: "cpl_kode", label: "CPL" },
            { key: "mk_kode", label: "MK" },
            { key: "cpmk_kode", label: "CPMK" },
            { key: "tahap", label: "Tahap" },
            { key: "teknik_penilaian_text", label: "Teknik" },
            { key: "instrumen", label: "Instrumen" },
            { key: "kriteria", label: "Kriteria" },
            { key: "bobot", label: "Bobot" },
        ],
        bobot: [
            { key: "mk_kode", label: "MK" },
            { key: "cpmk_kode", label: "CPMK" },
            { key: "partisipasi_pct", label: "Partisipasi (%)" },
            { key: "observasi_pct", label: "Observasi (%)" },
            { key: "unjuk_kerja_pct", label: "Unjuk Kerja (%)" },
            { key: "uts_pct", label: "UTS (%)" },
            { key: "uas_pct", label: "UAS (%)" },
            { key: "tes_lisan_pct", label: "Tes Lisan (%)" },
            { key: "total", label: "Total" },
        ],
    };

    var _activeTab = "teknik";

    function init() {
        var content = document.getElementById("page-content");
        content.innerHTML =
            '<div class="page-header">' +
            '  <h2 class="page-title">Penilaian dan Bobot</h2>' +
            '  <p class="page-desc">Teknik, tahap, dan bobot penilaian CPMK (Tabel 16-18)</p>' +
            '</div>' +
            '<div class="tab-bar" id="penilaian-tabs"></div>' +
            '<div id="penilaian-content"></div>';

        _renderTabs();
        _loadTab(_activeTab);
    }

    function _renderTabs() {
        var bar = document.getElementById("penilaian-tabs");
        var html = '';
        for (var i = 0; i < TABS.length; i++) {
            var active = TABS[i].key === _activeTab ? " tab-active" : "";
            html += '<button class="tab-btn' + active + '" data-tab="' + TABS[i].key + '">' + TABS[i].label + '</button>';
        }
        bar.innerHTML = html;
        var buttons = bar.querySelectorAll(".tab-btn");
        for (var j = 0; j < buttons.length; j++) {
            buttons[j].addEventListener("click", function () {
                _activeTab = this.dataset.tab;
                _renderTabs();
                _loadTab(_activeTab);
            });
        }
    }

    function _loadTab(tabKey) {
        var tab = null;
        for (var i = 0; i < TABS.length; i++) {
            if (TABS[i].key === tabKey) { tab = TABS[i]; break; }
        }
        if (!tab) return;

        var container = document.getElementById("penilaian-content");
        container.innerHTML = '<div class="loading-text">Memuat data...</div>';

        Api.get(tab.endpoint).then(function (res) {
            var items = res.data || [];
            if (items.length === 0) {
                container.innerHTML =
                    '<div class="empty-state">' +
                    '  <div class="empty-state-title">Belum ada data ' + tab.label + '</div>' +
                    '  <p>Data penilaian perlu diinput oleh dosen pengampu mata kuliah melalui form penilaian.</p>' +
                    '</div>';
                return;
            }
            var cols = COLUMNS[tabKey] || [];
            var html = '<table class="data-table">';
            html += '<thead><tr>';
            for (var c = 0; c < cols.length; c++) {
                html += '<th>' + cols[c].label + '</th>';
            }
            html += '</tr></thead><tbody>';
            for (var r = 0; r < items.length; r++) {
                html += '<tr>';
                for (var k = 0; k < cols.length; k++) {
                    var val = items[r][cols[k].key];
                    if (val === true) val = "Ya";
                    if (val === false) val = "-";
                    if (val === null || val === undefined) val = "-";
                    html += '<td>' + DomUtils.escape(String(val)) + '</td>';
                }
                html += '</tr>';
            }
            html += '</tbody></table>';
            container.innerHTML = html;
        });
    }

    return { init: init };

})();
