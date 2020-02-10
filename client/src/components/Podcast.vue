<template>
  <div class="episodes">
    <h2>{{ this.$parent.podcastName }}</h2>
    <button
      class="button"
      @click="sendToSubscribe()"
      :disabled="disableSubscribeButton(Number(this.$parent.podcastId))">
      Subscribe
    </button>
      <ul v-if="!play">
        <li id="episode-title-container" v-for="(episode, index) in episodeList" v-bind:key="index">
          <div id="episode-title" @click="playEpisode(episode) + getParentPodcastData(episode)">
            <h3>{{ episode.title }}</h3>
          </div>
          <div id="add-to-playlist">
            <select @change="dontPlay($event)" :value="null">
              <option value="" selected disabled hidden>Add Episode to Playlist</option>
              <option v-for="playlist in userPlaylists" :value="playlist.id" :key="playlist.id">
                {{ playlist.title }}
              </option>
            </select>
            <br>
          <button @click="getEpisode(episode) + addToPlaylist()">Add to playlist</button>
        </div>
      </li>
    </ul>
    <!--The player includes a button to show all the episodes again, tbe title of the episode and a simple html audio player with the mp3 file passed to it.-->
    <div class="player" v-if="play">
      <p>
        <strong>{{ episodeTitle }}</strong>
      </p>
      <div v-html="episodeDescription"></div>
      <audio controls id="podcast-audio" @play="testDuplicateHistoryEntry()" @pause="registerPause()">
        <source :src="musicFile" type="audio/mpeg" />
      </audio>
      <button class="button" style="margin: 20px auto;" @click="getRSSFeed(this.$parent.podcastFeedURL)">
        Return to episodes
      </button>
    </div>
  </div>
</template>

<script>
import axios from "axios";
var Sugar = require("sugar");
let Parser = require("rss-parser");

import { podcastBus } from '../main'

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
      episodeDescription: "",
      episodeUrl: "",
      musicFile: "",
      timeDateAccessed: "",
      trackPlaying: false,
      userPlaylists: [],
      addingToPlaylist: false,
      event: []
    };
  },
  methods: {
    dontPlay(event) {
      this.addingToPlaylist = true;
      this.event = event;
    },
    getAndSetUserPlaylists() {
      axios.get("/playlists")
      .then((response) => {
        this.userPlaylists = response.data.playlists;
      })
    },
    addToPlaylist() {
      this.addingToPlaylist = true;
      let playlistID = this.event.target.value;
      axios.post("/playlist_items", { playlist_id: playlistID, episode_title: this.episodeTitle, episode_description: this.episodeDescription, episode_url: this.episodeUrl })
      this.$parent.modalText = "Episode added to playlist"
      this.$parent.openModal();
    },
    testDuplicateHistoryEntry() {
      // before adding a new user to DB, make sure that username isn't already taken
      axios.post("/duplicate-history-entry-test", { episode_title: this.episodeTitle })
        .then(resp => {
          if (resp.data.does_the_history_entry_exist.length == 0) {
            // if the length of response is 0, the history entry doesn't exist - add it to the history
            this.addToHistory();
          } else {
            // otherwise, it does exist - we just need to track the place in audio and patch the history
            this.determinePlaceInTrack(this.episodeTitle);
          }
      });
    },
    registerPause(){
      this.trackPlaying = false;
    },
    sendToSubscribe() {
      podcastBus.$emit('feedFromPodcast');
    },
    getParentPodcastData(){
      let lookup_parent_podcast_url = "https://itunes.apple.com/lookup?id=" + this.$parent.podcastId + '&entity=podcast'
      axios.get("https://cors-anywhere.herokuapp.com/" + lookup_parent_podcast_url)
      .then((data) => {
        this.parentPodcastArtUrl = data.data.results[0].artworkUrl100;
      })
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
    disableSubscribeButton(podcastId){
      return this.$parent.disableSubscribeButton(podcastId);
    },
    addToHistory() {
      let timestamp = Sugar.Date.format(new Date(Date.now()),"%Y-%m-%d %H:%M:%S");
      this.timeDateAccessed = timestamp;
      axios.post("/add-to-history", {episode_title: this.episodeTitle, episode_summary: this.episodeDisplayed.contentSnippet, episode_url: this.episodeDisplayed.enclosure.url, time_date: this.timeDateAccessed, current_time_listened: 0, parent_podcast_id: this.$parent.podcastId, parent_podcast_art_url: this.parentPodcastArtUrl});
      this.determinePlaceInTrack(this.episodeTitle);
    },
    searchFeedRecieved(feedurl, podcastname) {
      this.podcastName = podcastname;
    },
    getEpisode(episode) {
      this.episodeTitle = episode.title;
      this.episodeDescription = episode.content;
      this.episodeUrl = episode.enclosure.url;
    },
    // playEpisode sets the variable in data() equal to the podcast title and the mp3 url and sets play equal to true so the player will element will show.
    playEpisode(episode) {
      if (this.addingToPlaylist === true) {
        this.addingToPlaylist = false;
        return
      }
      this.episodeDisplayed = episode;
      this.episodeTitle = episode.title;
      this.episodeDescription = episode.content;
      this.musicFile = episode.enclosure.url;
      this.play = true;
    },
    determinePlaceInTrack(episodeTitle) {
      // this part was necessary to prevent multiple instances of determinePlaceInTrack() from running when a user scrubs through audio
      // without this, the db would be updated multiple times per second if a user scrubs through audio multiple times
      if (this.trackPlaying == true){
        return;
      }
      this.trackPlaying = true;
      let podcastAudio = document.getElementById("podcast-audio");
      let interval = setInterval(function(){
        if (!podcastAudio.paused && podcastAudio.currentTime > 0 && !podcastAudio.ended) {
          let currentTime = Math.floor(podcastAudio.currentTime);
          axios.patch('/patch-current-time', {current_time: currentTime, episode_title: episodeTitle})
        } else if (podcastAudio.paused || podcastAudio.ended) {
          clearInterval(interval);
          this.trackPlaying = false;
        }
      }, 2000)
    }
  },

  //getRSSFeed is mounted so it will load when the Podcast component becomes visible
  mounted() {
    this.getRSSFeed(this.$parent.podcastFeedURL);
    this.getAndSetUserPlaylists();
  }
};
</script>
