"""
Seed data RPS dan Mahasiswa contoh.
Membuat beberapa dokumen RPS untuk MK semester 1-2
dan mahasiswa contoh untuk input nilai.
"""

import state
from models.rps import RPS, RPSMinggu
from models.user import Mahasiswa, User
from models.mata_kuliah import MataKuliah
from services.auth_service import hash_password


def seed_rps(periode_id):
    """Seed 3 dokumen RPS untuk MK semester 1."""
    session = state.db
    mk_list = session.query(MataKuliah).filter_by(semester=1).limit(3).all()

    dosen_names = [
        "Dr. Ahmad Fauzi, M.Kom",
        "Siti Rahayu, S.Kom, M.T",
        "Ir. Budi Santoso, M.Sc",
    ]

    for idx, mk in enumerate(mk_list):
        rps = RPS(
            mk_id=mk.id,
            periode_id=periode_id,
            kode_dokumen="RPS-SI-" + str(idx + 1).zfill(3),
            deskripsi_singkat="Rencana Pembelajaran Semester untuk " + mk.nama,
            dosen_pengampu=dosen_names[idx],
            dosen_koordinator=dosen_names[0],
            tanggal_penyusunan="2024-08-15",
        )
        session.add(rps)
        session.flush()

        for minggu in range(1, 17):
            label = "Ujian Tengah Semester" if minggu == 8 else "Ujian Akhir Semester" if minggu == 16 else "Pertemuan " + str(minggu)
            bentuk = "Ujian" if minggu in (8, 16) else "Ceramah, Diskusi, Praktik"
            bobot = 30.0 if minggu == 8 else 40.0 if minggu == 16 else round(30.0 / 14, 2)

            rm = RPSMinggu(
                rps_id=rps.id,
                minggu_ke=minggu,
                bentuk_pembelajaran=bentuk,
                materi=label,
                bobot_penilaian_persen=bobot,
            )
            session.add(rm)

    session.flush()


def seed_mahasiswa(prodi_id):
    """
    Seed 5 mahasiswa contoh + akun login masing-masing.
    Setiap mahasiswa otomatis memperoleh akun User (role=mahasiswa)
    dengan username = NIM dan password awal = NIM, lalu ditautkan via user_id
    sehingga mahasiswa dapat login dan melihat laporan capaian pribadinya.
    """
    session = state.db
    data = [
        ("2024001", "Andi Pratama", 2024),
        ("2024002", "Budi Setiawan", 2024),
        ("2024003", "Citra Dewi", 2024),
        ("2024004", "Dian Kusuma", 2024),
        ("2024005", "Eka Putri", 2024),
    ]
    for nim, nama, angkatan in data:
        # Akun login mahasiswa (username = NIM, password awal = NIM).
        akun = session.query(User).filter_by(username=nim).first()
        if akun is None:
            akun = User(
                username=nim,
                password_hash=hash_password(nim),
                nama=nama,
                email=nim + "@student.prodi.ac.id",
                role="mahasiswa",
                prodi_id=prodi_id,
            )
            session.add(akun)
            session.flush()

        mhs = Mahasiswa(
            user_id=akun.id,
            nim=nim,
            nama=nama,
            angkatan=angkatan,
            prodi_id=prodi_id,
        )
        session.add(mhs)
    session.flush()
