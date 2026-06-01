/**
 * Komponen matriks grid interaktif.
 * Klik sel untuk toggle centang.
 * Hover pada header menampilkan tooltip deskripsi.
 */
var MatrixGridComponent = (function () {

    function render(container, rowItems, colItems, activeSet, callbacks) {
        container.innerHTML = "";

        var wrapper = document.createElement("div");
        wrapper.className = "matrix-container";

        var table = document.createElement("table");
        table.className = "matrix-table";

        var thead = document.createElement("thead");
        var headerRow = document.createElement("tr");

        var corner = document.createElement("th");
        corner.className = "corner";
        corner.textContent = "";
        headerRow.appendChild(corner);

        for (var c = 0; c < colItems.length; c++) {
            var th = document.createElement("th");
            th.textContent = colItems[c].kode;
            th.className = "matrix-header-cell";
            _attachTooltip(th, colItems[c]);
            headerRow.appendChild(th);
        }

        thead.appendChild(headerRow);
        table.appendChild(thead);

        var tbody = document.createElement("tbody");

        for (var r = 0; r < rowItems.length; r++) {
            var tr = document.createElement("tr");
            var rowTh = document.createElement("th");
            rowTh.textContent = rowItems[r].kode;
            rowTh.className = "matrix-header-cell";
            _attachTooltip(rowTh, rowItems[r]);
            tr.appendChild(rowTh);

            for (var c2 = 0; c2 < colItems.length; c2++) {
                var td = document.createElement("td");
                td.className = "matrix-cell";
                td.dataset.row = rowItems[r].id;
                td.dataset.col = colItems[c2].id;

                var key = rowItems[r].id + "_" + colItems[c2].id;
                if (activeSet[key]) {
                    td.classList.add("active");
                }

                var checkSpan = document.createElement("span");
                checkSpan.className = "check-mark";
                checkSpan.textContent = "V";
                td.appendChild(checkSpan);

                td.addEventListener("click", _createToggleHandler(td, callbacks));
                tr.appendChild(td);
            }

            tbody.appendChild(tr);
        }

        table.appendChild(tbody);
        wrapper.appendChild(table);
        container.appendChild(wrapper);
    }

    function _attachTooltip(el, item) {
        var desc = item.deskripsi || item.nama || "";
        if (!desc) return;

        el.addEventListener("mouseenter", function (e) {
            _showTooltip(e, item.kode, desc);
        });
        el.addEventListener("mouseleave", _hideTooltip);
        el.addEventListener("mousemove", function (e) {
            var tip = document.getElementById("matrix-tooltip");
            if (tip) {
                tip.style.left = (e.pageX + 12) + "px";
                tip.style.top = (e.pageY + 12) + "px";
            }
        });
    }

    function _showTooltip(e, kode, deskripsi) {
        _hideTooltip();
        var tip = document.createElement("div");
        tip.id = "matrix-tooltip";
        tip.className = "matrix-tooltip";
        tip.innerHTML =
            '<div class="tooltip-kode">' + DomUtils.escape(kode) + '</div>' +
            '<div class="tooltip-desc">' + DomUtils.escape(deskripsi) + '</div>';
        tip.style.left = (e.pageX + 12) + "px";
        tip.style.top = (e.pageY + 12) + "px";
        document.body.appendChild(tip);
    }

    function _hideTooltip() {
        var existing = document.getElementById("matrix-tooltip");
        if (existing) existing.remove();
    }

    function _createToggleHandler(td, callbacks) {
        return function () {
            var rowId = td.dataset.row;
            var colId = td.dataset.col;

            td.classList.toggle("active");

            if (callbacks && callbacks.onToggle) {
                callbacks.onToggle(rowId, colId, td.classList.contains("active"));
            }
        };
    }

    function buildActiveSet(data, rowKey, colKey) {
        var set = {};
        for (var i = 0; i < data.length; i++) {
            var key = data[i][rowKey] + "_" + data[i][colKey];
            set[key] = true;
        }
        return set;
    }

    return { render: render, buildActiveSet: buildActiveSet };

})();
