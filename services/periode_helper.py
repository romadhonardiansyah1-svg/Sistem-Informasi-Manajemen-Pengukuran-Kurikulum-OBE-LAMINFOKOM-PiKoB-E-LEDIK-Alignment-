"""
Helper resolusi periode aktif untuk view turunan (BUG-4).

Urutan prioritas:
1. Query arg `periode_id` bila ada (dipasok frontend dari AppState.currentPeriode).
2. Periode dengan status 'aktif'.
3. Periode terbaru (tahun_mulai terbesar) sebagai cadangan terakhir.
"""

from flask import request

import state
from models.period import PeriodeKurikulum


def resolve_periode_id():
    """Tentukan periode yang difilter agar data antar periode tidak tercampur."""
    pid = request.args.get("periode_id", type=int)
    if pid:
        return pid

    aktif = (
        state.db.query(PeriodeKurikulum)
        .filter_by(status="aktif")
        .order_by(PeriodeKurikulum.tahun_mulai.desc())
        .first()
    )
    if aktif is not None:
        return aktif.id

    latest = (
        state.db.query(PeriodeKurikulum)
        .order_by(PeriodeKurikulum.tahun_mulai.desc())
        .first()
    )
    return latest.id if latest else None
