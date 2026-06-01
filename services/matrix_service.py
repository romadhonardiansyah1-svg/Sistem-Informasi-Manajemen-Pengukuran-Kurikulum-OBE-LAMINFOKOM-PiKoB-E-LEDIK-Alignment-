"""
Logika baca/tulis matriks pemetaan.
Sinkronisasi antar matriks.
"""

import state
from models.mapping import (
    mapping_cpl_bk, mapping_bk_mk, mapping_cpl_mk,
)


def get_matrix_data(table, row_key, col_key):
    """Mengambil seluruh data dari tabel asosiasi."""
    rows = state.db.execute(table.select()).fetchall()
    return [
        {row_key: getattr(r, row_key), col_key: getattr(r, col_key)}
        for r in rows
    ]


def toggle_mapping(table, row_key, col_key, row_id, col_id):
    """
    Toggle relasi: jika ada -> hapus, jika tidak -> tambah.
    Return: True jika sekarang aktif, False jika dihapus.
    """
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
        return False

    state.db.execute(
        table.insert().values(**{row_key: row_id, col_key: col_id})
    )
    state.db.commit()
    return True


def sync_cpl_mk_from_bk():
    """
    Sinkronisasi matriks CPL-MK berdasarkan CPL-BK dan BK-MK.
    Jika CPL terhubung ke BK, dan BK terhubung ke MK,
    maka CPL terhubung ke MK.
    """
    state.db.execute(mapping_cpl_mk.delete())

    cpl_bk_rows = state.db.execute(mapping_cpl_bk.select()).fetchall()
    bk_mk_rows = state.db.execute(mapping_bk_mk.select()).fetchall()

    bk_to_mk = {}
    for row in bk_mk_rows:
        bk_id = row.bk_id
        if bk_id not in bk_to_mk:
            bk_to_mk[bk_id] = []
        bk_to_mk[bk_id].append(row.mk_id)

    seen = set()
    for row in cpl_bk_rows:
        mk_ids = bk_to_mk.get(row.bk_id, [])
        for mk_id in mk_ids:
            pair = (row.cpl_id, mk_id)
            if pair not in seen:
                seen.add(pair)
                state.db.execute(
                    mapping_cpl_mk.insert().values(
                        cpl_id=row.cpl_id,
                        mk_id=mk_id,
                    )
                )

    state.db.commit()
