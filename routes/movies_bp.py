from flask import Blueprint, request
from flask_login import login_required

from constants import STATUS_CODE
from extensions import db
from models.movies import Movie

movies_bp = Blueprint("movies_bp", __name__)


@movies_bp.get("/")
@login_required
def get_all_movies():
    movies = Movie.query.all()
    return [movie.to_dict() for movie in movies]


@movies_bp.get("/<id>")
@login_required
def get_movie_by_id(id):
    movie = Movie.query.get(id)

    if movie is None:
        return {"message": "Movie not found"}, STATUS_CODE["NOT_FOUND"]

    return movie.to_dict()


@movies_bp.delete("/<id>")
@login_required
def delete_movie_by_id(id):
    movie = Movie.query.get(id)

    if movie is None:
        return {"message": "Movie not found"}, STATUS_CODE["NOT_FOUND"]

    try:
        db.session.delete(movie)
        db.session.commit()  # actually makes the change

        return {"data": movie.to_dict(), "message": f"Movie {id} deleted successfully."}
    except Exception as e:
        db.session.rollback()  # restores data, cannot be done after commit()
        return {"message": f"{e}"}, STATUS_CODE["SERVER_ERROR"]


@movies_bp.post("/")
@login_required
def create_movie():
    data = request.get_json()
    new_movie = Movie(**data)

    try:
        db.session.add(new_movie)
        db.session.commit()

        return {
            "message": "Movie created successfully",
            "data": new_movie.to_dict(),
        }, STATUS_CODE["CREATED"]
    except Exception as e:
        db.session.rollback()  # restores data, cannot be done after commit()
        return {"message": f"{e}"}, STATUS_CODE["SERVER_ERROR"]


@movies_bp.put("/<id>")
@login_required
def update_movie_by_id(id):
    body = request.get_json()

    try:
        updated = Movie.query.filter_by(id=id).update(body)

        if not updated:
            return {"message": "Movie not found"}, STATUS_CODE["SERVER_ERROR"]

        db.session.commit()

        updated_movie = Movie.query.get(id)
        return {
            "message": f"Updated movie {id}",
            "data": updated_movie.to_dict(),
        } if updated_movie is not None else {"message": "Movie not found"}, STATUS_CODE[
            "SERVER_ERROR"
        ]

    except Exception as e:
        db.session.rollback()  # Undo: Restore the data | After commit cannot undo
        return {"message": str(e)}, STATUS_CODE["SERVER_ERROR"]
