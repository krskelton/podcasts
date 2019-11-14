from sql_alchemy_db_instance import db

class Podcast(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(500))
    rss_feed_url = db.Column(db.String(2000))
