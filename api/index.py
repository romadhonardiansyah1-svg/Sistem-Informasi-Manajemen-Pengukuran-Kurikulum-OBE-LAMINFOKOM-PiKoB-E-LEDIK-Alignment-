"""
Vercel serverless entry point.
Mengexpose Flask app sebagai WSGI handler untuk Vercel.
"""

import sys
import os

# Tambahkan root project ke sys.path
_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

from app import create_app, seed_all

app = create_app()

# Seed data saat cold start (hanya jika tabel kosong)
try:
    seed_all()
except Exception:
    pass
