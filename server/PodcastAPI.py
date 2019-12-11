from flask import Blueprint, jsonify, request, session
from sql_alchemy_db_instance import db
from models import Podcast, Users, PlaylistItems, Playlists, History
import requests
from sqlalchemy import func

podcast_api = Blueprint('podcast_api', __name__)


@podcast_api.route('/subscriptions', methods=['GET'])
def serve_all_subscriptions():
    podcast_instances = db.session.query(Podcast).all()
    # needs to reference each user_in_session so that only user's subscriptions are shown
    podcast_items = [{"id": podcast.id, "name": podcast.name, "user_id": podcast.user_id,
                      "rss_feed_url": podcast.rss_feed_url} for podcast in podcast_instances]
    return jsonify({"name": podcast_items})


@podcast_api.route('/subscription', methods=['POST'])
def add_subscription():
    new_podcast = Podcast()
    user_in_session = session['user']
    username = db.session.query(Users).filter(
        Users.username == user_in_session).first()
    new_podcast.user_id = username.id
    new_podcast.name = request.json["name"]
    new_podcast.rss_feed_url = request.json["rss_feed_url"]
    db.session.add(new_podcast)
    db.session.commit()
    return jsonify(success=True)


@podcast_api.route('/subscription', methods=['PATCH'])
def remove_subscription():
    pod_id = request.json["id"]
    target_podcast = db.session.query(Podcast).filter_by(id=pod_id).first()
    db.session.delete(target_podcast)
    db.session.commit()
    return jsonify(success=True)

# The request to the iTunes API to get the RSS feed is made here because of an error with some podcasts returning html instead of XML. Here we can set the Headers so that we only get an XMLHttpRequest reponse, which is what we need in order for the rss-parser library to parse the response in Podcast.vue.
@podcast_api.route('/itunes-api', methods=['POST'])
def get_feed():
    rss_feed = request.json["rss_feed"]
    podcast_info = requests.get("https://cors-anywhere.herokuapp.com/" +
                                rss_feed, headers={"X-Requested-With": "XMLHttpRequest"})
    return podcast_info.content
