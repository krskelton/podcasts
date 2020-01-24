<template>
  <div id="app" @click="$refs.subscriptionModal.style.display='none'">
    <p>Logged in: {{ loggedIn }}</p>
    <router-link to="/register">
      <button>Register</button>
    </router-link>
    <router-link to="/login">
      <button>Login</button>
    </router-link>
    <button @click="logout">Log Out</button>
    <div class="modal" ref="subscriptionModal">
      <!-- Modal content -->
      <div class="modal-content" ref="subscriptionModalContent">
        <div class="modal-body">
          <span @click="$refs.subscriptionModal.style.display='none'" class="close">&times;</span>
          <p>You're subscribed to {{ this.podcastName }}</p>
          <router-link to="/subscriptions">
            <button class="button">Visit Subscriptions Page</button>
          </router-link>
        </div>
      </div>
    </div>
    <div class="modal" ref="logoutModal">
      <!-- Modal content -->
      <div class="modal-content" ref="logoutModalContent">
        <div class="modal-body">
          <span @click="$refs.logoutModal.style.display='none'" class="close">&times;</span>
          <p>You're logged out!</p>
        </div>
      </div>
    </div>
    <div class="modal" ref="registerModal">
      <!-- Modal content -->
      <div class="modal-content" ref="registerModalContent">
        <div class="modal-body">
          <span @click="$refs.logoutModal.style.display='none'" class="close">&times;</span>
          <p>Thanks for registering, {{ this.userInSession }}. You're logged in!</p>
        </div>
      </div>
    </div>
    <div class="modal" ref="loginModal">
      <!-- Modal content -->
      <div class="modal-content" ref="loginModalContent">
        <div class="modal-body">
          <span @click="$refs.logoutModal.style.display='none'" class="close">&times;</span>
          <p>You're logged in, {{ this.userInSession }}.</p>
        </div>
      </div>
    </div>
    <div class="modal" ref="createPlaylistModal">
      <!-- Modal content -->
      <div class="modal-content" ref="createPlaylistModalContent">
        <div class="modal-body">
          <span @click="$refs.logoutModal.style.display='none'" class="close">&times;</span>
          <p>Playlist created.</p>
        </div>
      </div>
    </div>
    <div class="modal" ref="addPlaylistItemModal">
      <!-- Modal content -->
      <div class="modal-content" ref="addPlaylistItemModalContent">
        <div class="modal-body">
          <span @click="$refs.logoutModal.style.display='none'" class="close">&times;</span>
          <p>Episode added to playlist.</p>
        </div>
      </div>
    </div>
    <div class="modal" ref="deletePlaylistModal">
      <!-- Modal content -->
      <div class="modal-content" ref="deletePlaylistModalContent">
        <div class="modal-body">
          <span @click="$refs.logoutModal.style.display='none'" class="close">&times;</span>
          <p>Playlist deleted.</p>
        </div>
      </div>
    </div>
    <div class="modal" ref="removePlaylistItemModal">
      <!-- Modal content -->
      <div class="modal-content" ref="removePlaylistItemModalContent">
        <div class="modal-body">
          <span @click="$refs.logoutModal.style.display='none'" class="close">&times;</span>
          <p>Playlist episode removed.</p>
        </div>
      </div>
    </div>

    <img alt="logo" class="logo" src="./assets/images/podcast-icon-small.jpg" />
    <router-view></router-view>
    <nav class="nav-bar">
      <router-link to="/subscriptions" class="nav-item">
        <img
          class="icon"
          :class="[currentPage.includes('subscriptions') ? activeClass : '', 'nav-item']"
          src="./assets/images/my-list.png"
        />
      </router-link>

      <router-link to="/searchresults" class="nav-item">
        <img
          class="icon"
          :class="[currentPage.includes('searchresults') ? activeClass : '', 'nav-item']"
          src="./assets/images/search.png"
        />
      </router-link>

      <router-link to="/browse">
        <img
          class="icon"
          :class="[currentPage.includes('browse') ? activeClass : '', 'nav-item']"
          src="./assets/images/browse.png"
        />
      </router-link>
      <router-link to="/history">
        <img
          class="icon"
          :class="[currentPage.includes('history') ? activeClass : '', 'nav-item']"
          src="./assets/images/my_history_gray.png"
        />
      </router-link>
      <router-link to="/playlists">
        <img
          class="icon"
          :class="[currentPage.includes('playlists') ? activeClass : '', 'nav-item']"
          src="./assets/images/playlist.png"
        />
      </router-link>
    </nav>
  </div>
