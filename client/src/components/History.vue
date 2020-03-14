<template>
  <div class="page-wrapper">
    <h2>My Listening History</h2>
    <ul class="history-list">
      <li class="Col1" v-for="item in myHistory" :key="item">
        <img class="Col1-img" :src="item.parent_podcast_art_url" />
        <span class="col1-title">{{ item.episode_title }}</span>

        <!-- would like to format the viewing of time stamp to be cleaner (take off GMT)  -->
        <audio controls class="Col2" :currentTime.prop="item.current_time_listened">
          <source :src="item.episode_url" type="audio/mpeg" />
        </audio>
        <br />
        <br />
        <span class="col2-timestamp">{{ item.time_stamp_accessed}}</span>
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
      myHistory: []
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
.page-wrapper {
  margin: 15px;
}
ul.history-list {
  flex-direction: column;
  display: flex;
  width: 100%;
}
li.Col1 {
  display: flex;
  flex-wrap: wrap;
}
audio.Col2 {
  display: flex;
}
span.col2-timestamp {
  display: flex;
}
</style>