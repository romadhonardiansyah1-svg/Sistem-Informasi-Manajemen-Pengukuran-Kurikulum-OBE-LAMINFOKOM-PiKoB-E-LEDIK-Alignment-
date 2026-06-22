"""
Seed data RPS (Rencana Pembelajaran Semester) dan Mahasiswa contoh.

Membuat dokumen RPS LENGKAP untuk sekumpulan MK inti lintas semester:
- Header RPS terisi penuh (dosen pengampu, deskripsi, pustaka, bobot SKS,
  media, prasyarat).
- Sub-CPMK dibuat (idempotent) untuk tiap CPMK yang terpetakan ke MK, agar
  rincian mingguan dapat menautkan sub_cpmk_id nyata.
- Rincian 16 minggu penuh (materi, bentuk pembelajaran, metode luring/daring,
  indikator, kriteria/teknik, bobot penilaian). Minggu 8 = UTS, minggu 16 = UAS.
  Total bobot penilaian seluruh minggu = 100.

Semua operasi idempotent (aman dijalankan berulang) melalui guard keberadaan.
"""

import state
from models.rps import RPS, RPSMinggu
from models.user import Mahasiswa, User
from models.mata_kuliah import MataKuliah
from models.cpmk import CPMK
from models.sub_cpmk import SubCPMK
from models.mapping import mapping_cpmk_mk
from services.auth_service import hash_password


