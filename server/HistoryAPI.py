from flask import Blueprint, jsonify, request
from sql_alchemy_db_instance import db
from models import Podcast, Users, PlaylistItems, Playlists, History
import requests

history_api = Blueprint('history_api', __name__)


@history_api.route('/my-history', methods=['GET'])
def show_my_history():
    # should this query by user_id so as to only get the histiory for that user?
    my_podcast_history = db.session.query(History).all()
    podcast_items_in_history = [{"id": history.id, "user_id": history.user_id,
                                 "episode_id": history.episode_id} for podcast in my_podcast_history]
    return jsonify({"name": podcast_items_in_history})
