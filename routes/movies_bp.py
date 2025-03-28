from flask import Blueprint, request

from constants import STATUS_CODE
from extensions import db
from models.movies import Movie

movies_bp = Blueprint("movies_bp", __name__)


@movies_bp.get("/")
def get_all_movies():
    movies = Movie.query.all()
    return [movie.to_dict() for movie in movies]


@movies_bp.get("/<id>")
def get_movie_by_id(id):
    movie = Movie.query.get(id)

    if movie is None:
        return {"message": "Movie not found"}, STATUS_CODE["NOT_FOUND"]

    return movie.to_dict()


@movies_bp.delete("/<id>")
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


# TODO
@movies_bp.put("/<id>")
def update_movie_by_id(id):
    movie = get_movie_by_id(id)

    body = request.get_json()

    movie.update(body)  # type: ignore

    return {
        "message": "Movie updated successfully",
        "data": movie,
    }, 200
