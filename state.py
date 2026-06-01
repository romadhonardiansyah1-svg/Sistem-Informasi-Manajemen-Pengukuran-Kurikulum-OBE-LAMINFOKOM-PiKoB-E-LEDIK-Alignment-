"""
Global state management.
Seluruh referensi shared disimpan di modul ini.
Tidak ada variabel global tersebar di tempat lain.

Cara pakai:
    import state
    state.db.query(...)
    state.current_user
"""

# SQLAlchemy session -- di-set oleh db/connection.py saat startup
db = None

# SQLAlchemy engine -- di-set oleh db/connection.py saat startup
engine = None

# Flask app instance -- di-set oleh app.py
app = None

# User yang sedang login (per-request, di-set oleh middleware)
current_user = None

# Konfigurasi aktif -- di-set oleh app.py
app_config = None
