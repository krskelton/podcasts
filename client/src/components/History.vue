<template>
  <!-- list of user's History, aka any audio feed clicked 'play'.-->
  <div>
    <h2>My Listening History</h2>
    <ul>
      <li v-for="item in myHistory">
        <img :src="item.parent_podcast_art_url">
        <span>{{ item.episode_title }}</span>
        <!-- would like to format the viewing of time stamp to be cleaner (take off GMT)  -->
         <audio controls id="podcast-audio">
          <source :src="item.episode_url" type="audio/mpeg" />
        </audio>       
        <span>{{ item.time_stamp_accessed}}</span>
      </li>
    </ul>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "History",
  data() {
    return {
      myHistory: [],
      trackID: "" //this piece of data is actually the whole podcast ID. not sure if we will use it.
    };
  },
  methods: {
    getMyHistory() {
      axios
        .get("/my-history")
        .then(res => (this.myHistory = res.data.my_history_list));
    }
  },
  mounted() {
    this.getMyHistory();
  }
};
</script>

<style>
</style>