/**
 * Number and string formatting utilities.
 */
var FormatUtils = (function () {

    function number(value, decimals) {
        decimals = decimals || 0;
        return Number(value).toFixed(decimals);
    }

    function percent(value) {
        return number(value, 1) + "%";
    }

    function truncate(text, maxLen) {
        maxLen = maxLen || 80;
        if (!text) return "";
        if (text.length <= maxLen) return text;
        return text.substring(0, maxLen - 3) + "...";
    }

    return { number: number, percent: percent, truncate: truncate };

})();
