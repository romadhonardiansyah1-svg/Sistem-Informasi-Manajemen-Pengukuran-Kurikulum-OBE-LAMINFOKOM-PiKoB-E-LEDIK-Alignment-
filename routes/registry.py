"""
Route registry -- mendaftarkan semua route menggunakan dispatch table.
Tidak ada @app.route berulang di mana-mana.
Setiap module route meng-export ROUTE_DEFINITIONS.
"""

from middleware.auth_guard import login_required
from middleware.role_guard import require_action


def register_routes(app):
    """
    Mendaftarkan seluruh route dari semua module.
    Setiap module menyediakan ROUTE_DEFINITIONS:
        [(method, path, handler, required_action_or_None), ...]
    """
    from routes import auth as auth_routes
    from routes import dashboard as dashboard_routes
    from routes import master_pl
    from routes import master_cpl
    from routes import master_bk
    from routes import master_mk
    from routes import master_cpmk
    from routes import matrix_grid
    from routes import rps_editor
    from routes import penilaian as penilaian_routes
    from routes import nilai_input
    from routes import kalkulasi
    from routes import report
    from routes import periode
    from routes import upload
    from routes import pemetaan_cpl_bk_mk
    from routes import organisasi_mk
    from routes import peta_cpl
    from routes import pemetaan_mk_subcpmk
    from routes import rumusan
    from routes import identitas_prodi
    from routes import log_peninjauan
    from routes import users as users_routes
    from routes import master_dropdown
    from routes import referensi_export

    modules = [
        auth_routes,
        dashboard_routes,
        master_pl,
        master_cpl,
        master_bk,
        master_mk,
        master_cpmk,
        matrix_grid,
        rps_editor,
        penilaian_routes,
        nilai_input,
        kalkulasi,
        report,
        periode,
        upload,
        pemetaan_cpl_bk_mk,
        organisasi_mk,
        peta_cpl,
        pemetaan_mk_subcpmk,
        rumusan,
        identitas_prodi,
        log_peninjauan,
        users_routes,
        master_dropdown,
        referensi_export,
    ]

    for module in modules:
        definitions = getattr(module, "ROUTE_DEFINITIONS", [])
        for method, path, handler, action in definitions:
            wrapped = _wrap_handler(handler, action)
            endpoint_name = handler.__name__ + "_" + method.lower()
            app.add_url_rule(
                path,
                endpoint=endpoint_name,
                view_func=wrapped,
                methods=[method],
            )


def _wrap_handler(handler, action):
    """
    Membungkus handler dengan auth dan permission guard.
    action=None berarti endpoint publik (contoh: login).
    """
    if action is None:
        return handler

    @login_required
    @require_action(action)
    def guarded(*args, **kwargs):
        return handler(*args, **kwargs)

    guarded.__name__ = handler.__name__ + "_guarded"
    return guarded
