<template>
  <div class="subscriptions">
    <h2>Subscriptions</h2>
    <ul>
        <!--TODO: Add link to Podcast.vue version of individual podcasts that lists the RSS feed-->
        <li v-for="(subscription, index) in subscriptions" v-bind:key="subscription.id" @click="sendFeedtoParent(subscription.rss_feed_url, subscription.name)"><span>{{ subscription.name }}</span> <button class="button" @click="removeSubscription(subscription.id)">Unsubscribe</button></li>
    </ul>
  </div>
  
</template>

<script>
import axios from 'axios';

export default {
  name: 'Subscriptions',
  data() {
    return {
      subscriptions: []
    }
  },
  methods:{
    //put getSubsciptions in the parent component so two child components can use
    getSubscriptions(){
      axios.get('/subscriptions').then(res => this.subscriptions = res.data.name);
    },
    removeSubscription(id){
      axios.patch('/subscription', {id : id})
      .then(() => this.getSubscriptions());
    },
    sendFeedtoParent(url, name){
      this.$emit('feedFromSubscription', url, name);
    }
  },
  mounted() {
    this.getSubscriptions();
  }
}
</script>
