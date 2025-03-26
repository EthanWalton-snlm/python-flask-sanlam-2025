import json

from flask import Blueprint, request

with open("movies.json", "r") as file:
    movies = json.load(file)

movies_bp = Blueprint("movies_bp", __name__)


@movies_bp.get("/")
def get_all_movies():
    return movies


@movies_bp.get("/<id>")
def get_movie_by_id(id):
    for movie in movies:
        if movie["id"] == id:
            return movie

    return {"message": "Movie not found"}, 404


@movies_bp.delete("/<id>")
def delete_movie_by_id(id):
    try:
        movie = get_movie_by_id(id)
        movies.remove(movie)  # type: ignore

        return {"message": f"Movie {id} deleted", "data": movie}, 200
    except ValueError as e:
        print("Error", e)

    return {"message": "Movie not found"}, 404


@movies_bp.post("/")
def create_movie():
    new_movie = request.get_json()

    ids = [int(movie["id"]) for movie in movies]

    new_movie["id"] = f"{max(ids) + 1}"

    movies.append(new_movie)

    return {
        "message": "Movie created successfully",
        "data": new_movie,
    }, 200


@movies_bp.put("/<id>")
def update_movie_by_id(id):
    movie = get_movie_by_id(id)

    body = request.get_json()

    movie.update(body)  # type: ignore

    return {
        "message": "Movie updated successfully",
        "data": movie,
    }, 200
