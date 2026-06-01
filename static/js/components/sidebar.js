/**
 * Sidebar navigation component.
 * Menu structure with inline SVG icons.
 */
var SidebarComponent = (function () {

    var ICON_MAP = {
        "identitas-prodi": '<svg viewBox="0 0 20 20" fill="currentColor"><path d="M10 9a3 3 0 100-6 3 3 0 000 6zm-7 9a7 7 0 1114 0H3z"/></svg>',
        "master-pl": '<svg viewBox="0 0 20 20" fill="currentColor"><path d="M9 2a1 1 0 000 2h2a1 1 0 100-2H9z"/><path fill-rule="evenodd" d="M4 5a2 2 0 012-2 3 3 0 003 3h2a3 3 0 003-3 2 2 0 012 2v11a2 2 0 01-2 2H6a2 2 0 01-2-2V5z" clip-rule="evenodd"/></svg>',
        "master-cpl": '<svg viewBox="0 0 20 20" fill="currentColor"><path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"/></svg>',
        "master-bk": '<svg viewBox="0 0 20 20" fill="currentColor"><path d="M9 4.804A7.968 7.968 0 005.5 4c-1.255 0-2.443.29-3.5.804v10A7.969 7.969 0 015.5 14c1.669 0 3.218.51 4.5 1.385A7.962 7.962 0 0114.5 14c1.255 0 2.443.29 3.5.804v-10A7.968 7.968 0 0014.5 4c-1.255 0-2.443.29-3.5.804V12a1 1 0 11-2 0V4.804z"/></svg>',
        "master-mk": '<svg viewBox="0 0 20 20" fill="currentColor"><path d="M7 3a1 1 0 000 2h6a1 1 0 100-2H7zM4 7a1 1 0 011-1h10a1 1 0 110 2H5a1 1 0 01-1-1zM2 11a2 2 0 012-2h12a2 2 0 012 2v4a2 2 0 01-2 2H4a2 2 0 01-2-2v-4z"/></svg>',
        "master-cpmk": '<svg viewBox="0 0 20 20" fill="currentColor"><path fill-rule="evenodd" d="M3 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm0 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm0 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm0 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1z" clip-rule="evenodd"/></svg>',
        "matrix": '<svg viewBox="0 0 20 20" fill="currentColor"><path fill-rule="evenodd" d="M5 4a3 3 0 00-3 3v6a3 3 0 003 3h10a3 3 0 003-3V7a3 3 0 00-3-3H5zm-1 9v-1h5v2H5a1 1 0 01-1-1zm7 1h4a1 1 0 001-1v-1h-5v2zm0-4h5V8h-5v2zM9 8H4v2h5V8z" clip-rule="evenodd"/></svg>',
        "pemetaan-cpl-bk-mk": '<svg viewBox="0 0 20 20" fill="currentColor"><path d="M5 3a2 2 0 00-2 2v2a2 2 0 002 2h2a2 2 0 002-2V5a2 2 0 00-2-2H5zM5 11a2 2 0 00-2 2v2a2 2 0 002 2h2a2 2 0 002-2v-2a2 2 0 00-2-2H5zM11 5a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2V5zM11 13a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2v-2z"/></svg>',
        "organisasi-mk": '<svg viewBox="0 0 20 20" fill="currentColor"><path d="M2 10a8 8 0 018-8v8h8a8 8 0 11-16 0z"/><path d="M12 2.252A8.014 8.014 0 0117.748 8H12V2.252z"/></svg>',
        "peta-cpl": '<svg viewBox="0 0 20 20" fill="currentColor"><path fill-rule="evenodd" d="M12 7a1 1 0 110-2h5a1 1 0 011 1v5a1 1 0 11-2 0V8.414l-4.293 4.293a1 1 0 01-1.414 0L8 10.414l-4.293 4.293a1 1 0 01-1.414-1.414l5-5a1 1 0 011.414 0L11 10.586 14.586 7H12z" clip-rule="evenodd"/></svg>',
        "mk-subcpmk": '<svg viewBox="0 0 20 20" fill="currentColor"><path d="M3 12v3c0 1.657 3.134 3 7 3s7-1.343 7-3v-3c0 1.657-3.134 3-7 3s-7-1.343-7-3z"/><path d="M3 7v3c0 1.657 3.134 3 7 3s7-1.343 7-3V7c0 1.657-3.134 3-7 3S3 8.657 3 7z"/><path d="M17 5c0 1.657-3.134 3-7 3S3 6.657 3 5s3.134-3 7-3 7 1.343 7 3z"/></svg>',
        "rps": '<svg viewBox="0 0 20 20" fill="currentColor"><path fill-rule="evenodd" d="M4 4a2 2 0 012-2h4.586A2 2 0 0112 2.586L15.414 6A2 2 0 0116 7.414V16a2 2 0 01-2 2H6a2 2 0 01-2-2V4z" clip-rule="evenodd"/></svg>',
        "penilaian": '<svg viewBox="0 0 20 20" fill="currentColor"><path d="M9 2a1 1 0 000 2h2a1 1 0 100-2H9z"/><path fill-rule="evenodd" d="M4 5a2 2 0 012-2 3 3 0 003 3h2a3 3 0 003-3 2 2 0 012 2v11a2 2 0 01-2 2H6a2 2 0 01-2-2V5zm9.707 5.707a1 1 0 00-1.414-1.414L9 12.586l-1.293-1.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"/></svg>',
        "rumusan": '<svg viewBox="0 0 20 20" fill="currentColor"><path fill-rule="evenodd" d="M6 2a2 2 0 00-2 2v12a2 2 0 002 2h8a2 2 0 002-2V7.414A2 2 0 0015.414 6L12 2.586A2 2 0 0010.586 2H6zm5 6a1 1 0 10-2 0v2H7a1 1 0 100 2h2v2a1 1 0 102 0v-2h2a1 1 0 100-2h-2V8z" clip-rule="evenodd"/></svg>',
        "nilai": '<svg viewBox="0 0 20 20" fill="currentColor"><path d="M5 4a1 1 0 00-2 0v7.268a2 2 0 000 3.464V16a1 1 0 102 0v-1.268a2 2 0 000-3.464V4zM11 4a1 1 0 10-2 0v1.268a2 2 0 000 3.464V16a1 1 0 102 0V8.732a2 2 0 000-3.464V4zM16 3a1 1 0 011 1v7.268a2 2 0 010 3.464V16a1 1 0 11-2 0v-1.268a2 2 0 010-3.464V4a1 1 0 011-1z"/></svg>',
        "report": '<svg viewBox="0 0 20 20" fill="currentColor"><path fill-rule="evenodd" d="M6 2a2 2 0 00-2 2v12a2 2 0 002 2h8a2 2 0 002-2V7.414A2 2 0 0015.414 6L12 2.586A2 2 0 0010.586 2H6zm2 10a1 1 0 10-2 0v3a1 1 0 102 0v-3zm2-3a1 1 0 011 1v5a1 1 0 11-2 0v-5a1 1 0 011-1zm4-1a1 1 0 10-2 0v7a1 1 0 102 0V8z" clip-rule="evenodd"/></svg>',
        "log-peninjauan": '<svg viewBox="0 0 20 20" fill="currentColor"><path fill-rule="evenodd" d="M18 13V5a2 2 0 00-2-2H4a2 2 0 00-2 2v8a2 2 0 002 2h3l3 3 3-3h3a2 2 0 002-2zM5 7a1 1 0 011-1h8a1 1 0 110 2H6a1 1 0 01-1-1zm1 3a1 1 0 100 2h3a1 1 0 100-2H6z" clip-rule="evenodd"/></svg>',
        "dashboard": '<svg viewBox="0 0 20 20" fill="currentColor"><path d="M10.707 2.293a1 1 0 00-1.414 0l-7 7a1 1 0 001.414 1.414L4 10.414V17a1 1 0 001 1h2a1 1 0 001-1v-2a1 1 0 011-1h2a1 1 0 011 1v2a1 1 0 001 1h2a1 1 0 001-1v-6.586l.293.293a1 1 0 001.414-1.414l-7-7z"/></svg>',
    };

    var MENU_STRUCTURE = [
        {
            section: "PLAN",
            items: [
                { key: "identitas-prodi",    label: "Identitas Prodi",            action: "view_all" },
                { key: "master-pl",          label: "Profil Lulusan",             action: "view_all" },
                { key: "master-cpl",         label: "CPL Prodi",                  action: "view_all" },
                { key: "master-bk",          label: "Bahan Kajian",               action: "view_all" },
                { key: "master-mk",          label: "Mata Kuliah",                action: "view_all" },
                { key: "master-cpmk",        label: "CPMK",                       action: "view_all" },
            ],
        },
        {
            section: "DO",
            items: [
                { key: "matrix-cpl-pl",    label: "Matriks CPL - PL",           action: "view_all",   icon: "matrix" },
                { key: "matrix-cpl-bk",    label: "Matriks CPL - BK",           action: "view_all",   icon: "matrix" },
                { key: "matrix-bk-mk",     label: "Matriks BK - MK",            action: "view_all",   icon: "matrix" },
                { key: "matrix-cpl-mk",    label: "Matriks CPL - MK",            action: "view_all",   icon: "matrix" },
                { key: "matrix-cpmk-mk",   label: "Matriks CPMK - MK",           action: "view_all",   icon: "matrix" },
                { key: "pemetaan-cpl-bk-mk", label: "Pemetaan CPL-BK-MK",       action: "view_all" },
                { key: "organisasi-mk",    label: "Organisasi MK",              action: "view_all" },
                { key: "peta-cpl",         label: "Peta Pemenuhan CPL",         action: "view_all" },
                { key: "mk-subcpmk",       label: "MK - CPMK - Sub CPMK",      action: "view_all" },
                { key: "rps",              label: "RPS",                        action: "view_all" },
            ],
        },
        {
            section: "CHECK",
            items: [
                { key: "penilaian",  label: "Penilaian dan Bobot",  action: "view_all" },
                { key: "rumusan-mk", label: "Rumusan Akhir MK",    action: "view_all",  icon: "rumusan" },
                { key: "rumusan-cpl",label: "Rumusan Akhir CPL",   action: "view_all",  icon: "rumusan" },
                { key: "nilai",      label: "Input Nilai",          action: "input_nilai" },
                { key: "report",     label: "Laporan CPL",          action: "view_report" },
            ],
        },
        {
            section: "ACTION",
            items: [
                { key: "log-peninjauan", label: "Log Peninjauan",     action: "view_all" },
            ],
        },
    ];

    function init(role) {
        var container = document.getElementById("sidebar-menu");
        container.innerHTML = "";

        var dashItem = _createItem({ key: "dashboard", label: "Dashboard", action: "view_all" });
        dashItem.style.marginBottom = "4px";
        container.appendChild(dashItem);

        for (var s = 0; s < MENU_STRUCTURE.length; s++) {
            var section = MENU_STRUCTURE[s];
            var sectionTitle = document.createElement("div");
            sectionTitle.className = "sidebar-section-title";
            sectionTitle.textContent = section.section;
            container.appendChild(sectionTitle);

            var sectionDiv = document.createElement("div");
            sectionDiv.className = "sidebar-section";

            for (var i = 0; i < section.items.length; i++) {
                var item = section.items[i];
                sectionDiv.appendChild(_createItem(item));
            }

            container.appendChild(sectionDiv);
        }
    }

    function _createItem(item) {
        var div = document.createElement("div");
        div.className = "sidebar-item";
        div.dataset.page = item.key;

        var iconKey = item.icon || item.key;
        var iconHtml = ICON_MAP[iconKey] || ICON_MAP["master-mk"];
        var iconSpan = document.createElement("span");
        iconSpan.className = "sidebar-item-icon";
        iconSpan.innerHTML = iconHtml;
        div.appendChild(iconSpan);

        var label = document.createElement("span");
        label.textContent = item.label;
        div.appendChild(label);

        div.addEventListener("click", function () {
            Router.navigateTo(item.key);
            _setActive(item.key);
        });

        return div;
    }

    function _setActive(key) {
        var items = document.querySelectorAll(".sidebar-item");
        for (var i = 0; i < items.length; i++) {
            items[i].classList.remove("active");
            if (items[i].dataset.page === key) {
                items[i].classList.add("active");
            }
        }
    }

    return { init: init };

})();
