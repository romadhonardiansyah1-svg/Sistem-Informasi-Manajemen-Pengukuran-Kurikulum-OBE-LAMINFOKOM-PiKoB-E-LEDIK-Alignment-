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

        Promise.all([
            Api.get(config.rowEndpoint),
            Api.get(config.colEndpoint),
            Api.get("/api/matrix/" + type),
        ]).then(function (results) {
            var rowItems = results[0].data || [];
            var colItems = results[1].data || [];
            var activeData = results[2].data || [];

            var activeSet = MatrixGridComponent.buildActiveSet(activeData, config.rowKey, config.colKey);

            var container = document.getElementById("matrix-render-area");
            MatrixGridComponent.render(container, rowItems, colItems, activeSet, {
                onToggle: function (rowId, colId, isActive) {
                    Api.post("/api/matrix/" + type + "/toggle", {
                        row_id: parseInt(rowId),
                        col_id: parseInt(colId),
                    });
                },
            });
        });
    }

    return { init: init };

})();
