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
            '  <p class="page-desc">Susunan mata kuliah per semester (memanjang ke samping, gaya Tabel 10 buku)</p>' +
            '</div>' +
            '<div id="organisasi-container" class="organisasi-wrapper"></div>';

        var pid = (AppState.currentPeriode && AppState.currentPeriode.id) || null;
        var url = "/api/organisasi-mk" + (pid ? ("?periode_id=" + pid) : "");
        Api.get(url).then(function (res) {
            var data = res.data || [];
            _renderHorizontal(data);
        });
    }

    var _JENIS_CLASS = {
        "wajib": "mk-wajib",
        "pilihan": "mk-pilihan",
        "mkwk": "mk-mkwk",
        "mkdu": "mk-mkdu",
    };

    function _renderHorizontal(data) {
        var container = document.getElementById("organisasi-container");

        if (data.length === 0) {
            container.innerHTML = '<div class="empty-state"><p>Belum ada data mata kuliah pada periode ini.</p></div>';
            return;
        }

        var grandTotal = 0;
        // Setiap semester = satu kolom yang berjajar horizontal.
        var html = '<div class="organisasi-horizontal">';
        for (var i = 0; i < data.length; i++) {
            var sem = data[i];
            grandTotal += sem.total_sks;
            html += '<div class="org-sem-col">';
            html += '<div class="org-sem-head">Semester ' + sem.semester +
                    '<span class="org-sem-sks">' + sem.total_sks + ' SKS</span></div>';
            html += '<div class="org-sem-body">';
            for (var j = 0; j < sem.mata_kuliah.length; j++) {
                var mk = sem.mata_kuliah[j];
                var cls = _JENIS_CLASS[(mk.jenis || "wajib").toLowerCase()] || "mk-wajib";
                html += '<div class="org-mk-card ' + cls + '" title="' + DomUtils.escape(mk.nama) + '">';
                html += '<span class="org-mk-kode">' + DomUtils.escape(mk.kode) + '</span>';
                html += '<span class="org-mk-nama">' + DomUtils.escape(mk.nama) + '</span>';
                html += '<span class="org-mk-sks">' + mk.sks + ' sks</span>';
                html += '</div>';
            }
            html += '</div></div>';
        }
        html += '</div>';

        // Legenda jenis MK + total beban belajar.
        html += '<div class="org-legend">';
        html += '<span><i class="org-dot mk-wajib"></i> Wajib</span>';
        html += '<span><i class="org-dot mk-pilihan"></i> Pilihan</span>';
        html += '<span><i class="org-dot mk-mkwk"></i> MKWK</span>';
        html += '<span><i class="org-dot mk-mkdu"></i> MKDU</span>';
        html += '<span class="org-total">Total beban belajar: <strong>' + grandTotal + ' SKS</strong></span>';
        html += '</div>';

        container.innerHTML = html;
    }

    return { init: init };

})();
