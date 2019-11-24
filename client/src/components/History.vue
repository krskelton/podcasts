<template>
  <!-- Would like to build out a list of user's History
  meaning any audio feed clicked play.-->
  <div>
    <h2>My Listening History</h2>
    <ul>
      <li v-for="item in myHistory">{{ item.item }}</li>
    </ul>
  </div>
</template>

<script>
// // 1. create an array of items listened to starting from empty array.
// // 2. write code to get items into array. ('GET'  method from db, ref HistoryAPI)
// Question - how to tell if user has clicked on item??
// // 3. display on front end.
export default {
  name: "History",
  data() {
    return {
      myHistory: [
        { item: "Podcast 1" },
        { item: "Podcast 2" },
        { item: "my podcast" }
      ]
    };
  }
};
</script>

<style>
</style>