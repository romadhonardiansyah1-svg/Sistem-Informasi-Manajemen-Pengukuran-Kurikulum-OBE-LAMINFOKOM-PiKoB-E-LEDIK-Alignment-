/**
 * Dynamic form generator.
 * Menggunakan konfigurasi fields, bukan hard-coded HTML.
 */
var FormBuilder = (function () {

    function build(fields, values) {
        values = values || {};
        var form = document.createElement("form");
        form.className = "form-dynamic";

        for (var i = 0; i < fields.length; i++) {
            var field = fields[i];
            var group = document.createElement("div");
            group.className = "form-group";

            var label = document.createElement("label");
            label.className = "form-label";
            label.textContent = field.label;
            label.setAttribute("for", "field-" + field.key);
            group.appendChild(label);

            var input = _createInput(field, values[field.key]);
            group.appendChild(input);

            form.appendChild(group);
        }

        return form;
    }

    function _createInput(field, value) {
        var INPUT_CREATORS = {
            "text":     _createTextInput,
            "number":   _createNumberInput,
            "textarea": _createTextarea,
            "select":   _createSelect,
            "remote-select": _createRemoteSelect,
        };

        var creator = INPUT_CREATORS[field.type] || _createTextInput;
        return creator(field, value);
    }

    function _createTextInput(field, value) {
        var input = document.createElement("input");
        input.type = "text";
        input.className = "form-input";
        input.id = "field-" + field.key;
        input.name = field.key;
        input.value = value || "";
        return input;
    }

    function _createNumberInput(field, value) {
        var input = document.createElement("input");
        input.type = "number";
        input.className = "form-input";
        input.id = "field-" + field.key;
        input.name = field.key;
        input.value = value || "";
        return input;
    }

    function _createTextarea(field, value) {
        var textarea = document.createElement("textarea");
        textarea.className = "form-textarea";
        textarea.id = "field-" + field.key;
        textarea.name = field.key;
        textarea.value = value || "";
        return textarea;
    }

    function _createSelect(field, value) {
        var select = document.createElement("select");
        select.className = "form-select";
        select.id = "field-" + field.key;
        select.name = field.key;

        var options = field.options || [];
        for (var i = 0; i < options.length; i++) {
            var opt = document.createElement("option");
            opt.value = options[i].value;
            opt.textContent = options[i].label;
            if (value && options[i].value === value) {
                opt.selected = true;
            }
            select.appendChild(opt);
        }
        return select;
    }

    function _createRemoteSelect(field, value) {
        var select = document.createElement("select");
        select.className = "form-select";
        select.id = "field-" + field.key;
        select.name = field.key;

        // Opsi default
        var defOpt = document.createElement("option");
        defOpt.value = "";
        defOpt.textContent = "-- Pilih " + field.label + " --";
        select.appendChild(defOpt);

        // Load opsi dari endpoint API
        Api.get(field.endpoint).then(function (res) {
            var items = res.data || [];
            var vKey = field.valueKey || "nama";
            for (var i = 0; i < items.length; i++) {
                var opt = document.createElement("option");
                opt.value = items[i][vKey];
                opt.textContent = items[i][vKey];
                if (value && items[i][vKey] === value) {
                    opt.selected = true;
                }
                select.appendChild(opt);
            }
        });

        // Atur nilai awal jika sudah ada
        if (value) {
            select.value = value;
        }

        return select;
    }

    function getValues(form) {
        var data = {};
        var elements = form.elements;
        for (var i = 0; i < elements.length; i++) {
            var el = elements[i];
            if (el.name) {
                data[el.name] = el.type === "number" ? Number(el.value) : el.value;
            }
        }
        return data;
    }

    return { build: build, getValues: getValues };

})();
