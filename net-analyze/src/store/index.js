//仓库--vuex
import Vue from 'vue';
import Vuex from 'vuex';
Vue.use(Vuex);
import feature from './feature';
export default new Vuex.Store({
    modules: {
        feature,
    }
});
