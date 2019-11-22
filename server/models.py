from sql_alchemy_db_instance import db

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), unique=True, nullable=False)
    password = db.Column(db.String(128, nullable=False))
    salt = db.Column(db.String(40), nullable=False)

class Subscriptions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rss_url = db.Column(db.String(2000), nullable=False)

class Favorites(db.Model)