# Rencana RPS per MK. topics = 14 materi untuk minggu 1-7 dan 9-15
# (minggu 8 = UTS, minggu 16 = UAS otomatis).
RPS_PLAN = [
    {
        "kode": "MK04",
        "dosen": "Dr. Ahmad Fauzi, M.Kom",
        "koordinator": "Dr. Ahmad Fauzi, M.Kom",
        "teori": 3, "praktikum": 0,
        "prasyarat": "-",
        "deskripsi": (
            "Mata kuliah ini membekali mahasiswa dengan pemahaman dasar konsep "
            "sistem informasi, komponen penyusun, serta peran strategisnya dalam "
            "mendukung proses bisnis dan pengambilan keputusan organisasi."
        ),
        "pustaka_utama": (
            "Laudon, K.C. & Laudon, J.P. (2022). Management Information Systems: "
            "Managing the Digital Firm, 17th ed. Pearson."
        ),
        "pustaka_pendukung": (
            "O'Brien, J.A. & Marakas, G.M. (2011). Management Information Systems, "
            "10th ed. McGraw-Hill."
        ),
        "topics": [
            "Pendahuluan, kontrak kuliah, dan ruang lingkup Sistem Informasi",
            "Konsep dasar data, informasi, pengetahuan, dan sistem",
            "Komponen dan klasifikasi Sistem Informasi",
            "Peran SI dalam organisasi dan keunggulan kompetitif",
            "Infrastruktur TI: perangkat keras dan perangkat lunak",
            "Basis data dan manajemen sumber daya informasi",
            "Telekomunikasi, jaringan, dan internet",
            "Sistem Informasi fungsional (SCM, CRM, ERP)",
            "E-business dan e-commerce",
            "Business intelligence dan dukungan keputusan",
            "Pengembangan sistem informasi",
            "Keamanan dan etika sistem informasi",
            "Tata kelola dan manajemen SI/TI",
            "Tren teknologi terkini dan studi kasus implementasi SI",
        ],
    },
    {
        "kode": "MK05",
        "dosen": "Siti Rahayu, S.Kom, M.T",
        "koordinator": "Dr. Ahmad Fauzi, M.Kom",
        "teori": 2, "praktikum": 1,
        "prasyarat": "-",
        "deskripsi": (
            "Mata kuliah ini mengajarkan dasar berpikir algoritmik dan penerapannya "
            "dalam bahasa pemrograman, mencakup struktur kontrol, struktur data dasar, "
            "fungsi, serta teknik pencarian dan pengurutan."
        ),
        "pustaka_utama": (
            "Cormen, T.H. et al. (2009). Introduction to Algorithms, 3rd ed. MIT Press."
        ),
        "pustaka_pendukung": (
            "Deitel, P. & Deitel, H. (2016). C How to Program, 8th ed. Pearson."
        ),
        "topics": [
            "Pendahuluan algoritma, flowchart, dan kontrak kuliah",
            "Tipe data, variabel, konstanta, dan operator",
            "Struktur input/output dan ekspresi",
            "Struktur kontrol percabangan (if, switch)",
            "Struktur kontrol perulangan (for, while, do-while)",
            "Array satu dimensi",
            "Array multidimensi dan manipulasi string",
            "Fungsi, prosedur, dan modularisasi program",
            "Parameter, ruang lingkup variabel, dan rekursi",
            "Algoritma pencarian (sequential dan binary search)",
            "Algoritma pengurutan (bubble, selection, insertion)",
            "Struktur data sederhana: stack dan queue",
            "Pemrosesan berkas (file processing)",
            "Studi kasus dan proyek pemrograman terapan",
        ],
    },
    {
        "kode": "MK11",
        "dosen": "Ir. Budi Santoso, M.Sc",
        "koordinator": "Dr. Ahmad Fauzi, M.Kom",
        "teori": 2, "praktikum": 0,
        "prasyarat": "MK04",
        "deskripsi": (
            "Mata kuliah ini membahas prinsip pengelolaan data organisasi, mulai dari "
            "pemodelan, normalisasi, manipulasi data dengan SQL, hingga tata kelola "
            "dan kualitas data."
        ),
        "pustaka_utama": (
            "Connolly, T. & Begg, C. (2015). Database Systems: A Practical Approach, "
            "6th ed. Pearson."
        ),
        "pustaka_pendukung": (
            "Hoffer, J.A. et al. (2016). Modern Database Management, 12th ed. Pearson."
        ),
        "topics": [
            "Pendahuluan dan konsep manajemen data",
            "Konsep basis data vs sistem berkas tradisional",
            "Model data dan Entity Relationship Diagram (ERD)",
            "Model relasional dan kunci (key)",
            "Normalisasi data (1NF s.d. 3NF)",
            "Bahasa query terstruktur (SQL) dasar",
            "Manipulasi data: INSERT, UPDATE, DELETE, SELECT",
            "Integritas dan keamanan data",
            "Transaksi dan kontrol konkurensi",
            "Tata kelola dan kualitas data",
            "Pengantar data warehouse",
            "Big data dan penyimpanan modern",
            "Backup, recovery, dan administrasi data",
            "Studi kasus pengelolaan data organisasi",
        ],
    },
    {
        "kode": "MK18",
        "dosen": "Dr. Rina Wijaya, M.Kom",
        "koordinator": "Dr. Ahmad Fauzi, M.Kom",
        "teori": 2, "praktikum": 1,
        "prasyarat": "MK05",
        "deskripsi": (
            "Mata kuliah ini membahas paradigma pemrograman berorientasi objek beserta "
            "penerapannya: kelas, objek, enkapsulasi, pewarisan, polimorfisme, hingga "
            "design pattern dan pengujian unit."
        ),
        "pustaka_utama": (
            "Horstmann, C.S. (2019). Core Java Volume I-Fundamentals, 11th ed. Pearson."
        ),
        "pustaka_pendukung": (
            "Gamma, E. et al. (1994). Design Patterns: Elements of Reusable "
            "Object-Oriented Software. Addison-Wesley."
        ),
        "topics": [
            "Pendahuluan dan paradigma pemrograman berorientasi objek",
            "Kelas (class) dan objek (object)",
            "Atribut, method, dan konstruktor",
            "Enkapsulasi dan access modifier",
            "Pewarisan (inheritance)",
            "Polimorfisme",
            "Abstraksi dan interface",
            "Penanganan kesalahan (exception handling)",
            "Collection dan generics",
            "Koneksi basis data berorientasi objek (JDBC/ORM)",
            "Perancangan antarmuka grafis berorientasi objek",
            "Design pattern dasar (Singleton, Factory, Observer)",
            "Pengujian unit pada aplikasi OOP",
            "Proyek aplikasi berorientasi objek",
        ],
    },
    {
        "kode": "MK19",
        "dosen": "Dr. Hendra Gunawan, M.Kom",
        "koordinator": "Dr. Hendra Gunawan, M.Kom",
        "teori": 3, "praktikum": 0,
        "prasyarat": "MK04",
        "deskripsi": (
            "Mata kuliah ini membekali kemampuan menganalisis kebutuhan dan merancang "
            "sistem informasi menggunakan pendekatan terstruktur dan berorientasi objek "
            "sepanjang siklus hidup pengembangan sistem."
        ),
        "pustaka_utama": (
            "Dennis, A. et al. (2015). Systems Analysis and Design, 6th ed. Wiley."
        ),
        "pustaka_pendukung": (
            "Satzinger, J.W. et al. (2016). Systems Analysis and Design in a Changing "
            "World, 7th ed. Cengage."
        ),
        "topics": [
            "Pendahuluan APSI dan System Development Life Cycle (SDLC)",
            "Identifikasi dan analisis kebutuhan sistem",
            "Teknik pengumpulan kebutuhan (wawancara, observasi, kuesioner)",
            "Pemodelan proses bisnis (BPMN)",
            "Use case dan skenario",
            "Diagram aktivitas dan sequence diagram",
            "Pemodelan data dan class diagram",
            "Perancangan antarmuka pengguna",
            "Perancangan basis data",
            "Perancangan arsitektur sistem",
            "Spesifikasi Kebutuhan Perangkat Lunak (SKPL)",
            "Estimasi dan manajemen proyek pengembangan",
            "Strategi implementasi dan pengujian",
            "Dokumentasi dan studi kasus perancangan sistem",
        ],
    },
    {
        "kode": "MK21",
        "dosen": "Ir. Budi Santoso, M.Sc",
        "koordinator": "Ir. Budi Santoso, M.Sc",
        "teori": 3, "praktikum": 1,
        "prasyarat": "MK11",
        "deskripsi": (
            "Mata kuliah ini membahas konsep dan implementasi sistem basis data secara "
            "mendalam, mencakup perancangan, SQL lanjutan, transaksi, optimasi, hingga "
            "basis data terdistribusi dan NoSQL."
        ),
        "pustaka_utama": (
            "Elmasri, R. & Navathe, S.B. (2016). Fundamentals of Database Systems, "
            "7th ed. Pearson."
        ),
        "pustaka_pendukung": (
            "Silberschatz, A. et al. (2019). Database System Concepts, 7th ed. "
            "McGraw-Hill."
        ),
        "topics": [
            "Pendahuluan sistem basis data dan kontrak kuliah",
            "Arsitektur DBMS dan model data",
            "Model relasional dan aljabar relasional",
            "Perancangan ERD dan pemetaan ke skema relasional",
            "Normalisasi lanjutan (BCNF, 4NF)",
            "SQL DDL dan DML lanjutan",
            "View, index, function, dan stored procedure",
            "Transaksi dan kontrol konkurensi",
            "Recovery dan backup basis data",
            "Keamanan dan otorisasi basis data",
            "Tuning dan optimasi query",
            "Basis data terdistribusi",
            "NoSQL dan basis data modern",
            "Administrasi basis data dan studi kasus",
        ],
    },
    {
        "kode": "MK22",
        "dosen": "Siti Rahayu, S.Kom, M.T",
        "koordinator": "Dr. Rina Wijaya, M.Kom",
        "teori": 2, "praktikum": 1,
        "prasyarat": "MK18",
        "deskripsi": (
            "Mata kuliah ini membekali kemampuan membangun aplikasi web dari sisi klien "
            "dan server, mencakup HTML/CSS/JavaScript, pemrograman server, basis data "
            "web, arsitektur MVC, REST API, dan keamanan aplikasi web."
        ),
        "pustaka_utama": (
            "Duckett, J. (2014). HTML and CSS: Design and Build Websites. Wiley."
        ),
        "pustaka_pendukung": (
            "Robbins, J.N. (2018). Learning Web Design, 5th ed. O'Reilly."
        ),
        "topics": [
            "Pendahuluan teknologi web dan arsitektur klien-server",
            "HTML dan struktur dokumen web",
            "CSS dan layout responsif",
            "JavaScript dasar",
            "Document Object Model (DOM) dan event handling",
            "Pemrograman sisi server",
            "Form dan validasi data",
            "Koneksi aplikasi web ke basis data",
            "Session, cookie, dan autentikasi",
            "Arsitektur Model-View-Controller (MVC)",
            "RESTful API",
            "Framework web modern",
            "Keamanan aplikasi web (OWASP)",
            "Proyek pengembangan aplikasi web",
        ],
    },
    {
        "kode": "MK23",
        "dosen": "Dr. Dewi Lestari, M.M",
        "koordinator": "Dr. Dewi Lestari, M.M",
        "teori": 3, "praktikum": 0,
        "prasyarat": "MK19",
        "deskripsi": (
            "Mata kuliah ini membahas konsep, teknik, dan metodologi manajemen proyek "
            "sistem informasi, mulai dari inisiasi, perencanaan, eksekusi, pengendalian, "
            "hingga penutupan proyek."
        ),
        "pustaka_utama": (
            "Schwalbe, K. (2018). Information Technology Project Management, 9th ed. "
            "Cengage."
        ),
        "pustaka_pendukung": (
            "PMI (2021). A Guide to the Project Management Body of Knowledge "
            "(PMBOK Guide), 7th ed."
        ),
        "topics": [
            "Pendahuluan manajemen proyek sistem informasi",
            "Siklus hidup dan metodologi proyek (waterfall, agile)",
            "Inisiasi dan studi kelayakan proyek",
            "Manajemen ruang lingkup (scope) proyek",
            "Manajemen waktu: WBS dan penjadwalan (Gantt, CPM)",
            "Manajemen biaya dan anggaran proyek",
            "Manajemen kualitas proyek",
            "Manajemen sumber daya manusia dan tim",
            "Manajemen risiko proyek",
            "Manajemen komunikasi dan stakeholder",
            "Manajemen pengadaan dan kontrak",
            "Eksekusi dan pengendalian proyek",
            "Penutupan proyek dan lesson learned",
            "Studi kasus dan alat bantu (MS Project)",
        ],
    },
    {
        "kode": "MK32",
        "dosen": "Dr. Hendra Gunawan, M.Kom",
        "koordinator": "Dr. Hendra Gunawan, M.Kom",
        "teori": 2, "praktikum": 1,
        "prasyarat": "MK21",
        "deskripsi": (
            "Mata kuliah ini membahas konsep dan teknik membangun data warehouse serta "
            "menambang pengetahuan dari data melalui klasifikasi, klastering, asosiasi, "
            "dan visualisasi hasil."
        ),
        "pustaka_utama": (
            "Han, J., Kamber, M. & Pei, J. (2011). Data Mining: Concepts and Techniques, "
            "3rd ed. Morgan Kaufmann."
        ),
        "pustaka_pendukung": (
            "Kimball, R. & Ross, M. (2013). The Data Warehouse Toolkit, 3rd ed. Wiley."
        ),
        "topics": [
            "Pendahuluan data warehouse dan data mining",
            "Arsitektur data warehouse",
            "Pemodelan dimensional (star dan snowflake schema)",
            "Proses Extract, Transform, Load (ETL)",
            "OLAP dan analisis multidimensi",
            "Praproses dan pembersihan data",
            "Klasifikasi (decision tree, naive bayes)",
            "Klastering (k-means, hierarchical)",
            "Aturan asosiasi dan pola sekuensial",
            "Evaluasi model dan validasi",
            "Visualisasi hasil data mining",
            "Text mining dan web mining",
            "Pengantar big data analytics",
            "Studi kasus dan proyek data mining",
        ],
    },
    {
        "kode": "MK34",
        "dosen": "Dr. Ahmad Fauzi, M.Kom",
        "koordinator": "Dr. Ahmad Fauzi, M.Kom",
        "teori": 1, "praktikum": 3,
        "prasyarat": "MK19, MK23",
        "deskripsi": (
            "Mata kuliah capstone yang mengintegrasikan kompetensi mahasiswa untuk "
            "merancang dan membangun solusi sistem informasi nyata secara berkelompok, "
            "mulai dari identifikasi masalah hingga presentasi akhir."
        ),
        "pustaka_utama": (
            "Sommerville, I. (2016). Software Engineering, 10th ed. Pearson."
        ),
        "pustaka_pendukung": (
            "Pressman, R.S. & Maxim, B.R. (2015). Software Engineering: A Practitioner's "
            "Approach, 8th ed. McGraw-Hill."
        ),
        "topics": [
            "Pendahuluan capstone dan pembentukan tim proyek",
            "Identifikasi masalah dan peluang",
            "Analisis kebutuhan stakeholder",
            "Perancangan solusi dan arsitektur sistem",
            "Perencanaan proyek dan timeline",
            "Pengembangan iterasi pertama",
            "Reviu progres dan umpan balik",
            "Pengembangan iterasi kedua",
            "Integrasi antar modul sistem",
            "Pengujian dan penjaminan mutu (QA)",
            "Deployment dan penyusunan dokumentasi",
            "Persiapan demo dan presentasi",
            "Evaluasi produk dan validasi pengguna",
            "Presentasi akhir dan serah terima produk",
        ],
    },
]


