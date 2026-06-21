/**
 * Halaman matriks pemetaan.
 */
var MatrixPage = (function () {

    var ROW_COL_CONFIG = {
        "cpl_pl":   { rowEndpoint: "/api/cpl-prodi", colEndpoint: "/api/pl",        rowKey: "cpl_id", colKey: "pl_id" },
        "cpl_bk":   { rowEndpoint: "/api/cpl-prodi", colEndpoint: "/api/bk",        rowKey: "cpl_id", colKey: "bk_id" },
        "bk_mk":    { rowEndpoint: "/api/bk",        colEndpoint: "/api/mk",        rowKey: "bk_id",  colKey: "mk_id" },
        "cpl_mk":   { rowEndpoint: "/api/cpl-prodi", colEndpoint: "/api/mk",        rowKey: "cpl_id", colKey: "mk_id" },
        "cpmk_mk":  { rowEndpoint: "/api/cpmk",      colEndpoint: "/api/mk",        rowKey: "cpmk_id",colKey: "mk_id" },
    };

    function init(entry) {
        var type = entry.type;
        var content = document.getElementById("page-content");

        content.innerHTML =
            '<div class="page-header">' +
            '  <h2 class="page-title">' + entry.title + '</h2>' +
            '</div>' +
            '<div id="matrix-render-area"></div>';

        var config = ROW_COL_CONFIG[type];
        if (!config) return;

        // Batasi baris/kolom matriks ke periode aktif agar tidak mencampur
        // entitas antar-periode.
        var pid = (AppState.currentPeriode && AppState.currentPeriode.id) || null;
        var pq = pid ? ("?periode_id=" + pid) : "";

        Promise.all([
            Api.get(config.rowEndpoint + pq),
            Api.get(config.colEndpoint + pq),
            Api.get("/api/matrix/" + type),
        ]).then(function (results) {
            var rowItems = results[0].data || [];
            var colItems = results[1].data || [];
            var activeData = results[2].data || [];

            var activeSet = MatrixGridComponent.buildActiveSet(activeData, config.rowKey, config.colKey);

            var container = document.getElementById("matrix-render-area");
            MatrixGridComponent.render(container, rowItems, colItems, activeSet, {
                onToggle: function (rowId, colId, isActive) {
                    // Kembalikan promise<boolean> agar grid bisa revert bila ditolak.
                    return Api.post("/api/matrix/" + type + "/toggle", {
                        row_id: parseInt(rowId),
                        col_id: parseInt(colId),
                    }).then(function (res) {
                        var ok = res && res.status === "success";
                        if (!ok && typeof ToastComponent !== "undefined") {
                            ToastComponent.show(
                                (res && res.message) || "Gagal menyimpan relasi",
                                "error"
                            );
                        }
                        return ok;
                    });
                },
            });
        });
    }

    return { init: init };

})();
