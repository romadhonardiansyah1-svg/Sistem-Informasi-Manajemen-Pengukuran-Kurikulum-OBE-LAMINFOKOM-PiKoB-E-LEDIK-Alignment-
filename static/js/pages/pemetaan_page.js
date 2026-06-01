/**
 * Halaman Pemetaan CPL-BK-MK (Tabel 8 Buku Panduan APTIKOM).
 * Read-only hierarchical view.
 */
var PemetaanPage = (function () {

    function init(entry) {
        var content = document.getElementById("page-content");
        content.innerHTML =
            '<div class="page-header">' +
            '  <h2 class="page-title">' + entry.title + '</h2>' +
            '  <p class="page-desc">Pemetaan gabungan CPL - Bahan Kajian - Mata Kuliah</p>' +
            '</div>' +
            '<div id="pemetaan-container" class="pemetaan-wrapper"></div>';

        Api.get("/api/pemetaan-cpl-bk-mk").then(function (res) {
            var data = res.data || [];
            _renderTable(data);
        });
    }

    function _renderTable(data) {
        var container = document.getElementById("pemetaan-container");
        var html = '<table class="data-table pemetaan-table">';
        html += '<thead><tr>';
        html += '<th>CPL</th>';
        html += '<th>Bahan Kajian</th>';
        html += '<th>Mata Kuliah</th>';
        html += '</tr></thead><tbody>';

        for (var i = 0; i < data.length; i++) {
            var cpl = data[i];
            var bks = cpl.bahan_kajian || [];

            if (bks.length === 0) {
                html += '<tr>';
                html += '<td class="cell-code" title="' + DomUtils.escape(cpl.deskripsi) + '">' + DomUtils.escape(cpl.kode) + '</td>';
                html += '<td>-</td><td>-</td>';
                html += '</tr>';
                continue;
            }

            for (var j = 0; j < bks.length; j++) {
                var bk = bks[j];
                var mkNames = [];
                for (var k = 0; k < bk.mata_kuliah.length; k++) {
                    mkNames.push(bk.mata_kuliah[k].kode + " (" + bk.mata_kuliah[k].nama + ")");
                }

                html += '<tr>';
                if (j === 0) {
                    html += '<td class="cell-code" rowspan="' + bks.length + '" title="' + DomUtils.escape(cpl.deskripsi) + '">' + DomUtils.escape(cpl.kode) + '</td>';
                }
                html += '<td class="cell-code" title="' + DomUtils.escape(bk.nama) + '">' + DomUtils.escape(bk.kode) + '</td>';
                html += '<td class="cell-detail">' + DomUtils.escape(mkNames.join(", ") || "-") + '</td>';
                html += '</tr>';
            }
        }

        html += '</tbody></table>';
        container.innerHTML = html;
    }

    return { init: init };

})();
