"""
Seed 66 Mata Kuliah dari Sheet 11. Susunan Mata Kuliah.
"""

import state
from models.mata_kuliah import MataKuliah


def seed_mata_kuliah(pid):
    """Seed 66 MK dari data Excel."""
    # Format: (kode, nama, sks, semester, jenis)
    data = [
        ("MK01", "Agama", 3, 1, "mkdu"),
        ("MK02", "Pancasila", 2, 1, "mkwk"),
        ("MK03", "Bahasa Indonesia", 2, 1, "mkdu"),
        ("MK04", "Pengantar Sistem Informasi", 3, 1, "wajib"),
        ("MK05", "Algoritma dan Pemrograman", 3, 1, "wajib"),
        ("MK06", "Literasi TIK", 2, 1, "wajib"),
        ("MK07", "Matematika Diskrit", 3, 1, "wajib"),
        ("MK08", "Aswaja", 2, 2, "mkwk"),
        ("MK09", "Kewarganegaraan", 2, 2, "mkwk"),
        ("MK10", "Logika dan Metode Berfikir Kritis", 2, 2, "mkdu"),
        ("MK11", "Manajemen Data", 2, 2, "wajib"),
        ("MK12", "Struktur Data", 2, 2, "wajib"),
        ("MK13", "Sistem Operasi", 2, 2, "wajib"),
        ("MK14", "Pengantar Manajemen", 3, 2, "wajib"),
        ("MK15", "Manajemen Proses Bisnis", 3, 2, "wajib"),
        ("MK16", "Kewirausahaan", 3, 3, "mkdu"),
        ("MK17", "Pengantar Akuntansi", 3, 3, "wajib"),
        ("MK18", "Pemrograman Berorientasi Objek", 3, 3, "wajib"),
        ("MK19", "Analisis dan Perancangan Sistem Informasi", 3, 3, "wajib"),
        ("MK20", "Desain UI/UX", 3, 3, "wajib"),
        ("MK21", "Sistem dan Manajemen Basis Data", 4, 3, "wajib"),
        ("MK22", "Pemrograman Web", 3, 4, "wajib"),
        ("MK23", "Manajemen Proyek Sistem Informasi", 3, 4, "wajib"),
        ("MK24", "Data Science", 2, 4, "wajib"),
        ("MK25", "Sistem Enterprise", 3, 4, "wajib"),
        ("MK26", "Rintisan Bisnis Digital", 3, 4, "wajib"),
        ("MK27", "Desain dan Manajemen Jaringan Komputer", 3, 4, "wajib"),
        ("MK28", "Riset Operasi", 3, 4, "wajib"),
        ("MK29", "Pengujian Perangkat Lunak", 3, 5, "wajib"),
        ("MK30", "Manajemen Investasi TI", 3, 5, "wajib"),
        ("MK31", "Proteksi Aset Informasi", 3, 5, "wajib"),
        ("MK32", "Data Warehouse dan Data Mining", 3, 5, "wajib"),
        ("MK33", "Tata Kelola TI", 3, 5, "wajib"),
        ("MK34", "Capstone Project", 4, 5, "wajib"),
        ("MK35", "Statistik", 3, 5, "wajib"),
        ("MK36", "Bahasa Inggris", 2, 5, "mkdu"),
        ("MK37", "Perencanaan Strategis SI/TI", 3, 6, "wajib"),
        ("MK38", "Manajemen Layanan TI", 3, 6, "wajib"),
        ("MK39", "Etika Profesi", 2, 6, "wajib"),
        ("MK40", "Magang", 5, 7, "wajib"),
        ("MK41", "Metodologi Penelitian", 3, 7, "wajib"),
        ("MK42", "Keterampilan Interpersonal", 2, 7, "wajib"),
        ("MK43", "Kuliah Kerja Nyata", 2, 7, "wajib"),
        ("MK44", "Tugas Akhir", 6, 8, "wajib"),
        ("MK45", "Teknologi dan Masyarakat", 3, 8, "wajib"),
        ("MK46", "Kuliah Lapangan", 2, 8, "wajib"),
        ("MK47", "Pemrograman Mobile", 3, 6, "pilihan"),
        ("MK48", "Internet untuk Segala", 3, 6, "pilihan"),
        ("MK49", "Teknologi Pemrograman", 3, 7, "pilihan"),
        ("MK50", "Arsitektur Teknologi", 3, 8, "pilihan"),
        ("MK51", "Komputasi Awan", 3, 8, "pilihan"),
        ("MK52", "Manajemen Risiko TI", 3, 6, "pilihan"),
        ("MK53", "Manajemen Perubahan", 3, 6, "pilihan"),
        ("MK54", "Pengukuran Kinerja TI", 3, 7, "pilihan"),
        ("MK55", "Manajemen Keberlangsungan Bisnis", 3, 8, "pilihan"),
        ("MK56", "Audit Sistem Informasi", 3, 8, "pilihan"),
        ("MK57", "Sistem Pendukung Keputusan", 3, 6, "pilihan"),
        ("MK58", "Visualisasi Informasi", 3, 6, "pilihan"),
        ("MK59", "Sistem Cerdas", 3, 7, "pilihan"),
        ("MK60", "Teknik Peramalan", 3, 8, "pilihan"),
        ("MK61", "Pengolahan Citra", 3, 8, "pilihan"),
        ("MK62", "Manajemen Merek Digital", 3, 6, "pilihan"),
        ("MK63", "Pemasaran Digital", 3, 6, "pilihan"),
        ("MK64", "Kreatif Digital", 3, 7, "pilihan"),
        ("MK65", "Manajemen Hubungan Pelanggan", 3, 8, "pilihan"),
        ("MK66", "Manajemen Rantai Pasok", 3, 8, "pilihan"),
    ]
    for kode, nama, sks, smt, jenis in data:
        mk = MataKuliah(
            periode_id=pid,
            kode=kode,
            nama=nama,
            sks=sks,
            semester=smt,
            jenis=jenis,
        )
        state.db.add(mk)
    state.db.flush()
