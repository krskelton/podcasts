<template>
  <div>
    <h3>Playlists</h3>
    <p>Create new playlist</p>
    <input v-model="playlistTitle" @keyup.enter="createPlaylist()" type="text" />
    <button class="playlist" @click="createPlaylist()">Create playlist</button>
    <p style="text-align: center;">View my playlists</p>
    <hr />
    <ul>
      <div v-for="(playlist, index) in userPlaylists" v-bind:key="index">
        <h2>{{playlist.title}}{{updateIndex(index)}}</h2>
        <button class="playlist" @click="deletePlaylist(playlist.id)">Delete playlist</button>
        <div v-for="(playlist_item, index) in userPlaylistItems" v-bind:key="index">
          <h5 v-if="playlist_item.playlist_id === playlist.id">
            {{playlist_item.playlist_id}} {{playlist_item.episode_title}}
            <button
              class="button"
              style="margin: 20px auto;"
              @click="removePlaylistItem(playlist_item.id)"
            >Remove episode</button>
            <hr />
          </h5>
        </div>
      </div>
    </ul>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "Playlists",

  // props are passed from app.vue
  props: {},
  data() {
    return {
      userPlaylists: [],
      userPlaylistItems: [],
      playlistID: null,
      playlistAPIID: null,
      episodeID: null,
      playlistTitle: "",
      playlistIDList: []
    };
  },
  methods: {
    createPlaylist() {
      axios
        .post("/playlists", { title: this.playlistTitle })
        .then(() => this.getAndSetUserPlaylists());
      this.$parent.modalText = "Playlist created";
      this.$parent.openModal();
    },
    updateIndex(index) {
      this.playlistID = index;
    },
    getAndSetUserPlaylists() {
      axios.get("/playlists").then(response => {
        this.userPlaylists = response.data.playlists;
        axios.get("/playlist_items").then(response => {
          this.userPlaylistItems = response.data.playlist_items;
        });
      });
    },
    removePlaylistItem(playlist_item_id) {
      axios
        .patch("/playlist_items", { playlist_item_id: playlist_item_id })
        .then(() => this.getAndSetUserPlaylists());
    },
    deletePlaylist(playlist_id) {
      for (let i = 0; i < this.userPlaylistItems.length; i++) {
        if (this.userPlaylistItems[i].playlist_id === playlist_id) {
          this.removePlaylistItem(this.userPlaylistItems[i].id);
        }
      }
      axios
        .patch("/playlists", { playlist_id: playlist_id })
      this.getAndSetUserPlaylists();
    }
  },
  mounted() {
    this.getAndSetUserPlaylists();
  }
};
</script>