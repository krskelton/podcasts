<template>
  <div id="app">
    <p> Logged in: {{loggedIn}}</p>
    <router-link to="/register"><button>Register</button></router-link>
    <router-link to="/login"><button>Login</button></router-link>
    <button @click="logout">Log Out</button>
    <img alt="logo" class="logo" src="./assets/images/podcast-icon-small.jpg">
    <router-view></router-view>
    <h1>Podcasts</h1>
    <nav>
      <router-link to="/subscriptions"><img class="icon" src="./assets/images/my-list.png"/></router-link>
      <router-link to="/searchresults" @click="showSearch"><img class="icon" src="./assets/images/search.png"/></router-link>
      <router-link to="/browse"><img class="icon" src="./assets/images/browse.png"/></router-link>
      <!-- <router-link to="/playlists"><img class="icon" src="./assets/images/playlist.png"/></router-link> -->
      <!-- <button @click="showSubscriptions"><img class="icon" src="./assets/images/my-list.png"/></button>
      <button @click="showSearch"><img class="icon" src="./assets/images/search.png"/></button>
      <button @click="showBrowse"><img class="icon" src="./assets/images/browse.png"/></button> -->
    </nav>
    <div id="content">
      <!--If the parent receives data from the child it will have @feedfrom[nameofchild]. This is passing the podcast name and feed url to the parent so the parent can pass it to the podcast.vue child component since child components can't pass data directly to each other.-->
      <!-- <Register v-if="viewRegister" />
      <Login v-if="viewLogin" />
      <Subscriptions v-if="viewSubscriptions" @feedFromSubscription="subscriptionFeedRecieved"/>
      <SearchResults v-if="viewSearch" @feedFromSearch="searchFeedRecieved"/>
      <Browse v-if="viewBrowse" @feedFromBrowse="browseFeedRecieved"/>
      <Podcast v-if="viewPodcast" :podcastName="podcastName" :feedURL="podcastFeedURL" :podcastId="podcastId"/> -->
    </div>
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

import { searchBus, browseBus } from './main'

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
      podcastId: '',

      loggedIn: false
    }
  },
  methods: {
    //The feedRecieved methods get the feed url and podcast name from the SearchResults, Browse and Subscription components. They set the podcastName and podcastFeedURL from the data() above so that app.vue can pass those variables to podcast.vue.
    searchFeedRecieved(feedurl, podcastname, podcastId){
        this.podcastName = podcastname;
        this.podcastFeedURL = feedurl;
        this.podcastId = podcastId;
    },
    browseFeedRecieved(feedurl2, podcastname2, podcastId2){
        this.podcastName = podcastname2;
        this.podcastFeedURL = feedurl2;
        this.podcastId = podcastId2;
    },
    subscriptionFeedRecieved(feedurl3, podcastname3, podcastId3){
        this.podcastName = podcastname3;
        this.podcastFeedURL = feedurl3;
        this.podcastId = podcastId3;
    },
    // Moved this method here so that it can react to the bus.$emit from SearchResults.vue without needing to go through Podcast.vue.
    subscribeToPodcast(name, rss_feed_url, id){
      console.log("app.vue - post: ", name, rss_feed_url, id)
      axios.post('/subscription', {name, rss_feed_url, id})
      .then(() => {
        this.$router.push('/subscriptions')
      })
    },
    viewThisPodcast(url, name) {
      console.log("viewThisPodcast()")
      this.podcastName = name
      this.podcastFeedURL = url
      console.log(this.podcastName, this.podcastFeedURL)
      this.$router.push('/podcast')
    },
    //The methods below simply show components and hide others when the user clicks on elements of the page.
    showRegister(){
      this.viewSubscriptions = false;
      this.viewSearch = false;
      this.viewBrowse = false;
      this.viewPodcast = false;
      this.viewRegister = true;
      this.viewLogin = false;

    },
    showLogin(){
      this.viewSubscriptions = false;
      this.viewSearch = false;
      this.viewBrowse = false;
      this.viewPodcast = false;
      this.viewRegister = false;
      this.viewLogin = true;

    },
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
    },
    async testUserInSession() {
      /* hits backend and checks to see if a user is in session - adjusts this.loggedIn accordingly
      this ensures that the correct navbar buttons are displayed at all times */
      let promise = axios.post('/users')
      .then((resp) => {
        if (resp.data.success == false){
          this.loggedIn = false;
          return false;
        }
        this.userInSession = resp.data.userInSession;
        this.loggedIn = true;
        return true;
      })
      // these lines ensure that the promise resolves before adjusting the value of this.loggedIn (accounts for asynch)
      let result = await promise;
      console.log(result)
      return result;
    }
  },
  created(){
    searchBus.$on('feedFromSearch', (url, name, id) => {
      console.log("app.vue - searchBus arrived!")
      // this.searchFeedRecieved(url, name)
      this.subscribeToPodcast(name, url, id)
    }),
    browseBus.$on('feedFromBrowse', (url, name) => {
      console.log("app.vue = browseBus arrived!")
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
  },
  mounted(){
    this.testUserInSession()
  }
}
</script>

<style lang="css">
  /* import the google font and external stylesheet */
  @import url(https://fonts.googleapis.com/css?family=Raleway:400,600&display=swap);
  @import './assets/css/styles.css';
</style>


