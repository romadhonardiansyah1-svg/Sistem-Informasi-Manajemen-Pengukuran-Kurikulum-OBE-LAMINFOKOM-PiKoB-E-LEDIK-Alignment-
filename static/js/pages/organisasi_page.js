/**
 * Halaman Organisasi MK (Tabel 10 Buku Panduan APTIKOM).
 * MK dikelompokkan per semester.
 */
var OrganisasiPage = (function () {

    function init(entry) {
        var content = document.getElementById("page-content");
        content.innerHTML =
            '<div class="page-header">' +
            '  <h2 class="page-title">' + entry.title + '</h2>' +
            '  <p class="page-desc">Susunan mata kuliah per semester</p>' +
            '</div>' +
            '<div id="organisasi-container" class="organisasi-wrapper"></div>';

        Api.get("/api/organisasi-mk").then(function (res) {
            var data = res.data || [];
            _renderSemesters(data);
        });
    }

    function _renderSemesters(data) {
        var container = document.getElementById("organisasi-container");
        var html = '<div class="semester-grid">';

        for (var i = 0; i < data.length; i++) {
            var sem = data[i];
            html += '<div class="semester-card">';
            html += '<div class="semester-header">';
            html += '<h3>Semester ' + sem.semester + '</h3>';
            html += '<span class="badge">' + sem.total_sks + ' SKS</span>';
            html += '</div>';
            html += '<table class="data-table compact">';
            html += '<thead><tr><th>Kode</th><th>Nama MK</th><th>SKS</th><th>Jenis</th></tr></thead>';
            html += '<tbody>';

            for (var j = 0; j < sem.mata_kuliah.length; j++) {
                var mk = sem.mata_kuliah[j];
                html += '<tr>';
                html += '<td class="cell-code">' + DomUtils.escape(mk.kode) + '</td>';
                html += '<td>' + DomUtils.escape(mk.nama) + '</td>';
                html += '<td class="cell-center">' + mk.sks + '</td>';
                html += '<td class="cell-center">' + DomUtils.escape(mk.jenis || "wajib") + '</td>';
                html += '</tr>';
            }

            html += '</tbody></table>';
            html += '</div>';
        }

        html += '</div>';
        container.innerHTML = html;
    }

    return { init: init };

})();
