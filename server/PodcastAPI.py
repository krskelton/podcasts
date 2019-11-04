from flask import Blueprint, jsonify, request
from sql_alchemy_db_instance import db
from models import Podcast

podcast_api = Blueprint('podcast_api', __name__)

@podcast_api.route('/subscriptions', methods=['GET'])
def serve_all_subscriptions():
    podcast_instances = db.session.query(Podcast).all()
    # podcast_items = [{"id": podcast.id, "name": podcast.name, "rss_feed_url": podcast.rss_feed_url, "podcast_id": podcast.podcast_id} for podcast in podcast_instances]
    # return jsonify({"name": podcast_items, "rss_feed_url": podcast_items, "podcast_id": podcast_items})
    podcast_items = [{"id": podcast.id, "name": podcast.name, "rss_feed_url": podcast.rss_feed_url} for podcast in podcast_instances]
    return jsonify({"name": podcast_items})

@podcast_api.route('/subscription', methods=['POST'])
def add_subscription():
    new_podcast = Podcast()
    new_podcast.name = request.json["name"]
    new_podcast.rss_feed_url = request.json["rss_feed_url"]
    # new_podcast.podcast_id = request.json["podcast_id"]
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
