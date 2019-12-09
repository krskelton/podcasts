<template>
    <div class="search-results">
        <h2>Find Podcast</h2>
        <div class="search">
            <input v-model="searchTerm"/>
            <button class="button" @click="searchForPodcast">Find Podcast</button>
        </div>
        <ul>
            <li v-for="(searchResult, index) in searchResults" v-bind:key="index" @click="sendFeedtoParent(searchResult.feedUrl, searchResult.collectionName, searchResult.collectionId)">{{searchResult.collectionName}}</li>
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
        //searchForPodcast adds the searchTerm from the user to make a call to the itunes api. The data from this response is capped at 50 responses. This can be changed by setting the parameter in the itunes url though.
        searchForPodcast(){
            axios.get('https://itunes.apple.com/search?term=' + this.searchTerm + '&country=US&media=podcast')
            .then((data) => {
                console.log(data)
                this.searchResults = data.data.results;
            })
        },
        //this.$emit sends the data to parent component
        sendFeedtoParent(url, name, id){
            this.$emit('feedFromSearch', url, name, id);
        }
    }
}
</script>

<style>
</style>