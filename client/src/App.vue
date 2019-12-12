<template>
  <div id="app">
    <p> Logged in: {{loggedIn}}</p>
    <router-link to="/register"><button>Register</button></router-link>
    <router-link to="/login"><button>Login</button></router-link>
    <img alt="logo" class="logo" src="./assets/images/podcast-icon-small.jpg">
    <router-view></router-view>
    <nav>
      <router-link to="/subscriptions"><img class="icon" src="./assets/images/my-list.png"/></router-link>
      <router-link to="/searchresults" @click="showSearch"><img class="icon" src="./assets/images/search.png"/></router-link>
      <router-link to="/browse"><img class="icon" src="./assets/images/browse.png"/></router-link>
    </nav>
  </div>
</template>


<script>
import Subscriptions from './components/Subscriptions.vue'
import SearchResults from './components/SearchResults.vue'
import Browse from './components/Browse.vue'
import Podcast from './components/Podcast.vue'
import Register from './components/Register.vue'
import Login from './components/Login.vue'
import axios from 'axios'

import { searchBus } from './main'
import { browseBus } from './main'

export default {
  name: 'app',
  data() {
    return{
      viewSubscriptions: false,
      viewSearch: false,
      viewBrowse: false,
      viewPodcast: false,
      viewRegister: false,
      viewLogin: false,

      podcastName: '',
      podcastFeedURL: '',

      loggedIn: false
    }
  },
  methods: {
    subscribeToPodcast(name, rss_feed_url){
      axios.post('/subscription', {name, rss_feed_url})
      .then(() => {
        this.$router.push('/subscriptions')
      })
    },
    viewThisPodcast(url, name) {
      this.podcastName = name
      this.podcastFeedURL = url
      this.$router.push('/podcast')
    },
    //The methods below simply show components and hide others when the user clicks on elements of the page.
    showSubscriptions(){
      this.viewSubscriptions = true;
      this.viewSearch = false;
      this.viewBrowse = false;
      this.viewPodcast = false;
      this.viewRegister = false;
      this.viewLogin = false;
    },
    showSearch(){
      this.viewSubscriptions = false;
      this.viewSearch = true;
      this.viewBrowse = false;
      this.viewPodcast = false;
      this.viewRegister = false;
      this.viewLogin = false;
      
    },
    showBrowse(){
      this.viewSubscriptions = false;
      this.viewSearch = false;
      this.viewBrowse = true;
      this.viewPodcast = false;
      this.viewRegister = false;
      this.viewLogin = false;
    },
    logout(){
      axios.post('/logout');
      this.loggedIn = false;
    }
  },
  created(){
    searchBus.$on('feedFromSearch', (url, name, isSubscribing) => {
      if (isSubscribing === true) {
        this.subscribeToPodcast(name, url)
        return
      }
      this.viewThisPodcast(url, name)
    }),
    browseBus.$on('feedFromBrowse', (url, name, isSubscribing) => {
      if (isSubscribing === true) {
        this.subscribeToPodcast(name, url)
        return
      }
    this.viewThisPodcast(url, name)
    })
  },
  components: {
    Subscriptions,
    Browse,
    SearchResults, 
    Podcast,
    Register,
    Login
  }
  
}
</script>

<style lang="css">
  /* import the google font and external stylesheet */
  @import url(https://fonts.googleapis.com/css?family=Raleway:400,600&display=swap);
  @import './assets/css/styles.css';
</style>


