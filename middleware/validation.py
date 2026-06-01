"""
Validasi input request.
Menggunakan schema dictionary, bukan if-else berulang.
"""

from flask import jsonify


def validate_request(data, schema):
    """
    Validasi data terhadap schema.
    Schema format: { field_name: { "required": bool, "type": str, "max_length": int } }
    Return: (is_valid, errors)
    """
    errors = []

    for field, rules in schema.items():
        value = data.get(field)

        is_required = rules.get("required", False)
        if is_required and (value is None or value == ""):
            errors.append({"field": field, "message": "Wajib diisi"})
            continue

        if value is None:
            continue

        expected_type = rules.get("type")
        type_map = {
            "str": str,
            "int": int,
            "float": float,
            "bool": bool,
        }
        if expected_type and expected_type in type_map:
            if not isinstance(value, type_map[expected_type]):
                errors.append({"field": field, "message": "Tipe data tidak sesuai"})

        max_length = rules.get("max_length")
        if max_length and isinstance(value, str) and len(value) > max_length:
            errors.append({"field": field, "message": "Melebihi panjang maksimal"})

        min_val = rules.get("min")
        if min_val is not None and isinstance(value, (int, float)) and value < min_val:
            errors.append({"field": field, "message": "Nilai terlalu kecil"})

        max_val = rules.get("max")
        if max_val is not None and isinstance(value, (int, float)) and value > max_val:
            errors.append({"field": field, "message": "Nilai terlalu besar"})

        choices = rules.get("choices")
        if choices and value not in choices:
            errors.append({"field": field, "message": "Pilihan tidak valid"})

    return len(errors) == 0, errors


def validation_error_response(errors):
    """Format error validasi sebagai JSON response."""
    return jsonify({"error": "Validasi gagal", "details": errors}), 400
