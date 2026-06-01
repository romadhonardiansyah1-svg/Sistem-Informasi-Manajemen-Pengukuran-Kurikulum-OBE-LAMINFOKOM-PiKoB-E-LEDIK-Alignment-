/**
 * Pub/sub event system.
 * Menggantikan coupling langsung antar komponen.
 */
var EventBus = (function () {

    var listeners = {};

    function on(event, callback) {
        if (!listeners[event]) {
            listeners[event] = [];
        }
        listeners[event].push(callback);
    }

    function off(event, callback) {
        if (!listeners[event]) return;
        listeners[event] = listeners[event].filter(function (cb) {
            return cb !== callback;
        });
    }

    function emit(event, data) {
        var list = listeners[event];
        if (!list) return;
        for (var i = 0; i < list.length; i++) {
            list[i](data);
        }
    }

    return { on: on, off: off, emit: emit };

})();
