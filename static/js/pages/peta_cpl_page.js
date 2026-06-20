/**
 * Halaman Peta Pemenuhan CPL (Tabel 11 Buku Panduan APTIKOM).
 * Matriks CPL x Semester, menunjukkan daftar MK + SKS per sel.
 * Data diturunkan OTOMATIS dari relasi CPL-MK + semester.
 */
var PetaCplPage = (function () {

    function init(entry) {
        var content = document.getElementById("page-content");
        content.innerHTML =
            '<div class="page-header">' +
            '  <h2 class="page-title">' + entry.title + '</h2>' +
            '  <p class="page-desc">Distribusi CPL per semester — data otomatis dari relasi CPL-MK</p>' +
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
        html += '<th class="cell-center">Total MK</th>';
        html += '<th class="cell-center">Total SKS</th>';
        html += '</tr></thead><tbody>';

        for (var j = 0; j < rows.length; j++) {
            var row = rows[j];
            html += '<tr>';
            html += '<td class="sticky-col cell-code" title="' + DomUtils.escape(row.deskripsi) + '">' + DomUtils.escape(row.kode) + '</td>';
            var totalMK = 0;
            var totalSKS = 0;
            for (var k = 0; k < semesters.length; k++) {
                var semData = row.semesters[String(semesters[k])];
                var count = 0;
                var sks = 0;
                var tooltipText = "";
                if (semData && typeof semData === "object") {
                    count = semData.count || 0;
                    sks = semData.sks || 0;
                    var mkList = semData.mk_list || [];
                    var parts = [];
                    for (var m = 0; m < mkList.length; m++) {
                        parts.push(mkList[m].kode + " (" + mkList[m].sks + " SKS)");
                    }
                    tooltipText = parts.join(", ");
                } else if (typeof semData === "number") {
                    count = semData;
                }
                totalMK += count;
                totalSKS += sks;
                var cellClass = count > 0 ? "cell-active" : "cell-empty";
                var cellContent = count > 0 ? count + " MK<br>" + sks + " SKS" : "-";
                html += '<td class="cell-center ' + cellClass + '" title="' + DomUtils.escape(tooltipText) + '">' + cellContent + '</td>';
            }
            html += '<td class="cell-center cell-total">' + totalMK + '</td>';
            html += '<td class="cell-center cell-total">' + totalSKS + '</td>';
            html += '</tr>';
        }

        html += '</tbody></table></div>';
        container.innerHTML = html;
    }

    return { init: init };

})();
