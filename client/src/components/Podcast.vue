<template>
  <div class="episodes">
    <h2>{{ this.$parent.podcastName }}</h2>
    <!--IDEA: add conditional so that subscribe button is disabled if you are already subscribed to that podcast-->
    <!--IDEA: add message when the user clicks the subscribe button to let them know they are subscribed now.-->
    <button
      class="button"
      @click="
        subscribeToPodcast(
          $parent.podcastName,
          $parent.podcastFeedURL,
          $parent.podcastId
        )
      "
    >
      Subscribe
    </button>
    <ul v-if="!play">
      <li
        v-for="(episode, index) in episodeList"
        v-bind:key="index"
        @click="playEpisode(episode) + printData(episode)"
      >
        <div>
          <h3>{{ episode.title }}</h3>
          <p>{{ episode.description }}</p>
        </div>
      </li>
    </ul>
    <!--The player includes a button to show all the episodes again, tbe title of the episode and a simple html audio player with the mp3 file passed to it.-->
    <div class="player" v-if="play">
      <p>
        <strong>{{ episodeTitle }}</strong>
      </p>
      <audio
        controls
        id="podcast-audio"
        v-on:play="addToHistory() + determinePlaceInTrack()"
      >
        <source :src="musicFile" type="audio/mpeg" />
      </audio>
      <button
        class="button"
        style="margin: 20px auto;"
        @click="getRSSFeed(this.$parent.podcastFeedURL)"
      >
        Return to episodes
      </button>
    </div>
  </div>
</template>

<script>
import axios from "axios";
var Sugar = require("sugar");
let Parser = require("rss-parser");

export default {
  name: "Podcast",

  data() {
    return {
      episodeList: [],
      episodeDisplayed: "",
      parentPodcastId: "",
      parentPodcastArtUrl: "",
      play: false,
      episodeTitle: "",
      musicFile: "",
      timeDateAccessed: "",
      d: ""
    };
  },
  methods: {
    subscribeToPodcast(name, rss_feed_url, podcast_id) {
      // Podcast_id not being submitted to db.
      axios.post("/subscription", { name, rss_feed_url, podcast_id })
        .then(() => {
          console.log("PODCAST ID; ", podcast_id);
          this.$router.push("/subscriptions");
        });
    },
    printData(episode){
      let lookup_parent_podcast_url = "https://itunes.apple.com/lookup?id=" + this.$parent.podcastId + '&entity=podcast'
      axios.get("https://cors-anywhere.herokuapp.com/" + lookup_parent_podcast_url)
      .then((data) => {
        this.parentPodcastArtUrl = data.data.results[0].artworkUrl100;
      })
      // console.log(episode.itunes.summary, episode.link, episode.title);
    },
    //The request to the iTunes API to get the RSS feed is made in PodcastAPI.py file because of an error with some podcasts returning html instead of XML. In Flask we can set the Headers so that we only get an XMLHttpRequest reponse, which is what we need in order for the rss-parser library to parse the response below.
    getRSSFeed(RSSFEED) {
      axios.post("/itunes-api", { rss_feed: RSSFEED }).then(data => {
        let parser = new Parser();
        parser.parseString(data.data, (err, feed) => {
          if (err) throw err;
          this.episodeList = feed.items;
          this.play = false;
        });
      });
    },
    addToHistory() {
      console.log(this.episodeDisplayed);
      let timestamp = Sugar.Date.format(
        new Date(Date.now()),
        "%Y-%m-%d %H:%M:%S"
      );
      this.timeDateAccessed = timestamp;
      axios.post("/add-to-history", {episode_title: this.episodeTitle, episode_summary: this.episodeDisplayed.itunes.summary, episode_url: this.episodeDisplayed.enclosure.url, time_date: this.timeDateAccessed, parent_podcast_id: this.$parent.podcastId, parent_podcast_art_url: this.parentPodcastArtUrl});
    },
    searchFeedRecieved(feedurl, podcastname) {
      this.podcastName = podcastname;
    },
    // playEpisode sets the variable in data() equal to the podcast title and the mp3 url and sets play equal to true so the player will element will show.
    playEpisode(episode) {
      this.episodeDisplayed = episode;
      this.episodeTitle = episode.title;
      this.musicFile = episode.enclosure.url;
      this.play = true;
    },
    determinePlaceInTrack() {
      var podcastAudio = document.getElementById("podcast-audio");
      podcastAudio.ontimeupdate = function() {
        console.log(podcastAudio.currentTime);
      };
    }
  },

  //getRSSFeed is mounted so it will load when the Podcast component becomes visible
  mounted() {
    this.getRSSFeed(this.$parent.podcastFeedURL);
  }
};
</script>
