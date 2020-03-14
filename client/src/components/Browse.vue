<template>
  <div class="categories">
    <h2>Browse Top Podcasts by Category</h2>
    <ul v-if="!viewTopList">
      <!--IDEA: Add categories with bulk upload from database then loop through list to get ids from database-->
      <!--Add +/- icon to make menu show and hide the submenu-->
      <li @click="getTopTenList('1301')">Arts</li>
      <ul>
        <li @click="getTopTenList('1306')">Food</li>
        <li @click="getTopTenList('1402')">Design</li>
        <li @click="getTopTenList('1405')">Performing Arts</li>
        <li @click="getTopTenList('1406')">Visual Arts</li>
        <li @click="getTopTenList('1459')">Fashion and Beauty</li>
        <li @click="getTopTenList('1482')">Books</li>
      </ul>
      <li @click="getTopTenList('1303')">Comedy</li>
      <ul>
        <li @click="getTopTenList('1495')">Improv</li>
        <li @click="getTopTenList('1496')">Comedy Interviews</li>
        <li @click="getTopTenList('1497')">Stand-Up</li>
      </ul>
      <li @click="getTopTenList('1304')">Education</li>
      <ul>
        <li @click="getTopTenList('1498')">Language Learning</li>
        <li @click="getTopTenList('1499')">How To</li>
        <li @click="getTopTenList('1500')">Self-Improvement</li>
        <li @click="getTopTenList('1501')">Courses</li>
      </ul>
      <li @click="getTopTenList('1305')">Kids & Family</li>
      <ul>
        <li @click="getTopTenList('1519')">Education for Kids</li>
        <li @click="getTopTenList('1520')">Stories for Kids</li>
        <li @click="getTopTenList('1521')">Parenting</li>
        <li @click="getTopTenList('1522')">Pets & Animals</li>
      </ul>
      <li @click="getTopTenList('1309')">TV & Film</li>
      <ul>
        <li @click="getTopTenList('1561')">TV Reviews</li>
        <li @click="getTopTenList('1562')">After Shows</li>
        <li @click="getTopTenList('1563')">Film Reviews</li>
        <li @click="getTopTenList('1564')">Film History</li>
        <li @click="getTopTenList('1565')">Film Interviews</li>
      </ul>
      <li @click="getTopTenList('1310')">Music</li>
      <ul>
        <li @click="getTopTenList('1523')">Music Commentary</li>
        <li @click="getTopTenList('1524')">Music History</li>
        <li @click="getTopTenList('1525')">Music Interviews</li>
      </ul>
    </ul>
    <ol v-if="viewTopList">
      <li v-for="(topTenPodcast, index) in topTenPodcasts" v-bind:key="index">
        <div
          id="episode-title"
          @click="subscribing = false; sendFeed(topTenPodcast['im:name'].label, topTenPodcast.link.attributes.href, topTenPodcast)"
        >{{topTenPodcast['im:name'].label}}</div>
        <div id="subscribe">
          <button
            @click="subscribing = true; sendFeed(topTenPodcast['im:name'].label, topTenPodcast.link.attributes.href, topTenPodcast)"
            :disabled="disableSubscribeButton(topTenPodcast.id.attributes['im:id'])"
          >{{ disableSubscribeButton(topTenPodcast.id.attributes['im:id']) }} Subscribe</button>
        </div>
      </li>
    </ol>
  </div>
</template>

<script>
import axios from "axios";

import { browseBus } from "../main";

export default {
  name: "Browse",
  data() {
    return {
      topTenPodcasts: [],
      podcastFeedUrl: "",
      viewTopList: false,
      subscribing: false,
      isDisabled: false
    };
  },
  methods: {
    //getTopTenList passes the id from clicking on the list above of the category. This id is added to an itunes url to make an axios get request. The data received from the json reponse contains the top ten list for the category.
    getTopTenList(id) {
      axios
        .get(
          "https://itunes.apple.com/us/rss/toppodcasts/genre=" + id + "/json"
        )
        .then(data => {
          this.topTenPodcasts = data.data.feed.entry;
          this.viewTopList = true;
        });
    },
    disableSubscribeButton(podcastId) {
      return this.$parent.disableSubscribeButton(Number(podcastId));
    },
    sendFeed(name, url) {
      browseBus.$emit(
        "feedFromBrowse",
        name,
        url,
        this.subscribing,
        this.addingToPlaylist
      );
    }
  }
};
</script>

<style>
</style>