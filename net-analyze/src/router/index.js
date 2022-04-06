//引入Vue
import Vue from 'vue';
import VueRouter from 'vue-router';
Vue.use(VueRouter);

import routes from './routes'

const router = new VueRouter({
     //配置路由
     routes
});
export default router;
