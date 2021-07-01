from gameover.api.ext.database import db

from .mixins import DateTimeMixin
from .news import News

class Category(DateTimeMixin, db.Model):
    __tablename__ = 'category'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), index=True, nullable=False)

    news = db.relationship(News, backref='category', lazy=True)

    def __repr__(self):
        return f'<Category name({self.name})>'

    def __init__(self, name):
        self.name = name

    def create(self):
        db.session.add(self)

    def update(self, name):
        self.name = name

    def delete(self):
        db.session.delete(self)

    def commit(self):
        db.session.commit()
