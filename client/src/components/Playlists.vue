<template>
    <div>
        <h3>Playlists</h3>
        <p>Create new playlist</p>
        <input v-model="playlistTitle" @keyup.enter="createPlaylist()" type="text" />
        <button @click="createPlaylist()">Create playlist</button>
        <p>View playlists</p>
        <hr>
        <ul>
            <div v-for="(playlist, index) in userPlaylists" v-bind:key="index">
            <h2>{{playlist.title}}{{updateIndex(index)}}</h2>
            <hr>
            <div v-for="(playlist_item, index) in userPlaylistItems" v-bind:key="index">
                <h5 v-if="playlist_item.playlist_id === playlist.id">
                    {{playlist_item.playlist_id}} {{playlist_item.episode_title}}
                    <button class="button" style="margin: 20px auto;" @click="removePlaylistItem(playlist_item.id)">
                        Remove episode
                    </button>
                    <hr>
                </h5>
            </div>
            </div>
        </ul>
    </div>
</template>

<script>
import axios from 'axios'

export default {
    name: 'Playlists',

    // props are passed from app.vue
    props: {
        
    },
    data() {
        return{
            userPlaylists: [],
            userPlaylistItems: [],
            playlistID: null,
            playlistAPIID: null,
            episodeID: null,
            playlistTitle: "",
            playlistIDList: []
        }
    },
    methods: {
        createPlaylist() {
            axios.post('/playlists', { title: this.playlistTitle })
            // axios.post('/playlist_items', {playlist_id: this.playlistID, playlistAPI_id: this.playlistAPIID, episode_id: this.episodeID})
        },
        updateIndex(index) {
            this.playlistID = index;
        },
        getAndSetUserPlaylists() {
            axios.get("/playlists")
            .then((response) => {
                this.userPlaylists = response.data.playlists;
                console.log("userPlaylists ", this.userPlaylists)
                axios.get("/playlist_items")
                .then((response) => {
                    this.userPlaylistItems = response.data.playlist_items;
                    console.log("userPlaylistItems ", this.userPlaylistItems)
                });
            });
            
        },
        removePlaylistItem(playlist_item_id) {
            console.log("playlist_item_id ", playlist_item_id)
            axios
            .patch("/playlist_items", { playlist_item_id: playlist_item_id })
            .then(() => this.getAndSetUserPlaylists());
        }
    },
    mounted() {
        this.getAndSetUserPlaylists();
    }
}
</script>