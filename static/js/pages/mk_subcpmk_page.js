/**
 * Halaman MK-CPMK-SubCPMK (Tabel 15 Buku Panduan APTIKOM).
 * Menampilkan hierarki per MK.
 */
var MkSubcpmkPage = (function () {

    function init(entry) {
        var content = document.getElementById("page-content");
        content.innerHTML =
            '<div class="page-header">' +
            '  <h2 class="page-title">' + entry.title + '</h2>' +
            '  <p class="page-desc">Pemetaan MK - CPMK - Sub CPMK</p>' +
            '</div>' +
            '<div id="mk-subcpmk-container"></div>';

        Api.get("/api/pemetaan-mk-subcpmk").then(function (res) {
            var data = res.data || [];
            _renderCards(data);
        });
    }

    function _renderCards(data) {
        var container = document.getElementById("mk-subcpmk-container");
        var html = '';

        for (var i = 0; i < data.length; i++) {
            var mk = data[i];
            var cpmks = mk.cpmk || [];
            if (cpmks.length === 0) continue;

            html += '<div class="mk-card">';
            html += '<div class="mk-card-header">';
            html += '<span class="badge">' + DomUtils.escape(mk.kode) + '</span>';
            html += '<span class="mk-name">' + DomUtils.escape(mk.nama) + '</span>';
            html += '<span class="badge badge-outline">Semester ' + mk.semester + '</span>';
            html += '</div>';

            html += '<table class="data-table compact">';
            html += '<thead><tr>';
            html += '<th>CPL</th><th>CPMK</th><th>Deskripsi</th><th>Sub-CPMK</th>';
            html += '</tr></thead><tbody>';

            for (var j = 0; j < cpmks.length; j++) {
                var cpmk = cpmks[j];
                var subs = cpmk.sub_cpmk || [];
                var subText = [];
                for (var k = 0; k < subs.length; k++) {
                    subText.push(subs[k].kode);
                }

                html += '<tr>';
                html += '<td class="cell-code">' + DomUtils.escape(cpmk.cpl_kode) + '</td>';
                html += '<td class="cell-code">' + DomUtils.escape(cpmk.kode) + '</td>';
                html += '<td>' + DomUtils.escape(cpmk.deskripsi) + '</td>';
                html += '<td class="cell-code">' + DomUtils.escape(subText.join(", ") || "(belum ada)") + '</td>';
                html += '</tr>';
            }

            html += '</tbody></table>';
            html += '</div>';
        }

        if (html === '') {
            html = '<div class="empty-state"><p>Belum ada data CPMK yang terpetakan ke mata kuliah.</p></div>';
        }

        container.innerHTML = html;
    }

    return { init: init };

})();
