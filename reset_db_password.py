import os
import sys

# Tambahkan current directory ke path agar model ter-import dengan benar
_ROOT = os.path.dirname(os.path.abspath(__file__))
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from werkzeug.security import generate_password_hash

def hash_password(plain_text):
    return generate_password_hash(plain_text, method="pbkdf2:sha256")

def main():
    print("==================================================")
    print("         OBE DATABASE PASSWORD RESET TOOL         ")
    print("==================================================")
    print("Untuk menghindari kesalahan tenant ID, silakan gunakan")
    print("Connection URI lengkap dari Dashboard Supabase Anda.")
    print("--------------------------------------------------")
    print("1. Buka Supabase Dashboard > Project Settings > Database")
    print("2. Scroll ke 'Connection string' > pilih 'URI'")
    print("3. Salin URI tersebut (biasanya berakhiran :5432/postgres atau :6543/postgres)")
    print("--------------------------------------------------")
    
    db_uri_input = input("Tempel (Paste) Connection URI dari Supabase: ").strip()
    if not db_uri_input:
        print("\n[ERROR] Connection URI tidak boleh kosong!")
        return

    password_db = input("Masukkan PASSWORD DATABASE Supabase Anda: ").strip()
    if not password_db:
        print("\n[ERROR] Password tidak boleh kosong!")
        return

    # Ganti placeholder password [YOUR-PASSWORD] jika ada
    db_uri = db_uri_input
    if "[YOUR-PASSWORD]" in db_uri:
        db_uri = db_uri.replace("[YOUR-PASSWORD]", password_db)
    elif ":YOUR_PASSWORD@" in db_uri:
        db_uri = db_uri.replace("YOUR_PASSWORD", password_db)
    else:
        # Jika tidak ada placeholder, coba ganti password di antara ':' kedua dan '@'
        # postgresql://username:password@host...
        try:
            from urllib.parse import quote_plus
            scheme, rest = db_uri.split("://", 1)
            if "@" in rest:
                auth, host_db = rest.rsplit("@", 1)
                if ":" in auth:
                    username, _ = auth.split(":", 1)
                    safe_password = quote_plus(password_db)
                    db_uri = f"{scheme}://{username}:{safe_password}@{host_db}"
        except Exception:
            pass

    # Paksa gunakan port 5432 (Session Mode) untuk kestabilan koneksi dari komputer lokal
    if ":6543/" in db_uri:
        db_uri = db_uri.replace(":6543/", ":5432/")

    print("\nMenghubungkan ke database Supabase...")
    try:
        engine = create_engine(db_uri)
        # Uji koneksi
        with engine.connect() as conn:
            pass
        print("[OK] Koneksi ke Supabase berhasil!")
        
        # Load user model
        from models.user import User
        Session = sessionmaker(bind=engine)
        session = Session()
        
        admin = session.query(User).filter_by(username="admin").first()
        if admin:
            print(f"Menemukan user: {admin.username} (Role: {admin.role})")
            print("Mereset password...")
            new_hash = hash_password("admin123")
            admin.password_hash = new_hash
            session.add(admin)
            session.commit()
            print("\n[SUKSES] Password untuk 'admin' telah direset menjadi: admin123")
            print("Silakan buka website Anda di Vercel dan login dengan sandi tersebut!")
        else:
            print("\n[ERROR] User 'admin' tidak ditemukan di database.")
            
        session.close()
    except Exception as e:
        print(f"\n[ERROR] Gagal terhubung ke database: {e}")
        print("Pastikan Connection URI dan password database yang Anda masukkan sudah benar.")


if __name__ == "__main__":
    main()
