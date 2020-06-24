/**
 * 程序名：Vue全局配置
 * 功能：Vue全局配置
 */
import Vue from "vue";
import App from "./App";
import router from "./router";
import ElementUI from "element-ui";
import "element-ui/lib/theme-chalk/index.css";
import VueClipboard from "vue-clipboard2";
import md5 from "./md5";

Vue.use(VueClipboard);
Vue.use(ElementUI);
Vue.use(md5);
Vue.config.productionTip = false;

/* eslint-disable no-new */
new Vue({
  el: "#app",
  router,
  components: { App },
  template: "<App/>"
});

//百度统计 id替换为自己的

var _hmt = _hmt || [];
window._hmt = _hmt;
(function() {
  var hm = document.createElement("script");
  hm.src = "https://hm.baidu.com/hm.js?9354205e2c5c77a15e07019792243422";
  var s = document.getElementsByTagName("script")[0];
  s.parentNode.insertBefore(hm, s);
})();

router.afterEach((to, from, next) => {
  setTimeout(() => {
    var _hmt = _hmt || [];
    (function() {
      //每次执行前，先移除上次插入的代码
      document.getElementById("baidu_tj") &&
        document.getElementById("baidu_tj").remove();
      var hm = document.createElement("script");
      hm.src = "https://hm.baidu.com/hm.js?9354205e2c5c77a15e07019792243422";
      hm.id = "baidu_tj";
      var s = document.getElementsByTagName("script")[0];
      s.parentNode.insertBefore(hm, s);
    })();
  }, 0);
});
