/**
 * Client-side page loader menggunakan dispatch table.
 * Tidak ada if-else untuk routing.
 */
var Router = (function () {

    var PAGE_REGISTRY = {
        "dashboard":        { loader: "DashboardPage",  title: "Dashboard" },
        "identitas-prodi":  { loader: "IdentitasPage",  title: "Identitas Program Studi" },
        "master-pl":        { loader: "MasterDataPage", title: "Profil Lulusan",             entity: "pl",   endpoint: "/api/pl" },
        "master-cpl":       { loader: "MasterDataPage", title: "CPL Prodi",                  entity: "cpl",  endpoint: "/api/cpl-prodi" },
        "master-bk":        { loader: "MasterDataPage", title: "Bahan Kajian",               entity: "bk",   endpoint: "/api/bk" },
        "master-mk":        { loader: "MasterDataPage", title: "Mata Kuliah",                entity: "mk",   endpoint: "/api/mk" },
        "master-cpmk":      { loader: "MasterDataPage", title: "CPMK",                       entity: "cpmk", endpoint: "/api/cpmk" },
        "matrix-cpl-pl":    { loader: "MatrixPage",     title: "Matriks CPL - PL",           type: "cpl_pl" },
        "matrix-cpl-bk":    { loader: "MatrixPage",     title: "Matriks CPL - BK",           type: "cpl_bk" },
        "matrix-bk-mk":     { loader: "MatrixPage",     title: "Matriks BK - MK",            type: "bk_mk" },
        "matrix-cpl-mk":    { loader: "MatrixPage",     title: "Matriks CPL - MK",           type: "cpl_mk" },
        "matrix-cpmk-mk":   { loader: "MatrixPage",     title: "Matriks CPMK - MK",          type: "cpmk_mk" },
        "pemetaan-cpl-bk-mk": { loader: "PemetaanPage", title: "Pemetaan CPL - BK - MK" },
        "organisasi-mk":    { loader: "OrganisasiPage", title: "Organisasi Mata Kuliah" },
        "peta-cpl":         { loader: "PetaCplPage",    title: "Peta Pemenuhan CPL" },
        "mk-subcpmk":       { loader: "MkSubcpmkPage",  title: "Pemetaan MK - CPMK - Sub CPMK" },
        "rumusan-mk":       { loader: "RumusanPage",    title: "Rumusan Akhir MK",           rumusanType: "rumusan-mk" },
        "rumusan-cpl":      { loader: "RumusanPage",    title: "Rumusan Akhir CPL",          rumusanType: "rumusan-cpl" },
        "rps":              { loader: "RPSPage",        title: "Rencana Pembelajaran Semester" },
        "penilaian":        { loader: "PenilaianPage",  title: "Penilaian" },
        "nilai":            { loader: "NilaiPage",      title: "Input Nilai" },
        "report":           { loader: "ReportPage",     title: "Laporan CPL" },
        "mahasiswa-report": { loader: "MahasiswaReportPage", title: "Laporan Capaian Saya" },
        "agenda":           { loader: "AgendaPage",     title: "Agenda & Dokumen Mutu" },
        "log-peninjauan":   { loader: "AgendaPage",     title: "Agenda & Dokumen Mutu" },
        "user-management":  { loader: "UserManagementPage", title: "Manajemen Pengguna" },
    };

    function navigateTo(pageKey) {
        var entry = PAGE_REGISTRY[pageKey];
        if (!entry) {
            console.warn("Halaman tidak ditemukan: " + pageKey);
            return;
        }

        AppState.activePage = pageKey;
        document.getElementById("page-title").textContent = entry.title;

        var loaderName = entry.loader;
        var loaderObj = window[loaderName];
        if (loaderObj && typeof loaderObj.init === "function") {
            loaderObj.init(entry);
        }

        EventBus.emit("page:changed", pageKey);
    }

    function init(user) {
        // Tentukan halaman awal sesuai role/hak akses.
        var actions = (user && user.allowed_actions) || [];
        var landing = "dashboard";
        if (user && user.role === "mahasiswa") {
            landing = "mahasiswa-report";
        } else if (actions.indexOf("view_kurikulum") === -1) {
            if (actions.indexOf("view_report_self") !== -1) landing = "mahasiswa-report";
            else if (actions.indexOf("view_report") !== -1) landing = "report";
            else if (actions.indexOf("view_dokumen") !== -1) landing = "agenda";
        }
        navigateTo(landing);
    }

    return { navigateTo: navigateTo, init: init, registry: PAGE_REGISTRY };

})();

document.addEventListener("DOMContentLoaded", function () {
    Api.get("/api/auth/session").then(function (res) {
        if (res.status === "success") {
            AppState.user = res.data;
            HeaderComponent.init(res.data);
            SidebarComponent.init(res.data.role, res.data.allowed_actions);
            Router.init(res.data);
        }
    });
});
