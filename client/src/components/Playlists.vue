<template>
    
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
            playlistName: "",
            playlistID: null,
            playlistAPIID: null,
            episodeID: null
        }
    },
    methods: {
        createPlaylist() {
            axios.post('/playlists', {name: this.playlistName})
            axios.post('/playlist_items', {playlist_id: this.playlistID, playlistAPI_id: this.playlistAPIID, episode_id: this.episodeID})
        }
    }
}
</script>