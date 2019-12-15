<template>
  <div class="subscriptions">
    <h2>Subscriptions</h2>
    <ul id="nav-margin">
      <li
        v-for="(subscription, index) in subscriptions"
        v-bind:key="subscription.id"
        @click="sendFeedtoParent(subscription.rss_feed_url, subscription.name)"
      >
        <span>{{ subscription.name }}</span>
        <button class="button" @click="removeSubscription(subscription.id)">Unsubscribe</button>
      </li>
    </ul>
  </div>
</template>

<script>
import axios from "axios";
//import { bus } from "../main";
export default {
  name: "Subscriptions",
  data() {
    return {
      subscriptions: []
    };
  },
  methods: {
    //Get subscriptions from the database
    getSubscriptions() {
      axios
        .get("/subscriptions")
        .then(res => (this.subscriptions = res.data.name));
    },
    //Remove a subsciption from the database
    removeSubscription(id) {
      axios
        .patch("/subscription", { id: id })
        .then(() => this.getSubscriptions());
    },
    //this.$emit sends the data to parent component
    sendFeedtoParent(url, name) {
      this.$emit("feedFromSubscription", url, name);
    }
  },
  //getSubscriptions is mounted so it will load when the Subscriptions component becomes visible
  mounted() {
    this.getSubscriptions();
  }
};
</script>
