/**
 * Frontend global state.
 * Seluruh data shared disimpan di AppState.
 */
var AppState = {
    user: null,
    currentPeriode: null,
    activePage: null,
    masterData: {
        pl: [],
        cpl: [],
        bk: [],
        mk: [],
        cpmk: [],
        sub_cpmk: [],
    },
    matrixCache: {},
    periodeList: [],
};