def _cpmk_ids_for_mk(mk_id):
    """Ambil daftar cpmk_id yang terpetakan ke sebuah MK (urut stabil)."""
    rows = state.db.execute(
        mapping_cpmk_mk.select().where(mapping_cpmk_mk.c.mk_id == mk_id)
    ).fetchall()
    return sorted({r.cpmk_id for r in rows})


def _ensure_sub_cpmk_for_mk(mk_id, cpmk_ids):
    """
    Pastikan ada Sub-CPMK untuk tiap CPMK yang terpetakan ke MK (idempotent).
    Return daftar id Sub-CPMK terurut untuk penautan rincian mingguan.
    """
    session = state.db
    sub_ids = []
    cpmk_map = {c.id: c for c in session.query(CPMK).filter(CPMK.id.in_(cpmk_ids)).all()} if cpmk_ids else {}

    for cpmk_id in cpmk_ids:
        cpmk = cpmk_map.get(cpmk_id)
        if cpmk is None:
            continue
        for n in (1, 2):
            kode = "Sub-{}.{}".format(cpmk.kode, n)
            existing = (
                session.query(SubCPMK)
                .filter_by(mk_id=mk_id, cpmk_id=cpmk_id, kode=kode)
                .first()
            )
            if existing is None:
                desc_dasar = (cpmk.deskripsi or "").strip()
                if len(desc_dasar) > 140:
                    desc_dasar = desc_dasar[:137] + "..."
                prefix = "Mampu memahami" if n == 1 else "Mampu menerapkan"
                existing = SubCPMK(
                    cpmk_id=cpmk_id,
                    mk_id=mk_id,
                    kode=kode,
                    deskripsi="{} bagian dari: {}".format(prefix, desc_dasar),
                )
                session.add(existing)
                session.flush()
            sub_ids.append(existing.id)
    return sub_ids


