import Vue from 'vue'
import Element from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'
import i18n from './lang' // 国际化
import App from './App'
import router from './router'
import store from './store'
import * as filters from './filters' // 全局filter
import './permission' // 权限
import './utils/jsArrayRemove'

Vue.use(Element, {
  i18n: (key, value) => i18n.t(key, value)
})

/* icon */
import 'vue-awesome/icons'
import Icon from 'vue-awesome/components/Icon'
Vue.component('icon', Icon)
import 'font-awesome/css/font-awesome.min.css'

/* markdown */
import mavonEditor from 'mavon-editor'
import 'mavon-editor/dist/css/index.css'
Vue.use(mavonEditor)

// register global utility filters.
Object.keys(filters).forEach(key => {
  Vue.filter(key, filters[key])
})

Vue.config.productionTip = false

new Vue({
  el: '#app',
  router,
  store,
  i18n,
  template: '<App/>',
  components: { App }
})
