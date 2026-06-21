/**
 * Halaman Referensi — peta 3 sumber per fitur.
 * Menampilkan tabel read-only yang memetakan setiap fitur sidebar ke:
 * 1. Rancangan Kurikulum (spreadsheet)
 * 2. Buku Kurikulum (panduan APTIKOM)
 * 3. PIKOBE / LEDIK
 */
var ReferensiPage = (function () {

    var REF_DATA = [
        { sidebar: "Identitas Prodi",       rancangan: "—",                         buku: "Tabel A Isian identitas (hal 6)",              pikobe: "—" },
        { sidebar: "Profil Lulusan",        rancangan: "—",                         buku: "Tabel 1 Profil Lulusan (hal 15)",              pikobe: "—" },
        { sidebar: "CPL Prodi",             rancangan: "Sheet 3. CPL Prodi",        buku: "Tabel 2 CPL Kompetensi Utama (hal 17)",        pikobe: "Tabel 2 Capaian Pembelajaran Lulusan" },
        { sidebar: "Bahan Kajian",          rancangan: "Sheet 6. Bahan Kajian",     buku: "Tabel 4 Rumusan Bahan Kajian (hal 19-20)",     pikobe: "—" },
        { sidebar: "Mata Kuliah",           rancangan: "Sheet 11. Susunan Mata Kuliah", buku: "Tabel 9 Susunan Mata Kuliah (hal 26-27)",  pikobe: "—" },
        { sidebar: "CPMK",                 rancangan: "—",                         buku: "Tabel 12 Pemetaan CPL-CPMK-MK (hal 31)",       pikobe: "—" },
        { sidebar: "Matriks CPL - PL",      rancangan: "—",                         buku: "Tabel 3 Pemetaan CPL dan PL (hal 18)",         pikobe: "—" },
        { sidebar: "Matriks CPL - BK",      rancangan: "—",                         buku: "Tabel 5 Pemetaan CPL-BK (hal 21)",             pikobe: "—" },
        { sidebar: "Matriks BK - MK",       rancangan: "—",                         buku: "Tabel 6 Pemetaan BK-MK (hal 22)",              pikobe: "—" },
        { sidebar: "Matriks CPL - MK",      rancangan: "—",                         buku: "Tabel 7 Pemetaan CPL-MK (hal 24)",             pikobe: "—" },
        { sidebar: "Matriks CPMK - MK",     rancangan: "—",                         buku: "Tabel 14 Pemetaan MK-CPL-CPMK (hal 33)",       pikobe: "—" },
        { sidebar: "Pemetaan CPL-BK-MK",    rancangan: "—",                         buku: "Tabel 8 Pemetaan BK-CPL-MK (hal 24)",          pikobe: "—" },
        { sidebar: "Organisasi MK",         rancangan: "—",                         buku: "Tabel 10 Organisasi Mata Kuliah (hal 29)",      pikobe: "—" },
        { sidebar: "Peta Pemenuhan CPL",    rancangan: "—",                         buku: "Tabel 11 Peta Pemenuhan CPL (hal 30)",          pikobe: "—" },
        { sidebar: "MK - CPMK - Sub CPMK", rancangan: "—",                         buku: "Tabel 15 Pemetaan MK-CPMK-Sub-CPMK (hal 35)",  pikobe: "—" },
        { sidebar: "RPS",                  rancangan: "Sheet 21. Rancangan RPS",   buku: "4. RPS (hal 42-45)",                           pikobe: "Sheet Contoh RPS" },
    ];

    function init() {
        var content = document.getElementById("page-content");

        var html = '<div class="page-header">' +
            '<h2 class="page-title">Referensi Sumber Data</h2>' +
            '<p class="page-desc">Pemetaan setiap fitur ke sumber dokumen: Rancangan Kurikulum (Spreadsheet), Buku Kurikulum (Panduan APTIKOM), dan PIKOBE/LEDIK.</p>' +
            '<button class="btn btn-sm btn-primary" id="btn-export-ref" style="margin-top:8px">⬇ Export Excel</button>' +
            '</div>';

        html += '<div class="card"><table class="data-table">';
        html += '<thead><tr>';
        html += '<th>Sidebar / Fitur</th>';
        html += '<th>Rancangan Kurikulum</th>';
        html += '<th>Buku Kurikulum</th>';
        html += '<th>PIKOBE / LEDIK</th>';
        html += '</tr></thead>';
        html += '<tbody>';

        for (var i = 0; i < REF_DATA.length; i++) {
            var r = REF_DATA[i];
            html += '<tr>';
            html += '<td><strong>' + DomUtils.escape(r.sidebar) + '</strong></td>';
            html += '<td>' + DomUtils.escape(r.rancangan) + '</td>';
            html += '<td>' + DomUtils.escape(r.buku) + '</td>';
            html += '<td>' + DomUtils.escape(r.pikobe) + '</td>';
            html += '</tr>';
        }

        html += '</tbody></table></div>';
        content.innerHTML = html;

        var exportBtn = document.getElementById("btn-export-ref");
        if (exportBtn) {
            exportBtn.addEventListener("click", function () {
                // Unduh langsung dari endpoint server (xlsx via openpyxl).
                window.location.href = "/api/referensi/export";
            });
        }
    }

    return { init: init };

})();
