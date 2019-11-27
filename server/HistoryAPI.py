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
    return jsonify({"my_history": podcast_items_in_history})
# any item clicked play has v-on:play functino to capture its info


@history_api.route('/add-to-history', methods=['POST'])
def add_to_history():
    new_history_item = History()
    # verify this is correct
    new_history_item.user_id = request.json['user_id']
    new_history_item.episode_id = request.json['episode_id']
    db.session.add(new_history_item)
    db.session.commit()
    return jsonify(success=True)
