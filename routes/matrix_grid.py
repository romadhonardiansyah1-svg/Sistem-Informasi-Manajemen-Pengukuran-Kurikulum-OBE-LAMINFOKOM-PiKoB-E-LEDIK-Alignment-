"""
API endpoint matriks interaktif.
Satu handler generic untuk 7 jenis matriks.
Dispatch berdasarkan key di MATRIX_TYPES -- tidak ada if-else per matriks.
"""

from flask import request

import state
from models.mapping import (
    mapping_cpl_pl, mapping_cpl_sndikti, mapping_cpl_bk,
    mapping_bk_mk, mapping_cpl_mk, mapping_cpmk_mk,
)
from utils.response import success, error
from services.sync_service import sync_cpl_mk_from_relations

SYNC_TRIGGER_TYPES = {"cpl_bk", "bk_mk"}


MATRIX_TYPES = {
    "cpl_pl": {
        "table": mapping_cpl_pl,
        "row_col": ("cpl_id", "pl_id"),
    },
    "cpl_sndikti": {
        "table": mapping_cpl_sndikti,
        "row_col": ("cpl_prodi_id", "cpl_sn_id"),
    },
    "cpl_bk": {
        "table": mapping_cpl_bk,
        "row_col": ("cpl_id", "bk_id"),
    },
    "bk_mk": {
        "table": mapping_bk_mk,
        "row_col": ("bk_id", "mk_id"),
    },
    "cpl_mk": {
        "table": mapping_cpl_mk,
        "row_col": ("cpl_id", "mk_id"),
    },
    "cpmk_mk": {
        "table": mapping_cpmk_mk,
        "row_col": ("cpmk_id", "mk_id"),
    },
}


def get_matrix(matrix_type):
    """GET /api/matrix/<matrix_type>"""
    config = MATRIX_TYPES.get(matrix_type)
    if config is None:
        return error("Tipe matriks tidak valid")

    table = config["table"]
    rows = state.db.execute(table.select()).fetchall()

    row_key, col_key = config["row_col"]
    data = [
        {row_key: getattr(r, row_key), col_key: getattr(r, col_key)}
        for r in rows
    ]

    return success(data=data)


def toggle_cell(matrix_type):
    """POST /api/matrix/<matrix_type>/toggle"""
    config = MATRIX_TYPES.get(matrix_type)
    if config is None:
        return error("Tipe matriks tidak valid")

    body = request.get_json(silent=True)
    table = config["table"]
    row_key, col_key = config["row_col"]

    row_id = body.get("row_id")
    col_id = body.get("col_id")

    existing = state.db.execute(
        table.select().where(
            (table.c[row_key] == row_id) & (table.c[col_key] == col_id)
        )
    ).fetchone()

    if existing:
        state.db.execute(
            table.delete().where(
                (table.c[row_key] == row_id) & (table.c[col_key] == col_id)
            )
        )
        state.db.commit()

        sync_result = None
        if matrix_type in SYNC_TRIGGER_TYPES:
            sync_result = sync_cpl_mk_from_relations()

        return success(
            data={"active": False, "sync": sync_result},
            message="Relasi dihapus",
        )

    state.db.execute(
        table.insert().values(**{row_key: row_id, col_key: col_id})
    )
    state.db.commit()

    sync_result = None
    if matrix_type in SYNC_TRIGGER_TYPES:
        sync_result = sync_cpl_mk_from_relations()

    return success(
        data={"active": True, "sync": sync_result},
        message="Relasi ditambahkan",
    )


ROUTE_DEFINITIONS = [
    ("GET", "/api/matrix/<matrix_type>", get_matrix, "view_all"),
    ("POST", "/api/matrix/<matrix_type>/toggle", toggle_cell, "manage_matrix"),
]
