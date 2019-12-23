<template>
  <div class="subscriptions">
    <h2>Subscriptions</h2>
    <ul>
      <li
        v-for="(subscription, index) in subscriptions"
        v-bind:key="subscription.id"
        @click="sendFeedtoParent(subscription.name, subscription.rss_feed_url, subscription.podcast_API_id)"
      >
        <span>{{ subscription.name }}</span>
        <button class="button" @click="removeSubscription(subscription.id)">Unsubscribe</button>
      </li>
    </ul>
  </div>
</template>

<script>
import axios from "axios";

import { subscriptionBus } from '../main'

export default {
  name: "Subscriptions",
  data() {
    return {
      subscriptions: [],
      isUnsubscribing: false
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
      this.isUnsubscribing = true
      axios
        .patch("/subscription", { id: id })
        .then(() => this.getSubscriptions());
    },
    //this.$emit sends the data to parent component
    sendFeedtoParent(name, url, podcast_id) {
      if (this.isUnsubscribing !== true) {
        this.isUnsubscribing = false;
        subscriptionBus.$emit("feedFromSubscription", name, url, podcast_id);
      }
      this.isUnsubscribing = false;
    }
  },
  //getSubscriptions is mounted so it will load when the Subscriptions component becomes visible
  mounted() {
    this.getSubscriptions();
  }
};
</script>
