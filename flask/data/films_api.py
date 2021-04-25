import flask
from flask import jsonify, request
from . import db_session
from .films import Films

blueprint = flask.Blueprint(
    'films_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/films')
def get_films():
    db_sess = db_session.create_session()
    films = db_sess.query(Films).all()
    return jsonify(
        {
            'films':
                [item.to_dict(only=('title', 'genres', 'link_img', 'age'))
                 for item in films]
        }
    )


@blueprint.route('/api/films/<int:films_id>', methods=['GET'])
def get_one_films(films_id):
    db_sess = db_session.create_session()
    films = db_sess.query(Films).get(films_id)
    if not films:
        return jsonify({'error': 'Not found'})
    return jsonify(
        {
            'films': films.to_dict(only=(
                'title', 'genres', 'link_img', 'age'))
        }
    )


@blueprint.route('/api/films', methods=['POST'])
def create_films():
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in
                 ['title', 'genres', 'link_img', 'age']):
        return jsonify({'error': 'Bad request'})
    db_sess = db_session.create_session()
    films = Films(
        title=request.json['title'],
        genres=request.json['genres'],
        link_img=request.json['link_img'],
        age=request.json['age']
    )
    db_sess.add(films)
    db_sess.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/films/<int:films_id>', methods=['DELETE'])
def delete_films(films_id):
    db_sess = db_session.create_session()
    films = db_sess.query(Films).get(films_id)
    if not films:
        return jsonify({'error': 'Not found'})
    db_sess.delete(films)
    db_sess.commit()
    return jsonify({'success': 'OK'})
