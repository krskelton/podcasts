<template>
  <div id="app">
    <p>Logged in: {{ loggedIn }}</p>
    <router-link to="/register"><button>Register</button></router-link>
    <router-link to="/login"><button>Login</button></router-link>
    <button @click="logout">Log Out</button>

    <img alt="logo" class="logo" src="./assets/images/podcast-icon-small.jpg" />
    <router-view></router-view>
    <nav>
      <router-link to="/subscriptions"
        ><img class="icon" src="./assets/images/my-list.png"
      /></router-link>
      <router-link to="/searchresults"
        ><img class="icon" src="./assets/images/search.png"
      /></router-link>
      <router-link to="/browse"
        ><img class="icon" src="./assets/images/browse.png"
      /></router-link>
      <router-link to="/history"
        ><img class="icon" src="./assets/images/my_history.png"
      /></router-link>
    </nav>
  </div>
</template>

<script>
import Subscriptions from "./components/Subscriptions.vue";
import SearchResults from "./components/SearchResults.vue";
import Browse from "./components/Browse.vue";
import Podcast from "./components/Podcast.vue";
import Register from "./components/Register.vue";
import Login from "./components/Login.vue";
import History from "./components/History.vue";
import axios from "axios";

import { searchBus, browseBus, historyBus, podcastBus } from "./main";

export default {
  name: "app",
  data() {
    return {
      podcastName: "",
      podcastFeedURL: "",
      podcastAPIid: "",
      episodeTitle: "",
      timeDateAccessed: "",
      podcastId: "",
      loggedIn: false
    };
  },
  methods: {
    subscribeToPodcast(name, rss_feed_url, podcast_id) {
      axios
        .post("/subscription", { name, rss_feed_url, podcast_id })
        .then(() => {
          this.$router.push("/subscriptions");
        });
    },
    viewThisPodcast(name, url, id) {
      this.podcastName = name;
      this.podcastFeedURL = url;
      this.podcastId = id;
      this.$router.push("/podcast");
    },
    logout() {
      axios.post("/logout");
      this.loggedIn = false;
    },
    async testUserInSession() {
      /* hits backend and checks to see if a user is in session - adjusts this.loggedIn accordingly
      this ensures that the correct navbar buttons are displayed at all times */
      let promise = axios.post("/users").then(resp => {
        if (resp.data.success == false) {
          this.loggedIn = false;
          return false;
        }
        this.userInSession = resp.data.userInSession;
        this.loggedIn = true;
        return true;
      });
      // these lines ensure that the promise resolves before adjusting the value of this.loggedIn (accounts for asynch)
      let result = await promise;
      return result;
    }
  },
  created() {
    podcastBus.$on("feedFromPodcast", () => {
      this.subscribeToPodcast(this.podcastName, this.podcastFeedURL, this.podcastId)
    }),
    searchBus.$on("feedFromSearch", (name, url, podcast_id, isSubscribing) => {
      if (isSubscribing === true) {
        this.subscribeToPodcast(name, url, podcast_id);
        return;
      }
      this.viewThisPodcast(name, url, podcast_id);
    }),
    browseBus.$on("feedFromBrowse", (name, url, podcast_id, isSubscribing) => {
      if (isSubscribing === true) {
        this.subscribeToPodcast(name, url, podcast_id);
        return;
      }
      this.viewThisPodcast(name, url, podcast_id);
    })
  },
  components: {
    Subscriptions,
    Browse,
    SearchResults,
    Podcast,
    History,
    Register,
    Login
  },
  mounted() {
    this.testUserInSession();
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
