/**
 * HTTP client wrapper.
 * Satu fungsi apiCall() untuk semua request.
 */
var Api = (function () {

    function apiCall(method, path, data) {
        var options = {
            method: method,
            headers: { "Content-Type": "application/json" },
            credentials: "same-origin",
        };

        if (data && method !== "GET") {
            options.body = JSON.stringify(data);
        }

        return fetch(path, options)
            .then(function (response) {
                if (response.status === 401 && !path.includes("/api/auth/login")) {
                    window.location.href = "/login";
                    return Promise.reject("Sesi habis");
                }
                return response.json();
            });
    }

    function get(path) { return apiCall("GET", path); }
    function post(path, data) { return apiCall("POST", path, data); }
    function put(path, data) { return apiCall("PUT", path, data); }
    function del(path) { return apiCall("DELETE", path); }

    return { get: get, post: post, put: put, del: del, call: apiCall };

})();
