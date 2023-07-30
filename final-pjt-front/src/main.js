import Vue from 'vue'
import App from './App.vue'
import router from './router'
import InfiniteLoading from 'vue-infinite-loading';

Vue.config.productionTip = false
Vue.use(InfiniteLoading, { /* options */ });
new Vue({
  router,
  render: h => h(App)
}).$mount('#app')
