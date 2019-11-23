# Verify all names when Authentication is ready!

from flask import Blueprint, jsonify, request
from sql_alchemy_db_instance import db
from models import Playlists, Playlist_Items #class names being used
import requests

playlists_api = Blueprint('playlists_api', __name__)
playlist_items_api = Blueprint('playlist_items_api', __name__)

@playlists_api.route('/playlists', methods=['POST'])
def add_playlist():
    new_playlist = Playlists()
    new_playlist.name = request.json["name"]
    new_playlist.user_id = request.json[""]
    db.session.add(new_playlist)
    db.session.commit()
    return jsonify(success=True)

@playlists_api.route('/playlist_items', methods=['POST'])
def add_playlist_item():
    new_playlist_item = Playlist_Items() #from models.py, class name for adding playlist items.
    new_playlist_item.playlist_id = request.json[""] #variable passed from Playlists.vue component, that I must create.
    new_playlist_item.podcastAPI_id = request.json[""]
    new_playlist_item.episode_id = request.json[""]
    db.session.add(new_playlist_item)
    db.session.commit()
    return jsonify(success=True)