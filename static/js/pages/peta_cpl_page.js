/**
 * Halaman Peta Pemenuhan CPL (Tabel 11 Buku Panduan APTIKOM).
 * Matriks CPL x Semester, menunjukkan jumlah MK per sel.
 */
var PetaCplPage = (function () {

    function init(entry) {
        var content = document.getElementById("page-content");
        content.innerHTML =
            '<div class="page-header">' +
            '  <h2 class="page-title">' + entry.title + '</h2>' +
            '  <p class="page-desc">Distribusi CPL per semester berdasarkan jumlah MK</p>' +
            '</div>' +
            '<div id="peta-cpl-container"></div>';

        Api.get("/api/peta-cpl").then(function (res) {
            var data = res.data || {};
            _renderMatrix(data);
        });
    }

    function _renderMatrix(data) {
        var container = document.getElementById("peta-cpl-container");
        var semesters = data.semesters || [];
        var rows = data.rows || [];

        var html = '<div class="matrix-scroll"><table class="data-table matrix-table">';
        html += '<thead><tr>';
        html += '<th class="sticky-col">CPL</th>';
        for (var i = 0; i < semesters.length; i++) {
            html += '<th class="cell-center">Sem ' + semesters[i] + '</th>';
        }
        html += '<th class="cell-center">Total</th>';
        html += '</tr></thead><tbody>';

        for (var j = 0; j < rows.length; j++) {
            var row = rows[j];
            html += '<tr>';
            html += '<td class="sticky-col cell-code" title="' + DomUtils.escape(row.deskripsi) + '">' + DomUtils.escape(row.kode) + '</td>';
            var total = 0;
            for (var k = 0; k < semesters.length; k++) {
                var count = row.semesters[String(semesters[k])] || 0;
                total += count;
                var cellClass = count > 0 ? "cell-active" : "cell-empty";
                html += '<td class="cell-center ' + cellClass + '">' + (count > 0 ? count : "-") + '</td>';
            }
            html += '<td class="cell-center cell-total">' + total + '</td>';
            html += '</tr>';
        }

        html += '</tbody></table></div>';
        container.innerHTML = html;
    }

    return { init: init };

})();
