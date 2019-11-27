<template>
  <!-- Would like to build out a list of user's History, aka any audio feed clicked 'play'.-->
  <div>
    <h2>My Listening History</h2>
    <ul>
      <li v-for="item in myHistory">{{ item.item }}</li>
    </ul>
  </div>
</template>

<script>
// // . create an array of items listened to starting from empty array.(see myHistory)
// // where to determine user has clicked on that item -front end.
// // . items clicked on must go into db
// // use 'GET' method to call to history table, query taht table's data to display
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
      //   this must read from db- history table
    };
  }
};
</script>

<style>
</style>