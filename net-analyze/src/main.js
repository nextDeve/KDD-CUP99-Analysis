import Vue from 'vue'
import App from './App.vue'
Vue.config.productionTip = false
import router from '@/router/index';
import store from '@/store/index';
import 'view-design/dist/styles/iview.css';
import { Button, Message } from 'view-design';
Vue.component('Button', Button);
new Vue({
  render: h => h(App),
  router,
  store,
  beforeCreate() {
    Vue.prototype.$Message = Message
    Vue.prototype.$bus = this
  }
}).$mount('#app')
