"""
Seed CPMK dari Sheet 13. Pemetaan CPL-CPMK-MK.
Total 33 CPMK terikat pada 14 CPL Prodi.
"""

import state
from models.cpl import CPLProdi
from models.cpmk import CPMK
from models.mata_kuliah import MataKuliah
from models.mapping import mapping_cpmk_mk


CPMK_DATA = [
    ("CPL01", "CPMK011", "Mampu memahami konsep dasar sistem informasi"),
    ("CPL01", "CPMK012", "Mampu menilai peran sistem informasi dalam memberikan rekomendasi pengambilan keputusan di organisasi"),
    ("CPL02", "CPMK021", "Mampu merancang dan menggunakan database"),
    ("CPL02", "CPMK022", "Mampu mengolah dan menganalisa data dengan alat dan teknik pengolahan data"),
    ("CPL03", "CPMK031", "Mampu menggunakan berbagai metodologi pengembangan sistem"),
    ("CPL03", "CPMK032", "Mampu menggunakan berbagai alat pemodelan sistem"),
    ("CPL03", "CPMK033", "Mampu menganalisa kebutuhan pengguna dalam membangun sistem informasi untuk mencapai tujuan organisasi"),
    ("CPL04", "CPMK041", "Mampu membuat perencanaan infrastruktur TI, arsitektur jaringan, layanan fisik dan cloud"),
    ("CPL04", "CPMK042", "Mampu menganalisa konsep identifikasi, otentikasi, otorisasi akses dalam konteks melindungi orang dan perangkat"),
    ("CPL05", "CPMK051", "Mampu memahami kode etik dalam penggunaan informasi dan data pada perancangan, implementasi, dan penggunaan suatu sistem"),
    ("CPL05", "CPMK052", "Mampu menerapkan kode etik dalam penggunaan informasi dan data pada perancangan, implementasi, dan penggunaan suatu sistem"),
    ("CPL06", "CPMK061", "Mampu merencanakan sistem informasi organisasi untuk mencapai tujuan dan sasaran organisasi jangka pendek maupun jangka panjang."),
    ("CPL06", "CPMK062", "Mampu menerapkan sistem informasi organisasi untuk mencapai tujuan dan sasaran organisasi jangka pendek maupun jangka panjang."),
    ("CPL06", "CPMK063", "Mampu memelihara sistem informasi organisasi untuk mencapai tujuan dan sasaran organisasi jangka pendek maupun jangka panjang."),
    ("CPL06", "CPMK064", "Mampu meningkatkan sistem informasi organisasi untuk mencapai tujuan dan sasaran organisasi jangka pendek maupun jangka panjang."),
    ("CPL07", "CPMK071", "Mampu memahami konsep, teknik dan metodologi manajemen proyek sistem informasi."),
    ("CPL07", "CPMK072", "Mampu mengidentifikasi konsep, teknik dan metodologi manajemen proyek sistem informasi."),
    ("CPL07", "CPMK073", "Mampu menerapkan konsep, teknik dan metodologi manajemen proyek sistem informasi."),
    ("CPL08", "CPMK081", "Mampu memahami konsep, metode, teknik, dan tahapan data mining serta visualisasi data dalam pengolahan data, pengorganisasian data, dan penyajian informasi yang efektif, efisien, dan estetik"),
    ("CPL08", "CPMK082", "Mampu menerapkan konsep, metode, teknik, dan tahapan data mining serta visualisasi data dalam pengolahan data, pengorganisasian data, dan penyajian informasi yang efektif, efisien, dan estetik"),
    ("CPL09", "CPMK091", "Mampu memahami model sistem, metode dan berbagai teknik peningkatan bisnis proses, peluang inovasi digital dalam pengelolaan bisnis bidang kesehatan yang memanfaatkan teknologi"),
    ("CPL09", "CPMK092", "Mampu menerapkan model sistem, metode dan berbagai teknik peningkatan bisnis proses, peluang inovasi digital dalam pengelolaan bisnis bidang kesehatan yang memanfaatkan teknologi"),
    ("CPL10", "CPMK101", "Mampu menunjukkan sikap berjati diri islami berlandaskan nilai ahlus sunah waljamahah"),
    ("CPL10", "CPMK102", "Mampu menunjukkan sikap profesionalitas, integritas, yang dilengkapi dengan kemampuan komunikasi, kepemimpinan, bekerja sama dan bertanggung jawab"),
    ("CPL11", "CPMK111", "Mampu menunjukkan sikap taat hukum dan disiplin melalui internalisasi nilai, norma, etika akademik, semangat kemandirian, kejuangan, dan kewirausahaan"),
    ("CPL11", "CPMK112", "Mampu menunjukkan sikap menghargai keanekaragaman melalui internalisasi nilai, norma, etika akademik, semangat kemandirian, kejuangan, dan kewirausahaan"),
    ("CPL12", "CPMK121", "Mampu menunjukkan kinerja mandiri, bermutu, dan terukur dalam mengembangkan ilmu pengetahuan yang memperhatikan nilai humaniora sesuai bidang keahliannya"),
    ("CPL12", "CPMK122", "Mampu berfikir logis, kritis kinerja sistematis, dan inovatif, komunikatif dalam mengembangkan ilmu pengetahuan"),
    ("CPL13", "CPMK131", "Mampu mengkaji implikasi pengembangan ilmu pengetahuan dengan menerapkan keahliannya dalam rangka menghasilkan solusi"),
    ("CPL13", "CPMK132", "Mampu menyusun deskripsi saintifik hasil kajian dalam bentuk laporan ilmiah yang sahih dan original"),
    ("CPL13", "CPMK133", "Mampu memelihara serta mengembangan jaringan kerja dengan pembimbing, kolega, sejawat baik di dalam maupun di luar lembaga"),
    ("CPL14", "CPMK141", "Mampu melakukan evaluasi diri terhadap penyelesaian pekerjaan sebagai wujud tanggung jawab atas pencapaian hasil kelompok kerja"),
    ("CPL14", "CPMK142", "Mampu melakukan supervisi terhadap penyelesaian pekerjaan sebagai wujud tanggung jawab atas pencapaian hasil kelompok kerja"),
]


def seed_cpmk():
    """Seed 33 CPMK terikat pada CPL Prodi."""
    session = state.db
    cpl_map = {}
    for row in session.query(CPLProdi).all():
        cpl_map[row.kode] = row.id

    for cpl_kode, kode, deskripsi in CPMK_DATA:
        cpl_id = cpl_map.get(cpl_kode)
        if cpl_id is None:
            continue
        cpmk = CPMK(cpl_id=cpl_id, kode=kode, deskripsi=deskripsi)
        session.add(cpmk)

    session.flush()
