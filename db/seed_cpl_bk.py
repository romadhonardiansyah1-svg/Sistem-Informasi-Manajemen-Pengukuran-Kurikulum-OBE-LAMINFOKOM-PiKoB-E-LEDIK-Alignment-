"""
Seed CPL Prodi dan Bahan Kajian.
Data dari Sheet 3 (CPL Prodi) dan Sheet 6 (Bahan Kajian).
"""

import state
from models.cpl import CPLProdi
from models.bahan_kajian import BahanKajian


def seed_cpl_prodi(pid):
    """Seed 14 CPL Prodi dari Sheet 3."""
    data = [
        ("CPL01", "Mampu memahami, menganalisis, dan menilai konsep dasar dan peran sistem informasi dalam mengelola data dan memberikan rekomendasi pengambilan keputusan pada proses dan sistem organisasi"),
        ("CPL02", "Mampu merancang dan menggunakan database, serta mengolah dan menganalisa data dengan alat dan teknik pengolahan data"),
        ("CPL03", "Mampu memahami dan menggunakan berbagai metodologi pengembangan sistem beserta alat pemodelan sistem dan menganalisa kebutuhan pengguna dalam membangun sistem informasi untuk mencapai tujuan organisasi"),
        ("CPL04", "Mampu membuat perencanaan infrastruktur TI, arsitektur jaringan, layanan fisik dan cloud, menganalisa konsep identifikasi, otentikasi, otorisasi akses dalam konteks melindungi orang dan perangkat"),
        ("CPL05", "Mampu memahami dan menerapkan kode etik dalam penggunaan informasi dan data pada perancangan, implementasi, dan penggunaan suatu sistem"),
        ("CPL06", "Memiliki kemampuan merencanakan, menerapkan, memelihara dan meningkatkan sistem informasi organisasi untuk mencapai tujuan dan sasaran organisasi yang strategis baik jangka pendek maupun jangka panjang"),
        ("CPL07", "Mampu memahami, mengidentifikasi dan menerapkan konsep, teknik dan metodologi manajemen proyek sistem informasi"),
        ("CPL08", "Mampu memahami dan menerapkan konsep, metode, teknik, dan tahapan data mining serta visualisasi data dalam pengolahan data, pengorganisasian data, dan penyajian informasi yang efektif, efisien, dan estetik"),
        ("CPL09", "Mampu memahami dan menerapkan model sistem, metode dan berbagai teknik peningkatan bisnis proses, peluang inovasi digital dalam pengelolaan bisnis yang memanfaatkan teknologi"),
        ("CPL10", "Mampu menunjukkan sikap profesionalitas, integritas, dan berjati diri islami yang dilengkapi dengan kemampuan komunikasi, kepemimpinan, bekerja sama dan bertanggung jawab atas pekerjaan di bidang keahliannya"),
        ("CPL11", "Mampu menunjukkan sikap taat hukum, disiplin, dan menghargai keanekaragaman melalui internalisasi nilai, norma, etika akademik, semangat kemandirian, kejuangan, dan kewirausahaan"),
        ("CPL12", "Mampu menunjukkan kinerja mandiri, bermutu, terukur, berfikir logis, kritis, sistematis, dan inovatif, komunikatif dalam mengembangkan ilmu pengetahuan yang memperhatikan nilai humaniora sesuai bidang keahliannya"),
        ("CPL13", "Mampu mengkaji implikasi pengembangan ilmu pengetahuan dengan menerapkan keahliannya dalam rangka menghasilkan solusi, menyusun deskripsi saintifik hasil kajian dalam bentuk laporan ilmiah yang sahih dan original"),
        ("CPL14", "Mampu melakukan evaluasi diri dan supervisi terhadap penyelesaian pekerjaan sebagai wujud tanggung jawab atas pencapaian hasil kelompok kerja"),
    ]
    for kode, desk in data:
        state.db.add(CPLProdi(periode_id=pid, kode=kode, deskripsi=desk))
    state.db.flush()


def seed_bahan_kajian(pid):
    """Seed 21 Bahan Kajian dari Sheet 6."""
    data = [
        ("BK01", "Foundation of Information Systems"),
        ("BK02", "Data / Information Management"),
        ("BK03", "Infrastructure"),
        ("BK04", "Project Management"),
        ("BK05", "Systems Analysis & Design"),
        ("BK06", "IS Management and Strategy"),
        ("BK07", "Application Development / Programming"),
        ("BK08", "Secure Computing"),
        ("BK09", "Ethics, Use and Implications for Society"),
        ("BK10", "Praktikum"),
        ("BK11", "Mathematics and Statistics"),
        ("BK12", "Data / Business Analytics"),
        ("BK13", "Personality Development"),
        ("BK14", "Business Process Management"),
        ("BK15", "Enterprise Architecture"),
        ("BK16", "User Interface Design"),
        ("BK17", "Digital Innovation"),
        ("BK18", "Visualisasi Informasi"),
        ("BK19", "Pemrograman Berorientasi Objek"),
        ("BK20", "Pemrograman Web"),
        ("BK21", "Pemrograman Mobile"),
    ]
    for kode, nama in data:
        state.db.add(BahanKajian(periode_id=pid, kode=kode, nama=nama, kompetensi="utama"))
    state.db.flush()
