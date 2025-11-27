from flask_login import UserMixin
from app import login, db
from werkzeug.security import generate_password_hash, check_password_hash
import sqlalchemy as sa
from flask import url_for
from app import db

@login.user_loader
def load_user(id):
    return db.session.get(User, int(id))

class PaginatedAPIMixin(object):
    @staticmethod
    def to_collection_dict(query, page, per_page, endpoint, **kwargs):
        resources = db.paginate(query, page=page, per_page=per_page,
                                error_out=False)
        data = {
            'items': [item.to_dict() for item in resources.items],
            '_meta': {
                'page': page,
                'per_page': per_page,
                'total_pages': resources.pages,
                'total_items': resources.total
            },
            '_links': {
                'self': url_for(endpoint, page=page, per_page=per_page,
                                **kwargs),
                'next': url_for(endpoint, page=page + 1, per_page=per_page,
                                **kwargs) if resources.has_next else None,
                'prev': url_for(endpoint, page=page - 1, per_page=per_page,
                                **kwargs) if resources.has_prev else None
            }
        }
        return data

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True, nullable=False)
    email = db.Column(db.String(120), unique=True, index=True, nullable=False)
    password_hash = db.Column(db.String(256))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
        
    def __repr__(self):
        return f"<User {self.username}>"

class Movie(PaginatedAPIMixin, db.Model):
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    year = db.Column(db.Integer)
    oscars = db.Column(db.Integer)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'year': self.year,
            'oscars': self.oscars,
            '_links': {
                'self': url_for('api.get_movie', id=self.id),
                'collection': url_for('api.get_movies')
            }
        }

    def from_dict(self, data, new_movie=False):
        for field in ['name', 'year', 'oscars']:
            if field in data:
                setattr(self, field, data[field])
