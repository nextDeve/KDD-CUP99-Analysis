import featureMap from "@/assets/featureMap";
import labelMap from "@/assets/labelMap";
const state = {
    selectInfo: [],
    featureMap,
    isSingleAnalyzed: false,
    isMultiAnalyzed: false,
    cof: [],
    label: [],
    features: [],
    singlePredict: -1,
    singlePredictProb: [],
    multiPredict: [],
    multiPredictProb: [],
    labelMap
};
const mutations = {
    CHANGESELECTED(state, selectInfo) {
        state.selectInfo = selectInfo
    },
    SAVESINGLERESPONSE(state, { cof, predict, predict_prob, label, features }) {
        state.cof = cof
        state.singlePredict = predict
        state.singlePredictProb = predict_prob
        state.label = label
        state.features = features

    },
    CHANGESINGLESTATE(state, isAnalyzed) {
        state.isSingleAnalyzed = isAnalyzed;
        state.isMultiAnalyzed = false;
    },
    CHANGEMULTISTATE(state, isAnalyzed) {
        state.isMultiAnalyzed = isAnalyzed;
        state.isSingleAnalyzed = false;
    },
    SAVEMULTIRESPONSE(state, { cof, predict, predict_prob, label, features }) {
        state.cof = cof
        state.multiPredict = predict
        state.multiPredictProb = predict_prob
        state.label = label
        state.features = features
    }
};
const actions = {
    changeSelected({ commit }, params) {
        commit('CHANGESELECTED', params)
    },
    saveSingelResponse({ commit }, params) {
        commit('SAVESINGLERESPONSE', params)
    },
    saveMultiResponse({ commit }, params) {
        commit('SAVEMULTIRESPONSE', params)

    }
};
const getters = {
    selectedInfo(state) {
        return state.selectInfo.filter((item) => item.selected)
    }
};
export default {
    state,
    mutations,
    actions,
    getters
}
