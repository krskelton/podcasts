<template>
  <div id="app">
    <button @click="showRegister">Register</button>
    <button @click="showLogin">Login</button>
    <button @click="logout">Log Out</button>
    <img alt="logo" class="logo" src="./assets/images/podcast-icon-small.jpg" />
    <h1>Podcasts</h1>
    <div id="content">
      <!--If the parent receives data from the child it will have @feedfrom[nameofchild]. This is passing the podcast name and feed url to the parent so the parent can pass it to the podcast.vue child component since child components can't pass data directly to each other.-->
      <Register v-if="viewRegister" />
      <Login v-if="viewLogin" />
      <Subscriptions v-if="viewSubscriptions" @feedFromSubscription="subscriptionFeedRecieved" />
      <SearchResults v-if="viewSearch" @feedFromSearch="searchFeedRecieved" />
      <Browse v-if="viewBrowse" @feedFromBrowse="browseFeedRecieved" />
      <Podcast
        v-if="viewPodcast"
        :podcastName="podcastName"
        :feedURL="podcastFeedURL"
        :userID="userID"
      />
      <History v-if="viewHistory" />
    </div>
    <nav>
      <button @click="showSubscriptions">
        <img class="icon" src="./assets/images/my-list.png" />
      </button>
      <button @click="showSearch">
        <img class="icon" src="./assets/images/search.png" />
      </button>
      <button @click="showBrowse">
        <img class="icon" src="./assets/images/browse.png" />
      </button>
      <button @click="showHistory">
        <img class="icon" src="./assets/images/my_history.png" />
      </button>
    </nav>
  </div>
</template>


<script>
import History from "./components/History.vue";
import Subscriptions from "./components/Subscriptions.vue";
import SearchResults from "./components/SearchResults.vue";
import Browse from "./components/Browse.vue";
import Podcast from "./components/Podcast.vue";
import Register from "./components/Register.vue";
import Login from "./components/Login.vue";

import axios from "axios";

export default {
  name: "app",
  data() {
    return {
      viewSubscriptions: false,
      viewSearch: false,
      viewBrowse: false,
      viewPodcast: false,
      viewHistory: false,
      viewRegister: false,
      viewLogin: false,
      podcastName: "",
      podcastFeedURL: "",
      podcastAPIid: "",
      episodeTitle: "",
      timeDateAccessed: "12-4-19",

      loggedIn: false
    };
  },
  methods: {
    //The feedRecieved methods get the feed url and podcast name from the SearchResults, Browse and Subscription components. They set the podcastName and podcastFeedURL from the data() above so that app.vue can pass those variables to podcast.vue.
    searchFeedRecieved(feedurl, podcastname) {
      this.podcastName = podcastname;
      this.podcastFeedURL = feedurl;
      this.viewSearch = false;
      this.viewPodcast = true;
      this.viewRegister = false;
      this.viewLogin = false;
      this.viewHistory = false;
    },
    browseFeedRecieved(feedurl2, podcastname2) {
      this.podcastName = podcastname2;
      this.podcastFeedURL = feedurl2;
      this.viewBrowse = false;
      this.viewPodcast = true;
      this.viewRegister = false;
      this.viewLogin = false;
      this.viewHistory = false;
    },
    subscriptionFeedRecieved(feedurl3, podcastname3) {
      this.podcastName = podcastname3;
      this.podcastFeedURL = feedurl3;
      this.viewSubscriptions = false;
      this.viewPodcast = true;
      this.viewRegister = false;
      this.viewLogin = false;
      this.viewHistory = false;
    },
    //The methods below simply show components and hide others when the user clicks on elements of the page.
    showRegister() {
      this.viewSubscriptions = false;
      this.viewSearch = false;
      this.viewBrowse = false;
      this.viewPodcast = false;
      this.viewRegister = true;
      this.viewLogin = false;
      this.viewHistory = false;
    },
    showLogin() {
      this.viewSubscriptions = false;
      this.viewSearch = false;
      this.viewBrowse = false;
      this.viewPodcast = false;
      this.viewRegister = false;
      this.viewLogin = true;
      this.viewHistory = false;
    },
    showSubscriptions() {
      this.viewSubscriptions = true;
      this.viewSearch = false;
      this.viewBrowse = false;
      this.viewPodcast = false;
      this.viewHistory = false;
      this.viewRegister = false;
      this.viewLogin = false;
    },
    showSearch() {
      this.viewSubscriptions = false;
      this.viewSearch = true;
      this.viewBrowse = false;
      this.viewPodcast = false;
      this.viewHistory = false;
      this.viewRegister = false;
      this.viewLogin = false;
    },
    showBrowse() {
      this.viewSubscriptions = false;
      this.viewSearch = false;
      this.viewBrowse = true;
      this.viewPodcast = false;
      this.viewHistory = false;
    },
    showHistory() {
      this.viewSubscriptions = false;
      this.viewSearch = false;
      this.viewBrowse = false;
      this.viewPodcast = false;
      this.viewHistory = true;
      this.viewRegister = false;
      this.viewLogin = false;
    },
    logout() {
      axios.post("/logout");
      this.loggedIn = false;
    }
  },
  components: {
    Subscriptions,
    Browse,
    SearchResults,
    Podcast,
    History,
    Register,
    Login
  }
};
</script>

<style lang="css">
/* import the google font and external stylesheet */
@import url(
  https://fonts.googleapis.com/css?family=Raleway:400,
  600&display=swap
);
@import "./assets/css/styles.css";
</style>