</template>

<script>
import axios from "axios";

import { searchBus, browseBus, podcastBus, subscriptionBus } from "./main";

export default {
  name: "app",
  data() {
    return {
      episodeList: [],
      podcastName: "",
      podcastFeedURL: "",
      podcastAPIid: "",
      episodeTitle: "",
      episodeDescription: "",
      episodeUrl: "",
      episodeDisplayed: "",
      timeDateAccessed: "",
      podcastId: "",
      loggedIn: "",
      subscribedPodcastIds: [],
      userInSession: "",
      activeClass: "active"
    };
  },
  methods: {
    subscribeToPodcast(name, rss_feed_url, podcast_id) {
      axios.post("/subscription", { name, rss_feed_url, podcast_id });
      this.getSubscribedPodcastIds();
      this.podcastName = name;
      this.openModal(
        this.$refs.subscriptionModal,
        this.$refs.subscriptionModalContent
      );
    },
    getSubscribedPodcastIds() {
      axios.post("/test-user-subscribed").then(res => {
        this.subscribedPodcastIds = res.data.podcast_ids;
      });
    },
    openModal(modal, modalContent) {
      modal.style.display = "block";
      setTimeout(function() {
        modalContent.classList.add("animate-up");
        modal.classList.add("fade-out");
      }, 3000);
      setTimeout(function() {
        modal.style.display = "none";
      }, 3400);
    },
    disableSubscribeButton(podcastId) {
      return this.subscribedPodcastIds.includes(podcastId);
    },
    getRSS(name, url, isSubscribing) {
      var match = url.match(/id(\d+)/);
      if (match) var podID = match[1];
      else podID = url.match(/\d+/);

      axios
        .get(
          "https://jsonp.afeld.me/?url=" +
            "https://itunes.apple.com/lookup?id=" +
            podID +
            "&entity=podcast"
        )
        .then(data => {
          this.podcastFeedUrl = data.data.results[0].feedUrl;
          this.podcastId = podID;
          this.podcastName = name;
          this.podcastFeedURL = this.podcastFeedUrl;
          // browseBus.$emit('feedFromBrowse', name, this.podcastFeedUrl, podID, this.subscribing);
          if (isSubscribing === true) {
            this.subscribeToPodcast(
              this.podcastName,
              this.podcastFeedURL,
              this.podcastId
            );
          }
          this.viewThisPodcast(
            this.podcastName,
            this.podcastFeedURL,
            this.podcastId
          );
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
      this.openModal(this.$refs.logoutModal, this.$refs.logoutModalContent);
    },
    async testUserInSession() {
      this.userInSession = this.userInSession;
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
      this.subscribeToPodcast(
        this.podcastName,
        this.podcastFeedURL,
        this.podcastId
      );
    }),
      subscriptionBus.$on("feedFromSubscription", (name, url, podcast_id) => {
        this.viewThisPodcast(name, url, podcast_id);
      }),
      searchBus.$on(
        "feedFromSearch",
        (name, url, podcast_id, isSubscribing) => {
          if (isSubscribing === true) {
            this.subscribeToPodcast(name, url, podcast_id);
            return;
          }
          this.viewThisPodcast(name, url, podcast_id);
        }
      ),
      browseBus.$on("feedFromBrowse", (name, url, isSubscribing) => {
        this.getRSS(name, url, isSubscribing);
      });
  },
  computed: {
    currentPage() {
      return this.$route.path;
    }
  },
  mounted() {
    this.testUserInSession();
    this.getSubscribedPodcastIds();
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
