<template>
    <div class="search-results">
        <h2>Find Podcast</h2>
        <div class="search">
            <input v-model="searchTerm" @keyup.enter="searchForPodcast"/>
            <button class="button" @click="searchForPodcast">Find Podcast</button>
        </div>
        <ul v-for="(searchResult, index) in searchResults" v-bind:key="index">
            <li>{{searchResult.collectionName}}
                <!-- <button @click="sendFeedtoParent(searchResult.feedUrl, searchResult.collectionName)">Subscribe</button> -->
                <button @click="sendFeedtoPodcast(searchResult.feedUrl, searchResult.collectionName, searchResult.collectionId)">Subscribe</button>
                <!-- <button @click="addToPlaylist(searchResult.feedUrl, searchResult.collectionName)">Add to playlist</button> -->
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
        }
    },
    methods: {
        //searchForPodcast adds the searchTerm from the user to make a call to the itunes api. The data from this response is capped at 50 responses. This can be changed by setting the parameter in the itunes url though.
        searchForPodcast(){
            axios.get('https://itunes.apple.com/search?term=' + this.searchTerm + '&country=US&media=podcast')
            .then((data) => {
                console.log(data)
                this.searchResults = data.data.results;
            })
        },
        //this.$emit sends the data to parent component

        // sendFeedtoParent(url, name){
        //     console.log("url: ", url, "name: ", name)
        //     // this.$emit('feedFromSearch', url, name);
        //     searchBus.$emit('feedFromSearch', url, name)
        //     this.$router.push('/podcast')
        // }
        sendFeedtoPodcast(url, name, podcast_id){
            console.log("send feed to podcast", url, name, podcast_id)
            // this.$emit('feedFromSearch', url, name);
            searchBus.$emit('feedFromSearch', url, name, podcast_id)
            // this.$router.push('/subscriptions')

            // it seems if /podcast isn't instanciated, the bus wont be 'detected' and acted upon.
            // this.$router.push('/podcast')
        }
    },
    created() {
        
    }
}
</script>

<style>
</style>