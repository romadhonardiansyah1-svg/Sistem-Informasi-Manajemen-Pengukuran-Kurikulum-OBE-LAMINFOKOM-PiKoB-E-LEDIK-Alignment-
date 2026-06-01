"""
Vercel serverless entry point.
Mengexpose Flask app sebagai WSGI handler untuk Vercel.
"""

import sys
import os

# Tambahkan root project ke sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app, seed_all

app = create_app()

# Seed data saat cold start (hanya jika tabel kosong)
with app.app_context():
    from models.institution import Universitas
    import state
    existing = state.db.query(Universitas).first()
    if existing is None:
        seed_all()
