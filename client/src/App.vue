<template>
  <div id="app">
    <img alt="logo" class="logo" src="./assets/images/podcast-icon-small.jpg">
    <h1>Podcasts</h1>
    <nav>
      <button @click="showSubscriptions"><img class="icon" src="./assets/images/my-list.png"/></button>
      <button @click="showSearch"><img class="icon" src="./assets/images/search.png"/></button>
      <button @click="showBrowse"><img class="icon" src="./assets/images/browse.png"/></button>
    </nav>
    <div id="content">
      <Subscriptions v-if="viewSubscriptions" @feedFromSubscription="subscriptionFeedRecieved"/>
      <SearchResults v-if="viewSearch" @feedFromSearch="searchFeedRecieved"/>
      <Browse v-if="viewBrowse" @feedFromBrowse="browseFeedRecieved"/>
      <Podcast v-if="viewPodcast" :podcastName="podcastName" :feedURL="podcastFeedURL" />
    </div>
  </div>
</template>


<script>
import Subscriptions from './components/Subscriptions.vue'
import SearchResults from './components/SearchResults.vue'
import Browse from './components/Browse.vue'
import Podcast from './components/Podcast.vue'

export default {
  name: 'app',
  data() {
    return{
      viewSubscriptions: false,
      viewSearch: false,
      viewBrowse: false,
      viewPodcast: false,

      podcastName: '',
      podcastFeedURL: '',
      // podcastID: 0,
    }
  },
  methods: {
    searchFeedRecieved(feedurl, podcastname){
        this.podcastName = podcastname;
        this.podcastFeedURL = feedurl;
        // this.podcastID = podcastid;
        this.viewSearch = false;
        this.viewPodcast = true;
    },
    browseFeedRecieved(feedurl2, podcastname2){
        this.podcastName = podcastname2;
        this.podcastFeedURL = feedurl2;
        // this.podcastID = podcastid2;
        this.viewBrowse = false;
        this.viewPodcast = true;
    },
    subscriptionFeedRecieved(feedurl3, podcastname3){
        this.podcastName = podcastname3;
        this.podcastFeedURL = feedurl3;
        // this.podcastID = podcastid3;
        this.viewSubscriptions = false;
        this.viewPodcast = true;
    },
    showSubscriptions(){
      this.viewSubscriptions = true;
      this.viewSearch = false;
      this.viewBrowse = false;
      this.viewPodcast = false;
    },
    showSearch(){
      this.viewSubscriptions = false;
      this.viewSearch = true;
      this.viewBrowse = false;
      this.viewPodcast = false;
    },
    showBrowse(){
      this.viewSubscriptions = false;
      this.viewSearch = false;
      this.viewBrowse = true;
      this.viewPodcast = false;
    }
  },
  components: {
    Subscriptions,
    Browse,
    SearchResults, 
    Podcast
  }
  
}
</script>

<style lang="css">
  @import url(https://fonts.googleapis.com/css?family=Raleway:400,600&display=swap);
  @import './assets/css/styles.css';
</style>


