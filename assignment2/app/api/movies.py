import sqlalchemy as sa
from flask import request
from app import db
from app.api import bp
from app.api.errors import bad_request
from app.api.auth import token_auth
from app.models import Movie

@bp.route('/movies/<int:id>', methods=['GET'])
@token_auth.login_required
def get_movie(id):
    return db.get_or_404(Movie, id).to_dict()

@bp.route('/movies', methods=['GET'])
@token_auth.login_required
def get_movies():
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)

    query = sa.select(Movie).order_by(Movie.name)
    return Movie.to_collection_dict(query, page, per_page, 'api.get_movies')

@bp.route('/movies', methods=['POST'])
@token_auth.login_required
def create_movie():
    data = request.get_json() or {}
    if 'name' not in data:
        return bad_request('Movie must have a name.')

    movie = Movie()
    movie.from_dict(data, new_movie=True)
    db.session.add(movie)
    db.session.commit()

    return movie.to_dict(), 201

@bp.route('/movies/<int:id>', methods=['PUT'])
@token_auth.login_required
def update_movie(id):
    movie = db.get_or_404(Movie, id)
    data = request.get_json() or {}
    movie.from_dict(data)
    db.session.commit()
    return movie.to_dict()

@bp.route('/movies/<int:id>', methods=['DELETE'])
@token_auth.login_required
def delete_movie(id):
    movie = db.get_or_404(Movie, id)
    db.session.delete(movie)
    db.session.commit()
    return '', 204