/**
 * Toast notification component.
 */
var ToastComponent = (function () {

    var DURATION_MS = 4000;

    function show(message, type) {
        type = type || "success";
        var container = document.getElementById("toast-container");

        var toast = document.createElement("div");
        toast.className = "toast toast-" + type;
        toast.innerHTML = '<div class="toast-message">' + message + '</div>';

        container.appendChild(toast);

        setTimeout(function () {
            toast.style.opacity = "0";
            toast.style.transition = "opacity 0.3s ease";
            setTimeout(function () {
                if (toast.parentNode) toast.parentNode.removeChild(toast);
            }, 300);
        }, DURATION_MS);
    }

    function success(message) { show(message, "success"); }
    function error(message) { show(message, "error"); }

    return { show: show, success: success, error: error };

})();
