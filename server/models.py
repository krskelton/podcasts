from sql_alchemy_db_instance import db
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), unique=True)
    password = db.Column(db.String(128), nullable=False)
    salt = db.Column(db.String(40), nullable=False)
    user_history = db.relationship('History', backref='users')


class Podcast(db.Model):
    # we want to change the name of this table as it is basically a subscriptions table.
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    name = db.Column(db.String(500))
    rss_feed_url = db.Column(db.String(2000))
    podcast_API_id = db.Column(db.Integer)


class Playlists(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(500))
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))


class PlaylistItems(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    playlist_id = db.Column(db.Integer, db.ForeignKey("playlists.id"))
    podcast_API_id = db.Column(db.Integer)
    episode_id = db.Column(db.Integer)


class History(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    # episode_name : currently storing title in place of unique episode ID
    episode_id = db.Column(db.String)
    # would like to change this to be actual date-time the user clicked on play.
    time_stamp_accessed = db.Column(db.String)
