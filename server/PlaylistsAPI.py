# Verify all names when Authentication is ready!

from flask import Blueprint, jsonify, request, session
from sql_alchemy_db_instance import db
from models import Users, Playlists, PlaylistItems #class names being used
import requests

playlists_api = Blueprint('playlists_api', __name__)
playlist_items_api = Blueprint('playlist_items_api', __name__)

@playlists_api.route('/playlists', methods=['POST'])
def add_playlist():
    new_playlist = Playlists()
    user_in_session = session['user']
    username = db.session.query(Users).filter(Users.username==user_in_session).first()
    new_playlist.user_id = username.id
    new_playlist.name = request.json["title"]
    db.session.add(new_playlist)
    db.session.commit()
    return jsonify(success=True)

@playlists_api.route('/playlist_items', methods=['POST'])
def add_playlist_item():
    new_playlist_item = Playlist_Items() #from models.py, class name for adding playlist items.

    # new_playlist_item.episode_summary = request.json['episode_summary']
    # new_playlist_item.episode_url = request.json['episode_url']
    # new_playlist_item.episode_title = request.json['episode_title']

    # new_playlist_item.playlist_id = request.json['playlist_id']
    # new_playlist_item.playlist_art_url = request.json['playlist_art_url']

    db.session.add(new_playlist_item)
    db.session.commit()
    return jsonify(success=True)

@playlists_api.route('/playlists', methods=['GET'])
def get_playlists():
    playlists = db.session.query(Playlists).all()
    playlist_info = [{"id": playlist.id, "title": playlist.name, user_id: playlist.user_id} for playlist in playlists]
    return jsonify({"playlist_info": playlist_info})
