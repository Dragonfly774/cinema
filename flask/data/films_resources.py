from flask import jsonify
from flask_restful import abort, Resource, reqparse

from . import db_session
from .films import Films

parser = reqparse.RequestParser()
parser.add_argument('title', required=True)
parser.add_argument('genres', required=True)
parser.add_argument('link_img', required=True)
parser.add_argument('age', required=True)


def abort_if_films_not_found(films_id):
    session = db_session.create_session()
    films = session.query(Films).get(films_id)
    if not films:
        abort(404, message=f"Films {films_id} not found")


class FilmsResource(Resource):
    def get(self, films_id):
        abort_if_films_not_found(films_id)
        session = db_session.create_session()
        films = session.query(Films).get(films_id)
        return jsonify({'films': films.to_dict(
            only=('title', 'genres', 'link_img', 'age'))})

    def delete(self, films_id):
        abort_if_films_not_found(films_id)
        session = db_session.create_session()
        films = session.query(Films).get(films_id)
        session.delete(films)
        session.commit()
        return jsonify({'success': 'OK'})


class FilmsListResource(Resource):
    def get(self):
        session = db_session.create_session()
        films = session.query(Films).all()
        return jsonify({'films': [item.to_dict(
            only=('title', 'genres', 'link_img', 'age')) for item in films]})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        films = Films(
            title=args['title'],
            genres=args['genres'],
            link_img=args['link_img'],
            is_published=args['is_published'],
            age=args['age']
        )
        session.add(films)
        session.commit()
        return jsonify({'success': 'OK'})

