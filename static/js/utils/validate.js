/**
 * Client-side validation utilities.
 */
var ValidateUtils = (function () {

    function required(value) {
        if (value === null || value === undefined) return false;
        if (typeof value === "string" && value.trim() === "") return false;
        return true;
    }

    function minLength(value, min) {
        return typeof value === "string" && value.length >= min;
    }

    function maxLength(value, max) {
        return typeof value === "string" && value.length <= max;
    }

    function isNumber(value) {
        return !isNaN(value) && isFinite(value);
    }

    function inRange(value, min, max) {
        var n = Number(value);
        return n >= min && n <= max;
    }

    return {
        required: required,
        minLength: minLength,
        maxLength: maxLength,
        isNumber: isNumber,
        inRange: inRange,
    };

})();
