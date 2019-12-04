<template>
  <div class="episodes">
    <h2>{{podcastName}}</h2>
    <h3>{{feedURL}}</h3>
    <!--IDEA: add conditional so that subscribe button is disabled if you are already subscribed to that podcast-->
    <!--IDEA: add message when the user clicks the subscribe button to let them know they are subscribed now.-->
    <button class="button" @click="subscribeToPodcast()">Subscribe</button>
    <ul v-if="!play">
      <li v-for="(episode, index) in episodeList" v-bind:key="index" @click="playEpisode(episode.title, episode.enclosure.url)">
          <div>
              <h3>{{episode.title}}</h3>
              <p>{{episode.description}}</p>
          </div>
      </li>
    </ul>
    <!--The player includes a button to show all the episodes again, tbe title of the episode and a simple html audio player with the mp3 file passed to it.-->
    <div class="player" v-if="play">
      <p><strong>{{episodeTitle}}</strong></p>
      <audio controls>
        <source :src="musicFile" type="audio/mpeg">
      </audio>
      <button class="button" style="margin: 20px auto;" @click="getRSSFeed(feedURL)">Return to episodes</button>
    </div>
  </div>
  
</template>

<script>
import axios from 'axios';
// import { bus } from '../main'

let Parser = require('rss-parser');

export default {
  name: 'Podcast',
  //The podcastName and feedURL are passed as props from the parent component app.vue
  // props: {
  //   podcastName: String,
  //   feedURL: String,
  // },
  data() {
    return {
      episodeList:[],
      play: false,
      episodeTitle: '',
      musicFile: '',

      podcastName: '',
      feedURL: ''
    }
  },
  methods:{
    //subscribeToPodcast adds the podcast to the database
    // subscribeToPodcast(){
    //   axios.post('/subscription', {name: this.podcastName, rss_feed_url: this.feedURL})
    // },
    // subscribeToPodcast(name, rss_feed_url){
    //   console.log("podcast.vue - post: ", name, rss_feed_url)
    //   axios.post('/subscription', {name, rss_feed_url})
    // },
    //The request to the iTunes API to get the RSS feed is made in PodcastAPI.py file because of an error with some podcasts returning html instead of XML. In Flask we can set the Headers so that we only get an XMLHttpRequest reponse, which is what we need in order for the rss-parser library to parse the response below.
    getRSSFeed(RSSFEED){
      axios.post('/itunes-api', {rss_feed: RSSFEED})
      .then((data)=>{
        console.log(data);
          let parser = new Parser();
           parser.parseString(data.data, (err, feed) => {
             if (err) throw err;
            this.episodeList = feed.items;
            this.play = false;
           });
      })
      
    },
    searchFeedRecieved(feedurl, podcastname){
      console.log("app.vue searchFeedRecieved", feedurl, podcastname)
      this.podcastName = podcastname;
    },
    //playEpisode sets the variable in data() equal to the podcast title and the mp3 url and sets play equal to true so the player will element will show.
    playEpisode(title, mp3){
      this.episodeTitle = title;
      this.musicFile = mp3;
      this.play = true;
    } 
  },
  //getRSSFeed is mounted so it will load when the Podcast component becomes visible
  mounted(){
    this.getRSSFeed(this.feedURL);
  },
  // created(){
  //   bus.$on('feedFromSearch', (url, name) => {
  //     console.log("Podcast.vue - bus arrived!", url, name)
  //     // this.searchFeedRecieved(url, name)
  //     this.subscribeToPodcast(name, url)
  //   })
  // },
}
</script>

