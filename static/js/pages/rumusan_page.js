/**
 * Halaman Rumusan Akhir MK dan CPL
 * (Tabel 19 dan 20 Buku Panduan APTIKOM).
 */
var RumusanPage = (function () {

    var ENDPOINTS = {
        "rumusan-mk":  { url: "/api/rumusan-mk",  label: "MK" },
        "rumusan-cpl": { url: "/api/rumusan-cpl", label: "CPL" },
    };

    function init(entry) {
        var content = document.getElementById("page-content");
        content.innerHTML =
            '<div class="page-header">' +
            '  <h2 class="page-title">' + entry.title + '</h2>' +
            '  <p class="page-desc">Rekapitulasi skor berdasarkan CPMK</p>' +
            '</div>' +
            '<div id="rumusan-container"></div>';

        var cfg = ENDPOINTS[entry.rumusanType];
        if (!cfg) return;

        Api.get(cfg.url).then(function (res) {
            var data = res.data || [];
            _renderTable(data, cfg.label);
        });
    }

    function _renderTable(data, label) {
        var container = document.getElementById("rumusan-container");
        var isMK = (label === "MK");

        var html = '<div class="matrix-scroll"><table class="data-table">';
        html += '<thead><tr>';
        html += '<th>' + label + '</th>';
        if (isMK) {
            html += '<th>Nama</th>';
        } else {
            html += '<th>Deskripsi</th>';
        }
        html += '<th>' + (isMK ? "CPL" : "MK") + '</th>';
        html += '<th>CPMK</th>';
        html += '<th>Skor Maks</th>';
        html += '<th>Total</th>';
        html += '</tr></thead><tbody>';

        for (var i = 0; i < data.length; i++) {
            var row = data[i];
            html += '<tr>';
            html += '<td class="cell-code">' + DomUtils.escape(row.kode) + '</td>';
            html += '<td>' + DomUtils.escape(isMK ? (row.nama || "") : (row.deskripsi || "")) + '</td>';
            html += '<td class="cell-code">' + DomUtils.escape((isMK ? row.cpl : row.mk).join(", ")) + '</td>';
            html += '<td class="cell-code">' + DomUtils.escape(row.cpmk.join(", ")) + '</td>';
            html += '<td class="cell-center">' + row.skor_maks + '</td>';
            html += '<td class="cell-center cell-total">' + row.total + '</td>';
            html += '</tr>';
        }

        html += '</tbody></table></div>';
        container.innerHTML = html;
    }

    return { init: init };

})();