def _bobot_per_minggu():
    """
    Distribusi bobot penilaian 16 minggu, total = 100.
    UTS (minggu 8) = 25, UAS (minggu 16) = 30, sisanya dibagi rata ke 14 minggu.
    """
    bobot = [0.0] * 16
    bobot[7] = 25.0   # minggu ke-8 (UTS)
    bobot[15] = 30.0  # minggu ke-16 (UAS)
    sisa = 100.0 - 55.0
    content_weeks = [i for i in range(16) if i not in (7, 15)]
    per = round(sisa / len(content_weeks), 2)
    for i in content_weeks:
        bobot[i] = per
    # Koreksi pembulatan agar total tepat 100.
    selisih = round(100.0 - sum(bobot), 2)
    if abs(selisih) >= 0.01:
        bobot[content_weeks[0]] = round(bobot[content_weeks[0]] + selisih, 2)
    return bobot


def seed_rps(periode_id):
    """Seed dokumen RPS lengkap untuk MK inti lintas semester (idempotent)."""
    session = state.db
    if session.query(RPS).count() > 0:
        return

    mk_by_kode = {mk.kode: mk for mk in session.query(MataKuliah).all()}
    bobot_minggu = _bobot_per_minggu()

    for idx, plan in enumerate(RPS_PLAN):
        mk = mk_by_kode.get(plan["kode"])
        if mk is None:
            continue

        rps = RPS(
            mk_id=mk.id,
            periode_id=periode_id,
            kode_dokumen="RPS-SI-{}".format(str(idx + 1).zfill(3)),
            deskripsi_singkat=plan["deskripsi"],
            pustaka_utama=plan["pustaka_utama"],
            pustaka_pendukung=plan["pustaka_pendukung"],
            dosen_pengampu=plan["dosen"],
            dosen_koordinator=plan["koordinator"],
            tanggal_penyusunan="2024-08-15",
            bobot_teori_sks=plan["teori"],
            bobot_praktikum_sks=plan["praktikum"],
            media_software="LMS, MS Office, Browser Web, IDE/aplikasi terkait MK",
            media_hardware="Komputer/Laptop, LCD Projector, Jaringan Internet",
            mk_prasyarat=plan["prasyarat"],
        )
        session.add(rps)
        session.flush()

        cpmk_ids = _cpmk_ids_for_mk(mk.id)
        sub_ids = _ensure_sub_cpmk_for_mk(mk.id, cpmk_ids)

        topics = plan["topics"]  # 14 materi untuk minggu non-ujian
        topic_iter = iter(topics)
        sub_pos = 0

        for minggu in range(1, 17):
            if minggu == 8:
                materi = "Ujian Tengah Semester (UTS) — evaluasi materi minggu 1-7"
                bentuk = "Ujian tertulis"
                metode_luring = "Ujian tertulis terjadwal di kelas"
                metode_daring = "Ujian daring melalui LMS (bila diperlukan)"
                indikator = "Ketepatan menjawab soal yang mencakup capaian minggu 1-7"
                kriteria = "Tes tulis UTS; rubrik analitik; kunci jawaban"
                sub_cpmk_id = None
            elif minggu == 16:
                materi = "Ujian Akhir Semester (UAS) — evaluasi materi minggu 9-15"
                bentuk = "Ujian tertulis"
                metode_luring = "Ujian tertulis terjadwal di kelas"
                metode_daring = "Ujian daring melalui LMS (bila diperlukan)"
                indikator = "Ketepatan menjawab soal yang mencakup capaian minggu 9-15"
                kriteria = "Tes tulis UAS; rubrik analitik; kunci jawaban"
                sub_cpmk_id = None
            else:
                materi = next(topic_iter)
                bentuk = "Kuliah, diskusi, dan studi kasus" + (
                    ", praktik/responsi" if plan["praktikum"] > 0 else ""
                )
                metode_luring = "Ceramah, diskusi kelompok, dan latihan terbimbing"
                metode_daring = "Materi dan kuis asinkron melalui LMS"
                indikator = "Mahasiswa mampu menjelaskan dan menerapkan: " + materi
                kriteria = (
                    "Partisipasi, tugas, dan unjuk kerja; rubrik analitik; "
                    "ketepatan dan kelengkapan"
                )
                sub_cpmk_id = sub_ids[sub_pos % len(sub_ids)] if sub_ids else None
                sub_pos += 1

            session.add(RPSMinggu(
                rps_id=rps.id,
                minggu_ke=minggu,
                sub_cpmk_id=sub_cpmk_id,
                bentuk_pembelajaran=bentuk,
                metode_luring=metode_luring,
                metode_daring=metode_daring,
                materi=materi,
                bobot_penilaian_persen=bobot_minggu[minggu - 1],
                indikator=indikator,
                kriteria_teknik=kriteria,
            ))

    session.flush()


def seed_mahasiswa(prodi_id):
    """
    Seed 5 mahasiswa contoh + akun login masing-masing (idempotent).
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
        # Idempotent: lewati bila data mahasiswa dengan NIM ini sudah ada.
        if session.query(Mahasiswa).filter_by(nim=nim).first() is not None:
            continue

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
