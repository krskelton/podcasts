<template>
    <div class="search-results">
        <h2>Find Podcast</h2>
        <input v-model="searchTerm"/>
        <button @click="searchForPodcast">Find Podcast</button>
        <ul>
            <li v-for="(searchResult, index) in searchResults" v-bind:key="index" @click="sendFeedtoParent(searchResult.feedUrl, searchResult.collectionName)">{{searchResult.collectionName}}</li>
        </ul>
        
    </div>
</template>

<script>
import axios from 'axios';


export default {
    name: 'SearchResults',
    data() {
        return {
            searchTerm: '',
            searchResults: [],
        }
    },
    methods: {
        searchForPodcast(){
            axios.get('https://itunes.apple.com/search?term=' + this.searchTerm + '&country=US&media=podcast')
            .then((data) => {
                this.searchResults = data.data.results;
            })
        },
        sendFeedtoParent(url, name){
            this.$emit('feedFromSearch', url, name);
        }
    }
}
</script>

<style>
</style>