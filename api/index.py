"""
Vercel serverless entry point.
Mengexpose Flask app sebagai WSGI handler untuk Vercel.
"""

import sys
import os
import traceback

# Tambahkan root project ke sys.path
_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

from flask import Flask

app = None
init_error = None

try:
    from app import create_app, seed_all
    app = create_app()

    # Seed data saat cold start (hanya jika tabel kosong)
    try:
        seed_all()
    except Exception as e:
        print(f"Seed error: {e}")
        # Keep going even if seeding fails
        pass

except Exception as e:
    init_error = traceback.format_exc()
    print(f"Initialization error:\n{init_error}")

if app is None:
    # Buat fallback app untuk menampilkan error ke user di Vercel
    app = Flask(__name__)
    
    @app.route("/", defaults={"path": ""})
    @app.route("/<path:path>")
    def catch_all(path):
        return f"""
        <html>
        <head>
            <title>Sistem OBE - App Initialization Error</title>
            <style>
                body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background: #0f172a; color: #f1f5f9; padding: 40px; line-height: 1.6; }}
                .container {{ max-width: 800px; margin: 0 auto; background: #1e293b; padding: 30px; border-radius: 12px; border: 1px solid #334155; box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.5); }}
                h1 {{ color: #ef4444; margin-top: 0; font-size: 24px; border-bottom: 1px solid #334155; padding-bottom: 15px; }}
                pre {{ background: #0f172a; padding: 20px; border-radius: 8px; border: 1px solid #1e293b; overflow-x: auto; color: #f87171; font-size: 14px; font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace; }}
                p {{ color: #94a3b8; }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Flask App Initialization Error on Vercel</h1>
                <p>The application crashed during startup. Here is the detailed traceback:</p>
                <pre>{init_error}</pre>
                <p style="margin-top: 20px; font-size: 12px; color: #64748b;">Environment: Vercel Serverless Function</p>
            </div>
        </body>
        </html>
        """, 500

