/**
 * Halaman Pemetaan CPL-BK-MK (Tabel 8 Buku Panduan APTIKOM, hal 24).
 * Dua tampilan:
 *  - Diagram gaya buku: MK di tengah, Bahan Kajian di atas, CPL sebagai kode.
 *  - Tabel hierarkis (read-only) sebagai cadangan.
 */
var PemetaanPage = (function () {

    var _data = [];
    var _view = "diagram";

    function init(entry) {
        var content = document.getElementById("page-content");
        content.innerHTML =
            '<div class="page-header">' +
            '  <div>' +
            '    <h2 class="page-title">' + entry.title + '</h2>' +
            '    <p class="page-desc">Pemetaan gabungan CPL - Bahan Kajian - Mata Kuliah (Tabel 8, hal 24)</p>' +
            '  </div>' +
            '  <div class="page-header-actions">' +
            '    <button class="btn btn-sm btn-primary" id="btn-view-diagram">Diagram (gaya buku)</button>' +
            '    <button class="btn btn-sm btn-outline" id="btn-view-tabel">Tabel</button>' +
            '  </div>' +
            '</div>' +
            '<div id="pemetaan-container" class="pemetaan-wrapper"></div>';

        var pid = (AppState.currentPeriode && AppState.currentPeriode.id) || null;
        var url = "/api/pemetaan-cpl-bk-mk" + (pid ? ("?periode_id=" + pid) : "");
        Api.get(url).then(function (res) {
            _data = res.data || [];
            _render();
        });

        document.getElementById("btn-view-diagram").addEventListener("click", function () {
            _view = "diagram";
            _syncButtons();
            _render();
        });
        document.getElementById("btn-view-tabel").addEventListener("click", function () {
            _view = "tabel";
            _syncButtons();
            _render();
        });
    }

    function _syncButtons() {
        var d = document.getElementById("btn-view-diagram");
        var t = document.getElementById("btn-view-tabel");
        d.className = "btn btn-sm " + (_view === "diagram" ? "btn-primary" : "btn-outline");
        t.className = "btn btn-sm " + (_view === "tabel" ? "btn-primary" : "btn-outline");
    }

    function _render() {
        if (_view === "diagram") {
            _renderDiagram(_data);
        } else {
            _renderTable(_data);
        }
    }

    /**
     * Bangun struktur MK-sentris dari data CPL-sentris:
     * mk[kode] = { nama, bks: {kode->nama}, cpls: {kode} }
     */
    function _buildMkCentric(data) {
        var mkMap = {};
        for (var i = 0; i < data.length; i++) {
            var cpl = data[i];
            var bks = cpl.bahan_kajian || [];
            for (var j = 0; j < bks.length; j++) {
                var bk = bks[j];
                var mks = bk.mata_kuliah || [];
                for (var k = 0; k < mks.length; k++) {
                    var mk = mks[k];
                    if (!mkMap[mk.kode]) {
                        mkMap[mk.kode] = { kode: mk.kode, nama: mk.nama, bks: {}, cpls: {} };
                    }
                    mkMap[mk.kode].bks[bk.kode] = bk.nama;
                    mkMap[mk.kode].cpls[cpl.kode] = true;
                }
            }
        }
        var list = [];
        Object.keys(mkMap).sort().forEach(function (key) {
            list.push(mkMap[key]);
        });
        return list;
    }

    function _renderDiagram(data) {
        var container = document.getElementById("pemetaan-container");
        var mks = _buildMkCentric(data);

        if (mks.length === 0) {
            container.innerHTML = '<div class="empty-state"><p>Belum ada relasi CPL-BK-MK pada periode ini.</p></div>';
            return;
        }

        var html = '<div class="pemetaan-diagram">';
        for (var i = 0; i < mks.length; i++) {
            var mk = mks[i];
            html += '<div class="pmt-node">';

            // BK di atas
            html += '<div class="pmt-bk-row">';
            var bkKodes = Object.keys(mk.bks).sort();
            for (var b = 0; b < bkKodes.length; b++) {
                html += '<span class="pmt-bk-chip" title="' + DomUtils.escape(mk.bks[bkKodes[b]]) + '">' +
                        DomUtils.escape(bkKodes[b]) + '</span>';
            }
            html += '</div>';

            html += '<div class="pmt-connector"></div>';

            // MK di tengah
            html += '<div class="pmt-mk-box" title="' + DomUtils.escape(mk.nama) + '">';
            html += '<span class="pmt-mk-kode">' + DomUtils.escape(mk.kode) + '</span>';
            html += '<span class="pmt-mk-nama">' + DomUtils.escape(mk.nama) + '</span>';
            html += '</div>';

            html += '<div class="pmt-connector"></div>';

            // CPL sebagai kode di bawah
            html += '<div class="pmt-cpl-row">';
            var cplKodes = Object.keys(mk.cpls).sort();
            for (var c = 0; c < cplKodes.length; c++) {
                html += '<span class="pmt-cpl-code">' + DomUtils.escape(cplKodes[c]) + '</span>';
            }
            html += '</div>';

            html += '</div>';
        }
        html += '</div>';

        // Legenda
        html += '<div class="pmt-legend">' +
                '<span><i class="pmt-dot pmt-bk"></i> Bahan Kajian (atas)</span>' +
                '<span><i class="pmt-dot pmt-mk"></i> Mata Kuliah (tengah)</span>' +
                '<span><i class="pmt-dot pmt-cpl"></i> CPL (kode, bawah)</span>' +
                '</div>';

        container.innerHTML = html;
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
