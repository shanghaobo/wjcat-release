/**
 * 程序名：md5加密配置
 * 功能：md5加密配置
 */
import md5 from 'js-md5'
export default {
  install: function (Vue) {
    Object.defineProperty(Vue.prototype, '$md5', { value: md5 })
  }
}
