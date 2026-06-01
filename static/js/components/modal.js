/**
 * Modal dialog component.
 */
var ModalComponent = (function () {

    function open(title, bodyHtml, footerHtml) {
        document.getElementById("modal-title").textContent = title;
        document.getElementById("modal-body").innerHTML = bodyHtml;
        document.getElementById("modal-footer").innerHTML = footerHtml || "";
        document.getElementById("modal-backdrop").classList.add("visible");
    }

    function close() {
        document.getElementById("modal-backdrop").classList.remove("visible");
        document.getElementById("modal-body").innerHTML = "";
        document.getElementById("modal-footer").innerHTML = "";
    }

    document.addEventListener("DOMContentLoaded", function () {
        var closeBtn = document.getElementById("modal-close");
        if (closeBtn) {
            closeBtn.addEventListener("click", close);
        }
        var backdrop = document.getElementById("modal-backdrop");
        if (backdrop) {
            backdrop.addEventListener("click", function (e) {
                if (e.target === backdrop) close();
            });
        }
    });

    return { open: open, close: close };

})();
