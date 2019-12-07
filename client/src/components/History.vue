<template>
  <!-- Would like to build out a list of user's History, aka any audio feed clicked 'play'.-->
  <div>
    <h2>My Listening History</h2>
    <ul>
      <!-- <li v-for="item in myHistory">
        <span>{{ item.item }} Name of episode and audio control to play</span>
      </li>-->
    </ul>
    <div class="buttons">
      <button @click="getMyHistory">get stuff</button>
    </div>
  </div>
</template>

<script>
import axios from "axios";

// // use 'GET' method to call to history table, display list of episodes.
// // 3. display on front end.
export default {
  name: "History",
  data() {
    return {
      myHistory: [],
      //   this must read from db- history table
      trackID: "" //this piece of data is actually the whole podcast ID. not sure if we will use it.
    };
  },
  methods: {
    getMyHistory() {
      console.log("i printed");
    }
  }
};
</script>

<style>
</style>