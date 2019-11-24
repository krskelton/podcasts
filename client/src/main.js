import Vue from 'vue'
import App from './App.vue'
import VueRouter from 'vue-router'
import Browse from "./components/Browse"
import Subscriptions from "./components/Subscriptions"
import SearchResults from "./components/SearchResults"

Vue.use(VueRouter)

Vue.config.productionTip = false

const router = new VueRouter({
  routes: [
    { path: '/browse', component: Browse },
    { path: '/subscriptions', component: Subscriptions },
    { path: '/searchresults', component: SearchResults }
  ]
})

new Vue({
  router,
  render: h => h(App),
}).$mount('#app')
