# Verify all names when Authentication is ready!

from flask import Blueprint, jsonify, request, session
from sql_alchemy_db_instance import db
from models import Users, Playlists, PlaylistItems #class names being used
import requests

playlists_api = Blueprint('playlists_api', __name__)
playlist_items_api = Blueprint('playlist_items_api', __name__)

@playlists_api.route('/playlists', methods=['POST'])
def add_playlist():
    user_id = Users.query.filter_by(username=session['user']).first().id
    new_playlist = Playlists(request.json["title"], user_id)
    new_playlist.save()
    return jsonify(success=True)

@playlists_api.route('/playlist_items', methods=['POST'])
def add_playlist_item():
    new_playlist_item = PlaylistItems() #from models.py, class name for adding playlist items.
    new_playlist_item.playlist_id = request.json['playlist_id']
    new_playlist_item.episode_title = request.json['episode_title']
    new_playlist_item.episode_summary = request.json['episode_description']
    new_playlist_item.episode_url = request.json['episode_url']

    db.session.add(new_playlist_item)
    db.session.commit()
    return jsonify(success=True)

@playlists_api.route('/playlists', methods=['GET'])
def get_playlists():
    user_playlists = Users.query.filter_by(username=session['user']).first().playlists

    return jsonify({"playlists": [{ "id": playlist.id, "title": playlist.name } for playlist in user_playlists]})

@playlists_api.route('/playlist_items', methods=['GET'])
def get_playlist_items():
    playlist_items = PlaylistItems.query.all()

    return jsonify({"playlist_items": [{ "id": playlist_item.id, "playlist_id": playlist_item.playlist_id, "episode_title": playlist_item.episode_title, "episode_summary": playlist_item.episode_summary, "episode_url": playlist_item.episode_url } for playlist_item in playlist_items]})

    # playlist_id = db.session.query(Playlists).filter(Playlists.id)
    # playlist_episodes = db.session.query(PlaylistItems).filter(PlaylistItems.playlist_id == playlist_id)
