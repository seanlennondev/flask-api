from gameover.api.ext.database import db

from .mixins import DateTimeMixin

class News(DateTimeMixin, db.Model):
    __tablename__ = 'news'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), index=True, nullable=False)
    subtitle = db.Column(db.String(100), index=True, nullable=False)
    content = db.Column(db.String, nullable=False)
    image = db.Column(db.String, nullable=True)
    author = db.Column(db.String(200), index=True, nullable=False)

    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
