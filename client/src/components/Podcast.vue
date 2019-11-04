<template>
  <div class="episodes">
    <h2>{{podcastName}}</h2>
    <!--TODO: add conditional so that subscribe button is disabled if you are already subscribed to that podcast-->
    <button class="button" @click="subscribeToPodcast()">Subscribe</button>
    <ul v-if="!play">
      <!--get list of podcast episodes-->
      <li v-for="(episode, index) in episodeList" v-bind:key="index" @click="playEpisode(episode.title, episode.enclosure.url)">
          <div>
              <h3>{{episode.title}}</h3>
              <p>{{episode.description}}</p>
          </div>
      </li>
    </ul>
    <div class="player" v-if="play">
      <button @click="getRSSFeed(feedURL)">Return to episodes</button>
      <p><strong>{{episodeTitle}}</strong></p>
      <audio controls>
        <source :src="musicFile" type="audio/mpeg">
      </audio>
    </div>
  </div>
  
</template>

<script>
import axios from 'axios';
let Parser = require('rss-parser');

export default {
  name: 'Podcast',
  props: {
    podcastName: String,
    feedURL: String,
    // podID: Number,
  },
  data() {
    return {
      episodeList:[],
      play: false,
      episodeTitle: '',
      musicFile: ''
    }
  },
  methods:{
    subscribeToPodcast(){
      //add podcast to the database
      //TODO: add podcast id and rss feed to database so I can pull the link from the subscription tab
      axios.post('/subscription', {name: this.podcastName, rss_feed_url: this.feedURL})
      
    },
    getRSSFeed(RSSFEED){
      // Note: some RSS feeds can't be loaded in the browser due to CORS security.
      // To get around this, you can use a proxy.
      const CORS_PROXY = "https://cors-anywhere.herokuapp.com/"
      
      let parser = new Parser();
      parser.parseURL(CORS_PROXY + RSSFEED, (err, feed) => {
        console.log(CORS_PROXY + RSSFEED);
        // if (err) throw err;
        console.log(feed);
        this.episodeList = feed.items;
        this.play = false;
      })
    },
    playEpisode(title, mp3){
      this.episodeTitle = title;
      this.musicFile = mp3;
      this.play = true;
    } 
  },
  mounted(){
    this.getRSSFeed(this.feedURL);
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

</style>
