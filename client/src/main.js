import Vue from "vue";
import App from "./App.vue";
import VueRouter from "vue-router";
import Browse from "./components/Browse";
import Subscriptions from "./components/Subscriptions";
import SearchResults from "./components/SearchResults";
import Podcast from "./components/Podcast";
import Register from "./components/Register";
import Login from "./components/Login";
import History from "./components/History";
import Playlists from "./components/Playlists";

Vue.use(VueRouter);

export const searchBus = new Vue();
export const browseBus = new Vue();
export const historyBus = new Vue();
export const podcastBus = new Vue();
export const subscriptionBus = new Vue();
export const playlistBus = new Vue();

Vue.config.productionTip = false;

const router = new VueRouter({
  routes: [
    { path: "/browse", component: Browse },
    { path: "/subscriptions", component: Subscriptions },
    { path: "/searchresults", component: SearchResults },
    { path: "/podcast", component: Podcast },
    { path: "/register", component: Register },
    { path: "/login", component: Login },
    { path: "/history", component: History },
    { path: "/playlists", component: Playlists }
  ]
});

new Vue({
  router,
  render: h => h(App)
}).$mount("#app");
