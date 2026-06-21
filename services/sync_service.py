"""
Service sinkronisasi otomatis relasi turunan.
Saat CPL-BK atau BK-MK berubah, CPL-MK di-update otomatis.
T-8.1 Backlog Notion.
"""

import state
from models.mapping import mapping_cpl_bk, mapping_bk_mk, mapping_cpl_mk


def sync_cpl_mk_from_relations():
    """
    Menghitung ulang CPL-MK berdasarkan CPL-BK dan BK-MK.
    Logika: CPL terhubung ke MK jika ada BK yang menghubungkan keduanya.
    CPL -> BK (dari mapping_cpl_bk) -> MK (dari mapping_bk_mk) = CPL -> MK.
    Return: jumlah relasi yang ditambahkan dan dihapus.
    """
    session = state.db

    cpl_bk_rows = session.execute(mapping_cpl_bk.select()).fetchall()
    bk_mk_rows = session.execute(mapping_bk_mk.select()).fetchall()

    # PENTING: tabel mapping berkolom (id, fk1, fk2). Akses lewat NAMA kolom,
    # bukan indeks posisi — row[0] adalah `id`, bukan FK pertama. Memakai indeks
    # posisi (lama) menghasilkan pasangan salah dan MERUSAK mapping_cpl_mk.
    bk_to_mk = {}
    for row in bk_mk_rows:
        bk_id = row.bk_id
        mk_id = row.mk_id
        if bk_id not in bk_to_mk:
            bk_to_mk[bk_id] = set()
        bk_to_mk[bk_id].add(mk_id)

    computed = set()
    for row in cpl_bk_rows:
        cpl_id = row.cpl_id
        bk_id = row.bk_id
        mk_ids = bk_to_mk.get(bk_id, set())
        for mk_id in mk_ids:
            computed.add((cpl_id, mk_id))

    existing_rows = session.execute(mapping_cpl_mk.select()).fetchall()
    existing = set()
    for row in existing_rows:
        existing.add((row.cpl_id, row.mk_id))

    to_add = computed - existing
    to_remove = existing - computed

    for cpl_id, mk_id in to_add:
        session.execute(mapping_cpl_mk.insert().values(cpl_id=cpl_id, mk_id=mk_id))

    for cpl_id, mk_id in to_remove:
        session.execute(
            mapping_cpl_mk.delete().where(
                (mapping_cpl_mk.c.cpl_id == cpl_id) &
                (mapping_cpl_mk.c.mk_id == mk_id)
            )
        )

    session.commit()

    return {
        "added": len(to_add),
        "removed": len(to_remove),
        "total": len(computed),
    }
