-- phpMyAdmin SQL Dump
-- version 5.2.3
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: May 27, 2026 at 05:23 PM
-- Server version: 8.4.3
-- PHP Version: 8.3.30

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `sistem_kurikulum_obe`
--

-- --------------------------------------------------------

--
-- Table structure for table `dokumen_bukti_fisik`
--

CREATE TABLE `dokumen_bukti_fisik` (
  `id_dokumen` int NOT NULL,
  `id_peninjauan` int NOT NULL,
  `nama_file` varchar(255) NOT NULL,
  `path_lokasi_file` varchar(255) NOT NULL,
  `ekstensi_file` varchar(10) NOT NULL,
  `uploaded_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `master_bahan_kajian`
--

CREATE TABLE `master_bahan_kajian` (
  `id_bk` int NOT NULL,
  `id_periode` int NOT NULL,
  `kode_bk` varchar(10) NOT NULL,
  `nama_bk` varchar(150) NOT NULL,
  `deskripsi_bk` text,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `master_cpl`
--

CREATE TABLE `master_cpl` (
  `id_cpl` int NOT NULL,
  `id_periode` int NOT NULL,
  `kode_cpl` varchar(10) NOT NULL,
  `deskripsi_cpl` text NOT NULL,
  `referensi_standar` varchar(100) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `master_cpmk`
--

CREATE TABLE `master_cpmk` (
  `id_cpmk` int NOT NULL,
  `id_mk` int NOT NULL,
  `id_cpl` int NOT NULL,
  `kode_cpmk` varchar(15) NOT NULL,
  `deskripsi_cpmk` text NOT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `master_fakultas`
--

CREATE TABLE `master_fakultas` (
  `id_fakultas` int NOT NULL,
  `id_universitas` int NOT NULL,
  `nama_fakultas` varchar(150) NOT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `master_komponen_asesmen`
--

CREATE TABLE `master_komponen_asesmen` (
  `id_asesmen` int NOT NULL,
  `id_sub_cpmk` int NOT NULL,
  `nama_komponen` varchar(100) NOT NULL,
  `teknik_penilaian` varchar(100) NOT NULL,
  `bobot_persen` decimal(5,2) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `master_mata_kuliah`
--

CREATE TABLE `master_mata_kuliah` (
  `id_mk` int NOT NULL,
  `id_prodi` int NOT NULL,
  `kode_mk` varchar(15) NOT NULL,
  `nama_mk` varchar(150) NOT NULL,
  `bobot_sks` int NOT NULL,
  `semester_penempatan` int NOT NULL,
  `is_capstone` tinyint(1) DEFAULT '0',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `master_periode_kurikulum`
--

CREATE TABLE `master_periode_kurikulum` (
  `id_periode` int NOT NULL,
  `id_prodi` int NOT NULL,
  `tahun_mulai` year NOT NULL,
  `tahun_selesai` year NOT NULL,
  `status_aktif` tinyint(1) DEFAULT '1',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `master_pl`
--

CREATE TABLE `master_pl` (
  `id_pl` int NOT NULL,
  `id_periode` int NOT NULL,
  `kode_pl` varchar(10) NOT NULL,
  `deskripsi_pl` text NOT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `master_prodi`
--

CREATE TABLE `master_prodi` (
  `id_prodi` int NOT NULL,
  `id_fakultas` int NOT NULL,
  `nama_prodi` varchar(150) NOT NULL,
  `jenjang_pendidikan` varchar(10) NOT NULL,
  `gelar_lulusan` varchar(50) NOT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `master_sub_cpmk`
--

CREATE TABLE `master_sub_cpmk` (
  `id_sub_cpmk` int NOT NULL,
  `id_cpmk` int NOT NULL,
  `kode_sub_cpmk` varchar(20) NOT NULL,
  `deskripsi_sub_cpmk` text NOT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `master_universitas`
--

CREATE TABLE `master_universitas` (
  `id_universitas` int NOT NULL,
  `nama_universitas` varchar(150) NOT NULL,
  `alamat_universitas` text,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `relasi_bk_mk`
--

CREATE TABLE `relasi_bk_mk` (
  `id_bk` int NOT NULL,
  `id_mk` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `relasi_cpl_bk`
--

CREATE TABLE `relasi_cpl_bk` (
  `id_cpl` int NOT NULL,
  `id_bk` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `relasi_cpl_mk`
--

CREATE TABLE `relasi_cpl_mk` (
  `id_cpl` int NOT NULL,
  `id_mk` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `relasi_cpl_pl`
--

CREATE TABLE `relasi_cpl_pl` (
  `id_cpl` int NOT NULL,
  `id_pl` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `transaksi_nilai_aktivitas`
--

CREATE TABLE `transaksi_nilai_aktivitas` (
  `id_nilai` bigint NOT NULL,
  `id_asesmen` int NOT NULL,
  `nim_mahasiswa` varchar(30) NOT NULL,
  `nama_mahasiswa` varchar(150) NOT NULL,
  `nilai_mentah` decimal(5,2) NOT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `transaksi_peninjauan_kurikulum`
--

CREATE TABLE `transaksi_peninjauan_kurikulum` (
  `id_peninjauan` int NOT NULL,
  `id_periode` int NOT NULL,
  `nama_kegiatan` varchar(255) NOT NULL,
  `tanggal_rapat` date NOT NULL,
  `rekomendasi_hasil` text NOT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `dokumen_bukti_fisik`
--
ALTER TABLE `dokumen_bukti_fisik`
  ADD PRIMARY KEY (`id_dokumen`),
  ADD KEY `fk_bukti_ke_peninjauan` (`id_peninjauan`);

--
-- Indexes for table `master_bahan_kajian`
--
ALTER TABLE `master_bahan_kajian`
  ADD PRIMARY KEY (`id_bk`),
  ADD KEY `fk_bk_periode` (`id_periode`);

--
-- Indexes for table `master_cpl`
--
ALTER TABLE `master_cpl`
  ADD PRIMARY KEY (`id_cpl`),
  ADD KEY `fk_cpl_periode` (`id_periode`);

--
-- Indexes for table `master_cpmk`
--
ALTER TABLE `master_cpmk`
  ADD PRIMARY KEY (`id_cpmk`),
  ADD KEY `fk_cpmk_mk` (`id_mk`),
  ADD KEY `fk_cpmk_cpl` (`id_cpl`);

--
-- Indexes for table `master_fakultas`
--
ALTER TABLE `master_fakultas`
  ADD PRIMARY KEY (`id_fakultas`),
  ADD KEY `fk_fakultas_universitas` (`id_universitas`);

--
-- Indexes for table `master_komponen_asesmen`
--
ALTER TABLE `master_komponen_asesmen`
  ADD PRIMARY KEY (`id_asesmen`),
  ADD KEY `fk_asesmen_sub_cpmk` (`id_sub_cpmk`);

--
-- Indexes for table `master_mata_kuliah`
--
ALTER TABLE `master_mata_kuliah`
  ADD PRIMARY KEY (`id_mk`),
  ADD KEY `fk_mk_prodi` (`id_prodi`);

--
-- Indexes for table `master_periode_kurikulum`
--
ALTER TABLE `master_periode_kurikulum`
  ADD PRIMARY KEY (`id_periode`),
  ADD KEY `fk_periode_prodi` (`id_prodi`);

--
-- Indexes for table `master_pl`
--
ALTER TABLE `master_pl`
  ADD PRIMARY KEY (`id_pl`),
  ADD KEY `fk_pl_periode` (`id_periode`);

--
-- Indexes for table `master_prodi`
--
ALTER TABLE `master_prodi`
  ADD PRIMARY KEY (`id_prodi`),
  ADD KEY `fk_prodi_fakultas` (`id_fakultas`);

--
-- Indexes for table `master_sub_cpmk`
--
ALTER TABLE `master_sub_cpmk`
  ADD PRIMARY KEY (`id_sub_cpmk`),
  ADD KEY `fk_sub_cpmk_parent` (`id_cpmk`);

--
-- Indexes for table `master_universitas`
--
ALTER TABLE `master_universitas`
  ADD PRIMARY KEY (`id_universitas`);

--
-- Indexes for table `relasi_bk_mk`
--
ALTER TABLE `relasi_bk_mk`
  ADD PRIMARY KEY (`id_bk`,`id_mk`),
  ADD KEY `fk_pivot_mk_to_bk` (`id_mk`);

--
-- Indexes for table `relasi_cpl_bk`
--
ALTER TABLE `relasi_cpl_bk`
  ADD PRIMARY KEY (`id_cpl`,`id_bk`),
  ADD KEY `fk_pivot_bk_to_cpl` (`id_bk`);

--
-- Indexes for table `relasi_cpl_mk`
--
ALTER TABLE `relasi_cpl_mk`
  ADD PRIMARY KEY (`id_cpl`,`id_mk`),
  ADD KEY `fk_pivot_mk_to_cpl` (`id_mk`);

--
-- Indexes for table `relasi_cpl_pl`
--
ALTER TABLE `relasi_cpl_pl`
  ADD PRIMARY KEY (`id_cpl`,`id_pl`),
  ADD KEY `fk_pivot_pl_to_cpl` (`id_pl`);

--
-- Indexes for table `transaksi_nilai_aktivitas`
--
ALTER TABLE `transaksi_nilai_aktivitas`
  ADD PRIMARY KEY (`id_nilai`),
  ADD KEY `fk_nilai_ke_asesmen` (`id_asesmen`);

--
-- Indexes for table `transaksi_peninjauan_kurikulum`
--
ALTER TABLE `transaksi_peninjauan_kurikulum`
  ADD PRIMARY KEY (`id_peninjauan`),
  ADD KEY `fk_peninjauan_periode` (`id_periode`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `dokumen_bukti_fisik`
--
ALTER TABLE `dokumen_bukti_fisik`
  MODIFY `id_dokumen` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `master_bahan_kajian`
--
ALTER TABLE `master_bahan_kajian`
  MODIFY `id_bk` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `master_cpl`
--
ALTER TABLE `master_cpl`
  MODIFY `id_cpl` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `master_cpmk`
--
ALTER TABLE `master_cpmk`
  MODIFY `id_cpmk` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `master_fakultas`
--
ALTER TABLE `master_fakultas`
  MODIFY `id_fakultas` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `master_komponen_asesmen`
--
ALTER TABLE `master_komponen_asesmen`
  MODIFY `id_asesmen` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `master_mata_kuliah`
--
ALTER TABLE `master_mata_kuliah`
  MODIFY `id_mk` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `master_periode_kurikulum`
--
ALTER TABLE `master_periode_kurikulum`
  MODIFY `id_periode` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `master_pl`
--
ALTER TABLE `master_pl`
  MODIFY `id_pl` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `master_prodi`
--
ALTER TABLE `master_prodi`
  MODIFY `id_prodi` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `master_sub_cpmk`
--
ALTER TABLE `master_sub_cpmk`
  MODIFY `id_sub_cpmk` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `master_universitas`
--
ALTER TABLE `master_universitas`
  MODIFY `id_universitas` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `transaksi_nilai_aktivitas`
--
ALTER TABLE `transaksi_nilai_aktivitas`
  MODIFY `id_nilai` bigint NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `transaksi_peninjauan_kurikulum`
--
ALTER TABLE `transaksi_peninjauan_kurikulum`
  MODIFY `id_peninjauan` int NOT NULL AUTO_INCREMENT;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `dokumen_bukti_fisik`
--
ALTER TABLE `dokumen_bukti_fisik`
  ADD CONSTRAINT `fk_bukti_ke_peninjauan` FOREIGN KEY (`id_peninjauan`) REFERENCES `transaksi_peninjauan_kurikulum` (`id_peninjauan`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `master_bahan_kajian`
--
ALTER TABLE `master_bahan_kajian`
  ADD CONSTRAINT `fk_bk_periode` FOREIGN KEY (`id_periode`) REFERENCES `master_periode_kurikulum` (`id_periode`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `master_cpl`
--
ALTER TABLE `master_cpl`
  ADD CONSTRAINT `fk_cpl_periode` FOREIGN KEY (`id_periode`) REFERENCES `master_periode_kurikulum` (`id_periode`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `master_cpmk`
--
ALTER TABLE `master_cpmk`
  ADD CONSTRAINT `fk_cpmk_cpl` FOREIGN KEY (`id_cpl`) REFERENCES `master_cpl` (`id_cpl`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_cpmk_mk` FOREIGN KEY (`id_mk`) REFERENCES `master_mata_kuliah` (`id_mk`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `master_fakultas`
--
ALTER TABLE `master_fakultas`
  ADD CONSTRAINT `fk_fakultas_universitas` FOREIGN KEY (`id_universitas`) REFERENCES `master_universitas` (`id_universitas`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `master_komponen_asesmen`
--
ALTER TABLE `master_komponen_asesmen`
  ADD CONSTRAINT `fk_asesmen_sub_cpmk` FOREIGN KEY (`id_sub_cpmk`) REFERENCES `master_sub_cpmk` (`id_sub_cpmk`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `master_mata_kuliah`
--
ALTER TABLE `master_mata_kuliah`
  ADD CONSTRAINT `fk_mk_prodi` FOREIGN KEY (`id_prodi`) REFERENCES `master_prodi` (`id_prodi`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `master_periode_kurikulum`
--
ALTER TABLE `master_periode_kurikulum`
  ADD CONSTRAINT `fk_periode_prodi` FOREIGN KEY (`id_prodi`) REFERENCES `master_prodi` (`id_prodi`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `master_pl`
--
ALTER TABLE `master_pl`
  ADD CONSTRAINT `fk_pl_periode` FOREIGN KEY (`id_periode`) REFERENCES `master_periode_kurikulum` (`id_periode`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `master_prodi`
--
ALTER TABLE `master_prodi`
  ADD CONSTRAINT `fk_prodi_fakultas` FOREIGN KEY (`id_fakultas`) REFERENCES `master_fakultas` (`id_fakultas`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `master_sub_cpmk`
--
ALTER TABLE `master_sub_cpmk`
  ADD CONSTRAINT `fk_sub_cpmk_parent` FOREIGN KEY (`id_cpmk`) REFERENCES `master_cpmk` (`id_cpmk`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `relasi_bk_mk`
--
ALTER TABLE `relasi_bk_mk`
  ADD CONSTRAINT `fk_pivot_bk_to_mk` FOREIGN KEY (`id_bk`) REFERENCES `master_bahan_kajian` (`id_bk`) ON DELETE CASCADE,
  ADD CONSTRAINT `fk_pivot_mk_to_bk` FOREIGN KEY (`id_mk`) REFERENCES `master_mata_kuliah` (`id_mk`) ON DELETE CASCADE;

--
-- Constraints for table `relasi_cpl_bk`
--
ALTER TABLE `relasi_cpl_bk`
  ADD CONSTRAINT `fk_pivot_bk_to_cpl` FOREIGN KEY (`id_bk`) REFERENCES `master_bahan_kajian` (`id_bk`) ON DELETE CASCADE,
  ADD CONSTRAINT `fk_pivot_cpl_to_bk` FOREIGN KEY (`id_cpl`) REFERENCES `master_cpl` (`id_cpl`) ON DELETE CASCADE;

--
-- Constraints for table `relasi_cpl_mk`
--
ALTER TABLE `relasi_cpl_mk`
  ADD CONSTRAINT `fk_pivot_cpl_to_mk` FOREIGN KEY (`id_cpl`) REFERENCES `master_cpl` (`id_cpl`) ON DELETE CASCADE,
  ADD CONSTRAINT `fk_pivot_mk_to_cpl` FOREIGN KEY (`id_mk`) REFERENCES `master_mata_kuliah` (`id_mk`) ON DELETE CASCADE;

--
-- Constraints for table `relasi_cpl_pl`
--
ALTER TABLE `relasi_cpl_pl`
  ADD CONSTRAINT `fk_pivot_cpl_to_pl` FOREIGN KEY (`id_cpl`) REFERENCES `master_cpl` (`id_cpl`) ON DELETE CASCADE,
  ADD CONSTRAINT `fk_pivot_pl_to_cpl` FOREIGN KEY (`id_pl`) REFERENCES `master_pl` (`id_pl`) ON DELETE CASCADE;

--
-- Constraints for table `transaksi_nilai_aktivitas`
--
ALTER TABLE `transaksi_nilai_aktivitas`
  ADD CONSTRAINT `fk_nilai_ke_asesmen` FOREIGN KEY (`id_asesmen`) REFERENCES `master_komponen_asesmen` (`id_asesmen`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `transaksi_peninjauan_kurikulum`
--
ALTER TABLE `transaksi_peninjauan_kurikulum`
  ADD CONSTRAINT `fk_peninjauan_periode` FOREIGN KEY (`id_periode`) REFERENCES `master_periode_kurikulum` (`id_periode`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
