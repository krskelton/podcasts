<template>
    <div class="categories">
        <h2>Browse Top Podcasts by Category</h2>
        <ul v-if="!viewTopList">
            <!--IDEA: Add categories with bulk upload from database then loop through list to get ids from database-->
            <!--Add +/- icon to make menu show and hide the submenu-->
            <li @click="getTopTenList('1301')">Arts</li>
                <ul>
                    <li @click="getTopTenList('1306')">Food</li>
                    <li @click="getTopTenList('1402')">Design</li>
                    <li @click="getTopTenList('1405')">Performing Arts</li>
                    <li @click="getTopTenList('1406')">Visual Arts</li>
                    <li @click="getTopTenList('1459')">Fashion and Beauty</li>
                    <li @click="getTopTenList('1482')">Books</li>
                </ul>
            <li @click="getTopTenList('1303')">Comedy</li>
                <ul>
                    <li @click="getTopTenList('1495')">Improv</li>
                    <li @click="getTopTenList('1496')">Comedy Interviews</li>
                    <li @click="getTopTenList('1497')">Stand-Up</li>
                </ul>
            <li @click="getTopTenList('1304')">Education</li>
                <ul>
                    <li @click="getTopTenList('1498')">Language Learning</li>
                    <li @click="getTopTenList('1499')">How To</li>
                    <li @click="getTopTenList('1500')">Self-Improvement</li>
                    <li @click="getTopTenList('1501')">Courses</li>
                </ul>
            <li @click="getTopTenList('1305')">Kids & Family</li>
                <ul>
                    <li @click="getTopTenList('1519')">Education for Kids</li>
                    <li @click="getTopTenList('1520')">Stories for Kids</li>
                    <li @click="getTopTenList('1521')">Parenting</li>
                    <li @click="getTopTenList('1522')">Pets & Animals</li>
                </ul>
            <li @click="getTopTenList('1309')">TV & Film</li>
                <ul>
                    <li @click="getTopTenList('1561')">TV Reviews</li>
                    <li @click="getTopTenList('1562')">After Shows</li>
                    <li @click="getTopTenList('1563')">Film Reviews</li>
                    <li @click="getTopTenList('1564')">Film History</li>
                    <li @click="getTopTenList('1565')">Film Interviews</li>
                </ul>
            <li @click="getTopTenList('1310')">Music</li>
                <ul>
                    <li @click="getTopTenList('1523')">Music Commentary</li>
                    <li @click="getTopTenList('1524')">Music History</li>
                    <li @click="getTopTenList('1525')">Music Interviews</li>
                </ul> 
        </ul>
        <ol v-if="viewTopList">
            <li v-for="(topTenPodcast, index) in topTenPodcasts" v-bind:key="index" @click="getRSS(topTenPodcast.link.attributes.href, topTenPodcast['im:name'].label)">{{topTenPodcast['im:name'].label}}</li>
        </ol>
    </div>
</template>

<script>
import axios from 'axios';
export default {
    name: 'Browse',
    data() {
        return{
            topTenPodcasts: [], 
            podcastFeedUrl: '',
            viewTopList: false
        }        
    },
    methods: {
        //getTopTenList passes the id from clicking on the list above of the category. This id is added to an itunes url to make an axios get request. The data received from the json reponse contains the top ten list for the category.
        getTopTenList(id){
            axios.get('https://itunes.apple.com/us/rss/toppodcasts/genre=' + id + '/json')
            .then((data) => {
                this.topTenPodcasts = data.data.feed.entry;
                this.viewTopList = true;
            })
        },
        //Since the json data in the above response does not return a feedUrl as a variable, the id needs to be parsed out of the url and sent to a different itunes api call that will return the feedUrl. The feedUrl is important because it's what returns the list of episodes.
        getRSS(url, name){
            var match = url.match(/id(\d+)/)
            if (match) var podID = match[1];
            else var podID = url.match(/\d+/);

            axios.get('https://jsonp.afeld.me/?url=' + 'https://itunes.apple.com/lookup?id=' + podID + '&entity=podcast')
            .then((data) => {
                this.podcastFeedUrl = data.data.results[0].feedUrl;
                //this.$emit sends the data to parent component
                this.$emit('feedFromBrowse', this.podcastFeedUrl, name);
            })
        }
    }
}
</script>

<style>
</style>