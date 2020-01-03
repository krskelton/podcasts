<template>
    <div>
        <h3>Playlists</h3>
        <input v-model="playlistTitle" @keyup.enter="createPlaylist()" type="text" />
        <button @click="createPlaylist()">Create playlist</button>
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
            playlistID: null,
            playlistAPIID: null,
            episodeID: null,
            playlistTitle: "Playlist title"
        }
    },
    methods: {
        createPlaylist() {
            axios.post('/playlists', {title: this.playlistTitle})
            // axios.post('/playlist_items', {playlist_id: this.playlistID, playlistAPI_id: this.playlistAPIID, episode_id: this.episodeID})
        }
    }
}
</script>