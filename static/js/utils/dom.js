/**
 * DOM manipulation helpers.
 */
var DomUtils = (function () {

    function el(tag, attrs, children) {
        var element = document.createElement(tag);
        if (attrs) {
            var keys = Object.keys(attrs);
            for (var i = 0; i < keys.length; i++) {
                element.setAttribute(keys[i], attrs[keys[i]]);
            }
        }
        if (children) {
            if (typeof children === "string") {
                element.textContent = children;
            } else if (Array.isArray(children)) {
                for (var c = 0; c < children.length; c++) {
                    element.appendChild(children[c]);
                }
            }
        }
        return element;
    }

    function clear(container) {
        container.innerHTML = "";
    }

    function show(element) { element.style.display = ""; }
    function hide(element) { element.style.display = "none"; }

    function escape(str) {
        if (str === null || str === undefined) return "";
        var s = String(str);
        var div = document.createElement("div");
        div.appendChild(document.createTextNode(s));
        return div.innerHTML;
    }

    return { el: el, clear: clear, show: show, hide: hide, escape: escape };

})();
