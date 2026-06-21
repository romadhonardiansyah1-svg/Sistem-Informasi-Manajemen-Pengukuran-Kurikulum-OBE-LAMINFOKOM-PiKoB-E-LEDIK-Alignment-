/**
 * Reusable data table component.
 */
var TableComponent = (function () {

    function render(containerId, columns, rows, actions) {
        var container = document.getElementById(containerId);
        if (!container) {
            container = document.getElementById("page-content");
        }

        var table = document.createElement("table");
        table.className = "data-table";

        var thead = document.createElement("thead");
        var headerRow = document.createElement("tr");

        for (var c = 0; c < columns.length; c++) {
            var th = document.createElement("th");
            th.textContent = columns[c].label;
            if (columns[c].className) {
                th.className = columns[c].className;
            }
            headerRow.appendChild(th);
        }

        if (actions && actions.length > 0) {
            var thAct = document.createElement("th");
            thAct.textContent = "Aksi";
            headerRow.appendChild(thAct);
        }

        thead.appendChild(headerRow);
        table.appendChild(thead);

        var tbody = document.createElement("tbody");

        for (var r = 0; r < rows.length; r++) {
            var tr = document.createElement("tr");
            var row = rows[r];

            for (var c2 = 0; c2 < columns.length; c2++) {
                var td = document.createElement("td");
                var key = columns[c2].key;
                var cellVal = row[key] !== undefined && row[key] !== null ? row[key] : "";
                td.textContent = cellVal;
                if (columns[c2].className) {
                    td.className = columns[c2].className;
                    // Sel ringkas (mis. kolom referensi) -> tampilkan teks penuh saat hover.
                    if (cellVal) {
                        td.title = cellVal;
                    }
                }
                // Tooltip (hover): tampilkan data dari field lain saat hover pada kolom ini
                if (columns[c2].tooltip && row[columns[c2].tooltip]) {
                    td.title = columns[c2].tooltip + ": " + row[columns[c2].tooltip];
                    td.style.cursor = "help";
                }
                tr.appendChild(td);
            }

            if (actions && actions.length > 0) {
                var tdActions = document.createElement("td");
                for (var a = 0; a < actions.length; a++) {
                    var btn = document.createElement("button");
                    btn.className = "btn btn-sm " + (actions[a].btnClass || "btn-outline");
                    btn.textContent = actions[a].label;
                    btn.dataset.id = row.id;
                    btn.addEventListener("click", actions[a].handler);
                    tdActions.appendChild(btn);
                }
                tr.appendChild(tdActions);
            }

            tbody.appendChild(tr);
        }

        table.appendChild(tbody);

        var wrapper = document.createElement("div");
        wrapper.className = "card";
        wrapper.appendChild(table);

        return wrapper;
    }

    return { render: render };

})();
