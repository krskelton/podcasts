from flask import Blueprint, jsonify, request, session
from sql_alchemy_db_instance import db
from models import Podcast, Users, PlaylistItems, Playlists, History
from usersAPI import test_users_in_session
import requests
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import func

history_api = Blueprint('history_api', __name__)


@history_api.route('/my-history', methods=['GET'])
def show_my_history():
    user = session.get('user')
    print('---------------')
    print(user)
    user_in_session = db.session.query(Users).filter(
        Users.username == user).first()
    print('---------------')
    print(user_in_session)
    user_id_of_user_in_session = user_in_session.id
    print('---------------')
    print(user_id_of_user_in_session)
    my_history_instances = db.session.query(
        History.id, History.user_id, History.episode_id, History.time_stamp_accessed).filter(History.user_id == user_id_of_user_in_session).all()

    podcast_items_in_history = [{"id": history.id, "user_id": history.user_id, "episode_id": history.episode_id,
                                 "time_stamp_accessed": history.time_stamp_accessed} for history in my_history_instances]
    return jsonify({"my_history_list": podcast_items_in_history})
# any item clicked play has v-on:play (addToHistory function) to capture its info
# filter(Users.id == History.user_id)


@history_api.route('/add-to-history', methods=['POST'])
def add_to_history():
    new_history_item = History()
    user_in_session = session['user']
    username = db.session.query(Users).filter(
        Users.username == user_in_session).first()
    new_history_item.user_id = username.id
    new_history_item.episode_id = request.json['episode_title']
    new_history_item.time_stamp_accessed = request.json['time_date']
    # new_history_item.episode_id = request.json['episode_id'] need to figure out what will go in here- how can we get the podcast ID here?

    db.session.add(new_history_item)
    db.session.commit()
    return jsonify(success=True)
