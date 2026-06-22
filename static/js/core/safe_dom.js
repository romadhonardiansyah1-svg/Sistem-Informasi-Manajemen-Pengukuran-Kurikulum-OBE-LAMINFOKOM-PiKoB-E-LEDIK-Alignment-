/**
 * Penjaga DOM defensif.
 *
 * Memperbaiki crash "Failed to execute 'removeChild'/'insertBefore' on 'Node':
 * The node to be removed is not a child of this node."
 *
 * Penyebab umum: ekstensi penerjemah halaman (mis. Google Translate Chrome)
 * membungkus/menyisipkan node teks. Ketika aplikasi me-render ulang konten
 * dengan innerHTML, observer penerjemah mencoba menghapus node yang sudah
 * tergantikan, sehingga melempar error dan mematahkan UI.
 *
 * Solusi standar (dipakai luas, mis. di aplikasi React): bungkus removeChild
 * dan insertBefore agar tidak melempar bila node bukan anak dari parent yang
 * dimaksud — cukup kembalikan node tanpa membatalkan eksekusi.
 *
 * Harus dimuat PALING AWAL (sebelum script lain).
 */
(function () {
    if (typeof Node !== "function" || !Node.prototype) {
        return;
    }

    var origRemoveChild = Node.prototype.removeChild;
    Node.prototype.removeChild = function (child) {
        if (child && child.parentNode !== this) {
            if (typeof console !== "undefined" && console.warn) {
                console.warn("safe-dom: removeChild dilewati (node bukan anak dari parent ini).");
            }
            return child;
        }
        return origRemoveChild.apply(this, arguments);
    };

    var origInsertBefore = Node.prototype.insertBefore;
    Node.prototype.insertBefore = function (newNode, referenceNode) {
        if (referenceNode && referenceNode.parentNode !== this) {
            if (typeof console !== "undefined" && console.warn) {
                console.warn("safe-dom: insertBefore dialihkan ke appendChild (reference bukan anak dari parent ini).");
            }
            return this.appendChild(newNode);
        }
        return origInsertBefore.apply(this, arguments);
    };
})();
