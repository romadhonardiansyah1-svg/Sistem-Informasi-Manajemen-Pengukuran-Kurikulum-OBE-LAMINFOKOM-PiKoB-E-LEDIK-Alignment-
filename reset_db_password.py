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
    print("Alamat database Anda:")
    print("aws-1-ap-southeast-1.pooler.supabase.com (Session Mode, port 5432)")
    print("--------------------------------------------------")
    
    password_db = input("Masukkan PASSWORD DATABASE Supabase Anda: ").strip()
    if not password_db:
        print("\n[ERROR] Password tidak boleh kosong!")
        return

    # Hubungkan ke Supabase (menggunakan port 5432 yang stabil)
    db_uri = f"postgresql://postgres:{password_db}@aws-1-ap-southeast-1.pooler.supabase.com:5432/postgres?sslmode=require"
    
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
        print("Pastikan password database yang Anda masukkan sudah benar.")

if __name__ == "__main__":
    main()
