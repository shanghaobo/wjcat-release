/**
 * 程序名：Vue全局配置
 * 功能：Vue全局配置
 */
import Vue from 'vue'
import App from './App'
import router from './router'
import ElementUI from 'element-ui';
import 'element-ui/lib/theme-chalk/index.css';
import VueClipboard from 'vue-clipboard2'
import md5 from './md5'


Vue.use(VueClipboard)
Vue.use(ElementUI);
Vue.use(md5);
Vue.config.productionTip = false

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  components: { App },
  template: '<App/>'
})
