<template>
    <div class="search-results">
        <h2>Find Podcast</h2>
        <div class="search">
            <input v-model="searchTerm" @keyup.enter="searchForPodcast"/>
            <button class="button" @click="searchForPodcast">Find Podcast</button>
        </div>
        <ul v-for="(searchResult, index) in searchResults" v-bind:key="index">
            <li>
                <div id="episode-title" @click="sendFeedtoApp(searchResult.collectionName, searchResult.feedUrl, searchResult.collectionId)">
                    {{searchResult.collectionName}}
                </div>
                <div id="subscribe">
                    <button @click="sendToSubscribe(searchResult.collectionName, searchResult.feedUrl, searchResult.collectionId)" :disabled="disableSubscribeButton(searchResult.collectionId)">Subscribe</button>
                </div>
            </li>
        </ul>
    </div>
</template>

<script>
import axios from 'axios';
import { searchBus } from '../main'

export default {
    name: 'SearchResults',
    data() {
        return {
            searchTerm: '',
            searchResults: [],
            isSubscribing: false,
        }
    },
    methods: {
        //searchForPodcast adds the searchTerm from the user to make a call to the itunes api. The data from this response is capped at 50 responses. This can be changed by setting the parameter in the itunes url though.
        searchForPodcast(){
            let searchUrl = 'https://itunes.apple.com/search?term=' + this.searchTerm + '&country=US&media=podcast'
            axios.get("https://cors-anywhere.herokuapp.com/" + searchUrl)
            .then((data) => {
                this.searchResults = data.data.results;
            })
        },
        disableSubscribeButton(podcastId){
            return this.$parent.disableSubscribeButton(podcastId);
        },
        sendToSubscribe(name, url, podcast_id) {
            this.isSubscribing = true;
            this.sendFeedtoApp(name, url, podcast_id);
        },
        sendFeedtoApp(name, url, podcast_id){
            searchBus.$emit('feedFromSearch', name, url, podcast_id, this.isSubscribing)
            this.isSubscribing = false
        }
    }
}

</script>

<style>
</style>